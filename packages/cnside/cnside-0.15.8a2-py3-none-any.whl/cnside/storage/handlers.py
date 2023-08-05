import json
import os
from pathlib import Path
from typing import Text, Dict, Optional

from pydantic import BaseModel

from cnside import metadata
from cnside.storage import StorageHandlerConfig

__all__ = ["StorageHandler", "ManifestData"]


class ManifestData(BaseModel):
    manifest_name: Text
    lockfile_name: Optional[Text] = None
    manifest: Optional[Text] = None
    lockfile: Optional[Text] = None


class FileHandler:
    def __init__(self, file_path: Text):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r+") as fp:
            data = json.load(fp)
        return data

    def save(self, data: Dict):
        if not os.path.exists(self.file_path):
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w+") as fp:
            json.dump(data, fp)


class ManifestHandler:
    @staticmethod
    def _get_file_contents(file_path: Text):
        if os.path.exists(file_path):
            with open(file_path, "r") as fp:
                rv = fp.read()
        else:
            rv = None

        return rv

    def get(self, package_manager: Text, base_dir: Text = None) -> ManifestData:
        manifest_name = metadata.packages.ManifestNames.get(package_manager)
        lockfile_name = metadata.packages.LockfileNames.get(package_manager)

        manifest_path = manifest_name if not base_dir else os.path.join(base_dir, manifest_name)
        lockfile_path = lockfile_name if not base_dir else os.path.join(base_dir, lockfile_name)

        rv = ManifestData(
            manifest_name=manifest_name,
            lockfile_name=lockfile_name,
            manifest=self._get_file_contents(file_path=manifest_path),
            lockfile=None if not lockfile_name else self._get_file_contents(file_path=lockfile_path)
        )
        return rv


class StorageHandler:
    def __init__(self, config: StorageHandlerConfig):
        self._config = config

    @property
    def token(self):
        return FileHandler(self._config.token_file_path)

    @property
    def config(self):
        return FileHandler(self._config.config_file_path)

    @property
    def manifest(self):
        return ManifestHandler()
