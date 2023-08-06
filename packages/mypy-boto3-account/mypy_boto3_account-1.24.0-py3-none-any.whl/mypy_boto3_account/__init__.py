"""
Main interface for account service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_account import (
        AccountClient,
        Client,
    )

    session = Session()
    client: AccountClient = session.client("account")
    ```
"""
from .client import AccountClient

Client = AccountClient


__all__ = ("AccountClient", "Client")
