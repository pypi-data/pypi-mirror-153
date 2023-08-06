""":obj:`Pydantic` schemas representing a :obj:`Card` for validation and serialisation.

For further details on the internal attributes and implementation see the original
`arkhamdb github repository`_.

.. _arkhamdb github repository: https://github.com/Kamalisk/arkhamdb/blob/arkham/src/AppBundle/Entity/Card.php

"""
from pydantic import BaseModel


class Card(BaseModel):
    """Represents a single :obj:`Card`. See the `arkhamdb github repository`_ for more information on the original implementation at source.

    The following fields are mandatory:

    - code (:obj:`str`)
    - position (:obj:`int`)
    - quantity (:obj:`int`)
    - name (:obj:`str`)

    All other fields seem to be optional.

    .. _arkhamdb github repository: https://github.com/Kamalisk/arkhamdb/blob/arkham/src/AppBundle/Entity/Card.php
    """

    code: str
    position: int
    quantity: int
    name: str
