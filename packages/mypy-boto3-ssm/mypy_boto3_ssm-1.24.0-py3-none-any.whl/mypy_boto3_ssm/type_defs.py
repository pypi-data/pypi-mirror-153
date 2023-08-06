"""
Type annotations for ssm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm.type_defs import AccountSharingInfoTypeDef

    data: AccountSharingInfoTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AssociationComplianceSeverityType,
    AssociationExecutionFilterKeyType,
    AssociationExecutionTargetsFilterKeyType,
    AssociationFilterKeyType,
    AssociationFilterOperatorTypeType,
    AssociationStatusNameType,
    AssociationSyncComplianceType,
    AttachmentsSourceKeyType,
    AutomationExecutionFilterKeyType,
    AutomationExecutionStatusType,
    AutomationTypeType,
    CalendarStateType,
    CommandFilterKeyType,
    CommandInvocationStatusType,
    CommandPluginStatusType,
    CommandStatusType,
    ComplianceQueryOperatorTypeType,
    ComplianceSeverityType,
    ComplianceStatusType,
    ComplianceUploadTypeType,
    ConnectionStatusType,
    DescribeActivationsFilterKeysType,
    DocumentFilterKeyType,
    DocumentFormatType,
    DocumentHashTypeType,
    DocumentParameterTypeType,
    DocumentReviewActionType,
    DocumentStatusType,
    DocumentTypeType,
    ExecutionModeType,
    FaultType,
    InstanceInformationFilterKeyType,
    InstancePatchStateOperatorTypeType,
    InventoryAttributeDataTypeType,
    InventoryDeletionStatusType,
    InventoryQueryOperatorTypeType,
    InventorySchemaDeleteOptionType,
    LastResourceDataSyncStatusType,
    MaintenanceWindowExecutionStatusType,
    MaintenanceWindowResourceTypeType,
    MaintenanceWindowTaskCutoffBehaviorType,
    MaintenanceWindowTaskTypeType,
    NotificationEventType,
    NotificationTypeType,
    OperatingSystemType,
    OpsFilterOperatorTypeType,
    OpsItemDataTypeType,
    OpsItemFilterKeyType,
    OpsItemFilterOperatorType,
    OpsItemRelatedItemsFilterKeyType,
    OpsItemStatusType,
    ParametersFilterKeyType,
    ParameterTierType,
    ParameterTypeType,
    PatchActionType,
    PatchComplianceDataStateType,
    PatchComplianceLevelType,
    PatchDeploymentStatusType,
    PatchFilterKeyType,
    PatchOperationTypeType,
    PatchPropertyType,
    PatchSetType,
    PingStatusType,
    PlatformTypeType,
    RebootOptionType,
    ResourceTypeForTaggingType,
    ResourceTypeType,
    ReviewStatusType,
    SessionFilterKeyType,
    SessionStateType,
    SessionStatusType,
    SignalTypeType,
    SourceTypeType,
    StepExecutionFilterKeyType,
    StopTypeType,
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
    "AccountSharingInfoTypeDef",
    "TagTypeDef",
    "AssociateOpsItemRelatedItemRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociationOverviewTypeDef",
    "AssociationStatusTypeDef",
    "TargetLocationTypeDef",
    "TargetTypeDef",
    "AssociationExecutionFilterTypeDef",
    "OutputSourceTypeDef",
    "AssociationExecutionTargetsFilterTypeDef",
    "AssociationExecutionTypeDef",
    "AssociationFilterTypeDef",
    "AttachmentContentTypeDef",
    "AttachmentInformationTypeDef",
    "AttachmentsSourceTypeDef",
    "AutomationExecutionFilterTypeDef",
    "ResolvedTargetsTypeDef",
    "ProgressCountersTypeDef",
    "PatchSourceTypeDef",
    "CancelCommandRequestRequestTypeDef",
    "CancelMaintenanceWindowExecutionRequestRequestTypeDef",
    "CloudWatchOutputConfigTypeDef",
    "CommandFilterTypeDef",
    "CommandPluginTypeDef",
    "NotificationConfigTypeDef",
    "ComplianceExecutionSummaryTypeDef",
    "ComplianceItemEntryTypeDef",
    "ComplianceStringFilterTypeDef",
    "SeveritySummaryTypeDef",
    "RegistrationMetadataItemTypeDef",
    "DocumentRequiresTypeDef",
    "OpsItemDataValueTypeDef",
    "OpsItemNotificationTypeDef",
    "RelatedOpsItemTypeDef",
    "MetadataValueTypeDef",
    "DeleteActivationRequestRequestTypeDef",
    "DeleteAssociationRequestRequestTypeDef",
    "DeleteDocumentRequestRequestTypeDef",
    "DeleteInventoryRequestRequestTypeDef",
    "DeleteMaintenanceWindowRequestRequestTypeDef",
    "DeleteOpsMetadataRequestRequestTypeDef",
    "DeleteParameterRequestRequestTypeDef",
    "DeleteParametersRequestRequestTypeDef",
    "DeletePatchBaselineRequestRequestTypeDef",
    "DeleteResourceDataSyncRequestRequestTypeDef",
    "DeregisterManagedInstanceRequestRequestTypeDef",
    "DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    "DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef",
    "DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef",
    "DescribeActivationsFilterTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAssociationRequestRequestTypeDef",
    "StepExecutionFilterTypeDef",
    "PatchOrchestratorFilterTypeDef",
    "PatchTypeDef",
    "DescribeDocumentPermissionRequestRequestTypeDef",
    "DescribeDocumentRequestRequestTypeDef",
    "DescribeEffectiveInstanceAssociationsRequestRequestTypeDef",
    "InstanceAssociationTypeDef",
    "DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef",
    "DescribeInstanceAssociationsStatusRequestRequestTypeDef",
    "InstanceInformationFilterTypeDef",
    "InstanceInformationStringFilterTypeDef",
    "InstancePatchStateFilterTypeDef",
    "InstancePatchStateTypeDef",
    "DescribeInstancePatchStatesRequestRequestTypeDef",
    "PatchComplianceDataTypeDef",
    "DescribeInventoryDeletionsRequestRequestTypeDef",
    "MaintenanceWindowFilterTypeDef",
    "MaintenanceWindowExecutionTaskInvocationIdentityTypeDef",
    "MaintenanceWindowExecutionTaskIdentityTypeDef",
    "MaintenanceWindowExecutionTypeDef",
    "ScheduledWindowExecutionTypeDef",
    "MaintenanceWindowIdentityForTargetTypeDef",
    "MaintenanceWindowIdentityTypeDef",
    "OpsItemFilterTypeDef",
    "ParameterStringFilterTypeDef",
    "ParametersFilterTypeDef",
    "PatchBaselineIdentityTypeDef",
    "DescribePatchGroupStateRequestRequestTypeDef",
    "DescribePatchPropertiesRequestRequestTypeDef",
    "SessionFilterTypeDef",
    "DisassociateOpsItemRelatedItemRequestRequestTypeDef",
    "DocumentDefaultVersionDescriptionTypeDef",
    "DocumentParameterTypeDef",
    "ReviewInformationTypeDef",
    "DocumentFilterTypeDef",
    "DocumentKeyValuesFilterTypeDef",
    "DocumentReviewCommentSourceTypeDef",
    "DocumentVersionInfoTypeDef",
    "PatchStatusTypeDef",
    "FailureDetailsTypeDef",
    "GetAutomationExecutionRequestRequestTypeDef",
    "GetCalendarStateRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetCommandInvocationRequestRequestTypeDef",
    "GetConnectionStatusRequestRequestTypeDef",
    "GetDefaultPatchBaselineRequestRequestTypeDef",
    "GetDocumentRequestRequestTypeDef",
    "InventoryFilterTypeDef",
    "ResultAttributeTypeDef",
    "GetInventorySchemaRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionTaskRequestRequestTypeDef",
    "MaintenanceWindowTaskParameterValueExpressionTypeDef",
    "GetMaintenanceWindowRequestRequestTypeDef",
    "GetMaintenanceWindowTaskRequestRequestTypeDef",
    "LoggingInfoTypeDef",
    "GetOpsItemRequestRequestTypeDef",
    "GetOpsMetadataRequestRequestTypeDef",
    "OpsFilterTypeDef",
    "OpsResultAttributeTypeDef",
    "GetParameterHistoryRequestRequestTypeDef",
    "GetParameterRequestRequestTypeDef",
    "ParameterTypeDef",
    "GetParametersRequestRequestTypeDef",
    "GetPatchBaselineForPatchGroupRequestRequestTypeDef",
    "GetPatchBaselineRequestRequestTypeDef",
    "GetServiceSettingRequestRequestTypeDef",
    "ServiceSettingTypeDef",
    "InstanceAggregatedAssociationOverviewTypeDef",
    "S3OutputLocationTypeDef",
    "S3OutputUrlTypeDef",
    "InventoryDeletionSummaryItemTypeDef",
    "InventoryItemAttributeTypeDef",
    "InventoryItemTypeDef",
    "InventoryResultItemTypeDef",
    "LabelParameterVersionRequestRequestTypeDef",
    "ListAssociationVersionsRequestRequestTypeDef",
    "ListDocumentMetadataHistoryRequestRequestTypeDef",
    "ListDocumentVersionsRequestRequestTypeDef",
    "OpsItemEventFilterTypeDef",
    "OpsItemRelatedItemsFilterTypeDef",
    "OpsMetadataFilterTypeDef",
    "OpsMetadataTypeDef",
    "ListResourceDataSyncRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MaintenanceWindowAutomationParametersTypeDef",
    "MaintenanceWindowLambdaParametersTypeDef",
    "MaintenanceWindowStepFunctionsParametersTypeDef",
    "ModifyDocumentPermissionRequestRequestTypeDef",
    "OpsEntityItemTypeDef",
    "OpsItemIdentityTypeDef",
    "ParameterInlinePolicyTypeDef",
    "PatchFilterTypeDef",
    "RegisterDefaultPatchBaselineRequestRequestTypeDef",
    "RegisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "ResetServiceSettingRequestRequestTypeDef",
    "ResourceDataSyncOrganizationalUnitTypeDef",
    "ResourceDataSyncDestinationDataSharingTypeDef",
    "ResumeSessionRequestRequestTypeDef",
    "SendAutomationSignalRequestRequestTypeDef",
    "SessionManagerOutputUrlTypeDef",
    "StartAssociationsOnceRequestRequestTypeDef",
    "StartSessionRequestRequestTypeDef",
    "StopAutomationExecutionRequestRequestTypeDef",
    "TerminateSessionRequestRequestTypeDef",
    "UnlabelParameterVersionRequestRequestTypeDef",
    "UpdateDocumentDefaultVersionRequestRequestTypeDef",
    "UpdateMaintenanceWindowRequestRequestTypeDef",
    "UpdateManagedInstanceRoleRequestRequestTypeDef",
    "UpdateServiceSettingRequestRequestTypeDef",
    "ActivationTypeDef",
    "AddTagsToResourceRequestRequestTypeDef",
    "CreateMaintenanceWindowRequestRequestTypeDef",
    "PutParameterRequestRequestTypeDef",
    "AssociateOpsItemRelatedItemResponseTypeDef",
    "CancelMaintenanceWindowExecutionResultTypeDef",
    "CreateActivationResultTypeDef",
    "CreateMaintenanceWindowResultTypeDef",
    "CreateOpsItemResponseTypeDef",
    "CreateOpsMetadataResultTypeDef",
    "CreatePatchBaselineResultTypeDef",
    "DeleteMaintenanceWindowResultTypeDef",
    "DeleteParametersResultTypeDef",
    "DeletePatchBaselineResultTypeDef",
    "DeregisterPatchBaselineForPatchGroupResultTypeDef",
    "DeregisterTargetFromMaintenanceWindowResultTypeDef",
    "DeregisterTaskFromMaintenanceWindowResultTypeDef",
    "DescribeDocumentPermissionResponseTypeDef",
    "DescribePatchGroupStateResultTypeDef",
    "DescribePatchPropertiesResultTypeDef",
    "GetCalendarStateResponseTypeDef",
    "GetConnectionStatusResponseTypeDef",
    "GetDefaultPatchBaselineResultTypeDef",
    "GetDeployablePatchSnapshotForInstanceResultTypeDef",
    "GetMaintenanceWindowExecutionResultTypeDef",
    "GetMaintenanceWindowExecutionTaskInvocationResultTypeDef",
    "GetMaintenanceWindowResultTypeDef",
    "GetPatchBaselineForPatchGroupResultTypeDef",
    "LabelParameterVersionResultTypeDef",
    "ListInventoryEntriesResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "PutInventoryResultTypeDef",
    "PutParameterResultTypeDef",
    "RegisterDefaultPatchBaselineResultTypeDef",
    "RegisterPatchBaselineForPatchGroupResultTypeDef",
    "RegisterTargetWithMaintenanceWindowResultTypeDef",
    "RegisterTaskWithMaintenanceWindowResultTypeDef",
    "ResumeSessionResponseTypeDef",
    "StartAutomationExecutionResultTypeDef",
    "StartChangeRequestExecutionResultTypeDef",
    "StartSessionResponseTypeDef",
    "TerminateSessionResponseTypeDef",
    "UnlabelParameterVersionResultTypeDef",
    "UpdateMaintenanceWindowResultTypeDef",
    "UpdateOpsMetadataResultTypeDef",
    "UpdateAssociationStatusRequestRequestTypeDef",
    "AssociationTypeDef",
    "DescribeMaintenanceWindowsForTargetRequestRequestTypeDef",
    "MaintenanceWindowTargetTypeDef",
    "RegisterTargetWithMaintenanceWindowRequestRequestTypeDef",
    "RunbookTypeDef",
    "StartAutomationExecutionRequestRequestTypeDef",
    "UpdateMaintenanceWindowTargetRequestRequestTypeDef",
    "UpdateMaintenanceWindowTargetResultTypeDef",
    "DescribeAssociationExecutionsRequestRequestTypeDef",
    "AssociationExecutionTargetTypeDef",
    "DescribeAssociationExecutionTargetsRequestRequestTypeDef",
    "DescribeAssociationExecutionsResultTypeDef",
    "ListAssociationsRequestRequestTypeDef",
    "UpdateDocumentRequestRequestTypeDef",
    "DescribeAutomationExecutionsRequestRequestTypeDef",
    "GetCommandInvocationResultTypeDef",
    "ListCommandInvocationsRequestRequestTypeDef",
    "ListCommandsRequestRequestTypeDef",
    "CommandInvocationTypeDef",
    "CommandTypeDef",
    "MaintenanceWindowRunCommandParametersTypeDef",
    "SendCommandRequestRequestTypeDef",
    "ComplianceItemTypeDef",
    "PutComplianceItemsRequestRequestTypeDef",
    "ListComplianceItemsRequestRequestTypeDef",
    "ListComplianceSummariesRequestRequestTypeDef",
    "ListResourceComplianceSummariesRequestRequestTypeDef",
    "CompliantSummaryTypeDef",
    "NonCompliantSummaryTypeDef",
    "CreateActivationRequestRequestTypeDef",
    "CreateDocumentRequestRequestTypeDef",
    "DocumentIdentifierTypeDef",
    "GetDocumentResultTypeDef",
    "OpsItemSummaryTypeDef",
    "CreateOpsItemRequestRequestTypeDef",
    "OpsItemTypeDef",
    "UpdateOpsItemRequestRequestTypeDef",
    "CreateOpsMetadataRequestRequestTypeDef",
    "GetOpsMetadataResultTypeDef",
    "UpdateOpsMetadataRequestRequestTypeDef",
    "DescribeActivationsRequestRequestTypeDef",
    "DescribeActivationsRequestDescribeActivationsPaginateTypeDef",
    "DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef",
    "DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef",
    "DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef",
    "DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef",
    "DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef",
    "DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef",
    "DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef",
    "DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef",
    "DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef",
    "DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef",
    "GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef",
    "GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef",
    "ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef",
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    "ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef",
    "ListCommandsRequestListCommandsPaginateTypeDef",
    "ListComplianceItemsRequestListComplianceItemsPaginateTypeDef",
    "ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef",
    "ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef",
    "ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef",
    "ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef",
    "DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef",
    "DescribeAutomationStepExecutionsRequestRequestTypeDef",
    "DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef",
    "DescribeAvailablePatchesRequestRequestTypeDef",
    "DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef",
    "DescribeInstancePatchesRequestRequestTypeDef",
    "DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef",
    "DescribeMaintenanceWindowScheduleRequestRequestTypeDef",
    "DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef",
    "DescribePatchBaselinesRequestRequestTypeDef",
    "DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef",
    "DescribePatchGroupsRequestRequestTypeDef",
    "DescribeAvailablePatchesResultTypeDef",
    "DescribeEffectiveInstanceAssociationsResultTypeDef",
    "DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef",
    "DescribeInstanceInformationRequestRequestTypeDef",
    "DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef",
    "DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef",
    "DescribeInstancePatchStatesForPatchGroupResultTypeDef",
    "DescribeInstancePatchStatesResultTypeDef",
    "DescribeInstancePatchesResultTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionsRequestRequestTypeDef",
    "DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef",
    "DescribeMaintenanceWindowTargetsRequestRequestTypeDef",
    "DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef",
    "DescribeMaintenanceWindowTasksRequestRequestTypeDef",
    "DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef",
    "DescribeMaintenanceWindowsRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef",
    "DescribeMaintenanceWindowExecutionTasksResultTypeDef",
    "DescribeMaintenanceWindowExecutionsResultTypeDef",
    "DescribeMaintenanceWindowScheduleResultTypeDef",
    "DescribeMaintenanceWindowsForTargetResultTypeDef",
    "DescribeMaintenanceWindowsResultTypeDef",
    "DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef",
    "DescribeOpsItemsRequestRequestTypeDef",
    "GetParametersByPathRequestGetParametersByPathPaginateTypeDef",
    "GetParametersByPathRequestRequestTypeDef",
    "DescribeParametersRequestDescribeParametersPaginateTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "DescribePatchBaselinesResultTypeDef",
    "PatchGroupPatchBaselineMappingTypeDef",
    "DescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    "DescribeSessionsRequestRequestTypeDef",
    "UpdateDocumentDefaultVersionResultTypeDef",
    "DocumentDescriptionTypeDef",
    "ListDocumentsRequestListDocumentsPaginateTypeDef",
    "ListDocumentsRequestRequestTypeDef",
    "DocumentReviewerResponseSourceTypeDef",
    "DocumentReviewsTypeDef",
    "ListDocumentVersionsResultTypeDef",
    "EffectivePatchTypeDef",
    "StepExecutionTypeDef",
    "GetCommandInvocationRequestCommandExecutedWaitTypeDef",
    "InventoryGroupTypeDef",
    "ListInventoryEntriesRequestRequestTypeDef",
    "GetInventoryRequestGetInventoryPaginateTypeDef",
    "GetInventoryRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionTaskResultTypeDef",
    "MaintenanceWindowTaskTypeDef",
    "OpsAggregatorTypeDef",
    "GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef",
    "GetOpsSummaryRequestRequestTypeDef",
    "GetParameterResultTypeDef",
    "GetParametersByPathResultTypeDef",
    "GetParametersResultTypeDef",
    "GetServiceSettingResultTypeDef",
    "ResetServiceSettingResultTypeDef",
    "InstanceInformationTypeDef",
    "InstanceAssociationOutputLocationTypeDef",
    "InstanceAssociationOutputUrlTypeDef",
    "InventoryDeletionSummaryTypeDef",
    "InventoryItemSchemaTypeDef",
    "PutInventoryRequestRequestTypeDef",
    "InventoryResultEntityTypeDef",
    "ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef",
    "ListOpsItemEventsRequestRequestTypeDef",
    "ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef",
    "ListOpsItemRelatedItemsRequestRequestTypeDef",
    "ListOpsMetadataRequestListOpsMetadataPaginateTypeDef",
    "ListOpsMetadataRequestRequestTypeDef",
    "ListOpsMetadataResultTypeDef",
    "OpsEntityTypeDef",
    "OpsItemEventSummaryTypeDef",
    "OpsItemRelatedItemSummaryTypeDef",
    "ParameterHistoryTypeDef",
    "ParameterMetadataTypeDef",
    "PatchFilterGroupTypeDef",
    "ResourceDataSyncAwsOrganizationsSourceTypeDef",
    "ResourceDataSyncS3DestinationTypeDef",
    "SessionTypeDef",
    "DescribeActivationsResultTypeDef",
    "ListAssociationsResultTypeDef",
    "DescribeMaintenanceWindowTargetsResultTypeDef",
    "AutomationExecutionMetadataTypeDef",
    "StartChangeRequestExecutionRequestRequestTypeDef",
    "DescribeAssociationExecutionTargetsResultTypeDef",
    "ListCommandInvocationsResultTypeDef",
    "ListCommandsResultTypeDef",
    "SendCommandResultTypeDef",
    "MaintenanceWindowTaskInvocationParametersTypeDef",
    "ListComplianceItemsResultTypeDef",
    "ComplianceSummaryItemTypeDef",
    "ResourceComplianceSummaryItemTypeDef",
    "ListDocumentsResultTypeDef",
    "DescribeOpsItemsResponseTypeDef",
    "GetOpsItemResponseTypeDef",
    "DescribePatchGroupsResultTypeDef",
    "CreateDocumentResultTypeDef",
    "DescribeDocumentResultTypeDef",
    "UpdateDocumentResultTypeDef",
    "DocumentMetadataResponseInfoTypeDef",
    "UpdateDocumentMetadataRequestRequestTypeDef",
    "DescribeEffectivePatchesForPatchBaselineResultTypeDef",
    "AutomationExecutionTypeDef",
    "DescribeAutomationStepExecutionsResultTypeDef",
    "InventoryAggregatorTypeDef",
    "DescribeMaintenanceWindowTasksResultTypeDef",
    "DescribeInstanceInformationResultTypeDef",
    "AssociationDescriptionTypeDef",
    "AssociationVersionInfoTypeDef",
    "CreateAssociationBatchRequestEntryTypeDef",
    "CreateAssociationRequestRequestTypeDef",
    "UpdateAssociationRequestRequestTypeDef",
    "InstanceAssociationStatusInfoTypeDef",
    "DeleteInventoryResultTypeDef",
    "InventoryDeletionStatusItemTypeDef",
    "GetInventorySchemaResultTypeDef",
    "GetInventoryResultTypeDef",
    "GetOpsSummaryResultTypeDef",
    "ListOpsItemEventsResponseTypeDef",
    "ListOpsItemRelatedItemsResponseTypeDef",
    "GetParameterHistoryResultTypeDef",
    "DescribeParametersResultTypeDef",
    "PatchRuleTypeDef",
    "ResourceDataSyncSourceTypeDef",
    "ResourceDataSyncSourceWithStateTypeDef",
    "DescribeSessionsResponseTypeDef",
    "DescribeAutomationExecutionsResultTypeDef",
    "GetMaintenanceWindowTaskResultTypeDef",
    "RegisterTaskWithMaintenanceWindowRequestRequestTypeDef",
    "UpdateMaintenanceWindowTaskRequestRequestTypeDef",
    "UpdateMaintenanceWindowTaskResultTypeDef",
    "ListComplianceSummariesResultTypeDef",
    "ListResourceComplianceSummariesResultTypeDef",
    "ListDocumentMetadataHistoryResponseTypeDef",
    "GetAutomationExecutionResultTypeDef",
    "CreateAssociationResultTypeDef",
    "DescribeAssociationResultTypeDef",
    "UpdateAssociationResultTypeDef",
    "UpdateAssociationStatusResultTypeDef",
    "ListAssociationVersionsResultTypeDef",
    "CreateAssociationBatchRequestRequestTypeDef",
    "FailedCreateAssociationTypeDef",
    "DescribeInstanceAssociationsStatusResultTypeDef",
    "DescribeInventoryDeletionsResultTypeDef",
    "PatchRuleGroupTypeDef",
    "CreateResourceDataSyncRequestRequestTypeDef",
    "UpdateResourceDataSyncRequestRequestTypeDef",
    "ResourceDataSyncItemTypeDef",
    "CreateAssociationBatchResultTypeDef",
    "BaselineOverrideTypeDef",
    "CreatePatchBaselineRequestRequestTypeDef",
    "GetPatchBaselineResultTypeDef",
    "UpdatePatchBaselineRequestRequestTypeDef",
    "UpdatePatchBaselineResultTypeDef",
    "ListResourceDataSyncResultTypeDef",
    "GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef",
)

AccountSharingInfoTypeDef = TypedDict(
    "AccountSharingInfoTypeDef",
    {
        "AccountId": str,
        "SharedDocumentVersion": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AssociateOpsItemRelatedItemRequestRequestTypeDef = TypedDict(
    "AssociateOpsItemRelatedItemRequestRequestTypeDef",
    {
        "OpsItemId": str,
        "AssociationType": str,
        "ResourceType": str,
        "ResourceUri": str,
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

AssociationOverviewTypeDef = TypedDict(
    "AssociationOverviewTypeDef",
    {
        "Status": str,
        "DetailedStatus": str,
        "AssociationStatusAggregatedCount": Dict[str, int],
    },
    total=False,
)

_RequiredAssociationStatusTypeDef = TypedDict(
    "_RequiredAssociationStatusTypeDef",
    {
        "Date": datetime,
        "Name": AssociationStatusNameType,
        "Message": str,
    },
)
_OptionalAssociationStatusTypeDef = TypedDict(
    "_OptionalAssociationStatusTypeDef",
    {
        "AdditionalInfo": str,
    },
    total=False,
)


class AssociationStatusTypeDef(
    _RequiredAssociationStatusTypeDef, _OptionalAssociationStatusTypeDef
):
    pass


TargetLocationTypeDef = TypedDict(
    "TargetLocationTypeDef",
    {
        "Accounts": Sequence[str],
        "Regions": Sequence[str],
        "TargetLocationMaxConcurrency": str,
        "TargetLocationMaxErrors": str,
        "ExecutionRoleName": str,
    },
    total=False,
)

TargetTypeDef = TypedDict(
    "TargetTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
    total=False,
)

AssociationExecutionFilterTypeDef = TypedDict(
    "AssociationExecutionFilterTypeDef",
    {
        "Key": AssociationExecutionFilterKeyType,
        "Value": str,
        "Type": AssociationFilterOperatorTypeType,
    },
)

OutputSourceTypeDef = TypedDict(
    "OutputSourceTypeDef",
    {
        "OutputSourceId": str,
        "OutputSourceType": str,
    },
    total=False,
)

AssociationExecutionTargetsFilterTypeDef = TypedDict(
    "AssociationExecutionTargetsFilterTypeDef",
    {
        "Key": AssociationExecutionTargetsFilterKeyType,
        "Value": str,
    },
)

AssociationExecutionTypeDef = TypedDict(
    "AssociationExecutionTypeDef",
    {
        "AssociationId": str,
        "AssociationVersion": str,
        "ExecutionId": str,
        "Status": str,
        "DetailedStatus": str,
        "CreatedTime": datetime,
        "LastExecutionDate": datetime,
        "ResourceCountByStatus": str,
    },
    total=False,
)

AssociationFilterTypeDef = TypedDict(
    "AssociationFilterTypeDef",
    {
        "key": AssociationFilterKeyType,
        "value": str,
    },
)

AttachmentContentTypeDef = TypedDict(
    "AttachmentContentTypeDef",
    {
        "Name": str,
        "Size": int,
        "Hash": str,
        "HashType": Literal["Sha256"],
        "Url": str,
    },
    total=False,
)

AttachmentInformationTypeDef = TypedDict(
    "AttachmentInformationTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AttachmentsSourceTypeDef = TypedDict(
    "AttachmentsSourceTypeDef",
    {
        "Key": AttachmentsSourceKeyType,
        "Values": Sequence[str],
        "Name": str,
    },
    total=False,
)

AutomationExecutionFilterTypeDef = TypedDict(
    "AutomationExecutionFilterTypeDef",
    {
        "Key": AutomationExecutionFilterKeyType,
        "Values": Sequence[str],
    },
)

ResolvedTargetsTypeDef = TypedDict(
    "ResolvedTargetsTypeDef",
    {
        "ParameterValues": List[str],
        "Truncated": bool,
    },
    total=False,
)

ProgressCountersTypeDef = TypedDict(
    "ProgressCountersTypeDef",
    {
        "TotalSteps": int,
        "SuccessSteps": int,
        "FailedSteps": int,
        "CancelledSteps": int,
        "TimedOutSteps": int,
    },
    total=False,
)

PatchSourceTypeDef = TypedDict(
    "PatchSourceTypeDef",
    {
        "Name": str,
        "Products": Sequence[str],
        "Configuration": str,
    },
)

_RequiredCancelCommandRequestRequestTypeDef = TypedDict(
    "_RequiredCancelCommandRequestRequestTypeDef",
    {
        "CommandId": str,
    },
)
_OptionalCancelCommandRequestRequestTypeDef = TypedDict(
    "_OptionalCancelCommandRequestRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
    total=False,
)


class CancelCommandRequestRequestTypeDef(
    _RequiredCancelCommandRequestRequestTypeDef, _OptionalCancelCommandRequestRequestTypeDef
):
    pass


CancelMaintenanceWindowExecutionRequestRequestTypeDef = TypedDict(
    "CancelMaintenanceWindowExecutionRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
    },
)

CloudWatchOutputConfigTypeDef = TypedDict(
    "CloudWatchOutputConfigTypeDef",
    {
        "CloudWatchLogGroupName": str,
        "CloudWatchOutputEnabled": bool,
    },
    total=False,
)

CommandFilterTypeDef = TypedDict(
    "CommandFilterTypeDef",
    {
        "key": CommandFilterKeyType,
        "value": str,
    },
)

CommandPluginTypeDef = TypedDict(
    "CommandPluginTypeDef",
    {
        "Name": str,
        "Status": CommandPluginStatusType,
        "StatusDetails": str,
        "ResponseCode": int,
        "ResponseStartDateTime": datetime,
        "ResponseFinishDateTime": datetime,
        "Output": str,
        "StandardOutputUrl": str,
        "StandardErrorUrl": str,
        "OutputS3Region": str,
        "OutputS3BucketName": str,
        "OutputS3KeyPrefix": str,
    },
    total=False,
)

NotificationConfigTypeDef = TypedDict(
    "NotificationConfigTypeDef",
    {
        "NotificationArn": str,
        "NotificationEvents": List[NotificationEventType],
        "NotificationType": NotificationTypeType,
    },
    total=False,
)

_RequiredComplianceExecutionSummaryTypeDef = TypedDict(
    "_RequiredComplianceExecutionSummaryTypeDef",
    {
        "ExecutionTime": datetime,
    },
)
_OptionalComplianceExecutionSummaryTypeDef = TypedDict(
    "_OptionalComplianceExecutionSummaryTypeDef",
    {
        "ExecutionId": str,
        "ExecutionType": str,
    },
    total=False,
)


class ComplianceExecutionSummaryTypeDef(
    _RequiredComplianceExecutionSummaryTypeDef, _OptionalComplianceExecutionSummaryTypeDef
):
    pass


_RequiredComplianceItemEntryTypeDef = TypedDict(
    "_RequiredComplianceItemEntryTypeDef",
    {
        "Severity": ComplianceSeverityType,
        "Status": ComplianceStatusType,
    },
)
_OptionalComplianceItemEntryTypeDef = TypedDict(
    "_OptionalComplianceItemEntryTypeDef",
    {
        "Id": str,
        "Title": str,
        "Details": Mapping[str, str],
    },
    total=False,
)


class ComplianceItemEntryTypeDef(
    _RequiredComplianceItemEntryTypeDef, _OptionalComplianceItemEntryTypeDef
):
    pass


ComplianceStringFilterTypeDef = TypedDict(
    "ComplianceStringFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "Type": ComplianceQueryOperatorTypeType,
    },
    total=False,
)

SeveritySummaryTypeDef = TypedDict(
    "SeveritySummaryTypeDef",
    {
        "CriticalCount": int,
        "HighCount": int,
        "MediumCount": int,
        "LowCount": int,
        "InformationalCount": int,
        "UnspecifiedCount": int,
    },
    total=False,
)

RegistrationMetadataItemTypeDef = TypedDict(
    "RegistrationMetadataItemTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredDocumentRequiresTypeDef = TypedDict(
    "_RequiredDocumentRequiresTypeDef",
    {
        "Name": str,
    },
)
_OptionalDocumentRequiresTypeDef = TypedDict(
    "_OptionalDocumentRequiresTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class DocumentRequiresTypeDef(_RequiredDocumentRequiresTypeDef, _OptionalDocumentRequiresTypeDef):
    pass


OpsItemDataValueTypeDef = TypedDict(
    "OpsItemDataValueTypeDef",
    {
        "Value": str,
        "Type": OpsItemDataTypeType,
    },
    total=False,
)

OpsItemNotificationTypeDef = TypedDict(
    "OpsItemNotificationTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

RelatedOpsItemTypeDef = TypedDict(
    "RelatedOpsItemTypeDef",
    {
        "OpsItemId": str,
    },
)

MetadataValueTypeDef = TypedDict(
    "MetadataValueTypeDef",
    {
        "Value": str,
    },
    total=False,
)

DeleteActivationRequestRequestTypeDef = TypedDict(
    "DeleteActivationRequestRequestTypeDef",
    {
        "ActivationId": str,
    },
)

DeleteAssociationRequestRequestTypeDef = TypedDict(
    "DeleteAssociationRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceId": str,
        "AssociationId": str,
    },
    total=False,
)

_RequiredDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDocumentRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDocumentRequestRequestTypeDef",
    {
        "DocumentVersion": str,
        "VersionName": str,
        "Force": bool,
    },
    total=False,
)


class DeleteDocumentRequestRequestTypeDef(
    _RequiredDeleteDocumentRequestRequestTypeDef, _OptionalDeleteDocumentRequestRequestTypeDef
):
    pass


_RequiredDeleteInventoryRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteInventoryRequestRequestTypeDef",
    {
        "TypeName": str,
    },
)
_OptionalDeleteInventoryRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteInventoryRequestRequestTypeDef",
    {
        "SchemaDeleteOption": InventorySchemaDeleteOptionType,
        "DryRun": bool,
        "ClientToken": str,
    },
    total=False,
)


class DeleteInventoryRequestRequestTypeDef(
    _RequiredDeleteInventoryRequestRequestTypeDef, _OptionalDeleteInventoryRequestRequestTypeDef
):
    pass


DeleteMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "DeleteMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)

DeleteOpsMetadataRequestRequestTypeDef = TypedDict(
    "DeleteOpsMetadataRequestRequestTypeDef",
    {
        "OpsMetadataArn": str,
    },
)

DeleteParameterRequestRequestTypeDef = TypedDict(
    "DeleteParameterRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteParametersRequestRequestTypeDef = TypedDict(
    "DeleteParametersRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)

DeletePatchBaselineRequestRequestTypeDef = TypedDict(
    "DeletePatchBaselineRequestRequestTypeDef",
    {
        "BaselineId": str,
    },
)

_RequiredDeleteResourceDataSyncRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResourceDataSyncRequestRequestTypeDef",
    {
        "SyncName": str,
    },
)
_OptionalDeleteResourceDataSyncRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResourceDataSyncRequestRequestTypeDef",
    {
        "SyncType": str,
    },
    total=False,
)


class DeleteResourceDataSyncRequestRequestTypeDef(
    _RequiredDeleteResourceDataSyncRequestRequestTypeDef,
    _OptionalDeleteResourceDataSyncRequestRequestTypeDef,
):
    pass


DeregisterManagedInstanceRequestRequestTypeDef = TypedDict(
    "DeregisterManagedInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef = TypedDict(
    "DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    {
        "BaselineId": str,
        "PatchGroup": str,
    },
)

_RequiredDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_RequiredDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
        "WindowTargetId": str,
    },
)
_OptionalDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_OptionalDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef",
    {
        "Safe": bool,
    },
    total=False,
)


class DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef(
    _RequiredDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef,
    _OptionalDeregisterTargetFromMaintenanceWindowRequestRequestTypeDef,
):
    pass


DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
    },
)

DescribeActivationsFilterTypeDef = TypedDict(
    "DescribeActivationsFilterTypeDef",
    {
        "FilterKey": DescribeActivationsFilterKeysType,
        "FilterValues": Sequence[str],
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

DescribeAssociationRequestRequestTypeDef = TypedDict(
    "DescribeAssociationRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceId": str,
        "AssociationId": str,
        "AssociationVersion": str,
    },
    total=False,
)

StepExecutionFilterTypeDef = TypedDict(
    "StepExecutionFilterTypeDef",
    {
        "Key": StepExecutionFilterKeyType,
        "Values": Sequence[str],
    },
)

PatchOrchestratorFilterTypeDef = TypedDict(
    "PatchOrchestratorFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
    total=False,
)

PatchTypeDef = TypedDict(
    "PatchTypeDef",
    {
        "Id": str,
        "ReleaseDate": datetime,
        "Title": str,
        "Description": str,
        "ContentUrl": str,
        "Vendor": str,
        "ProductFamily": str,
        "Product": str,
        "Classification": str,
        "MsrcSeverity": str,
        "KbNumber": str,
        "MsrcNumber": str,
        "Language": str,
        "AdvisoryIds": List[str],
        "BugzillaIds": List[str],
        "CVEIds": List[str],
        "Name": str,
        "Epoch": int,
        "Version": str,
        "Release": str,
        "Arch": str,
        "Severity": str,
        "Repository": str,
    },
    total=False,
)

_RequiredDescribeDocumentPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDocumentPermissionRequestRequestTypeDef",
    {
        "Name": str,
        "PermissionType": Literal["Share"],
    },
)
_OptionalDescribeDocumentPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDocumentPermissionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeDocumentPermissionRequestRequestTypeDef(
    _RequiredDescribeDocumentPermissionRequestRequestTypeDef,
    _OptionalDescribeDocumentPermissionRequestRequestTypeDef,
):
    pass


_RequiredDescribeDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDocumentRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDescribeDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDocumentRequestRequestTypeDef",
    {
        "DocumentVersion": str,
        "VersionName": str,
    },
    total=False,
)


class DescribeDocumentRequestRequestTypeDef(
    _RequiredDescribeDocumentRequestRequestTypeDef, _OptionalDescribeDocumentRequestRequestTypeDef
):
    pass


_RequiredDescribeEffectiveInstanceAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEffectiveInstanceAssociationsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeEffectiveInstanceAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEffectiveInstanceAssociationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeEffectiveInstanceAssociationsRequestRequestTypeDef(
    _RequiredDescribeEffectiveInstanceAssociationsRequestRequestTypeDef,
    _OptionalDescribeEffectiveInstanceAssociationsRequestRequestTypeDef,
):
    pass


InstanceAssociationTypeDef = TypedDict(
    "InstanceAssociationTypeDef",
    {
        "AssociationId": str,
        "InstanceId": str,
        "Content": str,
        "AssociationVersion": str,
    },
    total=False,
)

_RequiredDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef",
    {
        "BaselineId": str,
    },
)
_OptionalDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef(
    _RequiredDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef,
    _OptionalDescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef,
):
    pass


_RequiredDescribeInstanceAssociationsStatusRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInstanceAssociationsStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeInstanceAssociationsStatusRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInstanceAssociationsStatusRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeInstanceAssociationsStatusRequestRequestTypeDef(
    _RequiredDescribeInstanceAssociationsStatusRequestRequestTypeDef,
    _OptionalDescribeInstanceAssociationsStatusRequestRequestTypeDef,
):
    pass


InstanceInformationFilterTypeDef = TypedDict(
    "InstanceInformationFilterTypeDef",
    {
        "key": InstanceInformationFilterKeyType,
        "valueSet": Sequence[str],
    },
)

InstanceInformationStringFilterTypeDef = TypedDict(
    "InstanceInformationStringFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)

InstancePatchStateFilterTypeDef = TypedDict(
    "InstancePatchStateFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "Type": InstancePatchStateOperatorTypeType,
    },
)

_RequiredInstancePatchStateTypeDef = TypedDict(
    "_RequiredInstancePatchStateTypeDef",
    {
        "InstanceId": str,
        "PatchGroup": str,
        "BaselineId": str,
        "OperationStartTime": datetime,
        "OperationEndTime": datetime,
        "Operation": PatchOperationTypeType,
    },
)
_OptionalInstancePatchStateTypeDef = TypedDict(
    "_OptionalInstancePatchStateTypeDef",
    {
        "SnapshotId": str,
        "InstallOverrideList": str,
        "OwnerInformation": str,
        "InstalledCount": int,
        "InstalledOtherCount": int,
        "InstalledPendingRebootCount": int,
        "InstalledRejectedCount": int,
        "MissingCount": int,
        "FailedCount": int,
        "UnreportedNotApplicableCount": int,
        "NotApplicableCount": int,
        "LastNoRebootInstallOperationTime": datetime,
        "RebootOption": RebootOptionType,
        "CriticalNonCompliantCount": int,
        "SecurityNonCompliantCount": int,
        "OtherNonCompliantCount": int,
    },
    total=False,
)


class InstancePatchStateTypeDef(
    _RequiredInstancePatchStateTypeDef, _OptionalInstancePatchStateTypeDef
):
    pass


_RequiredDescribeInstancePatchStatesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchStatesRequestRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
)
_OptionalDescribeInstancePatchStatesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchStatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeInstancePatchStatesRequestRequestTypeDef(
    _RequiredDescribeInstancePatchStatesRequestRequestTypeDef,
    _OptionalDescribeInstancePatchStatesRequestRequestTypeDef,
):
    pass


_RequiredPatchComplianceDataTypeDef = TypedDict(
    "_RequiredPatchComplianceDataTypeDef",
    {
        "Title": str,
        "KBId": str,
        "Classification": str,
        "Severity": str,
        "State": PatchComplianceDataStateType,
        "InstalledTime": datetime,
    },
)
_OptionalPatchComplianceDataTypeDef = TypedDict(
    "_OptionalPatchComplianceDataTypeDef",
    {
        "CVEIds": str,
    },
    total=False,
)


class PatchComplianceDataTypeDef(
    _RequiredPatchComplianceDataTypeDef, _OptionalPatchComplianceDataTypeDef
):
    pass


DescribeInventoryDeletionsRequestRequestTypeDef = TypedDict(
    "DescribeInventoryDeletionsRequestRequestTypeDef",
    {
        "DeletionId": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MaintenanceWindowFilterTypeDef = TypedDict(
    "MaintenanceWindowFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
    total=False,
)

MaintenanceWindowExecutionTaskInvocationIdentityTypeDef = TypedDict(
    "MaintenanceWindowExecutionTaskInvocationIdentityTypeDef",
    {
        "WindowExecutionId": str,
        "TaskExecutionId": str,
        "InvocationId": str,
        "ExecutionId": str,
        "TaskType": MaintenanceWindowTaskTypeType,
        "Parameters": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "OwnerInformation": str,
        "WindowTargetId": str,
    },
    total=False,
)

MaintenanceWindowExecutionTaskIdentityTypeDef = TypedDict(
    "MaintenanceWindowExecutionTaskIdentityTypeDef",
    {
        "WindowExecutionId": str,
        "TaskExecutionId": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "TaskArn": str,
        "TaskType": MaintenanceWindowTaskTypeType,
    },
    total=False,
)

MaintenanceWindowExecutionTypeDef = TypedDict(
    "MaintenanceWindowExecutionTypeDef",
    {
        "WindowId": str,
        "WindowExecutionId": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

ScheduledWindowExecutionTypeDef = TypedDict(
    "ScheduledWindowExecutionTypeDef",
    {
        "WindowId": str,
        "Name": str,
        "ExecutionTime": str,
    },
    total=False,
)

MaintenanceWindowIdentityForTargetTypeDef = TypedDict(
    "MaintenanceWindowIdentityForTargetTypeDef",
    {
        "WindowId": str,
        "Name": str,
    },
    total=False,
)

MaintenanceWindowIdentityTypeDef = TypedDict(
    "MaintenanceWindowIdentityTypeDef",
    {
        "WindowId": str,
        "Name": str,
        "Description": str,
        "Enabled": bool,
        "Duration": int,
        "Cutoff": int,
        "Schedule": str,
        "ScheduleTimezone": str,
        "ScheduleOffset": int,
        "EndDate": str,
        "StartDate": str,
        "NextExecutionTime": str,
    },
    total=False,
)

OpsItemFilterTypeDef = TypedDict(
    "OpsItemFilterTypeDef",
    {
        "Key": OpsItemFilterKeyType,
        "Values": Sequence[str],
        "Operator": OpsItemFilterOperatorType,
    },
)

_RequiredParameterStringFilterTypeDef = TypedDict(
    "_RequiredParameterStringFilterTypeDef",
    {
        "Key": str,
    },
)
_OptionalParameterStringFilterTypeDef = TypedDict(
    "_OptionalParameterStringFilterTypeDef",
    {
        "Option": str,
        "Values": Sequence[str],
    },
    total=False,
)


class ParameterStringFilterTypeDef(
    _RequiredParameterStringFilterTypeDef, _OptionalParameterStringFilterTypeDef
):
    pass


ParametersFilterTypeDef = TypedDict(
    "ParametersFilterTypeDef",
    {
        "Key": ParametersFilterKeyType,
        "Values": Sequence[str],
    },
)

PatchBaselineIdentityTypeDef = TypedDict(
    "PatchBaselineIdentityTypeDef",
    {
        "BaselineId": str,
        "BaselineName": str,
        "OperatingSystem": OperatingSystemType,
        "BaselineDescription": str,
        "DefaultBaseline": bool,
    },
    total=False,
)

DescribePatchGroupStateRequestRequestTypeDef = TypedDict(
    "DescribePatchGroupStateRequestRequestTypeDef",
    {
        "PatchGroup": str,
    },
)

_RequiredDescribePatchPropertiesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribePatchPropertiesRequestRequestTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
        "Property": PatchPropertyType,
    },
)
_OptionalDescribePatchPropertiesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribePatchPropertiesRequestRequestTypeDef",
    {
        "PatchSet": PatchSetType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribePatchPropertiesRequestRequestTypeDef(
    _RequiredDescribePatchPropertiesRequestRequestTypeDef,
    _OptionalDescribePatchPropertiesRequestRequestTypeDef,
):
    pass


SessionFilterTypeDef = TypedDict(
    "SessionFilterTypeDef",
    {
        "key": SessionFilterKeyType,
        "value": str,
    },
)

DisassociateOpsItemRelatedItemRequestRequestTypeDef = TypedDict(
    "DisassociateOpsItemRelatedItemRequestRequestTypeDef",
    {
        "OpsItemId": str,
        "AssociationId": str,
    },
)

DocumentDefaultVersionDescriptionTypeDef = TypedDict(
    "DocumentDefaultVersionDescriptionTypeDef",
    {
        "Name": str,
        "DefaultVersion": str,
        "DefaultVersionName": str,
    },
    total=False,
)

DocumentParameterTypeDef = TypedDict(
    "DocumentParameterTypeDef",
    {
        "Name": str,
        "Type": DocumentParameterTypeType,
        "Description": str,
        "DefaultValue": str,
    },
    total=False,
)

ReviewInformationTypeDef = TypedDict(
    "ReviewInformationTypeDef",
    {
        "ReviewedTime": datetime,
        "Status": ReviewStatusType,
        "Reviewer": str,
    },
    total=False,
)

DocumentFilterTypeDef = TypedDict(
    "DocumentFilterTypeDef",
    {
        "key": DocumentFilterKeyType,
        "value": str,
    },
)

DocumentKeyValuesFilterTypeDef = TypedDict(
    "DocumentKeyValuesFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
    total=False,
)

DocumentReviewCommentSourceTypeDef = TypedDict(
    "DocumentReviewCommentSourceTypeDef",
    {
        "Type": Literal["Comment"],
        "Content": str,
    },
    total=False,
)

DocumentVersionInfoTypeDef = TypedDict(
    "DocumentVersionInfoTypeDef",
    {
        "Name": str,
        "DisplayName": str,
        "DocumentVersion": str,
        "VersionName": str,
        "CreatedDate": datetime,
        "IsDefaultVersion": bool,
        "DocumentFormat": DocumentFormatType,
        "Status": DocumentStatusType,
        "StatusInformation": str,
        "ReviewStatus": ReviewStatusType,
    },
    total=False,
)

PatchStatusTypeDef = TypedDict(
    "PatchStatusTypeDef",
    {
        "DeploymentStatus": PatchDeploymentStatusType,
        "ComplianceLevel": PatchComplianceLevelType,
        "ApprovalDate": datetime,
    },
    total=False,
)

FailureDetailsTypeDef = TypedDict(
    "FailureDetailsTypeDef",
    {
        "FailureStage": str,
        "FailureType": str,
        "Details": Dict[str, List[str]],
    },
    total=False,
)

GetAutomationExecutionRequestRequestTypeDef = TypedDict(
    "GetAutomationExecutionRequestRequestTypeDef",
    {
        "AutomationExecutionId": str,
    },
)

_RequiredGetCalendarStateRequestRequestTypeDef = TypedDict(
    "_RequiredGetCalendarStateRequestRequestTypeDef",
    {
        "CalendarNames": Sequence[str],
    },
)
_OptionalGetCalendarStateRequestRequestTypeDef = TypedDict(
    "_OptionalGetCalendarStateRequestRequestTypeDef",
    {
        "AtTime": str,
    },
    total=False,
)


class GetCalendarStateRequestRequestTypeDef(
    _RequiredGetCalendarStateRequestRequestTypeDef, _OptionalGetCalendarStateRequestRequestTypeDef
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

_RequiredGetCommandInvocationRequestRequestTypeDef = TypedDict(
    "_RequiredGetCommandInvocationRequestRequestTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
    },
)
_OptionalGetCommandInvocationRequestRequestTypeDef = TypedDict(
    "_OptionalGetCommandInvocationRequestRequestTypeDef",
    {
        "PluginName": str,
    },
    total=False,
)


class GetCommandInvocationRequestRequestTypeDef(
    _RequiredGetCommandInvocationRequestRequestTypeDef,
    _OptionalGetCommandInvocationRequestRequestTypeDef,
):
    pass


GetConnectionStatusRequestRequestTypeDef = TypedDict(
    "GetConnectionStatusRequestRequestTypeDef",
    {
        "Target": str,
    },
)

GetDefaultPatchBaselineRequestRequestTypeDef = TypedDict(
    "GetDefaultPatchBaselineRequestRequestTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
    },
    total=False,
)

_RequiredGetDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentRequestRequestTypeDef",
    {
        "VersionName": str,
        "DocumentVersion": str,
        "DocumentFormat": DocumentFormatType,
    },
    total=False,
)


class GetDocumentRequestRequestTypeDef(
    _RequiredGetDocumentRequestRequestTypeDef, _OptionalGetDocumentRequestRequestTypeDef
):
    pass


_RequiredInventoryFilterTypeDef = TypedDict(
    "_RequiredInventoryFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)
_OptionalInventoryFilterTypeDef = TypedDict(
    "_OptionalInventoryFilterTypeDef",
    {
        "Type": InventoryQueryOperatorTypeType,
    },
    total=False,
)


class InventoryFilterTypeDef(_RequiredInventoryFilterTypeDef, _OptionalInventoryFilterTypeDef):
    pass


ResultAttributeTypeDef = TypedDict(
    "ResultAttributeTypeDef",
    {
        "TypeName": str,
    },
)

GetInventorySchemaRequestRequestTypeDef = TypedDict(
    "GetInventorySchemaRequestRequestTypeDef",
    {
        "TypeName": str,
        "NextToken": str,
        "MaxResults": int,
        "Aggregator": bool,
        "SubType": bool,
    },
    total=False,
)

GetMaintenanceWindowExecutionRequestRequestTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
    },
)

GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
        "TaskId": str,
        "InvocationId": str,
    },
)

GetMaintenanceWindowExecutionTaskRequestRequestTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionTaskRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
        "TaskId": str,
    },
)

MaintenanceWindowTaskParameterValueExpressionTypeDef = TypedDict(
    "MaintenanceWindowTaskParameterValueExpressionTypeDef",
    {
        "Values": List[str],
    },
    total=False,
)

GetMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "GetMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)

GetMaintenanceWindowTaskRequestRequestTypeDef = TypedDict(
    "GetMaintenanceWindowTaskRequestRequestTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
    },
)

_RequiredLoggingInfoTypeDef = TypedDict(
    "_RequiredLoggingInfoTypeDef",
    {
        "S3BucketName": str,
        "S3Region": str,
    },
)
_OptionalLoggingInfoTypeDef = TypedDict(
    "_OptionalLoggingInfoTypeDef",
    {
        "S3KeyPrefix": str,
    },
    total=False,
)


class LoggingInfoTypeDef(_RequiredLoggingInfoTypeDef, _OptionalLoggingInfoTypeDef):
    pass


GetOpsItemRequestRequestTypeDef = TypedDict(
    "GetOpsItemRequestRequestTypeDef",
    {
        "OpsItemId": str,
    },
)

_RequiredGetOpsMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredGetOpsMetadataRequestRequestTypeDef",
    {
        "OpsMetadataArn": str,
    },
)
_OptionalGetOpsMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalGetOpsMetadataRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetOpsMetadataRequestRequestTypeDef(
    _RequiredGetOpsMetadataRequestRequestTypeDef, _OptionalGetOpsMetadataRequestRequestTypeDef
):
    pass


_RequiredOpsFilterTypeDef = TypedDict(
    "_RequiredOpsFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)
_OptionalOpsFilterTypeDef = TypedDict(
    "_OptionalOpsFilterTypeDef",
    {
        "Type": OpsFilterOperatorTypeType,
    },
    total=False,
)


class OpsFilterTypeDef(_RequiredOpsFilterTypeDef, _OptionalOpsFilterTypeDef):
    pass


OpsResultAttributeTypeDef = TypedDict(
    "OpsResultAttributeTypeDef",
    {
        "TypeName": str,
    },
)

_RequiredGetParameterHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetParameterHistoryRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetParameterHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetParameterHistoryRequestRequestTypeDef",
    {
        "WithDecryption": bool,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetParameterHistoryRequestRequestTypeDef(
    _RequiredGetParameterHistoryRequestRequestTypeDef,
    _OptionalGetParameterHistoryRequestRequestTypeDef,
):
    pass


_RequiredGetParameterRequestRequestTypeDef = TypedDict(
    "_RequiredGetParameterRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetParameterRequestRequestTypeDef = TypedDict(
    "_OptionalGetParameterRequestRequestTypeDef",
    {
        "WithDecryption": bool,
    },
    total=False,
)


class GetParameterRequestRequestTypeDef(
    _RequiredGetParameterRequestRequestTypeDef, _OptionalGetParameterRequestRequestTypeDef
):
    pass


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "Value": str,
        "Version": int,
        "Selector": str,
        "SourceResult": str,
        "LastModifiedDate": datetime,
        "ARN": str,
        "DataType": str,
    },
    total=False,
)

_RequiredGetParametersRequestRequestTypeDef = TypedDict(
    "_RequiredGetParametersRequestRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
_OptionalGetParametersRequestRequestTypeDef = TypedDict(
    "_OptionalGetParametersRequestRequestTypeDef",
    {
        "WithDecryption": bool,
    },
    total=False,
)


class GetParametersRequestRequestTypeDef(
    _RequiredGetParametersRequestRequestTypeDef, _OptionalGetParametersRequestRequestTypeDef
):
    pass


_RequiredGetPatchBaselineForPatchGroupRequestRequestTypeDef = TypedDict(
    "_RequiredGetPatchBaselineForPatchGroupRequestRequestTypeDef",
    {
        "PatchGroup": str,
    },
)
_OptionalGetPatchBaselineForPatchGroupRequestRequestTypeDef = TypedDict(
    "_OptionalGetPatchBaselineForPatchGroupRequestRequestTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
    },
    total=False,
)


class GetPatchBaselineForPatchGroupRequestRequestTypeDef(
    _RequiredGetPatchBaselineForPatchGroupRequestRequestTypeDef,
    _OptionalGetPatchBaselineForPatchGroupRequestRequestTypeDef,
):
    pass


GetPatchBaselineRequestRequestTypeDef = TypedDict(
    "GetPatchBaselineRequestRequestTypeDef",
    {
        "BaselineId": str,
    },
)

GetServiceSettingRequestRequestTypeDef = TypedDict(
    "GetServiceSettingRequestRequestTypeDef",
    {
        "SettingId": str,
    },
)

ServiceSettingTypeDef = TypedDict(
    "ServiceSettingTypeDef",
    {
        "SettingId": str,
        "SettingValue": str,
        "LastModifiedDate": datetime,
        "LastModifiedUser": str,
        "ARN": str,
        "Status": str,
    },
    total=False,
)

InstanceAggregatedAssociationOverviewTypeDef = TypedDict(
    "InstanceAggregatedAssociationOverviewTypeDef",
    {
        "DetailedStatus": str,
        "InstanceAssociationStatusAggregatedCount": Dict[str, int],
    },
    total=False,
)

S3OutputLocationTypeDef = TypedDict(
    "S3OutputLocationTypeDef",
    {
        "OutputS3Region": str,
        "OutputS3BucketName": str,
        "OutputS3KeyPrefix": str,
    },
    total=False,
)

S3OutputUrlTypeDef = TypedDict(
    "S3OutputUrlTypeDef",
    {
        "OutputUrl": str,
    },
    total=False,
)

InventoryDeletionSummaryItemTypeDef = TypedDict(
    "InventoryDeletionSummaryItemTypeDef",
    {
        "Version": str,
        "Count": int,
        "RemainingCount": int,
    },
    total=False,
)

InventoryItemAttributeTypeDef = TypedDict(
    "InventoryItemAttributeTypeDef",
    {
        "Name": str,
        "DataType": InventoryAttributeDataTypeType,
    },
)

_RequiredInventoryItemTypeDef = TypedDict(
    "_RequiredInventoryItemTypeDef",
    {
        "TypeName": str,
        "SchemaVersion": str,
        "CaptureTime": str,
    },
)
_OptionalInventoryItemTypeDef = TypedDict(
    "_OptionalInventoryItemTypeDef",
    {
        "ContentHash": str,
        "Content": Sequence[Mapping[str, str]],
        "Context": Mapping[str, str],
    },
    total=False,
)


class InventoryItemTypeDef(_RequiredInventoryItemTypeDef, _OptionalInventoryItemTypeDef):
    pass


_RequiredInventoryResultItemTypeDef = TypedDict(
    "_RequiredInventoryResultItemTypeDef",
    {
        "TypeName": str,
        "SchemaVersion": str,
        "Content": List[Dict[str, str]],
    },
)
_OptionalInventoryResultItemTypeDef = TypedDict(
    "_OptionalInventoryResultItemTypeDef",
    {
        "CaptureTime": str,
        "ContentHash": str,
    },
    total=False,
)


class InventoryResultItemTypeDef(
    _RequiredInventoryResultItemTypeDef, _OptionalInventoryResultItemTypeDef
):
    pass


_RequiredLabelParameterVersionRequestRequestTypeDef = TypedDict(
    "_RequiredLabelParameterVersionRequestRequestTypeDef",
    {
        "Name": str,
        "Labels": Sequence[str],
    },
)
_OptionalLabelParameterVersionRequestRequestTypeDef = TypedDict(
    "_OptionalLabelParameterVersionRequestRequestTypeDef",
    {
        "ParameterVersion": int,
    },
    total=False,
)


class LabelParameterVersionRequestRequestTypeDef(
    _RequiredLabelParameterVersionRequestRequestTypeDef,
    _OptionalLabelParameterVersionRequestRequestTypeDef,
):
    pass


_RequiredListAssociationVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociationVersionsRequestRequestTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalListAssociationVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociationVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAssociationVersionsRequestRequestTypeDef(
    _RequiredListAssociationVersionsRequestRequestTypeDef,
    _OptionalListAssociationVersionsRequestRequestTypeDef,
):
    pass


_RequiredListDocumentMetadataHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredListDocumentMetadataHistoryRequestRequestTypeDef",
    {
        "Name": str,
        "Metadata": Literal["DocumentReviews"],
    },
)
_OptionalListDocumentMetadataHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalListDocumentMetadataHistoryRequestRequestTypeDef",
    {
        "DocumentVersion": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDocumentMetadataHistoryRequestRequestTypeDef(
    _RequiredListDocumentMetadataHistoryRequestRequestTypeDef,
    _OptionalListDocumentMetadataHistoryRequestRequestTypeDef,
):
    pass


_RequiredListDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDocumentVersionsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalListDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDocumentVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListDocumentVersionsRequestRequestTypeDef(
    _RequiredListDocumentVersionsRequestRequestTypeDef,
    _OptionalListDocumentVersionsRequestRequestTypeDef,
):
    pass


OpsItemEventFilterTypeDef = TypedDict(
    "OpsItemEventFilterTypeDef",
    {
        "Key": Literal["OpsItemId"],
        "Values": Sequence[str],
        "Operator": Literal["Equal"],
    },
)

OpsItemRelatedItemsFilterTypeDef = TypedDict(
    "OpsItemRelatedItemsFilterTypeDef",
    {
        "Key": OpsItemRelatedItemsFilterKeyType,
        "Values": Sequence[str],
        "Operator": Literal["Equal"],
    },
)

OpsMetadataFilterTypeDef = TypedDict(
    "OpsMetadataFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)

OpsMetadataTypeDef = TypedDict(
    "OpsMetadataTypeDef",
    {
        "ResourceId": str,
        "OpsMetadataArn": str,
        "LastModifiedDate": datetime,
        "LastModifiedUser": str,
        "CreationDate": datetime,
    },
    total=False,
)

ListResourceDataSyncRequestRequestTypeDef = TypedDict(
    "ListResourceDataSyncRequestRequestTypeDef",
    {
        "SyncType": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeForTaggingType,
        "ResourceId": str,
    },
)

MaintenanceWindowAutomationParametersTypeDef = TypedDict(
    "MaintenanceWindowAutomationParametersTypeDef",
    {
        "DocumentVersion": str,
        "Parameters": Dict[str, List[str]],
    },
    total=False,
)

MaintenanceWindowLambdaParametersTypeDef = TypedDict(
    "MaintenanceWindowLambdaParametersTypeDef",
    {
        "ClientContext": str,
        "Qualifier": str,
        "Payload": bytes,
    },
    total=False,
)

MaintenanceWindowStepFunctionsParametersTypeDef = TypedDict(
    "MaintenanceWindowStepFunctionsParametersTypeDef",
    {
        "Input": str,
        "Name": str,
    },
    total=False,
)

_RequiredModifyDocumentPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredModifyDocumentPermissionRequestRequestTypeDef",
    {
        "Name": str,
        "PermissionType": Literal["Share"],
    },
)
_OptionalModifyDocumentPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalModifyDocumentPermissionRequestRequestTypeDef",
    {
        "AccountIdsToAdd": Sequence[str],
        "AccountIdsToRemove": Sequence[str],
        "SharedDocumentVersion": str,
    },
    total=False,
)


class ModifyDocumentPermissionRequestRequestTypeDef(
    _RequiredModifyDocumentPermissionRequestRequestTypeDef,
    _OptionalModifyDocumentPermissionRequestRequestTypeDef,
):
    pass


OpsEntityItemTypeDef = TypedDict(
    "OpsEntityItemTypeDef",
    {
        "CaptureTime": str,
        "Content": List[Dict[str, str]],
    },
    total=False,
)

OpsItemIdentityTypeDef = TypedDict(
    "OpsItemIdentityTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

ParameterInlinePolicyTypeDef = TypedDict(
    "ParameterInlinePolicyTypeDef",
    {
        "PolicyText": str,
        "PolicyType": str,
        "PolicyStatus": str,
    },
    total=False,
)

PatchFilterTypeDef = TypedDict(
    "PatchFilterTypeDef",
    {
        "Key": PatchFilterKeyType,
        "Values": Sequence[str],
    },
)

RegisterDefaultPatchBaselineRequestRequestTypeDef = TypedDict(
    "RegisterDefaultPatchBaselineRequestRequestTypeDef",
    {
        "BaselineId": str,
    },
)

RegisterPatchBaselineForPatchGroupRequestRequestTypeDef = TypedDict(
    "RegisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    {
        "BaselineId": str,
        "PatchGroup": str,
    },
)

RemoveTagsFromResourceRequestRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeForTaggingType,
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

ResetServiceSettingRequestRequestTypeDef = TypedDict(
    "ResetServiceSettingRequestRequestTypeDef",
    {
        "SettingId": str,
    },
)

ResourceDataSyncOrganizationalUnitTypeDef = TypedDict(
    "ResourceDataSyncOrganizationalUnitTypeDef",
    {
        "OrganizationalUnitId": str,
    },
    total=False,
)

ResourceDataSyncDestinationDataSharingTypeDef = TypedDict(
    "ResourceDataSyncDestinationDataSharingTypeDef",
    {
        "DestinationDataSharingType": str,
    },
    total=False,
)

ResumeSessionRequestRequestTypeDef = TypedDict(
    "ResumeSessionRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)

_RequiredSendAutomationSignalRequestRequestTypeDef = TypedDict(
    "_RequiredSendAutomationSignalRequestRequestTypeDef",
    {
        "AutomationExecutionId": str,
        "SignalType": SignalTypeType,
    },
)
_OptionalSendAutomationSignalRequestRequestTypeDef = TypedDict(
    "_OptionalSendAutomationSignalRequestRequestTypeDef",
    {
        "Payload": Mapping[str, Sequence[str]],
    },
    total=False,
)


class SendAutomationSignalRequestRequestTypeDef(
    _RequiredSendAutomationSignalRequestRequestTypeDef,
    _OptionalSendAutomationSignalRequestRequestTypeDef,
):
    pass


SessionManagerOutputUrlTypeDef = TypedDict(
    "SessionManagerOutputUrlTypeDef",
    {
        "S3OutputUrl": str,
        "CloudWatchOutputUrl": str,
    },
    total=False,
)

StartAssociationsOnceRequestRequestTypeDef = TypedDict(
    "StartAssociationsOnceRequestRequestTypeDef",
    {
        "AssociationIds": Sequence[str],
    },
)

_RequiredStartSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStartSessionRequestRequestTypeDef",
    {
        "Target": str,
    },
)
_OptionalStartSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStartSessionRequestRequestTypeDef",
    {
        "DocumentName": str,
        "Reason": str,
        "Parameters": Mapping[str, Sequence[str]],
    },
    total=False,
)


class StartSessionRequestRequestTypeDef(
    _RequiredStartSessionRequestRequestTypeDef, _OptionalStartSessionRequestRequestTypeDef
):
    pass


_RequiredStopAutomationExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStopAutomationExecutionRequestRequestTypeDef",
    {
        "AutomationExecutionId": str,
    },
)
_OptionalStopAutomationExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStopAutomationExecutionRequestRequestTypeDef",
    {
        "Type": StopTypeType,
    },
    total=False,
)


class StopAutomationExecutionRequestRequestTypeDef(
    _RequiredStopAutomationExecutionRequestRequestTypeDef,
    _OptionalStopAutomationExecutionRequestRequestTypeDef,
):
    pass


TerminateSessionRequestRequestTypeDef = TypedDict(
    "TerminateSessionRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)

UnlabelParameterVersionRequestRequestTypeDef = TypedDict(
    "UnlabelParameterVersionRequestRequestTypeDef",
    {
        "Name": str,
        "ParameterVersion": int,
        "Labels": Sequence[str],
    },
)

UpdateDocumentDefaultVersionRequestRequestTypeDef = TypedDict(
    "UpdateDocumentDefaultVersionRequestRequestTypeDef",
    {
        "Name": str,
        "DocumentVersion": str,
    },
)

_RequiredUpdateMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalUpdateMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMaintenanceWindowRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "StartDate": str,
        "EndDate": str,
        "Schedule": str,
        "ScheduleTimezone": str,
        "ScheduleOffset": int,
        "Duration": int,
        "Cutoff": int,
        "AllowUnassociatedTargets": bool,
        "Enabled": bool,
        "Replace": bool,
    },
    total=False,
)


class UpdateMaintenanceWindowRequestRequestTypeDef(
    _RequiredUpdateMaintenanceWindowRequestRequestTypeDef,
    _OptionalUpdateMaintenanceWindowRequestRequestTypeDef,
):
    pass


UpdateManagedInstanceRoleRequestRequestTypeDef = TypedDict(
    "UpdateManagedInstanceRoleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IamRole": str,
    },
)

UpdateServiceSettingRequestRequestTypeDef = TypedDict(
    "UpdateServiceSettingRequestRequestTypeDef",
    {
        "SettingId": str,
        "SettingValue": str,
    },
)

ActivationTypeDef = TypedDict(
    "ActivationTypeDef",
    {
        "ActivationId": str,
        "Description": str,
        "DefaultInstanceName": str,
        "IamRole": str,
        "RegistrationLimit": int,
        "RegistrationsCount": int,
        "ExpirationDate": datetime,
        "Expired": bool,
        "CreatedDate": datetime,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

AddTagsToResourceRequestRequestTypeDef = TypedDict(
    "AddTagsToResourceRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeForTaggingType,
        "ResourceId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMaintenanceWindowRequestRequestTypeDef",
    {
        "Name": str,
        "Schedule": str,
        "Duration": int,
        "Cutoff": int,
        "AllowUnassociatedTargets": bool,
    },
)
_OptionalCreateMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMaintenanceWindowRequestRequestTypeDef",
    {
        "Description": str,
        "StartDate": str,
        "EndDate": str,
        "ScheduleTimezone": str,
        "ScheduleOffset": int,
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMaintenanceWindowRequestRequestTypeDef(
    _RequiredCreateMaintenanceWindowRequestRequestTypeDef,
    _OptionalCreateMaintenanceWindowRequestRequestTypeDef,
):
    pass


_RequiredPutParameterRequestRequestTypeDef = TypedDict(
    "_RequiredPutParameterRequestRequestTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalPutParameterRequestRequestTypeDef = TypedDict(
    "_OptionalPutParameterRequestRequestTypeDef",
    {
        "Description": str,
        "Type": ParameterTypeType,
        "KeyId": str,
        "Overwrite": bool,
        "AllowedPattern": str,
        "Tags": Sequence[TagTypeDef],
        "Tier": ParameterTierType,
        "Policies": str,
        "DataType": str,
    },
    total=False,
)


class PutParameterRequestRequestTypeDef(
    _RequiredPutParameterRequestRequestTypeDef, _OptionalPutParameterRequestRequestTypeDef
):
    pass


AssociateOpsItemRelatedItemResponseTypeDef = TypedDict(
    "AssociateOpsItemRelatedItemResponseTypeDef",
    {
        "AssociationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelMaintenanceWindowExecutionResultTypeDef = TypedDict(
    "CancelMaintenanceWindowExecutionResultTypeDef",
    {
        "WindowExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateActivationResultTypeDef = TypedDict(
    "CreateActivationResultTypeDef",
    {
        "ActivationId": str,
        "ActivationCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMaintenanceWindowResultTypeDef = TypedDict(
    "CreateMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOpsItemResponseTypeDef = TypedDict(
    "CreateOpsItemResponseTypeDef",
    {
        "OpsItemId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOpsMetadataResultTypeDef = TypedDict(
    "CreateOpsMetadataResultTypeDef",
    {
        "OpsMetadataArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePatchBaselineResultTypeDef = TypedDict(
    "CreatePatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMaintenanceWindowResultTypeDef = TypedDict(
    "DeleteMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteParametersResultTypeDef = TypedDict(
    "DeleteParametersResultTypeDef",
    {
        "DeletedParameters": List[str],
        "InvalidParameters": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePatchBaselineResultTypeDef = TypedDict(
    "DeletePatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterPatchBaselineForPatchGroupResultTypeDef = TypedDict(
    "DeregisterPatchBaselineForPatchGroupResultTypeDef",
    {
        "BaselineId": str,
        "PatchGroup": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterTargetFromMaintenanceWindowResultTypeDef = TypedDict(
    "DeregisterTargetFromMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "WindowTargetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterTaskFromMaintenanceWindowResultTypeDef = TypedDict(
    "DeregisterTaskFromMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDocumentPermissionResponseTypeDef = TypedDict(
    "DescribeDocumentPermissionResponseTypeDef",
    {
        "AccountIds": List[str],
        "AccountSharingInfoList": List[AccountSharingInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePatchGroupStateResultTypeDef = TypedDict(
    "DescribePatchGroupStateResultTypeDef",
    {
        "Instances": int,
        "InstancesWithInstalledPatches": int,
        "InstancesWithInstalledOtherPatches": int,
        "InstancesWithInstalledPendingRebootPatches": int,
        "InstancesWithInstalledRejectedPatches": int,
        "InstancesWithMissingPatches": int,
        "InstancesWithFailedPatches": int,
        "InstancesWithNotApplicablePatches": int,
        "InstancesWithUnreportedNotApplicablePatches": int,
        "InstancesWithCriticalNonCompliantPatches": int,
        "InstancesWithSecurityNonCompliantPatches": int,
        "InstancesWithOtherNonCompliantPatches": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePatchPropertiesResultTypeDef = TypedDict(
    "DescribePatchPropertiesResultTypeDef",
    {
        "Properties": List[Dict[str, str]],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCalendarStateResponseTypeDef = TypedDict(
    "GetCalendarStateResponseTypeDef",
    {
        "State": CalendarStateType,
        "AtTime": str,
        "NextTransitionTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectionStatusResponseTypeDef = TypedDict(
    "GetConnectionStatusResponseTypeDef",
    {
        "Target": str,
        "Status": ConnectionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDefaultPatchBaselineResultTypeDef = TypedDict(
    "GetDefaultPatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "OperatingSystem": OperatingSystemType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeployablePatchSnapshotForInstanceResultTypeDef = TypedDict(
    "GetDeployablePatchSnapshotForInstanceResultTypeDef",
    {
        "InstanceId": str,
        "SnapshotId": str,
        "SnapshotDownloadUrl": str,
        "Product": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMaintenanceWindowExecutionResultTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionResultTypeDef",
    {
        "WindowExecutionId": str,
        "TaskIds": List[str],
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMaintenanceWindowExecutionTaskInvocationResultTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionTaskInvocationResultTypeDef",
    {
        "WindowExecutionId": str,
        "TaskExecutionId": str,
        "InvocationId": str,
        "ExecutionId": str,
        "TaskType": MaintenanceWindowTaskTypeType,
        "Parameters": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "OwnerInformation": str,
        "WindowTargetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMaintenanceWindowResultTypeDef = TypedDict(
    "GetMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "Name": str,
        "Description": str,
        "StartDate": str,
        "EndDate": str,
        "Schedule": str,
        "ScheduleTimezone": str,
        "ScheduleOffset": int,
        "NextExecutionTime": str,
        "Duration": int,
        "Cutoff": int,
        "AllowUnassociatedTargets": bool,
        "Enabled": bool,
        "CreatedDate": datetime,
        "ModifiedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPatchBaselineForPatchGroupResultTypeDef = TypedDict(
    "GetPatchBaselineForPatchGroupResultTypeDef",
    {
        "BaselineId": str,
        "PatchGroup": str,
        "OperatingSystem": OperatingSystemType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LabelParameterVersionResultTypeDef = TypedDict(
    "LabelParameterVersionResultTypeDef",
    {
        "InvalidLabels": List[str],
        "ParameterVersion": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInventoryEntriesResultTypeDef = TypedDict(
    "ListInventoryEntriesResultTypeDef",
    {
        "TypeName": str,
        "InstanceId": str,
        "SchemaVersion": str,
        "CaptureTime": str,
        "Entries": List[Dict[str, str]],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutInventoryResultTypeDef = TypedDict(
    "PutInventoryResultTypeDef",
    {
        "Message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutParameterResultTypeDef = TypedDict(
    "PutParameterResultTypeDef",
    {
        "Version": int,
        "Tier": ParameterTierType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterDefaultPatchBaselineResultTypeDef = TypedDict(
    "RegisterDefaultPatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterPatchBaselineForPatchGroupResultTypeDef = TypedDict(
    "RegisterPatchBaselineForPatchGroupResultTypeDef",
    {
        "BaselineId": str,
        "PatchGroup": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterTargetWithMaintenanceWindowResultTypeDef = TypedDict(
    "RegisterTargetWithMaintenanceWindowResultTypeDef",
    {
        "WindowTargetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterTaskWithMaintenanceWindowResultTypeDef = TypedDict(
    "RegisterTaskWithMaintenanceWindowResultTypeDef",
    {
        "WindowTaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResumeSessionResponseTypeDef = TypedDict(
    "ResumeSessionResponseTypeDef",
    {
        "SessionId": str,
        "TokenValue": str,
        "StreamUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAutomationExecutionResultTypeDef = TypedDict(
    "StartAutomationExecutionResultTypeDef",
    {
        "AutomationExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartChangeRequestExecutionResultTypeDef = TypedDict(
    "StartChangeRequestExecutionResultTypeDef",
    {
        "AutomationExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSessionResponseTypeDef = TypedDict(
    "StartSessionResponseTypeDef",
    {
        "SessionId": str,
        "TokenValue": str,
        "StreamUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateSessionResponseTypeDef = TypedDict(
    "TerminateSessionResponseTypeDef",
    {
        "SessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UnlabelParameterVersionResultTypeDef = TypedDict(
    "UnlabelParameterVersionResultTypeDef",
    {
        "RemovedLabels": List[str],
        "InvalidLabels": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMaintenanceWindowResultTypeDef = TypedDict(
    "UpdateMaintenanceWindowResultTypeDef",
    {
        "WindowId": str,
        "Name": str,
        "Description": str,
        "StartDate": str,
        "EndDate": str,
        "Schedule": str,
        "ScheduleTimezone": str,
        "ScheduleOffset": int,
        "Duration": int,
        "Cutoff": int,
        "AllowUnassociatedTargets": bool,
        "Enabled": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateOpsMetadataResultTypeDef = TypedDict(
    "UpdateOpsMetadataResultTypeDef",
    {
        "OpsMetadataArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssociationStatusRequestRequestTypeDef = TypedDict(
    "UpdateAssociationStatusRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceId": str,
        "AssociationStatus": AssociationStatusTypeDef,
    },
)

AssociationTypeDef = TypedDict(
    "AssociationTypeDef",
    {
        "Name": str,
        "InstanceId": str,
        "AssociationId": str,
        "AssociationVersion": str,
        "DocumentVersion": str,
        "Targets": List[TargetTypeDef],
        "LastExecutionDate": datetime,
        "Overview": AssociationOverviewTypeDef,
        "ScheduleExpression": str,
        "AssociationName": str,
        "ScheduleOffset": int,
        "TargetMaps": List[Dict[str, List[str]]],
    },
    total=False,
)

_RequiredDescribeMaintenanceWindowsForTargetRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowsForTargetRequestRequestTypeDef",
    {
        "Targets": Sequence[TargetTypeDef],
        "ResourceType": MaintenanceWindowResourceTypeType,
    },
)
_OptionalDescribeMaintenanceWindowsForTargetRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowsForTargetRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowsForTargetRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowsForTargetRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowsForTargetRequestRequestTypeDef,
):
    pass


MaintenanceWindowTargetTypeDef = TypedDict(
    "MaintenanceWindowTargetTypeDef",
    {
        "WindowId": str,
        "WindowTargetId": str,
        "ResourceType": MaintenanceWindowResourceTypeType,
        "Targets": List[TargetTypeDef],
        "OwnerInformation": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

_RequiredRegisterTargetWithMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterTargetWithMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
        "ResourceType": MaintenanceWindowResourceTypeType,
        "Targets": Sequence[TargetTypeDef],
    },
)
_OptionalRegisterTargetWithMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterTargetWithMaintenanceWindowRequestRequestTypeDef",
    {
        "OwnerInformation": str,
        "Name": str,
        "Description": str,
        "ClientToken": str,
    },
    total=False,
)


class RegisterTargetWithMaintenanceWindowRequestRequestTypeDef(
    _RequiredRegisterTargetWithMaintenanceWindowRequestRequestTypeDef,
    _OptionalRegisterTargetWithMaintenanceWindowRequestRequestTypeDef,
):
    pass


_RequiredRunbookTypeDef = TypedDict(
    "_RequiredRunbookTypeDef",
    {
        "DocumentName": str,
    },
)
_OptionalRunbookTypeDef = TypedDict(
    "_OptionalRunbookTypeDef",
    {
        "DocumentVersion": str,
        "Parameters": Dict[str, List[str]],
        "TargetParameterName": str,
        "Targets": List[TargetTypeDef],
        "TargetMaps": List[Dict[str, List[str]]],
        "MaxConcurrency": str,
        "MaxErrors": str,
        "TargetLocations": List[TargetLocationTypeDef],
    },
    total=False,
)


class RunbookTypeDef(_RequiredRunbookTypeDef, _OptionalRunbookTypeDef):
    pass


_RequiredStartAutomationExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartAutomationExecutionRequestRequestTypeDef",
    {
        "DocumentName": str,
    },
)
_OptionalStartAutomationExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartAutomationExecutionRequestRequestTypeDef",
    {
        "DocumentVersion": str,
        "Parameters": Mapping[str, Sequence[str]],
        "ClientToken": str,
        "Mode": ExecutionModeType,
        "TargetParameterName": str,
        "Targets": Sequence[TargetTypeDef],
        "TargetMaps": Sequence[Mapping[str, Sequence[str]]],
        "MaxConcurrency": str,
        "MaxErrors": str,
        "TargetLocations": Sequence[TargetLocationTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartAutomationExecutionRequestRequestTypeDef(
    _RequiredStartAutomationExecutionRequestRequestTypeDef,
    _OptionalStartAutomationExecutionRequestRequestTypeDef,
):
    pass


_RequiredUpdateMaintenanceWindowTargetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMaintenanceWindowTargetRequestRequestTypeDef",
    {
        "WindowId": str,
        "WindowTargetId": str,
    },
)
_OptionalUpdateMaintenanceWindowTargetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMaintenanceWindowTargetRequestRequestTypeDef",
    {
        "Targets": Sequence[TargetTypeDef],
        "OwnerInformation": str,
        "Name": str,
        "Description": str,
        "Replace": bool,
    },
    total=False,
)


class UpdateMaintenanceWindowTargetRequestRequestTypeDef(
    _RequiredUpdateMaintenanceWindowTargetRequestRequestTypeDef,
    _OptionalUpdateMaintenanceWindowTargetRequestRequestTypeDef,
):
    pass


UpdateMaintenanceWindowTargetResultTypeDef = TypedDict(
    "UpdateMaintenanceWindowTargetResultTypeDef",
    {
        "WindowId": str,
        "WindowTargetId": str,
        "Targets": List[TargetTypeDef],
        "OwnerInformation": str,
        "Name": str,
        "Description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeAssociationExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAssociationExecutionsRequestRequestTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalDescribeAssociationExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAssociationExecutionsRequestRequestTypeDef",
    {
        "Filters": Sequence[AssociationExecutionFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeAssociationExecutionsRequestRequestTypeDef(
    _RequiredDescribeAssociationExecutionsRequestRequestTypeDef,
    _OptionalDescribeAssociationExecutionsRequestRequestTypeDef,
):
    pass


AssociationExecutionTargetTypeDef = TypedDict(
    "AssociationExecutionTargetTypeDef",
    {
        "AssociationId": str,
        "AssociationVersion": str,
        "ExecutionId": str,
        "ResourceId": str,
        "ResourceType": str,
        "Status": str,
        "DetailedStatus": str,
        "LastExecutionDate": datetime,
        "OutputSource": OutputSourceTypeDef,
    },
    total=False,
)

_RequiredDescribeAssociationExecutionTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAssociationExecutionTargetsRequestRequestTypeDef",
    {
        "AssociationId": str,
        "ExecutionId": str,
    },
)
_OptionalDescribeAssociationExecutionTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAssociationExecutionTargetsRequestRequestTypeDef",
    {
        "Filters": Sequence[AssociationExecutionTargetsFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeAssociationExecutionTargetsRequestRequestTypeDef(
    _RequiredDescribeAssociationExecutionTargetsRequestRequestTypeDef,
    _OptionalDescribeAssociationExecutionTargetsRequestRequestTypeDef,
):
    pass


DescribeAssociationExecutionsResultTypeDef = TypedDict(
    "DescribeAssociationExecutionsResultTypeDef",
    {
        "AssociationExecutions": List[AssociationExecutionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociationsRequestRequestTypeDef = TypedDict(
    "ListAssociationsRequestRequestTypeDef",
    {
        "AssociationFilterList": Sequence[AssociationFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredUpdateDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDocumentRequestRequestTypeDef",
    {
        "Content": str,
        "Name": str,
    },
)
_OptionalUpdateDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDocumentRequestRequestTypeDef",
    {
        "Attachments": Sequence[AttachmentsSourceTypeDef],
        "DisplayName": str,
        "VersionName": str,
        "DocumentVersion": str,
        "DocumentFormat": DocumentFormatType,
        "TargetType": str,
    },
    total=False,
)


class UpdateDocumentRequestRequestTypeDef(
    _RequiredUpdateDocumentRequestRequestTypeDef, _OptionalUpdateDocumentRequestRequestTypeDef
):
    pass


DescribeAutomationExecutionsRequestRequestTypeDef = TypedDict(
    "DescribeAutomationExecutionsRequestRequestTypeDef",
    {
        "Filters": Sequence[AutomationExecutionFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

GetCommandInvocationResultTypeDef = TypedDict(
    "GetCommandInvocationResultTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "Comment": str,
        "DocumentName": str,
        "DocumentVersion": str,
        "PluginName": str,
        "ResponseCode": int,
        "ExecutionStartDateTime": str,
        "ExecutionElapsedTime": str,
        "ExecutionEndDateTime": str,
        "Status": CommandInvocationStatusType,
        "StatusDetails": str,
        "StandardOutputContent": str,
        "StandardOutputUrl": str,
        "StandardErrorContent": str,
        "StandardErrorUrl": str,
        "CloudWatchOutputConfig": CloudWatchOutputConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCommandInvocationsRequestRequestTypeDef = TypedDict(
    "ListCommandInvocationsRequestRequestTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[CommandFilterTypeDef],
        "Details": bool,
    },
    total=False,
)

ListCommandsRequestRequestTypeDef = TypedDict(
    "ListCommandsRequestRequestTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[CommandFilterTypeDef],
    },
    total=False,
)

CommandInvocationTypeDef = TypedDict(
    "CommandInvocationTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "InstanceName": str,
        "Comment": str,
        "DocumentName": str,
        "DocumentVersion": str,
        "RequestedDateTime": datetime,
        "Status": CommandInvocationStatusType,
        "StatusDetails": str,
        "TraceOutput": str,
        "StandardOutputUrl": str,
        "StandardErrorUrl": str,
        "CommandPlugins": List[CommandPluginTypeDef],
        "ServiceRole": str,
        "NotificationConfig": NotificationConfigTypeDef,
        "CloudWatchOutputConfig": CloudWatchOutputConfigTypeDef,
    },
    total=False,
)

CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "CommandId": str,
        "DocumentName": str,
        "DocumentVersion": str,
        "Comment": str,
        "ExpiresAfter": datetime,
        "Parameters": Dict[str, List[str]],
        "InstanceIds": List[str],
        "Targets": List[TargetTypeDef],
        "RequestedDateTime": datetime,
        "Status": CommandStatusType,
        "StatusDetails": str,
        "OutputS3Region": str,
        "OutputS3BucketName": str,
        "OutputS3KeyPrefix": str,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "TargetCount": int,
        "CompletedCount": int,
        "ErrorCount": int,
        "DeliveryTimedOutCount": int,
        "ServiceRole": str,
        "NotificationConfig": NotificationConfigTypeDef,
        "CloudWatchOutputConfig": CloudWatchOutputConfigTypeDef,
        "TimeoutSeconds": int,
    },
    total=False,
)

MaintenanceWindowRunCommandParametersTypeDef = TypedDict(
    "MaintenanceWindowRunCommandParametersTypeDef",
    {
        "Comment": str,
        "CloudWatchOutputConfig": CloudWatchOutputConfigTypeDef,
        "DocumentHash": str,
        "DocumentHashType": DocumentHashTypeType,
        "DocumentVersion": str,
        "NotificationConfig": NotificationConfigTypeDef,
        "OutputS3BucketName": str,
        "OutputS3KeyPrefix": str,
        "Parameters": Dict[str, List[str]],
        "ServiceRoleArn": str,
        "TimeoutSeconds": int,
    },
    total=False,
)

_RequiredSendCommandRequestRequestTypeDef = TypedDict(
    "_RequiredSendCommandRequestRequestTypeDef",
    {
        "DocumentName": str,
    },
)
_OptionalSendCommandRequestRequestTypeDef = TypedDict(
    "_OptionalSendCommandRequestRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
        "Targets": Sequence[TargetTypeDef],
        "DocumentVersion": str,
        "DocumentHash": str,
        "DocumentHashType": DocumentHashTypeType,
        "TimeoutSeconds": int,
        "Comment": str,
        "Parameters": Mapping[str, Sequence[str]],
        "OutputS3Region": str,
        "OutputS3BucketName": str,
        "OutputS3KeyPrefix": str,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "ServiceRoleArn": str,
        "NotificationConfig": NotificationConfigTypeDef,
        "CloudWatchOutputConfig": CloudWatchOutputConfigTypeDef,
    },
    total=False,
)


class SendCommandRequestRequestTypeDef(
    _RequiredSendCommandRequestRequestTypeDef, _OptionalSendCommandRequestRequestTypeDef
):
    pass


ComplianceItemTypeDef = TypedDict(
    "ComplianceItemTypeDef",
    {
        "ComplianceType": str,
        "ResourceType": str,
        "ResourceId": str,
        "Id": str,
        "Title": str,
        "Status": ComplianceStatusType,
        "Severity": ComplianceSeverityType,
        "ExecutionSummary": ComplianceExecutionSummaryTypeDef,
        "Details": Dict[str, str],
    },
    total=False,
)

_RequiredPutComplianceItemsRequestRequestTypeDef = TypedDict(
    "_RequiredPutComplianceItemsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "ResourceType": str,
        "ComplianceType": str,
        "ExecutionSummary": ComplianceExecutionSummaryTypeDef,
        "Items": Sequence[ComplianceItemEntryTypeDef],
    },
)
_OptionalPutComplianceItemsRequestRequestTypeDef = TypedDict(
    "_OptionalPutComplianceItemsRequestRequestTypeDef",
    {
        "ItemContentHash": str,
        "UploadType": ComplianceUploadTypeType,
    },
    total=False,
)


class PutComplianceItemsRequestRequestTypeDef(
    _RequiredPutComplianceItemsRequestRequestTypeDef,
    _OptionalPutComplianceItemsRequestRequestTypeDef,
):
    pass


ListComplianceItemsRequestRequestTypeDef = TypedDict(
    "ListComplianceItemsRequestRequestTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "ResourceIds": Sequence[str],
        "ResourceTypes": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListComplianceSummariesRequestRequestTypeDef = TypedDict(
    "ListComplianceSummariesRequestRequestTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListResourceComplianceSummariesRequestRequestTypeDef = TypedDict(
    "ListResourceComplianceSummariesRequestRequestTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

CompliantSummaryTypeDef = TypedDict(
    "CompliantSummaryTypeDef",
    {
        "CompliantCount": int,
        "SeveritySummary": SeveritySummaryTypeDef,
    },
    total=False,
)

NonCompliantSummaryTypeDef = TypedDict(
    "NonCompliantSummaryTypeDef",
    {
        "NonCompliantCount": int,
        "SeveritySummary": SeveritySummaryTypeDef,
    },
    total=False,
)

_RequiredCreateActivationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateActivationRequestRequestTypeDef",
    {
        "IamRole": str,
    },
)
_OptionalCreateActivationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateActivationRequestRequestTypeDef",
    {
        "Description": str,
        "DefaultInstanceName": str,
        "RegistrationLimit": int,
        "ExpirationDate": Union[datetime, str],
        "Tags": Sequence[TagTypeDef],
        "RegistrationMetadata": Sequence[RegistrationMetadataItemTypeDef],
    },
    total=False,
)


class CreateActivationRequestRequestTypeDef(
    _RequiredCreateActivationRequestRequestTypeDef, _OptionalCreateActivationRequestRequestTypeDef
):
    pass


_RequiredCreateDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDocumentRequestRequestTypeDef",
    {
        "Content": str,
        "Name": str,
    },
)
_OptionalCreateDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDocumentRequestRequestTypeDef",
    {
        "Requires": Sequence[DocumentRequiresTypeDef],
        "Attachments": Sequence[AttachmentsSourceTypeDef],
        "DisplayName": str,
        "VersionName": str,
        "DocumentType": DocumentTypeType,
        "DocumentFormat": DocumentFormatType,
        "TargetType": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDocumentRequestRequestTypeDef(
    _RequiredCreateDocumentRequestRequestTypeDef, _OptionalCreateDocumentRequestRequestTypeDef
):
    pass


DocumentIdentifierTypeDef = TypedDict(
    "DocumentIdentifierTypeDef",
    {
        "Name": str,
        "CreatedDate": datetime,
        "DisplayName": str,
        "Owner": str,
        "VersionName": str,
        "PlatformTypes": List[PlatformTypeType],
        "DocumentVersion": str,
        "DocumentType": DocumentTypeType,
        "SchemaVersion": str,
        "DocumentFormat": DocumentFormatType,
        "TargetType": str,
        "Tags": List[TagTypeDef],
        "Requires": List[DocumentRequiresTypeDef],
        "ReviewStatus": ReviewStatusType,
        "Author": str,
    },
    total=False,
)

GetDocumentResultTypeDef = TypedDict(
    "GetDocumentResultTypeDef",
    {
        "Name": str,
        "CreatedDate": datetime,
        "DisplayName": str,
        "VersionName": str,
        "DocumentVersion": str,
        "Status": DocumentStatusType,
        "StatusInformation": str,
        "Content": str,
        "DocumentType": DocumentTypeType,
        "DocumentFormat": DocumentFormatType,
        "Requires": List[DocumentRequiresTypeDef],
        "AttachmentsContent": List[AttachmentContentTypeDef],
        "ReviewStatus": ReviewStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OpsItemSummaryTypeDef = TypedDict(
    "OpsItemSummaryTypeDef",
    {
        "CreatedBy": str,
        "CreatedTime": datetime,
        "LastModifiedBy": str,
        "LastModifiedTime": datetime,
        "Priority": int,
        "Source": str,
        "Status": OpsItemStatusType,
        "OpsItemId": str,
        "Title": str,
        "OperationalData": Dict[str, OpsItemDataValueTypeDef],
        "Category": str,
        "Severity": str,
        "OpsItemType": str,
        "ActualStartTime": datetime,
        "ActualEndTime": datetime,
        "PlannedStartTime": datetime,
        "PlannedEndTime": datetime,
    },
    total=False,
)

_RequiredCreateOpsItemRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOpsItemRequestRequestTypeDef",
    {
        "Description": str,
        "Source": str,
        "Title": str,
    },
)
_OptionalCreateOpsItemRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOpsItemRequestRequestTypeDef",
    {
        "OpsItemType": str,
        "OperationalData": Mapping[str, OpsItemDataValueTypeDef],
        "Notifications": Sequence[OpsItemNotificationTypeDef],
        "Priority": int,
        "RelatedOpsItems": Sequence[RelatedOpsItemTypeDef],
        "Tags": Sequence[TagTypeDef],
        "Category": str,
        "Severity": str,
        "ActualStartTime": Union[datetime, str],
        "ActualEndTime": Union[datetime, str],
        "PlannedStartTime": Union[datetime, str],
        "PlannedEndTime": Union[datetime, str],
    },
    total=False,
)


class CreateOpsItemRequestRequestTypeDef(
    _RequiredCreateOpsItemRequestRequestTypeDef, _OptionalCreateOpsItemRequestRequestTypeDef
):
    pass


OpsItemTypeDef = TypedDict(
    "OpsItemTypeDef",
    {
        "CreatedBy": str,
        "OpsItemType": str,
        "CreatedTime": datetime,
        "Description": str,
        "LastModifiedBy": str,
        "LastModifiedTime": datetime,
        "Notifications": List[OpsItemNotificationTypeDef],
        "Priority": int,
        "RelatedOpsItems": List[RelatedOpsItemTypeDef],
        "Status": OpsItemStatusType,
        "OpsItemId": str,
        "Version": str,
        "Title": str,
        "Source": str,
        "OperationalData": Dict[str, OpsItemDataValueTypeDef],
        "Category": str,
        "Severity": str,
        "ActualStartTime": datetime,
        "ActualEndTime": datetime,
        "PlannedStartTime": datetime,
        "PlannedEndTime": datetime,
    },
    total=False,
)

_RequiredUpdateOpsItemRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOpsItemRequestRequestTypeDef",
    {
        "OpsItemId": str,
    },
)
_OptionalUpdateOpsItemRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOpsItemRequestRequestTypeDef",
    {
        "Description": str,
        "OperationalData": Mapping[str, OpsItemDataValueTypeDef],
        "OperationalDataToDelete": Sequence[str],
        "Notifications": Sequence[OpsItemNotificationTypeDef],
        "Priority": int,
        "RelatedOpsItems": Sequence[RelatedOpsItemTypeDef],
        "Status": OpsItemStatusType,
        "Title": str,
        "Category": str,
        "Severity": str,
        "ActualStartTime": Union[datetime, str],
        "ActualEndTime": Union[datetime, str],
        "PlannedStartTime": Union[datetime, str],
        "PlannedEndTime": Union[datetime, str],
    },
    total=False,
)


class UpdateOpsItemRequestRequestTypeDef(
    _RequiredUpdateOpsItemRequestRequestTypeDef, _OptionalUpdateOpsItemRequestRequestTypeDef
):
    pass


_RequiredCreateOpsMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOpsMetadataRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalCreateOpsMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOpsMetadataRequestRequestTypeDef",
    {
        "Metadata": Mapping[str, MetadataValueTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateOpsMetadataRequestRequestTypeDef(
    _RequiredCreateOpsMetadataRequestRequestTypeDef, _OptionalCreateOpsMetadataRequestRequestTypeDef
):
    pass


GetOpsMetadataResultTypeDef = TypedDict(
    "GetOpsMetadataResultTypeDef",
    {
        "ResourceId": str,
        "Metadata": Dict[str, MetadataValueTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateOpsMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOpsMetadataRequestRequestTypeDef",
    {
        "OpsMetadataArn": str,
    },
)
_OptionalUpdateOpsMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOpsMetadataRequestRequestTypeDef",
    {
        "MetadataToUpdate": Mapping[str, MetadataValueTypeDef],
        "KeysToDelete": Sequence[str],
    },
    total=False,
)


class UpdateOpsMetadataRequestRequestTypeDef(
    _RequiredUpdateOpsMetadataRequestRequestTypeDef, _OptionalUpdateOpsMetadataRequestRequestTypeDef
):
    pass


DescribeActivationsRequestRequestTypeDef = TypedDict(
    "DescribeActivationsRequestRequestTypeDef",
    {
        "Filters": Sequence[DescribeActivationsFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeActivationsRequestDescribeActivationsPaginateTypeDef = TypedDict(
    "DescribeActivationsRequestDescribeActivationsPaginateTypeDef",
    {
        "Filters": Sequence[DescribeActivationsFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef = TypedDict(
    "_RequiredDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef",
    {
        "AssociationId": str,
        "ExecutionId": str,
    },
)
_OptionalDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef = TypedDict(
    "_OptionalDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef",
    {
        "Filters": Sequence[AssociationExecutionTargetsFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef(
    _RequiredDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef,
    _OptionalDescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef,
):
    pass


_RequiredDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef = (
    TypedDict(
        "_RequiredDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef",
        {
            "AssociationId": str,
        },
    )
)
_OptionalDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef = (
    TypedDict(
        "_OptionalDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef",
        {
            "Filters": Sequence[AssociationExecutionFilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)


class DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef(
    _RequiredDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef,
    _OptionalDescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef,
):
    pass


DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef = TypedDict(
    "DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef",
    {
        "Filters": Sequence[AutomationExecutionFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef = TypedDict(
    "_RequiredDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef = TypedDict(
    "_OptionalDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef(
    _RequiredDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef,
    _OptionalDescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef,
):
    pass


_RequiredDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef = TypedDict(
    "_RequiredDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef",
    {
        "BaselineId": str,
    },
)
_OptionalDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef = TypedDict(
    "_OptionalDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef(
    _RequiredDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef,
    _OptionalDescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef,
):
    pass


_RequiredDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef = TypedDict(
    "_RequiredDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef = TypedDict(
    "_OptionalDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef(
    _RequiredDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef,
    _OptionalDescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef,
):
    pass


_RequiredDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef",
    {
        "InstanceIds": Sequence[str],
    },
)
_OptionalDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef(
    _RequiredDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef,
    _OptionalDescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef,
):
    pass


DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef = TypedDict(
    "DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef",
    {
        "DeletionId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef",
    {
        "Targets": Sequence[TargetTypeDef],
        "ResourceType": MaintenanceWindowResourceTypeType,
    },
)
_OptionalDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef,
):
    pass


_RequiredDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef = TypedDict(
    "_RequiredDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
        "Property": PatchPropertyType,
    },
)
_OptionalDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef = TypedDict(
    "_OptionalDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef",
    {
        "PatchSet": PatchSetType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef(
    _RequiredDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef,
    _OptionalDescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef,
):
    pass


GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef = TypedDict(
    "GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef",
    {
        "TypeName": str,
        "Aggregator": bool,
        "SubType": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef = TypedDict(
    "_RequiredGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef = TypedDict(
    "_OptionalGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef",
    {
        "WithDecryption": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef(
    _RequiredGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef,
    _OptionalGetParameterHistoryRequestGetParameterHistoryPaginateTypeDef,
):
    pass


_RequiredListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef = TypedDict(
    "_RequiredListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef = TypedDict(
    "_OptionalListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef(
    _RequiredListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef,
    _OptionalListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef,
):
    pass


ListAssociationsRequestListAssociationsPaginateTypeDef = TypedDict(
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    {
        "AssociationFilterList": Sequence[AssociationFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef = TypedDict(
    "ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "Filters": Sequence[CommandFilterTypeDef],
        "Details": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCommandsRequestListCommandsPaginateTypeDef = TypedDict(
    "ListCommandsRequestListCommandsPaginateTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
        "Filters": Sequence[CommandFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListComplianceItemsRequestListComplianceItemsPaginateTypeDef = TypedDict(
    "ListComplianceItemsRequestListComplianceItemsPaginateTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "ResourceIds": Sequence[str],
        "ResourceTypes": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef = TypedDict(
    "ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef = TypedDict(
    "_RequiredListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef",
    {
        "Name": str,
    },
)
_OptionalListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef = TypedDict(
    "_OptionalListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef(
    _RequiredListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef,
    _OptionalListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef,
):
    pass


ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef = TypedDict(
    "ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef",
    {
        "Filters": Sequence[ComplianceStringFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef = TypedDict(
    "ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef",
    {
        "SyncType": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef",
    {
        "AutomationExecutionId": str,
    },
)
_OptionalDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef",
    {
        "Filters": Sequence[StepExecutionFilterTypeDef],
        "ReverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef(
    _RequiredDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef,
    _OptionalDescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef,
):
    pass


_RequiredDescribeAutomationStepExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAutomationStepExecutionsRequestRequestTypeDef",
    {
        "AutomationExecutionId": str,
    },
)
_OptionalDescribeAutomationStepExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAutomationStepExecutionsRequestRequestTypeDef",
    {
        "Filters": Sequence[StepExecutionFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
        "ReverseOrder": bool,
    },
    total=False,
)


class DescribeAutomationStepExecutionsRequestRequestTypeDef(
    _RequiredDescribeAutomationStepExecutionsRequestRequestTypeDef,
    _OptionalDescribeAutomationStepExecutionsRequestRequestTypeDef,
):
    pass


DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef = TypedDict(
    "DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAvailablePatchesRequestRequestTypeDef = TypedDict(
    "DescribeAvailablePatchesRequestRequestTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef(
    _RequiredDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef,
    _OptionalDescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef,
):
    pass


_RequiredDescribeInstancePatchesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDescribeInstancePatchesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchesRequestRequestTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeInstancePatchesRequestRequestTypeDef(
    _RequiredDescribeInstancePatchesRequestRequestTypeDef,
    _OptionalDescribeInstancePatchesRequestRequestTypeDef,
):
    pass


DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef = (
    TypedDict(
        "DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef",
        {
            "WindowId": str,
            "Targets": Sequence[TargetTypeDef],
            "ResourceType": MaintenanceWindowResourceTypeType,
            "Filters": Sequence[PatchOrchestratorFilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

DescribeMaintenanceWindowScheduleRequestRequestTypeDef = TypedDict(
    "DescribeMaintenanceWindowScheduleRequestRequestTypeDef",
    {
        "WindowId": str,
        "Targets": Sequence[TargetTypeDef],
        "ResourceType": MaintenanceWindowResourceTypeType,
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef = TypedDict(
    "DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePatchBaselinesRequestRequestTypeDef = TypedDict(
    "DescribePatchBaselinesRequestRequestTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef = TypedDict(
    "DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef",
    {
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePatchGroupsRequestRequestTypeDef = TypedDict(
    "DescribePatchGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "Filters": Sequence[PatchOrchestratorFilterTypeDef],
        "NextToken": str,
    },
    total=False,
)

DescribeAvailablePatchesResultTypeDef = TypedDict(
    "DescribeAvailablePatchesResultTypeDef",
    {
        "Patches": List[PatchTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEffectiveInstanceAssociationsResultTypeDef = TypedDict(
    "DescribeEffectiveInstanceAssociationsResultTypeDef",
    {
        "Associations": List[InstanceAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef = TypedDict(
    "DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef",
    {
        "InstanceInformationFilterList": Sequence[InstanceInformationFilterTypeDef],
        "Filters": Sequence[InstanceInformationStringFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeInstanceInformationRequestRequestTypeDef = TypedDict(
    "DescribeInstanceInformationRequestRequestTypeDef",
    {
        "InstanceInformationFilterList": Sequence[InstanceInformationFilterTypeDef],
        "Filters": Sequence[InstanceInformationStringFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef",
    {
        "PatchGroup": str,
    },
)
_OptionalDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef",
    {
        "Filters": Sequence[InstancePatchStateFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef(
    _RequiredDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef,
    _OptionalDescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef,
):
    pass


_RequiredDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef",
    {
        "PatchGroup": str,
    },
)
_OptionalDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef",
    {
        "Filters": Sequence[InstancePatchStateFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef(
    _RequiredDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef,
    _OptionalDescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef,
):
    pass


DescribeInstancePatchStatesForPatchGroupResultTypeDef = TypedDict(
    "DescribeInstancePatchStatesForPatchGroupResultTypeDef",
    {
        "InstancePatchStates": List[InstancePatchStateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstancePatchStatesResultTypeDef = TypedDict(
    "DescribeInstancePatchStatesResultTypeDef",
    {
        "InstancePatchStates": List[InstancePatchStateTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstancePatchesResultTypeDef = TypedDict(
    "DescribeInstancePatchesResultTypeDef",
    {
        "Patches": List[PatchComplianceDataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef",
    {
        "WindowExecutionId": str,
        "TaskId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
        "TaskId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef",
    {
        "WindowExecutionId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef",
    {
        "WindowExecutionId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowExecutionsRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowExecutionsRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowExecutionsRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowExecutionsRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowExecutionsRequestRequestTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowTargetsRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowTargetsRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowTargetsRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowTargetsRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowTargetsRequestRequestTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef(
    _RequiredDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef,
    _OptionalDescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef,
):
    pass


_RequiredDescribeMaintenanceWindowTasksRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMaintenanceWindowTasksRequestRequestTypeDef",
    {
        "WindowId": str,
    },
)
_OptionalDescribeMaintenanceWindowTasksRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMaintenanceWindowTasksRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeMaintenanceWindowTasksRequestRequestTypeDef(
    _RequiredDescribeMaintenanceWindowTasksRequestRequestTypeDef,
    _OptionalDescribeMaintenanceWindowTasksRequestRequestTypeDef,
):
    pass


DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef = TypedDict(
    "DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeMaintenanceWindowsRequestRequestTypeDef = TypedDict(
    "DescribeMaintenanceWindowsRequestRequestTypeDef",
    {
        "Filters": Sequence[MaintenanceWindowFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef",
    {
        "WindowExecutionTaskInvocationIdentities": List[
            MaintenanceWindowExecutionTaskInvocationIdentityTypeDef
        ],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowExecutionTasksResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowExecutionTasksResultTypeDef",
    {
        "WindowExecutionTaskIdentities": List[MaintenanceWindowExecutionTaskIdentityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowExecutionsResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowExecutionsResultTypeDef",
    {
        "WindowExecutions": List[MaintenanceWindowExecutionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowScheduleResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowScheduleResultTypeDef",
    {
        "ScheduledWindowExecutions": List[ScheduledWindowExecutionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowsForTargetResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowsForTargetResultTypeDef",
    {
        "WindowIdentities": List[MaintenanceWindowIdentityForTargetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowsResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowsResultTypeDef",
    {
        "WindowIdentities": List[MaintenanceWindowIdentityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef = TypedDict(
    "DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef",
    {
        "OpsItemFilters": Sequence[OpsItemFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeOpsItemsRequestRequestTypeDef = TypedDict(
    "DescribeOpsItemsRequestRequestTypeDef",
    {
        "OpsItemFilters": Sequence[OpsItemFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredGetParametersByPathRequestGetParametersByPathPaginateTypeDef = TypedDict(
    "_RequiredGetParametersByPathRequestGetParametersByPathPaginateTypeDef",
    {
        "Path": str,
    },
)
_OptionalGetParametersByPathRequestGetParametersByPathPaginateTypeDef = TypedDict(
    "_OptionalGetParametersByPathRequestGetParametersByPathPaginateTypeDef",
    {
        "Recursive": bool,
        "ParameterFilters": Sequence[ParameterStringFilterTypeDef],
        "WithDecryption": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetParametersByPathRequestGetParametersByPathPaginateTypeDef(
    _RequiredGetParametersByPathRequestGetParametersByPathPaginateTypeDef,
    _OptionalGetParametersByPathRequestGetParametersByPathPaginateTypeDef,
):
    pass


_RequiredGetParametersByPathRequestRequestTypeDef = TypedDict(
    "_RequiredGetParametersByPathRequestRequestTypeDef",
    {
        "Path": str,
    },
)
_OptionalGetParametersByPathRequestRequestTypeDef = TypedDict(
    "_OptionalGetParametersByPathRequestRequestTypeDef",
    {
        "Recursive": bool,
        "ParameterFilters": Sequence[ParameterStringFilterTypeDef],
        "WithDecryption": bool,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetParametersByPathRequestRequestTypeDef(
    _RequiredGetParametersByPathRequestRequestTypeDef,
    _OptionalGetParametersByPathRequestRequestTypeDef,
):
    pass


DescribeParametersRequestDescribeParametersPaginateTypeDef = TypedDict(
    "DescribeParametersRequestDescribeParametersPaginateTypeDef",
    {
        "Filters": Sequence[ParametersFilterTypeDef],
        "ParameterFilters": Sequence[ParameterStringFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeParametersRequestRequestTypeDef = TypedDict(
    "DescribeParametersRequestRequestTypeDef",
    {
        "Filters": Sequence[ParametersFilterTypeDef],
        "ParameterFilters": Sequence[ParameterStringFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribePatchBaselinesResultTypeDef = TypedDict(
    "DescribePatchBaselinesResultTypeDef",
    {
        "BaselineIdentities": List[PatchBaselineIdentityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PatchGroupPatchBaselineMappingTypeDef = TypedDict(
    "PatchGroupPatchBaselineMappingTypeDef",
    {
        "PatchGroup": str,
        "BaselineIdentity": PatchBaselineIdentityTypeDef,
    },
    total=False,
)

_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "State": SessionStateType,
    },
)
_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "Filters": Sequence[SessionFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeSessionsRequestDescribeSessionsPaginateTypeDef(
    _RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    _OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
):
    pass


_RequiredDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestRequestTypeDef",
    {
        "State": SessionStateType,
    },
)
_OptionalDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[SessionFilterTypeDef],
    },
    total=False,
)


class DescribeSessionsRequestRequestTypeDef(
    _RequiredDescribeSessionsRequestRequestTypeDef, _OptionalDescribeSessionsRequestRequestTypeDef
):
    pass


UpdateDocumentDefaultVersionResultTypeDef = TypedDict(
    "UpdateDocumentDefaultVersionResultTypeDef",
    {
        "Description": DocumentDefaultVersionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DocumentDescriptionTypeDef = TypedDict(
    "DocumentDescriptionTypeDef",
    {
        "Sha1": str,
        "Hash": str,
        "HashType": DocumentHashTypeType,
        "Name": str,
        "DisplayName": str,
        "VersionName": str,
        "Owner": str,
        "CreatedDate": datetime,
        "Status": DocumentStatusType,
        "StatusInformation": str,
        "DocumentVersion": str,
        "Description": str,
        "Parameters": List[DocumentParameterTypeDef],
        "PlatformTypes": List[PlatformTypeType],
        "DocumentType": DocumentTypeType,
        "SchemaVersion": str,
        "LatestVersion": str,
        "DefaultVersion": str,
        "DocumentFormat": DocumentFormatType,
        "TargetType": str,
        "Tags": List[TagTypeDef],
        "AttachmentsInformation": List[AttachmentInformationTypeDef],
        "Requires": List[DocumentRequiresTypeDef],
        "Author": str,
        "ReviewInformation": List[ReviewInformationTypeDef],
        "ApprovedVersion": str,
        "PendingReviewVersion": str,
        "ReviewStatus": ReviewStatusType,
        "Category": List[str],
        "CategoryEnum": List[str],
    },
    total=False,
)

ListDocumentsRequestListDocumentsPaginateTypeDef = TypedDict(
    "ListDocumentsRequestListDocumentsPaginateTypeDef",
    {
        "DocumentFilterList": Sequence[DocumentFilterTypeDef],
        "Filters": Sequence[DocumentKeyValuesFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDocumentsRequestRequestTypeDef = TypedDict(
    "ListDocumentsRequestRequestTypeDef",
    {
        "DocumentFilterList": Sequence[DocumentFilterTypeDef],
        "Filters": Sequence[DocumentKeyValuesFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DocumentReviewerResponseSourceTypeDef = TypedDict(
    "DocumentReviewerResponseSourceTypeDef",
    {
        "CreateTime": datetime,
        "UpdatedTime": datetime,
        "ReviewStatus": ReviewStatusType,
        "Comment": List[DocumentReviewCommentSourceTypeDef],
        "Reviewer": str,
    },
    total=False,
)

_RequiredDocumentReviewsTypeDef = TypedDict(
    "_RequiredDocumentReviewsTypeDef",
    {
        "Action": DocumentReviewActionType,
    },
)
_OptionalDocumentReviewsTypeDef = TypedDict(
    "_OptionalDocumentReviewsTypeDef",
    {
        "Comment": Sequence[DocumentReviewCommentSourceTypeDef],
    },
    total=False,
)


class DocumentReviewsTypeDef(_RequiredDocumentReviewsTypeDef, _OptionalDocumentReviewsTypeDef):
    pass


ListDocumentVersionsResultTypeDef = TypedDict(
    "ListDocumentVersionsResultTypeDef",
    {
        "DocumentVersions": List[DocumentVersionInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EffectivePatchTypeDef = TypedDict(
    "EffectivePatchTypeDef",
    {
        "Patch": PatchTypeDef,
        "PatchStatus": PatchStatusTypeDef,
    },
    total=False,
)

StepExecutionTypeDef = TypedDict(
    "StepExecutionTypeDef",
    {
        "StepName": str,
        "Action": str,
        "TimeoutSeconds": int,
        "OnFailure": str,
        "MaxAttempts": int,
        "ExecutionStartTime": datetime,
        "ExecutionEndTime": datetime,
        "StepStatus": AutomationExecutionStatusType,
        "ResponseCode": str,
        "Inputs": Dict[str, str],
        "Outputs": Dict[str, List[str]],
        "Response": str,
        "FailureMessage": str,
        "FailureDetails": FailureDetailsTypeDef,
        "StepExecutionId": str,
        "OverriddenParameters": Dict[str, List[str]],
        "IsEnd": bool,
        "NextStep": str,
        "IsCritical": bool,
        "ValidNextSteps": List[str],
        "Targets": List[TargetTypeDef],
        "TargetLocation": TargetLocationTypeDef,
    },
    total=False,
)

_RequiredGetCommandInvocationRequestCommandExecutedWaitTypeDef = TypedDict(
    "_RequiredGetCommandInvocationRequestCommandExecutedWaitTypeDef",
    {
        "CommandId": str,
        "InstanceId": str,
    },
)
_OptionalGetCommandInvocationRequestCommandExecutedWaitTypeDef = TypedDict(
    "_OptionalGetCommandInvocationRequestCommandExecutedWaitTypeDef",
    {
        "PluginName": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetCommandInvocationRequestCommandExecutedWaitTypeDef(
    _RequiredGetCommandInvocationRequestCommandExecutedWaitTypeDef,
    _OptionalGetCommandInvocationRequestCommandExecutedWaitTypeDef,
):
    pass


InventoryGroupTypeDef = TypedDict(
    "InventoryGroupTypeDef",
    {
        "Name": str,
        "Filters": Sequence[InventoryFilterTypeDef],
    },
)

_RequiredListInventoryEntriesRequestRequestTypeDef = TypedDict(
    "_RequiredListInventoryEntriesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "TypeName": str,
    },
)
_OptionalListInventoryEntriesRequestRequestTypeDef = TypedDict(
    "_OptionalListInventoryEntriesRequestRequestTypeDef",
    {
        "Filters": Sequence[InventoryFilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListInventoryEntriesRequestRequestTypeDef(
    _RequiredListInventoryEntriesRequestRequestTypeDef,
    _OptionalListInventoryEntriesRequestRequestTypeDef,
):
    pass


GetInventoryRequestGetInventoryPaginateTypeDef = TypedDict(
    "GetInventoryRequestGetInventoryPaginateTypeDef",
    {
        "Filters": Sequence[InventoryFilterTypeDef],
        "Aggregators": Sequence["InventoryAggregatorTypeDef"],
        "ResultAttributes": Sequence[ResultAttributeTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetInventoryRequestRequestTypeDef = TypedDict(
    "GetInventoryRequestRequestTypeDef",
    {
        "Filters": Sequence[InventoryFilterTypeDef],
        "Aggregators": Sequence["InventoryAggregatorTypeDef"],
        "ResultAttributes": Sequence[ResultAttributeTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetMaintenanceWindowExecutionTaskResultTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionTaskResultTypeDef",
    {
        "WindowExecutionId": str,
        "TaskExecutionId": str,
        "TaskArn": str,
        "ServiceRole": str,
        "Type": MaintenanceWindowTaskTypeType,
        "TaskParameters": List[Dict[str, MaintenanceWindowTaskParameterValueExpressionTypeDef]],
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MaintenanceWindowTaskTypeDef = TypedDict(
    "MaintenanceWindowTaskTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
        "TaskArn": str,
        "Type": MaintenanceWindowTaskTypeType,
        "Targets": List[TargetTypeDef],
        "TaskParameters": Dict[str, MaintenanceWindowTaskParameterValueExpressionTypeDef],
        "Priority": int,
        "LoggingInfo": LoggingInfoTypeDef,
        "ServiceRoleArn": str,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "Name": str,
        "Description": str,
        "CutoffBehavior": MaintenanceWindowTaskCutoffBehaviorType,
    },
    total=False,
)

OpsAggregatorTypeDef = TypedDict(
    "OpsAggregatorTypeDef",
    {
        "AggregatorType": str,
        "TypeName": str,
        "AttributeName": str,
        "Values": Mapping[str, str],
        "Filters": Sequence[OpsFilterTypeDef],
        "Aggregators": Sequence[Dict[str, Any]],
    },
    total=False,
)

GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef = TypedDict(
    "GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef",
    {
        "SyncName": str,
        "Filters": Sequence[OpsFilterTypeDef],
        "Aggregators": Sequence["OpsAggregatorTypeDef"],
        "ResultAttributes": Sequence[OpsResultAttributeTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetOpsSummaryRequestRequestTypeDef = TypedDict(
    "GetOpsSummaryRequestRequestTypeDef",
    {
        "SyncName": str,
        "Filters": Sequence[OpsFilterTypeDef],
        "Aggregators": Sequence["OpsAggregatorTypeDef"],
        "ResultAttributes": Sequence[OpsResultAttributeTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetParameterResultTypeDef = TypedDict(
    "GetParameterResultTypeDef",
    {
        "Parameter": ParameterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParametersByPathResultTypeDef = TypedDict(
    "GetParametersByPathResultTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParametersResultTypeDef = TypedDict(
    "GetParametersResultTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "InvalidParameters": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceSettingResultTypeDef = TypedDict(
    "GetServiceSettingResultTypeDef",
    {
        "ServiceSetting": ServiceSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResetServiceSettingResultTypeDef = TypedDict(
    "ResetServiceSettingResultTypeDef",
    {
        "ServiceSetting": ServiceSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceInformationTypeDef = TypedDict(
    "InstanceInformationTypeDef",
    {
        "InstanceId": str,
        "PingStatus": PingStatusType,
        "LastPingDateTime": datetime,
        "AgentVersion": str,
        "IsLatestVersion": bool,
        "PlatformType": PlatformTypeType,
        "PlatformName": str,
        "PlatformVersion": str,
        "ActivationId": str,
        "IamRole": str,
        "RegistrationDate": datetime,
        "ResourceType": ResourceTypeType,
        "Name": str,
        "IPAddress": str,
        "ComputerName": str,
        "AssociationStatus": str,
        "LastAssociationExecutionDate": datetime,
        "LastSuccessfulAssociationExecutionDate": datetime,
        "AssociationOverview": InstanceAggregatedAssociationOverviewTypeDef,
        "SourceId": str,
        "SourceType": SourceTypeType,
    },
    total=False,
)

InstanceAssociationOutputLocationTypeDef = TypedDict(
    "InstanceAssociationOutputLocationTypeDef",
    {
        "S3Location": S3OutputLocationTypeDef,
    },
    total=False,
)

InstanceAssociationOutputUrlTypeDef = TypedDict(
    "InstanceAssociationOutputUrlTypeDef",
    {
        "S3OutputUrl": S3OutputUrlTypeDef,
    },
    total=False,
)

InventoryDeletionSummaryTypeDef = TypedDict(
    "InventoryDeletionSummaryTypeDef",
    {
        "TotalCount": int,
        "RemainingCount": int,
        "SummaryItems": List[InventoryDeletionSummaryItemTypeDef],
    },
    total=False,
)

_RequiredInventoryItemSchemaTypeDef = TypedDict(
    "_RequiredInventoryItemSchemaTypeDef",
    {
        "TypeName": str,
        "Attributes": List[InventoryItemAttributeTypeDef],
    },
)
_OptionalInventoryItemSchemaTypeDef = TypedDict(
    "_OptionalInventoryItemSchemaTypeDef",
    {
        "Version": str,
        "DisplayName": str,
    },
    total=False,
)


class InventoryItemSchemaTypeDef(
    _RequiredInventoryItemSchemaTypeDef, _OptionalInventoryItemSchemaTypeDef
):
    pass


PutInventoryRequestRequestTypeDef = TypedDict(
    "PutInventoryRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Items": Sequence[InventoryItemTypeDef],
    },
)

InventoryResultEntityTypeDef = TypedDict(
    "InventoryResultEntityTypeDef",
    {
        "Id": str,
        "Data": Dict[str, InventoryResultItemTypeDef],
    },
    total=False,
)

ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef = TypedDict(
    "ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef",
    {
        "Filters": Sequence[OpsItemEventFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOpsItemEventsRequestRequestTypeDef = TypedDict(
    "ListOpsItemEventsRequestRequestTypeDef",
    {
        "Filters": Sequence[OpsItemEventFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef = TypedDict(
    "ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef",
    {
        "OpsItemId": str,
        "Filters": Sequence[OpsItemRelatedItemsFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOpsItemRelatedItemsRequestRequestTypeDef = TypedDict(
    "ListOpsItemRelatedItemsRequestRequestTypeDef",
    {
        "OpsItemId": str,
        "Filters": Sequence[OpsItemRelatedItemsFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOpsMetadataRequestListOpsMetadataPaginateTypeDef = TypedDict(
    "ListOpsMetadataRequestListOpsMetadataPaginateTypeDef",
    {
        "Filters": Sequence[OpsMetadataFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOpsMetadataRequestRequestTypeDef = TypedDict(
    "ListOpsMetadataRequestRequestTypeDef",
    {
        "Filters": Sequence[OpsMetadataFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOpsMetadataResultTypeDef = TypedDict(
    "ListOpsMetadataResultTypeDef",
    {
        "OpsMetadataList": List[OpsMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OpsEntityTypeDef = TypedDict(
    "OpsEntityTypeDef",
    {
        "Id": str,
        "Data": Dict[str, OpsEntityItemTypeDef],
    },
    total=False,
)

OpsItemEventSummaryTypeDef = TypedDict(
    "OpsItemEventSummaryTypeDef",
    {
        "OpsItemId": str,
        "EventId": str,
        "Source": str,
        "DetailType": str,
        "Detail": str,
        "CreatedBy": OpsItemIdentityTypeDef,
        "CreatedTime": datetime,
    },
    total=False,
)

OpsItemRelatedItemSummaryTypeDef = TypedDict(
    "OpsItemRelatedItemSummaryTypeDef",
    {
        "OpsItemId": str,
        "AssociationId": str,
        "ResourceType": str,
        "AssociationType": str,
        "ResourceUri": str,
        "CreatedBy": OpsItemIdentityTypeDef,
        "CreatedTime": datetime,
        "LastModifiedBy": OpsItemIdentityTypeDef,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ParameterHistoryTypeDef = TypedDict(
    "ParameterHistoryTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "KeyId": str,
        "LastModifiedDate": datetime,
        "LastModifiedUser": str,
        "Description": str,
        "Value": str,
        "AllowedPattern": str,
        "Version": int,
        "Labels": List[str],
        "Tier": ParameterTierType,
        "Policies": List[ParameterInlinePolicyTypeDef],
        "DataType": str,
    },
    total=False,
)

ParameterMetadataTypeDef = TypedDict(
    "ParameterMetadataTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "KeyId": str,
        "LastModifiedDate": datetime,
        "LastModifiedUser": str,
        "Description": str,
        "AllowedPattern": str,
        "Version": int,
        "Tier": ParameterTierType,
        "Policies": List[ParameterInlinePolicyTypeDef],
        "DataType": str,
    },
    total=False,
)

PatchFilterGroupTypeDef = TypedDict(
    "PatchFilterGroupTypeDef",
    {
        "PatchFilters": Sequence[PatchFilterTypeDef],
    },
)

_RequiredResourceDataSyncAwsOrganizationsSourceTypeDef = TypedDict(
    "_RequiredResourceDataSyncAwsOrganizationsSourceTypeDef",
    {
        "OrganizationSourceType": str,
    },
)
_OptionalResourceDataSyncAwsOrganizationsSourceTypeDef = TypedDict(
    "_OptionalResourceDataSyncAwsOrganizationsSourceTypeDef",
    {
        "OrganizationalUnits": Sequence[ResourceDataSyncOrganizationalUnitTypeDef],
    },
    total=False,
)


class ResourceDataSyncAwsOrganizationsSourceTypeDef(
    _RequiredResourceDataSyncAwsOrganizationsSourceTypeDef,
    _OptionalResourceDataSyncAwsOrganizationsSourceTypeDef,
):
    pass


_RequiredResourceDataSyncS3DestinationTypeDef = TypedDict(
    "_RequiredResourceDataSyncS3DestinationTypeDef",
    {
        "BucketName": str,
        "SyncFormat": Literal["JsonSerDe"],
        "Region": str,
    },
)
_OptionalResourceDataSyncS3DestinationTypeDef = TypedDict(
    "_OptionalResourceDataSyncS3DestinationTypeDef",
    {
        "Prefix": str,
        "AWSKMSKeyARN": str,
        "DestinationDataSharing": ResourceDataSyncDestinationDataSharingTypeDef,
    },
    total=False,
)


class ResourceDataSyncS3DestinationTypeDef(
    _RequiredResourceDataSyncS3DestinationTypeDef, _OptionalResourceDataSyncS3DestinationTypeDef
):
    pass


SessionTypeDef = TypedDict(
    "SessionTypeDef",
    {
        "SessionId": str,
        "Target": str,
        "Status": SessionStatusType,
        "StartDate": datetime,
        "EndDate": datetime,
        "DocumentName": str,
        "Owner": str,
        "Reason": str,
        "Details": str,
        "OutputUrl": SessionManagerOutputUrlTypeDef,
        "MaxSessionDuration": str,
    },
    total=False,
)

DescribeActivationsResultTypeDef = TypedDict(
    "DescribeActivationsResultTypeDef",
    {
        "ActivationList": List[ActivationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociationsResultTypeDef = TypedDict(
    "ListAssociationsResultTypeDef",
    {
        "Associations": List[AssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceWindowTargetsResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowTargetsResultTypeDef",
    {
        "Targets": List[MaintenanceWindowTargetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutomationExecutionMetadataTypeDef = TypedDict(
    "AutomationExecutionMetadataTypeDef",
    {
        "AutomationExecutionId": str,
        "DocumentName": str,
        "DocumentVersion": str,
        "AutomationExecutionStatus": AutomationExecutionStatusType,
        "ExecutionStartTime": datetime,
        "ExecutionEndTime": datetime,
        "ExecutedBy": str,
        "LogFile": str,
        "Outputs": Dict[str, List[str]],
        "Mode": ExecutionModeType,
        "ParentAutomationExecutionId": str,
        "CurrentStepName": str,
        "CurrentAction": str,
        "FailureMessage": str,
        "TargetParameterName": str,
        "Targets": List[TargetTypeDef],
        "TargetMaps": List[Dict[str, List[str]]],
        "ResolvedTargets": ResolvedTargetsTypeDef,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "Target": str,
        "AutomationType": AutomationTypeType,
        "AutomationSubtype": Literal["ChangeRequest"],
        "ScheduledTime": datetime,
        "Runbooks": List[RunbookTypeDef],
        "OpsItemId": str,
        "AssociationId": str,
        "ChangeRequestName": str,
    },
    total=False,
)

_RequiredStartChangeRequestExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartChangeRequestExecutionRequestRequestTypeDef",
    {
        "DocumentName": str,
        "Runbooks": Sequence[RunbookTypeDef],
    },
)
_OptionalStartChangeRequestExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartChangeRequestExecutionRequestRequestTypeDef",
    {
        "ScheduledTime": Union[datetime, str],
        "DocumentVersion": str,
        "Parameters": Mapping[str, Sequence[str]],
        "ChangeRequestName": str,
        "ClientToken": str,
        "AutoApprove": bool,
        "Tags": Sequence[TagTypeDef],
        "ScheduledEndTime": Union[datetime, str],
        "ChangeDetails": str,
    },
    total=False,
)


class StartChangeRequestExecutionRequestRequestTypeDef(
    _RequiredStartChangeRequestExecutionRequestRequestTypeDef,
    _OptionalStartChangeRequestExecutionRequestRequestTypeDef,
):
    pass


DescribeAssociationExecutionTargetsResultTypeDef = TypedDict(
    "DescribeAssociationExecutionTargetsResultTypeDef",
    {
        "AssociationExecutionTargets": List[AssociationExecutionTargetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCommandInvocationsResultTypeDef = TypedDict(
    "ListCommandInvocationsResultTypeDef",
    {
        "CommandInvocations": List[CommandInvocationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCommandsResultTypeDef = TypedDict(
    "ListCommandsResultTypeDef",
    {
        "Commands": List[CommandTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendCommandResultTypeDef = TypedDict(
    "SendCommandResultTypeDef",
    {
        "Command": CommandTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MaintenanceWindowTaskInvocationParametersTypeDef = TypedDict(
    "MaintenanceWindowTaskInvocationParametersTypeDef",
    {
        "RunCommand": MaintenanceWindowRunCommandParametersTypeDef,
        "Automation": MaintenanceWindowAutomationParametersTypeDef,
        "StepFunctions": MaintenanceWindowStepFunctionsParametersTypeDef,
        "Lambda": MaintenanceWindowLambdaParametersTypeDef,
    },
    total=False,
)

ListComplianceItemsResultTypeDef = TypedDict(
    "ListComplianceItemsResultTypeDef",
    {
        "ComplianceItems": List[ComplianceItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComplianceSummaryItemTypeDef = TypedDict(
    "ComplianceSummaryItemTypeDef",
    {
        "ComplianceType": str,
        "CompliantSummary": CompliantSummaryTypeDef,
        "NonCompliantSummary": NonCompliantSummaryTypeDef,
    },
    total=False,
)

ResourceComplianceSummaryItemTypeDef = TypedDict(
    "ResourceComplianceSummaryItemTypeDef",
    {
        "ComplianceType": str,
        "ResourceType": str,
        "ResourceId": str,
        "Status": ComplianceStatusType,
        "OverallSeverity": ComplianceSeverityType,
        "ExecutionSummary": ComplianceExecutionSummaryTypeDef,
        "CompliantSummary": CompliantSummaryTypeDef,
        "NonCompliantSummary": NonCompliantSummaryTypeDef,
    },
    total=False,
)

ListDocumentsResultTypeDef = TypedDict(
    "ListDocumentsResultTypeDef",
    {
        "DocumentIdentifiers": List[DocumentIdentifierTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOpsItemsResponseTypeDef = TypedDict(
    "DescribeOpsItemsResponseTypeDef",
    {
        "NextToken": str,
        "OpsItemSummaries": List[OpsItemSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOpsItemResponseTypeDef = TypedDict(
    "GetOpsItemResponseTypeDef",
    {
        "OpsItem": OpsItemTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePatchGroupsResultTypeDef = TypedDict(
    "DescribePatchGroupsResultTypeDef",
    {
        "Mappings": List[PatchGroupPatchBaselineMappingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDocumentResultTypeDef = TypedDict(
    "CreateDocumentResultTypeDef",
    {
        "DocumentDescription": DocumentDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDocumentResultTypeDef = TypedDict(
    "DescribeDocumentResultTypeDef",
    {
        "Document": DocumentDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDocumentResultTypeDef = TypedDict(
    "UpdateDocumentResultTypeDef",
    {
        "DocumentDescription": DocumentDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DocumentMetadataResponseInfoTypeDef = TypedDict(
    "DocumentMetadataResponseInfoTypeDef",
    {
        "ReviewerResponse": List[DocumentReviewerResponseSourceTypeDef],
    },
    total=False,
)

_RequiredUpdateDocumentMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDocumentMetadataRequestRequestTypeDef",
    {
        "Name": str,
        "DocumentReviews": DocumentReviewsTypeDef,
    },
)
_OptionalUpdateDocumentMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDocumentMetadataRequestRequestTypeDef",
    {
        "DocumentVersion": str,
    },
    total=False,
)


class UpdateDocumentMetadataRequestRequestTypeDef(
    _RequiredUpdateDocumentMetadataRequestRequestTypeDef,
    _OptionalUpdateDocumentMetadataRequestRequestTypeDef,
):
    pass


DescribeEffectivePatchesForPatchBaselineResultTypeDef = TypedDict(
    "DescribeEffectivePatchesForPatchBaselineResultTypeDef",
    {
        "EffectivePatches": List[EffectivePatchTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutomationExecutionTypeDef = TypedDict(
    "AutomationExecutionTypeDef",
    {
        "AutomationExecutionId": str,
        "DocumentName": str,
        "DocumentVersion": str,
        "ExecutionStartTime": datetime,
        "ExecutionEndTime": datetime,
        "AutomationExecutionStatus": AutomationExecutionStatusType,
        "StepExecutions": List[StepExecutionTypeDef],
        "StepExecutionsTruncated": bool,
        "Parameters": Dict[str, List[str]],
        "Outputs": Dict[str, List[str]],
        "FailureMessage": str,
        "Mode": ExecutionModeType,
        "ParentAutomationExecutionId": str,
        "ExecutedBy": str,
        "CurrentStepName": str,
        "CurrentAction": str,
        "TargetParameterName": str,
        "Targets": List[TargetTypeDef],
        "TargetMaps": List[Dict[str, List[str]]],
        "ResolvedTargets": ResolvedTargetsTypeDef,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "Target": str,
        "TargetLocations": List[TargetLocationTypeDef],
        "ProgressCounters": ProgressCountersTypeDef,
        "AutomationSubtype": Literal["ChangeRequest"],
        "ScheduledTime": datetime,
        "Runbooks": List[RunbookTypeDef],
        "OpsItemId": str,
        "AssociationId": str,
        "ChangeRequestName": str,
    },
    total=False,
)

DescribeAutomationStepExecutionsResultTypeDef = TypedDict(
    "DescribeAutomationStepExecutionsResultTypeDef",
    {
        "StepExecutions": List[StepExecutionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InventoryAggregatorTypeDef = TypedDict(
    "InventoryAggregatorTypeDef",
    {
        "Expression": str,
        "Aggregators": Sequence[Dict[str, Any]],
        "Groups": Sequence[InventoryGroupTypeDef],
    },
    total=False,
)

DescribeMaintenanceWindowTasksResultTypeDef = TypedDict(
    "DescribeMaintenanceWindowTasksResultTypeDef",
    {
        "Tasks": List[MaintenanceWindowTaskTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstanceInformationResultTypeDef = TypedDict(
    "DescribeInstanceInformationResultTypeDef",
    {
        "InstanceInformationList": List[InstanceInformationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociationDescriptionTypeDef = TypedDict(
    "AssociationDescriptionTypeDef",
    {
        "Name": str,
        "InstanceId": str,
        "AssociationVersion": str,
        "Date": datetime,
        "LastUpdateAssociationDate": datetime,
        "Status": AssociationStatusTypeDef,
        "Overview": AssociationOverviewTypeDef,
        "DocumentVersion": str,
        "AutomationTargetParameterName": str,
        "Parameters": Dict[str, List[str]],
        "AssociationId": str,
        "Targets": List[TargetTypeDef],
        "ScheduleExpression": str,
        "OutputLocation": InstanceAssociationOutputLocationTypeDef,
        "LastExecutionDate": datetime,
        "LastSuccessfulExecutionDate": datetime,
        "AssociationName": str,
        "MaxErrors": str,
        "MaxConcurrency": str,
        "ComplianceSeverity": AssociationComplianceSeverityType,
        "SyncCompliance": AssociationSyncComplianceType,
        "ApplyOnlyAtCronInterval": bool,
        "CalendarNames": List[str],
        "TargetLocations": List[TargetLocationTypeDef],
        "ScheduleOffset": int,
        "TargetMaps": List[Dict[str, List[str]]],
    },
    total=False,
)

AssociationVersionInfoTypeDef = TypedDict(
    "AssociationVersionInfoTypeDef",
    {
        "AssociationId": str,
        "AssociationVersion": str,
        "CreatedDate": datetime,
        "Name": str,
        "DocumentVersion": str,
        "Parameters": Dict[str, List[str]],
        "Targets": List[TargetTypeDef],
        "ScheduleExpression": str,
        "OutputLocation": InstanceAssociationOutputLocationTypeDef,
        "AssociationName": str,
        "MaxErrors": str,
        "MaxConcurrency": str,
        "ComplianceSeverity": AssociationComplianceSeverityType,
        "SyncCompliance": AssociationSyncComplianceType,
        "ApplyOnlyAtCronInterval": bool,
        "CalendarNames": List[str],
        "TargetLocations": List[TargetLocationTypeDef],
        "ScheduleOffset": int,
        "TargetMaps": List[Dict[str, List[str]]],
    },
    total=False,
)

_RequiredCreateAssociationBatchRequestEntryTypeDef = TypedDict(
    "_RequiredCreateAssociationBatchRequestEntryTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateAssociationBatchRequestEntryTypeDef = TypedDict(
    "_OptionalCreateAssociationBatchRequestEntryTypeDef",
    {
        "InstanceId": str,
        "Parameters": Mapping[str, Sequence[str]],
        "AutomationTargetParameterName": str,
        "DocumentVersion": str,
        "Targets": Sequence[TargetTypeDef],
        "ScheduleExpression": str,
        "OutputLocation": InstanceAssociationOutputLocationTypeDef,
        "AssociationName": str,
        "MaxErrors": str,
        "MaxConcurrency": str,
        "ComplianceSeverity": AssociationComplianceSeverityType,
        "SyncCompliance": AssociationSyncComplianceType,
        "ApplyOnlyAtCronInterval": bool,
        "CalendarNames": Sequence[str],
        "TargetLocations": Sequence[TargetLocationTypeDef],
        "ScheduleOffset": int,
        "TargetMaps": Sequence[Mapping[str, Sequence[str]]],
    },
    total=False,
)


class CreateAssociationBatchRequestEntryTypeDef(
    _RequiredCreateAssociationBatchRequestEntryTypeDef,
    _OptionalCreateAssociationBatchRequestEntryTypeDef,
):
    pass


_RequiredCreateAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssociationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssociationRequestRequestTypeDef",
    {
        "DocumentVersion": str,
        "InstanceId": str,
        "Parameters": Mapping[str, Sequence[str]],
        "Targets": Sequence[TargetTypeDef],
        "ScheduleExpression": str,
        "OutputLocation": InstanceAssociationOutputLocationTypeDef,
        "AssociationName": str,
        "AutomationTargetParameterName": str,
        "MaxErrors": str,
        "MaxConcurrency": str,
        "ComplianceSeverity": AssociationComplianceSeverityType,
        "SyncCompliance": AssociationSyncComplianceType,
        "ApplyOnlyAtCronInterval": bool,
        "CalendarNames": Sequence[str],
        "TargetLocations": Sequence[TargetLocationTypeDef],
        "ScheduleOffset": int,
        "TargetMaps": Sequence[Mapping[str, Sequence[str]]],
    },
    total=False,
)


class CreateAssociationRequestRequestTypeDef(
    _RequiredCreateAssociationRequestRequestTypeDef, _OptionalCreateAssociationRequestRequestTypeDef
):
    pass


_RequiredUpdateAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssociationRequestRequestTypeDef",
    {
        "AssociationId": str,
    },
)
_OptionalUpdateAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssociationRequestRequestTypeDef",
    {
        "Parameters": Mapping[str, Sequence[str]],
        "DocumentVersion": str,
        "ScheduleExpression": str,
        "OutputLocation": InstanceAssociationOutputLocationTypeDef,
        "Name": str,
        "Targets": Sequence[TargetTypeDef],
        "AssociationName": str,
        "AssociationVersion": str,
        "AutomationTargetParameterName": str,
        "MaxErrors": str,
        "MaxConcurrency": str,
        "ComplianceSeverity": AssociationComplianceSeverityType,
        "SyncCompliance": AssociationSyncComplianceType,
        "ApplyOnlyAtCronInterval": bool,
        "CalendarNames": Sequence[str],
        "TargetLocations": Sequence[TargetLocationTypeDef],
        "ScheduleOffset": int,
        "TargetMaps": Sequence[Mapping[str, Sequence[str]]],
    },
    total=False,
)


class UpdateAssociationRequestRequestTypeDef(
    _RequiredUpdateAssociationRequestRequestTypeDef, _OptionalUpdateAssociationRequestRequestTypeDef
):
    pass


InstanceAssociationStatusInfoTypeDef = TypedDict(
    "InstanceAssociationStatusInfoTypeDef",
    {
        "AssociationId": str,
        "Name": str,
        "DocumentVersion": str,
        "AssociationVersion": str,
        "InstanceId": str,
        "ExecutionDate": datetime,
        "Status": str,
        "DetailedStatus": str,
        "ExecutionSummary": str,
        "ErrorCode": str,
        "OutputUrl": InstanceAssociationOutputUrlTypeDef,
        "AssociationName": str,
    },
    total=False,
)

DeleteInventoryResultTypeDef = TypedDict(
    "DeleteInventoryResultTypeDef",
    {
        "DeletionId": str,
        "TypeName": str,
        "DeletionSummary": InventoryDeletionSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InventoryDeletionStatusItemTypeDef = TypedDict(
    "InventoryDeletionStatusItemTypeDef",
    {
        "DeletionId": str,
        "TypeName": str,
        "DeletionStartTime": datetime,
        "LastStatus": InventoryDeletionStatusType,
        "LastStatusMessage": str,
        "DeletionSummary": InventoryDeletionSummaryTypeDef,
        "LastStatusUpdateTime": datetime,
    },
    total=False,
)

GetInventorySchemaResultTypeDef = TypedDict(
    "GetInventorySchemaResultTypeDef",
    {
        "Schemas": List[InventoryItemSchemaTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInventoryResultTypeDef = TypedDict(
    "GetInventoryResultTypeDef",
    {
        "Entities": List[InventoryResultEntityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOpsSummaryResultTypeDef = TypedDict(
    "GetOpsSummaryResultTypeDef",
    {
        "Entities": List[OpsEntityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOpsItemEventsResponseTypeDef = TypedDict(
    "ListOpsItemEventsResponseTypeDef",
    {
        "NextToken": str,
        "Summaries": List[OpsItemEventSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOpsItemRelatedItemsResponseTypeDef = TypedDict(
    "ListOpsItemRelatedItemsResponseTypeDef",
    {
        "NextToken": str,
        "Summaries": List[OpsItemRelatedItemSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParameterHistoryResultTypeDef = TypedDict(
    "GetParameterHistoryResultTypeDef",
    {
        "Parameters": List[ParameterHistoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeParametersResultTypeDef = TypedDict(
    "DescribeParametersResultTypeDef",
    {
        "Parameters": List[ParameterMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPatchRuleTypeDef = TypedDict(
    "_RequiredPatchRuleTypeDef",
    {
        "PatchFilterGroup": PatchFilterGroupTypeDef,
    },
)
_OptionalPatchRuleTypeDef = TypedDict(
    "_OptionalPatchRuleTypeDef",
    {
        "ComplianceLevel": PatchComplianceLevelType,
        "ApproveAfterDays": int,
        "ApproveUntilDate": str,
        "EnableNonSecurity": bool,
    },
    total=False,
)


class PatchRuleTypeDef(_RequiredPatchRuleTypeDef, _OptionalPatchRuleTypeDef):
    pass


_RequiredResourceDataSyncSourceTypeDef = TypedDict(
    "_RequiredResourceDataSyncSourceTypeDef",
    {
        "SourceType": str,
        "SourceRegions": Sequence[str],
    },
)
_OptionalResourceDataSyncSourceTypeDef = TypedDict(
    "_OptionalResourceDataSyncSourceTypeDef",
    {
        "AwsOrganizationsSource": ResourceDataSyncAwsOrganizationsSourceTypeDef,
        "IncludeFutureRegions": bool,
        "EnableAllOpsDataSources": bool,
    },
    total=False,
)


class ResourceDataSyncSourceTypeDef(
    _RequiredResourceDataSyncSourceTypeDef, _OptionalResourceDataSyncSourceTypeDef
):
    pass


ResourceDataSyncSourceWithStateTypeDef = TypedDict(
    "ResourceDataSyncSourceWithStateTypeDef",
    {
        "SourceType": str,
        "AwsOrganizationsSource": ResourceDataSyncAwsOrganizationsSourceTypeDef,
        "SourceRegions": List[str],
        "IncludeFutureRegions": bool,
        "State": str,
        "EnableAllOpsDataSources": bool,
    },
    total=False,
)

DescribeSessionsResponseTypeDef = TypedDict(
    "DescribeSessionsResponseTypeDef",
    {
        "Sessions": List[SessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAutomationExecutionsResultTypeDef = TypedDict(
    "DescribeAutomationExecutionsResultTypeDef",
    {
        "AutomationExecutionMetadataList": List[AutomationExecutionMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMaintenanceWindowTaskResultTypeDef = TypedDict(
    "GetMaintenanceWindowTaskResultTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
        "Targets": List[TargetTypeDef],
        "TaskArn": str,
        "ServiceRoleArn": str,
        "TaskType": MaintenanceWindowTaskTypeType,
        "TaskParameters": Dict[str, MaintenanceWindowTaskParameterValueExpressionTypeDef],
        "TaskInvocationParameters": MaintenanceWindowTaskInvocationParametersTypeDef,
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "LoggingInfo": LoggingInfoTypeDef,
        "Name": str,
        "Description": str,
        "CutoffBehavior": MaintenanceWindowTaskCutoffBehaviorType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRegisterTaskWithMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterTaskWithMaintenanceWindowRequestRequestTypeDef",
    {
        "WindowId": str,
        "TaskArn": str,
        "TaskType": MaintenanceWindowTaskTypeType,
    },
)
_OptionalRegisterTaskWithMaintenanceWindowRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterTaskWithMaintenanceWindowRequestRequestTypeDef",
    {
        "Targets": Sequence[TargetTypeDef],
        "ServiceRoleArn": str,
        "TaskParameters": Mapping[str, MaintenanceWindowTaskParameterValueExpressionTypeDef],
        "TaskInvocationParameters": MaintenanceWindowTaskInvocationParametersTypeDef,
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "LoggingInfo": LoggingInfoTypeDef,
        "Name": str,
        "Description": str,
        "ClientToken": str,
        "CutoffBehavior": MaintenanceWindowTaskCutoffBehaviorType,
    },
    total=False,
)


class RegisterTaskWithMaintenanceWindowRequestRequestTypeDef(
    _RequiredRegisterTaskWithMaintenanceWindowRequestRequestTypeDef,
    _OptionalRegisterTaskWithMaintenanceWindowRequestRequestTypeDef,
):
    pass


_RequiredUpdateMaintenanceWindowTaskRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMaintenanceWindowTaskRequestRequestTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
    },
)
_OptionalUpdateMaintenanceWindowTaskRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMaintenanceWindowTaskRequestRequestTypeDef",
    {
        "Targets": Sequence[TargetTypeDef],
        "TaskArn": str,
        "ServiceRoleArn": str,
        "TaskParameters": Mapping[str, MaintenanceWindowTaskParameterValueExpressionTypeDef],
        "TaskInvocationParameters": MaintenanceWindowTaskInvocationParametersTypeDef,
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "LoggingInfo": LoggingInfoTypeDef,
        "Name": str,
        "Description": str,
        "Replace": bool,
        "CutoffBehavior": MaintenanceWindowTaskCutoffBehaviorType,
    },
    total=False,
)


class UpdateMaintenanceWindowTaskRequestRequestTypeDef(
    _RequiredUpdateMaintenanceWindowTaskRequestRequestTypeDef,
    _OptionalUpdateMaintenanceWindowTaskRequestRequestTypeDef,
):
    pass


UpdateMaintenanceWindowTaskResultTypeDef = TypedDict(
    "UpdateMaintenanceWindowTaskResultTypeDef",
    {
        "WindowId": str,
        "WindowTaskId": str,
        "Targets": List[TargetTypeDef],
        "TaskArn": str,
        "ServiceRoleArn": str,
        "TaskParameters": Dict[str, MaintenanceWindowTaskParameterValueExpressionTypeDef],
        "TaskInvocationParameters": MaintenanceWindowTaskInvocationParametersTypeDef,
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "LoggingInfo": LoggingInfoTypeDef,
        "Name": str,
        "Description": str,
        "CutoffBehavior": MaintenanceWindowTaskCutoffBehaviorType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComplianceSummariesResultTypeDef = TypedDict(
    "ListComplianceSummariesResultTypeDef",
    {
        "ComplianceSummaryItems": List[ComplianceSummaryItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceComplianceSummariesResultTypeDef = TypedDict(
    "ListResourceComplianceSummariesResultTypeDef",
    {
        "ResourceComplianceSummaryItems": List[ResourceComplianceSummaryItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDocumentMetadataHistoryResponseTypeDef = TypedDict(
    "ListDocumentMetadataHistoryResponseTypeDef",
    {
        "Name": str,
        "DocumentVersion": str,
        "Author": str,
        "Metadata": DocumentMetadataResponseInfoTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAutomationExecutionResultTypeDef = TypedDict(
    "GetAutomationExecutionResultTypeDef",
    {
        "AutomationExecution": AutomationExecutionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssociationResultTypeDef = TypedDict(
    "CreateAssociationResultTypeDef",
    {
        "AssociationDescription": AssociationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAssociationResultTypeDef = TypedDict(
    "DescribeAssociationResultTypeDef",
    {
        "AssociationDescription": AssociationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssociationResultTypeDef = TypedDict(
    "UpdateAssociationResultTypeDef",
    {
        "AssociationDescription": AssociationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssociationStatusResultTypeDef = TypedDict(
    "UpdateAssociationStatusResultTypeDef",
    {
        "AssociationDescription": AssociationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociationVersionsResultTypeDef = TypedDict(
    "ListAssociationVersionsResultTypeDef",
    {
        "AssociationVersions": List[AssociationVersionInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssociationBatchRequestRequestTypeDef = TypedDict(
    "CreateAssociationBatchRequestRequestTypeDef",
    {
        "Entries": Sequence[CreateAssociationBatchRequestEntryTypeDef],
    },
)

FailedCreateAssociationTypeDef = TypedDict(
    "FailedCreateAssociationTypeDef",
    {
        "Entry": CreateAssociationBatchRequestEntryTypeDef,
        "Message": str,
        "Fault": FaultType,
    },
    total=False,
)

DescribeInstanceAssociationsStatusResultTypeDef = TypedDict(
    "DescribeInstanceAssociationsStatusResultTypeDef",
    {
        "InstanceAssociationStatusInfos": List[InstanceAssociationStatusInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInventoryDeletionsResultTypeDef = TypedDict(
    "DescribeInventoryDeletionsResultTypeDef",
    {
        "InventoryDeletions": List[InventoryDeletionStatusItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PatchRuleGroupTypeDef = TypedDict(
    "PatchRuleGroupTypeDef",
    {
        "PatchRules": Sequence[PatchRuleTypeDef],
    },
)

_RequiredCreateResourceDataSyncRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResourceDataSyncRequestRequestTypeDef",
    {
        "SyncName": str,
    },
)
_OptionalCreateResourceDataSyncRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResourceDataSyncRequestRequestTypeDef",
    {
        "S3Destination": ResourceDataSyncS3DestinationTypeDef,
        "SyncType": str,
        "SyncSource": ResourceDataSyncSourceTypeDef,
    },
    total=False,
)


class CreateResourceDataSyncRequestRequestTypeDef(
    _RequiredCreateResourceDataSyncRequestRequestTypeDef,
    _OptionalCreateResourceDataSyncRequestRequestTypeDef,
):
    pass


UpdateResourceDataSyncRequestRequestTypeDef = TypedDict(
    "UpdateResourceDataSyncRequestRequestTypeDef",
    {
        "SyncName": str,
        "SyncType": str,
        "SyncSource": ResourceDataSyncSourceTypeDef,
    },
)

ResourceDataSyncItemTypeDef = TypedDict(
    "ResourceDataSyncItemTypeDef",
    {
        "SyncName": str,
        "SyncType": str,
        "SyncSource": ResourceDataSyncSourceWithStateTypeDef,
        "S3Destination": ResourceDataSyncS3DestinationTypeDef,
        "LastSyncTime": datetime,
        "LastSuccessfulSyncTime": datetime,
        "SyncLastModifiedTime": datetime,
        "LastStatus": LastResourceDataSyncStatusType,
        "SyncCreatedTime": datetime,
        "LastSyncStatusMessage": str,
    },
    total=False,
)

CreateAssociationBatchResultTypeDef = TypedDict(
    "CreateAssociationBatchResultTypeDef",
    {
        "Successful": List[AssociationDescriptionTypeDef],
        "Failed": List[FailedCreateAssociationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BaselineOverrideTypeDef = TypedDict(
    "BaselineOverrideTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
        "GlobalFilters": PatchFilterGroupTypeDef,
        "ApprovalRules": PatchRuleGroupTypeDef,
        "ApprovedPatches": Sequence[str],
        "ApprovedPatchesComplianceLevel": PatchComplianceLevelType,
        "RejectedPatches": Sequence[str],
        "RejectedPatchesAction": PatchActionType,
        "ApprovedPatchesEnableNonSecurity": bool,
        "Sources": Sequence[PatchSourceTypeDef],
    },
    total=False,
)

_RequiredCreatePatchBaselineRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePatchBaselineRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreatePatchBaselineRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePatchBaselineRequestRequestTypeDef",
    {
        "OperatingSystem": OperatingSystemType,
        "GlobalFilters": PatchFilterGroupTypeDef,
        "ApprovalRules": PatchRuleGroupTypeDef,
        "ApprovedPatches": Sequence[str],
        "ApprovedPatchesComplianceLevel": PatchComplianceLevelType,
        "ApprovedPatchesEnableNonSecurity": bool,
        "RejectedPatches": Sequence[str],
        "RejectedPatchesAction": PatchActionType,
        "Description": str,
        "Sources": Sequence[PatchSourceTypeDef],
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePatchBaselineRequestRequestTypeDef(
    _RequiredCreatePatchBaselineRequestRequestTypeDef,
    _OptionalCreatePatchBaselineRequestRequestTypeDef,
):
    pass


GetPatchBaselineResultTypeDef = TypedDict(
    "GetPatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "Name": str,
        "OperatingSystem": OperatingSystemType,
        "GlobalFilters": PatchFilterGroupTypeDef,
        "ApprovalRules": PatchRuleGroupTypeDef,
        "ApprovedPatches": List[str],
        "ApprovedPatchesComplianceLevel": PatchComplianceLevelType,
        "ApprovedPatchesEnableNonSecurity": bool,
        "RejectedPatches": List[str],
        "RejectedPatchesAction": PatchActionType,
        "PatchGroups": List[str],
        "CreatedDate": datetime,
        "ModifiedDate": datetime,
        "Description": str,
        "Sources": List[PatchSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdatePatchBaselineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePatchBaselineRequestRequestTypeDef",
    {
        "BaselineId": str,
    },
)
_OptionalUpdatePatchBaselineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePatchBaselineRequestRequestTypeDef",
    {
        "Name": str,
        "GlobalFilters": PatchFilterGroupTypeDef,
        "ApprovalRules": PatchRuleGroupTypeDef,
        "ApprovedPatches": Sequence[str],
        "ApprovedPatchesComplianceLevel": PatchComplianceLevelType,
        "ApprovedPatchesEnableNonSecurity": bool,
        "RejectedPatches": Sequence[str],
        "RejectedPatchesAction": PatchActionType,
        "Description": str,
        "Sources": Sequence[PatchSourceTypeDef],
        "Replace": bool,
    },
    total=False,
)


class UpdatePatchBaselineRequestRequestTypeDef(
    _RequiredUpdatePatchBaselineRequestRequestTypeDef,
    _OptionalUpdatePatchBaselineRequestRequestTypeDef,
):
    pass


UpdatePatchBaselineResultTypeDef = TypedDict(
    "UpdatePatchBaselineResultTypeDef",
    {
        "BaselineId": str,
        "Name": str,
        "OperatingSystem": OperatingSystemType,
        "GlobalFilters": PatchFilterGroupTypeDef,
        "ApprovalRules": PatchRuleGroupTypeDef,
        "ApprovedPatches": List[str],
        "ApprovedPatchesComplianceLevel": PatchComplianceLevelType,
        "ApprovedPatchesEnableNonSecurity": bool,
        "RejectedPatches": List[str],
        "RejectedPatchesAction": PatchActionType,
        "CreatedDate": datetime,
        "ModifiedDate": datetime,
        "Description": str,
        "Sources": List[PatchSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourceDataSyncResultTypeDef = TypedDict(
    "ListResourceDataSyncResultTypeDef",
    {
        "ResourceDataSyncItems": List[ResourceDataSyncItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
        "SnapshotId": str,
    },
)
_OptionalGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef",
    {
        "BaselineOverride": BaselineOverrideTypeDef,
    },
    total=False,
)


class GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef(
    _RequiredGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef,
    _OptionalGetDeployablePatchSnapshotForInstanceRequestRequestTypeDef,
):
    pass
