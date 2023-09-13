import time
import asyncio
import functools

from collections import OrderedDict


def time_cache(max_age_seconds, maxsize=128, typed=False):
    """
        Least-recently-used cache decorator with time-based cache invalidation.

        Args:
            max_age_seconds: Time to live for cached results (in seconds).
            maxsize: Maximum cache size (see `functools.lru_cache`).
            typed: Cache on distinct input types (see `functools.lru_cache`).
    """
    def _decorator(fn):
        @functools.lru_cache(maxsize=maxsize, typed=typed)
        def _new(*args, __time_salt, **kwargs):
            return fn(*args, **kwargs)

        @functools.wraps(fn)
        def _wrapped(*args, **kwargs):
            return _new(*args, **kwargs, __time_salt=int(time.time() / max_age_seconds))

        return _wrapped

    return _decorator


def aio_time_cache(max_age_seconds, maxsize=128, typed=False):
    """Least-recently-used cache decorator with time-based cache invalidation for async functions.

    Args:
        max_age_seconds: Time to live for cached results (in seconds).
        maxsize: Maximum cache size.
        typed: Cache on distinct input types.
    """
    cache = OrderedDict()
    lock = asyncio.Lock()

    def _key(args, kwargs):
        return args, tuple(sorted(kwargs.items()))

    def _decorator(fn):
        @functools.wraps(fn)
        async def _wrapped(*args, **kwargs):
            async with lock:
                key = _key(args, kwargs)
                if typed:
                    key += (tuple(type(arg) for arg in args),
                            tuple(type(value) for value in kwargs.values()))
                now = time.time()

                # Cache hit and check if value is still fresh
                if key in cache:
                    result, timestamp = cache.pop(key)
                    if now - timestamp <= max_age_seconds:
                        # Move to end to show that it was recently used
                        cache[key] = (result, timestamp)
                        return result

                # Cache miss or value has expired
                result = await fn(*args, **kwargs)
                cache[key] = (result, now)

                # Remove oldest items if cache is full
                while len(cache) > maxsize:
                    cache.popitem(last=False)

                return result

        return _wrapped

    return _decorator
