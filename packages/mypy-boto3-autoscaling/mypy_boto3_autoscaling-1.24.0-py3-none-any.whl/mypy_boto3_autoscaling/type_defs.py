"""
Type annotations for autoscaling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/type_defs/)

Usage::

    ```python
    from mypy_boto3_autoscaling.type_defs import AcceleratorCountRequestTypeDef

    data: AcceleratorCountRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AcceleratorManufacturerType,
    AcceleratorNameType,
    AcceleratorTypeType,
    BareMetalType,
    BurstablePerformanceType,
    CpuManufacturerType,
    InstanceGenerationType,
    InstanceMetadataEndpointStateType,
    InstanceMetadataHttpTokensStateType,
    InstanceRefreshStatusType,
    LifecycleStateType,
    LocalStorageType,
    LocalStorageTypeType,
    MetricStatisticType,
    MetricTypeType,
    PredefinedLoadMetricTypeType,
    PredefinedMetricPairTypeType,
    PredefinedScalingMetricTypeType,
    PredictiveScalingMaxCapacityBreachBehaviorType,
    PredictiveScalingModeType,
    ScalingActivityStatusCodeType,
    WarmPoolStateType,
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
    "AcceleratorCountRequestTypeDef",
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    "ActivityTypeDef",
    "ResponseMetadataTypeDef",
    "AdjustmentTypeTypeDef",
    "AlarmTypeDef",
    "AttachInstancesQueryRequestTypeDef",
    "AttachLoadBalancerTargetGroupsTypeRequestTypeDef",
    "AttachLoadBalancersTypeRequestTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "EnabledMetricTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "SuspendedProcessTypeDef",
    "TagDescriptionTypeDef",
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    "FailedScheduledUpdateGroupActionRequestTypeDef",
    "BatchDeleteScheduledActionTypeRequestTypeDef",
    "ScheduledUpdateGroupActionRequestTypeDef",
    "EbsTypeDef",
    "CancelInstanceRefreshTypeRequestTypeDef",
    "CapacityForecastTypeDef",
    "CompleteLifecycleActionTypeRequestTypeDef",
    "LifecycleHookSpecificationTypeDef",
    "TagTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "InstanceMonitoringTypeDef",
    "MetricDimensionTypeDef",
    "DeleteAutoScalingGroupTypeRequestTypeDef",
    "DeleteLifecycleHookTypeRequestTypeDef",
    "DeleteNotificationConfigurationTypeRequestTypeDef",
    "DeletePolicyTypeRequestTypeDef",
    "DeleteScheduledActionTypeRequestTypeDef",
    "DeleteWarmPoolTypeRequestTypeDef",
    "DescribeAutoScalingInstancesTypeRequestTypeDef",
    "DescribeInstanceRefreshesTypeRequestTypeDef",
    "LifecycleHookTypeDef",
    "DescribeLifecycleHooksTypeRequestTypeDef",
    "DescribeLoadBalancerTargetGroupsRequestRequestTypeDef",
    "LoadBalancerTargetGroupStateTypeDef",
    "DescribeLoadBalancersRequestRequestTypeDef",
    "LoadBalancerStateTypeDef",
    "MetricCollectionTypeTypeDef",
    "MetricGranularityTypeTypeDef",
    "NotificationConfigurationTypeDef",
    "DescribeNotificationConfigurationsTypeRequestTypeDef",
    "DescribePoliciesTypeRequestTypeDef",
    "DescribeScalingActivitiesTypeRequestTypeDef",
    "DescribeScheduledActionsTypeRequestTypeDef",
    "DescribeWarmPoolTypeRequestTypeDef",
    "DetachInstancesQueryRequestTypeDef",
    "DetachLoadBalancerTargetGroupsTypeRequestTypeDef",
    "DetachLoadBalancersTypeRequestTypeDef",
    "DisableMetricsCollectionQueryRequestTypeDef",
    "EnableMetricsCollectionQueryRequestTypeDef",
    "EnterStandbyQueryRequestTypeDef",
    "ExecutePolicyTypeRequestTypeDef",
    "ExitStandbyQueryRequestTypeDef",
    "GetPredictiveScalingForecastTypeRequestTypeDef",
    "InstanceRefreshLivePoolProgressTypeDef",
    "InstanceRefreshWarmPoolProgressTypeDef",
    "RefreshPreferencesTypeDef",
    "MemoryGiBPerVCpuRequestTypeDef",
    "MemoryMiBRequestTypeDef",
    "NetworkInterfaceCountRequestTypeDef",
    "TotalLocalStorageGBRequestTypeDef",
    "VCpuCountRequestTypeDef",
    "InstanceReusePolicyTypeDef",
    "InstancesDistributionTypeDef",
    "LaunchConfigurationNameTypeRequestTypeDef",
    "LaunchConfigurationNamesTypeRequestTypeDef",
    "PredefinedMetricSpecificationTypeDef",
    "PredictiveScalingPredefinedLoadMetricTypeDef",
    "PredictiveScalingPredefinedMetricPairTypeDef",
    "PredictiveScalingPredefinedScalingMetricTypeDef",
    "ProcessTypeTypeDef",
    "PutLifecycleHookTypeRequestTypeDef",
    "PutNotificationConfigurationTypeRequestTypeDef",
    "StepAdjustmentTypeDef",
    "PutScheduledUpdateGroupActionTypeRequestTypeDef",
    "RecordLifecycleActionHeartbeatTypeRequestTypeDef",
    "ScalingProcessQueryRequestTypeDef",
    "ScheduledUpdateGroupActionTypeDef",
    "SetDesiredCapacityTypeRequestTypeDef",
    "SetInstanceHealthQueryRequestTypeDef",
    "SetInstanceProtectionQueryRequestTypeDef",
    "TerminateInstanceInAutoScalingGroupTypeRequestTypeDef",
    "ActivitiesTypeTypeDef",
    "ActivityTypeTypeDef",
    "CancelInstanceRefreshAnswerTypeDef",
    "DescribeAccountLimitsAnswerTypeDef",
    "DescribeAutoScalingNotificationTypesAnswerTypeDef",
    "DescribeLifecycleHookTypesAnswerTypeDef",
    "DescribeTerminationPolicyTypesAnswerTypeDef",
    "DetachInstancesAnswerTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnterStandbyAnswerTypeDef",
    "ExitStandbyAnswerTypeDef",
    "StartInstanceRefreshAnswerTypeDef",
    "DescribeAdjustmentTypesAnswerTypeDef",
    "PolicyARNTypeTypeDef",
    "AutoScalingGroupNamesTypeRequestTypeDef",
    "DescribeTagsTypeRequestTypeDef",
    "AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef",
    "DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef",
    "DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef",
    "DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef",
    "DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef",
    "DescribePoliciesTypeDescribePoliciesPaginateTypeDef",
    "DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef",
    "DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef",
    "DescribeTagsTypeDescribeTagsPaginateTypeDef",
    "LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef",
    "AutoScalingInstanceDetailsTypeDef",
    "InstanceTypeDef",
    "TagsTypeTypeDef",
    "BatchDeleteScheduledActionAnswerTypeDef",
    "BatchPutScheduledUpdateGroupActionAnswerTypeDef",
    "BatchPutScheduledUpdateGroupActionTypeRequestTypeDef",
    "BlockDeviceMappingTypeDef",
    "CreateOrUpdateTagsTypeRequestTypeDef",
    "DeleteTagsTypeRequestTypeDef",
    "CustomizedMetricSpecificationTypeDef",
    "MetricTypeDef",
    "DescribeLifecycleHooksAnswerTypeDef",
    "DescribeLoadBalancerTargetGroupsResponseTypeDef",
    "DescribeLoadBalancersResponseTypeDef",
    "DescribeMetricCollectionTypesAnswerTypeDef",
    "DescribeNotificationConfigurationsAnswerTypeDef",
    "InstanceRefreshProgressDetailsTypeDef",
    "InstanceRequirementsTypeDef",
    "PutWarmPoolTypeRequestTypeDef",
    "WarmPoolConfigurationTypeDef",
    "ProcessesTypeTypeDef",
    "ScheduledActionsTypeTypeDef",
    "AutoScalingInstancesTypeTypeDef",
    "CreateLaunchConfigurationTypeRequestTypeDef",
    "LaunchConfigurationTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "MetricStatTypeDef",
    "LaunchTemplateOverridesTypeDef",
    "DescribeWarmPoolAnswerTypeDef",
    "LaunchConfigurationsTypeTypeDef",
    "MetricDataQueryTypeDef",
    "LaunchTemplateTypeDef",
    "PredictiveScalingCustomizedCapacityMetricTypeDef",
    "PredictiveScalingCustomizedLoadMetricTypeDef",
    "PredictiveScalingCustomizedScalingMetricTypeDef",
    "MixedInstancesPolicyTypeDef",
    "PredictiveScalingMetricSpecificationTypeDef",
    "AutoScalingGroupTypeDef",
    "CreateAutoScalingGroupTypeRequestTypeDef",
    "DesiredConfigurationTypeDef",
    "UpdateAutoScalingGroupTypeRequestTypeDef",
    "LoadForecastTypeDef",
    "PredictiveScalingConfigurationTypeDef",
    "AutoScalingGroupsTypeTypeDef",
    "InstanceRefreshTypeDef",
    "StartInstanceRefreshTypeRequestTypeDef",
    "GetPredictiveScalingForecastAnswerTypeDef",
    "PutScalingPolicyTypeRequestTypeDef",
    "ScalingPolicyTypeDef",
    "DescribeInstanceRefreshesAnswerTypeDef",
    "PoliciesTypeTypeDef",
)

AcceleratorCountRequestTypeDef = TypedDict(
    "AcceleratorCountRequestTypeDef",
    {
        "Min": int,
        "Max": int,
    },
    total=False,
)

AcceleratorTotalMemoryMiBRequestTypeDef = TypedDict(
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    {
        "Min": int,
        "Max": int,
    },
    total=False,
)

_RequiredActivityTypeDef = TypedDict(
    "_RequiredActivityTypeDef",
    {
        "ActivityId": str,
        "AutoScalingGroupName": str,
        "Cause": str,
        "StartTime": datetime,
        "StatusCode": ScalingActivityStatusCodeType,
    },
)
_OptionalActivityTypeDef = TypedDict(
    "_OptionalActivityTypeDef",
    {
        "Description": str,
        "EndTime": datetime,
        "StatusMessage": str,
        "Progress": int,
        "Details": str,
        "AutoScalingGroupState": str,
        "AutoScalingGroupARN": str,
    },
    total=False,
)


class ActivityTypeDef(_RequiredActivityTypeDef, _OptionalActivityTypeDef):
    pass


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

AdjustmentTypeTypeDef = TypedDict(
    "AdjustmentTypeTypeDef",
    {
        "AdjustmentType": str,
    },
    total=False,
)

AlarmTypeDef = TypedDict(
    "AlarmTypeDef",
    {
        "AlarmName": str,
        "AlarmARN": str,
    },
    total=False,
)

_RequiredAttachInstancesQueryRequestTypeDef = TypedDict(
    "_RequiredAttachInstancesQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalAttachInstancesQueryRequestTypeDef = TypedDict(
    "_OptionalAttachInstancesQueryRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
    total=False,
)


class AttachInstancesQueryRequestTypeDef(
    _RequiredAttachInstancesQueryRequestTypeDef, _OptionalAttachInstancesQueryRequestTypeDef
):
    pass


AttachLoadBalancerTargetGroupsTypeRequestTypeDef = TypedDict(
    "AttachLoadBalancerTargetGroupsTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "TargetGroupARNs": Sequence[str],
    },
)

AttachLoadBalancersTypeRequestTypeDef = TypedDict(
    "AttachLoadBalancersTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "LoadBalancerNames": Sequence[str],
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
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

EnabledMetricTypeDef = TypedDict(
    "EnabledMetricTypeDef",
    {
        "Metric": str,
        "Granularity": str,
    },
    total=False,
)

LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

SuspendedProcessTypeDef = TypedDict(
    "SuspendedProcessTypeDef",
    {
        "ProcessName": str,
        "SuspensionReason": str,
    },
    total=False,
)

TagDescriptionTypeDef = TypedDict(
    "TagDescriptionTypeDef",
    {
        "ResourceId": str,
        "ResourceType": str,
        "Key": str,
        "Value": str,
        "PropagateAtLaunch": bool,
    },
    total=False,
)

BaselineEbsBandwidthMbpsRequestTypeDef = TypedDict(
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    {
        "Min": int,
        "Max": int,
    },
    total=False,
)

_RequiredFailedScheduledUpdateGroupActionRequestTypeDef = TypedDict(
    "_RequiredFailedScheduledUpdateGroupActionRequestTypeDef",
    {
        "ScheduledActionName": str,
    },
)
_OptionalFailedScheduledUpdateGroupActionRequestTypeDef = TypedDict(
    "_OptionalFailedScheduledUpdateGroupActionRequestTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)


class FailedScheduledUpdateGroupActionRequestTypeDef(
    _RequiredFailedScheduledUpdateGroupActionRequestTypeDef,
    _OptionalFailedScheduledUpdateGroupActionRequestTypeDef,
):
    pass


BatchDeleteScheduledActionTypeRequestTypeDef = TypedDict(
    "BatchDeleteScheduledActionTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionNames": Sequence[str],
    },
)

_RequiredScheduledUpdateGroupActionRequestTypeDef = TypedDict(
    "_RequiredScheduledUpdateGroupActionRequestTypeDef",
    {
        "ScheduledActionName": str,
    },
)
_OptionalScheduledUpdateGroupActionRequestTypeDef = TypedDict(
    "_OptionalScheduledUpdateGroupActionRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Recurrence": str,
        "MinSize": int,
        "MaxSize": int,
        "DesiredCapacity": int,
        "TimeZone": str,
    },
    total=False,
)


class ScheduledUpdateGroupActionRequestTypeDef(
    _RequiredScheduledUpdateGroupActionRequestTypeDef,
    _OptionalScheduledUpdateGroupActionRequestTypeDef,
):
    pass


EbsTypeDef = TypedDict(
    "EbsTypeDef",
    {
        "SnapshotId": str,
        "VolumeSize": int,
        "VolumeType": str,
        "DeleteOnTermination": bool,
        "Iops": int,
        "Encrypted": bool,
        "Throughput": int,
    },
    total=False,
)

CancelInstanceRefreshTypeRequestTypeDef = TypedDict(
    "CancelInstanceRefreshTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)

CapacityForecastTypeDef = TypedDict(
    "CapacityForecastTypeDef",
    {
        "Timestamps": List[datetime],
        "Values": List[float],
    },
)

_RequiredCompleteLifecycleActionTypeRequestTypeDef = TypedDict(
    "_RequiredCompleteLifecycleActionTypeRequestTypeDef",
    {
        "LifecycleHookName": str,
        "AutoScalingGroupName": str,
        "LifecycleActionResult": str,
    },
)
_OptionalCompleteLifecycleActionTypeRequestTypeDef = TypedDict(
    "_OptionalCompleteLifecycleActionTypeRequestTypeDef",
    {
        "LifecycleActionToken": str,
        "InstanceId": str,
    },
    total=False,
)


class CompleteLifecycleActionTypeRequestTypeDef(
    _RequiredCompleteLifecycleActionTypeRequestTypeDef,
    _OptionalCompleteLifecycleActionTypeRequestTypeDef,
):
    pass


_RequiredLifecycleHookSpecificationTypeDef = TypedDict(
    "_RequiredLifecycleHookSpecificationTypeDef",
    {
        "LifecycleHookName": str,
        "LifecycleTransition": str,
    },
)
_OptionalLifecycleHookSpecificationTypeDef = TypedDict(
    "_OptionalLifecycleHookSpecificationTypeDef",
    {
        "NotificationMetadata": str,
        "HeartbeatTimeout": int,
        "DefaultResult": str,
        "NotificationTargetARN": str,
        "RoleARN": str,
    },
    total=False,
)


class LifecycleHookSpecificationTypeDef(
    _RequiredLifecycleHookSpecificationTypeDef, _OptionalLifecycleHookSpecificationTypeDef
):
    pass


_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "ResourceId": str,
        "ResourceType": str,
        "Value": str,
        "PropagateAtLaunch": bool,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


InstanceMetadataOptionsTypeDef = TypedDict(
    "InstanceMetadataOptionsTypeDef",
    {
        "HttpTokens": InstanceMetadataHttpTokensStateType,
        "HttpPutResponseHopLimit": int,
        "HttpEndpoint": InstanceMetadataEndpointStateType,
    },
    total=False,
)

InstanceMonitoringTypeDef = TypedDict(
    "InstanceMonitoringTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

_RequiredDeleteAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_RequiredDeleteAutoScalingGroupTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDeleteAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_OptionalDeleteAutoScalingGroupTypeRequestTypeDef",
    {
        "ForceDelete": bool,
    },
    total=False,
)


class DeleteAutoScalingGroupTypeRequestTypeDef(
    _RequiredDeleteAutoScalingGroupTypeRequestTypeDef,
    _OptionalDeleteAutoScalingGroupTypeRequestTypeDef,
):
    pass


DeleteLifecycleHookTypeRequestTypeDef = TypedDict(
    "DeleteLifecycleHookTypeRequestTypeDef",
    {
        "LifecycleHookName": str,
        "AutoScalingGroupName": str,
    },
)

DeleteNotificationConfigurationTypeRequestTypeDef = TypedDict(
    "DeleteNotificationConfigurationTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "TopicARN": str,
    },
)

_RequiredDeletePolicyTypeRequestTypeDef = TypedDict(
    "_RequiredDeletePolicyTypeRequestTypeDef",
    {
        "PolicyName": str,
    },
)
_OptionalDeletePolicyTypeRequestTypeDef = TypedDict(
    "_OptionalDeletePolicyTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
    total=False,
)


class DeletePolicyTypeRequestTypeDef(
    _RequiredDeletePolicyTypeRequestTypeDef, _OptionalDeletePolicyTypeRequestTypeDef
):
    pass


DeleteScheduledActionTypeRequestTypeDef = TypedDict(
    "DeleteScheduledActionTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionName": str,
    },
)

_RequiredDeleteWarmPoolTypeRequestTypeDef = TypedDict(
    "_RequiredDeleteWarmPoolTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDeleteWarmPoolTypeRequestTypeDef = TypedDict(
    "_OptionalDeleteWarmPoolTypeRequestTypeDef",
    {
        "ForceDelete": bool,
    },
    total=False,
)


class DeleteWarmPoolTypeRequestTypeDef(
    _RequiredDeleteWarmPoolTypeRequestTypeDef, _OptionalDeleteWarmPoolTypeRequestTypeDef
):
    pass


DescribeAutoScalingInstancesTypeRequestTypeDef = TypedDict(
    "DescribeAutoScalingInstancesTypeRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeInstanceRefreshesTypeRequestTypeDef = TypedDict(
    "_RequiredDescribeInstanceRefreshesTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeInstanceRefreshesTypeRequestTypeDef = TypedDict(
    "_OptionalDescribeInstanceRefreshesTypeRequestTypeDef",
    {
        "InstanceRefreshIds": Sequence[str],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeInstanceRefreshesTypeRequestTypeDef(
    _RequiredDescribeInstanceRefreshesTypeRequestTypeDef,
    _OptionalDescribeInstanceRefreshesTypeRequestTypeDef,
):
    pass


LifecycleHookTypeDef = TypedDict(
    "LifecycleHookTypeDef",
    {
        "LifecycleHookName": str,
        "AutoScalingGroupName": str,
        "LifecycleTransition": str,
        "NotificationTargetARN": str,
        "RoleARN": str,
        "NotificationMetadata": str,
        "HeartbeatTimeout": int,
        "GlobalTimeout": int,
        "DefaultResult": str,
    },
    total=False,
)

_RequiredDescribeLifecycleHooksTypeRequestTypeDef = TypedDict(
    "_RequiredDescribeLifecycleHooksTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeLifecycleHooksTypeRequestTypeDef = TypedDict(
    "_OptionalDescribeLifecycleHooksTypeRequestTypeDef",
    {
        "LifecycleHookNames": Sequence[str],
    },
    total=False,
)


class DescribeLifecycleHooksTypeRequestTypeDef(
    _RequiredDescribeLifecycleHooksTypeRequestTypeDef,
    _OptionalDescribeLifecycleHooksTypeRequestTypeDef,
):
    pass


_RequiredDescribeLoadBalancerTargetGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeLoadBalancerTargetGroupsRequestRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeLoadBalancerTargetGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeLoadBalancerTargetGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeLoadBalancerTargetGroupsRequestRequestTypeDef(
    _RequiredDescribeLoadBalancerTargetGroupsRequestRequestTypeDef,
    _OptionalDescribeLoadBalancerTargetGroupsRequestRequestTypeDef,
):
    pass


LoadBalancerTargetGroupStateTypeDef = TypedDict(
    "LoadBalancerTargetGroupStateTypeDef",
    {
        "LoadBalancerTargetGroupARN": str,
        "State": str,
    },
    total=False,
)

_RequiredDescribeLoadBalancersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeLoadBalancersRequestRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeLoadBalancersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeLoadBalancersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeLoadBalancersRequestRequestTypeDef(
    _RequiredDescribeLoadBalancersRequestRequestTypeDef,
    _OptionalDescribeLoadBalancersRequestRequestTypeDef,
):
    pass


LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef",
    {
        "LoadBalancerName": str,
        "State": str,
    },
    total=False,
)

MetricCollectionTypeTypeDef = TypedDict(
    "MetricCollectionTypeTypeDef",
    {
        "Metric": str,
    },
    total=False,
)

MetricGranularityTypeTypeDef = TypedDict(
    "MetricGranularityTypeTypeDef",
    {
        "Granularity": str,
    },
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "AutoScalingGroupName": str,
        "TopicARN": str,
        "NotificationType": str,
    },
    total=False,
)

DescribeNotificationConfigurationsTypeRequestTypeDef = TypedDict(
    "DescribeNotificationConfigurationsTypeRequestTypeDef",
    {
        "AutoScalingGroupNames": Sequence[str],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribePoliciesTypeRequestTypeDef = TypedDict(
    "DescribePoliciesTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "PolicyNames": Sequence[str],
        "PolicyTypes": Sequence[str],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeScalingActivitiesTypeRequestTypeDef = TypedDict(
    "DescribeScalingActivitiesTypeRequestTypeDef",
    {
        "ActivityIds": Sequence[str],
        "AutoScalingGroupName": str,
        "IncludeDeletedGroups": bool,
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeScheduledActionsTypeRequestTypeDef = TypedDict(
    "DescribeScheduledActionsTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionNames": Sequence[str],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)

_RequiredDescribeWarmPoolTypeRequestTypeDef = TypedDict(
    "_RequiredDescribeWarmPoolTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeWarmPoolTypeRequestTypeDef = TypedDict(
    "_OptionalDescribeWarmPoolTypeRequestTypeDef",
    {
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeWarmPoolTypeRequestTypeDef(
    _RequiredDescribeWarmPoolTypeRequestTypeDef, _OptionalDescribeWarmPoolTypeRequestTypeDef
):
    pass


_RequiredDetachInstancesQueryRequestTypeDef = TypedDict(
    "_RequiredDetachInstancesQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ShouldDecrementDesiredCapacity": bool,
    },
)
_OptionalDetachInstancesQueryRequestTypeDef = TypedDict(
    "_OptionalDetachInstancesQueryRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
    total=False,
)


class DetachInstancesQueryRequestTypeDef(
    _RequiredDetachInstancesQueryRequestTypeDef, _OptionalDetachInstancesQueryRequestTypeDef
):
    pass


DetachLoadBalancerTargetGroupsTypeRequestTypeDef = TypedDict(
    "DetachLoadBalancerTargetGroupsTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "TargetGroupARNs": Sequence[str],
    },
)

DetachLoadBalancersTypeRequestTypeDef = TypedDict(
    "DetachLoadBalancersTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "LoadBalancerNames": Sequence[str],
    },
)

_RequiredDisableMetricsCollectionQueryRequestTypeDef = TypedDict(
    "_RequiredDisableMetricsCollectionQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDisableMetricsCollectionQueryRequestTypeDef = TypedDict(
    "_OptionalDisableMetricsCollectionQueryRequestTypeDef",
    {
        "Metrics": Sequence[str],
    },
    total=False,
)


class DisableMetricsCollectionQueryRequestTypeDef(
    _RequiredDisableMetricsCollectionQueryRequestTypeDef,
    _OptionalDisableMetricsCollectionQueryRequestTypeDef,
):
    pass


_RequiredEnableMetricsCollectionQueryRequestTypeDef = TypedDict(
    "_RequiredEnableMetricsCollectionQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "Granularity": str,
    },
)
_OptionalEnableMetricsCollectionQueryRequestTypeDef = TypedDict(
    "_OptionalEnableMetricsCollectionQueryRequestTypeDef",
    {
        "Metrics": Sequence[str],
    },
    total=False,
)


class EnableMetricsCollectionQueryRequestTypeDef(
    _RequiredEnableMetricsCollectionQueryRequestTypeDef,
    _OptionalEnableMetricsCollectionQueryRequestTypeDef,
):
    pass


_RequiredEnterStandbyQueryRequestTypeDef = TypedDict(
    "_RequiredEnterStandbyQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ShouldDecrementDesiredCapacity": bool,
    },
)
_OptionalEnterStandbyQueryRequestTypeDef = TypedDict(
    "_OptionalEnterStandbyQueryRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
    total=False,
)


class EnterStandbyQueryRequestTypeDef(
    _RequiredEnterStandbyQueryRequestTypeDef, _OptionalEnterStandbyQueryRequestTypeDef
):
    pass


_RequiredExecutePolicyTypeRequestTypeDef = TypedDict(
    "_RequiredExecutePolicyTypeRequestTypeDef",
    {
        "PolicyName": str,
    },
)
_OptionalExecutePolicyTypeRequestTypeDef = TypedDict(
    "_OptionalExecutePolicyTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "HonorCooldown": bool,
        "MetricValue": float,
        "BreachThreshold": float,
    },
    total=False,
)


class ExecutePolicyTypeRequestTypeDef(
    _RequiredExecutePolicyTypeRequestTypeDef, _OptionalExecutePolicyTypeRequestTypeDef
):
    pass


_RequiredExitStandbyQueryRequestTypeDef = TypedDict(
    "_RequiredExitStandbyQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalExitStandbyQueryRequestTypeDef = TypedDict(
    "_OptionalExitStandbyQueryRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
    total=False,
)


class ExitStandbyQueryRequestTypeDef(
    _RequiredExitStandbyQueryRequestTypeDef, _OptionalExitStandbyQueryRequestTypeDef
):
    pass


GetPredictiveScalingForecastTypeRequestTypeDef = TypedDict(
    "GetPredictiveScalingForecastTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "PolicyName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)

InstanceRefreshLivePoolProgressTypeDef = TypedDict(
    "InstanceRefreshLivePoolProgressTypeDef",
    {
        "PercentageComplete": int,
        "InstancesToUpdate": int,
    },
    total=False,
)

InstanceRefreshWarmPoolProgressTypeDef = TypedDict(
    "InstanceRefreshWarmPoolProgressTypeDef",
    {
        "PercentageComplete": int,
        "InstancesToUpdate": int,
    },
    total=False,
)

RefreshPreferencesTypeDef = TypedDict(
    "RefreshPreferencesTypeDef",
    {
        "MinHealthyPercentage": int,
        "InstanceWarmup": int,
        "CheckpointPercentages": List[int],
        "CheckpointDelay": int,
        "SkipMatching": bool,
    },
    total=False,
)

MemoryGiBPerVCpuRequestTypeDef = TypedDict(
    "MemoryGiBPerVCpuRequestTypeDef",
    {
        "Min": float,
        "Max": float,
    },
    total=False,
)

_RequiredMemoryMiBRequestTypeDef = TypedDict(
    "_RequiredMemoryMiBRequestTypeDef",
    {
        "Min": int,
    },
)
_OptionalMemoryMiBRequestTypeDef = TypedDict(
    "_OptionalMemoryMiBRequestTypeDef",
    {
        "Max": int,
    },
    total=False,
)


class MemoryMiBRequestTypeDef(_RequiredMemoryMiBRequestTypeDef, _OptionalMemoryMiBRequestTypeDef):
    pass


NetworkInterfaceCountRequestTypeDef = TypedDict(
    "NetworkInterfaceCountRequestTypeDef",
    {
        "Min": int,
        "Max": int,
    },
    total=False,
)

TotalLocalStorageGBRequestTypeDef = TypedDict(
    "TotalLocalStorageGBRequestTypeDef",
    {
        "Min": float,
        "Max": float,
    },
    total=False,
)

_RequiredVCpuCountRequestTypeDef = TypedDict(
    "_RequiredVCpuCountRequestTypeDef",
    {
        "Min": int,
    },
)
_OptionalVCpuCountRequestTypeDef = TypedDict(
    "_OptionalVCpuCountRequestTypeDef",
    {
        "Max": int,
    },
    total=False,
)


class VCpuCountRequestTypeDef(_RequiredVCpuCountRequestTypeDef, _OptionalVCpuCountRequestTypeDef):
    pass


InstanceReusePolicyTypeDef = TypedDict(
    "InstanceReusePolicyTypeDef",
    {
        "ReuseOnScaleIn": bool,
    },
    total=False,
)

InstancesDistributionTypeDef = TypedDict(
    "InstancesDistributionTypeDef",
    {
        "OnDemandAllocationStrategy": str,
        "OnDemandBaseCapacity": int,
        "OnDemandPercentageAboveBaseCapacity": int,
        "SpotAllocationStrategy": str,
        "SpotInstancePools": int,
        "SpotMaxPrice": str,
    },
    total=False,
)

LaunchConfigurationNameTypeRequestTypeDef = TypedDict(
    "LaunchConfigurationNameTypeRequestTypeDef",
    {
        "LaunchConfigurationName": str,
    },
)

LaunchConfigurationNamesTypeRequestTypeDef = TypedDict(
    "LaunchConfigurationNamesTypeRequestTypeDef",
    {
        "LaunchConfigurationNames": Sequence[str],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)

_RequiredPredefinedMetricSpecificationTypeDef = TypedDict(
    "_RequiredPredefinedMetricSpecificationTypeDef",
    {
        "PredefinedMetricType": MetricTypeType,
    },
)
_OptionalPredefinedMetricSpecificationTypeDef = TypedDict(
    "_OptionalPredefinedMetricSpecificationTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredefinedMetricSpecificationTypeDef(
    _RequiredPredefinedMetricSpecificationTypeDef, _OptionalPredefinedMetricSpecificationTypeDef
):
    pass


_RequiredPredictiveScalingPredefinedLoadMetricTypeDef = TypedDict(
    "_RequiredPredictiveScalingPredefinedLoadMetricTypeDef",
    {
        "PredefinedMetricType": PredefinedLoadMetricTypeType,
    },
)
_OptionalPredictiveScalingPredefinedLoadMetricTypeDef = TypedDict(
    "_OptionalPredictiveScalingPredefinedLoadMetricTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredictiveScalingPredefinedLoadMetricTypeDef(
    _RequiredPredictiveScalingPredefinedLoadMetricTypeDef,
    _OptionalPredictiveScalingPredefinedLoadMetricTypeDef,
):
    pass


_RequiredPredictiveScalingPredefinedMetricPairTypeDef = TypedDict(
    "_RequiredPredictiveScalingPredefinedMetricPairTypeDef",
    {
        "PredefinedMetricType": PredefinedMetricPairTypeType,
    },
)
_OptionalPredictiveScalingPredefinedMetricPairTypeDef = TypedDict(
    "_OptionalPredictiveScalingPredefinedMetricPairTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredictiveScalingPredefinedMetricPairTypeDef(
    _RequiredPredictiveScalingPredefinedMetricPairTypeDef,
    _OptionalPredictiveScalingPredefinedMetricPairTypeDef,
):
    pass


_RequiredPredictiveScalingPredefinedScalingMetricTypeDef = TypedDict(
    "_RequiredPredictiveScalingPredefinedScalingMetricTypeDef",
    {
        "PredefinedMetricType": PredefinedScalingMetricTypeType,
    },
)
_OptionalPredictiveScalingPredefinedScalingMetricTypeDef = TypedDict(
    "_OptionalPredictiveScalingPredefinedScalingMetricTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredictiveScalingPredefinedScalingMetricTypeDef(
    _RequiredPredictiveScalingPredefinedScalingMetricTypeDef,
    _OptionalPredictiveScalingPredefinedScalingMetricTypeDef,
):
    pass


ProcessTypeTypeDef = TypedDict(
    "ProcessTypeTypeDef",
    {
        "ProcessName": str,
    },
)

_RequiredPutLifecycleHookTypeRequestTypeDef = TypedDict(
    "_RequiredPutLifecycleHookTypeRequestTypeDef",
    {
        "LifecycleHookName": str,
        "AutoScalingGroupName": str,
    },
)
_OptionalPutLifecycleHookTypeRequestTypeDef = TypedDict(
    "_OptionalPutLifecycleHookTypeRequestTypeDef",
    {
        "LifecycleTransition": str,
        "RoleARN": str,
        "NotificationTargetARN": str,
        "NotificationMetadata": str,
        "HeartbeatTimeout": int,
        "DefaultResult": str,
    },
    total=False,
)


class PutLifecycleHookTypeRequestTypeDef(
    _RequiredPutLifecycleHookTypeRequestTypeDef, _OptionalPutLifecycleHookTypeRequestTypeDef
):
    pass


PutNotificationConfigurationTypeRequestTypeDef = TypedDict(
    "PutNotificationConfigurationTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "TopicARN": str,
        "NotificationTypes": Sequence[str],
    },
)

_RequiredStepAdjustmentTypeDef = TypedDict(
    "_RequiredStepAdjustmentTypeDef",
    {
        "ScalingAdjustment": int,
    },
)
_OptionalStepAdjustmentTypeDef = TypedDict(
    "_OptionalStepAdjustmentTypeDef",
    {
        "MetricIntervalLowerBound": float,
        "MetricIntervalUpperBound": float,
    },
    total=False,
)


class StepAdjustmentTypeDef(_RequiredStepAdjustmentTypeDef, _OptionalStepAdjustmentTypeDef):
    pass


_RequiredPutScheduledUpdateGroupActionTypeRequestTypeDef = TypedDict(
    "_RequiredPutScheduledUpdateGroupActionTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionName": str,
    },
)
_OptionalPutScheduledUpdateGroupActionTypeRequestTypeDef = TypedDict(
    "_OptionalPutScheduledUpdateGroupActionTypeRequestTypeDef",
    {
        "Time": Union[datetime, str],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Recurrence": str,
        "MinSize": int,
        "MaxSize": int,
        "DesiredCapacity": int,
        "TimeZone": str,
    },
    total=False,
)


class PutScheduledUpdateGroupActionTypeRequestTypeDef(
    _RequiredPutScheduledUpdateGroupActionTypeRequestTypeDef,
    _OptionalPutScheduledUpdateGroupActionTypeRequestTypeDef,
):
    pass


_RequiredRecordLifecycleActionHeartbeatTypeRequestTypeDef = TypedDict(
    "_RequiredRecordLifecycleActionHeartbeatTypeRequestTypeDef",
    {
        "LifecycleHookName": str,
        "AutoScalingGroupName": str,
    },
)
_OptionalRecordLifecycleActionHeartbeatTypeRequestTypeDef = TypedDict(
    "_OptionalRecordLifecycleActionHeartbeatTypeRequestTypeDef",
    {
        "LifecycleActionToken": str,
        "InstanceId": str,
    },
    total=False,
)


class RecordLifecycleActionHeartbeatTypeRequestTypeDef(
    _RequiredRecordLifecycleActionHeartbeatTypeRequestTypeDef,
    _OptionalRecordLifecycleActionHeartbeatTypeRequestTypeDef,
):
    pass


_RequiredScalingProcessQueryRequestTypeDef = TypedDict(
    "_RequiredScalingProcessQueryRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalScalingProcessQueryRequestTypeDef = TypedDict(
    "_OptionalScalingProcessQueryRequestTypeDef",
    {
        "ScalingProcesses": Sequence[str],
    },
    total=False,
)


class ScalingProcessQueryRequestTypeDef(
    _RequiredScalingProcessQueryRequestTypeDef, _OptionalScalingProcessQueryRequestTypeDef
):
    pass


ScheduledUpdateGroupActionTypeDef = TypedDict(
    "ScheduledUpdateGroupActionTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionName": str,
        "ScheduledActionARN": str,
        "Time": datetime,
        "StartTime": datetime,
        "EndTime": datetime,
        "Recurrence": str,
        "MinSize": int,
        "MaxSize": int,
        "DesiredCapacity": int,
        "TimeZone": str,
    },
    total=False,
)

_RequiredSetDesiredCapacityTypeRequestTypeDef = TypedDict(
    "_RequiredSetDesiredCapacityTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "DesiredCapacity": int,
    },
)
_OptionalSetDesiredCapacityTypeRequestTypeDef = TypedDict(
    "_OptionalSetDesiredCapacityTypeRequestTypeDef",
    {
        "HonorCooldown": bool,
    },
    total=False,
)


class SetDesiredCapacityTypeRequestTypeDef(
    _RequiredSetDesiredCapacityTypeRequestTypeDef, _OptionalSetDesiredCapacityTypeRequestTypeDef
):
    pass


_RequiredSetInstanceHealthQueryRequestTypeDef = TypedDict(
    "_RequiredSetInstanceHealthQueryRequestTypeDef",
    {
        "InstanceId": str,
        "HealthStatus": str,
    },
)
_OptionalSetInstanceHealthQueryRequestTypeDef = TypedDict(
    "_OptionalSetInstanceHealthQueryRequestTypeDef",
    {
        "ShouldRespectGracePeriod": bool,
    },
    total=False,
)


class SetInstanceHealthQueryRequestTypeDef(
    _RequiredSetInstanceHealthQueryRequestTypeDef, _OptionalSetInstanceHealthQueryRequestTypeDef
):
    pass


SetInstanceProtectionQueryRequestTypeDef = TypedDict(
    "SetInstanceProtectionQueryRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
        "AutoScalingGroupName": str,
        "ProtectedFromScaleIn": bool,
    },
)

TerminateInstanceInAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "TerminateInstanceInAutoScalingGroupTypeRequestTypeDef",
    {
        "InstanceId": str,
        "ShouldDecrementDesiredCapacity": bool,
    },
)

ActivitiesTypeTypeDef = TypedDict(
    "ActivitiesTypeTypeDef",
    {
        "Activities": List[ActivityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActivityTypeTypeDef = TypedDict(
    "ActivityTypeTypeDef",
    {
        "Activity": ActivityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelInstanceRefreshAnswerTypeDef = TypedDict(
    "CancelInstanceRefreshAnswerTypeDef",
    {
        "InstanceRefreshId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountLimitsAnswerTypeDef = TypedDict(
    "DescribeAccountLimitsAnswerTypeDef",
    {
        "MaxNumberOfAutoScalingGroups": int,
        "MaxNumberOfLaunchConfigurations": int,
        "NumberOfAutoScalingGroups": int,
        "NumberOfLaunchConfigurations": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAutoScalingNotificationTypesAnswerTypeDef = TypedDict(
    "DescribeAutoScalingNotificationTypesAnswerTypeDef",
    {
        "AutoScalingNotificationTypes": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLifecycleHookTypesAnswerTypeDef = TypedDict(
    "DescribeLifecycleHookTypesAnswerTypeDef",
    {
        "LifecycleHookTypes": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTerminationPolicyTypesAnswerTypeDef = TypedDict(
    "DescribeTerminationPolicyTypesAnswerTypeDef",
    {
        "TerminationPolicyTypes": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetachInstancesAnswerTypeDef = TypedDict(
    "DetachInstancesAnswerTypeDef",
    {
        "Activities": List[ActivityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnterStandbyAnswerTypeDef = TypedDict(
    "EnterStandbyAnswerTypeDef",
    {
        "Activities": List[ActivityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExitStandbyAnswerTypeDef = TypedDict(
    "ExitStandbyAnswerTypeDef",
    {
        "Activities": List[ActivityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartInstanceRefreshAnswerTypeDef = TypedDict(
    "StartInstanceRefreshAnswerTypeDef",
    {
        "InstanceRefreshId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAdjustmentTypesAnswerTypeDef = TypedDict(
    "DescribeAdjustmentTypesAnswerTypeDef",
    {
        "AdjustmentTypes": List[AdjustmentTypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PolicyARNTypeTypeDef = TypedDict(
    "PolicyARNTypeTypeDef",
    {
        "PolicyARN": str,
        "Alarms": List[AlarmTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutoScalingGroupNamesTypeRequestTypeDef = TypedDict(
    "AutoScalingGroupNamesTypeRequestTypeDef",
    {
        "AutoScalingGroupNames": Sequence[str],
        "NextToken": str,
        "MaxRecords": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeTagsTypeRequestTypeDef = TypedDict(
    "DescribeTagsTypeRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxRecords": int,
    },
    total=False,
)

AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef = TypedDict(
    "AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef",
    {
        "AutoScalingGroupNames": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef = TypedDict(
    "DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef",
    {
        "InstanceIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef = TypedDict(
    "_RequiredDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef = TypedDict(
    "_OptionalDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef(
    _RequiredDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef,
    _OptionalDescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef,
):
    pass


_RequiredDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef = TypedDict(
    "_RequiredDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef = TypedDict(
    "_OptionalDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef(
    _RequiredDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef,
    _OptionalDescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef,
):
    pass


DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef = TypedDict(
    "DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef",
    {
        "AutoScalingGroupNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePoliciesTypeDescribePoliciesPaginateTypeDef = TypedDict(
    "DescribePoliciesTypeDescribePoliciesPaginateTypeDef",
    {
        "AutoScalingGroupName": str,
        "PolicyNames": Sequence[str],
        "PolicyTypes": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef = TypedDict(
    "DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef",
    {
        "ActivityIds": Sequence[str],
        "AutoScalingGroupName": str,
        "IncludeDeletedGroups": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef = TypedDict(
    "DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledActionNames": Sequence[str],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTagsTypeDescribeTagsPaginateTypeDef = TypedDict(
    "DescribeTagsTypeDescribeTagsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef = TypedDict(
    "LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef",
    {
        "LaunchConfigurationNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredAutoScalingInstanceDetailsTypeDef = TypedDict(
    "_RequiredAutoScalingInstanceDetailsTypeDef",
    {
        "InstanceId": str,
        "AutoScalingGroupName": str,
        "AvailabilityZone": str,
        "LifecycleState": str,
        "HealthStatus": str,
        "ProtectedFromScaleIn": bool,
    },
)
_OptionalAutoScalingInstanceDetailsTypeDef = TypedDict(
    "_OptionalAutoScalingInstanceDetailsTypeDef",
    {
        "InstanceType": str,
        "LaunchConfigurationName": str,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "WeightedCapacity": str,
    },
    total=False,
)


class AutoScalingInstanceDetailsTypeDef(
    _RequiredAutoScalingInstanceDetailsTypeDef, _OptionalAutoScalingInstanceDetailsTypeDef
):
    pass


_RequiredInstanceTypeDef = TypedDict(
    "_RequiredInstanceTypeDef",
    {
        "InstanceId": str,
        "AvailabilityZone": str,
        "LifecycleState": LifecycleStateType,
        "HealthStatus": str,
        "ProtectedFromScaleIn": bool,
    },
)
_OptionalInstanceTypeDef = TypedDict(
    "_OptionalInstanceTypeDef",
    {
        "InstanceType": str,
        "LaunchConfigurationName": str,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "WeightedCapacity": str,
    },
    total=False,
)


class InstanceTypeDef(_RequiredInstanceTypeDef, _OptionalInstanceTypeDef):
    pass


TagsTypeTypeDef = TypedDict(
    "TagsTypeTypeDef",
    {
        "Tags": List[TagDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteScheduledActionAnswerTypeDef = TypedDict(
    "BatchDeleteScheduledActionAnswerTypeDef",
    {
        "FailedScheduledActions": List[FailedScheduledUpdateGroupActionRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutScheduledUpdateGroupActionAnswerTypeDef = TypedDict(
    "BatchPutScheduledUpdateGroupActionAnswerTypeDef",
    {
        "FailedScheduledUpdateGroupActions": List[FailedScheduledUpdateGroupActionRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutScheduledUpdateGroupActionTypeRequestTypeDef = TypedDict(
    "BatchPutScheduledUpdateGroupActionTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "ScheduledUpdateGroupActions": Sequence[ScheduledUpdateGroupActionRequestTypeDef],
    },
)

_RequiredBlockDeviceMappingTypeDef = TypedDict(
    "_RequiredBlockDeviceMappingTypeDef",
    {
        "DeviceName": str,
    },
)
_OptionalBlockDeviceMappingTypeDef = TypedDict(
    "_OptionalBlockDeviceMappingTypeDef",
    {
        "VirtualName": str,
        "Ebs": EbsTypeDef,
        "NoDevice": bool,
    },
    total=False,
)


class BlockDeviceMappingTypeDef(
    _RequiredBlockDeviceMappingTypeDef, _OptionalBlockDeviceMappingTypeDef
):
    pass


CreateOrUpdateTagsTypeRequestTypeDef = TypedDict(
    "CreateOrUpdateTagsTypeRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
)

DeleteTagsTypeRequestTypeDef = TypedDict(
    "DeleteTagsTypeRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCustomizedMetricSpecificationTypeDef = TypedDict(
    "_RequiredCustomizedMetricSpecificationTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
    },
)
_OptionalCustomizedMetricSpecificationTypeDef = TypedDict(
    "_OptionalCustomizedMetricSpecificationTypeDef",
    {
        "Dimensions": List[MetricDimensionTypeDef],
        "Unit": str,
    },
    total=False,
)


class CustomizedMetricSpecificationTypeDef(
    _RequiredCustomizedMetricSpecificationTypeDef, _OptionalCustomizedMetricSpecificationTypeDef
):
    pass


_RequiredMetricTypeDef = TypedDict(
    "_RequiredMetricTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
    },
)
_OptionalMetricTypeDef = TypedDict(
    "_OptionalMetricTypeDef",
    {
        "Dimensions": List[MetricDimensionTypeDef],
    },
    total=False,
)


class MetricTypeDef(_RequiredMetricTypeDef, _OptionalMetricTypeDef):
    pass


DescribeLifecycleHooksAnswerTypeDef = TypedDict(
    "DescribeLifecycleHooksAnswerTypeDef",
    {
        "LifecycleHooks": List[LifecycleHookTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancerTargetGroupsResponseTypeDef = TypedDict(
    "DescribeLoadBalancerTargetGroupsResponseTypeDef",
    {
        "LoadBalancerTargetGroups": List[LoadBalancerTargetGroupStateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBalancersResponseTypeDef = TypedDict(
    "DescribeLoadBalancersResponseTypeDef",
    {
        "LoadBalancers": List[LoadBalancerStateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMetricCollectionTypesAnswerTypeDef = TypedDict(
    "DescribeMetricCollectionTypesAnswerTypeDef",
    {
        "Metrics": List[MetricCollectionTypeTypeDef],
        "Granularities": List[MetricGranularityTypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeNotificationConfigurationsAnswerTypeDef = TypedDict(
    "DescribeNotificationConfigurationsAnswerTypeDef",
    {
        "NotificationConfigurations": List[NotificationConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceRefreshProgressDetailsTypeDef = TypedDict(
    "InstanceRefreshProgressDetailsTypeDef",
    {
        "LivePoolProgress": InstanceRefreshLivePoolProgressTypeDef,
        "WarmPoolProgress": InstanceRefreshWarmPoolProgressTypeDef,
    },
    total=False,
)

_RequiredInstanceRequirementsTypeDef = TypedDict(
    "_RequiredInstanceRequirementsTypeDef",
    {
        "VCpuCount": VCpuCountRequestTypeDef,
        "MemoryMiB": MemoryMiBRequestTypeDef,
    },
)
_OptionalInstanceRequirementsTypeDef = TypedDict(
    "_OptionalInstanceRequirementsTypeDef",
    {
        "CpuManufacturers": Sequence[CpuManufacturerType],
        "MemoryGiBPerVCpu": MemoryGiBPerVCpuRequestTypeDef,
        "ExcludedInstanceTypes": Sequence[str],
        "InstanceGenerations": Sequence[InstanceGenerationType],
        "SpotMaxPricePercentageOverLowestPrice": int,
        "OnDemandMaxPricePercentageOverLowestPrice": int,
        "BareMetal": BareMetalType,
        "BurstablePerformance": BurstablePerformanceType,
        "RequireHibernateSupport": bool,
        "NetworkInterfaceCount": NetworkInterfaceCountRequestTypeDef,
        "LocalStorage": LocalStorageType,
        "LocalStorageTypes": Sequence[LocalStorageTypeType],
        "TotalLocalStorageGB": TotalLocalStorageGBRequestTypeDef,
        "BaselineEbsBandwidthMbps": BaselineEbsBandwidthMbpsRequestTypeDef,
        "AcceleratorTypes": Sequence[AcceleratorTypeType],
        "AcceleratorCount": AcceleratorCountRequestTypeDef,
        "AcceleratorManufacturers": Sequence[AcceleratorManufacturerType],
        "AcceleratorNames": Sequence[AcceleratorNameType],
        "AcceleratorTotalMemoryMiB": AcceleratorTotalMemoryMiBRequestTypeDef,
    },
    total=False,
)


class InstanceRequirementsTypeDef(
    _RequiredInstanceRequirementsTypeDef, _OptionalInstanceRequirementsTypeDef
):
    pass


_RequiredPutWarmPoolTypeRequestTypeDef = TypedDict(
    "_RequiredPutWarmPoolTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalPutWarmPoolTypeRequestTypeDef = TypedDict(
    "_OptionalPutWarmPoolTypeRequestTypeDef",
    {
        "MaxGroupPreparedCapacity": int,
        "MinSize": int,
        "PoolState": WarmPoolStateType,
        "InstanceReusePolicy": InstanceReusePolicyTypeDef,
    },
    total=False,
)


class PutWarmPoolTypeRequestTypeDef(
    _RequiredPutWarmPoolTypeRequestTypeDef, _OptionalPutWarmPoolTypeRequestTypeDef
):
    pass


WarmPoolConfigurationTypeDef = TypedDict(
    "WarmPoolConfigurationTypeDef",
    {
        "MaxGroupPreparedCapacity": int,
        "MinSize": int,
        "PoolState": WarmPoolStateType,
        "Status": Literal["PendingDelete"],
        "InstanceReusePolicy": InstanceReusePolicyTypeDef,
    },
    total=False,
)

ProcessesTypeTypeDef = TypedDict(
    "ProcessesTypeTypeDef",
    {
        "Processes": List[ProcessTypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduledActionsTypeTypeDef = TypedDict(
    "ScheduledActionsTypeTypeDef",
    {
        "ScheduledUpdateGroupActions": List[ScheduledUpdateGroupActionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutoScalingInstancesTypeTypeDef = TypedDict(
    "AutoScalingInstancesTypeTypeDef",
    {
        "AutoScalingInstances": List[AutoScalingInstanceDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLaunchConfigurationTypeRequestTypeDef = TypedDict(
    "_RequiredCreateLaunchConfigurationTypeRequestTypeDef",
    {
        "LaunchConfigurationName": str,
    },
)
_OptionalCreateLaunchConfigurationTypeRequestTypeDef = TypedDict(
    "_OptionalCreateLaunchConfigurationTypeRequestTypeDef",
    {
        "ImageId": str,
        "KeyName": str,
        "SecurityGroups": Sequence[str],
        "ClassicLinkVPCId": str,
        "ClassicLinkVPCSecurityGroups": Sequence[str],
        "UserData": str,
        "InstanceId": str,
        "InstanceType": str,
        "KernelId": str,
        "RamdiskId": str,
        "BlockDeviceMappings": Sequence[BlockDeviceMappingTypeDef],
        "InstanceMonitoring": InstanceMonitoringTypeDef,
        "SpotPrice": str,
        "IamInstanceProfile": str,
        "EbsOptimized": bool,
        "AssociatePublicIpAddress": bool,
        "PlacementTenancy": str,
        "MetadataOptions": InstanceMetadataOptionsTypeDef,
    },
    total=False,
)


class CreateLaunchConfigurationTypeRequestTypeDef(
    _RequiredCreateLaunchConfigurationTypeRequestTypeDef,
    _OptionalCreateLaunchConfigurationTypeRequestTypeDef,
):
    pass


_RequiredLaunchConfigurationTypeDef = TypedDict(
    "_RequiredLaunchConfigurationTypeDef",
    {
        "LaunchConfigurationName": str,
        "ImageId": str,
        "InstanceType": str,
        "CreatedTime": datetime,
    },
)
_OptionalLaunchConfigurationTypeDef = TypedDict(
    "_OptionalLaunchConfigurationTypeDef",
    {
        "LaunchConfigurationARN": str,
        "KeyName": str,
        "SecurityGroups": List[str],
        "ClassicLinkVPCId": str,
        "ClassicLinkVPCSecurityGroups": List[str],
        "UserData": str,
        "KernelId": str,
        "RamdiskId": str,
        "BlockDeviceMappings": List[BlockDeviceMappingTypeDef],
        "InstanceMonitoring": InstanceMonitoringTypeDef,
        "SpotPrice": str,
        "IamInstanceProfile": str,
        "EbsOptimized": bool,
        "AssociatePublicIpAddress": bool,
        "PlacementTenancy": str,
        "MetadataOptions": InstanceMetadataOptionsTypeDef,
    },
    total=False,
)


class LaunchConfigurationTypeDef(
    _RequiredLaunchConfigurationTypeDef, _OptionalLaunchConfigurationTypeDef
):
    pass


_RequiredTargetTrackingConfigurationTypeDef = TypedDict(
    "_RequiredTargetTrackingConfigurationTypeDef",
    {
        "TargetValue": float,
    },
)
_OptionalTargetTrackingConfigurationTypeDef = TypedDict(
    "_OptionalTargetTrackingConfigurationTypeDef",
    {
        "PredefinedMetricSpecification": PredefinedMetricSpecificationTypeDef,
        "CustomizedMetricSpecification": CustomizedMetricSpecificationTypeDef,
        "DisableScaleIn": bool,
    },
    total=False,
)


class TargetTrackingConfigurationTypeDef(
    _RequiredTargetTrackingConfigurationTypeDef, _OptionalTargetTrackingConfigurationTypeDef
):
    pass


_RequiredMetricStatTypeDef = TypedDict(
    "_RequiredMetricStatTypeDef",
    {
        "Metric": MetricTypeDef,
        "Stat": str,
    },
)
_OptionalMetricStatTypeDef = TypedDict(
    "_OptionalMetricStatTypeDef",
    {
        "Unit": str,
    },
    total=False,
)


class MetricStatTypeDef(_RequiredMetricStatTypeDef, _OptionalMetricStatTypeDef):
    pass


LaunchTemplateOverridesTypeDef = TypedDict(
    "LaunchTemplateOverridesTypeDef",
    {
        "InstanceType": str,
        "WeightedCapacity": str,
        "LaunchTemplateSpecification": LaunchTemplateSpecificationTypeDef,
        "InstanceRequirements": InstanceRequirementsTypeDef,
    },
    total=False,
)

DescribeWarmPoolAnswerTypeDef = TypedDict(
    "DescribeWarmPoolAnswerTypeDef",
    {
        "WarmPoolConfiguration": WarmPoolConfigurationTypeDef,
        "Instances": List[InstanceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LaunchConfigurationsTypeTypeDef = TypedDict(
    "LaunchConfigurationsTypeTypeDef",
    {
        "LaunchConfigurations": List[LaunchConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMetricDataQueryTypeDef = TypedDict(
    "_RequiredMetricDataQueryTypeDef",
    {
        "Id": str,
    },
)
_OptionalMetricDataQueryTypeDef = TypedDict(
    "_OptionalMetricDataQueryTypeDef",
    {
        "Expression": str,
        "MetricStat": MetricStatTypeDef,
        "Label": str,
        "ReturnData": bool,
    },
    total=False,
)


class MetricDataQueryTypeDef(_RequiredMetricDataQueryTypeDef, _OptionalMetricDataQueryTypeDef):
    pass


LaunchTemplateTypeDef = TypedDict(
    "LaunchTemplateTypeDef",
    {
        "LaunchTemplateSpecification": LaunchTemplateSpecificationTypeDef,
        "Overrides": Sequence[LaunchTemplateOverridesTypeDef],
    },
    total=False,
)

PredictiveScalingCustomizedCapacityMetricTypeDef = TypedDict(
    "PredictiveScalingCustomizedCapacityMetricTypeDef",
    {
        "MetricDataQueries": List[MetricDataQueryTypeDef],
    },
)

PredictiveScalingCustomizedLoadMetricTypeDef = TypedDict(
    "PredictiveScalingCustomizedLoadMetricTypeDef",
    {
        "MetricDataQueries": List[MetricDataQueryTypeDef],
    },
)

PredictiveScalingCustomizedScalingMetricTypeDef = TypedDict(
    "PredictiveScalingCustomizedScalingMetricTypeDef",
    {
        "MetricDataQueries": List[MetricDataQueryTypeDef],
    },
)

MixedInstancesPolicyTypeDef = TypedDict(
    "MixedInstancesPolicyTypeDef",
    {
        "LaunchTemplate": LaunchTemplateTypeDef,
        "InstancesDistribution": InstancesDistributionTypeDef,
    },
    total=False,
)

_RequiredPredictiveScalingMetricSpecificationTypeDef = TypedDict(
    "_RequiredPredictiveScalingMetricSpecificationTypeDef",
    {
        "TargetValue": float,
    },
)
_OptionalPredictiveScalingMetricSpecificationTypeDef = TypedDict(
    "_OptionalPredictiveScalingMetricSpecificationTypeDef",
    {
        "PredefinedMetricPairSpecification": PredictiveScalingPredefinedMetricPairTypeDef,
        "PredefinedScalingMetricSpecification": PredictiveScalingPredefinedScalingMetricTypeDef,
        "PredefinedLoadMetricSpecification": PredictiveScalingPredefinedLoadMetricTypeDef,
        "CustomizedScalingMetricSpecification": PredictiveScalingCustomizedScalingMetricTypeDef,
        "CustomizedLoadMetricSpecification": PredictiveScalingCustomizedLoadMetricTypeDef,
        "CustomizedCapacityMetricSpecification": PredictiveScalingCustomizedCapacityMetricTypeDef,
    },
    total=False,
)


class PredictiveScalingMetricSpecificationTypeDef(
    _RequiredPredictiveScalingMetricSpecificationTypeDef,
    _OptionalPredictiveScalingMetricSpecificationTypeDef,
):
    pass


_RequiredAutoScalingGroupTypeDef = TypedDict(
    "_RequiredAutoScalingGroupTypeDef",
    {
        "AutoScalingGroupName": str,
        "MinSize": int,
        "MaxSize": int,
        "DesiredCapacity": int,
        "DefaultCooldown": int,
        "AvailabilityZones": List[str],
        "HealthCheckType": str,
        "CreatedTime": datetime,
    },
)
_OptionalAutoScalingGroupTypeDef = TypedDict(
    "_OptionalAutoScalingGroupTypeDef",
    {
        "AutoScalingGroupARN": str,
        "LaunchConfigurationName": str,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "MixedInstancesPolicy": MixedInstancesPolicyTypeDef,
        "PredictedCapacity": int,
        "LoadBalancerNames": List[str],
        "TargetGroupARNs": List[str],
        "HealthCheckGracePeriod": int,
        "Instances": List[InstanceTypeDef],
        "SuspendedProcesses": List[SuspendedProcessTypeDef],
        "PlacementGroup": str,
        "VPCZoneIdentifier": str,
        "EnabledMetrics": List[EnabledMetricTypeDef],
        "Status": str,
        "Tags": List[TagDescriptionTypeDef],
        "TerminationPolicies": List[str],
        "NewInstancesProtectedFromScaleIn": bool,
        "ServiceLinkedRoleARN": str,
        "MaxInstanceLifetime": int,
        "CapacityRebalance": bool,
        "WarmPoolConfiguration": WarmPoolConfigurationTypeDef,
        "WarmPoolSize": int,
        "Context": str,
        "DesiredCapacityType": str,
        "DefaultInstanceWarmup": int,
    },
    total=False,
)


class AutoScalingGroupTypeDef(_RequiredAutoScalingGroupTypeDef, _OptionalAutoScalingGroupTypeDef):
    pass


_RequiredCreateAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_RequiredCreateAutoScalingGroupTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "MinSize": int,
        "MaxSize": int,
    },
)
_OptionalCreateAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_OptionalCreateAutoScalingGroupTypeRequestTypeDef",
    {
        "LaunchConfigurationName": str,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "MixedInstancesPolicy": MixedInstancesPolicyTypeDef,
        "InstanceId": str,
        "DesiredCapacity": int,
        "DefaultCooldown": int,
        "AvailabilityZones": Sequence[str],
        "LoadBalancerNames": Sequence[str],
        "TargetGroupARNs": Sequence[str],
        "HealthCheckType": str,
        "HealthCheckGracePeriod": int,
        "PlacementGroup": str,
        "VPCZoneIdentifier": str,
        "TerminationPolicies": Sequence[str],
        "NewInstancesProtectedFromScaleIn": bool,
        "CapacityRebalance": bool,
        "LifecycleHookSpecificationList": Sequence[LifecycleHookSpecificationTypeDef],
        "Tags": Sequence[TagTypeDef],
        "ServiceLinkedRoleARN": str,
        "MaxInstanceLifetime": int,
        "Context": str,
        "DesiredCapacityType": str,
        "DefaultInstanceWarmup": int,
    },
    total=False,
)


class CreateAutoScalingGroupTypeRequestTypeDef(
    _RequiredCreateAutoScalingGroupTypeRequestTypeDef,
    _OptionalCreateAutoScalingGroupTypeRequestTypeDef,
):
    pass


DesiredConfigurationTypeDef = TypedDict(
    "DesiredConfigurationTypeDef",
    {
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "MixedInstancesPolicy": MixedInstancesPolicyTypeDef,
    },
    total=False,
)

_RequiredUpdateAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_RequiredUpdateAutoScalingGroupTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalUpdateAutoScalingGroupTypeRequestTypeDef = TypedDict(
    "_OptionalUpdateAutoScalingGroupTypeRequestTypeDef",
    {
        "LaunchConfigurationName": str,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "MixedInstancesPolicy": MixedInstancesPolicyTypeDef,
        "MinSize": int,
        "MaxSize": int,
        "DesiredCapacity": int,
        "DefaultCooldown": int,
        "AvailabilityZones": Sequence[str],
        "HealthCheckType": str,
        "HealthCheckGracePeriod": int,
        "PlacementGroup": str,
        "VPCZoneIdentifier": str,
        "TerminationPolicies": Sequence[str],
        "NewInstancesProtectedFromScaleIn": bool,
        "ServiceLinkedRoleARN": str,
        "MaxInstanceLifetime": int,
        "CapacityRebalance": bool,
        "Context": str,
        "DesiredCapacityType": str,
        "DefaultInstanceWarmup": int,
    },
    total=False,
)


class UpdateAutoScalingGroupTypeRequestTypeDef(
    _RequiredUpdateAutoScalingGroupTypeRequestTypeDef,
    _OptionalUpdateAutoScalingGroupTypeRequestTypeDef,
):
    pass


LoadForecastTypeDef = TypedDict(
    "LoadForecastTypeDef",
    {
        "Timestamps": List[datetime],
        "Values": List[float],
        "MetricSpecification": PredictiveScalingMetricSpecificationTypeDef,
    },
)

_RequiredPredictiveScalingConfigurationTypeDef = TypedDict(
    "_RequiredPredictiveScalingConfigurationTypeDef",
    {
        "MetricSpecifications": List[PredictiveScalingMetricSpecificationTypeDef],
    },
)
_OptionalPredictiveScalingConfigurationTypeDef = TypedDict(
    "_OptionalPredictiveScalingConfigurationTypeDef",
    {
        "Mode": PredictiveScalingModeType,
        "SchedulingBufferTime": int,
        "MaxCapacityBreachBehavior": PredictiveScalingMaxCapacityBreachBehaviorType,
        "MaxCapacityBuffer": int,
    },
    total=False,
)


class PredictiveScalingConfigurationTypeDef(
    _RequiredPredictiveScalingConfigurationTypeDef, _OptionalPredictiveScalingConfigurationTypeDef
):
    pass


AutoScalingGroupsTypeTypeDef = TypedDict(
    "AutoScalingGroupsTypeTypeDef",
    {
        "AutoScalingGroups": List[AutoScalingGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceRefreshTypeDef = TypedDict(
    "InstanceRefreshTypeDef",
    {
        "InstanceRefreshId": str,
        "AutoScalingGroupName": str,
        "Status": InstanceRefreshStatusType,
        "StatusReason": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "PercentageComplete": int,
        "InstancesToUpdate": int,
        "ProgressDetails": InstanceRefreshProgressDetailsTypeDef,
        "Preferences": RefreshPreferencesTypeDef,
        "DesiredConfiguration": DesiredConfigurationTypeDef,
    },
    total=False,
)

_RequiredStartInstanceRefreshTypeRequestTypeDef = TypedDict(
    "_RequiredStartInstanceRefreshTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
    },
)
_OptionalStartInstanceRefreshTypeRequestTypeDef = TypedDict(
    "_OptionalStartInstanceRefreshTypeRequestTypeDef",
    {
        "Strategy": Literal["Rolling"],
        "DesiredConfiguration": DesiredConfigurationTypeDef,
        "Preferences": RefreshPreferencesTypeDef,
    },
    total=False,
)


class StartInstanceRefreshTypeRequestTypeDef(
    _RequiredStartInstanceRefreshTypeRequestTypeDef, _OptionalStartInstanceRefreshTypeRequestTypeDef
):
    pass


GetPredictiveScalingForecastAnswerTypeDef = TypedDict(
    "GetPredictiveScalingForecastAnswerTypeDef",
    {
        "LoadForecast": List[LoadForecastTypeDef],
        "CapacityForecast": CapacityForecastTypeDef,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutScalingPolicyTypeRequestTypeDef = TypedDict(
    "_RequiredPutScalingPolicyTypeRequestTypeDef",
    {
        "AutoScalingGroupName": str,
        "PolicyName": str,
    },
)
_OptionalPutScalingPolicyTypeRequestTypeDef = TypedDict(
    "_OptionalPutScalingPolicyTypeRequestTypeDef",
    {
        "PolicyType": str,
        "AdjustmentType": str,
        "MinAdjustmentStep": int,
        "MinAdjustmentMagnitude": int,
        "ScalingAdjustment": int,
        "Cooldown": int,
        "MetricAggregationType": str,
        "StepAdjustments": Sequence[StepAdjustmentTypeDef],
        "EstimatedInstanceWarmup": int,
        "TargetTrackingConfiguration": TargetTrackingConfigurationTypeDef,
        "Enabled": bool,
        "PredictiveScalingConfiguration": PredictiveScalingConfigurationTypeDef,
    },
    total=False,
)


class PutScalingPolicyTypeRequestTypeDef(
    _RequiredPutScalingPolicyTypeRequestTypeDef, _OptionalPutScalingPolicyTypeRequestTypeDef
):
    pass


ScalingPolicyTypeDef = TypedDict(
    "ScalingPolicyTypeDef",
    {
        "AutoScalingGroupName": str,
        "PolicyName": str,
        "PolicyARN": str,
        "PolicyType": str,
        "AdjustmentType": str,
        "MinAdjustmentStep": int,
        "MinAdjustmentMagnitude": int,
        "ScalingAdjustment": int,
        "Cooldown": int,
        "StepAdjustments": List[StepAdjustmentTypeDef],
        "MetricAggregationType": str,
        "EstimatedInstanceWarmup": int,
        "Alarms": List[AlarmTypeDef],
        "TargetTrackingConfiguration": TargetTrackingConfigurationTypeDef,
        "Enabled": bool,
        "PredictiveScalingConfiguration": PredictiveScalingConfigurationTypeDef,
    },
    total=False,
)

DescribeInstanceRefreshesAnswerTypeDef = TypedDict(
    "DescribeInstanceRefreshesAnswerTypeDef",
    {
        "InstanceRefreshes": List[InstanceRefreshTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PoliciesTypeTypeDef = TypedDict(
    "PoliciesTypeTypeDef",
    {
        "ScalingPolicies": List[ScalingPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
