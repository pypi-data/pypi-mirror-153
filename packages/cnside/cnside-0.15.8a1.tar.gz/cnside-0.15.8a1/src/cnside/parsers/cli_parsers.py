import abc
import argparse
from typing import List, Text, Union

from cnside import metadata
from cnside.objects.core import UnifiedPackageID, PYPIPackage, NPMPackage, GenericPackage

__all__ = ["PackageParamType", "CLIPackageNameParam", "CLIParser", "PIPInstallParser", "NPMInstallParser",
           "YarnInstallParser"]


class PackageParamType:
    UPID = "UPID"
    MANIFEST = "MANIFEST"


class CLIPackageNameParam:
    def __init__(self, data: Union[UnifiedPackageID, Text], typ: Text):
        self.data = data
        self.typ = typ


class CLIParser(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def packages(self) -> List[CLIPackageNameParam]:
        raise NotImplementedError()


class PIPInstallParser(CLIParser):
    def __init__(self, arguments: List[Text]):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--requirement')
        parser.add_argument('-c', '--constraint')
        parser.add_argument('--no-deps', action='store_true')
        parser.add_argument('--pre', action='store_true')
        parser.add_argument('-e', '--editable')
        parser.add_argument('-t', '--target')
        parser.add_argument('--platform')
        parser.add_argument('--python-version')
        parser.add_argument('--implementation')
        parser.add_argument('--abi')
        parser.add_argument('--user', action='store_true')
        parser.add_argument('--root')
        parser.add_argument('--prefix')
        parser.add_argument('--src')
        parser.add_argument('-U', '--upgrade', action='store_true')
        parser.add_argument('--upgrade-strategy')
        parser.add_argument('--force-reinstall', action='store_true')
        parser.add_argument('-I', '--ignore-installed', action='store_true')
        parser.add_argument('--ignore-requires-python', action='store_true')
        parser.add_argument('--no-build-isolation', action='store_true')
        parser.add_argument('--use-pep517', action='store_true')
        parser.add_argument('--install-option')
        parser.add_argument('--global-option')
        parser.add_argument('--compile', action='store_true')
        parser.add_argument('--no-compile', action='store_true')
        parser.add_argument('--no-warn-script-location', action='store_true')
        parser.add_argument('--no-warn-conflicts', action='store_true')
        parser.add_argument('--no-binary')
        parser.add_argument('--only-binary')
        parser.add_argument('--prefer-binary', action='store_true')
        parser.add_argument('--require-hashes', action='store_true')
        parser.add_argument('--progress-bar')
        parser.add_argument('--no-clean', action='store_true')
        parser.add_argument('-i', '--index-url')
        parser.add_argument('--extra-index-url')
        parser.add_argument('--no-index', action='store_true')
        parser.add_argument('-f', '--find-links')
        parser.add_argument('--isolated', action='store_true')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-V', '--version', action='store_true')
        parser.add_argument('-q', '--quiet', action='store_true')
        parser.add_argument('--log')
        parser.add_argument('--no-input', action='store_true')
        parser.add_argument('--proxy')
        parser.add_argument('--retries')
        parser.add_argument('--timeout')
        parser.add_argument('--exists-action')
        parser.add_argument('--trusted-host')
        parser.add_argument('--cert')
        parser.add_argument('--client-cert')
        parser.add_argument('--cache-dir')
        parser.add_argument('--no-cache-dir', action='store_true')
        parser.add_argument('--disable-pip-version-check', action='store_true')
        parser.add_argument('--no-color', action='store_true')
        parser.add_argument('--no-python-version-warning', action='store_true')
        parser.add_argument('--use-feature')
        parser.add_argument('--use-deprecated')
        parser.add_argument('packages', nargs=argparse.REMAINDER)

        self.args = parser.parse_args(arguments)

    @property
    def packages(self) -> List[CLIPackageNameParam]:
        rv = []

        if not self.args.packages:
            rv.append(CLIPackageNameParam(data=self.args.requirement, typ=PackageParamType.MANIFEST))
        else:
            for p in self.args.packages:
                rv.append(CLIPackageNameParam(data=PYPIPackage(p).upid, typ=PackageParamType.UPID))

        return rv


class NPMInstallParser(CLIParser):
    def __init__(self, arguments: List[Text]):
        """
        ---------------------------------------------------------------------------------------
        npm install (with no args, in package dir)
        npm install [<@scope>/]<pkg>
        npm install [<@scope>/]<pkg>@<tag>
        npm install [<@scope>/]<pkg>@<version>
        npm install [<@scope>/]<pkg>@<version range>
        npm install <alias>@npm:<name>
        npm install <folder>
        npm install <tarball file>
        npm install <tarball url>
        npm install <git:// url>
        npm install <github username>/<github project>

        aliases: i, isntall, add
        common options: [--save-prod|--save-dev|--save-optional] [--save-exact] [--no-save]
        ---------------------------------------------------------------------------------------

        :param arguments:
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--save-prod", action="store_true")
        parser.add_argument("--save-dev", action="store_true")
        parser.add_argument("--save-optional", action="store_true")
        parser.add_argument("--save-exact", action="store_true")
        parser.add_argument("--no-save", action="store_true")
        parser.add_argument("packages", nargs=argparse.REMAINDER)

        self.args = parser.parse_args(arguments)

    @property
    def packages(self) -> List[CLIPackageNameParam]:
        rv = []

        # TODO: https://gitlab.com/illustria/cnside-cli/-/issues/1
        if not self.args.packages:
            rv.append(CLIPackageNameParam(data=metadata.packages.ManifestNames.NPM, typ=PackageParamType.MANIFEST))
        else:
            for p in self.args.packages:
                rv.append(CLIPackageNameParam(data=NPMPackage(p).upid, typ=PackageParamType.UPID))

        return rv


class YarnInstallParser(CLIParser):
    def __init__(self, arguments: List[Text]):
        parser = argparse.ArgumentParser()
        parser.add_argument("packages", nargs=argparse.REMAINDER)

        self.args = parser.parse_args(arguments)

    @property
    def packages(self) -> List[CLIPackageNameParam]:
        rv = []

        if not self.args.packages:
            rv.append(CLIPackageNameParam(data=metadata.packages.ManifestNames.NPM, typ=PackageParamType.MANIFEST))
        else:
            for p in self.args.packages:
                rv.append(
                    CLIPackageNameParam(
                        data=GenericPackage(package=p, package_manager=metadata.packages.PackageManagers.NPM).upid,
                        typ=PackageParamType.UPID
                    )
                )

        return rv
