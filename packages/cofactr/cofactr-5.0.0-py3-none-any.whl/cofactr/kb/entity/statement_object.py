"""Functions for constructing a KB entity."""
# Standard Modules
from typing import Dict, List, Optional

# Local Modules
from app.kb.entity.types import (
    Property,
    Rank,
    Reference,
    Snak,
    StatementObject,
    Type,
)


def statement_object(  # pylint: disable=too-many-arguments
    mainsnak: Snak,
    qualifiers: Optional[Dict[str, List[Snak]]] = None,
    qualifers_order: Optional[List[Property]] = None,
    type: Type = "statement",  # pylint: disable=redefined-builtin
    rank: Rank = "normal",
    references: Optional[List[Reference]] = None,
) -> StatementObject:
    """Create statement object."""

    return StatementObject(
        mainsnak=mainsnak,
        qualifiers=qualifiers or {},
        qualifiers_order=qualifers_order or [],
        type=type,
        rank=rank,
        references=references or [],
    )
