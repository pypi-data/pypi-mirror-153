"""Cofactr graph API client."""
# Python Modules
from concurrent.futures import ThreadPoolExecutor
import json
from typing import List, Literal, Optional

# 3rd Party Modules
import urllib3

# Local Modules
from cofactr.schema import (
    OfferSchemaName,
    OrgSchemaName,
    ProductSchemaName,
    schema_to_offer,
    schema_to_org,
    schema_to_product,
)

Protocol = Literal["http", "https"]


drop_none_values = lambda d: {k: v for k, v in d.items() if v is not None}


def get_products(
    http, url, query, fields, before, after, limit, external, schema
):  # pylint: disable=too-many-arguments
    """Get products."""
    res = http.request(
        "GET",
        f"{url}/products",
        fields=drop_none_values(
            {
                "q": query,
                "fields": fields,
                "before": before,
                "after": after,
                "limit": limit,
                "external": external,
                "schema": schema,
            }
        ),
    )

    return json.loads(res.data.decode("utf-8"))


def get_orgs(
    http, url, query, before, after, limit, schema
):  # pylint: disable=too-many-arguments
    """Get orgs."""
    res = http.request(
        "GET",
        f"{url}/orgs",
        fields=drop_none_values(
            {
                "q": query,
                "before": before,
                "after": after,
                "limit": limit,
                "schema": schema,
            }
        ),
    )

    return json.loads(res.data.decode("utf-8"))


class GraphAPI:
    """A client-side representation of the Cofactr graph API."""

    PROTOCOL: Protocol = "https"
    HOST = "graph.cofactr.com"

    def __init__(
        self, protocol: Optional[Protocol] = PROTOCOL, host: Optional[str] = HOST
    ):

        self.url = f"{protocol}://{host}"
        self.http = urllib3.PoolManager()

    def check_health(self):
        """Check the operational status of the service."""

        res = self.http.request("GET", self.url)

        return json.loads(res.data.decode("utf-8"))

    def get_products(  # pylint: disable=too-many-arguments
        self,
        query: Optional[str] = None,
        fields: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        external: Optional[bool] = True,
        schema: ProductSchemaName = ProductSchemaName.FLAGSHIP,
    ):
        """Get products.

        Args:
            query: Search query.
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: "id,aliases,labels,statements{spec,assembly},offers"
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            external: Whether to query external sources.
            schema: Response schema.
        """

        res = get_products(
            http=self.http,
            url=self.url,
            query=query,
            fields=fields,
            external=external,
            before=before,
            after=after,
            limit=limit,
            schema=schema.value,
        )

        Product = schema_to_product[schema]  # pylint: disable=invalid-name

        res["data"] = [Product(**data) for data in res["data"]]

        return res

    def get_products_by_ids(
        self,
        ids: List[str],
        external: Optional[bool] = True,
        schema: ProductSchemaName = ProductSchemaName.FLAGSHIP,
    ):
        """Get a batch of products.

        Note:
            Will evolve to use a batched requests. Where, for example, each request
            contains 50 part IDs.
        """
        with ThreadPoolExecutor() as executor:
            return dict(
                zip(
                    ids,
                    executor.map(
                        lambda cpid: self.get_product(
                            id=cpid, external=external, schema=schema
                        ),
                        ids,
                    ),
                )
            )

    def get_orgs(  # pylint: disable=too-many-arguments
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        schema: OrgSchemaName = OrgSchemaName.FLAGSHIP,
    ):
        """Get organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            schema: Response schema.
        """

        res = get_orgs(
            http=self.http,
            url=self.url,
            query=query,
            before=before,
            after=after,
            limit=limit,
            schema=schema.value,
        )

        Org = schema_to_org[schema]  # pylint: disable=invalid-name

        res["data"] = [Org(**data) for data in res["data"]]

        return res

    def get_product(
        self,
        id: str,
        fields: Optional[str] = None,
        external: Optional[bool] = True,
        schema: ProductSchemaName = ProductSchemaName.FLAGSHIP,
    ):
        """Get product.

        Args:
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: "id,aliases,labels,statements{spec,assembly},offers"
            external: Whether to query external sources in order to update information for the
                given product.
            schema: Response schema.
        """

        res = json.loads(
            self.http.request(
                "GET",
                f"{self.url}/products/{id}",
                fields=drop_none_values(
                    {
                        "fields": fields,
                        "external": external,
                        "schema": schema.value,
                    }
                ),
            ).data.decode("utf-8")
        )

        Product = schema_to_product[schema]  # pylint: disable=invalid-name

        res["data"] = Product(**res["data"]) if (res and res.get("data")) else None

        return res

    def get_offers(
        self,
        product_id: str,
        fields: Optional[str] = None,
        external: Optional[bool] = True,
        schema: OfferSchemaName = OfferSchemaName.FLAGSHIP,
    ):
        """Get product.

        Args:
            product_id: ID of the product to get offers for.
            fields: Used to filter properties that the response should contain.
            external: Whether to query external sources in order to update information.
            schema: Response schema.
        """

        res = json.loads(
            self.http.request(
                "GET",
                f"{self.url}/products/{product_id}/offers",
                fields=drop_none_values(
                    {
                        "fields": fields,
                        "external": external,
                        "schema": schema.value,
                    }
                ),
            ).data.decode("utf-8")
        )

        Offer = schema_to_offer[schema]  # pylint: disable=invalid-name

        res["data"] = [Offer(**data) for data in res["data"]]

        return res

    def get_org(
        self,
        id: str,
        schema: OrgSchemaName = OrgSchemaName.FLAGSHIP,
    ):
        """Get organization."""

        res = json.loads(
            self.http.request(
                "GET",
                f"{self.url}/orgs/{id}",
                fields=drop_none_values({"schema": schema.value}),
            ).data.decode("utf-8")
        )

        Org = schema_to_org[schema]  # pylint: disable=invalid-name

        res["data"] = Org(**res["data"]) if (res and res.get("data")) else None

        return res
