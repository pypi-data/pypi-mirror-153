from typing import List, Text


class PackageRepositories:  # NOT Package Repositories! (aka PyPi)
    PYPI = "pypi"
    NPM = "npm"
    MAVEN = "maven"
    NUGET = "nuget"

    @classmethod
    def to_list(cls) -> List[Text]:
        return [
            cls.PYPI,
            cls.NPM,
            cls.MAVEN,
            cls.NUGET
        ]


class PackageManagers:
    PIP = "pip"
    NPM = "npm"
    MAVEN = "mvn"
    NUGET = "nuget"
    YARN = "yarn"

    @classmethod
    def to_list(cls) -> List[Text]:
        return [
            cls.PIP,
            cls.NPM,
            cls.MAVEN,
            cls.NUGET,
            cls.YARN
        ]


class PackageExtensions:
    GZ = ".gz"
    TAR_GZ = ".tar.gz"
    NUPKG = ".nupkg"
    JAR = ".jar"

    @classmethod
    def to_list(cls) -> List[Text]:
        return [
            cls.GZ,
            cls.TAR_GZ,
            cls.JAR,
            cls.NUPKG
        ]


class ManifestExtensions:
    POM = ".pom"


class Archivers:
    ZIP = "zip"
    GZ = "gunzip"

    _ext_index = {
        PackageExtensions.GZ: GZ,
        PackageExtensions.TAR_GZ: GZ,
        PackageExtensions.JAR: ZIP,
        PackageExtensions.NUPKG: ZIP
    }

    @classmethod
    def get_by_extension(cls, ext: Text):
        return cls._ext_index[ext]


class ManifestNames:
    PIP = "requirements.txt"
    NPM = "package.json"
    YARN = "package.json"

    @classmethod
    def get(cls, package_manager: Text) -> Text:
        index = {
            PackageManagers.PIP: cls.PIP,
            PackageRepositories.PYPI: cls.PIP,
            PackageManagers.NPM: cls.NPM,
            PackageManagers.YARN: cls.YARN
        }
        return index[package_manager]


class LockfileNames:
    NPM = "package-lock.json"
    PIP = None
    YARN = "yarn.lock"

    @classmethod
    def get(cls, package_manager: Text) -> Text:
        index = {
            PackageManagers.PIP: cls.PIP,
            PackageRepositories.PYPI: cls.PIP,
            PackageManagers.NPM: cls.NPM,
            PackageManagers.YARN: cls.YARN
        }
        return index[package_manager]

    @classmethod
    def non_lockfile_managers(cls):
        return [PackageManagers.PIP]


class Constructors:
    ARCHIVE = "archive"
    COPY = "copy"
