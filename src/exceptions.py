from typing import Annotated, Any
from fastapi.exceptions import HTTPException


class CustomHttpException(HTTPException):

    def __init__(
            self,
            status_code: Annotated[
                int,
                """
                HTTP status code to send to the client
                """
            ],
            detail: Annotated[
                Any,
                """
                Any data to be sent to the client in the `detail` key of the JSON response.
                """
            ] = None,
            headers: Annotated[
                dict[str, str] | None,
                """
                Any headers to send to the client in the response.
                """
            ] = None,
            message: Annotated[
                Any,
                """
                Any data to be sent to the client in the `message` key of the JSON
                response.
                """
            ] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.message = message
        self.detail = detail


class CustomValueError(Exception):
    def __init__(self, message: str = "error", detail: dict | None = None):
        super().__init__(message)
        self.message = message
        self.detail = detail
