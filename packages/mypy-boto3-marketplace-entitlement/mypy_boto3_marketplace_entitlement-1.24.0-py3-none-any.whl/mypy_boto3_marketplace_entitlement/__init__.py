"""
Main interface for marketplace-entitlement service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_entitlement import (
        Client,
        GetEntitlementsPaginator,
        MarketplaceEntitlementServiceClient,
    )

    session = Session()
    client: MarketplaceEntitlementServiceClient = session.client("marketplace-entitlement")

    get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```
"""
from .client import MarketplaceEntitlementServiceClient
from .paginator import GetEntitlementsPaginator

Client = MarketplaceEntitlementServiceClient


__all__ = ("Client", "GetEntitlementsPaginator", "MarketplaceEntitlementServiceClient")
