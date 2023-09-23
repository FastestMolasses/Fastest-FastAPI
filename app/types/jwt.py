from datetime import datetime
from pydantic import BaseModel


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
