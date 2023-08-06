"""
Type annotations for opsworks service ServiceResource

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opsworks.service_resource import OpsWorksServiceResource
    import mypy_boto3_opsworks.service_resource as opsworks_resources

    session = Session()
    resource: OpsWorksServiceResource = session.resource("opsworks")

    my_layer: opsworks_resources.Layer = resource.Layer(...)
    my_stack: opsworks_resources.Stack = resource.Stack(...)
    my_stack_summary: opsworks_resources.StackSummary = resource.StackSummary(...)
```
"""
import sys
from typing import Dict, Iterator, List, Mapping, Sequence

from boto3.resources.base import ResourceMeta
from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import OpsWorksClient
from .literals import LayerAttributesKeysType, LayerTypeType, RootDeviceTypeType
from .type_defs import (
    ChefConfigurationResponseMetadataTypeDef,
    ChefConfigurationTypeDef,
    CloudWatchLogsConfigurationResponseMetadataTypeDef,
    CloudWatchLogsConfigurationTypeDef,
    InstancesCountResponseMetadataTypeDef,
    LifecycleEventConfigurationResponseMetadataTypeDef,
    LifecycleEventConfigurationTypeDef,
    RecipesResponseMetadataTypeDef,
    RecipesTypeDef,
    SourceResponseMetadataTypeDef,
    SourceTypeDef,
    StackConfigurationManagerResponseMetadataTypeDef,
    StackConfigurationManagerTypeDef,
    VolumeConfigurationTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "OpsWorksServiceResource",
    "Layer",
    "Stack",
    "StackSummary",
    "ServiceResourceStacksCollection",
    "StackLayersCollection",
)


class ServiceResourceStacksCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
    """

    def all(self) -> "ServiceResourceStacksCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def filter(  # type: ignore
        self, *, StackIds: Sequence[str] = ...
    ) -> "ServiceResourceStacksCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def limit(self, count: int) -> "ServiceResourceStacksCollection":
        """
        Return at most this many Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceStacksCollection":
        """
        Fetch at most this many Stacks per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def pages(self) -> Iterator[List["Stack"]]:
        """
        A generator which yields pages of Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def __iter__(self) -> Iterator["Stack"]:
        """
        A generator which yields Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.stacks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#serviceresourcestackscollection)
        """


class StackLayersCollection(ResourceCollection):
    def all(self) -> "StackLayersCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, StackId: str = ..., LayerIds: Sequence[str] = ...
    ) -> "StackLayersCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "StackLayersCollection":
        """
        Return at most this many Layers.
        """

    def page_size(self, count: int) -> "StackLayersCollection":
        """
        Fetch at most this many Layers per service request.
        """

    def pages(self) -> Iterator[List["Layer"]]:
        """
        A generator which yields pages of Layers.
        """

    def __iter__(self) -> Iterator["Layer"]:
        """
        A generator which yields Layers.
        """


class Layer(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.Layer)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#layer)
    """

    arn: str
    stack_id: str
    layer_id: str
    type: LayerTypeType
    name: str
    shortname: str
    attributes: Dict[LayerAttributesKeysType, str]
    cloud_watch_logs_configuration: CloudWatchLogsConfigurationResponseMetadataTypeDef
    custom_instance_profile_arn: str
    custom_json: str
    custom_security_group_ids: List[str]
    default_security_group_names: List[str]
    packages: List[str]
    volume_configurations: List[VolumeConfigurationTypeDef]
    enable_auto_healing: bool
    auto_assign_elastic_ips: bool
    auto_assign_public_ips: bool
    default_recipes: RecipesResponseMetadataTypeDef
    custom_recipes: RecipesResponseMetadataTypeDef
    created_at: str
    install_updates_on_boot: bool
    use_ebs_optimized_instances: bool
    lifecycle_event_configuration: LifecycleEventConfigurationResponseMetadataTypeDef
    id: str
    stack: "Stack"

    def delete(self) -> None:
        """
        Deletes a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Layer.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#layerdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Layer.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#layerget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_layers` to update the attributes of the
        Layer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Layer.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#layerload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_layers` to update the attributes of the
        Layer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Layer.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#layerreload-method)
        """


_Layer = Layer


class StackSummary(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.StackSummary)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummary)
    """

    name: str
    arn: str
    layers_count: int
    apps_count: int
    instances_count: InstancesCountResponseMetadataTypeDef
    stack_id: str

    def Stack(self) -> "_Stack":
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.StackSummary.Stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummarystack-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.StackSummary.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummaryget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_stack_summary` to update the attributes
        of the StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.StackSummary.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummaryload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_stack_summary` to update the attributes
        of the StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.StackSummary.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummaryreload-method)
        """


_StackSummary = StackSummary


class Stack(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.Stack)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stack)
    """

    stack_id: str
    name: str
    arn: str
    region: str
    vpc_id: str
    attributes: Dict[Literal["Color"], str]
    service_role_arn: str
    default_instance_profile_arn: str
    default_os: str
    hostname_theme: str
    default_availability_zone: str
    default_subnet_id: str
    custom_json: str
    configuration_manager: StackConfigurationManagerResponseMetadataTypeDef
    chef_configuration: ChefConfigurationResponseMetadataTypeDef
    use_custom_cookbooks: bool
    use_opsworks_security_groups: bool
    custom_cookbooks_source: SourceResponseMetadataTypeDef
    default_ssh_key_name: str
    created_at: str
    default_root_device_type: RootDeviceTypeType
    agent_version: str
    id: str
    layers: StackLayersCollection

    def Summary(self) -> _StackSummary:
        """
        Creates a StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.Summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stacksummary-method)
        """

    def create_layer(
        self,
        *,
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
    ) -> _Layer:
        """
        Creates a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.create_layer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stackcreate_layer-method)
        """

    def delete(self) -> None:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stackdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stackget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_stacks` to update the attributes of the
        Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stackload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`OpsWorks.Client.describe_stacks` to update the attributes of the
        Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Stack.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#stackreload-method)
        """


_Stack = Stack


class OpsWorksResourceMeta(ResourceMeta):
    client: OpsWorksClient


class OpsWorksServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/)
    """

    meta: "OpsWorksResourceMeta"
    stacks: ServiceResourceStacksCollection

    def Layer(self, id: str) -> _Layer:
        """
        Creates a Layer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.Layer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#opsworksserviceresourcelayer-method)
        """

    def Stack(self, id: str) -> _Stack:
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.Stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#opsworksserviceresourcestack-method)
        """

    def StackSummary(self, stack_id: str) -> _StackSummary:
        """
        Creates a StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.StackSummary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#opsworksserviceresourcestacksummary-method)
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
    ) -> _Stack:
        """
        Creates a new stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.create_stack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#opsworksserviceresourcecreate_stack-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworks/service_resource/#opsworksserviceresourceget_available_subresources-method)
        """
