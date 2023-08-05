import logging
import urllib.parse
import webbrowser
from typing import Text

import requests

from cnside.authenticator import AuthenticatorConfig, MiniServer, CallbackData, OAUTHToken
from cnside.errors import FailedToLoadToken, FailedToRefreshToken

LOGGER = logging.getLogger(__name__)


class Authenticator:
    def __init__(self, config: AuthenticatorConfig):
        self.config = config

    def _open_browser(self) -> Text:
        params = {
            "response_type": "code",
            "scope": "openId",
            "client_id": self.config.client_id,
            "state": self.config.state,
            "redirect_uri": self.config.redirect_url,
            "code_challenge": self.config.code_challenge,
            "code_challenge_method": self.config.code_challenge_method
        }

        auth_url = self.config.auth_url + "?" + urllib.parse.urlencode(params)

        webbrowser.open(url=auth_url)

        return auth_url

    def refresh_token(self, token: OAUTHToken):
        try:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": token.refresh_token,
                "client_id": self.config.client_id,
                "redirect_uri": self.config.redirect_url,
            }

            response = requests.post(
                url=self.config.token_url,
                data=data
            )

            rv = OAUTHToken(**response.json())
            return rv
        except Exception as e:
            raise FailedToRefreshToken(e)

    def _exchange_code_for_token(self, code: Text) -> OAUTHToken:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_url,
            "code_verifier": self.config.code_verifier
        }

        response = requests.post(
            url=self.config.token_url,
            data=data
        )

        # todo: validate status code

        rv = OAUTHToken(**response.json())
        return rv

    def authenticate(self) -> OAUTHToken:
        print("Starting Browser Interactive Authentication...\n")
        server = MiniServer(config=self.config)

        LOGGER.debug("Starting a MiniServer")
        server.start()

        LOGGER.debug("Opening browser and waiting for callback")
        auth_url = self._open_browser()
        print(f"Please continue the authentication process in your browser (Redirecting automatically).\n"
              "If nothing happens, click here: \n\n"
              f"{auth_url}\n")

        callback_data: CallbackData = server.rq.get()

        LOGGER.debug("Stopping MiniServer")
        server.stop()

        LOGGER.debug("Exchanging code for tokens")
        oauth_token = self._exchange_code_for_token(code=callback_data.code)

        LOGGER.debug("Saving token to disk")
        self.config.storage_handler.token.save(oauth_token.dict())

        print("Authenticated!")

        return oauth_token

    def load_token(self) -> OAUTHToken:
        try:
            token = OAUTHToken(**self.config.storage_handler.token.load())
        except FileNotFoundError:
            raise FailedToLoadToken("Failed to load token from disk.")
        except Exception as e:
            raise ValueError("Failed to load token! User is not authenticated.")

        return token
