"""
Type annotations for ecs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/type_defs/)

Usage::

    ```python
    from mypy_boto3_ecs.type_defs import AttachmentStateChangeTypeDef

    data: AttachmentStateChangeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AgentUpdateStatusType,
    AssignPublicIpType,
    CapacityProviderStatusType,
    CapacityProviderUpdateStatusType,
    ClusterFieldType,
    CompatibilityType,
    ConnectivityType,
    ContainerConditionType,
    ContainerInstanceFieldType,
    ContainerInstanceStatusType,
    CPUArchitectureType,
    DeploymentControllerTypeType,
    DeploymentRolloutStateType,
    DesiredStatusType,
    DeviceCgroupPermissionType,
    EFSAuthorizationConfigIAMType,
    EFSTransitEncryptionType,
    ExecuteCommandLoggingType,
    FirelensConfigurationTypeType,
    HealthStatusType,
    InstanceHealthCheckStateType,
    IpcModeType,
    LaunchTypeType,
    LogDriverType,
    ManagedScalingStatusType,
    ManagedTerminationProtectionType,
    NetworkModeType,
    OSFamilyType,
    PidModeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    PropagateTagsType,
    ResourceTypeType,
    SchedulingStrategyType,
    ScopeType,
    SettingNameType,
    SortOrderType,
    StabilityStatusType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
    TaskStopCodeType,
    TransportProtocolType,
    UlimitNameType,
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
    "AttachmentStateChangeTypeDef",
    "KeyValuePairTypeDef",
    "AttributeTypeDef",
    "ManagedScalingTypeDef",
    "AwsVpcConfigurationTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "TagTypeDef",
    "ClusterSettingTypeDef",
    "ContainerDependencyTypeDef",
    "EnvironmentFileTypeDef",
    "FirelensConfigurationTypeDef",
    "HealthCheckTypeDef",
    "HostEntryTypeDef",
    "MountPointTypeDef",
    "PortMappingTypeDef",
    "RepositoryCredentialsTypeDef",
    "ResourceRequirementTypeDef",
    "SecretTypeDef",
    "SystemControlTypeDef",
    "UlimitTypeDef",
    "VolumeFromTypeDef",
    "InstanceHealthCheckResultTypeDef",
    "ResourceTypeDef",
    "VersionInfoTypeDef",
    "NetworkBindingTypeDef",
    "ManagedAgentTypeDef",
    "NetworkInterfaceTypeDef",
    "ResponseMetadataTypeDef",
    "DeploymentControllerTypeDef",
    "LoadBalancerTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "ServiceRegistryTypeDef",
    "ScaleTypeDef",
    "DeleteAccountSettingRequestRequestTypeDef",
    "SettingTypeDef",
    "DeleteCapacityProviderRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteTaskSetRequestRequestTypeDef",
    "DeploymentCircuitBreakerTypeDef",
    "DeregisterContainerInstanceRequestRequestTypeDef",
    "DeregisterTaskDefinitionRequestRequestTypeDef",
    "DescribeCapacityProvidersRequestRequestTypeDef",
    "FailureTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeContainerInstancesRequestRequestTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeTaskDefinitionRequestRequestTypeDef",
    "DescribeTaskSetsRequestRequestTypeDef",
    "DescribeTasksRequestRequestTypeDef",
    "DeviceTypeDef",
    "DiscoverPollEndpointRequestRequestTypeDef",
    "DockerVolumeConfigurationTypeDef",
    "EFSAuthorizationConfigTypeDef",
    "EphemeralStorageTypeDef",
    "ExecuteCommandLogConfigurationTypeDef",
    "ExecuteCommandRequestRequestTypeDef",
    "SessionTypeDef",
    "FSxWindowsFileServerAuthorizationConfigTypeDef",
    "HostVolumePropertiesTypeDef",
    "InferenceAcceleratorOverrideTypeDef",
    "InferenceAcceleratorTypeDef",
    "KernelCapabilitiesTypeDef",
    "TmpfsTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccountSettingsRequestRequestTypeDef",
    "ListAttributesRequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListContainerInstancesRequestRequestTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTaskDefinitionFamiliesRequestRequestTypeDef",
    "ListTaskDefinitionsRequestRequestTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ManagedAgentStateChangeTypeDef",
    "PlatformDeviceTypeDef",
    "PutAccountSettingDefaultRequestRequestTypeDef",
    "PutAccountSettingRequestRequestTypeDef",
    "RuntimePlatformTypeDef",
    "TaskDefinitionPlacementConstraintTypeDef",
    "ServiceEventTypeDef",
    "StopTaskRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContainerAgentRequestRequestTypeDef",
    "UpdateContainerInstancesStateRequestRequestTypeDef",
    "UpdateServicePrimaryTaskSetRequestRequestTypeDef",
    "SubmitAttachmentStateChangesRequestRequestTypeDef",
    "AttachmentTypeDef",
    "ProxyConfigurationTypeDef",
    "DeleteAttributesRequestRequestTypeDef",
    "PutAttributesRequestRequestTypeDef",
    "AutoScalingGroupProviderTypeDef",
    "AutoScalingGroupProviderUpdateTypeDef",
    "NetworkConfigurationTypeDef",
    "PutClusterCapacityProvidersRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UpdateClusterSettingsRequestRequestTypeDef",
    "ContainerOverrideTypeDef",
    "LogConfigurationTypeDef",
    "ContainerInstanceHealthStatusTypeDef",
    "ContainerStateChangeTypeDef",
    "SubmitContainerStateChangeRequestRequestTypeDef",
    "ContainerTypeDef",
    "DeleteAttributesResponseTypeDef",
    "DiscoverPollEndpointResponseTypeDef",
    "ListAttributesResponseTypeDef",
    "ListClustersResponseTypeDef",
    "ListContainerInstancesResponseTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTaskDefinitionFamiliesResponseTypeDef",
    "ListTaskDefinitionsResponseTypeDef",
    "ListTasksResponseTypeDef",
    "PutAttributesResponseTypeDef",
    "SubmitAttachmentStateChangesResponseTypeDef",
    "SubmitContainerStateChangeResponseTypeDef",
    "SubmitTaskStateChangeResponseTypeDef",
    "UpdateTaskSetRequestRequestTypeDef",
    "DeleteAccountSettingResponseTypeDef",
    "ListAccountSettingsResponseTypeDef",
    "PutAccountSettingDefaultResponseTypeDef",
    "PutAccountSettingResponseTypeDef",
    "DeploymentConfigurationTypeDef",
    "DescribeServicesRequestServicesInactiveWaitTypeDef",
    "DescribeServicesRequestServicesStableWaitTypeDef",
    "DescribeTasksRequestTasksRunningWaitTypeDef",
    "DescribeTasksRequestTasksStoppedWaitTypeDef",
    "EFSVolumeConfigurationTypeDef",
    "ExecuteCommandConfigurationTypeDef",
    "ExecuteCommandResponseTypeDef",
    "FSxWindowsFileServerVolumeConfigurationTypeDef",
    "LinuxParametersTypeDef",
    "ListAccountSettingsRequestListAccountSettingsPaginateTypeDef",
    "ListAttributesRequestListAttributesPaginateTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListContainerInstancesRequestListContainerInstancesPaginateTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListTaskDefinitionFamiliesRequestListTaskDefinitionFamiliesPaginateTypeDef",
    "ListTaskDefinitionsRequestListTaskDefinitionsPaginateTypeDef",
    "ListTasksRequestListTasksPaginateTypeDef",
    "RegisterContainerInstanceRequestRequestTypeDef",
    "CapacityProviderTypeDef",
    "CreateCapacityProviderRequestRequestTypeDef",
    "UpdateCapacityProviderRequestRequestTypeDef",
    "CreateTaskSetRequestRequestTypeDef",
    "DeploymentTypeDef",
    "TaskSetTypeDef",
    "TaskOverrideTypeDef",
    "ContainerInstanceTypeDef",
    "SubmitTaskStateChangeRequestRequestTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "ClusterConfigurationTypeDef",
    "VolumeTypeDef",
    "ContainerDefinitionTypeDef",
    "CreateCapacityProviderResponseTypeDef",
    "DeleteCapacityProviderResponseTypeDef",
    "DescribeCapacityProvidersResponseTypeDef",
    "UpdateCapacityProviderResponseTypeDef",
    "CreateTaskSetResponseTypeDef",
    "DeleteTaskSetResponseTypeDef",
    "DescribeTaskSetsResponseTypeDef",
    "ServiceTypeDef",
    "UpdateServicePrimaryTaskSetResponseTypeDef",
    "UpdateTaskSetResponseTypeDef",
    "RunTaskRequestRequestTypeDef",
    "StartTaskRequestRequestTypeDef",
    "TaskTypeDef",
    "DeregisterContainerInstanceResponseTypeDef",
    "DescribeContainerInstancesResponseTypeDef",
    "RegisterContainerInstanceResponseTypeDef",
    "UpdateContainerAgentResponseTypeDef",
    "UpdateContainerInstancesStateResponseTypeDef",
    "ClusterTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "RegisterTaskDefinitionRequestRequestTypeDef",
    "TaskDefinitionTypeDef",
    "CreateServiceResponseTypeDef",
    "DeleteServiceResponseTypeDef",
    "DescribeServicesResponseTypeDef",
    "UpdateServiceResponseTypeDef",
    "DescribeTasksResponseTypeDef",
    "RunTaskResponseTypeDef",
    "StartTaskResponseTypeDef",
    "StopTaskResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DescribeClustersResponseTypeDef",
    "PutClusterCapacityProvidersResponseTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSettingsResponseTypeDef",
    "DeregisterTaskDefinitionResponseTypeDef",
    "DescribeTaskDefinitionResponseTypeDef",
    "RegisterTaskDefinitionResponseTypeDef",
)

AttachmentStateChangeTypeDef = TypedDict(
    "AttachmentStateChangeTypeDef",
    {
        "attachmentArn": str,
        "status": str,
    },
)

KeyValuePairTypeDef = TypedDict(
    "KeyValuePairTypeDef",
    {
        "name": str,
        "value": str,
    },
    total=False,
)

_RequiredAttributeTypeDef = TypedDict(
    "_RequiredAttributeTypeDef",
    {
        "name": str,
    },
)
_OptionalAttributeTypeDef = TypedDict(
    "_OptionalAttributeTypeDef",
    {
        "value": str,
        "targetType": Literal["container-instance"],
        "targetId": str,
    },
    total=False,
)

class AttributeTypeDef(_RequiredAttributeTypeDef, _OptionalAttributeTypeDef):
    pass

ManagedScalingTypeDef = TypedDict(
    "ManagedScalingTypeDef",
    {
        "status": ManagedScalingStatusType,
        "targetCapacity": int,
        "minimumScalingStepSize": int,
        "maximumScalingStepSize": int,
        "instanceWarmupPeriod": int,
    },
    total=False,
)

_RequiredAwsVpcConfigurationTypeDef = TypedDict(
    "_RequiredAwsVpcConfigurationTypeDef",
    {
        "subnets": Sequence[str],
    },
)
_OptionalAwsVpcConfigurationTypeDef = TypedDict(
    "_OptionalAwsVpcConfigurationTypeDef",
    {
        "securityGroups": Sequence[str],
        "assignPublicIp": AssignPublicIpType,
    },
    total=False,
)

class AwsVpcConfigurationTypeDef(
    _RequiredAwsVpcConfigurationTypeDef, _OptionalAwsVpcConfigurationTypeDef
):
    pass

_RequiredCapacityProviderStrategyItemTypeDef = TypedDict(
    "_RequiredCapacityProviderStrategyItemTypeDef",
    {
        "capacityProvider": str,
    },
)
_OptionalCapacityProviderStrategyItemTypeDef = TypedDict(
    "_OptionalCapacityProviderStrategyItemTypeDef",
    {
        "weight": int,
        "base": int,
    },
    total=False,
)

class CapacityProviderStrategyItemTypeDef(
    _RequiredCapacityProviderStrategyItemTypeDef, _OptionalCapacityProviderStrategyItemTypeDef
):
    pass

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
    total=False,
)

ClusterSettingTypeDef = TypedDict(
    "ClusterSettingTypeDef",
    {
        "name": Literal["containerInsights"],
        "value": str,
    },
    total=False,
)

ContainerDependencyTypeDef = TypedDict(
    "ContainerDependencyTypeDef",
    {
        "containerName": str,
        "condition": ContainerConditionType,
    },
)

EnvironmentFileTypeDef = TypedDict(
    "EnvironmentFileTypeDef",
    {
        "value": str,
        "type": Literal["s3"],
    },
)

_RequiredFirelensConfigurationTypeDef = TypedDict(
    "_RequiredFirelensConfigurationTypeDef",
    {
        "type": FirelensConfigurationTypeType,
    },
)
_OptionalFirelensConfigurationTypeDef = TypedDict(
    "_OptionalFirelensConfigurationTypeDef",
    {
        "options": Dict[str, str],
    },
    total=False,
)

class FirelensConfigurationTypeDef(
    _RequiredFirelensConfigurationTypeDef, _OptionalFirelensConfigurationTypeDef
):
    pass

_RequiredHealthCheckTypeDef = TypedDict(
    "_RequiredHealthCheckTypeDef",
    {
        "command": List[str],
    },
)
_OptionalHealthCheckTypeDef = TypedDict(
    "_OptionalHealthCheckTypeDef",
    {
        "interval": int,
        "timeout": int,
        "retries": int,
        "startPeriod": int,
    },
    total=False,
)

class HealthCheckTypeDef(_RequiredHealthCheckTypeDef, _OptionalHealthCheckTypeDef):
    pass

HostEntryTypeDef = TypedDict(
    "HostEntryTypeDef",
    {
        "hostname": str,
        "ipAddress": str,
    },
)

MountPointTypeDef = TypedDict(
    "MountPointTypeDef",
    {
        "sourceVolume": str,
        "containerPath": str,
        "readOnly": bool,
    },
    total=False,
)

PortMappingTypeDef = TypedDict(
    "PortMappingTypeDef",
    {
        "containerPort": int,
        "hostPort": int,
        "protocol": TransportProtocolType,
    },
    total=False,
)

RepositoryCredentialsTypeDef = TypedDict(
    "RepositoryCredentialsTypeDef",
    {
        "credentialsParameter": str,
    },
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

SystemControlTypeDef = TypedDict(
    "SystemControlTypeDef",
    {
        "namespace": str,
        "value": str,
    },
    total=False,
)

UlimitTypeDef = TypedDict(
    "UlimitTypeDef",
    {
        "name": UlimitNameType,
        "softLimit": int,
        "hardLimit": int,
    },
)

VolumeFromTypeDef = TypedDict(
    "VolumeFromTypeDef",
    {
        "sourceContainer": str,
        "readOnly": bool,
    },
    total=False,
)

InstanceHealthCheckResultTypeDef = TypedDict(
    "InstanceHealthCheckResultTypeDef",
    {
        "type": Literal["CONTAINER_RUNTIME"],
        "status": InstanceHealthCheckStateType,
        "lastUpdated": datetime,
        "lastStatusChange": datetime,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "name": str,
        "type": str,
        "doubleValue": float,
        "longValue": int,
        "integerValue": int,
        "stringSetValue": List[str],
    },
    total=False,
)

VersionInfoTypeDef = TypedDict(
    "VersionInfoTypeDef",
    {
        "agentVersion": str,
        "agentHash": str,
        "dockerVersion": str,
    },
    total=False,
)

NetworkBindingTypeDef = TypedDict(
    "NetworkBindingTypeDef",
    {
        "bindIP": str,
        "containerPort": int,
        "hostPort": int,
        "protocol": TransportProtocolType,
    },
    total=False,
)

ManagedAgentTypeDef = TypedDict(
    "ManagedAgentTypeDef",
    {
        "lastStartedAt": datetime,
        "name": Literal["ExecuteCommandAgent"],
        "reason": str,
        "lastStatus": str,
    },
    total=False,
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "attachmentId": str,
        "privateIpv4Address": str,
        "ipv6Address": str,
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

DeploymentControllerTypeDef = TypedDict(
    "DeploymentControllerTypeDef",
    {
        "type": DeploymentControllerTypeType,
    },
)

LoadBalancerTypeDef = TypedDict(
    "LoadBalancerTypeDef",
    {
        "targetGroupArn": str,
        "loadBalancerName": str,
        "containerName": str,
        "containerPort": int,
    },
    total=False,
)

PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "type": PlacementConstraintTypeType,
        "expression": str,
    },
    total=False,
)

PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "type": PlacementStrategyTypeType,
        "field": str,
    },
    total=False,
)

ServiceRegistryTypeDef = TypedDict(
    "ServiceRegistryTypeDef",
    {
        "registryArn": str,
        "port": int,
        "containerName": str,
        "containerPort": int,
    },
    total=False,
)

ScaleTypeDef = TypedDict(
    "ScaleTypeDef",
    {
        "value": float,
        "unit": Literal["PERCENT"],
    },
    total=False,
)

_RequiredDeleteAccountSettingRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccountSettingRequestRequestTypeDef",
    {
        "name": SettingNameType,
    },
)
_OptionalDeleteAccountSettingRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccountSettingRequestRequestTypeDef",
    {
        "principalArn": str,
    },
    total=False,
)

class DeleteAccountSettingRequestRequestTypeDef(
    _RequiredDeleteAccountSettingRequestRequestTypeDef,
    _OptionalDeleteAccountSettingRequestRequestTypeDef,
):
    pass

SettingTypeDef = TypedDict(
    "SettingTypeDef",
    {
        "name": SettingNameType,
        "value": str,
        "principalArn": str,
    },
    total=False,
)

DeleteCapacityProviderRequestRequestTypeDef = TypedDict(
    "DeleteCapacityProviderRequestRequestTypeDef",
    {
        "capacityProvider": str,
    },
)

DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "cluster": str,
    },
)

_RequiredDeleteServiceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteServiceRequestRequestTypeDef",
    {
        "service": str,
    },
)
_OptionalDeleteServiceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteServiceRequestRequestTypeDef",
    {
        "cluster": str,
        "force": bool,
    },
    total=False,
)

class DeleteServiceRequestRequestTypeDef(
    _RequiredDeleteServiceRequestRequestTypeDef, _OptionalDeleteServiceRequestRequestTypeDef
):
    pass

_RequiredDeleteTaskSetRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTaskSetRequestRequestTypeDef",
    {
        "cluster": str,
        "service": str,
        "taskSet": str,
    },
)
_OptionalDeleteTaskSetRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTaskSetRequestRequestTypeDef",
    {
        "force": bool,
    },
    total=False,
)

class DeleteTaskSetRequestRequestTypeDef(
    _RequiredDeleteTaskSetRequestRequestTypeDef, _OptionalDeleteTaskSetRequestRequestTypeDef
):
    pass

DeploymentCircuitBreakerTypeDef = TypedDict(
    "DeploymentCircuitBreakerTypeDef",
    {
        "enable": bool,
        "rollback": bool,
    },
)

_RequiredDeregisterContainerInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredDeregisterContainerInstanceRequestRequestTypeDef",
    {
        "containerInstance": str,
    },
)
_OptionalDeregisterContainerInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalDeregisterContainerInstanceRequestRequestTypeDef",
    {
        "cluster": str,
        "force": bool,
    },
    total=False,
)

class DeregisterContainerInstanceRequestRequestTypeDef(
    _RequiredDeregisterContainerInstanceRequestRequestTypeDef,
    _OptionalDeregisterContainerInstanceRequestRequestTypeDef,
):
    pass

DeregisterTaskDefinitionRequestRequestTypeDef = TypedDict(
    "DeregisterTaskDefinitionRequestRequestTypeDef",
    {
        "taskDefinition": str,
    },
)

DescribeCapacityProvidersRequestRequestTypeDef = TypedDict(
    "DescribeCapacityProvidersRequestRequestTypeDef",
    {
        "capacityProviders": Sequence[str],
        "include": Sequence[Literal["TAGS"]],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

FailureTypeDef = TypedDict(
    "FailureTypeDef",
    {
        "arn": str,
        "reason": str,
        "detail": str,
    },
    total=False,
)

DescribeClustersRequestRequestTypeDef = TypedDict(
    "DescribeClustersRequestRequestTypeDef",
    {
        "clusters": Sequence[str],
        "include": Sequence[ClusterFieldType],
    },
    total=False,
)

_RequiredDescribeContainerInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeContainerInstancesRequestRequestTypeDef",
    {
        "containerInstances": Sequence[str],
    },
)
_OptionalDescribeContainerInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeContainerInstancesRequestRequestTypeDef",
    {
        "cluster": str,
        "include": Sequence[ContainerInstanceFieldType],
    },
    total=False,
)

class DescribeContainerInstancesRequestRequestTypeDef(
    _RequiredDescribeContainerInstancesRequestRequestTypeDef,
    _OptionalDescribeContainerInstancesRequestRequestTypeDef,
):
    pass

_RequiredDescribeServicesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeServicesRequestRequestTypeDef",
    {
        "services": Sequence[str],
    },
)
_OptionalDescribeServicesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeServicesRequestRequestTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
    },
    total=False,
)

class DescribeServicesRequestRequestTypeDef(
    _RequiredDescribeServicesRequestRequestTypeDef, _OptionalDescribeServicesRequestRequestTypeDef
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

_RequiredDescribeTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTaskDefinitionRequestRequestTypeDef",
    {
        "taskDefinition": str,
    },
)
_OptionalDescribeTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTaskDefinitionRequestRequestTypeDef",
    {
        "include": Sequence[Literal["TAGS"]],
    },
    total=False,
)

class DescribeTaskDefinitionRequestRequestTypeDef(
    _RequiredDescribeTaskDefinitionRequestRequestTypeDef,
    _OptionalDescribeTaskDefinitionRequestRequestTypeDef,
):
    pass

_RequiredDescribeTaskSetsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTaskSetsRequestRequestTypeDef",
    {
        "cluster": str,
        "service": str,
    },
)
_OptionalDescribeTaskSetsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTaskSetsRequestRequestTypeDef",
    {
        "taskSets": Sequence[str],
        "include": Sequence[Literal["TAGS"]],
    },
    total=False,
)

class DescribeTaskSetsRequestRequestTypeDef(
    _RequiredDescribeTaskSetsRequestRequestTypeDef, _OptionalDescribeTaskSetsRequestRequestTypeDef
):
    pass

_RequiredDescribeTasksRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTasksRequestRequestTypeDef",
    {
        "tasks": Sequence[str],
    },
)
_OptionalDescribeTasksRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTasksRequestRequestTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
    },
    total=False,
)

class DescribeTasksRequestRequestTypeDef(
    _RequiredDescribeTasksRequestRequestTypeDef, _OptionalDescribeTasksRequestRequestTypeDef
):
    pass

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

DiscoverPollEndpointRequestRequestTypeDef = TypedDict(
    "DiscoverPollEndpointRequestRequestTypeDef",
    {
        "containerInstance": str,
        "cluster": str,
    },
    total=False,
)

DockerVolumeConfigurationTypeDef = TypedDict(
    "DockerVolumeConfigurationTypeDef",
    {
        "scope": ScopeType,
        "autoprovision": bool,
        "driver": str,
        "driverOpts": Dict[str, str],
        "labels": Dict[str, str],
    },
    total=False,
)

EFSAuthorizationConfigTypeDef = TypedDict(
    "EFSAuthorizationConfigTypeDef",
    {
        "accessPointId": str,
        "iam": EFSAuthorizationConfigIAMType,
    },
    total=False,
)

EphemeralStorageTypeDef = TypedDict(
    "EphemeralStorageTypeDef",
    {
        "sizeInGiB": int,
    },
)

ExecuteCommandLogConfigurationTypeDef = TypedDict(
    "ExecuteCommandLogConfigurationTypeDef",
    {
        "cloudWatchLogGroupName": str,
        "cloudWatchEncryptionEnabled": bool,
        "s3BucketName": str,
        "s3EncryptionEnabled": bool,
        "s3KeyPrefix": str,
    },
    total=False,
)

_RequiredExecuteCommandRequestRequestTypeDef = TypedDict(
    "_RequiredExecuteCommandRequestRequestTypeDef",
    {
        "command": str,
        "interactive": bool,
        "task": str,
    },
)
_OptionalExecuteCommandRequestRequestTypeDef = TypedDict(
    "_OptionalExecuteCommandRequestRequestTypeDef",
    {
        "cluster": str,
        "container": str,
    },
    total=False,
)

class ExecuteCommandRequestRequestTypeDef(
    _RequiredExecuteCommandRequestRequestTypeDef, _OptionalExecuteCommandRequestRequestTypeDef
):
    pass

SessionTypeDef = TypedDict(
    "SessionTypeDef",
    {
        "sessionId": str,
        "streamUrl": str,
        "tokenValue": str,
    },
    total=False,
)

FSxWindowsFileServerAuthorizationConfigTypeDef = TypedDict(
    "FSxWindowsFileServerAuthorizationConfigTypeDef",
    {
        "credentialsParameter": str,
        "domain": str,
    },
)

HostVolumePropertiesTypeDef = TypedDict(
    "HostVolumePropertiesTypeDef",
    {
        "sourcePath": str,
    },
    total=False,
)

InferenceAcceleratorOverrideTypeDef = TypedDict(
    "InferenceAcceleratorOverrideTypeDef",
    {
        "deviceName": str,
        "deviceType": str,
    },
    total=False,
)

InferenceAcceleratorTypeDef = TypedDict(
    "InferenceAcceleratorTypeDef",
    {
        "deviceName": str,
        "deviceType": str,
    },
)

KernelCapabilitiesTypeDef = TypedDict(
    "KernelCapabilitiesTypeDef",
    {
        "add": List[str],
        "drop": List[str],
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

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListAccountSettingsRequestRequestTypeDef = TypedDict(
    "ListAccountSettingsRequestRequestTypeDef",
    {
        "name": SettingNameType,
        "value": str,
        "principalArn": str,
        "effectiveSettings": bool,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredListAttributesRequestRequestTypeDef",
    {
        "targetType": Literal["container-instance"],
    },
)
_OptionalListAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalListAttributesRequestRequestTypeDef",
    {
        "cluster": str,
        "attributeName": str,
        "attributeValue": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListAttributesRequestRequestTypeDef(
    _RequiredListAttributesRequestRequestTypeDef, _OptionalListAttributesRequestRequestTypeDef
):
    pass

ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListContainerInstancesRequestRequestTypeDef = TypedDict(
    "ListContainerInstancesRequestRequestTypeDef",
    {
        "cluster": str,
        "filter": str,
        "nextToken": str,
        "maxResults": int,
        "status": ContainerInstanceStatusType,
    },
    total=False,
)

ListServicesRequestRequestTypeDef = TypedDict(
    "ListServicesRequestRequestTypeDef",
    {
        "cluster": str,
        "nextToken": str,
        "maxResults": int,
        "launchType": LaunchTypeType,
        "schedulingStrategy": SchedulingStrategyType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTaskDefinitionFamiliesRequestRequestTypeDef = TypedDict(
    "ListTaskDefinitionFamiliesRequestRequestTypeDef",
    {
        "familyPrefix": str,
        "status": TaskDefinitionFamilyStatusType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTaskDefinitionsRequestRequestTypeDef = TypedDict(
    "ListTaskDefinitionsRequestRequestTypeDef",
    {
        "familyPrefix": str,
        "status": TaskDefinitionStatusType,
        "sort": SortOrderType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTasksRequestRequestTypeDef = TypedDict(
    "ListTasksRequestRequestTypeDef",
    {
        "cluster": str,
        "containerInstance": str,
        "family": str,
        "nextToken": str,
        "maxResults": int,
        "startedBy": str,
        "serviceName": str,
        "desiredStatus": DesiredStatusType,
        "launchType": LaunchTypeType,
    },
    total=False,
)

_RequiredManagedAgentStateChangeTypeDef = TypedDict(
    "_RequiredManagedAgentStateChangeTypeDef",
    {
        "containerName": str,
        "managedAgentName": Literal["ExecuteCommandAgent"],
        "status": str,
    },
)
_OptionalManagedAgentStateChangeTypeDef = TypedDict(
    "_OptionalManagedAgentStateChangeTypeDef",
    {
        "reason": str,
    },
    total=False,
)

class ManagedAgentStateChangeTypeDef(
    _RequiredManagedAgentStateChangeTypeDef, _OptionalManagedAgentStateChangeTypeDef
):
    pass

PlatformDeviceTypeDef = TypedDict(
    "PlatformDeviceTypeDef",
    {
        "id": str,
        "type": Literal["GPU"],
    },
)

PutAccountSettingDefaultRequestRequestTypeDef = TypedDict(
    "PutAccountSettingDefaultRequestRequestTypeDef",
    {
        "name": SettingNameType,
        "value": str,
    },
)

_RequiredPutAccountSettingRequestRequestTypeDef = TypedDict(
    "_RequiredPutAccountSettingRequestRequestTypeDef",
    {
        "name": SettingNameType,
        "value": str,
    },
)
_OptionalPutAccountSettingRequestRequestTypeDef = TypedDict(
    "_OptionalPutAccountSettingRequestRequestTypeDef",
    {
        "principalArn": str,
    },
    total=False,
)

class PutAccountSettingRequestRequestTypeDef(
    _RequiredPutAccountSettingRequestRequestTypeDef, _OptionalPutAccountSettingRequestRequestTypeDef
):
    pass

RuntimePlatformTypeDef = TypedDict(
    "RuntimePlatformTypeDef",
    {
        "cpuArchitecture": CPUArchitectureType,
        "operatingSystemFamily": OSFamilyType,
    },
    total=False,
)

TaskDefinitionPlacementConstraintTypeDef = TypedDict(
    "TaskDefinitionPlacementConstraintTypeDef",
    {
        "type": Literal["memberOf"],
        "expression": str,
    },
    total=False,
)

ServiceEventTypeDef = TypedDict(
    "ServiceEventTypeDef",
    {
        "id": str,
        "createdAt": datetime,
        "message": str,
    },
    total=False,
)

_RequiredStopTaskRequestRequestTypeDef = TypedDict(
    "_RequiredStopTaskRequestRequestTypeDef",
    {
        "task": str,
    },
)
_OptionalStopTaskRequestRequestTypeDef = TypedDict(
    "_OptionalStopTaskRequestRequestTypeDef",
    {
        "cluster": str,
        "reason": str,
    },
    total=False,
)

class StopTaskRequestRequestTypeDef(
    _RequiredStopTaskRequestRequestTypeDef, _OptionalStopTaskRequestRequestTypeDef
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateContainerAgentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContainerAgentRequestRequestTypeDef",
    {
        "containerInstance": str,
    },
)
_OptionalUpdateContainerAgentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContainerAgentRequestRequestTypeDef",
    {
        "cluster": str,
    },
    total=False,
)

class UpdateContainerAgentRequestRequestTypeDef(
    _RequiredUpdateContainerAgentRequestRequestTypeDef,
    _OptionalUpdateContainerAgentRequestRequestTypeDef,
):
    pass

_RequiredUpdateContainerInstancesStateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContainerInstancesStateRequestRequestTypeDef",
    {
        "containerInstances": Sequence[str],
        "status": ContainerInstanceStatusType,
    },
)
_OptionalUpdateContainerInstancesStateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContainerInstancesStateRequestRequestTypeDef",
    {
        "cluster": str,
    },
    total=False,
)

class UpdateContainerInstancesStateRequestRequestTypeDef(
    _RequiredUpdateContainerInstancesStateRequestRequestTypeDef,
    _OptionalUpdateContainerInstancesStateRequestRequestTypeDef,
):
    pass

UpdateServicePrimaryTaskSetRequestRequestTypeDef = TypedDict(
    "UpdateServicePrimaryTaskSetRequestRequestTypeDef",
    {
        "cluster": str,
        "service": str,
        "primaryTaskSet": str,
    },
)

_RequiredSubmitAttachmentStateChangesRequestRequestTypeDef = TypedDict(
    "_RequiredSubmitAttachmentStateChangesRequestRequestTypeDef",
    {
        "attachments": Sequence[AttachmentStateChangeTypeDef],
    },
)
_OptionalSubmitAttachmentStateChangesRequestRequestTypeDef = TypedDict(
    "_OptionalSubmitAttachmentStateChangesRequestRequestTypeDef",
    {
        "cluster": str,
    },
    total=False,
)

class SubmitAttachmentStateChangesRequestRequestTypeDef(
    _RequiredSubmitAttachmentStateChangesRequestRequestTypeDef,
    _OptionalSubmitAttachmentStateChangesRequestRequestTypeDef,
):
    pass

AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "id": str,
        "type": str,
        "status": str,
        "details": List[KeyValuePairTypeDef],
    },
    total=False,
)

_RequiredProxyConfigurationTypeDef = TypedDict(
    "_RequiredProxyConfigurationTypeDef",
    {
        "containerName": str,
    },
)
_OptionalProxyConfigurationTypeDef = TypedDict(
    "_OptionalProxyConfigurationTypeDef",
    {
        "type": Literal["APPMESH"],
        "properties": List[KeyValuePairTypeDef],
    },
    total=False,
)

class ProxyConfigurationTypeDef(
    _RequiredProxyConfigurationTypeDef, _OptionalProxyConfigurationTypeDef
):
    pass

_RequiredDeleteAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAttributesRequestRequestTypeDef",
    {
        "attributes": Sequence[AttributeTypeDef],
    },
)
_OptionalDeleteAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAttributesRequestRequestTypeDef",
    {
        "cluster": str,
    },
    total=False,
)

class DeleteAttributesRequestRequestTypeDef(
    _RequiredDeleteAttributesRequestRequestTypeDef, _OptionalDeleteAttributesRequestRequestTypeDef
):
    pass

_RequiredPutAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutAttributesRequestRequestTypeDef",
    {
        "attributes": Sequence[AttributeTypeDef],
    },
)
_OptionalPutAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutAttributesRequestRequestTypeDef",
    {
        "cluster": str,
    },
    total=False,
)

class PutAttributesRequestRequestTypeDef(
    _RequiredPutAttributesRequestRequestTypeDef, _OptionalPutAttributesRequestRequestTypeDef
):
    pass

_RequiredAutoScalingGroupProviderTypeDef = TypedDict(
    "_RequiredAutoScalingGroupProviderTypeDef",
    {
        "autoScalingGroupArn": str,
    },
)
_OptionalAutoScalingGroupProviderTypeDef = TypedDict(
    "_OptionalAutoScalingGroupProviderTypeDef",
    {
        "managedScaling": ManagedScalingTypeDef,
        "managedTerminationProtection": ManagedTerminationProtectionType,
    },
    total=False,
)

class AutoScalingGroupProviderTypeDef(
    _RequiredAutoScalingGroupProviderTypeDef, _OptionalAutoScalingGroupProviderTypeDef
):
    pass

AutoScalingGroupProviderUpdateTypeDef = TypedDict(
    "AutoScalingGroupProviderUpdateTypeDef",
    {
        "managedScaling": ManagedScalingTypeDef,
        "managedTerminationProtection": ManagedTerminationProtectionType,
    },
    total=False,
)

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "awsvpcConfiguration": AwsVpcConfigurationTypeDef,
    },
    total=False,
)

PutClusterCapacityProvidersRequestRequestTypeDef = TypedDict(
    "PutClusterCapacityProvidersRequestRequestTypeDef",
    {
        "cluster": str,
        "capacityProviders": Sequence[str],
        "defaultCapacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

UpdateClusterSettingsRequestRequestTypeDef = TypedDict(
    "UpdateClusterSettingsRequestRequestTypeDef",
    {
        "cluster": str,
        "settings": Sequence[ClusterSettingTypeDef],
    },
)

ContainerOverrideTypeDef = TypedDict(
    "ContainerOverrideTypeDef",
    {
        "name": str,
        "command": List[str],
        "environment": List[KeyValuePairTypeDef],
        "environmentFiles": List[EnvironmentFileTypeDef],
        "cpu": int,
        "memory": int,
        "memoryReservation": int,
        "resourceRequirements": List[ResourceRequirementTypeDef],
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

ContainerInstanceHealthStatusTypeDef = TypedDict(
    "ContainerInstanceHealthStatusTypeDef",
    {
        "overallStatus": InstanceHealthCheckStateType,
        "details": List[InstanceHealthCheckResultTypeDef],
    },
    total=False,
)

ContainerStateChangeTypeDef = TypedDict(
    "ContainerStateChangeTypeDef",
    {
        "containerName": str,
        "imageDigest": str,
        "runtimeId": str,
        "exitCode": int,
        "networkBindings": Sequence[NetworkBindingTypeDef],
        "reason": str,
        "status": str,
    },
    total=False,
)

SubmitContainerStateChangeRequestRequestTypeDef = TypedDict(
    "SubmitContainerStateChangeRequestRequestTypeDef",
    {
        "cluster": str,
        "task": str,
        "containerName": str,
        "runtimeId": str,
        "status": str,
        "exitCode": int,
        "reason": str,
        "networkBindings": Sequence[NetworkBindingTypeDef],
    },
    total=False,
)

ContainerTypeDef = TypedDict(
    "ContainerTypeDef",
    {
        "containerArn": str,
        "taskArn": str,
        "name": str,
        "image": str,
        "imageDigest": str,
        "runtimeId": str,
        "lastStatus": str,
        "exitCode": int,
        "reason": str,
        "networkBindings": List[NetworkBindingTypeDef],
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "healthStatus": HealthStatusType,
        "managedAgents": List[ManagedAgentTypeDef],
        "cpu": str,
        "memory": str,
        "memoryReservation": str,
        "gpuIds": List[str],
    },
    total=False,
)

DeleteAttributesResponseTypeDef = TypedDict(
    "DeleteAttributesResponseTypeDef",
    {
        "attributes": List[AttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DiscoverPollEndpointResponseTypeDef = TypedDict(
    "DiscoverPollEndpointResponseTypeDef",
    {
        "endpoint": str,
        "telemetryEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttributesResponseTypeDef = TypedDict(
    "ListAttributesResponseTypeDef",
    {
        "attributes": List[AttributeTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResponseTypeDef = TypedDict(
    "ListClustersResponseTypeDef",
    {
        "clusterArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContainerInstancesResponseTypeDef = TypedDict(
    "ListContainerInstancesResponseTypeDef",
    {
        "containerInstanceArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicesResponseTypeDef = TypedDict(
    "ListServicesResponseTypeDef",
    {
        "serviceArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTaskDefinitionFamiliesResponseTypeDef = TypedDict(
    "ListTaskDefinitionFamiliesResponseTypeDef",
    {
        "families": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTaskDefinitionsResponseTypeDef = TypedDict(
    "ListTaskDefinitionsResponseTypeDef",
    {
        "taskDefinitionArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTasksResponseTypeDef = TypedDict(
    "ListTasksResponseTypeDef",
    {
        "taskArns": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAttributesResponseTypeDef = TypedDict(
    "PutAttributesResponseTypeDef",
    {
        "attributes": List[AttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubmitAttachmentStateChangesResponseTypeDef = TypedDict(
    "SubmitAttachmentStateChangesResponseTypeDef",
    {
        "acknowledgment": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubmitContainerStateChangeResponseTypeDef = TypedDict(
    "SubmitContainerStateChangeResponseTypeDef",
    {
        "acknowledgment": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubmitTaskStateChangeResponseTypeDef = TypedDict(
    "SubmitTaskStateChangeResponseTypeDef",
    {
        "acknowledgment": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTaskSetRequestRequestTypeDef = TypedDict(
    "UpdateTaskSetRequestRequestTypeDef",
    {
        "cluster": str,
        "service": str,
        "taskSet": str,
        "scale": ScaleTypeDef,
    },
)

DeleteAccountSettingResponseTypeDef = TypedDict(
    "DeleteAccountSettingResponseTypeDef",
    {
        "setting": SettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountSettingsResponseTypeDef = TypedDict(
    "ListAccountSettingsResponseTypeDef",
    {
        "settings": List[SettingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAccountSettingDefaultResponseTypeDef = TypedDict(
    "PutAccountSettingDefaultResponseTypeDef",
    {
        "setting": SettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAccountSettingResponseTypeDef = TypedDict(
    "PutAccountSettingResponseTypeDef",
    {
        "setting": SettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentConfigurationTypeDef = TypedDict(
    "DeploymentConfigurationTypeDef",
    {
        "deploymentCircuitBreaker": DeploymentCircuitBreakerTypeDef,
        "maximumPercent": int,
        "minimumHealthyPercent": int,
    },
    total=False,
)

_RequiredDescribeServicesRequestServicesInactiveWaitTypeDef = TypedDict(
    "_RequiredDescribeServicesRequestServicesInactiveWaitTypeDef",
    {
        "services": Sequence[str],
    },
)
_OptionalDescribeServicesRequestServicesInactiveWaitTypeDef = TypedDict(
    "_OptionalDescribeServicesRequestServicesInactiveWaitTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeServicesRequestServicesInactiveWaitTypeDef(
    _RequiredDescribeServicesRequestServicesInactiveWaitTypeDef,
    _OptionalDescribeServicesRequestServicesInactiveWaitTypeDef,
):
    pass

_RequiredDescribeServicesRequestServicesStableWaitTypeDef = TypedDict(
    "_RequiredDescribeServicesRequestServicesStableWaitTypeDef",
    {
        "services": Sequence[str],
    },
)
_OptionalDescribeServicesRequestServicesStableWaitTypeDef = TypedDict(
    "_OptionalDescribeServicesRequestServicesStableWaitTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeServicesRequestServicesStableWaitTypeDef(
    _RequiredDescribeServicesRequestServicesStableWaitTypeDef,
    _OptionalDescribeServicesRequestServicesStableWaitTypeDef,
):
    pass

_RequiredDescribeTasksRequestTasksRunningWaitTypeDef = TypedDict(
    "_RequiredDescribeTasksRequestTasksRunningWaitTypeDef",
    {
        "tasks": Sequence[str],
    },
)
_OptionalDescribeTasksRequestTasksRunningWaitTypeDef = TypedDict(
    "_OptionalDescribeTasksRequestTasksRunningWaitTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeTasksRequestTasksRunningWaitTypeDef(
    _RequiredDescribeTasksRequestTasksRunningWaitTypeDef,
    _OptionalDescribeTasksRequestTasksRunningWaitTypeDef,
):
    pass

_RequiredDescribeTasksRequestTasksStoppedWaitTypeDef = TypedDict(
    "_RequiredDescribeTasksRequestTasksStoppedWaitTypeDef",
    {
        "tasks": Sequence[str],
    },
)
_OptionalDescribeTasksRequestTasksStoppedWaitTypeDef = TypedDict(
    "_OptionalDescribeTasksRequestTasksStoppedWaitTypeDef",
    {
        "cluster": str,
        "include": Sequence[Literal["TAGS"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeTasksRequestTasksStoppedWaitTypeDef(
    _RequiredDescribeTasksRequestTasksStoppedWaitTypeDef,
    _OptionalDescribeTasksRequestTasksStoppedWaitTypeDef,
):
    pass

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

ExecuteCommandConfigurationTypeDef = TypedDict(
    "ExecuteCommandConfigurationTypeDef",
    {
        "kmsKeyId": str,
        "logging": ExecuteCommandLoggingType,
        "logConfiguration": ExecuteCommandLogConfigurationTypeDef,
    },
    total=False,
)

ExecuteCommandResponseTypeDef = TypedDict(
    "ExecuteCommandResponseTypeDef",
    {
        "clusterArn": str,
        "containerArn": str,
        "containerName": str,
        "interactive": bool,
        "session": SessionTypeDef,
        "taskArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FSxWindowsFileServerVolumeConfigurationTypeDef = TypedDict(
    "FSxWindowsFileServerVolumeConfigurationTypeDef",
    {
        "fileSystemId": str,
        "rootDirectory": str,
        "authorizationConfig": FSxWindowsFileServerAuthorizationConfigTypeDef,
    },
)

LinuxParametersTypeDef = TypedDict(
    "LinuxParametersTypeDef",
    {
        "capabilities": KernelCapabilitiesTypeDef,
        "devices": List[DeviceTypeDef],
        "initProcessEnabled": bool,
        "sharedMemorySize": int,
        "tmpfs": List[TmpfsTypeDef],
        "maxSwap": int,
        "swappiness": int,
    },
    total=False,
)

ListAccountSettingsRequestListAccountSettingsPaginateTypeDef = TypedDict(
    "ListAccountSettingsRequestListAccountSettingsPaginateTypeDef",
    {
        "name": SettingNameType,
        "value": str,
        "principalArn": str,
        "effectiveSettings": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAttributesRequestListAttributesPaginateTypeDef = TypedDict(
    "_RequiredListAttributesRequestListAttributesPaginateTypeDef",
    {
        "targetType": Literal["container-instance"],
    },
)
_OptionalListAttributesRequestListAttributesPaginateTypeDef = TypedDict(
    "_OptionalListAttributesRequestListAttributesPaginateTypeDef",
    {
        "cluster": str,
        "attributeName": str,
        "attributeValue": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAttributesRequestListAttributesPaginateTypeDef(
    _RequiredListAttributesRequestListAttributesPaginateTypeDef,
    _OptionalListAttributesRequestListAttributesPaginateTypeDef,
):
    pass

ListClustersRequestListClustersPaginateTypeDef = TypedDict(
    "ListClustersRequestListClustersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListContainerInstancesRequestListContainerInstancesPaginateTypeDef = TypedDict(
    "ListContainerInstancesRequestListContainerInstancesPaginateTypeDef",
    {
        "cluster": str,
        "filter": str,
        "status": ContainerInstanceStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "ListServicesRequestListServicesPaginateTypeDef",
    {
        "cluster": str,
        "launchType": LaunchTypeType,
        "schedulingStrategy": SchedulingStrategyType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTaskDefinitionFamiliesRequestListTaskDefinitionFamiliesPaginateTypeDef = TypedDict(
    "ListTaskDefinitionFamiliesRequestListTaskDefinitionFamiliesPaginateTypeDef",
    {
        "familyPrefix": str,
        "status": TaskDefinitionFamilyStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTaskDefinitionsRequestListTaskDefinitionsPaginateTypeDef = TypedDict(
    "ListTaskDefinitionsRequestListTaskDefinitionsPaginateTypeDef",
    {
        "familyPrefix": str,
        "status": TaskDefinitionStatusType,
        "sort": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTasksRequestListTasksPaginateTypeDef = TypedDict(
    "ListTasksRequestListTasksPaginateTypeDef",
    {
        "cluster": str,
        "containerInstance": str,
        "family": str,
        "startedBy": str,
        "serviceName": str,
        "desiredStatus": DesiredStatusType,
        "launchType": LaunchTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

RegisterContainerInstanceRequestRequestTypeDef = TypedDict(
    "RegisterContainerInstanceRequestRequestTypeDef",
    {
        "cluster": str,
        "instanceIdentityDocument": str,
        "instanceIdentityDocumentSignature": str,
        "totalResources": Sequence[ResourceTypeDef],
        "versionInfo": VersionInfoTypeDef,
        "containerInstanceArn": str,
        "attributes": Sequence[AttributeTypeDef],
        "platformDevices": Sequence[PlatformDeviceTypeDef],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

CapacityProviderTypeDef = TypedDict(
    "CapacityProviderTypeDef",
    {
        "capacityProviderArn": str,
        "name": str,
        "status": CapacityProviderStatusType,
        "autoScalingGroupProvider": AutoScalingGroupProviderTypeDef,
        "updateStatus": CapacityProviderUpdateStatusType,
        "updateStatusReason": str,
        "tags": List[TagTypeDef],
    },
    total=False,
)

_RequiredCreateCapacityProviderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCapacityProviderRequestRequestTypeDef",
    {
        "name": str,
        "autoScalingGroupProvider": AutoScalingGroupProviderTypeDef,
    },
)
_OptionalCreateCapacityProviderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCapacityProviderRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateCapacityProviderRequestRequestTypeDef(
    _RequiredCreateCapacityProviderRequestRequestTypeDef,
    _OptionalCreateCapacityProviderRequestRequestTypeDef,
):
    pass

UpdateCapacityProviderRequestRequestTypeDef = TypedDict(
    "UpdateCapacityProviderRequestRequestTypeDef",
    {
        "name": str,
        "autoScalingGroupProvider": AutoScalingGroupProviderUpdateTypeDef,
    },
)

_RequiredCreateTaskSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTaskSetRequestRequestTypeDef",
    {
        "service": str,
        "cluster": str,
        "taskDefinition": str,
    },
)
_OptionalCreateTaskSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTaskSetRequestRequestTypeDef",
    {
        "externalId": str,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "loadBalancers": Sequence[LoadBalancerTypeDef],
        "serviceRegistries": Sequence[ServiceRegistryTypeDef],
        "launchType": LaunchTypeType,
        "capacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "platformVersion": str,
        "scale": ScaleTypeDef,
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateTaskSetRequestRequestTypeDef(
    _RequiredCreateTaskSetRequestRequestTypeDef, _OptionalCreateTaskSetRequestRequestTypeDef
):
    pass

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "id": str,
        "status": str,
        "taskDefinition": str,
        "desiredCount": int,
        "pendingCount": int,
        "runningCount": int,
        "failedTasks": int,
        "createdAt": datetime,
        "updatedAt": datetime,
        "capacityProviderStrategy": List[CapacityProviderStrategyItemTypeDef],
        "launchType": LaunchTypeType,
        "platformVersion": str,
        "platformFamily": str,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "rolloutState": DeploymentRolloutStateType,
        "rolloutStateReason": str,
    },
    total=False,
)

TaskSetTypeDef = TypedDict(
    "TaskSetTypeDef",
    {
        "id": str,
        "taskSetArn": str,
        "serviceArn": str,
        "clusterArn": str,
        "startedBy": str,
        "externalId": str,
        "status": str,
        "taskDefinition": str,
        "computedDesiredCount": int,
        "pendingCount": int,
        "runningCount": int,
        "createdAt": datetime,
        "updatedAt": datetime,
        "launchType": LaunchTypeType,
        "capacityProviderStrategy": List[CapacityProviderStrategyItemTypeDef],
        "platformVersion": str,
        "platformFamily": str,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "loadBalancers": List[LoadBalancerTypeDef],
        "serviceRegistries": List[ServiceRegistryTypeDef],
        "scale": ScaleTypeDef,
        "stabilityStatus": StabilityStatusType,
        "stabilityStatusAt": datetime,
        "tags": List[TagTypeDef],
    },
    total=False,
)

TaskOverrideTypeDef = TypedDict(
    "TaskOverrideTypeDef",
    {
        "containerOverrides": List[ContainerOverrideTypeDef],
        "cpu": str,
        "inferenceAcceleratorOverrides": List[InferenceAcceleratorOverrideTypeDef],
        "executionRoleArn": str,
        "memory": str,
        "taskRoleArn": str,
        "ephemeralStorage": EphemeralStorageTypeDef,
    },
    total=False,
)

ContainerInstanceTypeDef = TypedDict(
    "ContainerInstanceTypeDef",
    {
        "containerInstanceArn": str,
        "ec2InstanceId": str,
        "capacityProviderName": str,
        "version": int,
        "versionInfo": VersionInfoTypeDef,
        "remainingResources": List[ResourceTypeDef],
        "registeredResources": List[ResourceTypeDef],
        "status": str,
        "statusReason": str,
        "agentConnected": bool,
        "runningTasksCount": int,
        "pendingTasksCount": int,
        "agentUpdateStatus": AgentUpdateStatusType,
        "attributes": List[AttributeTypeDef],
        "registeredAt": datetime,
        "attachments": List[AttachmentTypeDef],
        "tags": List[TagTypeDef],
        "healthStatus": ContainerInstanceHealthStatusTypeDef,
    },
    total=False,
)

SubmitTaskStateChangeRequestRequestTypeDef = TypedDict(
    "SubmitTaskStateChangeRequestRequestTypeDef",
    {
        "cluster": str,
        "task": str,
        "status": str,
        "reason": str,
        "containers": Sequence[ContainerStateChangeTypeDef],
        "attachments": Sequence[AttachmentStateChangeTypeDef],
        "managedAgents": Sequence[ManagedAgentStateChangeTypeDef],
        "pullStartedAt": Union[datetime, str],
        "pullStoppedAt": Union[datetime, str],
        "executionStoppedAt": Union[datetime, str],
    },
    total=False,
)

_RequiredCreateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceRequestRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalCreateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceRequestRequestTypeDef",
    {
        "cluster": str,
        "taskDefinition": str,
        "loadBalancers": Sequence[LoadBalancerTypeDef],
        "serviceRegistries": Sequence[ServiceRegistryTypeDef],
        "desiredCount": int,
        "clientToken": str,
        "launchType": LaunchTypeType,
        "capacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "platformVersion": str,
        "role": str,
        "deploymentConfiguration": DeploymentConfigurationTypeDef,
        "placementConstraints": Sequence[PlacementConstraintTypeDef],
        "placementStrategy": Sequence[PlacementStrategyTypeDef],
        "networkConfiguration": NetworkConfigurationTypeDef,
        "healthCheckGracePeriodSeconds": int,
        "schedulingStrategy": SchedulingStrategyType,
        "deploymentController": DeploymentControllerTypeDef,
        "tags": Sequence[TagTypeDef],
        "enableECSManagedTags": bool,
        "propagateTags": PropagateTagsType,
        "enableExecuteCommand": bool,
    },
    total=False,
)

class CreateServiceRequestRequestTypeDef(
    _RequiredCreateServiceRequestRequestTypeDef, _OptionalCreateServiceRequestRequestTypeDef
):
    pass

_RequiredUpdateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceRequestRequestTypeDef",
    {
        "service": str,
    },
)
_OptionalUpdateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceRequestRequestTypeDef",
    {
        "cluster": str,
        "desiredCount": int,
        "taskDefinition": str,
        "capacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "deploymentConfiguration": DeploymentConfigurationTypeDef,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "placementConstraints": Sequence[PlacementConstraintTypeDef],
        "placementStrategy": Sequence[PlacementStrategyTypeDef],
        "platformVersion": str,
        "forceNewDeployment": bool,
        "healthCheckGracePeriodSeconds": int,
        "enableExecuteCommand": bool,
        "enableECSManagedTags": bool,
        "loadBalancers": Sequence[LoadBalancerTypeDef],
        "propagateTags": PropagateTagsType,
        "serviceRegistries": Sequence[ServiceRegistryTypeDef],
    },
    total=False,
)

class UpdateServiceRequestRequestTypeDef(
    _RequiredUpdateServiceRequestRequestTypeDef, _OptionalUpdateServiceRequestRequestTypeDef
):
    pass

ClusterConfigurationTypeDef = TypedDict(
    "ClusterConfigurationTypeDef",
    {
        "executeCommandConfiguration": ExecuteCommandConfigurationTypeDef,
    },
    total=False,
)

VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "name": str,
        "host": HostVolumePropertiesTypeDef,
        "dockerVolumeConfiguration": DockerVolumeConfigurationTypeDef,
        "efsVolumeConfiguration": EFSVolumeConfigurationTypeDef,
        "fsxWindowsFileServerVolumeConfiguration": FSxWindowsFileServerVolumeConfigurationTypeDef,
    },
    total=False,
)

ContainerDefinitionTypeDef = TypedDict(
    "ContainerDefinitionTypeDef",
    {
        "name": str,
        "image": str,
        "repositoryCredentials": RepositoryCredentialsTypeDef,
        "cpu": int,
        "memory": int,
        "memoryReservation": int,
        "links": List[str],
        "portMappings": List[PortMappingTypeDef],
        "essential": bool,
        "entryPoint": List[str],
        "command": List[str],
        "environment": List[KeyValuePairTypeDef],
        "environmentFiles": List[EnvironmentFileTypeDef],
        "mountPoints": List[MountPointTypeDef],
        "volumesFrom": List[VolumeFromTypeDef],
        "linuxParameters": LinuxParametersTypeDef,
        "secrets": List[SecretTypeDef],
        "dependsOn": List[ContainerDependencyTypeDef],
        "startTimeout": int,
        "stopTimeout": int,
        "hostname": str,
        "user": str,
        "workingDirectory": str,
        "disableNetworking": bool,
        "privileged": bool,
        "readonlyRootFilesystem": bool,
        "dnsServers": List[str],
        "dnsSearchDomains": List[str],
        "extraHosts": List[HostEntryTypeDef],
        "dockerSecurityOptions": List[str],
        "interactive": bool,
        "pseudoTerminal": bool,
        "dockerLabels": Dict[str, str],
        "ulimits": List[UlimitTypeDef],
        "logConfiguration": LogConfigurationTypeDef,
        "healthCheck": HealthCheckTypeDef,
        "systemControls": List[SystemControlTypeDef],
        "resourceRequirements": List[ResourceRequirementTypeDef],
        "firelensConfiguration": FirelensConfigurationTypeDef,
    },
    total=False,
)

CreateCapacityProviderResponseTypeDef = TypedDict(
    "CreateCapacityProviderResponseTypeDef",
    {
        "capacityProvider": CapacityProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCapacityProviderResponseTypeDef = TypedDict(
    "DeleteCapacityProviderResponseTypeDef",
    {
        "capacityProvider": CapacityProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCapacityProvidersResponseTypeDef = TypedDict(
    "DescribeCapacityProvidersResponseTypeDef",
    {
        "capacityProviders": List[CapacityProviderTypeDef],
        "failures": List[FailureTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCapacityProviderResponseTypeDef = TypedDict(
    "UpdateCapacityProviderResponseTypeDef",
    {
        "capacityProvider": CapacityProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTaskSetResponseTypeDef = TypedDict(
    "CreateTaskSetResponseTypeDef",
    {
        "taskSet": TaskSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTaskSetResponseTypeDef = TypedDict(
    "DeleteTaskSetResponseTypeDef",
    {
        "taskSet": TaskSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTaskSetsResponseTypeDef = TypedDict(
    "DescribeTaskSetsResponseTypeDef",
    {
        "taskSets": List[TaskSetTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "serviceArn": str,
        "serviceName": str,
        "clusterArn": str,
        "loadBalancers": List[LoadBalancerTypeDef],
        "serviceRegistries": List[ServiceRegistryTypeDef],
        "status": str,
        "desiredCount": int,
        "runningCount": int,
        "pendingCount": int,
        "launchType": LaunchTypeType,
        "capacityProviderStrategy": List[CapacityProviderStrategyItemTypeDef],
        "platformVersion": str,
        "platformFamily": str,
        "taskDefinition": str,
        "deploymentConfiguration": DeploymentConfigurationTypeDef,
        "taskSets": List[TaskSetTypeDef],
        "deployments": List[DeploymentTypeDef],
        "roleArn": str,
        "events": List[ServiceEventTypeDef],
        "createdAt": datetime,
        "placementConstraints": List[PlacementConstraintTypeDef],
        "placementStrategy": List[PlacementStrategyTypeDef],
        "networkConfiguration": NetworkConfigurationTypeDef,
        "healthCheckGracePeriodSeconds": int,
        "schedulingStrategy": SchedulingStrategyType,
        "deploymentController": DeploymentControllerTypeDef,
        "tags": List[TagTypeDef],
        "createdBy": str,
        "enableECSManagedTags": bool,
        "propagateTags": PropagateTagsType,
        "enableExecuteCommand": bool,
    },
    total=False,
)

UpdateServicePrimaryTaskSetResponseTypeDef = TypedDict(
    "UpdateServicePrimaryTaskSetResponseTypeDef",
    {
        "taskSet": TaskSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTaskSetResponseTypeDef = TypedDict(
    "UpdateTaskSetResponseTypeDef",
    {
        "taskSet": TaskSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRunTaskRequestRequestTypeDef = TypedDict(
    "_RequiredRunTaskRequestRequestTypeDef",
    {
        "taskDefinition": str,
    },
)
_OptionalRunTaskRequestRequestTypeDef = TypedDict(
    "_OptionalRunTaskRequestRequestTypeDef",
    {
        "capacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "cluster": str,
        "count": int,
        "enableECSManagedTags": bool,
        "enableExecuteCommand": bool,
        "group": str,
        "launchType": LaunchTypeType,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "overrides": TaskOverrideTypeDef,
        "placementConstraints": Sequence[PlacementConstraintTypeDef],
        "placementStrategy": Sequence[PlacementStrategyTypeDef],
        "platformVersion": str,
        "propagateTags": PropagateTagsType,
        "referenceId": str,
        "startedBy": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class RunTaskRequestRequestTypeDef(
    _RequiredRunTaskRequestRequestTypeDef, _OptionalRunTaskRequestRequestTypeDef
):
    pass

_RequiredStartTaskRequestRequestTypeDef = TypedDict(
    "_RequiredStartTaskRequestRequestTypeDef",
    {
        "containerInstances": Sequence[str],
        "taskDefinition": str,
    },
)
_OptionalStartTaskRequestRequestTypeDef = TypedDict(
    "_OptionalStartTaskRequestRequestTypeDef",
    {
        "cluster": str,
        "enableECSManagedTags": bool,
        "enableExecuteCommand": bool,
        "group": str,
        "networkConfiguration": NetworkConfigurationTypeDef,
        "overrides": TaskOverrideTypeDef,
        "propagateTags": PropagateTagsType,
        "referenceId": str,
        "startedBy": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartTaskRequestRequestTypeDef(
    _RequiredStartTaskRequestRequestTypeDef, _OptionalStartTaskRequestRequestTypeDef
):
    pass

TaskTypeDef = TypedDict(
    "TaskTypeDef",
    {
        "attachments": List[AttachmentTypeDef],
        "attributes": List[AttributeTypeDef],
        "availabilityZone": str,
        "capacityProviderName": str,
        "clusterArn": str,
        "connectivity": ConnectivityType,
        "connectivityAt": datetime,
        "containerInstanceArn": str,
        "containers": List[ContainerTypeDef],
        "cpu": str,
        "createdAt": datetime,
        "desiredStatus": str,
        "enableExecuteCommand": bool,
        "executionStoppedAt": datetime,
        "group": str,
        "healthStatus": HealthStatusType,
        "inferenceAccelerators": List[InferenceAcceleratorTypeDef],
        "lastStatus": str,
        "launchType": LaunchTypeType,
        "memory": str,
        "overrides": TaskOverrideTypeDef,
        "platformVersion": str,
        "platformFamily": str,
        "pullStartedAt": datetime,
        "pullStoppedAt": datetime,
        "startedAt": datetime,
        "startedBy": str,
        "stopCode": TaskStopCodeType,
        "stoppedAt": datetime,
        "stoppedReason": str,
        "stoppingAt": datetime,
        "tags": List[TagTypeDef],
        "taskArn": str,
        "taskDefinitionArn": str,
        "version": int,
        "ephemeralStorage": EphemeralStorageTypeDef,
    },
    total=False,
)

DeregisterContainerInstanceResponseTypeDef = TypedDict(
    "DeregisterContainerInstanceResponseTypeDef",
    {
        "containerInstance": ContainerInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeContainerInstancesResponseTypeDef = TypedDict(
    "DescribeContainerInstancesResponseTypeDef",
    {
        "containerInstances": List[ContainerInstanceTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterContainerInstanceResponseTypeDef = TypedDict(
    "RegisterContainerInstanceResponseTypeDef",
    {
        "containerInstance": ContainerInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateContainerAgentResponseTypeDef = TypedDict(
    "UpdateContainerAgentResponseTypeDef",
    {
        "containerInstance": ContainerInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateContainerInstancesStateResponseTypeDef = TypedDict(
    "UpdateContainerInstancesStateResponseTypeDef",
    {
        "containerInstances": List[ContainerInstanceTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "clusterArn": str,
        "clusterName": str,
        "configuration": ClusterConfigurationTypeDef,
        "status": str,
        "registeredContainerInstancesCount": int,
        "runningTasksCount": int,
        "pendingTasksCount": int,
        "activeServicesCount": int,
        "statistics": List[KeyValuePairTypeDef],
        "tags": List[TagTypeDef],
        "settings": List[ClusterSettingTypeDef],
        "capacityProviders": List[str],
        "defaultCapacityProviderStrategy": List[CapacityProviderStrategyItemTypeDef],
        "attachments": List[AttachmentTypeDef],
        "attachmentsStatus": str,
    },
    total=False,
)

CreateClusterRequestRequestTypeDef = TypedDict(
    "CreateClusterRequestRequestTypeDef",
    {
        "clusterName": str,
        "tags": Sequence[TagTypeDef],
        "settings": Sequence[ClusterSettingTypeDef],
        "configuration": ClusterConfigurationTypeDef,
        "capacityProviders": Sequence[str],
        "defaultCapacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
    },
    total=False,
)

_RequiredUpdateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterRequestRequestTypeDef",
    {
        "cluster": str,
    },
)
_OptionalUpdateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterRequestRequestTypeDef",
    {
        "settings": Sequence[ClusterSettingTypeDef],
        "configuration": ClusterConfigurationTypeDef,
    },
    total=False,
)

class UpdateClusterRequestRequestTypeDef(
    _RequiredUpdateClusterRequestRequestTypeDef, _OptionalUpdateClusterRequestRequestTypeDef
):
    pass

_RequiredRegisterTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterTaskDefinitionRequestRequestTypeDef",
    {
        "family": str,
        "containerDefinitions": Sequence[ContainerDefinitionTypeDef],
    },
)
_OptionalRegisterTaskDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterTaskDefinitionRequestRequestTypeDef",
    {
        "taskRoleArn": str,
        "executionRoleArn": str,
        "networkMode": NetworkModeType,
        "volumes": Sequence[VolumeTypeDef],
        "placementConstraints": Sequence[TaskDefinitionPlacementConstraintTypeDef],
        "requiresCompatibilities": Sequence[CompatibilityType],
        "cpu": str,
        "memory": str,
        "tags": Sequence[TagTypeDef],
        "pidMode": PidModeType,
        "ipcMode": IpcModeType,
        "proxyConfiguration": ProxyConfigurationTypeDef,
        "inferenceAccelerators": Sequence[InferenceAcceleratorTypeDef],
        "ephemeralStorage": EphemeralStorageTypeDef,
        "runtimePlatform": RuntimePlatformTypeDef,
    },
    total=False,
)

class RegisterTaskDefinitionRequestRequestTypeDef(
    _RequiredRegisterTaskDefinitionRequestRequestTypeDef,
    _OptionalRegisterTaskDefinitionRequestRequestTypeDef,
):
    pass

TaskDefinitionTypeDef = TypedDict(
    "TaskDefinitionTypeDef",
    {
        "taskDefinitionArn": str,
        "containerDefinitions": List[ContainerDefinitionTypeDef],
        "family": str,
        "taskRoleArn": str,
        "executionRoleArn": str,
        "networkMode": NetworkModeType,
        "revision": int,
        "volumes": List[VolumeTypeDef],
        "status": TaskDefinitionStatusType,
        "requiresAttributes": List[AttributeTypeDef],
        "placementConstraints": List[TaskDefinitionPlacementConstraintTypeDef],
        "compatibilities": List[CompatibilityType],
        "runtimePlatform": RuntimePlatformTypeDef,
        "requiresCompatibilities": List[CompatibilityType],
        "cpu": str,
        "memory": str,
        "inferenceAccelerators": List[InferenceAcceleratorTypeDef],
        "pidMode": PidModeType,
        "ipcMode": IpcModeType,
        "proxyConfiguration": ProxyConfigurationTypeDef,
        "registeredAt": datetime,
        "deregisteredAt": datetime,
        "registeredBy": str,
        "ephemeralStorage": EphemeralStorageTypeDef,
    },
    total=False,
)

CreateServiceResponseTypeDef = TypedDict(
    "CreateServiceResponseTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceResponseTypeDef = TypedDict(
    "DeleteServiceResponseTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeServicesResponseTypeDef = TypedDict(
    "DescribeServicesResponseTypeDef",
    {
        "services": List[ServiceTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceResponseTypeDef = TypedDict(
    "UpdateServiceResponseTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTasksResponseTypeDef = TypedDict(
    "DescribeTasksResponseTypeDef",
    {
        "tasks": List[TaskTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunTaskResponseTypeDef = TypedDict(
    "RunTaskResponseTypeDef",
    {
        "tasks": List[TaskTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTaskResponseTypeDef = TypedDict(
    "StartTaskResponseTypeDef",
    {
        "tasks": List[TaskTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopTaskResponseTypeDef = TypedDict(
    "StopTaskResponseTypeDef",
    {
        "task": TaskTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClustersResponseTypeDef = TypedDict(
    "DescribeClustersResponseTypeDef",
    {
        "clusters": List[ClusterTypeDef],
        "failures": List[FailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutClusterCapacityProvidersResponseTypeDef = TypedDict(
    "PutClusterCapacityProvidersResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterResponseTypeDef = TypedDict(
    "UpdateClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterSettingsResponseTypeDef = TypedDict(
    "UpdateClusterSettingsResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterTaskDefinitionResponseTypeDef = TypedDict(
    "DeregisterTaskDefinitionResponseTypeDef",
    {
        "taskDefinition": TaskDefinitionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTaskDefinitionResponseTypeDef = TypedDict(
    "DescribeTaskDefinitionResponseTypeDef",
    {
        "taskDefinition": TaskDefinitionTypeDef,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterTaskDefinitionResponseTypeDef = TypedDict(
    "RegisterTaskDefinitionResponseTypeDef",
    {
        "taskDefinition": TaskDefinitionTypeDef,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
