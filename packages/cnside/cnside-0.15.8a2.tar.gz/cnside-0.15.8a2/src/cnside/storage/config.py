import os
from pathlib import Path
from typing import Text, Optional

from pydantic import BaseModel

__all__ = ["StorageHandlerConfig"]


class StorageHandlerConfig(BaseModel):
    base_dir: Optional[Text] = os.path.join(Path.home(), ".cnside")
    _token_name: Optional[Text] = "token.json"
    _config_name: Optional[Text] = "cnside.config.json"

    @property
    def token_file_path(self):
        return os.path.join(self.base_dir, self._token_name)

    @property
    def config_file_path(self):
        return os.path.join(self.base_dir, self._config_name)
