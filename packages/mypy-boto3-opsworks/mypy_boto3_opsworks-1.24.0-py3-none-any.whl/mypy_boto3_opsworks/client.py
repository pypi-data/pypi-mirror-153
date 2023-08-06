"""
Type annotations for opsworks service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opsworks.client import OpsWorksClient

    session = Session()
    client: OpsWorksClient = session.client("opsworks")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AppAttributesKeysType,
    AppTypeType,
    ArchitectureType,
    AutoScalingTypeType,
    LayerAttributesKeysType,
    LayerTypeType,
    RootDeviceTypeType,
)
from .paginator import DescribeEcsClustersPaginator
from .type_defs import (
    AutoScalingThresholdsTypeDef,
    BlockDeviceMappingTypeDef,
    ChefConfigurationTypeDef,
    CloneStackResultTypeDef,
    CloudWatchLogsConfigurationTypeDef,
    CreateAppResultTypeDef,
    CreateDeploymentResultTypeDef,
    CreateInstanceResultTypeDef,
    CreateLayerResultTypeDef,
    CreateStackResultTypeDef,
    CreateUserProfileResultTypeDef,
    DataSourceTypeDef,
    DeploymentCommandTypeDef,
    DescribeAgentVersionsResultTypeDef,
    DescribeAppsResultTypeDef,
    DescribeCommandsResultTypeDef,
    DescribeDeploymentsResultTypeDef,
    DescribeEcsClustersResultTypeDef,
    DescribeElasticIpsResultTypeDef,
    DescribeElasticLoadBalancersResultTypeDef,
    DescribeInstancesResultTypeDef,
    DescribeLayersResultTypeDef,
    DescribeLoadBasedAutoScalingResultTypeDef,
    DescribeMyUserProfileResultTypeDef,
    DescribeOperatingSystemsResponseTypeDef,
    DescribePermissionsResultTypeDef,
    DescribeRaidArraysResultTypeDef,
    DescribeRdsDbInstancesResultTypeDef,
    DescribeServiceErrorsResultTypeDef,
    DescribeStackProvisioningParametersResultTypeDef,
    DescribeStacksResultTypeDef,
    DescribeStackSummaryResultTypeDef,
    DescribeTimeBasedAutoScalingResultTypeDef,
    DescribeUserProfilesResultTypeDef,
    DescribeVolumesResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EnvironmentVariableTypeDef,
    GetHostnameSuggestionResultTypeDef,
    GrantAccessResultTypeDef,
    InstanceIdentityTypeDef,
    LifecycleEventConfigurationTypeDef,
    ListTagsResultTypeDef,
    RecipesTypeDef,
    RegisterEcsClusterResultTypeDef,
    RegisterElasticIpResultTypeDef,
    RegisterInstanceResultTypeDef,
    RegisterVolumeResultTypeDef,
    SourceTypeDef,
    SslConfigurationTypeDef,
    StackConfigurationManagerTypeDef,
    VolumeConfigurationTypeDef,
    WeeklyAutoScalingScheduleTypeDef,
)
from .waiter import (
    AppExistsWaiter,
    DeploymentSuccessfulWaiter,
    InstanceOnlineWaiter,
    InstanceRegisteredWaiter,
    InstanceStoppedWaiter,
    InstanceTerminatedWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("OpsWorksClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OpsWorksClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpsWorksClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#exceptions)
        """

    def assign_instance(
        self, *, InstanceId: str, LayerIds: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assign a registered instance to a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.assign_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#assign_instance)
        """

    def assign_volume(
        self, *, VolumeId: str, InstanceId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one of the stack's registered Amazon EBS volumes to a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.assign_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#assign_volume)
        """

    def associate_elastic_ip(
        self, *, ElasticIp: str, InstanceId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates one of the stack's registered Elastic IP addresses with a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.associate_elastic_ip)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#associate_elastic_ip)
        """

    def attach_elastic_load_balancer(
        self, *, ElasticLoadBalancerName: str, LayerId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches an Elastic Load Balancing load balancer to a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.attach_elastic_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#attach_elastic_load_balancer)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#can_paginate)
        """

    def clone_stack(
        self,
        *,
        SourceStackId: str,
        ServiceRoleArn: str,
        Name: str = ...,
        Region: str = ...,
        VpcId: str = ...,
        Attributes: Mapping[Literal["Color"], str] = ...,
        DefaultInstanceProfileArn: str = ...,
        DefaultOs: str = ...,
        HostnameTheme: str = ...,
        DefaultAvailabilityZone: str = ...,
        DefaultSubnetId: str = ...,
        CustomJson: str = ...,
        ConfigurationManager: StackConfigurationManagerTypeDef = ...,
        ChefConfiguration: ChefConfigurationTypeDef = ...,
        UseCustomCookbooks: bool = ...,
        UseOpsworksSecurityGroups: bool = ...,
        CustomCookbooksSource: SourceTypeDef = ...,
        DefaultSshKeyName: str = ...,
        ClonePermissions: bool = ...,
        CloneAppIds: Sequence[str] = ...,
        DefaultRootDeviceType: RootDeviceTypeType = ...,
        AgentVersion: str = ...
    ) -> CloneStackResultTypeDef:
        """
        Creates a clone of a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.clone_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#clone_stack)
        """

    def create_app(
        self,
        *,
        StackId: str,
        Name: str,
        Type: AppTypeType,
        Shortname: str = ...,
        Description: str = ...,
        DataSources: Sequence[DataSourceTypeDef] = ...,
        AppSource: SourceTypeDef = ...,
        Domains: Sequence[str] = ...,
        EnableSsl: bool = ...,
        SslConfiguration: SslConfigurationTypeDef = ...,
        Attributes: Mapping[AppAttributesKeysType, str] = ...,
        Environment: Sequence[EnvironmentVariableTypeDef] = ...
    ) -> CreateAppResultTypeDef:
        """
        Creates an app for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_app)
        """

    def create_deployment(
        self,
        *,
        StackId: str,
        Command: DeploymentCommandTypeDef,
        AppId: str = ...,
        InstanceIds: Sequence[str] = ...,
        LayerIds: Sequence[str] = ...,
        Comment: str = ...,
        CustomJson: str = ...
    ) -> CreateDeploymentResultTypeDef:
        """
        Runs deployment or stack commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_deployment)
        """

    def create_instance(
        self,
        *,
        StackId: str,
        LayerIds: Sequence[str],
        InstanceType: str,
        AutoScalingType: AutoScalingTypeType = ...,
        Hostname: str = ...,
        Os: str = ...,
        AmiId: str = ...,
        SshKeyName: str = ...,
        AvailabilityZone: str = ...,
        VirtualizationType: str = ...,
        SubnetId: str = ...,
        Architecture: ArchitectureType = ...,
        RootDeviceType: RootDeviceTypeType = ...,
        BlockDeviceMappings: Sequence[BlockDeviceMappingTypeDef] = ...,
        InstallUpdatesOnBoot: bool = ...,
        EbsOptimized: bool = ...,
        AgentVersion: str = ...,
        Tenancy: str = ...
    ) -> CreateInstanceResultTypeDef:
        """
        Creates an instance in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_instance)
        """

    def create_layer(
        self,
        *,
        StackId: str,
        Type: LayerTypeType,
        Name: str,
        Shortname: str,
        Attributes: Mapping[LayerAttributesKeysType, str] = ...,
        CloudWatchLogsConfiguration: CloudWatchLogsConfigurationTypeDef = ...,
        CustomInstanceProfileArn: str = ...,
        CustomJson: str = ...,
        CustomSecurityGroupIds: Sequence[str] = ...,
        Packages: Sequence[str] = ...,
        VolumeConfigurations: Sequence[VolumeConfigurationTypeDef] = ...,
        EnableAutoHealing: bool = ...,
        AutoAssignElasticIps: bool = ...,
        AutoAssignPublicIps: bool = ...,
        CustomRecipes: RecipesTypeDef = ...,
        InstallUpdatesOnBoot: bool = ...,
        UseEbsOptimizedInstances: bool = ...,
        LifecycleEventConfiguration: LifecycleEventConfigurationTypeDef = ...
    ) -> CreateLayerResultTypeDef:
        """
        Creates a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_layer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_layer)
        """

    def create_stack(
        self,
        *,
        Name: str,
        Region: str,
        ServiceRoleArn: str,
        DefaultInstanceProfileArn: str,
        VpcId: str = ...,
        Attributes: Mapping[Literal["Color"], str] = ...,
        DefaultOs: str = ...,
        HostnameTheme: str = ...,
        DefaultAvailabilityZone: str = ...,
        DefaultSubnetId: str = ...,
        CustomJson: str = ...,
        ConfigurationManager: StackConfigurationManagerTypeDef = ...,
        ChefConfiguration: ChefConfigurationTypeDef = ...,
        UseCustomCookbooks: bool = ...,
        UseOpsworksSecurityGroups: bool = ...,
        CustomCookbooksSource: SourceTypeDef = ...,
        DefaultSshKeyName: str = ...,
        DefaultRootDeviceType: RootDeviceTypeType = ...,
        AgentVersion: str = ...
    ) -> CreateStackResultTypeDef:
        """
        Creates a new stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_stack)
        """

    def create_user_profile(
        self,
        *,
        IamUserArn: str,
        SshUsername: str = ...,
        SshPublicKey: str = ...,
        AllowSelfManagement: bool = ...
    ) -> CreateUserProfileResultTypeDef:
        """
        Creates a new user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.create_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#create_user_profile)
        """

    def delete_app(self, *, AppId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.delete_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#delete_app)
        """

    def delete_instance(
        self, *, InstanceId: str, DeleteElasticIp: bool = ..., DeleteVolumes: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified instance, which terminates the associated Amazon EC2
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.delete_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#delete_instance)
        """

    def delete_layer(self, *, LayerId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.delete_layer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#delete_layer)
        """

    def delete_stack(self, *, StackId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.delete_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#delete_stack)
        """

    def delete_user_profile(self, *, IamUserArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.delete_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#delete_user_profile)
        """

    def deregister_ecs_cluster(self, *, EcsClusterArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Amazon ECS cluster from a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.deregister_ecs_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#deregister_ecs_cluster)
        """

    def deregister_elastic_ip(self, *, ElasticIp: str) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.deregister_elastic_ip)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#deregister_elastic_ip)
        """

    def deregister_instance(self, *, InstanceId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deregister a registered Amazon EC2 or on-premises instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.deregister_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#deregister_instance)
        """

    def deregister_rds_db_instance(self, *, RdsDbInstanceArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.deregister_rds_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#deregister_rds_db_instance)
        """

    def deregister_volume(self, *, VolumeId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.deregister_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#deregister_volume)
        """

    def describe_agent_versions(
        self, *, StackId: str = ..., ConfigurationManager: StackConfigurationManagerTypeDef = ...
    ) -> DescribeAgentVersionsResultTypeDef:
        """
        Describes the available AWS OpsWorks Stacks agent versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_agent_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_agent_versions)
        """

    def describe_apps(
        self, *, StackId: str = ..., AppIds: Sequence[str] = ...
    ) -> DescribeAppsResultTypeDef:
        """
        Requests a description of a specified set of apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_apps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_apps)
        """

    def describe_commands(
        self, *, DeploymentId: str = ..., InstanceId: str = ..., CommandIds: Sequence[str] = ...
    ) -> DescribeCommandsResultTypeDef:
        """
        Describes the results of specified commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_commands)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_commands)
        """

    def describe_deployments(
        self, *, StackId: str = ..., AppId: str = ..., DeploymentIds: Sequence[str] = ...
    ) -> DescribeDeploymentsResultTypeDef:
        """
        Requests a description of a specified set of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_deployments)
        """

    def describe_ecs_clusters(
        self,
        *,
        EcsClusterArns: Sequence[str] = ...,
        StackId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> DescribeEcsClustersResultTypeDef:
        """
        Describes Amazon ECS clusters that are registered with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_ecs_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_ecs_clusters)
        """

    def describe_elastic_ips(
        self, *, InstanceId: str = ..., StackId: str = ..., Ips: Sequence[str] = ...
    ) -> DescribeElasticIpsResultTypeDef:
        """
        Describes [Elastic IP
        addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-
        addresses-eip.html)_ .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_elastic_ips)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_elastic_ips)
        """

    def describe_elastic_load_balancers(
        self, *, StackId: str = ..., LayerIds: Sequence[str] = ...
    ) -> DescribeElasticLoadBalancersResultTypeDef:
        """
        Describes a stack's Elastic Load Balancing instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_elastic_load_balancers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_elastic_load_balancers)
        """

    def describe_instances(
        self, *, StackId: str = ..., LayerId: str = ..., InstanceIds: Sequence[str] = ...
    ) -> DescribeInstancesResultTypeDef:
        """
        Requests a description of a set of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_instances)
        """

    def describe_layers(
        self, *, StackId: str = ..., LayerIds: Sequence[str] = ...
    ) -> DescribeLayersResultTypeDef:
        """
        Requests a description of one or more layers in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_layers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_layers)
        """

    def describe_load_based_auto_scaling(
        self, *, LayerIds: Sequence[str]
    ) -> DescribeLoadBasedAutoScalingResultTypeDef:
        """
        Describes load-based auto scaling configurations for specified layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_load_based_auto_scaling)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_load_based_auto_scaling)
        """

    def describe_my_user_profile(self) -> DescribeMyUserProfileResultTypeDef:
        """
        Describes a user's SSH information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_my_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_my_user_profile)
        """

    def describe_operating_systems(self) -> DescribeOperatingSystemsResponseTypeDef:
        """
        Describes the operating systems that are supported by AWS OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_operating_systems)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_operating_systems)
        """

    def describe_permissions(
        self, *, IamUserArn: str = ..., StackId: str = ...
    ) -> DescribePermissionsResultTypeDef:
        """
        Describes the permissions for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_permissions)
        """

    def describe_raid_arrays(
        self, *, InstanceId: str = ..., StackId: str = ..., RaidArrayIds: Sequence[str] = ...
    ) -> DescribeRaidArraysResultTypeDef:
        """
        Describe an instance's RAID arrays.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_raid_arrays)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_raid_arrays)
        """

    def describe_rds_db_instances(
        self, *, StackId: str, RdsDbInstanceArns: Sequence[str] = ...
    ) -> DescribeRdsDbInstancesResultTypeDef:
        """
        Describes Amazon RDS instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_rds_db_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_rds_db_instances)
        """

    def describe_service_errors(
        self, *, StackId: str = ..., InstanceId: str = ..., ServiceErrorIds: Sequence[str] = ...
    ) -> DescribeServiceErrorsResultTypeDef:
        """
        Describes AWS OpsWorks Stacks service errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_service_errors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_service_errors)
        """

    def describe_stack_provisioning_parameters(
        self, *, StackId: str
    ) -> DescribeStackProvisioningParametersResultTypeDef:
        """
        Requests a description of a stack's provisioning parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_stack_provisioning_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_stack_provisioning_parameters)
        """

    def describe_stack_summary(self, *, StackId: str) -> DescribeStackSummaryResultTypeDef:
        """
        Describes the number of layers and apps in a specified stack, and the number of
        instances in each state, such as `running_setup` or `online` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_stack_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_stack_summary)
        """

    def describe_stacks(self, *, StackIds: Sequence[str] = ...) -> DescribeStacksResultTypeDef:
        """
        Requests a description of one or more stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_stacks)
        """

    def describe_time_based_auto_scaling(
        self, *, InstanceIds: Sequence[str]
    ) -> DescribeTimeBasedAutoScalingResultTypeDef:
        """
        Describes time-based auto scaling configurations for specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_time_based_auto_scaling)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_time_based_auto_scaling)
        """

    def describe_user_profiles(
        self, *, IamUserArns: Sequence[str] = ...
    ) -> DescribeUserProfilesResultTypeDef:
        """
        Describe specified users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_user_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_user_profiles)
        """

    def describe_volumes(
        self,
        *,
        InstanceId: str = ...,
        StackId: str = ...,
        RaidArrayId: str = ...,
        VolumeIds: Sequence[str] = ...
    ) -> DescribeVolumesResultTypeDef:
        """
        Describes an instance's Amazon EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.describe_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#describe_volumes)
        """

    def detach_elastic_load_balancer(
        self, *, ElasticLoadBalancerName: str, LayerId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a specified Elastic Load Balancing instance from its layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.detach_elastic_load_balancer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#detach_elastic_load_balancer)
        """

    def disassociate_elastic_ip(self, *, ElasticIp: str) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Elastic IP address from its instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.disassociate_elastic_ip)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#disassociate_elastic_ip)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#generate_presigned_url)
        """

    def get_hostname_suggestion(self, *, LayerId: str) -> GetHostnameSuggestionResultTypeDef:
        """
        Gets a generated host name for the specified layer, based on the current host
        name theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_hostname_suggestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_hostname_suggestion)
        """

    def grant_access(
        self, *, InstanceId: str, ValidForInMinutes: int = ...
    ) -> GrantAccessResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.grant_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#grant_access)
        """

    def list_tags(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsResultTypeDef:
        """
        Returns a list of tags that are applied to the specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#list_tags)
        """

    def reboot_instance(self, *, InstanceId: str) -> EmptyResponseMetadataTypeDef:
        """
        Reboots a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.reboot_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#reboot_instance)
        """

    def register_ecs_cluster(
        self, *, EcsClusterArn: str, StackId: str
    ) -> RegisterEcsClusterResultTypeDef:
        """
        Registers a specified Amazon ECS cluster with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.register_ecs_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#register_ecs_cluster)
        """

    def register_elastic_ip(
        self, *, ElasticIp: str, StackId: str
    ) -> RegisterElasticIpResultTypeDef:
        """
        Registers an Elastic IP address with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.register_elastic_ip)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#register_elastic_ip)
        """

    def register_instance(
        self,
        *,
        StackId: str,
        Hostname: str = ...,
        PublicIp: str = ...,
        PrivateIp: str = ...,
        RsaPublicKey: str = ...,
        RsaPublicKeyFingerprint: str = ...,
        InstanceIdentity: InstanceIdentityTypeDef = ...
    ) -> RegisterInstanceResultTypeDef:
        """
        Registers instances that were created outside of AWS OpsWorks Stacks with a
        specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.register_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#register_instance)
        """

    def register_rds_db_instance(
        self, *, StackId: str, RdsDbInstanceArn: str, DbUser: str, DbPassword: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers an Amazon RDS instance with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.register_rds_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#register_rds_db_instance)
        """

    def register_volume(
        self, *, StackId: str, Ec2VolumeId: str = ...
    ) -> RegisterVolumeResultTypeDef:
        """
        Registers an Amazon EBS volume with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.register_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#register_volume)
        """

    def set_load_based_auto_scaling(
        self,
        *,
        LayerId: str,
        Enable: bool = ...,
        UpScaling: AutoScalingThresholdsTypeDef = ...,
        DownScaling: AutoScalingThresholdsTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the load-based auto scaling configuration for a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.set_load_based_auto_scaling)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#set_load_based_auto_scaling)
        """

    def set_permission(
        self,
        *,
        StackId: str,
        IamUserArn: str,
        AllowSsh: bool = ...,
        AllowSudo: bool = ...,
        Level: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies a user's permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.set_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#set_permission)
        """

    def set_time_based_auto_scaling(
        self, *, InstanceId: str, AutoScalingSchedule: WeeklyAutoScalingScheduleTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the time-based auto scaling configuration for a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.set_time_based_auto_scaling)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#set_time_based_auto_scaling)
        """

    def start_instance(self, *, InstanceId: str) -> EmptyResponseMetadataTypeDef:
        """
        Starts a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.start_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#start_instance)
        """

    def start_stack(self, *, StackId: str) -> EmptyResponseMetadataTypeDef:
        """
        Starts a stack's instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.start_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#start_stack)
        """

    def stop_instance(self, *, InstanceId: str, Force: bool = ...) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.stop_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#stop_instance)
        """

    def stop_stack(self, *, StackId: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.stop_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#stop_stack)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Apply cost-allocation tags to a specified stack or layer in AWS OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#tag_resource)
        """

    def unassign_instance(self, *, InstanceId: str) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns a registered instance from all layers that are using the instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.unassign_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#unassign_instance)
        """

    def unassign_volume(self, *, VolumeId: str) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns an assigned Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.unassign_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#unassign_volume)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#untag_resource)
        """

    def update_app(
        self,
        *,
        AppId: str,
        Name: str = ...,
        Description: str = ...,
        DataSources: Sequence[DataSourceTypeDef] = ...,
        Type: AppTypeType = ...,
        AppSource: SourceTypeDef = ...,
        Domains: Sequence[str] = ...,
        EnableSsl: bool = ...,
        SslConfiguration: SslConfigurationTypeDef = ...,
        Attributes: Mapping[AppAttributesKeysType, str] = ...,
        Environment: Sequence[EnvironmentVariableTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_app)
        """

    def update_elastic_ip(self, *, ElasticIp: str, Name: str = ...) -> EmptyResponseMetadataTypeDef:
        """
        Updates a registered Elastic IP address's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_elastic_ip)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_elastic_ip)
        """

    def update_instance(
        self,
        *,
        InstanceId: str,
        LayerIds: Sequence[str] = ...,
        InstanceType: str = ...,
        AutoScalingType: AutoScalingTypeType = ...,
        Hostname: str = ...,
        Os: str = ...,
        AmiId: str = ...,
        SshKeyName: str = ...,
        Architecture: ArchitectureType = ...,
        InstallUpdatesOnBoot: bool = ...,
        EbsOptimized: bool = ...,
        AgentVersion: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_instance)
        """

    def update_layer(
        self,
        *,
        LayerId: str,
        Name: str = ...,
        Shortname: str = ...,
        Attributes: Mapping[LayerAttributesKeysType, str] = ...,
        CloudWatchLogsConfiguration: CloudWatchLogsConfigurationTypeDef = ...,
        CustomInstanceProfileArn: str = ...,
        CustomJson: str = ...,
        CustomSecurityGroupIds: Sequence[str] = ...,
        Packages: Sequence[str] = ...,
        VolumeConfigurations: Sequence[VolumeConfigurationTypeDef] = ...,
        EnableAutoHealing: bool = ...,
        AutoAssignElasticIps: bool = ...,
        AutoAssignPublicIps: bool = ...,
        CustomRecipes: RecipesTypeDef = ...,
        InstallUpdatesOnBoot: bool = ...,
        UseEbsOptimizedInstances: bool = ...,
        LifecycleEventConfiguration: LifecycleEventConfigurationTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_layer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_layer)
        """

    def update_my_user_profile(self, *, SshPublicKey: str = ...) -> EmptyResponseMetadataTypeDef:
        """
        Updates a user's SSH public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_my_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_my_user_profile)
        """

    def update_rds_db_instance(
        self, *, RdsDbInstanceArn: str, DbUser: str = ..., DbPassword: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_rds_db_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_rds_db_instance)
        """

    def update_stack(
        self,
        *,
        StackId: str,
        Name: str = ...,
        Attributes: Mapping[Literal["Color"], str] = ...,
        ServiceRoleArn: str = ...,
        DefaultInstanceProfileArn: str = ...,
        DefaultOs: str = ...,
        HostnameTheme: str = ...,
        DefaultAvailabilityZone: str = ...,
        DefaultSubnetId: str = ...,
        CustomJson: str = ...,
        ConfigurationManager: StackConfigurationManagerTypeDef = ...,
        ChefConfiguration: ChefConfigurationTypeDef = ...,
        UseCustomCookbooks: bool = ...,
        CustomCookbooksSource: SourceTypeDef = ...,
        DefaultSshKeyName: str = ...,
        DefaultRootDeviceType: RootDeviceTypeType = ...,
        UseOpsworksSecurityGroups: bool = ...,
        AgentVersion: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_stack)
        """

    def update_user_profile(
        self,
        *,
        IamUserArn: str,
        SshUsername: str = ...,
        SshPublicKey: str = ...,
        AllowSelfManagement: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_user_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_user_profile)
        """

    def update_volume(
        self, *, VolumeId: str, Name: str = ..., MountPoint: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon EBS volume's name or mount point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.update_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#update_volume)
        """

    def get_paginator(
        self, operation_name: Literal["describe_ecs_clusters"]
    ) -> DescribeEcsClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["app_exists"]) -> AppExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["deployment_successful"]
    ) -> DeploymentSuccessfulWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_online"]) -> InstanceOnlineWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_registered"]) -> InstanceRegisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_stopped"]) -> InstanceStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_terminated"]) -> InstanceTerminatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/client/#get_waiter)
        """
