"""
Type annotations for migrationhub-config service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/type_defs/)

Usage::

    ```python
    from mypy_boto3_migrationhub_config.type_defs import TargetTypeDef

    data: TargetTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TargetTypeDef",
    "ResponseMetadataTypeDef",
    "CreateHomeRegionControlRequestRequestTypeDef",
    "DescribeHomeRegionControlsRequestRequestTypeDef",
    "HomeRegionControlTypeDef",
    "GetHomeRegionResultTypeDef",
    "CreateHomeRegionControlResultTypeDef",
    "DescribeHomeRegionControlsResultTypeDef",
)

_RequiredTargetTypeDef = TypedDict(
    "_RequiredTargetTypeDef",
    {
        "Type": Literal["ACCOUNT"],
    },
)
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "Id": str,
    },
    total=False,
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateHomeRegionControlRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHomeRegionControlRequestRequestTypeDef",
    {
        "HomeRegion": str,
        "Target": TargetTypeDef,
    },
)
_OptionalCreateHomeRegionControlRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHomeRegionControlRequestRequestTypeDef",
    {
        "DryRun": bool,
    },
    total=False,
)


class CreateHomeRegionControlRequestRequestTypeDef(
    _RequiredCreateHomeRegionControlRequestRequestTypeDef,
    _OptionalCreateHomeRegionControlRequestRequestTypeDef,
):
    pass


DescribeHomeRegionControlsRequestRequestTypeDef = TypedDict(
    "DescribeHomeRegionControlsRequestRequestTypeDef",
    {
        "ControlId": str,
        "HomeRegion": str,
        "Target": TargetTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

HomeRegionControlTypeDef = TypedDict(
    "HomeRegionControlTypeDef",
    {
        "ControlId": str,
        "HomeRegion": str,
        "Target": TargetTypeDef,
        "RequestedTime": datetime,
    },
    total=False,
)

GetHomeRegionResultTypeDef = TypedDict(
    "GetHomeRegionResultTypeDef",
    {
        "HomeRegion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHomeRegionControlResultTypeDef = TypedDict(
    "CreateHomeRegionControlResultTypeDef",
    {
        "HomeRegionControl": HomeRegionControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHomeRegionControlsResultTypeDef = TypedDict(
    "DescribeHomeRegionControlsResultTypeDef",
    {
        "HomeRegionControls": List[HomeRegionControlTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
