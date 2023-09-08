from enum import IntEnum
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any, Literal

DataT = TypeVar('DataT')

ServerStatus = Literal['ok', 'error', 'missing_parameters']


class ServerCode(IntEnum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# Not an enum because it's not a finite set of values
class Cookie:
    REFRESH_TOKEN = 'refresh_token'


class ServerResponse(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
    status: ServerStatus = 'ok'
    message: Optional[str] = None

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """
            Override the default dict method to exclude None values in the response
        """
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)
