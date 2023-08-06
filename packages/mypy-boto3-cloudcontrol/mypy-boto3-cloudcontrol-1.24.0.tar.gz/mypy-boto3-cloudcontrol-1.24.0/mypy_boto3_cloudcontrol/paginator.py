"""
Type annotations for cloudcontrol service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudcontrol.client import CloudControlApiClient
    from mypy_boto3_cloudcontrol.paginator import (
        ListResourceRequestsPaginator,
        ListResourcesPaginator,
    )

    session = Session()
    client: CloudControlApiClient = session.client("cloudcontrol")

    list_resource_requests_paginator: ListResourceRequestsPaginator = client.get_paginator("list_resource_requests")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListResourceRequestsOutputTypeDef,
    ListResourcesOutputTypeDef,
    PaginatorConfigTypeDef,
    ResourceRequestStatusFilterTypeDef,
)

__all__ = ("ListResourceRequestsPaginator", "ListResourcesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListResourceRequestsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Paginator.ListResourceRequests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcerequestspaginator)
    """

    def paginate(
        self,
        *,
        ResourceRequestStatusFilter: ResourceRequestStatusFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Paginator.ListResourceRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcerequestspaginator)
        """


class ListResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Paginator.ListResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcespaginator)
    """

    def paginate(
        self,
        *,
        TypeName: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ResourceModel: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Paginator.ListResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/paginators/#listresourcespaginator)
        """
