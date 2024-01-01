from abc import ABC

from pydantic import BaseModel


class AcmeDnsUpdateIn(BaseModel):
    subdomain: str
    txt: str


class AcmeDnsUpdateOut(BaseModel):
    txt: str


class AcmeDNSUpdateException(Exception):
    ...


class AcmeDnsUpdateService(ABC):
    async def update(self, x_api_user: str, x_api_key: str, in_info: AcmeDnsUpdateIn) -> AcmeDnsUpdateOut:
        ...
