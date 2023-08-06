"""
Type annotations for snowball service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snowball/type_defs/)

Usage::

    ```python
    from mypy_boto3_snowball.type_defs import AddressTypeDef

    data: AddressTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ClusterStateType,
    DeviceServiceNameType,
    JobStateType,
    JobTypeType,
    LongTermPricingTypeType,
    RemoteManagementType,
    ShipmentStateType,
    ShippingLabelStatusType,
    ShippingOptionType,
    SnowballCapacityType,
    SnowballTypeType,
    TransferOptionType,
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
    "AddressTypeDef",
    "CancelClusterRequestRequestTypeDef",
    "CancelJobRequestRequestTypeDef",
    "ClusterListEntryTypeDef",
    "NotificationTypeDef",
    "CompatibleImageTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLongTermPricingRequestRequestTypeDef",
    "CreateReturnShippingLabelRequestRequestTypeDef",
    "DataTransferTypeDef",
    "DescribeAddressRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAddressesRequestRequestTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeReturnShippingLabelRequestRequestTypeDef",
    "Ec2AmiResourceTypeDef",
    "EventTriggerDefinitionTypeDef",
    "GetJobManifestRequestRequestTypeDef",
    "GetJobUnlockCodeRequestRequestTypeDef",
    "GetSoftwareUpdatesRequestRequestTypeDef",
    "INDTaxDocumentsTypeDef",
    "JobListEntryTypeDef",
    "JobLogsTypeDef",
    "KeyRangeTypeDef",
    "ListClusterJobsRequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListCompatibleImagesRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListLongTermPricingRequestRequestTypeDef",
    "LongTermPricingListEntryTypeDef",
    "NFSOnDeviceServiceConfigurationTypeDef",
    "TGWOnDeviceServiceConfigurationTypeDef",
    "TargetOnDeviceServiceTypeDef",
    "ShipmentTypeDef",
    "WirelessConnectionTypeDef",
    "UpdateJobShipmentStateRequestRequestTypeDef",
    "UpdateLongTermPricingRequestRequestTypeDef",
    "CreateAddressRequestRequestTypeDef",
    "CreateAddressResultTypeDef",
    "CreateClusterResultTypeDef",
    "CreateJobResultTypeDef",
    "CreateLongTermPricingResultTypeDef",
    "CreateReturnShippingLabelResultTypeDef",
    "DescribeAddressResultTypeDef",
    "DescribeAddressesResultTypeDef",
    "DescribeReturnShippingLabelResultTypeDef",
    "GetJobManifestResultTypeDef",
    "GetJobUnlockCodeResultTypeDef",
    "GetSnowballUsageResultTypeDef",
    "GetSoftwareUpdatesResultTypeDef",
    "ListClustersResultTypeDef",
    "ListCompatibleImagesResultTypeDef",
    "DescribeAddressesRequestDescribeAddressesPaginateTypeDef",
    "ListClusterJobsRequestListClusterJobsPaginateTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "LambdaResourceTypeDef",
    "TaxDocumentsTypeDef",
    "ListClusterJobsResultTypeDef",
    "ListJobsResultTypeDef",
    "ListLongTermPricingResultTypeDef",
    "OnDeviceServiceConfigurationTypeDef",
    "S3ResourceTypeDef",
    "ShippingDetailsTypeDef",
    "SnowconeDeviceConfigurationTypeDef",
    "JobResourceTypeDef",
    "DeviceConfigurationTypeDef",
    "ClusterMetadataTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "CreateJobRequestRequestTypeDef",
    "JobMetadataTypeDef",
    "DescribeClusterResultTypeDef",
    "DescribeJobResultTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "AddressId": str,
        "Name": str,
        "Company": str,
        "Street1": str,
        "Street2": str,
        "Street3": str,
        "City": str,
        "StateOrProvince": str,
        "PrefectureOrDistrict": str,
        "Landmark": str,
        "Country": str,
        "PostalCode": str,
        "PhoneNumber": str,
        "IsRestricted": bool,
    },
    total=False,
)

CancelClusterRequestRequestTypeDef = TypedDict(
    "CancelClusterRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

ClusterListEntryTypeDef = TypedDict(
    "ClusterListEntryTypeDef",
    {
        "ClusterId": str,
        "ClusterState": ClusterStateType,
        "CreationDate": datetime,
        "Description": str,
    },
    total=False,
)

NotificationTypeDef = TypedDict(
    "NotificationTypeDef",
    {
        "SnsTopicARN": str,
        "JobStatesToNotify": Sequence[JobStateType],
        "NotifyAll": bool,
    },
    total=False,
)

CompatibleImageTypeDef = TypedDict(
    "CompatibleImageTypeDef",
    {
        "AmiId": str,
        "Name": str,
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

_RequiredCreateLongTermPricingRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLongTermPricingRequestRequestTypeDef",
    {
        "LongTermPricingType": LongTermPricingTypeType,
    },
)
_OptionalCreateLongTermPricingRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLongTermPricingRequestRequestTypeDef",
    {
        "IsLongTermPricingAutoRenew": bool,
        "SnowballType": SnowballTypeType,
    },
    total=False,
)


class CreateLongTermPricingRequestRequestTypeDef(
    _RequiredCreateLongTermPricingRequestRequestTypeDef,
    _OptionalCreateLongTermPricingRequestRequestTypeDef,
):
    pass


_RequiredCreateReturnShippingLabelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReturnShippingLabelRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalCreateReturnShippingLabelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReturnShippingLabelRequestRequestTypeDef",
    {
        "ShippingOption": ShippingOptionType,
    },
    total=False,
)


class CreateReturnShippingLabelRequestRequestTypeDef(
    _RequiredCreateReturnShippingLabelRequestRequestTypeDef,
    _OptionalCreateReturnShippingLabelRequestRequestTypeDef,
):
    pass


DataTransferTypeDef = TypedDict(
    "DataTransferTypeDef",
    {
        "BytesTransferred": int,
        "ObjectsTransferred": int,
        "TotalBytes": int,
        "TotalObjects": int,
    },
    total=False,
)

DescribeAddressRequestRequestTypeDef = TypedDict(
    "DescribeAddressRequestRequestTypeDef",
    {
        "AddressId": str,
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

DescribeAddressesRequestRequestTypeDef = TypedDict(
    "DescribeAddressesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeClusterRequestRequestTypeDef = TypedDict(
    "DescribeClusterRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)

DescribeJobRequestRequestTypeDef = TypedDict(
    "DescribeJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeReturnShippingLabelRequestRequestTypeDef = TypedDict(
    "DescribeReturnShippingLabelRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

_RequiredEc2AmiResourceTypeDef = TypedDict(
    "_RequiredEc2AmiResourceTypeDef",
    {
        "AmiId": str,
    },
)
_OptionalEc2AmiResourceTypeDef = TypedDict(
    "_OptionalEc2AmiResourceTypeDef",
    {
        "SnowballAmiId": str,
    },
    total=False,
)


class Ec2AmiResourceTypeDef(_RequiredEc2AmiResourceTypeDef, _OptionalEc2AmiResourceTypeDef):
    pass


EventTriggerDefinitionTypeDef = TypedDict(
    "EventTriggerDefinitionTypeDef",
    {
        "EventResourceARN": str,
    },
    total=False,
)

GetJobManifestRequestRequestTypeDef = TypedDict(
    "GetJobManifestRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetJobUnlockCodeRequestRequestTypeDef = TypedDict(
    "GetJobUnlockCodeRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetSoftwareUpdatesRequestRequestTypeDef = TypedDict(
    "GetSoftwareUpdatesRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

INDTaxDocumentsTypeDef = TypedDict(
    "INDTaxDocumentsTypeDef",
    {
        "GSTIN": str,
    },
    total=False,
)

JobListEntryTypeDef = TypedDict(
    "JobListEntryTypeDef",
    {
        "JobId": str,
        "JobState": JobStateType,
        "IsMaster": bool,
        "JobType": JobTypeType,
        "SnowballType": SnowballTypeType,
        "CreationDate": datetime,
        "Description": str,
    },
    total=False,
)

JobLogsTypeDef = TypedDict(
    "JobLogsTypeDef",
    {
        "JobCompletionReportURI": str,
        "JobSuccessLogURI": str,
        "JobFailureLogURI": str,
    },
    total=False,
)

KeyRangeTypeDef = TypedDict(
    "KeyRangeTypeDef",
    {
        "BeginMarker": str,
        "EndMarker": str,
    },
    total=False,
)

_RequiredListClusterJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListClusterJobsRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListClusterJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListClusterJobsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListClusterJobsRequestRequestTypeDef(
    _RequiredListClusterJobsRequestRequestTypeDef, _OptionalListClusterJobsRequestRequestTypeDef
):
    pass


ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListCompatibleImagesRequestRequestTypeDef = TypedDict(
    "ListCompatibleImagesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListLongTermPricingRequestRequestTypeDef = TypedDict(
    "ListLongTermPricingRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

LongTermPricingListEntryTypeDef = TypedDict(
    "LongTermPricingListEntryTypeDef",
    {
        "LongTermPricingId": str,
        "LongTermPricingEndDate": datetime,
        "LongTermPricingStartDate": datetime,
        "LongTermPricingType": LongTermPricingTypeType,
        "CurrentActiveJob": str,
        "ReplacementJob": str,
        "IsLongTermPricingAutoRenew": bool,
        "LongTermPricingStatus": str,
        "SnowballType": SnowballTypeType,
        "JobIds": List[str],
    },
    total=False,
)

NFSOnDeviceServiceConfigurationTypeDef = TypedDict(
    "NFSOnDeviceServiceConfigurationTypeDef",
    {
        "StorageLimit": int,
        "StorageUnit": Literal["TB"],
    },
    total=False,
)

TGWOnDeviceServiceConfigurationTypeDef = TypedDict(
    "TGWOnDeviceServiceConfigurationTypeDef",
    {
        "StorageLimit": int,
        "StorageUnit": Literal["TB"],
    },
    total=False,
)

TargetOnDeviceServiceTypeDef = TypedDict(
    "TargetOnDeviceServiceTypeDef",
    {
        "ServiceName": DeviceServiceNameType,
        "TransferOption": TransferOptionType,
    },
    total=False,
)

ShipmentTypeDef = TypedDict(
    "ShipmentTypeDef",
    {
        "Status": str,
        "TrackingNumber": str,
    },
    total=False,
)

WirelessConnectionTypeDef = TypedDict(
    "WirelessConnectionTypeDef",
    {
        "IsWifiEnabled": bool,
    },
    total=False,
)

UpdateJobShipmentStateRequestRequestTypeDef = TypedDict(
    "UpdateJobShipmentStateRequestRequestTypeDef",
    {
        "JobId": str,
        "ShipmentState": ShipmentStateType,
    },
)

_RequiredUpdateLongTermPricingRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLongTermPricingRequestRequestTypeDef",
    {
        "LongTermPricingId": str,
    },
)
_OptionalUpdateLongTermPricingRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLongTermPricingRequestRequestTypeDef",
    {
        "ReplacementJob": str,
        "IsLongTermPricingAutoRenew": bool,
    },
    total=False,
)


class UpdateLongTermPricingRequestRequestTypeDef(
    _RequiredUpdateLongTermPricingRequestRequestTypeDef,
    _OptionalUpdateLongTermPricingRequestRequestTypeDef,
):
    pass


CreateAddressRequestRequestTypeDef = TypedDict(
    "CreateAddressRequestRequestTypeDef",
    {
        "Address": AddressTypeDef,
    },
)

CreateAddressResultTypeDef = TypedDict(
    "CreateAddressResultTypeDef",
    {
        "AddressId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResultTypeDef = TypedDict(
    "CreateClusterResultTypeDef",
    {
        "ClusterId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobResultTypeDef = TypedDict(
    "CreateJobResultTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLongTermPricingResultTypeDef = TypedDict(
    "CreateLongTermPricingResultTypeDef",
    {
        "LongTermPricingId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateReturnShippingLabelResultTypeDef = TypedDict(
    "CreateReturnShippingLabelResultTypeDef",
    {
        "Status": ShippingLabelStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddressResultTypeDef = TypedDict(
    "DescribeAddressResultTypeDef",
    {
        "Address": AddressTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddressesResultTypeDef = TypedDict(
    "DescribeAddressesResultTypeDef",
    {
        "Addresses": List[AddressTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeReturnShippingLabelResultTypeDef = TypedDict(
    "DescribeReturnShippingLabelResultTypeDef",
    {
        "Status": ShippingLabelStatusType,
        "ExpirationDate": datetime,
        "ReturnShippingLabelURI": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobManifestResultTypeDef = TypedDict(
    "GetJobManifestResultTypeDef",
    {
        "ManifestURI": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobUnlockCodeResultTypeDef = TypedDict(
    "GetJobUnlockCodeResultTypeDef",
    {
        "UnlockCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSnowballUsageResultTypeDef = TypedDict(
    "GetSnowballUsageResultTypeDef",
    {
        "SnowballLimit": int,
        "SnowballsInUse": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSoftwareUpdatesResultTypeDef = TypedDict(
    "GetSoftwareUpdatesResultTypeDef",
    {
        "UpdatesURI": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResultTypeDef = TypedDict(
    "ListClustersResultTypeDef",
    {
        "ClusterListEntries": List[ClusterListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCompatibleImagesResultTypeDef = TypedDict(
    "ListCompatibleImagesResultTypeDef",
    {
        "CompatibleImages": List[CompatibleImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddressesRequestDescribeAddressesPaginateTypeDef = TypedDict(
    "DescribeAddressesRequestDescribeAddressesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListClusterJobsRequestListClusterJobsPaginateTypeDef = TypedDict(
    "_RequiredListClusterJobsRequestListClusterJobsPaginateTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalListClusterJobsRequestListClusterJobsPaginateTypeDef = TypedDict(
    "_OptionalListClusterJobsRequestListClusterJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListClusterJobsRequestListClusterJobsPaginateTypeDef(
    _RequiredListClusterJobsRequestListClusterJobsPaginateTypeDef,
    _OptionalListClusterJobsRequestListClusterJobsPaginateTypeDef,
):
    pass


ListClustersRequestListClustersPaginateTypeDef = TypedDict(
    "ListClustersRequestListClustersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef = TypedDict(
    "ListCompatibleImagesRequestListCompatibleImagesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

LambdaResourceTypeDef = TypedDict(
    "LambdaResourceTypeDef",
    {
        "LambdaArn": str,
        "EventTriggers": Sequence[EventTriggerDefinitionTypeDef],
    },
    total=False,
)

TaxDocumentsTypeDef = TypedDict(
    "TaxDocumentsTypeDef",
    {
        "IND": INDTaxDocumentsTypeDef,
    },
    total=False,
)

ListClusterJobsResultTypeDef = TypedDict(
    "ListClusterJobsResultTypeDef",
    {
        "JobListEntries": List[JobListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "JobListEntries": List[JobListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLongTermPricingResultTypeDef = TypedDict(
    "ListLongTermPricingResultTypeDef",
    {
        "LongTermPricingEntries": List[LongTermPricingListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OnDeviceServiceConfigurationTypeDef = TypedDict(
    "OnDeviceServiceConfigurationTypeDef",
    {
        "NFSOnDeviceService": NFSOnDeviceServiceConfigurationTypeDef,
        "TGWOnDeviceService": TGWOnDeviceServiceConfigurationTypeDef,
    },
    total=False,
)

S3ResourceTypeDef = TypedDict(
    "S3ResourceTypeDef",
    {
        "BucketArn": str,
        "KeyRange": KeyRangeTypeDef,
        "TargetOnDeviceServices": Sequence[TargetOnDeviceServiceTypeDef],
    },
    total=False,
)

ShippingDetailsTypeDef = TypedDict(
    "ShippingDetailsTypeDef",
    {
        "ShippingOption": ShippingOptionType,
        "InboundShipment": ShipmentTypeDef,
        "OutboundShipment": ShipmentTypeDef,
    },
    total=False,
)

SnowconeDeviceConfigurationTypeDef = TypedDict(
    "SnowconeDeviceConfigurationTypeDef",
    {
        "WirelessConnection": WirelessConnectionTypeDef,
    },
    total=False,
)

JobResourceTypeDef = TypedDict(
    "JobResourceTypeDef",
    {
        "S3Resources": Sequence[S3ResourceTypeDef],
        "LambdaResources": Sequence[LambdaResourceTypeDef],
        "Ec2AmiResources": Sequence[Ec2AmiResourceTypeDef],
    },
    total=False,
)

DeviceConfigurationTypeDef = TypedDict(
    "DeviceConfigurationTypeDef",
    {
        "SnowconeDeviceConfiguration": SnowconeDeviceConfigurationTypeDef,
    },
    total=False,
)

ClusterMetadataTypeDef = TypedDict(
    "ClusterMetadataTypeDef",
    {
        "ClusterId": str,
        "Description": str,
        "KmsKeyARN": str,
        "RoleARN": str,
        "ClusterState": ClusterStateType,
        "JobType": JobTypeType,
        "SnowballType": SnowballTypeType,
        "CreationDate": datetime,
        "Resources": JobResourceTypeDef,
        "AddressId": str,
        "ShippingOption": ShippingOptionType,
        "Notification": NotificationTypeDef,
        "ForwardingAddressId": str,
        "TaxDocuments": TaxDocumentsTypeDef,
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "JobType": JobTypeType,
        "Resources": JobResourceTypeDef,
        "AddressId": str,
        "RoleARN": str,
        "SnowballType": SnowballTypeType,
        "ShippingOption": ShippingOptionType,
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
        "Description": str,
        "KmsKeyARN": str,
        "Notification": NotificationTypeDef,
        "ForwardingAddressId": str,
        "TaxDocuments": TaxDocumentsTypeDef,
        "RemoteManagement": RemoteManagementType,
    },
    total=False,
)


class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
):
    pass


_RequiredUpdateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterRequestRequestTypeDef",
    {
        "ClusterId": str,
    },
)
_OptionalUpdateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterRequestRequestTypeDef",
    {
        "RoleARN": str,
        "Description": str,
        "Resources": JobResourceTypeDef,
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
        "AddressId": str,
        "ShippingOption": ShippingOptionType,
        "Notification": NotificationTypeDef,
        "ForwardingAddressId": str,
    },
    total=False,
)


class UpdateClusterRequestRequestTypeDef(
    _RequiredUpdateClusterRequestRequestTypeDef, _OptionalUpdateClusterRequestRequestTypeDef
):
    pass


_RequiredUpdateJobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalUpdateJobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobRequestRequestTypeDef",
    {
        "RoleARN": str,
        "Notification": NotificationTypeDef,
        "Resources": JobResourceTypeDef,
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
        "AddressId": str,
        "ShippingOption": ShippingOptionType,
        "Description": str,
        "SnowballCapacityPreference": SnowballCapacityType,
        "ForwardingAddressId": str,
    },
    total=False,
)


class UpdateJobRequestRequestTypeDef(
    _RequiredUpdateJobRequestRequestTypeDef, _OptionalUpdateJobRequestRequestTypeDef
):
    pass


CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "JobType": JobTypeType,
        "Resources": JobResourceTypeDef,
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
        "Description": str,
        "AddressId": str,
        "KmsKeyARN": str,
        "RoleARN": str,
        "SnowballCapacityPreference": SnowballCapacityType,
        "ShippingOption": ShippingOptionType,
        "Notification": NotificationTypeDef,
        "ClusterId": str,
        "SnowballType": SnowballTypeType,
        "ForwardingAddressId": str,
        "TaxDocuments": TaxDocumentsTypeDef,
        "DeviceConfiguration": DeviceConfigurationTypeDef,
        "RemoteManagement": RemoteManagementType,
        "LongTermPricingId": str,
    },
    total=False,
)

JobMetadataTypeDef = TypedDict(
    "JobMetadataTypeDef",
    {
        "JobId": str,
        "JobState": JobStateType,
        "JobType": JobTypeType,
        "SnowballType": SnowballTypeType,
        "CreationDate": datetime,
        "Resources": JobResourceTypeDef,
        "Description": str,
        "KmsKeyARN": str,
        "RoleARN": str,
        "AddressId": str,
        "ShippingDetails": ShippingDetailsTypeDef,
        "SnowballCapacityPreference": SnowballCapacityType,
        "Notification": NotificationTypeDef,
        "DataTransferProgress": DataTransferTypeDef,
        "JobLogInfo": JobLogsTypeDef,
        "ClusterId": str,
        "ForwardingAddressId": str,
        "TaxDocuments": TaxDocumentsTypeDef,
        "DeviceConfiguration": DeviceConfigurationTypeDef,
        "RemoteManagement": RemoteManagementType,
        "LongTermPricingId": str,
        "OnDeviceServiceConfiguration": OnDeviceServiceConfigurationTypeDef,
    },
    total=False,
)

DescribeClusterResultTypeDef = TypedDict(
    "DescribeClusterResultTypeDef",
    {
        "ClusterMetadata": ClusterMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeJobResultTypeDef = TypedDict(
    "DescribeJobResultTypeDef",
    {
        "JobMetadata": JobMetadataTypeDef,
        "SubJobMetadata": List[JobMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
