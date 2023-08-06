"""
Type annotations for storagegateway service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_storagegateway.client import StorageGatewayClient

    session = Session()
    client: StorageGatewayClient = session.client("storagegateway")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CaseSensitivityType,
    GatewayCapacityType,
    ObjectACLType,
    RetentionLockTypeType,
    SMBSecurityStrategyType,
    TapeStorageClassType,
)
from .paginator import (
    DescribeTapeArchivesPaginator,
    DescribeTapeRecoveryPointsPaginator,
    DescribeTapesPaginator,
    DescribeVTLDevicesPaginator,
    ListFileSharesPaginator,
    ListFileSystemAssociationsPaginator,
    ListGatewaysPaginator,
    ListTagsForResourcePaginator,
    ListTapePoolsPaginator,
    ListTapesPaginator,
    ListVolumesPaginator,
)
from .type_defs import (
    ActivateGatewayOutputTypeDef,
    AddCacheOutputTypeDef,
    AddTagsToResourceOutputTypeDef,
    AddUploadBufferOutputTypeDef,
    AddWorkingStorageOutputTypeDef,
    AssignTapePoolOutputTypeDef,
    AssociateFileSystemOutputTypeDef,
    AttachVolumeOutputTypeDef,
    AutomaticTapeCreationRuleTypeDef,
    BandwidthRateLimitIntervalTypeDef,
    CacheAttributesTypeDef,
    CancelArchivalOutputTypeDef,
    CancelRetrievalOutputTypeDef,
    CreateCachediSCSIVolumeOutputTypeDef,
    CreateNFSFileShareOutputTypeDef,
    CreateSMBFileShareOutputTypeDef,
    CreateSnapshotFromVolumeRecoveryPointOutputTypeDef,
    CreateSnapshotOutputTypeDef,
    CreateStorediSCSIVolumeOutputTypeDef,
    CreateTapePoolOutputTypeDef,
    CreateTapesOutputTypeDef,
    CreateTapeWithBarcodeOutputTypeDef,
    DeleteAutomaticTapeCreationPolicyOutputTypeDef,
    DeleteBandwidthRateLimitOutputTypeDef,
    DeleteChapCredentialsOutputTypeDef,
    DeleteFileShareOutputTypeDef,
    DeleteGatewayOutputTypeDef,
    DeleteSnapshotScheduleOutputTypeDef,
    DeleteTapeArchiveOutputTypeDef,
    DeleteTapeOutputTypeDef,
    DeleteTapePoolOutputTypeDef,
    DeleteVolumeOutputTypeDef,
    DescribeAvailabilityMonitorTestOutputTypeDef,
    DescribeBandwidthRateLimitOutputTypeDef,
    DescribeBandwidthRateLimitScheduleOutputTypeDef,
    DescribeCachediSCSIVolumesOutputTypeDef,
    DescribeCacheOutputTypeDef,
    DescribeChapCredentialsOutputTypeDef,
    DescribeFileSystemAssociationsOutputTypeDef,
    DescribeGatewayInformationOutputTypeDef,
    DescribeMaintenanceStartTimeOutputTypeDef,
    DescribeNFSFileSharesOutputTypeDef,
    DescribeSMBFileSharesOutputTypeDef,
    DescribeSMBSettingsOutputTypeDef,
    DescribeSnapshotScheduleOutputTypeDef,
    DescribeStorediSCSIVolumesOutputTypeDef,
    DescribeTapeArchivesOutputTypeDef,
    DescribeTapeRecoveryPointsOutputTypeDef,
    DescribeTapesOutputTypeDef,
    DescribeUploadBufferOutputTypeDef,
    DescribeVTLDevicesOutputTypeDef,
    DescribeWorkingStorageOutputTypeDef,
    DetachVolumeOutputTypeDef,
    DisableGatewayOutputTypeDef,
    DisassociateFileSystemOutputTypeDef,
    EndpointNetworkConfigurationTypeDef,
    JoinDomainOutputTypeDef,
    ListAutomaticTapeCreationPoliciesOutputTypeDef,
    ListFileSharesOutputTypeDef,
    ListFileSystemAssociationsOutputTypeDef,
    ListGatewaysOutputTypeDef,
    ListLocalDisksOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTapePoolsOutputTypeDef,
    ListTapesOutputTypeDef,
    ListVolumeInitiatorsOutputTypeDef,
    ListVolumeRecoveryPointsOutputTypeDef,
    ListVolumesOutputTypeDef,
    NFSFileShareDefaultsTypeDef,
    NotifyWhenUploadedOutputTypeDef,
    RefreshCacheOutputTypeDef,
    RemoveTagsFromResourceOutputTypeDef,
    ResetCacheOutputTypeDef,
    RetrieveTapeArchiveOutputTypeDef,
    RetrieveTapeRecoveryPointOutputTypeDef,
    SetLocalConsolePasswordOutputTypeDef,
    SetSMBGuestPasswordOutputTypeDef,
    ShutdownGatewayOutputTypeDef,
    SMBLocalGroupsTypeDef,
    StartAvailabilityMonitorTestOutputTypeDef,
    StartGatewayOutputTypeDef,
    TagTypeDef,
    UpdateAutomaticTapeCreationPolicyOutputTypeDef,
    UpdateBandwidthRateLimitOutputTypeDef,
    UpdateBandwidthRateLimitScheduleOutputTypeDef,
    UpdateChapCredentialsOutputTypeDef,
    UpdateFileSystemAssociationOutputTypeDef,
    UpdateGatewayInformationOutputTypeDef,
    UpdateGatewaySoftwareNowOutputTypeDef,
    UpdateMaintenanceStartTimeOutputTypeDef,
    UpdateNFSFileShareOutputTypeDef,
    UpdateSMBFileShareOutputTypeDef,
    UpdateSMBFileShareVisibilityOutputTypeDef,
    UpdateSMBLocalGroupsOutputTypeDef,
    UpdateSMBSecurityStrategyOutputTypeDef,
    UpdateSnapshotScheduleOutputTypeDef,
    UpdateVTLDeviceTypeOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("StorageGatewayClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidGatewayRequestException: Type[BotocoreClientError]
    ServiceUnavailableError: Type[BotocoreClientError]


class StorageGatewayClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        StorageGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#exceptions)
        """

    def activate_gateway(
        self,
        *,
        ActivationKey: str,
        GatewayName: str,
        GatewayTimezone: str,
        GatewayRegion: str,
        GatewayType: str = ...,
        TapeDriveType: str = ...,
        MediumChangerType: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> ActivateGatewayOutputTypeDef:
        """
        Activates the gateway you previously deployed on your host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.activate_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#activate_gateway)
        """

    def add_cache(self, *, GatewayARN: str, DiskIds: Sequence[str]) -> AddCacheOutputTypeDef:
        """
        Configures one or more gateway local disks as cache for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.add_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#add_cache)
        """

    def add_tags_to_resource(
        self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]
    ) -> AddTagsToResourceOutputTypeDef:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.add_tags_to_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#add_tags_to_resource)
        """

    def add_upload_buffer(
        self, *, GatewayARN: str, DiskIds: Sequence[str]
    ) -> AddUploadBufferOutputTypeDef:
        """
        Configures one or more gateway local disks as upload buffer for a specified
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.add_upload_buffer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#add_upload_buffer)
        """

    def add_working_storage(
        self, *, GatewayARN: str, DiskIds: Sequence[str]
    ) -> AddWorkingStorageOutputTypeDef:
        """
        Configures one or more gateway local disks as working storage for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.add_working_storage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#add_working_storage)
        """

    def assign_tape_pool(
        self, *, TapeARN: str, PoolId: str, BypassGovernanceRetention: bool = ...
    ) -> AssignTapePoolOutputTypeDef:
        """
        Assigns a tape to a tape pool for archiving.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.assign_tape_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#assign_tape_pool)
        """

    def associate_file_system(
        self,
        *,
        UserName: str,
        Password: str,
        ClientToken: str,
        GatewayARN: str,
        LocationARN: str,
        Tags: Sequence[TagTypeDef] = ...,
        AuditDestinationARN: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...,
        EndpointNetworkConfiguration: EndpointNetworkConfigurationTypeDef = ...
    ) -> AssociateFileSystemOutputTypeDef:
        """
        Associate an Amazon FSx file system with the FSx File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.associate_file_system)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#associate_file_system)
        """

    def attach_volume(
        self,
        *,
        GatewayARN: str,
        VolumeARN: str,
        NetworkInterfaceId: str,
        TargetName: str = ...,
        DiskId: str = ...
    ) -> AttachVolumeOutputTypeDef:
        """
        Connects a volume to an iSCSI connection and then attaches the volume to the
        specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.attach_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#attach_volume)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#can_paginate)
        """

    def cancel_archival(self, *, GatewayARN: str, TapeARN: str) -> CancelArchivalOutputTypeDef:
        """
        Cancels archiving of a virtual tape to the virtual tape shelf (VTS) after the
        archiving process is initiated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.cancel_archival)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#cancel_archival)
        """

    def cancel_retrieval(self, *, GatewayARN: str, TapeARN: str) -> CancelRetrievalOutputTypeDef:
        """
        Cancels retrieval of a virtual tape from the virtual tape shelf (VTS) to a
        gateway after the retrieval process is initiated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.cancel_retrieval)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#cancel_retrieval)
        """

    def create_cached_iscsi_volume(
        self,
        *,
        GatewayARN: str,
        VolumeSizeInBytes: int,
        TargetName: str,
        NetworkInterfaceId: str,
        ClientToken: str,
        SnapshotId: str = ...,
        SourceVolumeARN: str = ...,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateCachediSCSIVolumeOutputTypeDef:
        """
        Creates a cached volume on a specified cached volume gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_cached_iscsi_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_cached_iscsi_volume)
        """

    def create_nfs_file_share(
        self,
        *,
        ClientToken: str,
        GatewayARN: str,
        Role: str,
        LocationARN: str,
        NFSFileShareDefaults: NFSFileShareDefaultsTypeDef = ...,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        DefaultStorageClass: str = ...,
        ObjectACL: ObjectACLType = ...,
        ClientList: Sequence[str] = ...,
        Squash: str = ...,
        ReadOnly: bool = ...,
        GuessMIMETypeEnabled: bool = ...,
        RequesterPays: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        FileShareName: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...,
        NotificationPolicy: str = ...,
        VPCEndpointDNSName: str = ...,
        BucketRegion: str = ...,
        AuditDestinationARN: str = ...
    ) -> CreateNFSFileShareOutputTypeDef:
        """
        Creates a Network File System (NFS) file share on an existing S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_nfs_file_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_nfs_file_share)
        """

    def create_smb_file_share(
        self,
        *,
        ClientToken: str,
        GatewayARN: str,
        Role: str,
        LocationARN: str,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        DefaultStorageClass: str = ...,
        ObjectACL: ObjectACLType = ...,
        ReadOnly: bool = ...,
        GuessMIMETypeEnabled: bool = ...,
        RequesterPays: bool = ...,
        SMBACLEnabled: bool = ...,
        AccessBasedEnumeration: bool = ...,
        AdminUserList: Sequence[str] = ...,
        ValidUserList: Sequence[str] = ...,
        InvalidUserList: Sequence[str] = ...,
        AuditDestinationARN: str = ...,
        Authentication: str = ...,
        CaseSensitivity: CaseSensitivityType = ...,
        Tags: Sequence[TagTypeDef] = ...,
        FileShareName: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...,
        NotificationPolicy: str = ...,
        VPCEndpointDNSName: str = ...,
        BucketRegion: str = ...,
        OplocksEnabled: bool = ...
    ) -> CreateSMBFileShareOutputTypeDef:
        """
        Creates a Server Message Block (SMB) file share on an existing S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_smb_file_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_smb_file_share)
        """

    def create_snapshot(
        self, *, VolumeARN: str, SnapshotDescription: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateSnapshotOutputTypeDef:
        """
        Initiates a snapshot of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_snapshot)
        """

    def create_snapshot_from_volume_recovery_point(
        self, *, VolumeARN: str, SnapshotDescription: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateSnapshotFromVolumeRecoveryPointOutputTypeDef:
        """
        Initiates a snapshot of a gateway from a volume recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_snapshot_from_volume_recovery_point)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_snapshot_from_volume_recovery_point)
        """

    def create_stored_iscsi_volume(
        self,
        *,
        GatewayARN: str,
        DiskId: str,
        PreserveExistingData: bool,
        TargetName: str,
        NetworkInterfaceId: str,
        SnapshotId: str = ...,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateStorediSCSIVolumeOutputTypeDef:
        """
        Creates a volume on a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_stored_iscsi_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_stored_iscsi_volume)
        """

    def create_tape_pool(
        self,
        *,
        PoolName: str,
        StorageClass: TapeStorageClassType,
        RetentionLockType: RetentionLockTypeType = ...,
        RetentionLockTimeInDays: int = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateTapePoolOutputTypeDef:
        """
        Creates a new custom tape pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_tape_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_tape_pool)
        """

    def create_tape_with_barcode(
        self,
        *,
        GatewayARN: str,
        TapeSizeInBytes: int,
        TapeBarcode: str,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        PoolId: str = ...,
        Worm: bool = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateTapeWithBarcodeOutputTypeDef:
        """
        Creates a virtual tape by using your own barcode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_tape_with_barcode)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_tape_with_barcode)
        """

    def create_tapes(
        self,
        *,
        GatewayARN: str,
        TapeSizeInBytes: int,
        ClientToken: str,
        NumTapesToCreate: int,
        TapeBarcodePrefix: str,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        PoolId: str = ...,
        Worm: bool = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateTapesOutputTypeDef:
        """
        Creates one or more virtual tapes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_tapes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#create_tapes)
        """

    def delete_automatic_tape_creation_policy(
        self, *, GatewayARN: str
    ) -> DeleteAutomaticTapeCreationPolicyOutputTypeDef:
        """
        Deletes the automatic tape creation policy of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_automatic_tape_creation_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_automatic_tape_creation_policy)
        """

    def delete_bandwidth_rate_limit(
        self, *, GatewayARN: str, BandwidthType: str
    ) -> DeleteBandwidthRateLimitOutputTypeDef:
        """
        Deletes the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_bandwidth_rate_limit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_bandwidth_rate_limit)
        """

    def delete_chap_credentials(
        self, *, TargetARN: str, InitiatorName: str
    ) -> DeleteChapCredentialsOutputTypeDef:
        """
        Deletes Challenge-Handshake Authentication Protocol (CHAP) credentials for a
        specified iSCSI target and initiator pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_chap_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_chap_credentials)
        """

    def delete_file_share(
        self, *, FileShareARN: str, ForceDelete: bool = ...
    ) -> DeleteFileShareOutputTypeDef:
        """
        Deletes a file share from an S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_file_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_file_share)
        """

    def delete_gateway(self, *, GatewayARN: str) -> DeleteGatewayOutputTypeDef:
        """
        Deletes a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_gateway)
        """

    def delete_snapshot_schedule(self, *, VolumeARN: str) -> DeleteSnapshotScheduleOutputTypeDef:
        """
        Deletes a snapshot of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_snapshot_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_snapshot_schedule)
        """

    def delete_tape(
        self, *, GatewayARN: str, TapeARN: str, BypassGovernanceRetention: bool = ...
    ) -> DeleteTapeOutputTypeDef:
        """
        Deletes the specified virtual tape.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_tape)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_tape)
        """

    def delete_tape_archive(
        self, *, TapeARN: str, BypassGovernanceRetention: bool = ...
    ) -> DeleteTapeArchiveOutputTypeDef:
        """
        Deletes the specified virtual tape from the virtual tape shelf (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_tape_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_tape_archive)
        """

    def delete_tape_pool(self, *, PoolARN: str) -> DeleteTapePoolOutputTypeDef:
        """
        Delete a custom tape pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_tape_pool)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_tape_pool)
        """

    def delete_volume(self, *, VolumeARN: str) -> DeleteVolumeOutputTypeDef:
        """
        Deletes the specified storage volume that you previously created using the
        CreateCachediSCSIVolume or  CreateStorediSCSIVolume API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.delete_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#delete_volume)
        """

    def describe_availability_monitor_test(
        self, *, GatewayARN: str
    ) -> DescribeAvailabilityMonitorTestOutputTypeDef:
        """
        Returns information about the most recent high availability monitoring test that
        was performed on the host in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_availability_monitor_test)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_availability_monitor_test)
        """

    def describe_bandwidth_rate_limit(
        self, *, GatewayARN: str
    ) -> DescribeBandwidthRateLimitOutputTypeDef:
        """
        Returns the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_bandwidth_rate_limit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_bandwidth_rate_limit)
        """

    def describe_bandwidth_rate_limit_schedule(
        self, *, GatewayARN: str
    ) -> DescribeBandwidthRateLimitScheduleOutputTypeDef:
        """
        Returns information about the bandwidth rate limit schedule of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_bandwidth_rate_limit_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_bandwidth_rate_limit_schedule)
        """

    def describe_cache(self, *, GatewayARN: str) -> DescribeCacheOutputTypeDef:
        """
        Returns information about the cache of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_cache)
        """

    def describe_cached_iscsi_volumes(
        self, *, VolumeARNs: Sequence[str]
    ) -> DescribeCachediSCSIVolumesOutputTypeDef:
        """
        Returns a description of the gateway volumes specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_cached_iscsi_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_cached_iscsi_volumes)
        """

    def describe_chap_credentials(self, *, TargetARN: str) -> DescribeChapCredentialsOutputTypeDef:
        """
        Returns an array of Challenge-Handshake Authentication Protocol (CHAP)
        credentials information for a specified iSCSI target, one for each target-
        initiator pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_chap_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_chap_credentials)
        """

    def describe_file_system_associations(
        self, *, FileSystemAssociationARNList: Sequence[str]
    ) -> DescribeFileSystemAssociationsOutputTypeDef:
        """
        Gets the file system association information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_file_system_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_file_system_associations)
        """

    def describe_gateway_information(
        self, *, GatewayARN: str
    ) -> DescribeGatewayInformationOutputTypeDef:
        """
        Returns metadata about a gateway such as its name, network interfaces,
        configured time zone, and the state (whether the gateway is running or not).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_gateway_information)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_gateway_information)
        """

    def describe_maintenance_start_time(
        self, *, GatewayARN: str
    ) -> DescribeMaintenanceStartTimeOutputTypeDef:
        """
        Returns your gateway's weekly maintenance start time including the day and time
        of the week.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_maintenance_start_time)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_maintenance_start_time)
        """

    def describe_nfs_file_shares(
        self, *, FileShareARNList: Sequence[str]
    ) -> DescribeNFSFileSharesOutputTypeDef:
        """
        Gets a description for one or more Network File System (NFS) file shares from an
        S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_nfs_file_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_nfs_file_shares)
        """

    def describe_smb_file_shares(
        self, *, FileShareARNList: Sequence[str]
    ) -> DescribeSMBFileSharesOutputTypeDef:
        """
        Gets a description for one or more Server Message Block (SMB) file shares from a
        S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_smb_file_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_smb_file_shares)
        """

    def describe_smb_settings(self, *, GatewayARN: str) -> DescribeSMBSettingsOutputTypeDef:
        """
        Gets a description of a Server Message Block (SMB) file share settings from a
        file gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_smb_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_smb_settings)
        """

    def describe_snapshot_schedule(
        self, *, VolumeARN: str
    ) -> DescribeSnapshotScheduleOutputTypeDef:
        """
        Describes the snapshot schedule for the specified gateway volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_snapshot_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_snapshot_schedule)
        """

    def describe_stored_iscsi_volumes(
        self, *, VolumeARNs: Sequence[str]
    ) -> DescribeStorediSCSIVolumesOutputTypeDef:
        """
        Returns the description of the gateway volumes specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_stored_iscsi_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_stored_iscsi_volumes)
        """

    def describe_tape_archives(
        self, *, TapeARNs: Sequence[str] = ..., Marker: str = ..., Limit: int = ...
    ) -> DescribeTapeArchivesOutputTypeDef:
        """
        Returns a description of specified virtual tapes in the virtual tape shelf
        (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_tape_archives)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_tape_archives)
        """

    def describe_tape_recovery_points(
        self, *, GatewayARN: str, Marker: str = ..., Limit: int = ...
    ) -> DescribeTapeRecoveryPointsOutputTypeDef:
        """
        Returns a list of virtual tape recovery points that are available for the
        specified tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_tape_recovery_points)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_tape_recovery_points)
        """

    def describe_tapes(
        self, *, GatewayARN: str, TapeARNs: Sequence[str] = ..., Marker: str = ..., Limit: int = ...
    ) -> DescribeTapesOutputTypeDef:
        """
        Returns a description of the specified Amazon Resource Name (ARN) of virtual
        tapes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_tapes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_tapes)
        """

    def describe_upload_buffer(self, *, GatewayARN: str) -> DescribeUploadBufferOutputTypeDef:
        """
        Returns information about the upload buffer of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_upload_buffer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_upload_buffer)
        """

    def describe_vtl_devices(
        self,
        *,
        GatewayARN: str,
        VTLDeviceARNs: Sequence[str] = ...,
        Marker: str = ...,
        Limit: int = ...
    ) -> DescribeVTLDevicesOutputTypeDef:
        """
        Returns a description of virtual tape library (VTL) devices for the specified
        tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_vtl_devices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_vtl_devices)
        """

    def describe_working_storage(self, *, GatewayARN: str) -> DescribeWorkingStorageOutputTypeDef:
        """
        Returns information about the working storage of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_working_storage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#describe_working_storage)
        """

    def detach_volume(
        self, *, VolumeARN: str, ForceDetach: bool = ...
    ) -> DetachVolumeOutputTypeDef:
        """
        Disconnects a volume from an iSCSI connection and then detaches the volume from
        the specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.detach_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#detach_volume)
        """

    def disable_gateway(self, *, GatewayARN: str) -> DisableGatewayOutputTypeDef:
        """
        Disables a tape gateway when the gateway is no longer functioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.disable_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#disable_gateway)
        """

    def disassociate_file_system(
        self, *, FileSystemAssociationARN: str, ForceDelete: bool = ...
    ) -> DisassociateFileSystemOutputTypeDef:
        """
        Disassociates an Amazon FSx file system from the specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.disassociate_file_system)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#disassociate_file_system)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#generate_presigned_url)
        """

    def join_domain(
        self,
        *,
        GatewayARN: str,
        DomainName: str,
        UserName: str,
        Password: str,
        OrganizationalUnit: str = ...,
        DomainControllers: Sequence[str] = ...,
        TimeoutInSeconds: int = ...
    ) -> JoinDomainOutputTypeDef:
        """
        Adds a file gateway to an Active Directory domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.join_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#join_domain)
        """

    def list_automatic_tape_creation_policies(
        self, *, GatewayARN: str = ...
    ) -> ListAutomaticTapeCreationPoliciesOutputTypeDef:
        """
        Lists the automatic tape creation policies for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_automatic_tape_creation_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_automatic_tape_creation_policies)
        """

    def list_file_shares(
        self, *, GatewayARN: str = ..., Limit: int = ..., Marker: str = ...
    ) -> ListFileSharesOutputTypeDef:
        """
        Gets a list of the file shares for a specific S3 File Gateway, or the list of
        file shares that belong to the calling user account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_file_shares)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_file_shares)
        """

    def list_file_system_associations(
        self, *, GatewayARN: str = ..., Limit: int = ..., Marker: str = ...
    ) -> ListFileSystemAssociationsOutputTypeDef:
        """
        Gets a list of `FileSystemAssociationSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_file_system_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_file_system_associations)
        """

    def list_gateways(self, *, Marker: str = ..., Limit: int = ...) -> ListGatewaysOutputTypeDef:
        """
        Lists gateways owned by an Amazon Web Services account in an Amazon Web Services
        Region specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_gateways)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_gateways)
        """

    def list_local_disks(self, *, GatewayARN: str) -> ListLocalDisksOutputTypeDef:
        """
        Returns a list of the gateway's local disks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_local_disks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_local_disks)
        """

    def list_tags_for_resource(
        self, *, ResourceARN: str, Marker: str = ..., Limit: int = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags that have been added to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_tags_for_resource)
        """

    def list_tape_pools(
        self, *, PoolARNs: Sequence[str] = ..., Marker: str = ..., Limit: int = ...
    ) -> ListTapePoolsOutputTypeDef:
        """
        Lists custom tape pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_tape_pools)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_tape_pools)
        """

    def list_tapes(
        self, *, TapeARNs: Sequence[str] = ..., Marker: str = ..., Limit: int = ...
    ) -> ListTapesOutputTypeDef:
        """
        Lists virtual tapes in your virtual tape library (VTL) and your virtual tape
        shelf (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_tapes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_tapes)
        """

    def list_volume_initiators(self, *, VolumeARN: str) -> ListVolumeInitiatorsOutputTypeDef:
        """
        Lists iSCSI initiators that are connected to a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_volume_initiators)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_volume_initiators)
        """

    def list_volume_recovery_points(
        self, *, GatewayARN: str
    ) -> ListVolumeRecoveryPointsOutputTypeDef:
        """
        Lists the recovery points for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_volume_recovery_points)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_volume_recovery_points)
        """

    def list_volumes(
        self, *, GatewayARN: str = ..., Marker: str = ..., Limit: int = ...
    ) -> ListVolumesOutputTypeDef:
        """
        Lists the iSCSI stored volumes of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.list_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#list_volumes)
        """

    def notify_when_uploaded(self, *, FileShareARN: str) -> NotifyWhenUploadedOutputTypeDef:
        """
        Sends you notification through CloudWatch Events when all files written to your
        file share have been uploaded to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.notify_when_uploaded)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#notify_when_uploaded)
        """

    def refresh_cache(
        self, *, FileShareARN: str, FolderList: Sequence[str] = ..., Recursive: bool = ...
    ) -> RefreshCacheOutputTypeDef:
        """
        Refreshes the cached inventory of objects for the specified file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.refresh_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#refresh_cache)
        """

    def remove_tags_from_resource(
        self, *, ResourceARN: str, TagKeys: Sequence[str]
    ) -> RemoveTagsFromResourceOutputTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.remove_tags_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#remove_tags_from_resource)
        """

    def reset_cache(self, *, GatewayARN: str) -> ResetCacheOutputTypeDef:
        """
        Resets all cache disks that have encountered an error and makes the disks
        available for reconfiguration as cache storage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.reset_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#reset_cache)
        """

    def retrieve_tape_archive(
        self, *, TapeARN: str, GatewayARN: str
    ) -> RetrieveTapeArchiveOutputTypeDef:
        """
        Retrieves an archived virtual tape from the virtual tape shelf (VTS) to a tape
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.retrieve_tape_archive)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#retrieve_tape_archive)
        """

    def retrieve_tape_recovery_point(
        self, *, TapeARN: str, GatewayARN: str
    ) -> RetrieveTapeRecoveryPointOutputTypeDef:
        """
        Retrieves the recovery point for the specified virtual tape.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.retrieve_tape_recovery_point)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#retrieve_tape_recovery_point)
        """

    def set_local_console_password(
        self, *, GatewayARN: str, LocalConsolePassword: str
    ) -> SetLocalConsolePasswordOutputTypeDef:
        """
        Sets the password for your VM local console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.set_local_console_password)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#set_local_console_password)
        """

    def set_smb_guest_password(
        self, *, GatewayARN: str, Password: str
    ) -> SetSMBGuestPasswordOutputTypeDef:
        """
        Sets the password for the guest user `smbguest`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.set_smb_guest_password)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#set_smb_guest_password)
        """

    def shutdown_gateway(self, *, GatewayARN: str) -> ShutdownGatewayOutputTypeDef:
        """
        Shuts down a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.shutdown_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#shutdown_gateway)
        """

    def start_availability_monitor_test(
        self, *, GatewayARN: str
    ) -> StartAvailabilityMonitorTestOutputTypeDef:
        """
        Start a test that verifies that the specified gateway is configured for High
        Availability monitoring in your host environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.start_availability_monitor_test)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#start_availability_monitor_test)
        """

    def start_gateway(self, *, GatewayARN: str) -> StartGatewayOutputTypeDef:
        """
        Starts a gateway that you previously shut down (see  ShutdownGateway ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.start_gateway)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#start_gateway)
        """

    def update_automatic_tape_creation_policy(
        self,
        *,
        AutomaticTapeCreationRules: Sequence[AutomaticTapeCreationRuleTypeDef],
        GatewayARN: str
    ) -> UpdateAutomaticTapeCreationPolicyOutputTypeDef:
        """
        Updates the automatic tape creation policy of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_automatic_tape_creation_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_automatic_tape_creation_policy)
        """

    def update_bandwidth_rate_limit(
        self,
        *,
        GatewayARN: str,
        AverageUploadRateLimitInBitsPerSec: int = ...,
        AverageDownloadRateLimitInBitsPerSec: int = ...
    ) -> UpdateBandwidthRateLimitOutputTypeDef:
        """
        Updates the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_bandwidth_rate_limit)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_bandwidth_rate_limit)
        """

    def update_bandwidth_rate_limit_schedule(
        self,
        *,
        GatewayARN: str,
        BandwidthRateLimitIntervals: Sequence[BandwidthRateLimitIntervalTypeDef]
    ) -> UpdateBandwidthRateLimitScheduleOutputTypeDef:
        """
        Updates the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_bandwidth_rate_limit_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_bandwidth_rate_limit_schedule)
        """

    def update_chap_credentials(
        self,
        *,
        TargetARN: str,
        SecretToAuthenticateInitiator: str,
        InitiatorName: str,
        SecretToAuthenticateTarget: str = ...
    ) -> UpdateChapCredentialsOutputTypeDef:
        """
        Updates the Challenge-Handshake Authentication Protocol (CHAP) credentials for a
        specified iSCSI target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_chap_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_chap_credentials)
        """

    def update_file_system_association(
        self,
        *,
        FileSystemAssociationARN: str,
        UserName: str = ...,
        Password: str = ...,
        AuditDestinationARN: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...
    ) -> UpdateFileSystemAssociationOutputTypeDef:
        """
        Updates a file system association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_file_system_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_file_system_association)
        """

    def update_gateway_information(
        self,
        *,
        GatewayARN: str,
        GatewayName: str = ...,
        GatewayTimezone: str = ...,
        CloudWatchLogGroupARN: str = ...,
        GatewayCapacity: GatewayCapacityType = ...
    ) -> UpdateGatewayInformationOutputTypeDef:
        """
        Updates a gateway's metadata, which includes the gateway's name and time zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_gateway_information)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_gateway_information)
        """

    def update_gateway_software_now(
        self, *, GatewayARN: str
    ) -> UpdateGatewaySoftwareNowOutputTypeDef:
        """
        Updates the gateway virtual machine (VM) software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_gateway_software_now)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_gateway_software_now)
        """

    def update_maintenance_start_time(
        self,
        *,
        GatewayARN: str,
        HourOfDay: int,
        MinuteOfHour: int,
        DayOfWeek: int = ...,
        DayOfMonth: int = ...
    ) -> UpdateMaintenanceStartTimeOutputTypeDef:
        """
        Updates a gateway's weekly maintenance start time information, including day and
        time of the week.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_maintenance_start_time)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_maintenance_start_time)
        """

    def update_nfs_file_share(
        self,
        *,
        FileShareARN: str,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        NFSFileShareDefaults: NFSFileShareDefaultsTypeDef = ...,
        DefaultStorageClass: str = ...,
        ObjectACL: ObjectACLType = ...,
        ClientList: Sequence[str] = ...,
        Squash: str = ...,
        ReadOnly: bool = ...,
        GuessMIMETypeEnabled: bool = ...,
        RequesterPays: bool = ...,
        FileShareName: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...,
        NotificationPolicy: str = ...,
        AuditDestinationARN: str = ...
    ) -> UpdateNFSFileShareOutputTypeDef:
        """
        Updates a Network File System (NFS) file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_nfs_file_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_nfs_file_share)
        """

    def update_smb_file_share(
        self,
        *,
        FileShareARN: str,
        KMSEncrypted: bool = ...,
        KMSKey: str = ...,
        DefaultStorageClass: str = ...,
        ObjectACL: ObjectACLType = ...,
        ReadOnly: bool = ...,
        GuessMIMETypeEnabled: bool = ...,
        RequesterPays: bool = ...,
        SMBACLEnabled: bool = ...,
        AccessBasedEnumeration: bool = ...,
        AdminUserList: Sequence[str] = ...,
        ValidUserList: Sequence[str] = ...,
        InvalidUserList: Sequence[str] = ...,
        AuditDestinationARN: str = ...,
        CaseSensitivity: CaseSensitivityType = ...,
        FileShareName: str = ...,
        CacheAttributes: CacheAttributesTypeDef = ...,
        NotificationPolicy: str = ...,
        OplocksEnabled: bool = ...
    ) -> UpdateSMBFileShareOutputTypeDef:
        """
        Updates a Server Message Block (SMB) file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_smb_file_share)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_smb_file_share)
        """

    def update_smb_file_share_visibility(
        self, *, GatewayARN: str, FileSharesVisible: bool
    ) -> UpdateSMBFileShareVisibilityOutputTypeDef:
        """
        Controls whether the shares on an S3 File Gateway are visible in a net view or
        browse list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_smb_file_share_visibility)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_smb_file_share_visibility)
        """

    def update_smb_local_groups(
        self, *, GatewayARN: str, SMBLocalGroups: SMBLocalGroupsTypeDef
    ) -> UpdateSMBLocalGroupsOutputTypeDef:
        """
        Updates the list of Active Directory users and groups that have special
        permissions for SMB file shares on the gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_smb_local_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_smb_local_groups)
        """

    def update_smb_security_strategy(
        self, *, GatewayARN: str, SMBSecurityStrategy: SMBSecurityStrategyType
    ) -> UpdateSMBSecurityStrategyOutputTypeDef:
        """
        Updates the SMB security strategy on a file gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_smb_security_strategy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_smb_security_strategy)
        """

    def update_snapshot_schedule(
        self,
        *,
        VolumeARN: str,
        StartAt: int,
        RecurrenceInHours: int,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> UpdateSnapshotScheduleOutputTypeDef:
        """
        Updates a snapshot schedule configured for a gateway volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_snapshot_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_snapshot_schedule)
        """

    def update_vtl_device_type(
        self, *, VTLDeviceARN: str, DeviceType: str
    ) -> UpdateVTLDeviceTypeOutputTypeDef:
        """
        Updates the type of medium changer in a tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.update_vtl_device_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#update_vtl_device_type)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_tape_archives"]
    ) -> DescribeTapeArchivesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_tape_recovery_points"]
    ) -> DescribeTapeRecoveryPointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tapes"]) -> DescribeTapesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vtl_devices"]
    ) -> DescribeVTLDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_file_shares"]) -> ListFileSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_file_system_associations"]
    ) -> ListFileSystemAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tape_pools"]) -> ListTapePoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tapes"]) -> ListTapesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_volumes"]) -> ListVolumesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/client/#get_paginator)
        """
