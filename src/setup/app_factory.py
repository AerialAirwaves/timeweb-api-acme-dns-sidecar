import logging
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.views.health_check import HealthCheckView
from setup.dependencies import Dependencies
from setup.settings import AppSettings


class AppFactory:
    APP_TITLE = "ACME DNS Timeweb Sidecar"
    APP_SUMMARY = (
        "A sidecar, that mimics an acme-dns API server and allows to easily"
        " automate LetsEncrypt DNS-01 challenge for domains with Timeweb Cloud managed nameservers"
    )

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    def build(self) -> FastAPI:
        dependencies = Dependencies(self._settings)

        app = FastAPI(
            title=self.APP_TITLE,
            summary=self.APP_SUMMARY,
            docs_url="/docs" if self._settings.DOCS_ENABLED else None,
            redoc_url="/redoc" if self._settings.DOCS_ENABLED else None,
            openapi_url="/openapi.json" if self._settings.DOCS_ENABLED else None,
        )

        self.setup_routers(app, dependencies)
        self.setup_middlewares(app)
        return app

    def setup_routers(self, app: FastAPI, dependencies: Dependencies) -> None:
        app.include_router(HealthCheckView().router, prefix="/health")
        app.include_router(dependencies.acme_dns_update_view.router, prefix="")

    def setup_middlewares(self, app) -> None:
        # CORS
        origins = []

        # Set all CORS enabled origins : adding security between Backend and Frontend
        if self._settings.BACKEND_CORS_ORIGINS:
            origins_raw = self._settings.BACKEND_CORS_ORIGINS.split(",")

            for origin in origins_raw:
                use_origin = origin.strip()
                origins.append(use_origin)

            app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
