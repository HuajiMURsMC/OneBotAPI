class OneBotAPIError(Exception):
    pass


class FormatError(OneBotAPIError):
    pass


class APINotFound(OneBotAPIError):
    pass
