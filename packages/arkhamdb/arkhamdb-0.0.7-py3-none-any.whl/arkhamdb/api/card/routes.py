"""Contains logic for interacting with the :obj:`Card` routes in the API.

See: https://arkhamdb.com/api/doc#section-Card
"""
from httpx import AsyncClient, Response


async def get_card(card_code: str, client: AsyncClient) -> Response:
    """Returns a response from :obj:`/api/public/card/{card_code}`. This contains an individual card.

    Args:
        card_code (str): the identifying code for the card. Eg. '01001'
        client (AsyncClient): an instance of a :class:`httpx.AsyncClient`

    Returns:
        :class:`httpx.Response`
    """
    res: Response = await client.get(f"public/card/{card_code}")
    return res


async def get_all_cards(client: AsyncClient) -> Response:
    """Returns a response from :obj:`/api/public/cards`. This contains all the cards in the database.

    Args:
        client (AsyncClient): an instance of a :obj:`httpx.AsyncClient`

    Returns:
        :class:`httpx.Response`
    """
    res: Response = await client.get("public/cards/")
    return res


async def get_pack(pack_code: str, client: AsyncClient) -> Response:
    """Returns a response from :obj:`/api/public/cards/{pack_code}/`. This contains all the cards in the database where they are from this pack.

    Args:
        pack_code (str): the code for the pack, eg. 'core'
        client (AsyncClient): an instance of a :obj:`httpx.AsyncClient`

    Returns:
        :class:`httpx.Response`
    """
    res: Response = await client.get(f"public/cards/{pack_code}")
    return res
