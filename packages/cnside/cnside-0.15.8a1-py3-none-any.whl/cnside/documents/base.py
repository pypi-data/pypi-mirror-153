from typing import Text


class Document(dict):
    __version__ = "1.0.0"
    __doc_type__ = "BaseDocument"

    def __getattribute__(self, item):
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self[key] = value


class RequestDocument(Document):
    __version__ = "1.0.0"
    __doc_type__ = "RequestDocument"

    def __init__(self, version: Text = None, doc_type: Text = None, **kwargs):
        super().__init__()

        self.version = self.__version__ if not version else version
        self.doc_type = self.__doc_type__ if not doc_type else doc_type
