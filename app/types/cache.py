# Don't use enums because usually places where we use these values require
# string values, not Enum values.


class RedisTokenPrefix:
    """
    When creating a SessionStore, it is useful to have a prefix to avoid
    collisions with other keys in Redis.
    """
    USER = 'user'


class UserKey:
    """
    Keys used to store user data in Redis.
    """
    NONCE = 'nonce'
