from jose import jwt
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError

from app.models.mysql import User
from app.core.config import settings
from app.cache.redis import SessionStore
from app.util.common import generateNonce

from app.types.server import Cookie
from app.types.cache import UserKey
from app.types.jwt import TokenData, JWTPayload

ALGORITHM = 'HS256'


def create_jwt(data: TokenData,
               session: Session | None = None,
               userID: int | None = None) -> tuple[str, str]:
    """
        Create a JWT token that expires in 30 min. If a user role is provided, the token will be
        created with that role. Otherwise, the user's role will be queried from the database if
        the session is provided. If the user does not exist in the database, a new user will be
        created.

        Raises:
            JWTError: If there is an error encoding the claims.
    """
    # If no user info was provided, we need to query it
    if session and userID is None:
        # Query the database to get the user's role. Create a new user if needed.
        user: User | None = session.query(
            User).filter_by(address=data.sub).first()
        if not user:
            user = User(address=data.sub)
            session.add(user)
            session.commit()
        userID = user.id

    if userID is None:
        raise JWTError('Could not get user info.')

    nonce = generateNonce()

    # Create the access token
    payload = JWTPayload(
        exp=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        id=userID,
        nonce=nonce,
        iat=datetime.utcnow(),
        **data.model_dump(),
    ).model_dump()
    accessToken = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Create the refresh token
    payload['exp'] = datetime.utcnow(
    ) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refreshToken = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Save the nonce in redis
    cache = SessionStore(data.sub, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
    cache.set(UserKey.NONCE, nonce)

    return accessToken, refreshToken


def verify_token(token: str) -> JWTPayload | None:
    """
        Decode a JWT token.
    """
    try:
        return JWTPayload(**jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                'require_iat': True,
                'require_exp': True,
                'require_sub': True,
            }
        ))
    except (JWTError, ExpiredSignatureError, JWTClaimsError):
        return None


class RequireJWT(HTTPBearer):
    """
        Custom FastAPI dependency for JWT authentication.
        Returns the decoded JWT payload if the token is valid.
    """
    async def __call__(self, request: Request):
        credentials = await super(RequireJWT, self).__call__(request)
        refreshToken = request.cookies.get(Cookie.REFRESH_TOKEN, '')

        if credentials:
            payload = verify_token(credentials.credentials)
            refreshTokenPayload = verify_token(refreshToken)
            if not payload or not refreshTokenPayload or \
                    not payload.nonce == refreshTokenPayload.nonce:
                raise HTTPException(
                    status_code=403, detail='Invalid token or expired token.')

            # Make sure the nonce is in the cache
            # This is the invalidation mechanism for refresh tokens
            if not _nonceInCache(refreshTokenPayload.sub, refreshTokenPayload.nonce):
                raise HTTPException(
                    status_code=403, detail='Invalid token or expired token.')

            return payload

        else:
            raise HTTPException(
                status_code=403, detail='Invalid authorization code.')


def RequireRefreshToken(request: Request) -> JWTPayload:
    refreshToken = request.cookies.get(Cookie.REFRESH_TOKEN, '')
    refreshTokenPayload = verify_token(refreshToken)
    if not refreshTokenPayload:
        raise HTTPException(
            status_code=403, detail='Invalid token or expired token.')

    # Make sure the nonce is in the cache
    # This is the invalidation mechanism for refresh tokens
    if not _nonceInCache(refreshTokenPayload.sub, refreshTokenPayload.nonce):
        raise HTTPException(
            status_code=403, detail='Invalid token or expired token.')

    return refreshTokenPayload


def _nonceInCache(address: str, nonce: str) -> bool:
    """
        Check if the nonce is in the cache.
    """
    cache = SessionStore(address)
    return cache.get(UserKey.NONCE) == nonce
