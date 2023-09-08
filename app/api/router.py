from fastapi import APIRouter
from app.api.endpoints import auth

apiRouter = APIRouter()
apiRouter.include_router(auth.router, tags=['auth'])
