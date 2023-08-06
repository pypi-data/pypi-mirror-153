"""
Type annotations for apigatewaymanagementapi service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewaymanagementapi/type_defs/)

Usage::

    ```python
    from mypy_boto3_apigatewaymanagementapi.type_defs import DeleteConnectionRequestRequestTypeDef

    data: DeleteConnectionRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DeleteConnectionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetConnectionRequestRequestTypeDef",
    "IdentityTypeDef",
    "PostToConnectionRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetConnectionResponseTypeDef",
)

DeleteConnectionRequestRequestTypeDef = TypedDict(
    "DeleteConnectionRequestRequestTypeDef",
    {
        "ConnectionId": str,
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

GetConnectionRequestRequestTypeDef = TypedDict(
    "GetConnectionRequestRequestTypeDef",
    {
        "ConnectionId": str,
    },
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "SourceIp": str,
        "UserAgent": str,
    },
)

PostToConnectionRequestRequestTypeDef = TypedDict(
    "PostToConnectionRequestRequestTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
        "ConnectionId": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectionResponseTypeDef = TypedDict(
    "GetConnectionResponseTypeDef",
    {
        "ConnectedAt": datetime,
        "Identity": IdentityTypeDef,
        "LastActiveAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
