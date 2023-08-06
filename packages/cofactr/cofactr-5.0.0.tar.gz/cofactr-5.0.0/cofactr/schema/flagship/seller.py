"""Part seller class."""
# Standard Modules
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class Seller:  # pylint: disable=too-many-instance-attributes
    """Part seller."""

    id: str
    label: str
    aliases: List[str]
    authenticity_score: Optional[int]
    availability_score: Optional[int]
    additional_markup: Optional[float]
    additional_fee: Optional[float]
    certifications: List[str]
    #  A separate flag that's independent from accuracy.
    is_buyable: bool
    lead: Optional[int]
    free_ship: Dict[Literal["threshold", "shipping_lead"], Optional[int]]
    shipping_options: List[Dict[Literal["price", "shipping_lead"], int]]
