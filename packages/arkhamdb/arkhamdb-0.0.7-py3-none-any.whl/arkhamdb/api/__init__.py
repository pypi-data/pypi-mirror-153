"""All logic for interacting with the ArkhamDB external API."""
from typing import Optional

from arkhamdb.config import Config
from httpx import AsyncClient


async def APIClient(config: Optional[Config] = None) -> AsyncClient:
    """Creates and returns a :class:`httpx.AsyncClient` based on a given configuration.

    Args:
        config (:obj:`Config`, optional): A :class:`arkhamdb.config.Config` configuration object.
            If none provided a default will be initialised via :obj:`arkhamdb.config.Config.__init__`.

    Returns:
        AsyncClient
    """
    if not config:
        config = Config()
    return AsyncClient(
        base_url=config.API_ROOT,
        headers={"Content-Type": "application/json"},
    )
