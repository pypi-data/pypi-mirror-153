from typing import Optional


class SpiderError(Exception):
    """Base Class for spider errors."""
    def __init__(self, msg: str, cause: Optional[Exception] = None) -> None:
        self.msg = msg
        self.cause = cause
        self.req = None
        self.res = None


class RequestIgnored(SpiderError):
    """Indicates a decision was made not to process a request."""
    def __init__(self, url: str, cause: Optional[Exception] = None) -> None:
        super().__init__('Request was ignored for {}.'.format(url), cause)


class ResponseIgnored(SpiderError):
    """Indicates a decision was made not to process a response."""
    def __init__(self, url: str, cause: Optional[Exception] = None) -> None:
        self.new_req = None
        super().__init__('Response was ignored for {}'.format(url), cause)


class DownLoadError(SpiderError):
    """Indicates an error when downloading."""
    def __init__(self, url: str, cause: Optional[Exception] = None) -> None:
        self.need_retry = False
        super().__init__('Cannot download from {}'.format(url), cause)


class ParseError(SpiderError):
    """Indicates an error when parsing."""
    def __init__(self, url: str, cause: Optional[Exception] = None) -> None:
        super().__init__('Error when parsing response from {}'.format(url), cause)


class PipeError(SpiderError):
    """Indicates an error when collecting."""
    def __init__(self, url: str, cause: Optional[Exception] = None) -> None:
        super().__init__('Error when collecting results from {}'.format(url), cause)


class FailedStatusCode(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(status_code)
