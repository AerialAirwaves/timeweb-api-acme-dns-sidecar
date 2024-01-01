from abc import ABC
from typing import Optional


class AuthorizationError(Exception):
    ...


class UnauthorizedError(AuthorizationError):
    ...


class AuthService(ABC):
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authentication for /update method
        :param username: X-Api-Username
        :param password: X-Api-Password
        :raises UnauthorizedError:
        :return: domain FQDN or None if credentials invalid
        """

        ...
