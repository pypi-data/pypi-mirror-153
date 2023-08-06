"""
Type annotations for route53-recovery-cluster service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_cluster.type_defs import GetRoutingControlStateRequestRequestTypeDef

    data: GetRoutingControlStateRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import RoutingControlStateType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "GetRoutingControlStateRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "ListRoutingControlsRequestRequestTypeDef",
    "RoutingControlTypeDef",
    "UpdateRoutingControlStateEntryTypeDef",
    "UpdateRoutingControlStateRequestRequestTypeDef",
    "GetRoutingControlStateResponseTypeDef",
    "ListRoutingControlsRequestListRoutingControlsPaginateTypeDef",
    "ListRoutingControlsResponseTypeDef",
    "UpdateRoutingControlStatesRequestRequestTypeDef",
)

GetRoutingControlStateRequestRequestTypeDef = TypedDict(
    "GetRoutingControlStateRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
    },
)

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

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListRoutingControlsRequestRequestTypeDef = TypedDict(
    "ListRoutingControlsRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

RoutingControlTypeDef = TypedDict(
    "RoutingControlTypeDef",
    {
        "ControlPanelArn": str,
        "ControlPanelName": str,
        "RoutingControlArn": str,
        "RoutingControlName": str,
        "RoutingControlState": RoutingControlStateType,
    },
    total=False,
)

UpdateRoutingControlStateEntryTypeDef = TypedDict(
    "UpdateRoutingControlStateEntryTypeDef",
    {
        "RoutingControlArn": str,
        "RoutingControlState": RoutingControlStateType,
    },
)

_RequiredUpdateRoutingControlStateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRoutingControlStateRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
        "RoutingControlState": RoutingControlStateType,
    },
)
_OptionalUpdateRoutingControlStateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRoutingControlStateRequestRequestTypeDef",
    {
        "SafetyRulesToOverride": Sequence[str],
    },
    total=False,
)

class UpdateRoutingControlStateRequestRequestTypeDef(
    _RequiredUpdateRoutingControlStateRequestRequestTypeDef,
    _OptionalUpdateRoutingControlStateRequestRequestTypeDef,
):
    pass

GetRoutingControlStateResponseTypeDef = TypedDict(
    "GetRoutingControlStateResponseTypeDef",
    {
        "RoutingControlArn": str,
        "RoutingControlState": RoutingControlStateType,
        "RoutingControlName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutingControlsRequestListRoutingControlsPaginateTypeDef = TypedDict(
    "ListRoutingControlsRequestListRoutingControlsPaginateTypeDef",
    {
        "ControlPanelArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRoutingControlsResponseTypeDef = TypedDict(
    "ListRoutingControlsResponseTypeDef",
    {
        "RoutingControls": List[RoutingControlTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateRoutingControlStatesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRoutingControlStatesRequestRequestTypeDef",
    {
        "UpdateRoutingControlStateEntries": Sequence[UpdateRoutingControlStateEntryTypeDef],
    },
)
_OptionalUpdateRoutingControlStatesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRoutingControlStatesRequestRequestTypeDef",
    {
        "SafetyRulesToOverride": Sequence[str],
    },
    total=False,
)

class UpdateRoutingControlStatesRequestRequestTypeDef(
    _RequiredUpdateRoutingControlStatesRequestRequestTypeDef,
    _OptionalUpdateRoutingControlStatesRequestRequestTypeDef,
):
    pass
