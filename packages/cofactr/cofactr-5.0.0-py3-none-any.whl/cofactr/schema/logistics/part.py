"""Part class."""
# Standard Modules
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, TypedDict

# Local Modules
from cofactr.schema.types import Document


class Spec(TypedDict):
    """Specification."""

    type: Literal[
        "boolean",
        "external_id",
        "monolingual_text",
        "quantity",
        "url",
        "time",
        "kb_item",
    ]
    unit: Optional[str]
    value: Any
    display: str


@dataclass
class Part:  # pylint: disable=too-many-instance-attributes
    """Part."""

    id: str

    classification: Optional[str]
    description: Optional[str]
    documents: List[Document]
    hero_image: Optional[str]
    mpn: Optional[str]
    mfr: Optional[str]  # manufacturer name.
    msl: Optional[int]  # Num of hours until a bake is required.
    package: Optional[str]
    specs: List[Dict[Literal["id", "label", "value"], str]]
    terminations: Optional[int]

    updated_at: Optional[str]

    # def calc_overage(quant: int) -> int:
    #     return quant
