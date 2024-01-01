import secrets
from typing import Optional

from app.domain.auth import AuthService, UnauthorizedError


class SimpleAuthService(AuthService):
    def __init__(self, domain: str, username: str, password: str):
        self._domain = domain
        self._username_digest = username.encode()
        self._password_digest = password.encode()

    def authenticate(self, username: str, password: str) -> Optional[str]:
        username_digest = username.encode()
        password_digest = password.encode()

        if secrets.compare_digest(self._username_digest, username_digest) and secrets.compare_digest(
            self._password_digest, password_digest
        ):
            return self._domain

        raise UnauthorizedError()
