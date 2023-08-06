"""
Type annotations for ecs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecs.client import ECSClient
    from mypy_boto3_ecs.paginator import (
        ListAccountSettingsPaginator,
        ListAttributesPaginator,
        ListClustersPaginator,
        ListContainerInstancesPaginator,
        ListServicesPaginator,
        ListTaskDefinitionFamiliesPaginator,
        ListTaskDefinitionsPaginator,
        ListTasksPaginator,
    )

    session = Session()
    client: ECSClient = session.client("ecs")

    list_account_settings_paginator: ListAccountSettingsPaginator = client.get_paginator("list_account_settings")
    list_attributes_paginator: ListAttributesPaginator = client.get_paginator("list_attributes")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_container_instances_paginator: ListContainerInstancesPaginator = client.get_paginator("list_container_instances")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_task_definition_families_paginator: ListTaskDefinitionFamiliesPaginator = client.get_paginator("list_task_definition_families")
    list_task_definitions_paginator: ListTaskDefinitionsPaginator = client.get_paginator("list_task_definitions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ContainerInstanceStatusType,
    DesiredStatusType,
    LaunchTypeType,
    SchedulingStrategyType,
    SettingNameType,
    SortOrderType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
)
from .type_defs import (
    ListAccountSettingsResponseTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAccountSettingsPaginator",
    "ListAttributesPaginator",
    "ListClustersPaginator",
    "ListContainerInstancesPaginator",
    "ListServicesPaginator",
    "ListTaskDefinitionFamiliesPaginator",
    "ListTaskDefinitionsPaginator",
    "ListTasksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountSettingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListAccountSettings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listaccountsettingspaginator)
    """

    def paginate(
        self,
        *,
        name: SettingNameType = ...,
        value: str = ...,
        principalArn: str = ...,
        effectiveSettings: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountSettingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListAccountSettings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listaccountsettingspaginator)
        """


class ListAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListAttributes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listattributespaginator)
    """

    def paginate(
        self,
        *,
        targetType: Literal["container-instance"],
        cluster: str = ...,
        attributeName: str = ...,
        attributeValue: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListAttributes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listattributespaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListClusters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listclusterspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listclusterspaginator)
        """


class ListContainerInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListContainerInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listcontainerinstancespaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = ...,
        filter: str = ...,
        status: ContainerInstanceStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContainerInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListContainerInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listcontainerinstancespaginator)
        """


class ListServicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicespaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = ...,
        launchType: LaunchTypeType = ...,
        schedulingStrategy: SchedulingStrategyType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listservicespaginator)
        """


class ListTaskDefinitionFamiliesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitionFamilies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionfamiliespaginator)
    """

    def paginate(
        self,
        *,
        familyPrefix: str = ...,
        status: TaskDefinitionFamilyStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTaskDefinitionFamiliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitionFamilies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionfamiliespaginator)
        """


class ListTaskDefinitionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        familyPrefix: str = ...,
        status: TaskDefinitionStatusType = ...,
        sort: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTaskDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskdefinitionspaginator)
        """


class ListTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskspaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = ...,
        containerInstance: str = ...,
        family: str = ...,
        startedBy: str = ...,
        serviceName: str = ...,
        desiredStatus: DesiredStatusType = ...,
        launchType: LaunchTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Paginator.ListTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators/#listtaskspaginator)
        """
