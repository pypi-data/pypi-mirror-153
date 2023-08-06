"""
Main interface for appintegrations service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appintegrations import (
        AppIntegrationsServiceClient,
        Client,
    )

    session = Session()
    client: AppIntegrationsServiceClient = session.client("appintegrations")
    ```
"""
from .client import AppIntegrationsServiceClient

Client = AppIntegrationsServiceClient


__all__ = ("AppIntegrationsServiceClient", "Client")
