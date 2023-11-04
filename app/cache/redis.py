import redis

from app.core.config import settings


class SessionStore:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                connection_class=redis.SSLConnection,
            )
        return cls._pool

    def __init__(self, *tokens: str, ttl: int = (60 * 60 * 4)):
        """
        Params:\n
            tokens - Used to create a session in redis. Key/value pairs are unique to this token.
            Pass in multiple tokens and they will be joined into one.\n
            ttl - Time to live in seconds. Defaults to 4 hours.
        """
        self.token = ':'.join(tokens)
        self.redis = redis.StrictRedis(connection_pool=self.get_pool())
        self.ttl = ttl

    def set(self, key: str, value: str) -> int:
        self._refresh()
        return self.redis.hset(self.token, key, value)

    def get(self, key: str) -> str:
        self._refresh()
        val = self.redis.hget(self.token, key)
        if not val:
            return ''
        return val.decode('utf-8')

    def delete(self, key: str) -> int:
        self._refresh()
        return self.redis.hdel(self.token, key)

    def deleteSelf(self):
        self.redis.delete(self.token)

    def incr(self, key: str, amount: int = 1) -> int:
        self._refresh()
        return self.redis.hincrby(self.token, key, amount)

    def _refresh(self):
        self.redis.expire(self.token, self.ttl)
