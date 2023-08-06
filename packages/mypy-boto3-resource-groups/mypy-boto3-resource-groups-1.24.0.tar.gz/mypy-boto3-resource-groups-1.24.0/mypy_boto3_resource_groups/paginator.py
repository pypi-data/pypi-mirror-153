"""
Type annotations for resource-groups service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_resource_groups.client import ResourceGroupsClient
    from mypy_boto3_resource_groups.paginator import (
        ListGroupResourcesPaginator,
        ListGroupsPaginator,
        SearchResourcesPaginator,
    )

    session = Session()
    client: ResourceGroupsClient = session.client("resource-groups")

    list_group_resources_paginator: ListGroupResourcesPaginator = client.get_paginator("list_group_resources")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GroupFilterTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
    ResourceFilterTypeDef,
    ResourceQueryTypeDef,
    SearchResourcesOutputTypeDef,
)

__all__ = ("ListGroupResourcesPaginator", "ListGroupsPaginator", "SearchResourcesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListGroupResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#listgroupresourcespaginator)
    """

    def paginate(
        self,
        *,
        GroupName: str = ...,
        Group: str = ...,
        Filters: Sequence[ResourceFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGroupResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#listgroupresourcespaginator)
        """


class ListGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#listgroupspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[GroupFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#listgroupspaginator)
        """


class SearchResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#searchresourcespaginator)
    """

    def paginate(
        self, *, ResourceQuery: ResourceQueryTypeDef, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/paginators/#searchresourcespaginator)
        """
