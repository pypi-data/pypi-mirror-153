"""
Type annotations for migrationhub-config service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_migrationhub_config.client import MigrationHubConfigClient

    session = Session()
    client: MigrationHubConfigClient = session.client("migrationhub-config")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateHomeRegionControlResultTypeDef,
    DescribeHomeRegionControlsResultTypeDef,
    GetHomeRegionResultTypeDef,
    TargetTypeDef,
)

__all__ = ("MigrationHubConfigClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DryRunOperation: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class MigrationHubConfigClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubConfigClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#can_paginate)
        """

    def create_home_region_control(
        self, *, HomeRegion: str, Target: TargetTypeDef, DryRun: bool = ...
    ) -> CreateHomeRegionControlResultTypeDef:
        """
        This API sets up the home region for the calling account only.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.create_home_region_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#create_home_region_control)
        """

    def describe_home_region_controls(
        self,
        *,
        ControlId: str = ...,
        HomeRegion: str = ...,
        Target: TargetTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeHomeRegionControlsResultTypeDef:
        """
        This API permits filtering on the `ControlId` and `HomeRegion` fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.describe_home_region_controls)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#describe_home_region_controls)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#generate_presigned_url)
        """

    def get_home_region(self) -> GetHomeRegionResultTypeDef:
        """
        Returns the calling account’s home region, if configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig.Client.get_home_region)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/client/#get_home_region)
        """
