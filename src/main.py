# from app.domain.logger import logger
import logging

import uvicorn

from setup.app_factory import AppFactory
from setup.logging import logging_format, setup_logging
from setup.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()

    setup_logging(settings.LOGGING_LEVEL)
    uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
    uvicorn_log_config["formatters"]["access"]["fmt"] = logging_format
    uvicorn_log_config["formatters"]["default"]["fmt"] = logging_format

    app_factory = AppFactory(settings)
    app = app_factory.build()

    logging.info("Starting uvicorn")
    uvicorn.run(app, host=settings.HOST, reload=settings.DEBUG, port=settings.PORT)
