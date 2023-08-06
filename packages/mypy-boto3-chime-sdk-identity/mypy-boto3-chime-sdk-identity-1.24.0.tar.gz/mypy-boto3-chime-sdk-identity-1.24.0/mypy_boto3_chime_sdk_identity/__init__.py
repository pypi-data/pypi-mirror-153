"""
Main interface for chime-sdk-identity service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_identity import (
        ChimeSDKIdentityClient,
        Client,
    )

    session = Session()
    client: ChimeSDKIdentityClient = session.client("chime-sdk-identity")
    ```
"""
from .client import ChimeSDKIdentityClient

Client = ChimeSDKIdentityClient


__all__ = ("ChimeSDKIdentityClient", "Client")
