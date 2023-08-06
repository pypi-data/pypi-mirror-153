"""
Type annotations for serverlessrepo service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_serverlessrepo/type_defs/)

Usage::

    ```python
    from mypy_boto3_serverlessrepo.type_defs import ApplicationDependencySummaryTypeDef

    data: ApplicationDependencySummaryTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import CapabilityType, StatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApplicationDependencySummaryTypeDef",
    "ApplicationPolicyStatementTypeDef",
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateApplicationVersionRequestRequestTypeDef",
    "ParameterDefinitionTypeDef",
    "ParameterValueTypeDef",
    "TagTypeDef",
    "CreateCloudFormationTemplateRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "GetApplicationPolicyRequestRequestTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetCloudFormationTemplateRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationDependenciesRequestRequestTypeDef",
    "ListApplicationVersionsRequestRequestTypeDef",
    "VersionSummaryTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "RollbackTriggerTypeDef",
    "UnshareApplicationRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "PutApplicationPolicyRequestRequestTypeDef",
    "CreateCloudFormationChangeSetResponseTypeDef",
    "CreateCloudFormationTemplateResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApplicationPolicyResponseTypeDef",
    "GetCloudFormationTemplateResponseTypeDef",
    "ListApplicationDependenciesResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "PutApplicationPolicyResponseTypeDef",
    "CreateApplicationVersionResponseTypeDef",
    "VersionTypeDef",
    "ListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef",
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationVersionsResponseTypeDef",
    "RollbackConfigurationTypeDef",
    "CreateApplicationResponseTypeDef",
    "GetApplicationResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "CreateCloudFormationChangeSetRequestRequestTypeDef",
)

ApplicationDependencySummaryTypeDef = TypedDict(
    "ApplicationDependencySummaryTypeDef",
    {
        "ApplicationId": str,
        "SemanticVersion": str,
    },
)

_RequiredApplicationPolicyStatementTypeDef = TypedDict(
    "_RequiredApplicationPolicyStatementTypeDef",
    {
        "Actions": List[str],
        "Principals": List[str],
    },
)
_OptionalApplicationPolicyStatementTypeDef = TypedDict(
    "_OptionalApplicationPolicyStatementTypeDef",
    {
        "PrincipalOrgIDs": List[str],
        "StatementId": str,
    },
    total=False,
)


class ApplicationPolicyStatementTypeDef(
    _RequiredApplicationPolicyStatementTypeDef, _OptionalApplicationPolicyStatementTypeDef
):
    pass


_RequiredApplicationSummaryTypeDef = TypedDict(
    "_RequiredApplicationSummaryTypeDef",
    {
        "ApplicationId": str,
        "Author": str,
        "Description": str,
        "Name": str,
    },
)
_OptionalApplicationSummaryTypeDef = TypedDict(
    "_OptionalApplicationSummaryTypeDef",
    {
        "CreationTime": str,
        "HomePageUrl": str,
        "Labels": List[str],
        "SpdxLicenseId": str,
    },
    total=False,
)


class ApplicationSummaryTypeDef(
    _RequiredApplicationSummaryTypeDef, _OptionalApplicationSummaryTypeDef
):
    pass


_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "Author": str,
        "Description": str,
        "Name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "HomePageUrl": str,
        "Labels": Sequence[str],
        "LicenseBody": str,
        "LicenseUrl": str,
        "ReadmeBody": str,
        "ReadmeUrl": str,
        "SemanticVersion": str,
        "SourceCodeArchiveUrl": str,
        "SourceCodeUrl": str,
        "SpdxLicenseId": str,
        "TemplateBody": str,
        "TemplateUrl": str,
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
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

_RequiredCreateApplicationVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "SemanticVersion": str,
    },
)
_OptionalCreateApplicationVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationVersionRequestRequestTypeDef",
    {
        "SourceCodeArchiveUrl": str,
        "SourceCodeUrl": str,
        "TemplateBody": str,
        "TemplateUrl": str,
    },
    total=False,
)


class CreateApplicationVersionRequestRequestTypeDef(
    _RequiredCreateApplicationVersionRequestRequestTypeDef,
    _OptionalCreateApplicationVersionRequestRequestTypeDef,
):
    pass


_RequiredParameterDefinitionTypeDef = TypedDict(
    "_RequiredParameterDefinitionTypeDef",
    {
        "Name": str,
        "ReferencedByResources": List[str],
    },
)
_OptionalParameterDefinitionTypeDef = TypedDict(
    "_OptionalParameterDefinitionTypeDef",
    {
        "AllowedPattern": str,
        "AllowedValues": List[str],
        "ConstraintDescription": str,
        "DefaultValue": str,
        "Description": str,
        "MaxLength": int,
        "MaxValue": int,
        "MinLength": int,
        "MinValue": int,
        "NoEcho": bool,
        "Type": str,
    },
    total=False,
)


class ParameterDefinitionTypeDef(
    _RequiredParameterDefinitionTypeDef, _OptionalParameterDefinitionTypeDef
):
    pass


ParameterValueTypeDef = TypedDict(
    "ParameterValueTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateCloudFormationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCloudFormationTemplateRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalCreateCloudFormationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCloudFormationTemplateRequestRequestTypeDef",
    {
        "SemanticVersion": str,
    },
    total=False,
)


class CreateCloudFormationTemplateRequestRequestTypeDef(
    _RequiredCreateCloudFormationTemplateRequestRequestTypeDef,
    _OptionalCreateCloudFormationTemplateRequestRequestTypeDef,
):
    pass


DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetApplicationPolicyRequestRequestTypeDef = TypedDict(
    "GetApplicationPolicyRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

_RequiredGetApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredGetApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalGetApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalGetApplicationRequestRequestTypeDef",
    {
        "SemanticVersion": str,
    },
    total=False,
)


class GetApplicationRequestRequestTypeDef(
    _RequiredGetApplicationRequestRequestTypeDef, _OptionalGetApplicationRequestRequestTypeDef
):
    pass


GetCloudFormationTemplateRequestRequestTypeDef = TypedDict(
    "GetCloudFormationTemplateRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "TemplateId": str,
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

_RequiredListApplicationDependenciesRequestRequestTypeDef = TypedDict(
    "_RequiredListApplicationDependenciesRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListApplicationDependenciesRequestRequestTypeDef = TypedDict(
    "_OptionalListApplicationDependenciesRequestRequestTypeDef",
    {
        "MaxItems": int,
        "NextToken": str,
        "SemanticVersion": str,
    },
    total=False,
)


class ListApplicationDependenciesRequestRequestTypeDef(
    _RequiredListApplicationDependenciesRequestRequestTypeDef,
    _OptionalListApplicationDependenciesRequestRequestTypeDef,
):
    pass


_RequiredListApplicationVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListApplicationVersionsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListApplicationVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListApplicationVersionsRequestRequestTypeDef",
    {
        "MaxItems": int,
        "NextToken": str,
    },
    total=False,
)


class ListApplicationVersionsRequestRequestTypeDef(
    _RequiredListApplicationVersionsRequestRequestTypeDef,
    _OptionalListApplicationVersionsRequestRequestTypeDef,
):
    pass


_RequiredVersionSummaryTypeDef = TypedDict(
    "_RequiredVersionSummaryTypeDef",
    {
        "ApplicationId": str,
        "CreationTime": str,
        "SemanticVersion": str,
    },
)
_OptionalVersionSummaryTypeDef = TypedDict(
    "_OptionalVersionSummaryTypeDef",
    {
        "SourceCodeUrl": str,
    },
    total=False,
)


class VersionSummaryTypeDef(_RequiredVersionSummaryTypeDef, _OptionalVersionSummaryTypeDef):
    pass


ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "MaxItems": int,
        "NextToken": str,
    },
    total=False,
)

RollbackTriggerTypeDef = TypedDict(
    "RollbackTriggerTypeDef",
    {
        "Arn": str,
        "Type": str,
    },
)

UnshareApplicationRequestRequestTypeDef = TypedDict(
    "UnshareApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "OrganizationId": str,
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "Author": str,
        "Description": str,
        "HomePageUrl": str,
        "Labels": Sequence[str],
        "ReadmeBody": str,
        "ReadmeUrl": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


PutApplicationPolicyRequestRequestTypeDef = TypedDict(
    "PutApplicationPolicyRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Statements": Sequence[ApplicationPolicyStatementTypeDef],
    },
)

CreateCloudFormationChangeSetResponseTypeDef = TypedDict(
    "CreateCloudFormationChangeSetResponseTypeDef",
    {
        "ApplicationId": str,
        "ChangeSetId": str,
        "SemanticVersion": str,
        "StackId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCloudFormationTemplateResponseTypeDef = TypedDict(
    "CreateCloudFormationTemplateResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationTime": str,
        "ExpirationTime": str,
        "SemanticVersion": str,
        "Status": StatusType,
        "TemplateId": str,
        "TemplateUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationPolicyResponseTypeDef = TypedDict(
    "GetApplicationPolicyResponseTypeDef",
    {
        "Statements": List[ApplicationPolicyStatementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCloudFormationTemplateResponseTypeDef = TypedDict(
    "GetCloudFormationTemplateResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationTime": str,
        "ExpirationTime": str,
        "SemanticVersion": str,
        "Status": StatusType,
        "TemplateId": str,
        "TemplateUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationDependenciesResponseTypeDef = TypedDict(
    "ListApplicationDependenciesResponseTypeDef",
    {
        "Dependencies": List[ApplicationDependencySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "Applications": List[ApplicationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutApplicationPolicyResponseTypeDef = TypedDict(
    "PutApplicationPolicyResponseTypeDef",
    {
        "Statements": List[ApplicationPolicyStatementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationVersionResponseTypeDef = TypedDict(
    "CreateApplicationVersionResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationTime": str,
        "ParameterDefinitions": List[ParameterDefinitionTypeDef],
        "RequiredCapabilities": List[CapabilityType],
        "ResourcesSupported": bool,
        "SemanticVersion": str,
        "SourceCodeArchiveUrl": str,
        "SourceCodeUrl": str,
        "TemplateUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredVersionTypeDef = TypedDict(
    "_RequiredVersionTypeDef",
    {
        "ApplicationId": str,
        "CreationTime": str,
        "ParameterDefinitions": List[ParameterDefinitionTypeDef],
        "RequiredCapabilities": List[CapabilityType],
        "ResourcesSupported": bool,
        "SemanticVersion": str,
        "TemplateUrl": str,
    },
)
_OptionalVersionTypeDef = TypedDict(
    "_OptionalVersionTypeDef",
    {
        "SourceCodeArchiveUrl": str,
        "SourceCodeUrl": str,
    },
    total=False,
)


class VersionTypeDef(_RequiredVersionTypeDef, _OptionalVersionTypeDef):
    pass


_RequiredListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef = TypedDict(
    "_RequiredListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef = TypedDict(
    "_OptionalListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef",
    {
        "SemanticVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef(
    _RequiredListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef,
    _OptionalListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef,
):
    pass


_RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef = TypedDict(
    "_RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef = TypedDict(
    "_OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef(
    _RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
    _OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
):
    pass


ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListApplicationVersionsResponseTypeDef = TypedDict(
    "ListApplicationVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Versions": List[VersionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RollbackConfigurationTypeDef = TypedDict(
    "RollbackConfigurationTypeDef",
    {
        "MonitoringTimeInMinutes": int,
        "RollbackTriggers": Sequence[RollbackTriggerTypeDef],
    },
    total=False,
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "ApplicationId": str,
        "Author": str,
        "CreationTime": str,
        "Description": str,
        "HomePageUrl": str,
        "IsVerifiedAuthor": bool,
        "Labels": List[str],
        "LicenseUrl": str,
        "Name": str,
        "ReadmeUrl": str,
        "SpdxLicenseId": str,
        "VerifiedAuthorUrl": str,
        "Version": VersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "ApplicationId": str,
        "Author": str,
        "CreationTime": str,
        "Description": str,
        "HomePageUrl": str,
        "IsVerifiedAuthor": bool,
        "Labels": List[str],
        "LicenseUrl": str,
        "Name": str,
        "ReadmeUrl": str,
        "SpdxLicenseId": str,
        "VerifiedAuthorUrl": str,
        "Version": VersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "ApplicationId": str,
        "Author": str,
        "CreationTime": str,
        "Description": str,
        "HomePageUrl": str,
        "IsVerifiedAuthor": bool,
        "Labels": List[str],
        "LicenseUrl": str,
        "Name": str,
        "ReadmeUrl": str,
        "SpdxLicenseId": str,
        "VerifiedAuthorUrl": str,
        "Version": VersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateCloudFormationChangeSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCloudFormationChangeSetRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "StackName": str,
    },
)
_OptionalCreateCloudFormationChangeSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCloudFormationChangeSetRequestRequestTypeDef",
    {
        "Capabilities": Sequence[str],
        "ChangeSetName": str,
        "ClientToken": str,
        "Description": str,
        "NotificationArns": Sequence[str],
        "ParameterOverrides": Sequence[ParameterValueTypeDef],
        "ResourceTypes": Sequence[str],
        "RollbackConfiguration": RollbackConfigurationTypeDef,
        "SemanticVersion": str,
        "Tags": Sequence[TagTypeDef],
        "TemplateId": str,
    },
    total=False,
)


class CreateCloudFormationChangeSetRequestRequestTypeDef(
    _RequiredCreateCloudFormationChangeSetRequestRequestTypeDef,
    _OptionalCreateCloudFormationChangeSetRequestRequestTypeDef,
):
    pass
