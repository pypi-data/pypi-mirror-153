""":obj:`Pydantic` schemas representing a :obj:`Decklist` for validation and serialisation.

For further details on the internal attributes and implementation see the original
`arkhamdb github repository`_.

.. _arkhamdb github repository: https://github.com/Kamalisk/arkhamdb/blob/arkham/src/AppBundle/Entity/Decklist.php
"""
from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class DeckList(BaseModel):
    """Represents a single :obj:`Decklist`. See the `arkhamdb github repository`_ for more information on the original implementation at source.

    The following fields are mandatory:

    - id (:obj:`int`)
    - name (:obj:`str`)
    - date_creation (:obj:`datetime`)
    - date_update (:obj:`datetime`)
    - description_md: (:obj:`str`)
    - user_id (:obj:`int`)
    - investigator_code (:obj:`str`)
    - investigator_name (:obj:`str`)
    - slots (:obj:`dict[str, int]`) - dictionary with keys for :obj:`card_code` as a foreign key for :class:`arkhamdb.api.card.schemas.Card` and an :obj:`int` for the number of instances of that card

    All other fields seem to be optional.

    .. _arkhamdb github repository: https://github.com/Kamalisk/arkhamdb/blob/arkham/src/AppBundle/Entity/Decklist.php
    """

    id: int
    name: str
    date_creation: datetime
    date_update: datetime
    description_md: str
    user_id: int
    investigator_code: str
    investigator_name: str
    slots: Dict[str, int]
