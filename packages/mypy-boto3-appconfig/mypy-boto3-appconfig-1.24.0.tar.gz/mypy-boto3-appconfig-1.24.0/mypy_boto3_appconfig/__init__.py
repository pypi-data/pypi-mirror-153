"""
Main interface for appconfig service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appconfig import (
        AppConfigClient,
        Client,
    )

    session = Session()
    client: AppConfigClient = session.client("appconfig")
    ```
"""
from .client import AppConfigClient

Client = AppConfigClient


__all__ = ("AppConfigClient", "Client")
