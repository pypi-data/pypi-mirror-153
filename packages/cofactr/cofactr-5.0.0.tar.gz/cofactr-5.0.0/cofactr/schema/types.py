"""Types for use in schema definitions."""
# Standard Modules
from typing import TypedDict


class Document(TypedDict):
    """Document."""

    label: str
    url: str
    filename: str
