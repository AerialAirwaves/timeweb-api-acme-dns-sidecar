from typing import Optional

import tinydb
from aiotinydb import AIOTinyDB

from app.domain.db import DatabaseService


class TinyDBDatabaseService(DatabaseService):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    async def get_last_dns_record_id(self, domain: str) -> Optional[int]:
        async with AIOTinyDB(self._filename) as db:
            table = db.table("last_dns_records")

            query = tinydb.Query()
            row = table.get(query.domain == domain)

            if row is not None:
                return row["record_id"]

    async def update_last_dns_record(self, domain: str, record_id: int) -> None:
        async with AIOTinyDB(self._filename) as db:
            table = db.table("last_dns_records")

            query = tinydb.Query()
            table.remove(query.domain == domain)

            table.insert({"domain": domain, "record_id": record_id})
