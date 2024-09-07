class RequestApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TiktokError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class YoutubeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TwitterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
