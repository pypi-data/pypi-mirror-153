"""
Main interface for mediastore-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediastore_data import (
        Client,
        ListItemsPaginator,
        MediaStoreDataClient,
    )

    session = Session()
    client: MediaStoreDataClient = session.client("mediastore-data")

    list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```
"""
from .client import MediaStoreDataClient
from .paginator import ListItemsPaginator

Client = MediaStoreDataClient


__all__ = ("Client", "ListItemsPaginator", "MediaStoreDataClient")
