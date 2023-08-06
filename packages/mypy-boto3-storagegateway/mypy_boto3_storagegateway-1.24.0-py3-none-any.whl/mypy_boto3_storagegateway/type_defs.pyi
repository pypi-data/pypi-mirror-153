"""
Type annotations for storagegateway service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/type_defs/)

Usage::

    ```python
    from mypy_boto3_storagegateway.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ActiveDirectoryStatusType,
    AvailabilityMonitorTestStatusType,
    CaseSensitivityType,
    FileShareTypeType,
    GatewayCapacityType,
    HostEnvironmentType,
    ObjectACLType,
    PoolStatusType,
    RetentionLockTypeType,
    SMBSecurityStrategyType,
    TapeStorageClassType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "AddCacheInputRequestTypeDef",
    "AddUploadBufferInputRequestTypeDef",
    "AddWorkingStorageInputRequestTypeDef",
    "AssignTapePoolInputRequestTypeDef",
    "CacheAttributesTypeDef",
    "EndpointNetworkConfigurationTypeDef",
    "AttachVolumeInputRequestTypeDef",
    "AutomaticTapeCreationRuleTypeDef",
    "BandwidthRateLimitIntervalTypeDef",
    "VolumeiSCSIAttributesTypeDef",
    "CancelArchivalInputRequestTypeDef",
    "CancelRetrievalInputRequestTypeDef",
    "ChapInfoTypeDef",
    "NFSFileShareDefaultsTypeDef",
    "DeleteAutomaticTapeCreationPolicyInputRequestTypeDef",
    "DeleteBandwidthRateLimitInputRequestTypeDef",
    "DeleteChapCredentialsInputRequestTypeDef",
    "DeleteFileShareInputRequestTypeDef",
    "DeleteGatewayInputRequestTypeDef",
    "DeleteSnapshotScheduleInputRequestTypeDef",
    "DeleteTapeArchiveInputRequestTypeDef",
    "DeleteTapeInputRequestTypeDef",
    "DeleteTapePoolInputRequestTypeDef",
    "DeleteVolumeInputRequestTypeDef",
    "DescribeAvailabilityMonitorTestInputRequestTypeDef",
    "DescribeBandwidthRateLimitInputRequestTypeDef",
    "DescribeBandwidthRateLimitScheduleInputRequestTypeDef",
    "DescribeCacheInputRequestTypeDef",
    "DescribeCachediSCSIVolumesInputRequestTypeDef",
    "DescribeChapCredentialsInputRequestTypeDef",
    "DescribeFileSystemAssociationsInputRequestTypeDef",
    "DescribeGatewayInformationInputRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "DescribeMaintenanceStartTimeInputRequestTypeDef",
    "DescribeNFSFileSharesInputRequestTypeDef",
    "DescribeSMBFileSharesInputRequestTypeDef",
    "DescribeSMBSettingsInputRequestTypeDef",
    "SMBLocalGroupsTypeDef",
    "DescribeSnapshotScheduleInputRequestTypeDef",
    "DescribeStorediSCSIVolumesInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeTapeArchivesInputRequestTypeDef",
    "TapeArchiveTypeDef",
    "DescribeTapeRecoveryPointsInputRequestTypeDef",
    "TapeRecoveryPointInfoTypeDef",
    "DescribeTapesInputRequestTypeDef",
    "TapeTypeDef",
    "DescribeUploadBufferInputRequestTypeDef",
    "DescribeVTLDevicesInputRequestTypeDef",
    "DescribeWorkingStorageInputRequestTypeDef",
    "DetachVolumeInputRequestTypeDef",
    "DeviceiSCSIAttributesTypeDef",
    "DisableGatewayInputRequestTypeDef",
    "DisassociateFileSystemInputRequestTypeDef",
    "DiskTypeDef",
    "FileShareInfoTypeDef",
    "FileSystemAssociationStatusDetailTypeDef",
    "FileSystemAssociationSummaryTypeDef",
    "GatewayInfoTypeDef",
    "JoinDomainInputRequestTypeDef",
    "ListAutomaticTapeCreationPoliciesInputRequestTypeDef",
    "ListFileSharesInputRequestTypeDef",
    "ListFileSystemAssociationsInputRequestTypeDef",
    "ListGatewaysInputRequestTypeDef",
    "ListLocalDisksInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTapePoolsInputRequestTypeDef",
    "PoolInfoTypeDef",
    "ListTapesInputRequestTypeDef",
    "TapeInfoTypeDef",
    "ListVolumeInitiatorsInputRequestTypeDef",
    "ListVolumeRecoveryPointsInputRequestTypeDef",
    "VolumeRecoveryPointInfoTypeDef",
    "ListVolumesInputRequestTypeDef",
    "VolumeInfoTypeDef",
    "NotifyWhenUploadedInputRequestTypeDef",
    "RefreshCacheInputRequestTypeDef",
    "RemoveTagsFromResourceInputRequestTypeDef",
    "ResetCacheInputRequestTypeDef",
    "RetrieveTapeArchiveInputRequestTypeDef",
    "RetrieveTapeRecoveryPointInputRequestTypeDef",
    "SetLocalConsolePasswordInputRequestTypeDef",
    "SetSMBGuestPasswordInputRequestTypeDef",
    "ShutdownGatewayInputRequestTypeDef",
    "StartAvailabilityMonitorTestInputRequestTypeDef",
    "StartGatewayInputRequestTypeDef",
    "UpdateBandwidthRateLimitInputRequestTypeDef",
    "UpdateChapCredentialsInputRequestTypeDef",
    "UpdateGatewayInformationInputRequestTypeDef",
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    "UpdateMaintenanceStartTimeInputRequestTypeDef",
    "UpdateSMBFileShareVisibilityInputRequestTypeDef",
    "UpdateSMBSecurityStrategyInputRequestTypeDef",
    "UpdateVTLDeviceTypeInputRequestTypeDef",
    "ActivateGatewayInputRequestTypeDef",
    "AddTagsToResourceInputRequestTypeDef",
    "CreateCachediSCSIVolumeInputRequestTypeDef",
    "CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef",
    "CreateSnapshotInputRequestTypeDef",
    "CreateStorediSCSIVolumeInputRequestTypeDef",
    "CreateTapePoolInputRequestTypeDef",
    "CreateTapeWithBarcodeInputRequestTypeDef",
    "CreateTapesInputRequestTypeDef",
    "UpdateSnapshotScheduleInputRequestTypeDef",
    "ActivateGatewayOutputTypeDef",
    "AddCacheOutputTypeDef",
    "AddTagsToResourceOutputTypeDef",
    "AddUploadBufferOutputTypeDef",
    "AddWorkingStorageOutputTypeDef",
    "AssignTapePoolOutputTypeDef",
    "AssociateFileSystemOutputTypeDef",
    "AttachVolumeOutputTypeDef",
    "CancelArchivalOutputTypeDef",
    "CancelRetrievalOutputTypeDef",
    "CreateCachediSCSIVolumeOutputTypeDef",
    "CreateNFSFileShareOutputTypeDef",
    "CreateSMBFileShareOutputTypeDef",
    "CreateSnapshotFromVolumeRecoveryPointOutputTypeDef",
    "CreateSnapshotOutputTypeDef",
    "CreateStorediSCSIVolumeOutputTypeDef",
    "CreateTapePoolOutputTypeDef",
    "CreateTapeWithBarcodeOutputTypeDef",
    "CreateTapesOutputTypeDef",
    "DeleteAutomaticTapeCreationPolicyOutputTypeDef",
    "DeleteBandwidthRateLimitOutputTypeDef",
    "DeleteChapCredentialsOutputTypeDef",
    "DeleteFileShareOutputTypeDef",
    "DeleteGatewayOutputTypeDef",
    "DeleteSnapshotScheduleOutputTypeDef",
    "DeleteTapeArchiveOutputTypeDef",
    "DeleteTapeOutputTypeDef",
    "DeleteTapePoolOutputTypeDef",
    "DeleteVolumeOutputTypeDef",
    "DescribeAvailabilityMonitorTestOutputTypeDef",
    "DescribeBandwidthRateLimitOutputTypeDef",
    "DescribeCacheOutputTypeDef",
    "DescribeMaintenanceStartTimeOutputTypeDef",
    "DescribeSnapshotScheduleOutputTypeDef",
    "DescribeUploadBufferOutputTypeDef",
    "DescribeWorkingStorageOutputTypeDef",
    "DetachVolumeOutputTypeDef",
    "DisableGatewayOutputTypeDef",
    "DisassociateFileSystemOutputTypeDef",
    "JoinDomainOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListVolumeInitiatorsOutputTypeDef",
    "NotifyWhenUploadedOutputTypeDef",
    "RefreshCacheOutputTypeDef",
    "RemoveTagsFromResourceOutputTypeDef",
    "ResetCacheOutputTypeDef",
    "RetrieveTapeArchiveOutputTypeDef",
    "RetrieveTapeRecoveryPointOutputTypeDef",
    "SetLocalConsolePasswordOutputTypeDef",
    "SetSMBGuestPasswordOutputTypeDef",
    "ShutdownGatewayOutputTypeDef",
    "StartAvailabilityMonitorTestOutputTypeDef",
    "StartGatewayOutputTypeDef",
    "UpdateAutomaticTapeCreationPolicyOutputTypeDef",
    "UpdateBandwidthRateLimitOutputTypeDef",
    "UpdateBandwidthRateLimitScheduleOutputTypeDef",
    "UpdateChapCredentialsOutputTypeDef",
    "UpdateFileSystemAssociationOutputTypeDef",
    "UpdateGatewayInformationOutputTypeDef",
    "UpdateGatewaySoftwareNowOutputTypeDef",
    "UpdateMaintenanceStartTimeOutputTypeDef",
    "UpdateNFSFileShareOutputTypeDef",
    "UpdateSMBFileShareOutputTypeDef",
    "UpdateSMBFileShareVisibilityOutputTypeDef",
    "UpdateSMBLocalGroupsOutputTypeDef",
    "UpdateSMBSecurityStrategyOutputTypeDef",
    "UpdateSnapshotScheduleOutputTypeDef",
    "UpdateVTLDeviceTypeOutputTypeDef",
    "CreateSMBFileShareInputRequestTypeDef",
    "SMBFileShareInfoTypeDef",
    "UpdateFileSystemAssociationInputRequestTypeDef",
    "UpdateSMBFileShareInputRequestTypeDef",
    "AssociateFileSystemInputRequestTypeDef",
    "AutomaticTapeCreationPolicyInfoTypeDef",
    "UpdateAutomaticTapeCreationPolicyInputRequestTypeDef",
    "DescribeBandwidthRateLimitScheduleOutputTypeDef",
    "UpdateBandwidthRateLimitScheduleInputRequestTypeDef",
    "CachediSCSIVolumeTypeDef",
    "StorediSCSIVolumeTypeDef",
    "DescribeChapCredentialsOutputTypeDef",
    "CreateNFSFileShareInputRequestTypeDef",
    "NFSFileShareInfoTypeDef",
    "UpdateNFSFileShareInputRequestTypeDef",
    "DescribeGatewayInformationOutputTypeDef",
    "DescribeSMBSettingsOutputTypeDef",
    "UpdateSMBLocalGroupsInputRequestTypeDef",
    "DescribeTapeArchivesInputDescribeTapeArchivesPaginateTypeDef",
    "DescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef",
    "DescribeTapesInputDescribeTapesPaginateTypeDef",
    "DescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef",
    "ListFileSharesInputListFileSharesPaginateTypeDef",
    "ListFileSystemAssociationsInputListFileSystemAssociationsPaginateTypeDef",
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTapePoolsInputListTapePoolsPaginateTypeDef",
    "ListTapesInputListTapesPaginateTypeDef",
    "ListVolumesInputListVolumesPaginateTypeDef",
    "DescribeTapeArchivesOutputTypeDef",
    "DescribeTapeRecoveryPointsOutputTypeDef",
    "DescribeTapesOutputTypeDef",
    "VTLDeviceTypeDef",
    "ListLocalDisksOutputTypeDef",
    "ListFileSharesOutputTypeDef",
    "FileSystemAssociationInfoTypeDef",
    "ListFileSystemAssociationsOutputTypeDef",
    "ListGatewaysOutputTypeDef",
    "ListTapePoolsOutputTypeDef",
    "ListTapesOutputTypeDef",
    "ListVolumeRecoveryPointsOutputTypeDef",
    "ListVolumesOutputTypeDef",
    "DescribeSMBFileSharesOutputTypeDef",
    "ListAutomaticTapeCreationPoliciesOutputTypeDef",
    "DescribeCachediSCSIVolumesOutputTypeDef",
    "DescribeStorediSCSIVolumesOutputTypeDef",
    "DescribeNFSFileSharesOutputTypeDef",
    "DescribeVTLDevicesOutputTypeDef",
    "DescribeFileSystemAssociationsOutputTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

AddCacheInputRequestTypeDef = TypedDict(
    "AddCacheInputRequestTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": Sequence[str],
    },
)

AddUploadBufferInputRequestTypeDef = TypedDict(
    "AddUploadBufferInputRequestTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": Sequence[str],
    },
)

AddWorkingStorageInputRequestTypeDef = TypedDict(
    "AddWorkingStorageInputRequestTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": Sequence[str],
    },
)

_RequiredAssignTapePoolInputRequestTypeDef = TypedDict(
    "_RequiredAssignTapePoolInputRequestTypeDef",
    {
        "TapeARN": str,
        "PoolId": str,
    },
)
_OptionalAssignTapePoolInputRequestTypeDef = TypedDict(
    "_OptionalAssignTapePoolInputRequestTypeDef",
    {
        "BypassGovernanceRetention": bool,
    },
    total=False,
)

class AssignTapePoolInputRequestTypeDef(
    _RequiredAssignTapePoolInputRequestTypeDef, _OptionalAssignTapePoolInputRequestTypeDef
):
    pass

CacheAttributesTypeDef = TypedDict(
    "CacheAttributesTypeDef",
    {
        "CacheStaleTimeoutInSeconds": int,
    },
    total=False,
)

EndpointNetworkConfigurationTypeDef = TypedDict(
    "EndpointNetworkConfigurationTypeDef",
    {
        "IpAddresses": Sequence[str],
    },
    total=False,
)

_RequiredAttachVolumeInputRequestTypeDef = TypedDict(
    "_RequiredAttachVolumeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "VolumeARN": str,
        "NetworkInterfaceId": str,
    },
)
_OptionalAttachVolumeInputRequestTypeDef = TypedDict(
    "_OptionalAttachVolumeInputRequestTypeDef",
    {
        "TargetName": str,
        "DiskId": str,
    },
    total=False,
)

class AttachVolumeInputRequestTypeDef(
    _RequiredAttachVolumeInputRequestTypeDef, _OptionalAttachVolumeInputRequestTypeDef
):
    pass

_RequiredAutomaticTapeCreationRuleTypeDef = TypedDict(
    "_RequiredAutomaticTapeCreationRuleTypeDef",
    {
        "TapeBarcodePrefix": str,
        "PoolId": str,
        "TapeSizeInBytes": int,
        "MinimumNumTapes": int,
    },
)
_OptionalAutomaticTapeCreationRuleTypeDef = TypedDict(
    "_OptionalAutomaticTapeCreationRuleTypeDef",
    {
        "Worm": bool,
    },
    total=False,
)

class AutomaticTapeCreationRuleTypeDef(
    _RequiredAutomaticTapeCreationRuleTypeDef, _OptionalAutomaticTapeCreationRuleTypeDef
):
    pass

_RequiredBandwidthRateLimitIntervalTypeDef = TypedDict(
    "_RequiredBandwidthRateLimitIntervalTypeDef",
    {
        "StartHourOfDay": int,
        "StartMinuteOfHour": int,
        "EndHourOfDay": int,
        "EndMinuteOfHour": int,
        "DaysOfWeek": List[int],
    },
)
_OptionalBandwidthRateLimitIntervalTypeDef = TypedDict(
    "_OptionalBandwidthRateLimitIntervalTypeDef",
    {
        "AverageUploadRateLimitInBitsPerSec": int,
        "AverageDownloadRateLimitInBitsPerSec": int,
    },
    total=False,
)

class BandwidthRateLimitIntervalTypeDef(
    _RequiredBandwidthRateLimitIntervalTypeDef, _OptionalBandwidthRateLimitIntervalTypeDef
):
    pass

VolumeiSCSIAttributesTypeDef = TypedDict(
    "VolumeiSCSIAttributesTypeDef",
    {
        "TargetARN": str,
        "NetworkInterfaceId": str,
        "NetworkInterfacePort": int,
        "LunNumber": int,
        "ChapEnabled": bool,
    },
    total=False,
)

CancelArchivalInputRequestTypeDef = TypedDict(
    "CancelArchivalInputRequestTypeDef",
    {
        "GatewayARN": str,
        "TapeARN": str,
    },
)

CancelRetrievalInputRequestTypeDef = TypedDict(
    "CancelRetrievalInputRequestTypeDef",
    {
        "GatewayARN": str,
        "TapeARN": str,
    },
)

ChapInfoTypeDef = TypedDict(
    "ChapInfoTypeDef",
    {
        "TargetARN": str,
        "SecretToAuthenticateInitiator": str,
        "InitiatorName": str,
        "SecretToAuthenticateTarget": str,
    },
    total=False,
)

NFSFileShareDefaultsTypeDef = TypedDict(
    "NFSFileShareDefaultsTypeDef",
    {
        "FileMode": str,
        "DirectoryMode": str,
        "GroupId": int,
        "OwnerId": int,
    },
    total=False,
)

DeleteAutomaticTapeCreationPolicyInputRequestTypeDef = TypedDict(
    "DeleteAutomaticTapeCreationPolicyInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DeleteBandwidthRateLimitInputRequestTypeDef = TypedDict(
    "DeleteBandwidthRateLimitInputRequestTypeDef",
    {
        "GatewayARN": str,
        "BandwidthType": str,
    },
)

DeleteChapCredentialsInputRequestTypeDef = TypedDict(
    "DeleteChapCredentialsInputRequestTypeDef",
    {
        "TargetARN": str,
        "InitiatorName": str,
    },
)

_RequiredDeleteFileShareInputRequestTypeDef = TypedDict(
    "_RequiredDeleteFileShareInputRequestTypeDef",
    {
        "FileShareARN": str,
    },
)
_OptionalDeleteFileShareInputRequestTypeDef = TypedDict(
    "_OptionalDeleteFileShareInputRequestTypeDef",
    {
        "ForceDelete": bool,
    },
    total=False,
)

class DeleteFileShareInputRequestTypeDef(
    _RequiredDeleteFileShareInputRequestTypeDef, _OptionalDeleteFileShareInputRequestTypeDef
):
    pass

DeleteGatewayInputRequestTypeDef = TypedDict(
    "DeleteGatewayInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DeleteSnapshotScheduleInputRequestTypeDef = TypedDict(
    "DeleteSnapshotScheduleInputRequestTypeDef",
    {
        "VolumeARN": str,
    },
)

_RequiredDeleteTapeArchiveInputRequestTypeDef = TypedDict(
    "_RequiredDeleteTapeArchiveInputRequestTypeDef",
    {
        "TapeARN": str,
    },
)
_OptionalDeleteTapeArchiveInputRequestTypeDef = TypedDict(
    "_OptionalDeleteTapeArchiveInputRequestTypeDef",
    {
        "BypassGovernanceRetention": bool,
    },
    total=False,
)

class DeleteTapeArchiveInputRequestTypeDef(
    _RequiredDeleteTapeArchiveInputRequestTypeDef, _OptionalDeleteTapeArchiveInputRequestTypeDef
):
    pass

_RequiredDeleteTapeInputRequestTypeDef = TypedDict(
    "_RequiredDeleteTapeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "TapeARN": str,
    },
)
_OptionalDeleteTapeInputRequestTypeDef = TypedDict(
    "_OptionalDeleteTapeInputRequestTypeDef",
    {
        "BypassGovernanceRetention": bool,
    },
    total=False,
)

class DeleteTapeInputRequestTypeDef(
    _RequiredDeleteTapeInputRequestTypeDef, _OptionalDeleteTapeInputRequestTypeDef
):
    pass

DeleteTapePoolInputRequestTypeDef = TypedDict(
    "DeleteTapePoolInputRequestTypeDef",
    {
        "PoolARN": str,
    },
)

DeleteVolumeInputRequestTypeDef = TypedDict(
    "DeleteVolumeInputRequestTypeDef",
    {
        "VolumeARN": str,
    },
)

DescribeAvailabilityMonitorTestInputRequestTypeDef = TypedDict(
    "DescribeAvailabilityMonitorTestInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DescribeBandwidthRateLimitInputRequestTypeDef = TypedDict(
    "DescribeBandwidthRateLimitInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DescribeBandwidthRateLimitScheduleInputRequestTypeDef = TypedDict(
    "DescribeBandwidthRateLimitScheduleInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DescribeCacheInputRequestTypeDef = TypedDict(
    "DescribeCacheInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DescribeCachediSCSIVolumesInputRequestTypeDef = TypedDict(
    "DescribeCachediSCSIVolumesInputRequestTypeDef",
    {
        "VolumeARNs": Sequence[str],
    },
)

DescribeChapCredentialsInputRequestTypeDef = TypedDict(
    "DescribeChapCredentialsInputRequestTypeDef",
    {
        "TargetARN": str,
    },
)

DescribeFileSystemAssociationsInputRequestTypeDef = TypedDict(
    "DescribeFileSystemAssociationsInputRequestTypeDef",
    {
        "FileSystemAssociationARNList": Sequence[str],
    },
)

DescribeGatewayInformationInputRequestTypeDef = TypedDict(
    "DescribeGatewayInformationInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "Ipv4Address": str,
        "MacAddress": str,
        "Ipv6Address": str,
    },
    total=False,
)

DescribeMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "DescribeMaintenanceStartTimeInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

DescribeNFSFileSharesInputRequestTypeDef = TypedDict(
    "DescribeNFSFileSharesInputRequestTypeDef",
    {
        "FileShareARNList": Sequence[str],
    },
)

DescribeSMBFileSharesInputRequestTypeDef = TypedDict(
    "DescribeSMBFileSharesInputRequestTypeDef",
    {
        "FileShareARNList": Sequence[str],
    },
)

DescribeSMBSettingsInputRequestTypeDef = TypedDict(
    "DescribeSMBSettingsInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

SMBLocalGroupsTypeDef = TypedDict(
    "SMBLocalGroupsTypeDef",
    {
        "GatewayAdmins": List[str],
    },
    total=False,
)

DescribeSnapshotScheduleInputRequestTypeDef = TypedDict(
    "DescribeSnapshotScheduleInputRequestTypeDef",
    {
        "VolumeARN": str,
    },
)

DescribeStorediSCSIVolumesInputRequestTypeDef = TypedDict(
    "DescribeStorediSCSIVolumesInputRequestTypeDef",
    {
        "VolumeARNs": Sequence[str],
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

DescribeTapeArchivesInputRequestTypeDef = TypedDict(
    "DescribeTapeArchivesInputRequestTypeDef",
    {
        "TapeARNs": Sequence[str],
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

TapeArchiveTypeDef = TypedDict(
    "TapeArchiveTypeDef",
    {
        "TapeARN": str,
        "TapeBarcode": str,
        "TapeCreatedDate": datetime,
        "TapeSizeInBytes": int,
        "CompletionTime": datetime,
        "RetrievedTo": str,
        "TapeStatus": str,
        "TapeUsedInBytes": int,
        "KMSKey": str,
        "PoolId": str,
        "Worm": bool,
        "RetentionStartDate": datetime,
        "PoolEntryDate": datetime,
    },
    total=False,
)

_RequiredDescribeTapeRecoveryPointsInputRequestTypeDef = TypedDict(
    "_RequiredDescribeTapeRecoveryPointsInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeTapeRecoveryPointsInputRequestTypeDef = TypedDict(
    "_OptionalDescribeTapeRecoveryPointsInputRequestTypeDef",
    {
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class DescribeTapeRecoveryPointsInputRequestTypeDef(
    _RequiredDescribeTapeRecoveryPointsInputRequestTypeDef,
    _OptionalDescribeTapeRecoveryPointsInputRequestTypeDef,
):
    pass

TapeRecoveryPointInfoTypeDef = TypedDict(
    "TapeRecoveryPointInfoTypeDef",
    {
        "TapeARN": str,
        "TapeRecoveryPointTime": datetime,
        "TapeSizeInBytes": int,
        "TapeStatus": str,
    },
    total=False,
)

_RequiredDescribeTapesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeTapesInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeTapesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeTapesInputRequestTypeDef",
    {
        "TapeARNs": Sequence[str],
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class DescribeTapesInputRequestTypeDef(
    _RequiredDescribeTapesInputRequestTypeDef, _OptionalDescribeTapesInputRequestTypeDef
):
    pass

TapeTypeDef = TypedDict(
    "TapeTypeDef",
    {
        "TapeARN": str,
        "TapeBarcode": str,
        "TapeCreatedDate": datetime,
        "TapeSizeInBytes": int,
        "TapeStatus": str,
        "VTLDevice": str,
        "Progress": float,
        "TapeUsedInBytes": int,
        "KMSKey": str,
        "PoolId": str,
        "Worm": bool,
        "RetentionStartDate": datetime,
        "PoolEntryDate": datetime,
    },
    total=False,
)

DescribeUploadBufferInputRequestTypeDef = TypedDict(
    "DescribeUploadBufferInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredDescribeVTLDevicesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVTLDevicesInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeVTLDevicesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVTLDevicesInputRequestTypeDef",
    {
        "VTLDeviceARNs": Sequence[str],
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class DescribeVTLDevicesInputRequestTypeDef(
    _RequiredDescribeVTLDevicesInputRequestTypeDef, _OptionalDescribeVTLDevicesInputRequestTypeDef
):
    pass

DescribeWorkingStorageInputRequestTypeDef = TypedDict(
    "DescribeWorkingStorageInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredDetachVolumeInputRequestTypeDef = TypedDict(
    "_RequiredDetachVolumeInputRequestTypeDef",
    {
        "VolumeARN": str,
    },
)
_OptionalDetachVolumeInputRequestTypeDef = TypedDict(
    "_OptionalDetachVolumeInputRequestTypeDef",
    {
        "ForceDetach": bool,
    },
    total=False,
)

class DetachVolumeInputRequestTypeDef(
    _RequiredDetachVolumeInputRequestTypeDef, _OptionalDetachVolumeInputRequestTypeDef
):
    pass

DeviceiSCSIAttributesTypeDef = TypedDict(
    "DeviceiSCSIAttributesTypeDef",
    {
        "TargetARN": str,
        "NetworkInterfaceId": str,
        "NetworkInterfacePort": int,
        "ChapEnabled": bool,
    },
    total=False,
)

DisableGatewayInputRequestTypeDef = TypedDict(
    "DisableGatewayInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredDisassociateFileSystemInputRequestTypeDef = TypedDict(
    "_RequiredDisassociateFileSystemInputRequestTypeDef",
    {
        "FileSystemAssociationARN": str,
    },
)
_OptionalDisassociateFileSystemInputRequestTypeDef = TypedDict(
    "_OptionalDisassociateFileSystemInputRequestTypeDef",
    {
        "ForceDelete": bool,
    },
    total=False,
)

class DisassociateFileSystemInputRequestTypeDef(
    _RequiredDisassociateFileSystemInputRequestTypeDef,
    _OptionalDisassociateFileSystemInputRequestTypeDef,
):
    pass

DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "DiskId": str,
        "DiskPath": str,
        "DiskNode": str,
        "DiskStatus": str,
        "DiskSizeInBytes": int,
        "DiskAllocationType": str,
        "DiskAllocationResource": str,
        "DiskAttributeList": List[str],
    },
    total=False,
)

FileShareInfoTypeDef = TypedDict(
    "FileShareInfoTypeDef",
    {
        "FileShareType": FileShareTypeType,
        "FileShareARN": str,
        "FileShareId": str,
        "FileShareStatus": str,
        "GatewayARN": str,
    },
    total=False,
)

FileSystemAssociationStatusDetailTypeDef = TypedDict(
    "FileSystemAssociationStatusDetailTypeDef",
    {
        "ErrorCode": str,
    },
    total=False,
)

FileSystemAssociationSummaryTypeDef = TypedDict(
    "FileSystemAssociationSummaryTypeDef",
    {
        "FileSystemAssociationId": str,
        "FileSystemAssociationARN": str,
        "FileSystemAssociationStatus": str,
        "GatewayARN": str,
    },
    total=False,
)

GatewayInfoTypeDef = TypedDict(
    "GatewayInfoTypeDef",
    {
        "GatewayId": str,
        "GatewayARN": str,
        "GatewayType": str,
        "GatewayOperationalState": str,
        "GatewayName": str,
        "Ec2InstanceId": str,
        "Ec2InstanceRegion": str,
        "HostEnvironment": HostEnvironmentType,
        "HostEnvironmentId": str,
    },
    total=False,
)

_RequiredJoinDomainInputRequestTypeDef = TypedDict(
    "_RequiredJoinDomainInputRequestTypeDef",
    {
        "GatewayARN": str,
        "DomainName": str,
        "UserName": str,
        "Password": str,
    },
)
_OptionalJoinDomainInputRequestTypeDef = TypedDict(
    "_OptionalJoinDomainInputRequestTypeDef",
    {
        "OrganizationalUnit": str,
        "DomainControllers": Sequence[str],
        "TimeoutInSeconds": int,
    },
    total=False,
)

class JoinDomainInputRequestTypeDef(
    _RequiredJoinDomainInputRequestTypeDef, _OptionalJoinDomainInputRequestTypeDef
):
    pass

ListAutomaticTapeCreationPoliciesInputRequestTypeDef = TypedDict(
    "ListAutomaticTapeCreationPoliciesInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
    total=False,
)

ListFileSharesInputRequestTypeDef = TypedDict(
    "ListFileSharesInputRequestTypeDef",
    {
        "GatewayARN": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

ListFileSystemAssociationsInputRequestTypeDef = TypedDict(
    "ListFileSystemAssociationsInputRequestTypeDef",
    {
        "GatewayARN": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

ListGatewaysInputRequestTypeDef = TypedDict(
    "ListGatewaysInputRequestTypeDef",
    {
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

ListLocalDisksInputRequestTypeDef = TypedDict(
    "ListLocalDisksInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass

ListTapePoolsInputRequestTypeDef = TypedDict(
    "ListTapePoolsInputRequestTypeDef",
    {
        "PoolARNs": Sequence[str],
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

PoolInfoTypeDef = TypedDict(
    "PoolInfoTypeDef",
    {
        "PoolARN": str,
        "PoolName": str,
        "StorageClass": TapeStorageClassType,
        "RetentionLockType": RetentionLockTypeType,
        "RetentionLockTimeInDays": int,
        "PoolStatus": PoolStatusType,
    },
    total=False,
)

ListTapesInputRequestTypeDef = TypedDict(
    "ListTapesInputRequestTypeDef",
    {
        "TapeARNs": Sequence[str],
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

TapeInfoTypeDef = TypedDict(
    "TapeInfoTypeDef",
    {
        "TapeARN": str,
        "TapeBarcode": str,
        "TapeSizeInBytes": int,
        "TapeStatus": str,
        "GatewayARN": str,
        "PoolId": str,
        "RetentionStartDate": datetime,
        "PoolEntryDate": datetime,
    },
    total=False,
)

ListVolumeInitiatorsInputRequestTypeDef = TypedDict(
    "ListVolumeInitiatorsInputRequestTypeDef",
    {
        "VolumeARN": str,
    },
)

ListVolumeRecoveryPointsInputRequestTypeDef = TypedDict(
    "ListVolumeRecoveryPointsInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

VolumeRecoveryPointInfoTypeDef = TypedDict(
    "VolumeRecoveryPointInfoTypeDef",
    {
        "VolumeARN": str,
        "VolumeSizeInBytes": int,
        "VolumeUsageInBytes": int,
        "VolumeRecoveryPointTime": str,
    },
    total=False,
)

ListVolumesInputRequestTypeDef = TypedDict(
    "ListVolumesInputRequestTypeDef",
    {
        "GatewayARN": str,
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

VolumeInfoTypeDef = TypedDict(
    "VolumeInfoTypeDef",
    {
        "VolumeARN": str,
        "VolumeId": str,
        "GatewayARN": str,
        "GatewayId": str,
        "VolumeType": str,
        "VolumeSizeInBytes": int,
        "VolumeAttachmentStatus": str,
    },
    total=False,
)

NotifyWhenUploadedInputRequestTypeDef = TypedDict(
    "NotifyWhenUploadedInputRequestTypeDef",
    {
        "FileShareARN": str,
    },
)

_RequiredRefreshCacheInputRequestTypeDef = TypedDict(
    "_RequiredRefreshCacheInputRequestTypeDef",
    {
        "FileShareARN": str,
    },
)
_OptionalRefreshCacheInputRequestTypeDef = TypedDict(
    "_OptionalRefreshCacheInputRequestTypeDef",
    {
        "FolderList": Sequence[str],
        "Recursive": bool,
    },
    total=False,
)

class RefreshCacheInputRequestTypeDef(
    _RequiredRefreshCacheInputRequestTypeDef, _OptionalRefreshCacheInputRequestTypeDef
):
    pass

RemoveTagsFromResourceInputRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

ResetCacheInputRequestTypeDef = TypedDict(
    "ResetCacheInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

RetrieveTapeArchiveInputRequestTypeDef = TypedDict(
    "RetrieveTapeArchiveInputRequestTypeDef",
    {
        "TapeARN": str,
        "GatewayARN": str,
    },
)

RetrieveTapeRecoveryPointInputRequestTypeDef = TypedDict(
    "RetrieveTapeRecoveryPointInputRequestTypeDef",
    {
        "TapeARN": str,
        "GatewayARN": str,
    },
)

SetLocalConsolePasswordInputRequestTypeDef = TypedDict(
    "SetLocalConsolePasswordInputRequestTypeDef",
    {
        "GatewayARN": str,
        "LocalConsolePassword": str,
    },
)

SetSMBGuestPasswordInputRequestTypeDef = TypedDict(
    "SetSMBGuestPasswordInputRequestTypeDef",
    {
        "GatewayARN": str,
        "Password": str,
    },
)

ShutdownGatewayInputRequestTypeDef = TypedDict(
    "ShutdownGatewayInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

StartAvailabilityMonitorTestInputRequestTypeDef = TypedDict(
    "StartAvailabilityMonitorTestInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

StartGatewayInputRequestTypeDef = TypedDict(
    "StartGatewayInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredUpdateBandwidthRateLimitInputRequestTypeDef = TypedDict(
    "_RequiredUpdateBandwidthRateLimitInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalUpdateBandwidthRateLimitInputRequestTypeDef = TypedDict(
    "_OptionalUpdateBandwidthRateLimitInputRequestTypeDef",
    {
        "AverageUploadRateLimitInBitsPerSec": int,
        "AverageDownloadRateLimitInBitsPerSec": int,
    },
    total=False,
)

class UpdateBandwidthRateLimitInputRequestTypeDef(
    _RequiredUpdateBandwidthRateLimitInputRequestTypeDef,
    _OptionalUpdateBandwidthRateLimitInputRequestTypeDef,
):
    pass

_RequiredUpdateChapCredentialsInputRequestTypeDef = TypedDict(
    "_RequiredUpdateChapCredentialsInputRequestTypeDef",
    {
        "TargetARN": str,
        "SecretToAuthenticateInitiator": str,
        "InitiatorName": str,
    },
)
_OptionalUpdateChapCredentialsInputRequestTypeDef = TypedDict(
    "_OptionalUpdateChapCredentialsInputRequestTypeDef",
    {
        "SecretToAuthenticateTarget": str,
    },
    total=False,
)

class UpdateChapCredentialsInputRequestTypeDef(
    _RequiredUpdateChapCredentialsInputRequestTypeDef,
    _OptionalUpdateChapCredentialsInputRequestTypeDef,
):
    pass

_RequiredUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayName": str,
        "GatewayTimezone": str,
        "CloudWatchLogGroupARN": str,
        "GatewayCapacity": GatewayCapacityType,
    },
    total=False,
)

class UpdateGatewayInformationInputRequestTypeDef(
    _RequiredUpdateGatewayInformationInputRequestTypeDef,
    _OptionalUpdateGatewayInformationInputRequestTypeDef,
):
    pass

UpdateGatewaySoftwareNowInputRequestTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    {
        "GatewayARN": str,
    },
)

_RequiredUpdateMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMaintenanceStartTimeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "HourOfDay": int,
        "MinuteOfHour": int,
    },
)
_OptionalUpdateMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMaintenanceStartTimeInputRequestTypeDef",
    {
        "DayOfWeek": int,
        "DayOfMonth": int,
    },
    total=False,
)

class UpdateMaintenanceStartTimeInputRequestTypeDef(
    _RequiredUpdateMaintenanceStartTimeInputRequestTypeDef,
    _OptionalUpdateMaintenanceStartTimeInputRequestTypeDef,
):
    pass

UpdateSMBFileShareVisibilityInputRequestTypeDef = TypedDict(
    "UpdateSMBFileShareVisibilityInputRequestTypeDef",
    {
        "GatewayARN": str,
        "FileSharesVisible": bool,
    },
)

UpdateSMBSecurityStrategyInputRequestTypeDef = TypedDict(
    "UpdateSMBSecurityStrategyInputRequestTypeDef",
    {
        "GatewayARN": str,
        "SMBSecurityStrategy": SMBSecurityStrategyType,
    },
)

UpdateVTLDeviceTypeInputRequestTypeDef = TypedDict(
    "UpdateVTLDeviceTypeInputRequestTypeDef",
    {
        "VTLDeviceARN": str,
        "DeviceType": str,
    },
)

_RequiredActivateGatewayInputRequestTypeDef = TypedDict(
    "_RequiredActivateGatewayInputRequestTypeDef",
    {
        "ActivationKey": str,
        "GatewayName": str,
        "GatewayTimezone": str,
        "GatewayRegion": str,
    },
)
_OptionalActivateGatewayInputRequestTypeDef = TypedDict(
    "_OptionalActivateGatewayInputRequestTypeDef",
    {
        "GatewayType": str,
        "TapeDriveType": str,
        "MediumChangerType": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class ActivateGatewayInputRequestTypeDef(
    _RequiredActivateGatewayInputRequestTypeDef, _OptionalActivateGatewayInputRequestTypeDef
):
    pass

AddTagsToResourceInputRequestTypeDef = TypedDict(
    "AddTagsToResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateCachediSCSIVolumeInputRequestTypeDef = TypedDict(
    "_RequiredCreateCachediSCSIVolumeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "VolumeSizeInBytes": int,
        "TargetName": str,
        "NetworkInterfaceId": str,
        "ClientToken": str,
    },
)
_OptionalCreateCachediSCSIVolumeInputRequestTypeDef = TypedDict(
    "_OptionalCreateCachediSCSIVolumeInputRequestTypeDef",
    {
        "SnapshotId": str,
        "SourceVolumeARN": str,
        "KMSEncrypted": bool,
        "KMSKey": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateCachediSCSIVolumeInputRequestTypeDef(
    _RequiredCreateCachediSCSIVolumeInputRequestTypeDef,
    _OptionalCreateCachediSCSIVolumeInputRequestTypeDef,
):
    pass

_RequiredCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef",
    {
        "VolumeARN": str,
        "SnapshotDescription": str,
    },
)
_OptionalCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef(
    _RequiredCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef,
    _OptionalCreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef,
):
    pass

_RequiredCreateSnapshotInputRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotInputRequestTypeDef",
    {
        "VolumeARN": str,
        "SnapshotDescription": str,
    },
)
_OptionalCreateSnapshotInputRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateSnapshotInputRequestTypeDef(
    _RequiredCreateSnapshotInputRequestTypeDef, _OptionalCreateSnapshotInputRequestTypeDef
):
    pass

_RequiredCreateStorediSCSIVolumeInputRequestTypeDef = TypedDict(
    "_RequiredCreateStorediSCSIVolumeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "DiskId": str,
        "PreserveExistingData": bool,
        "TargetName": str,
        "NetworkInterfaceId": str,
    },
)
_OptionalCreateStorediSCSIVolumeInputRequestTypeDef = TypedDict(
    "_OptionalCreateStorediSCSIVolumeInputRequestTypeDef",
    {
        "SnapshotId": str,
        "KMSEncrypted": bool,
        "KMSKey": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateStorediSCSIVolumeInputRequestTypeDef(
    _RequiredCreateStorediSCSIVolumeInputRequestTypeDef,
    _OptionalCreateStorediSCSIVolumeInputRequestTypeDef,
):
    pass

_RequiredCreateTapePoolInputRequestTypeDef = TypedDict(
    "_RequiredCreateTapePoolInputRequestTypeDef",
    {
        "PoolName": str,
        "StorageClass": TapeStorageClassType,
    },
)
_OptionalCreateTapePoolInputRequestTypeDef = TypedDict(
    "_OptionalCreateTapePoolInputRequestTypeDef",
    {
        "RetentionLockType": RetentionLockTypeType,
        "RetentionLockTimeInDays": int,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateTapePoolInputRequestTypeDef(
    _RequiredCreateTapePoolInputRequestTypeDef, _OptionalCreateTapePoolInputRequestTypeDef
):
    pass

_RequiredCreateTapeWithBarcodeInputRequestTypeDef = TypedDict(
    "_RequiredCreateTapeWithBarcodeInputRequestTypeDef",
    {
        "GatewayARN": str,
        "TapeSizeInBytes": int,
        "TapeBarcode": str,
    },
)
_OptionalCreateTapeWithBarcodeInputRequestTypeDef = TypedDict(
    "_OptionalCreateTapeWithBarcodeInputRequestTypeDef",
    {
        "KMSEncrypted": bool,
        "KMSKey": str,
        "PoolId": str,
        "Worm": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateTapeWithBarcodeInputRequestTypeDef(
    _RequiredCreateTapeWithBarcodeInputRequestTypeDef,
    _OptionalCreateTapeWithBarcodeInputRequestTypeDef,
):
    pass

_RequiredCreateTapesInputRequestTypeDef = TypedDict(
    "_RequiredCreateTapesInputRequestTypeDef",
    {
        "GatewayARN": str,
        "TapeSizeInBytes": int,
        "ClientToken": str,
        "NumTapesToCreate": int,
        "TapeBarcodePrefix": str,
    },
)
_OptionalCreateTapesInputRequestTypeDef = TypedDict(
    "_OptionalCreateTapesInputRequestTypeDef",
    {
        "KMSEncrypted": bool,
        "KMSKey": str,
        "PoolId": str,
        "Worm": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateTapesInputRequestTypeDef(
    _RequiredCreateTapesInputRequestTypeDef, _OptionalCreateTapesInputRequestTypeDef
):
    pass

_RequiredUpdateSnapshotScheduleInputRequestTypeDef = TypedDict(
    "_RequiredUpdateSnapshotScheduleInputRequestTypeDef",
    {
        "VolumeARN": str,
        "StartAt": int,
        "RecurrenceInHours": int,
    },
)
_OptionalUpdateSnapshotScheduleInputRequestTypeDef = TypedDict(
    "_OptionalUpdateSnapshotScheduleInputRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class UpdateSnapshotScheduleInputRequestTypeDef(
    _RequiredUpdateSnapshotScheduleInputRequestTypeDef,
    _OptionalUpdateSnapshotScheduleInputRequestTypeDef,
):
    pass

ActivateGatewayOutputTypeDef = TypedDict(
    "ActivateGatewayOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddCacheOutputTypeDef = TypedDict(
    "AddCacheOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsToResourceOutputTypeDef = TypedDict(
    "AddTagsToResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddUploadBufferOutputTypeDef = TypedDict(
    "AddUploadBufferOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddWorkingStorageOutputTypeDef = TypedDict(
    "AddWorkingStorageOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssignTapePoolOutputTypeDef = TypedDict(
    "AssignTapePoolOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateFileSystemOutputTypeDef = TypedDict(
    "AssociateFileSystemOutputTypeDef",
    {
        "FileSystemAssociationARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AttachVolumeOutputTypeDef = TypedDict(
    "AttachVolumeOutputTypeDef",
    {
        "VolumeARN": str,
        "TargetARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelArchivalOutputTypeDef = TypedDict(
    "CancelArchivalOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelRetrievalOutputTypeDef = TypedDict(
    "CancelRetrievalOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCachediSCSIVolumeOutputTypeDef = TypedDict(
    "CreateCachediSCSIVolumeOutputTypeDef",
    {
        "VolumeARN": str,
        "TargetARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNFSFileShareOutputTypeDef = TypedDict(
    "CreateNFSFileShareOutputTypeDef",
    {
        "FileShareARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSMBFileShareOutputTypeDef = TypedDict(
    "CreateSMBFileShareOutputTypeDef",
    {
        "FileShareARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotFromVolumeRecoveryPointOutputTypeDef = TypedDict(
    "CreateSnapshotFromVolumeRecoveryPointOutputTypeDef",
    {
        "SnapshotId": str,
        "VolumeARN": str,
        "VolumeRecoveryPointTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotOutputTypeDef = TypedDict(
    "CreateSnapshotOutputTypeDef",
    {
        "VolumeARN": str,
        "SnapshotId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStorediSCSIVolumeOutputTypeDef = TypedDict(
    "CreateStorediSCSIVolumeOutputTypeDef",
    {
        "VolumeARN": str,
        "VolumeSizeInBytes": int,
        "TargetARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTapePoolOutputTypeDef = TypedDict(
    "CreateTapePoolOutputTypeDef",
    {
        "PoolARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTapeWithBarcodeOutputTypeDef = TypedDict(
    "CreateTapeWithBarcodeOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTapesOutputTypeDef = TypedDict(
    "CreateTapesOutputTypeDef",
    {
        "TapeARNs": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAutomaticTapeCreationPolicyOutputTypeDef = TypedDict(
    "DeleteAutomaticTapeCreationPolicyOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBandwidthRateLimitOutputTypeDef = TypedDict(
    "DeleteBandwidthRateLimitOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteChapCredentialsOutputTypeDef = TypedDict(
    "DeleteChapCredentialsOutputTypeDef",
    {
        "TargetARN": str,
        "InitiatorName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFileShareOutputTypeDef = TypedDict(
    "DeleteFileShareOutputTypeDef",
    {
        "FileShareARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGatewayOutputTypeDef = TypedDict(
    "DeleteGatewayOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSnapshotScheduleOutputTypeDef = TypedDict(
    "DeleteSnapshotScheduleOutputTypeDef",
    {
        "VolumeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTapeArchiveOutputTypeDef = TypedDict(
    "DeleteTapeArchiveOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTapeOutputTypeDef = TypedDict(
    "DeleteTapeOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTapePoolOutputTypeDef = TypedDict(
    "DeleteTapePoolOutputTypeDef",
    {
        "PoolARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVolumeOutputTypeDef = TypedDict(
    "DeleteVolumeOutputTypeDef",
    {
        "VolumeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAvailabilityMonitorTestOutputTypeDef = TypedDict(
    "DescribeAvailabilityMonitorTestOutputTypeDef",
    {
        "GatewayARN": str,
        "Status": AvailabilityMonitorTestStatusType,
        "StartTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBandwidthRateLimitOutputTypeDef = TypedDict(
    "DescribeBandwidthRateLimitOutputTypeDef",
    {
        "GatewayARN": str,
        "AverageUploadRateLimitInBitsPerSec": int,
        "AverageDownloadRateLimitInBitsPerSec": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCacheOutputTypeDef = TypedDict(
    "DescribeCacheOutputTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": List[str],
        "CacheAllocatedInBytes": int,
        "CacheUsedPercentage": float,
        "CacheDirtyPercentage": float,
        "CacheHitPercentage": float,
        "CacheMissPercentage": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMaintenanceStartTimeOutputTypeDef = TypedDict(
    "DescribeMaintenanceStartTimeOutputTypeDef",
    {
        "GatewayARN": str,
        "HourOfDay": int,
        "MinuteOfHour": int,
        "DayOfWeek": int,
        "DayOfMonth": int,
        "Timezone": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSnapshotScheduleOutputTypeDef = TypedDict(
    "DescribeSnapshotScheduleOutputTypeDef",
    {
        "VolumeARN": str,
        "StartAt": int,
        "RecurrenceInHours": int,
        "Description": str,
        "Timezone": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUploadBufferOutputTypeDef = TypedDict(
    "DescribeUploadBufferOutputTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": List[str],
        "UploadBufferUsedInBytes": int,
        "UploadBufferAllocatedInBytes": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkingStorageOutputTypeDef = TypedDict(
    "DescribeWorkingStorageOutputTypeDef",
    {
        "GatewayARN": str,
        "DiskIds": List[str],
        "WorkingStorageUsedInBytes": int,
        "WorkingStorageAllocatedInBytes": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetachVolumeOutputTypeDef = TypedDict(
    "DetachVolumeOutputTypeDef",
    {
        "VolumeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableGatewayOutputTypeDef = TypedDict(
    "DisableGatewayOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateFileSystemOutputTypeDef = TypedDict(
    "DisassociateFileSystemOutputTypeDef",
    {
        "FileSystemAssociationARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JoinDomainOutputTypeDef = TypedDict(
    "JoinDomainOutputTypeDef",
    {
        "GatewayARN": str,
        "ActiveDirectoryStatus": ActiveDirectoryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "Marker": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVolumeInitiatorsOutputTypeDef = TypedDict(
    "ListVolumeInitiatorsOutputTypeDef",
    {
        "Initiators": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NotifyWhenUploadedOutputTypeDef = TypedDict(
    "NotifyWhenUploadedOutputTypeDef",
    {
        "FileShareARN": str,
        "NotificationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RefreshCacheOutputTypeDef = TypedDict(
    "RefreshCacheOutputTypeDef",
    {
        "FileShareARN": str,
        "NotificationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveTagsFromResourceOutputTypeDef = TypedDict(
    "RemoveTagsFromResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResetCacheOutputTypeDef = TypedDict(
    "ResetCacheOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RetrieveTapeArchiveOutputTypeDef = TypedDict(
    "RetrieveTapeArchiveOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RetrieveTapeRecoveryPointOutputTypeDef = TypedDict(
    "RetrieveTapeRecoveryPointOutputTypeDef",
    {
        "TapeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetLocalConsolePasswordOutputTypeDef = TypedDict(
    "SetLocalConsolePasswordOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetSMBGuestPasswordOutputTypeDef = TypedDict(
    "SetSMBGuestPasswordOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ShutdownGatewayOutputTypeDef = TypedDict(
    "ShutdownGatewayOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAvailabilityMonitorTestOutputTypeDef = TypedDict(
    "StartAvailabilityMonitorTestOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGatewayOutputTypeDef = TypedDict(
    "StartGatewayOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAutomaticTapeCreationPolicyOutputTypeDef = TypedDict(
    "UpdateAutomaticTapeCreationPolicyOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBandwidthRateLimitOutputTypeDef = TypedDict(
    "UpdateBandwidthRateLimitOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBandwidthRateLimitScheduleOutputTypeDef = TypedDict(
    "UpdateBandwidthRateLimitScheduleOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateChapCredentialsOutputTypeDef = TypedDict(
    "UpdateChapCredentialsOutputTypeDef",
    {
        "TargetARN": str,
        "InitiatorName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFileSystemAssociationOutputTypeDef = TypedDict(
    "UpdateFileSystemAssociationOutputTypeDef",
    {
        "FileSystemAssociationARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewayInformationOutputTypeDef = TypedDict(
    "UpdateGatewayInformationOutputTypeDef",
    {
        "GatewayARN": str,
        "GatewayName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewaySoftwareNowOutputTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMaintenanceStartTimeOutputTypeDef = TypedDict(
    "UpdateMaintenanceStartTimeOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNFSFileShareOutputTypeDef = TypedDict(
    "UpdateNFSFileShareOutputTypeDef",
    {
        "FileShareARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSMBFileShareOutputTypeDef = TypedDict(
    "UpdateSMBFileShareOutputTypeDef",
    {
        "FileShareARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSMBFileShareVisibilityOutputTypeDef = TypedDict(
    "UpdateSMBFileShareVisibilityOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSMBLocalGroupsOutputTypeDef = TypedDict(
    "UpdateSMBLocalGroupsOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSMBSecurityStrategyOutputTypeDef = TypedDict(
    "UpdateSMBSecurityStrategyOutputTypeDef",
    {
        "GatewayARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSnapshotScheduleOutputTypeDef = TypedDict(
    "UpdateSnapshotScheduleOutputTypeDef",
    {
        "VolumeARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVTLDeviceTypeOutputTypeDef = TypedDict(
    "UpdateVTLDeviceTypeOutputTypeDef",
    {
        "VTLDeviceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateSMBFileShareInputRequestTypeDef = TypedDict(
    "_RequiredCreateSMBFileShareInputRequestTypeDef",
    {
        "ClientToken": str,
        "GatewayARN": str,
        "Role": str,
        "LocationARN": str,
    },
)
_OptionalCreateSMBFileShareInputRequestTypeDef = TypedDict(
    "_OptionalCreateSMBFileShareInputRequestTypeDef",
    {
        "KMSEncrypted": bool,
        "KMSKey": str,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "SMBACLEnabled": bool,
        "AccessBasedEnumeration": bool,
        "AdminUserList": Sequence[str],
        "ValidUserList": Sequence[str],
        "InvalidUserList": Sequence[str],
        "AuditDestinationARN": str,
        "Authentication": str,
        "CaseSensitivity": CaseSensitivityType,
        "Tags": Sequence[TagTypeDef],
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "VPCEndpointDNSName": str,
        "BucketRegion": str,
        "OplocksEnabled": bool,
    },
    total=False,
)

class CreateSMBFileShareInputRequestTypeDef(
    _RequiredCreateSMBFileShareInputRequestTypeDef, _OptionalCreateSMBFileShareInputRequestTypeDef
):
    pass

SMBFileShareInfoTypeDef = TypedDict(
    "SMBFileShareInfoTypeDef",
    {
        "FileShareARN": str,
        "FileShareId": str,
        "FileShareStatus": str,
        "GatewayARN": str,
        "KMSEncrypted": bool,
        "KMSKey": str,
        "Path": str,
        "Role": str,
        "LocationARN": str,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "SMBACLEnabled": bool,
        "AccessBasedEnumeration": bool,
        "AdminUserList": List[str],
        "ValidUserList": List[str],
        "InvalidUserList": List[str],
        "AuditDestinationARN": str,
        "Authentication": str,
        "CaseSensitivity": CaseSensitivityType,
        "Tags": List[TagTypeDef],
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "VPCEndpointDNSName": str,
        "BucketRegion": str,
        "OplocksEnabled": bool,
    },
    total=False,
)

_RequiredUpdateFileSystemAssociationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateFileSystemAssociationInputRequestTypeDef",
    {
        "FileSystemAssociationARN": str,
    },
)
_OptionalUpdateFileSystemAssociationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateFileSystemAssociationInputRequestTypeDef",
    {
        "UserName": str,
        "Password": str,
        "AuditDestinationARN": str,
        "CacheAttributes": CacheAttributesTypeDef,
    },
    total=False,
)

class UpdateFileSystemAssociationInputRequestTypeDef(
    _RequiredUpdateFileSystemAssociationInputRequestTypeDef,
    _OptionalUpdateFileSystemAssociationInputRequestTypeDef,
):
    pass

_RequiredUpdateSMBFileShareInputRequestTypeDef = TypedDict(
    "_RequiredUpdateSMBFileShareInputRequestTypeDef",
    {
        "FileShareARN": str,
    },
)
_OptionalUpdateSMBFileShareInputRequestTypeDef = TypedDict(
    "_OptionalUpdateSMBFileShareInputRequestTypeDef",
    {
        "KMSEncrypted": bool,
        "KMSKey": str,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "SMBACLEnabled": bool,
        "AccessBasedEnumeration": bool,
        "AdminUserList": Sequence[str],
        "ValidUserList": Sequence[str],
        "InvalidUserList": Sequence[str],
        "AuditDestinationARN": str,
        "CaseSensitivity": CaseSensitivityType,
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "OplocksEnabled": bool,
    },
    total=False,
)

class UpdateSMBFileShareInputRequestTypeDef(
    _RequiredUpdateSMBFileShareInputRequestTypeDef, _OptionalUpdateSMBFileShareInputRequestTypeDef
):
    pass

_RequiredAssociateFileSystemInputRequestTypeDef = TypedDict(
    "_RequiredAssociateFileSystemInputRequestTypeDef",
    {
        "UserName": str,
        "Password": str,
        "ClientToken": str,
        "GatewayARN": str,
        "LocationARN": str,
    },
)
_OptionalAssociateFileSystemInputRequestTypeDef = TypedDict(
    "_OptionalAssociateFileSystemInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "AuditDestinationARN": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "EndpointNetworkConfiguration": EndpointNetworkConfigurationTypeDef,
    },
    total=False,
)

class AssociateFileSystemInputRequestTypeDef(
    _RequiredAssociateFileSystemInputRequestTypeDef, _OptionalAssociateFileSystemInputRequestTypeDef
):
    pass

AutomaticTapeCreationPolicyInfoTypeDef = TypedDict(
    "AutomaticTapeCreationPolicyInfoTypeDef",
    {
        "AutomaticTapeCreationRules": List[AutomaticTapeCreationRuleTypeDef],
        "GatewayARN": str,
    },
    total=False,
)

UpdateAutomaticTapeCreationPolicyInputRequestTypeDef = TypedDict(
    "UpdateAutomaticTapeCreationPolicyInputRequestTypeDef",
    {
        "AutomaticTapeCreationRules": Sequence[AutomaticTapeCreationRuleTypeDef],
        "GatewayARN": str,
    },
)

DescribeBandwidthRateLimitScheduleOutputTypeDef = TypedDict(
    "DescribeBandwidthRateLimitScheduleOutputTypeDef",
    {
        "GatewayARN": str,
        "BandwidthRateLimitIntervals": List[BandwidthRateLimitIntervalTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBandwidthRateLimitScheduleInputRequestTypeDef = TypedDict(
    "UpdateBandwidthRateLimitScheduleInputRequestTypeDef",
    {
        "GatewayARN": str,
        "BandwidthRateLimitIntervals": Sequence[BandwidthRateLimitIntervalTypeDef],
    },
)

CachediSCSIVolumeTypeDef = TypedDict(
    "CachediSCSIVolumeTypeDef",
    {
        "VolumeARN": str,
        "VolumeId": str,
        "VolumeType": str,
        "VolumeStatus": str,
        "VolumeAttachmentStatus": str,
        "VolumeSizeInBytes": int,
        "VolumeProgress": float,
        "SourceSnapshotId": str,
        "VolumeiSCSIAttributes": VolumeiSCSIAttributesTypeDef,
        "CreatedDate": datetime,
        "VolumeUsedInBytes": int,
        "KMSKey": str,
        "TargetName": str,
    },
    total=False,
)

StorediSCSIVolumeTypeDef = TypedDict(
    "StorediSCSIVolumeTypeDef",
    {
        "VolumeARN": str,
        "VolumeId": str,
        "VolumeType": str,
        "VolumeStatus": str,
        "VolumeAttachmentStatus": str,
        "VolumeSizeInBytes": int,
        "VolumeProgress": float,
        "VolumeDiskId": str,
        "SourceSnapshotId": str,
        "PreservedExistingData": bool,
        "VolumeiSCSIAttributes": VolumeiSCSIAttributesTypeDef,
        "CreatedDate": datetime,
        "VolumeUsedInBytes": int,
        "KMSKey": str,
        "TargetName": str,
    },
    total=False,
)

DescribeChapCredentialsOutputTypeDef = TypedDict(
    "DescribeChapCredentialsOutputTypeDef",
    {
        "ChapCredentials": List[ChapInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateNFSFileShareInputRequestTypeDef = TypedDict(
    "_RequiredCreateNFSFileShareInputRequestTypeDef",
    {
        "ClientToken": str,
        "GatewayARN": str,
        "Role": str,
        "LocationARN": str,
    },
)
_OptionalCreateNFSFileShareInputRequestTypeDef = TypedDict(
    "_OptionalCreateNFSFileShareInputRequestTypeDef",
    {
        "NFSFileShareDefaults": NFSFileShareDefaultsTypeDef,
        "KMSEncrypted": bool,
        "KMSKey": str,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ClientList": Sequence[str],
        "Squash": str,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "Tags": Sequence[TagTypeDef],
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "VPCEndpointDNSName": str,
        "BucketRegion": str,
        "AuditDestinationARN": str,
    },
    total=False,
)

class CreateNFSFileShareInputRequestTypeDef(
    _RequiredCreateNFSFileShareInputRequestTypeDef, _OptionalCreateNFSFileShareInputRequestTypeDef
):
    pass

NFSFileShareInfoTypeDef = TypedDict(
    "NFSFileShareInfoTypeDef",
    {
        "NFSFileShareDefaults": NFSFileShareDefaultsTypeDef,
        "FileShareARN": str,
        "FileShareId": str,
        "FileShareStatus": str,
        "GatewayARN": str,
        "KMSEncrypted": bool,
        "KMSKey": str,
        "Path": str,
        "Role": str,
        "LocationARN": str,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ClientList": List[str],
        "Squash": str,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "Tags": List[TagTypeDef],
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "VPCEndpointDNSName": str,
        "BucketRegion": str,
        "AuditDestinationARN": str,
    },
    total=False,
)

_RequiredUpdateNFSFileShareInputRequestTypeDef = TypedDict(
    "_RequiredUpdateNFSFileShareInputRequestTypeDef",
    {
        "FileShareARN": str,
    },
)
_OptionalUpdateNFSFileShareInputRequestTypeDef = TypedDict(
    "_OptionalUpdateNFSFileShareInputRequestTypeDef",
    {
        "KMSEncrypted": bool,
        "KMSKey": str,
        "NFSFileShareDefaults": NFSFileShareDefaultsTypeDef,
        "DefaultStorageClass": str,
        "ObjectACL": ObjectACLType,
        "ClientList": Sequence[str],
        "Squash": str,
        "ReadOnly": bool,
        "GuessMIMETypeEnabled": bool,
        "RequesterPays": bool,
        "FileShareName": str,
        "CacheAttributes": CacheAttributesTypeDef,
        "NotificationPolicy": str,
        "AuditDestinationARN": str,
    },
    total=False,
)

class UpdateNFSFileShareInputRequestTypeDef(
    _RequiredUpdateNFSFileShareInputRequestTypeDef, _OptionalUpdateNFSFileShareInputRequestTypeDef
):
    pass

DescribeGatewayInformationOutputTypeDef = TypedDict(
    "DescribeGatewayInformationOutputTypeDef",
    {
        "GatewayARN": str,
        "GatewayId": str,
        "GatewayName": str,
        "GatewayTimezone": str,
        "GatewayState": str,
        "GatewayNetworkInterfaces": List[NetworkInterfaceTypeDef],
        "GatewayType": str,
        "NextUpdateAvailabilityDate": str,
        "LastSoftwareUpdate": str,
        "Ec2InstanceId": str,
        "Ec2InstanceRegion": str,
        "Tags": List[TagTypeDef],
        "VPCEndpoint": str,
        "CloudWatchLogGroupARN": str,
        "HostEnvironment": HostEnvironmentType,
        "EndpointType": str,
        "SoftwareUpdatesEndDate": str,
        "DeprecationDate": str,
        "GatewayCapacity": GatewayCapacityType,
        "SupportedGatewayCapacities": List[GatewayCapacityType],
        "HostEnvironmentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSMBSettingsOutputTypeDef = TypedDict(
    "DescribeSMBSettingsOutputTypeDef",
    {
        "GatewayARN": str,
        "DomainName": str,
        "ActiveDirectoryStatus": ActiveDirectoryStatusType,
        "SMBGuestPasswordSet": bool,
        "SMBSecurityStrategy": SMBSecurityStrategyType,
        "FileSharesVisible": bool,
        "SMBLocalGroups": SMBLocalGroupsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSMBLocalGroupsInputRequestTypeDef = TypedDict(
    "UpdateSMBLocalGroupsInputRequestTypeDef",
    {
        "GatewayARN": str,
        "SMBLocalGroups": SMBLocalGroupsTypeDef,
    },
)

DescribeTapeArchivesInputDescribeTapeArchivesPaginateTypeDef = TypedDict(
    "DescribeTapeArchivesInputDescribeTapeArchivesPaginateTypeDef",
    {
        "TapeARNs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef = TypedDict(
    "_RequiredDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef = TypedDict(
    "_OptionalDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef(
    _RequiredDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef,
    _OptionalDescribeTapeRecoveryPointsInputDescribeTapeRecoveryPointsPaginateTypeDef,
):
    pass

_RequiredDescribeTapesInputDescribeTapesPaginateTypeDef = TypedDict(
    "_RequiredDescribeTapesInputDescribeTapesPaginateTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeTapesInputDescribeTapesPaginateTypeDef = TypedDict(
    "_OptionalDescribeTapesInputDescribeTapesPaginateTypeDef",
    {
        "TapeARNs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeTapesInputDescribeTapesPaginateTypeDef(
    _RequiredDescribeTapesInputDescribeTapesPaginateTypeDef,
    _OptionalDescribeTapesInputDescribeTapesPaginateTypeDef,
):
    pass

_RequiredDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef = TypedDict(
    "_RequiredDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef",
    {
        "GatewayARN": str,
    },
)
_OptionalDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef = TypedDict(
    "_OptionalDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef",
    {
        "VTLDeviceARNs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef(
    _RequiredDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef,
    _OptionalDescribeVTLDevicesInputDescribeVTLDevicesPaginateTypeDef,
):
    pass

ListFileSharesInputListFileSharesPaginateTypeDef = TypedDict(
    "ListFileSharesInputListFileSharesPaginateTypeDef",
    {
        "GatewayARN": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFileSystemAssociationsInputListFileSystemAssociationsPaginateTypeDef = TypedDict(
    "ListFileSystemAssociationsInputListFileSystemAssociationsPaginateTypeDef",
    {
        "GatewayARN": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListGatewaysInputListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "ResourceARN": str,
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

ListTapePoolsInputListTapePoolsPaginateTypeDef = TypedDict(
    "ListTapePoolsInputListTapePoolsPaginateTypeDef",
    {
        "PoolARNs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTapesInputListTapesPaginateTypeDef = TypedDict(
    "ListTapesInputListTapesPaginateTypeDef",
    {
        "TapeARNs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVolumesInputListVolumesPaginateTypeDef = TypedDict(
    "ListVolumesInputListVolumesPaginateTypeDef",
    {
        "GatewayARN": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeTapeArchivesOutputTypeDef = TypedDict(
    "DescribeTapeArchivesOutputTypeDef",
    {
        "TapeArchives": List[TapeArchiveTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTapeRecoveryPointsOutputTypeDef = TypedDict(
    "DescribeTapeRecoveryPointsOutputTypeDef",
    {
        "GatewayARN": str,
        "TapeRecoveryPointInfos": List[TapeRecoveryPointInfoTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTapesOutputTypeDef = TypedDict(
    "DescribeTapesOutputTypeDef",
    {
        "Tapes": List[TapeTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VTLDeviceTypeDef = TypedDict(
    "VTLDeviceTypeDef",
    {
        "VTLDeviceARN": str,
        "VTLDeviceType": str,
        "VTLDeviceVendor": str,
        "VTLDeviceProductIdentifier": str,
        "DeviceiSCSIAttributes": DeviceiSCSIAttributesTypeDef,
    },
    total=False,
)

ListLocalDisksOutputTypeDef = TypedDict(
    "ListLocalDisksOutputTypeDef",
    {
        "GatewayARN": str,
        "Disks": List[DiskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFileSharesOutputTypeDef = TypedDict(
    "ListFileSharesOutputTypeDef",
    {
        "Marker": str,
        "NextMarker": str,
        "FileShareInfoList": List[FileShareInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FileSystemAssociationInfoTypeDef = TypedDict(
    "FileSystemAssociationInfoTypeDef",
    {
        "FileSystemAssociationARN": str,
        "LocationARN": str,
        "FileSystemAssociationStatus": str,
        "AuditDestinationARN": str,
        "GatewayARN": str,
        "Tags": List[TagTypeDef],
        "CacheAttributes": CacheAttributesTypeDef,
        "EndpointNetworkConfiguration": EndpointNetworkConfigurationTypeDef,
        "FileSystemAssociationStatusDetails": List[FileSystemAssociationStatusDetailTypeDef],
    },
    total=False,
)

ListFileSystemAssociationsOutputTypeDef = TypedDict(
    "ListFileSystemAssociationsOutputTypeDef",
    {
        "Marker": str,
        "NextMarker": str,
        "FileSystemAssociationSummaryList": List[FileSystemAssociationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysOutputTypeDef = TypedDict(
    "ListGatewaysOutputTypeDef",
    {
        "Gateways": List[GatewayInfoTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTapePoolsOutputTypeDef = TypedDict(
    "ListTapePoolsOutputTypeDef",
    {
        "PoolInfos": List[PoolInfoTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTapesOutputTypeDef = TypedDict(
    "ListTapesOutputTypeDef",
    {
        "TapeInfos": List[TapeInfoTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVolumeRecoveryPointsOutputTypeDef = TypedDict(
    "ListVolumeRecoveryPointsOutputTypeDef",
    {
        "GatewayARN": str,
        "VolumeRecoveryPointInfos": List[VolumeRecoveryPointInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVolumesOutputTypeDef = TypedDict(
    "ListVolumesOutputTypeDef",
    {
        "GatewayARN": str,
        "Marker": str,
        "VolumeInfos": List[VolumeInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSMBFileSharesOutputTypeDef = TypedDict(
    "DescribeSMBFileSharesOutputTypeDef",
    {
        "SMBFileShareInfoList": List[SMBFileShareInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAutomaticTapeCreationPoliciesOutputTypeDef = TypedDict(
    "ListAutomaticTapeCreationPoliciesOutputTypeDef",
    {
        "AutomaticTapeCreationPolicyInfos": List[AutomaticTapeCreationPolicyInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCachediSCSIVolumesOutputTypeDef = TypedDict(
    "DescribeCachediSCSIVolumesOutputTypeDef",
    {
        "CachediSCSIVolumes": List[CachediSCSIVolumeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStorediSCSIVolumesOutputTypeDef = TypedDict(
    "DescribeStorediSCSIVolumesOutputTypeDef",
    {
        "StorediSCSIVolumes": List[StorediSCSIVolumeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeNFSFileSharesOutputTypeDef = TypedDict(
    "DescribeNFSFileSharesOutputTypeDef",
    {
        "NFSFileShareInfoList": List[NFSFileShareInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVTLDevicesOutputTypeDef = TypedDict(
    "DescribeVTLDevicesOutputTypeDef",
    {
        "GatewayARN": str,
        "VTLDevices": List[VTLDeviceTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFileSystemAssociationsOutputTypeDef = TypedDict(
    "DescribeFileSystemAssociationsOutputTypeDef",
    {
        "FileSystemAssociationInfoList": List[FileSystemAssociationInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
