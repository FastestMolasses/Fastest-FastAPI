from fastapi import APIRouter
from app.api.endpoints import collection, auth

apiRouter = APIRouter()
apiRouter.include_router(collection.router, tags=['collection'])
apiRouter.include_router(auth.router, tags=['auth'])
