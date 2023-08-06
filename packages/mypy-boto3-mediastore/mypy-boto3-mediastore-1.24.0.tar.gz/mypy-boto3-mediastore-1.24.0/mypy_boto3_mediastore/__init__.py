"""
Main interface for mediastore service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediastore import (
        Client,
        ListContainersPaginator,
        MediaStoreClient,
    )

    session = Session()
    client: MediaStoreClient = session.client("mediastore")

    list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```
"""
from .client import MediaStoreClient
from .paginator import ListContainersPaginator

Client = MediaStoreClient


__all__ = ("Client", "ListContainersPaginator", "MediaStoreClient")
