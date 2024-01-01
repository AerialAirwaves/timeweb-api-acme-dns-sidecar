import logging

import app.domain.acme_dns_update
from app.domain.acme_dns_update import AcmeDnsUpdateService
from app.domain.auth import AuthService, UnauthorizedError
from app.domain.db import DatabaseService
from app.services.tw_api import TimewebAPIService


class TimewebACMEDnsUpdateService(AcmeDnsUpdateService):
    def __init__(
        self, auth_service: AuthService, db_service: DatabaseService, timeweb_service: TimewebAPIService
    ) -> None:
        self._auth_service = auth_service
        self._db_service = db_service
        self._tw = timeweb_service

    @staticmethod
    def is_subdomain(root: str, sub: str) -> bool:
        root_parts = root.lower().split(".")
        sub_parts = sub.lower().split(".")

        if root_parts[-1] == "":
            root_parts.pop()

        if sub_parts[-1] == "":
            sub_parts.pop()

        len_sub = len(sub_parts)
        return len(root_parts) >= len_sub and root_parts[-len_sub:] == sub_parts

    async def update(
        self, x_api_user: str, x_api_key: str, in_info: app.domain.acme_dns_update.AcmeDnsUpdateIn
    ) -> app.domain.acme_dns_update.AcmeDnsUpdateOut:
        root_domain = self._auth_service.authenticate(x_api_user, x_api_key)
        domain = in_info.subdomain
        if not self.is_subdomain(root_domain, domain):
            raise UnauthorizedError()

        last_record_id = await self._db_service.get_last_dns_record_id(domain)
        if last_record_id is not None:
            logging.info(f"Last record found {last_record_id} for domain {domain}, deleting..")
            await self._tw.delete_acme_record(domain, last_record_id)

        record_id = await self._tw.create_acme_record(domain, in_info.txt)
        logging.info(f"New record {record_id} for domain {domain}")
        await self._db_service.update_last_dns_record(domain, record_id)

        return app.domain.acme_dns_update.AcmeDnsUpdateOut(txt=in_info.txt)
