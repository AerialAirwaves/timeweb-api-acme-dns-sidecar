from abc import ABC
from typing import Optional


class DatabaseService(ABC):
    async def get_last_dns_record_id(self, domain: str) -> Optional[int]:
        ...

    async def update_last_dns_record(self, domain: str, record_id: int) -> None:
        ...
