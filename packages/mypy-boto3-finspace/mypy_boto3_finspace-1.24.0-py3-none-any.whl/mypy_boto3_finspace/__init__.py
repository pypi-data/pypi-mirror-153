"""
Main interface for finspace service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace import (
        Client,
        finspaceClient,
    )

    session = Session()
    client: finspaceClient = session.client("finspace")
    ```
"""
from .client import finspaceClient

Client = finspaceClient


__all__ = ("Client", "finspaceClient")
