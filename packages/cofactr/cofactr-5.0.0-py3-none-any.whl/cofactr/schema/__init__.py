"""Schema definitions."""
# Standard Modules
from enum import Enum

# Local Modules
from cofactr.helpers import identity
from cofactr.schema.flagship.offer import Offer as FlagshipOffer
from cofactr.schema.logistics.offer import Offer as LogisticsOffer
from cofactr.schema.flagship.part import Part as FlagshipPart
from cofactr.schema.logistics.part import Part as LogisticsPart
from cofactr.schema.flagship.seller import Seller as FlagshipSeller


class ProductSchemaName(str, Enum):
    """Product schema name."""

    INTERNAL = "internal"
    FLAGSHIP = "flagship"
    LOGISTICS = "logistics"


schema_to_product = {
    ProductSchemaName.INTERNAL: identity,
    ProductSchemaName.FLAGSHIP: FlagshipPart,
    ProductSchemaName.LOGISTICS: LogisticsPart,
}


class OfferSchemaName(str, Enum):
    """Offer schema name."""

    INTERNAL = "internal"
    FLAGSHIP = "flagship"
    LOGISTICS = "logistics"


schema_to_offer = {
    OfferSchemaName.INTERNAL: identity,
    OfferSchemaName.FLAGSHIP: FlagshipOffer,
    OfferSchemaName.LOGISTICS: LogisticsOffer,
}


class OrgSchemaName(str, Enum):
    """Organization schema name."""

    INTERNAL = "internal"
    FLAGSHIP = "flagship"
    LOGISTICS = "logistics"


schema_to_org = {
    OrgSchemaName.INTERNAL: identity,
    OrgSchemaName.FLAGSHIP: FlagshipSeller,
    OrgSchemaName.LOGISTICS: FlagshipSeller,
}
