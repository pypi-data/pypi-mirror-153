from typing import Optional, TYPE_CHECKING, Union


class OpenDataHubError(Exception):
    def __init__(
        self,
        response_code: Optional[int] = None,
        error_message: str = "",
    ) -> None:

        Exception.__init__(self, error_message)
        self.response_code = response_code
        self.error_message = error_message

    def __str__(self) -> str:
        if self.response_code is not None:
            return f"{self.response_code}: {self.error_message}"
        else:
            return f"{self.error_message}"


class ODLAuthenticationError(OpenDataHubError):
    pass


class ODLDeprecateError(OpenDataHubError):
    pass

class ODLRNError(OpenDataHubError):
    pass