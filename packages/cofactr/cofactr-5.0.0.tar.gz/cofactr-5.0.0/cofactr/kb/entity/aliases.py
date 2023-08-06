"""Functions for constructing a KB entity."""
# Standard Modules
from typing import Dict, List

# Local Modules
from app.kb.entity.types import Alias, Aliases


def aliases(
    aliases: List[Alias],  # pylint: disable=redefined-outer-name
) -> Aliases:
    """Create aliases.

    Args:
        aliases: Language, value pairs.

    Returns:
        Aliases in KB structure.
    """
    acc: Dict = {}

    for alias in aliases:
        lang = alias["language"]

        if alias["value"]:  # Don't propagate aliases with falsy values.
            acc[lang] = [*acc.get(lang, []), alias]

    return acc
