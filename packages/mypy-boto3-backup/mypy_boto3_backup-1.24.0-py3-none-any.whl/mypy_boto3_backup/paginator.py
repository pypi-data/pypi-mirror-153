"""
Type annotations for backup service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_backup.client import BackupClient
    from mypy_boto3_backup.paginator import (
        ListBackupJobsPaginator,
        ListBackupPlanTemplatesPaginator,
        ListBackupPlanVersionsPaginator,
        ListBackupPlansPaginator,
        ListBackupSelectionsPaginator,
        ListBackupVaultsPaginator,
        ListCopyJobsPaginator,
        ListProtectedResourcesPaginator,
        ListRecoveryPointsByBackupVaultPaginator,
        ListRecoveryPointsByResourcePaginator,
        ListRestoreJobsPaginator,
    )

    session = Session()
    client: BackupClient = session.client("backup")

    list_backup_jobs_paginator: ListBackupJobsPaginator = client.get_paginator("list_backup_jobs")
    list_backup_plan_templates_paginator: ListBackupPlanTemplatesPaginator = client.get_paginator("list_backup_plan_templates")
    list_backup_plan_versions_paginator: ListBackupPlanVersionsPaginator = client.get_paginator("list_backup_plan_versions")
    list_backup_plans_paginator: ListBackupPlansPaginator = client.get_paginator("list_backup_plans")
    list_backup_selections_paginator: ListBackupSelectionsPaginator = client.get_paginator("list_backup_selections")
    list_backup_vaults_paginator: ListBackupVaultsPaginator = client.get_paginator("list_backup_vaults")
    list_copy_jobs_paginator: ListCopyJobsPaginator = client.get_paginator("list_copy_jobs")
    list_protected_resources_paginator: ListProtectedResourcesPaginator = client.get_paginator("list_protected_resources")
    list_recovery_points_by_backup_vault_paginator: ListRecoveryPointsByBackupVaultPaginator = client.get_paginator("list_recovery_points_by_backup_vault")
    list_recovery_points_by_resource_paginator: ListRecoveryPointsByResourcePaginator = client.get_paginator("list_recovery_points_by_resource")
    list_restore_jobs_paginator: ListRestoreJobsPaginator = client.get_paginator("list_restore_jobs")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import BackupJobStateType, CopyJobStateType, RestoreJobStatusType
from .type_defs import (
    ListBackupJobsOutputTypeDef,
    ListBackupPlansOutputTypeDef,
    ListBackupPlanTemplatesOutputTypeDef,
    ListBackupPlanVersionsOutputTypeDef,
    ListBackupSelectionsOutputTypeDef,
    ListBackupVaultsOutputTypeDef,
    ListCopyJobsOutputTypeDef,
    ListProtectedResourcesOutputTypeDef,
    ListRecoveryPointsByBackupVaultOutputTypeDef,
    ListRecoveryPointsByResourceOutputTypeDef,
    ListRestoreJobsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListBackupJobsPaginator",
    "ListBackupPlanTemplatesPaginator",
    "ListBackupPlanVersionsPaginator",
    "ListBackupPlansPaginator",
    "ListBackupSelectionsPaginator",
    "ListBackupVaultsPaginator",
    "ListCopyJobsPaginator",
    "ListProtectedResourcesPaginator",
    "ListRecoveryPointsByBackupVaultPaginator",
    "ListRecoveryPointsByResourcePaginator",
    "ListRestoreJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBackupJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupjobspaginator)
    """

    def paginate(
        self,
        *,
        ByResourceArn: str = ...,
        ByState: BackupJobStateType = ...,
        ByBackupVaultName: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByResourceType: str = ...,
        ByAccountId: str = ...,
        ByCompleteAfter: Union[datetime, str] = ...,
        ByCompleteBefore: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupjobspaginator)
        """


class ListBackupPlanTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlanTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplantemplatespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupPlanTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlanTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplantemplatespaginator)
        """


class ListBackupPlanVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlanVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanversionspaginator)
    """

    def paginate(
        self, *, BackupPlanId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupPlanVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlanVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanversionspaginator)
        """


class ListBackupPlansPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlans)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanspaginator)
    """

    def paginate(
        self, *, IncludeDeleted: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupPlans.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupplanspaginator)
        """


class ListBackupSelectionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupSelections)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupselectionspaginator)
    """

    def paginate(
        self, *, BackupPlanId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupSelectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupSelections.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupselectionspaginator)
        """


class ListBackupVaultsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupVaults)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupvaultspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListBackupVaults.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listbackupvaultspaginator)
        """


class ListCopyJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListCopyJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listcopyjobspaginator)
    """

    def paginate(
        self,
        *,
        ByResourceArn: str = ...,
        ByState: CopyJobStateType = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByResourceType: str = ...,
        ByDestinationVaultArn: str = ...,
        ByAccountId: str = ...,
        ByCompleteBefore: Union[datetime, str] = ...,
        ByCompleteAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCopyJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListCopyJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listcopyjobspaginator)
        """


class ListProtectedResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListProtectedResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProtectedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListProtectedResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listprotectedresourcespaginator)
        """


class ListRecoveryPointsByBackupVaultPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRecoveryPointsByBackupVault)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
    """

    def paginate(
        self,
        *,
        BackupVaultName: str,
        ByResourceArn: str = ...,
        ByResourceType: str = ...,
        ByBackupPlanId: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecoveryPointsByBackupVaultOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRecoveryPointsByBackupVault.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbybackupvaultpaginator)
        """


class ListRecoveryPointsByResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRecoveryPointsByResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbyresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecoveryPointsByResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRecoveryPointsByResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrecoverypointsbyresourcepaginator)
        """


class ListRestoreJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRestoreJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobspaginator)
    """

    def paginate(
        self,
        *,
        ByAccountId: str = ...,
        ByCreatedBefore: Union[datetime, str] = ...,
        ByCreatedAfter: Union[datetime, str] = ...,
        ByStatus: RestoreJobStatusType = ...,
        ByCompleteBefore: Union[datetime, str] = ...,
        ByCompleteAfter: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRestoreJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Paginator.ListRestoreJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/paginators/#listrestorejobspaginator)
        """
