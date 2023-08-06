"""
Type annotations for proton service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/type_defs/)

Usage::

    ```python
    from mypy_boto3_proton.type_defs import AcceptEnvironmentAccountConnectionInputRequestTypeDef

    data: AcceptEnvironmentAccountConnectionInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ComponentDeploymentUpdateTypeType,
    DeploymentStatusType,
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    ProvisionedResourceEngineType,
    RepositoryProviderType,
    RepositorySyncStatusType,
    ResourceDeploymentStatusType,
    ResourceSyncStatusType,
    ServiceStatusType,
    TemplateTypeType,
    TemplateVersionStatusType,
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
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    "EnvironmentAccountConnectionTypeDef",
    "ResponseMetadataTypeDef",
    "RepositoryBranchTypeDef",
    "CancelComponentDeploymentInputRequestTypeDef",
    "ComponentTypeDef",
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    "ServiceInstanceTypeDef",
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    "ServicePipelineTypeDef",
    "CompatibleEnvironmentTemplateInputTypeDef",
    "CompatibleEnvironmentTemplateTypeDef",
    "ComponentSummaryTypeDef",
    "TagTypeDef",
    "RepositoryBranchInputTypeDef",
    "EnvironmentTemplateTypeDef",
    "EnvironmentTemplateVersionTypeDef",
    "RepositoryTypeDef",
    "ServiceTemplateTypeDef",
    "CreateTemplateSyncConfigInputRequestTypeDef",
    "TemplateSyncConfigTypeDef",
    "DeleteComponentInputRequestTypeDef",
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DeleteServiceInputRequestTypeDef",
    "DeleteServiceTemplateInputRequestTypeDef",
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    "EnvironmentAccountConnectionSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTemplateFilterTypeDef",
    "EnvironmentTemplateSummaryTypeDef",
    "EnvironmentTemplateVersionSummaryTypeDef",
    "WaiterConfigTypeDef",
    "GetComponentInputRequestTypeDef",
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentTemplateInputRequestTypeDef",
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositorySyncStatusInputRequestTypeDef",
    "GetServiceInputRequestTypeDef",
    "GetServiceInstanceInputRequestTypeDef",
    "GetServiceTemplateInputRequestTypeDef",
    "GetServiceTemplateVersionInputRequestTypeDef",
    "GetTemplateSyncConfigInputRequestTypeDef",
    "GetTemplateSyncStatusInputRequestTypeDef",
    "RevisionTypeDef",
    "PaginatorConfigTypeDef",
    "ListComponentOutputsInputRequestTypeDef",
    "OutputTypeDef",
    "ListComponentProvisionedResourcesInputRequestTypeDef",
    "ProvisionedResourceTypeDef",
    "ListComponentsInputRequestTypeDef",
    "ListEnvironmentAccountConnectionsInputRequestTypeDef",
    "ListEnvironmentOutputsInputRequestTypeDef",
    "ListEnvironmentProvisionedResourcesInputRequestTypeDef",
    "ListEnvironmentTemplateVersionsInputRequestTypeDef",
    "ListEnvironmentTemplatesInputRequestTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "RepositorySummaryTypeDef",
    "ListRepositorySyncDefinitionsInputRequestTypeDef",
    "RepositorySyncDefinitionTypeDef",
    "ListServiceInstanceOutputsInputRequestTypeDef",
    "ListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    "ListServiceInstancesInputRequestTypeDef",
    "ServiceInstanceSummaryTypeDef",
    "ListServicePipelineOutputsInputRequestTypeDef",
    "ListServicePipelineProvisionedResourcesInputRequestTypeDef",
    "ListServiceTemplateVersionsInputRequestTypeDef",
    "ServiceTemplateVersionSummaryTypeDef",
    "ListServiceTemplatesInputRequestTypeDef",
    "ServiceTemplateSummaryTypeDef",
    "ListServicesInputRequestTypeDef",
    "ServiceSummaryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    "RepositorySyncEventTypeDef",
    "ResourceSyncEventTypeDef",
    "S3ObjectSourceTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateComponentInputRequestTypeDef",
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    "UpdateEnvironmentTemplateInputRequestTypeDef",
    "UpdateEnvironmentTemplateVersionInputRequestTypeDef",
    "UpdateServiceInputRequestTypeDef",
    "UpdateServiceInstanceInputRequestTypeDef",
    "UpdateServicePipelineInputRequestTypeDef",
    "UpdateServiceTemplateInputRequestTypeDef",
    "UpdateTemplateSyncConfigInputRequestTypeDef",
    "AcceptEnvironmentAccountConnectionOutputTypeDef",
    "CreateEnvironmentAccountConnectionOutputTypeDef",
    "DeleteEnvironmentAccountConnectionOutputTypeDef",
    "GetEnvironmentAccountConnectionOutputTypeDef",
    "RejectEnvironmentAccountConnectionOutputTypeDef",
    "UpdateEnvironmentAccountConnectionOutputTypeDef",
    "AccountSettingsTypeDef",
    "EnvironmentTypeDef",
    "CancelComponentDeploymentOutputTypeDef",
    "CreateComponentOutputTypeDef",
    "DeleteComponentOutputTypeDef",
    "GetComponentOutputTypeDef",
    "UpdateComponentOutputTypeDef",
    "CancelServiceInstanceDeploymentOutputTypeDef",
    "GetServiceInstanceOutputTypeDef",
    "UpdateServiceInstanceOutputTypeDef",
    "CancelServicePipelineDeploymentOutputTypeDef",
    "ServiceTypeDef",
    "UpdateServicePipelineOutputTypeDef",
    "UpdateServiceTemplateVersionInputRequestTypeDef",
    "ServiceTemplateVersionTypeDef",
    "ListComponentsOutputTypeDef",
    "CreateComponentInputRequestTypeDef",
    "CreateEnvironmentAccountConnectionInputRequestTypeDef",
    "CreateEnvironmentTemplateInputRequestTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "CreateServiceInputRequestTypeDef",
    "CreateServiceTemplateInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentTemplateOutputTypeDef",
    "DeleteEnvironmentTemplateOutputTypeDef",
    "GetEnvironmentTemplateOutputTypeDef",
    "UpdateEnvironmentTemplateOutputTypeDef",
    "CreateEnvironmentTemplateVersionOutputTypeDef",
    "DeleteEnvironmentTemplateVersionOutputTypeDef",
    "GetEnvironmentTemplateVersionOutputTypeDef",
    "UpdateEnvironmentTemplateVersionOutputTypeDef",
    "CreateRepositoryOutputTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "GetRepositoryOutputTypeDef",
    "CreateServiceTemplateOutputTypeDef",
    "DeleteServiceTemplateOutputTypeDef",
    "GetServiceTemplateOutputTypeDef",
    "UpdateServiceTemplateOutputTypeDef",
    "CreateTemplateSyncConfigOutputTypeDef",
    "DeleteTemplateSyncConfigOutputTypeDef",
    "GetTemplateSyncConfigOutputTypeDef",
    "UpdateTemplateSyncConfigOutputTypeDef",
    "ListEnvironmentAccountConnectionsOutputTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentTemplatesOutputTypeDef",
    "ListEnvironmentTemplateVersionsOutputTypeDef",
    "GetComponentInputComponentDeletedWaitTypeDef",
    "GetComponentInputComponentDeployedWaitTypeDef",
    "GetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    "GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    "GetServiceInputServiceCreatedWaitTypeDef",
    "GetServiceInputServiceDeletedWaitTypeDef",
    "GetServiceInputServicePipelineDeployedWaitTypeDef",
    "GetServiceInputServiceUpdatedWaitTypeDef",
    "GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    "GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    "ListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    "ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    "ListComponentsInputListComponentsPaginateTypeDef",
    "ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    "ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    "ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    "ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    "ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    "ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    "ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    "ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    "ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    "ListServicesInputListServicesPaginateTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListComponentOutputsOutputTypeDef",
    "ListEnvironmentOutputsOutputTypeDef",
    "ListServiceInstanceOutputsOutputTypeDef",
    "ListServicePipelineOutputsOutputTypeDef",
    "NotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    "ListComponentProvisionedResourcesOutputTypeDef",
    "ListEnvironmentProvisionedResourcesOutputTypeDef",
    "ListServiceInstanceProvisionedResourcesOutputTypeDef",
    "ListServicePipelineProvisionedResourcesOutputTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListRepositorySyncDefinitionsOutputTypeDef",
    "ListServiceInstancesOutputTypeDef",
    "ListServiceTemplateVersionsOutputTypeDef",
    "ListServiceTemplatesOutputTypeDef",
    "ListServicesOutputTypeDef",
    "RepositorySyncAttemptTypeDef",
    "ResourceSyncAttemptTypeDef",
    "TemplateVersionSourceInputTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "CancelEnvironmentDeploymentOutputTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "DeleteEnvironmentOutputTypeDef",
    "GetEnvironmentOutputTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "CreateServiceOutputTypeDef",
    "DeleteServiceOutputTypeDef",
    "GetServiceOutputTypeDef",
    "UpdateServiceOutputTypeDef",
    "CreateServiceTemplateVersionOutputTypeDef",
    "DeleteServiceTemplateVersionOutputTypeDef",
    "GetServiceTemplateVersionOutputTypeDef",
    "UpdateServiceTemplateVersionOutputTypeDef",
    "GetRepositorySyncStatusOutputTypeDef",
    "GetTemplateSyncStatusOutputTypeDef",
    "CreateEnvironmentTemplateVersionInputRequestTypeDef",
    "CreateServiceTemplateVersionInputRequestTypeDef",
)

AcceptEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredEnvironmentAccountConnectionTypeDef = TypedDict(
    "_RequiredEnvironmentAccountConnectionTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)
_OptionalEnvironmentAccountConnectionTypeDef = TypedDict(
    "_OptionalEnvironmentAccountConnectionTypeDef",
    {
        "componentRoleArn": str,
    },
    total=False,
)

class EnvironmentAccountConnectionTypeDef(
    _RequiredEnvironmentAccountConnectionTypeDef, _OptionalEnvironmentAccountConnectionTypeDef
):
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

RepositoryBranchTypeDef = TypedDict(
    "RepositoryBranchTypeDef",
    {
        "arn": str,
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

CancelComponentDeploymentInputRequestTypeDef = TypedDict(
    "CancelComponentDeploymentInputRequestTypeDef",
    {
        "componentName": str,
    },
)

_RequiredComponentTypeDef = TypedDict(
    "_RequiredComponentTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalComponentTypeDef = TypedDict(
    "_OptionalComponentTypeDef",
    {
        "deploymentStatusMessage": str,
        "description": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
    },
    total=False,
)

class ComponentTypeDef(_RequiredComponentTypeDef, _OptionalComponentTypeDef):
    pass

CancelEnvironmentDeploymentInputRequestTypeDef = TypedDict(
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    {
        "environmentName": str,
    },
)

CancelServiceInstanceDeploymentInputRequestTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

_RequiredServiceInstanceTypeDef = TypedDict(
    "_RequiredServiceInstanceTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "serviceName": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServiceInstanceTypeDef = TypedDict(
    "_OptionalServiceInstanceTypeDef",
    {
        "deploymentStatusMessage": str,
        "spec": str,
    },
    total=False,
)

class ServiceInstanceTypeDef(_RequiredServiceInstanceTypeDef, _OptionalServiceInstanceTypeDef):
    pass

CancelServicePipelineDeploymentInputRequestTypeDef = TypedDict(
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    {
        "serviceName": str,
    },
)

_RequiredServicePipelineTypeDef = TypedDict(
    "_RequiredServicePipelineTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServicePipelineTypeDef = TypedDict(
    "_OptionalServicePipelineTypeDef",
    {
        "deploymentStatusMessage": str,
        "spec": str,
    },
    total=False,
)

class ServicePipelineTypeDef(_RequiredServicePipelineTypeDef, _OptionalServicePipelineTypeDef):
    pass

CompatibleEnvironmentTemplateInputTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateInputTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

CompatibleEnvironmentTemplateTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

_RequiredComponentSummaryTypeDef = TypedDict(
    "_RequiredComponentSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalComponentSummaryTypeDef = TypedDict(
    "_OptionalComponentSummaryTypeDef",
    {
        "deploymentStatusMessage": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "serviceInstanceName": str,
        "serviceName": str,
    },
    total=False,
)

class ComponentSummaryTypeDef(_RequiredComponentSummaryTypeDef, _OptionalComponentSummaryTypeDef):
    pass

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

RepositoryBranchInputTypeDef = TypedDict(
    "RepositoryBranchInputTypeDef",
    {
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

_RequiredEnvironmentTemplateTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalEnvironmentTemplateTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)

class EnvironmentTemplateTypeDef(
    _RequiredEnvironmentTemplateTypeDef, _OptionalEnvironmentTemplateTypeDef
):
    pass

_RequiredEnvironmentTemplateVersionTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateVersionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalEnvironmentTemplateVersionTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateVersionTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "statusMessage": str,
    },
    total=False,
)

class EnvironmentTemplateVersionTypeDef(
    _RequiredEnvironmentTemplateVersionTypeDef, _OptionalEnvironmentTemplateVersionTypeDef
):
    pass

_RequiredRepositoryTypeDef = TypedDict(
    "_RequiredRepositoryTypeDef",
    {
        "arn": str,
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)
_OptionalRepositoryTypeDef = TypedDict(
    "_OptionalRepositoryTypeDef",
    {
        "encryptionKey": str,
    },
    total=False,
)

class RepositoryTypeDef(_RequiredRepositoryTypeDef, _OptionalRepositoryTypeDef):
    pass

_RequiredServiceTemplateTypeDef = TypedDict(
    "_RequiredServiceTemplateTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalServiceTemplateTypeDef = TypedDict(
    "_OptionalServiceTemplateTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)

class ServiceTemplateTypeDef(_RequiredServiceTemplateTypeDef, _OptionalServiceTemplateTypeDef):
    pass

_RequiredCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)

class CreateTemplateSyncConfigInputRequestTypeDef(
    _RequiredCreateTemplateSyncConfigInputRequestTypeDef,
    _OptionalCreateTemplateSyncConfigInputRequestTypeDef,
):
    pass

_RequiredTemplateSyncConfigTypeDef = TypedDict(
    "_RequiredTemplateSyncConfigTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalTemplateSyncConfigTypeDef = TypedDict(
    "_OptionalTemplateSyncConfigTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)

class TemplateSyncConfigTypeDef(
    _RequiredTemplateSyncConfigTypeDef, _OptionalTemplateSyncConfigTypeDef
):
    pass

DeleteComponentInputRequestTypeDef = TypedDict(
    "DeleteComponentInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

DeleteEnvironmentInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteRepositoryInputRequestTypeDef = TypedDict(
    "DeleteRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

DeleteServiceInputRequestTypeDef = TypedDict(
    "DeleteServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceTemplateInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

_RequiredEnvironmentAccountConnectionSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentAccountConnectionSummaryTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)
_OptionalEnvironmentAccountConnectionSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentAccountConnectionSummaryTypeDef",
    {
        "componentRoleArn": str,
    },
    total=False,
)

class EnvironmentAccountConnectionSummaryTypeDef(
    _RequiredEnvironmentAccountConnectionSummaryTypeDef,
    _OptionalEnvironmentAccountConnectionSummaryTypeDef,
):
    pass

_RequiredEnvironmentSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalEnvironmentSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentSummaryTypeDef",
    {
        "componentRoleArn": str,
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
    },
    total=False,
)

class EnvironmentSummaryTypeDef(
    _RequiredEnvironmentSummaryTypeDef, _OptionalEnvironmentSummaryTypeDef
):
    pass

EnvironmentTemplateFilterTypeDef = TypedDict(
    "EnvironmentTemplateFilterTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

_RequiredEnvironmentTemplateSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalEnvironmentTemplateSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateSummaryTypeDef",
    {
        "description": str,
        "displayName": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)

class EnvironmentTemplateSummaryTypeDef(
    _RequiredEnvironmentTemplateSummaryTypeDef, _OptionalEnvironmentTemplateSummaryTypeDef
):
    pass

_RequiredEnvironmentTemplateVersionSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalEnvironmentTemplateVersionSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateVersionSummaryTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "statusMessage": str,
    },
    total=False,
)

class EnvironmentTemplateVersionSummaryTypeDef(
    _RequiredEnvironmentTemplateVersionSummaryTypeDef,
    _OptionalEnvironmentTemplateVersionSummaryTypeDef,
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

GetComponentInputRequestTypeDef = TypedDict(
    "GetComponentInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

GetEnvironmentInputRequestTypeDef = TypedDict(
    "GetEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

GetRepositoryInputRequestTypeDef = TypedDict(
    "GetRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

GetRepositorySyncStatusInputRequestTypeDef = TypedDict(
    "GetRepositorySyncStatusInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)

GetServiceInputRequestTypeDef = TypedDict(
    "GetServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

GetServiceInstanceInputRequestTypeDef = TypedDict(
    "GetServiceInstanceInputRequestTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)

GetServiceTemplateInputRequestTypeDef = TypedDict(
    "GetServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "GetServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

GetTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "GetTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

GetTemplateSyncStatusInputRequestTypeDef = TypedDict(
    "GetTemplateSyncStatusInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
        "templateVersion": str,
    },
)

RevisionTypeDef = TypedDict(
    "RevisionTypeDef",
    {
        "branch": str,
        "directory": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "sha": str,
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

_RequiredListComponentOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListComponentOutputsInputRequestTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListComponentOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListComponentOutputsInputRequestTypeDef(
    _RequiredListComponentOutputsInputRequestTypeDef,
    _OptionalListComponentOutputsInputRequestTypeDef,
):
    pass

OutputTypeDef = TypedDict(
    "OutputTypeDef",
    {
        "key": str,
        "valueString": str,
    },
    total=False,
)

_RequiredListComponentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListComponentProvisionedResourcesInputRequestTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListComponentProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListComponentProvisionedResourcesInputRequestTypeDef(
    _RequiredListComponentProvisionedResourcesInputRequestTypeDef,
    _OptionalListComponentProvisionedResourcesInputRequestTypeDef,
):
    pass

ProvisionedResourceTypeDef = TypedDict(
    "ProvisionedResourceTypeDef",
    {
        "identifier": str,
        "name": str,
        "provisioningEngine": ProvisionedResourceEngineType,
    },
    total=False,
)

ListComponentsInputRequestTypeDef = TypedDict(
    "ListComponentsInputRequestTypeDef",
    {
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "serviceInstanceName": str,
        "serviceName": str,
    },
    total=False,
)

_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
    },
    total=False,
)

class ListEnvironmentAccountConnectionsInputRequestTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputRequestTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentOutputsInputRequestTypeDef(
    _RequiredListEnvironmentOutputsInputRequestTypeDef,
    _OptionalListEnvironmentOutputsInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentProvisionedResourcesInputRequestTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef,
):
    pass

_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListEnvironmentTemplateVersionsInputRequestTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputRequestTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputRequestTypeDef,
):
    pass

ListEnvironmentTemplatesInputRequestTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListRepositoriesInputRequestTypeDef = TypedDict(
    "ListRepositoriesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

RepositorySummaryTypeDef = TypedDict(
    "RepositorySummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

_RequiredListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)
_OptionalListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListRepositorySyncDefinitionsInputRequestTypeDef(
    _RequiredListRepositorySyncDefinitionsInputRequestTypeDef,
    _OptionalListRepositorySyncDefinitionsInputRequestTypeDef,
):
    pass

RepositorySyncDefinitionTypeDef = TypedDict(
    "RepositorySyncDefinitionTypeDef",
    {
        "branch": str,
        "directory": str,
        "parent": str,
        "target": str,
    },
)

_RequiredListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServiceInstanceOutputsInputRequestTypeDef(
    _RequiredListServiceInstanceOutputsInputRequestTypeDef,
    _OptionalListServiceInstanceOutputsInputRequestTypeDef,
):
    pass

_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServiceInstanceProvisionedResourcesInputRequestTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef,
):
    pass

ListServiceInstancesInputRequestTypeDef = TypedDict(
    "ListServiceInstancesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "serviceName": str,
    },
    total=False,
)

_RequiredServiceInstanceSummaryTypeDef = TypedDict(
    "_RequiredServiceInstanceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "serviceName": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServiceInstanceSummaryTypeDef = TypedDict(
    "_OptionalServiceInstanceSummaryTypeDef",
    {
        "deploymentStatusMessage": str,
    },
    total=False,
)

class ServiceInstanceSummaryTypeDef(
    _RequiredServiceInstanceSummaryTypeDef, _OptionalServiceInstanceSummaryTypeDef
):
    pass

_RequiredListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServicePipelineOutputsInputRequestTypeDef(
    _RequiredListServicePipelineOutputsInputRequestTypeDef,
    _OptionalListServicePipelineOutputsInputRequestTypeDef,
):
    pass

_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class ListServicePipelineProvisionedResourcesInputRequestTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef,
):
    pass

_RequiredListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListServiceTemplateVersionsInputRequestTypeDef(
    _RequiredListServiceTemplateVersionsInputRequestTypeDef,
    _OptionalListServiceTemplateVersionsInputRequestTypeDef,
):
    pass

_RequiredServiceTemplateVersionSummaryTypeDef = TypedDict(
    "_RequiredServiceTemplateVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalServiceTemplateVersionSummaryTypeDef = TypedDict(
    "_OptionalServiceTemplateVersionSummaryTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "statusMessage": str,
    },
    total=False,
)

class ServiceTemplateVersionSummaryTypeDef(
    _RequiredServiceTemplateVersionSummaryTypeDef, _OptionalServiceTemplateVersionSummaryTypeDef
):
    pass

ListServiceTemplatesInputRequestTypeDef = TypedDict(
    "ListServiceTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredServiceTemplateSummaryTypeDef = TypedDict(
    "_RequiredServiceTemplateSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalServiceTemplateSummaryTypeDef = TypedDict(
    "_OptionalServiceTemplateSummaryTypeDef",
    {
        "description": str,
        "displayName": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)

class ServiceTemplateSummaryTypeDef(
    _RequiredServiceTemplateSummaryTypeDef, _OptionalServiceTemplateSummaryTypeDef
):
    pass

ListServicesInputRequestTypeDef = TypedDict(
    "ListServicesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredServiceSummaryTypeDef = TypedDict(
    "_RequiredServiceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
        "templateName": str,
    },
)
_OptionalServiceSummaryTypeDef = TypedDict(
    "_OptionalServiceSummaryTypeDef",
    {
        "description": str,
        "statusMessage": str,
    },
    total=False,
)

class ServiceSummaryTypeDef(_RequiredServiceSummaryTypeDef, _OptionalServiceSummaryTypeDef):
    pass

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass

RejectEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredRepositorySyncEventTypeDef = TypedDict(
    "_RequiredRepositorySyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
    },
)
_OptionalRepositorySyncEventTypeDef = TypedDict(
    "_OptionalRepositorySyncEventTypeDef",
    {
        "externalId": str,
    },
    total=False,
)

class RepositorySyncEventTypeDef(
    _RequiredRepositorySyncEventTypeDef, _OptionalRepositorySyncEventTypeDef
):
    pass

_RequiredResourceSyncEventTypeDef = TypedDict(
    "_RequiredResourceSyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
    },
)
_OptionalResourceSyncEventTypeDef = TypedDict(
    "_OptionalResourceSyncEventTypeDef",
    {
        "externalId": str,
    },
    total=False,
)

class ResourceSyncEventTypeDef(
    _RequiredResourceSyncEventTypeDef, _OptionalResourceSyncEventTypeDef
):
    pass

S3ObjectSourceTypeDef = TypedDict(
    "S3ObjectSourceTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateComponentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentInputRequestTypeDef",
    {
        "deploymentType": ComponentDeploymentUpdateTypeType,
        "name": str,
    },
)
_OptionalUpdateComponentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentInputRequestTypeDef",
    {
        "description": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
        "templateFile": str,
    },
    total=False,
)

class UpdateComponentInputRequestTypeDef(
    _RequiredUpdateComponentInputRequestTypeDef, _OptionalUpdateComponentInputRequestTypeDef
):
    pass

_RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "componentRoleArn": str,
        "roleArn": str,
    },
    total=False,
)

class UpdateEnvironmentAccountConnectionInputRequestTypeDef(
    _RequiredUpdateEnvironmentAccountConnectionInputRequestTypeDef,
    _OptionalUpdateEnvironmentAccountConnectionInputRequestTypeDef,
):
    pass

_RequiredUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)

class UpdateEnvironmentTemplateInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateInputRequestTypeDef,
):
    pass

_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "description": str,
        "status": TemplateVersionStatusType,
    },
    total=False,
)

class UpdateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass

_RequiredUpdateServiceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInputRequestTypeDef",
    {
        "description": str,
        "spec": str,
    },
    total=False,
)

class UpdateServiceInputRequestTypeDef(
    _RequiredUpdateServiceInputRequestTypeDef, _OptionalUpdateServiceInputRequestTypeDef
):
    pass

_RequiredUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInstanceInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
        "serviceName": str,
    },
)
_OptionalUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInstanceInputRequestTypeDef",
    {
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateServiceInstanceInputRequestTypeDef(
    _RequiredUpdateServiceInstanceInputRequestTypeDef,
    _OptionalUpdateServiceInstanceInputRequestTypeDef,
):
    pass

_RequiredUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServicePipelineInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "serviceName": str,
        "spec": str,
    },
)
_OptionalUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServicePipelineInputRequestTypeDef",
    {
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateServicePipelineInputRequestTypeDef(
    _RequiredUpdateServicePipelineInputRequestTypeDef,
    _OptionalUpdateServicePipelineInputRequestTypeDef,
):
    pass

_RequiredUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)

class UpdateServiceTemplateInputRequestTypeDef(
    _RequiredUpdateServiceTemplateInputRequestTypeDef,
    _OptionalUpdateServiceTemplateInputRequestTypeDef,
):
    pass

_RequiredUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)

class UpdateTemplateSyncConfigInputRequestTypeDef(
    _RequiredUpdateTemplateSyncConfigInputRequestTypeDef,
    _OptionalUpdateTemplateSyncConfigInputRequestTypeDef,
):
    pass

AcceptEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "CreateEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RejectEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "UpdateEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": EnvironmentAccountConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "pipelineProvisioningRepository": RepositoryBranchTypeDef,
        "pipelineServiceRoleArn": str,
    },
    total=False,
)

_RequiredEnvironmentTypeDef = TypedDict(
    "_RequiredEnvironmentTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalEnvironmentTypeDef = TypedDict(
    "_OptionalEnvironmentTypeDef",
    {
        "componentRoleArn": str,
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "provisioningRepository": RepositoryBranchTypeDef,
        "spec": str,
    },
    total=False,
)

class EnvironmentTypeDef(_RequiredEnvironmentTypeDef, _OptionalEnvironmentTypeDef):
    pass

CancelComponentDeploymentOutputTypeDef = TypedDict(
    "CancelComponentDeploymentOutputTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateComponentOutputTypeDef = TypedDict(
    "CreateComponentOutputTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteComponentOutputTypeDef = TypedDict(
    "DeleteComponentOutputTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComponentOutputTypeDef = TypedDict(
    "GetComponentOutputTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateComponentOutputTypeDef = TypedDict(
    "UpdateComponentOutputTypeDef",
    {
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelServiceInstanceDeploymentOutputTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceInstanceOutputTypeDef = TypedDict(
    "GetServiceInstanceOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceInstanceOutputTypeDef = TypedDict(
    "UpdateServiceInstanceOutputTypeDef",
    {
        "serviceInstance": ServiceInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelServicePipelineDeploymentOutputTypeDef = TypedDict(
    "CancelServicePipelineDeploymentOutputTypeDef",
    {
        "pipeline": ServicePipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredServiceTypeDef = TypedDict(
    "_RequiredServiceTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
        "spec": str,
        "status": ServiceStatusType,
        "templateName": str,
    },
)
_OptionalServiceTypeDef = TypedDict(
    "_OptionalServiceTypeDef",
    {
        "branchName": str,
        "description": str,
        "pipeline": ServicePipelineTypeDef,
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "statusMessage": str,
    },
    total=False,
)

class ServiceTypeDef(_RequiredServiceTypeDef, _OptionalServiceTypeDef):
    pass

UpdateServicePipelineOutputTypeDef = TypedDict(
    "UpdateServicePipelineOutputTypeDef",
    {
        "pipeline": ServicePipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence[CompatibleEnvironmentTemplateInputTypeDef],
        "description": str,
        "status": TemplateVersionStatusType,
        "supportedComponentSources": Sequence[Literal["DIRECTLY_DEFINED"]],
    },
    total=False,
)

class UpdateServiceTemplateVersionInputRequestTypeDef(
    _RequiredUpdateServiceTemplateVersionInputRequestTypeDef,
    _OptionalUpdateServiceTemplateVersionInputRequestTypeDef,
):
    pass

_RequiredServiceTemplateVersionTypeDef = TypedDict(
    "_RequiredServiceTemplateVersionTypeDef",
    {
        "arn": str,
        "compatibleEnvironmentTemplates": List[CompatibleEnvironmentTemplateTypeDef],
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalServiceTemplateVersionTypeDef = TypedDict(
    "_OptionalServiceTemplateVersionTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "statusMessage": str,
        "supportedComponentSources": List[Literal["DIRECTLY_DEFINED"]],
    },
    total=False,
)

class ServiceTemplateVersionTypeDef(
    _RequiredServiceTemplateVersionTypeDef, _OptionalServiceTemplateVersionTypeDef
):
    pass

ListComponentsOutputTypeDef = TypedDict(
    "ListComponentsOutputTypeDef",
    {
        "components": List[ComponentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateComponentInputRequestTypeDef = TypedDict(
    "_RequiredCreateComponentInputRequestTypeDef",
    {
        "manifest": str,
        "name": str,
        "templateFile": str,
    },
)
_OptionalCreateComponentInputRequestTypeDef = TypedDict(
    "_OptionalCreateComponentInputRequestTypeDef",
    {
        "description": str,
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "serviceSpec": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateComponentInputRequestTypeDef(
    _RequiredCreateComponentInputRequestTypeDef, _OptionalCreateComponentInputRequestTypeDef
):
    pass

_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "environmentName": str,
        "managementAccountId": str,
        "roleArn": str,
    },
)
_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "clientToken": str,
        "componentRoleArn": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentAccountConnectionInputRequestTypeDef(
    _RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef,
    _OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef,
):
    pass

_RequiredCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentTemplateInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateInputRequestTypeDef,
):
    pass

_RequiredCreateRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryInputRequestTypeDef",
    {
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)
_OptionalCreateRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryInputRequestTypeDef",
    {
        "encryptionKey": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateRepositoryInputRequestTypeDef(
    _RequiredCreateRepositoryInputRequestTypeDef, _OptionalCreateRepositoryInputRequestTypeDef
):
    pass

_RequiredCreateServiceInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateServiceInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceInputRequestTypeDef",
    {
        "branchName": str,
        "description": str,
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "tags": Sequence[TagTypeDef],
        "templateMinorVersion": str,
    },
    total=False,
)

class CreateServiceInputRequestTypeDef(
    _RequiredCreateServiceInputRequestTypeDef, _OptionalCreateServiceInputRequestTypeDef
):
    pass

_RequiredCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateServiceTemplateInputRequestTypeDef(
    _RequiredCreateServiceTemplateInputRequestTypeDef,
    _OptionalCreateServiceTemplateInputRequestTypeDef,
):
    pass

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "nextToken": str,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentInputRequestTypeDef",
    {
        "componentRoleArn": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": RepositoryBranchInputTypeDef,
        "tags": Sequence[TagTypeDef],
        "templateMinorVersion": str,
    },
    total=False,
)

class CreateEnvironmentInputRequestTypeDef(
    _RequiredCreateEnvironmentInputRequestTypeDef, _OptionalCreateEnvironmentInputRequestTypeDef
):
    pass

UpdateAccountSettingsInputRequestTypeDef = TypedDict(
    "UpdateAccountSettingsInputRequestTypeDef",
    {
        "pipelineProvisioningRepository": RepositoryBranchInputTypeDef,
        "pipelineServiceRoleArn": str,
    },
    total=False,
)

_RequiredUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
    },
)
_OptionalUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentInputRequestTypeDef",
    {
        "componentRoleArn": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": RepositoryBranchInputTypeDef,
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)

class UpdateEnvironmentInputRequestTypeDef(
    _RequiredUpdateEnvironmentInputRequestTypeDef, _OptionalUpdateEnvironmentInputRequestTypeDef
):
    pass

CreateEnvironmentTemplateOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEnvironmentTemplateOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnvironmentTemplateOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentTemplateOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": EnvironmentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": EnvironmentTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRepositoryOutputTypeDef = TypedDict(
    "CreateRepositoryOutputTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryOutputTypeDef = TypedDict(
    "DeleteRepositoryOutputTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositoryOutputTypeDef = TypedDict(
    "GetRepositoryOutputTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceTemplateOutputTypeDef = TypedDict(
    "CreateServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceTemplateOutputTypeDef = TypedDict(
    "DeleteServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceTemplateOutputTypeDef = TypedDict(
    "GetServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceTemplateOutputTypeDef = TypedDict(
    "UpdateServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": ServiceTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateSyncConfigOutputTypeDef = TypedDict(
    "CreateTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateSyncConfigOutputTypeDef = TypedDict(
    "DeleteTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTemplateSyncConfigOutputTypeDef = TypedDict(
    "GetTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateSyncConfigOutputTypeDef = TypedDict(
    "UpdateTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": TemplateSyncConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentAccountConnectionsOutputTypeDef = TypedDict(
    "ListEnvironmentAccountConnectionsOutputTypeDef",
    {
        "environmentAccountConnections": List[EnvironmentAccountConnectionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsOutputTypeDef = TypedDict(
    "ListEnvironmentsOutputTypeDef",
    {
        "environments": List[EnvironmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsInputRequestTypeDef = TypedDict(
    "ListEnvironmentsInputRequestTypeDef",
    {
        "environmentTemplates": Sequence[EnvironmentTemplateFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListEnvironmentTemplatesOutputTypeDef = TypedDict(
    "ListEnvironmentTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "templates": List[EnvironmentTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentTemplateVersionsOutputTypeDef = TypedDict(
    "ListEnvironmentTemplateVersionsOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List[EnvironmentTemplateVersionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetComponentInputComponentDeletedWaitTypeDef = TypedDict(
    "_RequiredGetComponentInputComponentDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetComponentInputComponentDeletedWaitTypeDef = TypedDict(
    "_OptionalGetComponentInputComponentDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetComponentInputComponentDeletedWaitTypeDef(
    _RequiredGetComponentInputComponentDeletedWaitTypeDef,
    _OptionalGetComponentInputComponentDeletedWaitTypeDef,
):
    pass

_RequiredGetComponentInputComponentDeployedWaitTypeDef = TypedDict(
    "_RequiredGetComponentInputComponentDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetComponentInputComponentDeployedWaitTypeDef = TypedDict(
    "_OptionalGetComponentInputComponentDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetComponentInputComponentDeployedWaitTypeDef(
    _RequiredGetComponentInputComponentDeployedWaitTypeDef,
    _OptionalGetComponentInputComponentDeployedWaitTypeDef,
):
    pass

_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetEnvironmentInputEnvironmentDeployedWaitTypeDef(
    _RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
    _OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
):
    pass

_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceCreatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceCreatedWaitTypeDef(
    _RequiredGetServiceInputServiceCreatedWaitTypeDef,
    _OptionalGetServiceInputServiceCreatedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceDeletedWaitTypeDef(
    _RequiredGetServiceInputServiceDeletedWaitTypeDef,
    _OptionalGetServiceInputServiceDeletedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServicePipelineDeployedWaitTypeDef(
    _RequiredGetServiceInputServicePipelineDeployedWaitTypeDef,
    _OptionalGetServiceInputServicePipelineDeployedWaitTypeDef,
):
    pass

_RequiredGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInputServiceUpdatedWaitTypeDef(
    _RequiredGetServiceInputServiceUpdatedWaitTypeDef,
    _OptionalGetServiceInputServiceUpdatedWaitTypeDef,
):
    pass

_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)
_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef(
    _RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
    _OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
):
    pass

_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
):
    pass

_RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef = TypedDict(
    "_RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef = TypedDict(
    "_OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListComponentOutputsInputListComponentOutputsPaginateTypeDef(
    _RequiredListComponentOutputsInputListComponentOutputsPaginateTypeDef,
    _OptionalListComponentOutputsInputListComponentOutputsPaginateTypeDef,
):
    pass

_RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    {
        "componentName": str,
    },
)
_OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef(
    _RequiredListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef,
    _OptionalListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef,
):
    pass

ListComponentsInputListComponentsPaginateTypeDef = TypedDict(
    "ListComponentsInputListComponentsPaginateTypeDef",
    {
        "environmentName": str,
        "serviceInstanceName": str,
        "serviceName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "environmentName": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
):
    pass

_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef(
    _RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
    _OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
):
    pass

_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
):
    pass

ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEnvironmentsInputListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    {
        "environmentTemplates": Sequence[EnvironmentTemplateFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRepositoriesInputListRepositoriesPaginateTypeDef = TypedDict(
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)
_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef(
    _RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
    _OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
):
    pass

_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef(
    _RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
    _OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
):
    pass

_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
):
    pass

ListServiceInstancesInputListServiceInstancesPaginateTypeDef = TypedDict(
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    {
        "serviceName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef(
    _RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
    _OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
):
    pass

_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
):
    pass

_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef(
    _RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
    _OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
):
    pass

ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef = TypedDict(
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServicesInputListServicesPaginateTypeDef = TypedDict(
    "ListServicesInputListServicesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass

ListComponentOutputsOutputTypeDef = TypedDict(
    "ListComponentOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentOutputsOutputTypeDef = TypedDict(
    "ListEnvironmentOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceInstanceOutputsOutputTypeDef = TypedDict(
    "ListServiceInstanceOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicePipelineOutputsOutputTypeDef = TypedDict(
    "ListServicePipelineOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List[OutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "resourceArn": str,
        "status": ResourceDeploymentStatusType,
    },
)
_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "deploymentId": str,
        "outputs": Sequence[OutputTypeDef],
        "statusMessage": str,
    },
    total=False,
)

class NotifyResourceDeploymentStatusChangeInputRequestTypeDef(
    _RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
    _OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
):
    pass

ListComponentProvisionedResourcesOutputTypeDef = TypedDict(
    "ListComponentProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentProvisionedResourcesOutputTypeDef = TypedDict(
    "ListEnvironmentProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceInstanceProvisionedResourcesOutputTypeDef = TypedDict(
    "ListServiceInstanceProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicePipelineProvisionedResourcesOutputTypeDef = TypedDict(
    "ListServicePipelineProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List[ProvisionedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRepositoriesOutputTypeDef = TypedDict(
    "ListRepositoriesOutputTypeDef",
    {
        "nextToken": str,
        "repositories": List[RepositorySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRepositorySyncDefinitionsOutputTypeDef = TypedDict(
    "ListRepositorySyncDefinitionsOutputTypeDef",
    {
        "nextToken": str,
        "syncDefinitions": List[RepositorySyncDefinitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceInstancesOutputTypeDef = TypedDict(
    "ListServiceInstancesOutputTypeDef",
    {
        "nextToken": str,
        "serviceInstances": List[ServiceInstanceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceTemplateVersionsOutputTypeDef = TypedDict(
    "ListServiceTemplateVersionsOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List[ServiceTemplateVersionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceTemplatesOutputTypeDef = TypedDict(
    "ListServiceTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "templates": List[ServiceTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicesOutputTypeDef = TypedDict(
    "ListServicesOutputTypeDef",
    {
        "nextToken": str,
        "services": List[ServiceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RepositorySyncAttemptTypeDef = TypedDict(
    "RepositorySyncAttemptTypeDef",
    {
        "events": List[RepositorySyncEventTypeDef],
        "startedAt": datetime,
        "status": RepositorySyncStatusType,
    },
)

ResourceSyncAttemptTypeDef = TypedDict(
    "ResourceSyncAttemptTypeDef",
    {
        "events": List[ResourceSyncEventTypeDef],
        "initialRevision": RevisionTypeDef,
        "startedAt": datetime,
        "status": ResourceSyncStatusType,
        "target": str,
        "targetRevision": RevisionTypeDef,
    },
)

TemplateVersionSourceInputTypeDef = TypedDict(
    "TemplateVersionSourceInputTypeDef",
    {
        "s3": S3ObjectSourceTypeDef,
    },
    total=False,
)

GetAccountSettingsOutputTypeDef = TypedDict(
    "GetAccountSettingsOutputTypeDef",
    {
        "accountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsOutputTypeDef = TypedDict(
    "UpdateAccountSettingsOutputTypeDef",
    {
        "accountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelEnvironmentDeploymentOutputTypeDef = TypedDict(
    "CancelEnvironmentDeploymentOutputTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEnvironmentOutputTypeDef = TypedDict(
    "DeleteEnvironmentOutputTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceOutputTypeDef = TypedDict(
    "CreateServiceOutputTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceOutputTypeDef = TypedDict(
    "DeleteServiceOutputTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceOutputTypeDef = TypedDict(
    "GetServiceOutputTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceOutputTypeDef = TypedDict(
    "UpdateServiceOutputTypeDef",
    {
        "service": ServiceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceTemplateVersionOutputTypeDef = TypedDict(
    "CreateServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceTemplateVersionOutputTypeDef = TypedDict(
    "DeleteServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceTemplateVersionOutputTypeDef = TypedDict(
    "GetServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceTemplateVersionOutputTypeDef = TypedDict(
    "UpdateServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": ServiceTemplateVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositorySyncStatusOutputTypeDef = TypedDict(
    "GetRepositorySyncStatusOutputTypeDef",
    {
        "latestSync": RepositorySyncAttemptTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTemplateSyncStatusOutputTypeDef = TypedDict(
    "GetTemplateSyncStatusOutputTypeDef",
    {
        "desiredState": RevisionTypeDef,
        "latestSuccessfulSync": ResourceSyncAttemptTypeDef,
        "latestSync": ResourceSyncAttemptTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "source": TemplateVersionSourceInputTypeDef,
        "templateName": str,
    },
)
_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass

_RequiredCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence[CompatibleEnvironmentTemplateInputTypeDef],
        "source": TemplateVersionSourceInputTypeDef,
        "templateName": str,
    },
)
_OptionalCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "supportedComponentSources": Sequence[Literal["DIRECTLY_DEFINED"]],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateServiceTemplateVersionInputRequestTypeDef(
    _RequiredCreateServiceTemplateVersionInputRequestTypeDef,
    _OptionalCreateServiceTemplateVersionInputRequestTypeDef,
):
    pass
