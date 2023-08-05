from requests import Response
import logging
from typing import TYPE_CHECKING
from argus_api.utils import error_messages, _format_error
try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError

if TYPE_CHECKING:
    from requests import Response

log = logging.getLogger(__name__)


class ArgusException(Exception):
    """Parent class for server-side errors."""

    #: error message
    message: str
    #: HTTP error response
    response: "Response"
    #: response status code
    status_code: int

    def __init__(self, resp):

        self.response = resp

        if isinstance(resp, Response):
            try:
                parsed_resp = resp.json()
            except JSONDecodeError:
                # response content is not JSON, which is suspicious because
                # error responses are in JSON format
                parsed_resp = self.response
        else:
            parsed_resp = resp

        if "messages" in parsed_resp:
            message_body = "\n".join(
                [_format_error(msg) for msg in parsed_resp["messages"]]
            )
        else:
            message_body = str(parsed_resp)

        if hasattr(resp, "reason") and hasattr(resp, "status_code"):
            self.status_code = resp.status_code
            self.message = (
                f"Status code {resp.status_code}: " f"{resp.reason}\n{message_body} "
            )
        else:
            self.message = message_body

        self.parsed_resp = parsed_resp
        super().__init__(self.message)


class AuthenticationFailedException(ArgusException):
    """Used for HTTP 401"""

    pass


class AccessDeniedException(ArgusException):
    """Used for HTTP 403"""

    pass


class ObjectNotFoundException(ArgusException):
    """Used for HTTP 404"""

    pass


class ValidationErrorException(ArgusException):
    """Used for HTTP 412"""

    pass


class ServiceUnavailableException(ArgusException):
    """Used for HTTP 503"""

    pass


class MultipleValidationErrorException(Exception):
    pass
