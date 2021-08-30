from onebot_api.exceptions import FormatError, APINotFound

__all__ = ['ID', "ERROR_CODES", "DEFAULT_CONFIG", "PATHS"]

ID = "onebot_api"

ERROR_CODES = {
    1400: FormatError,
    1404: APINotFound
}

DEFAULT_CONFIG = {
    "url": "ws://127.0.0.1:6700"
}

PREFIX = "!!ob"


class PATHS:
    API = "/api"
    EVENT = "/event"


class HELP_MESSAGE:
    RELOAD = "Reload the OneBot API"
