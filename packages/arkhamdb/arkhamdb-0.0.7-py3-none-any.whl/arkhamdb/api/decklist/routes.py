"""Contains logic for interacting with the :obj:`Decklist` routes in the API.

See: https://arkhamdb.com/api/doc#section-Decklist
"""
from datetime import datetime

from httpx import AsyncClient, Response


async def get_decklist(decklist_id: int, client: AsyncClient) -> Response:
    """Returns a response from :obj:`public/decklist/{decklist_id}`. This contains an individual decklist.

    Args:
        decklist_id (int): the identifying code for the decklist. Eg. 101
        client (AsyncClient): an instance of a :class:`httpx.AsyncClient`

    Returns:
        :class:`httpx.Response`
    """
    res: Response = await client.get(f"public/decklist/{decklist_id}")
    return res


async def get_decklists_by_date(date: datetime, client: AsyncClient) -> Response:
    """Returns a response from :obj:`public/decklists/by_date/{date}`. This contains a list of decks..

    Args:
        date (datetime): the datetime for which we want to query all the decklists published
        client (AsyncClient): an instance of a :class:`httpx.AsyncClient`

    Returns:
        :class:`httpx.Response`
    """
    datestr = date.strftime("%Y-%m-%d")
    res: Response = await client.get(f"public/decklists/by_date/{datestr}")
    return res
