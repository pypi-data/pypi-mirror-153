"""
Main interface for migrationhub-config service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_migrationhub_config import (
        Client,
        MigrationHubConfigClient,
    )

    session = Session()
    client: MigrationHubConfigClient = session.client("migrationhub-config")
    ```
"""
from .client import MigrationHubConfigClient

Client = MigrationHubConfigClient


__all__ = ("Client", "MigrationHubConfigClient")
