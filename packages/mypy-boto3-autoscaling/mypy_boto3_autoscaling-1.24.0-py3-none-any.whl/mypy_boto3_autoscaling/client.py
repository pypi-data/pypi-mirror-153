"""
Type annotations for autoscaling service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_autoscaling.client import AutoScalingClient

    session = Session()
    client: AutoScalingClient = session.client("autoscaling")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import WarmPoolStateType
from .paginator import (
    DescribeAutoScalingGroupsPaginator,
    DescribeAutoScalingInstancesPaginator,
    DescribeLaunchConfigurationsPaginator,
    DescribeLoadBalancersPaginator,
    DescribeLoadBalancerTargetGroupsPaginator,
    DescribeNotificationConfigurationsPaginator,
    DescribePoliciesPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeTagsPaginator,
)
from .type_defs import (
    ActivitiesTypeTypeDef,
    ActivityTypeTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    BatchDeleteScheduledActionAnswerTypeDef,
    BatchPutScheduledUpdateGroupActionAnswerTypeDef,
    BlockDeviceMappingTypeDef,
    CancelInstanceRefreshAnswerTypeDef,
    DescribeAccountLimitsAnswerTypeDef,
    DescribeAdjustmentTypesAnswerTypeDef,
    DescribeAutoScalingNotificationTypesAnswerTypeDef,
    DescribeInstanceRefreshesAnswerTypeDef,
    DescribeLifecycleHooksAnswerTypeDef,
    DescribeLifecycleHookTypesAnswerTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeMetricCollectionTypesAnswerTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeTerminationPolicyTypesAnswerTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DesiredConfigurationTypeDef,
    DetachInstancesAnswerTypeDef,
    EmptyResponseMetadataTypeDef,
    EnterStandbyAnswerTypeDef,
    ExitStandbyAnswerTypeDef,
    FilterTypeDef,
    GetPredictiveScalingForecastAnswerTypeDef,
    InstanceMetadataOptionsTypeDef,
    InstanceMonitoringTypeDef,
    InstanceReusePolicyTypeDef,
    LaunchConfigurationsTypeTypeDef,
    LaunchTemplateSpecificationTypeDef,
    LifecycleHookSpecificationTypeDef,
    MixedInstancesPolicyTypeDef,
    PoliciesTypeTypeDef,
    PolicyARNTypeTypeDef,
    PredictiveScalingConfigurationTypeDef,
    ProcessesTypeTypeDef,
    RefreshPreferencesTypeDef,
    ScheduledActionsTypeTypeDef,
    ScheduledUpdateGroupActionRequestTypeDef,
    StartInstanceRefreshAnswerTypeDef,
    StepAdjustmentTypeDef,
    TagsTypeTypeDef,
    TagTypeDef,
    TargetTrackingConfigurationTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AutoScalingClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActiveInstanceRefreshNotFoundFault: Type[BotocoreClientError]
    AlreadyExistsFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InstanceRefreshInProgressFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    ResourceContentionFault: Type[BotocoreClientError]
    ResourceInUseFault: Type[BotocoreClientError]
    ScalingActivityInProgressFault: Type[BotocoreClientError]
    ServiceLinkedRoleFailure: Type[BotocoreClientError]


class AutoScalingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#exceptions)
        """

    def attach_instances(
        self, *, AutoScalingGroupName: str, InstanceIds: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches one or more EC2 instances to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#attach_instances)
        """

    def attach_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, TargetGroupARNs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Attaches one or more target groups to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancer_target_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#attach_load_balancer_target_groups)
        """

    def attach_load_balancers(
        self, *, AutoScalingGroupName: str, LoadBalancerNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#attach_load_balancers)
        """

    def batch_delete_scheduled_action(
        self, *, AutoScalingGroupName: str, ScheduledActionNames: Sequence[str]
    ) -> BatchDeleteScheduledActionAnswerTypeDef:
        """
        Deletes one or more scheduled actions for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_delete_scheduled_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#batch_delete_scheduled_action)
        """

    def batch_put_scheduled_update_group_action(
        self,
        *,
        AutoScalingGroupName: str,
        ScheduledUpdateGroupActions: Sequence[ScheduledUpdateGroupActionRequestTypeDef]
    ) -> BatchPutScheduledUpdateGroupActionAnswerTypeDef:
        """
        Creates or updates one or more scheduled scaling actions for an Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_put_scheduled_update_group_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#batch_put_scheduled_update_group_action)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#can_paginate)
        """

    def cancel_instance_refresh(
        self, *, AutoScalingGroupName: str
    ) -> CancelInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh operation in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.cancel_instance_refresh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#cancel_instance_refresh)
        """

    def complete_lifecycle_action(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleActionResult: str,
        LifecycleActionToken: str = ...,
        InstanceId: str = ...
    ) -> Dict[str, Any]:
        """
        Completes the lifecycle action for the specified token or instance with the
        specified result.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.complete_lifecycle_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#complete_lifecycle_action)
        """

    def create_auto_scaling_group(
        self,
        *,
        AutoScalingGroupName: str,
        MinSize: int,
        MaxSize: int,
        LaunchConfigurationName: str = ...,
        LaunchTemplate: LaunchTemplateSpecificationTypeDef = ...,
        MixedInstancesPolicy: MixedInstancesPolicyTypeDef = ...,
        InstanceId: str = ...,
        DesiredCapacity: int = ...,
        DefaultCooldown: int = ...,
        AvailabilityZones: Sequence[str] = ...,
        LoadBalancerNames: Sequence[str] = ...,
        TargetGroupARNs: Sequence[str] = ...,
        HealthCheckType: str = ...,
        HealthCheckGracePeriod: int = ...,
        PlacementGroup: str = ...,
        VPCZoneIdentifier: str = ...,
        TerminationPolicies: Sequence[str] = ...,
        NewInstancesProtectedFromScaleIn: bool = ...,
        CapacityRebalance: bool = ...,
        LifecycleHookSpecificationList: Sequence[LifecycleHookSpecificationTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ServiceLinkedRoleARN: str = ...,
        MaxInstanceLifetime: int = ...,
        Context: str = ...,
        DesiredCapacityType: str = ...,
        DefaultInstanceWarmup: int = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        **We strongly recommend using a launch template when calling this operation to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Creates
        an Auto Scaling group with the specified name and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#create_auto_scaling_group)
        """

    def create_launch_configuration(
        self,
        *,
        LaunchConfigurationName: str,
        ImageId: str = ...,
        KeyName: str = ...,
        SecurityGroups: Sequence[str] = ...,
        ClassicLinkVPCId: str = ...,
        ClassicLinkVPCSecurityGroups: Sequence[str] = ...,
        UserData: str = ...,
        InstanceId: str = ...,
        InstanceType: str = ...,
        KernelId: str = ...,
        RamdiskId: str = ...,
        BlockDeviceMappings: Sequence[BlockDeviceMappingTypeDef] = ...,
        InstanceMonitoring: InstanceMonitoringTypeDef = ...,
        SpotPrice: str = ...,
        IamInstanceProfile: str = ...,
        EbsOptimized: bool = ...,
        AssociatePublicIpAddress: bool = ...,
        PlacementTenancy: str = ...,
        MetadataOptions: InstanceMetadataOptionsTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_launch_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#create_launch_configuration)
        """

    def create_or_update_tags(self, *, Tags: Sequence[TagTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates tags for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_or_update_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#create_or_update_tags)
        """

    def delete_auto_scaling_group(
        self, *, AutoScalingGroupName: str, ForceDelete: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_auto_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_auto_scaling_group)
        """

    def delete_launch_configuration(
        self, *, LaunchConfigurationName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_launch_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_launch_configuration)
        """

    def delete_lifecycle_hook(
        self, *, LifecycleHookName: str, AutoScalingGroupName: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle hook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_lifecycle_hook)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_lifecycle_hook)
        """

    def delete_notification_configuration(
        self, *, AutoScalingGroupName: str, TopicARN: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_notification_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_notification_configuration)
        """

    def delete_policy(
        self, *, PolicyName: str, AutoScalingGroupName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_policy)
        """

    def delete_scheduled_action(
        self, *, AutoScalingGroupName: str, ScheduledActionName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_scheduled_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_scheduled_action)
        """

    def delete_tags(self, *, Tags: Sequence[TagTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_tags)
        """

    def delete_warm_pool(
        self, *, AutoScalingGroupName: str, ForceDelete: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_warm_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#delete_warm_pool)
        """

    def describe_account_limits(self) -> DescribeAccountLimitsAnswerTypeDef:
        """
        Describes the current Amazon EC2 Auto Scaling resource quotas for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_account_limits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_account_limits)
        """

    def describe_adjustment_types(self) -> DescribeAdjustmentTypesAnswerTypeDef:
        """
        Describes the available adjustment types for step scaling and simple scaling
        policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_adjustment_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_adjustment_types)
        """

    def describe_auto_scaling_groups(
        self,
        *,
        AutoScalingGroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...,
        Filters: Sequence[FilterTypeDef] = ...
    ) -> AutoScalingGroupsTypeTypeDef:
        """
        Gets information about the Auto Scaling groups in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_auto_scaling_groups)
        """

    def describe_auto_scaling_instances(
        self, *, InstanceIds: Sequence[str] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> AutoScalingInstancesTypeTypeDef:
        """
        Gets information about the Auto Scaling instances in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_auto_scaling_instances)
        """

    def describe_auto_scaling_notification_types(
        self,
    ) -> DescribeAutoScalingNotificationTypesAnswerTypeDef:
        """
        Describes the notification types that are supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_notification_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_auto_scaling_notification_types)
        """

    def describe_instance_refreshes(
        self,
        *,
        AutoScalingGroupName: str,
        InstanceRefreshIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> DescribeInstanceRefreshesAnswerTypeDef:
        """
        Gets information about the instance refreshes for the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_instance_refreshes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_instance_refreshes)
        """

    def describe_launch_configurations(
        self,
        *,
        LaunchConfigurationNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> LaunchConfigurationsTypeTypeDef:
        """
        Gets information about the launch configurations in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_launch_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_launch_configurations)
        """

    def describe_lifecycle_hook_types(self) -> DescribeLifecycleHookTypesAnswerTypeDef:
        """
        Describes the available types of lifecycle hooks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hook_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_lifecycle_hook_types)
        """

    def describe_lifecycle_hooks(
        self, *, AutoScalingGroupName: str, LifecycleHookNames: Sequence[str] = ...
    ) -> DescribeLifecycleHooksAnswerTypeDef:
        """
        Gets information about the lifecycle hooks for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hooks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_lifecycle_hooks)
        """

    def describe_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, NextToken: str = ..., MaxRecords: int = ...
    ) -> DescribeLoadBalancerTargetGroupsResponseTypeDef:
        """
        Gets information about the load balancer target groups for the specified Auto
        Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancer_target_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_load_balancer_target_groups)
        """

    def describe_load_balancers(
        self, *, AutoScalingGroupName: str, NextToken: str = ..., MaxRecords: int = ...
    ) -> DescribeLoadBalancersResponseTypeDef:
        """
        Gets information about the load balancers for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_load_balancers)
        """

    def describe_metric_collection_types(self) -> DescribeMetricCollectionTypesAnswerTypeDef:
        """
        Describes the available CloudWatch metrics for Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_metric_collection_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_metric_collection_types)
        """

    def describe_notification_configurations(
        self,
        *,
        AutoScalingGroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> DescribeNotificationConfigurationsAnswerTypeDef:
        """
        Gets information about the Amazon SNS notifications that are configured for one
        or more Auto Scaling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_notification_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_notification_configurations)
        """

    def describe_policies(
        self,
        *,
        AutoScalingGroupName: str = ...,
        PolicyNames: Sequence[str] = ...,
        PolicyTypes: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> PoliciesTypeTypeDef:
        """
        Gets information about the scaling policies in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_policies)
        """

    def describe_scaling_activities(
        self,
        *,
        ActivityIds: Sequence[str] = ...,
        AutoScalingGroupName: str = ...,
        IncludeDeletedGroups: bool = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> ActivitiesTypeTypeDef:
        """
        Gets information about the scaling activities in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_activities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_scaling_activities)
        """

    def describe_scaling_process_types(self) -> ProcessesTypeTypeDef:
        """
        Describes the scaling process types for use with the  ResumeProcesses and
        SuspendProcesses APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_process_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_scaling_process_types)
        """

    def describe_scheduled_actions(
        self,
        *,
        AutoScalingGroupName: str = ...,
        ScheduledActionNames: Sequence[str] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> ScheduledActionsTypeTypeDef:
        """
        Gets information about the scheduled actions that haven't run or that have not
        reached their end time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scheduled_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_scheduled_actions)
        """

    def describe_tags(
        self, *, Filters: Sequence[FilterTypeDef] = ..., NextToken: str = ..., MaxRecords: int = ...
    ) -> TagsTypeTypeDef:
        """
        Describes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_tags)
        """

    def describe_termination_policy_types(self) -> DescribeTerminationPolicyTypesAnswerTypeDef:
        """
        Describes the termination policies supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_termination_policy_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_termination_policy_types)
        """

    def describe_warm_pool(
        self, *, AutoScalingGroupName: str, MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeWarmPoolAnswerTypeDef:
        """
        Gets information about a warm pool and its instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_warm_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#describe_warm_pool)
        """

    def detach_instances(
        self,
        *,
        AutoScalingGroupName: str,
        ShouldDecrementDesiredCapacity: bool,
        InstanceIds: Sequence[str] = ...
    ) -> DetachInstancesAnswerTypeDef:
        """
        Removes one or more instances from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#detach_instances)
        """

    def detach_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, TargetGroupARNs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Detaches one or more target groups from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancer_target_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#detach_load_balancer_target_groups)
        """

    def detach_load_balancers(
        self, *, AutoScalingGroupName: str, LoadBalancerNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Detaches one or more Classic Load Balancers from the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#detach_load_balancers)
        """

    def disable_metrics_collection(
        self, *, AutoScalingGroupName: str, Metrics: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables group metrics for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.disable_metrics_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#disable_metrics_collection)
        """

    def enable_metrics_collection(
        self, *, AutoScalingGroupName: str, Granularity: str, Metrics: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables group metrics for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enable_metrics_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#enable_metrics_collection)
        """

    def enter_standby(
        self,
        *,
        AutoScalingGroupName: str,
        ShouldDecrementDesiredCapacity: bool,
        InstanceIds: Sequence[str] = ...
    ) -> EnterStandbyAnswerTypeDef:
        """
        Moves the specified instances into the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enter_standby)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#enter_standby)
        """

    def execute_policy(
        self,
        *,
        PolicyName: str,
        AutoScalingGroupName: str = ...,
        HonorCooldown: bool = ...,
        MetricValue: float = ...,
        BreachThreshold: float = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Executes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.execute_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#execute_policy)
        """

    def exit_standby(
        self, *, AutoScalingGroupName: str, InstanceIds: Sequence[str] = ...
    ) -> ExitStandbyAnswerTypeDef:
        """
        Moves the specified instances out of the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exit_standby)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#exit_standby)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#generate_presigned_url)
        """

    def get_predictive_scaling_forecast(
        self,
        *,
        AutoScalingGroupName: str,
        PolicyName: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str]
    ) -> GetPredictiveScalingForecastAnswerTypeDef:
        """
        Retrieves the forecast data for a predictive scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_predictive_scaling_forecast)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_predictive_scaling_forecast)
        """

    def put_lifecycle_hook(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleTransition: str = ...,
        RoleARN: str = ...,
        NotificationTargetARN: str = ...,
        NotificationMetadata: str = ...,
        HeartbeatTimeout: int = ...,
        DefaultResult: str = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates a lifecycle hook for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_lifecycle_hook)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#put_lifecycle_hook)
        """

    def put_notification_configuration(
        self, *, AutoScalingGroupName: str, TopicARN: str, NotificationTypes: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Configures an Auto Scaling group to send notifications when specified events
        take place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_notification_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#put_notification_configuration)
        """

    def put_scaling_policy(
        self,
        *,
        AutoScalingGroupName: str,
        PolicyName: str,
        PolicyType: str = ...,
        AdjustmentType: str = ...,
        MinAdjustmentStep: int = ...,
        MinAdjustmentMagnitude: int = ...,
        ScalingAdjustment: int = ...,
        Cooldown: int = ...,
        MetricAggregationType: str = ...,
        StepAdjustments: Sequence[StepAdjustmentTypeDef] = ...,
        EstimatedInstanceWarmup: int = ...,
        TargetTrackingConfiguration: TargetTrackingConfigurationTypeDef = ...,
        Enabled: bool = ...,
        PredictiveScalingConfiguration: PredictiveScalingConfigurationTypeDef = ...
    ) -> PolicyARNTypeTypeDef:
        """
        Creates or updates a scaling policy for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#put_scaling_policy)
        """

    def put_scheduled_update_group_action(
        self,
        *,
        AutoScalingGroupName: str,
        ScheduledActionName: str,
        Time: Union[datetime, str] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Recurrence: str = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        DesiredCapacity: int = ...,
        TimeZone: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a scheduled scaling action for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scheduled_update_group_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#put_scheduled_update_group_action)
        """

    def put_warm_pool(
        self,
        *,
        AutoScalingGroupName: str,
        MaxGroupPreparedCapacity: int = ...,
        MinSize: int = ...,
        PoolState: WarmPoolStateType = ...,
        InstanceReusePolicy: InstanceReusePolicyTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates a warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_warm_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#put_warm_pool)
        """

    def record_lifecycle_action_heartbeat(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleActionToken: str = ...,
        InstanceId: str = ...
    ) -> Dict[str, Any]:
        """
        Records a heartbeat for the lifecycle action associated with the specified token
        or instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.record_lifecycle_action_heartbeat)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#record_lifecycle_action_heartbeat)
        """

    def resume_processes(
        self, *, AutoScalingGroupName: str, ScalingProcesses: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resumes the specified suspended auto scaling processes, or all suspended
        process, for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.resume_processes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#resume_processes)
        """

    def set_desired_capacity(
        self, *, AutoScalingGroupName: str, DesiredCapacity: int, HonorCooldown: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the size of the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_desired_capacity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#set_desired_capacity)
        """

    def set_instance_health(
        self, *, InstanceId: str, HealthStatus: str, ShouldRespectGracePeriod: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the health status of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_health)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#set_instance_health)
        """

    def set_instance_protection(
        self, *, InstanceIds: Sequence[str], AutoScalingGroupName: str, ProtectedFromScaleIn: bool
    ) -> Dict[str, Any]:
        """
        Updates the instance protection settings of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_protection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#set_instance_protection)
        """

    def start_instance_refresh(
        self,
        *,
        AutoScalingGroupName: str,
        Strategy: Literal["Rolling"] = ...,
        DesiredConfiguration: DesiredConfigurationTypeDef = ...,
        Preferences: RefreshPreferencesTypeDef = ...
    ) -> StartInstanceRefreshAnswerTypeDef:
        """
        Starts a new instance refresh operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.start_instance_refresh)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#start_instance_refresh)
        """

    def suspend_processes(
        self, *, AutoScalingGroupName: str, ScalingProcesses: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Suspends the specified auto scaling processes, or all processes, for the
        specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.suspend_processes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#suspend_processes)
        """

    def terminate_instance_in_auto_scaling_group(
        self, *, InstanceId: str, ShouldDecrementDesiredCapacity: bool
    ) -> ActivityTypeTypeDef:
        """
        Terminates the specified instance and optionally adjusts the desired group size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.terminate_instance_in_auto_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#terminate_instance_in_auto_scaling_group)
        """

    def update_auto_scaling_group(
        self,
        *,
        AutoScalingGroupName: str,
        LaunchConfigurationName: str = ...,
        LaunchTemplate: LaunchTemplateSpecificationTypeDef = ...,
        MixedInstancesPolicy: MixedInstancesPolicyTypeDef = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        DesiredCapacity: int = ...,
        DefaultCooldown: int = ...,
        AvailabilityZones: Sequence[str] = ...,
        HealthCheckType: str = ...,
        HealthCheckGracePeriod: int = ...,
        PlacementGroup: str = ...,
        VPCZoneIdentifier: str = ...,
        TerminationPolicies: Sequence[str] = ...,
        NewInstancesProtectedFromScaleIn: bool = ...,
        ServiceLinkedRoleARN: str = ...,
        MaxInstanceLifetime: int = ...,
        CapacityRebalance: bool = ...,
        Context: str = ...,
        DesiredCapacityType: str = ...,
        DefaultInstanceWarmup: int = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        **We strongly recommend that all Auto Scaling groups use launch templates to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Updates
        the configuration for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.update_auto_scaling_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#update_auto_scaling_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_groups"]
    ) -> DescribeAutoScalingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_instances"]
    ) -> DescribeAutoScalingInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configurations"]
    ) -> DescribeLaunchConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancer_target_groups"]
    ) -> DescribeLoadBalancerTargetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_configurations"]
    ) -> DescribeNotificationConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_policies"]
    ) -> DescribePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling/client/#get_paginator)
        """
