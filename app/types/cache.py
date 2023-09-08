# Don't use enums because usually places where we use these values require
# string values, not Enum values.


class AuthSession:
    ADDRESS = 'address'
    SESSION_ID = 'session_id'
    NONCE = 'nonce'


class UserKey:
    NONCE = 'nonce'
