"""
Main interface for marketplacecommerceanalytics service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplacecommerceanalytics import (
        Client,
        MarketplaceCommerceAnalyticsClient,
    )

    session = Session()
    client: MarketplaceCommerceAnalyticsClient = session.client("marketplacecommerceanalytics")
    ```
"""
from .client import MarketplaceCommerceAnalyticsClient

Client = MarketplaceCommerceAnalyticsClient


__all__ = ("Client", "MarketplaceCommerceAnalyticsClient")
