"""
Main interface for cognito-sync service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cognito_sync import (
        Client,
        CognitoSyncClient,
    )

    session = Session()
    client: CognitoSyncClient = session.client("cognito-sync")
    ```
"""
from .client import CognitoSyncClient

Client = CognitoSyncClient


__all__ = ("Client", "CognitoSyncClient")
