from typing import TYPE_CHECKING, Optional
from argus_api.utils import error_messages
if TYPE_CHECKING:
    from requests import Response


class ArgusAPIClientException(Exception):
    """Parent class for client exceptions"""
    ...


class ArgusAPIAuthenticationError(ArgusAPIClientException):
    """Error that happened during authentication of a session."""
    DEFAULT_MESSAGE = "authentication failed"

    #: error message
    message: Optional[str] = None
    #: HTTP error response (if available)
    response: Optional["Response"] = None

    def __init__(
        self,
        message: Optional[str]=None,
        response: Optional["Response"]=None
    ):

        self.response = response
        self.message = message if message else self._get_message(response)

        super().__init__(self.message)

    @classmethod
    def _get_message(cls, response: Optional["Response"]):
        if response is None:
            return cls.DEFAULT_MESSAGE
        try:
            content = response.json()
        except Exception as e:
            return cls.DEFAULT_MESSAGE
        return error_messages(content.get("messages"), default=cls.DEFAULT_MESSAGE)

