"""
Type annotations for codedeploy service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/type_defs/)

Usage::

    ```python
    from mypy_boto3_codedeploy.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationRevisionSortByType,
    AutoRollbackEventType,
    BundleTypeType,
    ComputePlatformType,
    DeploymentCreatorType,
    DeploymentOptionType,
    DeploymentReadyActionType,
    DeploymentStatusType,
    DeploymentTargetTypeType,
    DeploymentTypeType,
    DeploymentWaitTypeType,
    EC2TagFilterTypeType,
    ErrorCodeType,
    FileExistsBehaviorType,
    GreenFleetProvisioningActionType,
    InstanceActionType,
    InstanceStatusType,
    InstanceTypeType,
    LifecycleErrorCodeType,
    LifecycleEventStatusType,
    ListStateFilterActionType,
    MinimumHealthyHostsTypeType,
    OutdatedInstancesStrategyType,
    RegistrationStatusType,
    RevisionLocationTypeType,
    SortOrderType,
    StopStatusType,
    TagFilterTypeType,
    TargetFilterNameType,
    TargetLabelType,
    TargetStatusType,
    TrafficRoutingTypeType,
    TriggerEventTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TagTypeDef",
    "AlarmTypeDef",
    "AppSpecContentTypeDef",
    "ApplicationInfoTypeDef",
    "AutoRollbackConfigurationTypeDef",
    "AutoScalingGroupTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetApplicationsInputRequestTypeDef",
    "BatchGetDeploymentGroupsInputRequestTypeDef",
    "BatchGetDeploymentInstancesInputRequestTypeDef",
    "BatchGetDeploymentTargetsInputRequestTypeDef",
    "BatchGetDeploymentsInputRequestTypeDef",
    "BatchGetOnPremisesInstancesInputRequestTypeDef",
    "BlueInstanceTerminationOptionTypeDef",
    "DeploymentReadyOptionTypeDef",
    "GreenFleetProvisioningOptionTypeDef",
    "ContinueDeploymentInputRequestTypeDef",
    "MinimumHealthyHostsTypeDef",
    "DeploymentStyleTypeDef",
    "EC2TagFilterTypeDef",
    "ECSServiceTypeDef",
    "TagFilterTypeDef",
    "TriggerConfigTypeDef",
    "DeleteApplicationInputRequestTypeDef",
    "DeleteDeploymentConfigInputRequestTypeDef",
    "DeleteDeploymentGroupInputRequestTypeDef",
    "DeleteGitHubAccountTokenInputRequestTypeDef",
    "DeleteResourcesByExternalIdInputRequestTypeDef",
    "LastDeploymentInfoTypeDef",
    "DeploymentOverviewTypeDef",
    "ErrorInformationTypeDef",
    "RelatedDeploymentsTypeDef",
    "RollbackInfoTypeDef",
    "DeregisterOnPremisesInstanceInputRequestTypeDef",
    "DiagnosticsTypeDef",
    "TargetGroupInfoTypeDef",
    "ELBInfoTypeDef",
    "GenericRevisionInfoTypeDef",
    "GetApplicationInputRequestTypeDef",
    "GetDeploymentConfigInputRequestTypeDef",
    "GetDeploymentGroupInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetDeploymentInputRequestTypeDef",
    "GetDeploymentInstanceInputRequestTypeDef",
    "GetDeploymentTargetInputRequestTypeDef",
    "GetOnPremisesInstanceInputRequestTypeDef",
    "GitHubLocationTypeDef",
    "LambdaFunctionInfoTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationRevisionsInputRequestTypeDef",
    "ListApplicationsInputRequestTypeDef",
    "ListDeploymentConfigsInputRequestTypeDef",
    "ListDeploymentGroupsInputRequestTypeDef",
    "ListDeploymentInstancesInputRequestTypeDef",
    "ListDeploymentTargetsInputRequestTypeDef",
    "TimeRangeTypeDef",
    "ListGitHubAccountTokenNamesInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "PutLifecycleEventHookExecutionStatusInputRequestTypeDef",
    "RawStringTypeDef",
    "RegisterOnPremisesInstanceInputRequestTypeDef",
    "S3LocationTypeDef",
    "SkipWaitTimeForInstanceTerminationInputRequestTypeDef",
    "StopDeploymentInputRequestTypeDef",
    "TrafficRouteTypeDef",
    "TimeBasedCanaryTypeDef",
    "TimeBasedLinearTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateApplicationInputRequestTypeDef",
    "AddTagsToOnPremisesInstancesInputRequestTypeDef",
    "CreateApplicationInputRequestTypeDef",
    "InstanceInfoTypeDef",
    "RemoveTagsFromOnPremisesInstancesInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "AlarmConfigurationTypeDef",
    "BatchGetApplicationsOutputTypeDef",
    "CreateApplicationOutputTypeDef",
    "CreateDeploymentConfigOutputTypeDef",
    "CreateDeploymentGroupOutputTypeDef",
    "CreateDeploymentOutputTypeDef",
    "DeleteDeploymentGroupOutputTypeDef",
    "DeleteGitHubAccountTokenOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApplicationOutputTypeDef",
    "ListApplicationsOutputTypeDef",
    "ListDeploymentConfigsOutputTypeDef",
    "ListDeploymentGroupsOutputTypeDef",
    "ListDeploymentInstancesOutputTypeDef",
    "ListDeploymentTargetsOutputTypeDef",
    "ListDeploymentsOutputTypeDef",
    "ListGitHubAccountTokenNamesOutputTypeDef",
    "ListOnPremisesInstancesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PutLifecycleEventHookExecutionStatusOutputTypeDef",
    "StopDeploymentOutputTypeDef",
    "UpdateDeploymentGroupOutputTypeDef",
    "BlueGreenDeploymentConfigurationTypeDef",
    "EC2TagSetTypeDef",
    "ListOnPremisesInstancesInputRequestTypeDef",
    "OnPremisesTagSetTypeDef",
    "LifecycleEventTypeDef",
    "ECSTaskSetTypeDef",
    "GetDeploymentInputDeploymentSuccessfulWaitTypeDef",
    "ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef",
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    "ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef",
    "ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef",
    "ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef",
    "ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef",
    "ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef",
    "ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef",
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    "ListDeploymentsInputRequestTypeDef",
    "RevisionLocationTypeDef",
    "TargetGroupPairInfoTypeDef",
    "TrafficRoutingConfigTypeDef",
    "BatchGetOnPremisesInstancesOutputTypeDef",
    "GetOnPremisesInstanceOutputTypeDef",
    "TargetInstancesTypeDef",
    "CloudFormationTargetTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceTargetTypeDef",
    "LambdaTargetTypeDef",
    "ECSTargetTypeDef",
    "BatchGetApplicationRevisionsInputRequestTypeDef",
    "GetApplicationRevisionInputRequestTypeDef",
    "GetApplicationRevisionOutputTypeDef",
    "ListApplicationRevisionsOutputTypeDef",
    "RegisterApplicationRevisionInputRequestTypeDef",
    "RevisionInfoTypeDef",
    "LoadBalancerInfoTypeDef",
    "CreateDeploymentConfigInputRequestTypeDef",
    "DeploymentConfigInfoTypeDef",
    "CreateDeploymentInputRequestTypeDef",
    "BatchGetDeploymentInstancesOutputTypeDef",
    "GetDeploymentInstanceOutputTypeDef",
    "DeploymentTargetTypeDef",
    "BatchGetApplicationRevisionsOutputTypeDef",
    "CreateDeploymentGroupInputRequestTypeDef",
    "DeploymentGroupInfoTypeDef",
    "DeploymentInfoTypeDef",
    "UpdateDeploymentGroupInputRequestTypeDef",
    "GetDeploymentConfigOutputTypeDef",
    "BatchGetDeploymentTargetsOutputTypeDef",
    "GetDeploymentTargetOutputTypeDef",
    "BatchGetDeploymentGroupsOutputTypeDef",
    "GetDeploymentGroupOutputTypeDef",
    "BatchGetDeploymentsOutputTypeDef",
    "GetDeploymentOutputTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AlarmTypeDef = TypedDict(
    "AlarmTypeDef",
    {
        "name": str,
    },
    total=False,
)

AppSpecContentTypeDef = TypedDict(
    "AppSpecContentTypeDef",
    {
        "content": str,
        "sha256": str,
    },
    total=False,
)

ApplicationInfoTypeDef = TypedDict(
    "ApplicationInfoTypeDef",
    {
        "applicationId": str,
        "applicationName": str,
        "createTime": datetime,
        "linkedToGitHub": bool,
        "gitHubAccountName": str,
        "computePlatform": ComputePlatformType,
    },
    total=False,
)

AutoRollbackConfigurationTypeDef = TypedDict(
    "AutoRollbackConfigurationTypeDef",
    {
        "enabled": bool,
        "events": List[AutoRollbackEventType],
    },
    total=False,
)

AutoScalingGroupTypeDef = TypedDict(
    "AutoScalingGroupTypeDef",
    {
        "name": str,
        "hook": str,
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

BatchGetApplicationsInputRequestTypeDef = TypedDict(
    "BatchGetApplicationsInputRequestTypeDef",
    {
        "applicationNames": Sequence[str],
    },
)

BatchGetDeploymentGroupsInputRequestTypeDef = TypedDict(
    "BatchGetDeploymentGroupsInputRequestTypeDef",
    {
        "applicationName": str,
        "deploymentGroupNames": Sequence[str],
    },
)

BatchGetDeploymentInstancesInputRequestTypeDef = TypedDict(
    "BatchGetDeploymentInstancesInputRequestTypeDef",
    {
        "deploymentId": str,
        "instanceIds": Sequence[str],
    },
)

BatchGetDeploymentTargetsInputRequestTypeDef = TypedDict(
    "BatchGetDeploymentTargetsInputRequestTypeDef",
    {
        "deploymentId": str,
        "targetIds": Sequence[str],
    },
    total=False,
)

BatchGetDeploymentsInputRequestTypeDef = TypedDict(
    "BatchGetDeploymentsInputRequestTypeDef",
    {
        "deploymentIds": Sequence[str],
    },
)

BatchGetOnPremisesInstancesInputRequestTypeDef = TypedDict(
    "BatchGetOnPremisesInstancesInputRequestTypeDef",
    {
        "instanceNames": Sequence[str],
    },
)

BlueInstanceTerminationOptionTypeDef = TypedDict(
    "BlueInstanceTerminationOptionTypeDef",
    {
        "action": InstanceActionType,
        "terminationWaitTimeInMinutes": int,
    },
    total=False,
)

DeploymentReadyOptionTypeDef = TypedDict(
    "DeploymentReadyOptionTypeDef",
    {
        "actionOnTimeout": DeploymentReadyActionType,
        "waitTimeInMinutes": int,
    },
    total=False,
)

GreenFleetProvisioningOptionTypeDef = TypedDict(
    "GreenFleetProvisioningOptionTypeDef",
    {
        "action": GreenFleetProvisioningActionType,
    },
    total=False,
)

ContinueDeploymentInputRequestTypeDef = TypedDict(
    "ContinueDeploymentInputRequestTypeDef",
    {
        "deploymentId": str,
        "deploymentWaitType": DeploymentWaitTypeType,
    },
    total=False,
)

MinimumHealthyHostsTypeDef = TypedDict(
    "MinimumHealthyHostsTypeDef",
    {
        "type": MinimumHealthyHostsTypeType,
        "value": int,
    },
    total=False,
)

DeploymentStyleTypeDef = TypedDict(
    "DeploymentStyleTypeDef",
    {
        "deploymentType": DeploymentTypeType,
        "deploymentOption": DeploymentOptionType,
    },
    total=False,
)

EC2TagFilterTypeDef = TypedDict(
    "EC2TagFilterTypeDef",
    {
        "Key": str,
        "Value": str,
        "Type": EC2TagFilterTypeType,
    },
    total=False,
)

ECSServiceTypeDef = TypedDict(
    "ECSServiceTypeDef",
    {
        "serviceName": str,
        "clusterName": str,
    },
    total=False,
)

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "Key": str,
        "Value": str,
        "Type": TagFilterTypeType,
    },
    total=False,
)

TriggerConfigTypeDef = TypedDict(
    "TriggerConfigTypeDef",
    {
        "triggerName": str,
        "triggerTargetArn": str,
        "triggerEvents": List[TriggerEventTypeType],
    },
    total=False,
)

DeleteApplicationInputRequestTypeDef = TypedDict(
    "DeleteApplicationInputRequestTypeDef",
    {
        "applicationName": str,
    },
)

DeleteDeploymentConfigInputRequestTypeDef = TypedDict(
    "DeleteDeploymentConfigInputRequestTypeDef",
    {
        "deploymentConfigName": str,
    },
)

DeleteDeploymentGroupInputRequestTypeDef = TypedDict(
    "DeleteDeploymentGroupInputRequestTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
    },
)

DeleteGitHubAccountTokenInputRequestTypeDef = TypedDict(
    "DeleteGitHubAccountTokenInputRequestTypeDef",
    {
        "tokenName": str,
    },
    total=False,
)

DeleteResourcesByExternalIdInputRequestTypeDef = TypedDict(
    "DeleteResourcesByExternalIdInputRequestTypeDef",
    {
        "externalId": str,
    },
    total=False,
)

LastDeploymentInfoTypeDef = TypedDict(
    "LastDeploymentInfoTypeDef",
    {
        "deploymentId": str,
        "status": DeploymentStatusType,
        "endTime": datetime,
        "createTime": datetime,
    },
    total=False,
)

DeploymentOverviewTypeDef = TypedDict(
    "DeploymentOverviewTypeDef",
    {
        "Pending": int,
        "InProgress": int,
        "Succeeded": int,
        "Failed": int,
        "Skipped": int,
        "Ready": int,
    },
    total=False,
)

ErrorInformationTypeDef = TypedDict(
    "ErrorInformationTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
    total=False,
)

RelatedDeploymentsTypeDef = TypedDict(
    "RelatedDeploymentsTypeDef",
    {
        "autoUpdateOutdatedInstancesRootDeploymentId": str,
        "autoUpdateOutdatedInstancesDeploymentIds": List[str],
    },
    total=False,
)

RollbackInfoTypeDef = TypedDict(
    "RollbackInfoTypeDef",
    {
        "rollbackDeploymentId": str,
        "rollbackTriggeringDeploymentId": str,
        "rollbackMessage": str,
    },
    total=False,
)

DeregisterOnPremisesInstanceInputRequestTypeDef = TypedDict(
    "DeregisterOnPremisesInstanceInputRequestTypeDef",
    {
        "instanceName": str,
    },
)

DiagnosticsTypeDef = TypedDict(
    "DiagnosticsTypeDef",
    {
        "errorCode": LifecycleErrorCodeType,
        "scriptName": str,
        "message": str,
        "logTail": str,
    },
    total=False,
)

TargetGroupInfoTypeDef = TypedDict(
    "TargetGroupInfoTypeDef",
    {
        "name": str,
    },
    total=False,
)

ELBInfoTypeDef = TypedDict(
    "ELBInfoTypeDef",
    {
        "name": str,
    },
    total=False,
)

GenericRevisionInfoTypeDef = TypedDict(
    "GenericRevisionInfoTypeDef",
    {
        "description": str,
        "deploymentGroups": List[str],
        "firstUsedTime": datetime,
        "lastUsedTime": datetime,
        "registerTime": datetime,
    },
    total=False,
)

GetApplicationInputRequestTypeDef = TypedDict(
    "GetApplicationInputRequestTypeDef",
    {
        "applicationName": str,
    },
)

GetDeploymentConfigInputRequestTypeDef = TypedDict(
    "GetDeploymentConfigInputRequestTypeDef",
    {
        "deploymentConfigName": str,
    },
)

GetDeploymentGroupInputRequestTypeDef = TypedDict(
    "GetDeploymentGroupInputRequestTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
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

GetDeploymentInputRequestTypeDef = TypedDict(
    "GetDeploymentInputRequestTypeDef",
    {
        "deploymentId": str,
    },
)

GetDeploymentInstanceInputRequestTypeDef = TypedDict(
    "GetDeploymentInstanceInputRequestTypeDef",
    {
        "deploymentId": str,
        "instanceId": str,
    },
)

GetDeploymentTargetInputRequestTypeDef = TypedDict(
    "GetDeploymentTargetInputRequestTypeDef",
    {
        "deploymentId": str,
        "targetId": str,
    },
    total=False,
)

GetOnPremisesInstanceInputRequestTypeDef = TypedDict(
    "GetOnPremisesInstanceInputRequestTypeDef",
    {
        "instanceName": str,
    },
)

GitHubLocationTypeDef = TypedDict(
    "GitHubLocationTypeDef",
    {
        "repository": str,
        "commitId": str,
    },
    total=False,
)

LambdaFunctionInfoTypeDef = TypedDict(
    "LambdaFunctionInfoTypeDef",
    {
        "functionName": str,
        "functionAlias": str,
        "currentVersion": str,
        "targetVersion": str,
        "targetVersionWeight": float,
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

_RequiredListApplicationRevisionsInputRequestTypeDef = TypedDict(
    "_RequiredListApplicationRevisionsInputRequestTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalListApplicationRevisionsInputRequestTypeDef = TypedDict(
    "_OptionalListApplicationRevisionsInputRequestTypeDef",
    {
        "sortBy": ApplicationRevisionSortByType,
        "sortOrder": SortOrderType,
        "s3Bucket": str,
        "s3KeyPrefix": str,
        "deployed": ListStateFilterActionType,
        "nextToken": str,
    },
    total=False,
)


class ListApplicationRevisionsInputRequestTypeDef(
    _RequiredListApplicationRevisionsInputRequestTypeDef,
    _OptionalListApplicationRevisionsInputRequestTypeDef,
):
    pass


ListApplicationsInputRequestTypeDef = TypedDict(
    "ListApplicationsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

ListDeploymentConfigsInputRequestTypeDef = TypedDict(
    "ListDeploymentConfigsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

_RequiredListDeploymentGroupsInputRequestTypeDef = TypedDict(
    "_RequiredListDeploymentGroupsInputRequestTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalListDeploymentGroupsInputRequestTypeDef = TypedDict(
    "_OptionalListDeploymentGroupsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListDeploymentGroupsInputRequestTypeDef(
    _RequiredListDeploymentGroupsInputRequestTypeDef,
    _OptionalListDeploymentGroupsInputRequestTypeDef,
):
    pass


_RequiredListDeploymentInstancesInputRequestTypeDef = TypedDict(
    "_RequiredListDeploymentInstancesInputRequestTypeDef",
    {
        "deploymentId": str,
    },
)
_OptionalListDeploymentInstancesInputRequestTypeDef = TypedDict(
    "_OptionalListDeploymentInstancesInputRequestTypeDef",
    {
        "nextToken": str,
        "instanceStatusFilter": Sequence[InstanceStatusType],
        "instanceTypeFilter": Sequence[InstanceTypeType],
    },
    total=False,
)


class ListDeploymentInstancesInputRequestTypeDef(
    _RequiredListDeploymentInstancesInputRequestTypeDef,
    _OptionalListDeploymentInstancesInputRequestTypeDef,
):
    pass


ListDeploymentTargetsInputRequestTypeDef = TypedDict(
    "ListDeploymentTargetsInputRequestTypeDef",
    {
        "deploymentId": str,
        "nextToken": str,
        "targetFilters": Mapping[TargetFilterNameType, Sequence[str]],
    },
    total=False,
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef",
    {
        "start": Union[datetime, str],
        "end": Union[datetime, str],
    },
    total=False,
)

ListGitHubAccountTokenNamesInputRequestTypeDef = TypedDict(
    "ListGitHubAccountTokenNamesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


PutLifecycleEventHookExecutionStatusInputRequestTypeDef = TypedDict(
    "PutLifecycleEventHookExecutionStatusInputRequestTypeDef",
    {
        "deploymentId": str,
        "lifecycleEventHookExecutionId": str,
        "status": LifecycleEventStatusType,
    },
    total=False,
)

RawStringTypeDef = TypedDict(
    "RawStringTypeDef",
    {
        "content": str,
        "sha256": str,
    },
    total=False,
)

_RequiredRegisterOnPremisesInstanceInputRequestTypeDef = TypedDict(
    "_RequiredRegisterOnPremisesInstanceInputRequestTypeDef",
    {
        "instanceName": str,
    },
)
_OptionalRegisterOnPremisesInstanceInputRequestTypeDef = TypedDict(
    "_OptionalRegisterOnPremisesInstanceInputRequestTypeDef",
    {
        "iamSessionArn": str,
        "iamUserArn": str,
    },
    total=False,
)


class RegisterOnPremisesInstanceInputRequestTypeDef(
    _RequiredRegisterOnPremisesInstanceInputRequestTypeDef,
    _OptionalRegisterOnPremisesInstanceInputRequestTypeDef,
):
    pass


S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": str,
        "key": str,
        "bundleType": BundleTypeType,
        "version": str,
        "eTag": str,
    },
    total=False,
)

SkipWaitTimeForInstanceTerminationInputRequestTypeDef = TypedDict(
    "SkipWaitTimeForInstanceTerminationInputRequestTypeDef",
    {
        "deploymentId": str,
    },
    total=False,
)

_RequiredStopDeploymentInputRequestTypeDef = TypedDict(
    "_RequiredStopDeploymentInputRequestTypeDef",
    {
        "deploymentId": str,
    },
)
_OptionalStopDeploymentInputRequestTypeDef = TypedDict(
    "_OptionalStopDeploymentInputRequestTypeDef",
    {
        "autoRollbackEnabled": bool,
    },
    total=False,
)


class StopDeploymentInputRequestTypeDef(
    _RequiredStopDeploymentInputRequestTypeDef, _OptionalStopDeploymentInputRequestTypeDef
):
    pass


TrafficRouteTypeDef = TypedDict(
    "TrafficRouteTypeDef",
    {
        "listenerArns": List[str],
    },
    total=False,
)

TimeBasedCanaryTypeDef = TypedDict(
    "TimeBasedCanaryTypeDef",
    {
        "canaryPercentage": int,
        "canaryInterval": int,
    },
    total=False,
)

TimeBasedLinearTypeDef = TypedDict(
    "TimeBasedLinearTypeDef",
    {
        "linearPercentage": int,
        "linearInterval": int,
    },
    total=False,
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateApplicationInputRequestTypeDef = TypedDict(
    "UpdateApplicationInputRequestTypeDef",
    {
        "applicationName": str,
        "newApplicationName": str,
    },
    total=False,
)

AddTagsToOnPremisesInstancesInputRequestTypeDef = TypedDict(
    "AddTagsToOnPremisesInstancesInputRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
        "instanceNames": Sequence[str],
    },
)

_RequiredCreateApplicationInputRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationInputRequestTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalCreateApplicationInputRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationInputRequestTypeDef",
    {
        "computePlatform": ComputePlatformType,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateApplicationInputRequestTypeDef(
    _RequiredCreateApplicationInputRequestTypeDef, _OptionalCreateApplicationInputRequestTypeDef
):
    pass


InstanceInfoTypeDef = TypedDict(
    "InstanceInfoTypeDef",
    {
        "instanceName": str,
        "iamSessionArn": str,
        "iamUserArn": str,
        "instanceArn": str,
        "registerTime": datetime,
        "deregisterTime": datetime,
        "tags": List[TagTypeDef],
    },
    total=False,
)

RemoveTagsFromOnPremisesInstancesInputRequestTypeDef = TypedDict(
    "RemoveTagsFromOnPremisesInstancesInputRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
        "instanceNames": Sequence[str],
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

AlarmConfigurationTypeDef = TypedDict(
    "AlarmConfigurationTypeDef",
    {
        "enabled": bool,
        "ignorePollAlarmFailure": bool,
        "alarms": List[AlarmTypeDef],
    },
    total=False,
)

BatchGetApplicationsOutputTypeDef = TypedDict(
    "BatchGetApplicationsOutputTypeDef",
    {
        "applicationsInfo": List[ApplicationInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationOutputTypeDef = TypedDict(
    "CreateApplicationOutputTypeDef",
    {
        "applicationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentConfigOutputTypeDef = TypedDict(
    "CreateDeploymentConfigOutputTypeDef",
    {
        "deploymentConfigId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentGroupOutputTypeDef = TypedDict(
    "CreateDeploymentGroupOutputTypeDef",
    {
        "deploymentGroupId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentOutputTypeDef = TypedDict(
    "CreateDeploymentOutputTypeDef",
    {
        "deploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDeploymentGroupOutputTypeDef = TypedDict(
    "DeleteDeploymentGroupOutputTypeDef",
    {
        "hooksNotCleanedUp": List[AutoScalingGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGitHubAccountTokenOutputTypeDef = TypedDict(
    "DeleteGitHubAccountTokenOutputTypeDef",
    {
        "tokenName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationOutputTypeDef = TypedDict(
    "GetApplicationOutputTypeDef",
    {
        "application": ApplicationInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsOutputTypeDef = TypedDict(
    "ListApplicationsOutputTypeDef",
    {
        "applications": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentConfigsOutputTypeDef = TypedDict(
    "ListDeploymentConfigsOutputTypeDef",
    {
        "deploymentConfigsList": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentGroupsOutputTypeDef = TypedDict(
    "ListDeploymentGroupsOutputTypeDef",
    {
        "applicationName": str,
        "deploymentGroups": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentInstancesOutputTypeDef = TypedDict(
    "ListDeploymentInstancesOutputTypeDef",
    {
        "instancesList": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentTargetsOutputTypeDef = TypedDict(
    "ListDeploymentTargetsOutputTypeDef",
    {
        "targetIds": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentsOutputTypeDef = TypedDict(
    "ListDeploymentsOutputTypeDef",
    {
        "deployments": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGitHubAccountTokenNamesOutputTypeDef = TypedDict(
    "ListGitHubAccountTokenNamesOutputTypeDef",
    {
        "tokenNameList": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOnPremisesInstancesOutputTypeDef = TypedDict(
    "ListOnPremisesInstancesOutputTypeDef",
    {
        "instanceNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLifecycleEventHookExecutionStatusOutputTypeDef = TypedDict(
    "PutLifecycleEventHookExecutionStatusOutputTypeDef",
    {
        "lifecycleEventHookExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDeploymentOutputTypeDef = TypedDict(
    "StopDeploymentOutputTypeDef",
    {
        "status": StopStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDeploymentGroupOutputTypeDef = TypedDict(
    "UpdateDeploymentGroupOutputTypeDef",
    {
        "hooksNotCleanedUp": List[AutoScalingGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BlueGreenDeploymentConfigurationTypeDef = TypedDict(
    "BlueGreenDeploymentConfigurationTypeDef",
    {
        "terminateBlueInstancesOnDeploymentSuccess": BlueInstanceTerminationOptionTypeDef,
        "deploymentReadyOption": DeploymentReadyOptionTypeDef,
        "greenFleetProvisioningOption": GreenFleetProvisioningOptionTypeDef,
    },
    total=False,
)

EC2TagSetTypeDef = TypedDict(
    "EC2TagSetTypeDef",
    {
        "ec2TagSetList": List[List[EC2TagFilterTypeDef]],
    },
    total=False,
)

ListOnPremisesInstancesInputRequestTypeDef = TypedDict(
    "ListOnPremisesInstancesInputRequestTypeDef",
    {
        "registrationStatus": RegistrationStatusType,
        "tagFilters": Sequence[TagFilterTypeDef],
        "nextToken": str,
    },
    total=False,
)

OnPremisesTagSetTypeDef = TypedDict(
    "OnPremisesTagSetTypeDef",
    {
        "onPremisesTagSetList": List[List[TagFilterTypeDef]],
    },
    total=False,
)

LifecycleEventTypeDef = TypedDict(
    "LifecycleEventTypeDef",
    {
        "lifecycleEventName": str,
        "diagnostics": DiagnosticsTypeDef,
        "startTime": datetime,
        "endTime": datetime,
        "status": LifecycleEventStatusType,
    },
    total=False,
)

ECSTaskSetTypeDef = TypedDict(
    "ECSTaskSetTypeDef",
    {
        "identifer": str,
        "desiredCount": int,
        "pendingCount": int,
        "runningCount": int,
        "status": str,
        "trafficWeight": float,
        "targetGroup": TargetGroupInfoTypeDef,
        "taskSetLabel": TargetLabelType,
    },
    total=False,
)

_RequiredGetDeploymentInputDeploymentSuccessfulWaitTypeDef = TypedDict(
    "_RequiredGetDeploymentInputDeploymentSuccessfulWaitTypeDef",
    {
        "deploymentId": str,
    },
)
_OptionalGetDeploymentInputDeploymentSuccessfulWaitTypeDef = TypedDict(
    "_OptionalGetDeploymentInputDeploymentSuccessfulWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetDeploymentInputDeploymentSuccessfulWaitTypeDef(
    _RequiredGetDeploymentInputDeploymentSuccessfulWaitTypeDef,
    _OptionalGetDeploymentInputDeploymentSuccessfulWaitTypeDef,
):
    pass


_RequiredListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef = TypedDict(
    "_RequiredListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef = TypedDict(
    "_OptionalListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef",
    {
        "sortBy": ApplicationRevisionSortByType,
        "sortOrder": SortOrderType,
        "s3Bucket": str,
        "s3KeyPrefix": str,
        "deployed": ListStateFilterActionType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef(
    _RequiredListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef,
    _OptionalListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef,
):
    pass


ListApplicationsInputListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsInputListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef = TypedDict(
    "ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef = TypedDict(
    "_RequiredListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef = TypedDict(
    "_OptionalListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef(
    _RequiredListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef,
    _OptionalListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef,
):
    pass


_RequiredListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef = TypedDict(
    "_RequiredListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef",
    {
        "deploymentId": str,
    },
)
_OptionalListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef = TypedDict(
    "_OptionalListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef",
    {
        "instanceStatusFilter": Sequence[InstanceStatusType],
        "instanceTypeFilter": Sequence[InstanceTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef(
    _RequiredListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef,
    _OptionalListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef,
):
    pass


ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef = TypedDict(
    "ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef",
    {
        "deploymentId": str,
        "targetFilters": Mapping[TargetFilterNameType, Sequence[str]],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef = TypedDict(
    "ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef = TypedDict(
    "ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef",
    {
        "registrationStatus": RegistrationStatusType,
        "tagFilters": Sequence[TagFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDeploymentsInputListDeploymentsPaginateTypeDef = TypedDict(
    "ListDeploymentsInputListDeploymentsPaginateTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
        "externalId": str,
        "includeOnlyStatuses": Sequence[DeploymentStatusType],
        "createTimeRange": TimeRangeTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDeploymentsInputRequestTypeDef = TypedDict(
    "ListDeploymentsInputRequestTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
        "externalId": str,
        "includeOnlyStatuses": Sequence[DeploymentStatusType],
        "createTimeRange": TimeRangeTypeDef,
        "nextToken": str,
    },
    total=False,
)

RevisionLocationTypeDef = TypedDict(
    "RevisionLocationTypeDef",
    {
        "revisionType": RevisionLocationTypeType,
        "s3Location": S3LocationTypeDef,
        "gitHubLocation": GitHubLocationTypeDef,
        "string": RawStringTypeDef,
        "appSpecContent": AppSpecContentTypeDef,
    },
    total=False,
)

TargetGroupPairInfoTypeDef = TypedDict(
    "TargetGroupPairInfoTypeDef",
    {
        "targetGroups": List[TargetGroupInfoTypeDef],
        "prodTrafficRoute": TrafficRouteTypeDef,
        "testTrafficRoute": TrafficRouteTypeDef,
    },
    total=False,
)

TrafficRoutingConfigTypeDef = TypedDict(
    "TrafficRoutingConfigTypeDef",
    {
        "type": TrafficRoutingTypeType,
        "timeBasedCanary": TimeBasedCanaryTypeDef,
        "timeBasedLinear": TimeBasedLinearTypeDef,
    },
    total=False,
)

BatchGetOnPremisesInstancesOutputTypeDef = TypedDict(
    "BatchGetOnPremisesInstancesOutputTypeDef",
    {
        "instanceInfos": List[InstanceInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOnPremisesInstanceOutputTypeDef = TypedDict(
    "GetOnPremisesInstanceOutputTypeDef",
    {
        "instanceInfo": InstanceInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TargetInstancesTypeDef = TypedDict(
    "TargetInstancesTypeDef",
    {
        "tagFilters": List[EC2TagFilterTypeDef],
        "autoScalingGroups": List[str],
        "ec2TagSet": EC2TagSetTypeDef,
    },
    total=False,
)

CloudFormationTargetTypeDef = TypedDict(
    "CloudFormationTargetTypeDef",
    {
        "deploymentId": str,
        "targetId": str,
        "lastUpdatedAt": datetime,
        "lifecycleEvents": List[LifecycleEventTypeDef],
        "status": TargetStatusType,
        "resourceType": str,
        "targetVersionWeight": float,
    },
    total=False,
)

InstanceSummaryTypeDef = TypedDict(
    "InstanceSummaryTypeDef",
    {
        "deploymentId": str,
        "instanceId": str,
        "status": InstanceStatusType,
        "lastUpdatedAt": datetime,
        "lifecycleEvents": List[LifecycleEventTypeDef],
        "instanceType": InstanceTypeType,
    },
    total=False,
)

InstanceTargetTypeDef = TypedDict(
    "InstanceTargetTypeDef",
    {
        "deploymentId": str,
        "targetId": str,
        "targetArn": str,
        "status": TargetStatusType,
        "lastUpdatedAt": datetime,
        "lifecycleEvents": List[LifecycleEventTypeDef],
        "instanceLabel": TargetLabelType,
    },
    total=False,
)

LambdaTargetTypeDef = TypedDict(
    "LambdaTargetTypeDef",
    {
        "deploymentId": str,
        "targetId": str,
        "targetArn": str,
        "status": TargetStatusType,
        "lastUpdatedAt": datetime,
        "lifecycleEvents": List[LifecycleEventTypeDef],
        "lambdaFunctionInfo": LambdaFunctionInfoTypeDef,
    },
    total=False,
)

ECSTargetTypeDef = TypedDict(
    "ECSTargetTypeDef",
    {
        "deploymentId": str,
        "targetId": str,
        "targetArn": str,
        "lastUpdatedAt": datetime,
        "lifecycleEvents": List[LifecycleEventTypeDef],
        "status": TargetStatusType,
        "taskSetsInfo": List[ECSTaskSetTypeDef],
    },
    total=False,
)

BatchGetApplicationRevisionsInputRequestTypeDef = TypedDict(
    "BatchGetApplicationRevisionsInputRequestTypeDef",
    {
        "applicationName": str,
        "revisions": Sequence[RevisionLocationTypeDef],
    },
)

GetApplicationRevisionInputRequestTypeDef = TypedDict(
    "GetApplicationRevisionInputRequestTypeDef",
    {
        "applicationName": str,
        "revision": RevisionLocationTypeDef,
    },
)

GetApplicationRevisionOutputTypeDef = TypedDict(
    "GetApplicationRevisionOutputTypeDef",
    {
        "applicationName": str,
        "revision": RevisionLocationTypeDef,
        "revisionInfo": GenericRevisionInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationRevisionsOutputTypeDef = TypedDict(
    "ListApplicationRevisionsOutputTypeDef",
    {
        "revisions": List[RevisionLocationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRegisterApplicationRevisionInputRequestTypeDef = TypedDict(
    "_RequiredRegisterApplicationRevisionInputRequestTypeDef",
    {
        "applicationName": str,
        "revision": RevisionLocationTypeDef,
    },
)
_OptionalRegisterApplicationRevisionInputRequestTypeDef = TypedDict(
    "_OptionalRegisterApplicationRevisionInputRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class RegisterApplicationRevisionInputRequestTypeDef(
    _RequiredRegisterApplicationRevisionInputRequestTypeDef,
    _OptionalRegisterApplicationRevisionInputRequestTypeDef,
):
    pass


RevisionInfoTypeDef = TypedDict(
    "RevisionInfoTypeDef",
    {
        "revisionLocation": RevisionLocationTypeDef,
        "genericRevisionInfo": GenericRevisionInfoTypeDef,
    },
    total=False,
)

LoadBalancerInfoTypeDef = TypedDict(
    "LoadBalancerInfoTypeDef",
    {
        "elbInfoList": List[ELBInfoTypeDef],
        "targetGroupInfoList": List[TargetGroupInfoTypeDef],
        "targetGroupPairInfoList": List[TargetGroupPairInfoTypeDef],
    },
    total=False,
)

_RequiredCreateDeploymentConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentConfigInputRequestTypeDef",
    {
        "deploymentConfigName": str,
    },
)
_OptionalCreateDeploymentConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentConfigInputRequestTypeDef",
    {
        "minimumHealthyHosts": MinimumHealthyHostsTypeDef,
        "trafficRoutingConfig": TrafficRoutingConfigTypeDef,
        "computePlatform": ComputePlatformType,
    },
    total=False,
)


class CreateDeploymentConfigInputRequestTypeDef(
    _RequiredCreateDeploymentConfigInputRequestTypeDef,
    _OptionalCreateDeploymentConfigInputRequestTypeDef,
):
    pass


DeploymentConfigInfoTypeDef = TypedDict(
    "DeploymentConfigInfoTypeDef",
    {
        "deploymentConfigId": str,
        "deploymentConfigName": str,
        "minimumHealthyHosts": MinimumHealthyHostsTypeDef,
        "createTime": datetime,
        "computePlatform": ComputePlatformType,
        "trafficRoutingConfig": TrafficRoutingConfigTypeDef,
    },
    total=False,
)

_RequiredCreateDeploymentInputRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentInputRequestTypeDef",
    {
        "applicationName": str,
    },
)
_OptionalCreateDeploymentInputRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentInputRequestTypeDef",
    {
        "deploymentGroupName": str,
        "revision": RevisionLocationTypeDef,
        "deploymentConfigName": str,
        "description": str,
        "ignoreApplicationStopFailures": bool,
        "targetInstances": TargetInstancesTypeDef,
        "autoRollbackConfiguration": AutoRollbackConfigurationTypeDef,
        "updateOutdatedInstancesOnly": bool,
        "fileExistsBehavior": FileExistsBehaviorType,
    },
    total=False,
)


class CreateDeploymentInputRequestTypeDef(
    _RequiredCreateDeploymentInputRequestTypeDef, _OptionalCreateDeploymentInputRequestTypeDef
):
    pass


BatchGetDeploymentInstancesOutputTypeDef = TypedDict(
    "BatchGetDeploymentInstancesOutputTypeDef",
    {
        "instancesSummary": List[InstanceSummaryTypeDef],
        "errorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentInstanceOutputTypeDef = TypedDict(
    "GetDeploymentInstanceOutputTypeDef",
    {
        "instanceSummary": InstanceSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentTargetTypeDef = TypedDict(
    "DeploymentTargetTypeDef",
    {
        "deploymentTargetType": DeploymentTargetTypeType,
        "instanceTarget": InstanceTargetTypeDef,
        "lambdaTarget": LambdaTargetTypeDef,
        "ecsTarget": ECSTargetTypeDef,
        "cloudFormationTarget": CloudFormationTargetTypeDef,
    },
    total=False,
)

BatchGetApplicationRevisionsOutputTypeDef = TypedDict(
    "BatchGetApplicationRevisionsOutputTypeDef",
    {
        "applicationName": str,
        "errorMessage": str,
        "revisions": List[RevisionInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDeploymentGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentGroupInputRequestTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
        "serviceRoleArn": str,
    },
)
_OptionalCreateDeploymentGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentGroupInputRequestTypeDef",
    {
        "deploymentConfigName": str,
        "ec2TagFilters": Sequence[EC2TagFilterTypeDef],
        "onPremisesInstanceTagFilters": Sequence[TagFilterTypeDef],
        "autoScalingGroups": Sequence[str],
        "triggerConfigurations": Sequence[TriggerConfigTypeDef],
        "alarmConfiguration": AlarmConfigurationTypeDef,
        "autoRollbackConfiguration": AutoRollbackConfigurationTypeDef,
        "outdatedInstancesStrategy": OutdatedInstancesStrategyType,
        "deploymentStyle": DeploymentStyleTypeDef,
        "blueGreenDeploymentConfiguration": BlueGreenDeploymentConfigurationTypeDef,
        "loadBalancerInfo": LoadBalancerInfoTypeDef,
        "ec2TagSet": EC2TagSetTypeDef,
        "ecsServices": Sequence[ECSServiceTypeDef],
        "onPremisesTagSet": OnPremisesTagSetTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDeploymentGroupInputRequestTypeDef(
    _RequiredCreateDeploymentGroupInputRequestTypeDef,
    _OptionalCreateDeploymentGroupInputRequestTypeDef,
):
    pass


DeploymentGroupInfoTypeDef = TypedDict(
    "DeploymentGroupInfoTypeDef",
    {
        "applicationName": str,
        "deploymentGroupId": str,
        "deploymentGroupName": str,
        "deploymentConfigName": str,
        "ec2TagFilters": List[EC2TagFilterTypeDef],
        "onPremisesInstanceTagFilters": List[TagFilterTypeDef],
        "autoScalingGroups": List[AutoScalingGroupTypeDef],
        "serviceRoleArn": str,
        "targetRevision": RevisionLocationTypeDef,
        "triggerConfigurations": List[TriggerConfigTypeDef],
        "alarmConfiguration": AlarmConfigurationTypeDef,
        "autoRollbackConfiguration": AutoRollbackConfigurationTypeDef,
        "deploymentStyle": DeploymentStyleTypeDef,
        "outdatedInstancesStrategy": OutdatedInstancesStrategyType,
        "blueGreenDeploymentConfiguration": BlueGreenDeploymentConfigurationTypeDef,
        "loadBalancerInfo": LoadBalancerInfoTypeDef,
        "lastSuccessfulDeployment": LastDeploymentInfoTypeDef,
        "lastAttemptedDeployment": LastDeploymentInfoTypeDef,
        "ec2TagSet": EC2TagSetTypeDef,
        "onPremisesTagSet": OnPremisesTagSetTypeDef,
        "computePlatform": ComputePlatformType,
        "ecsServices": List[ECSServiceTypeDef],
    },
    total=False,
)

DeploymentInfoTypeDef = TypedDict(
    "DeploymentInfoTypeDef",
    {
        "applicationName": str,
        "deploymentGroupName": str,
        "deploymentConfigName": str,
        "deploymentId": str,
        "previousRevision": RevisionLocationTypeDef,
        "revision": RevisionLocationTypeDef,
        "status": DeploymentStatusType,
        "errorInformation": ErrorInformationTypeDef,
        "createTime": datetime,
        "startTime": datetime,
        "completeTime": datetime,
        "deploymentOverview": DeploymentOverviewTypeDef,
        "description": str,
        "creator": DeploymentCreatorType,
        "ignoreApplicationStopFailures": bool,
        "autoRollbackConfiguration": AutoRollbackConfigurationTypeDef,
        "updateOutdatedInstancesOnly": bool,
        "rollbackInfo": RollbackInfoTypeDef,
        "deploymentStyle": DeploymentStyleTypeDef,
        "targetInstances": TargetInstancesTypeDef,
        "instanceTerminationWaitTimeStarted": bool,
        "blueGreenDeploymentConfiguration": BlueGreenDeploymentConfigurationTypeDef,
        "loadBalancerInfo": LoadBalancerInfoTypeDef,
        "additionalDeploymentStatusInfo": str,
        "fileExistsBehavior": FileExistsBehaviorType,
        "deploymentStatusMessages": List[str],
        "computePlatform": ComputePlatformType,
        "externalId": str,
        "relatedDeployments": RelatedDeploymentsTypeDef,
    },
    total=False,
)

_RequiredUpdateDeploymentGroupInputRequestTypeDef = TypedDict(
    "_RequiredUpdateDeploymentGroupInputRequestTypeDef",
    {
        "applicationName": str,
        "currentDeploymentGroupName": str,
    },
)
_OptionalUpdateDeploymentGroupInputRequestTypeDef = TypedDict(
    "_OptionalUpdateDeploymentGroupInputRequestTypeDef",
    {
        "newDeploymentGroupName": str,
        "deploymentConfigName": str,
        "ec2TagFilters": Sequence[EC2TagFilterTypeDef],
        "onPremisesInstanceTagFilters": Sequence[TagFilterTypeDef],
        "autoScalingGroups": Sequence[str],
        "serviceRoleArn": str,
        "triggerConfigurations": Sequence[TriggerConfigTypeDef],
        "alarmConfiguration": AlarmConfigurationTypeDef,
        "autoRollbackConfiguration": AutoRollbackConfigurationTypeDef,
        "outdatedInstancesStrategy": OutdatedInstancesStrategyType,
        "deploymentStyle": DeploymentStyleTypeDef,
        "blueGreenDeploymentConfiguration": BlueGreenDeploymentConfigurationTypeDef,
        "loadBalancerInfo": LoadBalancerInfoTypeDef,
        "ec2TagSet": EC2TagSetTypeDef,
        "ecsServices": Sequence[ECSServiceTypeDef],
        "onPremisesTagSet": OnPremisesTagSetTypeDef,
    },
    total=False,
)


class UpdateDeploymentGroupInputRequestTypeDef(
    _RequiredUpdateDeploymentGroupInputRequestTypeDef,
    _OptionalUpdateDeploymentGroupInputRequestTypeDef,
):
    pass


GetDeploymentConfigOutputTypeDef = TypedDict(
    "GetDeploymentConfigOutputTypeDef",
    {
        "deploymentConfigInfo": DeploymentConfigInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetDeploymentTargetsOutputTypeDef = TypedDict(
    "BatchGetDeploymentTargetsOutputTypeDef",
    {
        "deploymentTargets": List[DeploymentTargetTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentTargetOutputTypeDef = TypedDict(
    "GetDeploymentTargetOutputTypeDef",
    {
        "deploymentTarget": DeploymentTargetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetDeploymentGroupsOutputTypeDef = TypedDict(
    "BatchGetDeploymentGroupsOutputTypeDef",
    {
        "deploymentGroupsInfo": List[DeploymentGroupInfoTypeDef],
        "errorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentGroupOutputTypeDef = TypedDict(
    "GetDeploymentGroupOutputTypeDef",
    {
        "deploymentGroupInfo": DeploymentGroupInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetDeploymentsOutputTypeDef = TypedDict(
    "BatchGetDeploymentsOutputTypeDef",
    {
        "deploymentsInfo": List[DeploymentInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentOutputTypeDef = TypedDict(
    "GetDeploymentOutputTypeDef",
    {
        "deploymentInfo": DeploymentInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
