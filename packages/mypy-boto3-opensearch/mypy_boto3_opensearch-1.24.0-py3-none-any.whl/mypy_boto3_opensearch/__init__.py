"""
Main interface for opensearch service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearch import (
        Client,
        OpenSearchServiceClient,
    )

    session = Session()
    client: OpenSearchServiceClient = session.client("opensearch")
    ```
"""
from .client import OpenSearchServiceClient

Client = OpenSearchServiceClient


__all__ = ("Client", "OpenSearchServiceClient")
