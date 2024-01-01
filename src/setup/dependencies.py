from functools import cached_property

from app.domain.acme_dns_update import AcmeDnsUpdateService
from app.domain.auth import AuthService
from app.domain.cbv import ClassBasedView
from app.domain.db import DatabaseService
from app.services.auth_simple import SimpleAuthService
from app.services.database_tinydb import TinyDBDatabaseService
from app.services.tw_acme_dns_update import TimewebACMEDnsUpdateService
from app.services.tw_api import TimewebAPIService
from app.views.acme_dns_update import ACMEDnsUpdateView
from setup.settings import AppSettings


class Dependencies:
    def __init__(self, config: AppSettings):
        self._config = config

    @cached_property
    def auth_service(self) -> AuthService:
        return SimpleAuthService(
            self._config.MANAGED_DOMAIN, self._config.UPDATE_USERNAME, self._config.UPDATE_PASSWORD
        )

    @cached_property
    def db_service(self) -> DatabaseService:
        return TinyDBDatabaseService(self._config.DB_PATH)

    @cached_property
    def timeweb_api_service(self) -> TimewebAPIService:
        return TimewebAPIService(self._config.TIMEWEB_API_TOKEN)

    @cached_property
    def acme_dns_update_service(self) -> AcmeDnsUpdateService:
        return TimewebACMEDnsUpdateService(self.auth_service, self.db_service, self.timeweb_api_service)

    @cached_property
    def acme_dns_update_view(self) -> ClassBasedView:
        return ACMEDnsUpdateView(self.acme_dns_update_service)
