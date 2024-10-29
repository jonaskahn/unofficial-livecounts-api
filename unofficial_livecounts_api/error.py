class RequestApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@DeprecationWarning
class TiktokError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@DeprecationWarning
class YoutubeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@DeprecationWarning
class TwitterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
