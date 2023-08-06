"""
Type annotations for directconnect service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_directconnect.client import DirectConnectClient
    from mypy_boto3_directconnect.paginator import (
        DescribeDirectConnectGatewayAssociationsPaginator,
        DescribeDirectConnectGatewayAttachmentsPaginator,
        DescribeDirectConnectGatewaysPaginator,
    )

    session = Session()
    client: DirectConnectClient = session.client("directconnect")

    describe_direct_connect_gateway_associations_paginator: DescribeDirectConnectGatewayAssociationsPaginator = client.get_paginator("describe_direct_connect_gateway_associations")
    describe_direct_connect_gateway_attachments_paginator: DescribeDirectConnectGatewayAttachmentsPaginator = client.get_paginator("describe_direct_connect_gateway_attachments")
    describe_direct_connect_gateways_paginator: DescribeDirectConnectGatewaysPaginator = client.get_paginator("describe_direct_connect_gateways")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeDirectConnectGatewayAssociationsResultTypeDef,
    DescribeDirectConnectGatewayAttachmentsResultTypeDef,
    DescribeDirectConnectGatewaysResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeDirectConnectGatewayAssociationsPaginator",
    "DescribeDirectConnectGatewayAttachmentsPaginator",
    "DescribeDirectConnectGatewaysPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectConnectGatewayAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
    """

    def paginate(
        self,
        *,
        associationId: str = ...,
        associatedGatewayId: str = ...,
        directConnectGatewayId: str = ...,
        virtualGatewayId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDirectConnectGatewayAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
        """


class DescribeDirectConnectGatewayAttachmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
    """

    def paginate(
        self,
        *,
        directConnectGatewayId: str = ...,
        virtualInterfaceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDirectConnectGatewayAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
        """


class DescribeDirectConnectGatewaysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGateways)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayspaginator)
    """

    def paginate(
        self, *, directConnectGatewayId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDirectConnectGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Paginator.DescribeDirectConnectGateways.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayspaginator)
        """
