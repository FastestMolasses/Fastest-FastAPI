from loguru import logger
from typing import Callable
from fastapi import Request
# from pyinstrument import Profiler
from app.core.config import settings
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

        except NoResultFound as e:
            logger.exception(f'NoResultFound: {e}')
            response = ServerResponse(status='error', message='Row not found')

        except MultipleResultsFound as e:
            logger.exception(f'MultipleResultsFound: {e}')
            response = ServerResponse(
                status='error', message='Multiple rows found')

        except IntegrityError as e:
            e.hide_parameters = True
            logger.exception(f'IntegrityError: {e}')
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
            logger.exception(e)
            response = ServerResponse(
                status='error', message=str(e))
            return ORJSONResponse(response.dict(), status_code=400)


class ProfilingMiddleware(BaseHTTPMiddleware):
    """
        Middleware to catch errors.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        if settings.PROFILING:
            # profiler = Profiler(interval=settings.profiling_interval, async_mode='enabled')

            # profiler.start()
            # response = await call_next(request)
            # profiler.stop()

            # return response
            return await call_next(request)
        else:
            return await call_next(request)
