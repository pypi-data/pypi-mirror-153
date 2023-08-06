"""
Type annotations for iotsecuretunneling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotsecuretunneling.type_defs import CloseTunnelRequestRequestTypeDef

    data: CloseTunnelRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import ClientModeType, ConnectionStatusType, TunnelStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CloseTunnelRequestRequestTypeDef",
    "ConnectionStateTypeDef",
    "DescribeTunnelRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DestinationConfigTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ListTunnelsRequestRequestTypeDef",
    "TunnelSummaryTypeDef",
    "TimeoutConfigTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "OpenTunnelResponseTypeDef",
    "RotateTunnelAccessTokenResponseTypeDef",
    "RotateTunnelAccessTokenRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListTunnelsResponseTypeDef",
    "OpenTunnelRequestRequestTypeDef",
    "TunnelTypeDef",
    "DescribeTunnelResponseTypeDef",
)

_RequiredCloseTunnelRequestRequestTypeDef = TypedDict(
    "_RequiredCloseTunnelRequestRequestTypeDef",
    {
        "tunnelId": str,
    },
)
_OptionalCloseTunnelRequestRequestTypeDef = TypedDict(
    "_OptionalCloseTunnelRequestRequestTypeDef",
    {
        "delete": bool,
    },
    total=False,
)


class CloseTunnelRequestRequestTypeDef(
    _RequiredCloseTunnelRequestRequestTypeDef, _OptionalCloseTunnelRequestRequestTypeDef
):
    pass


ConnectionStateTypeDef = TypedDict(
    "ConnectionStateTypeDef",
    {
        "status": ConnectionStatusType,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

DescribeTunnelRequestRequestTypeDef = TypedDict(
    "DescribeTunnelRequestRequestTypeDef",
    {
        "tunnelId": str,
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

_RequiredDestinationConfigTypeDef = TypedDict(
    "_RequiredDestinationConfigTypeDef",
    {
        "services": List[str],
    },
)
_OptionalDestinationConfigTypeDef = TypedDict(
    "_OptionalDestinationConfigTypeDef",
    {
        "thingName": str,
    },
    total=False,
)


class DestinationConfigTypeDef(
    _RequiredDestinationConfigTypeDef, _OptionalDestinationConfigTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

ListTunnelsRequestRequestTypeDef = TypedDict(
    "ListTunnelsRequestRequestTypeDef",
    {
        "thingName": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

TunnelSummaryTypeDef = TypedDict(
    "TunnelSummaryTypeDef",
    {
        "tunnelId": str,
        "tunnelArn": str,
        "status": TunnelStatusType,
        "description": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

TimeoutConfigTypeDef = TypedDict(
    "TimeoutConfigTypeDef",
    {
        "maxLifetimeTimeoutMinutes": int,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

OpenTunnelResponseTypeDef = TypedDict(
    "OpenTunnelResponseTypeDef",
    {
        "tunnelId": str,
        "tunnelArn": str,
        "sourceAccessToken": str,
        "destinationAccessToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RotateTunnelAccessTokenResponseTypeDef = TypedDict(
    "RotateTunnelAccessTokenResponseTypeDef",
    {
        "tunnelArn": str,
        "sourceAccessToken": str,
        "destinationAccessToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRotateTunnelAccessTokenRequestRequestTypeDef = TypedDict(
    "_RequiredRotateTunnelAccessTokenRequestRequestTypeDef",
    {
        "tunnelId": str,
        "clientMode": ClientModeType,
    },
)
_OptionalRotateTunnelAccessTokenRequestRequestTypeDef = TypedDict(
    "_OptionalRotateTunnelAccessTokenRequestRequestTypeDef",
    {
        "destinationConfig": DestinationConfigTypeDef,
    },
    total=False,
)


class RotateTunnelAccessTokenRequestRequestTypeDef(
    _RequiredRotateTunnelAccessTokenRequestRequestTypeDef,
    _OptionalRotateTunnelAccessTokenRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

ListTunnelsResponseTypeDef = TypedDict(
    "ListTunnelsResponseTypeDef",
    {
        "tunnelSummaries": List[TunnelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OpenTunnelRequestRequestTypeDef = TypedDict(
    "OpenTunnelRequestRequestTypeDef",
    {
        "description": str,
        "tags": Sequence[TagTypeDef],
        "destinationConfig": DestinationConfigTypeDef,
        "timeoutConfig": TimeoutConfigTypeDef,
    },
    total=False,
)

TunnelTypeDef = TypedDict(
    "TunnelTypeDef",
    {
        "tunnelId": str,
        "tunnelArn": str,
        "status": TunnelStatusType,
        "sourceConnectionState": ConnectionStateTypeDef,
        "destinationConnectionState": ConnectionStateTypeDef,
        "description": str,
        "destinationConfig": DestinationConfigTypeDef,
        "timeoutConfig": TimeoutConfigTypeDef,
        "tags": List[TagTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

DescribeTunnelResponseTypeDef = TypedDict(
    "DescribeTunnelResponseTypeDef",
    {
        "tunnel": TunnelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
