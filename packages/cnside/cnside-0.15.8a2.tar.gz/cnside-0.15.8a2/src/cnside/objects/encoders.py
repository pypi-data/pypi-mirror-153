import datetime
from json import JSONEncoder
from pathlib import PurePath, PurePosixPath
from typing import Any

from cnside.objects.core import DelimitedObject


class CNSIDEJsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime.datetime, DelimitedObject, PurePath, PurePosixPath)):
            return o.__str__()
