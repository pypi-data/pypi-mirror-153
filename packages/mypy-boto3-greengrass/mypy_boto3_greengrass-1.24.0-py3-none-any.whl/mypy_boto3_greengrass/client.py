"""
Type annotations for greengrass service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_greengrass.client import GreengrassClient

    session = Session()
    client: GreengrassClient = session.client("greengrass")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    DeploymentTypeType,
    SoftwareToUpdateType,
    UpdateAgentLogLevelType,
    UpdateTargetsArchitectureType,
    UpdateTargetsOperatingSystemType,
)
from .paginator import (
    ListBulkDeploymentDetailedReportsPaginator,
    ListBulkDeploymentsPaginator,
    ListConnectorDefinitionsPaginator,
    ListConnectorDefinitionVersionsPaginator,
    ListCoreDefinitionsPaginator,
    ListCoreDefinitionVersionsPaginator,
    ListDeploymentsPaginator,
    ListDeviceDefinitionsPaginator,
    ListDeviceDefinitionVersionsPaginator,
    ListFunctionDefinitionsPaginator,
    ListFunctionDefinitionVersionsPaginator,
    ListGroupsPaginator,
    ListGroupVersionsPaginator,
    ListLoggerDefinitionsPaginator,
    ListLoggerDefinitionVersionsPaginator,
    ListResourceDefinitionsPaginator,
    ListResourceDefinitionVersionsPaginator,
    ListSubscriptionDefinitionsPaginator,
    ListSubscriptionDefinitionVersionsPaginator,
)
from .type_defs import (
    AssociateRoleToGroupResponseTypeDef,
    AssociateServiceRoleToAccountResponseTypeDef,
    ConnectivityInfoTypeDef,
    ConnectorDefinitionVersionTypeDef,
    ConnectorTypeDef,
    CoreDefinitionVersionTypeDef,
    CoreTypeDef,
    CreateConnectorDefinitionResponseTypeDef,
    CreateConnectorDefinitionVersionResponseTypeDef,
    CreateCoreDefinitionResponseTypeDef,
    CreateCoreDefinitionVersionResponseTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateDeviceDefinitionResponseTypeDef,
    CreateDeviceDefinitionVersionResponseTypeDef,
    CreateFunctionDefinitionResponseTypeDef,
    CreateFunctionDefinitionVersionResponseTypeDef,
    CreateGroupCertificateAuthorityResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateGroupVersionResponseTypeDef,
    CreateLoggerDefinitionResponseTypeDef,
    CreateLoggerDefinitionVersionResponseTypeDef,
    CreateResourceDefinitionResponseTypeDef,
    CreateResourceDefinitionVersionResponseTypeDef,
    CreateSoftwareUpdateJobResponseTypeDef,
    CreateSubscriptionDefinitionResponseTypeDef,
    CreateSubscriptionDefinitionVersionResponseTypeDef,
    DeviceDefinitionVersionTypeDef,
    DeviceTypeDef,
    DisassociateRoleFromGroupResponseTypeDef,
    DisassociateServiceRoleFromAccountResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FunctionDefaultConfigTypeDef,
    FunctionDefinitionVersionTypeDef,
    FunctionTypeDef,
    GetAssociatedRoleResponseTypeDef,
    GetBulkDeploymentStatusResponseTypeDef,
    GetConnectivityInfoResponseTypeDef,
    GetConnectorDefinitionResponseTypeDef,
    GetConnectorDefinitionVersionResponseTypeDef,
    GetCoreDefinitionResponseTypeDef,
    GetCoreDefinitionVersionResponseTypeDef,
    GetDeploymentStatusResponseTypeDef,
    GetDeviceDefinitionResponseTypeDef,
    GetDeviceDefinitionVersionResponseTypeDef,
    GetFunctionDefinitionResponseTypeDef,
    GetFunctionDefinitionVersionResponseTypeDef,
    GetGroupCertificateAuthorityResponseTypeDef,
    GetGroupCertificateConfigurationResponseTypeDef,
    GetGroupResponseTypeDef,
    GetGroupVersionResponseTypeDef,
    GetLoggerDefinitionResponseTypeDef,
    GetLoggerDefinitionVersionResponseTypeDef,
    GetResourceDefinitionResponseTypeDef,
    GetResourceDefinitionVersionResponseTypeDef,
    GetServiceRoleForAccountResponseTypeDef,
    GetSubscriptionDefinitionResponseTypeDef,
    GetSubscriptionDefinitionVersionResponseTypeDef,
    GetThingRuntimeConfigurationResponseTypeDef,
    GroupVersionTypeDef,
    ListBulkDeploymentDetailedReportsResponseTypeDef,
    ListBulkDeploymentsResponseTypeDef,
    ListConnectorDefinitionsResponseTypeDef,
    ListConnectorDefinitionVersionsResponseTypeDef,
    ListCoreDefinitionsResponseTypeDef,
    ListCoreDefinitionVersionsResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListDeviceDefinitionsResponseTypeDef,
    ListDeviceDefinitionVersionsResponseTypeDef,
    ListFunctionDefinitionsResponseTypeDef,
    ListFunctionDefinitionVersionsResponseTypeDef,
    ListGroupCertificateAuthoritiesResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListGroupVersionsResponseTypeDef,
    ListLoggerDefinitionsResponseTypeDef,
    ListLoggerDefinitionVersionsResponseTypeDef,
    ListResourceDefinitionsResponseTypeDef,
    ListResourceDefinitionVersionsResponseTypeDef,
    ListSubscriptionDefinitionsResponseTypeDef,
    ListSubscriptionDefinitionVersionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggerDefinitionVersionTypeDef,
    LoggerTypeDef,
    ResetDeploymentsResponseTypeDef,
    ResourceDefinitionVersionTypeDef,
    ResourceTypeDef,
    StartBulkDeploymentResponseTypeDef,
    SubscriptionDefinitionVersionTypeDef,
    SubscriptionTypeDef,
    TelemetryConfigurationUpdateTypeDef,
    UpdateConnectivityInfoResponseTypeDef,
    UpdateGroupCertificateConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GreengrassClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]


class GreengrassClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GreengrassClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#exceptions)
        """

    def associate_role_to_group(
        self, *, GroupId: str, RoleArn: str
    ) -> AssociateRoleToGroupResponseTypeDef:
        """
        Associates a role with a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.associate_role_to_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#associate_role_to_group)
        """

    def associate_service_role_to_account(
        self, *, RoleArn: str
    ) -> AssociateServiceRoleToAccountResponseTypeDef:
        """
        Associates a role with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.associate_service_role_to_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#associate_service_role_to_account)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#can_paginate)
        """

    def create_connector_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: ConnectorDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateConnectorDefinitionResponseTypeDef:
        """
        Creates a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_connector_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_connector_definition)
        """

    def create_connector_definition_version(
        self,
        *,
        ConnectorDefinitionId: str,
        AmznClientToken: str = ...,
        Connectors: Sequence[ConnectorTypeDef] = ...
    ) -> CreateConnectorDefinitionVersionResponseTypeDef:
        """
        Creates a version of a connector definition which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_connector_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_connector_definition_version)
        """

    def create_core_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: CoreDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateCoreDefinitionResponseTypeDef:
        """
        Creates a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_core_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_core_definition)
        """

    def create_core_definition_version(
        self,
        *,
        CoreDefinitionId: str,
        AmznClientToken: str = ...,
        Cores: Sequence[CoreTypeDef] = ...
    ) -> CreateCoreDefinitionVersionResponseTypeDef:
        """
        Creates a version of a core definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_core_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_core_definition_version)
        """

    def create_deployment(
        self,
        *,
        DeploymentType: DeploymentTypeType,
        GroupId: str,
        AmznClientToken: str = ...,
        DeploymentId: str = ...,
        GroupVersionId: str = ...
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_deployment)
        """

    def create_device_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: DeviceDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateDeviceDefinitionResponseTypeDef:
        """
        Creates a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_device_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_device_definition)
        """

    def create_device_definition_version(
        self,
        *,
        DeviceDefinitionId: str,
        AmznClientToken: str = ...,
        Devices: Sequence[DeviceTypeDef] = ...
    ) -> CreateDeviceDefinitionVersionResponseTypeDef:
        """
        Creates a version of a device definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_device_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_device_definition_version)
        """

    def create_function_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: FunctionDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateFunctionDefinitionResponseTypeDef:
        """
        Creates a Lambda function definition which contains a list of Lambda functions
        and their configurations to be used in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_function_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_function_definition)
        """

    def create_function_definition_version(
        self,
        *,
        FunctionDefinitionId: str,
        AmznClientToken: str = ...,
        DefaultConfig: FunctionDefaultConfigTypeDef = ...,
        Functions: Sequence[FunctionTypeDef] = ...
    ) -> CreateFunctionDefinitionVersionResponseTypeDef:
        """
        Creates a version of a Lambda function definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_function_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_function_definition_version)
        """

    def create_group(
        self,
        *,
        Name: str,
        AmznClientToken: str = ...,
        InitialVersion: GroupVersionTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_group)
        """

    def create_group_certificate_authority(
        self, *, GroupId: str, AmznClientToken: str = ...
    ) -> CreateGroupCertificateAuthorityResponseTypeDef:
        """
        Creates a CA for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_group_certificate_authority)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_group_certificate_authority)
        """

    def create_group_version(
        self,
        *,
        GroupId: str,
        AmznClientToken: str = ...,
        ConnectorDefinitionVersionArn: str = ...,
        CoreDefinitionVersionArn: str = ...,
        DeviceDefinitionVersionArn: str = ...,
        FunctionDefinitionVersionArn: str = ...,
        LoggerDefinitionVersionArn: str = ...,
        ResourceDefinitionVersionArn: str = ...,
        SubscriptionDefinitionVersionArn: str = ...
    ) -> CreateGroupVersionResponseTypeDef:
        """
        Creates a version of a group which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_group_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_group_version)
        """

    def create_logger_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: LoggerDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateLoggerDefinitionResponseTypeDef:
        """
        Creates a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_logger_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_logger_definition)
        """

    def create_logger_definition_version(
        self,
        *,
        LoggerDefinitionId: str,
        AmznClientToken: str = ...,
        Loggers: Sequence[LoggerTypeDef] = ...
    ) -> CreateLoggerDefinitionVersionResponseTypeDef:
        """
        Creates a version of a logger definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_logger_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_logger_definition_version)
        """

    def create_resource_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: ResourceDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateResourceDefinitionResponseTypeDef:
        """
        Creates a resource definition which contains a list of resources to be used in a
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_resource_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_resource_definition)
        """

    def create_resource_definition_version(
        self,
        *,
        ResourceDefinitionId: str,
        AmznClientToken: str = ...,
        Resources: Sequence[ResourceTypeDef] = ...
    ) -> CreateResourceDefinitionVersionResponseTypeDef:
        """
        Creates a version of a resource definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_resource_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_resource_definition_version)
        """

    def create_software_update_job(
        self,
        *,
        S3UrlSignerRole: str,
        SoftwareToUpdate: SoftwareToUpdateType,
        UpdateTargets: Sequence[str],
        UpdateTargetsArchitecture: UpdateTargetsArchitectureType,
        UpdateTargetsOperatingSystem: UpdateTargetsOperatingSystemType,
        AmznClientToken: str = ...,
        UpdateAgentLogLevel: UpdateAgentLogLevelType = ...
    ) -> CreateSoftwareUpdateJobResponseTypeDef:
        """
        Creates a software update for a core or group of cores (specified as an IoT
        thing group.) Use this to update the OTA Agent as well as the Greengrass core
        software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_software_update_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_software_update_job)
        """

    def create_subscription_definition(
        self,
        *,
        AmznClientToken: str = ...,
        InitialVersion: SubscriptionDefinitionVersionTypeDef = ...,
        Name: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSubscriptionDefinitionResponseTypeDef:
        """
        Creates a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_subscription_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_subscription_definition)
        """

    def create_subscription_definition_version(
        self,
        *,
        SubscriptionDefinitionId: str,
        AmznClientToken: str = ...,
        Subscriptions: Sequence[SubscriptionTypeDef] = ...
    ) -> CreateSubscriptionDefinitionVersionResponseTypeDef:
        """
        Creates a version of a subscription definition which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.create_subscription_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#create_subscription_definition_version)
        """

    def delete_connector_definition(self, *, ConnectorDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_connector_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_connector_definition)
        """

    def delete_core_definition(self, *, CoreDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_core_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_core_definition)
        """

    def delete_device_definition(self, *, DeviceDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_device_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_device_definition)
        """

    def delete_function_definition(self, *, FunctionDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_function_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_function_definition)
        """

    def delete_group(self, *, GroupId: str) -> Dict[str, Any]:
        """
        Deletes a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_group)
        """

    def delete_logger_definition(self, *, LoggerDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_logger_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_logger_definition)
        """

    def delete_resource_definition(self, *, ResourceDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_resource_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_resource_definition)
        """

    def delete_subscription_definition(self, *, SubscriptionDefinitionId: str) -> Dict[str, Any]:
        """
        Deletes a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.delete_subscription_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#delete_subscription_definition)
        """

    def disassociate_role_from_group(
        self, *, GroupId: str
    ) -> DisassociateRoleFromGroupResponseTypeDef:
        """
        Disassociates the role from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.disassociate_role_from_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#disassociate_role_from_group)
        """

    def disassociate_service_role_from_account(
        self,
    ) -> DisassociateServiceRoleFromAccountResponseTypeDef:
        """
        Disassociates the service role from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.disassociate_service_role_from_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#disassociate_service_role_from_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#generate_presigned_url)
        """

    def get_associated_role(self, *, GroupId: str) -> GetAssociatedRoleResponseTypeDef:
        """
        Retrieves the role associated with a particular group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_associated_role)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_associated_role)
        """

    def get_bulk_deployment_status(
        self, *, BulkDeploymentId: str
    ) -> GetBulkDeploymentStatusResponseTypeDef:
        """
        Returns the status of a bulk deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_bulk_deployment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_bulk_deployment_status)
        """

    def get_connectivity_info(self, *, ThingName: str) -> GetConnectivityInfoResponseTypeDef:
        """
        Retrieves the connectivity information for a core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_connectivity_info)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_connectivity_info)
        """

    def get_connector_definition(
        self, *, ConnectorDefinitionId: str
    ) -> GetConnectorDefinitionResponseTypeDef:
        """
        Retrieves information about a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_connector_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_connector_definition)
        """

    def get_connector_definition_version(
        self, *, ConnectorDefinitionId: str, ConnectorDefinitionVersionId: str, NextToken: str = ...
    ) -> GetConnectorDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a connector definition version, including the
        connectors that the version contains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_connector_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_connector_definition_version)
        """

    def get_core_definition(self, *, CoreDefinitionId: str) -> GetCoreDefinitionResponseTypeDef:
        """
        Retrieves information about a core definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_core_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_core_definition)
        """

    def get_core_definition_version(
        self, *, CoreDefinitionId: str, CoreDefinitionVersionId: str
    ) -> GetCoreDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a core definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_core_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_core_definition_version)
        """

    def get_deployment_status(
        self, *, DeploymentId: str, GroupId: str
    ) -> GetDeploymentStatusResponseTypeDef:
        """
        Returns the status of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_deployment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_deployment_status)
        """

    def get_device_definition(
        self, *, DeviceDefinitionId: str
    ) -> GetDeviceDefinitionResponseTypeDef:
        """
        Retrieves information about a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_device_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_device_definition)
        """

    def get_device_definition_version(
        self, *, DeviceDefinitionId: str, DeviceDefinitionVersionId: str, NextToken: str = ...
    ) -> GetDeviceDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a device definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_device_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_device_definition_version)
        """

    def get_function_definition(
        self, *, FunctionDefinitionId: str
    ) -> GetFunctionDefinitionResponseTypeDef:
        """
        Retrieves information about a Lambda function definition, including its creation
        time and latest version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_function_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_function_definition)
        """

    def get_function_definition_version(
        self, *, FunctionDefinitionId: str, FunctionDefinitionVersionId: str, NextToken: str = ...
    ) -> GetFunctionDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a Lambda function definition version, including
        which Lambda functions are included in the version and their configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_function_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_function_definition_version)
        """

    def get_group(self, *, GroupId: str) -> GetGroupResponseTypeDef:
        """
        Retrieves information about a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_group)
        """

    def get_group_certificate_authority(
        self, *, CertificateAuthorityId: str, GroupId: str
    ) -> GetGroupCertificateAuthorityResponseTypeDef:
        """
        Retreives the CA associated with a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_group_certificate_authority)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_group_certificate_authority)
        """

    def get_group_certificate_configuration(
        self, *, GroupId: str
    ) -> GetGroupCertificateConfigurationResponseTypeDef:
        """
        Retrieves the current configuration for the CA used by the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_group_certificate_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_group_certificate_configuration)
        """

    def get_group_version(
        self, *, GroupId: str, GroupVersionId: str
    ) -> GetGroupVersionResponseTypeDef:
        """
        Retrieves information about a group version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_group_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_group_version)
        """

    def get_logger_definition(
        self, *, LoggerDefinitionId: str
    ) -> GetLoggerDefinitionResponseTypeDef:
        """
        Retrieves information about a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_logger_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_logger_definition)
        """

    def get_logger_definition_version(
        self, *, LoggerDefinitionId: str, LoggerDefinitionVersionId: str, NextToken: str = ...
    ) -> GetLoggerDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a logger definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_logger_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_logger_definition_version)
        """

    def get_resource_definition(
        self, *, ResourceDefinitionId: str
    ) -> GetResourceDefinitionResponseTypeDef:
        """
        Retrieves information about a resource definition, including its creation time
        and latest version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_resource_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_resource_definition)
        """

    def get_resource_definition_version(
        self, *, ResourceDefinitionId: str, ResourceDefinitionVersionId: str
    ) -> GetResourceDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a resource definition version, including which
        resources are included in the version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_resource_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_resource_definition_version)
        """

    def get_service_role_for_account(self) -> GetServiceRoleForAccountResponseTypeDef:
        """
        Retrieves the service role that is attached to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_service_role_for_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_service_role_for_account)
        """

    def get_subscription_definition(
        self, *, SubscriptionDefinitionId: str
    ) -> GetSubscriptionDefinitionResponseTypeDef:
        """
        Retrieves information about a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_subscription_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_subscription_definition)
        """

    def get_subscription_definition_version(
        self,
        *,
        SubscriptionDefinitionId: str,
        SubscriptionDefinitionVersionId: str,
        NextToken: str = ...
    ) -> GetSubscriptionDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a subscription definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_subscription_definition_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_subscription_definition_version)
        """

    def get_thing_runtime_configuration(
        self, *, ThingName: str
    ) -> GetThingRuntimeConfigurationResponseTypeDef:
        """
        Get the runtime configuration of a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_thing_runtime_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_thing_runtime_configuration)
        """

    def list_bulk_deployment_detailed_reports(
        self, *, BulkDeploymentId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListBulkDeploymentDetailedReportsResponseTypeDef:
        """
        Gets a paginated list of the deployments that have been started in a bulk
        deployment operation, and their current deployment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_bulk_deployment_detailed_reports)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_bulk_deployment_detailed_reports)
        """

    def list_bulk_deployments(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListBulkDeploymentsResponseTypeDef:
        """
        Returns a list of bulk deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_bulk_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_bulk_deployments)
        """

    def list_connector_definition_versions(
        self, *, ConnectorDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListConnectorDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a connector definition, which are containers for
        connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_connector_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_connector_definition_versions)
        """

    def list_connector_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListConnectorDefinitionsResponseTypeDef:
        """
        Retrieves a list of connector definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_connector_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_connector_definitions)
        """

    def list_core_definition_versions(
        self, *, CoreDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListCoreDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_core_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_core_definition_versions)
        """

    def list_core_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListCoreDefinitionsResponseTypeDef:
        """
        Retrieves a list of core definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_core_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_core_definitions)
        """

    def list_deployments(
        self, *, GroupId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListDeploymentsResponseTypeDef:
        """
        Returns a history of deployments for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_deployments)
        """

    def list_device_definition_versions(
        self, *, DeviceDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListDeviceDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_device_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_device_definition_versions)
        """

    def list_device_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListDeviceDefinitionsResponseTypeDef:
        """
        Retrieves a list of device definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_device_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_device_definitions)
        """

    def list_function_definition_versions(
        self, *, FunctionDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListFunctionDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_function_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_function_definition_versions)
        """

    def list_function_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListFunctionDefinitionsResponseTypeDef:
        """
        Retrieves a list of Lambda function definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_function_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_function_definitions)
        """

    def list_group_certificate_authorities(
        self, *, GroupId: str
    ) -> ListGroupCertificateAuthoritiesResponseTypeDef:
        """
        Retrieves the current CAs for a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_group_certificate_authorities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_group_certificate_authorities)
        """

    def list_group_versions(
        self, *, GroupId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListGroupVersionsResponseTypeDef:
        """
        Lists the versions of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_group_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_group_versions)
        """

    def list_groups(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListGroupsResponseTypeDef:
        """
        Retrieves a list of groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_groups)
        """

    def list_logger_definition_versions(
        self, *, LoggerDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListLoggerDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_logger_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_logger_definition_versions)
        """

    def list_logger_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListLoggerDefinitionsResponseTypeDef:
        """
        Retrieves a list of logger definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_logger_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_logger_definitions)
        """

    def list_resource_definition_versions(
        self, *, ResourceDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListResourceDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_resource_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_resource_definition_versions)
        """

    def list_resource_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListResourceDefinitionsResponseTypeDef:
        """
        Retrieves a list of resource definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_resource_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_resource_definitions)
        """

    def list_subscription_definition_versions(
        self, *, SubscriptionDefinitionId: str, MaxResults: str = ..., NextToken: str = ...
    ) -> ListSubscriptionDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_subscription_definition_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_subscription_definition_versions)
        """

    def list_subscription_definitions(
        self, *, MaxResults: str = ..., NextToken: str = ...
    ) -> ListSubscriptionDefinitionsResponseTypeDef:
        """
        Retrieves a list of subscription definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_subscription_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_subscription_definitions)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of resource tags for a resource arn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#list_tags_for_resource)
        """

    def reset_deployments(
        self, *, GroupId: str, AmznClientToken: str = ..., Force: bool = ...
    ) -> ResetDeploymentsResponseTypeDef:
        """
        Resets a group's deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.reset_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#reset_deployments)
        """

    def start_bulk_deployment(
        self,
        *,
        ExecutionRoleArn: str,
        InputFileUri: str,
        AmznClientToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> StartBulkDeploymentResponseTypeDef:
        """
        Deploys multiple groups in one operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.start_bulk_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#start_bulk_deployment)
        """

    def stop_bulk_deployment(self, *, BulkDeploymentId: str) -> Dict[str, Any]:
        """
        Stops the execution of a bulk deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.stop_bulk_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#stop_bulk_deployment)
        """

    def tag_resource(
        self, *, ResourceArn: str, tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove resource tags from a Greengrass Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#untag_resource)
        """

    def update_connectivity_info(
        self, *, ThingName: str, ConnectivityInfo: Sequence[ConnectivityInfoTypeDef] = ...
    ) -> UpdateConnectivityInfoResponseTypeDef:
        """
        Updates the connectivity information for the core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_connectivity_info)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_connectivity_info)
        """

    def update_connector_definition(
        self, *, ConnectorDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_connector_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_connector_definition)
        """

    def update_core_definition(self, *, CoreDefinitionId: str, Name: str = ...) -> Dict[str, Any]:
        """
        Updates a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_core_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_core_definition)
        """

    def update_device_definition(
        self, *, DeviceDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_device_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_device_definition)
        """

    def update_function_definition(
        self, *, FunctionDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_function_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_function_definition)
        """

    def update_group(self, *, GroupId: str, Name: str = ...) -> Dict[str, Any]:
        """
        Updates a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_group)
        """

    def update_group_certificate_configuration(
        self, *, GroupId: str, CertificateExpiryInMilliseconds: str = ...
    ) -> UpdateGroupCertificateConfigurationResponseTypeDef:
        """
        Updates the Certificate expiry time for a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_group_certificate_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_group_certificate_configuration)
        """

    def update_logger_definition(
        self, *, LoggerDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_logger_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_logger_definition)
        """

    def update_resource_definition(
        self, *, ResourceDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_resource_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_resource_definition)
        """

    def update_subscription_definition(
        self, *, SubscriptionDefinitionId: str, Name: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_subscription_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_subscription_definition)
        """

    def update_thing_runtime_configuration(
        self, *, ThingName: str, TelemetryConfiguration: TelemetryConfigurationUpdateTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates the runtime configuration of a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.update_thing_runtime_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#update_thing_runtime_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bulk_deployment_detailed_reports"]
    ) -> ListBulkDeploymentDetailedReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bulk_deployments"]
    ) -> ListBulkDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connector_definition_versions"]
    ) -> ListConnectorDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connector_definitions"]
    ) -> ListConnectorDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_definition_versions"]
    ) -> ListCoreDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_definitions"]
    ) -> ListCoreDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_definition_versions"]
    ) -> ListDeviceDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_definitions"]
    ) -> ListDeviceDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_definition_versions"]
    ) -> ListFunctionDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_definitions"]
    ) -> ListFunctionDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_versions"]
    ) -> ListGroupVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_logger_definition_versions"]
    ) -> ListLoggerDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_logger_definitions"]
    ) -> ListLoggerDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_definition_versions"]
    ) -> ListResourceDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_definitions"]
    ) -> ListResourceDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_definition_versions"]
    ) -> ListSubscriptionDefinitionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_definitions"]
    ) -> ListSubscriptionDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/client/#get_paginator)
        """
