"""
Type annotations for cloudhsm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudhsm.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import ClientVersionType, CloudHsmObjectStateType, HsmStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateHapgRequestRequestTypeDef",
    "CreateHsmRequestRequestTypeDef",
    "CreateLunaClientRequestRequestTypeDef",
    "DeleteHapgRequestRequestTypeDef",
    "DeleteHsmRequestRequestTypeDef",
    "DeleteLunaClientRequestRequestTypeDef",
    "DescribeHapgRequestRequestTypeDef",
    "DescribeHsmRequestRequestTypeDef",
    "DescribeLunaClientRequestRequestTypeDef",
    "GetConfigRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListHapgsRequestRequestTypeDef",
    "ListHsmsRequestRequestTypeDef",
    "ListLunaClientsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ModifyHapgRequestRequestTypeDef",
    "ModifyHsmRequestRequestTypeDef",
    "ModifyLunaClientRequestRequestTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "AddTagsToResourceRequestRequestTypeDef",
    "AddTagsToResourceResponseTypeDef",
    "CreateHapgResponseTypeDef",
    "CreateHsmResponseTypeDef",
    "CreateLunaClientResponseTypeDef",
    "DeleteHapgResponseTypeDef",
    "DeleteHsmResponseTypeDef",
    "DeleteLunaClientResponseTypeDef",
    "DescribeHapgResponseTypeDef",
    "DescribeHsmResponseTypeDef",
    "DescribeLunaClientResponseTypeDef",
    "GetConfigResponseTypeDef",
    "ListAvailableZonesResponseTypeDef",
    "ListHapgsResponseTypeDef",
    "ListHsmsResponseTypeDef",
    "ListLunaClientsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyHapgResponseTypeDef",
    "ModifyHsmResponseTypeDef",
    "ModifyLunaClientResponseTypeDef",
    "RemoveTagsFromResourceResponseTypeDef",
    "ListHapgsRequestListHapgsPaginateTypeDef",
    "ListHsmsRequestListHsmsPaginateTypeDef",
    "ListLunaClientsRequestListLunaClientsPaginateTypeDef",
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

CreateHapgRequestRequestTypeDef = TypedDict(
    "CreateHapgRequestRequestTypeDef",
    {
        "Label": str,
    },
)

_RequiredCreateHsmRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHsmRequestRequestTypeDef",
    {
        "SubnetId": str,
        "SshKey": str,
        "IamRoleArn": str,
        "SubscriptionType": Literal["PRODUCTION"],
    },
)
_OptionalCreateHsmRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHsmRequestRequestTypeDef",
    {
        "EniIp": str,
        "ExternalId": str,
        "ClientToken": str,
        "SyslogIp": str,
    },
    total=False,
)

class CreateHsmRequestRequestTypeDef(
    _RequiredCreateHsmRequestRequestTypeDef, _OptionalCreateHsmRequestRequestTypeDef
):
    pass

_RequiredCreateLunaClientRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLunaClientRequestRequestTypeDef",
    {
        "Certificate": str,
    },
)
_OptionalCreateLunaClientRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLunaClientRequestRequestTypeDef",
    {
        "Label": str,
    },
    total=False,
)

class CreateLunaClientRequestRequestTypeDef(
    _RequiredCreateLunaClientRequestRequestTypeDef, _OptionalCreateLunaClientRequestRequestTypeDef
):
    pass

DeleteHapgRequestRequestTypeDef = TypedDict(
    "DeleteHapgRequestRequestTypeDef",
    {
        "HapgArn": str,
    },
)

DeleteHsmRequestRequestTypeDef = TypedDict(
    "DeleteHsmRequestRequestTypeDef",
    {
        "HsmArn": str,
    },
)

DeleteLunaClientRequestRequestTypeDef = TypedDict(
    "DeleteLunaClientRequestRequestTypeDef",
    {
        "ClientArn": str,
    },
)

DescribeHapgRequestRequestTypeDef = TypedDict(
    "DescribeHapgRequestRequestTypeDef",
    {
        "HapgArn": str,
    },
)

DescribeHsmRequestRequestTypeDef = TypedDict(
    "DescribeHsmRequestRequestTypeDef",
    {
        "HsmArn": str,
        "HsmSerialNumber": str,
    },
    total=False,
)

DescribeLunaClientRequestRequestTypeDef = TypedDict(
    "DescribeLunaClientRequestRequestTypeDef",
    {
        "ClientArn": str,
        "CertificateFingerprint": str,
    },
    total=False,
)

GetConfigRequestRequestTypeDef = TypedDict(
    "GetConfigRequestRequestTypeDef",
    {
        "ClientArn": str,
        "ClientVersion": ClientVersionType,
        "HapgList": Sequence[str],
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

ListHapgsRequestRequestTypeDef = TypedDict(
    "ListHapgsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListHsmsRequestRequestTypeDef = TypedDict(
    "ListHsmsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListLunaClientsRequestRequestTypeDef = TypedDict(
    "ListLunaClientsRequestRequestTypeDef",
    {
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

_RequiredModifyHapgRequestRequestTypeDef = TypedDict(
    "_RequiredModifyHapgRequestRequestTypeDef",
    {
        "HapgArn": str,
    },
)
_OptionalModifyHapgRequestRequestTypeDef = TypedDict(
    "_OptionalModifyHapgRequestRequestTypeDef",
    {
        "Label": str,
        "PartitionSerialList": Sequence[str],
    },
    total=False,
)

class ModifyHapgRequestRequestTypeDef(
    _RequiredModifyHapgRequestRequestTypeDef, _OptionalModifyHapgRequestRequestTypeDef
):
    pass

_RequiredModifyHsmRequestRequestTypeDef = TypedDict(
    "_RequiredModifyHsmRequestRequestTypeDef",
    {
        "HsmArn": str,
    },
)
_OptionalModifyHsmRequestRequestTypeDef = TypedDict(
    "_OptionalModifyHsmRequestRequestTypeDef",
    {
        "SubnetId": str,
        "EniIp": str,
        "IamRoleArn": str,
        "ExternalId": str,
        "SyslogIp": str,
    },
    total=False,
)

class ModifyHsmRequestRequestTypeDef(
    _RequiredModifyHsmRequestRequestTypeDef, _OptionalModifyHsmRequestRequestTypeDef
):
    pass

ModifyLunaClientRequestRequestTypeDef = TypedDict(
    "ModifyLunaClientRequestRequestTypeDef",
    {
        "ClientArn": str,
        "Certificate": str,
    },
)

RemoveTagsFromResourceRequestRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeyList": Sequence[str],
    },
)

AddTagsToResourceRequestRequestTypeDef = TypedDict(
    "AddTagsToResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagList": Sequence[TagTypeDef],
    },
)

AddTagsToResourceResponseTypeDef = TypedDict(
    "AddTagsToResourceResponseTypeDef",
    {
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHapgResponseTypeDef = TypedDict(
    "CreateHapgResponseTypeDef",
    {
        "HapgArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHsmResponseTypeDef = TypedDict(
    "CreateHsmResponseTypeDef",
    {
        "HsmArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLunaClientResponseTypeDef = TypedDict(
    "CreateLunaClientResponseTypeDef",
    {
        "ClientArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHapgResponseTypeDef = TypedDict(
    "DeleteHapgResponseTypeDef",
    {
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHsmResponseTypeDef = TypedDict(
    "DeleteHsmResponseTypeDef",
    {
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteLunaClientResponseTypeDef = TypedDict(
    "DeleteLunaClientResponseTypeDef",
    {
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHapgResponseTypeDef = TypedDict(
    "DescribeHapgResponseTypeDef",
    {
        "HapgArn": str,
        "HapgSerial": str,
        "HsmsLastActionFailed": List[str],
        "HsmsPendingDeletion": List[str],
        "HsmsPendingRegistration": List[str],
        "Label": str,
        "LastModifiedTimestamp": str,
        "PartitionSerialList": List[str],
        "State": CloudHsmObjectStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHsmResponseTypeDef = TypedDict(
    "DescribeHsmResponseTypeDef",
    {
        "HsmArn": str,
        "Status": HsmStatusType,
        "StatusDetails": str,
        "AvailabilityZone": str,
        "EniId": str,
        "EniIp": str,
        "SubscriptionType": Literal["PRODUCTION"],
        "SubscriptionStartDate": str,
        "SubscriptionEndDate": str,
        "VpcId": str,
        "SubnetId": str,
        "IamRoleArn": str,
        "SerialNumber": str,
        "VendorName": str,
        "HsmType": str,
        "SoftwareVersion": str,
        "SshPublicKey": str,
        "SshKeyLastUpdated": str,
        "ServerCertUri": str,
        "ServerCertLastUpdated": str,
        "Partitions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLunaClientResponseTypeDef = TypedDict(
    "DescribeLunaClientResponseTypeDef",
    {
        "ClientArn": str,
        "Certificate": str,
        "CertificateFingerprint": str,
        "LastModifiedTimestamp": str,
        "Label": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConfigResponseTypeDef = TypedDict(
    "GetConfigResponseTypeDef",
    {
        "ConfigType": str,
        "ConfigFile": str,
        "ConfigCred": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableZonesResponseTypeDef = TypedDict(
    "ListAvailableZonesResponseTypeDef",
    {
        "AZList": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHapgsResponseTypeDef = TypedDict(
    "ListHapgsResponseTypeDef",
    {
        "HapgList": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHsmsResponseTypeDef = TypedDict(
    "ListHsmsResponseTypeDef",
    {
        "HsmList": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLunaClientsResponseTypeDef = TypedDict(
    "ListLunaClientsResponseTypeDef",
    {
        "ClientList": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyHapgResponseTypeDef = TypedDict(
    "ModifyHapgResponseTypeDef",
    {
        "HapgArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyHsmResponseTypeDef = TypedDict(
    "ModifyHsmResponseTypeDef",
    {
        "HsmArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyLunaClientResponseTypeDef = TypedDict(
    "ModifyLunaClientResponseTypeDef",
    {
        "ClientArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveTagsFromResourceResponseTypeDef = TypedDict(
    "RemoveTagsFromResourceResponseTypeDef",
    {
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHapgsRequestListHapgsPaginateTypeDef = TypedDict(
    "ListHapgsRequestListHapgsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListHsmsRequestListHsmsPaginateTypeDef = TypedDict(
    "ListHsmsRequestListHsmsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListLunaClientsRequestListLunaClientsPaginateTypeDef = TypedDict(
    "ListLunaClientsRequestListLunaClientsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)
