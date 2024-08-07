# uvicorn main:server --reload
import app.models.mysql
import app.db.connection
import app.api.middleware as middleware

from fastapi import FastAPI
from app.api.router import apiRouter
from app.core.config import settings
from app.log.setup import setup_logging
from app.types.server import ServerResponse
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

server = FastAPI(
    title='fastapi-server',
    debug=settings.DEBUG,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    default_response_class=ORJSONResponse,
)
server.include_router(apiRouter, prefix=settings.API_V1_STR)

setup_logging()

# Prometheus metrics
Instrumentator(
    env_var_name='ENABLE_METRICS',
).instrument(server).expose(server)

# Creates the tables if they dont exist
app.db.connection.createMySQLTables()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    server.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

server.add_middleware(middleware.DBExceptionsMiddleware)
server.add_middleware(middleware.CatchAllMiddleware)
server.add_middleware(middleware.ProfilingMiddleware)

@server.get('/')
async def root() -> ServerResponse:
    return ServerResponse()
