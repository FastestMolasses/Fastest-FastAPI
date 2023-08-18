from enum import Enum


class AuthSession(Enum):
    ADDRESS = 'address'
    SESSION_ID = 'session_id'
    NONCE = 'nonce'


class UserKey(Enum):
    NONCE = 'nonce'
