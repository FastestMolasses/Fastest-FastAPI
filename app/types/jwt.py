from enum import IntEnum
from datetime import datetime
from pydantic import BaseModel


class Role(IntEnum):
    SUPER = 1
    ADMIN = 2
    SUBSCRIBER = 3
    USER = 4


class JWTPayload(BaseModel):
    """
        The payload of a JWT token.
    """
    # Subject
    sub: str
    # Expiration
    exp: datetime
    # Issued at
    iat: datetime
    # Authorization role
    role: Role
    # Unique hex number
    nonce: str
    # User ID
    id: int


class TokenData(BaseModel):
    """
        Data passed to create a JWT token.
    """
    # Subject
    sub: str
