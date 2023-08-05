from typing import Text

from pydantic import BaseModel


class ServerErrorData(BaseModel):
    status_code: int


class TokenExpired(Exception):
    pass


class RemoteServerError(Exception):

    def __init__(self, data: ServerErrorData, message: Text = None) -> None:
        super().__init__(message)

        self.data = data
