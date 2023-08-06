"""
Type annotations for batch service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_batch/type_defs/)

Usage::

    ```python
    from mypy_boto3_batch.type_defs import ArrayPropertiesDetailTypeDef

    data: ArrayPropertiesDetailTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ArrayJobDependencyType,
    AssignPublicIpType,
    CEStateType,
    CEStatusType,
    CETypeType,
    CRAllocationStrategyType,
    CRTypeType,
    CRUpdateAllocationStrategyType,
    DeviceCgroupPermissionType,
    EFSAuthorizationConfigIAMType,
    EFSTransitEncryptionType,
    JobDefinitionTypeType,
    JobStatusType,
    JQStateType,
    JQStatusType,
    LogDriverType,
    PlatformCapabilityType,
    ResourceTypeType,
    RetryActionType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ArrayPropertiesDetailTypeDef",
    "ArrayPropertiesSummaryTypeDef",
    "ArrayPropertiesTypeDef",
    "NetworkInterfaceTypeDef",
    "CancelJobRequestRequestTypeDef",
    "UpdatePolicyTypeDef",
    "ComputeEnvironmentOrderTypeDef",
    "Ec2ConfigurationTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "FargatePlatformConfigurationTypeDef",
    "KeyValuePairTypeDef",
    "MountPointTypeDef",
    "NetworkConfigurationTypeDef",
    "ResourceRequirementTypeDef",
    "SecretTypeDef",
    "UlimitTypeDef",
    "ContainerSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteComputeEnvironmentRequestRequestTypeDef",
    "DeleteJobQueueRequestRequestTypeDef",
    "DeleteSchedulingPolicyRequestRequestTypeDef",
    "DeregisterJobDefinitionRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeComputeEnvironmentsRequestRequestTypeDef",
    "DescribeJobDefinitionsRequestRequestTypeDef",
    "DescribeJobQueuesRequestRequestTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeSchedulingPoliciesRequestRequestTypeDef",
    "DeviceTypeDef",
    "EFSAuthorizationConfigTypeDef",
    "EvaluateOnExitTypeDef",
    "ShareAttributesTypeDef",
    "HostTypeDef",
    "JobTimeoutTypeDef",
    "JobDependencyTypeDef",
    "NodeDetailsTypeDef",
    "NodePropertiesSummaryTypeDef",
    "KeyValuesPairTypeDef",
    "TmpfsTypeDef",
    "ListSchedulingPoliciesRequestRequestTypeDef",
    "SchedulingPolicyListingDetailTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TerminateJobRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AttemptContainerDetailTypeDef",
    "CreateJobQueueRequestRequestTypeDef",
    "JobQueueDetailTypeDef",
    "UpdateJobQueueRequestRequestTypeDef",
    "ComputeResourceTypeDef",
    "ComputeResourceUpdateTypeDef",
    "ContainerOverridesTypeDef",
    "LogConfigurationTypeDef",
    "CreateComputeEnvironmentResponseTypeDef",
    "CreateJobQueueResponseTypeDef",
    "CreateSchedulingPolicyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RegisterJobDefinitionResponseTypeDef",
    "SubmitJobResponseTypeDef",
    "UpdateComputeEnvironmentResponseTypeDef",
    "UpdateJobQueueResponseTypeDef",
    "DescribeComputeEnvironmentsRequestDescribeComputeEnvironmentsPaginateTypeDef",
    "DescribeJobDefinitionsRequestDescribeJobDefinitionsPaginateTypeDef",
    "DescribeJobQueuesRequestDescribeJobQueuesPaginateTypeDef",
    "ListSchedulingPoliciesRequestListSchedulingPoliciesPaginateTypeDef",
    "EFSVolumeConfigurationTypeDef",
    "RetryStrategyTypeDef",
    "FairsharePolicyTypeDef",
    "JobSummaryTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "LinuxParametersTypeDef",
    "ListSchedulingPoliciesResponseTypeDef",
    "AttemptDetailTypeDef",
    "DescribeJobQueuesResponseTypeDef",
    "ComputeEnvironmentDetailTypeDef",
    "CreateComputeEnvironmentRequestRequestTypeDef",
    "UpdateComputeEnvironmentRequestRequestTypeDef",
    "NodePropertyOverrideTypeDef",
    "VolumeTypeDef",
    "CreateSchedulingPolicyRequestRequestTypeDef",
    "SchedulingPolicyDetailTypeDef",
    "UpdateSchedulingPolicyRequestRequestTypeDef",
    "ListJobsResponseTypeDef",
    "DescribeComputeEnvironmentsResponseTypeDef",
    "NodeOverridesTypeDef",
    "ContainerDetailTypeDef",
    "ContainerPropertiesTypeDef",
    "DescribeSchedulingPoliciesResponseTypeDef",
    "SubmitJobRequestRequestTypeDef",
    "NodeRangePropertyTypeDef",
    "NodePropertiesTypeDef",
    "JobDefinitionTypeDef",
    "JobDetailTypeDef",
    "RegisterJobDefinitionRequestRequestTypeDef",
    "DescribeJobDefinitionsResponseTypeDef",
    "DescribeJobsResponseTypeDef",
)

ArrayPropertiesDetailTypeDef = TypedDict(
    "ArrayPropertiesDetailTypeDef",
    {
        "statusSummary": Dict[str, int],
        "size": int,
        "index": int,
    },
    total=False,
)

ArrayPropertiesSummaryTypeDef = TypedDict(
    "ArrayPropertiesSummaryTypeDef",
    {
        "size": int,
        "index": int,
    },
    total=False,
)

ArrayPropertiesTypeDef = TypedDict(
    "ArrayPropertiesTypeDef",
    {
        "size": int,
    },
    total=False,
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "attachmentId": str,
        "ipv6Address": str,
        "privateIpv4Address": str,
    },
    total=False,
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "jobId": str,
        "reason": str,
    },
)

UpdatePolicyTypeDef = TypedDict(
    "UpdatePolicyTypeDef",
    {
        "terminateJobsOnUpdate": bool,
        "jobExecutionTimeoutMinutes": int,
    },
    total=False,
)

ComputeEnvironmentOrderTypeDef = TypedDict(
    "ComputeEnvironmentOrderTypeDef",
    {
        "order": int,
        "computeEnvironment": str,
    },
)

_RequiredEc2ConfigurationTypeDef = TypedDict(
    "_RequiredEc2ConfigurationTypeDef",
    {
        "imageType": str,
    },
)
_OptionalEc2ConfigurationTypeDef = TypedDict(
    "_OptionalEc2ConfigurationTypeDef",
    {
        "imageIdOverride": str,
    },
    total=False,
)


class Ec2ConfigurationTypeDef(_RequiredEc2ConfigurationTypeDef, _OptionalEc2ConfigurationTypeDef):
    pass


LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "launchTemplateId": str,
        "launchTemplateName": str,
        "version": str,
    },
    total=False,
)

FargatePlatformConfigurationTypeDef = TypedDict(
    "FargatePlatformConfigurationTypeDef",
    {
        "platformVersion": str,
    },
    total=False,
)

KeyValuePairTypeDef = TypedDict(
    "KeyValuePairTypeDef",
    {
        "name": str,
        "value": str,
    },
    total=False,
)

MountPointTypeDef = TypedDict(
    "MountPointTypeDef",
    {
        "containerPath": str,
        "readOnly": bool,
        "sourceVolume": str,
    },
    total=False,
)

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "assignPublicIp": AssignPublicIpType,
    },
    total=False,
)

ResourceRequirementTypeDef = TypedDict(
    "ResourceRequirementTypeDef",
    {
        "value": str,
        "type": ResourceTypeType,
    },
)

SecretTypeDef = TypedDict(
    "SecretTypeDef",
    {
        "name": str,
        "valueFrom": str,
    },
)

UlimitTypeDef = TypedDict(
    "UlimitTypeDef",
    {
        "hardLimit": int,
        "name": str,
        "softLimit": int,
    },
)

ContainerSummaryTypeDef = TypedDict(
    "ContainerSummaryTypeDef",
    {
        "exitCode": int,
        "reason": str,
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

DeleteComputeEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteComputeEnvironmentRequestRequestTypeDef",
    {
        "computeEnvironment": str,
    },
)

DeleteJobQueueRequestRequestTypeDef = TypedDict(
    "DeleteJobQueueRequestRequestTypeDef",
    {
        "jobQueue": str,
    },
)

DeleteSchedulingPolicyRequestRequestTypeDef = TypedDict(
    "DeleteSchedulingPolicyRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeregisterJobDefinitionRequestRequestTypeDef = TypedDict(
    "DeregisterJobDefinitionRequestRequestTypeDef",
    {
        "jobDefinition": str,
    },
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

DescribeComputeEnvironmentsRequestRequestTypeDef = TypedDict(
    "DescribeComputeEnvironmentsRequestRequestTypeDef",
    {
        "computeEnvironments": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeJobDefinitionsRequestRequestTypeDef = TypedDict(
    "DescribeJobDefinitionsRequestRequestTypeDef",
    {
        "jobDefinitions": Sequence[str],
        "maxResults": int,
        "jobDefinitionName": str,
        "status": str,
        "nextToken": str,
    },
    total=False,
)

DescribeJobQueuesRequestRequestTypeDef = TypedDict(
    "DescribeJobQueuesRequestRequestTypeDef",
    {
        "jobQueues": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeJobsRequestRequestTypeDef = TypedDict(
    "DescribeJobsRequestRequestTypeDef",
    {
        "jobs": Sequence[str],
    },
)

DescribeSchedulingPoliciesRequestRequestTypeDef = TypedDict(
    "DescribeSchedulingPoliciesRequestRequestTypeDef",
    {
        "arns": Sequence[str],
    },
)

_RequiredDeviceTypeDef = TypedDict(
    "_RequiredDeviceTypeDef",
    {
        "hostPath": str,
    },
)
_OptionalDeviceTypeDef = TypedDict(
    "_OptionalDeviceTypeDef",
    {
        "containerPath": str,
        "permissions": List[DeviceCgroupPermissionType],
    },
    total=False,
)


class DeviceTypeDef(_RequiredDeviceTypeDef, _OptionalDeviceTypeDef):
    pass


EFSAuthorizationConfigTypeDef = TypedDict(
    "EFSAuthorizationConfigTypeDef",
    {
        "accessPointId": str,
        "iam": EFSAuthorizationConfigIAMType,
    },
    total=False,
)

_RequiredEvaluateOnExitTypeDef = TypedDict(
    "_RequiredEvaluateOnExitTypeDef",
    {
        "action": RetryActionType,
    },
)
_OptionalEvaluateOnExitTypeDef = TypedDict(
    "_OptionalEvaluateOnExitTypeDef",
    {
        "onStatusReason": str,
        "onReason": str,
        "onExitCode": str,
    },
    total=False,
)


class EvaluateOnExitTypeDef(_RequiredEvaluateOnExitTypeDef, _OptionalEvaluateOnExitTypeDef):
    pass


_RequiredShareAttributesTypeDef = TypedDict(
    "_RequiredShareAttributesTypeDef",
    {
        "shareIdentifier": str,
    },
)
_OptionalShareAttributesTypeDef = TypedDict(
    "_OptionalShareAttributesTypeDef",
    {
        "weightFactor": float,
    },
    total=False,
)


class ShareAttributesTypeDef(_RequiredShareAttributesTypeDef, _OptionalShareAttributesTypeDef):
    pass


HostTypeDef = TypedDict(
    "HostTypeDef",
    {
        "sourcePath": str,
    },
    total=False,
)

JobTimeoutTypeDef = TypedDict(
    "JobTimeoutTypeDef",
    {
        "attemptDurationSeconds": int,
    },
    total=False,
)

JobDependencyTypeDef = TypedDict(
    "JobDependencyTypeDef",
    {
        "jobId": str,
        "type": ArrayJobDependencyType,
    },
    total=False,
)

NodeDetailsTypeDef = TypedDict(
    "NodeDetailsTypeDef",
    {
        "nodeIndex": int,
        "isMainNode": bool,
    },
    total=False,
)

NodePropertiesSummaryTypeDef = TypedDict(
    "NodePropertiesSummaryTypeDef",
    {
        "isMainNode": bool,
        "numNodes": int,
        "nodeIndex": int,
    },
    total=False,
)

KeyValuesPairTypeDef = TypedDict(
    "KeyValuesPairTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
    total=False,
)

_RequiredTmpfsTypeDef = TypedDict(
    "_RequiredTmpfsTypeDef",
    {
        "containerPath": str,
        "size": int,
    },
)
_OptionalTmpfsTypeDef = TypedDict(
    "_OptionalTmpfsTypeDef",
    {
        "mountOptions": List[str],
    },
    total=False,
)


class TmpfsTypeDef(_RequiredTmpfsTypeDef, _OptionalTmpfsTypeDef):
    pass


ListSchedulingPoliciesRequestRequestTypeDef = TypedDict(
    "ListSchedulingPoliciesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SchedulingPolicyListingDetailTypeDef = TypedDict(
    "SchedulingPolicyListingDetailTypeDef",
    {
        "arn": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TerminateJobRequestRequestTypeDef = TypedDict(
    "TerminateJobRequestRequestTypeDef",
    {
        "jobId": str,
        "reason": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AttemptContainerDetailTypeDef = TypedDict(
    "AttemptContainerDetailTypeDef",
    {
        "containerInstanceArn": str,
        "taskArn": str,
        "exitCode": int,
        "reason": str,
        "logStreamName": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
    },
    total=False,
)

_RequiredCreateJobQueueRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobQueueRequestRequestTypeDef",
    {
        "jobQueueName": str,
        "priority": int,
        "computeEnvironmentOrder": Sequence[ComputeEnvironmentOrderTypeDef],
    },
)
_OptionalCreateJobQueueRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobQueueRequestRequestTypeDef",
    {
        "state": JQStateType,
        "schedulingPolicyArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateJobQueueRequestRequestTypeDef(
    _RequiredCreateJobQueueRequestRequestTypeDef, _OptionalCreateJobQueueRequestRequestTypeDef
):
    pass


_RequiredJobQueueDetailTypeDef = TypedDict(
    "_RequiredJobQueueDetailTypeDef",
    {
        "jobQueueName": str,
        "jobQueueArn": str,
        "state": JQStateType,
        "priority": int,
        "computeEnvironmentOrder": List[ComputeEnvironmentOrderTypeDef],
    },
)
_OptionalJobQueueDetailTypeDef = TypedDict(
    "_OptionalJobQueueDetailTypeDef",
    {
        "schedulingPolicyArn": str,
        "status": JQStatusType,
        "statusReason": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class JobQueueDetailTypeDef(_RequiredJobQueueDetailTypeDef, _OptionalJobQueueDetailTypeDef):
    pass


_RequiredUpdateJobQueueRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobQueueRequestRequestTypeDef",
    {
        "jobQueue": str,
    },
)
_OptionalUpdateJobQueueRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobQueueRequestRequestTypeDef",
    {
        "state": JQStateType,
        "schedulingPolicyArn": str,
        "priority": int,
        "computeEnvironmentOrder": Sequence[ComputeEnvironmentOrderTypeDef],
    },
    total=False,
)


class UpdateJobQueueRequestRequestTypeDef(
    _RequiredUpdateJobQueueRequestRequestTypeDef, _OptionalUpdateJobQueueRequestRequestTypeDef
):
    pass


_RequiredComputeResourceTypeDef = TypedDict(
    "_RequiredComputeResourceTypeDef",
    {
        "type": CRTypeType,
        "maxvCpus": int,
        "subnets": Sequence[str],
    },
)
_OptionalComputeResourceTypeDef = TypedDict(
    "_OptionalComputeResourceTypeDef",
    {
        "allocationStrategy": CRAllocationStrategyType,
        "minvCpus": int,
        "desiredvCpus": int,
        "instanceTypes": Sequence[str],
        "imageId": str,
        "securityGroupIds": Sequence[str],
        "ec2KeyPair": str,
        "instanceRole": str,
        "tags": Mapping[str, str],
        "placementGroup": str,
        "bidPercentage": int,
        "spotIamFleetRole": str,
        "launchTemplate": LaunchTemplateSpecificationTypeDef,
        "ec2Configuration": Sequence[Ec2ConfigurationTypeDef],
    },
    total=False,
)


class ComputeResourceTypeDef(_RequiredComputeResourceTypeDef, _OptionalComputeResourceTypeDef):
    pass


ComputeResourceUpdateTypeDef = TypedDict(
    "ComputeResourceUpdateTypeDef",
    {
        "minvCpus": int,
        "maxvCpus": int,
        "desiredvCpus": int,
        "subnets": Sequence[str],
        "securityGroupIds": Sequence[str],
        "allocationStrategy": CRUpdateAllocationStrategyType,
        "instanceTypes": Sequence[str],
        "ec2KeyPair": str,
        "instanceRole": str,
        "tags": Mapping[str, str],
        "placementGroup": str,
        "bidPercentage": int,
        "launchTemplate": LaunchTemplateSpecificationTypeDef,
        "ec2Configuration": Sequence[Ec2ConfigurationTypeDef],
        "updateToLatestImageVersion": bool,
        "type": CRTypeType,
        "imageId": str,
    },
    total=False,
)

ContainerOverridesTypeDef = TypedDict(
    "ContainerOverridesTypeDef",
    {
        "vcpus": int,
        "memory": int,
        "command": Sequence[str],
        "instanceType": str,
        "environment": Sequence[KeyValuePairTypeDef],
        "resourceRequirements": Sequence[ResourceRequirementTypeDef],
    },
    total=False,
)

_RequiredLogConfigurationTypeDef = TypedDict(
    "_RequiredLogConfigurationTypeDef",
    {
        "logDriver": LogDriverType,
    },
)
_OptionalLogConfigurationTypeDef = TypedDict(
    "_OptionalLogConfigurationTypeDef",
    {
        "options": Dict[str, str],
        "secretOptions": List[SecretTypeDef],
    },
    total=False,
)


class LogConfigurationTypeDef(_RequiredLogConfigurationTypeDef, _OptionalLogConfigurationTypeDef):
    pass


CreateComputeEnvironmentResponseTypeDef = TypedDict(
    "CreateComputeEnvironmentResponseTypeDef",
    {
        "computeEnvironmentName": str,
        "computeEnvironmentArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobQueueResponseTypeDef = TypedDict(
    "CreateJobQueueResponseTypeDef",
    {
        "jobQueueName": str,
        "jobQueueArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSchedulingPolicyResponseTypeDef = TypedDict(
    "CreateSchedulingPolicyResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterJobDefinitionResponseTypeDef = TypedDict(
    "RegisterJobDefinitionResponseTypeDef",
    {
        "jobDefinitionName": str,
        "jobDefinitionArn": str,
        "revision": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubmitJobResponseTypeDef = TypedDict(
    "SubmitJobResponseTypeDef",
    {
        "jobArn": str,
        "jobName": str,
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateComputeEnvironmentResponseTypeDef = TypedDict(
    "UpdateComputeEnvironmentResponseTypeDef",
    {
        "computeEnvironmentName": str,
        "computeEnvironmentArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobQueueResponseTypeDef = TypedDict(
    "UpdateJobQueueResponseTypeDef",
    {
        "jobQueueName": str,
        "jobQueueArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeComputeEnvironmentsRequestDescribeComputeEnvironmentsPaginateTypeDef = TypedDict(
    "DescribeComputeEnvironmentsRequestDescribeComputeEnvironmentsPaginateTypeDef",
    {
        "computeEnvironments": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobDefinitionsRequestDescribeJobDefinitionsPaginateTypeDef = TypedDict(
    "DescribeJobDefinitionsRequestDescribeJobDefinitionsPaginateTypeDef",
    {
        "jobDefinitions": Sequence[str],
        "jobDefinitionName": str,
        "status": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobQueuesRequestDescribeJobQueuesPaginateTypeDef = TypedDict(
    "DescribeJobQueuesRequestDescribeJobQueuesPaginateTypeDef",
    {
        "jobQueues": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSchedulingPoliciesRequestListSchedulingPoliciesPaginateTypeDef = TypedDict(
    "ListSchedulingPoliciesRequestListSchedulingPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredEFSVolumeConfigurationTypeDef = TypedDict(
    "_RequiredEFSVolumeConfigurationTypeDef",
    {
        "fileSystemId": str,
    },
)
_OptionalEFSVolumeConfigurationTypeDef = TypedDict(
    "_OptionalEFSVolumeConfigurationTypeDef",
    {
        "rootDirectory": str,
        "transitEncryption": EFSTransitEncryptionType,
        "transitEncryptionPort": int,
        "authorizationConfig": EFSAuthorizationConfigTypeDef,
    },
    total=False,
)


class EFSVolumeConfigurationTypeDef(
    _RequiredEFSVolumeConfigurationTypeDef, _OptionalEFSVolumeConfigurationTypeDef
):
    pass


RetryStrategyTypeDef = TypedDict(
    "RetryStrategyTypeDef",
    {
        "attempts": int,
        "evaluateOnExit": List[EvaluateOnExitTypeDef],
    },
    total=False,
)

FairsharePolicyTypeDef = TypedDict(
    "FairsharePolicyTypeDef",
    {
        "shareDecaySeconds": int,
        "computeReservation": int,
        "shareDistribution": Sequence[ShareAttributesTypeDef],
    },
    total=False,
)

_RequiredJobSummaryTypeDef = TypedDict(
    "_RequiredJobSummaryTypeDef",
    {
        "jobId": str,
        "jobName": str,
    },
)
_OptionalJobSummaryTypeDef = TypedDict(
    "_OptionalJobSummaryTypeDef",
    {
        "jobArn": str,
        "createdAt": int,
        "status": JobStatusType,
        "statusReason": str,
        "startedAt": int,
        "stoppedAt": int,
        "container": ContainerSummaryTypeDef,
        "arrayProperties": ArrayPropertiesSummaryTypeDef,
        "nodeProperties": NodePropertiesSummaryTypeDef,
        "jobDefinition": str,
    },
    total=False,
)


class JobSummaryTypeDef(_RequiredJobSummaryTypeDef, _OptionalJobSummaryTypeDef):
    pass


ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "jobQueue": str,
        "arrayJobId": str,
        "multiNodeJobId": str,
        "jobStatus": JobStatusType,
        "filters": Sequence[KeyValuesPairTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "jobQueue": str,
        "arrayJobId": str,
        "multiNodeJobId": str,
        "jobStatus": JobStatusType,
        "maxResults": int,
        "nextToken": str,
        "filters": Sequence[KeyValuesPairTypeDef],
    },
    total=False,
)

LinuxParametersTypeDef = TypedDict(
    "LinuxParametersTypeDef",
    {
        "devices": List[DeviceTypeDef],
        "initProcessEnabled": bool,
        "sharedMemorySize": int,
        "tmpfs": List[TmpfsTypeDef],
        "maxSwap": int,
        "swappiness": int,
    },
    total=False,
)

ListSchedulingPoliciesResponseTypeDef = TypedDict(
    "ListSchedulingPoliciesResponseTypeDef",
    {
        "schedulingPolicies": List[SchedulingPolicyListingDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AttemptDetailTypeDef = TypedDict(
    "AttemptDetailTypeDef",
    {
        "container": AttemptContainerDetailTypeDef,
        "startedAt": int,
        "stoppedAt": int,
        "statusReason": str,
    },
    total=False,
)

DescribeJobQueuesResponseTypeDef = TypedDict(
    "DescribeJobQueuesResponseTypeDef",
    {
        "jobQueues": List[JobQueueDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredComputeEnvironmentDetailTypeDef = TypedDict(
    "_RequiredComputeEnvironmentDetailTypeDef",
    {
        "computeEnvironmentName": str,
        "computeEnvironmentArn": str,
    },
)
_OptionalComputeEnvironmentDetailTypeDef = TypedDict(
    "_OptionalComputeEnvironmentDetailTypeDef",
    {
        "unmanagedvCpus": int,
        "ecsClusterArn": str,
        "tags": Dict[str, str],
        "type": CETypeType,
        "state": CEStateType,
        "status": CEStatusType,
        "statusReason": str,
        "computeResources": ComputeResourceTypeDef,
        "serviceRole": str,
        "updatePolicy": UpdatePolicyTypeDef,
    },
    total=False,
)


class ComputeEnvironmentDetailTypeDef(
    _RequiredComputeEnvironmentDetailTypeDef, _OptionalComputeEnvironmentDetailTypeDef
):
    pass


_RequiredCreateComputeEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateComputeEnvironmentRequestRequestTypeDef",
    {
        "computeEnvironmentName": str,
        "type": CETypeType,
    },
)
_OptionalCreateComputeEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateComputeEnvironmentRequestRequestTypeDef",
    {
        "state": CEStateType,
        "unmanagedvCpus": int,
        "computeResources": ComputeResourceTypeDef,
        "serviceRole": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateComputeEnvironmentRequestRequestTypeDef(
    _RequiredCreateComputeEnvironmentRequestRequestTypeDef,
    _OptionalCreateComputeEnvironmentRequestRequestTypeDef,
):
    pass


_RequiredUpdateComputeEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateComputeEnvironmentRequestRequestTypeDef",
    {
        "computeEnvironment": str,
    },
)
_OptionalUpdateComputeEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateComputeEnvironmentRequestRequestTypeDef",
    {
        "state": CEStateType,
        "unmanagedvCpus": int,
        "computeResources": ComputeResourceUpdateTypeDef,
        "serviceRole": str,
        "updatePolicy": UpdatePolicyTypeDef,
    },
    total=False,
)


class UpdateComputeEnvironmentRequestRequestTypeDef(
    _RequiredUpdateComputeEnvironmentRequestRequestTypeDef,
    _OptionalUpdateComputeEnvironmentRequestRequestTypeDef,
):
    pass


_RequiredNodePropertyOverrideTypeDef = TypedDict(
    "_RequiredNodePropertyOverrideTypeDef",
    {
        "targetNodes": str,
    },
)
_OptionalNodePropertyOverrideTypeDef = TypedDict(
    "_OptionalNodePropertyOverrideTypeDef",
    {
        "containerOverrides": ContainerOverridesTypeDef,
    },
    total=False,
)


class NodePropertyOverrideTypeDef(
    _RequiredNodePropertyOverrideTypeDef, _OptionalNodePropertyOverrideTypeDef
):
    pass


VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "host": HostTypeDef,
        "name": str,
        "efsVolumeConfiguration": EFSVolumeConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateSchedulingPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSchedulingPolicyRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateSchedulingPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSchedulingPolicyRequestRequestTypeDef",
    {
        "fairsharePolicy": FairsharePolicyTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateSchedulingPolicyRequestRequestTypeDef(
    _RequiredCreateSchedulingPolicyRequestRequestTypeDef,
    _OptionalCreateSchedulingPolicyRequestRequestTypeDef,
):
    pass


_RequiredSchedulingPolicyDetailTypeDef = TypedDict(
    "_RequiredSchedulingPolicyDetailTypeDef",
    {
        "name": str,
        "arn": str,
    },
)
_OptionalSchedulingPolicyDetailTypeDef = TypedDict(
    "_OptionalSchedulingPolicyDetailTypeDef",
    {
        "fairsharePolicy": FairsharePolicyTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)


class SchedulingPolicyDetailTypeDef(
    _RequiredSchedulingPolicyDetailTypeDef, _OptionalSchedulingPolicyDetailTypeDef
):
    pass


_RequiredUpdateSchedulingPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSchedulingPolicyRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateSchedulingPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSchedulingPolicyRequestRequestTypeDef",
    {
        "fairsharePolicy": FairsharePolicyTypeDef,
    },
    total=False,
)


class UpdateSchedulingPolicyRequestRequestTypeDef(
    _RequiredUpdateSchedulingPolicyRequestRequestTypeDef,
    _OptionalUpdateSchedulingPolicyRequestRequestTypeDef,
):
    pass


ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "jobSummaryList": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeComputeEnvironmentsResponseTypeDef = TypedDict(
    "DescribeComputeEnvironmentsResponseTypeDef",
    {
        "computeEnvironments": List[ComputeEnvironmentDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NodeOverridesTypeDef = TypedDict(
    "NodeOverridesTypeDef",
    {
        "numNodes": int,
        "nodePropertyOverrides": Sequence[NodePropertyOverrideTypeDef],
    },
    total=False,
)

ContainerDetailTypeDef = TypedDict(
    "ContainerDetailTypeDef",
    {
        "image": str,
        "vcpus": int,
        "memory": int,
        "command": List[str],
        "jobRoleArn": str,
        "executionRoleArn": str,
        "volumes": List[VolumeTypeDef],
        "environment": List[KeyValuePairTypeDef],
        "mountPoints": List[MountPointTypeDef],
        "readonlyRootFilesystem": bool,
        "ulimits": List[UlimitTypeDef],
        "privileged": bool,
        "user": str,
        "exitCode": int,
        "reason": str,
        "containerInstanceArn": str,
        "taskArn": str,
        "logStreamName": str,
        "instanceType": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "resourceRequirements": List[ResourceRequirementTypeDef],
        "linuxParameters": LinuxParametersTypeDef,
        "logConfiguration": LogConfigurationTypeDef,
        "secrets": List[SecretTypeDef],
        "networkConfiguration": NetworkConfigurationTypeDef,
        "fargatePlatformConfiguration": FargatePlatformConfigurationTypeDef,
    },
    total=False,
)

ContainerPropertiesTypeDef = TypedDict(
    "ContainerPropertiesTypeDef",
    {
        "image": str,
        "vcpus": int,
        "memory": int,
        "command": List[str],
        "jobRoleArn": str,
        "executionRoleArn": str,
        "volumes": List[VolumeTypeDef],
        "environment": List[KeyValuePairTypeDef],
        "mountPoints": List[MountPointTypeDef],
        "readonlyRootFilesystem": bool,
        "privileged": bool,
        "ulimits": List[UlimitTypeDef],
        "user": str,
        "instanceType": str,
        "resourceRequirements": List[ResourceRequirementTypeDef],
        "linuxParameters": LinuxParametersTypeDef,
        "logConfiguration": LogConfigurationTypeDef,
        "secrets": List[SecretTypeDef],
        "networkConfiguration": NetworkConfigurationTypeDef,
        "fargatePlatformConfiguration": FargatePlatformConfigurationTypeDef,
    },
    total=False,
)

DescribeSchedulingPoliciesResponseTypeDef = TypedDict(
    "DescribeSchedulingPoliciesResponseTypeDef",
    {
        "schedulingPolicies": List[SchedulingPolicyDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSubmitJobRequestRequestTypeDef = TypedDict(
    "_RequiredSubmitJobRequestRequestTypeDef",
    {
        "jobName": str,
        "jobQueue": str,
        "jobDefinition": str,
    },
)
_OptionalSubmitJobRequestRequestTypeDef = TypedDict(
    "_OptionalSubmitJobRequestRequestTypeDef",
    {
        "shareIdentifier": str,
        "schedulingPriorityOverride": int,
        "arrayProperties": ArrayPropertiesTypeDef,
        "dependsOn": Sequence[JobDependencyTypeDef],
        "parameters": Mapping[str, str],
        "containerOverrides": ContainerOverridesTypeDef,
        "nodeOverrides": NodeOverridesTypeDef,
        "retryStrategy": RetryStrategyTypeDef,
        "propagateTags": bool,
        "timeout": JobTimeoutTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class SubmitJobRequestRequestTypeDef(
    _RequiredSubmitJobRequestRequestTypeDef, _OptionalSubmitJobRequestRequestTypeDef
):
    pass


_RequiredNodeRangePropertyTypeDef = TypedDict(
    "_RequiredNodeRangePropertyTypeDef",
    {
        "targetNodes": str,
    },
)
_OptionalNodeRangePropertyTypeDef = TypedDict(
    "_OptionalNodeRangePropertyTypeDef",
    {
        "container": ContainerPropertiesTypeDef,
    },
    total=False,
)


class NodeRangePropertyTypeDef(
    _RequiredNodeRangePropertyTypeDef, _OptionalNodeRangePropertyTypeDef
):
    pass


NodePropertiesTypeDef = TypedDict(
    "NodePropertiesTypeDef",
    {
        "numNodes": int,
        "mainNode": int,
        "nodeRangeProperties": List[NodeRangePropertyTypeDef],
    },
)

_RequiredJobDefinitionTypeDef = TypedDict(
    "_RequiredJobDefinitionTypeDef",
    {
        "jobDefinitionName": str,
        "jobDefinitionArn": str,
        "revision": int,
        "type": str,
    },
)
_OptionalJobDefinitionTypeDef = TypedDict(
    "_OptionalJobDefinitionTypeDef",
    {
        "status": str,
        "schedulingPriority": int,
        "parameters": Dict[str, str],
        "retryStrategy": RetryStrategyTypeDef,
        "containerProperties": ContainerPropertiesTypeDef,
        "timeout": JobTimeoutTypeDef,
        "nodeProperties": NodePropertiesTypeDef,
        "tags": Dict[str, str],
        "propagateTags": bool,
        "platformCapabilities": List[PlatformCapabilityType],
    },
    total=False,
)


class JobDefinitionTypeDef(_RequiredJobDefinitionTypeDef, _OptionalJobDefinitionTypeDef):
    pass


_RequiredJobDetailTypeDef = TypedDict(
    "_RequiredJobDetailTypeDef",
    {
        "jobName": str,
        "jobId": str,
        "jobQueue": str,
        "status": JobStatusType,
        "startedAt": int,
        "jobDefinition": str,
    },
)
_OptionalJobDetailTypeDef = TypedDict(
    "_OptionalJobDetailTypeDef",
    {
        "jobArn": str,
        "shareIdentifier": str,
        "schedulingPriority": int,
        "attempts": List[AttemptDetailTypeDef],
        "statusReason": str,
        "createdAt": int,
        "retryStrategy": RetryStrategyTypeDef,
        "stoppedAt": int,
        "dependsOn": List[JobDependencyTypeDef],
        "parameters": Dict[str, str],
        "container": ContainerDetailTypeDef,
        "nodeDetails": NodeDetailsTypeDef,
        "nodeProperties": NodePropertiesTypeDef,
        "arrayProperties": ArrayPropertiesDetailTypeDef,
        "timeout": JobTimeoutTypeDef,
        "tags": Dict[str, str],
        "propagateTags": bool,
        "platformCapabilities": List[PlatformCapabilityType],
    },
    total=False,
)


class JobDetailTypeDef(_RequiredJobDetailTypeDef, _OptionalJobDetailTypeDef):
    pass


_RequiredRegisterJobDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterJobDefinitionRequestRequestTypeDef",
    {
        "jobDefinitionName": str,
        "type": JobDefinitionTypeType,
    },
)
_OptionalRegisterJobDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterJobDefinitionRequestRequestTypeDef",
    {
        "parameters": Mapping[str, str],
        "schedulingPriority": int,
        "containerProperties": ContainerPropertiesTypeDef,
        "nodeProperties": NodePropertiesTypeDef,
        "retryStrategy": RetryStrategyTypeDef,
        "propagateTags": bool,
        "timeout": JobTimeoutTypeDef,
        "tags": Mapping[str, str],
        "platformCapabilities": Sequence[PlatformCapabilityType],
    },
    total=False,
)


class RegisterJobDefinitionRequestRequestTypeDef(
    _RequiredRegisterJobDefinitionRequestRequestTypeDef,
    _OptionalRegisterJobDefinitionRequestRequestTypeDef,
):
    pass


DescribeJobDefinitionsResponseTypeDef = TypedDict(
    "DescribeJobDefinitionsResponseTypeDef",
    {
        "jobDefinitions": List[JobDefinitionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeJobsResponseTypeDef = TypedDict(
    "DescribeJobsResponseTypeDef",
    {
        "jobs": List[JobDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
