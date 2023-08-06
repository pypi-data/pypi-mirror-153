"""
Main interface for marketplace-catalog service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_catalog import (
        Client,
        MarketplaceCatalogClient,
    )

    session = Session()
    client: MarketplaceCatalogClient = session.client("marketplace-catalog")
    ```
"""
from .client import MarketplaceCatalogClient

Client = MarketplaceCatalogClient


__all__ = ("Client", "MarketplaceCatalogClient")
