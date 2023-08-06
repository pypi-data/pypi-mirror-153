"""
Type annotations for mediaconnect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediaconnect.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AlgorithmType,
    ColorimetryType,
    EncoderProfileType,
    EncodingNameType,
    EntitlementStatusType,
    FailoverModeType,
    KeyTypeType,
    MaintenanceDayType,
    MediaStreamTypeType,
    NetworkInterfaceTypeType,
    ProtocolType,
    RangeType,
    ReservationStateType,
    ScanModeType,
    SourceTypeType,
    StateType,
    StatusType,
    TcsType,
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
    "ResponseMetadataTypeDef",
    "VpcInterfaceRequestTypeDef",
    "VpcInterfaceTypeDef",
    "AddMaintenanceTypeDef",
    "EncryptionTypeDef",
    "VpcInterfaceAttachmentTypeDef",
    "DeleteFlowRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeFlowRequestRequestTypeDef",
    "MessagesTypeDef",
    "DescribeOfferingRequestRequestTypeDef",
    "DescribeReservationRequestRequestTypeDef",
    "InterfaceRequestTypeDef",
    "InterfaceTypeDef",
    "EncodingParametersRequestTypeDef",
    "EncodingParametersTypeDef",
    "SourcePriorityTypeDef",
    "MaintenanceTypeDef",
    "FmtpRequestTypeDef",
    "FmtpTypeDef",
    "PaginatorConfigTypeDef",
    "ListEntitlementsRequestRequestTypeDef",
    "ListedEntitlementTypeDef",
    "ListFlowsRequestRequestTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListReservationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResourceSpecificationTypeDef",
    "TransportTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "RemoveFlowMediaStreamRequestRequestTypeDef",
    "RemoveFlowOutputRequestRequestTypeDef",
    "RemoveFlowSourceRequestRequestTypeDef",
    "RemoveFlowVpcInterfaceRequestRequestTypeDef",
    "RevokeFlowEntitlementRequestRequestTypeDef",
    "StartFlowRequestRequestTypeDef",
    "StopFlowRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEncryptionTypeDef",
    "UpdateMaintenanceTypeDef",
    "DeleteFlowResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RemoveFlowMediaStreamResponseTypeDef",
    "RemoveFlowOutputResponseTypeDef",
    "RemoveFlowSourceResponseTypeDef",
    "RemoveFlowVpcInterfaceResponseTypeDef",
    "RevokeFlowEntitlementResponseTypeDef",
    "StartFlowResponseTypeDef",
    "StopFlowResponseTypeDef",
    "AddFlowVpcInterfacesRequestRequestTypeDef",
    "AddFlowVpcInterfacesResponseTypeDef",
    "EntitlementTypeDef",
    "GrantEntitlementRequestTypeDef",
    "DescribeFlowRequestFlowActiveWaitTypeDef",
    "DescribeFlowRequestFlowDeletedWaitTypeDef",
    "DescribeFlowRequestFlowStandbyWaitTypeDef",
    "DestinationConfigurationRequestTypeDef",
    "InputConfigurationRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "InputConfigurationTypeDef",
    "FailoverConfigTypeDef",
    "UpdateFailoverConfigTypeDef",
    "ListedFlowTypeDef",
    "MediaStreamAttributesRequestTypeDef",
    "MediaStreamAttributesTypeDef",
    "ListEntitlementsRequestListEntitlementsPaginateTypeDef",
    "ListFlowsRequestListFlowsPaginateTypeDef",
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    "ListReservationsRequestListReservationsPaginateTypeDef",
    "ListEntitlementsResponseTypeDef",
    "OfferingTypeDef",
    "ReservationTypeDef",
    "UpdateFlowEntitlementRequestRequestTypeDef",
    "GrantFlowEntitlementsResponseTypeDef",
    "UpdateFlowEntitlementResponseTypeDef",
    "GrantFlowEntitlementsRequestRequestTypeDef",
    "MediaStreamOutputConfigurationRequestTypeDef",
    "MediaStreamSourceConfigurationRequestTypeDef",
    "MediaStreamOutputConfigurationTypeDef",
    "MediaStreamSourceConfigurationTypeDef",
    "UpdateFlowRequestRequestTypeDef",
    "ListFlowsResponseTypeDef",
    "AddMediaStreamRequestTypeDef",
    "UpdateFlowMediaStreamRequestRequestTypeDef",
    "MediaStreamTypeDef",
    "DescribeOfferingResponseTypeDef",
    "ListOfferingsResponseTypeDef",
    "DescribeReservationResponseTypeDef",
    "ListReservationsResponseTypeDef",
    "PurchaseOfferingResponseTypeDef",
    "AddOutputRequestTypeDef",
    "UpdateFlowOutputRequestRequestTypeDef",
    "SetSourceRequestTypeDef",
    "UpdateFlowSourceRequestRequestTypeDef",
    "OutputTypeDef",
    "SourceTypeDef",
    "AddFlowMediaStreamsRequestRequestTypeDef",
    "AddFlowMediaStreamsResponseTypeDef",
    "UpdateFlowMediaStreamResponseTypeDef",
    "AddFlowOutputsRequestRequestTypeDef",
    "AddFlowSourcesRequestRequestTypeDef",
    "CreateFlowRequestRequestTypeDef",
    "AddFlowOutputsResponseTypeDef",
    "UpdateFlowOutputResponseTypeDef",
    "AddFlowSourcesResponseTypeDef",
    "FlowTypeDef",
    "UpdateFlowSourceResponseTypeDef",
    "CreateFlowResponseTypeDef",
    "DescribeFlowResponseTypeDef",
    "UpdateFlowResponseTypeDef",
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

_RequiredVpcInterfaceRequestTypeDef = TypedDict(
    "_RequiredVpcInterfaceRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
        "SecurityGroupIds": Sequence[str],
        "SubnetId": str,
    },
)
_OptionalVpcInterfaceRequestTypeDef = TypedDict(
    "_OptionalVpcInterfaceRequestTypeDef",
    {
        "NetworkInterfaceType": NetworkInterfaceTypeType,
    },
    total=False,
)


class VpcInterfaceRequestTypeDef(
    _RequiredVpcInterfaceRequestTypeDef, _OptionalVpcInterfaceRequestTypeDef
):
    pass


VpcInterfaceTypeDef = TypedDict(
    "VpcInterfaceTypeDef",
    {
        "Name": str,
        "NetworkInterfaceIds": List[str],
        "NetworkInterfaceType": NetworkInterfaceTypeType,
        "RoleArn": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
    },
)

AddMaintenanceTypeDef = TypedDict(
    "AddMaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceStartHour": str,
    },
)

_RequiredEncryptionTypeDef = TypedDict(
    "_RequiredEncryptionTypeDef",
    {
        "RoleArn": str,
    },
)
_OptionalEncryptionTypeDef = TypedDict(
    "_OptionalEncryptionTypeDef",
    {
        "Algorithm": AlgorithmType,
        "ConstantInitializationVector": str,
        "DeviceId": str,
        "KeyType": KeyTypeType,
        "Region": str,
        "ResourceId": str,
        "SecretArn": str,
        "Url": str,
    },
    total=False,
)


class EncryptionTypeDef(_RequiredEncryptionTypeDef, _OptionalEncryptionTypeDef):
    pass


VpcInterfaceAttachmentTypeDef = TypedDict(
    "VpcInterfaceAttachmentTypeDef",
    {
        "VpcInterfaceName": str,
    },
    total=False,
)

DeleteFlowRequestRequestTypeDef = TypedDict(
    "DeleteFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeFlowRequestRequestTypeDef = TypedDict(
    "DescribeFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

MessagesTypeDef = TypedDict(
    "MessagesTypeDef",
    {
        "Errors": List[str],
    },
)

DescribeOfferingRequestRequestTypeDef = TypedDict(
    "DescribeOfferingRequestRequestTypeDef",
    {
        "OfferingArn": str,
    },
)

DescribeReservationRequestRequestTypeDef = TypedDict(
    "DescribeReservationRequestRequestTypeDef",
    {
        "ReservationArn": str,
    },
)

InterfaceRequestTypeDef = TypedDict(
    "InterfaceRequestTypeDef",
    {
        "Name": str,
    },
)

InterfaceTypeDef = TypedDict(
    "InterfaceTypeDef",
    {
        "Name": str,
    },
)

EncodingParametersRequestTypeDef = TypedDict(
    "EncodingParametersRequestTypeDef",
    {
        "CompressionFactor": float,
        "EncoderProfile": EncoderProfileType,
    },
)

EncodingParametersTypeDef = TypedDict(
    "EncodingParametersTypeDef",
    {
        "CompressionFactor": float,
        "EncoderProfile": EncoderProfileType,
    },
)

SourcePriorityTypeDef = TypedDict(
    "SourcePriorityTypeDef",
    {
        "PrimarySource": str,
    },
    total=False,
)

MaintenanceTypeDef = TypedDict(
    "MaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceDeadline": str,
        "MaintenanceScheduledDate": str,
        "MaintenanceStartHour": str,
    },
    total=False,
)

FmtpRequestTypeDef = TypedDict(
    "FmtpRequestTypeDef",
    {
        "ChannelOrder": str,
        "Colorimetry": ColorimetryType,
        "ExactFramerate": str,
        "Par": str,
        "Range": RangeType,
        "ScanMode": ScanModeType,
        "Tcs": TcsType,
    },
    total=False,
)

FmtpTypeDef = TypedDict(
    "FmtpTypeDef",
    {
        "ChannelOrder": str,
        "Colorimetry": ColorimetryType,
        "ExactFramerate": str,
        "Par": str,
        "Range": RangeType,
        "ScanMode": ScanModeType,
        "Tcs": TcsType,
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

ListEntitlementsRequestRequestTypeDef = TypedDict(
    "ListEntitlementsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListedEntitlementTypeDef = TypedDict(
    "_RequiredListedEntitlementTypeDef",
    {
        "EntitlementArn": str,
        "EntitlementName": str,
    },
)
_OptionalListedEntitlementTypeDef = TypedDict(
    "_OptionalListedEntitlementTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
    },
    total=False,
)


class ListedEntitlementTypeDef(
    _RequiredListedEntitlementTypeDef, _OptionalListedEntitlementTypeDef
):
    pass


ListFlowsRequestRequestTypeDef = TypedDict(
    "ListFlowsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOfferingsRequestRequestTypeDef = TypedDict(
    "ListOfferingsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListReservationsRequestRequestTypeDef = TypedDict(
    "ListReservationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredResourceSpecificationTypeDef = TypedDict(
    "_RequiredResourceSpecificationTypeDef",
    {
        "ResourceType": Literal["Mbps_Outbound_Bandwidth"],
    },
)
_OptionalResourceSpecificationTypeDef = TypedDict(
    "_OptionalResourceSpecificationTypeDef",
    {
        "ReservedBitrate": int,
    },
    total=False,
)


class ResourceSpecificationTypeDef(
    _RequiredResourceSpecificationTypeDef, _OptionalResourceSpecificationTypeDef
):
    pass


_RequiredTransportTypeDef = TypedDict(
    "_RequiredTransportTypeDef",
    {
        "Protocol": ProtocolType,
    },
)
_OptionalTransportTypeDef = TypedDict(
    "_OptionalTransportTypeDef",
    {
        "CidrAllowList": List[str],
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MinLatency": int,
        "RemoteId": str,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SmoothingLatency": int,
        "StreamId": str,
    },
    total=False,
)


class TransportTypeDef(_RequiredTransportTypeDef, _OptionalTransportTypeDef):
    pass


PurchaseOfferingRequestRequestTypeDef = TypedDict(
    "PurchaseOfferingRequestRequestTypeDef",
    {
        "OfferingArn": str,
        "ReservationName": str,
        "Start": str,
    },
)

RemoveFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "RemoveFlowMediaStreamRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
    },
)

RemoveFlowOutputRequestRequestTypeDef = TypedDict(
    "RemoveFlowOutputRequestRequestTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
    },
)

RemoveFlowSourceRequestRequestTypeDef = TypedDict(
    "RemoveFlowSourceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
    },
)

RemoveFlowVpcInterfaceRequestRequestTypeDef = TypedDict(
    "RemoveFlowVpcInterfaceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaceName": str,
    },
)

RevokeFlowEntitlementRequestRequestTypeDef = TypedDict(
    "RevokeFlowEntitlementRequestRequestTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
    },
)

StartFlowRequestRequestTypeDef = TypedDict(
    "StartFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

StopFlowRequestRequestTypeDef = TypedDict(
    "StopFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateEncryptionTypeDef = TypedDict(
    "UpdateEncryptionTypeDef",
    {
        "Algorithm": AlgorithmType,
        "ConstantInitializationVector": str,
        "DeviceId": str,
        "KeyType": KeyTypeType,
        "Region": str,
        "ResourceId": str,
        "RoleArn": str,
        "SecretArn": str,
        "Url": str,
    },
    total=False,
)

UpdateMaintenanceTypeDef = TypedDict(
    "UpdateMaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceScheduledDate": str,
        "MaintenanceStartHour": str,
    },
    total=False,
)

DeleteFlowResponseTypeDef = TypedDict(
    "DeleteFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFlowMediaStreamResponseTypeDef = TypedDict(
    "RemoveFlowMediaStreamResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFlowOutputResponseTypeDef = TypedDict(
    "RemoveFlowOutputResponseTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFlowSourceResponseTypeDef = TypedDict(
    "RemoveFlowSourceResponseTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFlowVpcInterfaceResponseTypeDef = TypedDict(
    "RemoveFlowVpcInterfaceResponseTypeDef",
    {
        "FlowArn": str,
        "NonDeletedNetworkInterfaceIds": List[str],
        "VpcInterfaceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RevokeFlowEntitlementResponseTypeDef = TypedDict(
    "RevokeFlowEntitlementResponseTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFlowResponseTypeDef = TypedDict(
    "StartFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopFlowResponseTypeDef = TypedDict(
    "StopFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddFlowVpcInterfacesRequestRequestTypeDef = TypedDict(
    "AddFlowVpcInterfacesRequestRequestTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaces": Sequence[VpcInterfaceRequestTypeDef],
    },
)

AddFlowVpcInterfacesResponseTypeDef = TypedDict(
    "AddFlowVpcInterfacesResponseTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaces": List[VpcInterfaceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredEntitlementTypeDef = TypedDict(
    "_RequiredEntitlementTypeDef",
    {
        "EntitlementArn": str,
        "Name": str,
        "Subscribers": List[str],
    },
)
_OptionalEntitlementTypeDef = TypedDict(
    "_OptionalEntitlementTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
    },
    total=False,
)


class EntitlementTypeDef(_RequiredEntitlementTypeDef, _OptionalEntitlementTypeDef):
    pass


_RequiredGrantEntitlementRequestTypeDef = TypedDict(
    "_RequiredGrantEntitlementRequestTypeDef",
    {
        "Subscribers": Sequence[str],
    },
)
_OptionalGrantEntitlementRequestTypeDef = TypedDict(
    "_OptionalGrantEntitlementRequestTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
        "Name": str,
    },
    total=False,
)


class GrantEntitlementRequestTypeDef(
    _RequiredGrantEntitlementRequestTypeDef, _OptionalGrantEntitlementRequestTypeDef
):
    pass


_RequiredDescribeFlowRequestFlowActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowActiveWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowActiveWaitTypeDef(
    _RequiredDescribeFlowRequestFlowActiveWaitTypeDef,
    _OptionalDescribeFlowRequestFlowActiveWaitTypeDef,
):
    pass


_RequiredDescribeFlowRequestFlowDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowDeletedWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowDeletedWaitTypeDef(
    _RequiredDescribeFlowRequestFlowDeletedWaitTypeDef,
    _OptionalDescribeFlowRequestFlowDeletedWaitTypeDef,
):
    pass


_RequiredDescribeFlowRequestFlowStandbyWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowStandbyWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowStandbyWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowStandbyWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowStandbyWaitTypeDef(
    _RequiredDescribeFlowRequestFlowStandbyWaitTypeDef,
    _OptionalDescribeFlowRequestFlowStandbyWaitTypeDef,
):
    pass


DestinationConfigurationRequestTypeDef = TypedDict(
    "DestinationConfigurationRequestTypeDef",
    {
        "DestinationIp": str,
        "DestinationPort": int,
        "Interface": InterfaceRequestTypeDef,
    },
)

InputConfigurationRequestTypeDef = TypedDict(
    "InputConfigurationRequestTypeDef",
    {
        "InputPort": int,
        "Interface": InterfaceRequestTypeDef,
    },
)

DestinationConfigurationTypeDef = TypedDict(
    "DestinationConfigurationTypeDef",
    {
        "DestinationIp": str,
        "DestinationPort": int,
        "Interface": InterfaceTypeDef,
        "OutboundIp": str,
    },
)

InputConfigurationTypeDef = TypedDict(
    "InputConfigurationTypeDef",
    {
        "InputIp": str,
        "InputPort": int,
        "Interface": InterfaceTypeDef,
    },
)

FailoverConfigTypeDef = TypedDict(
    "FailoverConfigTypeDef",
    {
        "FailoverMode": FailoverModeType,
        "RecoveryWindow": int,
        "SourcePriority": SourcePriorityTypeDef,
        "State": StateType,
    },
    total=False,
)

UpdateFailoverConfigTypeDef = TypedDict(
    "UpdateFailoverConfigTypeDef",
    {
        "FailoverMode": FailoverModeType,
        "RecoveryWindow": int,
        "SourcePriority": SourcePriorityTypeDef,
        "State": StateType,
    },
    total=False,
)

_RequiredListedFlowTypeDef = TypedDict(
    "_RequiredListedFlowTypeDef",
    {
        "AvailabilityZone": str,
        "Description": str,
        "FlowArn": str,
        "Name": str,
        "SourceType": SourceTypeType,
        "Status": StatusType,
    },
)
_OptionalListedFlowTypeDef = TypedDict(
    "_OptionalListedFlowTypeDef",
    {
        "Maintenance": MaintenanceTypeDef,
    },
    total=False,
)


class ListedFlowTypeDef(_RequiredListedFlowTypeDef, _OptionalListedFlowTypeDef):
    pass


MediaStreamAttributesRequestTypeDef = TypedDict(
    "MediaStreamAttributesRequestTypeDef",
    {
        "Fmtp": FmtpRequestTypeDef,
        "Lang": str,
    },
    total=False,
)

_RequiredMediaStreamAttributesTypeDef = TypedDict(
    "_RequiredMediaStreamAttributesTypeDef",
    {
        "Fmtp": FmtpTypeDef,
    },
)
_OptionalMediaStreamAttributesTypeDef = TypedDict(
    "_OptionalMediaStreamAttributesTypeDef",
    {
        "Lang": str,
    },
    total=False,
)


class MediaStreamAttributesTypeDef(
    _RequiredMediaStreamAttributesTypeDef, _OptionalMediaStreamAttributesTypeDef
):
    pass


ListEntitlementsRequestListEntitlementsPaginateTypeDef = TypedDict(
    "ListEntitlementsRequestListEntitlementsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFlowsRequestListFlowsPaginateTypeDef = TypedDict(
    "ListFlowsRequestListFlowsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOfferingsRequestListOfferingsPaginateTypeDef = TypedDict(
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListReservationsRequestListReservationsPaginateTypeDef = TypedDict(
    "ListReservationsRequestListReservationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEntitlementsResponseTypeDef = TypedDict(
    "ListEntitlementsResponseTypeDef",
    {
        "Entitlements": List[ListedEntitlementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OfferingTypeDef = TypedDict(
    "OfferingTypeDef",
    {
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "OfferingArn": str,
        "OfferingDescription": str,
        "PricePerUnit": str,
        "PriceUnits": Literal["HOURLY"],
        "ResourceSpecification": ResourceSpecificationTypeDef,
    },
)

ReservationTypeDef = TypedDict(
    "ReservationTypeDef",
    {
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "End": str,
        "OfferingArn": str,
        "OfferingDescription": str,
        "PricePerUnit": str,
        "PriceUnits": Literal["HOURLY"],
        "ReservationArn": str,
        "ReservationName": str,
        "ReservationState": ReservationStateType,
        "ResourceSpecification": ResourceSpecificationTypeDef,
        "Start": str,
    },
)

_RequiredUpdateFlowEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowEntitlementRequestRequestTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
    },
)
_OptionalUpdateFlowEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowEntitlementRequestRequestTypeDef",
    {
        "Description": str,
        "Encryption": UpdateEncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
        "Subscribers": Sequence[str],
    },
    total=False,
)


class UpdateFlowEntitlementRequestRequestTypeDef(
    _RequiredUpdateFlowEntitlementRequestRequestTypeDef,
    _OptionalUpdateFlowEntitlementRequestRequestTypeDef,
):
    pass


GrantFlowEntitlementsResponseTypeDef = TypedDict(
    "GrantFlowEntitlementsResponseTypeDef",
    {
        "Entitlements": List[EntitlementTypeDef],
        "FlowArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFlowEntitlementResponseTypeDef = TypedDict(
    "UpdateFlowEntitlementResponseTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "FlowArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GrantFlowEntitlementsRequestRequestTypeDef = TypedDict(
    "GrantFlowEntitlementsRequestRequestTypeDef",
    {
        "Entitlements": Sequence[GrantEntitlementRequestTypeDef],
        "FlowArn": str,
    },
)

_RequiredMediaStreamOutputConfigurationRequestTypeDef = TypedDict(
    "_RequiredMediaStreamOutputConfigurationRequestTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamOutputConfigurationRequestTypeDef = TypedDict(
    "_OptionalMediaStreamOutputConfigurationRequestTypeDef",
    {
        "DestinationConfigurations": Sequence[DestinationConfigurationRequestTypeDef],
        "EncodingParameters": EncodingParametersRequestTypeDef,
    },
    total=False,
)


class MediaStreamOutputConfigurationRequestTypeDef(
    _RequiredMediaStreamOutputConfigurationRequestTypeDef,
    _OptionalMediaStreamOutputConfigurationRequestTypeDef,
):
    pass


_RequiredMediaStreamSourceConfigurationRequestTypeDef = TypedDict(
    "_RequiredMediaStreamSourceConfigurationRequestTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamSourceConfigurationRequestTypeDef = TypedDict(
    "_OptionalMediaStreamSourceConfigurationRequestTypeDef",
    {
        "InputConfigurations": Sequence[InputConfigurationRequestTypeDef],
    },
    total=False,
)


class MediaStreamSourceConfigurationRequestTypeDef(
    _RequiredMediaStreamSourceConfigurationRequestTypeDef,
    _OptionalMediaStreamSourceConfigurationRequestTypeDef,
):
    pass


_RequiredMediaStreamOutputConfigurationTypeDef = TypedDict(
    "_RequiredMediaStreamOutputConfigurationTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamOutputConfigurationTypeDef = TypedDict(
    "_OptionalMediaStreamOutputConfigurationTypeDef",
    {
        "DestinationConfigurations": List[DestinationConfigurationTypeDef],
        "EncodingParameters": EncodingParametersTypeDef,
    },
    total=False,
)


class MediaStreamOutputConfigurationTypeDef(
    _RequiredMediaStreamOutputConfigurationTypeDef, _OptionalMediaStreamOutputConfigurationTypeDef
):
    pass


_RequiredMediaStreamSourceConfigurationTypeDef = TypedDict(
    "_RequiredMediaStreamSourceConfigurationTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamSourceConfigurationTypeDef = TypedDict(
    "_OptionalMediaStreamSourceConfigurationTypeDef",
    {
        "InputConfigurations": List[InputConfigurationTypeDef],
    },
    total=False,
)


class MediaStreamSourceConfigurationTypeDef(
    _RequiredMediaStreamSourceConfigurationTypeDef, _OptionalMediaStreamSourceConfigurationTypeDef
):
    pass


_RequiredUpdateFlowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalUpdateFlowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowRequestRequestTypeDef",
    {
        "SourceFailoverConfig": UpdateFailoverConfigTypeDef,
        "Maintenance": UpdateMaintenanceTypeDef,
    },
    total=False,
)


class UpdateFlowRequestRequestTypeDef(
    _RequiredUpdateFlowRequestRequestTypeDef, _OptionalUpdateFlowRequestRequestTypeDef
):
    pass


ListFlowsResponseTypeDef = TypedDict(
    "ListFlowsResponseTypeDef",
    {
        "Flows": List[ListedFlowTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAddMediaStreamRequestTypeDef = TypedDict(
    "_RequiredAddMediaStreamRequestTypeDef",
    {
        "MediaStreamId": int,
        "MediaStreamName": str,
        "MediaStreamType": MediaStreamTypeType,
    },
)
_OptionalAddMediaStreamRequestTypeDef = TypedDict(
    "_OptionalAddMediaStreamRequestTypeDef",
    {
        "Attributes": MediaStreamAttributesRequestTypeDef,
        "ClockRate": int,
        "Description": str,
        "VideoFormat": str,
    },
    total=False,
)


class AddMediaStreamRequestTypeDef(
    _RequiredAddMediaStreamRequestTypeDef, _OptionalAddMediaStreamRequestTypeDef
):
    pass


_RequiredUpdateFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowMediaStreamRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
    },
)
_OptionalUpdateFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowMediaStreamRequestRequestTypeDef",
    {
        "Attributes": MediaStreamAttributesRequestTypeDef,
        "ClockRate": int,
        "Description": str,
        "MediaStreamType": MediaStreamTypeType,
        "VideoFormat": str,
    },
    total=False,
)


class UpdateFlowMediaStreamRequestRequestTypeDef(
    _RequiredUpdateFlowMediaStreamRequestRequestTypeDef,
    _OptionalUpdateFlowMediaStreamRequestRequestTypeDef,
):
    pass


_RequiredMediaStreamTypeDef = TypedDict(
    "_RequiredMediaStreamTypeDef",
    {
        "Fmt": int,
        "MediaStreamId": int,
        "MediaStreamName": str,
        "MediaStreamType": MediaStreamTypeType,
    },
)
_OptionalMediaStreamTypeDef = TypedDict(
    "_OptionalMediaStreamTypeDef",
    {
        "Attributes": MediaStreamAttributesTypeDef,
        "ClockRate": int,
        "Description": str,
        "VideoFormat": str,
    },
    total=False,
)


class MediaStreamTypeDef(_RequiredMediaStreamTypeDef, _OptionalMediaStreamTypeDef):
    pass


DescribeOfferingResponseTypeDef = TypedDict(
    "DescribeOfferingResponseTypeDef",
    {
        "Offering": OfferingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOfferingsResponseTypeDef = TypedDict(
    "ListOfferingsResponseTypeDef",
    {
        "NextToken": str,
        "Offerings": List[OfferingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeReservationResponseTypeDef = TypedDict(
    "DescribeReservationResponseTypeDef",
    {
        "Reservation": ReservationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReservationsResponseTypeDef = TypedDict(
    "ListReservationsResponseTypeDef",
    {
        "NextToken": str,
        "Reservations": List[ReservationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PurchaseOfferingResponseTypeDef = TypedDict(
    "PurchaseOfferingResponseTypeDef",
    {
        "Reservation": ReservationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAddOutputRequestTypeDef = TypedDict(
    "_RequiredAddOutputRequestTypeDef",
    {
        "Protocol": ProtocolType,
    },
)
_OptionalAddOutputRequestTypeDef = TypedDict(
    "_OptionalAddOutputRequestTypeDef",
    {
        "CidrAllowList": Sequence[str],
        "Description": str,
        "Destination": str,
        "Encryption": EncryptionTypeDef,
        "MaxLatency": int,
        "MediaStreamOutputConfigurations": Sequence[MediaStreamOutputConfigurationRequestTypeDef],
        "MinLatency": int,
        "Name": str,
        "Port": int,
        "RemoteId": str,
        "SenderControlPort": int,
        "SmoothingLatency": int,
        "StreamId": str,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class AddOutputRequestTypeDef(_RequiredAddOutputRequestTypeDef, _OptionalAddOutputRequestTypeDef):
    pass


_RequiredUpdateFlowOutputRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowOutputRequestRequestTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
    },
)
_OptionalUpdateFlowOutputRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowOutputRequestRequestTypeDef",
    {
        "CidrAllowList": Sequence[str],
        "Description": str,
        "Destination": str,
        "Encryption": UpdateEncryptionTypeDef,
        "MaxLatency": int,
        "MediaStreamOutputConfigurations": Sequence[MediaStreamOutputConfigurationRequestTypeDef],
        "MinLatency": int,
        "Port": int,
        "Protocol": ProtocolType,
        "RemoteId": str,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SmoothingLatency": int,
        "StreamId": str,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class UpdateFlowOutputRequestRequestTypeDef(
    _RequiredUpdateFlowOutputRequestRequestTypeDef, _OptionalUpdateFlowOutputRequestRequestTypeDef
):
    pass


SetSourceRequestTypeDef = TypedDict(
    "SetSourceRequestTypeDef",
    {
        "Decryption": EncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestPort": int,
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MediaStreamSourceConfigurations": Sequence[MediaStreamSourceConfigurationRequestTypeDef],
        "MinLatency": int,
        "Name": str,
        "Protocol": ProtocolType,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "StreamId": str,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
    },
    total=False,
)

_RequiredUpdateFlowSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowSourceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
    },
)
_OptionalUpdateFlowSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowSourceRequestRequestTypeDef",
    {
        "Decryption": UpdateEncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestPort": int,
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MediaStreamSourceConfigurations": Sequence[MediaStreamSourceConfigurationRequestTypeDef],
        "MinLatency": int,
        "Protocol": ProtocolType,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "StreamId": str,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
    },
    total=False,
)


class UpdateFlowSourceRequestRequestTypeDef(
    _RequiredUpdateFlowSourceRequestRequestTypeDef, _OptionalUpdateFlowSourceRequestRequestTypeDef
):
    pass


_RequiredOutputTypeDef = TypedDict(
    "_RequiredOutputTypeDef",
    {
        "Name": str,
        "OutputArn": str,
    },
)
_OptionalOutputTypeDef = TypedDict(
    "_OptionalOutputTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Destination": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementArn": str,
        "ListenerAddress": str,
        "MediaLiveInputArn": str,
        "MediaStreamOutputConfigurations": List[MediaStreamOutputConfigurationTypeDef],
        "Port": int,
        "Transport": TransportTypeDef,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class OutputTypeDef(_RequiredOutputTypeDef, _OptionalOutputTypeDef):
    pass


_RequiredSourceTypeDef = TypedDict(
    "_RequiredSourceTypeDef",
    {
        "Name": str,
        "SourceArn": str,
    },
)
_OptionalSourceTypeDef = TypedDict(
    "_OptionalSourceTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Decryption": EncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestIp": str,
        "IngestPort": int,
        "MediaStreamSourceConfigurations": List[MediaStreamSourceConfigurationTypeDef],
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "Transport": TransportTypeDef,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
    },
    total=False,
)


class SourceTypeDef(_RequiredSourceTypeDef, _OptionalSourceTypeDef):
    pass


AddFlowMediaStreamsRequestRequestTypeDef = TypedDict(
    "AddFlowMediaStreamsRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreams": Sequence[AddMediaStreamRequestTypeDef],
    },
)

AddFlowMediaStreamsResponseTypeDef = TypedDict(
    "AddFlowMediaStreamsResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStreams": List[MediaStreamTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFlowMediaStreamResponseTypeDef = TypedDict(
    "UpdateFlowMediaStreamResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStream": MediaStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddFlowOutputsRequestRequestTypeDef = TypedDict(
    "AddFlowOutputsRequestRequestTypeDef",
    {
        "FlowArn": str,
        "Outputs": Sequence[AddOutputRequestTypeDef],
    },
)

AddFlowSourcesRequestRequestTypeDef = TypedDict(
    "AddFlowSourcesRequestRequestTypeDef",
    {
        "FlowArn": str,
        "Sources": Sequence[SetSourceRequestTypeDef],
    },
)

_RequiredCreateFlowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFlowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateFlowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFlowRequestRequestTypeDef",
    {
        "AvailabilityZone": str,
        "Entitlements": Sequence[GrantEntitlementRequestTypeDef],
        "MediaStreams": Sequence[AddMediaStreamRequestTypeDef],
        "Outputs": Sequence[AddOutputRequestTypeDef],
        "Source": SetSourceRequestTypeDef,
        "SourceFailoverConfig": FailoverConfigTypeDef,
        "Sources": Sequence[SetSourceRequestTypeDef],
        "VpcInterfaces": Sequence[VpcInterfaceRequestTypeDef],
        "Maintenance": AddMaintenanceTypeDef,
    },
    total=False,
)


class CreateFlowRequestRequestTypeDef(
    _RequiredCreateFlowRequestRequestTypeDef, _OptionalCreateFlowRequestRequestTypeDef
):
    pass


AddFlowOutputsResponseTypeDef = TypedDict(
    "AddFlowOutputsResponseTypeDef",
    {
        "FlowArn": str,
        "Outputs": List[OutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFlowOutputResponseTypeDef = TypedDict(
    "UpdateFlowOutputResponseTypeDef",
    {
        "FlowArn": str,
        "Output": OutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddFlowSourcesResponseTypeDef = TypedDict(
    "AddFlowSourcesResponseTypeDef",
    {
        "FlowArn": str,
        "Sources": List[SourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFlowTypeDef = TypedDict(
    "_RequiredFlowTypeDef",
    {
        "AvailabilityZone": str,
        "Entitlements": List[EntitlementTypeDef],
        "FlowArn": str,
        "Name": str,
        "Outputs": List[OutputTypeDef],
        "Source": SourceTypeDef,
        "Status": StatusType,
    },
)
_OptionalFlowTypeDef = TypedDict(
    "_OptionalFlowTypeDef",
    {
        "Description": str,
        "EgressIp": str,
        "MediaStreams": List[MediaStreamTypeDef],
        "SourceFailoverConfig": FailoverConfigTypeDef,
        "Sources": List[SourceTypeDef],
        "VpcInterfaces": List[VpcInterfaceTypeDef],
        "Maintenance": MaintenanceTypeDef,
    },
    total=False,
)


class FlowTypeDef(_RequiredFlowTypeDef, _OptionalFlowTypeDef):
    pass


UpdateFlowSourceResponseTypeDef = TypedDict(
    "UpdateFlowSourceResponseTypeDef",
    {
        "FlowArn": str,
        "Source": SourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFlowResponseTypeDef = TypedDict(
    "CreateFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFlowResponseTypeDef = TypedDict(
    "DescribeFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "Messages": MessagesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFlowResponseTypeDef = TypedDict(
    "UpdateFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
