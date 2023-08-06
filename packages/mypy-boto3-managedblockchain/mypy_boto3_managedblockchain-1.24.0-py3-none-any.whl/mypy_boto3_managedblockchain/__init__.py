"""
Main interface for managedblockchain service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_managedblockchain import (
        Client,
        ManagedBlockchainClient,
    )

    session = Session()
    client: ManagedBlockchainClient = session.client("managedblockchain")
    ```
"""
from .client import ManagedBlockchainClient

Client = ManagedBlockchainClient


__all__ = ("Client", "ManagedBlockchainClient")
