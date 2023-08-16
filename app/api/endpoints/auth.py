from jose import JWTError
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.models.mysql import User
from app.core.config import settings
from app.db.connection import MySqlSession
from app.auth.jwt import RequireRefreshToken, RequireRole, create_jwt

from app.types.server import ServerResponse, Cookie
from app.types.jwt import TokenData, Role, JWTPayload

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(address: str, response: ORJSONResponse) -> ServerResponse[str]:
    session = MySqlSession()
    token = TokenData(sub=address)

    try:
        accessToken, refreshToken = create_jwt(token, session)
    except JWTError as e:
        return ServerResponse(status='error', message=f'JWT Error: {e}')
    finally:
        session.close()

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
async def refresh(response: ORJSONResponse,
                  payload: JWTPayload = Depends(RequireRefreshToken)) -> ServerResponse[str]:
    token = TokenData(sub=payload.sub)

    try:
        accessToken, refreshToken = create_jwt(
            token, userRole=payload.role, userID=payload.id)
    except JWTError as e:
        return ServerResponse(status='error', message=f'JWT Error: {e}')

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
async def decodeToken(user: User = Depends(RequireRole(Role.USER))):
    with MySqlSession() as session:
        return user.load(session)
