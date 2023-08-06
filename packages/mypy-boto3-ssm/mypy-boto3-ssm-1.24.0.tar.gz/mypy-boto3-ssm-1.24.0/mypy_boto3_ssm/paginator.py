"""
Type annotations for ssm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm.client import SSMClient
    from mypy_boto3_ssm.paginator import (
        DescribeActivationsPaginator,
        DescribeAssociationExecutionTargetsPaginator,
        DescribeAssociationExecutionsPaginator,
        DescribeAutomationExecutionsPaginator,
        DescribeAutomationStepExecutionsPaginator,
        DescribeAvailablePatchesPaginator,
        DescribeEffectiveInstanceAssociationsPaginator,
        DescribeEffectivePatchesForPatchBaselinePaginator,
        DescribeInstanceAssociationsStatusPaginator,
        DescribeInstanceInformationPaginator,
        DescribeInstancePatchStatesPaginator,
        DescribeInstancePatchStatesForPatchGroupPaginator,
        DescribeInstancePatchesPaginator,
        DescribeInventoryDeletionsPaginator,
        DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
        DescribeMaintenanceWindowExecutionTasksPaginator,
        DescribeMaintenanceWindowExecutionsPaginator,
        DescribeMaintenanceWindowSchedulePaginator,
        DescribeMaintenanceWindowTargetsPaginator,
        DescribeMaintenanceWindowTasksPaginator,
        DescribeMaintenanceWindowsPaginator,
        DescribeMaintenanceWindowsForTargetPaginator,
        DescribeOpsItemsPaginator,
        DescribeParametersPaginator,
        DescribePatchBaselinesPaginator,
        DescribePatchGroupsPaginator,
        DescribePatchPropertiesPaginator,
        DescribeSessionsPaginator,
        GetInventoryPaginator,
        GetInventorySchemaPaginator,
        GetOpsSummaryPaginator,
        GetParameterHistoryPaginator,
        GetParametersByPathPaginator,
        ListAssociationVersionsPaginator,
        ListAssociationsPaginator,
        ListCommandInvocationsPaginator,
        ListCommandsPaginator,
        ListComplianceItemsPaginator,
        ListComplianceSummariesPaginator,
        ListDocumentVersionsPaginator,
        ListDocumentsPaginator,
        ListOpsItemEventsPaginator,
        ListOpsItemRelatedItemsPaginator,
        ListOpsMetadataPaginator,
        ListResourceComplianceSummariesPaginator,
        ListResourceDataSyncPaginator,
    )

    session = Session()
    client: SSMClient = session.client("ssm")

    describe_activations_paginator: DescribeActivationsPaginator = client.get_paginator("describe_activations")
    describe_association_execution_targets_paginator: DescribeAssociationExecutionTargetsPaginator = client.get_paginator("describe_association_execution_targets")
    describe_association_executions_paginator: DescribeAssociationExecutionsPaginator = client.get_paginator("describe_association_executions")
    describe_automation_executions_paginator: DescribeAutomationExecutionsPaginator = client.get_paginator("describe_automation_executions")
    describe_automation_step_executions_paginator: DescribeAutomationStepExecutionsPaginator = client.get_paginator("describe_automation_step_executions")
    describe_available_patches_paginator: DescribeAvailablePatchesPaginator = client.get_paginator("describe_available_patches")
    describe_effective_instance_associations_paginator: DescribeEffectiveInstanceAssociationsPaginator = client.get_paginator("describe_effective_instance_associations")
    describe_effective_patches_for_patch_baseline_paginator: DescribeEffectivePatchesForPatchBaselinePaginator = client.get_paginator("describe_effective_patches_for_patch_baseline")
    describe_instance_associations_status_paginator: DescribeInstanceAssociationsStatusPaginator = client.get_paginator("describe_instance_associations_status")
    describe_instance_information_paginator: DescribeInstanceInformationPaginator = client.get_paginator("describe_instance_information")
    describe_instance_patch_states_paginator: DescribeInstancePatchStatesPaginator = client.get_paginator("describe_instance_patch_states")
    describe_instance_patch_states_for_patch_group_paginator: DescribeInstancePatchStatesForPatchGroupPaginator = client.get_paginator("describe_instance_patch_states_for_patch_group")
    describe_instance_patches_paginator: DescribeInstancePatchesPaginator = client.get_paginator("describe_instance_patches")
    describe_inventory_deletions_paginator: DescribeInventoryDeletionsPaginator = client.get_paginator("describe_inventory_deletions")
    describe_maintenance_window_execution_task_invocations_paginator: DescribeMaintenanceWindowExecutionTaskInvocationsPaginator = client.get_paginator("describe_maintenance_window_execution_task_invocations")
    describe_maintenance_window_execution_tasks_paginator: DescribeMaintenanceWindowExecutionTasksPaginator = client.get_paginator("describe_maintenance_window_execution_tasks")
    describe_maintenance_window_executions_paginator: DescribeMaintenanceWindowExecutionsPaginator = client.get_paginator("describe_maintenance_window_executions")
    describe_maintenance_window_schedule_paginator: DescribeMaintenanceWindowSchedulePaginator = client.get_paginator("describe_maintenance_window_schedule")
    describe_maintenance_window_targets_paginator: DescribeMaintenanceWindowTargetsPaginator = client.get_paginator("describe_maintenance_window_targets")
    describe_maintenance_window_tasks_paginator: DescribeMaintenanceWindowTasksPaginator = client.get_paginator("describe_maintenance_window_tasks")
    describe_maintenance_windows_paginator: DescribeMaintenanceWindowsPaginator = client.get_paginator("describe_maintenance_windows")
    describe_maintenance_windows_for_target_paginator: DescribeMaintenanceWindowsForTargetPaginator = client.get_paginator("describe_maintenance_windows_for_target")
    describe_ops_items_paginator: DescribeOpsItemsPaginator = client.get_paginator("describe_ops_items")
    describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
    describe_patch_baselines_paginator: DescribePatchBaselinesPaginator = client.get_paginator("describe_patch_baselines")
    describe_patch_groups_paginator: DescribePatchGroupsPaginator = client.get_paginator("describe_patch_groups")
    describe_patch_properties_paginator: DescribePatchPropertiesPaginator = client.get_paginator("describe_patch_properties")
    describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
    get_inventory_paginator: GetInventoryPaginator = client.get_paginator("get_inventory")
    get_inventory_schema_paginator: GetInventorySchemaPaginator = client.get_paginator("get_inventory_schema")
    get_ops_summary_paginator: GetOpsSummaryPaginator = client.get_paginator("get_ops_summary")
    get_parameter_history_paginator: GetParameterHistoryPaginator = client.get_paginator("get_parameter_history")
    get_parameters_by_path_paginator: GetParametersByPathPaginator = client.get_paginator("get_parameters_by_path")
    list_association_versions_paginator: ListAssociationVersionsPaginator = client.get_paginator("list_association_versions")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_command_invocations_paginator: ListCommandInvocationsPaginator = client.get_paginator("list_command_invocations")
    list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
    list_compliance_items_paginator: ListComplianceItemsPaginator = client.get_paginator("list_compliance_items")
    list_compliance_summaries_paginator: ListComplianceSummariesPaginator = client.get_paginator("list_compliance_summaries")
    list_document_versions_paginator: ListDocumentVersionsPaginator = client.get_paginator("list_document_versions")
    list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
    list_ops_item_events_paginator: ListOpsItemEventsPaginator = client.get_paginator("list_ops_item_events")
    list_ops_item_related_items_paginator: ListOpsItemRelatedItemsPaginator = client.get_paginator("list_ops_item_related_items")
    list_ops_metadata_paginator: ListOpsMetadataPaginator = client.get_paginator("list_ops_metadata")
    list_resource_compliance_summaries_paginator: ListResourceComplianceSummariesPaginator = client.get_paginator("list_resource_compliance_summaries")
    list_resource_data_sync_paginator: ListResourceDataSyncPaginator = client.get_paginator("list_resource_data_sync")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    MaintenanceWindowResourceTypeType,
    OperatingSystemType,
    PatchPropertyType,
    PatchSetType,
    SessionStateType,
)
from .type_defs import (
    AssociationExecutionFilterTypeDef,
    AssociationExecutionTargetsFilterTypeDef,
    AssociationFilterTypeDef,
    AutomationExecutionFilterTypeDef,
    CommandFilterTypeDef,
    ComplianceStringFilterTypeDef,
    DescribeActivationsFilterTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsResponseTypeDef,
    DocumentFilterTypeDef,
    DocumentKeyValuesFilterTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaResultTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParametersByPathResultTypeDef,
    InstanceInformationFilterTypeDef,
    InstanceInformationStringFilterTypeDef,
    InstancePatchStateFilterTypeDef,
    InventoryAggregatorTypeDef,
    InventoryFilterTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncResultTypeDef,
    MaintenanceWindowFilterTypeDef,
    OpsAggregatorTypeDef,
    OpsFilterTypeDef,
    OpsItemEventFilterTypeDef,
    OpsItemFilterTypeDef,
    OpsItemRelatedItemsFilterTypeDef,
    OpsMetadataFilterTypeDef,
    OpsResultAttributeTypeDef,
    PaginatorConfigTypeDef,
    ParametersFilterTypeDef,
    ParameterStringFilterTypeDef,
    PatchOrchestratorFilterTypeDef,
    ResultAttributeTypeDef,
    SessionFilterTypeDef,
    StepExecutionFilterTypeDef,
    TargetTypeDef,
)

__all__ = (
    "DescribeActivationsPaginator",
    "DescribeAssociationExecutionTargetsPaginator",
    "DescribeAssociationExecutionsPaginator",
    "DescribeAutomationExecutionsPaginator",
    "DescribeAutomationStepExecutionsPaginator",
    "DescribeAvailablePatchesPaginator",
    "DescribeEffectiveInstanceAssociationsPaginator",
    "DescribeEffectivePatchesForPatchBaselinePaginator",
    "DescribeInstanceAssociationsStatusPaginator",
    "DescribeInstanceInformationPaginator",
    "DescribeInstancePatchStatesPaginator",
    "DescribeInstancePatchStatesForPatchGroupPaginator",
    "DescribeInstancePatchesPaginator",
    "DescribeInventoryDeletionsPaginator",
    "DescribeMaintenanceWindowExecutionTaskInvocationsPaginator",
    "DescribeMaintenanceWindowExecutionTasksPaginator",
    "DescribeMaintenanceWindowExecutionsPaginator",
    "DescribeMaintenanceWindowSchedulePaginator",
    "DescribeMaintenanceWindowTargetsPaginator",
    "DescribeMaintenanceWindowTasksPaginator",
    "DescribeMaintenanceWindowsPaginator",
    "DescribeMaintenanceWindowsForTargetPaginator",
    "DescribeOpsItemsPaginator",
    "DescribeParametersPaginator",
    "DescribePatchBaselinesPaginator",
    "DescribePatchGroupsPaginator",
    "DescribePatchPropertiesPaginator",
    "DescribeSessionsPaginator",
    "GetInventoryPaginator",
    "GetInventorySchemaPaginator",
    "GetOpsSummaryPaginator",
    "GetParameterHistoryPaginator",
    "GetParametersByPathPaginator",
    "ListAssociationVersionsPaginator",
    "ListAssociationsPaginator",
    "ListCommandInvocationsPaginator",
    "ListCommandsPaginator",
    "ListComplianceItemsPaginator",
    "ListComplianceSummariesPaginator",
    "ListDocumentVersionsPaginator",
    "ListDocumentsPaginator",
    "ListOpsItemEventsPaginator",
    "ListOpsItemRelatedItemsPaginator",
    "ListOpsMetadataPaginator",
    "ListResourceComplianceSummariesPaginator",
    "ListResourceDataSyncPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeActivations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeactivationspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[DescribeActivationsFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeActivationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeActivations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeactivationspaginator)
        """


class DescribeAssociationExecutionTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutionTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutiontargetspaginator)
    """

    def paginate(
        self,
        *,
        AssociationId: str,
        ExecutionId: str,
        Filters: Sequence[AssociationExecutionTargetsFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAssociationExecutionTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutionTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutiontargetspaginator)
        """


class DescribeAssociationExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutionspaginator)
    """

    def paginate(
        self,
        *,
        AssociationId: str,
        Filters: Sequence[AssociationExecutionFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAssociationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAssociationExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutionspaginator)
        """


class DescribeAutomationExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationexecutionspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[AutomationExecutionFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAutomationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationexecutionspaginator)
        """


class DescribeAutomationStepExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationStepExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationstepexecutionspaginator)
    """

    def paginate(
        self,
        *,
        AutomationExecutionId: str,
        Filters: Sequence[StepExecutionFilterTypeDef] = ...,
        ReverseOrder: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAutomationStepExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAutomationStepExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationstepexecutionspaginator)
        """


class DescribeAvailablePatchesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAvailablePatches)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeavailablepatchespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAvailablePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeAvailablePatches.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeavailablepatchespaginator)
        """


class DescribeEffectiveInstanceAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectiveInstanceAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEffectiveInstanceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectiveInstanceAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
        """


class DescribeEffectivePatchesForPatchBaselinePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
    """

    def paginate(
        self, *, BaselineId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEffectivePatchesForPatchBaselineResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
        """


class DescribeInstanceAssociationsStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceAssociationsStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceassociationsstatuspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstanceAssociationsStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceAssociationsStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceassociationsstatuspaginator)
        """


class DescribeInstanceInformationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceInformation)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceinformationpaginator)
    """

    def paginate(
        self,
        *,
        InstanceInformationFilterList: Sequence[InstanceInformationFilterTypeDef] = ...,
        Filters: Sequence[InstanceInformationStringFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstanceInformationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstanceInformation.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceinformationpaginator)
        """


class DescribeInstancePatchStatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatespaginator)
    """

    def paginate(
        self, *, InstanceIds: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatespaginator)
        """


class DescribeInstancePatchStatesForPatchGroupPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
    """

    def paginate(
        self,
        *,
        PatchGroup: str,
        Filters: Sequence[InstancePatchStateFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchStatesForPatchGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
        """


class DescribeInstancePatchesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatches)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInstancePatches.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchespaginator)
        """


class DescribeInventoryDeletionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInventoryDeletions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinventorydeletionspaginator)
    """

    def paginate(
        self, *, DeletionId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInventoryDeletionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeInventoryDeletions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinventorydeletionspaginator)
        """


class DescribeMaintenanceWindowExecutionTaskInvocationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
    """

    def paginate(
        self,
        *,
        WindowExecutionId: str,
        TaskId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
        """


class DescribeMaintenanceWindowExecutionTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
    """

    def paginate(
        self,
        *,
        WindowExecutionId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
        """


class DescribeMaintenanceWindowExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutionspaginator)
    """

    def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutionspaginator)
        """


class DescribeMaintenanceWindowSchedulePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowSchedule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowschedulepaginator)
    """

    def paginate(
        self,
        *,
        WindowId: str = ...,
        Targets: Sequence[TargetTypeDef] = ...,
        ResourceType: MaintenanceWindowResourceTypeType = ...,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowScheduleResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowSchedule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowschedulepaginator)
        """


class DescribeMaintenanceWindowTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtargetspaginator)
    """

    def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtargetspaginator)
        """


class DescribeMaintenanceWindowTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtaskspaginator)
    """

    def paginate(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtaskspaginator)
        """


class DescribeMaintenanceWindowsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindows)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindows.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowspaginator)
        """


class DescribeMaintenanceWindowsForTargetPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
    """

    def paginate(
        self,
        *,
        Targets: Sequence[TargetTypeDef],
        ResourceType: MaintenanceWindowResourceTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMaintenanceWindowsForTargetResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
        """


class DescribeOpsItemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeOpsItems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeopsitemspaginator)
    """

    def paginate(
        self,
        *,
        OpsItemFilters: Sequence[OpsItemFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOpsItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeOpsItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeopsitemspaginator)
        """


class DescribeParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeParameters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeparameterspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ParametersFilterTypeDef] = ...,
        ParameterFilters: Sequence[ParameterStringFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeParameters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeparameterspaginator)
        """


class DescribePatchBaselinesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchBaselines)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchbaselinespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchBaselinesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchBaselines.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchbaselinespaginator)
        """


class DescribePatchGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchgroupspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchgroupspaginator)
        """


class DescribePatchPropertiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchProperties)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchpropertiespaginator)
    """

    def paginate(
        self,
        *,
        OperatingSystem: OperatingSystemType,
        Property: PatchPropertyType,
        PatchSet: PatchSetType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePatchPropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribePatchProperties.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchpropertiespaginator)
        """


class DescribeSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeSessions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describesessionspaginator)
    """

    def paginate(
        self,
        *,
        State: SessionStateType,
        Filters: Sequence[SessionFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.DescribeSessions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describesessionspaginator)
        """


class GetInventoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventorypaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[InventoryFilterTypeDef] = ...,
        Aggregators: Sequence["InventoryAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence[ResultAttributeTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInventoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventorypaginator)
        """


class GetInventorySchemaPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventorySchema)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventoryschemapaginator)
    """

    def paginate(
        self,
        *,
        TypeName: str = ...,
        Aggregator: bool = ...,
        SubType: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInventorySchemaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetInventorySchema.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventoryschemapaginator)
        """


class GetOpsSummaryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetOpsSummary)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getopssummarypaginator)
    """

    def paginate(
        self,
        *,
        SyncName: str = ...,
        Filters: Sequence[OpsFilterTypeDef] = ...,
        Aggregators: Sequence["OpsAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence[OpsResultAttributeTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetOpsSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetOpsSummary.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getopssummarypaginator)
        """


class GetParameterHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParameterHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparameterhistorypaginator)
    """

    def paginate(
        self,
        *,
        Name: str,
        WithDecryption: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetParameterHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParameterHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparameterhistorypaginator)
        """


class GetParametersByPathPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParametersByPath)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparametersbypathpaginator)
    """

    def paginate(
        self,
        *,
        Path: str,
        Recursive: bool = ...,
        ParameterFilters: Sequence[ParameterStringFilterTypeDef] = ...,
        WithDecryption: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetParametersByPathResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.GetParametersByPath.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparametersbypathpaginator)
        """


class ListAssociationVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociationVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationversionspaginator)
    """

    def paginate(
        self, *, AssociationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociationVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationversionspaginator)
        """


class ListAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationspaginator)
    """

    def paginate(
        self,
        *,
        AssociationFilterList: Sequence[AssociationFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationspaginator)
        """


class ListCommandInvocationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommandInvocations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandinvocationspaginator)
    """

    def paginate(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        Filters: Sequence[CommandFilterTypeDef] = ...,
        Details: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCommandInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommandInvocations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandinvocationspaginator)
        """


class ListCommandsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommands)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandspaginator)
    """

    def paginate(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        Filters: Sequence[CommandFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCommandsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListCommands.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandspaginator)
        """


class ListComplianceItemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceItems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcomplianceitemspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        ResourceIds: Sequence[str] = ...,
        ResourceTypes: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceItemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcomplianceitemspaginator)
        """


class ListComplianceSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcompliancesummariespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListComplianceSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcompliancesummariespaginator)
        """


class ListDocumentVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocumentVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentversionspaginator)
    """

    def paginate(
        self, *, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDocumentVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocumentVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentversionspaginator)
        """


class ListDocumentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocuments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentspaginator)
    """

    def paginate(
        self,
        *,
        DocumentFilterList: Sequence[DocumentFilterTypeDef] = ...,
        Filters: Sequence[DocumentKeyValuesFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDocumentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListDocuments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentspaginator)
        """


class ListOpsItemEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemeventspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[OpsItemEventFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsItemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemeventspaginator)
        """


class ListOpsItemRelatedItemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemRelatedItems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemrelateditemspaginator)
    """

    def paginate(
        self,
        *,
        OpsItemId: str = ...,
        Filters: Sequence[OpsItemRelatedItemsFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsItemRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsItemRelatedItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemrelateditemspaginator)
        """


class ListOpsMetadataPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsMetadata)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsmetadatapaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[OpsMetadataFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOpsMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListOpsMetadata.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsmetadatapaginator)
        """


class ListResourceComplianceSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceComplianceSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcecompliancesummariespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceComplianceSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcecompliancesummariespaginator)
        """


class ListResourceDataSyncPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceDataSync)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcedatasyncpaginator)
    """

    def paginate(
        self, *, SyncType: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResourceDataSyncResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Paginator.ListResourceDataSync.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcedatasyncpaginator)
        """
