from typing import Callable
from fastapi import Request
from sqlalchemy.exc import IntegrityError
from app.types.server import ServerResponse
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


class DBExceptionsMiddleware(BaseHTTPMiddleware):
    """
        Middleware to catch and handle database exceptions.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response

        except NoResultFound:
            response = ServerResponse(status='error', message='Row not found')

        except MultipleResultsFound:
            response = ServerResponse(
                status='error', message='Multiple rows found')

        except IntegrityError as e:
            e.hide_parameters = True
            response = ServerResponse(
                status='error', message=str(e))

        return ORJSONResponse(response.dict(), status_code=400)


class CatchAllMiddleware(BaseHTTPMiddleware):
    """
        Middleware to catch errors.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response

        except Exception as e:
            # TODO: SEND NOTIFICATION HERE
            response = ServerResponse(
                status='error', message=str(e))
            return ORJSONResponse(response.dict(), status_code=400)
