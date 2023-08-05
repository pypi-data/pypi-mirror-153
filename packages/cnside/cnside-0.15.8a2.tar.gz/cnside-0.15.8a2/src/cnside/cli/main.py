#!/usr/bin/env python
import argparse
import logging
import os
import random
import sys
import tempfile
import time
from pathlib import Path
from typing import Text, Tuple, List, Optional

import click
import progressbar
from pydantic import BaseModel

from cnside import metadata, errors
from cnside.authenticator import Authenticator, AuthenticatorConfig, OAUTHToken
from cnside.cli import APIClient, APIClientConfig
from cnside.cli.api import ConfigFile
from cnside.cli.core import PrintColors, execute_cli_parsed_command, execute_subprocess_popen_command
from cnside.cli.documents import AnalyzeRequestDoc, CLIParsedCommand
from cnside.errors import FailedToLoadToken, FailedToRefreshToken, LockfileNotFoundError, ManifestNotFoundError, \
    LockfileGenerateFailed, TerminateRequest, FailedPackageResolution, FailedSwitchYarnVersion
from cnside.storage import StorageHandlerConfig, StorageHandler
from cnside.storage.handlers import ManifestData
from packaging import version as pv


class Joker:
    def __init__(self):
        self.colors = PrintColors()

    def ill_let_myself_out(self):
        if not random.randint(0, 1000):
            time.sleep(1)
            self.colors.point_warning("ENCRYPTING ALL YOUR COMPUTER FILES!")
            time.sleep(3)
            self.colors.point_fail("SYKE!!! THE FILE ENCRYPTION MODE IS DISABLED. 😑")
            time.sleep(1)
            self.colors.point("TIP: To enable file encryption mode run 'cnside --enable-encrypt-my-file'")


class Messages:
    LOGGED_IN = ""
    LOGGED_OUT = ""
    TOKEN_LOAD_FAILED = "Failed to load token."
    AUTH_REQUIRED = "Authentication required. Please run: 'cnside illustria auth'."
    UNHANDLED_AUTH_ERROR = "Unhandled authentication error."
    UNHANDLED_REQUEST_ERROR = "Unhandled package request error."
    LIBRARY_REJECTED = "LIBRARY REJECTED"
    LIBRARY_APPROVED = "LIBRARY APPROVED"
    FAILED_REFRESH_TOKEN = "Failed to refresh authentication token."


class CLIConfig(BaseModel):
    cnside_base_url: Text = "https://cnside.illustria.io"
    cnside_npm_repo: Text = "https://repo.illustria.io/repository/cnside_npm_hosted/"
    cnside_pypi_repo: Text = "https://repo.illustria.io/repository/cnside_pypi_hosted/simple"
    auth_url: Text = "https://illustria.frontegg.com/oauth/authorize"
    token_url: Text = "https://illustria.frontegg.com/oauth/token"
    client_id: Text = "cf890130-015c-41b0-bd3d-ea03fa393b41"
    # max_attempts: Optional[int] = 500
    request_interval: Optional[int] = 3


class CLIInterface:
    def __init__(self, config: CLIConfig, logging_level: int = None):
        self.logger = PrintColors(level=logging_level)
        self.config = config

        self.storage_handler = StorageHandler(StorageHandlerConfig())
        self.authenticator = Authenticator(
            config=AuthenticatorConfig(auth_url=config.auth_url, token_url=config.token_url,
                                       storage_handler=self.storage_handler, client_id=self.config.client_id)
        )

        self._npm_lockfile_generate_command = ["npm", "i", "--package-lock-only"]
        self._v2_package_managers = [
            metadata.packages.PackageManagers.NPM,
            metadata.packages.PackageManagers.YARN
        ]

    def parse_cli_arguments(self) -> CLIParsedCommand:
        """
        Provides script interface for end user.

        """
        # todo: build a hierarchical parser for all commands
        parser = argparse.ArgumentParser(description="cnside (see-inside) is the secure package manager wrapper by "
                                                     "illustria. for more information please visit "
                                                     "https://illustria.io.")
        parser.add_argument("--skip-install", help="Skip installation when package approved", action='store_true')
        parser.add_argument("--examine-all", help="Examine the whole lockfile and not only diffs", action='store_true')
        parser.add_argument("--generate-lockfile", help="Auto generate lockfile if needed", action='store_true')
        parser.add_argument("--debug", help="output debug information", action='store_true')
        parser.add_argument("manager", help="package manager (supported: pip, npm, illustria)")
        parser.add_argument("action", help="action (install, auth)")
        parser.add_argument('arguments', nargs=argparse.REMAINDER)
        # parser.add_argument('-v', '--version', action='version', version='')
        args = parser.parse_args()
        cli_command = CLIParsedCommand(package_manager=args.manager, action=args.action, arguments=args.arguments,
                                       skip_install=args.skip_install, examine_all=args.examine_all,
                                       generate_lockfile=args.generate_lockfile)
        if args.debug:
            self.logger = PrintColors(level=logging.DEBUG)

        return cli_command

    def _get_project_name(self, package_manager: Text, manifest_exists: bool = False) -> Text:
        project_name = None

        if package_manager in self._v2_package_managers:
            stdout, stderr = execute_subprocess_popen_command(["npm", "run", "env"])
            for i in stdout:
                if i.startswith("npm_package_name"):
                    project_name = i.strip("\n").split("=")[1]
        else:
            project_name = Path(os.getcwd()).name if manifest_exists else None

        return project_name

    def run(self, command: CLIParsedCommand):
        skip_install: bool = command.skip_install
        examine_all: bool = command.examine_all

        if command.package_manager == "illustria":
            index = {
                "auth": self.authenticator.authenticate
            }
            index[command.action]()
        else:
            # Analyze
            # self.analyze_environment(command=command)

            # Preprocess Dependency Tree
            data, resolved_data = self.preprocess_package_resolution(command=command)

            # Set request variables
            analyzer_version = 2 if command.package_manager in self._v2_package_managers else 1

            # get project name
            project_name = self._get_project_name(
                package_manager=command.package_manager,
                manifest_exists=bool(data.manifest)
            )

            # Generate request documents and request from illustria
            # TODO: set project name: https://gitlab.com/illustria/cnside-cli/-/issues/6
            request_document = AnalyzeRequestDoc(
                package_manager=command.package_manager,
                packages=command.packages,
                install_manifest=command.install_manifest,
                manifest=data.manifest,
                lockfile=data.lockfile,
                resolved_lockfile=resolved_data.lockfile,
                analyzer_version=analyzer_version,
                project=project_name
            )

            if examine_all:
                request_document.lockfile = None

            approved, failed_checks = self.request_packages(request_document=request_document)

            if approved:
                self.logger.point_ok(Messages.LIBRARY_APPROVED)
            else:
                self.logger.point("Issues Found:")
                for i in failed_checks:
                    if i:
                        for b in i:
                            self.logger.point(
                                f"{b['upid_str']} - "
                                f"{b['policy_id'].split('-')[0]} - "
                                f"{b['policy_category']} - "
                                f"{b['policy_rule_id']} - "
                                f"{b['failed_labels']}"
                            )

                self.logger.point_fail(Messages.LIBRARY_REJECTED)

            self.logger.header("Installation")
            if skip_install:
                self.logger.point("Skipping Installation (--skip_install)")
            else:
                install = click.confirm("[Q] Would you like to install packages?", default=True if approved else False)

                if install:
                    self.logger.point("Installing packages (Using package manager).")
                    std_out, std_err = execute_cli_parsed_command(command=command)
                    self.logger.point("Package manager output:")
                    for line in std_out:
                        self.logger.out_data(line)

                    for line in std_err:
                        self.logger.err_data(line)

                    self.logger.point_ok("INSTALLED. (Please Verify Output)")
                else:
                    self.logger.point("Skipping installation.")
                    self.logger.point_fail("INSTALL ABORTED")

            self.logger.footer("FINISHED")

    def gen_api_client(self):
        token = self.load_token()
        config_file = self.load_config_file()
        config = APIClientConfig(
            base_url=self.config.cnside_base_url,
            headers={"Authorization": f"{token.token_type} {token.access_token}"},
            proxy=config_file.proxy
        )
        api_client = APIClient(config=config)
        return api_client

    def _generate_npm_package_lock_json(self):

        _, std_err = execute_subprocess_popen_command(command=self._npm_lockfile_generate_command)
        if std_err:
            raise LockfileGenerateFailed(
                command=self._npm_lockfile_generate_command,
                suggestion=["npm", "i", "--package-lock-only", "--legacy-peer-deps"],
                caution="If install command is needed to solve the issue, make sure to skip download by appending "
                        "'--package-lock-only' to the command.",
                std_err=std_err
            )

    def _generate_lock_file(self, package_manager: Text):
        generators_index = {
            metadata.packages.PackageManagers.NPM: self._generate_npm_package_lock_json,
            metadata.packages.PackageManagers.YARN: self._generate_npm_package_lock_json,
        }

        generators_index[package_manager]()

    @staticmethod
    def _ll_get_yarn_version(project_dir: Text) -> pv.Version:
        yarn_version_command = ["yarn", "--version"]
        std_out, std_err = execute_subprocess_popen_command(yarn_version_command, cwd=project_dir)
        if std_out:
            yarn_version = pv.parse("".join(std_out).replace("\n", ""))
        else:
            raise ValueError("Failed to get yarn version.")

        return yarn_version

    def _ll_switch_yarn_version(self, project_dir: Text, target_version: Text):
        self.logger.debug(f"Updating yarn version to {target_version}")
        yarn_switch_version_command = ["yarn", "set", "version", target_version]
        std_out, std_err = execute_subprocess_popen_command(yarn_switch_version_command, cwd=project_dir)
        self.logger.debug("".join(std_out))
        self.logger.debug("".join(std_err))

        yarn_version = self._ll_get_yarn_version(project_dir=project_dir)
        if not yarn_version == pv.parse(target_version):
            raise FailedSwitchYarnVersion("Failed to switch yarn version")

    def _switch_yarn_version(self, temp_dir_path: Text):
        self.logger.debug("Switching local yarn version for dependency resolution")
        stable_yarn_v1_version = "1.22.17"
        stable_yarn_v3_version = "3.2.0"

        self.logger.debug("Creating local .yarnrc[.yml] files")
        open(os.path.join(temp_dir_path, ".yarnrc"), "w+").close()
        open(os.path.join(temp_dir_path, ".yarnrc.yml"), "w+").close()

        # switching to a stable v1 version, to prevent any bugs with `yarn set version`.
        if not self._ll_get_yarn_version(project_dir=temp_dir_path) >= pv.parse(stable_yarn_v1_version):
            self._ll_switch_yarn_version(project_dir=temp_dir_path, target_version=stable_yarn_v1_version)

        # switching to yarn v3 version for dependency resolution.
        self._ll_switch_yarn_version(project_dir=temp_dir_path, target_version=stable_yarn_v3_version)

    def _copy_npmrc_and_yarnrc_file(self, dest_dir: Text):
        npmrc_file_path = os.path.expanduser("~/.npmrc")
        npmrc_file = Path(npmrc_file_path)
        if npmrc_file.exists():
            self.logger.debug(f"Copying .~/.npmrc to {dest_dir}")
            copy_npmrc_command = ["cp", npmrc_file_path, dest_dir]
            std_out, std_err = execute_subprocess_popen_command(copy_npmrc_command, cwd=dest_dir)
            self.logger.debug("".join(std_out))
            self.logger.debug("".join(std_err))

        yarnrc_file_path = os.path.expanduser("~/.yarnrc")
        yarnrc_file = Path(yarnrc_file_path)
        if yarnrc_file.exists():
            self.logger.debug(f"Copying .~/.yarnrc to {dest_dir}")
            copy_yarnrc_command = ["cp", yarnrc_file_path, dest_dir]
            std_out, std_err = execute_subprocess_popen_command(copy_yarnrc_command, cwd=dest_dir)
            self.logger.debug("".join(std_out))
            self.logger.debug("".join(std_err))

    def _npm_or_yarn_temp_dir_package_resolution(self, data: ManifestData, command: CLIParsedCommand) -> ManifestData:
        with tempfile.TemporaryDirectory(prefix="cnside_") as temp_dir_path:
            self.logger.debug(f"Temporary directory: {temp_dir_path}")

            self._copy_npmrc_and_yarnrc_file(dest_dir=temp_dir_path)

            install_commands = {
                metadata.packages.PackageManagers.NPM: ["npm", "i", "--package-lock-only"],
                metadata.packages.PackageManagers.YARN: ["yarn", "add", "--mode", "update-lockfile"]
            }

            init_command = ["npm", "init", "-y"]
            install_command = install_commands[command.package_manager]

            manifest_path = os.path.join(temp_dir_path, metadata.packages.ManifestNames.get(command.package_manager))
            lockfile_path = os.path.join(temp_dir_path, metadata.packages.LockfileNames.get(command.package_manager))

            # Building the installation command
            for upid in command.packages:
                install_command.append(upid.pm_repr())

            # Saving manifest and lockfile if they exist or generating them if needed.
            if data.manifest:
                with open(manifest_path, "w+") as fp:
                    fp.write(data.manifest)
            else:
                execute_subprocess_popen_command(init_command, cwd=temp_dir_path)

            if data.lockfile:
                with open(lockfile_path, "w+") as fp:
                    fp.write(data.lockfile)

            # Resolving tree without downloading packages
            if command.package_manager == metadata.packages.PackageManagers.YARN:
                self._switch_yarn_version(temp_dir_path=temp_dir_path)

            std_out, std_err = execute_subprocess_popen_command(install_command, cwd=temp_dir_path)
            self.logger.debug("".join(std_out))
            self.logger.debug("".join(std_err))

            # evaluating results
            if std_out:
                if "Errors happened when preparing the environment required to run this command" in std_out[-1]:
                    raise FailedPackageResolution("".join(std_out))

            resolved_data = self.storage_handler.manifest.get(package_manager=command.package_manager,
                                                              base_dir=temp_dir_path)

            # Instead of validating Popen output we just make sure that the files have been generated.
            # TODO: turn into a custom error.
            assert all([resolved_data.manifest, resolved_data.lockfile]), "Failed to resolve dependencies"

        return resolved_data

    def preprocess_package_resolution(self, command: CLIParsedCommand) -> Tuple[ManifestData, ManifestData]:
        """
        Resolves the tree for analyzer version 2 package managers.

        :param command:
        :return:
        """

        try:
            self.logger.header("Resolving Dependency Tree")
            data = self.storage_handler.manifest.get(package_manager=command.package_manager)

            if command.package_manager in self._v2_package_managers:
                self.logger.point("Using: Temporary directory for dependency resolution.")
                # Create temp directory, save the manifest and lockfile in there, resolve the tree and request it.
                resolved_data = self._npm_or_yarn_temp_dir_package_resolution(data=data, command=command)
            else:
                resolved_data = data

            self.logger.point_ok("Dependency Tree Resolved!")
        except FailedSwitchYarnVersion as e:
            self.logger.point_fail(e)
            sys.exit(1)
        except FailedPackageResolution as e:
            self.logger.point_fail("Failed to resolve dependencies (Incorrect package name or version?)")
            self.logger.err_data("Details:\n" + str(e))
            sys.exit(1)

        return data, resolved_data

    def analyze_environment(self, command: CLIParsedCommand):
        self.logger.header("Analyzing Command & Environment")
        try:
            # Load and evaluate manifest and lockfile data. They both must exist for package resolution to work
            # correctly when requesting a package from illustria cloud in analyzer_mode version 2. In order to
            # prevent any package name or version discrepancy between what illustria is checking and what the client
            # is receiving, the whole package resolution must happen within the client itself. This is done by
            # generating a lockfile is a manifest file exists.
            manifest_data = self.storage_handler.manifest.get(package_manager=command.package_manager)

            # validating that the manifest exists if the user asked to install it.
            if command.install_manifest and not manifest_data.manifest:
                raise ManifestNotFoundError(
                    f"Manifest install requested but no manifest file found ({manifest_data.manifest_name}).")

            # Setting lockfile_exists as true for package managers that have no lockfile.
            lockfile_exists = True \
                if command.package_manager in metadata.packages.LockfileNames.non_lockfile_managers() \
                else manifest_data.lockfile

            # Generating a lockfile if there is a manifest and the lockfile doesn't exist - with users' permission.
            if all([manifest_data.manifest, not lockfile_exists]):
                self.logger.point_warning_prefix(f"Lockfile not found: {manifest_data.lockfile_name}")
                self.logger.point("Lockfile needed to continue...")
                if command.generate_lockfile:
                    gen_lockfile = True
                else:
                    gen_lockfile = click.confirm(
                        f"[Q] Would you like us to generate a lockfile for you? ({manifest_data.lockfile_name})",
                        default=True)

                if gen_lockfile:
                    try:
                        self.logger.point("Generating a lock file...")
                        self._generate_lock_file(command.package_manager)
                        self.logger.point("Lockfile generated!")
                    except LockfileGenerateFailed as e:
                        self.logger.point_fail(
                            f"Error: Failed to generate a lockfile, using this command: '{' '.join(e.command)}'")
                        for line in e.std_err:
                            self.logger.err_data(line)
                        self.logger.point_warning(f"NOTICE!: {e.caution}")
                        sys.exit()
                else:
                    self.logger.point_warning(
                        "Caution: Generating a lockfile by yourself might result in packages being downloaded. It "
                        "is best to let us do it for you.")
                    raise LockfileNotFoundError()

            self.logger.point_ok("Command & Environment OK!")

        except (ManifestNotFoundError, LockfileNotFoundError) as e:
            self.logger.point_fail_prefix(f"Error: {e}")
            sys.exit()
        except Exception as e:
            raise e

        return manifest_data

    def request_packages(self, request_document: AnalyzeRequestDoc) -> Tuple[bool, List]:
        try:
            self.logger.header("Requesting packages from CNSIDE System")
            # generating request document

            api_client = self.gen_api_client()

            self.logger.point(f"Analyzer Version: {request_document.analyzer_version}")
            if request_document.analyzer_version == 1:
                self.logger.point(f"Packages: {request_document.packages}")

            try:
                # requesting to analyze package
                try:
                    analyze_response_doc = api_client.post_analyze_request(request_document=request_document)
                except errors.api.TokenExpired:
                    api_client.close()

                    try:
                        token = self.authenticator.load_token()
                        token = self.authenticator.refresh_token(token=token)
                        self.storage_handler.token.save(token)
                    except FailedToRefreshToken:
                        self.logger.point_fail(Messages.FAILED_REFRESH_TOKEN)
                        self.logger.point_fail(Messages.AUTH_REQUIRED)
                        sys.exit()

                    api_client = self.gen_api_client()
                    analyze_response_doc = api_client.post_analyze_request(request_document=request_document)

                # handling check status
                # todo: https://gitlab.com/illustria/cnside-cli/-/issues/9
                workflow_id = analyze_response_doc.workflow_id

                approved = False
                failed_checks = []

                finished = False
                bar_initiated = False
                bar: progressbar.ProgressBar

                self.logger.point("Waiting for request analysis (this might take a few seconds)")
                while not finished:
                    time.sleep(self.config.request_interval)

                    data = api_client.get_analyze_status(workflow_id=workflow_id)
                    if data.status == "PROCESSING":
                        if not bar_initiated:
                            self.logger.point(f"Total packages requested: {data.total_packages}")
                            self.logger.point(f"New packages to process: {data.new_packages}")
                            self.logger.point("Processing...")
                            bar = progressbar.ProgressBar(
                                maxval=data.total_stages,
                                widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()],
                                fd=sys.stdout
                            )
                            bar.start()
                            bar_initiated = True

                        # noinspection PyUnboundLocalVariable
                        bar.update(data.total_stages - data.remaining_stages)
                    if data.status == "COMPLETED":
                        if bar_initiated:
                            bar.update(data.total_stages - data.remaining_stages)
                            bar.finish()
                        approved = data.accepted
                        failed_checks = data.failed_checks
                        finished = True

                api_client.close()

                return approved, failed_checks

            except errors.api.RemoteServerError as e:
                self.logger.point_fail(f"Error: Remote Server Error:\n\tStatus Code: {e.data.status_code}")
                raise TerminateRequest()
            except Exception as e:
                raise e
            finally:
                api_client.close()

        except (KeyboardInterrupt, TerminateRequest):
            sys.exit()
        except Exception as e:
            self.logger.point_fail(Messages.UNHANDLED_REQUEST_ERROR)
            self.logger.point_fail(e)
            sys.exit()

    def load_token(self) -> OAUTHToken:
        try:
            token = self.authenticator.load_token()
        except FailedToLoadToken:
            self.logger.point_fail(Messages.TOKEN_LOAD_FAILED)
            self.logger.point_fail(Messages.AUTH_REQUIRED)
            sys.exit()
        except Exception as e:
            self.logger.point_fail(Messages.UNHANDLED_AUTH_ERROR)
            self.logger.point_fail(e)
            sys.exit()

        return token

    def load_config_file(self) -> ConfigFile:
        try:
            return ConfigFile(**self.storage_handler.config.load())
        except FileNotFoundError:
            self.logger.debug("Config file not found. Creating empty config file")
            config_file = ConfigFile()
            self.storage_handler.config.save(config_file.dict())
            return config_file


def main():
    cli_interface = CLIInterface(config=CLIConfig())
    command = cli_interface.parse_cli_arguments()
    cli_interface.run(command=command)


# todo: add report error functionality - when error happens
# todo: save to config file


if __name__ == '__main__':
    main()
