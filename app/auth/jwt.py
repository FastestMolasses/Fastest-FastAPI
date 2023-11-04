from jose import jwt
from loguru import logger
from jose.constants import Algorithms
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError

from app.core.config import settings
from app.cache.redis import SessionStore
from app.util.common import generateNonce

from app.types.server import Cookie
from app.types.jwt import TokenData, JWTPayload
from app.types.cache import RedisTokenPrefix, UserKey

ALGORITHM = Algorithms.HS256


def create_jwt(data: TokenData) -> tuple[str, str]:
    """
    Create access and refresh JWT tokens.
    If the user ID is provided, the database won't be queried.
    If the user does not exist in the database and no user ID is provided, a new user will be created.
    The nonce is stored in the cache for refresh token invalidation.
    """
    nonce = None
    if settings.JWT_USE_NONCE:
        nonce = generateNonce()

    access_token = create_token(data, nonce, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(data, nonce, settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    # Save the nonce in the cache for refresh token invalidation, only if using nonce
    if nonce:
        set_nonce_in_cache(data.sub, nonce, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    return access_token, refresh_token


def verify_token(token: str) -> JWTPayload | None:
    """
    Decode a JWT token.
    """
    try:
        payload = JWTPayload(
            **jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[ALGORITHM],
                options={
                    'require_iat': True,
                    'require_exp': True,
                    'require_sub': True,
                },
            )
        )
        if settings.JWT_USE_NONCE and not payload.nonce:
            logger.error('Nonce not found in JWT payload.')
            return None
        return payload
    except (JWTError, ExpiredSignatureError, JWTClaimsError) as e:
        logger.error(f'Error while verifying JWT: {e}')
        return None


class RequireJWT(HTTPBearer):
    """
    Custom FastAPI dependency for JWT authentication.
    Returns the decoded JWT payload if the token is valid.
    """

    async def __call__(self, request: Request):
        credentials = await super(RequireJWT, self).__call__(request)
        refreshToken = request.cookies.get(Cookie.REFRESH_TOKEN, '')

        if credentials and credentials.credentials:
            payload = verify_token(credentials.credentials)
            refreshTokenPayload = verify_token(refreshToken)

            print(payload)
            print(refreshTokenPayload)

            # Check if payloads are valid
            if not (payload and refreshTokenPayload):
                raise HTTPException(status_code=403, detail='Invalid token or expired token.')

            # If using nonce, check nonce
            if not validate_nonce(payload, refreshTokenPayload):
                raise HTTPException(status_code=403, detail='Nonce validation failed.')

            return payload
        else:
            raise HTTPException(status_code=403, detail='Invalid authorization code.')


def RequireRefreshToken(request: Request) -> JWTPayload:
    refreshToken = request.cookies.get(Cookie.REFRESH_TOKEN, '')
    refreshTokenPayload = verify_token(refreshToken)
    if not refreshTokenPayload:
        raise HTTPException(status_code=403, detail='Invalid token or expired token.')

    # If using nonce, ensure it's in the cache
    if settings.JWT_USE_NONCE and not is_nonce_in_cache(
        refreshTokenPayload.sub, refreshTokenPayload.nonce
    ):
        raise HTTPException(status_code=403, detail='Invalid token or expired token.')

    return refreshTokenPayload


def create_token(data: TokenData, nonce: str | None, expire_minutes: int) -> str:
    payload = {
        **data.model_dump(),
        'exp': datetime.utcnow() + timedelta(minutes=expire_minutes),
        'iat': datetime.utcnow(),
    }
    if settings.JWT_USE_NONCE and nonce:
        payload['nonce'] = nonce
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def validate_nonce(payload: JWTPayload, refreshTokenPayload: JWTPayload) -> bool:
    if not settings.JWT_USE_NONCE:
        return True
    if payload.nonce != refreshTokenPayload.nonce:
        raise HTTPException(status_code=403, detail='Nonce mismatch.')
    if not is_nonce_in_cache(refreshTokenPayload.sub, refreshTokenPayload.nonce):
        raise HTTPException(status_code=403, detail='Invalid token or expired token.')
    return True


def set_nonce_in_cache(user_id: str, nonce: str, expiration_time: int):
    """
    Store nonce in cache with a specified expiration time.
    """
    if settings.JWT_USE_NONCE:
        cache = SessionStore(RedisTokenPrefix.USER, user_id, ttl=expiration_time)
        cache.set(UserKey.NONCE, nonce)


def is_nonce_in_cache(user_id: str, nonce: str | None) -> bool:
    """
    Check if the nonce is in the cache.
    """
    if not nonce:
        return False
    cache = SessionStore(RedisTokenPrefix.USER, user_id)
    return cache.get(UserKey.NONCE) == nonce
