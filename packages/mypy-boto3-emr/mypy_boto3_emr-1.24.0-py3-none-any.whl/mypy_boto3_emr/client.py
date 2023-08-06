"""
Type annotations for emr service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_emr.client import EMRClient

    session = Session()
    client: EMRClient = session.client("emr")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AuthModeType,
    ClusterStateType,
    IdentityTypeType,
    InstanceFleetTypeType,
    InstanceGroupTypeType,
    InstanceStateType,
    JobFlowExecutionStateType,
    NotebookExecutionStatusType,
    RepoUpgradeOnBootType,
    ScaleDownBehaviorType,
    StepCancellationOptionType,
    StepStateType,
)
from .paginator import (
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
from .type_defs import (
    AddInstanceFleetOutputTypeDef,
    AddInstanceGroupsOutputTypeDef,
    AddJobFlowStepsOutputTypeDef,
    ApplicationTypeDef,
    AutoScalingPolicyTypeDef,
    AutoTerminationPolicyTypeDef,
    BlockPublicAccessConfigurationTypeDef,
    BootstrapActionConfigTypeDef,
    CancelStepsOutputTypeDef,
    ConfigurationTypeDef,
    CreateSecurityConfigurationOutputTypeDef,
    CreateStudioOutputTypeDef,
    DescribeClusterOutputTypeDef,
    DescribeJobFlowsOutputTypeDef,
    DescribeNotebookExecutionOutputTypeDef,
    DescribeReleaseLabelOutputTypeDef,
    DescribeSecurityConfigurationOutputTypeDef,
    DescribeStepOutputTypeDef,
    DescribeStudioOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecutionEngineConfigTypeDef,
    GetAutoTerminationPolicyOutputTypeDef,
    GetBlockPublicAccessConfigurationOutputTypeDef,
    GetManagedScalingPolicyOutputTypeDef,
    GetStudioSessionMappingOutputTypeDef,
    InstanceFleetConfigTypeDef,
    InstanceFleetModifyConfigTypeDef,
    InstanceGroupConfigTypeDef,
    InstanceGroupModifyConfigTypeDef,
    JobFlowInstancesConfigTypeDef,
    KerberosAttributesTypeDef,
    ListBootstrapActionsOutputTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsOutputTypeDef,
    ListInstanceGroupsOutputTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListReleaseLabelsOutputTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosOutputTypeDef,
    ManagedScalingPolicyTypeDef,
    ModifyClusterOutputTypeDef,
    PlacementGroupConfigTypeDef,
    PutAutoScalingPolicyOutputTypeDef,
    ReleaseLabelFilterTypeDef,
    RunJobFlowOutputTypeDef,
    StartNotebookExecutionOutputTypeDef,
    StepConfigTypeDef,
    SupportedProductConfigTypeDef,
    TagTypeDef,
)
from .waiter import ClusterRunningWaiter, ClusterTerminatedWaiter, StepCompleteWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("EMRClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]


class EMRClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EMRClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#exceptions)
        """

    def add_instance_fleet(
        self, *, ClusterId: str, InstanceFleet: InstanceFleetConfigTypeDef
    ) -> AddInstanceFleetOutputTypeDef:
        """
        Adds an instance fleet to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_instance_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_instance_fleet)
        """

    def add_instance_groups(
        self, *, InstanceGroups: Sequence[InstanceGroupConfigTypeDef], JobFlowId: str
    ) -> AddInstanceGroupsOutputTypeDef:
        """
        Adds one or more instance groups to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_instance_groups)
        """

    def add_job_flow_steps(
        self, *, JobFlowId: str, Steps: Sequence[StepConfigTypeDef]
    ) -> AddJobFlowStepsOutputTypeDef:
        """
        AddJobFlowSteps adds new steps to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_job_flow_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_job_flow_steps)
        """

    def add_tags(self, *, ResourceId: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an Amazon EMR resource, such as a cluster or an Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_tags)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#can_paginate)
        """

    def cancel_steps(
        self,
        *,
        ClusterId: str,
        StepIds: Sequence[str],
        StepCancellationOption: StepCancellationOptionType = ...
    ) -> CancelStepsOutputTypeDef:
        """
        Cancels a pending step or steps in a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.cancel_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#cancel_steps)
        """

    def create_security_configuration(
        self, *, Name: str, SecurityConfiguration: str
    ) -> CreateSecurityConfigurationOutputTypeDef:
        """
        Creates a security configuration, which is stored in the service and can be
        specified when a cluster is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_security_configuration)
        """

    def create_studio(
        self,
        *,
        Name: str,
        AuthMode: AuthModeType,
        VpcId: str,
        SubnetIds: Sequence[str],
        ServiceRole: str,
        WorkspaceSecurityGroupId: str,
        EngineSecurityGroupId: str,
        DefaultS3Location: str,
        Description: str = ...,
        UserRole: str = ...,
        IdpAuthUrl: str = ...,
        IdpRelayStateParameterName: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateStudioOutputTypeDef:
        """
        Creates a new Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_studio)
        """

    def create_studio_session_mapping(
        self,
        *,
        StudioId: str,
        IdentityType: IdentityTypeType,
        SessionPolicyArn: str,
        IdentityId: str = ...,
        IdentityName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Maps a user or group to the Amazon EMR Studio specified by `StudioId` , and
        applies a session policy to refine Studio permissions for that user or group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_studio_session_mapping)
        """

    def delete_security_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_security_configuration)
        """

    def delete_studio(self, *, StudioId: str) -> EmptyResponseMetadataTypeDef:
        """
        Removes an Amazon EMR Studio from the Studio metadata store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_studio)
        """

    def delete_studio_session_mapping(
        self,
        *,
        StudioId: str,
        IdentityType: IdentityTypeType,
        IdentityId: str = ...,
        IdentityName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a user or group from an Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_studio_session_mapping)
        """

    def describe_cluster(self, *, ClusterId: str) -> DescribeClusterOutputTypeDef:
        """
        Provides cluster-level details including status, hardware and software
        configuration, VPC settings, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_cluster)
        """

    def describe_job_flows(
        self,
        *,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        JobFlowIds: Sequence[str] = ...,
        JobFlowStates: Sequence[JobFlowExecutionStateType] = ...
    ) -> DescribeJobFlowsOutputTypeDef:
        """
        This API is no longer supported and will eventually be removed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_job_flows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_job_flows)
        """

    def describe_notebook_execution(
        self, *, NotebookExecutionId: str
    ) -> DescribeNotebookExecutionOutputTypeDef:
        """
        Provides details of a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_notebook_execution)
        """

    def describe_release_label(
        self, *, ReleaseLabel: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeReleaseLabelOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_release_label)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_release_label)
        """

    def describe_security_configuration(
        self, *, Name: str
    ) -> DescribeSecurityConfigurationOutputTypeDef:
        """
        Provides the details of a security configuration by returning the configuration
        JSON.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_security_configuration)
        """

    def describe_step(self, *, ClusterId: str, StepId: str) -> DescribeStepOutputTypeDef:
        """
        Provides more detail about the cluster step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_step)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_step)
        """

    def describe_studio(self, *, StudioId: str) -> DescribeStudioOutputTypeDef:
        """
        Returns details for the specified Amazon EMR Studio including ID, Name, VPC,
        Studio access URL, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_studio)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#generate_presigned_url)
        """

    def get_auto_termination_policy(
        self, *, ClusterId: str
    ) -> GetAutoTerminationPolicyOutputTypeDef:
        """
        Returns the auto-termination policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_auto_termination_policy)
        """

    def get_block_public_access_configuration(
        self,
    ) -> GetBlockPublicAccessConfigurationOutputTypeDef:
        """
        Returns the Amazon EMR block public access configuration for your Amazon Web
        Services account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_block_public_access_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_block_public_access_configuration)
        """

    def get_managed_scaling_policy(self, *, ClusterId: str) -> GetManagedScalingPolicyOutputTypeDef:
        """
        Fetches the attached managed scaling policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_managed_scaling_policy)
        """

    def get_studio_session_mapping(
        self,
        *,
        StudioId: str,
        IdentityType: IdentityTypeType,
        IdentityId: str = ...,
        IdentityName: str = ...
    ) -> GetStudioSessionMappingOutputTypeDef:
        """
        Fetches mapping details for the specified Amazon EMR Studio and identity (user
        or group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_studio_session_mapping)
        """

    def list_bootstrap_actions(
        self, *, ClusterId: str, Marker: str = ...
    ) -> ListBootstrapActionsOutputTypeDef:
        """
        Provides information about the bootstrap actions associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_bootstrap_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_bootstrap_actions)
        """

    def list_clusters(
        self,
        *,
        CreatedAfter: Union[datetime, str] = ...,
        CreatedBefore: Union[datetime, str] = ...,
        ClusterStates: Sequence[ClusterStateType] = ...,
        Marker: str = ...
    ) -> ListClustersOutputTypeDef:
        """
        Provides the status of all clusters visible to this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_clusters)
        """

    def list_instance_fleets(
        self, *, ClusterId: str, Marker: str = ...
    ) -> ListInstanceFleetsOutputTypeDef:
        """
        Lists all available details about the instance fleets in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instance_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instance_fleets)
        """

    def list_instance_groups(
        self, *, ClusterId: str, Marker: str = ...
    ) -> ListInstanceGroupsOutputTypeDef:
        """
        Provides all available details about the instance groups in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instance_groups)
        """

    def list_instances(
        self,
        *,
        ClusterId: str,
        InstanceGroupId: str = ...,
        InstanceGroupTypes: Sequence[InstanceGroupTypeType] = ...,
        InstanceFleetId: str = ...,
        InstanceFleetType: InstanceFleetTypeType = ...,
        InstanceStates: Sequence[InstanceStateType] = ...,
        Marker: str = ...
    ) -> ListInstancesOutputTypeDef:
        """
        Provides information for all active EC2 instances and EC2 instances terminated
        in the last 30 days, up to a maximum of 2,000.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instances)
        """

    def list_notebook_executions(
        self,
        *,
        EditorId: str = ...,
        Status: NotebookExecutionStatusType = ...,
        From: Union[datetime, str] = ...,
        To: Union[datetime, str] = ...,
        Marker: str = ...
    ) -> ListNotebookExecutionsOutputTypeDef:
        """
        Provides summaries of all notebook executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_notebook_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_notebook_executions)
        """

    def list_release_labels(
        self,
        *,
        Filters: ReleaseLabelFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListReleaseLabelsOutputTypeDef:
        """
        Retrieves release labels of EMR services in the region where the API is called.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_release_labels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_release_labels)
        """

    def list_security_configurations(
        self, *, Marker: str = ...
    ) -> ListSecurityConfigurationsOutputTypeDef:
        """
        Lists all the security configurations visible to this account, providing their
        creation dates and times, and their names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_security_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_security_configurations)
        """

    def list_steps(
        self,
        *,
        ClusterId: str,
        StepStates: Sequence[StepStateType] = ...,
        StepIds: Sequence[str] = ...,
        Marker: str = ...
    ) -> ListStepsOutputTypeDef:
        """
        Provides a list of steps for the cluster in reverse order unless you specify
        `stepIds` with the request or filter by `StepStates`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_steps)
        """

    def list_studio_session_mappings(
        self, *, StudioId: str = ..., IdentityType: IdentityTypeType = ..., Marker: str = ...
    ) -> ListStudioSessionMappingsOutputTypeDef:
        """
        Returns a list of all user or group session mappings for the Amazon EMR Studio
        specified by `StudioId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_studio_session_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_studio_session_mappings)
        """

    def list_studios(self, *, Marker: str = ...) -> ListStudiosOutputTypeDef:
        """
        Returns a list of all Amazon EMR Studios associated with the Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_studios)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_studios)
        """

    def modify_cluster(
        self, *, ClusterId: str, StepConcurrencyLevel: int = ...
    ) -> ModifyClusterOutputTypeDef:
        """
        Modifies the number of steps that can be executed concurrently for the cluster
        specified using ClusterID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_cluster)
        """

    def modify_instance_fleet(
        self, *, ClusterId: str, InstanceFleet: InstanceFleetModifyConfigTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the target On-Demand and target Spot capacities for the instance fleet
        with the specified InstanceFleetID within the cluster specified using ClusterID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_instance_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_instance_fleet)
        """

    def modify_instance_groups(
        self,
        *,
        ClusterId: str = ...,
        InstanceGroups: Sequence[InstanceGroupModifyConfigTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        ModifyInstanceGroups modifies the number of nodes and configuration settings of
        an instance group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_instance_groups)
        """

    def put_auto_scaling_policy(
        self, *, ClusterId: str, InstanceGroupId: str, AutoScalingPolicy: AutoScalingPolicyTypeDef
    ) -> PutAutoScalingPolicyOutputTypeDef:
        """
        Creates or updates an automatic scaling policy for a core instance group or task
        instance group in an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_auto_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_auto_scaling_policy)
        """

    def put_auto_termination_policy(
        self, *, ClusterId: str, AutoTerminationPolicy: AutoTerminationPolicyTypeDef = ...
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_auto_termination_policy)
        """

    def put_block_public_access_configuration(
        self, *, BlockPublicAccessConfiguration: BlockPublicAccessConfigurationTypeDef
    ) -> Dict[str, Any]:
        """
        Creates or updates an Amazon EMR block public access configuration for your
        Amazon Web Services account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_block_public_access_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_block_public_access_configuration)
        """

    def put_managed_scaling_policy(
        self, *, ClusterId: str, ManagedScalingPolicy: ManagedScalingPolicyTypeDef
    ) -> Dict[str, Any]:
        """
        Creates or updates a managed scaling policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_managed_scaling_policy)
        """

    def remove_auto_scaling_policy(self, *, ClusterId: str, InstanceGroupId: str) -> Dict[str, Any]:
        """
        Removes an automatic scaling policy from a specified instance group within an
        EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_auto_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_auto_scaling_policy)
        """

    def remove_auto_termination_policy(self, *, ClusterId: str) -> Dict[str, Any]:
        """
        Removes an auto-termination policy from an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_auto_termination_policy)
        """

    def remove_managed_scaling_policy(self, *, ClusterId: str) -> Dict[str, Any]:
        """
        Removes a managed scaling policy from a specified EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_managed_scaling_policy)
        """

    def remove_tags(self, *, ResourceId: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from an Amazon EMR resource, such as a cluster or Amazon EMR
        Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_tags)
        """

    def run_job_flow(
        self,
        *,
        Name: str,
        Instances: JobFlowInstancesConfigTypeDef,
        LogUri: str = ...,
        LogEncryptionKmsKeyId: str = ...,
        AdditionalInfo: str = ...,
        AmiVersion: str = ...,
        ReleaseLabel: str = ...,
        Steps: Sequence[StepConfigTypeDef] = ...,
        BootstrapActions: Sequence[BootstrapActionConfigTypeDef] = ...,
        SupportedProducts: Sequence[str] = ...,
        NewSupportedProducts: Sequence[SupportedProductConfigTypeDef] = ...,
        Applications: Sequence[ApplicationTypeDef] = ...,
        Configurations: Sequence["ConfigurationTypeDef"] = ...,
        VisibleToAllUsers: bool = ...,
        JobFlowRole: str = ...,
        ServiceRole: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SecurityConfiguration: str = ...,
        AutoScalingRole: str = ...,
        ScaleDownBehavior: ScaleDownBehaviorType = ...,
        CustomAmiId: str = ...,
        EbsRootVolumeSize: int = ...,
        RepoUpgradeOnBoot: RepoUpgradeOnBootType = ...,
        KerberosAttributes: KerberosAttributesTypeDef = ...,
        StepConcurrencyLevel: int = ...,
        ManagedScalingPolicy: ManagedScalingPolicyTypeDef = ...,
        PlacementGroupConfigs: Sequence[PlacementGroupConfigTypeDef] = ...,
        AutoTerminationPolicy: AutoTerminationPolicyTypeDef = ...,
        OSReleaseLabel: str = ...
    ) -> RunJobFlowOutputTypeDef:
        """
        RunJobFlow creates and starts running a new cluster (job flow).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.run_job_flow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#run_job_flow)
        """

    def set_termination_protection(
        self, *, JobFlowIds: Sequence[str], TerminationProtected: bool
    ) -> EmptyResponseMetadataTypeDef:
        """
        SetTerminationProtection locks a cluster (job flow) so the EC2 instances in the
        cluster cannot be terminated by user intervention, an API call, or in the event
        of a job-flow error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_termination_protection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_termination_protection)
        """

    def set_visible_to_all_users(
        self, *, JobFlowIds: Sequence[str], VisibleToAllUsers: bool
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_visible_to_all_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_visible_to_all_users)
        """

    def start_notebook_execution(
        self,
        *,
        EditorId: str,
        RelativePath: str,
        ExecutionEngine: ExecutionEngineConfigTypeDef,
        ServiceRole: str,
        NotebookExecutionName: str = ...,
        NotebookParams: str = ...,
        NotebookInstanceSecurityGroupId: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> StartNotebookExecutionOutputTypeDef:
        """
        Starts a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.start_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#start_notebook_execution)
        """

    def stop_notebook_execution(self, *, NotebookExecutionId: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.stop_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#stop_notebook_execution)
        """

    def terminate_job_flows(self, *, JobFlowIds: Sequence[str]) -> EmptyResponseMetadataTypeDef:
        """
        TerminateJobFlows shuts a list of clusters (job flows) down.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.terminate_job_flows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#terminate_job_flows)
        """

    def update_studio(
        self,
        *,
        StudioId: str,
        Name: str = ...,
        Description: str = ...,
        SubnetIds: Sequence[str] = ...,
        DefaultS3Location: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon EMR Studio configuration, including attributes such as name,
        description, and subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.update_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#update_studio)
        """

    def update_studio_session_mapping(
        self,
        *,
        StudioId: str,
        IdentityType: IdentityTypeType,
        SessionPolicyArn: str,
        IdentityId: str = ...,
        IdentityName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the session policy attached to the user or group for the specified
        Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.update_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#update_studio_session_mapping)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bootstrap_actions"]
    ) -> ListBootstrapActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_fleets"]
    ) -> ListInstanceFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_groups"]
    ) -> ListInstanceGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notebook_executions"]
    ) -> ListNotebookExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_configurations"]
    ) -> ListSecurityConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_steps"]) -> ListStepsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_studio_session_mappings"]
    ) -> ListStudioSessionMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_studios"]) -> ListStudiosPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_running"]) -> ClusterRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_terminated"]) -> ClusterTerminatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["step_complete"]) -> StepCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """
