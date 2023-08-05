import abc
from typing import Text, Any, List

from packaging import version

from cnside import errors
from cnside import metadata


# Taken from Evix
def dependent_args(arg: Any, dependents: List[Any]):
    if arg:
        if not all(dependents):
            raise ValueError("Missing depending arguments: %s", dependents)


# Taken from Engine
class DelimitedObject(metaclass=abc.ABCMeta):
    __version__ = "1.0.1"
    __object_type__ = "delimited_object"

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.descriptor

    @property
    def descriptor(self):
        return self.build_descriptor()

    def build_descriptor(self):
        return self._append_headers(self._build_descriptor()).lower()

    def _append_headers(self, d: Text):
        return f"{self.__object_type__}:{self.__version__}:{d}"

    @abc.abstractmethod
    def _build_descriptor(self) -> Text:
        """
        Build a text descriptor from self.
        """
        raise NotImplementedError

    @classmethod
    def from_descriptor(cls, d: Text):
        cls._verify_descriptor(d)
        no_headers_d = cls._remove_headers(d)
        return cls._from_descriptor(d=no_headers_d, dv=cls._parse_descriptor(d=d, remove_headers=False)[1])

    @classmethod
    def _remove_headers(cls, d: Text) -> Text:
        return ":".join(cls._parse_descriptor(d, remove_headers=True))

    @classmethod
    def _parse_descriptor(cls, d: Text, remove_headers: bool = True) -> List[Text]:
        parsed_descriptor = d.split(":")
        rv = parsed_descriptor[2::] if remove_headers else parsed_descriptor
        return rv

    @classmethod
    def _verify_descriptor(cls, d: Text):
        parsed_descriptor = cls._parse_descriptor(d, remove_headers=False)

        cved_object_type = parsed_descriptor[0]
        cved_version = parsed_descriptor[1]

        if not cved_object_type == cls.__object_type__:
            raise errors.IncorrectObjectDescriptor(cved_object_type)

        if not version.parse(cved_version) <= version.parse(cls.__version__):
            raise errors.UnsupportedObjectVersion(cved_version)

    @classmethod
    @abc.abstractmethod
    def _from_descriptor(cls, d: Text, dv: Text):
        """
        Initiate class from descriptor string.

        :param d: descriptor
        :param dv: descriptor version
        """

        raise NotImplementedError


# # todo: extend upid +/ packages with package types?
# class PackageType:
#     MANIFEST = 1
#     PACKAGE = 2
#     ALIASED = 3
#     FOLDER = 4
#     LOCAL_ARCHIVE = 5
#     REMOTE_ARCHIVE = 6
#     GIT_URL = 7
#     GITHUB_URI = 8


class GenericPackage:
    def __init__(self, package: Text, package_manager: Text = None):
        self.package = package
        self.package_manager = package_manager

    @property
    def upid(self):
        rv = UnifiedPackageID(
            package_manager=self.package_manager,
            package_name=self.package
        )
        return rv


class NPMPackage(GenericPackage):
    def __init__(self, package: Text):
        super().__init__(package, package_manager=metadata.packages.PackageRepositories.NPM)


class PYPIPackage(GenericPackage):
    def __init__(self, package: Text):
        super().__init__(package, package_manager=metadata.packages.PackageRepositories.PYPI)


# Taken from Engine
class UnifiedPackageID(DelimitedObject):
    """
    Unified Package ID:
        Generic: {package_manager}:{package_name}:{package_version: optional}
        Nuget: {package_manager}:{package_name}:{package_version}:{framework}
        Maven: {package_manager}:{group_id}:{artifact_id}:{package_version}:{framework}
        PyPi: {package_manager}:{package_name}:{package_version}

    See project documentation for more info.
    """

    __version__ = "2.1.1"
    __object_type__ = "upid"

    def __init__(self, package_manager: Text, package_name: Text = None, group_id: Text = None,
                 artifact_id: Text = None, package_version: Text = None, framework: Text = None):

        self.package_manager = package_manager
        if self.package_manager == metadata.packages.PackageRepositories.MAVEN:
            dependent_args(True, [group_id, artifact_id, package_version])

            self.group_id = group_id
            self.artifact_id = artifact_id
            self.package_name = f"{self.group_id}:{self.artifact_id}"
            self.package_version = package_version
            self.framework = framework
        else:
            self.group_id = group_id
            self.artifact_id = artifact_id
            self.package_name = package_name
            self.package_version = package_version
            self.framework = framework

    def _build_descriptor(self) -> Text:
        if self.package_manager == metadata.packages.PackageRepositories.MAVEN:
            package_id = f"{self.package_manager}:{self.group_id}:{self.artifact_id}:{self.package_version}:" \
                         f"{self.framework}"
        elif self.package_manager == metadata.packages.PackageRepositories.NUGET:
            package_id = f"{self.package_manager}:{self.package_name}:{self.package_version}:{self.framework}"
        elif self.package_manager == metadata.packages.PackageRepositories.PYPI:
            package_id = f"{self.package_manager}:" + \
                         (f'{self.package_name.split("==")[0]}:{self.package_name.split("==")[1]}'
                          if '==' in self.package_name else f'{self.package_name}')
        else:
            package_id = f"{self.package_manager}:{self.package_name}" + \
                         ("" if not self.package_version else f":{self.package_version}")
        return package_id

    @classmethod
    def _from_descriptor(cls, d: Text, dv: Text):
        parsed_package_id = d.split(":")

        package_manager = parsed_package_id[0]
        if package_manager == metadata.packages.PackageRepositories.MAVEN:
            group_id = parsed_package_id[1]
            artifact_id = parsed_package_id[2]
            package_name = f"{group_id}:{artifact_id}"
            package_version = parsed_package_id[3]
            framework = parsed_package_id[4]
        else:
            version_specified = True if len(parsed_package_id) > 2 else None
            framework_specified = True if len(parsed_package_id) > 3 else None
            group_id = None
            artifact_id = None
            package_name = parsed_package_id[1]
            package_version = parsed_package_id[2] if version_specified else None
            framework = parsed_package_id[3] if framework_specified else None

        rv = cls(package_manager=package_manager, package_name=package_name, group_id=group_id,
                 artifact_id=artifact_id, package_version=package_version, framework=framework)

        return rv

    @classmethod
    def from_repr(cls, package_manager: Text, r: Text):
        index = {
            metadata.packages.PackageRepositories.PYPI: PYPIPackage,
            metadata.packages.PackageManagers.NPM: NPMPackage
        }
        return index[package_manager](r).upid

    # TODO: transfer to packages
    def _build_pypi_package_full_name(self) -> Text:
        if self.package_version:
            rv = f"{self.package_name}=={self.package_version}"
        else:
            rv = self.package_name
        return rv

    def _build_npm_package_full_name(self) -> Text:
        rv = self.package_name if not self.package_version \
            else f"{self.package_name}@{self.package_version}"
        return rv

    def pm_repr(self) -> Text:
        index = {
            metadata.packages.PackageRepositories.PYPI: self._build_pypi_package_full_name,
            metadata.packages.PackageManagers.NPM: self._build_npm_package_full_name,
            metadata.packages.PackageManagers.YARN: self._build_npm_package_full_name
        }

        return index[self.package_manager]()
