from http import HTTPStatus
from typing import TypeVar

from fastapi.exceptions import HTTPException

DatabaseModel = TypeVar("DatabaseModel")


class ObjectAlreadyExistsError(HTTPException):
    def __init__(self, instance):
        self.detail = f"Object {instance!r} already exists."
        self.status_code = HTTPStatus.BAD_REQUEST


class ObjectNotFoundError(HTTPException):
    def __init__(self, model: DatabaseModel):
        self.detail = f"Object '{model}' not found."
        self.status_code = HTTPStatus.NOT_FOUND
