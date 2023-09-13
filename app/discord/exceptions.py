class Unauthorized(Exception):
    """Raised when user is not authorized."""


class InvalidRequest(Exception):
    """Raised when a Request is not Valid"""


class RateLimited(Exception):
    """Raised when a Request is not Valid"""

    def __init__(self, json, headers):
        self.json = json
        self.headers = headers
        self.message = json['message']
        self.retry_after = json['retry_after']
        super().__init__(self.message)


class InvalidToken(Exception):
    """Raised when a Response has invalid tokens"""


class ScopeMissing(Exception):
    scope: str

    def __init__(self, scope: str):
        self.scope = scope
        super().__init__(self.scope)


class ClientSessionNotInitialized(Exception):
    """Raised when no Client Session is initialized but one would be needed"""
    pass
