"""
Type annotations for resource-groups service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resource_groups.client import ResourceGroupsClient

    session = Session()
    client: ResourceGroupsClient = session.client("resource-groups")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListGroupResourcesPaginator, ListGroupsPaginator, SearchResourcesPaginator
from .type_defs import (
    CreateGroupOutputTypeDef,
    DeleteGroupOutputTypeDef,
    GetGroupConfigurationOutputTypeDef,
    GetGroupOutputTypeDef,
    GetGroupQueryOutputTypeDef,
    GetTagsOutputTypeDef,
    GroupConfigurationItemTypeDef,
    GroupFilterTypeDef,
    GroupResourcesOutputTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsOutputTypeDef,
    ResourceFilterTypeDef,
    ResourceQueryTypeDef,
    SearchResourcesOutputTypeDef,
    TagOutputTypeDef,
    UngroupResourcesOutputTypeDef,
    UntagOutputTypeDef,
    UpdateGroupOutputTypeDef,
    UpdateGroupQueryOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ResourceGroupsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class ResourceGroupsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#can_paginate)
        """

    def create_group(
        self,
        *,
        Name: str,
        Description: str = ...,
        ResourceQuery: ResourceQueryTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        Configuration: Sequence[GroupConfigurationItemTypeDef] = ...
    ) -> CreateGroupOutputTypeDef:
        """
        Creates a resource group with the specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.create_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#create_group)
        """

    def delete_group(self, *, GroupName: str = ..., Group: str = ...) -> DeleteGroupOutputTypeDef:
        """
        Deletes the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.delete_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#delete_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#generate_presigned_url)
        """

    def get_group(self, *, GroupName: str = ..., Group: str = ...) -> GetGroupOutputTypeDef:
        """
        Returns information about a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_group)
        """

    def get_group_configuration(self, *, Group: str = ...) -> GetGroupConfigurationOutputTypeDef:
        """
        Returns the service configuration associated with the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_group_configuration)
        """

    def get_group_query(
        self, *, GroupName: str = ..., Group: str = ...
    ) -> GetGroupQueryOutputTypeDef:
        """
        Retrieves the resource query associated with the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_group_query)
        """

    def get_tags(self, *, Arn: str) -> GetTagsOutputTypeDef:
        """
        Returns a list of tags that are associated with a resource group, specified by
        an ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_tags)
        """

    def group_resources(
        self, *, Group: str, ResourceArns: Sequence[str]
    ) -> GroupResourcesOutputTypeDef:
        """
        Adds the specified resources to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.group_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#group_resources)
        """

    def list_group_resources(
        self,
        *,
        GroupName: str = ...,
        Group: str = ...,
        Filters: Sequence[ResourceFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListGroupResourcesOutputTypeDef:
        """
        Returns a list of ARNs of the resources that are members of a specified resource
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.list_group_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#list_group_resources)
        """

    def list_groups(
        self,
        *,
        Filters: Sequence[GroupFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListGroupsOutputTypeDef:
        """
        Returns a list of existing resource groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.list_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#list_groups)
        """

    def put_group_configuration(
        self, *, Group: str = ..., Configuration: Sequence[GroupConfigurationItemTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Attaches a service configuration to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.put_group_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#put_group_configuration)
        """

    def search_resources(
        self, *, ResourceQuery: ResourceQueryTypeDef, MaxResults: int = ..., NextToken: str = ...
    ) -> SearchResourcesOutputTypeDef:
        """
        Returns a list of AWS resource identifiers that matches the specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.search_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#search_resources)
        """

    def tag(self, *, Arn: str, Tags: Mapping[str, str]) -> TagOutputTypeDef:
        """
        Adds tags to a resource group with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.tag)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#tag)
        """

    def ungroup_resources(
        self, *, Group: str, ResourceArns: Sequence[str]
    ) -> UngroupResourcesOutputTypeDef:
        """
        Removes the specified resources from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.ungroup_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#ungroup_resources)
        """

    def untag(self, *, Arn: str, Keys: Sequence[str]) -> UntagOutputTypeDef:
        """
        Deletes tags from a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.untag)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#untag)
        """

    def update_group(
        self, *, GroupName: str = ..., Group: str = ..., Description: str = ...
    ) -> UpdateGroupOutputTypeDef:
        """
        Updates the description for an existing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.update_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#update_group)
        """

    def update_group_query(
        self, *, ResourceQuery: ResourceQueryTypeDef, GroupName: str = ..., Group: str = ...
    ) -> UpdateGroupQueryOutputTypeDef:
        """
        Updates the resource query of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.update_group_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#update_group_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_resources"]
    ) -> ListGroupResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/client/#get_paginator)
        """
