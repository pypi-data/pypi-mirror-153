"""
Type annotations for auditmanager service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_auditmanager.client import AuditManagerClient

    session = Session()
    client: AuditManagerClient = session.client("auditmanager")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AssessmentStatusType,
    ControlSetStatusType,
    ControlStatusType,
    ControlTypeType,
    FrameworkTypeType,
    SettingAttributeType,
    ShareRequestActionType,
    ShareRequestTypeType,
    SourceTypeType,
)
from .type_defs import (
    AssessmentReportsDestinationTypeDef,
    BatchAssociateAssessmentReportEvidenceResponseTypeDef,
    BatchCreateDelegationByAssessmentResponseTypeDef,
    BatchDeleteDelegationByAssessmentResponseTypeDef,
    BatchDisassociateAssessmentReportEvidenceResponseTypeDef,
    BatchImportEvidenceToAssessmentControlResponseTypeDef,
    ControlMappingSourceTypeDef,
    CreateAssessmentFrameworkControlSetTypeDef,
    CreateAssessmentFrameworkResponseTypeDef,
    CreateAssessmentReportResponseTypeDef,
    CreateAssessmentResponseTypeDef,
    CreateControlMappingSourceTypeDef,
    CreateControlResponseTypeDef,
    CreateDelegationRequestTypeDef,
    DeregisterAccountResponseTypeDef,
    GetAccountStatusResponseTypeDef,
    GetAssessmentFrameworkResponseTypeDef,
    GetAssessmentReportUrlResponseTypeDef,
    GetAssessmentResponseTypeDef,
    GetChangeLogsResponseTypeDef,
    GetControlResponseTypeDef,
    GetDelegationsResponseTypeDef,
    GetEvidenceByEvidenceFolderResponseTypeDef,
    GetEvidenceFolderResponseTypeDef,
    GetEvidenceFoldersByAssessmentControlResponseTypeDef,
    GetEvidenceFoldersByAssessmentResponseTypeDef,
    GetEvidenceResponseTypeDef,
    GetInsightsByAssessmentResponseTypeDef,
    GetInsightsResponseTypeDef,
    GetOrganizationAdminAccountResponseTypeDef,
    GetServicesInScopeResponseTypeDef,
    GetSettingsResponseTypeDef,
    ListAssessmentControlInsightsByControlDomainResponseTypeDef,
    ListAssessmentFrameworkShareRequestsResponseTypeDef,
    ListAssessmentFrameworksResponseTypeDef,
    ListAssessmentReportsResponseTypeDef,
    ListAssessmentsResponseTypeDef,
    ListControlDomainInsightsByAssessmentResponseTypeDef,
    ListControlDomainInsightsResponseTypeDef,
    ListControlInsightsByControlDomainResponseTypeDef,
    ListControlsResponseTypeDef,
    ListKeywordsForDataSourceResponseTypeDef,
    ListNotificationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ManualEvidenceTypeDef,
    RegisterAccountResponseTypeDef,
    RegisterOrganizationAdminAccountResponseTypeDef,
    RoleTypeDef,
    ScopeTypeDef,
    StartAssessmentFrameworkShareResponseTypeDef,
    UpdateAssessmentControlResponseTypeDef,
    UpdateAssessmentControlSetStatusResponseTypeDef,
    UpdateAssessmentFrameworkControlSetTypeDef,
    UpdateAssessmentFrameworkResponseTypeDef,
    UpdateAssessmentFrameworkShareResponseTypeDef,
    UpdateAssessmentResponseTypeDef,
    UpdateAssessmentStatusResponseTypeDef,
    UpdateControlResponseTypeDef,
    UpdateSettingsResponseTypeDef,
    ValidateAssessmentReportIntegrityResponseTypeDef,
)

__all__ = ("AuditManagerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AuditManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AuditManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#exceptions)
        """

    def associate_assessment_report_evidence_folder(
        self, *, assessmentId: str, evidenceFolderId: str
    ) -> Dict[str, Any]:
        """
        Associates an evidence folder to an assessment report in a Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.associate_assessment_report_evidence_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#associate_assessment_report_evidence_folder)
        """

    def batch_associate_assessment_report_evidence(
        self, *, assessmentId: str, evidenceFolderId: str, evidenceIds: Sequence[str]
    ) -> BatchAssociateAssessmentReportEvidenceResponseTypeDef:
        """
        Associates a list of evidence to an assessment report in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.batch_associate_assessment_report_evidence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#batch_associate_assessment_report_evidence)
        """

    def batch_create_delegation_by_assessment(
        self,
        *,
        createDelegationRequests: Sequence[CreateDelegationRequestTypeDef],
        assessmentId: str
    ) -> BatchCreateDelegationByAssessmentResponseTypeDef:
        """
        Creates a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.batch_create_delegation_by_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#batch_create_delegation_by_assessment)
        """

    def batch_delete_delegation_by_assessment(
        self, *, delegationIds: Sequence[str], assessmentId: str
    ) -> BatchDeleteDelegationByAssessmentResponseTypeDef:
        """
        Deletes a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.batch_delete_delegation_by_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#batch_delete_delegation_by_assessment)
        """

    def batch_disassociate_assessment_report_evidence(
        self, *, assessmentId: str, evidenceFolderId: str, evidenceIds: Sequence[str]
    ) -> BatchDisassociateAssessmentReportEvidenceResponseTypeDef:
        """
        Disassociates a list of evidence from an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.batch_disassociate_assessment_report_evidence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#batch_disassociate_assessment_report_evidence)
        """

    def batch_import_evidence_to_assessment_control(
        self,
        *,
        assessmentId: str,
        controlSetId: str,
        controlId: str,
        manualEvidence: Sequence[ManualEvidenceTypeDef]
    ) -> BatchImportEvidenceToAssessmentControlResponseTypeDef:
        """
        Uploads one or more pieces of evidence to a control in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.batch_import_evidence_to_assessment_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#batch_import_evidence_to_assessment_control)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#can_paginate)
        """

    def create_assessment(
        self,
        *,
        name: str,
        assessmentReportsDestination: AssessmentReportsDestinationTypeDef,
        scope: ScopeTypeDef,
        roles: Sequence[RoleTypeDef],
        frameworkId: str,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAssessmentResponseTypeDef:
        """
        Creates an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.create_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#create_assessment)
        """

    def create_assessment_framework(
        self,
        *,
        name: str,
        controlSets: Sequence[CreateAssessmentFrameworkControlSetTypeDef],
        description: str = ...,
        complianceType: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAssessmentFrameworkResponseTypeDef:
        """
        Creates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.create_assessment_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#create_assessment_framework)
        """

    def create_assessment_report(
        self, *, name: str, assessmentId: str, description: str = ...
    ) -> CreateAssessmentReportResponseTypeDef:
        """
        Creates an assessment report for the specified assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.create_assessment_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#create_assessment_report)
        """

    def create_control(
        self,
        *,
        name: str,
        controlMappingSources: Sequence[CreateControlMappingSourceTypeDef],
        description: str = ...,
        testingInformation: str = ...,
        actionPlanTitle: str = ...,
        actionPlanInstructions: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateControlResponseTypeDef:
        """
        Creates a new custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.create_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#create_control)
        """

    def delete_assessment(self, *, assessmentId: str) -> Dict[str, Any]:
        """
        Deletes an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.delete_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#delete_assessment)
        """

    def delete_assessment_framework(self, *, frameworkId: str) -> Dict[str, Any]:
        """
        Deletes a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.delete_assessment_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#delete_assessment_framework)
        """

    def delete_assessment_framework_share(
        self, *, requestId: str, requestType: ShareRequestTypeType
    ) -> Dict[str, Any]:
        """
        Deletes a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.delete_assessment_framework_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#delete_assessment_framework_share)
        """

    def delete_assessment_report(
        self, *, assessmentId: str, assessmentReportId: str
    ) -> Dict[str, Any]:
        """
        Deletes an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.delete_assessment_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#delete_assessment_report)
        """

    def delete_control(self, *, controlId: str) -> Dict[str, Any]:
        """
        Deletes a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.delete_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#delete_control)
        """

    def deregister_account(self) -> DeregisterAccountResponseTypeDef:
        """
        Deregisters an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.deregister_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#deregister_account)
        """

    def deregister_organization_admin_account(self, *, adminAccountId: str = ...) -> Dict[str, Any]:
        """
        Removes the specified Amazon Web Services account as a delegated administrator
        for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.deregister_organization_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#deregister_organization_admin_account)
        """

    def disassociate_assessment_report_evidence_folder(
        self, *, assessmentId: str, evidenceFolderId: str
    ) -> Dict[str, Any]:
        """
        Disassociates an evidence folder from the specified assessment report in Audit
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.disassociate_assessment_report_evidence_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#disassociate_assessment_report_evidence_folder)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#generate_presigned_url)
        """

    def get_account_status(self) -> GetAccountStatusResponseTypeDef:
        """
        Returns the registration status of an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_account_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_account_status)
        """

    def get_assessment(self, *, assessmentId: str) -> GetAssessmentResponseTypeDef:
        """
        Returns an assessment from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_assessment)
        """

    def get_assessment_framework(
        self, *, frameworkId: str
    ) -> GetAssessmentFrameworkResponseTypeDef:
        """
        Returns a framework from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_assessment_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_assessment_framework)
        """

    def get_assessment_report_url(
        self, *, assessmentReportId: str, assessmentId: str
    ) -> GetAssessmentReportUrlResponseTypeDef:
        """
        Returns the URL of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_assessment_report_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_assessment_report_url)
        """

    def get_change_logs(
        self,
        *,
        assessmentId: str,
        controlSetId: str = ...,
        controlId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetChangeLogsResponseTypeDef:
        """
        Returns a list of changelogs from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_change_logs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_change_logs)
        """

    def get_control(self, *, controlId: str) -> GetControlResponseTypeDef:
        """
        Returns a control from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_control)
        """

    def get_delegations(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> GetDelegationsResponseTypeDef:
        """
        Returns a list of delegations from an audit owner to a delegate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_delegations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_delegations)
        """

    def get_evidence(
        self, *, assessmentId: str, controlSetId: str, evidenceFolderId: str, evidenceId: str
    ) -> GetEvidenceResponseTypeDef:
        """
        Returns evidence from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_evidence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_evidence)
        """

    def get_evidence_by_evidence_folder(
        self,
        *,
        assessmentId: str,
        controlSetId: str,
        evidenceFolderId: str,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetEvidenceByEvidenceFolderResponseTypeDef:
        """
        Returns all evidence from a specified evidence folder in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_evidence_by_evidence_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_evidence_by_evidence_folder)
        """

    def get_evidence_folder(
        self, *, assessmentId: str, controlSetId: str, evidenceFolderId: str
    ) -> GetEvidenceFolderResponseTypeDef:
        """
        Returns an evidence folder from the specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_evidence_folder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_evidence_folder)
        """

    def get_evidence_folders_by_assessment(
        self, *, assessmentId: str, nextToken: str = ..., maxResults: int = ...
    ) -> GetEvidenceFoldersByAssessmentResponseTypeDef:
        """
        Returns the evidence folders from a specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_evidence_folders_by_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_evidence_folders_by_assessment)
        """

    def get_evidence_folders_by_assessment_control(
        self,
        *,
        assessmentId: str,
        controlSetId: str,
        controlId: str,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetEvidenceFoldersByAssessmentControlResponseTypeDef:
        """
        Returns a list of evidence folders that are associated with a specified control
        of an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_evidence_folders_by_assessment_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_evidence_folders_by_assessment_control)
        """

    def get_insights(self) -> GetInsightsResponseTypeDef:
        """
        Gets the latest analytics data for all your current active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_insights)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_insights)
        """

    def get_insights_by_assessment(
        self, *, assessmentId: str
    ) -> GetInsightsByAssessmentResponseTypeDef:
        """
        Gets the latest analytics data for a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_insights_by_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_insights_by_assessment)
        """

    def get_organization_admin_account(self) -> GetOrganizationAdminAccountResponseTypeDef:
        """
        Returns the name of the delegated Amazon Web Services administrator account for
        the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_organization_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_organization_admin_account)
        """

    def get_services_in_scope(self) -> GetServicesInScopeResponseTypeDef:
        """
        Returns a list of the in-scope Amazon Web Services services for the specified
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_services_in_scope)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_services_in_scope)
        """

    def get_settings(self, *, attribute: SettingAttributeType) -> GetSettingsResponseTypeDef:
        """
        Returns the settings for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.get_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#get_settings)
        """

    def list_assessment_control_insights_by_control_domain(
        self,
        *,
        controlDomainId: str,
        assessmentId: str,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        and a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_assessment_control_insights_by_control_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_assessment_control_insights_by_control_domain)
        """

    def list_assessment_framework_share_requests(
        self, *, requestType: ShareRequestTypeType, nextToken: str = ..., maxResults: int = ...
    ) -> ListAssessmentFrameworkShareRequestsResponseTypeDef:
        """
        Returns a list of sent or received share requests for custom frameworks in Audit
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_assessment_framework_share_requests)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_assessment_framework_share_requests)
        """

    def list_assessment_frameworks(
        self, *, frameworkType: FrameworkTypeType, nextToken: str = ..., maxResults: int = ...
    ) -> ListAssessmentFrameworksResponseTypeDef:
        """
        Returns a list of the frameworks that are available in the Audit Manager
        framework library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_assessment_frameworks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_assessment_frameworks)
        """

    def list_assessment_reports(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListAssessmentReportsResponseTypeDef:
        """
        Returns a list of assessment reports created in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_assessment_reports)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_assessment_reports)
        """

    def list_assessments(
        self, *, status: AssessmentStatusType = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListAssessmentsResponseTypeDef:
        """
        Returns a list of current and past assessments from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_assessments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_assessments)
        """

    def list_control_domain_insights(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListControlDomainInsightsResponseTypeDef:
        """
        Lists the latest analytics data for control domains across all of your active
        assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_control_domain_insights)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_control_domain_insights)
        """

    def list_control_domain_insights_by_assessment(
        self, *, assessmentId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListControlDomainInsightsByAssessmentResponseTypeDef:
        """
        Lists analytics data for control domains within a specified active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_control_domain_insights_by_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_control_domain_insights_by_assessment)
        """

    def list_control_insights_by_control_domain(
        self, *, controlDomainId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        across all active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_control_insights_by_control_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_control_insights_by_control_domain)
        """

    def list_controls(
        self, *, controlType: ControlTypeType, nextToken: str = ..., maxResults: int = ...
    ) -> ListControlsResponseTypeDef:
        """
        Returns a list of controls from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_controls)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_controls)
        """

    def list_keywords_for_data_source(
        self, *, source: SourceTypeType, nextToken: str = ..., maxResults: int = ...
    ) -> ListKeywordsForDataSourceResponseTypeDef:
        """
        Returns a list of keywords that are pre-mapped to the specified control data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_keywords_for_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_keywords_for_data_source)
        """

    def list_notifications(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListNotificationsResponseTypeDef:
        """
        Returns a list of all Audit Manager notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_notifications)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#list_tags_for_resource)
        """

    def register_account(
        self, *, kmsKey: str = ..., delegatedAdminAccount: str = ...
    ) -> RegisterAccountResponseTypeDef:
        """
        Enables Audit Manager for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.register_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#register_account)
        """

    def register_organization_admin_account(
        self, *, adminAccountId: str
    ) -> RegisterOrganizationAdminAccountResponseTypeDef:
        """
        Enables an Amazon Web Services account within the organization as the delegated
        administrator for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.register_organization_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#register_organization_admin_account)
        """

    def start_assessment_framework_share(
        self,
        *,
        frameworkId: str,
        destinationAccount: str,
        destinationRegion: str,
        comment: str = ...
    ) -> StartAssessmentFrameworkShareResponseTypeDef:
        """
        Creates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.start_assessment_framework_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#start_assessment_framework_share)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#untag_resource)
        """

    def update_assessment(
        self,
        *,
        assessmentId: str,
        scope: ScopeTypeDef,
        assessmentName: str = ...,
        assessmentDescription: str = ...,
        assessmentReportsDestination: AssessmentReportsDestinationTypeDef = ...,
        roles: Sequence[RoleTypeDef] = ...
    ) -> UpdateAssessmentResponseTypeDef:
        """
        Edits an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment)
        """

    def update_assessment_control(
        self,
        *,
        assessmentId: str,
        controlSetId: str,
        controlId: str,
        controlStatus: ControlStatusType = ...,
        commentBody: str = ...
    ) -> UpdateAssessmentControlResponseTypeDef:
        """
        Updates a control within an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment_control)
        """

    def update_assessment_control_set_status(
        self, *, assessmentId: str, controlSetId: str, status: ControlSetStatusType, comment: str
    ) -> UpdateAssessmentControlSetStatusResponseTypeDef:
        """
        Updates the status of a control set in an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment_control_set_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment_control_set_status)
        """

    def update_assessment_framework(
        self,
        *,
        frameworkId: str,
        name: str,
        controlSets: Sequence[UpdateAssessmentFrameworkControlSetTypeDef],
        description: str = ...,
        complianceType: str = ...
    ) -> UpdateAssessmentFrameworkResponseTypeDef:
        """
        Updates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment_framework)
        """

    def update_assessment_framework_share(
        self, *, requestId: str, requestType: ShareRequestTypeType, action: ShareRequestActionType
    ) -> UpdateAssessmentFrameworkShareResponseTypeDef:
        """
        Updates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment_framework_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment_framework_share)
        """

    def update_assessment_status(
        self, *, assessmentId: str, status: AssessmentStatusType
    ) -> UpdateAssessmentStatusResponseTypeDef:
        """
        Updates the status of an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_assessment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_assessment_status)
        """

    def update_control(
        self,
        *,
        controlId: str,
        name: str,
        controlMappingSources: Sequence[ControlMappingSourceTypeDef],
        description: str = ...,
        testingInformation: str = ...,
        actionPlanTitle: str = ...,
        actionPlanInstructions: str = ...
    ) -> UpdateControlResponseTypeDef:
        """
        Updates a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_control)
        """

    def update_settings(
        self,
        *,
        snsTopic: str = ...,
        defaultAssessmentReportsDestination: AssessmentReportsDestinationTypeDef = ...,
        defaultProcessOwners: Sequence[RoleTypeDef] = ...,
        kmsKey: str = ...
    ) -> UpdateSettingsResponseTypeDef:
        """
        Updates Audit Manager settings for the current user account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.update_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#update_settings)
        """

    def validate_assessment_report_integrity(
        self, *, s3RelativePath: str
    ) -> ValidateAssessmentReportIntegrityResponseTypeDef:
        """
        Validates the integrity of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client.validate_assessment_report_integrity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_auditmanager/client/#validate_assessment_report_integrity)
        """
