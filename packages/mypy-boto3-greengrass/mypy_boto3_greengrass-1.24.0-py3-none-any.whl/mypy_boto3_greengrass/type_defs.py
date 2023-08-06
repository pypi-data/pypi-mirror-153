"""
Type annotations for greengrass service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrass/type_defs/)

Usage::

    ```python
    from mypy_boto3_greengrass.type_defs import AssociateRoleToGroupRequestRequestTypeDef

    data: AssociateRoleToGroupRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BulkDeploymentStatusType,
    ConfigurationSyncStatusType,
    DeploymentTypeType,
    EncodingTypeType,
    FunctionIsolationModeType,
    LoggerComponentType,
    LoggerLevelType,
    LoggerTypeType,
    PermissionType,
    SoftwareToUpdateType,
    TelemetryType,
    UpdateAgentLogLevelType,
    UpdateTargetsArchitectureType,
    UpdateTargetsOperatingSystemType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateRoleToGroupRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateServiceRoleToAccountRequestRequestTypeDef",
    "BulkDeploymentMetricsTypeDef",
    "ErrorDetailTypeDef",
    "BulkDeploymentTypeDef",
    "ConnectivityInfoTypeDef",
    "ConnectorTypeDef",
    "CoreTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "DeviceTypeDef",
    "CreateGroupCertificateAuthorityRequestRequestTypeDef",
    "GroupVersionTypeDef",
    "CreateGroupVersionRequestRequestTypeDef",
    "LoggerTypeDef",
    "CreateSoftwareUpdateJobRequestRequestTypeDef",
    "SubscriptionTypeDef",
    "DefinitionInformationTypeDef",
    "DeleteConnectorDefinitionRequestRequestTypeDef",
    "DeleteCoreDefinitionRequestRequestTypeDef",
    "DeleteDeviceDefinitionRequestRequestTypeDef",
    "DeleteFunctionDefinitionRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteLoggerDefinitionRequestRequestTypeDef",
    "DeleteResourceDefinitionRequestRequestTypeDef",
    "DeleteSubscriptionDefinitionRequestRequestTypeDef",
    "DeploymentTypeDef",
    "DisassociateRoleFromGroupRequestRequestTypeDef",
    "ResourceAccessPolicyTypeDef",
    "FunctionRunAsConfigTypeDef",
    "GetAssociatedRoleRequestRequestTypeDef",
    "GetBulkDeploymentStatusRequestRequestTypeDef",
    "GetConnectivityInfoRequestRequestTypeDef",
    "GetConnectorDefinitionRequestRequestTypeDef",
    "GetConnectorDefinitionVersionRequestRequestTypeDef",
    "GetCoreDefinitionRequestRequestTypeDef",
    "GetCoreDefinitionVersionRequestRequestTypeDef",
    "GetDeploymentStatusRequestRequestTypeDef",
    "GetDeviceDefinitionRequestRequestTypeDef",
    "GetDeviceDefinitionVersionRequestRequestTypeDef",
    "GetFunctionDefinitionRequestRequestTypeDef",
    "GetFunctionDefinitionVersionRequestRequestTypeDef",
    "GetGroupCertificateAuthorityRequestRequestTypeDef",
    "GetGroupCertificateConfigurationRequestRequestTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupVersionRequestRequestTypeDef",
    "GetLoggerDefinitionRequestRequestTypeDef",
    "GetLoggerDefinitionVersionRequestRequestTypeDef",
    "GetResourceDefinitionRequestRequestTypeDef",
    "GetResourceDefinitionVersionRequestRequestTypeDef",
    "GetSubscriptionDefinitionRequestRequestTypeDef",
    "GetSubscriptionDefinitionVersionRequestRequestTypeDef",
    "GetThingRuntimeConfigurationRequestRequestTypeDef",
    "GroupCertificateAuthorityPropertiesTypeDef",
    "GroupInformationTypeDef",
    "GroupOwnerSettingTypeDef",
    "PaginatorConfigTypeDef",
    "ListBulkDeploymentDetailedReportsRequestRequestTypeDef",
    "ListBulkDeploymentsRequestRequestTypeDef",
    "ListConnectorDefinitionVersionsRequestRequestTypeDef",
    "VersionInformationTypeDef",
    "ListConnectorDefinitionsRequestRequestTypeDef",
    "ListCoreDefinitionVersionsRequestRequestTypeDef",
    "ListCoreDefinitionsRequestRequestTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListDeviceDefinitionVersionsRequestRequestTypeDef",
    "ListDeviceDefinitionsRequestRequestTypeDef",
    "ListFunctionDefinitionVersionsRequestRequestTypeDef",
    "ListFunctionDefinitionsRequestRequestTypeDef",
    "ListGroupCertificateAuthoritiesRequestRequestTypeDef",
    "ListGroupVersionsRequestRequestTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListLoggerDefinitionVersionsRequestRequestTypeDef",
    "ListLoggerDefinitionsRequestRequestTypeDef",
    "ListResourceDefinitionVersionsRequestRequestTypeDef",
    "ListResourceDefinitionsRequestRequestTypeDef",
    "ListSubscriptionDefinitionVersionsRequestRequestTypeDef",
    "ListSubscriptionDefinitionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResetDeploymentsRequestRequestTypeDef",
    "SecretsManagerSecretResourceDataTypeDef",
    "ResourceDownloadOwnerSettingTypeDef",
    "TelemetryConfigurationTypeDef",
    "StartBulkDeploymentRequestRequestTypeDef",
    "StopBulkDeploymentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TelemetryConfigurationUpdateTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConnectorDefinitionRequestRequestTypeDef",
    "UpdateCoreDefinitionRequestRequestTypeDef",
    "UpdateDeviceDefinitionRequestRequestTypeDef",
    "UpdateFunctionDefinitionRequestRequestTypeDef",
    "UpdateGroupCertificateConfigurationRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateLoggerDefinitionRequestRequestTypeDef",
    "UpdateResourceDefinitionRequestRequestTypeDef",
    "UpdateSubscriptionDefinitionRequestRequestTypeDef",
    "AssociateRoleToGroupResponseTypeDef",
    "AssociateServiceRoleToAccountResponseTypeDef",
    "CreateConnectorDefinitionResponseTypeDef",
    "CreateConnectorDefinitionVersionResponseTypeDef",
    "CreateCoreDefinitionResponseTypeDef",
    "CreateCoreDefinitionVersionResponseTypeDef",
    "CreateDeploymentResponseTypeDef",
    "CreateDeviceDefinitionResponseTypeDef",
    "CreateDeviceDefinitionVersionResponseTypeDef",
    "CreateFunctionDefinitionResponseTypeDef",
    "CreateFunctionDefinitionVersionResponseTypeDef",
    "CreateGroupCertificateAuthorityResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateGroupVersionResponseTypeDef",
    "CreateLoggerDefinitionResponseTypeDef",
    "CreateLoggerDefinitionVersionResponseTypeDef",
    "CreateResourceDefinitionResponseTypeDef",
    "CreateResourceDefinitionVersionResponseTypeDef",
    "CreateSoftwareUpdateJobResponseTypeDef",
    "CreateSubscriptionDefinitionResponseTypeDef",
    "CreateSubscriptionDefinitionVersionResponseTypeDef",
    "DisassociateRoleFromGroupResponseTypeDef",
    "DisassociateServiceRoleFromAccountResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAssociatedRoleResponseTypeDef",
    "GetConnectorDefinitionResponseTypeDef",
    "GetCoreDefinitionResponseTypeDef",
    "GetDeviceDefinitionResponseTypeDef",
    "GetFunctionDefinitionResponseTypeDef",
    "GetGroupCertificateAuthorityResponseTypeDef",
    "GetGroupCertificateConfigurationResponseTypeDef",
    "GetGroupResponseTypeDef",
    "GetLoggerDefinitionResponseTypeDef",
    "GetResourceDefinitionResponseTypeDef",
    "GetServiceRoleForAccountResponseTypeDef",
    "GetSubscriptionDefinitionResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ResetDeploymentsResponseTypeDef",
    "StartBulkDeploymentResponseTypeDef",
    "UpdateConnectivityInfoResponseTypeDef",
    "UpdateGroupCertificateConfigurationResponseTypeDef",
    "BulkDeploymentResultTypeDef",
    "GetBulkDeploymentStatusResponseTypeDef",
    "GetDeploymentStatusResponseTypeDef",
    "ListBulkDeploymentsResponseTypeDef",
    "GetConnectivityInfoResponseTypeDef",
    "UpdateConnectivityInfoRequestRequestTypeDef",
    "ConnectorDefinitionVersionTypeDef",
    "CreateConnectorDefinitionVersionRequestRequestTypeDef",
    "CoreDefinitionVersionTypeDef",
    "CreateCoreDefinitionVersionRequestRequestTypeDef",
    "CreateDeviceDefinitionVersionRequestRequestTypeDef",
    "DeviceDefinitionVersionTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "GetGroupVersionResponseTypeDef",
    "CreateLoggerDefinitionVersionRequestRequestTypeDef",
    "LoggerDefinitionVersionTypeDef",
    "CreateSubscriptionDefinitionVersionRequestRequestTypeDef",
    "SubscriptionDefinitionVersionTypeDef",
    "ListConnectorDefinitionsResponseTypeDef",
    "ListCoreDefinitionsResponseTypeDef",
    "ListDeviceDefinitionsResponseTypeDef",
    "ListFunctionDefinitionsResponseTypeDef",
    "ListLoggerDefinitionsResponseTypeDef",
    "ListResourceDefinitionsResponseTypeDef",
    "ListSubscriptionDefinitionsResponseTypeDef",
    "ListDeploymentsResponseTypeDef",
    "FunctionDefaultExecutionConfigTypeDef",
    "FunctionExecutionConfigTypeDef",
    "ListGroupCertificateAuthoritiesResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "LocalDeviceResourceDataTypeDef",
    "LocalVolumeResourceDataTypeDef",
    "ListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef",
    "ListBulkDeploymentsRequestListBulkDeploymentsPaginateTypeDef",
    "ListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef",
    "ListConnectorDefinitionsRequestListConnectorDefinitionsPaginateTypeDef",
    "ListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef",
    "ListCoreDefinitionsRequestListCoreDefinitionsPaginateTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef",
    "ListDeviceDefinitionsRequestListDeviceDefinitionsPaginateTypeDef",
    "ListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef",
    "ListFunctionDefinitionsRequestListFunctionDefinitionsPaginateTypeDef",
    "ListGroupVersionsRequestListGroupVersionsPaginateTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef",
    "ListLoggerDefinitionsRequestListLoggerDefinitionsPaginateTypeDef",
    "ListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef",
    "ListResourceDefinitionsRequestListResourceDefinitionsPaginateTypeDef",
    "ListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef",
    "ListSubscriptionDefinitionsRequestListSubscriptionDefinitionsPaginateTypeDef",
    "ListConnectorDefinitionVersionsResponseTypeDef",
    "ListCoreDefinitionVersionsResponseTypeDef",
    "ListDeviceDefinitionVersionsResponseTypeDef",
    "ListFunctionDefinitionVersionsResponseTypeDef",
    "ListGroupVersionsResponseTypeDef",
    "ListLoggerDefinitionVersionsResponseTypeDef",
    "ListResourceDefinitionVersionsResponseTypeDef",
    "ListSubscriptionDefinitionVersionsResponseTypeDef",
    "S3MachineLearningModelResourceDataTypeDef",
    "SageMakerMachineLearningModelResourceDataTypeDef",
    "RuntimeConfigurationTypeDef",
    "UpdateThingRuntimeConfigurationRequestRequestTypeDef",
    "ListBulkDeploymentDetailedReportsResponseTypeDef",
    "CreateConnectorDefinitionRequestRequestTypeDef",
    "GetConnectorDefinitionVersionResponseTypeDef",
    "CreateCoreDefinitionRequestRequestTypeDef",
    "GetCoreDefinitionVersionResponseTypeDef",
    "CreateDeviceDefinitionRequestRequestTypeDef",
    "GetDeviceDefinitionVersionResponseTypeDef",
    "CreateLoggerDefinitionRequestRequestTypeDef",
    "GetLoggerDefinitionVersionResponseTypeDef",
    "CreateSubscriptionDefinitionRequestRequestTypeDef",
    "GetSubscriptionDefinitionVersionResponseTypeDef",
    "FunctionDefaultConfigTypeDef",
    "FunctionConfigurationEnvironmentTypeDef",
    "ResourceDataContainerTypeDef",
    "GetThingRuntimeConfigurationResponseTypeDef",
    "FunctionConfigurationTypeDef",
    "ResourceTypeDef",
    "FunctionTypeDef",
    "CreateResourceDefinitionVersionRequestRequestTypeDef",
    "ResourceDefinitionVersionTypeDef",
    "CreateFunctionDefinitionVersionRequestRequestTypeDef",
    "FunctionDefinitionVersionTypeDef",
    "CreateResourceDefinitionRequestRequestTypeDef",
    "GetResourceDefinitionVersionResponseTypeDef",
    "CreateFunctionDefinitionRequestRequestTypeDef",
    "GetFunctionDefinitionVersionResponseTypeDef",
)

AssociateRoleToGroupRequestRequestTypeDef = TypedDict(
    "AssociateRoleToGroupRequestRequestTypeDef",
    {
        "GroupId": str,
        "RoleArn": str,
    },
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

AssociateServiceRoleToAccountRequestRequestTypeDef = TypedDict(
    "AssociateServiceRoleToAccountRequestRequestTypeDef",
    {
        "RoleArn": str,
    },
)

BulkDeploymentMetricsTypeDef = TypedDict(
    "BulkDeploymentMetricsTypeDef",
    {
        "InvalidInputRecords": int,
        "RecordsProcessed": int,
        "RetryAttempts": int,
    },
    total=False,
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "DetailedErrorCode": str,
        "DetailedErrorMessage": str,
    },
    total=False,
)

BulkDeploymentTypeDef = TypedDict(
    "BulkDeploymentTypeDef",
    {
        "BulkDeploymentArn": str,
        "BulkDeploymentId": str,
        "CreatedAt": str,
    },
    total=False,
)

ConnectivityInfoTypeDef = TypedDict(
    "ConnectivityInfoTypeDef",
    {
        "HostAddress": str,
        "Id": str,
        "Metadata": str,
        "PortNumber": int,
    },
    total=False,
)

_RequiredConnectorTypeDef = TypedDict(
    "_RequiredConnectorTypeDef",
    {
        "ConnectorArn": str,
        "Id": str,
    },
)
_OptionalConnectorTypeDef = TypedDict(
    "_OptionalConnectorTypeDef",
    {
        "Parameters": Mapping[str, str],
    },
    total=False,
)


class ConnectorTypeDef(_RequiredConnectorTypeDef, _OptionalConnectorTypeDef):
    pass


_RequiredCoreTypeDef = TypedDict(
    "_RequiredCoreTypeDef",
    {
        "CertificateArn": str,
        "Id": str,
        "ThingArn": str,
    },
)
_OptionalCoreTypeDef = TypedDict(
    "_OptionalCoreTypeDef",
    {
        "SyncShadow": bool,
    },
    total=False,
)


class CoreTypeDef(_RequiredCoreTypeDef, _OptionalCoreTypeDef):
    pass


_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "DeploymentType": DeploymentTypeType,
        "GroupId": str,
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "DeploymentId": str,
        "GroupVersionId": str,
    },
    total=False,
)


class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass


_RequiredDeviceTypeDef = TypedDict(
    "_RequiredDeviceTypeDef",
    {
        "CertificateArn": str,
        "Id": str,
        "ThingArn": str,
    },
)
_OptionalDeviceTypeDef = TypedDict(
    "_OptionalDeviceTypeDef",
    {
        "SyncShadow": bool,
    },
    total=False,
)


class DeviceTypeDef(_RequiredDeviceTypeDef, _OptionalDeviceTypeDef):
    pass


_RequiredCreateGroupCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupCertificateAuthorityRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalCreateGroupCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupCertificateAuthorityRequestRequestTypeDef",
    {
        "AmznClientToken": str,
    },
    total=False,
)


class CreateGroupCertificateAuthorityRequestRequestTypeDef(
    _RequiredCreateGroupCertificateAuthorityRequestRequestTypeDef,
    _OptionalCreateGroupCertificateAuthorityRequestRequestTypeDef,
):
    pass


GroupVersionTypeDef = TypedDict(
    "GroupVersionTypeDef",
    {
        "ConnectorDefinitionVersionArn": str,
        "CoreDefinitionVersionArn": str,
        "DeviceDefinitionVersionArn": str,
        "FunctionDefinitionVersionArn": str,
        "LoggerDefinitionVersionArn": str,
        "ResourceDefinitionVersionArn": str,
        "SubscriptionDefinitionVersionArn": str,
    },
    total=False,
)

_RequiredCreateGroupVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupVersionRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalCreateGroupVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "ConnectorDefinitionVersionArn": str,
        "CoreDefinitionVersionArn": str,
        "DeviceDefinitionVersionArn": str,
        "FunctionDefinitionVersionArn": str,
        "LoggerDefinitionVersionArn": str,
        "ResourceDefinitionVersionArn": str,
        "SubscriptionDefinitionVersionArn": str,
    },
    total=False,
)


class CreateGroupVersionRequestRequestTypeDef(
    _RequiredCreateGroupVersionRequestRequestTypeDef,
    _OptionalCreateGroupVersionRequestRequestTypeDef,
):
    pass


_RequiredLoggerTypeDef = TypedDict(
    "_RequiredLoggerTypeDef",
    {
        "Component": LoggerComponentType,
        "Id": str,
        "Level": LoggerLevelType,
        "Type": LoggerTypeType,
    },
)
_OptionalLoggerTypeDef = TypedDict(
    "_OptionalLoggerTypeDef",
    {
        "Space": int,
    },
    total=False,
)


class LoggerTypeDef(_RequiredLoggerTypeDef, _OptionalLoggerTypeDef):
    pass


_RequiredCreateSoftwareUpdateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSoftwareUpdateJobRequestRequestTypeDef",
    {
        "S3UrlSignerRole": str,
        "SoftwareToUpdate": SoftwareToUpdateType,
        "UpdateTargets": Sequence[str],
        "UpdateTargetsArchitecture": UpdateTargetsArchitectureType,
        "UpdateTargetsOperatingSystem": UpdateTargetsOperatingSystemType,
    },
)
_OptionalCreateSoftwareUpdateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSoftwareUpdateJobRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "UpdateAgentLogLevel": UpdateAgentLogLevelType,
    },
    total=False,
)


class CreateSoftwareUpdateJobRequestRequestTypeDef(
    _RequiredCreateSoftwareUpdateJobRequestRequestTypeDef,
    _OptionalCreateSoftwareUpdateJobRequestRequestTypeDef,
):
    pass


SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "Id": str,
        "Source": str,
        "Subject": str,
        "Target": str,
    },
)

DefinitionInformationTypeDef = TypedDict(
    "DefinitionInformationTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

DeleteConnectorDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteConnectorDefinitionRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)

DeleteCoreDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteCoreDefinitionRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
    },
)

DeleteDeviceDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteDeviceDefinitionRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)

DeleteFunctionDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteFunctionDefinitionRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

DeleteLoggerDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteLoggerDefinitionRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)

DeleteResourceDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteResourceDefinitionRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)

DeleteSubscriptionDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteSubscriptionDefinitionRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "CreatedAt": str,
        "DeploymentArn": str,
        "DeploymentId": str,
        "DeploymentType": DeploymentTypeType,
        "GroupArn": str,
    },
    total=False,
)

DisassociateRoleFromGroupRequestRequestTypeDef = TypedDict(
    "DisassociateRoleFromGroupRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

_RequiredResourceAccessPolicyTypeDef = TypedDict(
    "_RequiredResourceAccessPolicyTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalResourceAccessPolicyTypeDef = TypedDict(
    "_OptionalResourceAccessPolicyTypeDef",
    {
        "Permission": PermissionType,
    },
    total=False,
)


class ResourceAccessPolicyTypeDef(
    _RequiredResourceAccessPolicyTypeDef, _OptionalResourceAccessPolicyTypeDef
):
    pass


FunctionRunAsConfigTypeDef = TypedDict(
    "FunctionRunAsConfigTypeDef",
    {
        "Gid": int,
        "Uid": int,
    },
    total=False,
)

GetAssociatedRoleRequestRequestTypeDef = TypedDict(
    "GetAssociatedRoleRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

GetBulkDeploymentStatusRequestRequestTypeDef = TypedDict(
    "GetBulkDeploymentStatusRequestRequestTypeDef",
    {
        "BulkDeploymentId": str,
    },
)

GetConnectivityInfoRequestRequestTypeDef = TypedDict(
    "GetConnectivityInfoRequestRequestTypeDef",
    {
        "ThingName": str,
    },
)

GetConnectorDefinitionRequestRequestTypeDef = TypedDict(
    "GetConnectorDefinitionRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)

_RequiredGetConnectorDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetConnectorDefinitionVersionRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
        "ConnectorDefinitionVersionId": str,
    },
)
_OptionalGetConnectorDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetConnectorDefinitionVersionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetConnectorDefinitionVersionRequestRequestTypeDef(
    _RequiredGetConnectorDefinitionVersionRequestRequestTypeDef,
    _OptionalGetConnectorDefinitionVersionRequestRequestTypeDef,
):
    pass


GetCoreDefinitionRequestRequestTypeDef = TypedDict(
    "GetCoreDefinitionRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
    },
)

GetCoreDefinitionVersionRequestRequestTypeDef = TypedDict(
    "GetCoreDefinitionVersionRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
        "CoreDefinitionVersionId": str,
    },
)

GetDeploymentStatusRequestRequestTypeDef = TypedDict(
    "GetDeploymentStatusRequestRequestTypeDef",
    {
        "DeploymentId": str,
        "GroupId": str,
    },
)

GetDeviceDefinitionRequestRequestTypeDef = TypedDict(
    "GetDeviceDefinitionRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)

_RequiredGetDeviceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetDeviceDefinitionVersionRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
        "DeviceDefinitionVersionId": str,
    },
)
_OptionalGetDeviceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetDeviceDefinitionVersionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetDeviceDefinitionVersionRequestRequestTypeDef(
    _RequiredGetDeviceDefinitionVersionRequestRequestTypeDef,
    _OptionalGetDeviceDefinitionVersionRequestRequestTypeDef,
):
    pass


GetFunctionDefinitionRequestRequestTypeDef = TypedDict(
    "GetFunctionDefinitionRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)

_RequiredGetFunctionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetFunctionDefinitionVersionRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
        "FunctionDefinitionVersionId": str,
    },
)
_OptionalGetFunctionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetFunctionDefinitionVersionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetFunctionDefinitionVersionRequestRequestTypeDef(
    _RequiredGetFunctionDefinitionVersionRequestRequestTypeDef,
    _OptionalGetFunctionDefinitionVersionRequestRequestTypeDef,
):
    pass


GetGroupCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "GetGroupCertificateAuthorityRequestRequestTypeDef",
    {
        "CertificateAuthorityId": str,
        "GroupId": str,
    },
)

GetGroupCertificateConfigurationRequestRequestTypeDef = TypedDict(
    "GetGroupCertificateConfigurationRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

GetGroupRequestRequestTypeDef = TypedDict(
    "GetGroupRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

GetGroupVersionRequestRequestTypeDef = TypedDict(
    "GetGroupVersionRequestRequestTypeDef",
    {
        "GroupId": str,
        "GroupVersionId": str,
    },
)

GetLoggerDefinitionRequestRequestTypeDef = TypedDict(
    "GetLoggerDefinitionRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)

_RequiredGetLoggerDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetLoggerDefinitionVersionRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
        "LoggerDefinitionVersionId": str,
    },
)
_OptionalGetLoggerDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetLoggerDefinitionVersionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetLoggerDefinitionVersionRequestRequestTypeDef(
    _RequiredGetLoggerDefinitionVersionRequestRequestTypeDef,
    _OptionalGetLoggerDefinitionVersionRequestRequestTypeDef,
):
    pass


GetResourceDefinitionRequestRequestTypeDef = TypedDict(
    "GetResourceDefinitionRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)

GetResourceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "GetResourceDefinitionVersionRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
        "ResourceDefinitionVersionId": str,
    },
)

GetSubscriptionDefinitionRequestRequestTypeDef = TypedDict(
    "GetSubscriptionDefinitionRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)

_RequiredGetSubscriptionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetSubscriptionDefinitionVersionRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
        "SubscriptionDefinitionVersionId": str,
    },
)
_OptionalGetSubscriptionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetSubscriptionDefinitionVersionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetSubscriptionDefinitionVersionRequestRequestTypeDef(
    _RequiredGetSubscriptionDefinitionVersionRequestRequestTypeDef,
    _OptionalGetSubscriptionDefinitionVersionRequestRequestTypeDef,
):
    pass


GetThingRuntimeConfigurationRequestRequestTypeDef = TypedDict(
    "GetThingRuntimeConfigurationRequestRequestTypeDef",
    {
        "ThingName": str,
    },
)

GroupCertificateAuthorityPropertiesTypeDef = TypedDict(
    "GroupCertificateAuthorityPropertiesTypeDef",
    {
        "GroupCertificateAuthorityArn": str,
        "GroupCertificateAuthorityId": str,
    },
    total=False,
)

GroupInformationTypeDef = TypedDict(
    "GroupInformationTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
    },
    total=False,
)

GroupOwnerSettingTypeDef = TypedDict(
    "GroupOwnerSettingTypeDef",
    {
        "AutoAddGroupOwner": bool,
        "GroupOwner": str,
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

_RequiredListBulkDeploymentDetailedReportsRequestRequestTypeDef = TypedDict(
    "_RequiredListBulkDeploymentDetailedReportsRequestRequestTypeDef",
    {
        "BulkDeploymentId": str,
    },
)
_OptionalListBulkDeploymentDetailedReportsRequestRequestTypeDef = TypedDict(
    "_OptionalListBulkDeploymentDetailedReportsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListBulkDeploymentDetailedReportsRequestRequestTypeDef(
    _RequiredListBulkDeploymentDetailedReportsRequestRequestTypeDef,
    _OptionalListBulkDeploymentDetailedReportsRequestRequestTypeDef,
):
    pass


ListBulkDeploymentsRequestRequestTypeDef = TypedDict(
    "ListBulkDeploymentsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListConnectorDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListConnectorDefinitionVersionsRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)
_OptionalListConnectorDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListConnectorDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListConnectorDefinitionVersionsRequestRequestTypeDef(
    _RequiredListConnectorDefinitionVersionsRequestRequestTypeDef,
    _OptionalListConnectorDefinitionVersionsRequestRequestTypeDef,
):
    pass


VersionInformationTypeDef = TypedDict(
    "VersionInformationTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
    },
    total=False,
)

ListConnectorDefinitionsRequestRequestTypeDef = TypedDict(
    "ListConnectorDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListCoreDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListCoreDefinitionVersionsRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
    },
)
_OptionalListCoreDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListCoreDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListCoreDefinitionVersionsRequestRequestTypeDef(
    _RequiredListCoreDefinitionVersionsRequestRequestTypeDef,
    _OptionalListCoreDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListCoreDefinitionsRequestRequestTypeDef = TypedDict(
    "ListCoreDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredListDeploymentsRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalListDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalListDeploymentsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListDeploymentsRequestRequestTypeDef(
    _RequiredListDeploymentsRequestRequestTypeDef, _OptionalListDeploymentsRequestRequestTypeDef
):
    pass


_RequiredListDeviceDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDeviceDefinitionVersionsRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)
_OptionalListDeviceDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDeviceDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListDeviceDefinitionVersionsRequestRequestTypeDef(
    _RequiredListDeviceDefinitionVersionsRequestRequestTypeDef,
    _OptionalListDeviceDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListDeviceDefinitionsRequestRequestTypeDef = TypedDict(
    "ListDeviceDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListFunctionDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListFunctionDefinitionVersionsRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)
_OptionalListFunctionDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListFunctionDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListFunctionDefinitionVersionsRequestRequestTypeDef(
    _RequiredListFunctionDefinitionVersionsRequestRequestTypeDef,
    _OptionalListFunctionDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListFunctionDefinitionsRequestRequestTypeDef = TypedDict(
    "ListFunctionDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

ListGroupCertificateAuthoritiesRequestRequestTypeDef = TypedDict(
    "ListGroupCertificateAuthoritiesRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)

_RequiredListGroupVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupVersionsRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalListGroupVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListGroupVersionsRequestRequestTypeDef(
    _RequiredListGroupVersionsRequestRequestTypeDef, _OptionalListGroupVersionsRequestRequestTypeDef
):
    pass


ListGroupsRequestRequestTypeDef = TypedDict(
    "ListGroupsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListLoggerDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListLoggerDefinitionVersionsRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)
_OptionalListLoggerDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListLoggerDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListLoggerDefinitionVersionsRequestRequestTypeDef(
    _RequiredListLoggerDefinitionVersionsRequestRequestTypeDef,
    _OptionalListLoggerDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListLoggerDefinitionsRequestRequestTypeDef = TypedDict(
    "ListLoggerDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListResourceDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListResourceDefinitionVersionsRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)
_OptionalListResourceDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListResourceDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListResourceDefinitionVersionsRequestRequestTypeDef(
    _RequiredListResourceDefinitionVersionsRequestRequestTypeDef,
    _OptionalListResourceDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListResourceDefinitionsRequestRequestTypeDef = TypedDict(
    "ListResourceDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

_RequiredListSubscriptionDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSubscriptionDefinitionVersionsRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)
_OptionalListSubscriptionDefinitionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSubscriptionDefinitionVersionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)


class ListSubscriptionDefinitionVersionsRequestRequestTypeDef(
    _RequiredListSubscriptionDefinitionVersionsRequestRequestTypeDef,
    _OptionalListSubscriptionDefinitionVersionsRequestRequestTypeDef,
):
    pass


ListSubscriptionDefinitionsRequestRequestTypeDef = TypedDict(
    "ListSubscriptionDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": str,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredResetDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredResetDeploymentsRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalResetDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalResetDeploymentsRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Force": bool,
    },
    total=False,
)


class ResetDeploymentsRequestRequestTypeDef(
    _RequiredResetDeploymentsRequestRequestTypeDef, _OptionalResetDeploymentsRequestRequestTypeDef
):
    pass


SecretsManagerSecretResourceDataTypeDef = TypedDict(
    "SecretsManagerSecretResourceDataTypeDef",
    {
        "ARN": str,
        "AdditionalStagingLabelsToDownload": Sequence[str],
    },
    total=False,
)

ResourceDownloadOwnerSettingTypeDef = TypedDict(
    "ResourceDownloadOwnerSettingTypeDef",
    {
        "GroupOwner": str,
        "GroupPermission": PermissionType,
    },
)

_RequiredTelemetryConfigurationTypeDef = TypedDict(
    "_RequiredTelemetryConfigurationTypeDef",
    {
        "Telemetry": TelemetryType,
    },
)
_OptionalTelemetryConfigurationTypeDef = TypedDict(
    "_OptionalTelemetryConfigurationTypeDef",
    {
        "ConfigurationSyncStatus": ConfigurationSyncStatusType,
    },
    total=False,
)


class TelemetryConfigurationTypeDef(
    _RequiredTelemetryConfigurationTypeDef, _OptionalTelemetryConfigurationTypeDef
):
    pass


_RequiredStartBulkDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredStartBulkDeploymentRequestRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "InputFileUri": str,
    },
)
_OptionalStartBulkDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalStartBulkDeploymentRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartBulkDeploymentRequestRequestTypeDef(
    _RequiredStartBulkDeploymentRequestRequestTypeDef,
    _OptionalStartBulkDeploymentRequestRequestTypeDef,
):
    pass


StopBulkDeploymentRequestRequestTypeDef = TypedDict(
    "StopBulkDeploymentRequestRequestTypeDef",
    {
        "BulkDeploymentId": str,
    },
)

_RequiredTagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredTagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalTagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalTagResourceRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class TagResourceRequestRequestTypeDef(
    _RequiredTagResourceRequestRequestTypeDef, _OptionalTagResourceRequestRequestTypeDef
):
    pass


TelemetryConfigurationUpdateTypeDef = TypedDict(
    "TelemetryConfigurationUpdateTypeDef",
    {
        "Telemetry": TelemetryType,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateConnectorDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConnectorDefinitionRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)
_OptionalUpdateConnectorDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConnectorDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateConnectorDefinitionRequestRequestTypeDef(
    _RequiredUpdateConnectorDefinitionRequestRequestTypeDef,
    _OptionalUpdateConnectorDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateCoreDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCoreDefinitionRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
    },
)
_OptionalUpdateCoreDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCoreDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateCoreDefinitionRequestRequestTypeDef(
    _RequiredUpdateCoreDefinitionRequestRequestTypeDef,
    _OptionalUpdateCoreDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateDeviceDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDeviceDefinitionRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)
_OptionalUpdateDeviceDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDeviceDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateDeviceDefinitionRequestRequestTypeDef(
    _RequiredUpdateDeviceDefinitionRequestRequestTypeDef,
    _OptionalUpdateDeviceDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateFunctionDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFunctionDefinitionRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)
_OptionalUpdateFunctionDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFunctionDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateFunctionDefinitionRequestRequestTypeDef(
    _RequiredUpdateFunctionDefinitionRequestRequestTypeDef,
    _OptionalUpdateFunctionDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateGroupCertificateConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupCertificateConfigurationRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalUpdateGroupCertificateConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupCertificateConfigurationRequestRequestTypeDef",
    {
        "CertificateExpiryInMilliseconds": str,
    },
    total=False,
)


class UpdateGroupCertificateConfigurationRequestRequestTypeDef(
    _RequiredUpdateGroupCertificateConfigurationRequestRequestTypeDef,
    _OptionalUpdateGroupCertificateConfigurationRequestRequestTypeDef,
):
    pass


_RequiredUpdateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupRequestRequestTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalUpdateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateGroupRequestRequestTypeDef(
    _RequiredUpdateGroupRequestRequestTypeDef, _OptionalUpdateGroupRequestRequestTypeDef
):
    pass


_RequiredUpdateLoggerDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLoggerDefinitionRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)
_OptionalUpdateLoggerDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLoggerDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateLoggerDefinitionRequestRequestTypeDef(
    _RequiredUpdateLoggerDefinitionRequestRequestTypeDef,
    _OptionalUpdateLoggerDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateResourceDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceDefinitionRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)
_OptionalUpdateResourceDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateResourceDefinitionRequestRequestTypeDef(
    _RequiredUpdateResourceDefinitionRequestRequestTypeDef,
    _OptionalUpdateResourceDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateSubscriptionDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubscriptionDefinitionRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)
_OptionalUpdateSubscriptionDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubscriptionDefinitionRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateSubscriptionDefinitionRequestRequestTypeDef(
    _RequiredUpdateSubscriptionDefinitionRequestRequestTypeDef,
    _OptionalUpdateSubscriptionDefinitionRequestRequestTypeDef,
):
    pass


AssociateRoleToGroupResponseTypeDef = TypedDict(
    "AssociateRoleToGroupResponseTypeDef",
    {
        "AssociatedAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateServiceRoleToAccountResponseTypeDef = TypedDict(
    "AssociateServiceRoleToAccountResponseTypeDef",
    {
        "AssociatedAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConnectorDefinitionResponseTypeDef = TypedDict(
    "CreateConnectorDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConnectorDefinitionVersionResponseTypeDef = TypedDict(
    "CreateConnectorDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCoreDefinitionResponseTypeDef = TypedDict(
    "CreateCoreDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCoreDefinitionVersionResponseTypeDef = TypedDict(
    "CreateCoreDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentResponseTypeDef = TypedDict(
    "CreateDeploymentResponseTypeDef",
    {
        "DeploymentArn": str,
        "DeploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeviceDefinitionResponseTypeDef = TypedDict(
    "CreateDeviceDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeviceDefinitionVersionResponseTypeDef = TypedDict(
    "CreateDeviceDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFunctionDefinitionResponseTypeDef = TypedDict(
    "CreateFunctionDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFunctionDefinitionVersionResponseTypeDef = TypedDict(
    "CreateFunctionDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupCertificateAuthorityResponseTypeDef = TypedDict(
    "CreateGroupCertificateAuthorityResponseTypeDef",
    {
        "GroupCertificateAuthorityArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupVersionResponseTypeDef = TypedDict(
    "CreateGroupVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLoggerDefinitionResponseTypeDef = TypedDict(
    "CreateLoggerDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLoggerDefinitionVersionResponseTypeDef = TypedDict(
    "CreateLoggerDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourceDefinitionResponseTypeDef = TypedDict(
    "CreateResourceDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourceDefinitionVersionResponseTypeDef = TypedDict(
    "CreateResourceDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSoftwareUpdateJobResponseTypeDef = TypedDict(
    "CreateSoftwareUpdateJobResponseTypeDef",
    {
        "IotJobArn": str,
        "IotJobId": str,
        "PlatformSoftwareVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriptionDefinitionResponseTypeDef = TypedDict(
    "CreateSubscriptionDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriptionDefinitionVersionResponseTypeDef = TypedDict(
    "CreateSubscriptionDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateRoleFromGroupResponseTypeDef = TypedDict(
    "DisassociateRoleFromGroupResponseTypeDef",
    {
        "DisassociatedAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateServiceRoleFromAccountResponseTypeDef = TypedDict(
    "DisassociateServiceRoleFromAccountResponseTypeDef",
    {
        "DisassociatedAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssociatedRoleResponseTypeDef = TypedDict(
    "GetAssociatedRoleResponseTypeDef",
    {
        "AssociatedAt": str,
        "RoleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectorDefinitionResponseTypeDef = TypedDict(
    "GetConnectorDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCoreDefinitionResponseTypeDef = TypedDict(
    "GetCoreDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeviceDefinitionResponseTypeDef = TypedDict(
    "GetDeviceDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFunctionDefinitionResponseTypeDef = TypedDict(
    "GetFunctionDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupCertificateAuthorityResponseTypeDef = TypedDict(
    "GetGroupCertificateAuthorityResponseTypeDef",
    {
        "GroupCertificateAuthorityArn": str,
        "GroupCertificateAuthorityId": str,
        "PemEncodedCertificate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupCertificateConfigurationResponseTypeDef = TypedDict(
    "GetGroupCertificateConfigurationResponseTypeDef",
    {
        "CertificateAuthorityExpiryInMilliseconds": str,
        "CertificateExpiryInMilliseconds": str,
        "GroupId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupResponseTypeDef = TypedDict(
    "GetGroupResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLoggerDefinitionResponseTypeDef = TypedDict(
    "GetLoggerDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceDefinitionResponseTypeDef = TypedDict(
    "GetResourceDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceRoleForAccountResponseTypeDef = TypedDict(
    "GetServiceRoleForAccountResponseTypeDef",
    {
        "AssociatedAt": str,
        "RoleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriptionDefinitionResponseTypeDef = TypedDict(
    "GetSubscriptionDefinitionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Id": str,
        "LastUpdatedTimestamp": str,
        "LatestVersion": str,
        "LatestVersionArn": str,
        "Name": str,
        "tags": Dict[str, str],
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

ResetDeploymentsResponseTypeDef = TypedDict(
    "ResetDeploymentsResponseTypeDef",
    {
        "DeploymentArn": str,
        "DeploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBulkDeploymentResponseTypeDef = TypedDict(
    "StartBulkDeploymentResponseTypeDef",
    {
        "BulkDeploymentArn": str,
        "BulkDeploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConnectivityInfoResponseTypeDef = TypedDict(
    "UpdateConnectivityInfoResponseTypeDef",
    {
        "Message": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGroupCertificateConfigurationResponseTypeDef = TypedDict(
    "UpdateGroupCertificateConfigurationResponseTypeDef",
    {
        "CertificateAuthorityExpiryInMilliseconds": str,
        "CertificateExpiryInMilliseconds": str,
        "GroupId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BulkDeploymentResultTypeDef = TypedDict(
    "BulkDeploymentResultTypeDef",
    {
        "CreatedAt": str,
        "DeploymentArn": str,
        "DeploymentId": str,
        "DeploymentStatus": str,
        "DeploymentType": DeploymentTypeType,
        "ErrorDetails": List[ErrorDetailTypeDef],
        "ErrorMessage": str,
        "GroupArn": str,
    },
    total=False,
)

GetBulkDeploymentStatusResponseTypeDef = TypedDict(
    "GetBulkDeploymentStatusResponseTypeDef",
    {
        "BulkDeploymentMetrics": BulkDeploymentMetricsTypeDef,
        "BulkDeploymentStatus": BulkDeploymentStatusType,
        "CreatedAt": str,
        "ErrorDetails": List[ErrorDetailTypeDef],
        "ErrorMessage": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentStatusResponseTypeDef = TypedDict(
    "GetDeploymentStatusResponseTypeDef",
    {
        "DeploymentStatus": str,
        "DeploymentType": DeploymentTypeType,
        "ErrorDetails": List[ErrorDetailTypeDef],
        "ErrorMessage": str,
        "UpdatedAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBulkDeploymentsResponseTypeDef = TypedDict(
    "ListBulkDeploymentsResponseTypeDef",
    {
        "BulkDeployments": List[BulkDeploymentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectivityInfoResponseTypeDef = TypedDict(
    "GetConnectivityInfoResponseTypeDef",
    {
        "ConnectivityInfo": List[ConnectivityInfoTypeDef],
        "Message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateConnectivityInfoRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConnectivityInfoRequestRequestTypeDef",
    {
        "ThingName": str,
    },
)
_OptionalUpdateConnectivityInfoRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConnectivityInfoRequestRequestTypeDef",
    {
        "ConnectivityInfo": Sequence[ConnectivityInfoTypeDef],
    },
    total=False,
)


class UpdateConnectivityInfoRequestRequestTypeDef(
    _RequiredUpdateConnectivityInfoRequestRequestTypeDef,
    _OptionalUpdateConnectivityInfoRequestRequestTypeDef,
):
    pass


ConnectorDefinitionVersionTypeDef = TypedDict(
    "ConnectorDefinitionVersionTypeDef",
    {
        "Connectors": Sequence[ConnectorTypeDef],
    },
    total=False,
)

_RequiredCreateConnectorDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConnectorDefinitionVersionRequestRequestTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)
_OptionalCreateConnectorDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConnectorDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Connectors": Sequence[ConnectorTypeDef],
    },
    total=False,
)


class CreateConnectorDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateConnectorDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateConnectorDefinitionVersionRequestRequestTypeDef,
):
    pass


CoreDefinitionVersionTypeDef = TypedDict(
    "CoreDefinitionVersionTypeDef",
    {
        "Cores": Sequence[CoreTypeDef],
    },
    total=False,
)

_RequiredCreateCoreDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCoreDefinitionVersionRequestRequestTypeDef",
    {
        "CoreDefinitionId": str,
    },
)
_OptionalCreateCoreDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCoreDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Cores": Sequence[CoreTypeDef],
    },
    total=False,
)


class CreateCoreDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateCoreDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateCoreDefinitionVersionRequestRequestTypeDef,
):
    pass


_RequiredCreateDeviceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeviceDefinitionVersionRequestRequestTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)
_OptionalCreateDeviceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeviceDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Devices": Sequence[DeviceTypeDef],
    },
    total=False,
)


class CreateDeviceDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateDeviceDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateDeviceDefinitionVersionRequestRequestTypeDef,
):
    pass


DeviceDefinitionVersionTypeDef = TypedDict(
    "DeviceDefinitionVersionTypeDef",
    {
        "Devices": Sequence[DeviceTypeDef],
    },
    total=False,
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": GroupVersionTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass


GetGroupVersionResponseTypeDef = TypedDict(
    "GetGroupVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": GroupVersionTypeDef,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLoggerDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLoggerDefinitionVersionRequestRequestTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)
_OptionalCreateLoggerDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLoggerDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Loggers": Sequence[LoggerTypeDef],
    },
    total=False,
)


class CreateLoggerDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateLoggerDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateLoggerDefinitionVersionRequestRequestTypeDef,
):
    pass


LoggerDefinitionVersionTypeDef = TypedDict(
    "LoggerDefinitionVersionTypeDef",
    {
        "Loggers": Sequence[LoggerTypeDef],
    },
    total=False,
)

_RequiredCreateSubscriptionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubscriptionDefinitionVersionRequestRequestTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)
_OptionalCreateSubscriptionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubscriptionDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Subscriptions": Sequence[SubscriptionTypeDef],
    },
    total=False,
)


class CreateSubscriptionDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateSubscriptionDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateSubscriptionDefinitionVersionRequestRequestTypeDef,
):
    pass


SubscriptionDefinitionVersionTypeDef = TypedDict(
    "SubscriptionDefinitionVersionTypeDef",
    {
        "Subscriptions": Sequence[SubscriptionTypeDef],
    },
    total=False,
)

ListConnectorDefinitionsResponseTypeDef = TypedDict(
    "ListConnectorDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCoreDefinitionsResponseTypeDef = TypedDict(
    "ListCoreDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeviceDefinitionsResponseTypeDef = TypedDict(
    "ListDeviceDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFunctionDefinitionsResponseTypeDef = TypedDict(
    "ListFunctionDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLoggerDefinitionsResponseTypeDef = TypedDict(
    "ListLoggerDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceDefinitionsResponseTypeDef = TypedDict(
    "ListResourceDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscriptionDefinitionsResponseTypeDef = TypedDict(
    "ListSubscriptionDefinitionsResponseTypeDef",
    {
        "Definitions": List[DefinitionInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentsResponseTypeDef = TypedDict(
    "ListDeploymentsResponseTypeDef",
    {
        "Deployments": List[DeploymentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FunctionDefaultExecutionConfigTypeDef = TypedDict(
    "FunctionDefaultExecutionConfigTypeDef",
    {
        "IsolationMode": FunctionIsolationModeType,
        "RunAs": FunctionRunAsConfigTypeDef,
    },
    total=False,
)

FunctionExecutionConfigTypeDef = TypedDict(
    "FunctionExecutionConfigTypeDef",
    {
        "IsolationMode": FunctionIsolationModeType,
        "RunAs": FunctionRunAsConfigTypeDef,
    },
    total=False,
)

ListGroupCertificateAuthoritiesResponseTypeDef = TypedDict(
    "ListGroupCertificateAuthoritiesResponseTypeDef",
    {
        "GroupCertificateAuthorities": List[GroupCertificateAuthorityPropertiesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "Groups": List[GroupInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LocalDeviceResourceDataTypeDef = TypedDict(
    "LocalDeviceResourceDataTypeDef",
    {
        "GroupOwnerSetting": GroupOwnerSettingTypeDef,
        "SourcePath": str,
    },
    total=False,
)

LocalVolumeResourceDataTypeDef = TypedDict(
    "LocalVolumeResourceDataTypeDef",
    {
        "DestinationPath": str,
        "GroupOwnerSetting": GroupOwnerSettingTypeDef,
        "SourcePath": str,
    },
    total=False,
)

_RequiredListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef = TypedDict(
    "_RequiredListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef",
    {
        "BulkDeploymentId": str,
    },
)
_OptionalListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef = TypedDict(
    "_OptionalListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef(
    _RequiredListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef,
    _OptionalListBulkDeploymentDetailedReportsRequestListBulkDeploymentDetailedReportsPaginateTypeDef,
):
    pass


ListBulkDeploymentsRequestListBulkDeploymentsPaginateTypeDef = TypedDict(
    "ListBulkDeploymentsRequestListBulkDeploymentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef",
    {
        "ConnectorDefinitionId": str,
    },
)
_OptionalListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef(
    _RequiredListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef,
    _OptionalListConnectorDefinitionVersionsRequestListConnectorDefinitionVersionsPaginateTypeDef,
):
    pass


ListConnectorDefinitionsRequestListConnectorDefinitionsPaginateTypeDef = TypedDict(
    "ListConnectorDefinitionsRequestListConnectorDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef",
    {
        "CoreDefinitionId": str,
    },
)
_OptionalListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef(
    _RequiredListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef,
    _OptionalListCoreDefinitionVersionsRequestListCoreDefinitionVersionsPaginateTypeDef,
):
    pass


ListCoreDefinitionsRequestListCoreDefinitionsPaginateTypeDef = TypedDict(
    "ListCoreDefinitionsRequestListCoreDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "_RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "_OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDeploymentsRequestListDeploymentsPaginateTypeDef(
    _RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef,
    _OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef,
):
    pass


_RequiredListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef",
    {
        "DeviceDefinitionId": str,
    },
)
_OptionalListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef(
    _RequiredListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef,
    _OptionalListDeviceDefinitionVersionsRequestListDeviceDefinitionVersionsPaginateTypeDef,
):
    pass


ListDeviceDefinitionsRequestListDeviceDefinitionsPaginateTypeDef = TypedDict(
    "ListDeviceDefinitionsRequestListDeviceDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)
_OptionalListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef(
    _RequiredListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef,
    _OptionalListFunctionDefinitionVersionsRequestListFunctionDefinitionVersionsPaginateTypeDef,
):
    pass


ListFunctionDefinitionsRequestListFunctionDefinitionsPaginateTypeDef = TypedDict(
    "ListFunctionDefinitionsRequestListFunctionDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListGroupVersionsRequestListGroupVersionsPaginateTypeDef = TypedDict(
    "_RequiredListGroupVersionsRequestListGroupVersionsPaginateTypeDef",
    {
        "GroupId": str,
    },
)
_OptionalListGroupVersionsRequestListGroupVersionsPaginateTypeDef = TypedDict(
    "_OptionalListGroupVersionsRequestListGroupVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGroupVersionsRequestListGroupVersionsPaginateTypeDef(
    _RequiredListGroupVersionsRequestListGroupVersionsPaginateTypeDef,
    _OptionalListGroupVersionsRequestListGroupVersionsPaginateTypeDef,
):
    pass


ListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "ListGroupsRequestListGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef",
    {
        "LoggerDefinitionId": str,
    },
)
_OptionalListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef(
    _RequiredListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef,
    _OptionalListLoggerDefinitionVersionsRequestListLoggerDefinitionVersionsPaginateTypeDef,
):
    pass


ListLoggerDefinitionsRequestListLoggerDefinitionsPaginateTypeDef = TypedDict(
    "ListLoggerDefinitionsRequestListLoggerDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)
_OptionalListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef(
    _RequiredListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef,
    _OptionalListResourceDefinitionVersionsRequestListResourceDefinitionVersionsPaginateTypeDef,
):
    pass


ListResourceDefinitionsRequestListResourceDefinitionsPaginateTypeDef = TypedDict(
    "ListResourceDefinitionsRequestListResourceDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef = TypedDict(
    "_RequiredListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef",
    {
        "SubscriptionDefinitionId": str,
    },
)
_OptionalListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef = TypedDict(
    "_OptionalListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef(
    _RequiredListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef,
    _OptionalListSubscriptionDefinitionVersionsRequestListSubscriptionDefinitionVersionsPaginateTypeDef,
):
    pass


ListSubscriptionDefinitionsRequestListSubscriptionDefinitionsPaginateTypeDef = TypedDict(
    "ListSubscriptionDefinitionsRequestListSubscriptionDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListConnectorDefinitionVersionsResponseTypeDef = TypedDict(
    "ListConnectorDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCoreDefinitionVersionsResponseTypeDef = TypedDict(
    "ListCoreDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeviceDefinitionVersionsResponseTypeDef = TypedDict(
    "ListDeviceDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFunctionDefinitionVersionsResponseTypeDef = TypedDict(
    "ListFunctionDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupVersionsResponseTypeDef = TypedDict(
    "ListGroupVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLoggerDefinitionVersionsResponseTypeDef = TypedDict(
    "ListLoggerDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceDefinitionVersionsResponseTypeDef = TypedDict(
    "ListResourceDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscriptionDefinitionVersionsResponseTypeDef = TypedDict(
    "ListSubscriptionDefinitionVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3MachineLearningModelResourceDataTypeDef = TypedDict(
    "S3MachineLearningModelResourceDataTypeDef",
    {
        "DestinationPath": str,
        "OwnerSetting": ResourceDownloadOwnerSettingTypeDef,
        "S3Uri": str,
    },
    total=False,
)

SageMakerMachineLearningModelResourceDataTypeDef = TypedDict(
    "SageMakerMachineLearningModelResourceDataTypeDef",
    {
        "DestinationPath": str,
        "OwnerSetting": ResourceDownloadOwnerSettingTypeDef,
        "SageMakerJobArn": str,
    },
    total=False,
)

RuntimeConfigurationTypeDef = TypedDict(
    "RuntimeConfigurationTypeDef",
    {
        "TelemetryConfiguration": TelemetryConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateThingRuntimeConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThingRuntimeConfigurationRequestRequestTypeDef",
    {
        "ThingName": str,
    },
)
_OptionalUpdateThingRuntimeConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThingRuntimeConfigurationRequestRequestTypeDef",
    {
        "TelemetryConfiguration": TelemetryConfigurationUpdateTypeDef,
    },
    total=False,
)


class UpdateThingRuntimeConfigurationRequestRequestTypeDef(
    _RequiredUpdateThingRuntimeConfigurationRequestRequestTypeDef,
    _OptionalUpdateThingRuntimeConfigurationRequestRequestTypeDef,
):
    pass


ListBulkDeploymentDetailedReportsResponseTypeDef = TypedDict(
    "ListBulkDeploymentDetailedReportsResponseTypeDef",
    {
        "Deployments": List[BulkDeploymentResultTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConnectorDefinitionRequestRequestTypeDef = TypedDict(
    "CreateConnectorDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": ConnectorDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetConnectorDefinitionVersionResponseTypeDef = TypedDict(
    "GetConnectorDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": ConnectorDefinitionVersionTypeDef,
        "Id": str,
        "NextToken": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCoreDefinitionRequestRequestTypeDef = TypedDict(
    "CreateCoreDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": CoreDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetCoreDefinitionVersionResponseTypeDef = TypedDict(
    "GetCoreDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": CoreDefinitionVersionTypeDef,
        "Id": str,
        "NextToken": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeviceDefinitionRequestRequestTypeDef = TypedDict(
    "CreateDeviceDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": DeviceDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetDeviceDefinitionVersionResponseTypeDef = TypedDict(
    "GetDeviceDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": DeviceDefinitionVersionTypeDef,
        "Id": str,
        "NextToken": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLoggerDefinitionRequestRequestTypeDef = TypedDict(
    "CreateLoggerDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": LoggerDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetLoggerDefinitionVersionResponseTypeDef = TypedDict(
    "GetLoggerDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": LoggerDefinitionVersionTypeDef,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriptionDefinitionRequestRequestTypeDef = TypedDict(
    "CreateSubscriptionDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": SubscriptionDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetSubscriptionDefinitionVersionResponseTypeDef = TypedDict(
    "GetSubscriptionDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": SubscriptionDefinitionVersionTypeDef,
        "Id": str,
        "NextToken": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FunctionDefaultConfigTypeDef = TypedDict(
    "FunctionDefaultConfigTypeDef",
    {
        "Execution": FunctionDefaultExecutionConfigTypeDef,
    },
    total=False,
)

FunctionConfigurationEnvironmentTypeDef = TypedDict(
    "FunctionConfigurationEnvironmentTypeDef",
    {
        "AccessSysfs": bool,
        "Execution": FunctionExecutionConfigTypeDef,
        "ResourceAccessPolicies": Sequence[ResourceAccessPolicyTypeDef],
        "Variables": Mapping[str, str],
    },
    total=False,
)

ResourceDataContainerTypeDef = TypedDict(
    "ResourceDataContainerTypeDef",
    {
        "LocalDeviceResourceData": LocalDeviceResourceDataTypeDef,
        "LocalVolumeResourceData": LocalVolumeResourceDataTypeDef,
        "S3MachineLearningModelResourceData": S3MachineLearningModelResourceDataTypeDef,
        "SageMakerMachineLearningModelResourceData": SageMakerMachineLearningModelResourceDataTypeDef,
        "SecretsManagerSecretResourceData": SecretsManagerSecretResourceDataTypeDef,
    },
    total=False,
)

GetThingRuntimeConfigurationResponseTypeDef = TypedDict(
    "GetThingRuntimeConfigurationResponseTypeDef",
    {
        "RuntimeConfiguration": RuntimeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FunctionConfigurationTypeDef = TypedDict(
    "FunctionConfigurationTypeDef",
    {
        "EncodingType": EncodingTypeType,
        "Environment": FunctionConfigurationEnvironmentTypeDef,
        "ExecArgs": str,
        "Executable": str,
        "MemorySize": int,
        "Pinned": bool,
        "Timeout": int,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Id": str,
        "Name": str,
        "ResourceDataContainer": ResourceDataContainerTypeDef,
    },
)

_RequiredFunctionTypeDef = TypedDict(
    "_RequiredFunctionTypeDef",
    {
        "Id": str,
    },
)
_OptionalFunctionTypeDef = TypedDict(
    "_OptionalFunctionTypeDef",
    {
        "FunctionArn": str,
        "FunctionConfiguration": FunctionConfigurationTypeDef,
    },
    total=False,
)


class FunctionTypeDef(_RequiredFunctionTypeDef, _OptionalFunctionTypeDef):
    pass


_RequiredCreateResourceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResourceDefinitionVersionRequestRequestTypeDef",
    {
        "ResourceDefinitionId": str,
    },
)
_OptionalCreateResourceDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResourceDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "Resources": Sequence[ResourceTypeDef],
    },
    total=False,
)


class CreateResourceDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateResourceDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateResourceDefinitionVersionRequestRequestTypeDef,
):
    pass


ResourceDefinitionVersionTypeDef = TypedDict(
    "ResourceDefinitionVersionTypeDef",
    {
        "Resources": Sequence[ResourceTypeDef],
    },
    total=False,
)

_RequiredCreateFunctionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFunctionDefinitionVersionRequestRequestTypeDef",
    {
        "FunctionDefinitionId": str,
    },
)
_OptionalCreateFunctionDefinitionVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFunctionDefinitionVersionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "DefaultConfig": FunctionDefaultConfigTypeDef,
        "Functions": Sequence[FunctionTypeDef],
    },
    total=False,
)


class CreateFunctionDefinitionVersionRequestRequestTypeDef(
    _RequiredCreateFunctionDefinitionVersionRequestRequestTypeDef,
    _OptionalCreateFunctionDefinitionVersionRequestRequestTypeDef,
):
    pass


FunctionDefinitionVersionTypeDef = TypedDict(
    "FunctionDefinitionVersionTypeDef",
    {
        "DefaultConfig": FunctionDefaultConfigTypeDef,
        "Functions": Sequence[FunctionTypeDef],
    },
    total=False,
)

CreateResourceDefinitionRequestRequestTypeDef = TypedDict(
    "CreateResourceDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": ResourceDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetResourceDefinitionVersionResponseTypeDef = TypedDict(
    "GetResourceDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": ResourceDefinitionVersionTypeDef,
        "Id": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFunctionDefinitionRequestRequestTypeDef = TypedDict(
    "CreateFunctionDefinitionRequestRequestTypeDef",
    {
        "AmznClientToken": str,
        "InitialVersion": FunctionDefinitionVersionTypeDef,
        "Name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

GetFunctionDefinitionVersionResponseTypeDef = TypedDict(
    "GetFunctionDefinitionVersionResponseTypeDef",
    {
        "Arn": str,
        "CreationTimestamp": str,
        "Definition": FunctionDefinitionVersionTypeDef,
        "Id": str,
        "NextToken": str,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
