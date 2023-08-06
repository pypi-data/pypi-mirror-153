"""
Type annotations for storagegateway service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_storagegateway.client import StorageGatewayClient
    from mypy_boto3_storagegateway.paginator import (
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

    session = Session()
    client: StorageGatewayClient = session.client("storagegateway")

    describe_tape_archives_paginator: DescribeTapeArchivesPaginator = client.get_paginator("describe_tape_archives")
    describe_tape_recovery_points_paginator: DescribeTapeRecoveryPointsPaginator = client.get_paginator("describe_tape_recovery_points")
    describe_tapes_paginator: DescribeTapesPaginator = client.get_paginator("describe_tapes")
    describe_vtl_devices_paginator: DescribeVTLDevicesPaginator = client.get_paginator("describe_vtl_devices")
    list_file_shares_paginator: ListFileSharesPaginator = client.get_paginator("list_file_shares")
    list_file_system_associations_paginator: ListFileSystemAssociationsPaginator = client.get_paginator("list_file_system_associations")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_tape_pools_paginator: ListTapePoolsPaginator = client.get_paginator("list_tape_pools")
    list_tapes_paginator: ListTapesPaginator = client.get_paginator("list_tapes")
    list_volumes_paginator: ListVolumesPaginator = client.get_paginator("list_volumes")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeTapeArchivesOutputTypeDef,
    DescribeTapeRecoveryPointsOutputTypeDef,
    DescribeTapesOutputTypeDef,
    DescribeVTLDevicesOutputTypeDef,
    ListFileSharesOutputTypeDef,
    ListFileSystemAssociationsOutputTypeDef,
    ListGatewaysOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTapePoolsOutputTypeDef,
    ListTapesOutputTypeDef,
    ListVolumesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeTapeArchivesPaginator",
    "DescribeTapeRecoveryPointsPaginator",
    "DescribeTapesPaginator",
    "DescribeVTLDevicesPaginator",
    "ListFileSharesPaginator",
    "ListFileSystemAssociationsPaginator",
    "ListGatewaysPaginator",
    "ListTagsForResourcePaginator",
    "ListTapePoolsPaginator",
    "ListTapesPaginator",
    "ListVolumesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeTapeArchivesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetapearchivespaginator)
    """

    def paginate(
        self, *, TapeARNs: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTapeArchivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetapearchivespaginator)
        """


class DescribeTapeRecoveryPointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetaperecoverypointspaginator)
    """

    def paginate(
        self, *, GatewayARN: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTapeRecoveryPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetaperecoverypointspaginator)
        """


class DescribeTapesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetapespaginator)
    """

    def paginate(
        self,
        *,
        GatewayARN: str,
        TapeARNs: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describetapespaginator)
        """


class DescribeVTLDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describevtldevicespaginator)
    """

    def paginate(
        self,
        *,
        GatewayARN: str,
        VTLDeviceARNs: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeVTLDevicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#describevtldevicespaginator)
        """


class ListFileSharesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listfilesharespaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFileSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listfilesharespaginator)
        """


class ListFileSystemAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listfilesystemassociationspaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFileSystemAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listfilesystemassociationspaginator)
        """


class ListGatewaysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listgatewayspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listgatewayspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceARN: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtagsforresourcepaginator)
        """


class ListTapePoolsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtapepoolspaginator)
    """

    def paginate(
        self, *, PoolARNs: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTapePoolsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtapepoolspaginator)
        """


class ListTapesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtapespaginator)
    """

    def paginate(
        self, *, TapeARNs: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listtapespaginator)
        """


class ListVolumesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listvolumespaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListVolumesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_storagegateway/paginators/#listvolumespaginator)
        """
