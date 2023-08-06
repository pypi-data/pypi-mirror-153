"""
Main interface for identitystore service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_identitystore import (
        Client,
        IdentityStoreClient,
    )

    session = Session()
    client: IdentityStoreClient = session.client("identitystore")
    ```
"""
from .client import IdentityStoreClient

Client = IdentityStoreClient


__all__ = ("Client", "IdentityStoreClient")
