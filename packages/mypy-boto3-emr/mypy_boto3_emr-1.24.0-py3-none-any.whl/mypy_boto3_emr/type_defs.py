"""
Type annotations for emr service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/type_defs/)

Usage::

    ```python
    from mypy_boto3_emr.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionOnFailureType,
    AdjustmentTypeType,
    AuthModeType,
    AutoScalingPolicyStateChangeReasonCodeType,
    AutoScalingPolicyStateType,
    CancelStepsRequestStatusType,
    ClusterStateChangeReasonCodeType,
    ClusterStateType,
    ComparisonOperatorType,
    ComputeLimitsUnitTypeType,
    IdentityTypeType,
    InstanceCollectionTypeType,
    InstanceFleetStateChangeReasonCodeType,
    InstanceFleetStateType,
    InstanceFleetTypeType,
    InstanceGroupStateChangeReasonCodeType,
    InstanceGroupStateType,
    InstanceGroupTypeType,
    InstanceRoleTypeType,
    InstanceStateChangeReasonCodeType,
    InstanceStateType,
    JobFlowExecutionStateType,
    MarketTypeType,
    NotebookExecutionStatusType,
    OnDemandCapacityReservationPreferenceType,
    PlacementGroupStrategyType,
    ReconfigurationTypeType,
    RepoUpgradeOnBootType,
    ScaleDownBehaviorType,
    SpotProvisioningTimeoutActionType,
    StatisticType,
    StepCancellationOptionType,
    StepExecutionStateType,
    StepStateType,
    UnitType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "ApplicationTypeDef",
    "ScalingConstraintsTypeDef",
    "AutoScalingPolicyStateChangeReasonTypeDef",
    "AutoTerminationPolicyTypeDef",
    "BlockPublicAccessConfigurationMetadataTypeDef",
    "PortRangeTypeDef",
    "ScriptBootstrapActionConfigTypeDef",
    "CancelStepsInfoTypeDef",
    "CancelStepsInputRequestTypeDef",
    "MetricDimensionTypeDef",
    "ClusterStateChangeReasonTypeDef",
    "ClusterTimelineTypeDef",
    "Ec2InstanceAttributesTypeDef",
    "KerberosAttributesTypeDef",
    "PlacementGroupConfigTypeDef",
    "CommandTypeDef",
    "ComputeLimitsTypeDef",
    "ConfigurationTypeDef",
    "CreateSecurityConfigurationInputRequestTypeDef",
    "CreateStudioSessionMappingInputRequestTypeDef",
    "DeleteSecurityConfigurationInputRequestTypeDef",
    "DeleteStudioInputRequestTypeDef",
    "DeleteStudioSessionMappingInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeClusterInputRequestTypeDef",
    "DescribeJobFlowsInputRequestTypeDef",
    "DescribeNotebookExecutionInputRequestTypeDef",
    "DescribeReleaseLabelInputRequestTypeDef",
    "OSReleaseTypeDef",
    "SimplifiedApplicationTypeDef",
    "DescribeSecurityConfigurationInputRequestTypeDef",
    "DescribeStepInputRequestTypeDef",
    "DescribeStudioInputRequestTypeDef",
    "VolumeSpecificationTypeDef",
    "EbsVolumeTypeDef",
    "ExecutionEngineConfigTypeDef",
    "FailureDetailsTypeDef",
    "GetAutoTerminationPolicyInputRequestTypeDef",
    "GetManagedScalingPolicyInputRequestTypeDef",
    "GetStudioSessionMappingInputRequestTypeDef",
    "SessionMappingDetailTypeDef",
    "KeyValueTypeDef",
    "HadoopStepConfigTypeDef",
    "InstanceFleetModifyConfigTypeDef",
    "SpotProvisioningSpecificationTypeDef",
    "InstanceFleetStateChangeReasonTypeDef",
    "InstanceFleetTimelineTypeDef",
    "InstanceGroupDetailTypeDef",
    "InstanceGroupStateChangeReasonTypeDef",
    "InstanceGroupTimelineTypeDef",
    "InstanceResizePolicyTypeDef",
    "InstanceStateChangeReasonTypeDef",
    "InstanceTimelineTypeDef",
    "JobFlowExecutionStatusDetailTypeDef",
    "PlacementTypeTypeDef",
    "PaginatorConfigTypeDef",
    "ListBootstrapActionsInputRequestTypeDef",
    "ListClustersInputRequestTypeDef",
    "ListInstanceFleetsInputRequestTypeDef",
    "ListInstanceGroupsInputRequestTypeDef",
    "ListInstancesInputRequestTypeDef",
    "ListNotebookExecutionsInputRequestTypeDef",
    "NotebookExecutionSummaryTypeDef",
    "ReleaseLabelFilterTypeDef",
    "ListSecurityConfigurationsInputRequestTypeDef",
    "SecurityConfigurationSummaryTypeDef",
    "ListStepsInputRequestTypeDef",
    "ListStudioSessionMappingsInputRequestTypeDef",
    "SessionMappingSummaryTypeDef",
    "ListStudiosInputRequestTypeDef",
    "StudioSummaryTypeDef",
    "ModifyClusterInputRequestTypeDef",
    "OnDemandCapacityReservationOptionsTypeDef",
    "RemoveAutoScalingPolicyInputRequestTypeDef",
    "RemoveAutoTerminationPolicyInputRequestTypeDef",
    "RemoveManagedScalingPolicyInputRequestTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "SupportedProductConfigTypeDef",
    "SimpleScalingPolicyConfigurationTypeDef",
    "SetTerminationProtectionInputRequestTypeDef",
    "SetVisibleToAllUsersInputRequestTypeDef",
    "StepExecutionStatusDetailTypeDef",
    "StepStateChangeReasonTypeDef",
    "StepTimelineTypeDef",
    "StopNotebookExecutionInputRequestTypeDef",
    "TerminateJobFlowsInputRequestTypeDef",
    "UpdateStudioInputRequestTypeDef",
    "UpdateStudioSessionMappingInputRequestTypeDef",
    "AddInstanceFleetOutputTypeDef",
    "AddInstanceGroupsOutputTypeDef",
    "AddJobFlowStepsOutputTypeDef",
    "CreateSecurityConfigurationOutputTypeDef",
    "CreateStudioOutputTypeDef",
    "DescribeSecurityConfigurationOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListReleaseLabelsOutputTypeDef",
    "ModifyClusterOutputTypeDef",
    "RunJobFlowOutputTypeDef",
    "StartNotebookExecutionOutputTypeDef",
    "AddTagsInputRequestTypeDef",
    "CreateStudioInputRequestTypeDef",
    "StudioTypeDef",
    "AutoScalingPolicyStatusTypeDef",
    "GetAutoTerminationPolicyOutputTypeDef",
    "PutAutoTerminationPolicyInputRequestTypeDef",
    "BlockPublicAccessConfigurationTypeDef",
    "BootstrapActionConfigTypeDef",
    "CancelStepsOutputTypeDef",
    "CloudWatchAlarmDefinitionTypeDef",
    "ClusterStatusTypeDef",
    "ListBootstrapActionsOutputTypeDef",
    "ManagedScalingPolicyTypeDef",
    "DescribeClusterInputClusterRunningWaitTypeDef",
    "DescribeClusterInputClusterTerminatedWaitTypeDef",
    "DescribeStepInputStepCompleteWaitTypeDef",
    "DescribeReleaseLabelOutputTypeDef",
    "EbsBlockDeviceConfigTypeDef",
    "EbsBlockDeviceTypeDef",
    "NotebookExecutionTypeDef",
    "StartNotebookExecutionInputRequestTypeDef",
    "GetStudioSessionMappingOutputTypeDef",
    "HadoopJarStepConfigTypeDef",
    "ModifyInstanceFleetInputRequestTypeDef",
    "InstanceFleetStatusTypeDef",
    "InstanceGroupStatusTypeDef",
    "ShrinkPolicyTypeDef",
    "InstanceStatusTypeDef",
    "JobFlowInstancesDetailTypeDef",
    "ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef",
    "ListClustersInputListClustersPaginateTypeDef",
    "ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef",
    "ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef",
    "ListInstancesInputListInstancesPaginateTypeDef",
    "ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef",
    "ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef",
    "ListStepsInputListStepsPaginateTypeDef",
    "ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef",
    "ListStudiosInputListStudiosPaginateTypeDef",
    "ListNotebookExecutionsOutputTypeDef",
    "ListReleaseLabelsInputRequestTypeDef",
    "ListSecurityConfigurationsOutputTypeDef",
    "ListStudioSessionMappingsOutputTypeDef",
    "ListStudiosOutputTypeDef",
    "OnDemandProvisioningSpecificationTypeDef",
    "ScalingActionTypeDef",
    "StepStatusTypeDef",
    "DescribeStudioOutputTypeDef",
    "GetBlockPublicAccessConfigurationOutputTypeDef",
    "PutBlockPublicAccessConfigurationInputRequestTypeDef",
    "BootstrapActionDetailTypeDef",
    "ScalingTriggerTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTypeDef",
    "GetManagedScalingPolicyOutputTypeDef",
    "PutManagedScalingPolicyInputRequestTypeDef",
    "EbsConfigurationTypeDef",
    "InstanceTypeSpecificationTypeDef",
    "DescribeNotebookExecutionOutputTypeDef",
    "StepConfigTypeDef",
    "InstanceGroupModifyConfigTypeDef",
    "InstanceTypeDef",
    "InstanceFleetProvisioningSpecificationsTypeDef",
    "StepSummaryTypeDef",
    "StepTypeDef",
    "ScalingRuleTypeDef",
    "ListClustersOutputTypeDef",
    "DescribeClusterOutputTypeDef",
    "InstanceTypeConfigTypeDef",
    "AddJobFlowStepsInputRequestTypeDef",
    "StepDetailTypeDef",
    "ModifyInstanceGroupsInputRequestTypeDef",
    "ListInstancesOutputTypeDef",
    "InstanceFleetTypeDef",
    "ListStepsOutputTypeDef",
    "DescribeStepOutputTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingPolicyTypeDef",
    "InstanceFleetConfigTypeDef",
    "JobFlowDetailTypeDef",
    "ListInstanceFleetsOutputTypeDef",
    "InstanceGroupTypeDef",
    "PutAutoScalingPolicyOutputTypeDef",
    "InstanceGroupConfigTypeDef",
    "PutAutoScalingPolicyInputRequestTypeDef",
    "AddInstanceFleetInputRequestTypeDef",
    "DescribeJobFlowsOutputTypeDef",
    "ListInstanceGroupsOutputTypeDef",
    "AddInstanceGroupsInputRequestTypeDef",
    "JobFlowInstancesConfigTypeDef",
    "RunJobFlowInputRequestTypeDef",
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Name": str,
        "Version": str,
        "Args": List[str],
        "AdditionalInfo": Dict[str, str],
    },
    total=False,
)

ScalingConstraintsTypeDef = TypedDict(
    "ScalingConstraintsTypeDef",
    {
        "MinCapacity": int,
        "MaxCapacity": int,
    },
)

AutoScalingPolicyStateChangeReasonTypeDef = TypedDict(
    "AutoScalingPolicyStateChangeReasonTypeDef",
    {
        "Code": AutoScalingPolicyStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

AutoTerminationPolicyTypeDef = TypedDict(
    "AutoTerminationPolicyTypeDef",
    {
        "IdleTimeout": int,
    },
    total=False,
)

BlockPublicAccessConfigurationMetadataTypeDef = TypedDict(
    "BlockPublicAccessConfigurationMetadataTypeDef",
    {
        "CreationDateTime": datetime,
        "CreatedByArn": str,
    },
)

_RequiredPortRangeTypeDef = TypedDict(
    "_RequiredPortRangeTypeDef",
    {
        "MinRange": int,
    },
)
_OptionalPortRangeTypeDef = TypedDict(
    "_OptionalPortRangeTypeDef",
    {
        "MaxRange": int,
    },
    total=False,
)


class PortRangeTypeDef(_RequiredPortRangeTypeDef, _OptionalPortRangeTypeDef):
    pass


_RequiredScriptBootstrapActionConfigTypeDef = TypedDict(
    "_RequiredScriptBootstrapActionConfigTypeDef",
    {
        "Path": str,
    },
)
_OptionalScriptBootstrapActionConfigTypeDef = TypedDict(
    "_OptionalScriptBootstrapActionConfigTypeDef",
    {
        "Args": List[str],
    },
    total=False,
)


class ScriptBootstrapActionConfigTypeDef(
    _RequiredScriptBootstrapActionConfigTypeDef, _OptionalScriptBootstrapActionConfigTypeDef
):
    pass


CancelStepsInfoTypeDef = TypedDict(
    "CancelStepsInfoTypeDef",
    {
        "StepId": str,
        "Status": CancelStepsRequestStatusType,
        "Reason": str,
    },
    total=False,
)

_RequiredCancelStepsInputRequestTypeDef = TypedDict(
    "_RequiredCancelStepsInputRequestTypeDef",
    {
        "ClusterId": str,
        "StepIds": Sequence[str],
    },
)
_OptionalCancelStepsInputRequestTypeDef = TypedDict(
    "_OptionalCancelStepsInputRequestTypeDef",
    {
        "StepCancellationOption": StepCancellationOptionType,
    },
    total=False,
)


class CancelStepsInputRequestTypeDef(
    _RequiredCancelStepsInputRequestTypeDef, _OptionalCancelStepsInputRequestTypeDef
):
    pass


MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ClusterStateChangeReasonTypeDef = TypedDict(
    "ClusterStateChangeReasonTypeDef",
    {
        "Code": ClusterStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

ClusterTimelineTypeDef = TypedDict(
    "ClusterTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

Ec2InstanceAttributesTypeDef = TypedDict(
    "Ec2InstanceAttributesTypeDef",
    {
        "Ec2KeyName": str,
        "Ec2SubnetId": str,
        "RequestedEc2SubnetIds": List[str],
        "Ec2AvailabilityZone": str,
        "RequestedEc2AvailabilityZones": List[str],
        "IamInstanceProfile": str,
        "EmrManagedMasterSecurityGroup": str,
        "EmrManagedSlaveSecurityGroup": str,
        "ServiceAccessSecurityGroup": str,
        "AdditionalMasterSecurityGroups": List[str],
        "AdditionalSlaveSecurityGroups": List[str],
    },
    total=False,
)

_RequiredKerberosAttributesTypeDef = TypedDict(
    "_RequiredKerberosAttributesTypeDef",
    {
        "Realm": str,
        "KdcAdminPassword": str,
    },
)
_OptionalKerberosAttributesTypeDef = TypedDict(
    "_OptionalKerberosAttributesTypeDef",
    {
        "CrossRealmTrustPrincipalPassword": str,
        "ADDomainJoinUser": str,
        "ADDomainJoinPassword": str,
    },
    total=False,
)


class KerberosAttributesTypeDef(
    _RequiredKerberosAttributesTypeDef, _OptionalKerberosAttributesTypeDef
):
    pass


_RequiredPlacementGroupConfigTypeDef = TypedDict(
    "_RequiredPlacementGroupConfigTypeDef",
    {
        "InstanceRole": InstanceRoleTypeType,
    },
)
_OptionalPlacementGroupConfigTypeDef = TypedDict(
    "_OptionalPlacementGroupConfigTypeDef",
    {
        "PlacementStrategy": PlacementGroupStrategyType,
    },
    total=False,
)


class PlacementGroupConfigTypeDef(
    _RequiredPlacementGroupConfigTypeDef, _OptionalPlacementGroupConfigTypeDef
):
    pass


CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "Name": str,
        "ScriptPath": str,
        "Args": List[str],
    },
    total=False,
)

_RequiredComputeLimitsTypeDef = TypedDict(
    "_RequiredComputeLimitsTypeDef",
    {
        "UnitType": ComputeLimitsUnitTypeType,
        "MinimumCapacityUnits": int,
        "MaximumCapacityUnits": int,
    },
)
_OptionalComputeLimitsTypeDef = TypedDict(
    "_OptionalComputeLimitsTypeDef",
    {
        "MaximumOnDemandCapacityUnits": int,
        "MaximumCoreCapacityUnits": int,
    },
    total=False,
)


class ComputeLimitsTypeDef(_RequiredComputeLimitsTypeDef, _OptionalComputeLimitsTypeDef):
    pass


ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Classification": str,
        "Configurations": Sequence[Dict[str, Any]],
        "Properties": Mapping[str, str],
    },
    total=False,
)

CreateSecurityConfigurationInputRequestTypeDef = TypedDict(
    "CreateSecurityConfigurationInputRequestTypeDef",
    {
        "Name": str,
        "SecurityConfiguration": str,
    },
)

_RequiredCreateStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_RequiredCreateStudioSessionMappingInputRequestTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
        "SessionPolicyArn": str,
    },
)
_OptionalCreateStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_OptionalCreateStudioSessionMappingInputRequestTypeDef",
    {
        "IdentityId": str,
        "IdentityName": str,
    },
    total=False,
)


class CreateStudioSessionMappingInputRequestTypeDef(
    _RequiredCreateStudioSessionMappingInputRequestTypeDef,
    _OptionalCreateStudioSessionMappingInputRequestTypeDef,
):
    pass


DeleteSecurityConfigurationInputRequestTypeDef = TypedDict(
    "DeleteSecurityConfigurationInputRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteStudioInputRequestTypeDef = TypedDict(
    "DeleteStudioInputRequestTypeDef",
    {
        "StudioId": str,
    },
)

_RequiredDeleteStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_RequiredDeleteStudioSessionMappingInputRequestTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
    },
)
_OptionalDeleteStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_OptionalDeleteStudioSessionMappingInputRequestTypeDef",
    {
        "IdentityId": str,
        "IdentityName": str,
    },
    total=False,
)


class DeleteStudioSessionMappingInputRequestTypeDef(
    _RequiredDeleteStudioSessionMappingInputRequestTypeDef,
    _OptionalDeleteStudioSessionMappingInputRequestTypeDef,
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeClusterInputRequestTypeDef = TypedDict(
    "DescribeClusterInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)

DescribeJobFlowsInputRequestTypeDef = TypedDict(
    "DescribeJobFlowsInputRequestTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "JobFlowIds": Sequence[str],
        "JobFlowStates": Sequence[JobFlowExecutionStateType],
    },
    total=False,
)

DescribeNotebookExecutionInputRequestTypeDef = TypedDict(
    "DescribeNotebookExecutionInputRequestTypeDef",
    {
        "NotebookExecutionId": str,
    },
)

DescribeReleaseLabelInputRequestTypeDef = TypedDict(
    "DescribeReleaseLabelInputRequestTypeDef",
    {
        "ReleaseLabel": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

OSReleaseTypeDef = TypedDict(
    "OSReleaseTypeDef",
    {
        "Label": str,
    },
    total=False,
)

SimplifiedApplicationTypeDef = TypedDict(
    "SimplifiedApplicationTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

DescribeSecurityConfigurationInputRequestTypeDef = TypedDict(
    "DescribeSecurityConfigurationInputRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeStepInputRequestTypeDef = TypedDict(
    "DescribeStepInputRequestTypeDef",
    {
        "ClusterId": str,
        "StepId": str,
    },
)

DescribeStudioInputRequestTypeDef = TypedDict(
    "DescribeStudioInputRequestTypeDef",
    {
        "StudioId": str,
    },
)

_RequiredVolumeSpecificationTypeDef = TypedDict(
    "_RequiredVolumeSpecificationTypeDef",
    {
        "VolumeType": str,
        "SizeInGB": int,
    },
)
_OptionalVolumeSpecificationTypeDef = TypedDict(
    "_OptionalVolumeSpecificationTypeDef",
    {
        "Iops": int,
    },
    total=False,
)


class VolumeSpecificationTypeDef(
    _RequiredVolumeSpecificationTypeDef, _OptionalVolumeSpecificationTypeDef
):
    pass


EbsVolumeTypeDef = TypedDict(
    "EbsVolumeTypeDef",
    {
        "Device": str,
        "VolumeId": str,
    },
    total=False,
)

_RequiredExecutionEngineConfigTypeDef = TypedDict(
    "_RequiredExecutionEngineConfigTypeDef",
    {
        "Id": str,
    },
)
_OptionalExecutionEngineConfigTypeDef = TypedDict(
    "_OptionalExecutionEngineConfigTypeDef",
    {
        "Type": Literal["EMR"],
        "MasterInstanceSecurityGroupId": str,
    },
    total=False,
)


class ExecutionEngineConfigTypeDef(
    _RequiredExecutionEngineConfigTypeDef, _OptionalExecutionEngineConfigTypeDef
):
    pass


FailureDetailsTypeDef = TypedDict(
    "FailureDetailsTypeDef",
    {
        "Reason": str,
        "Message": str,
        "LogFile": str,
    },
    total=False,
)

GetAutoTerminationPolicyInputRequestTypeDef = TypedDict(
    "GetAutoTerminationPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)

GetManagedScalingPolicyInputRequestTypeDef = TypedDict(
    "GetManagedScalingPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)

_RequiredGetStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_RequiredGetStudioSessionMappingInputRequestTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
    },
)
_OptionalGetStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_OptionalGetStudioSessionMappingInputRequestTypeDef",
    {
        "IdentityId": str,
        "IdentityName": str,
    },
    total=False,
)


class GetStudioSessionMappingInputRequestTypeDef(
    _RequiredGetStudioSessionMappingInputRequestTypeDef,
    _OptionalGetStudioSessionMappingInputRequestTypeDef,
):
    pass


SessionMappingDetailTypeDef = TypedDict(
    "SessionMappingDetailTypeDef",
    {
        "StudioId": str,
        "IdentityId": str,
        "IdentityName": str,
        "IdentityType": IdentityTypeType,
        "SessionPolicyArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

KeyValueTypeDef = TypedDict(
    "KeyValueTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

HadoopStepConfigTypeDef = TypedDict(
    "HadoopStepConfigTypeDef",
    {
        "Jar": str,
        "Properties": Dict[str, str],
        "MainClass": str,
        "Args": List[str],
    },
    total=False,
)

_RequiredInstanceFleetModifyConfigTypeDef = TypedDict(
    "_RequiredInstanceFleetModifyConfigTypeDef",
    {
        "InstanceFleetId": str,
    },
)
_OptionalInstanceFleetModifyConfigTypeDef = TypedDict(
    "_OptionalInstanceFleetModifyConfigTypeDef",
    {
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
    },
    total=False,
)


class InstanceFleetModifyConfigTypeDef(
    _RequiredInstanceFleetModifyConfigTypeDef, _OptionalInstanceFleetModifyConfigTypeDef
):
    pass


_RequiredSpotProvisioningSpecificationTypeDef = TypedDict(
    "_RequiredSpotProvisioningSpecificationTypeDef",
    {
        "TimeoutDurationMinutes": int,
        "TimeoutAction": SpotProvisioningTimeoutActionType,
    },
)
_OptionalSpotProvisioningSpecificationTypeDef = TypedDict(
    "_OptionalSpotProvisioningSpecificationTypeDef",
    {
        "BlockDurationMinutes": int,
        "AllocationStrategy": Literal["capacity-optimized"],
    },
    total=False,
)


class SpotProvisioningSpecificationTypeDef(
    _RequiredSpotProvisioningSpecificationTypeDef, _OptionalSpotProvisioningSpecificationTypeDef
):
    pass


InstanceFleetStateChangeReasonTypeDef = TypedDict(
    "InstanceFleetStateChangeReasonTypeDef",
    {
        "Code": InstanceFleetStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

InstanceFleetTimelineTypeDef = TypedDict(
    "InstanceFleetTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

_RequiredInstanceGroupDetailTypeDef = TypedDict(
    "_RequiredInstanceGroupDetailTypeDef",
    {
        "Market": MarketTypeType,
        "InstanceRole": InstanceRoleTypeType,
        "InstanceType": str,
        "InstanceRequestCount": int,
        "InstanceRunningCount": int,
        "State": InstanceGroupStateType,
        "CreationDateTime": datetime,
    },
)
_OptionalInstanceGroupDetailTypeDef = TypedDict(
    "_OptionalInstanceGroupDetailTypeDef",
    {
        "InstanceGroupId": str,
        "Name": str,
        "BidPrice": str,
        "LastStateChangeReason": str,
        "StartDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
        "CustomAmiId": str,
    },
    total=False,
)


class InstanceGroupDetailTypeDef(
    _RequiredInstanceGroupDetailTypeDef, _OptionalInstanceGroupDetailTypeDef
):
    pass


InstanceGroupStateChangeReasonTypeDef = TypedDict(
    "InstanceGroupStateChangeReasonTypeDef",
    {
        "Code": InstanceGroupStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

InstanceGroupTimelineTypeDef = TypedDict(
    "InstanceGroupTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

InstanceResizePolicyTypeDef = TypedDict(
    "InstanceResizePolicyTypeDef",
    {
        "InstancesToTerminate": List[str],
        "InstancesToProtect": List[str],
        "InstanceTerminationTimeout": int,
    },
    total=False,
)

InstanceStateChangeReasonTypeDef = TypedDict(
    "InstanceStateChangeReasonTypeDef",
    {
        "Code": InstanceStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

InstanceTimelineTypeDef = TypedDict(
    "InstanceTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

_RequiredJobFlowExecutionStatusDetailTypeDef = TypedDict(
    "_RequiredJobFlowExecutionStatusDetailTypeDef",
    {
        "State": JobFlowExecutionStateType,
        "CreationDateTime": datetime,
    },
)
_OptionalJobFlowExecutionStatusDetailTypeDef = TypedDict(
    "_OptionalJobFlowExecutionStatusDetailTypeDef",
    {
        "StartDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
        "LastStateChangeReason": str,
    },
    total=False,
)


class JobFlowExecutionStatusDetailTypeDef(
    _RequiredJobFlowExecutionStatusDetailTypeDef, _OptionalJobFlowExecutionStatusDetailTypeDef
):
    pass


PlacementTypeTypeDef = TypedDict(
    "PlacementTypeTypeDef",
    {
        "AvailabilityZone": str,
        "AvailabilityZones": List[str],
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

_RequiredListBootstrapActionsInputRequestTypeDef = TypedDict(
    "_RequiredListBootstrapActionsInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListBootstrapActionsInputRequestTypeDef = TypedDict(
    "_OptionalListBootstrapActionsInputRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)


class ListBootstrapActionsInputRequestTypeDef(
    _RequiredListBootstrapActionsInputRequestTypeDef,
    _OptionalListBootstrapActionsInputRequestTypeDef,
):
    pass


ListClustersInputRequestTypeDef = TypedDict(
    "ListClustersInputRequestTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "ClusterStates": Sequence[ClusterStateType],
        "Marker": str,
    },
    total=False,
)

_RequiredListInstanceFleetsInputRequestTypeDef = TypedDict(
    "_RequiredListInstanceFleetsInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstanceFleetsInputRequestTypeDef = TypedDict(
    "_OptionalListInstanceFleetsInputRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)


class ListInstanceFleetsInputRequestTypeDef(
    _RequiredListInstanceFleetsInputRequestTypeDef, _OptionalListInstanceFleetsInputRequestTypeDef
):
    pass


_RequiredListInstanceGroupsInputRequestTypeDef = TypedDict(
    "_RequiredListInstanceGroupsInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstanceGroupsInputRequestTypeDef = TypedDict(
    "_OptionalListInstanceGroupsInputRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)


class ListInstanceGroupsInputRequestTypeDef(
    _RequiredListInstanceGroupsInputRequestTypeDef, _OptionalListInstanceGroupsInputRequestTypeDef
):
    pass


_RequiredListInstancesInputRequestTypeDef = TypedDict(
    "_RequiredListInstancesInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstancesInputRequestTypeDef = TypedDict(
    "_OptionalListInstancesInputRequestTypeDef",
    {
        "InstanceGroupId": str,
        "InstanceGroupTypes": Sequence[InstanceGroupTypeType],
        "InstanceFleetId": str,
        "InstanceFleetType": InstanceFleetTypeType,
        "InstanceStates": Sequence[InstanceStateType],
        "Marker": str,
    },
    total=False,
)


class ListInstancesInputRequestTypeDef(
    _RequiredListInstancesInputRequestTypeDef, _OptionalListInstancesInputRequestTypeDef
):
    pass


ListNotebookExecutionsInputRequestTypeDef = TypedDict(
    "ListNotebookExecutionsInputRequestTypeDef",
    {
        "EditorId": str,
        "Status": NotebookExecutionStatusType,
        "From": Union[datetime, str],
        "To": Union[datetime, str],
        "Marker": str,
    },
    total=False,
)

NotebookExecutionSummaryTypeDef = TypedDict(
    "NotebookExecutionSummaryTypeDef",
    {
        "NotebookExecutionId": str,
        "EditorId": str,
        "NotebookExecutionName": str,
        "Status": NotebookExecutionStatusType,
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

ReleaseLabelFilterTypeDef = TypedDict(
    "ReleaseLabelFilterTypeDef",
    {
        "Prefix": str,
        "Application": str,
    },
    total=False,
)

ListSecurityConfigurationsInputRequestTypeDef = TypedDict(
    "ListSecurityConfigurationsInputRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)

SecurityConfigurationSummaryTypeDef = TypedDict(
    "SecurityConfigurationSummaryTypeDef",
    {
        "Name": str,
        "CreationDateTime": datetime,
    },
    total=False,
)

_RequiredListStepsInputRequestTypeDef = TypedDict(
    "_RequiredListStepsInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListStepsInputRequestTypeDef = TypedDict(
    "_OptionalListStepsInputRequestTypeDef",
    {
        "StepStates": Sequence[StepStateType],
        "StepIds": Sequence[str],
        "Marker": str,
    },
    total=False,
)


class ListStepsInputRequestTypeDef(
    _RequiredListStepsInputRequestTypeDef, _OptionalListStepsInputRequestTypeDef
):
    pass


ListStudioSessionMappingsInputRequestTypeDef = TypedDict(
    "ListStudioSessionMappingsInputRequestTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
        "Marker": str,
    },
    total=False,
)

SessionMappingSummaryTypeDef = TypedDict(
    "SessionMappingSummaryTypeDef",
    {
        "StudioId": str,
        "IdentityId": str,
        "IdentityName": str,
        "IdentityType": IdentityTypeType,
        "SessionPolicyArn": str,
        "CreationTime": datetime,
    },
    total=False,
)

ListStudiosInputRequestTypeDef = TypedDict(
    "ListStudiosInputRequestTypeDef",
    {
        "Marker": str,
    },
    total=False,
)

StudioSummaryTypeDef = TypedDict(
    "StudioSummaryTypeDef",
    {
        "StudioId": str,
        "Name": str,
        "VpcId": str,
        "Description": str,
        "Url": str,
        "AuthMode": AuthModeType,
        "CreationTime": datetime,
    },
    total=False,
)

_RequiredModifyClusterInputRequestTypeDef = TypedDict(
    "_RequiredModifyClusterInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalModifyClusterInputRequestTypeDef = TypedDict(
    "_OptionalModifyClusterInputRequestTypeDef",
    {
        "StepConcurrencyLevel": int,
    },
    total=False,
)


class ModifyClusterInputRequestTypeDef(
    _RequiredModifyClusterInputRequestTypeDef, _OptionalModifyClusterInputRequestTypeDef
):
    pass


OnDemandCapacityReservationOptionsTypeDef = TypedDict(
    "OnDemandCapacityReservationOptionsTypeDef",
    {
        "UsageStrategy": Literal["use-capacity-reservations-first"],
        "CapacityReservationPreference": OnDemandCapacityReservationPreferenceType,
        "CapacityReservationResourceGroupArn": str,
    },
    total=False,
)

RemoveAutoScalingPolicyInputRequestTypeDef = TypedDict(
    "RemoveAutoScalingPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
        "InstanceGroupId": str,
    },
)

RemoveAutoTerminationPolicyInputRequestTypeDef = TypedDict(
    "RemoveAutoTerminationPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)

RemoveManagedScalingPolicyInputRequestTypeDef = TypedDict(
    "RemoveManagedScalingPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)

RemoveTagsInputRequestTypeDef = TypedDict(
    "RemoveTagsInputRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

SupportedProductConfigTypeDef = TypedDict(
    "SupportedProductConfigTypeDef",
    {
        "Name": str,
        "Args": Sequence[str],
    },
    total=False,
)

_RequiredSimpleScalingPolicyConfigurationTypeDef = TypedDict(
    "_RequiredSimpleScalingPolicyConfigurationTypeDef",
    {
        "ScalingAdjustment": int,
    },
)
_OptionalSimpleScalingPolicyConfigurationTypeDef = TypedDict(
    "_OptionalSimpleScalingPolicyConfigurationTypeDef",
    {
        "AdjustmentType": AdjustmentTypeType,
        "CoolDown": int,
    },
    total=False,
)


class SimpleScalingPolicyConfigurationTypeDef(
    _RequiredSimpleScalingPolicyConfigurationTypeDef,
    _OptionalSimpleScalingPolicyConfigurationTypeDef,
):
    pass


SetTerminationProtectionInputRequestTypeDef = TypedDict(
    "SetTerminationProtectionInputRequestTypeDef",
    {
        "JobFlowIds": Sequence[str],
        "TerminationProtected": bool,
    },
)

SetVisibleToAllUsersInputRequestTypeDef = TypedDict(
    "SetVisibleToAllUsersInputRequestTypeDef",
    {
        "JobFlowIds": Sequence[str],
        "VisibleToAllUsers": bool,
    },
)

_RequiredStepExecutionStatusDetailTypeDef = TypedDict(
    "_RequiredStepExecutionStatusDetailTypeDef",
    {
        "State": StepExecutionStateType,
        "CreationDateTime": datetime,
    },
)
_OptionalStepExecutionStatusDetailTypeDef = TypedDict(
    "_OptionalStepExecutionStatusDetailTypeDef",
    {
        "StartDateTime": datetime,
        "EndDateTime": datetime,
        "LastStateChangeReason": str,
    },
    total=False,
)


class StepExecutionStatusDetailTypeDef(
    _RequiredStepExecutionStatusDetailTypeDef, _OptionalStepExecutionStatusDetailTypeDef
):
    pass


StepStateChangeReasonTypeDef = TypedDict(
    "StepStateChangeReasonTypeDef",
    {
        "Code": Literal["NONE"],
        "Message": str,
    },
    total=False,
)

StepTimelineTypeDef = TypedDict(
    "StepTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "StartDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

StopNotebookExecutionInputRequestTypeDef = TypedDict(
    "StopNotebookExecutionInputRequestTypeDef",
    {
        "NotebookExecutionId": str,
    },
)

TerminateJobFlowsInputRequestTypeDef = TypedDict(
    "TerminateJobFlowsInputRequestTypeDef",
    {
        "JobFlowIds": Sequence[str],
    },
)

_RequiredUpdateStudioInputRequestTypeDef = TypedDict(
    "_RequiredUpdateStudioInputRequestTypeDef",
    {
        "StudioId": str,
    },
)
_OptionalUpdateStudioInputRequestTypeDef = TypedDict(
    "_OptionalUpdateStudioInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "SubnetIds": Sequence[str],
        "DefaultS3Location": str,
    },
    total=False,
)


class UpdateStudioInputRequestTypeDef(
    _RequiredUpdateStudioInputRequestTypeDef, _OptionalUpdateStudioInputRequestTypeDef
):
    pass


_RequiredUpdateStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_RequiredUpdateStudioSessionMappingInputRequestTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
        "SessionPolicyArn": str,
    },
)
_OptionalUpdateStudioSessionMappingInputRequestTypeDef = TypedDict(
    "_OptionalUpdateStudioSessionMappingInputRequestTypeDef",
    {
        "IdentityId": str,
        "IdentityName": str,
    },
    total=False,
)


class UpdateStudioSessionMappingInputRequestTypeDef(
    _RequiredUpdateStudioSessionMappingInputRequestTypeDef,
    _OptionalUpdateStudioSessionMappingInputRequestTypeDef,
):
    pass


AddInstanceFleetOutputTypeDef = TypedDict(
    "AddInstanceFleetOutputTypeDef",
    {
        "ClusterId": str,
        "InstanceFleetId": str,
        "ClusterArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddInstanceGroupsOutputTypeDef = TypedDict(
    "AddInstanceGroupsOutputTypeDef",
    {
        "JobFlowId": str,
        "InstanceGroupIds": List[str],
        "ClusterArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddJobFlowStepsOutputTypeDef = TypedDict(
    "AddJobFlowStepsOutputTypeDef",
    {
        "StepIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSecurityConfigurationOutputTypeDef = TypedDict(
    "CreateSecurityConfigurationOutputTypeDef",
    {
        "Name": str,
        "CreationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStudioOutputTypeDef = TypedDict(
    "CreateStudioOutputTypeDef",
    {
        "StudioId": str,
        "Url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSecurityConfigurationOutputTypeDef = TypedDict(
    "DescribeSecurityConfigurationOutputTypeDef",
    {
        "Name": str,
        "SecurityConfiguration": str,
        "CreationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReleaseLabelsOutputTypeDef = TypedDict(
    "ListReleaseLabelsOutputTypeDef",
    {
        "ReleaseLabels": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyClusterOutputTypeDef = TypedDict(
    "ModifyClusterOutputTypeDef",
    {
        "StepConcurrencyLevel": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunJobFlowOutputTypeDef = TypedDict(
    "RunJobFlowOutputTypeDef",
    {
        "JobFlowId": str,
        "ClusterArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartNotebookExecutionOutputTypeDef = TypedDict(
    "StartNotebookExecutionOutputTypeDef",
    {
        "NotebookExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "ResourceId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateStudioInputRequestTypeDef = TypedDict(
    "_RequiredCreateStudioInputRequestTypeDef",
    {
        "Name": str,
        "AuthMode": AuthModeType,
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "ServiceRole": str,
        "WorkspaceSecurityGroupId": str,
        "EngineSecurityGroupId": str,
        "DefaultS3Location": str,
    },
)
_OptionalCreateStudioInputRequestTypeDef = TypedDict(
    "_OptionalCreateStudioInputRequestTypeDef",
    {
        "Description": str,
        "UserRole": str,
        "IdpAuthUrl": str,
        "IdpRelayStateParameterName": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateStudioInputRequestTypeDef(
    _RequiredCreateStudioInputRequestTypeDef, _OptionalCreateStudioInputRequestTypeDef
):
    pass


StudioTypeDef = TypedDict(
    "StudioTypeDef",
    {
        "StudioId": str,
        "StudioArn": str,
        "Name": str,
        "Description": str,
        "AuthMode": AuthModeType,
        "VpcId": str,
        "SubnetIds": List[str],
        "ServiceRole": str,
        "UserRole": str,
        "WorkspaceSecurityGroupId": str,
        "EngineSecurityGroupId": str,
        "Url": str,
        "CreationTime": datetime,
        "DefaultS3Location": str,
        "IdpAuthUrl": str,
        "IdpRelayStateParameterName": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

AutoScalingPolicyStatusTypeDef = TypedDict(
    "AutoScalingPolicyStatusTypeDef",
    {
        "State": AutoScalingPolicyStateType,
        "StateChangeReason": AutoScalingPolicyStateChangeReasonTypeDef,
    },
    total=False,
)

GetAutoTerminationPolicyOutputTypeDef = TypedDict(
    "GetAutoTerminationPolicyOutputTypeDef",
    {
        "AutoTerminationPolicy": AutoTerminationPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutAutoTerminationPolicyInputRequestTypeDef = TypedDict(
    "_RequiredPutAutoTerminationPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalPutAutoTerminationPolicyInputRequestTypeDef = TypedDict(
    "_OptionalPutAutoTerminationPolicyInputRequestTypeDef",
    {
        "AutoTerminationPolicy": AutoTerminationPolicyTypeDef,
    },
    total=False,
)


class PutAutoTerminationPolicyInputRequestTypeDef(
    _RequiredPutAutoTerminationPolicyInputRequestTypeDef,
    _OptionalPutAutoTerminationPolicyInputRequestTypeDef,
):
    pass


_RequiredBlockPublicAccessConfigurationTypeDef = TypedDict(
    "_RequiredBlockPublicAccessConfigurationTypeDef",
    {
        "BlockPublicSecurityGroupRules": bool,
    },
)
_OptionalBlockPublicAccessConfigurationTypeDef = TypedDict(
    "_OptionalBlockPublicAccessConfigurationTypeDef",
    {
        "PermittedPublicSecurityGroupRuleRanges": List[PortRangeTypeDef],
    },
    total=False,
)


class BlockPublicAccessConfigurationTypeDef(
    _RequiredBlockPublicAccessConfigurationTypeDef, _OptionalBlockPublicAccessConfigurationTypeDef
):
    pass


BootstrapActionConfigTypeDef = TypedDict(
    "BootstrapActionConfigTypeDef",
    {
        "Name": str,
        "ScriptBootstrapAction": ScriptBootstrapActionConfigTypeDef,
    },
)

CancelStepsOutputTypeDef = TypedDict(
    "CancelStepsOutputTypeDef",
    {
        "CancelStepsInfoList": List[CancelStepsInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCloudWatchAlarmDefinitionTypeDef = TypedDict(
    "_RequiredCloudWatchAlarmDefinitionTypeDef",
    {
        "ComparisonOperator": ComparisonOperatorType,
        "MetricName": str,
        "Period": int,
        "Threshold": float,
    },
)
_OptionalCloudWatchAlarmDefinitionTypeDef = TypedDict(
    "_OptionalCloudWatchAlarmDefinitionTypeDef",
    {
        "EvaluationPeriods": int,
        "Namespace": str,
        "Statistic": StatisticType,
        "Unit": UnitType,
        "Dimensions": Sequence[MetricDimensionTypeDef],
    },
    total=False,
)


class CloudWatchAlarmDefinitionTypeDef(
    _RequiredCloudWatchAlarmDefinitionTypeDef, _OptionalCloudWatchAlarmDefinitionTypeDef
):
    pass


ClusterStatusTypeDef = TypedDict(
    "ClusterStatusTypeDef",
    {
        "State": ClusterStateType,
        "StateChangeReason": ClusterStateChangeReasonTypeDef,
        "Timeline": ClusterTimelineTypeDef,
    },
    total=False,
)

ListBootstrapActionsOutputTypeDef = TypedDict(
    "ListBootstrapActionsOutputTypeDef",
    {
        "BootstrapActions": List[CommandTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ManagedScalingPolicyTypeDef = TypedDict(
    "ManagedScalingPolicyTypeDef",
    {
        "ComputeLimits": ComputeLimitsTypeDef,
    },
    total=False,
)

_RequiredDescribeClusterInputClusterRunningWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterInputClusterRunningWaitTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalDescribeClusterInputClusterRunningWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterInputClusterRunningWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeClusterInputClusterRunningWaitTypeDef(
    _RequiredDescribeClusterInputClusterRunningWaitTypeDef,
    _OptionalDescribeClusterInputClusterRunningWaitTypeDef,
):
    pass


_RequiredDescribeClusterInputClusterTerminatedWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterInputClusterTerminatedWaitTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalDescribeClusterInputClusterTerminatedWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterInputClusterTerminatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeClusterInputClusterTerminatedWaitTypeDef(
    _RequiredDescribeClusterInputClusterTerminatedWaitTypeDef,
    _OptionalDescribeClusterInputClusterTerminatedWaitTypeDef,
):
    pass


_RequiredDescribeStepInputStepCompleteWaitTypeDef = TypedDict(
    "_RequiredDescribeStepInputStepCompleteWaitTypeDef",
    {
        "ClusterId": str,
        "StepId": str,
    },
)
_OptionalDescribeStepInputStepCompleteWaitTypeDef = TypedDict(
    "_OptionalDescribeStepInputStepCompleteWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeStepInputStepCompleteWaitTypeDef(
    _RequiredDescribeStepInputStepCompleteWaitTypeDef,
    _OptionalDescribeStepInputStepCompleteWaitTypeDef,
):
    pass


DescribeReleaseLabelOutputTypeDef = TypedDict(
    "DescribeReleaseLabelOutputTypeDef",
    {
        "ReleaseLabel": str,
        "Applications": List[SimplifiedApplicationTypeDef],
        "NextToken": str,
        "AvailableOSReleases": List[OSReleaseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredEbsBlockDeviceConfigTypeDef = TypedDict(
    "_RequiredEbsBlockDeviceConfigTypeDef",
    {
        "VolumeSpecification": VolumeSpecificationTypeDef,
    },
)
_OptionalEbsBlockDeviceConfigTypeDef = TypedDict(
    "_OptionalEbsBlockDeviceConfigTypeDef",
    {
        "VolumesPerInstance": int,
    },
    total=False,
)


class EbsBlockDeviceConfigTypeDef(
    _RequiredEbsBlockDeviceConfigTypeDef, _OptionalEbsBlockDeviceConfigTypeDef
):
    pass


EbsBlockDeviceTypeDef = TypedDict(
    "EbsBlockDeviceTypeDef",
    {
        "VolumeSpecification": VolumeSpecificationTypeDef,
        "Device": str,
    },
    total=False,
)

NotebookExecutionTypeDef = TypedDict(
    "NotebookExecutionTypeDef",
    {
        "NotebookExecutionId": str,
        "EditorId": str,
        "ExecutionEngine": ExecutionEngineConfigTypeDef,
        "NotebookExecutionName": str,
        "NotebookParams": str,
        "Status": NotebookExecutionStatusType,
        "StartTime": datetime,
        "EndTime": datetime,
        "Arn": str,
        "OutputNotebookURI": str,
        "LastStateChangeReason": str,
        "NotebookInstanceSecurityGroupId": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

_RequiredStartNotebookExecutionInputRequestTypeDef = TypedDict(
    "_RequiredStartNotebookExecutionInputRequestTypeDef",
    {
        "EditorId": str,
        "RelativePath": str,
        "ExecutionEngine": ExecutionEngineConfigTypeDef,
        "ServiceRole": str,
    },
)
_OptionalStartNotebookExecutionInputRequestTypeDef = TypedDict(
    "_OptionalStartNotebookExecutionInputRequestTypeDef",
    {
        "NotebookExecutionName": str,
        "NotebookParams": str,
        "NotebookInstanceSecurityGroupId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartNotebookExecutionInputRequestTypeDef(
    _RequiredStartNotebookExecutionInputRequestTypeDef,
    _OptionalStartNotebookExecutionInputRequestTypeDef,
):
    pass


GetStudioSessionMappingOutputTypeDef = TypedDict(
    "GetStudioSessionMappingOutputTypeDef",
    {
        "SessionMapping": SessionMappingDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredHadoopJarStepConfigTypeDef = TypedDict(
    "_RequiredHadoopJarStepConfigTypeDef",
    {
        "Jar": str,
    },
)
_OptionalHadoopJarStepConfigTypeDef = TypedDict(
    "_OptionalHadoopJarStepConfigTypeDef",
    {
        "Properties": Sequence[KeyValueTypeDef],
        "MainClass": str,
        "Args": Sequence[str],
    },
    total=False,
)


class HadoopJarStepConfigTypeDef(
    _RequiredHadoopJarStepConfigTypeDef, _OptionalHadoopJarStepConfigTypeDef
):
    pass


ModifyInstanceFleetInputRequestTypeDef = TypedDict(
    "ModifyInstanceFleetInputRequestTypeDef",
    {
        "ClusterId": str,
        "InstanceFleet": InstanceFleetModifyConfigTypeDef,
    },
)

InstanceFleetStatusTypeDef = TypedDict(
    "InstanceFleetStatusTypeDef",
    {
        "State": InstanceFleetStateType,
        "StateChangeReason": InstanceFleetStateChangeReasonTypeDef,
        "Timeline": InstanceFleetTimelineTypeDef,
    },
    total=False,
)

InstanceGroupStatusTypeDef = TypedDict(
    "InstanceGroupStatusTypeDef",
    {
        "State": InstanceGroupStateType,
        "StateChangeReason": InstanceGroupStateChangeReasonTypeDef,
        "Timeline": InstanceGroupTimelineTypeDef,
    },
    total=False,
)

ShrinkPolicyTypeDef = TypedDict(
    "ShrinkPolicyTypeDef",
    {
        "DecommissionTimeout": int,
        "InstanceResizePolicy": InstanceResizePolicyTypeDef,
    },
    total=False,
)

InstanceStatusTypeDef = TypedDict(
    "InstanceStatusTypeDef",
    {
        "State": InstanceStateType,
        "StateChangeReason": InstanceStateChangeReasonTypeDef,
        "Timeline": InstanceTimelineTypeDef,
    },
    total=False,
)

_RequiredJobFlowInstancesDetailTypeDef = TypedDict(
    "_RequiredJobFlowInstancesDetailTypeDef",
    {
        "MasterInstanceType": str,
        "SlaveInstanceType": str,
        "InstanceCount": int,
    },
)
_OptionalJobFlowInstancesDetailTypeDef = TypedDict(
    "_OptionalJobFlowInstancesDetailTypeDef",
    {
        "MasterPublicDnsName": str,
        "MasterInstanceId": str,
        "InstanceGroups": List[InstanceGroupDetailTypeDef],
        "NormalizedInstanceHours": int,
        "Ec2KeyName": str,
        "Ec2SubnetId": str,
        "Placement": PlacementTypeTypeDef,
        "KeepJobFlowAliveWhenNoSteps": bool,
        "TerminationProtected": bool,
        "HadoopVersion": str,
    },
    total=False,
)


class JobFlowInstancesDetailTypeDef(
    _RequiredJobFlowInstancesDetailTypeDef, _OptionalJobFlowInstancesDetailTypeDef
):
    pass


_RequiredListBootstrapActionsInputListBootstrapActionsPaginateTypeDef = TypedDict(
    "_RequiredListBootstrapActionsInputListBootstrapActionsPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListBootstrapActionsInputListBootstrapActionsPaginateTypeDef = TypedDict(
    "_OptionalListBootstrapActionsInputListBootstrapActionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef(
    _RequiredListBootstrapActionsInputListBootstrapActionsPaginateTypeDef,
    _OptionalListBootstrapActionsInputListBootstrapActionsPaginateTypeDef,
):
    pass


ListClustersInputListClustersPaginateTypeDef = TypedDict(
    "ListClustersInputListClustersPaginateTypeDef",
    {
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "ClusterStates": Sequence[ClusterStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListInstanceFleetsInputListInstanceFleetsPaginateTypeDef = TypedDict(
    "_RequiredListInstanceFleetsInputListInstanceFleetsPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstanceFleetsInputListInstanceFleetsPaginateTypeDef = TypedDict(
    "_OptionalListInstanceFleetsInputListInstanceFleetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef(
    _RequiredListInstanceFleetsInputListInstanceFleetsPaginateTypeDef,
    _OptionalListInstanceFleetsInputListInstanceFleetsPaginateTypeDef,
):
    pass


_RequiredListInstanceGroupsInputListInstanceGroupsPaginateTypeDef = TypedDict(
    "_RequiredListInstanceGroupsInputListInstanceGroupsPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstanceGroupsInputListInstanceGroupsPaginateTypeDef = TypedDict(
    "_OptionalListInstanceGroupsInputListInstanceGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef(
    _RequiredListInstanceGroupsInputListInstanceGroupsPaginateTypeDef,
    _OptionalListInstanceGroupsInputListInstanceGroupsPaginateTypeDef,
):
    pass


_RequiredListInstancesInputListInstancesPaginateTypeDef = TypedDict(
    "_RequiredListInstancesInputListInstancesPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListInstancesInputListInstancesPaginateTypeDef = TypedDict(
    "_OptionalListInstancesInputListInstancesPaginateTypeDef",
    {
        "InstanceGroupId": str,
        "InstanceGroupTypes": Sequence[InstanceGroupTypeType],
        "InstanceFleetId": str,
        "InstanceFleetType": InstanceFleetTypeType,
        "InstanceStates": Sequence[InstanceStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInstancesInputListInstancesPaginateTypeDef(
    _RequiredListInstancesInputListInstancesPaginateTypeDef,
    _OptionalListInstancesInputListInstancesPaginateTypeDef,
):
    pass


ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef = TypedDict(
    "ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef",
    {
        "EditorId": str,
        "Status": NotebookExecutionStatusType,
        "From": Union[datetime, str],
        "To": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef = TypedDict(
    "ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListStepsInputListStepsPaginateTypeDef = TypedDict(
    "_RequiredListStepsInputListStepsPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListStepsInputListStepsPaginateTypeDef = TypedDict(
    "_OptionalListStepsInputListStepsPaginateTypeDef",
    {
        "StepStates": Sequence[StepStateType],
        "StepIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListStepsInputListStepsPaginateTypeDef(
    _RequiredListStepsInputListStepsPaginateTypeDef, _OptionalListStepsInputListStepsPaginateTypeDef
):
    pass


ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef = TypedDict(
    "ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef",
    {
        "StudioId": str,
        "IdentityType": IdentityTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListStudiosInputListStudiosPaginateTypeDef = TypedDict(
    "ListStudiosInputListStudiosPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListNotebookExecutionsOutputTypeDef = TypedDict(
    "ListNotebookExecutionsOutputTypeDef",
    {
        "NotebookExecutions": List[NotebookExecutionSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReleaseLabelsInputRequestTypeDef = TypedDict(
    "ListReleaseLabelsInputRequestTypeDef",
    {
        "Filters": ReleaseLabelFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListSecurityConfigurationsOutputTypeDef = TypedDict(
    "ListSecurityConfigurationsOutputTypeDef",
    {
        "SecurityConfigurations": List[SecurityConfigurationSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStudioSessionMappingsOutputTypeDef = TypedDict(
    "ListStudioSessionMappingsOutputTypeDef",
    {
        "SessionMappings": List[SessionMappingSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStudiosOutputTypeDef = TypedDict(
    "ListStudiosOutputTypeDef",
    {
        "Studios": List[StudioSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredOnDemandProvisioningSpecificationTypeDef = TypedDict(
    "_RequiredOnDemandProvisioningSpecificationTypeDef",
    {
        "AllocationStrategy": Literal["lowest-price"],
    },
)
_OptionalOnDemandProvisioningSpecificationTypeDef = TypedDict(
    "_OptionalOnDemandProvisioningSpecificationTypeDef",
    {
        "CapacityReservationOptions": OnDemandCapacityReservationOptionsTypeDef,
    },
    total=False,
)


class OnDemandProvisioningSpecificationTypeDef(
    _RequiredOnDemandProvisioningSpecificationTypeDef,
    _OptionalOnDemandProvisioningSpecificationTypeDef,
):
    pass


_RequiredScalingActionTypeDef = TypedDict(
    "_RequiredScalingActionTypeDef",
    {
        "SimpleScalingPolicyConfiguration": SimpleScalingPolicyConfigurationTypeDef,
    },
)
_OptionalScalingActionTypeDef = TypedDict(
    "_OptionalScalingActionTypeDef",
    {
        "Market": MarketTypeType,
    },
    total=False,
)


class ScalingActionTypeDef(_RequiredScalingActionTypeDef, _OptionalScalingActionTypeDef):
    pass


StepStatusTypeDef = TypedDict(
    "StepStatusTypeDef",
    {
        "State": StepStateType,
        "StateChangeReason": StepStateChangeReasonTypeDef,
        "FailureDetails": FailureDetailsTypeDef,
        "Timeline": StepTimelineTypeDef,
    },
    total=False,
)

DescribeStudioOutputTypeDef = TypedDict(
    "DescribeStudioOutputTypeDef",
    {
        "Studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBlockPublicAccessConfigurationOutputTypeDef = TypedDict(
    "GetBlockPublicAccessConfigurationOutputTypeDef",
    {
        "BlockPublicAccessConfiguration": BlockPublicAccessConfigurationTypeDef,
        "BlockPublicAccessConfigurationMetadata": BlockPublicAccessConfigurationMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutBlockPublicAccessConfigurationInputRequestTypeDef = TypedDict(
    "PutBlockPublicAccessConfigurationInputRequestTypeDef",
    {
        "BlockPublicAccessConfiguration": BlockPublicAccessConfigurationTypeDef,
    },
)

BootstrapActionDetailTypeDef = TypedDict(
    "BootstrapActionDetailTypeDef",
    {
        "BootstrapActionConfig": BootstrapActionConfigTypeDef,
    },
    total=False,
)

ScalingTriggerTypeDef = TypedDict(
    "ScalingTriggerTypeDef",
    {
        "CloudWatchAlarmDefinition": CloudWatchAlarmDefinitionTypeDef,
    },
)

ClusterSummaryTypeDef = TypedDict(
    "ClusterSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": ClusterStatusTypeDef,
        "NormalizedInstanceHours": int,
        "ClusterArn": str,
        "OutpostArn": str,
    },
    total=False,
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": ClusterStatusTypeDef,
        "Ec2InstanceAttributes": Ec2InstanceAttributesTypeDef,
        "InstanceCollectionType": InstanceCollectionTypeType,
        "LogUri": str,
        "LogEncryptionKmsKeyId": str,
        "RequestedAmiVersion": str,
        "RunningAmiVersion": str,
        "ReleaseLabel": str,
        "AutoTerminate": bool,
        "TerminationProtected": bool,
        "VisibleToAllUsers": bool,
        "Applications": List[ApplicationTypeDef],
        "Tags": List[TagTypeDef],
        "ServiceRole": str,
        "NormalizedInstanceHours": int,
        "MasterPublicDnsName": str,
        "Configurations": List["ConfigurationTypeDef"],
        "SecurityConfiguration": str,
        "AutoScalingRole": str,
        "ScaleDownBehavior": ScaleDownBehaviorType,
        "CustomAmiId": str,
        "EbsRootVolumeSize": int,
        "RepoUpgradeOnBoot": RepoUpgradeOnBootType,
        "KerberosAttributes": KerberosAttributesTypeDef,
        "ClusterArn": str,
        "OutpostArn": str,
        "StepConcurrencyLevel": int,
        "PlacementGroups": List[PlacementGroupConfigTypeDef],
        "OSReleaseLabel": str,
    },
    total=False,
)

GetManagedScalingPolicyOutputTypeDef = TypedDict(
    "GetManagedScalingPolicyOutputTypeDef",
    {
        "ManagedScalingPolicy": ManagedScalingPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutManagedScalingPolicyInputRequestTypeDef = TypedDict(
    "PutManagedScalingPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
        "ManagedScalingPolicy": ManagedScalingPolicyTypeDef,
    },
)

EbsConfigurationTypeDef = TypedDict(
    "EbsConfigurationTypeDef",
    {
        "EbsBlockDeviceConfigs": Sequence[EbsBlockDeviceConfigTypeDef],
        "EbsOptimized": bool,
    },
    total=False,
)

InstanceTypeSpecificationTypeDef = TypedDict(
    "InstanceTypeSpecificationTypeDef",
    {
        "InstanceType": str,
        "WeightedCapacity": int,
        "BidPrice": str,
        "BidPriceAsPercentageOfOnDemandPrice": float,
        "Configurations": List["ConfigurationTypeDef"],
        "EbsBlockDevices": List[EbsBlockDeviceTypeDef],
        "EbsOptimized": bool,
        "CustomAmiId": str,
    },
    total=False,
)

DescribeNotebookExecutionOutputTypeDef = TypedDict(
    "DescribeNotebookExecutionOutputTypeDef",
    {
        "NotebookExecution": NotebookExecutionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStepConfigTypeDef = TypedDict(
    "_RequiredStepConfigTypeDef",
    {
        "Name": str,
        "HadoopJarStep": HadoopJarStepConfigTypeDef,
    },
)
_OptionalStepConfigTypeDef = TypedDict(
    "_OptionalStepConfigTypeDef",
    {
        "ActionOnFailure": ActionOnFailureType,
    },
    total=False,
)


class StepConfigTypeDef(_RequiredStepConfigTypeDef, _OptionalStepConfigTypeDef):
    pass


_RequiredInstanceGroupModifyConfigTypeDef = TypedDict(
    "_RequiredInstanceGroupModifyConfigTypeDef",
    {
        "InstanceGroupId": str,
    },
)
_OptionalInstanceGroupModifyConfigTypeDef = TypedDict(
    "_OptionalInstanceGroupModifyConfigTypeDef",
    {
        "InstanceCount": int,
        "EC2InstanceIdsToTerminate": Sequence[str],
        "ShrinkPolicy": ShrinkPolicyTypeDef,
        "ReconfigurationType": ReconfigurationTypeType,
        "Configurations": Sequence["ConfigurationTypeDef"],
    },
    total=False,
)


class InstanceGroupModifyConfigTypeDef(
    _RequiredInstanceGroupModifyConfigTypeDef, _OptionalInstanceGroupModifyConfigTypeDef
):
    pass


InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "Id": str,
        "Ec2InstanceId": str,
        "PublicDnsName": str,
        "PublicIpAddress": str,
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
        "Status": InstanceStatusTypeDef,
        "InstanceGroupId": str,
        "InstanceFleetId": str,
        "Market": MarketTypeType,
        "InstanceType": str,
        "EbsVolumes": List[EbsVolumeTypeDef],
    },
    total=False,
)

InstanceFleetProvisioningSpecificationsTypeDef = TypedDict(
    "InstanceFleetProvisioningSpecificationsTypeDef",
    {
        "SpotSpecification": SpotProvisioningSpecificationTypeDef,
        "OnDemandSpecification": OnDemandProvisioningSpecificationTypeDef,
    },
    total=False,
)

StepSummaryTypeDef = TypedDict(
    "StepSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Config": HadoopStepConfigTypeDef,
        "ActionOnFailure": ActionOnFailureType,
        "Status": StepStatusTypeDef,
    },
    total=False,
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "Id": str,
        "Name": str,
        "Config": HadoopStepConfigTypeDef,
        "ActionOnFailure": ActionOnFailureType,
        "Status": StepStatusTypeDef,
    },
    total=False,
)

_RequiredScalingRuleTypeDef = TypedDict(
    "_RequiredScalingRuleTypeDef",
    {
        "Name": str,
        "Action": ScalingActionTypeDef,
        "Trigger": ScalingTriggerTypeDef,
    },
)
_OptionalScalingRuleTypeDef = TypedDict(
    "_OptionalScalingRuleTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class ScalingRuleTypeDef(_RequiredScalingRuleTypeDef, _OptionalScalingRuleTypeDef):
    pass


ListClustersOutputTypeDef = TypedDict(
    "ListClustersOutputTypeDef",
    {
        "Clusters": List[ClusterSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterOutputTypeDef = TypedDict(
    "DescribeClusterOutputTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredInstanceTypeConfigTypeDef = TypedDict(
    "_RequiredInstanceTypeConfigTypeDef",
    {
        "InstanceType": str,
    },
)
_OptionalInstanceTypeConfigTypeDef = TypedDict(
    "_OptionalInstanceTypeConfigTypeDef",
    {
        "WeightedCapacity": int,
        "BidPrice": str,
        "BidPriceAsPercentageOfOnDemandPrice": float,
        "EbsConfiguration": EbsConfigurationTypeDef,
        "Configurations": Sequence["ConfigurationTypeDef"],
        "CustomAmiId": str,
    },
    total=False,
)


class InstanceTypeConfigTypeDef(
    _RequiredInstanceTypeConfigTypeDef, _OptionalInstanceTypeConfigTypeDef
):
    pass


AddJobFlowStepsInputRequestTypeDef = TypedDict(
    "AddJobFlowStepsInputRequestTypeDef",
    {
        "JobFlowId": str,
        "Steps": Sequence[StepConfigTypeDef],
    },
)

StepDetailTypeDef = TypedDict(
    "StepDetailTypeDef",
    {
        "StepConfig": StepConfigTypeDef,
        "ExecutionStatusDetail": StepExecutionStatusDetailTypeDef,
    },
)

ModifyInstanceGroupsInputRequestTypeDef = TypedDict(
    "ModifyInstanceGroupsInputRequestTypeDef",
    {
        "ClusterId": str,
        "InstanceGroups": Sequence[InstanceGroupModifyConfigTypeDef],
    },
    total=False,
)

ListInstancesOutputTypeDef = TypedDict(
    "ListInstancesOutputTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceFleetTypeDef = TypedDict(
    "InstanceFleetTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": InstanceFleetStatusTypeDef,
        "InstanceFleetType": InstanceFleetTypeType,
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
        "ProvisionedOnDemandCapacity": int,
        "ProvisionedSpotCapacity": int,
        "InstanceTypeSpecifications": List[InstanceTypeSpecificationTypeDef],
        "LaunchSpecifications": InstanceFleetProvisioningSpecificationsTypeDef,
    },
    total=False,
)

ListStepsOutputTypeDef = TypedDict(
    "ListStepsOutputTypeDef",
    {
        "Steps": List[StepSummaryTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStepOutputTypeDef = TypedDict(
    "DescribeStepOutputTypeDef",
    {
        "Step": StepTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutoScalingPolicyDescriptionTypeDef = TypedDict(
    "AutoScalingPolicyDescriptionTypeDef",
    {
        "Status": AutoScalingPolicyStatusTypeDef,
        "Constraints": ScalingConstraintsTypeDef,
        "Rules": List[ScalingRuleTypeDef],
    },
    total=False,
)

AutoScalingPolicyTypeDef = TypedDict(
    "AutoScalingPolicyTypeDef",
    {
        "Constraints": ScalingConstraintsTypeDef,
        "Rules": Sequence[ScalingRuleTypeDef],
    },
)

_RequiredInstanceFleetConfigTypeDef = TypedDict(
    "_RequiredInstanceFleetConfigTypeDef",
    {
        "InstanceFleetType": InstanceFleetTypeType,
    },
)
_OptionalInstanceFleetConfigTypeDef = TypedDict(
    "_OptionalInstanceFleetConfigTypeDef",
    {
        "Name": str,
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
        "InstanceTypeConfigs": Sequence[InstanceTypeConfigTypeDef],
        "LaunchSpecifications": InstanceFleetProvisioningSpecificationsTypeDef,
    },
    total=False,
)


class InstanceFleetConfigTypeDef(
    _RequiredInstanceFleetConfigTypeDef, _OptionalInstanceFleetConfigTypeDef
):
    pass


_RequiredJobFlowDetailTypeDef = TypedDict(
    "_RequiredJobFlowDetailTypeDef",
    {
        "JobFlowId": str,
        "Name": str,
        "ExecutionStatusDetail": JobFlowExecutionStatusDetailTypeDef,
        "Instances": JobFlowInstancesDetailTypeDef,
    },
)
_OptionalJobFlowDetailTypeDef = TypedDict(
    "_OptionalJobFlowDetailTypeDef",
    {
        "LogUri": str,
        "LogEncryptionKmsKeyId": str,
        "AmiVersion": str,
        "Steps": List[StepDetailTypeDef],
        "BootstrapActions": List[BootstrapActionDetailTypeDef],
        "SupportedProducts": List[str],
        "VisibleToAllUsers": bool,
        "JobFlowRole": str,
        "ServiceRole": str,
        "AutoScalingRole": str,
        "ScaleDownBehavior": ScaleDownBehaviorType,
    },
    total=False,
)


class JobFlowDetailTypeDef(_RequiredJobFlowDetailTypeDef, _OptionalJobFlowDetailTypeDef):
    pass


ListInstanceFleetsOutputTypeDef = TypedDict(
    "ListInstanceFleetsOutputTypeDef",
    {
        "InstanceFleets": List[InstanceFleetTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceGroupTypeDef = TypedDict(
    "InstanceGroupTypeDef",
    {
        "Id": str,
        "Name": str,
        "Market": MarketTypeType,
        "InstanceGroupType": InstanceGroupTypeType,
        "BidPrice": str,
        "InstanceType": str,
        "RequestedInstanceCount": int,
        "RunningInstanceCount": int,
        "Status": InstanceGroupStatusTypeDef,
        "Configurations": List["ConfigurationTypeDef"],
        "ConfigurationsVersion": int,
        "LastSuccessfullyAppliedConfigurations": List["ConfigurationTypeDef"],
        "LastSuccessfullyAppliedConfigurationsVersion": int,
        "EbsBlockDevices": List[EbsBlockDeviceTypeDef],
        "EbsOptimized": bool,
        "ShrinkPolicy": ShrinkPolicyTypeDef,
        "AutoScalingPolicy": AutoScalingPolicyDescriptionTypeDef,
        "CustomAmiId": str,
    },
    total=False,
)

PutAutoScalingPolicyOutputTypeDef = TypedDict(
    "PutAutoScalingPolicyOutputTypeDef",
    {
        "ClusterId": str,
        "InstanceGroupId": str,
        "AutoScalingPolicy": AutoScalingPolicyDescriptionTypeDef,
        "ClusterArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredInstanceGroupConfigTypeDef = TypedDict(
    "_RequiredInstanceGroupConfigTypeDef",
    {
        "InstanceRole": InstanceRoleTypeType,
        "InstanceType": str,
        "InstanceCount": int,
    },
)
_OptionalInstanceGroupConfigTypeDef = TypedDict(
    "_OptionalInstanceGroupConfigTypeDef",
    {
        "Name": str,
        "Market": MarketTypeType,
        "BidPrice": str,
        "Configurations": Sequence["ConfigurationTypeDef"],
        "EbsConfiguration": EbsConfigurationTypeDef,
        "AutoScalingPolicy": AutoScalingPolicyTypeDef,
        "CustomAmiId": str,
    },
    total=False,
)


class InstanceGroupConfigTypeDef(
    _RequiredInstanceGroupConfigTypeDef, _OptionalInstanceGroupConfigTypeDef
):
    pass


PutAutoScalingPolicyInputRequestTypeDef = TypedDict(
    "PutAutoScalingPolicyInputRequestTypeDef",
    {
        "ClusterId": str,
        "InstanceGroupId": str,
        "AutoScalingPolicy": AutoScalingPolicyTypeDef,
    },
)

AddInstanceFleetInputRequestTypeDef = TypedDict(
    "AddInstanceFleetInputRequestTypeDef",
    {
        "ClusterId": str,
        "InstanceFleet": InstanceFleetConfigTypeDef,
    },
)

DescribeJobFlowsOutputTypeDef = TypedDict(
    "DescribeJobFlowsOutputTypeDef",
    {
        "JobFlows": List[JobFlowDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceGroupsOutputTypeDef = TypedDict(
    "ListInstanceGroupsOutputTypeDef",
    {
        "InstanceGroups": List[InstanceGroupTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddInstanceGroupsInputRequestTypeDef = TypedDict(
    "AddInstanceGroupsInputRequestTypeDef",
    {
        "InstanceGroups": Sequence[InstanceGroupConfigTypeDef],
        "JobFlowId": str,
    },
)

JobFlowInstancesConfigTypeDef = TypedDict(
    "JobFlowInstancesConfigTypeDef",
    {
        "MasterInstanceType": str,
        "SlaveInstanceType": str,
        "InstanceCount": int,
        "InstanceGroups": Sequence[InstanceGroupConfigTypeDef],
        "InstanceFleets": Sequence[InstanceFleetConfigTypeDef],
        "Ec2KeyName": str,
        "Placement": PlacementTypeTypeDef,
        "KeepJobFlowAliveWhenNoSteps": bool,
        "TerminationProtected": bool,
        "HadoopVersion": str,
        "Ec2SubnetId": str,
        "Ec2SubnetIds": Sequence[str],
        "EmrManagedMasterSecurityGroup": str,
        "EmrManagedSlaveSecurityGroup": str,
        "ServiceAccessSecurityGroup": str,
        "AdditionalMasterSecurityGroups": Sequence[str],
        "AdditionalSlaveSecurityGroups": Sequence[str],
    },
    total=False,
)

_RequiredRunJobFlowInputRequestTypeDef = TypedDict(
    "_RequiredRunJobFlowInputRequestTypeDef",
    {
        "Name": str,
        "Instances": JobFlowInstancesConfigTypeDef,
    },
)
_OptionalRunJobFlowInputRequestTypeDef = TypedDict(
    "_OptionalRunJobFlowInputRequestTypeDef",
    {
        "LogUri": str,
        "LogEncryptionKmsKeyId": str,
        "AdditionalInfo": str,
        "AmiVersion": str,
        "ReleaseLabel": str,
        "Steps": Sequence[StepConfigTypeDef],
        "BootstrapActions": Sequence[BootstrapActionConfigTypeDef],
        "SupportedProducts": Sequence[str],
        "NewSupportedProducts": Sequence[SupportedProductConfigTypeDef],
        "Applications": Sequence[ApplicationTypeDef],
        "Configurations": Sequence["ConfigurationTypeDef"],
        "VisibleToAllUsers": bool,
        "JobFlowRole": str,
        "ServiceRole": str,
        "Tags": Sequence[TagTypeDef],
        "SecurityConfiguration": str,
        "AutoScalingRole": str,
        "ScaleDownBehavior": ScaleDownBehaviorType,
        "CustomAmiId": str,
        "EbsRootVolumeSize": int,
        "RepoUpgradeOnBoot": RepoUpgradeOnBootType,
        "KerberosAttributes": KerberosAttributesTypeDef,
        "StepConcurrencyLevel": int,
        "ManagedScalingPolicy": ManagedScalingPolicyTypeDef,
        "PlacementGroupConfigs": Sequence[PlacementGroupConfigTypeDef],
        "AutoTerminationPolicy": AutoTerminationPolicyTypeDef,
        "OSReleaseLabel": str,
    },
    total=False,
)


class RunJobFlowInputRequestTypeDef(
    _RequiredRunJobFlowInputRequestTypeDef, _OptionalRunJobFlowInputRequestTypeDef
):
    pass
