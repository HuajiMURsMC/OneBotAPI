from typing import Optional
import os

from mcdreforged.api.utils.serializer import Serializable

from onebot_api.exceptions import FormatError, APINotFound

__all__ = [
    "ID",
    "CONFIG_FILE",
    "ERROR_CODES",
    "PREFIX",
    "PATHS",
    "HELP_MESSAGE",
    "CONFIG",
]

ID = "onebot_api"

CONFIG_FILE = os.path.join("config", "onebot_api.json")

ERROR_CODES = {1400: FormatError, 1404: APINotFound}

PREFIX = "!!ob"


class PATHS:
    API = "/api"
    EVENT = "/event"


class HELP_MESSAGE:
    RELOAD = "Reload the OneBot API"


class CONFIG(Serializable):
    url: str = "ws://127.0.0.1:6700"
    access_token: Optional[str] = None
