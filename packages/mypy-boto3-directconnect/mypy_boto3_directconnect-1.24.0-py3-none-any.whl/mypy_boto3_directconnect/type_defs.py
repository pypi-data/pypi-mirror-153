"""
Type annotations for directconnect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/type_defs/)

Usage::

    ```python
    from mypy_boto3_directconnect.type_defs import RouteFilterPrefixTypeDef

    data: RouteFilterPrefixTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AddressFamilyType,
    BGPPeerStateType,
    BGPStatusType,
    ConnectionStateType,
    DirectConnectGatewayAssociationProposalStateType,
    DirectConnectGatewayAssociationStateType,
    DirectConnectGatewayAttachmentStateType,
    DirectConnectGatewayAttachmentTypeType,
    DirectConnectGatewayStateType,
    GatewayTypeType,
    HasLogicalRedundancyType,
    InterconnectStateType,
    LagStateType,
    NniPartnerTypeType,
    VirtualInterfaceStateType,
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
    "RouteFilterPrefixTypeDef",
    "ResponseMetadataTypeDef",
    "AllocateConnectionOnInterconnectRequestRequestTypeDef",
    "TagTypeDef",
    "AssociateConnectionWithLagRequestRequestTypeDef",
    "AssociateHostedConnectionRequestRequestTypeDef",
    "AssociateMacSecKeyRequestRequestTypeDef",
    "MacSecKeyTypeDef",
    "AssociateVirtualInterfaceRequestRequestTypeDef",
    "AssociatedGatewayTypeDef",
    "BGPPeerTypeDef",
    "ConfirmConnectionRequestRequestTypeDef",
    "ConfirmCustomerAgreementRequestRequestTypeDef",
    "ConfirmPrivateVirtualInterfaceRequestRequestTypeDef",
    "ConfirmPublicVirtualInterfaceRequestRequestTypeDef",
    "ConfirmTransitVirtualInterfaceRequestRequestTypeDef",
    "NewBGPPeerTypeDef",
    "CreateDirectConnectGatewayRequestRequestTypeDef",
    "DirectConnectGatewayTypeDef",
    "CustomerAgreementTypeDef",
    "DeleteBGPPeerRequestRequestTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    "DeleteDirectConnectGatewayAssociationRequestRequestTypeDef",
    "DeleteDirectConnectGatewayRequestRequestTypeDef",
    "DeleteInterconnectRequestRequestTypeDef",
    "DeleteLagRequestRequestTypeDef",
    "DeleteVirtualInterfaceRequestRequestTypeDef",
    "DescribeConnectionLoaRequestRequestTypeDef",
    "LoaTypeDef",
    "DescribeConnectionsOnInterconnectRequestRequestTypeDef",
    "DescribeConnectionsRequestRequestTypeDef",
    "DescribeDirectConnectGatewayAssociationProposalsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDirectConnectGatewayAssociationsRequestRequestTypeDef",
    "DescribeDirectConnectGatewayAttachmentsRequestRequestTypeDef",
    "DirectConnectGatewayAttachmentTypeDef",
    "DescribeDirectConnectGatewaysRequestRequestTypeDef",
    "DescribeHostedConnectionsRequestRequestTypeDef",
    "DescribeInterconnectLoaRequestRequestTypeDef",
    "DescribeInterconnectsRequestRequestTypeDef",
    "DescribeLagsRequestRequestTypeDef",
    "DescribeLoaRequestRequestTypeDef",
    "DescribeRouterConfigurationRequestRequestTypeDef",
    "RouterTypeTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeVirtualInterfacesRequestRequestTypeDef",
    "DisassociateConnectionFromLagRequestRequestTypeDef",
    "DisassociateMacSecKeyRequestRequestTypeDef",
    "ListVirtualInterfaceTestHistoryRequestRequestTypeDef",
    "VirtualInterfaceTestHistoryTypeDef",
    "LocationTypeDef",
    "StartBgpFailoverTestRequestRequestTypeDef",
    "StopBgpFailoverTestRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConnectionRequestRequestTypeDef",
    "UpdateDirectConnectGatewayRequestRequestTypeDef",
    "UpdateLagRequestRequestTypeDef",
    "UpdateVirtualInterfaceAttributesRequestRequestTypeDef",
    "VirtualGatewayTypeDef",
    "AcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    "CreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    "CreateDirectConnectGatewayAssociationRequestRequestTypeDef",
    "UpdateDirectConnectGatewayAssociationRequestRequestTypeDef",
    "ConfirmConnectionResponseTypeDef",
    "ConfirmCustomerAgreementResponseTypeDef",
    "ConfirmPrivateVirtualInterfaceResponseTypeDef",
    "ConfirmPublicVirtualInterfaceResponseTypeDef",
    "ConfirmTransitVirtualInterfaceResponseTypeDef",
    "DeleteInterconnectResponseTypeDef",
    "DeleteVirtualInterfaceResponseTypeDef",
    "LoaResponseMetadataTypeDef",
    "AllocateHostedConnectionRequestRequestTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "CreateInterconnectRequestRequestTypeDef",
    "CreateLagRequestRequestTypeDef",
    "InterconnectResponseMetadataTypeDef",
    "InterconnectTypeDef",
    "NewPrivateVirtualInterfaceAllocationTypeDef",
    "NewPrivateVirtualInterfaceTypeDef",
    "NewPublicVirtualInterfaceAllocationTypeDef",
    "NewPublicVirtualInterfaceTypeDef",
    "NewTransitVirtualInterfaceAllocationTypeDef",
    "NewTransitVirtualInterfaceTypeDef",
    "ResourceTagTypeDef",
    "TagResourceRequestRequestTypeDef",
    "AssociateMacSecKeyResponseTypeDef",
    "ConnectionResponseMetadataTypeDef",
    "ConnectionTypeDef",
    "DisassociateMacSecKeyResponseTypeDef",
    "DirectConnectGatewayAssociationProposalTypeDef",
    "DirectConnectGatewayAssociationTypeDef",
    "VirtualInterfaceResponseMetadataTypeDef",
    "VirtualInterfaceTypeDef",
    "CreateBGPPeerRequestRequestTypeDef",
    "CreateDirectConnectGatewayResultTypeDef",
    "DeleteDirectConnectGatewayResultTypeDef",
    "DescribeDirectConnectGatewaysResultTypeDef",
    "UpdateDirectConnectGatewayResponseTypeDef",
    "DescribeCustomerMetadataResponseTypeDef",
    "DescribeConnectionLoaResponseTypeDef",
    "DescribeInterconnectLoaResponseTypeDef",
    "DescribeDirectConnectGatewayAssociationsRequestDescribeDirectConnectGatewayAssociationsPaginateTypeDef",
    "DescribeDirectConnectGatewayAttachmentsRequestDescribeDirectConnectGatewayAttachmentsPaginateTypeDef",
    "DescribeDirectConnectGatewaysRequestDescribeDirectConnectGatewaysPaginateTypeDef",
    "DescribeDirectConnectGatewayAttachmentsResultTypeDef",
    "DescribeRouterConfigurationResponseTypeDef",
    "ListVirtualInterfaceTestHistoryResponseTypeDef",
    "StartBgpFailoverTestResponseTypeDef",
    "StopBgpFailoverTestResponseTypeDef",
    "LocationsTypeDef",
    "VirtualGatewaysTypeDef",
    "InterconnectsTypeDef",
    "AllocatePrivateVirtualInterfaceRequestRequestTypeDef",
    "CreatePrivateVirtualInterfaceRequestRequestTypeDef",
    "AllocatePublicVirtualInterfaceRequestRequestTypeDef",
    "CreatePublicVirtualInterfaceRequestRequestTypeDef",
    "AllocateTransitVirtualInterfaceRequestRequestTypeDef",
    "CreateTransitVirtualInterfaceRequestRequestTypeDef",
    "DescribeTagsResponseTypeDef",
    "ConnectionsTypeDef",
    "LagResponseMetadataTypeDef",
    "LagTypeDef",
    "CreateDirectConnectGatewayAssociationProposalResultTypeDef",
    "DeleteDirectConnectGatewayAssociationProposalResultTypeDef",
    "DescribeDirectConnectGatewayAssociationProposalsResultTypeDef",
    "AcceptDirectConnectGatewayAssociationProposalResultTypeDef",
    "CreateDirectConnectGatewayAssociationResultTypeDef",
    "DeleteDirectConnectGatewayAssociationResultTypeDef",
    "DescribeDirectConnectGatewayAssociationsResultTypeDef",
    "UpdateDirectConnectGatewayAssociationResultTypeDef",
    "AllocateTransitVirtualInterfaceResultTypeDef",
    "CreateBGPPeerResponseTypeDef",
    "CreateTransitVirtualInterfaceResultTypeDef",
    "DeleteBGPPeerResponseTypeDef",
    "VirtualInterfacesTypeDef",
    "LagsTypeDef",
)

RouteFilterPrefixTypeDef = TypedDict(
    "RouteFilterPrefixTypeDef",
    {
        "cidr": str,
    },
    total=False,
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

AllocateConnectionOnInterconnectRequestRequestTypeDef = TypedDict(
    "AllocateConnectionOnInterconnectRequestRequestTypeDef",
    {
        "bandwidth": str,
        "connectionName": str,
        "ownerAccount": str,
        "interconnectId": str,
        "vlan": int,
    },
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


AssociateConnectionWithLagRequestRequestTypeDef = TypedDict(
    "AssociateConnectionWithLagRequestRequestTypeDef",
    {
        "connectionId": str,
        "lagId": str,
    },
)

AssociateHostedConnectionRequestRequestTypeDef = TypedDict(
    "AssociateHostedConnectionRequestRequestTypeDef",
    {
        "connectionId": str,
        "parentConnectionId": str,
    },
)

_RequiredAssociateMacSecKeyRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateMacSecKeyRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)
_OptionalAssociateMacSecKeyRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateMacSecKeyRequestRequestTypeDef",
    {
        "secretARN": str,
        "ckn": str,
        "cak": str,
    },
    total=False,
)


class AssociateMacSecKeyRequestRequestTypeDef(
    _RequiredAssociateMacSecKeyRequestRequestTypeDef,
    _OptionalAssociateMacSecKeyRequestRequestTypeDef,
):
    pass


MacSecKeyTypeDef = TypedDict(
    "MacSecKeyTypeDef",
    {
        "secretARN": str,
        "ckn": str,
        "state": str,
        "startOn": str,
    },
    total=False,
)

AssociateVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "AssociateVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
        "connectionId": str,
    },
)

AssociatedGatewayTypeDef = TypedDict(
    "AssociatedGatewayTypeDef",
    {
        "id": str,
        "type": GatewayTypeType,
        "ownerAccount": str,
        "region": str,
    },
    total=False,
)

BGPPeerTypeDef = TypedDict(
    "BGPPeerTypeDef",
    {
        "bgpPeerId": str,
        "asn": int,
        "authKey": str,
        "addressFamily": AddressFamilyType,
        "amazonAddress": str,
        "customerAddress": str,
        "bgpPeerState": BGPPeerStateType,
        "bgpStatus": BGPStatusType,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
    },
    total=False,
)

ConfirmConnectionRequestRequestTypeDef = TypedDict(
    "ConfirmConnectionRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)

ConfirmCustomerAgreementRequestRequestTypeDef = TypedDict(
    "ConfirmCustomerAgreementRequestRequestTypeDef",
    {
        "agreementName": str,
    },
    total=False,
)

_RequiredConfirmPrivateVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "_RequiredConfirmPrivateVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)
_OptionalConfirmPrivateVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "_OptionalConfirmPrivateVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualGatewayId": str,
        "directConnectGatewayId": str,
    },
    total=False,
)


class ConfirmPrivateVirtualInterfaceRequestRequestTypeDef(
    _RequiredConfirmPrivateVirtualInterfaceRequestRequestTypeDef,
    _OptionalConfirmPrivateVirtualInterfaceRequestRequestTypeDef,
):
    pass


ConfirmPublicVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "ConfirmPublicVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)

ConfirmTransitVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "ConfirmTransitVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
        "directConnectGatewayId": str,
    },
)

NewBGPPeerTypeDef = TypedDict(
    "NewBGPPeerTypeDef",
    {
        "asn": int,
        "authKey": str,
        "addressFamily": AddressFamilyType,
        "amazonAddress": str,
        "customerAddress": str,
    },
    total=False,
)

_RequiredCreateDirectConnectGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectConnectGatewayRequestRequestTypeDef",
    {
        "directConnectGatewayName": str,
    },
)
_OptionalCreateDirectConnectGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectConnectGatewayRequestRequestTypeDef",
    {
        "amazonSideAsn": int,
    },
    total=False,
)


class CreateDirectConnectGatewayRequestRequestTypeDef(
    _RequiredCreateDirectConnectGatewayRequestRequestTypeDef,
    _OptionalCreateDirectConnectGatewayRequestRequestTypeDef,
):
    pass


DirectConnectGatewayTypeDef = TypedDict(
    "DirectConnectGatewayTypeDef",
    {
        "directConnectGatewayId": str,
        "directConnectGatewayName": str,
        "amazonSideAsn": int,
        "ownerAccount": str,
        "directConnectGatewayState": DirectConnectGatewayStateType,
        "stateChangeError": str,
    },
    total=False,
)

CustomerAgreementTypeDef = TypedDict(
    "CustomerAgreementTypeDef",
    {
        "agreementName": str,
        "status": str,
    },
    total=False,
)

DeleteBGPPeerRequestRequestTypeDef = TypedDict(
    "DeleteBGPPeerRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
        "asn": int,
        "customerAddress": str,
        "bgpPeerId": str,
    },
    total=False,
)

DeleteConnectionRequestRequestTypeDef = TypedDict(
    "DeleteConnectionRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)

DeleteDirectConnectGatewayAssociationProposalRequestRequestTypeDef = TypedDict(
    "DeleteDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    {
        "proposalId": str,
    },
)

DeleteDirectConnectGatewayAssociationRequestRequestTypeDef = TypedDict(
    "DeleteDirectConnectGatewayAssociationRequestRequestTypeDef",
    {
        "associationId": str,
        "directConnectGatewayId": str,
        "virtualGatewayId": str,
    },
    total=False,
)

DeleteDirectConnectGatewayRequestRequestTypeDef = TypedDict(
    "DeleteDirectConnectGatewayRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
    },
)

DeleteInterconnectRequestRequestTypeDef = TypedDict(
    "DeleteInterconnectRequestRequestTypeDef",
    {
        "interconnectId": str,
    },
)

DeleteLagRequestRequestTypeDef = TypedDict(
    "DeleteLagRequestRequestTypeDef",
    {
        "lagId": str,
    },
)

DeleteVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "DeleteVirtualInterfaceRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)

_RequiredDescribeConnectionLoaRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeConnectionLoaRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)
_OptionalDescribeConnectionLoaRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeConnectionLoaRequestRequestTypeDef",
    {
        "providerName": str,
        "loaContentType": Literal["application/pdf"],
    },
    total=False,
)


class DescribeConnectionLoaRequestRequestTypeDef(
    _RequiredDescribeConnectionLoaRequestRequestTypeDef,
    _OptionalDescribeConnectionLoaRequestRequestTypeDef,
):
    pass


LoaTypeDef = TypedDict(
    "LoaTypeDef",
    {
        "loaContent": bytes,
        "loaContentType": Literal["application/pdf"],
    },
    total=False,
)

DescribeConnectionsOnInterconnectRequestRequestTypeDef = TypedDict(
    "DescribeConnectionsOnInterconnectRequestRequestTypeDef",
    {
        "interconnectId": str,
    },
)

DescribeConnectionsRequestRequestTypeDef = TypedDict(
    "DescribeConnectionsRequestRequestTypeDef",
    {
        "connectionId": str,
    },
    total=False,
)

DescribeDirectConnectGatewayAssociationProposalsRequestRequestTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAssociationProposalsRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "proposalId": str,
        "associatedGatewayId": str,
        "maxResults": int,
        "nextToken": str,
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

DescribeDirectConnectGatewayAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAssociationsRequestRequestTypeDef",
    {
        "associationId": str,
        "associatedGatewayId": str,
        "directConnectGatewayId": str,
        "maxResults": int,
        "nextToken": str,
        "virtualGatewayId": str,
    },
    total=False,
)

DescribeDirectConnectGatewayAttachmentsRequestRequestTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAttachmentsRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "virtualInterfaceId": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DirectConnectGatewayAttachmentTypeDef = TypedDict(
    "DirectConnectGatewayAttachmentTypeDef",
    {
        "directConnectGatewayId": str,
        "virtualInterfaceId": str,
        "virtualInterfaceRegion": str,
        "virtualInterfaceOwnerAccount": str,
        "attachmentState": DirectConnectGatewayAttachmentStateType,
        "attachmentType": DirectConnectGatewayAttachmentTypeType,
        "stateChangeError": str,
    },
    total=False,
)

DescribeDirectConnectGatewaysRequestRequestTypeDef = TypedDict(
    "DescribeDirectConnectGatewaysRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeHostedConnectionsRequestRequestTypeDef = TypedDict(
    "DescribeHostedConnectionsRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)

_RequiredDescribeInterconnectLoaRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInterconnectLoaRequestRequestTypeDef",
    {
        "interconnectId": str,
    },
)
_OptionalDescribeInterconnectLoaRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInterconnectLoaRequestRequestTypeDef",
    {
        "providerName": str,
        "loaContentType": Literal["application/pdf"],
    },
    total=False,
)


class DescribeInterconnectLoaRequestRequestTypeDef(
    _RequiredDescribeInterconnectLoaRequestRequestTypeDef,
    _OptionalDescribeInterconnectLoaRequestRequestTypeDef,
):
    pass


DescribeInterconnectsRequestRequestTypeDef = TypedDict(
    "DescribeInterconnectsRequestRequestTypeDef",
    {
        "interconnectId": str,
    },
    total=False,
)

DescribeLagsRequestRequestTypeDef = TypedDict(
    "DescribeLagsRequestRequestTypeDef",
    {
        "lagId": str,
    },
    total=False,
)

_RequiredDescribeLoaRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeLoaRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)
_OptionalDescribeLoaRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeLoaRequestRequestTypeDef",
    {
        "providerName": str,
        "loaContentType": Literal["application/pdf"],
    },
    total=False,
)


class DescribeLoaRequestRequestTypeDef(
    _RequiredDescribeLoaRequestRequestTypeDef, _OptionalDescribeLoaRequestRequestTypeDef
):
    pass


_RequiredDescribeRouterConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRouterConfigurationRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)
_OptionalDescribeRouterConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRouterConfigurationRequestRequestTypeDef",
    {
        "routerTypeIdentifier": str,
    },
    total=False,
)


class DescribeRouterConfigurationRequestRequestTypeDef(
    _RequiredDescribeRouterConfigurationRequestRequestTypeDef,
    _OptionalDescribeRouterConfigurationRequestRequestTypeDef,
):
    pass


RouterTypeTypeDef = TypedDict(
    "RouterTypeTypeDef",
    {
        "vendor": str,
        "platform": str,
        "software": str,
        "xsltTemplateName": str,
        "xsltTemplateNameForMacSec": str,
        "routerTypeIdentifier": str,
    },
    total=False,
)

DescribeTagsRequestRequestTypeDef = TypedDict(
    "DescribeTagsRequestRequestTypeDef",
    {
        "resourceArns": Sequence[str],
    },
)

DescribeVirtualInterfacesRequestRequestTypeDef = TypedDict(
    "DescribeVirtualInterfacesRequestRequestTypeDef",
    {
        "connectionId": str,
        "virtualInterfaceId": str,
    },
    total=False,
)

DisassociateConnectionFromLagRequestRequestTypeDef = TypedDict(
    "DisassociateConnectionFromLagRequestRequestTypeDef",
    {
        "connectionId": str,
        "lagId": str,
    },
)

DisassociateMacSecKeyRequestRequestTypeDef = TypedDict(
    "DisassociateMacSecKeyRequestRequestTypeDef",
    {
        "connectionId": str,
        "secretARN": str,
    },
)

ListVirtualInterfaceTestHistoryRequestRequestTypeDef = TypedDict(
    "ListVirtualInterfaceTestHistoryRequestRequestTypeDef",
    {
        "testId": str,
        "virtualInterfaceId": str,
        "bgpPeers": Sequence[str],
        "status": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

VirtualInterfaceTestHistoryTypeDef = TypedDict(
    "VirtualInterfaceTestHistoryTypeDef",
    {
        "testId": str,
        "virtualInterfaceId": str,
        "bgpPeers": List[str],
        "status": str,
        "ownerAccount": str,
        "testDurationInMinutes": int,
        "startTime": datetime,
        "endTime": datetime,
    },
    total=False,
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "locationCode": str,
        "locationName": str,
        "region": str,
        "availablePortSpeeds": List[str],
        "availableProviders": List[str],
        "availableMacSecPortSpeeds": List[str],
    },
    total=False,
)

_RequiredStartBgpFailoverTestRequestRequestTypeDef = TypedDict(
    "_RequiredStartBgpFailoverTestRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)
_OptionalStartBgpFailoverTestRequestRequestTypeDef = TypedDict(
    "_OptionalStartBgpFailoverTestRequestRequestTypeDef",
    {
        "bgpPeers": Sequence[str],
        "testDurationInMinutes": int,
    },
    total=False,
)


class StartBgpFailoverTestRequestRequestTypeDef(
    _RequiredStartBgpFailoverTestRequestRequestTypeDef,
    _OptionalStartBgpFailoverTestRequestRequestTypeDef,
):
    pass


StopBgpFailoverTestRequestRequestTypeDef = TypedDict(
    "StopBgpFailoverTestRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConnectionRequestRequestTypeDef",
    {
        "connectionId": str,
    },
)
_OptionalUpdateConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConnectionRequestRequestTypeDef",
    {
        "connectionName": str,
        "encryptionMode": str,
    },
    total=False,
)


class UpdateConnectionRequestRequestTypeDef(
    _RequiredUpdateConnectionRequestRequestTypeDef, _OptionalUpdateConnectionRequestRequestTypeDef
):
    pass


UpdateDirectConnectGatewayRequestRequestTypeDef = TypedDict(
    "UpdateDirectConnectGatewayRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "newDirectConnectGatewayName": str,
    },
)

_RequiredUpdateLagRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLagRequestRequestTypeDef",
    {
        "lagId": str,
    },
)
_OptionalUpdateLagRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLagRequestRequestTypeDef",
    {
        "lagName": str,
        "minimumLinks": int,
        "encryptionMode": str,
    },
    total=False,
)


class UpdateLagRequestRequestTypeDef(
    _RequiredUpdateLagRequestRequestTypeDef, _OptionalUpdateLagRequestRequestTypeDef
):
    pass


_RequiredUpdateVirtualInterfaceAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVirtualInterfaceAttributesRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
    },
)
_OptionalUpdateVirtualInterfaceAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVirtualInterfaceAttributesRequestRequestTypeDef",
    {
        "mtu": int,
        "enableSiteLink": bool,
        "virtualInterfaceName": str,
    },
    total=False,
)


class UpdateVirtualInterfaceAttributesRequestRequestTypeDef(
    _RequiredUpdateVirtualInterfaceAttributesRequestRequestTypeDef,
    _OptionalUpdateVirtualInterfaceAttributesRequestRequestTypeDef,
):
    pass


VirtualGatewayTypeDef = TypedDict(
    "VirtualGatewayTypeDef",
    {
        "virtualGatewayId": str,
        "virtualGatewayState": str,
    },
    total=False,
)

_RequiredAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef = TypedDict(
    "_RequiredAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "proposalId": str,
        "associatedGatewayOwnerAccount": str,
    },
)
_OptionalAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef = TypedDict(
    "_OptionalAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    {
        "overrideAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
    },
    total=False,
)


class AcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef(
    _RequiredAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
    _OptionalAcceptDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
):
    pass


_RequiredCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
        "directConnectGatewayOwnerAccount": str,
        "gatewayId": str,
    },
)
_OptionalCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef",
    {
        "addAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
        "removeAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
    },
    total=False,
)


class CreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef(
    _RequiredCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
    _OptionalCreateDirectConnectGatewayAssociationProposalRequestRequestTypeDef,
):
    pass


_RequiredCreateDirectConnectGatewayAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectConnectGatewayAssociationRequestRequestTypeDef",
    {
        "directConnectGatewayId": str,
    },
)
_OptionalCreateDirectConnectGatewayAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectConnectGatewayAssociationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "addAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
        "virtualGatewayId": str,
    },
    total=False,
)


class CreateDirectConnectGatewayAssociationRequestRequestTypeDef(
    _RequiredCreateDirectConnectGatewayAssociationRequestRequestTypeDef,
    _OptionalCreateDirectConnectGatewayAssociationRequestRequestTypeDef,
):
    pass


UpdateDirectConnectGatewayAssociationRequestRequestTypeDef = TypedDict(
    "UpdateDirectConnectGatewayAssociationRequestRequestTypeDef",
    {
        "associationId": str,
        "addAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
        "removeAllowedPrefixesToDirectConnectGateway": Sequence[RouteFilterPrefixTypeDef],
    },
    total=False,
)

ConfirmConnectionResponseTypeDef = TypedDict(
    "ConfirmConnectionResponseTypeDef",
    {
        "connectionState": ConnectionStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfirmCustomerAgreementResponseTypeDef = TypedDict(
    "ConfirmCustomerAgreementResponseTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfirmPrivateVirtualInterfaceResponseTypeDef = TypedDict(
    "ConfirmPrivateVirtualInterfaceResponseTypeDef",
    {
        "virtualInterfaceState": VirtualInterfaceStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfirmPublicVirtualInterfaceResponseTypeDef = TypedDict(
    "ConfirmPublicVirtualInterfaceResponseTypeDef",
    {
        "virtualInterfaceState": VirtualInterfaceStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfirmTransitVirtualInterfaceResponseTypeDef = TypedDict(
    "ConfirmTransitVirtualInterfaceResponseTypeDef",
    {
        "virtualInterfaceState": VirtualInterfaceStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInterconnectResponseTypeDef = TypedDict(
    "DeleteInterconnectResponseTypeDef",
    {
        "interconnectState": InterconnectStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualInterfaceResponseTypeDef = TypedDict(
    "DeleteVirtualInterfaceResponseTypeDef",
    {
        "virtualInterfaceState": VirtualInterfaceStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoaResponseMetadataTypeDef = TypedDict(
    "LoaResponseMetadataTypeDef",
    {
        "loaContent": bytes,
        "loaContentType": Literal["application/pdf"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAllocateHostedConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredAllocateHostedConnectionRequestRequestTypeDef",
    {
        "connectionId": str,
        "ownerAccount": str,
        "bandwidth": str,
        "connectionName": str,
        "vlan": int,
    },
)
_OptionalAllocateHostedConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalAllocateHostedConnectionRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class AllocateHostedConnectionRequestRequestTypeDef(
    _RequiredAllocateHostedConnectionRequestRequestTypeDef,
    _OptionalAllocateHostedConnectionRequestRequestTypeDef,
):
    pass


_RequiredCreateConnectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConnectionRequestRequestTypeDef",
    {
        "location": str,
        "bandwidth": str,
        "connectionName": str,
    },
)
_OptionalCreateConnectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConnectionRequestRequestTypeDef",
    {
        "lagId": str,
        "tags": Sequence[TagTypeDef],
        "providerName": str,
        "requestMACSec": bool,
    },
    total=False,
)


class CreateConnectionRequestRequestTypeDef(
    _RequiredCreateConnectionRequestRequestTypeDef, _OptionalCreateConnectionRequestRequestTypeDef
):
    pass


_RequiredCreateInterconnectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInterconnectRequestRequestTypeDef",
    {
        "interconnectName": str,
        "bandwidth": str,
        "location": str,
    },
)
_OptionalCreateInterconnectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInterconnectRequestRequestTypeDef",
    {
        "lagId": str,
        "tags": Sequence[TagTypeDef],
        "providerName": str,
    },
    total=False,
)


class CreateInterconnectRequestRequestTypeDef(
    _RequiredCreateInterconnectRequestRequestTypeDef,
    _OptionalCreateInterconnectRequestRequestTypeDef,
):
    pass


_RequiredCreateLagRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLagRequestRequestTypeDef",
    {
        "numberOfConnections": int,
        "location": str,
        "connectionsBandwidth": str,
        "lagName": str,
    },
)
_OptionalCreateLagRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLagRequestRequestTypeDef",
    {
        "connectionId": str,
        "tags": Sequence[TagTypeDef],
        "childConnectionTags": Sequence[TagTypeDef],
        "providerName": str,
        "requestMACSec": bool,
    },
    total=False,
)


class CreateLagRequestRequestTypeDef(
    _RequiredCreateLagRequestRequestTypeDef, _OptionalCreateLagRequestRequestTypeDef
):
    pass


InterconnectResponseMetadataTypeDef = TypedDict(
    "InterconnectResponseMetadataTypeDef",
    {
        "interconnectId": str,
        "interconnectName": str,
        "interconnectState": InterconnectStateType,
        "region": str,
        "location": str,
        "bandwidth": str,
        "loaIssueTime": datetime,
        "lagId": str,
        "awsDevice": str,
        "jumboFrameCapable": bool,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InterconnectTypeDef = TypedDict(
    "InterconnectTypeDef",
    {
        "interconnectId": str,
        "interconnectName": str,
        "interconnectState": InterconnectStateType,
        "region": str,
        "location": str,
        "bandwidth": str,
        "loaIssueTime": datetime,
        "lagId": str,
        "awsDevice": str,
        "jumboFrameCapable": bool,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
    },
    total=False,
)

_RequiredNewPrivateVirtualInterfaceAllocationTypeDef = TypedDict(
    "_RequiredNewPrivateVirtualInterfaceAllocationTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
    },
)
_OptionalNewPrivateVirtualInterfaceAllocationTypeDef = TypedDict(
    "_OptionalNewPrivateVirtualInterfaceAllocationTypeDef",
    {
        "mtu": int,
        "authKey": str,
        "amazonAddress": str,
        "addressFamily": AddressFamilyType,
        "customerAddress": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class NewPrivateVirtualInterfaceAllocationTypeDef(
    _RequiredNewPrivateVirtualInterfaceAllocationTypeDef,
    _OptionalNewPrivateVirtualInterfaceAllocationTypeDef,
):
    pass


_RequiredNewPrivateVirtualInterfaceTypeDef = TypedDict(
    "_RequiredNewPrivateVirtualInterfaceTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
    },
)
_OptionalNewPrivateVirtualInterfaceTypeDef = TypedDict(
    "_OptionalNewPrivateVirtualInterfaceTypeDef",
    {
        "mtu": int,
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "virtualGatewayId": str,
        "directConnectGatewayId": str,
        "tags": Sequence[TagTypeDef],
        "enableSiteLink": bool,
    },
    total=False,
)


class NewPrivateVirtualInterfaceTypeDef(
    _RequiredNewPrivateVirtualInterfaceTypeDef, _OptionalNewPrivateVirtualInterfaceTypeDef
):
    pass


_RequiredNewPublicVirtualInterfaceAllocationTypeDef = TypedDict(
    "_RequiredNewPublicVirtualInterfaceAllocationTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
    },
)
_OptionalNewPublicVirtualInterfaceAllocationTypeDef = TypedDict(
    "_OptionalNewPublicVirtualInterfaceAllocationTypeDef",
    {
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "routeFilterPrefixes": Sequence[RouteFilterPrefixTypeDef],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class NewPublicVirtualInterfaceAllocationTypeDef(
    _RequiredNewPublicVirtualInterfaceAllocationTypeDef,
    _OptionalNewPublicVirtualInterfaceAllocationTypeDef,
):
    pass


_RequiredNewPublicVirtualInterfaceTypeDef = TypedDict(
    "_RequiredNewPublicVirtualInterfaceTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
    },
)
_OptionalNewPublicVirtualInterfaceTypeDef = TypedDict(
    "_OptionalNewPublicVirtualInterfaceTypeDef",
    {
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "routeFilterPrefixes": Sequence[RouteFilterPrefixTypeDef],
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class NewPublicVirtualInterfaceTypeDef(
    _RequiredNewPublicVirtualInterfaceTypeDef, _OptionalNewPublicVirtualInterfaceTypeDef
):
    pass


NewTransitVirtualInterfaceAllocationTypeDef = TypedDict(
    "NewTransitVirtualInterfaceAllocationTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
        "mtu": int,
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

NewTransitVirtualInterfaceTypeDef = TypedDict(
    "NewTransitVirtualInterfaceTypeDef",
    {
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
        "mtu": int,
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "directConnectGatewayId": str,
        "tags": Sequence[TagTypeDef],
        "enableSiteLink": bool,
    },
    total=False,
)

ResourceTagTypeDef = TypedDict(
    "ResourceTagTypeDef",
    {
        "resourceArn": str,
        "tags": List[TagTypeDef],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

AssociateMacSecKeyResponseTypeDef = TypedDict(
    "AssociateMacSecKeyResponseTypeDef",
    {
        "connectionId": str,
        "macSecKeys": List[MacSecKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConnectionResponseMetadataTypeDef = TypedDict(
    "ConnectionResponseMetadataTypeDef",
    {
        "ownerAccount": str,
        "connectionId": str,
        "connectionName": str,
        "connectionState": ConnectionStateType,
        "region": str,
        "location": str,
        "bandwidth": str,
        "vlan": int,
        "partnerName": str,
        "loaIssueTime": datetime,
        "lagId": str,
        "awsDevice": str,
        "jumboFrameCapable": bool,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
        "macSecCapable": bool,
        "portEncryptionStatus": str,
        "encryptionMode": str,
        "macSecKeys": List[MacSecKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ownerAccount": str,
        "connectionId": str,
        "connectionName": str,
        "connectionState": ConnectionStateType,
        "region": str,
        "location": str,
        "bandwidth": str,
        "vlan": int,
        "partnerName": str,
        "loaIssueTime": datetime,
        "lagId": str,
        "awsDevice": str,
        "jumboFrameCapable": bool,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
        "macSecCapable": bool,
        "portEncryptionStatus": str,
        "encryptionMode": str,
        "macSecKeys": List[MacSecKeyTypeDef],
    },
    total=False,
)

DisassociateMacSecKeyResponseTypeDef = TypedDict(
    "DisassociateMacSecKeyResponseTypeDef",
    {
        "connectionId": str,
        "macSecKeys": List[MacSecKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DirectConnectGatewayAssociationProposalTypeDef = TypedDict(
    "DirectConnectGatewayAssociationProposalTypeDef",
    {
        "proposalId": str,
        "directConnectGatewayId": str,
        "directConnectGatewayOwnerAccount": str,
        "proposalState": DirectConnectGatewayAssociationProposalStateType,
        "associatedGateway": AssociatedGatewayTypeDef,
        "existingAllowedPrefixesToDirectConnectGateway": List[RouteFilterPrefixTypeDef],
        "requestedAllowedPrefixesToDirectConnectGateway": List[RouteFilterPrefixTypeDef],
    },
    total=False,
)

DirectConnectGatewayAssociationTypeDef = TypedDict(
    "DirectConnectGatewayAssociationTypeDef",
    {
        "directConnectGatewayId": str,
        "directConnectGatewayOwnerAccount": str,
        "associationState": DirectConnectGatewayAssociationStateType,
        "stateChangeError": str,
        "associatedGateway": AssociatedGatewayTypeDef,
        "associationId": str,
        "allowedPrefixesToDirectConnectGateway": List[RouteFilterPrefixTypeDef],
        "virtualGatewayId": str,
        "virtualGatewayRegion": str,
        "virtualGatewayOwnerAccount": str,
    },
    total=False,
)

VirtualInterfaceResponseMetadataTypeDef = TypedDict(
    "VirtualInterfaceResponseMetadataTypeDef",
    {
        "ownerAccount": str,
        "virtualInterfaceId": str,
        "location": str,
        "connectionId": str,
        "virtualInterfaceType": str,
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
        "amazonSideAsn": int,
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "virtualInterfaceState": VirtualInterfaceStateType,
        "customerRouterConfig": str,
        "mtu": int,
        "jumboFrameCapable": bool,
        "virtualGatewayId": str,
        "directConnectGatewayId": str,
        "routeFilterPrefixes": List[RouteFilterPrefixTypeDef],
        "bgpPeers": List[BGPPeerTypeDef],
        "region": str,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "tags": List[TagTypeDef],
        "siteLinkEnabled": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VirtualInterfaceTypeDef = TypedDict(
    "VirtualInterfaceTypeDef",
    {
        "ownerAccount": str,
        "virtualInterfaceId": str,
        "location": str,
        "connectionId": str,
        "virtualInterfaceType": str,
        "virtualInterfaceName": str,
        "vlan": int,
        "asn": int,
        "amazonSideAsn": int,
        "authKey": str,
        "amazonAddress": str,
        "customerAddress": str,
        "addressFamily": AddressFamilyType,
        "virtualInterfaceState": VirtualInterfaceStateType,
        "customerRouterConfig": str,
        "mtu": int,
        "jumboFrameCapable": bool,
        "virtualGatewayId": str,
        "directConnectGatewayId": str,
        "routeFilterPrefixes": List[RouteFilterPrefixTypeDef],
        "bgpPeers": List[BGPPeerTypeDef],
        "region": str,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "tags": List[TagTypeDef],
        "siteLinkEnabled": bool,
    },
    total=False,
)

CreateBGPPeerRequestRequestTypeDef = TypedDict(
    "CreateBGPPeerRequestRequestTypeDef",
    {
        "virtualInterfaceId": str,
        "newBGPPeer": NewBGPPeerTypeDef,
    },
    total=False,
)

CreateDirectConnectGatewayResultTypeDef = TypedDict(
    "CreateDirectConnectGatewayResultTypeDef",
    {
        "directConnectGateway": DirectConnectGatewayTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDirectConnectGatewayResultTypeDef = TypedDict(
    "DeleteDirectConnectGatewayResultTypeDef",
    {
        "directConnectGateway": DirectConnectGatewayTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectConnectGatewaysResultTypeDef = TypedDict(
    "DescribeDirectConnectGatewaysResultTypeDef",
    {
        "directConnectGateways": List[DirectConnectGatewayTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDirectConnectGatewayResponseTypeDef = TypedDict(
    "UpdateDirectConnectGatewayResponseTypeDef",
    {
        "directConnectGateway": DirectConnectGatewayTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomerMetadataResponseTypeDef = TypedDict(
    "DescribeCustomerMetadataResponseTypeDef",
    {
        "agreements": List[CustomerAgreementTypeDef],
        "nniPartnerType": NniPartnerTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConnectionLoaResponseTypeDef = TypedDict(
    "DescribeConnectionLoaResponseTypeDef",
    {
        "loa": LoaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInterconnectLoaResponseTypeDef = TypedDict(
    "DescribeInterconnectLoaResponseTypeDef",
    {
        "loa": LoaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectConnectGatewayAssociationsRequestDescribeDirectConnectGatewayAssociationsPaginateTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAssociationsRequestDescribeDirectConnectGatewayAssociationsPaginateTypeDef",
    {
        "associationId": str,
        "associatedGatewayId": str,
        "directConnectGatewayId": str,
        "virtualGatewayId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDirectConnectGatewayAttachmentsRequestDescribeDirectConnectGatewayAttachmentsPaginateTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAttachmentsRequestDescribeDirectConnectGatewayAttachmentsPaginateTypeDef",
    {
        "directConnectGatewayId": str,
        "virtualInterfaceId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDirectConnectGatewaysRequestDescribeDirectConnectGatewaysPaginateTypeDef = TypedDict(
    "DescribeDirectConnectGatewaysRequestDescribeDirectConnectGatewaysPaginateTypeDef",
    {
        "directConnectGatewayId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDirectConnectGatewayAttachmentsResultTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAttachmentsResultTypeDef",
    {
        "directConnectGatewayAttachments": List[DirectConnectGatewayAttachmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRouterConfigurationResponseTypeDef = TypedDict(
    "DescribeRouterConfigurationResponseTypeDef",
    {
        "customerRouterConfig": str,
        "router": RouterTypeTypeDef,
        "virtualInterfaceId": str,
        "virtualInterfaceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualInterfaceTestHistoryResponseTypeDef = TypedDict(
    "ListVirtualInterfaceTestHistoryResponseTypeDef",
    {
        "virtualInterfaceTestHistory": List[VirtualInterfaceTestHistoryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBgpFailoverTestResponseTypeDef = TypedDict(
    "StartBgpFailoverTestResponseTypeDef",
    {
        "virtualInterfaceTest": VirtualInterfaceTestHistoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopBgpFailoverTestResponseTypeDef = TypedDict(
    "StopBgpFailoverTestResponseTypeDef",
    {
        "virtualInterfaceTest": VirtualInterfaceTestHistoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LocationsTypeDef = TypedDict(
    "LocationsTypeDef",
    {
        "locations": List[LocationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VirtualGatewaysTypeDef = TypedDict(
    "VirtualGatewaysTypeDef",
    {
        "virtualGateways": List[VirtualGatewayTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InterconnectsTypeDef = TypedDict(
    "InterconnectsTypeDef",
    {
        "interconnects": List[InterconnectTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AllocatePrivateVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "AllocatePrivateVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "ownerAccount": str,
        "newPrivateVirtualInterfaceAllocation": NewPrivateVirtualInterfaceAllocationTypeDef,
    },
)

CreatePrivateVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "CreatePrivateVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "newPrivateVirtualInterface": NewPrivateVirtualInterfaceTypeDef,
    },
)

AllocatePublicVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "AllocatePublicVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "ownerAccount": str,
        "newPublicVirtualInterfaceAllocation": NewPublicVirtualInterfaceAllocationTypeDef,
    },
)

CreatePublicVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "CreatePublicVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "newPublicVirtualInterface": NewPublicVirtualInterfaceTypeDef,
    },
)

AllocateTransitVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "AllocateTransitVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "ownerAccount": str,
        "newTransitVirtualInterfaceAllocation": NewTransitVirtualInterfaceAllocationTypeDef,
    },
)

CreateTransitVirtualInterfaceRequestRequestTypeDef = TypedDict(
    "CreateTransitVirtualInterfaceRequestRequestTypeDef",
    {
        "connectionId": str,
        "newTransitVirtualInterface": NewTransitVirtualInterfaceTypeDef,
    },
)

DescribeTagsResponseTypeDef = TypedDict(
    "DescribeTagsResponseTypeDef",
    {
        "resourceTags": List[ResourceTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConnectionsTypeDef = TypedDict(
    "ConnectionsTypeDef",
    {
        "connections": List[ConnectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LagResponseMetadataTypeDef = TypedDict(
    "LagResponseMetadataTypeDef",
    {
        "connectionsBandwidth": str,
        "numberOfConnections": int,
        "lagId": str,
        "ownerAccount": str,
        "lagName": str,
        "lagState": LagStateType,
        "location": str,
        "region": str,
        "minimumLinks": int,
        "awsDevice": str,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "connections": List[ConnectionTypeDef],
        "allowsHostedConnections": bool,
        "jumboFrameCapable": bool,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
        "macSecCapable": bool,
        "encryptionMode": str,
        "macSecKeys": List[MacSecKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LagTypeDef = TypedDict(
    "LagTypeDef",
    {
        "connectionsBandwidth": str,
        "numberOfConnections": int,
        "lagId": str,
        "ownerAccount": str,
        "lagName": str,
        "lagState": LagStateType,
        "location": str,
        "region": str,
        "minimumLinks": int,
        "awsDevice": str,
        "awsDeviceV2": str,
        "awsLogicalDeviceId": str,
        "connections": List[ConnectionTypeDef],
        "allowsHostedConnections": bool,
        "jumboFrameCapable": bool,
        "hasLogicalRedundancy": HasLogicalRedundancyType,
        "tags": List[TagTypeDef],
        "providerName": str,
        "macSecCapable": bool,
        "encryptionMode": str,
        "macSecKeys": List[MacSecKeyTypeDef],
    },
    total=False,
)

CreateDirectConnectGatewayAssociationProposalResultTypeDef = TypedDict(
    "CreateDirectConnectGatewayAssociationProposalResultTypeDef",
    {
        "directConnectGatewayAssociationProposal": DirectConnectGatewayAssociationProposalTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDirectConnectGatewayAssociationProposalResultTypeDef = TypedDict(
    "DeleteDirectConnectGatewayAssociationProposalResultTypeDef",
    {
        "directConnectGatewayAssociationProposal": DirectConnectGatewayAssociationProposalTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectConnectGatewayAssociationProposalsResultTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAssociationProposalsResultTypeDef",
    {
        "directConnectGatewayAssociationProposals": List[
            DirectConnectGatewayAssociationProposalTypeDef
        ],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AcceptDirectConnectGatewayAssociationProposalResultTypeDef = TypedDict(
    "AcceptDirectConnectGatewayAssociationProposalResultTypeDef",
    {
        "directConnectGatewayAssociation": DirectConnectGatewayAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDirectConnectGatewayAssociationResultTypeDef = TypedDict(
    "CreateDirectConnectGatewayAssociationResultTypeDef",
    {
        "directConnectGatewayAssociation": DirectConnectGatewayAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDirectConnectGatewayAssociationResultTypeDef = TypedDict(
    "DeleteDirectConnectGatewayAssociationResultTypeDef",
    {
        "directConnectGatewayAssociation": DirectConnectGatewayAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectConnectGatewayAssociationsResultTypeDef = TypedDict(
    "DescribeDirectConnectGatewayAssociationsResultTypeDef",
    {
        "directConnectGatewayAssociations": List[DirectConnectGatewayAssociationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDirectConnectGatewayAssociationResultTypeDef = TypedDict(
    "UpdateDirectConnectGatewayAssociationResultTypeDef",
    {
        "directConnectGatewayAssociation": DirectConnectGatewayAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AllocateTransitVirtualInterfaceResultTypeDef = TypedDict(
    "AllocateTransitVirtualInterfaceResultTypeDef",
    {
        "virtualInterface": VirtualInterfaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBGPPeerResponseTypeDef = TypedDict(
    "CreateBGPPeerResponseTypeDef",
    {
        "virtualInterface": VirtualInterfaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTransitVirtualInterfaceResultTypeDef = TypedDict(
    "CreateTransitVirtualInterfaceResultTypeDef",
    {
        "virtualInterface": VirtualInterfaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBGPPeerResponseTypeDef = TypedDict(
    "DeleteBGPPeerResponseTypeDef",
    {
        "virtualInterface": VirtualInterfaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VirtualInterfacesTypeDef = TypedDict(
    "VirtualInterfacesTypeDef",
    {
        "virtualInterfaces": List[VirtualInterfaceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LagsTypeDef = TypedDict(
    "LagsTypeDef",
    {
        "lags": List[LagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
