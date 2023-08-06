"""Types defining KB entities."""
# Standard Modules
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

Property = str


class Alias(TypedDict):
    """Alias in KB structure."""

    language: str  # Country code.
    value: str  # Alias name.


Aliases = Dict[str, List[Alias]]

Labels = Dict[str, Alias]

SnakType = Literal["value"]
DataType = Literal[
    "boolean",
    "external_id",
    "monolingual_text",
    "quantity",
    "url",
    "time",
]
# "number", "string", { "amount": number, "unit": str }, etc.
DataValue = Dict[str, Any]


class Snak(TypedDict):
    """S.N.A.K. (Some Notation About Knowledge)."""

    snaktype: SnakType
    property: Property
    datavalue: DataValue
    datatype: DataType


Mainsnak = Snak


Qualifier = Dict[str, List[Snak]]

Rank = Literal["preferred", "normal", "deprecated"]
Type = Literal["statement"]


Snaks = Dict[Property, List[Snak]]
SnaksOrder = List[Property]


class Reference(TypedDict):
    """Reference."""

    snaks: Snaks
    snaks_order: SnaksOrder


class StatementObject(TypedDict):
    """Statement Object."""

    mainsnak: Snak
    qualifiers: Dict[str, List[Snak]]
    qualifiers_order: List[Property]
    type: Type
    rank: Rank
    references: List[Reference]


Statements = Dict[Property, List[StatementObject]]


class PricePoint(TypedDict):
    """Price in a specific currency + quantity.

    Based on https://octopart.com/api/v4/reference#pricepoint
    """

    # Minimum purchase quantity to get this price (aka price break).
    quantity: NotRequired[int]
    # Price in currency.
    price: NotRequired[float]
    # Currency for price.
    currency: NotRequired[str]
    # Currency for converted_price. Will match value of currency argument.
    converted_currency: NotRequired[str]
    # Price converted to user's currency using foreign exchange rates.
    converted_price: NotRequired[float]
    # The exchange rate used to calculate converted_price.
    conversion_rate: NotRequired[float]


class Offer(TypedDict):
    """A specific buyable part from a distributor.

    Based on https://octopart.com/api/v4/reference#offer
    """

    # Stock Keeping Unit used internally by distributor.
    sku: NotRequired[str]
    # The geo-political region(s) for which the offer is valid.
    eligible_region: NotRequired[Optional[str]]
    # Number of units available to be shipped (aka Stock, Quantity).
    inventory_level: NotRequired[int]
    # Packaging of parts (eg Tape, Reel).
    packaging: NotRequired[Optional[str]]
    # Minimum Order Quantity: smallest number of parts that can be
    # purchased.
    moq: NotRequired[int]
    prices: NotRequired[List[PricePoint]]
    # The URL to view offer on distributor website. This will
    # redirect via Octopart's server.
    click_url: NotRequired[str]
    # The last time data was fetched from external sources.
    updated_at: NotRequired[Optional[datetime]]
    # Number of days to acquire parts from factory.
    factory_lead_days: NotRequired[Optional[int]]
    # Number of parts on order from factory.
    on_order_quantity: NotRequired[Optional[int]]
    # Order multiple for factory orders.
    factory_pack_quantity: NotRequired[Optional[int]]
    # Number of items which must be ordered together.
    order_multiple: NotRequired[Optional[int]]
    # The quantity of parts as packaged by the seller.
    multipack_quantity: NotRequired[Optional[int]]


class Entity(TypedDict):
    """Entity."""

    aliases: NotRequired[Aliases]
    id: NotRequired[str]
    internal: NotRequired[Dict[str, Any]]
    labels: NotRequired[Labels]
    modified: NotRequired[datetime]
    statements: NotRequired[Statements]


class Seller(Entity):
    """Seller entity."""


class OfferGroup(TypedDict):
    """Offer group."""

    seller: Seller
    offers: List[Offer]


class Product(Entity):
    """Product entity."""

    offers: NotRequired[List[OfferGroup]]
