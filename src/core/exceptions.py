from http import HTTPStatus

from fastapi.exceptions import HTTPException


class ObjectAlreadyExistsError(HTTPException):
    """ Exception for existed object."""

    def __init__(self, instance):
        self.detail = f'Object {instance!r} already exists.'
        self.status_code = HTTPStatus.BAD_REQUEST


class ObjectNotFoundError(HTTPException):
    """" Exception for 404 error."""

    def __init__(self, message: str):
        self.detail = message
        self.status_code = HTTPStatus.NOT_FOUND
