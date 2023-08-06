"""
Type annotations for cloudcontrol service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudcontrol.type_defs import CancelResourceRequestInputRequestTypeDef

    data: CancelResourceRequestInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import HandlerErrorCodeType, OperationStatusType, OperationType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelResourceRequestInputRequestTypeDef",
    "ProgressEventTypeDef",
    "ResponseMetadataTypeDef",
    "CreateResourceInputRequestTypeDef",
    "DeleteResourceInputRequestTypeDef",
    "GetResourceInputRequestTypeDef",
    "ResourceDescriptionTypeDef",
    "GetResourceRequestStatusInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceRequestStatusFilterTypeDef",
    "ListResourcesInputRequestTypeDef",
    "UpdateResourceInputRequestTypeDef",
    "CancelResourceRequestOutputTypeDef",
    "CreateResourceOutputTypeDef",
    "DeleteResourceOutputTypeDef",
    "GetResourceRequestStatusOutputTypeDef",
    "ListResourceRequestsOutputTypeDef",
    "UpdateResourceOutputTypeDef",
    "GetResourceOutputTypeDef",
    "ListResourcesOutputTypeDef",
    "GetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef",
    "ListResourcesInputListResourcesPaginateTypeDef",
    "ListResourceRequestsInputListResourceRequestsPaginateTypeDef",
    "ListResourceRequestsInputRequestTypeDef",
)

CancelResourceRequestInputRequestTypeDef = TypedDict(
    "CancelResourceRequestInputRequestTypeDef",
    {
        "RequestToken": str,
    },
)

ProgressEventTypeDef = TypedDict(
    "ProgressEventTypeDef",
    {
        "TypeName": str,
        "Identifier": str,
        "RequestToken": str,
        "Operation": OperationType,
        "OperationStatus": OperationStatusType,
        "EventTime": datetime,
        "ResourceModel": str,
        "StatusMessage": str,
        "ErrorCode": HandlerErrorCodeType,
        "RetryAfter": datetime,
    },
    total=False,
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

_RequiredCreateResourceInputRequestTypeDef = TypedDict(
    "_RequiredCreateResourceInputRequestTypeDef",
    {
        "TypeName": str,
        "DesiredState": str,
    },
)
_OptionalCreateResourceInputRequestTypeDef = TypedDict(
    "_OptionalCreateResourceInputRequestTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
        "ClientToken": str,
    },
    total=False,
)


class CreateResourceInputRequestTypeDef(
    _RequiredCreateResourceInputRequestTypeDef, _OptionalCreateResourceInputRequestTypeDef
):
    pass


_RequiredDeleteResourceInputRequestTypeDef = TypedDict(
    "_RequiredDeleteResourceInputRequestTypeDef",
    {
        "TypeName": str,
        "Identifier": str,
    },
)
_OptionalDeleteResourceInputRequestTypeDef = TypedDict(
    "_OptionalDeleteResourceInputRequestTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
        "ClientToken": str,
    },
    total=False,
)


class DeleteResourceInputRequestTypeDef(
    _RequiredDeleteResourceInputRequestTypeDef, _OptionalDeleteResourceInputRequestTypeDef
):
    pass


_RequiredGetResourceInputRequestTypeDef = TypedDict(
    "_RequiredGetResourceInputRequestTypeDef",
    {
        "TypeName": str,
        "Identifier": str,
    },
)
_OptionalGetResourceInputRequestTypeDef = TypedDict(
    "_OptionalGetResourceInputRequestTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
    },
    total=False,
)


class GetResourceInputRequestTypeDef(
    _RequiredGetResourceInputRequestTypeDef, _OptionalGetResourceInputRequestTypeDef
):
    pass


ResourceDescriptionTypeDef = TypedDict(
    "ResourceDescriptionTypeDef",
    {
        "Identifier": str,
        "Properties": str,
    },
    total=False,
)

GetResourceRequestStatusInputRequestTypeDef = TypedDict(
    "GetResourceRequestStatusInputRequestTypeDef",
    {
        "RequestToken": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
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

ResourceRequestStatusFilterTypeDef = TypedDict(
    "ResourceRequestStatusFilterTypeDef",
    {
        "Operations": Sequence[OperationType],
        "OperationStatuses": Sequence[OperationStatusType],
    },
    total=False,
)

_RequiredListResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListResourcesInputRequestTypeDef",
    {
        "TypeName": str,
    },
)
_OptionalListResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListResourcesInputRequestTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
        "NextToken": str,
        "MaxResults": int,
        "ResourceModel": str,
    },
    total=False,
)


class ListResourcesInputRequestTypeDef(
    _RequiredListResourcesInputRequestTypeDef, _OptionalListResourcesInputRequestTypeDef
):
    pass


_RequiredUpdateResourceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceInputRequestTypeDef",
    {
        "TypeName": str,
        "Identifier": str,
        "PatchDocument": str,
    },
)
_OptionalUpdateResourceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceInputRequestTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
        "ClientToken": str,
    },
    total=False,
)


class UpdateResourceInputRequestTypeDef(
    _RequiredUpdateResourceInputRequestTypeDef, _OptionalUpdateResourceInputRequestTypeDef
):
    pass


CancelResourceRequestOutputTypeDef = TypedDict(
    "CancelResourceRequestOutputTypeDef",
    {
        "ProgressEvent": ProgressEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourceOutputTypeDef = TypedDict(
    "CreateResourceOutputTypeDef",
    {
        "ProgressEvent": ProgressEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResourceOutputTypeDef = TypedDict(
    "DeleteResourceOutputTypeDef",
    {
        "ProgressEvent": ProgressEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceRequestStatusOutputTypeDef = TypedDict(
    "GetResourceRequestStatusOutputTypeDef",
    {
        "ProgressEvent": ProgressEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceRequestsOutputTypeDef = TypedDict(
    "ListResourceRequestsOutputTypeDef",
    {
        "ResourceRequestStatusSummaries": List[ProgressEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResourceOutputTypeDef = TypedDict(
    "UpdateResourceOutputTypeDef",
    {
        "ProgressEvent": ProgressEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceOutputTypeDef = TypedDict(
    "GetResourceOutputTypeDef",
    {
        "TypeName": str,
        "ResourceDescription": ResourceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesOutputTypeDef = TypedDict(
    "ListResourcesOutputTypeDef",
    {
        "TypeName": str,
        "ResourceDescriptions": List[ResourceDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef = TypedDict(
    "_RequiredGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef",
    {
        "RequestToken": str,
    },
)
_OptionalGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef = TypedDict(
    "_OptionalGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef(
    _RequiredGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef,
    _OptionalGetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef,
):
    pass


_RequiredListResourcesInputListResourcesPaginateTypeDef = TypedDict(
    "_RequiredListResourcesInputListResourcesPaginateTypeDef",
    {
        "TypeName": str,
    },
)
_OptionalListResourcesInputListResourcesPaginateTypeDef = TypedDict(
    "_OptionalListResourcesInputListResourcesPaginateTypeDef",
    {
        "TypeVersionId": str,
        "RoleArn": str,
        "ResourceModel": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResourcesInputListResourcesPaginateTypeDef(
    _RequiredListResourcesInputListResourcesPaginateTypeDef,
    _OptionalListResourcesInputListResourcesPaginateTypeDef,
):
    pass


ListResourceRequestsInputListResourceRequestsPaginateTypeDef = TypedDict(
    "ListResourceRequestsInputListResourceRequestsPaginateTypeDef",
    {
        "ResourceRequestStatusFilter": ResourceRequestStatusFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResourceRequestsInputRequestTypeDef = TypedDict(
    "ListResourceRequestsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "ResourceRequestStatusFilter": ResourceRequestStatusFilterTypeDef,
    },
    total=False,
)
