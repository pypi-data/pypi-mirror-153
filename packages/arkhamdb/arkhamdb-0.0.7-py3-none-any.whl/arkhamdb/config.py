"""Contains configuration processing options for the library."""
import logging
from logging import Logger
from typing import Any, Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    """Configuration base class using :class:`pydantic.BaseSettings`.

    Environment variables prefixed with :obj:`ARKHAM_` will be mapped against their matching
    attributes.

    Attributes:
        LOG_LEVEL (str): Level for application logging output. Default is :obj:`INFO`. Other
            valid options (found within the :obj:`logging` module) are :obj:`WARN`, :obj:`DEBUG`
        API_ROOT (str): Root URL for the ArkhamDB API. Defaults to `arkhamdb.com/api`_ but can
            be overridden for testing and other purposes.

    .. _arkhamdb.com/api: https://arkhamdb.com/api
    """

    # ----- Logging
    LOG_LEVEL: str = "INFO"
    LOGGER: Optional[Logger]
    # ----- Core Application
    API_ROOT: str = "https://arkhamdb.com/api"

    def _init_logging(self) -> Logger:
        """Configures and returns an instance of :class:`logging.Logger`."""
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=format)
        log: Logger = logging.getLogger("ArkhamDB")
        log.setLevel(self.LOG_LEVEL)
        return log

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Creates a new `Config` and initialises an associated `Logger`."""
        super().__init__(*args, **kwargs)
        self.LOGGER = self._init_logging()

    class Config:
        """Auto-configures pydantic for pulling through the environment variables prefixed with :obj:`ARKHAM`."""

        env_prefix = "ARKHAM_"
