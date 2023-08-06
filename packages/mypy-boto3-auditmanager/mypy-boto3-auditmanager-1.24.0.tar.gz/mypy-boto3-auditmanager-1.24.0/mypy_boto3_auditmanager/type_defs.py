"""
Type annotations for auditmanager service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/type_defs/)

Usage::

    ```python
    from mypy_boto3_auditmanager.type_defs import AWSAccountTypeDef

    data: AWSAccountTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccountStatusType,
    ActionEnumType,
    AssessmentReportStatusType,
    AssessmentStatusType,
    ControlResponseType,
    ControlSetStatusType,
    ControlStatusType,
    ControlTypeType,
    DelegationStatusType,
    FrameworkTypeType,
    ObjectTypeEnumType,
    RoleTypeType,
    SettingAttributeType,
    ShareRequestActionType,
    ShareRequestStatusType,
    ShareRequestTypeType,
    SourceFrequencyType,
    SourceSetUpOptionType,
    SourceTypeType,
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
    "AWSAccountTypeDef",
    "AWSServiceTypeDef",
    "DelegationTypeDef",
    "RoleTypeDef",
    "ControlCommentTypeDef",
    "AssessmentEvidenceFolderTypeDef",
    "AssessmentFrameworkMetadataTypeDef",
    "AssessmentFrameworkShareRequestTypeDef",
    "FrameworkMetadataTypeDef",
    "AssessmentReportsDestinationTypeDef",
    "AssessmentReportEvidenceErrorTypeDef",
    "AssessmentReportMetadataTypeDef",
    "AssessmentReportTypeDef",
    "AssociateAssessmentReportEvidenceFolderRequestRequestTypeDef",
    "BatchAssociateAssessmentReportEvidenceRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateDelegationRequestTypeDef",
    "BatchDeleteDelegationByAssessmentErrorTypeDef",
    "BatchDeleteDelegationByAssessmentRequestRequestTypeDef",
    "BatchDisassociateAssessmentReportEvidenceRequestRequestTypeDef",
    "ManualEvidenceTypeDef",
    "ChangeLogTypeDef",
    "EvidenceInsightsTypeDef",
    "SourceKeywordTypeDef",
    "ControlMetadataTypeDef",
    "CreateAssessmentFrameworkControlTypeDef",
    "CreateAssessmentReportRequestRequestTypeDef",
    "DelegationMetadataTypeDef",
    "DeleteAssessmentFrameworkRequestRequestTypeDef",
    "DeleteAssessmentFrameworkShareRequestRequestTypeDef",
    "DeleteAssessmentReportRequestRequestTypeDef",
    "DeleteAssessmentRequestRequestTypeDef",
    "DeleteControlRequestRequestTypeDef",
    "DeregisterOrganizationAdminAccountRequestRequestTypeDef",
    "DisassociateAssessmentReportEvidenceFolderRequestRequestTypeDef",
    "ResourceTypeDef",
    "GetAssessmentFrameworkRequestRequestTypeDef",
    "GetAssessmentReportUrlRequestRequestTypeDef",
    "URLTypeDef",
    "GetAssessmentRequestRequestTypeDef",
    "GetChangeLogsRequestRequestTypeDef",
    "GetControlRequestRequestTypeDef",
    "GetDelegationsRequestRequestTypeDef",
    "GetEvidenceByEvidenceFolderRequestRequestTypeDef",
    "GetEvidenceFolderRequestRequestTypeDef",
    "GetEvidenceFoldersByAssessmentControlRequestRequestTypeDef",
    "GetEvidenceFoldersByAssessmentRequestRequestTypeDef",
    "GetEvidenceRequestRequestTypeDef",
    "GetInsightsByAssessmentRequestRequestTypeDef",
    "InsightsByAssessmentTypeDef",
    "InsightsTypeDef",
    "ServiceMetadataTypeDef",
    "GetSettingsRequestRequestTypeDef",
    "ListAssessmentControlInsightsByControlDomainRequestRequestTypeDef",
    "ListAssessmentFrameworkShareRequestsRequestRequestTypeDef",
    "ListAssessmentFrameworksRequestRequestTypeDef",
    "ListAssessmentReportsRequestRequestTypeDef",
    "ListAssessmentsRequestRequestTypeDef",
    "ListControlDomainInsightsByAssessmentRequestRequestTypeDef",
    "ListControlDomainInsightsRequestRequestTypeDef",
    "ListControlInsightsByControlDomainRequestRequestTypeDef",
    "ListControlsRequestRequestTypeDef",
    "ListKeywordsForDataSourceRequestRequestTypeDef",
    "ListNotificationsRequestRequestTypeDef",
    "NotificationTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RegisterAccountRequestRequestTypeDef",
    "RegisterOrganizationAdminAccountRequestRequestTypeDef",
    "StartAssessmentFrameworkShareRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssessmentControlRequestRequestTypeDef",
    "UpdateAssessmentControlSetStatusRequestRequestTypeDef",
    "UpdateAssessmentFrameworkShareRequestRequestTypeDef",
    "UpdateAssessmentStatusRequestRequestTypeDef",
    "ValidateAssessmentReportIntegrityRequestRequestTypeDef",
    "ScopeTypeDef",
    "AssessmentMetadataItemTypeDef",
    "AssessmentControlTypeDef",
    "SettingsTypeDef",
    "UpdateSettingsRequestRequestTypeDef",
    "BatchAssociateAssessmentReportEvidenceResponseTypeDef",
    "BatchDisassociateAssessmentReportEvidenceResponseTypeDef",
    "CreateAssessmentReportResponseTypeDef",
    "DeregisterAccountResponseTypeDef",
    "GetAccountStatusResponseTypeDef",
    "GetEvidenceFolderResponseTypeDef",
    "GetEvidenceFoldersByAssessmentControlResponseTypeDef",
    "GetEvidenceFoldersByAssessmentResponseTypeDef",
    "GetOrganizationAdminAccountResponseTypeDef",
    "ListAssessmentFrameworkShareRequestsResponseTypeDef",
    "ListAssessmentFrameworksResponseTypeDef",
    "ListAssessmentReportsResponseTypeDef",
    "ListKeywordsForDataSourceResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RegisterAccountResponseTypeDef",
    "RegisterOrganizationAdminAccountResponseTypeDef",
    "StartAssessmentFrameworkShareResponseTypeDef",
    "UpdateAssessmentFrameworkShareResponseTypeDef",
    "ValidateAssessmentReportIntegrityResponseTypeDef",
    "BatchCreateDelegationByAssessmentErrorTypeDef",
    "BatchCreateDelegationByAssessmentRequestRequestTypeDef",
    "BatchDeleteDelegationByAssessmentResponseTypeDef",
    "BatchImportEvidenceToAssessmentControlErrorTypeDef",
    "BatchImportEvidenceToAssessmentControlRequestRequestTypeDef",
    "GetChangeLogsResponseTypeDef",
    "ControlDomainInsightsTypeDef",
    "ControlInsightsMetadataByAssessmentItemTypeDef",
    "ControlInsightsMetadataItemTypeDef",
    "ControlMappingSourceTypeDef",
    "CreateControlMappingSourceTypeDef",
    "ListControlsResponseTypeDef",
    "CreateAssessmentFrameworkControlSetTypeDef",
    "UpdateAssessmentFrameworkControlSetTypeDef",
    "GetDelegationsResponseTypeDef",
    "EvidenceTypeDef",
    "GetAssessmentReportUrlResponseTypeDef",
    "GetInsightsByAssessmentResponseTypeDef",
    "GetInsightsResponseTypeDef",
    "GetServicesInScopeResponseTypeDef",
    "ListNotificationsResponseTypeDef",
    "AssessmentMetadataTypeDef",
    "CreateAssessmentRequestRequestTypeDef",
    "UpdateAssessmentRequestRequestTypeDef",
    "ListAssessmentsResponseTypeDef",
    "AssessmentControlSetTypeDef",
    "UpdateAssessmentControlResponseTypeDef",
    "GetSettingsResponseTypeDef",
    "UpdateSettingsResponseTypeDef",
    "BatchCreateDelegationByAssessmentResponseTypeDef",
    "BatchImportEvidenceToAssessmentControlResponseTypeDef",
    "ListControlDomainInsightsByAssessmentResponseTypeDef",
    "ListControlDomainInsightsResponseTypeDef",
    "ListAssessmentControlInsightsByControlDomainResponseTypeDef",
    "ListControlInsightsByControlDomainResponseTypeDef",
    "ControlTypeDef",
    "UpdateControlRequestRequestTypeDef",
    "CreateControlRequestRequestTypeDef",
    "CreateAssessmentFrameworkRequestRequestTypeDef",
    "UpdateAssessmentFrameworkRequestRequestTypeDef",
    "GetEvidenceByEvidenceFolderResponseTypeDef",
    "GetEvidenceResponseTypeDef",
    "AssessmentFrameworkTypeDef",
    "UpdateAssessmentControlSetStatusResponseTypeDef",
    "ControlSetTypeDef",
    "CreateControlResponseTypeDef",
    "GetControlResponseTypeDef",
    "UpdateControlResponseTypeDef",
    "AssessmentTypeDef",
    "FrameworkTypeDef",
    "CreateAssessmentResponseTypeDef",
    "GetAssessmentResponseTypeDef",
    "UpdateAssessmentResponseTypeDef",
    "UpdateAssessmentStatusResponseTypeDef",
    "CreateAssessmentFrameworkResponseTypeDef",
    "GetAssessmentFrameworkResponseTypeDef",
    "UpdateAssessmentFrameworkResponseTypeDef",
)

AWSAccountTypeDef = TypedDict(
    "AWSAccountTypeDef",
    {
        "id": str,
        "emailAddress": str,
        "name": str,
    },
    total=False,
)

AWSServiceTypeDef = TypedDict(
    "AWSServiceTypeDef",
    {
        "serviceName": str,
    },
    total=False,
)

DelegationTypeDef = TypedDict(
    "DelegationTypeDef",
    {
        "id": str,
        "assessmentName": str,
        "assessmentId": str,
        "status": DelegationStatusType,
        "roleArn": str,
        "roleType": RoleTypeType,
        "creationTime": datetime,
        "lastUpdated": datetime,
        "controlSetId": str,
        "comment": str,
        "createdBy": str,
    },
    total=False,
)

RoleTypeDef = TypedDict(
    "RoleTypeDef",
    {
        "roleType": RoleTypeType,
        "roleArn": str,
    },
    total=False,
)

ControlCommentTypeDef = TypedDict(
    "ControlCommentTypeDef",
    {
        "authorName": str,
        "commentBody": str,
        "postedDate": datetime,
    },
    total=False,
)

AssessmentEvidenceFolderTypeDef = TypedDict(
    "AssessmentEvidenceFolderTypeDef",
    {
        "name": str,
        "date": datetime,
        "assessmentId": str,
        "controlSetId": str,
        "controlId": str,
        "id": str,
        "dataSource": str,
        "author": str,
        "totalEvidence": int,
        "assessmentReportSelectionCount": int,
        "controlName": str,
        "evidenceResourcesIncludedCount": int,
        "evidenceByTypeConfigurationDataCount": int,
        "evidenceByTypeManualCount": int,
        "evidenceByTypeComplianceCheckCount": int,
        "evidenceByTypeComplianceCheckIssuesCount": int,
        "evidenceByTypeUserActivityCount": int,
        "evidenceAwsServiceSourceCount": int,
    },
    total=False,
)

AssessmentFrameworkMetadataTypeDef = TypedDict(
    "AssessmentFrameworkMetadataTypeDef",
    {
        "arn": str,
        "id": str,
        "type": FrameworkTypeType,
        "name": str,
        "description": str,
        "logo": str,
        "complianceType": str,
        "controlsCount": int,
        "controlSetsCount": int,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

AssessmentFrameworkShareRequestTypeDef = TypedDict(
    "AssessmentFrameworkShareRequestTypeDef",
    {
        "id": str,
        "frameworkId": str,
        "frameworkName": str,
        "frameworkDescription": str,
        "status": ShareRequestStatusType,
        "sourceAccount": str,
        "destinationAccount": str,
        "destinationRegion": str,
        "expirationTime": datetime,
        "creationTime": datetime,
        "lastUpdated": datetime,
        "comment": str,
        "standardControlsCount": int,
        "customControlsCount": int,
        "complianceType": str,
    },
    total=False,
)

FrameworkMetadataTypeDef = TypedDict(
    "FrameworkMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "logo": str,
        "complianceType": str,
    },
    total=False,
)

AssessmentReportsDestinationTypeDef = TypedDict(
    "AssessmentReportsDestinationTypeDef",
    {
        "destinationType": Literal["S3"],
        "destination": str,
    },
    total=False,
)

AssessmentReportEvidenceErrorTypeDef = TypedDict(
    "AssessmentReportEvidenceErrorTypeDef",
    {
        "evidenceId": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

AssessmentReportMetadataTypeDef = TypedDict(
    "AssessmentReportMetadataTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "assessmentId": str,
        "assessmentName": str,
        "author": str,
        "status": AssessmentReportStatusType,
        "creationTime": datetime,
    },
    total=False,
)

AssessmentReportTypeDef = TypedDict(
    "AssessmentReportTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "awsAccountId": str,
        "assessmentId": str,
        "assessmentName": str,
        "author": str,
        "status": AssessmentReportStatusType,
        "creationTime": datetime,
    },
    total=False,
)

AssociateAssessmentReportEvidenceFolderRequestRequestTypeDef = TypedDict(
    "AssociateAssessmentReportEvidenceFolderRequestRequestTypeDef",
    {
        "assessmentId": str,
        "evidenceFolderId": str,
    },
)

BatchAssociateAssessmentReportEvidenceRequestRequestTypeDef = TypedDict(
    "BatchAssociateAssessmentReportEvidenceRequestRequestTypeDef",
    {
        "assessmentId": str,
        "evidenceFolderId": str,
        "evidenceIds": Sequence[str],
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

CreateDelegationRequestTypeDef = TypedDict(
    "CreateDelegationRequestTypeDef",
    {
        "comment": str,
        "controlSetId": str,
        "roleArn": str,
        "roleType": RoleTypeType,
    },
    total=False,
)

BatchDeleteDelegationByAssessmentErrorTypeDef = TypedDict(
    "BatchDeleteDelegationByAssessmentErrorTypeDef",
    {
        "delegationId": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchDeleteDelegationByAssessmentRequestRequestTypeDef = TypedDict(
    "BatchDeleteDelegationByAssessmentRequestRequestTypeDef",
    {
        "delegationIds": Sequence[str],
        "assessmentId": str,
    },
)

BatchDisassociateAssessmentReportEvidenceRequestRequestTypeDef = TypedDict(
    "BatchDisassociateAssessmentReportEvidenceRequestRequestTypeDef",
    {
        "assessmentId": str,
        "evidenceFolderId": str,
        "evidenceIds": Sequence[str],
    },
)

ManualEvidenceTypeDef = TypedDict(
    "ManualEvidenceTypeDef",
    {
        "s3ResourcePath": str,
    },
    total=False,
)

ChangeLogTypeDef = TypedDict(
    "ChangeLogTypeDef",
    {
        "objectType": ObjectTypeEnumType,
        "objectName": str,
        "action": ActionEnumType,
        "createdAt": datetime,
        "createdBy": str,
    },
    total=False,
)

EvidenceInsightsTypeDef = TypedDict(
    "EvidenceInsightsTypeDef",
    {
        "noncompliantEvidenceCount": int,
        "compliantEvidenceCount": int,
        "inconclusiveEvidenceCount": int,
    },
    total=False,
)

SourceKeywordTypeDef = TypedDict(
    "SourceKeywordTypeDef",
    {
        "keywordInputType": Literal["SELECT_FROM_LIST"],
        "keywordValue": str,
    },
    total=False,
)

ControlMetadataTypeDef = TypedDict(
    "ControlMetadataTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "controlSources": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

CreateAssessmentFrameworkControlTypeDef = TypedDict(
    "CreateAssessmentFrameworkControlTypeDef",
    {
        "id": str,
    },
)

_RequiredCreateAssessmentReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssessmentReportRequestRequestTypeDef",
    {
        "name": str,
        "assessmentId": str,
    },
)
_OptionalCreateAssessmentReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssessmentReportRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class CreateAssessmentReportRequestRequestTypeDef(
    _RequiredCreateAssessmentReportRequestRequestTypeDef,
    _OptionalCreateAssessmentReportRequestRequestTypeDef,
):
    pass


DelegationMetadataTypeDef = TypedDict(
    "DelegationMetadataTypeDef",
    {
        "id": str,
        "assessmentName": str,
        "assessmentId": str,
        "status": DelegationStatusType,
        "roleArn": str,
        "creationTime": datetime,
        "controlSetName": str,
    },
    total=False,
)

DeleteAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentFrameworkRequestRequestTypeDef",
    {
        "frameworkId": str,
    },
)

DeleteAssessmentFrameworkShareRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentFrameworkShareRequestRequestTypeDef",
    {
        "requestId": str,
        "requestType": ShareRequestTypeType,
    },
)

DeleteAssessmentReportRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentReportRequestRequestTypeDef",
    {
        "assessmentId": str,
        "assessmentReportId": str,
    },
)

DeleteAssessmentRequestRequestTypeDef = TypedDict(
    "DeleteAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)

DeleteControlRequestRequestTypeDef = TypedDict(
    "DeleteControlRequestRequestTypeDef",
    {
        "controlId": str,
    },
)

DeregisterOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "DeregisterOrganizationAdminAccountRequestRequestTypeDef",
    {
        "adminAccountId": str,
    },
    total=False,
)

DisassociateAssessmentReportEvidenceFolderRequestRequestTypeDef = TypedDict(
    "DisassociateAssessmentReportEvidenceFolderRequestRequestTypeDef",
    {
        "assessmentId": str,
        "evidenceFolderId": str,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "arn": str,
        "value": str,
    },
    total=False,
)

GetAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "GetAssessmentFrameworkRequestRequestTypeDef",
    {
        "frameworkId": str,
    },
)

GetAssessmentReportUrlRequestRequestTypeDef = TypedDict(
    "GetAssessmentReportUrlRequestRequestTypeDef",
    {
        "assessmentReportId": str,
        "assessmentId": str,
    },
)

URLTypeDef = TypedDict(
    "URLTypeDef",
    {
        "hyperlinkName": str,
        "link": str,
    },
    total=False,
)

GetAssessmentRequestRequestTypeDef = TypedDict(
    "GetAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)

_RequiredGetChangeLogsRequestRequestTypeDef = TypedDict(
    "_RequiredGetChangeLogsRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)
_OptionalGetChangeLogsRequestRequestTypeDef = TypedDict(
    "_OptionalGetChangeLogsRequestRequestTypeDef",
    {
        "controlSetId": str,
        "controlId": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetChangeLogsRequestRequestTypeDef(
    _RequiredGetChangeLogsRequestRequestTypeDef, _OptionalGetChangeLogsRequestRequestTypeDef
):
    pass


GetControlRequestRequestTypeDef = TypedDict(
    "GetControlRequestRequestTypeDef",
    {
        "controlId": str,
    },
)

GetDelegationsRequestRequestTypeDef = TypedDict(
    "GetDelegationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredGetEvidenceByEvidenceFolderRequestRequestTypeDef = TypedDict(
    "_RequiredGetEvidenceByEvidenceFolderRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "evidenceFolderId": str,
    },
)
_OptionalGetEvidenceByEvidenceFolderRequestRequestTypeDef = TypedDict(
    "_OptionalGetEvidenceByEvidenceFolderRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetEvidenceByEvidenceFolderRequestRequestTypeDef(
    _RequiredGetEvidenceByEvidenceFolderRequestRequestTypeDef,
    _OptionalGetEvidenceByEvidenceFolderRequestRequestTypeDef,
):
    pass


GetEvidenceFolderRequestRequestTypeDef = TypedDict(
    "GetEvidenceFolderRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "evidenceFolderId": str,
    },
)

_RequiredGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef = TypedDict(
    "_RequiredGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "controlId": str,
    },
)
_OptionalGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef = TypedDict(
    "_OptionalGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetEvidenceFoldersByAssessmentControlRequestRequestTypeDef(
    _RequiredGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef,
    _OptionalGetEvidenceFoldersByAssessmentControlRequestRequestTypeDef,
):
    pass


_RequiredGetEvidenceFoldersByAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredGetEvidenceFoldersByAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)
_OptionalGetEvidenceFoldersByAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalGetEvidenceFoldersByAssessmentRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetEvidenceFoldersByAssessmentRequestRequestTypeDef(
    _RequiredGetEvidenceFoldersByAssessmentRequestRequestTypeDef,
    _OptionalGetEvidenceFoldersByAssessmentRequestRequestTypeDef,
):
    pass


GetEvidenceRequestRequestTypeDef = TypedDict(
    "GetEvidenceRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "evidenceFolderId": str,
        "evidenceId": str,
    },
)

GetInsightsByAssessmentRequestRequestTypeDef = TypedDict(
    "GetInsightsByAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)

InsightsByAssessmentTypeDef = TypedDict(
    "InsightsByAssessmentTypeDef",
    {
        "noncompliantEvidenceCount": int,
        "compliantEvidenceCount": int,
        "inconclusiveEvidenceCount": int,
        "assessmentControlsCountByNoncompliantEvidence": int,
        "totalAssessmentControlsCount": int,
        "lastUpdated": datetime,
    },
    total=False,
)

InsightsTypeDef = TypedDict(
    "InsightsTypeDef",
    {
        "activeAssessmentsCount": int,
        "noncompliantEvidenceCount": int,
        "compliantEvidenceCount": int,
        "inconclusiveEvidenceCount": int,
        "assessmentControlsCountByNoncompliantEvidence": int,
        "totalAssessmentControlsCount": int,
        "lastUpdated": datetime,
    },
    total=False,
)

ServiceMetadataTypeDef = TypedDict(
    "ServiceMetadataTypeDef",
    {
        "name": str,
        "displayName": str,
        "description": str,
        "category": str,
    },
    total=False,
)

GetSettingsRequestRequestTypeDef = TypedDict(
    "GetSettingsRequestRequestTypeDef",
    {
        "attribute": SettingAttributeType,
    },
)

_RequiredListAssessmentControlInsightsByControlDomainRequestRequestTypeDef = TypedDict(
    "_RequiredListAssessmentControlInsightsByControlDomainRequestRequestTypeDef",
    {
        "controlDomainId": str,
        "assessmentId": str,
    },
)
_OptionalListAssessmentControlInsightsByControlDomainRequestRequestTypeDef = TypedDict(
    "_OptionalListAssessmentControlInsightsByControlDomainRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssessmentControlInsightsByControlDomainRequestRequestTypeDef(
    _RequiredListAssessmentControlInsightsByControlDomainRequestRequestTypeDef,
    _OptionalListAssessmentControlInsightsByControlDomainRequestRequestTypeDef,
):
    pass


_RequiredListAssessmentFrameworkShareRequestsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssessmentFrameworkShareRequestsRequestRequestTypeDef",
    {
        "requestType": ShareRequestTypeType,
    },
)
_OptionalListAssessmentFrameworkShareRequestsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssessmentFrameworkShareRequestsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssessmentFrameworkShareRequestsRequestRequestTypeDef(
    _RequiredListAssessmentFrameworkShareRequestsRequestRequestTypeDef,
    _OptionalListAssessmentFrameworkShareRequestsRequestRequestTypeDef,
):
    pass


_RequiredListAssessmentFrameworksRequestRequestTypeDef = TypedDict(
    "_RequiredListAssessmentFrameworksRequestRequestTypeDef",
    {
        "frameworkType": FrameworkTypeType,
    },
)
_OptionalListAssessmentFrameworksRequestRequestTypeDef = TypedDict(
    "_OptionalListAssessmentFrameworksRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssessmentFrameworksRequestRequestTypeDef(
    _RequiredListAssessmentFrameworksRequestRequestTypeDef,
    _OptionalListAssessmentFrameworksRequestRequestTypeDef,
):
    pass


ListAssessmentReportsRequestRequestTypeDef = TypedDict(
    "ListAssessmentReportsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListAssessmentsRequestRequestTypeDef = TypedDict(
    "ListAssessmentsRequestRequestTypeDef",
    {
        "status": AssessmentStatusType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListControlDomainInsightsByAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredListControlDomainInsightsByAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
    },
)
_OptionalListControlDomainInsightsByAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalListControlDomainInsightsByAssessmentRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListControlDomainInsightsByAssessmentRequestRequestTypeDef(
    _RequiredListControlDomainInsightsByAssessmentRequestRequestTypeDef,
    _OptionalListControlDomainInsightsByAssessmentRequestRequestTypeDef,
):
    pass


ListControlDomainInsightsRequestRequestTypeDef = TypedDict(
    "ListControlDomainInsightsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListControlInsightsByControlDomainRequestRequestTypeDef = TypedDict(
    "_RequiredListControlInsightsByControlDomainRequestRequestTypeDef",
    {
        "controlDomainId": str,
    },
)
_OptionalListControlInsightsByControlDomainRequestRequestTypeDef = TypedDict(
    "_OptionalListControlInsightsByControlDomainRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListControlInsightsByControlDomainRequestRequestTypeDef(
    _RequiredListControlInsightsByControlDomainRequestRequestTypeDef,
    _OptionalListControlInsightsByControlDomainRequestRequestTypeDef,
):
    pass


_RequiredListControlsRequestRequestTypeDef = TypedDict(
    "_RequiredListControlsRequestRequestTypeDef",
    {
        "controlType": ControlTypeType,
    },
)
_OptionalListControlsRequestRequestTypeDef = TypedDict(
    "_OptionalListControlsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListControlsRequestRequestTypeDef(
    _RequiredListControlsRequestRequestTypeDef, _OptionalListControlsRequestRequestTypeDef
):
    pass


_RequiredListKeywordsForDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredListKeywordsForDataSourceRequestRequestTypeDef",
    {
        "source": SourceTypeType,
    },
)
_OptionalListKeywordsForDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalListKeywordsForDataSourceRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListKeywordsForDataSourceRequestRequestTypeDef(
    _RequiredListKeywordsForDataSourceRequestRequestTypeDef,
    _OptionalListKeywordsForDataSourceRequestRequestTypeDef,
):
    pass


ListNotificationsRequestRequestTypeDef = TypedDict(
    "ListNotificationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

NotificationTypeDef = TypedDict(
    "NotificationTypeDef",
    {
        "id": str,
        "assessmentId": str,
        "assessmentName": str,
        "controlSetId": str,
        "controlSetName": str,
        "description": str,
        "eventTime": datetime,
        "source": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

RegisterAccountRequestRequestTypeDef = TypedDict(
    "RegisterAccountRequestRequestTypeDef",
    {
        "kmsKey": str,
        "delegatedAdminAccount": str,
    },
    total=False,
)

RegisterOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "RegisterOrganizationAdminAccountRequestRequestTypeDef",
    {
        "adminAccountId": str,
    },
)

_RequiredStartAssessmentFrameworkShareRequestRequestTypeDef = TypedDict(
    "_RequiredStartAssessmentFrameworkShareRequestRequestTypeDef",
    {
        "frameworkId": str,
        "destinationAccount": str,
        "destinationRegion": str,
    },
)
_OptionalStartAssessmentFrameworkShareRequestRequestTypeDef = TypedDict(
    "_OptionalStartAssessmentFrameworkShareRequestRequestTypeDef",
    {
        "comment": str,
    },
    total=False,
)


class StartAssessmentFrameworkShareRequestRequestTypeDef(
    _RequiredStartAssessmentFrameworkShareRequestRequestTypeDef,
    _OptionalStartAssessmentFrameworkShareRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAssessmentControlRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssessmentControlRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "controlId": str,
    },
)
_OptionalUpdateAssessmentControlRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssessmentControlRequestRequestTypeDef",
    {
        "controlStatus": ControlStatusType,
        "commentBody": str,
    },
    total=False,
)


class UpdateAssessmentControlRequestRequestTypeDef(
    _RequiredUpdateAssessmentControlRequestRequestTypeDef,
    _OptionalUpdateAssessmentControlRequestRequestTypeDef,
):
    pass


UpdateAssessmentControlSetStatusRequestRequestTypeDef = TypedDict(
    "UpdateAssessmentControlSetStatusRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "status": ControlSetStatusType,
        "comment": str,
    },
)

UpdateAssessmentFrameworkShareRequestRequestTypeDef = TypedDict(
    "UpdateAssessmentFrameworkShareRequestRequestTypeDef",
    {
        "requestId": str,
        "requestType": ShareRequestTypeType,
        "action": ShareRequestActionType,
    },
)

UpdateAssessmentStatusRequestRequestTypeDef = TypedDict(
    "UpdateAssessmentStatusRequestRequestTypeDef",
    {
        "assessmentId": str,
        "status": AssessmentStatusType,
    },
)

ValidateAssessmentReportIntegrityRequestRequestTypeDef = TypedDict(
    "ValidateAssessmentReportIntegrityRequestRequestTypeDef",
    {
        "s3RelativePath": str,
    },
)

ScopeTypeDef = TypedDict(
    "ScopeTypeDef",
    {
        "awsAccounts": Sequence[AWSAccountTypeDef],
        "awsServices": Sequence[AWSServiceTypeDef],
    },
    total=False,
)

AssessmentMetadataItemTypeDef = TypedDict(
    "AssessmentMetadataItemTypeDef",
    {
        "name": str,
        "id": str,
        "complianceType": str,
        "status": AssessmentStatusType,
        "roles": List[RoleTypeDef],
        "delegations": List[DelegationTypeDef],
        "creationTime": datetime,
        "lastUpdated": datetime,
    },
    total=False,
)

AssessmentControlTypeDef = TypedDict(
    "AssessmentControlTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "status": ControlStatusType,
        "response": ControlResponseType,
        "comments": List[ControlCommentTypeDef],
        "evidenceSources": List[str],
        "evidenceCount": int,
        "assessmentReportEvidenceCount": int,
    },
    total=False,
)

SettingsTypeDef = TypedDict(
    "SettingsTypeDef",
    {
        "isAwsOrgEnabled": bool,
        "snsTopic": str,
        "defaultAssessmentReportsDestination": AssessmentReportsDestinationTypeDef,
        "defaultProcessOwners": List[RoleTypeDef],
        "kmsKey": str,
    },
    total=False,
)

UpdateSettingsRequestRequestTypeDef = TypedDict(
    "UpdateSettingsRequestRequestTypeDef",
    {
        "snsTopic": str,
        "defaultAssessmentReportsDestination": AssessmentReportsDestinationTypeDef,
        "defaultProcessOwners": Sequence[RoleTypeDef],
        "kmsKey": str,
    },
    total=False,
)

BatchAssociateAssessmentReportEvidenceResponseTypeDef = TypedDict(
    "BatchAssociateAssessmentReportEvidenceResponseTypeDef",
    {
        "evidenceIds": List[str],
        "errors": List[AssessmentReportEvidenceErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateAssessmentReportEvidenceResponseTypeDef = TypedDict(
    "BatchDisassociateAssessmentReportEvidenceResponseTypeDef",
    {
        "evidenceIds": List[str],
        "errors": List[AssessmentReportEvidenceErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssessmentReportResponseTypeDef = TypedDict(
    "CreateAssessmentReportResponseTypeDef",
    {
        "assessmentReport": AssessmentReportTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterAccountResponseTypeDef = TypedDict(
    "DeregisterAccountResponseTypeDef",
    {
        "status": AccountStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountStatusResponseTypeDef = TypedDict(
    "GetAccountStatusResponseTypeDef",
    {
        "status": AccountStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEvidenceFolderResponseTypeDef = TypedDict(
    "GetEvidenceFolderResponseTypeDef",
    {
        "evidenceFolder": AssessmentEvidenceFolderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEvidenceFoldersByAssessmentControlResponseTypeDef = TypedDict(
    "GetEvidenceFoldersByAssessmentControlResponseTypeDef",
    {
        "evidenceFolders": List[AssessmentEvidenceFolderTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEvidenceFoldersByAssessmentResponseTypeDef = TypedDict(
    "GetEvidenceFoldersByAssessmentResponseTypeDef",
    {
        "evidenceFolders": List[AssessmentEvidenceFolderTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOrganizationAdminAccountResponseTypeDef = TypedDict(
    "GetOrganizationAdminAccountResponseTypeDef",
    {
        "adminAccountId": str,
        "organizationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentFrameworkShareRequestsResponseTypeDef = TypedDict(
    "ListAssessmentFrameworkShareRequestsResponseTypeDef",
    {
        "assessmentFrameworkShareRequests": List[AssessmentFrameworkShareRequestTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentFrameworksResponseTypeDef = TypedDict(
    "ListAssessmentFrameworksResponseTypeDef",
    {
        "frameworkMetadataList": List[AssessmentFrameworkMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentReportsResponseTypeDef = TypedDict(
    "ListAssessmentReportsResponseTypeDef",
    {
        "assessmentReports": List[AssessmentReportMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKeywordsForDataSourceResponseTypeDef = TypedDict(
    "ListKeywordsForDataSourceResponseTypeDef",
    {
        "keywords": List[str],
        "nextToken": str,
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

RegisterAccountResponseTypeDef = TypedDict(
    "RegisterAccountResponseTypeDef",
    {
        "status": AccountStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterOrganizationAdminAccountResponseTypeDef = TypedDict(
    "RegisterOrganizationAdminAccountResponseTypeDef",
    {
        "adminAccountId": str,
        "organizationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAssessmentFrameworkShareResponseTypeDef = TypedDict(
    "StartAssessmentFrameworkShareResponseTypeDef",
    {
        "assessmentFrameworkShareRequest": AssessmentFrameworkShareRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssessmentFrameworkShareResponseTypeDef = TypedDict(
    "UpdateAssessmentFrameworkShareResponseTypeDef",
    {
        "assessmentFrameworkShareRequest": AssessmentFrameworkShareRequestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidateAssessmentReportIntegrityResponseTypeDef = TypedDict(
    "ValidateAssessmentReportIntegrityResponseTypeDef",
    {
        "signatureValid": bool,
        "signatureAlgorithm": str,
        "signatureDateTime": str,
        "signatureKeyId": str,
        "validationErrors": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchCreateDelegationByAssessmentErrorTypeDef = TypedDict(
    "BatchCreateDelegationByAssessmentErrorTypeDef",
    {
        "createDelegationRequest": CreateDelegationRequestTypeDef,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchCreateDelegationByAssessmentRequestRequestTypeDef = TypedDict(
    "BatchCreateDelegationByAssessmentRequestRequestTypeDef",
    {
        "createDelegationRequests": Sequence[CreateDelegationRequestTypeDef],
        "assessmentId": str,
    },
)

BatchDeleteDelegationByAssessmentResponseTypeDef = TypedDict(
    "BatchDeleteDelegationByAssessmentResponseTypeDef",
    {
        "errors": List[BatchDeleteDelegationByAssessmentErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchImportEvidenceToAssessmentControlErrorTypeDef = TypedDict(
    "BatchImportEvidenceToAssessmentControlErrorTypeDef",
    {
        "manualEvidence": ManualEvidenceTypeDef,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

BatchImportEvidenceToAssessmentControlRequestRequestTypeDef = TypedDict(
    "BatchImportEvidenceToAssessmentControlRequestRequestTypeDef",
    {
        "assessmentId": str,
        "controlSetId": str,
        "controlId": str,
        "manualEvidence": Sequence[ManualEvidenceTypeDef],
    },
)

GetChangeLogsResponseTypeDef = TypedDict(
    "GetChangeLogsResponseTypeDef",
    {
        "changeLogs": List[ChangeLogTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ControlDomainInsightsTypeDef = TypedDict(
    "ControlDomainInsightsTypeDef",
    {
        "name": str,
        "id": str,
        "controlsCountByNoncompliantEvidence": int,
        "totalControlsCount": int,
        "evidenceInsights": EvidenceInsightsTypeDef,
        "lastUpdated": datetime,
    },
    total=False,
)

ControlInsightsMetadataByAssessmentItemTypeDef = TypedDict(
    "ControlInsightsMetadataByAssessmentItemTypeDef",
    {
        "name": str,
        "id": str,
        "evidenceInsights": EvidenceInsightsTypeDef,
        "controlSetName": str,
        "lastUpdated": datetime,
    },
    total=False,
)

ControlInsightsMetadataItemTypeDef = TypedDict(
    "ControlInsightsMetadataItemTypeDef",
    {
        "name": str,
        "id": str,
        "evidenceInsights": EvidenceInsightsTypeDef,
        "lastUpdated": datetime,
    },
    total=False,
)

ControlMappingSourceTypeDef = TypedDict(
    "ControlMappingSourceTypeDef",
    {
        "sourceId": str,
        "sourceName": str,
        "sourceDescription": str,
        "sourceSetUpOption": SourceSetUpOptionType,
        "sourceType": SourceTypeType,
        "sourceKeyword": SourceKeywordTypeDef,
        "sourceFrequency": SourceFrequencyType,
        "troubleshootingText": str,
    },
    total=False,
)

CreateControlMappingSourceTypeDef = TypedDict(
    "CreateControlMappingSourceTypeDef",
    {
        "sourceName": str,
        "sourceDescription": str,
        "sourceSetUpOption": SourceSetUpOptionType,
        "sourceType": SourceTypeType,
        "sourceKeyword": SourceKeywordTypeDef,
        "sourceFrequency": SourceFrequencyType,
        "troubleshootingText": str,
    },
    total=False,
)

ListControlsResponseTypeDef = TypedDict(
    "ListControlsResponseTypeDef",
    {
        "controlMetadataList": List[ControlMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAssessmentFrameworkControlSetTypeDef = TypedDict(
    "_RequiredCreateAssessmentFrameworkControlSetTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateAssessmentFrameworkControlSetTypeDef = TypedDict(
    "_OptionalCreateAssessmentFrameworkControlSetTypeDef",
    {
        "controls": Sequence[CreateAssessmentFrameworkControlTypeDef],
    },
    total=False,
)


class CreateAssessmentFrameworkControlSetTypeDef(
    _RequiredCreateAssessmentFrameworkControlSetTypeDef,
    _OptionalCreateAssessmentFrameworkControlSetTypeDef,
):
    pass


_RequiredUpdateAssessmentFrameworkControlSetTypeDef = TypedDict(
    "_RequiredUpdateAssessmentFrameworkControlSetTypeDef",
    {
        "name": str,
        "controls": Sequence[CreateAssessmentFrameworkControlTypeDef],
    },
)
_OptionalUpdateAssessmentFrameworkControlSetTypeDef = TypedDict(
    "_OptionalUpdateAssessmentFrameworkControlSetTypeDef",
    {
        "id": str,
    },
    total=False,
)


class UpdateAssessmentFrameworkControlSetTypeDef(
    _RequiredUpdateAssessmentFrameworkControlSetTypeDef,
    _OptionalUpdateAssessmentFrameworkControlSetTypeDef,
):
    pass


GetDelegationsResponseTypeDef = TypedDict(
    "GetDelegationsResponseTypeDef",
    {
        "delegations": List[DelegationMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EvidenceTypeDef = TypedDict(
    "EvidenceTypeDef",
    {
        "dataSource": str,
        "evidenceAwsAccountId": str,
        "time": datetime,
        "eventSource": str,
        "eventName": str,
        "evidenceByType": str,
        "resourcesIncluded": List[ResourceTypeDef],
        "attributes": Dict[str, str],
        "iamId": str,
        "complianceCheck": str,
        "awsOrganization": str,
        "awsAccountId": str,
        "evidenceFolderId": str,
        "id": str,
        "assessmentReportSelection": str,
    },
    total=False,
)

GetAssessmentReportUrlResponseTypeDef = TypedDict(
    "GetAssessmentReportUrlResponseTypeDef",
    {
        "preSignedUrl": URLTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightsByAssessmentResponseTypeDef = TypedDict(
    "GetInsightsByAssessmentResponseTypeDef",
    {
        "insights": InsightsByAssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightsResponseTypeDef = TypedDict(
    "GetInsightsResponseTypeDef",
    {
        "insights": InsightsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServicesInScopeResponseTypeDef = TypedDict(
    "GetServicesInScopeResponseTypeDef",
    {
        "serviceMetadata": List[ServiceMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNotificationsResponseTypeDef = TypedDict(
    "ListNotificationsResponseTypeDef",
    {
        "notifications": List[NotificationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssessmentMetadataTypeDef = TypedDict(
    "AssessmentMetadataTypeDef",
    {
        "name": str,
        "id": str,
        "description": str,
        "complianceType": str,
        "status": AssessmentStatusType,
        "assessmentReportsDestination": AssessmentReportsDestinationTypeDef,
        "scope": ScopeTypeDef,
        "roles": List[RoleTypeDef],
        "delegations": List[DelegationTypeDef],
        "creationTime": datetime,
        "lastUpdated": datetime,
    },
    total=False,
)

_RequiredCreateAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssessmentRequestRequestTypeDef",
    {
        "name": str,
        "assessmentReportsDestination": AssessmentReportsDestinationTypeDef,
        "scope": ScopeTypeDef,
        "roles": Sequence[RoleTypeDef],
        "frameworkId": str,
    },
)
_OptionalCreateAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssessmentRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssessmentRequestRequestTypeDef(
    _RequiredCreateAssessmentRequestRequestTypeDef, _OptionalCreateAssessmentRequestRequestTypeDef
):
    pass


_RequiredUpdateAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssessmentRequestRequestTypeDef",
    {
        "assessmentId": str,
        "scope": ScopeTypeDef,
    },
)
_OptionalUpdateAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssessmentRequestRequestTypeDef",
    {
        "assessmentName": str,
        "assessmentDescription": str,
        "assessmentReportsDestination": AssessmentReportsDestinationTypeDef,
        "roles": Sequence[RoleTypeDef],
    },
    total=False,
)


class UpdateAssessmentRequestRequestTypeDef(
    _RequiredUpdateAssessmentRequestRequestTypeDef, _OptionalUpdateAssessmentRequestRequestTypeDef
):
    pass


ListAssessmentsResponseTypeDef = TypedDict(
    "ListAssessmentsResponseTypeDef",
    {
        "assessmentMetadata": List[AssessmentMetadataItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssessmentControlSetTypeDef = TypedDict(
    "AssessmentControlSetTypeDef",
    {
        "id": str,
        "description": str,
        "status": ControlSetStatusType,
        "roles": List[RoleTypeDef],
        "controls": List[AssessmentControlTypeDef],
        "delegations": List[DelegationTypeDef],
        "systemEvidenceCount": int,
        "manualEvidenceCount": int,
    },
    total=False,
)

UpdateAssessmentControlResponseTypeDef = TypedDict(
    "UpdateAssessmentControlResponseTypeDef",
    {
        "control": AssessmentControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSettingsResponseTypeDef = TypedDict(
    "GetSettingsResponseTypeDef",
    {
        "settings": SettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSettingsResponseTypeDef = TypedDict(
    "UpdateSettingsResponseTypeDef",
    {
        "settings": SettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchCreateDelegationByAssessmentResponseTypeDef = TypedDict(
    "BatchCreateDelegationByAssessmentResponseTypeDef",
    {
        "delegations": List[DelegationTypeDef],
        "errors": List[BatchCreateDelegationByAssessmentErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchImportEvidenceToAssessmentControlResponseTypeDef = TypedDict(
    "BatchImportEvidenceToAssessmentControlResponseTypeDef",
    {
        "errors": List[BatchImportEvidenceToAssessmentControlErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListControlDomainInsightsByAssessmentResponseTypeDef = TypedDict(
    "ListControlDomainInsightsByAssessmentResponseTypeDef",
    {
        "controlDomainInsights": List[ControlDomainInsightsTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListControlDomainInsightsResponseTypeDef = TypedDict(
    "ListControlDomainInsightsResponseTypeDef",
    {
        "controlDomainInsights": List[ControlDomainInsightsTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssessmentControlInsightsByControlDomainResponseTypeDef = TypedDict(
    "ListAssessmentControlInsightsByControlDomainResponseTypeDef",
    {
        "controlInsightsByAssessment": List[ControlInsightsMetadataByAssessmentItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListControlInsightsByControlDomainResponseTypeDef = TypedDict(
    "ListControlInsightsByControlDomainResponseTypeDef",
    {
        "controlInsightsMetadata": List[ControlInsightsMetadataItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ControlTypeDef = TypedDict(
    "ControlTypeDef",
    {
        "arn": str,
        "id": str,
        "type": ControlTypeType,
        "name": str,
        "description": str,
        "testingInformation": str,
        "actionPlanTitle": str,
        "actionPlanInstructions": str,
        "controlSources": str,
        "controlMappingSources": List[ControlMappingSourceTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "createdBy": str,
        "lastUpdatedBy": str,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredUpdateControlRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateControlRequestRequestTypeDef",
    {
        "controlId": str,
        "name": str,
        "controlMappingSources": Sequence[ControlMappingSourceTypeDef],
    },
)
_OptionalUpdateControlRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateControlRequestRequestTypeDef",
    {
        "description": str,
        "testingInformation": str,
        "actionPlanTitle": str,
        "actionPlanInstructions": str,
    },
    total=False,
)


class UpdateControlRequestRequestTypeDef(
    _RequiredUpdateControlRequestRequestTypeDef, _OptionalUpdateControlRequestRequestTypeDef
):
    pass


_RequiredCreateControlRequestRequestTypeDef = TypedDict(
    "_RequiredCreateControlRequestRequestTypeDef",
    {
        "name": str,
        "controlMappingSources": Sequence[CreateControlMappingSourceTypeDef],
    },
)
_OptionalCreateControlRequestRequestTypeDef = TypedDict(
    "_OptionalCreateControlRequestRequestTypeDef",
    {
        "description": str,
        "testingInformation": str,
        "actionPlanTitle": str,
        "actionPlanInstructions": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateControlRequestRequestTypeDef(
    _RequiredCreateControlRequestRequestTypeDef, _OptionalCreateControlRequestRequestTypeDef
):
    pass


_RequiredCreateAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssessmentFrameworkRequestRequestTypeDef",
    {
        "name": str,
        "controlSets": Sequence[CreateAssessmentFrameworkControlSetTypeDef],
    },
)
_OptionalCreateAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssessmentFrameworkRequestRequestTypeDef",
    {
        "description": str,
        "complianceType": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssessmentFrameworkRequestRequestTypeDef(
    _RequiredCreateAssessmentFrameworkRequestRequestTypeDef,
    _OptionalCreateAssessmentFrameworkRequestRequestTypeDef,
):
    pass


_RequiredUpdateAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssessmentFrameworkRequestRequestTypeDef",
    {
        "frameworkId": str,
        "name": str,
        "controlSets": Sequence[UpdateAssessmentFrameworkControlSetTypeDef],
    },
)
_OptionalUpdateAssessmentFrameworkRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssessmentFrameworkRequestRequestTypeDef",
    {
        "description": str,
        "complianceType": str,
    },
    total=False,
)


class UpdateAssessmentFrameworkRequestRequestTypeDef(
    _RequiredUpdateAssessmentFrameworkRequestRequestTypeDef,
    _OptionalUpdateAssessmentFrameworkRequestRequestTypeDef,
):
    pass


GetEvidenceByEvidenceFolderResponseTypeDef = TypedDict(
    "GetEvidenceByEvidenceFolderResponseTypeDef",
    {
        "evidence": List[EvidenceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEvidenceResponseTypeDef = TypedDict(
    "GetEvidenceResponseTypeDef",
    {
        "evidence": EvidenceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssessmentFrameworkTypeDef = TypedDict(
    "AssessmentFrameworkTypeDef",
    {
        "id": str,
        "arn": str,
        "metadata": FrameworkMetadataTypeDef,
        "controlSets": List[AssessmentControlSetTypeDef],
    },
    total=False,
)

UpdateAssessmentControlSetStatusResponseTypeDef = TypedDict(
    "UpdateAssessmentControlSetStatusResponseTypeDef",
    {
        "controlSet": AssessmentControlSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ControlSetTypeDef = TypedDict(
    "ControlSetTypeDef",
    {
        "id": str,
        "name": str,
        "controls": List[ControlTypeDef],
    },
    total=False,
)

CreateControlResponseTypeDef = TypedDict(
    "CreateControlResponseTypeDef",
    {
        "control": ControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetControlResponseTypeDef = TypedDict(
    "GetControlResponseTypeDef",
    {
        "control": ControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateControlResponseTypeDef = TypedDict(
    "UpdateControlResponseTypeDef",
    {
        "control": ControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssessmentTypeDef = TypedDict(
    "AssessmentTypeDef",
    {
        "arn": str,
        "awsAccount": AWSAccountTypeDef,
        "metadata": AssessmentMetadataTypeDef,
        "framework": AssessmentFrameworkTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

FrameworkTypeDef = TypedDict(
    "FrameworkTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "type": FrameworkTypeType,
        "complianceType": str,
        "description": str,
        "logo": str,
        "controlSources": str,
        "controlSets": List[ControlSetTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "createdBy": str,
        "lastUpdatedBy": str,
        "tags": Dict[str, str],
    },
    total=False,
)

CreateAssessmentResponseTypeDef = TypedDict(
    "CreateAssessmentResponseTypeDef",
    {
        "assessment": AssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssessmentResponseTypeDef = TypedDict(
    "GetAssessmentResponseTypeDef",
    {
        "assessment": AssessmentTypeDef,
        "userRole": RoleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssessmentResponseTypeDef = TypedDict(
    "UpdateAssessmentResponseTypeDef",
    {
        "assessment": AssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssessmentStatusResponseTypeDef = TypedDict(
    "UpdateAssessmentStatusResponseTypeDef",
    {
        "assessment": AssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssessmentFrameworkResponseTypeDef = TypedDict(
    "CreateAssessmentFrameworkResponseTypeDef",
    {
        "framework": FrameworkTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssessmentFrameworkResponseTypeDef = TypedDict(
    "GetAssessmentFrameworkResponseTypeDef",
    {
        "framework": FrameworkTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssessmentFrameworkResponseTypeDef = TypedDict(
    "UpdateAssessmentFrameworkResponseTypeDef",
    {
        "framework": FrameworkTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
