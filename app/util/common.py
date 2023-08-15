import os

from typing import Callable


def getFunctionArguments(func: Callable[..., str]) -> tuple[str, ...]:
    """
        Gets the arguments of a function.
    """
    return func.__code__.co_varnames[:func.__code__.co_argcount]


def generateNonce() -> str:
    """
        Generates a 32 length nonce hex string.
    """
    return os.urandom(16).hex()
