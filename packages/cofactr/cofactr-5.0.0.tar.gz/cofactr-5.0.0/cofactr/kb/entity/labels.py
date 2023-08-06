"""Functions for constructing a KB entity."""
# Standard Modules
from typing import List

# Local Modules
from app.kb.entity.types import Alias, Labels


def labels(aliases: List[Alias]) -> Labels:
    """Create labels.

    Args:
        aliases: Language, value pairs.

    Returns:
        Labels in KB structure.
    """
    return {alias["language"]: alias for alias in aliases}
