import base64
import hashlib
import os
import uuid
from typing import Text, Optional, Any

from pydantic import BaseModel

from cnside.storage import StorageHandler

__all__ = ["AuthenticatorConfig", "CallbackData", "OAUTHToken"]


class AuthenticatorConfig(BaseModel):
    storage_handler: Any  # todo: StorageHandler BaseModel typing issue - FIX THIS SHIT
    auth_url: Text
    token_url: Text
    client_id: Text
    code_verifier: Optional[bytes] = base64.b64encode(os.urandom(64))
    state: Optional[Text] = str(uuid.uuid4())
    code_challenge_method: Optional[Text] = "S256"
    host: Optional[Text] = "127.0.0.1"
    port: Optional[int] = 8000 # todo: generate a random one and if taken generate another one and so on...

    @property
    def code_challenge(self):
        return base64.urlsafe_b64encode(hashlib.sha256(self.code_verifier).digest()).split("=".encode())[0]

    @property
    def redirect_url(self):
        # noinspection HttpUrlsUsage
        return f"http://{self.host}:{self.port}/login/callback"


class CallbackData(BaseModel):
    success: bool
    code: Text


class OAUTHToken(BaseModel):
    token_type: Text
    access_token: Text
    id_token: Text
    refresh_token: Text
