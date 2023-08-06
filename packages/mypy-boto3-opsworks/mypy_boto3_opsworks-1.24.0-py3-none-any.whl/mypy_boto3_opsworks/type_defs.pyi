"""
Type annotations for opsworks service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/type_defs/)

Usage::

    ```python
    from mypy_boto3_opsworks.type_defs import StackConfigurationManagerTypeDef

    data: StackConfigurationManagerTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AppAttributesKeysType,
    AppTypeType,
    ArchitectureType,
    AutoScalingTypeType,
    CloudWatchLogsEncodingType,
    CloudWatchLogsInitialPositionType,
    CloudWatchLogsTimeZoneType,
    DeploymentCommandNameType,
    LayerAttributesKeysType,
    LayerTypeType,
    RootDeviceTypeType,
    SourceTypeType,
    VirtualizationTypeType,
    VolumeTypeType,
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
    "StackConfigurationManagerTypeDef",
    "DataSourceTypeDef",
    "EnvironmentVariableTypeDef",
    "SourceTypeDef",
    "SslConfigurationTypeDef",
    "AssignInstanceRequestRequestTypeDef",
    "AssignVolumeRequestRequestTypeDef",
    "AssociateElasticIpRequestRequestTypeDef",
    "AttachElasticLoadBalancerRequestRequestTypeDef",
    "AutoScalingThresholdsTypeDef",
    "EbsBlockDeviceTypeDef",
    "ResponseMetadataTypeDef",
    "ChefConfigurationTypeDef",
    "CloudWatchLogsLogStreamTypeDef",
    "CommandTypeDef",
    "DeploymentCommandTypeDef",
    "RecipesTypeDef",
    "VolumeConfigurationTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeleteLayerRequestRequestTypeDef",
    "DeleteStackRequestRequestTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DeregisterEcsClusterRequestRequestTypeDef",
    "DeregisterElasticIpRequestRequestTypeDef",
    "DeregisterInstanceRequestRequestTypeDef",
    "DeregisterRdsDbInstanceRequestRequestTypeDef",
    "DeregisterVolumeRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAppsRequestRequestTypeDef",
    "DescribeCommandsRequestRequestTypeDef",
    "DescribeDeploymentsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeEcsClustersRequestRequestTypeDef",
    "EcsClusterTypeDef",
    "DescribeElasticIpsRequestRequestTypeDef",
    "ElasticIpTypeDef",
    "DescribeElasticLoadBalancersRequestRequestTypeDef",
    "ElasticLoadBalancerTypeDef",
    "DescribeInstancesRequestRequestTypeDef",
    "DescribeLayersRequestRequestTypeDef",
    "DescribeLoadBasedAutoScalingRequestRequestTypeDef",
    "SelfUserProfileTypeDef",
    "DescribePermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "DescribeRaidArraysRequestRequestTypeDef",
    "RaidArrayTypeDef",
    "DescribeRdsDbInstancesRequestRequestTypeDef",
    "RdsDbInstanceTypeDef",
    "DescribeServiceErrorsRequestRequestTypeDef",
    "ServiceErrorTypeDef",
    "DescribeStackProvisioningParametersRequestRequestTypeDef",
    "DescribeStackSummaryRequestRequestTypeDef",
    "DescribeStacksRequestRequestTypeDef",
    "DescribeTimeBasedAutoScalingRequestRequestTypeDef",
    "DescribeUserProfilesRequestRequestTypeDef",
    "UserProfileTypeDef",
    "DescribeVolumesRequestRequestTypeDef",
    "VolumeTypeDef",
    "DetachElasticLoadBalancerRequestRequestTypeDef",
    "DisassociateElasticIpRequestRequestTypeDef",
    "GetHostnameSuggestionRequestRequestTypeDef",
    "GrantAccessRequestRequestTypeDef",
    "TemporaryCredentialTypeDef",
    "InstanceIdentityTypeDef",
    "ReportedOsTypeDef",
    "InstancesCountTypeDef",
    "ShutdownEventConfigurationTypeDef",
    "ListTagsRequestRequestTypeDef",
    "OperatingSystemConfigurationManagerTypeDef",
    "RebootInstanceRequestRequestTypeDef",
    "RegisterEcsClusterRequestRequestTypeDef",
    "RegisterElasticIpRequestRequestTypeDef",
    "RegisterRdsDbInstanceRequestRequestTypeDef",
    "RegisterVolumeRequestRequestTypeDef",
    "ServiceResourceLayerRequestTypeDef",
    "ServiceResourceStackRequestTypeDef",
    "ServiceResourceStackSummaryRequestTypeDef",
    "SetPermissionRequestRequestTypeDef",
    "WeeklyAutoScalingScheduleTypeDef",
    "StartInstanceRequestRequestTypeDef",
    "StartStackRequestRequestTypeDef",
    "StopInstanceRequestRequestTypeDef",
    "StopStackRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UnassignInstanceRequestRequestTypeDef",
    "UnassignVolumeRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateElasticIpRequestRequestTypeDef",
    "UpdateInstanceRequestRequestTypeDef",
    "UpdateMyUserProfileRequestRequestTypeDef",
    "UpdateRdsDbInstanceRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "UpdateVolumeRequestRequestTypeDef",
    "AgentVersionTypeDef",
    "DescribeAgentVersionsRequestRequestTypeDef",
    "AppTypeDef",
    "CreateAppRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "LoadBasedAutoScalingConfigurationTypeDef",
    "SetLoadBasedAutoScalingRequestRequestTypeDef",
    "BlockDeviceMappingTypeDef",
    "ChefConfigurationResponseMetadataTypeDef",
    "CloneStackResultTypeDef",
    "CreateAppResultTypeDef",
    "CreateDeploymentResultTypeDef",
    "CreateInstanceResultTypeDef",
    "CreateLayerResultTypeDef",
    "CreateStackResultTypeDef",
    "CreateUserProfileResultTypeDef",
    "DescribeStackProvisioningParametersResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetHostnameSuggestionResultTypeDef",
    "InstancesCountResponseMetadataTypeDef",
    "ListTagsResultTypeDef",
    "RecipesResponseMetadataTypeDef",
    "RegisterEcsClusterResultTypeDef",
    "RegisterElasticIpResultTypeDef",
    "RegisterInstanceResultTypeDef",
    "RegisterVolumeResultTypeDef",
    "SourceResponseMetadataTypeDef",
    "StackConfigurationManagerResponseMetadataTypeDef",
    "CloneStackRequestRequestTypeDef",
    "CreateStackRequestRequestTypeDef",
    "CreateStackRequestServiceResourceCreateStackTypeDef",
    "StackTypeDef",
    "UpdateStackRequestRequestTypeDef",
    "CloudWatchLogsConfigurationResponseMetadataTypeDef",
    "CloudWatchLogsConfigurationTypeDef",
    "DescribeCommandsResultTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "DeploymentTypeDef",
    "DescribeAppsRequestAppExistsWaitTypeDef",
    "DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef",
    "DescribeInstancesRequestInstanceOnlineWaitTypeDef",
    "DescribeInstancesRequestInstanceRegisteredWaitTypeDef",
    "DescribeInstancesRequestInstanceStoppedWaitTypeDef",
    "DescribeInstancesRequestInstanceTerminatedWaitTypeDef",
    "DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef",
    "DescribeEcsClustersResultTypeDef",
    "DescribeElasticIpsResultTypeDef",
    "DescribeElasticLoadBalancersResultTypeDef",
    "DescribeMyUserProfileResultTypeDef",
    "DescribePermissionsResultTypeDef",
    "DescribeRaidArraysResultTypeDef",
    "DescribeRdsDbInstancesResultTypeDef",
    "DescribeServiceErrorsResultTypeDef",
    "DescribeUserProfilesResultTypeDef",
    "DescribeVolumesResultTypeDef",
    "GrantAccessResultTypeDef",
    "RegisterInstanceRequestRequestTypeDef",
    "StackSummaryTypeDef",
    "LifecycleEventConfigurationResponseMetadataTypeDef",
    "LifecycleEventConfigurationTypeDef",
    "OperatingSystemTypeDef",
    "SetTimeBasedAutoScalingRequestRequestTypeDef",
    "TimeBasedAutoScalingConfigurationTypeDef",
    "DescribeAgentVersionsResultTypeDef",
    "DescribeAppsResultTypeDef",
    "DescribeLoadBasedAutoScalingResultTypeDef",
    "CreateInstanceRequestRequestTypeDef",
    "InstanceTypeDef",
    "DescribeStacksResultTypeDef",
    "DescribeDeploymentsResultTypeDef",
    "DescribeStackSummaryResultTypeDef",
    "CreateLayerRequestRequestTypeDef",
    "CreateLayerRequestStackCreateLayerTypeDef",
    "LayerTypeDef",
    "UpdateLayerRequestRequestTypeDef",
    "DescribeOperatingSystemsResponseTypeDef",
    "DescribeTimeBasedAutoScalingResultTypeDef",
    "DescribeInstancesResultTypeDef",
    "DescribeLayersResultTypeDef",
)

StackConfigurationManagerTypeDef = TypedDict(
    "StackConfigurationManagerTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Type": str,
        "Arn": str,
        "DatabaseName": str,
    },
    total=False,
)

_RequiredEnvironmentVariableTypeDef = TypedDict(
    "_RequiredEnvironmentVariableTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)
_OptionalEnvironmentVariableTypeDef = TypedDict(
    "_OptionalEnvironmentVariableTypeDef",
    {
        "Secure": bool,
    },
    total=False,
)

class EnvironmentVariableTypeDef(
    _RequiredEnvironmentVariableTypeDef, _OptionalEnvironmentVariableTypeDef
):
    pass

SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "Type": SourceTypeType,
        "Url": str,
        "Username": str,
        "Password": str,
        "SshKey": str,
        "Revision": str,
    },
    total=False,
)

_RequiredSslConfigurationTypeDef = TypedDict(
    "_RequiredSslConfigurationTypeDef",
    {
        "Certificate": str,
        "PrivateKey": str,
    },
)
_OptionalSslConfigurationTypeDef = TypedDict(
    "_OptionalSslConfigurationTypeDef",
    {
        "Chain": str,
    },
    total=False,
)

class SslConfigurationTypeDef(_RequiredSslConfigurationTypeDef, _OptionalSslConfigurationTypeDef):
    pass

AssignInstanceRequestRequestTypeDef = TypedDict(
    "AssignInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
        "LayerIds": Sequence[str],
    },
)

_RequiredAssignVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredAssignVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalAssignVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalAssignVolumeRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)

class AssignVolumeRequestRequestTypeDef(
    _RequiredAssignVolumeRequestRequestTypeDef, _OptionalAssignVolumeRequestRequestTypeDef
):
    pass

_RequiredAssociateElasticIpRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)
_OptionalAssociateElasticIpRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateElasticIpRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)

class AssociateElasticIpRequestRequestTypeDef(
    _RequiredAssociateElasticIpRequestRequestTypeDef,
    _OptionalAssociateElasticIpRequestRequestTypeDef,
):
    pass

AttachElasticLoadBalancerRequestRequestTypeDef = TypedDict(
    "AttachElasticLoadBalancerRequestRequestTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "LayerId": str,
    },
)

AutoScalingThresholdsTypeDef = TypedDict(
    "AutoScalingThresholdsTypeDef",
    {
        "InstanceCount": int,
        "ThresholdsWaitTime": int,
        "IgnoreMetricsTime": int,
        "CpuThreshold": float,
        "MemoryThreshold": float,
        "LoadThreshold": float,
        "Alarms": List[str],
    },
    total=False,
)

EbsBlockDeviceTypeDef = TypedDict(
    "EbsBlockDeviceTypeDef",
    {
        "SnapshotId": str,
        "Iops": int,
        "VolumeSize": int,
        "VolumeType": VolumeTypeType,
        "DeleteOnTermination": bool,
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

ChefConfigurationTypeDef = TypedDict(
    "ChefConfigurationTypeDef",
    {
        "ManageBerkshelf": bool,
        "BerkshelfVersion": str,
    },
    total=False,
)

CloudWatchLogsLogStreamTypeDef = TypedDict(
    "CloudWatchLogsLogStreamTypeDef",
    {
        "LogGroupName": str,
        "DatetimeFormat": str,
        "TimeZone": CloudWatchLogsTimeZoneType,
        "File": str,
        "FileFingerprintLines": str,
        "MultiLineStartPattern": str,
        "InitialPosition": CloudWatchLogsInitialPositionType,
        "Encoding": CloudWatchLogsEncodingType,
        "BufferDuration": int,
        "BatchCount": int,
        "BatchSize": int,
    },
    total=False,
)

CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "DeploymentId": str,
        "CreatedAt": str,
        "AcknowledgedAt": str,
        "CompletedAt": str,
        "Status": str,
        "ExitCode": int,
        "LogUrl": str,
        "Type": str,
    },
    total=False,
)

_RequiredDeploymentCommandTypeDef = TypedDict(
    "_RequiredDeploymentCommandTypeDef",
    {
        "Name": DeploymentCommandNameType,
    },
)
_OptionalDeploymentCommandTypeDef = TypedDict(
    "_OptionalDeploymentCommandTypeDef",
    {
        "Args": Mapping[str, Sequence[str]],
    },
    total=False,
)

class DeploymentCommandTypeDef(
    _RequiredDeploymentCommandTypeDef, _OptionalDeploymentCommandTypeDef
):
    pass

RecipesTypeDef = TypedDict(
    "RecipesTypeDef",
    {
        "Setup": Sequence[str],
        "Configure": Sequence[str],
        "Deploy": Sequence[str],
        "Undeploy": Sequence[str],
        "Shutdown": Sequence[str],
    },
    total=False,
)

_RequiredVolumeConfigurationTypeDef = TypedDict(
    "_RequiredVolumeConfigurationTypeDef",
    {
        "MountPoint": str,
        "NumberOfDisks": int,
        "Size": int,
    },
)
_OptionalVolumeConfigurationTypeDef = TypedDict(
    "_OptionalVolumeConfigurationTypeDef",
    {
        "RaidLevel": int,
        "VolumeType": str,
        "Iops": int,
        "Encrypted": bool,
    },
    total=False,
)

class VolumeConfigurationTypeDef(
    _RequiredVolumeConfigurationTypeDef, _OptionalVolumeConfigurationTypeDef
):
    pass

_RequiredCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)
_OptionalCreateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserProfileRequestRequestTypeDef",
    {
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)

class CreateUserProfileRequestRequestTypeDef(
    _RequiredCreateUserProfileRequestRequestTypeDef, _OptionalCreateUserProfileRequestRequestTypeDef
):
    pass

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "AppId": str,
    },
)

_RequiredDeleteInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDeleteInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteInstanceRequestRequestTypeDef",
    {
        "DeleteElasticIp": bool,
        "DeleteVolumes": bool,
    },
    total=False,
)

class DeleteInstanceRequestRequestTypeDef(
    _RequiredDeleteInstanceRequestRequestTypeDef, _OptionalDeleteInstanceRequestRequestTypeDef
):
    pass

DeleteLayerRequestRequestTypeDef = TypedDict(
    "DeleteLayerRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)

DeleteStackRequestRequestTypeDef = TypedDict(
    "DeleteStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DeleteUserProfileRequestRequestTypeDef = TypedDict(
    "DeleteUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)

DeregisterEcsClusterRequestRequestTypeDef = TypedDict(
    "DeregisterEcsClusterRequestRequestTypeDef",
    {
        "EcsClusterArn": str,
    },
)

DeregisterElasticIpRequestRequestTypeDef = TypedDict(
    "DeregisterElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)

DeregisterInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DeregisterRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterRdsDbInstanceRequestRequestTypeDef",
    {
        "RdsDbInstanceArn": str,
    },
)

DeregisterVolumeRequestRequestTypeDef = TypedDict(
    "DeregisterVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
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

DescribeAppsRequestRequestTypeDef = TypedDict(
    "DescribeAppsRequestRequestTypeDef",
    {
        "StackId": str,
        "AppIds": Sequence[str],
    },
    total=False,
)

DescribeCommandsRequestRequestTypeDef = TypedDict(
    "DescribeCommandsRequestRequestTypeDef",
    {
        "DeploymentId": str,
        "InstanceId": str,
        "CommandIds": Sequence[str],
    },
    total=False,
)

DescribeDeploymentsRequestRequestTypeDef = TypedDict(
    "DescribeDeploymentsRequestRequestTypeDef",
    {
        "StackId": str,
        "AppId": str,
        "DeploymentIds": Sequence[str],
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

DescribeEcsClustersRequestRequestTypeDef = TypedDict(
    "DescribeEcsClustersRequestRequestTypeDef",
    {
        "EcsClusterArns": Sequence[str],
        "StackId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

EcsClusterTypeDef = TypedDict(
    "EcsClusterTypeDef",
    {
        "EcsClusterArn": str,
        "EcsClusterName": str,
        "StackId": str,
        "RegisteredAt": str,
    },
    total=False,
)

DescribeElasticIpsRequestRequestTypeDef = TypedDict(
    "DescribeElasticIpsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "Ips": Sequence[str],
    },
    total=False,
)

ElasticIpTypeDef = TypedDict(
    "ElasticIpTypeDef",
    {
        "Ip": str,
        "Name": str,
        "Domain": str,
        "Region": str,
        "InstanceId": str,
    },
    total=False,
)

DescribeElasticLoadBalancersRequestRequestTypeDef = TypedDict(
    "DescribeElasticLoadBalancersRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
    },
    total=False,
)

ElasticLoadBalancerTypeDef = TypedDict(
    "ElasticLoadBalancerTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "Region": str,
        "DnsName": str,
        "StackId": str,
        "LayerId": str,
        "VpcId": str,
        "AvailabilityZones": List[str],
        "SubnetIds": List[str],
        "Ec2InstanceIds": List[str],
    },
    total=False,
)

DescribeInstancesRequestRequestTypeDef = TypedDict(
    "DescribeInstancesRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
    },
    total=False,
)

DescribeLayersRequestRequestTypeDef = TypedDict(
    "DescribeLayersRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
    },
    total=False,
)

DescribeLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "DescribeLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "LayerIds": Sequence[str],
    },
)

SelfUserProfileTypeDef = TypedDict(
    "SelfUserProfileTypeDef",
    {
        "IamUserArn": str,
        "Name": str,
        "SshUsername": str,
        "SshPublicKey": str,
    },
    total=False,
)

DescribePermissionsRequestRequestTypeDef = TypedDict(
    "DescribePermissionsRequestRequestTypeDef",
    {
        "IamUserArn": str,
        "StackId": str,
    },
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "StackId": str,
        "IamUserArn": str,
        "AllowSsh": bool,
        "AllowSudo": bool,
        "Level": str,
    },
    total=False,
)

DescribeRaidArraysRequestRequestTypeDef = TypedDict(
    "DescribeRaidArraysRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "RaidArrayIds": Sequence[str],
    },
    total=False,
)

RaidArrayTypeDef = TypedDict(
    "RaidArrayTypeDef",
    {
        "RaidArrayId": str,
        "InstanceId": str,
        "Name": str,
        "RaidLevel": int,
        "NumberOfDisks": int,
        "Size": int,
        "Device": str,
        "MountPoint": str,
        "AvailabilityZone": str,
        "CreatedAt": str,
        "StackId": str,
        "VolumeType": str,
        "Iops": int,
    },
    total=False,
)

_RequiredDescribeRdsDbInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRdsDbInstancesRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalDescribeRdsDbInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRdsDbInstancesRequestRequestTypeDef",
    {
        "RdsDbInstanceArns": Sequence[str],
    },
    total=False,
)

class DescribeRdsDbInstancesRequestRequestTypeDef(
    _RequiredDescribeRdsDbInstancesRequestRequestTypeDef,
    _OptionalDescribeRdsDbInstancesRequestRequestTypeDef,
):
    pass

RdsDbInstanceTypeDef = TypedDict(
    "RdsDbInstanceTypeDef",
    {
        "RdsDbInstanceArn": str,
        "DbInstanceIdentifier": str,
        "DbUser": str,
        "DbPassword": str,
        "Region": str,
        "Address": str,
        "Engine": str,
        "StackId": str,
        "MissingOnRds": bool,
    },
    total=False,
)

DescribeServiceErrorsRequestRequestTypeDef = TypedDict(
    "DescribeServiceErrorsRequestRequestTypeDef",
    {
        "StackId": str,
        "InstanceId": str,
        "ServiceErrorIds": Sequence[str],
    },
    total=False,
)

ServiceErrorTypeDef = TypedDict(
    "ServiceErrorTypeDef",
    {
        "ServiceErrorId": str,
        "StackId": str,
        "InstanceId": str,
        "Type": str,
        "Message": str,
        "CreatedAt": str,
    },
    total=False,
)

DescribeStackProvisioningParametersRequestRequestTypeDef = TypedDict(
    "DescribeStackProvisioningParametersRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DescribeStackSummaryRequestRequestTypeDef = TypedDict(
    "DescribeStackSummaryRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

DescribeStacksRequestRequestTypeDef = TypedDict(
    "DescribeStacksRequestRequestTypeDef",
    {
        "StackIds": Sequence[str],
    },
    total=False,
)

DescribeTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "DescribeTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
)

DescribeUserProfilesRequestRequestTypeDef = TypedDict(
    "DescribeUserProfilesRequestRequestTypeDef",
    {
        "IamUserArns": Sequence[str],
    },
    total=False,
)

UserProfileTypeDef = TypedDict(
    "UserProfileTypeDef",
    {
        "IamUserArn": str,
        "Name": str,
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)

DescribeVolumesRequestRequestTypeDef = TypedDict(
    "DescribeVolumesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StackId": str,
        "RaidArrayId": str,
        "VolumeIds": Sequence[str],
    },
    total=False,
)

VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "VolumeId": str,
        "Ec2VolumeId": str,
        "Name": str,
        "RaidArrayId": str,
        "InstanceId": str,
        "Status": str,
        "Size": int,
        "Device": str,
        "MountPoint": str,
        "Region": str,
        "AvailabilityZone": str,
        "VolumeType": str,
        "Iops": int,
        "Encrypted": bool,
    },
    total=False,
)

DetachElasticLoadBalancerRequestRequestTypeDef = TypedDict(
    "DetachElasticLoadBalancerRequestRequestTypeDef",
    {
        "ElasticLoadBalancerName": str,
        "LayerId": str,
    },
)

DisassociateElasticIpRequestRequestTypeDef = TypedDict(
    "DisassociateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)

GetHostnameSuggestionRequestRequestTypeDef = TypedDict(
    "GetHostnameSuggestionRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)

_RequiredGrantAccessRequestRequestTypeDef = TypedDict(
    "_RequiredGrantAccessRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalGrantAccessRequestRequestTypeDef = TypedDict(
    "_OptionalGrantAccessRequestRequestTypeDef",
    {
        "ValidForInMinutes": int,
    },
    total=False,
)

class GrantAccessRequestRequestTypeDef(
    _RequiredGrantAccessRequestRequestTypeDef, _OptionalGrantAccessRequestRequestTypeDef
):
    pass

TemporaryCredentialTypeDef = TypedDict(
    "TemporaryCredentialTypeDef",
    {
        "Username": str,
        "Password": str,
        "ValidForInMinutes": int,
        "InstanceId": str,
    },
    total=False,
)

InstanceIdentityTypeDef = TypedDict(
    "InstanceIdentityTypeDef",
    {
        "Document": str,
        "Signature": str,
    },
    total=False,
)

ReportedOsTypeDef = TypedDict(
    "ReportedOsTypeDef",
    {
        "Family": str,
        "Name": str,
        "Version": str,
    },
    total=False,
)

InstancesCountTypeDef = TypedDict(
    "InstancesCountTypeDef",
    {
        "Assigning": int,
        "Booting": int,
        "ConnectionLost": int,
        "Deregistering": int,
        "Online": int,
        "Pending": int,
        "Rebooting": int,
        "Registered": int,
        "Registering": int,
        "Requested": int,
        "RunningSetup": int,
        "SetupFailed": int,
        "ShuttingDown": int,
        "StartFailed": int,
        "StopFailed": int,
        "Stopped": int,
        "Stopping": int,
        "Terminated": int,
        "Terminating": int,
        "Unassigning": int,
    },
    total=False,
)

ShutdownEventConfigurationTypeDef = TypedDict(
    "ShutdownEventConfigurationTypeDef",
    {
        "ExecutionTimeout": int,
        "DelayUntilElbConnectionsDrained": bool,
    },
    total=False,
)

_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass

OperatingSystemConfigurationManagerTypeDef = TypedDict(
    "OperatingSystemConfigurationManagerTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)

RebootInstanceRequestRequestTypeDef = TypedDict(
    "RebootInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

RegisterEcsClusterRequestRequestTypeDef = TypedDict(
    "RegisterEcsClusterRequestRequestTypeDef",
    {
        "EcsClusterArn": str,
        "StackId": str,
    },
)

RegisterElasticIpRequestRequestTypeDef = TypedDict(
    "RegisterElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
        "StackId": str,
    },
)

RegisterRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "RegisterRdsDbInstanceRequestRequestTypeDef",
    {
        "StackId": str,
        "RdsDbInstanceArn": str,
        "DbUser": str,
        "DbPassword": str,
    },
)

_RequiredRegisterVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterVolumeRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalRegisterVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterVolumeRequestRequestTypeDef",
    {
        "Ec2VolumeId": str,
    },
    total=False,
)

class RegisterVolumeRequestRequestTypeDef(
    _RequiredRegisterVolumeRequestRequestTypeDef, _OptionalRegisterVolumeRequestRequestTypeDef
):
    pass

ServiceResourceLayerRequestTypeDef = TypedDict(
    "ServiceResourceLayerRequestTypeDef",
    {
        "id": str,
    },
)

ServiceResourceStackRequestTypeDef = TypedDict(
    "ServiceResourceStackRequestTypeDef",
    {
        "id": str,
    },
)

ServiceResourceStackSummaryRequestTypeDef = TypedDict(
    "ServiceResourceStackSummaryRequestTypeDef",
    {
        "stack_id": str,
    },
)

_RequiredSetPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredSetPermissionRequestRequestTypeDef",
    {
        "StackId": str,
        "IamUserArn": str,
    },
)
_OptionalSetPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalSetPermissionRequestRequestTypeDef",
    {
        "AllowSsh": bool,
        "AllowSudo": bool,
        "Level": str,
    },
    total=False,
)

class SetPermissionRequestRequestTypeDef(
    _RequiredSetPermissionRequestRequestTypeDef, _OptionalSetPermissionRequestRequestTypeDef
):
    pass

WeeklyAutoScalingScheduleTypeDef = TypedDict(
    "WeeklyAutoScalingScheduleTypeDef",
    {
        "Monday": Dict[str, str],
        "Tuesday": Dict[str, str],
        "Wednesday": Dict[str, str],
        "Thursday": Dict[str, str],
        "Friday": Dict[str, str],
        "Saturday": Dict[str, str],
        "Sunday": Dict[str, str],
    },
    total=False,
)

StartInstanceRequestRequestTypeDef = TypedDict(
    "StartInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

StartStackRequestRequestTypeDef = TypedDict(
    "StartStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

_RequiredStopInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredStopInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalStopInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalStopInstanceRequestRequestTypeDef",
    {
        "Force": bool,
    },
    total=False,
)

class StopInstanceRequestRequestTypeDef(
    _RequiredStopInstanceRequestRequestTypeDef, _OptionalStopInstanceRequestRequestTypeDef
):
    pass

StopStackRequestRequestTypeDef = TypedDict(
    "StopStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UnassignInstanceRequestRequestTypeDef = TypedDict(
    "UnassignInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

UnassignVolumeRequestRequestTypeDef = TypedDict(
    "UnassignVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateElasticIpRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateElasticIpRequestRequestTypeDef",
    {
        "ElasticIp": str,
    },
)
_OptionalUpdateElasticIpRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateElasticIpRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)

class UpdateElasticIpRequestRequestTypeDef(
    _RequiredUpdateElasticIpRequestRequestTypeDef, _OptionalUpdateElasticIpRequestRequestTypeDef
):
    pass

_RequiredUpdateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalUpdateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInstanceRequestRequestTypeDef",
    {
        "LayerIds": Sequence[str],
        "InstanceType": str,
        "AutoScalingType": AutoScalingTypeType,
        "Hostname": str,
        "Os": str,
        "AmiId": str,
        "SshKeyName": str,
        "Architecture": ArchitectureType,
        "InstallUpdatesOnBoot": bool,
        "EbsOptimized": bool,
        "AgentVersion": str,
    },
    total=False,
)

class UpdateInstanceRequestRequestTypeDef(
    _RequiredUpdateInstanceRequestRequestTypeDef, _OptionalUpdateInstanceRequestRequestTypeDef
):
    pass

UpdateMyUserProfileRequestRequestTypeDef = TypedDict(
    "UpdateMyUserProfileRequestRequestTypeDef",
    {
        "SshPublicKey": str,
    },
    total=False,
)

_RequiredUpdateRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRdsDbInstanceRequestRequestTypeDef",
    {
        "RdsDbInstanceArn": str,
    },
)
_OptionalUpdateRdsDbInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRdsDbInstanceRequestRequestTypeDef",
    {
        "DbUser": str,
        "DbPassword": str,
    },
    total=False,
)

class UpdateRdsDbInstanceRequestRequestTypeDef(
    _RequiredUpdateRdsDbInstanceRequestRequestTypeDef,
    _OptionalUpdateRdsDbInstanceRequestRequestTypeDef,
):
    pass

_RequiredUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserProfileRequestRequestTypeDef",
    {
        "IamUserArn": str,
    },
)
_OptionalUpdateUserProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserProfileRequestRequestTypeDef",
    {
        "SshUsername": str,
        "SshPublicKey": str,
        "AllowSelfManagement": bool,
    },
    total=False,
)

class UpdateUserProfileRequestRequestTypeDef(
    _RequiredUpdateUserProfileRequestRequestTypeDef, _OptionalUpdateUserProfileRequestRequestTypeDef
):
    pass

_RequiredUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
    },
)
_OptionalUpdateVolumeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVolumeRequestRequestTypeDef",
    {
        "Name": str,
        "MountPoint": str,
    },
    total=False,
)

class UpdateVolumeRequestRequestTypeDef(
    _RequiredUpdateVolumeRequestRequestTypeDef, _OptionalUpdateVolumeRequestRequestTypeDef
):
    pass

AgentVersionTypeDef = TypedDict(
    "AgentVersionTypeDef",
    {
        "Version": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
    },
    total=False,
)

DescribeAgentVersionsRequestRequestTypeDef = TypedDict(
    "DescribeAgentVersionsRequestRequestTypeDef",
    {
        "StackId": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
    },
    total=False,
)

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "AppId": str,
        "StackId": str,
        "Shortname": str,
        "Name": str,
        "Description": str,
        "DataSources": List[DataSourceTypeDef],
        "Type": AppTypeType,
        "AppSource": SourceTypeDef,
        "Domains": List[str],
        "EnableSsl": bool,
        "SslConfiguration": SslConfigurationTypeDef,
        "Attributes": Dict[AppAttributesKeysType, str],
        "CreatedAt": str,
        "Environment": List[EnvironmentVariableTypeDef],
    },
    total=False,
)

_RequiredCreateAppRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppRequestRequestTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Type": AppTypeType,
    },
)
_OptionalCreateAppRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppRequestRequestTypeDef",
    {
        "Shortname": str,
        "Description": str,
        "DataSources": Sequence[DataSourceTypeDef],
        "AppSource": SourceTypeDef,
        "Domains": Sequence[str],
        "EnableSsl": bool,
        "SslConfiguration": SslConfigurationTypeDef,
        "Attributes": Mapping[AppAttributesKeysType, str],
        "Environment": Sequence[EnvironmentVariableTypeDef],
    },
    total=False,
)

class CreateAppRequestRequestTypeDef(
    _RequiredCreateAppRequestRequestTypeDef, _OptionalCreateAppRequestRequestTypeDef
):
    pass

_RequiredUpdateAppRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalUpdateAppRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "DataSources": Sequence[DataSourceTypeDef],
        "Type": AppTypeType,
        "AppSource": SourceTypeDef,
        "Domains": Sequence[str],
        "EnableSsl": bool,
        "SslConfiguration": SslConfigurationTypeDef,
        "Attributes": Mapping[AppAttributesKeysType, str],
        "Environment": Sequence[EnvironmentVariableTypeDef],
    },
    total=False,
)

class UpdateAppRequestRequestTypeDef(
    _RequiredUpdateAppRequestRequestTypeDef, _OptionalUpdateAppRequestRequestTypeDef
):
    pass

LoadBasedAutoScalingConfigurationTypeDef = TypedDict(
    "LoadBasedAutoScalingConfigurationTypeDef",
    {
        "LayerId": str,
        "Enable": bool,
        "UpScaling": AutoScalingThresholdsTypeDef,
        "DownScaling": AutoScalingThresholdsTypeDef,
    },
    total=False,
)

_RequiredSetLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_RequiredSetLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)
_OptionalSetLoadBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_OptionalSetLoadBasedAutoScalingRequestRequestTypeDef",
    {
        "Enable": bool,
        "UpScaling": AutoScalingThresholdsTypeDef,
        "DownScaling": AutoScalingThresholdsTypeDef,
    },
    total=False,
)

class SetLoadBasedAutoScalingRequestRequestTypeDef(
    _RequiredSetLoadBasedAutoScalingRequestRequestTypeDef,
    _OptionalSetLoadBasedAutoScalingRequestRequestTypeDef,
):
    pass

BlockDeviceMappingTypeDef = TypedDict(
    "BlockDeviceMappingTypeDef",
    {
        "DeviceName": str,
        "NoDevice": str,
        "VirtualName": str,
        "Ebs": EbsBlockDeviceTypeDef,
    },
    total=False,
)

ChefConfigurationResponseMetadataTypeDef = TypedDict(
    "ChefConfigurationResponseMetadataTypeDef",
    {
        "ManageBerkshelf": bool,
        "BerkshelfVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CloneStackResultTypeDef = TypedDict(
    "CloneStackResultTypeDef",
    {
        "StackId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppResultTypeDef = TypedDict(
    "CreateAppResultTypeDef",
    {
        "AppId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentResultTypeDef = TypedDict(
    "CreateDeploymentResultTypeDef",
    {
        "DeploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInstanceResultTypeDef = TypedDict(
    "CreateInstanceResultTypeDef",
    {
        "InstanceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLayerResultTypeDef = TypedDict(
    "CreateLayerResultTypeDef",
    {
        "LayerId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStackResultTypeDef = TypedDict(
    "CreateStackResultTypeDef",
    {
        "StackId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserProfileResultTypeDef = TypedDict(
    "CreateUserProfileResultTypeDef",
    {
        "IamUserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStackProvisioningParametersResultTypeDef = TypedDict(
    "DescribeStackProvisioningParametersResultTypeDef",
    {
        "AgentInstallerUrl": str,
        "Parameters": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHostnameSuggestionResultTypeDef = TypedDict(
    "GetHostnameSuggestionResultTypeDef",
    {
        "LayerId": str,
        "Hostname": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstancesCountResponseMetadataTypeDef = TypedDict(
    "InstancesCountResponseMetadataTypeDef",
    {
        "Assigning": int,
        "Booting": int,
        "ConnectionLost": int,
        "Deregistering": int,
        "Online": int,
        "Pending": int,
        "Rebooting": int,
        "Registered": int,
        "Registering": int,
        "Requested": int,
        "RunningSetup": int,
        "SetupFailed": int,
        "ShuttingDown": int,
        "StartFailed": int,
        "StopFailed": int,
        "Stopped": int,
        "Stopping": int,
        "Terminated": int,
        "Terminating": int,
        "Unassigning": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsResultTypeDef = TypedDict(
    "ListTagsResultTypeDef",
    {
        "Tags": Dict[str, str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecipesResponseMetadataTypeDef = TypedDict(
    "RecipesResponseMetadataTypeDef",
    {
        "Setup": List[str],
        "Configure": List[str],
        "Deploy": List[str],
        "Undeploy": List[str],
        "Shutdown": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterEcsClusterResultTypeDef = TypedDict(
    "RegisterEcsClusterResultTypeDef",
    {
        "EcsClusterArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterElasticIpResultTypeDef = TypedDict(
    "RegisterElasticIpResultTypeDef",
    {
        "ElasticIp": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterInstanceResultTypeDef = TypedDict(
    "RegisterInstanceResultTypeDef",
    {
        "InstanceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterVolumeResultTypeDef = TypedDict(
    "RegisterVolumeResultTypeDef",
    {
        "VolumeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceResponseMetadataTypeDef = TypedDict(
    "SourceResponseMetadataTypeDef",
    {
        "Type": SourceTypeType,
        "Url": str,
        "Username": str,
        "Password": str,
        "SshKey": str,
        "Revision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StackConfigurationManagerResponseMetadataTypeDef = TypedDict(
    "StackConfigurationManagerResponseMetadataTypeDef",
    {
        "Name": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCloneStackRequestRequestTypeDef = TypedDict(
    "_RequiredCloneStackRequestRequestTypeDef",
    {
        "SourceStackId": str,
        "ServiceRoleArn": str,
    },
)
_OptionalCloneStackRequestRequestTypeDef = TypedDict(
    "_OptionalCloneStackRequestRequestTypeDef",
    {
        "Name": str,
        "Region": str,
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
        "ChefConfiguration": ChefConfigurationTypeDef,
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": SourceTypeDef,
        "DefaultSshKeyName": str,
        "ClonePermissions": bool,
        "CloneAppIds": Sequence[str],
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)

class CloneStackRequestRequestTypeDef(
    _RequiredCloneStackRequestRequestTypeDef, _OptionalCloneStackRequestRequestTypeDef
):
    pass

_RequiredCreateStackRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStackRequestRequestTypeDef",
    {
        "Name": str,
        "Region": str,
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
    },
)
_OptionalCreateStackRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStackRequestRequestTypeDef",
    {
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
        "ChefConfiguration": ChefConfigurationTypeDef,
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": SourceTypeDef,
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)

class CreateStackRequestRequestTypeDef(
    _RequiredCreateStackRequestRequestTypeDef, _OptionalCreateStackRequestRequestTypeDef
):
    pass

_RequiredCreateStackRequestServiceResourceCreateStackTypeDef = TypedDict(
    "_RequiredCreateStackRequestServiceResourceCreateStackTypeDef",
    {
        "Name": str,
        "Region": str,
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
    },
)
_OptionalCreateStackRequestServiceResourceCreateStackTypeDef = TypedDict(
    "_OptionalCreateStackRequestServiceResourceCreateStackTypeDef",
    {
        "VpcId": str,
        "Attributes": Mapping[Literal["Color"], str],
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
        "ChefConfiguration": ChefConfigurationTypeDef,
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": SourceTypeDef,
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)

class CreateStackRequestServiceResourceCreateStackTypeDef(
    _RequiredCreateStackRequestServiceResourceCreateStackTypeDef,
    _OptionalCreateStackRequestServiceResourceCreateStackTypeDef,
):
    pass

StackTypeDef = TypedDict(
    "StackTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Arn": str,
        "Region": str,
        "VpcId": str,
        "Attributes": Dict[Literal["Color"], str],
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
        "ChefConfiguration": ChefConfigurationTypeDef,
        "UseCustomCookbooks": bool,
        "UseOpsworksSecurityGroups": bool,
        "CustomCookbooksSource": SourceTypeDef,
        "DefaultSshKeyName": str,
        "CreatedAt": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "AgentVersion": str,
    },
    total=False,
)

_RequiredUpdateStackRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStackRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalUpdateStackRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStackRequestRequestTypeDef",
    {
        "Name": str,
        "Attributes": Mapping[Literal["Color"], str],
        "ServiceRoleArn": str,
        "DefaultInstanceProfileArn": str,
        "DefaultOs": str,
        "HostnameTheme": str,
        "DefaultAvailabilityZone": str,
        "DefaultSubnetId": str,
        "CustomJson": str,
        "ConfigurationManager": StackConfigurationManagerTypeDef,
        "ChefConfiguration": ChefConfigurationTypeDef,
        "UseCustomCookbooks": bool,
        "CustomCookbooksSource": SourceTypeDef,
        "DefaultSshKeyName": str,
        "DefaultRootDeviceType": RootDeviceTypeType,
        "UseOpsworksSecurityGroups": bool,
        "AgentVersion": str,
    },
    total=False,
)

class UpdateStackRequestRequestTypeDef(
    _RequiredUpdateStackRequestRequestTypeDef, _OptionalUpdateStackRequestRequestTypeDef
):
    pass

CloudWatchLogsConfigurationResponseMetadataTypeDef = TypedDict(
    "CloudWatchLogsConfigurationResponseMetadataTypeDef",
    {
        "Enabled": bool,
        "LogStreams": List[CloudWatchLogsLogStreamTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CloudWatchLogsConfigurationTypeDef = TypedDict(
    "CloudWatchLogsConfigurationTypeDef",
    {
        "Enabled": bool,
        "LogStreams": Sequence[CloudWatchLogsLogStreamTypeDef],
    },
    total=False,
)

DescribeCommandsResultTypeDef = TypedDict(
    "DescribeCommandsResultTypeDef",
    {
        "Commands": List[CommandTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "StackId": str,
        "Command": DeploymentCommandTypeDef,
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "AppId": str,
        "InstanceIds": Sequence[str],
        "LayerIds": Sequence[str],
        "Comment": str,
        "CustomJson": str,
    },
    total=False,
)

class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "DeploymentId": str,
        "StackId": str,
        "AppId": str,
        "CreatedAt": str,
        "CompletedAt": str,
        "Duration": int,
        "IamUserArn": str,
        "Comment": str,
        "Command": DeploymentCommandTypeDef,
        "Status": str,
        "CustomJson": str,
        "InstanceIds": List[str],
    },
    total=False,
)

DescribeAppsRequestAppExistsWaitTypeDef = TypedDict(
    "DescribeAppsRequestAppExistsWaitTypeDef",
    {
        "StackId": str,
        "AppIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef = TypedDict(
    "DescribeDeploymentsRequestDeploymentSuccessfulWaitTypeDef",
    {
        "StackId": str,
        "AppId": str,
        "DeploymentIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeInstancesRequestInstanceOnlineWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceOnlineWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeInstancesRequestInstanceRegisteredWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceRegisteredWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeInstancesRequestInstanceStoppedWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceStoppedWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeInstancesRequestInstanceTerminatedWaitTypeDef = TypedDict(
    "DescribeInstancesRequestInstanceTerminatedWaitTypeDef",
    {
        "StackId": str,
        "LayerId": str,
        "InstanceIds": Sequence[str],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef = TypedDict(
    "DescribeEcsClustersRequestDescribeEcsClustersPaginateTypeDef",
    {
        "EcsClusterArns": Sequence[str],
        "StackId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEcsClustersResultTypeDef = TypedDict(
    "DescribeEcsClustersResultTypeDef",
    {
        "EcsClusters": List[EcsClusterTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeElasticIpsResultTypeDef = TypedDict(
    "DescribeElasticIpsResultTypeDef",
    {
        "ElasticIps": List[ElasticIpTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeElasticLoadBalancersResultTypeDef = TypedDict(
    "DescribeElasticLoadBalancersResultTypeDef",
    {
        "ElasticLoadBalancers": List[ElasticLoadBalancerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMyUserProfileResultTypeDef = TypedDict(
    "DescribeMyUserProfileResultTypeDef",
    {
        "UserProfile": SelfUserProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePermissionsResultTypeDef = TypedDict(
    "DescribePermissionsResultTypeDef",
    {
        "Permissions": List[PermissionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRaidArraysResultTypeDef = TypedDict(
    "DescribeRaidArraysResultTypeDef",
    {
        "RaidArrays": List[RaidArrayTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRdsDbInstancesResultTypeDef = TypedDict(
    "DescribeRdsDbInstancesResultTypeDef",
    {
        "RdsDbInstances": List[RdsDbInstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeServiceErrorsResultTypeDef = TypedDict(
    "DescribeServiceErrorsResultTypeDef",
    {
        "ServiceErrors": List[ServiceErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserProfilesResultTypeDef = TypedDict(
    "DescribeUserProfilesResultTypeDef",
    {
        "UserProfiles": List[UserProfileTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVolumesResultTypeDef = TypedDict(
    "DescribeVolumesResultTypeDef",
    {
        "Volumes": List[VolumeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GrantAccessResultTypeDef = TypedDict(
    "GrantAccessResultTypeDef",
    {
        "TemporaryCredential": TemporaryCredentialTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterInstanceRequestRequestTypeDef",
    {
        "StackId": str,
    },
)
_OptionalRegisterInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterInstanceRequestRequestTypeDef",
    {
        "Hostname": str,
        "PublicIp": str,
        "PrivateIp": str,
        "RsaPublicKey": str,
        "RsaPublicKeyFingerprint": str,
        "InstanceIdentity": InstanceIdentityTypeDef,
    },
    total=False,
)

class RegisterInstanceRequestRequestTypeDef(
    _RequiredRegisterInstanceRequestRequestTypeDef, _OptionalRegisterInstanceRequestRequestTypeDef
):
    pass

StackSummaryTypeDef = TypedDict(
    "StackSummaryTypeDef",
    {
        "StackId": str,
        "Name": str,
        "Arn": str,
        "LayersCount": int,
        "AppsCount": int,
        "InstancesCount": InstancesCountTypeDef,
    },
    total=False,
)

LifecycleEventConfigurationResponseMetadataTypeDef = TypedDict(
    "LifecycleEventConfigurationResponseMetadataTypeDef",
    {
        "Shutdown": ShutdownEventConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleEventConfigurationTypeDef = TypedDict(
    "LifecycleEventConfigurationTypeDef",
    {
        "Shutdown": ShutdownEventConfigurationTypeDef,
    },
    total=False,
)

OperatingSystemTypeDef = TypedDict(
    "OperatingSystemTypeDef",
    {
        "Name": str,
        "Id": str,
        "Type": str,
        "ConfigurationManagers": List[OperatingSystemConfigurationManagerTypeDef],
        "ReportedName": str,
        "ReportedVersion": str,
        "Supported": bool,
    },
    total=False,
)

_RequiredSetTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_RequiredSetTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSetTimeBasedAutoScalingRequestRequestTypeDef = TypedDict(
    "_OptionalSetTimeBasedAutoScalingRequestRequestTypeDef",
    {
        "AutoScalingSchedule": WeeklyAutoScalingScheduleTypeDef,
    },
    total=False,
)

class SetTimeBasedAutoScalingRequestRequestTypeDef(
    _RequiredSetTimeBasedAutoScalingRequestRequestTypeDef,
    _OptionalSetTimeBasedAutoScalingRequestRequestTypeDef,
):
    pass

TimeBasedAutoScalingConfigurationTypeDef = TypedDict(
    "TimeBasedAutoScalingConfigurationTypeDef",
    {
        "InstanceId": str,
        "AutoScalingSchedule": WeeklyAutoScalingScheduleTypeDef,
    },
    total=False,
)

DescribeAgentVersionsResultTypeDef = TypedDict(
    "DescribeAgentVersionsResultTypeDef",
    {
        "AgentVersions": List[AgentVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppsResultTypeDef = TypedDict(
    "DescribeAppsResultTypeDef",
    {
        "Apps": List[AppTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoadBasedAutoScalingResultTypeDef = TypedDict(
    "DescribeLoadBasedAutoScalingResultTypeDef",
    {
        "LoadBasedAutoScalingConfigurations": List[LoadBasedAutoScalingConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInstanceRequestRequestTypeDef",
    {
        "StackId": str,
        "LayerIds": Sequence[str],
        "InstanceType": str,
    },
)
_OptionalCreateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInstanceRequestRequestTypeDef",
    {
        "AutoScalingType": AutoScalingTypeType,
        "Hostname": str,
        "Os": str,
        "AmiId": str,
        "SshKeyName": str,
        "AvailabilityZone": str,
        "VirtualizationType": str,
        "SubnetId": str,
        "Architecture": ArchitectureType,
        "RootDeviceType": RootDeviceTypeType,
        "BlockDeviceMappings": Sequence[BlockDeviceMappingTypeDef],
        "InstallUpdatesOnBoot": bool,
        "EbsOptimized": bool,
        "AgentVersion": str,
        "Tenancy": str,
    },
    total=False,
)

class CreateInstanceRequestRequestTypeDef(
    _RequiredCreateInstanceRequestRequestTypeDef, _OptionalCreateInstanceRequestRequestTypeDef
):
    pass

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "AgentVersion": str,
        "AmiId": str,
        "Architecture": ArchitectureType,
        "Arn": str,
        "AutoScalingType": AutoScalingTypeType,
        "AvailabilityZone": str,
        "BlockDeviceMappings": List[BlockDeviceMappingTypeDef],
        "CreatedAt": str,
        "EbsOptimized": bool,
        "Ec2InstanceId": str,
        "EcsClusterArn": str,
        "EcsContainerInstanceArn": str,
        "ElasticIp": str,
        "Hostname": str,
        "InfrastructureClass": str,
        "InstallUpdatesOnBoot": bool,
        "InstanceId": str,
        "InstanceProfileArn": str,
        "InstanceType": str,
        "LastServiceErrorId": str,
        "LayerIds": List[str],
        "Os": str,
        "Platform": str,
        "PrivateDns": str,
        "PrivateIp": str,
        "PublicDns": str,
        "PublicIp": str,
        "RegisteredBy": str,
        "ReportedAgentVersion": str,
        "ReportedOs": ReportedOsTypeDef,
        "RootDeviceType": RootDeviceTypeType,
        "RootDeviceVolumeId": str,
        "SecurityGroupIds": List[str],
        "SshHostDsaKeyFingerprint": str,
        "SshHostRsaKeyFingerprint": str,
        "SshKeyName": str,
        "StackId": str,
        "Status": str,
        "SubnetId": str,
        "Tenancy": str,
        "VirtualizationType": VirtualizationTypeType,
    },
    total=False,
)

DescribeStacksResultTypeDef = TypedDict(
    "DescribeStacksResultTypeDef",
    {
        "Stacks": List[StackTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDeploymentsResultTypeDef = TypedDict(
    "DescribeDeploymentsResultTypeDef",
    {
        "Deployments": List[DeploymentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStackSummaryResultTypeDef = TypedDict(
    "DescribeStackSummaryResultTypeDef",
    {
        "StackSummary": StackSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLayerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLayerRequestRequestTypeDef",
    {
        "StackId": str,
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
    },
)
_OptionalCreateLayerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLayerRequestRequestTypeDef",
    {
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": CloudWatchLogsConfigurationTypeDef,
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence[VolumeConfigurationTypeDef],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": RecipesTypeDef,
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": LifecycleEventConfigurationTypeDef,
    },
    total=False,
)

class CreateLayerRequestRequestTypeDef(
    _RequiredCreateLayerRequestRequestTypeDef, _OptionalCreateLayerRequestRequestTypeDef
):
    pass

_RequiredCreateLayerRequestStackCreateLayerTypeDef = TypedDict(
    "_RequiredCreateLayerRequestStackCreateLayerTypeDef",
    {
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
    },
)
_OptionalCreateLayerRequestStackCreateLayerTypeDef = TypedDict(
    "_OptionalCreateLayerRequestStackCreateLayerTypeDef",
    {
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": CloudWatchLogsConfigurationTypeDef,
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence[VolumeConfigurationTypeDef],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": RecipesTypeDef,
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": LifecycleEventConfigurationTypeDef,
    },
    total=False,
)

class CreateLayerRequestStackCreateLayerTypeDef(
    _RequiredCreateLayerRequestStackCreateLayerTypeDef,
    _OptionalCreateLayerRequestStackCreateLayerTypeDef,
):
    pass

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "Arn": str,
        "StackId": str,
        "LayerId": str,
        "Type": LayerTypeType,
        "Name": str,
        "Shortname": str,
        "Attributes": Dict[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": CloudWatchLogsConfigurationTypeDef,
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": List[str],
        "DefaultSecurityGroupNames": List[str],
        "Packages": List[str],
        "VolumeConfigurations": List[VolumeConfigurationTypeDef],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "DefaultRecipes": RecipesTypeDef,
        "CustomRecipes": RecipesTypeDef,
        "CreatedAt": str,
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": LifecycleEventConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateLayerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLayerRequestRequestTypeDef",
    {
        "LayerId": str,
    },
)
_OptionalUpdateLayerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLayerRequestRequestTypeDef",
    {
        "Name": str,
        "Shortname": str,
        "Attributes": Mapping[LayerAttributesKeysType, str],
        "CloudWatchLogsConfiguration": CloudWatchLogsConfigurationTypeDef,
        "CustomInstanceProfileArn": str,
        "CustomJson": str,
        "CustomSecurityGroupIds": Sequence[str],
        "Packages": Sequence[str],
        "VolumeConfigurations": Sequence[VolumeConfigurationTypeDef],
        "EnableAutoHealing": bool,
        "AutoAssignElasticIps": bool,
        "AutoAssignPublicIps": bool,
        "CustomRecipes": RecipesTypeDef,
        "InstallUpdatesOnBoot": bool,
        "UseEbsOptimizedInstances": bool,
        "LifecycleEventConfiguration": LifecycleEventConfigurationTypeDef,
    },
    total=False,
)

class UpdateLayerRequestRequestTypeDef(
    _RequiredUpdateLayerRequestRequestTypeDef, _OptionalUpdateLayerRequestRequestTypeDef
):
    pass

DescribeOperatingSystemsResponseTypeDef = TypedDict(
    "DescribeOperatingSystemsResponseTypeDef",
    {
        "OperatingSystems": List[OperatingSystemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTimeBasedAutoScalingResultTypeDef = TypedDict(
    "DescribeTimeBasedAutoScalingResultTypeDef",
    {
        "TimeBasedAutoScalingConfigurations": List[TimeBasedAutoScalingConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstancesResultTypeDef = TypedDict(
    "DescribeInstancesResultTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLayersResultTypeDef = TypedDict(
    "DescribeLayersResultTypeDef",
    {
        "Layers": List[LayerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
