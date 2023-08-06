"""Helper functions."""
# Standard Modules
from functools import reduce
from operator import getitem
from typing import List

# Local Modules
from cofactr.kb.entity.types import Mainsnak


def get_path(data, keys, default=None):
    """Access a nested dictionary."""
    try:
        return reduce(getitem, keys, data)
    except (KeyError, IndexError):
        return default


def find_preferred(data: List[Mainsnak], default=None):
    """Find preferred value."""
    return next(
        (x for x in data if x.get("rank") == "preferred"), data[0] if data else default
    )


def drop_deprecated(data: List[Mainsnak]):
    """Drop deprecated values."""
    return filter(lambda x: x.get("rank") == "deprecated", data)


identity = lambda x: x
