from black.mode import Deprecated


class RequestApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@Deprecated
class TiktokError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@Deprecated
class YoutubeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@Deprecated
class TwitterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
