"""
Main interface for sso-oidc service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sso_oidc import (
        Client,
        SSOOIDCClient,
    )

    session = Session()
    client: SSOOIDCClient = session.client("sso-oidc")
    ```
"""
from .client import SSOOIDCClient

Client = SSOOIDCClient


__all__ = ("Client", "SSOOIDCClient")
