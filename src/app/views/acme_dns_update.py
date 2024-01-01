from functools import cached_property
from typing import Annotated, Any, Dict

from fastapi import APIRouter, Header, HTTPException

import app.domain.acme_dns_update
from app.domain.acme_dns_update import AcmeDnsUpdateService
from app.domain.auth import UnauthorizedError
from app.domain.cbv import ClassBasedView


class ACMEDnsUpdateView(ClassBasedView):
    def __init__(self, acme_dns_service: AcmeDnsUpdateService) -> None:
        self._acme_dns_service = acme_dns_service

    @cached_property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["ACME DNS Update"])
        router.add_api_route("/update", self.update, methods=["POST"])
        return router

    async def update(
        self,
        in_info: app.domain.acme_dns_update.AcmeDnsUpdateIn,
        x_api_user: Annotated[str, Header()],
        x_api_key: Annotated[str, Header()],
    ) -> app.domain.acme_dns_update.AcmeDnsUpdateOut:
        try:
            return await self._acme_dns_service.update(x_api_user, x_api_key, in_info)
        except UnauthorizedError:
            raise HTTPException(status_code=401, detail="Unauthorized")
