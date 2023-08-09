from http import HTTPStatus

from fastapi.exceptions import HTTPException


class ObjectAlreadyExistsError(HTTPException):
    """Exception for existing object."""

    def __init__(self, message: str):
        detail = message
        status_code = HTTPStatus.BAD_REQUEST
        super().__init__(status_code, detail=detail)


class ObjectNotFoundError(HTTPException):
    """ Exception for 404 error."""

    def __init__(self, message: str):
        self.detail = message
        self.status_code = HTTPStatus.NOT_FOUND
