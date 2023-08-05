import logging
from multiprocessing import Process, Queue
from typing import Text

from fastapi import FastAPI
from uvicorn import Config, Server

from cnside.authenticator import AuthenticatorConfig, CallbackData

__all__ = ["MiniServer"]


class MiniServer(Process):

    def __init__(self, config: AuthenticatorConfig):
        super().__init__()

        self.config = config
        self.rq = Queue()

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        app = FastAPI()

        @app.get("/login/callback")
        def login_callback(code: Text, state: Text):
            if not state == self.config.state:
                callback_data = CallbackData(success=False, code="")
            else:
                callback_data = CallbackData(success=True, code=code)

            self.rq.put(callback_data)

            # TODO: return a html response
            return

        server = Server(
            config=Config(app=app, host=self.config.host, port=self.config.port, log_level=logging.CRITICAL)
        )
        server.run()
