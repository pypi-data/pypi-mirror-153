"""
Type annotations for globalaccelerator service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/type_defs/)

Usage::

    ```python
    from mypy_boto3_globalaccelerator.type_defs import AcceleratorAttributesTypeDef

    data: AcceleratorAttributesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AcceleratorStatusType,
    ByoipCidrStateType,
    ClientAffinityType,
    CustomRoutingAcceleratorStatusType,
    CustomRoutingDestinationTrafficStateType,
    CustomRoutingProtocolType,
    HealthCheckProtocolType,
    HealthStateType,
    ProtocolType,
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
    "AcceleratorAttributesTypeDef",
    "IpSetTypeDef",
    "CustomRoutingEndpointConfigurationTypeDef",
    "CustomRoutingEndpointDescriptionTypeDef",
    "ResponseMetadataTypeDef",
    "AdvertiseByoipCidrRequestRequestTypeDef",
    "AllowCustomRoutingTrafficRequestRequestTypeDef",
    "ByoipCidrEventTypeDef",
    "CidrAuthorizationContextTypeDef",
    "TagTypeDef",
    "CustomRoutingDestinationConfigurationTypeDef",
    "PortRangeTypeDef",
    "EndpointConfigurationTypeDef",
    "PortOverrideTypeDef",
    "CustomRoutingAcceleratorAttributesTypeDef",
    "CustomRoutingDestinationDescriptionTypeDef",
    "DeleteAcceleratorRequestRequestTypeDef",
    "DeleteCustomRoutingAcceleratorRequestRequestTypeDef",
    "DeleteCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DeleteCustomRoutingListenerRequestRequestTypeDef",
    "DeleteEndpointGroupRequestRequestTypeDef",
    "DeleteListenerRequestRequestTypeDef",
    "DenyCustomRoutingTrafficRequestRequestTypeDef",
    "DeprovisionByoipCidrRequestRequestTypeDef",
    "DescribeAcceleratorAttributesRequestRequestTypeDef",
    "DescribeAcceleratorRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorRequestRequestTypeDef",
    "DescribeCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DescribeCustomRoutingListenerRequestRequestTypeDef",
    "DescribeEndpointGroupRequestRequestTypeDef",
    "DescribeListenerRequestRequestTypeDef",
    "SocketAddressTypeDef",
    "EndpointDescriptionTypeDef",
    "PaginatorConfigTypeDef",
    "ListAcceleratorsRequestRequestTypeDef",
    "ListByoipCidrsRequestRequestTypeDef",
    "ListCustomRoutingAcceleratorsRequestRequestTypeDef",
    "ListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    "ListCustomRoutingListenersRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsRequestRequestTypeDef",
    "ListEndpointGroupsRequestRequestTypeDef",
    "ListListenersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RemoveCustomRoutingEndpointsRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAcceleratorAttributesRequestRequestTypeDef",
    "UpdateAcceleratorRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    "WithdrawByoipCidrRequestRequestTypeDef",
    "AcceleratorTypeDef",
    "CustomRoutingAcceleratorTypeDef",
    "AddCustomRoutingEndpointsRequestRequestTypeDef",
    "AddCustomRoutingEndpointsResponseTypeDef",
    "DescribeAcceleratorAttributesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "UpdateAcceleratorAttributesResponseTypeDef",
    "ByoipCidrTypeDef",
    "ProvisionByoipCidrRequestRequestTypeDef",
    "CreateAcceleratorRequestRequestTypeDef",
    "CreateCustomRoutingAcceleratorRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateCustomRoutingEndpointGroupRequestRequestTypeDef",
    "CreateCustomRoutingListenerRequestRequestTypeDef",
    "CreateListenerRequestRequestTypeDef",
    "CustomRoutingListenerTypeDef",
    "ListenerTypeDef",
    "UpdateCustomRoutingListenerRequestRequestTypeDef",
    "UpdateListenerRequestRequestTypeDef",
    "CreateEndpointGroupRequestRequestTypeDef",
    "UpdateEndpointGroupRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesResponseTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesResponseTypeDef",
    "CustomRoutingEndpointGroupTypeDef",
    "DestinationPortMappingTypeDef",
    "PortMappingTypeDef",
    "EndpointGroupTypeDef",
    "ListAcceleratorsRequestListAcceleratorsPaginateTypeDef",
    "ListByoipCidrsRequestListByoipCidrsPaginateTypeDef",
    "ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef",
    "ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    "ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
    "ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    "ListListenersRequestListListenersPaginateTypeDef",
    "CreateAcceleratorResponseTypeDef",
    "DescribeAcceleratorResponseTypeDef",
    "ListAcceleratorsResponseTypeDef",
    "UpdateAcceleratorResponseTypeDef",
    "CreateCustomRoutingAcceleratorResponseTypeDef",
    "DescribeCustomRoutingAcceleratorResponseTypeDef",
    "ListCustomRoutingAcceleratorsResponseTypeDef",
    "UpdateCustomRoutingAcceleratorResponseTypeDef",
    "AdvertiseByoipCidrResponseTypeDef",
    "DeprovisionByoipCidrResponseTypeDef",
    "ListByoipCidrsResponseTypeDef",
    "ProvisionByoipCidrResponseTypeDef",
    "WithdrawByoipCidrResponseTypeDef",
    "CreateCustomRoutingListenerResponseTypeDef",
    "DescribeCustomRoutingListenerResponseTypeDef",
    "ListCustomRoutingListenersResponseTypeDef",
    "UpdateCustomRoutingListenerResponseTypeDef",
    "CreateListenerResponseTypeDef",
    "DescribeListenerResponseTypeDef",
    "ListListenersResponseTypeDef",
    "UpdateListenerResponseTypeDef",
    "CreateCustomRoutingEndpointGroupResponseTypeDef",
    "DescribeCustomRoutingEndpointGroupResponseTypeDef",
    "ListCustomRoutingEndpointGroupsResponseTypeDef",
    "ListCustomRoutingPortMappingsByDestinationResponseTypeDef",
    "ListCustomRoutingPortMappingsResponseTypeDef",
    "CreateEndpointGroupResponseTypeDef",
    "DescribeEndpointGroupResponseTypeDef",
    "ListEndpointGroupsResponseTypeDef",
    "UpdateEndpointGroupResponseTypeDef",
)

AcceleratorAttributesTypeDef = TypedDict(
    "AcceleratorAttributesTypeDef",
    {
        "FlowLogsEnabled": bool,
        "FlowLogsS3Bucket": str,
        "FlowLogsS3Prefix": str,
    },
    total=False,
)

IpSetTypeDef = TypedDict(
    "IpSetTypeDef",
    {
        "IpFamily": str,
        "IpAddresses": List[str],
    },
    total=False,
)

CustomRoutingEndpointConfigurationTypeDef = TypedDict(
    "CustomRoutingEndpointConfigurationTypeDef",
    {
        "EndpointId": str,
    },
    total=False,
)

CustomRoutingEndpointDescriptionTypeDef = TypedDict(
    "CustomRoutingEndpointDescriptionTypeDef",
    {
        "EndpointId": str,
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

AdvertiseByoipCidrRequestRequestTypeDef = TypedDict(
    "AdvertiseByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

_RequiredAllowCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "_RequiredAllowCustomRoutingTrafficRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointId": str,
    },
)
_OptionalAllowCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "_OptionalAllowCustomRoutingTrafficRequestRequestTypeDef",
    {
        "DestinationAddresses": Sequence[str],
        "DestinationPorts": Sequence[int],
        "AllowAllTrafficToEndpoint": bool,
    },
    total=False,
)


class AllowCustomRoutingTrafficRequestRequestTypeDef(
    _RequiredAllowCustomRoutingTrafficRequestRequestTypeDef,
    _OptionalAllowCustomRoutingTrafficRequestRequestTypeDef,
):
    pass


ByoipCidrEventTypeDef = TypedDict(
    "ByoipCidrEventTypeDef",
    {
        "Message": str,
        "Timestamp": datetime,
    },
    total=False,
)

CidrAuthorizationContextTypeDef = TypedDict(
    "CidrAuthorizationContextTypeDef",
    {
        "Message": str,
        "Signature": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CustomRoutingDestinationConfigurationTypeDef = TypedDict(
    "CustomRoutingDestinationConfigurationTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "Protocols": Sequence[CustomRoutingProtocolType],
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
    total=False,
)

EndpointConfigurationTypeDef = TypedDict(
    "EndpointConfigurationTypeDef",
    {
        "EndpointId": str,
        "Weight": int,
        "ClientIPPreservationEnabled": bool,
    },
    total=False,
)

PortOverrideTypeDef = TypedDict(
    "PortOverrideTypeDef",
    {
        "ListenerPort": int,
        "EndpointPort": int,
    },
    total=False,
)

CustomRoutingAcceleratorAttributesTypeDef = TypedDict(
    "CustomRoutingAcceleratorAttributesTypeDef",
    {
        "FlowLogsEnabled": bool,
        "FlowLogsS3Bucket": str,
        "FlowLogsS3Prefix": str,
    },
    total=False,
)

CustomRoutingDestinationDescriptionTypeDef = TypedDict(
    "CustomRoutingDestinationDescriptionTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "Protocols": List[ProtocolType],
    },
    total=False,
)

DeleteAcceleratorRequestRequestTypeDef = TypedDict(
    "DeleteAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DeleteCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DeleteCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DeleteCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DeleteEndpointGroupRequestRequestTypeDef = TypedDict(
    "DeleteEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DeleteListenerRequestRequestTypeDef = TypedDict(
    "DeleteListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

_RequiredDenyCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "_RequiredDenyCustomRoutingTrafficRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointId": str,
    },
)
_OptionalDenyCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "_OptionalDenyCustomRoutingTrafficRequestRequestTypeDef",
    {
        "DestinationAddresses": Sequence[str],
        "DestinationPorts": Sequence[int],
        "DenyAllTrafficToEndpoint": bool,
    },
    total=False,
)


class DenyCustomRoutingTrafficRequestRequestTypeDef(
    _RequiredDenyCustomRoutingTrafficRequestRequestTypeDef,
    _OptionalDenyCustomRoutingTrafficRequestRequestTypeDef,
):
    pass


DeprovisionByoipCidrRequestRequestTypeDef = TypedDict(
    "DeprovisionByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

DescribeAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "DescribeAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeAcceleratorRequestRequestTypeDef = TypedDict(
    "DescribeAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DescribeCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DescribeEndpointGroupRequestRequestTypeDef = TypedDict(
    "DescribeEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DescribeListenerRequestRequestTypeDef = TypedDict(
    "DescribeListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

SocketAddressTypeDef = TypedDict(
    "SocketAddressTypeDef",
    {
        "IpAddress": str,
        "Port": int,
    },
    total=False,
)

EndpointDescriptionTypeDef = TypedDict(
    "EndpointDescriptionTypeDef",
    {
        "EndpointId": str,
        "Weight": int,
        "HealthState": HealthStateType,
        "HealthReason": str,
        "ClientIPPreservationEnabled": bool,
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

ListAcceleratorsRequestRequestTypeDef = TypedDict(
    "ListAcceleratorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListByoipCidrsRequestRequestTypeDef = TypedDict(
    "ListByoipCidrsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListCustomRoutingAcceleratorsRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListCustomRoutingEndpointGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalListCustomRoutingEndpointGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListCustomRoutingEndpointGroupsRequestRequestTypeDef(
    _RequiredListCustomRoutingEndpointGroupsRequestRequestTypeDef,
    _OptionalListCustomRoutingEndpointGroupsRequestRequestTypeDef,
):
    pass


_RequiredListCustomRoutingListenersRequestRequestTypeDef = TypedDict(
    "_RequiredListCustomRoutingListenersRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalListCustomRoutingListenersRequestRequestTypeDef = TypedDict(
    "_OptionalListCustomRoutingListenersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListCustomRoutingListenersRequestRequestTypeDef(
    _RequiredListCustomRoutingListenersRequestRequestTypeDef,
    _OptionalListCustomRoutingListenersRequestRequestTypeDef,
):
    pass


_RequiredListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    {
        "EndpointId": str,
        "DestinationAddress": str,
    },
)
_OptionalListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef(
    _RequiredListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef,
    _OptionalListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef,
):
    pass


_RequiredListCustomRoutingPortMappingsRequestRequestTypeDef = TypedDict(
    "_RequiredListCustomRoutingPortMappingsRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalListCustomRoutingPortMappingsRequestRequestTypeDef = TypedDict(
    "_OptionalListCustomRoutingPortMappingsRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListCustomRoutingPortMappingsRequestRequestTypeDef(
    _RequiredListCustomRoutingPortMappingsRequestRequestTypeDef,
    _OptionalListCustomRoutingPortMappingsRequestRequestTypeDef,
):
    pass


_RequiredListEndpointGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListEndpointGroupsRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalListEndpointGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListEndpointGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListEndpointGroupsRequestRequestTypeDef(
    _RequiredListEndpointGroupsRequestRequestTypeDef,
    _OptionalListEndpointGroupsRequestRequestTypeDef,
):
    pass


_RequiredListListenersRequestRequestTypeDef = TypedDict(
    "_RequiredListListenersRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalListListenersRequestRequestTypeDef = TypedDict(
    "_OptionalListListenersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListListenersRequestRequestTypeDef(
    _RequiredListListenersRequestRequestTypeDef, _OptionalListListenersRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

RemoveCustomRoutingEndpointsRequestRequestTypeDef = TypedDict(
    "RemoveCustomRoutingEndpointsRequestRequestTypeDef",
    {
        "EndpointIds": Sequence[str],
        "EndpointGroupArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalUpdateAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAcceleratorAttributesRequestRequestTypeDef",
    {
        "FlowLogsEnabled": bool,
        "FlowLogsS3Bucket": str,
        "FlowLogsS3Prefix": str,
    },
    total=False,
)


class UpdateAcceleratorAttributesRequestRequestTypeDef(
    _RequiredUpdateAcceleratorAttributesRequestRequestTypeDef,
    _OptionalUpdateAcceleratorAttributesRequestRequestTypeDef,
):
    pass


_RequiredUpdateAcceleratorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalUpdateAcceleratorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IpAddressType": Literal["IPV4"],
        "Enabled": bool,
    },
    total=False,
)


class UpdateAcceleratorRequestRequestTypeDef(
    _RequiredUpdateAcceleratorRequestRequestTypeDef, _OptionalUpdateAcceleratorRequestRequestTypeDef
):
    pass


_RequiredUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    {
        "FlowLogsEnabled": bool,
        "FlowLogsS3Bucket": str,
        "FlowLogsS3Prefix": str,
    },
    total=False,
)


class UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef(
    _RequiredUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef,
    _OptionalUpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef,
):
    pass


_RequiredUpdateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalUpdateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IpAddressType": Literal["IPV4"],
        "Enabled": bool,
    },
    total=False,
)


class UpdateCustomRoutingAcceleratorRequestRequestTypeDef(
    _RequiredUpdateCustomRoutingAcceleratorRequestRequestTypeDef,
    _OptionalUpdateCustomRoutingAcceleratorRequestRequestTypeDef,
):
    pass


WithdrawByoipCidrRequestRequestTypeDef = TypedDict(
    "WithdrawByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

AcceleratorTypeDef = TypedDict(
    "AcceleratorTypeDef",
    {
        "AcceleratorArn": str,
        "Name": str,
        "IpAddressType": Literal["IPV4"],
        "Enabled": bool,
        "IpSets": List[IpSetTypeDef],
        "DnsName": str,
        "Status": AcceleratorStatusType,
        "CreatedTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

CustomRoutingAcceleratorTypeDef = TypedDict(
    "CustomRoutingAcceleratorTypeDef",
    {
        "AcceleratorArn": str,
        "Name": str,
        "IpAddressType": Literal["IPV4"],
        "Enabled": bool,
        "IpSets": List[IpSetTypeDef],
        "DnsName": str,
        "Status": CustomRoutingAcceleratorStatusType,
        "CreatedTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

AddCustomRoutingEndpointsRequestRequestTypeDef = TypedDict(
    "AddCustomRoutingEndpointsRequestRequestTypeDef",
    {
        "EndpointConfigurations": Sequence[CustomRoutingEndpointConfigurationTypeDef],
        "EndpointGroupArn": str,
    },
)

AddCustomRoutingEndpointsResponseTypeDef = TypedDict(
    "AddCustomRoutingEndpointsResponseTypeDef",
    {
        "EndpointDescriptions": List[CustomRoutingEndpointDescriptionTypeDef],
        "EndpointGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorAttributesResponseTypeDef = TypedDict(
    "DescribeAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": AcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAcceleratorAttributesResponseTypeDef = TypedDict(
    "UpdateAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": AcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ByoipCidrTypeDef = TypedDict(
    "ByoipCidrTypeDef",
    {
        "Cidr": str,
        "State": ByoipCidrStateType,
        "Events": List[ByoipCidrEventTypeDef],
    },
    total=False,
)

ProvisionByoipCidrRequestRequestTypeDef = TypedDict(
    "ProvisionByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
        "CidrAuthorizationContext": CidrAuthorizationContextTypeDef,
    },
)

_RequiredCreateAcceleratorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IdempotencyToken": str,
    },
)
_OptionalCreateAcceleratorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAcceleratorRequestRequestTypeDef",
    {
        "IpAddressType": Literal["IPV4"],
        "IpAddresses": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAcceleratorRequestRequestTypeDef(
    _RequiredCreateAcceleratorRequestRequestTypeDef, _OptionalCreateAcceleratorRequestRequestTypeDef
):
    pass


_RequiredCreateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IdempotencyToken": str,
    },
)
_OptionalCreateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "IpAddressType": Literal["IPV4"],
        "IpAddresses": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateCustomRoutingAcceleratorRequestRequestTypeDef(
    _RequiredCreateCustomRoutingAcceleratorRequestRequestTypeDef,
    _OptionalCreateCustomRoutingAcceleratorRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "CreateCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "EndpointGroupRegion": str,
        "DestinationConfigurations": Sequence[CustomRoutingDestinationConfigurationTypeDef],
        "IdempotencyToken": str,
    },
)

CreateCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "CreateCustomRoutingListenerRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
        "IdempotencyToken": str,
    },
)

_RequiredCreateListenerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateListenerRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
        "Protocol": ProtocolType,
        "IdempotencyToken": str,
    },
)
_OptionalCreateListenerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateListenerRequestRequestTypeDef",
    {
        "ClientAffinity": ClientAffinityType,
    },
    total=False,
)


class CreateListenerRequestRequestTypeDef(
    _RequiredCreateListenerRequestRequestTypeDef, _OptionalCreateListenerRequestRequestTypeDef
):
    pass


CustomRoutingListenerTypeDef = TypedDict(
    "CustomRoutingListenerTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": List[PortRangeTypeDef],
    },
    total=False,
)

ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": List[PortRangeTypeDef],
        "Protocol": ProtocolType,
        "ClientAffinity": ClientAffinityType,
    },
    total=False,
)

UpdateCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "UpdateCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
    },
)

_RequiredUpdateListenerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalUpdateListenerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateListenerRequestRequestTypeDef",
    {
        "PortRanges": Sequence[PortRangeTypeDef],
        "Protocol": ProtocolType,
        "ClientAffinity": ClientAffinityType,
    },
    total=False,
)


class UpdateListenerRequestRequestTypeDef(
    _RequiredUpdateListenerRequestRequestTypeDef, _OptionalUpdateListenerRequestRequestTypeDef
):
    pass


_RequiredCreateEndpointGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointGroupRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "EndpointGroupRegion": str,
        "IdempotencyToken": str,
    },
)
_OptionalCreateEndpointGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointGroupRequestRequestTypeDef",
    {
        "EndpointConfigurations": Sequence[EndpointConfigurationTypeDef],
        "TrafficDialPercentage": float,
        "HealthCheckPort": int,
        "HealthCheckProtocol": HealthCheckProtocolType,
        "HealthCheckPath": str,
        "HealthCheckIntervalSeconds": int,
        "ThresholdCount": int,
        "PortOverrides": Sequence[PortOverrideTypeDef],
    },
    total=False,
)


class CreateEndpointGroupRequestRequestTypeDef(
    _RequiredCreateEndpointGroupRequestRequestTypeDef,
    _OptionalCreateEndpointGroupRequestRequestTypeDef,
):
    pass


_RequiredUpdateEndpointGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)
_OptionalUpdateEndpointGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEndpointGroupRequestRequestTypeDef",
    {
        "EndpointConfigurations": Sequence[EndpointConfigurationTypeDef],
        "TrafficDialPercentage": float,
        "HealthCheckPort": int,
        "HealthCheckProtocol": HealthCheckProtocolType,
        "HealthCheckPath": str,
        "HealthCheckIntervalSeconds": int,
        "ThresholdCount": int,
        "PortOverrides": Sequence[PortOverrideTypeDef],
    },
    total=False,
)


class UpdateEndpointGroupRequestRequestTypeDef(
    _RequiredUpdateEndpointGroupRequestRequestTypeDef,
    _OptionalUpdateEndpointGroupRequestRequestTypeDef,
):
    pass


DescribeCustomRoutingAcceleratorAttributesResponseTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": CustomRoutingAcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingAcceleratorAttributesResponseTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": CustomRoutingAcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomRoutingEndpointGroupTypeDef = TypedDict(
    "CustomRoutingEndpointGroupTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointGroupRegion": str,
        "DestinationDescriptions": List[CustomRoutingDestinationDescriptionTypeDef],
        "EndpointDescriptions": List[CustomRoutingEndpointDescriptionTypeDef],
    },
    total=False,
)

DestinationPortMappingTypeDef = TypedDict(
    "DestinationPortMappingTypeDef",
    {
        "AcceleratorArn": str,
        "AcceleratorSocketAddresses": List[SocketAddressTypeDef],
        "EndpointGroupArn": str,
        "EndpointId": str,
        "EndpointGroupRegion": str,
        "DestinationSocketAddress": SocketAddressTypeDef,
        "IpAddressType": Literal["IPV4"],
        "DestinationTrafficState": CustomRoutingDestinationTrafficStateType,
    },
    total=False,
)

PortMappingTypeDef = TypedDict(
    "PortMappingTypeDef",
    {
        "AcceleratorPort": int,
        "EndpointGroupArn": str,
        "EndpointId": str,
        "DestinationSocketAddress": SocketAddressTypeDef,
        "Protocols": List[CustomRoutingProtocolType],
        "DestinationTrafficState": CustomRoutingDestinationTrafficStateType,
    },
    total=False,
)

EndpointGroupTypeDef = TypedDict(
    "EndpointGroupTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointGroupRegion": str,
        "EndpointDescriptions": List[EndpointDescriptionTypeDef],
        "TrafficDialPercentage": float,
        "HealthCheckPort": int,
        "HealthCheckProtocol": HealthCheckProtocolType,
        "HealthCheckPath": str,
        "HealthCheckIntervalSeconds": int,
        "ThresholdCount": int,
        "PortOverrides": List[PortOverrideTypeDef],
    },
    total=False,
)

ListAcceleratorsRequestListAcceleratorsPaginateTypeDef = TypedDict(
    "ListAcceleratorsRequestListAcceleratorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListByoipCidrsRequestListByoipCidrsPaginateTypeDef = TypedDict(
    "ListByoipCidrsRequestListByoipCidrsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef = TypedDict(
    "_RequiredListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef = TypedDict(
    "_OptionalListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef(
    _RequiredListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef,
    _OptionalListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef,
):
    pass


_RequiredListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef = TypedDict(
    "_RequiredListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    {
        "EndpointId": str,
        "DestinationAddress": str,
    },
)
_OptionalListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef = TypedDict(
    "_OptionalListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef(
    _RequiredListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef,
    _OptionalListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef,
):
    pass


_RequiredListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef = (
    TypedDict(
        "_RequiredListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
        {
            "AcceleratorArn": str,
        },
    )
)
_OptionalListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef = (
    TypedDict(
        "_OptionalListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
        {
            "EndpointGroupArn": str,
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)


class ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef(
    _RequiredListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef,
    _OptionalListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef,
):
    pass


_RequiredListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef = TypedDict(
    "_RequiredListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    {
        "ListenerArn": str,
    },
)
_OptionalListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef = TypedDict(
    "_OptionalListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef(
    _RequiredListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef,
    _OptionalListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef,
):
    pass


_RequiredListListenersRequestListListenersPaginateTypeDef = TypedDict(
    "_RequiredListListenersRequestListListenersPaginateTypeDef",
    {
        "AcceleratorArn": str,
    },
)
_OptionalListListenersRequestListListenersPaginateTypeDef = TypedDict(
    "_OptionalListListenersRequestListListenersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListListenersRequestListListenersPaginateTypeDef(
    _RequiredListListenersRequestListListenersPaginateTypeDef,
    _OptionalListListenersRequestListListenersPaginateTypeDef,
):
    pass


CreateAcceleratorResponseTypeDef = TypedDict(
    "CreateAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorResponseTypeDef = TypedDict(
    "DescribeAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAcceleratorsResponseTypeDef = TypedDict(
    "ListAcceleratorsResponseTypeDef",
    {
        "Accelerators": List[AcceleratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAcceleratorResponseTypeDef = TypedDict(
    "UpdateAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "CreateCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingAcceleratorsResponseTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsResponseTypeDef",
    {
        "Accelerators": List[CustomRoutingAcceleratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AdvertiseByoipCidrResponseTypeDef = TypedDict(
    "AdvertiseByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeprovisionByoipCidrResponseTypeDef = TypedDict(
    "DeprovisionByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListByoipCidrsResponseTypeDef = TypedDict(
    "ListByoipCidrsResponseTypeDef",
    {
        "ByoipCidrs": List[ByoipCidrTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProvisionByoipCidrResponseTypeDef = TypedDict(
    "ProvisionByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WithdrawByoipCidrResponseTypeDef = TypedDict(
    "WithdrawByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingListenerResponseTypeDef = TypedDict(
    "CreateCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingListenerResponseTypeDef = TypedDict(
    "DescribeCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingListenersResponseTypeDef = TypedDict(
    "ListCustomRoutingListenersResponseTypeDef",
    {
        "Listeners": List[CustomRoutingListenerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingListenerResponseTypeDef = TypedDict(
    "UpdateCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateListenerResponseTypeDef = TypedDict(
    "CreateListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeListenerResponseTypeDef = TypedDict(
    "DescribeListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListListenersResponseTypeDef = TypedDict(
    "ListListenersResponseTypeDef",
    {
        "Listeners": List[ListenerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateListenerResponseTypeDef = TypedDict(
    "UpdateListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingEndpointGroupResponseTypeDef = TypedDict(
    "CreateCustomRoutingEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": CustomRoutingEndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingEndpointGroupResponseTypeDef = TypedDict(
    "DescribeCustomRoutingEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": CustomRoutingEndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingEndpointGroupsResponseTypeDef = TypedDict(
    "ListCustomRoutingEndpointGroupsResponseTypeDef",
    {
        "EndpointGroups": List[CustomRoutingEndpointGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingPortMappingsByDestinationResponseTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsByDestinationResponseTypeDef",
    {
        "DestinationPortMappings": List[DestinationPortMappingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingPortMappingsResponseTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsResponseTypeDef",
    {
        "PortMappings": List[PortMappingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEndpointGroupResponseTypeDef = TypedDict(
    "CreateEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEndpointGroupResponseTypeDef = TypedDict(
    "DescribeEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEndpointGroupsResponseTypeDef = TypedDict(
    "ListEndpointGroupsResponseTypeDef",
    {
        "EndpointGroups": List[EndpointGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEndpointGroupResponseTypeDef = TypedDict(
    "UpdateEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
