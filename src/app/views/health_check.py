from functools import cached_property
from typing import Any, Dict

from fastapi import APIRouter

from app.domain.cbv import ClassBasedView


class HealthCheckView(ClassBasedView):
    @cached_property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Health Check"])
        router.add_api_route("", self.health_check, methods=["GET"])
        return router

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "ok"}
