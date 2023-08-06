"""
Type annotations for emr service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr.client import EMRClient
    from mypy_boto3_emr.paginator import (
        ListBootstrapActionsPaginator,
        ListClustersPaginator,
        ListInstanceFleetsPaginator,
        ListInstanceGroupsPaginator,
        ListInstancesPaginator,
        ListNotebookExecutionsPaginator,
        ListSecurityConfigurationsPaginator,
        ListStepsPaginator,
        ListStudioSessionMappingsPaginator,
        ListStudiosPaginator,
    )

    session = Session()
    client: EMRClient = session.client("emr")

    list_bootstrap_actions_paginator: ListBootstrapActionsPaginator = client.get_paginator("list_bootstrap_actions")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_instance_fleets_paginator: ListInstanceFleetsPaginator = client.get_paginator("list_instance_fleets")
    list_instance_groups_paginator: ListInstanceGroupsPaginator = client.get_paginator("list_instance_groups")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_notebook_executions_paginator: ListNotebookExecutionsPaginator = client.get_paginator("list_notebook_executions")
    list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
    list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
    list_studio_session_mappings_paginator: ListStudioSessionMappingsPaginator = client.get_paginator("list_studio_session_mappings")
    list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ClusterStateType,
    IdentityTypeType,
    InstanceFleetTypeType,
    InstanceGroupTypeType,
    InstanceStateType,
    NotebookExecutionStatusType,
    StepStateType,
)
from .type_defs import (
    ListBootstrapActionsOutputTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsOutputTypeDef,
    ListInstanceGroupsOutputTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListBootstrapActionsPaginator",
    "ListClustersPaginator",
    "ListInstanceFleetsPaginator",
    "ListInstanceGroupsPaginator",
    "ListInstancesPaginator",
    "ListNotebookExecutionsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListStepsPaginator",
    "ListStudioSessionMappingsPaginator",
    "ListStudiosPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBootstrapActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListBootstrapActions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listbootstrapactionspaginator)
    """

    def paginate(
        self, *, ClusterId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBootstrapActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListBootstrapActions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listbootstrapactionspaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListClusters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listclusterspaginator)
    """

    def paginate(
        self,
        *,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        ClusterStates: Sequence[ClusterStateType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listclusterspaginator)
        """


class ListInstanceFleetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceFleets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancefleetspaginator)
    """

    def paginate(
        self, *, ClusterId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstanceFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceFleets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancefleetspaginator)
        """


class ListInstanceGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancegroupspaginator)
    """

    def paginate(
        self, *, ClusterId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstanceGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancegroupspaginator)
        """


class ListInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancespaginator)
    """

    def paginate(
        self,
        *,
        ClusterId: str,
        InstanceGroupId: str = ...,
        InstanceGroupTypes: Sequence[InstanceGroupTypeType] = ...,
        InstanceFleetId: str = ...,
        InstanceFleetType: InstanceFleetTypeType = ...,
        InstanceStates: Sequence[InstanceStateType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listinstancespaginator)
        """


class ListNotebookExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListNotebookExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listnotebookexecutionspaginator)
    """

    def paginate(
        self,
        *,
        EditorId: str = ...,
        Status: NotebookExecutionStatusType = ...,
        From: Union[datetime, str] = ...,
        To: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNotebookExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListNotebookExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listnotebookexecutionspaginator)
        """


class ListSecurityConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSecurityConfigurations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listsecurityconfigurationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSecurityConfigurations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#listsecurityconfigurationspaginator)
        """


class ListStepsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSteps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststepspaginator)
    """

    def paginate(
        self,
        *,
        ClusterId: str,
        StepStates: Sequence[StepStateType] = ...,
        StepIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStepsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSteps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststepspaginator)
        """


class ListStudioSessionMappingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudioSessionMappings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiosessionmappingspaginator)
    """

    def paginate(
        self,
        *,
        StudioId: str = ...,
        IdentityType: IdentityTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStudioSessionMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudioSessionMappings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiosessionmappingspaginator)
        """


class ListStudiosPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudios)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiospaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStudiosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudios.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/paginators/#liststudiospaginator)
        """
