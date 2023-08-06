"""
Type annotations for backup service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_backup.client import BackupClient

    session = Session()
    client: BackupClient = session.client("backup")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    BackupJobStateType,
    BackupVaultEventType,
    CopyJobStateType,
    RestoreJobStatusType,
)
from .paginator import (
    ListBackupJobsPaginator,
    ListBackupPlansPaginator,
    ListBackupPlanTemplatesPaginator,
    ListBackupPlanVersionsPaginator,
    ListBackupSelectionsPaginator,
    ListBackupVaultsPaginator,
    ListCopyJobsPaginator,
    ListProtectedResourcesPaginator,
    ListRecoveryPointsByBackupVaultPaginator,
    ListRecoveryPointsByResourcePaginator,
    ListRestoreJobsPaginator,
)
from .type_defs import (
    BackupPlanInputTypeDef,
    BackupSelectionTypeDef,
    CreateBackupPlanOutputTypeDef,
    CreateBackupSelectionOutputTypeDef,
    CreateBackupVaultOutputTypeDef,
    CreateFrameworkOutputTypeDef,
    CreateReportPlanOutputTypeDef,
    DeleteBackupPlanOutputTypeDef,
    DescribeBackupJobOutputTypeDef,
    DescribeBackupVaultOutputTypeDef,
    DescribeCopyJobOutputTypeDef,
    DescribeFrameworkOutputTypeDef,
    DescribeGlobalSettingsOutputTypeDef,
    DescribeProtectedResourceOutputTypeDef,
    DescribeRecoveryPointOutputTypeDef,
    DescribeRegionSettingsOutputTypeDef,
    DescribeReportJobOutputTypeDef,
    DescribeReportPlanOutputTypeDef,
    DescribeRestoreJobOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportBackupPlanTemplateOutputTypeDef,
    FrameworkControlTypeDef,
    GetBackupPlanFromJSONOutputTypeDef,
    GetBackupPlanFromTemplateOutputTypeDef,
    GetBackupPlanOutputTypeDef,
    GetBackupSelectionOutputTypeDef,
    GetBackupVaultAccessPolicyOutputTypeDef,
    GetBackupVaultNotificationsOutputTypeDef,
    GetRecoveryPointRestoreMetadataOutputTypeDef,
    GetSupportedResourceTypesOutputTypeDef,
    LifecycleTypeDef,
    ListBackupJobsOutputTypeDef,
    ListBackupPlansOutputTypeDef,
    ListBackupPlanTemplatesOutputTypeDef,
    ListBackupPlanVersionsOutputTypeDef,
    ListBackupSelectionsOutputTypeDef,
    ListBackupVaultsOutputTypeDef,
    ListCopyJobsOutputTypeDef,
    ListFrameworksOutputTypeDef,
    ListProtectedResourcesOutputTypeDef,
    ListRecoveryPointsByBackupVaultOutputTypeDef,
    ListRecoveryPointsByResourceOutputTypeDef,
    ListReportJobsOutputTypeDef,
    ListReportPlansOutputTypeDef,
    ListRestoreJobsOutputTypeDef,
    ListTagsOutputTypeDef,
    ReportDeliveryChannelTypeDef,
    ReportSettingTypeDef,
    StartBackupJobOutputTypeDef,
    StartCopyJobOutputTypeDef,
    StartReportJobOutputTypeDef,
    StartRestoreJobOutputTypeDef,
    UpdateBackupPlanOutputTypeDef,
    UpdateFrameworkOutputTypeDef,
    UpdateRecoveryPointLifecycleOutputTypeDef,
    UpdateReportPlanOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("BackupClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailureException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingParameterValueException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]


class BackupClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#can_paginate)
        """

    def create_backup_plan(
        self,
        *,
        BackupPlan: BackupPlanInputTypeDef,
        BackupPlanTags: Mapping[str, str] = ...,
        CreatorRequestId: str = ...
    ) -> CreateBackupPlanOutputTypeDef:
        """
        Creates a backup plan using a backup plan name and backup rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#create_backup_plan)
        """

    def create_backup_selection(
        self,
        *,
        BackupPlanId: str,
        BackupSelection: BackupSelectionTypeDef,
        CreatorRequestId: str = ...
    ) -> CreateBackupSelectionOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_selection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#create_backup_selection)
        """

    def create_backup_vault(
        self,
        *,
        BackupVaultName: str,
        BackupVaultTags: Mapping[str, str] = ...,
        EncryptionKeyArn: str = ...,
        CreatorRequestId: str = ...
    ) -> CreateBackupVaultOutputTypeDef:
        """
        Creates a logical container where backups are stored.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_backup_vault)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#create_backup_vault)
        """

    def create_framework(
        self,
        *,
        FrameworkName: str,
        FrameworkControls: Sequence[FrameworkControlTypeDef],
        FrameworkDescription: str = ...,
        IdempotencyToken: str = ...,
        FrameworkTags: Mapping[str, str] = ...
    ) -> CreateFrameworkOutputTypeDef:
        """
        Creates a framework with one or more controls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#create_framework)
        """

    def create_report_plan(
        self,
        *,
        ReportPlanName: str,
        ReportDeliveryChannel: ReportDeliveryChannelTypeDef,
        ReportSetting: ReportSettingTypeDef,
        ReportPlanDescription: str = ...,
        ReportPlanTags: Mapping[str, str] = ...,
        IdempotencyToken: str = ...
    ) -> CreateReportPlanOutputTypeDef:
        """
        Creates a report plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.create_report_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#create_report_plan)
        """

    def delete_backup_plan(self, *, BackupPlanId: str) -> DeleteBackupPlanOutputTypeDef:
        """
        Deletes a backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_plan)
        """

    def delete_backup_selection(
        self, *, BackupPlanId: str, SelectionId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource selection associated with a backup plan that is specified
        by the `SelectionId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_selection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_selection)
        """

    def delete_backup_vault(self, *, BackupVaultName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the backup vault identified by its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_vault)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_vault)
        """

    def delete_backup_vault_access_policy(
        self, *, BackupVaultName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the policy document that manages permissions on a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_vault_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_vault_access_policy)
        """

    def delete_backup_vault_lock_configuration(
        self, *, BackupVaultName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes Backup Vault Lock from a backup vault specified by a backup vault name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_vault_lock_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_vault_lock_configuration)
        """

    def delete_backup_vault_notifications(
        self, *, BackupVaultName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes event notifications for the specified backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_backup_vault_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_backup_vault_notifications)
        """

    def delete_framework(self, *, FrameworkName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the framework specified by a framework name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_framework)
        """

    def delete_recovery_point(
        self, *, BackupVaultName: str, RecoveryPointArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the recovery point specified by a recovery point ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_recovery_point)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_recovery_point)
        """

    def delete_report_plan(self, *, ReportPlanName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the report plan specified by a report plan name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.delete_report_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#delete_report_plan)
        """

    def describe_backup_job(self, *, BackupJobId: str) -> DescribeBackupJobOutputTypeDef:
        """
        Returns backup job details for the specified `BackupJobId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_backup_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_backup_job)
        """

    def describe_backup_vault(self, *, BackupVaultName: str) -> DescribeBackupVaultOutputTypeDef:
        """
        Returns metadata about a backup vault specified by its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_backup_vault)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_backup_vault)
        """

    def describe_copy_job(self, *, CopyJobId: str) -> DescribeCopyJobOutputTypeDef:
        """
        Returns metadata associated with creating a copy of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_copy_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_copy_job)
        """

    def describe_framework(self, *, FrameworkName: str) -> DescribeFrameworkOutputTypeDef:
        """
        Returns the framework details for the specified `FrameworkName` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_framework)
        """

    def describe_global_settings(self) -> DescribeGlobalSettingsOutputTypeDef:
        """
        Describes whether the Amazon Web Services account is opted in to cross-account
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_global_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_global_settings)
        """

    def describe_protected_resource(
        self, *, ResourceArn: str
    ) -> DescribeProtectedResourceOutputTypeDef:
        """
        Returns information about a saved resource, including the last time it was
        backed up, its Amazon Resource Name (ARN), and the Amazon Web Services service
        type of the saved resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_protected_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_protected_resource)
        """

    def describe_recovery_point(
        self, *, BackupVaultName: str, RecoveryPointArn: str
    ) -> DescribeRecoveryPointOutputTypeDef:
        """
        Returns metadata associated with a recovery point, including ID, status,
        encryption, and lifecycle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_recovery_point)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_recovery_point)
        """

    def describe_region_settings(self) -> DescribeRegionSettingsOutputTypeDef:
        """
        Returns the current service opt-in settings for the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_region_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_region_settings)
        """

    def describe_report_job(self, *, ReportJobId: str) -> DescribeReportJobOutputTypeDef:
        """
        Returns the details associated with creating a report as specified by its
        `ReportJobId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_report_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_report_job)
        """

    def describe_report_plan(self, *, ReportPlanName: str) -> DescribeReportPlanOutputTypeDef:
        """
        Returns a list of all report plans for an Amazon Web Services account and Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_report_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_report_plan)
        """

    def describe_restore_job(self, *, RestoreJobId: str) -> DescribeRestoreJobOutputTypeDef:
        """
        Returns metadata associated with a restore job that is specified by a job ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.describe_restore_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#describe_restore_job)
        """

    def disassociate_recovery_point(
        self, *, BackupVaultName: str, RecoveryPointArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified continuous backup recovery point from Backup and releases
        control of that continuous backup to the source service, such as Amazon RDS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.disassociate_recovery_point)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#disassociate_recovery_point)
        """

    def export_backup_plan_template(
        self, *, BackupPlanId: str
    ) -> ExportBackupPlanTemplateOutputTypeDef:
        """
        Returns the backup plan that is specified by the plan ID as a backup template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.export_backup_plan_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#export_backup_plan_template)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#generate_presigned_url)
        """

    def get_backup_plan(
        self, *, BackupPlanId: str, VersionId: str = ...
    ) -> GetBackupPlanOutputTypeDef:
        """
        Returns `BackupPlan` details for the specified `BackupPlanId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_plan)
        """

    def get_backup_plan_from_json(
        self, *, BackupPlanTemplateJson: str
    ) -> GetBackupPlanFromJSONOutputTypeDef:
        """
        Returns a valid JSON document specifying a backup plan or an error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_plan_from_json)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_plan_from_json)
        """

    def get_backup_plan_from_template(
        self, *, BackupPlanTemplateId: str
    ) -> GetBackupPlanFromTemplateOutputTypeDef:
        """
        Returns the template specified by its `templateId` as a backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_plan_from_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_plan_from_template)
        """

    def get_backup_selection(
        self, *, BackupPlanId: str, SelectionId: str
    ) -> GetBackupSelectionOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_selection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_selection)
        """

    def get_backup_vault_access_policy(
        self, *, BackupVaultName: str
    ) -> GetBackupVaultAccessPolicyOutputTypeDef:
        """
        Returns the access policy document that is associated with the named backup
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_vault_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_vault_access_policy)
        """

    def get_backup_vault_notifications(
        self, *, BackupVaultName: str
    ) -> GetBackupVaultNotificationsOutputTypeDef:
        """
        Returns event notifications for the specified backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_backup_vault_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_backup_vault_notifications)
        """

    def get_recovery_point_restore_metadata(
        self, *, BackupVaultName: str, RecoveryPointArn: str
    ) -> GetRecoveryPointRestoreMetadataOutputTypeDef:
        """
        Returns a set of metadata key-value pairs that were used to create the backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_recovery_point_restore_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_recovery_point_restore_metadata)
        """

    def get_supported_resource_types(self) -> GetSupportedResourceTypesOutputTypeDef:
        """
        Returns the Amazon Web Services resource types supported by Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_supported_resource_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_supported_resource_types)
        """

    def list_backup_jobs(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        ByResourceArn: str = ...,
        ByState: BackupJobStateType = ...,
        ByBackupVaultName: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByResourceType: str = ...,
        ByAccountId: str = ...,
        ByCompleteAfter: Union[datetime, str] = ...,
        ByCompleteBefore: Union[datetime, str] = ...
    ) -> ListBackupJobsOutputTypeDef:
        """
        Returns a list of existing backup jobs for an authenticated account for the last
        30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_jobs)
        """

    def list_backup_plan_templates(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListBackupPlanTemplatesOutputTypeDef:
        """
        Returns metadata of your saved backup plan templates, including the template ID,
        name, and the creation and deletion dates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_plan_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_plan_templates)
        """

    def list_backup_plan_versions(
        self, *, BackupPlanId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListBackupPlanVersionsOutputTypeDef:
        """
        Returns version metadata of your backup plans, including Amazon Resource Names
        (ARNs), backup plan IDs, creation and deletion dates, plan names, and version
        IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_plan_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_plan_versions)
        """

    def list_backup_plans(
        self, *, NextToken: str = ..., MaxResults: int = ..., IncludeDeleted: bool = ...
    ) -> ListBackupPlansOutputTypeDef:
        """
        Returns a list of all active backup plans for an authenticated account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_plans)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_plans)
        """

    def list_backup_selections(
        self, *, BackupPlanId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListBackupSelectionsOutputTypeDef:
        """
        Returns an array containing metadata of the resources associated with the target
        backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_selections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_selections)
        """

    def list_backup_vaults(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListBackupVaultsOutputTypeDef:
        """
        Returns a list of recovery point storage containers along with information about
        them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_backup_vaults)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_backup_vaults)
        """

    def list_copy_jobs(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        ByResourceArn: str = ...,
        ByState: CopyJobStateType = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByResourceType: str = ...,
        ByDestinationVaultArn: str = ...,
        ByAccountId: str = ...,
        ByCompleteBefore: Union[datetime, str] = ...,
        ByCompleteAfter: Union[datetime, str] = ...
    ) -> ListCopyJobsOutputTypeDef:
        """
        Returns metadata about your copy jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_copy_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_copy_jobs)
        """

    def list_frameworks(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFrameworksOutputTypeDef:
        """
        Returns a list of all frameworks for an Amazon Web Services account and Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_frameworks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_frameworks)
        """

    def list_protected_resources(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListProtectedResourcesOutputTypeDef:
        """
        Returns an array of resources successfully backed up by Backup, including the
        time the resource was saved, an Amazon Resource Name (ARN) of the resource, and
        a resource type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_protected_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_protected_resources)
        """

    def list_recovery_points_by_backup_vault(
        self,
        *,
        BackupVaultName: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        ByResourceArn: str = ...,
        ByResourceType: str = ...,
        ByBackupPlanId: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...
    ) -> ListRecoveryPointsByBackupVaultOutputTypeDef:
        """
        Returns detailed information about the recovery points stored in a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_recovery_points_by_backup_vault)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_recovery_points_by_backup_vault)
        """

    def list_recovery_points_by_resource(
        self, *, ResourceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListRecoveryPointsByResourceOutputTypeDef:
        """
        Returns detailed information about all the recovery points of the type specified
        by a resource Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_recovery_points_by_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_recovery_points_by_resource)
        """

    def list_report_jobs(
        self,
        *,
        ByReportPlanName: str = ...,
        ByCreationBefore: Union[datetime, str] = ...,
        ByCreationAfter: Union[datetime, str] = ...,
        ByStatus: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListReportJobsOutputTypeDef:
        """
        Returns details about your report jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_report_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_report_jobs)
        """

    def list_report_plans(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListReportPlansOutputTypeDef:
        """
        Returns a list of your report plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_report_plans)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_report_plans)
        """

    def list_restore_jobs(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        ByAccountId: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByStatus: RestoreJobStatusType = ...,
        ByCompleteBefore: Union[datetime, str] = ...,
        ByCompleteAfter: Union[datetime, str] = ...
    ) -> ListRestoreJobsOutputTypeDef:
        """
        Returns a list of jobs that Backup initiated to restore a saved resource,
        including details about the recovery process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_restore_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_restore_jobs)
        """

    def list_tags(
        self, *, ResourceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsOutputTypeDef:
        """
        Returns a list of key-value pairs assigned to a target recovery point, backup
        plan, or backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#list_tags)
        """

    def put_backup_vault_access_policy(
        self, *, BackupVaultName: str, Policy: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a resource-based policy that is used to manage access permissions on the
        target backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.put_backup_vault_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#put_backup_vault_access_policy)
        """

    def put_backup_vault_lock_configuration(
        self,
        *,
        BackupVaultName: str,
        MinRetentionDays: int = ...,
        MaxRetentionDays: int = ...,
        ChangeableForDays: int = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies Backup Vault Lock to a backup vault, preventing attempts to delete any
        recovery point stored in or created in a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.put_backup_vault_lock_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#put_backup_vault_lock_configuration)
        """

    def put_backup_vault_notifications(
        self,
        *,
        BackupVaultName: str,
        SNSTopicArn: str,
        BackupVaultEvents: Sequence[BackupVaultEventType]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Turns on notifications on a backup vault for the specified topic and events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.put_backup_vault_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#put_backup_vault_notifications)
        """

    def start_backup_job(
        self,
        *,
        BackupVaultName: str,
        ResourceArn: str,
        IamRoleArn: str,
        IdempotencyToken: str = ...,
        StartWindowMinutes: int = ...,
        CompleteWindowMinutes: int = ...,
        Lifecycle: LifecycleTypeDef = ...,
        RecoveryPointTags: Mapping[str, str] = ...,
        BackupOptions: Mapping[str, str] = ...
    ) -> StartBackupJobOutputTypeDef:
        """
        Starts an on-demand backup job for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.start_backup_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#start_backup_job)
        """

    def start_copy_job(
        self,
        *,
        RecoveryPointArn: str,
        SourceBackupVaultName: str,
        DestinationBackupVaultArn: str,
        IamRoleArn: str,
        IdempotencyToken: str = ...,
        Lifecycle: LifecycleTypeDef = ...
    ) -> StartCopyJobOutputTypeDef:
        """
        Starts a job to create a one-time copy of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.start_copy_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#start_copy_job)
        """

    def start_report_job(
        self, *, ReportPlanName: str, IdempotencyToken: str = ...
    ) -> StartReportJobOutputTypeDef:
        """
        Starts an on-demand report job for the specified report plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.start_report_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#start_report_job)
        """

    def start_restore_job(
        self,
        *,
        RecoveryPointArn: str,
        Metadata: Mapping[str, str],
        IamRoleArn: str,
        IdempotencyToken: str = ...,
        ResourceType: str = ...
    ) -> StartRestoreJobOutputTypeDef:
        """
        Recovers the saved resource identified by an Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.start_restore_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#start_restore_job)
        """

    def stop_backup_job(self, *, BackupJobId: str) -> EmptyResponseMetadataTypeDef:
        """
        Attempts to cancel a job to create a one-time backup of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.stop_backup_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#stop_backup_job)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns a set of key-value pairs to a recovery point, backup plan, or backup
        vault identified by an Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeyList: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a set of key-value pairs from a recovery point, backup plan, or backup
        vault identified by an Amazon Resource Name (ARN) See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/backup-2018-11-15/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#untag_resource)
        """

    def update_backup_plan(
        self, *, BackupPlanId: str, BackupPlan: BackupPlanInputTypeDef
    ) -> UpdateBackupPlanOutputTypeDef:
        """
        Updates an existing backup plan identified by its `backupPlanId` with the input
        document in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_backup_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_backup_plan)
        """

    def update_framework(
        self,
        *,
        FrameworkName: str,
        FrameworkDescription: str = ...,
        FrameworkControls: Sequence[FrameworkControlTypeDef] = ...,
        IdempotencyToken: str = ...
    ) -> UpdateFrameworkOutputTypeDef:
        """
        Updates an existing framework identified by its `FrameworkName` with the input
        document in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_framework)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_framework)
        """

    def update_global_settings(
        self, *, GlobalSettings: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates whether the Amazon Web Services account is opted in to cross-account
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_global_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_global_settings)
        """

    def update_recovery_point_lifecycle(
        self, *, BackupVaultName: str, RecoveryPointArn: str, Lifecycle: LifecycleTypeDef = ...
    ) -> UpdateRecoveryPointLifecycleOutputTypeDef:
        """
        Sets the transition lifecycle of a recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_recovery_point_lifecycle)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_recovery_point_lifecycle)
        """

    def update_region_settings(
        self,
        *,
        ResourceTypeOptInPreference: Mapping[str, bool] = ...,
        ResourceTypeManagementPreference: Mapping[str, bool] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the current service opt-in settings for the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_region_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_region_settings)
        """

    def update_report_plan(
        self,
        *,
        ReportPlanName: str,
        ReportPlanDescription: str = ...,
        ReportDeliveryChannel: ReportDeliveryChannelTypeDef = ...,
        ReportSetting: ReportSettingTypeDef = ...,
        IdempotencyToken: str = ...
    ) -> UpdateReportPlanOutputTypeDef:
        """
        Updates an existing report plan identified by its `ReportPlanName` with the
        input document in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.update_report_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#update_report_plan)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_backup_jobs"]) -> ListBackupJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plan_templates"]
    ) -> ListBackupPlanTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plan_versions"]
    ) -> ListBackupPlanVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plans"]
    ) -> ListBackupPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_selections"]
    ) -> ListBackupSelectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_vaults"]
    ) -> ListBackupVaultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_copy_jobs"]) -> ListCopyJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protected_resources"]
    ) -> ListProtectedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points_by_backup_vault"]
    ) -> ListRecoveryPointsByBackupVaultPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points_by_resource"]
    ) -> ListRecoveryPointsByResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_restore_jobs"]
    ) -> ListRestoreJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/client/#get_paginator)
        """
