from typing import Text, List, Optional, Dict

from pydantic import BaseModel

from cnside import metadata
from cnside.documents.base import RequestDocument
from cnside.errors import UnsupportedPackageManager, UnsupportedAction
from cnside.objects.core import UnifiedPackageID

__all__ = ["AnalyzeRequestDoc", "AnalyzeResponseDoc", "CLIParsedCommand"]

# API Documents
from cnside.parsers import PIPInstallParser, NPMInstallParser, CLIPackageNameParam, PackageParamType, YarnInstallParser


class AnalyzeRequestDoc(RequestDocument):
    __version__ = "2.1.1"
    __doc_type__ = "analyze_request_document"

    def __init__(self, package_manager: Text, packages: List[UnifiedPackageID] = None, install_manifest: bool = None,
                 manifest: Text = None, lockfile: Text = None, resolved_lockfile: Text = None,
                 project: Text = None, analyzer_version: int = None):

        super().__init__()
        if package_manager == metadata.packages.PackageManagers.PIP:
            self.package_manager = metadata.packages.PackageRepositories.PYPI
        else:
            self.package_manager = package_manager

        self.project = "default" if not project else project

        self.packages = packages
        self.install_manifest = False if not install_manifest else install_manifest
        self.manifest = manifest
        self.lockfile = lockfile
        self.resolved_lockfile = resolved_lockfile
        self.analyzer_version = 1 if not analyzer_version else analyzer_version

        if self.install_manifest:
            assert all([self.manifest, any([self.lockfile, self.resolved_lockfile])]), \
                "manifest param is required when install_manifest param is set"


class AnalyzeResponseDoc(BaseModel):
    workflow_id: Text
    status: Text
    total_packages: int
    new_packages: int
    total_stages: int
    remaining_stages: int
    failed_checks: Optional[List[List[Dict]]]  # should have a data model instead of Dict
    accepted: Optional[bool]


# CLI Documents

class CLIParsedCommand:
    def __init__(self, package_manager: Text, action: Text, arguments: List, skip_install: bool = None,
                 examine_all: bool = None, generate_lockfile: bool = None):
        self.package_manager = package_manager
        self.action = action
        self.arguments = arguments
        self.skip_install = False if not skip_install else True
        self.examine_all = False if not examine_all else True
        self.generate_lockfile = False if not generate_lockfile else True

        self._packages = []
        self._install_manifest = False

        if not self.package_manager == "illustria":
            self._validate_command()
            self._digest()

    def _validate_command(self):
        supported_package_managers = metadata.packages.PackageManagers.to_list()
        supported_actions = ["install", "i", "add"]

        if self.package_manager not in supported_package_managers:
            raise UnsupportedPackageManager(self.package_manager)

        if self.action not in supported_actions:
            raise UnsupportedAction(self.action)

        return True

    def _extract_pip_packages(self) -> List[CLIPackageNameParam]:
        parser = PIPInstallParser(self.arguments)
        return parser.packages

    def _extract_npm_packages(self) -> List[CLIPackageNameParam]:
        parser = NPMInstallParser(self.arguments)
        return parser.packages

    def _extract_yarn_packages(self) -> List[CLIPackageNameParam]:
        parser = YarnInstallParser(self.arguments)
        return parser.packages

    def _digest(self):
        extractors = {
            metadata.packages.PackageManagers.PIP: self._extract_pip_packages,
            metadata.packages.PackageManagers.NPM: self._extract_npm_packages,
            metadata.packages.PackageManagers.YARN: self._extract_yarn_packages
        }

        cli_package_name_params_list: List[CLIPackageNameParam] = extractors[self.package_manager]()

        for package_param in cli_package_name_params_list:
            if package_param.typ == PackageParamType.UPID:
                self._packages.append(package_param.data)
            elif package_param.typ == PackageParamType.MANIFEST:
                self._install_manifest = True

    @property
    def packages(self) -> List[UnifiedPackageID]:
        return self._packages

    @property
    def install_manifest(self) -> bool:
        return self._install_manifest

    def subprocess_popen_list_command(self) -> List[Text]:
        rv = [self.package_manager, self.action]
        rv.extend(self.arguments)
        return rv
