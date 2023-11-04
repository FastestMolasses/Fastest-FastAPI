from jose import JWTError
from loguru import logger
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.models.mysql import User
from app.core.config import settings
from app.db.connection import MySqlSession
from app.auth.jwt import RequireRefreshToken, RequireJWT, create_jwt

from app.types.jwt import TokenData, JWTPayload
from app.types.server import ServerResponse, Cookie

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(response: ORJSONResponse) -> ServerResponse[str]:
    # TODO: Look up the user here, or create one if they don't exist
    # session = MySqlSession()
    token = TokenData(sub='example_user_id')

    try:
        accessToken, refreshToken = create_jwt(token)
    except JWTError as e:
        logger.error(f'JWT Error during login: {e}')
        return ServerResponse(status='error', message='JWT Error, try again')

    # Save the refresh token in an HTTPOnly cookie
    response.set_cookie(
        Cookie.REFRESH_TOKEN,
        value=refreshToken,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        expires=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )
    return ServerResponse[str](data=accessToken)


@router.get('/refresh')
async def refresh(
    response: ORJSONResponse, payload: JWTPayload = Depends(RequireRefreshToken)
) -> ServerResponse[str]:
    token = TokenData(sub=payload.sub)

    try:
        accessToken, refreshToken = create_jwt(token)
    except JWTError as e:
        logger.error(f'JWT Error during login: {e}')
        return ServerResponse(status='error', message='JWT Error, try again.')

    # Save the refresh token in an HTTPOnly cookie
    response.set_cookie(
        Cookie.REFRESH_TOKEN,
        value=refreshToken,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        expires=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )
    return ServerResponse[str](data=accessToken)


@router.get('/decodeToken')
async def decodeToken(user: User = Depends(RequireJWT())):
    with MySqlSession() as session:
        user = session.query(User).filter_by(id=user.id).one()
        return ServerResponse(data=user.__dict__)
