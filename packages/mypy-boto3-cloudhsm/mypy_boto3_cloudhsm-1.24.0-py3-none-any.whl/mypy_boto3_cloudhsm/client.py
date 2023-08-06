"""
Type annotations for cloudhsm service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudhsm.client import CloudHSMClient

    session = Session()
    client: CloudHSMClient = session.client("cloudhsm")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ClientVersionType
from .paginator import ListHapgsPaginator, ListHsmsPaginator, ListLunaClientsPaginator
from .type_defs import (
    AddTagsToResourceResponseTypeDef,
    CreateHapgResponseTypeDef,
    CreateHsmResponseTypeDef,
    CreateLunaClientResponseTypeDef,
    DeleteHapgResponseTypeDef,
    DeleteHsmResponseTypeDef,
    DeleteLunaClientResponseTypeDef,
    DescribeHapgResponseTypeDef,
    DescribeHsmResponseTypeDef,
    DescribeLunaClientResponseTypeDef,
    GetConfigResponseTypeDef,
    ListAvailableZonesResponseTypeDef,
    ListHapgsResponseTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyHapgResponseTypeDef,
    ModifyHsmResponseTypeDef,
    ModifyLunaClientResponseTypeDef,
    RemoveTagsFromResourceResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudHSMClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CloudHsmInternalException: Type[BotocoreClientError]
    CloudHsmServiceException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]


class CloudHSMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudHSMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#exceptions)
        """

    def add_tags_to_resource(
        self, *, ResourceArn: str, TagList: Sequence[TagTypeDef]
    ) -> AddTagsToResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.add_tags_to_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#add_tags_to_resource)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#can_paginate)
        """

    def create_hapg(self, *, Label: str) -> CreateHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_hapg)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#create_hapg)
        """

    def create_hsm(
        self,
        *,
        SubnetId: str,
        SshKey: str,
        IamRoleArn: str,
        SubscriptionType: Literal["PRODUCTION"],
        EniIp: str = ...,
        ExternalId: str = ...,
        ClientToken: str = ...,
        SyslogIp: str = ...
    ) -> CreateHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_hsm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#create_hsm)
        """

    def create_luna_client(
        self, *, Certificate: str, Label: str = ...
    ) -> CreateLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_luna_client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#create_luna_client)
        """

    def delete_hapg(self, *, HapgArn: str) -> DeleteHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_hapg)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#delete_hapg)
        """

    def delete_hsm(self, *, HsmArn: str) -> DeleteHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_hsm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#delete_hsm)
        """

    def delete_luna_client(self, *, ClientArn: str) -> DeleteLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_luna_client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#delete_luna_client)
        """

    def describe_hapg(self, *, HapgArn: str) -> DescribeHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_hapg)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#describe_hapg)
        """

    def describe_hsm(
        self, *, HsmArn: str = ..., HsmSerialNumber: str = ...
    ) -> DescribeHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_hsm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#describe_hsm)
        """

    def describe_luna_client(
        self, *, ClientArn: str = ..., CertificateFingerprint: str = ...
    ) -> DescribeLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_luna_client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#describe_luna_client)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#generate_presigned_url)
        """

    def get_config(
        self, *, ClientArn: str, ClientVersion: ClientVersionType, HapgList: Sequence[str]
    ) -> GetConfigResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#get_config)
        """

    def list_available_zones(self) -> ListAvailableZonesResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_available_zones)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#list_available_zones)
        """

    def list_hapgs(self, *, NextToken: str = ...) -> ListHapgsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_hapgs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#list_hapgs)
        """

    def list_hsms(self, *, NextToken: str = ...) -> ListHsmsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_hsms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#list_hsms)
        """

    def list_luna_clients(self, *, NextToken: str = ...) -> ListLunaClientsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_luna_clients)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#list_luna_clients)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#list_tags_for_resource)
        """

    def modify_hapg(
        self, *, HapgArn: str, Label: str = ..., PartitionSerialList: Sequence[str] = ...
    ) -> ModifyHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_hapg)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#modify_hapg)
        """

    def modify_hsm(
        self,
        *,
        HsmArn: str,
        SubnetId: str = ...,
        EniIp: str = ...,
        IamRoleArn: str = ...,
        ExternalId: str = ...,
        SyslogIp: str = ...
    ) -> ModifyHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_hsm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#modify_hsm)
        """

    def modify_luna_client(
        self, *, ClientArn: str, Certificate: str
    ) -> ModifyLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_luna_client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#modify_luna_client)
        """

    def remove_tags_from_resource(
        self, *, ResourceArn: str, TagKeyList: Sequence[str]
    ) -> RemoveTagsFromResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.remove_tags_from_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#remove_tags_from_resource)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hapgs"]) -> ListHapgsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hsms"]) -> ListHsmsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_luna_clients"]
    ) -> ListLunaClientsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/client/#get_paginator)
        """
