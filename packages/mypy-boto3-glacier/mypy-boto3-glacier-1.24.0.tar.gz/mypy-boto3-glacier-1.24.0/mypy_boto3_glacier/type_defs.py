"""
Type annotations for glacier service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/type_defs/)

Usage::

    ```python
    from mypy_boto3_glacier.type_defs import AbortMultipartUploadInputRequestTypeDef

    data: AbortMultipartUploadInputRequestTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ActionCodeType,
    CannedACLType,
    EncryptionTypeType,
    FileHeaderInfoType,
    PermissionType,
    QuoteFieldsType,
    StatusCodeType,
    StorageClassType,
    TypeType,
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
    "AbortMultipartUploadInputRequestTypeDef",
    "AbortVaultLockInputRequestTypeDef",
    "AccountVaultRequestTypeDef",
    "AddTagsToVaultInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CSVInputTypeDef",
    "CSVOutputTypeDef",
    "CompleteMultipartUploadInputMultipartUploadCompleteTypeDef",
    "CompleteMultipartUploadInputRequestTypeDef",
    "CompleteVaultLockInputRequestTypeDef",
    "CreateVaultInputAccountCreateVaultTypeDef",
    "CreateVaultInputRequestTypeDef",
    "CreateVaultInputServiceResourceCreateVaultTypeDef",
    "DataRetrievalRuleTypeDef",
    "DeleteArchiveInputRequestTypeDef",
    "DeleteVaultAccessPolicyInputRequestTypeDef",
    "DeleteVaultInputRequestTypeDef",
    "DeleteVaultNotificationsInputRequestTypeDef",
    "DescribeJobInputRequestTypeDef",
    "DescribeVaultInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeVaultOutputTypeDef",
    "EncryptionTypeDef",
    "GetDataRetrievalPolicyInputRequestTypeDef",
    "GetJobOutputInputJobGetOutputTypeDef",
    "GetJobOutputInputRequestTypeDef",
    "GetVaultAccessPolicyInputRequestTypeDef",
    "VaultAccessPolicyTypeDef",
    "GetVaultLockInputRequestTypeDef",
    "GetVaultNotificationsInputRequestTypeDef",
    "VaultNotificationConfigTypeDef",
    "InventoryRetrievalJobDescriptionTypeDef",
    "GranteeTypeDef",
    "InitiateMultipartUploadInputRequestTypeDef",
    "InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef",
    "VaultLockPolicyTypeDef",
    "InventoryRetrievalJobInputTypeDef",
    "PaginatorConfigTypeDef",
    "ListJobsInputRequestTypeDef",
    "ListMultipartUploadsInputRequestTypeDef",
    "UploadListElementTypeDef",
    "ListPartsInputMultipartUploadPartsTypeDef",
    "ListPartsInputRequestTypeDef",
    "PartListElementTypeDef",
    "ListProvisionedCapacityInputRequestTypeDef",
    "ProvisionedCapacityDescriptionTypeDef",
    "ListTagsForVaultInputRequestTypeDef",
    "ListVaultsInputRequestTypeDef",
    "PurchaseProvisionedCapacityInputRequestTypeDef",
    "RemoveTagsFromVaultInputRequestTypeDef",
    "ServiceResourceAccountRequestTypeDef",
    "ServiceResourceArchiveRequestTypeDef",
    "ServiceResourceJobRequestTypeDef",
    "ServiceResourceMultipartUploadRequestTypeDef",
    "ServiceResourceNotificationRequestTypeDef",
    "ServiceResourceVaultRequestTypeDef",
    "UploadArchiveInputRequestTypeDef",
    "UploadArchiveInputVaultUploadArchiveTypeDef",
    "UploadMultipartPartInputMultipartUploadUploadPartTypeDef",
    "UploadMultipartPartInputRequestTypeDef",
    "VaultArchiveRequestTypeDef",
    "VaultJobRequestTypeDef",
    "VaultMultipartUploadRequestTypeDef",
    "ArchiveCreationOutputTypeDef",
    "CreateVaultOutputTypeDef",
    "DescribeVaultOutputResponseMetadataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetJobOutputOutputTypeDef",
    "GetVaultLockOutputTypeDef",
    "InitiateJobOutputTypeDef",
    "InitiateMultipartUploadOutputTypeDef",
    "InitiateVaultLockOutputTypeDef",
    "InventoryRetrievalJobDescriptionResponseMetadataTypeDef",
    "ListTagsForVaultOutputTypeDef",
    "PurchaseProvisionedCapacityOutputTypeDef",
    "UploadMultipartPartOutputTypeDef",
    "InputSerializationTypeDef",
    "OutputSerializationTypeDef",
    "DataRetrievalPolicyTypeDef",
    "DescribeVaultInputVaultExistsWaitTypeDef",
    "DescribeVaultInputVaultNotExistsWaitTypeDef",
    "ListVaultsOutputTypeDef",
    "GetVaultAccessPolicyOutputTypeDef",
    "SetVaultAccessPolicyInputRequestTypeDef",
    "GetVaultNotificationsOutputTypeDef",
    "SetVaultNotificationsInputNotificationSetTypeDef",
    "SetVaultNotificationsInputRequestTypeDef",
    "GrantTypeDef",
    "InitiateVaultLockInputRequestTypeDef",
    "ListJobsInputListJobsPaginateTypeDef",
    "ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef",
    "ListPartsInputListPartsPaginateTypeDef",
    "ListVaultsInputListVaultsPaginateTypeDef",
    "ListMultipartUploadsOutputTypeDef",
    "ListPartsOutputTypeDef",
    "ListProvisionedCapacityOutputTypeDef",
    "SelectParametersResponseMetadataTypeDef",
    "SelectParametersTypeDef",
    "GetDataRetrievalPolicyOutputTypeDef",
    "SetDataRetrievalPolicyInputRequestTypeDef",
    "S3LocationTypeDef",
    "OutputLocationResponseMetadataTypeDef",
    "OutputLocationTypeDef",
    "GlacierJobDescriptionResponseMetadataTypeDef",
    "GlacierJobDescriptionTypeDef",
    "JobParametersTypeDef",
    "ListJobsOutputTypeDef",
    "InitiateJobInputRequestTypeDef",
)

_RequiredAbortMultipartUploadInputRequestTypeDef = TypedDict(
    "_RequiredAbortMultipartUploadInputRequestTypeDef",
    {
        "vaultName": str,
        "uploadId": str,
    },
)
_OptionalAbortMultipartUploadInputRequestTypeDef = TypedDict(
    "_OptionalAbortMultipartUploadInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class AbortMultipartUploadInputRequestTypeDef(
    _RequiredAbortMultipartUploadInputRequestTypeDef,
    _OptionalAbortMultipartUploadInputRequestTypeDef,
):
    pass


_RequiredAbortVaultLockInputRequestTypeDef = TypedDict(
    "_RequiredAbortVaultLockInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalAbortVaultLockInputRequestTypeDef = TypedDict(
    "_OptionalAbortVaultLockInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class AbortVaultLockInputRequestTypeDef(
    _RequiredAbortVaultLockInputRequestTypeDef, _OptionalAbortVaultLockInputRequestTypeDef
):
    pass


AccountVaultRequestTypeDef = TypedDict(
    "AccountVaultRequestTypeDef",
    {
        "name": str,
    },
)

_RequiredAddTagsToVaultInputRequestTypeDef = TypedDict(
    "_RequiredAddTagsToVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalAddTagsToVaultInputRequestTypeDef = TypedDict(
    "_OptionalAddTagsToVaultInputRequestTypeDef",
    {
        "accountId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class AddTagsToVaultInputRequestTypeDef(
    _RequiredAddTagsToVaultInputRequestTypeDef, _OptionalAddTagsToVaultInputRequestTypeDef
):
    pass


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

CSVInputTypeDef = TypedDict(
    "CSVInputTypeDef",
    {
        "FileHeaderInfo": FileHeaderInfoType,
        "Comments": str,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
    },
    total=False,
)

CSVOutputTypeDef = TypedDict(
    "CSVOutputTypeDef",
    {
        "QuoteFields": QuoteFieldsType,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
    },
    total=False,
)

CompleteMultipartUploadInputMultipartUploadCompleteTypeDef = TypedDict(
    "CompleteMultipartUploadInputMultipartUploadCompleteTypeDef",
    {
        "archiveSize": str,
        "checksum": str,
    },
    total=False,
)

_RequiredCompleteMultipartUploadInputRequestTypeDef = TypedDict(
    "_RequiredCompleteMultipartUploadInputRequestTypeDef",
    {
        "vaultName": str,
        "uploadId": str,
    },
)
_OptionalCompleteMultipartUploadInputRequestTypeDef = TypedDict(
    "_OptionalCompleteMultipartUploadInputRequestTypeDef",
    {
        "accountId": str,
        "archiveSize": str,
        "checksum": str,
    },
    total=False,
)


class CompleteMultipartUploadInputRequestTypeDef(
    _RequiredCompleteMultipartUploadInputRequestTypeDef,
    _OptionalCompleteMultipartUploadInputRequestTypeDef,
):
    pass


_RequiredCompleteVaultLockInputRequestTypeDef = TypedDict(
    "_RequiredCompleteVaultLockInputRequestTypeDef",
    {
        "vaultName": str,
        "lockId": str,
    },
)
_OptionalCompleteVaultLockInputRequestTypeDef = TypedDict(
    "_OptionalCompleteVaultLockInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class CompleteVaultLockInputRequestTypeDef(
    _RequiredCompleteVaultLockInputRequestTypeDef, _OptionalCompleteVaultLockInputRequestTypeDef
):
    pass


CreateVaultInputAccountCreateVaultTypeDef = TypedDict(
    "CreateVaultInputAccountCreateVaultTypeDef",
    {
        "vaultName": str,
    },
)

_RequiredCreateVaultInputRequestTypeDef = TypedDict(
    "_RequiredCreateVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalCreateVaultInputRequestTypeDef = TypedDict(
    "_OptionalCreateVaultInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class CreateVaultInputRequestTypeDef(
    _RequiredCreateVaultInputRequestTypeDef, _OptionalCreateVaultInputRequestTypeDef
):
    pass


_RequiredCreateVaultInputServiceResourceCreateVaultTypeDef = TypedDict(
    "_RequiredCreateVaultInputServiceResourceCreateVaultTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalCreateVaultInputServiceResourceCreateVaultTypeDef = TypedDict(
    "_OptionalCreateVaultInputServiceResourceCreateVaultTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class CreateVaultInputServiceResourceCreateVaultTypeDef(
    _RequiredCreateVaultInputServiceResourceCreateVaultTypeDef,
    _OptionalCreateVaultInputServiceResourceCreateVaultTypeDef,
):
    pass


DataRetrievalRuleTypeDef = TypedDict(
    "DataRetrievalRuleTypeDef",
    {
        "Strategy": str,
        "BytesPerHour": int,
    },
    total=False,
)

_RequiredDeleteArchiveInputRequestTypeDef = TypedDict(
    "_RequiredDeleteArchiveInputRequestTypeDef",
    {
        "vaultName": str,
        "archiveId": str,
    },
)
_OptionalDeleteArchiveInputRequestTypeDef = TypedDict(
    "_OptionalDeleteArchiveInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DeleteArchiveInputRequestTypeDef(
    _RequiredDeleteArchiveInputRequestTypeDef, _OptionalDeleteArchiveInputRequestTypeDef
):
    pass


_RequiredDeleteVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVaultAccessPolicyInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalDeleteVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVaultAccessPolicyInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DeleteVaultAccessPolicyInputRequestTypeDef(
    _RequiredDeleteVaultAccessPolicyInputRequestTypeDef,
    _OptionalDeleteVaultAccessPolicyInputRequestTypeDef,
):
    pass


_RequiredDeleteVaultInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalDeleteVaultInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVaultInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DeleteVaultInputRequestTypeDef(
    _RequiredDeleteVaultInputRequestTypeDef, _OptionalDeleteVaultInputRequestTypeDef
):
    pass


_RequiredDeleteVaultNotificationsInputRequestTypeDef = TypedDict(
    "_RequiredDeleteVaultNotificationsInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalDeleteVaultNotificationsInputRequestTypeDef = TypedDict(
    "_OptionalDeleteVaultNotificationsInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DeleteVaultNotificationsInputRequestTypeDef(
    _RequiredDeleteVaultNotificationsInputRequestTypeDef,
    _OptionalDeleteVaultNotificationsInputRequestTypeDef,
):
    pass


_RequiredDescribeJobInputRequestTypeDef = TypedDict(
    "_RequiredDescribeJobInputRequestTypeDef",
    {
        "vaultName": str,
        "jobId": str,
    },
)
_OptionalDescribeJobInputRequestTypeDef = TypedDict(
    "_OptionalDescribeJobInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DescribeJobInputRequestTypeDef(
    _RequiredDescribeJobInputRequestTypeDef, _OptionalDescribeJobInputRequestTypeDef
):
    pass


_RequiredDescribeVaultInputRequestTypeDef = TypedDict(
    "_RequiredDescribeVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalDescribeVaultInputRequestTypeDef = TypedDict(
    "_OptionalDescribeVaultInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class DescribeVaultInputRequestTypeDef(
    _RequiredDescribeVaultInputRequestTypeDef, _OptionalDescribeVaultInputRequestTypeDef
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeVaultOutputTypeDef = TypedDict(
    "DescribeVaultOutputTypeDef",
    {
        "VaultARN": str,
        "VaultName": str,
        "CreationDate": str,
        "LastInventoryDate": str,
        "NumberOfArchives": int,
        "SizeInBytes": int,
    },
    total=False,
)

EncryptionTypeDef = TypedDict(
    "EncryptionTypeDef",
    {
        "EncryptionType": EncryptionTypeType,
        "KMSKeyId": str,
        "KMSContext": str,
    },
    total=False,
)

GetDataRetrievalPolicyInputRequestTypeDef = TypedDict(
    "GetDataRetrievalPolicyInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)

GetJobOutputInputJobGetOutputTypeDef = TypedDict(
    "GetJobOutputInputJobGetOutputTypeDef",
    {
        "range": str,
    },
    total=False,
)

_RequiredGetJobOutputInputRequestTypeDef = TypedDict(
    "_RequiredGetJobOutputInputRequestTypeDef",
    {
        "vaultName": str,
        "jobId": str,
    },
)
_OptionalGetJobOutputInputRequestTypeDef = TypedDict(
    "_OptionalGetJobOutputInputRequestTypeDef",
    {
        "accountId": str,
        "range": str,
    },
    total=False,
)


class GetJobOutputInputRequestTypeDef(
    _RequiredGetJobOutputInputRequestTypeDef, _OptionalGetJobOutputInputRequestTypeDef
):
    pass


_RequiredGetVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_RequiredGetVaultAccessPolicyInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalGetVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_OptionalGetVaultAccessPolicyInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class GetVaultAccessPolicyInputRequestTypeDef(
    _RequiredGetVaultAccessPolicyInputRequestTypeDef,
    _OptionalGetVaultAccessPolicyInputRequestTypeDef,
):
    pass


VaultAccessPolicyTypeDef = TypedDict(
    "VaultAccessPolicyTypeDef",
    {
        "Policy": str,
    },
    total=False,
)

_RequiredGetVaultLockInputRequestTypeDef = TypedDict(
    "_RequiredGetVaultLockInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalGetVaultLockInputRequestTypeDef = TypedDict(
    "_OptionalGetVaultLockInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class GetVaultLockInputRequestTypeDef(
    _RequiredGetVaultLockInputRequestTypeDef, _OptionalGetVaultLockInputRequestTypeDef
):
    pass


_RequiredGetVaultNotificationsInputRequestTypeDef = TypedDict(
    "_RequiredGetVaultNotificationsInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalGetVaultNotificationsInputRequestTypeDef = TypedDict(
    "_OptionalGetVaultNotificationsInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class GetVaultNotificationsInputRequestTypeDef(
    _RequiredGetVaultNotificationsInputRequestTypeDef,
    _OptionalGetVaultNotificationsInputRequestTypeDef,
):
    pass


VaultNotificationConfigTypeDef = TypedDict(
    "VaultNotificationConfigTypeDef",
    {
        "SNSTopic": str,
        "Events": List[str],
    },
    total=False,
)

InventoryRetrievalJobDescriptionTypeDef = TypedDict(
    "InventoryRetrievalJobDescriptionTypeDef",
    {
        "Format": str,
        "StartDate": str,
        "EndDate": str,
        "Limit": str,
        "Marker": str,
    },
    total=False,
)

_RequiredGranteeTypeDef = TypedDict(
    "_RequiredGranteeTypeDef",
    {
        "Type": TypeType,
    },
)
_OptionalGranteeTypeDef = TypedDict(
    "_OptionalGranteeTypeDef",
    {
        "DisplayName": str,
        "URI": str,
        "ID": str,
        "EmailAddress": str,
    },
    total=False,
)


class GranteeTypeDef(_RequiredGranteeTypeDef, _OptionalGranteeTypeDef):
    pass


_RequiredInitiateMultipartUploadInputRequestTypeDef = TypedDict(
    "_RequiredInitiateMultipartUploadInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalInitiateMultipartUploadInputRequestTypeDef = TypedDict(
    "_OptionalInitiateMultipartUploadInputRequestTypeDef",
    {
        "accountId": str,
        "archiveDescription": str,
        "partSize": str,
    },
    total=False,
)


class InitiateMultipartUploadInputRequestTypeDef(
    _RequiredInitiateMultipartUploadInputRequestTypeDef,
    _OptionalInitiateMultipartUploadInputRequestTypeDef,
):
    pass


InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef = TypedDict(
    "InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef",
    {
        "archiveDescription": str,
        "partSize": str,
    },
    total=False,
)

VaultLockPolicyTypeDef = TypedDict(
    "VaultLockPolicyTypeDef",
    {
        "Policy": str,
    },
    total=False,
)

InventoryRetrievalJobInputTypeDef = TypedDict(
    "InventoryRetrievalJobInputTypeDef",
    {
        "StartDate": str,
        "EndDate": str,
        "Limit": str,
        "Marker": str,
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

_RequiredListJobsInputRequestTypeDef = TypedDict(
    "_RequiredListJobsInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalListJobsInputRequestTypeDef = TypedDict(
    "_OptionalListJobsInputRequestTypeDef",
    {
        "accountId": str,
        "limit": str,
        "marker": str,
        "statuscode": str,
        "completed": str,
    },
    total=False,
)


class ListJobsInputRequestTypeDef(
    _RequiredListJobsInputRequestTypeDef, _OptionalListJobsInputRequestTypeDef
):
    pass


_RequiredListMultipartUploadsInputRequestTypeDef = TypedDict(
    "_RequiredListMultipartUploadsInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalListMultipartUploadsInputRequestTypeDef = TypedDict(
    "_OptionalListMultipartUploadsInputRequestTypeDef",
    {
        "accountId": str,
        "marker": str,
        "limit": str,
    },
    total=False,
)


class ListMultipartUploadsInputRequestTypeDef(
    _RequiredListMultipartUploadsInputRequestTypeDef,
    _OptionalListMultipartUploadsInputRequestTypeDef,
):
    pass


UploadListElementTypeDef = TypedDict(
    "UploadListElementTypeDef",
    {
        "MultipartUploadId": str,
        "VaultARN": str,
        "ArchiveDescription": str,
        "PartSizeInBytes": int,
        "CreationDate": str,
    },
    total=False,
)

ListPartsInputMultipartUploadPartsTypeDef = TypedDict(
    "ListPartsInputMultipartUploadPartsTypeDef",
    {
        "marker": str,
        "limit": str,
    },
    total=False,
)

_RequiredListPartsInputRequestTypeDef = TypedDict(
    "_RequiredListPartsInputRequestTypeDef",
    {
        "vaultName": str,
        "uploadId": str,
    },
)
_OptionalListPartsInputRequestTypeDef = TypedDict(
    "_OptionalListPartsInputRequestTypeDef",
    {
        "accountId": str,
        "marker": str,
        "limit": str,
    },
    total=False,
)


class ListPartsInputRequestTypeDef(
    _RequiredListPartsInputRequestTypeDef, _OptionalListPartsInputRequestTypeDef
):
    pass


PartListElementTypeDef = TypedDict(
    "PartListElementTypeDef",
    {
        "RangeInBytes": str,
        "SHA256TreeHash": str,
    },
    total=False,
)

ListProvisionedCapacityInputRequestTypeDef = TypedDict(
    "ListProvisionedCapacityInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)

ProvisionedCapacityDescriptionTypeDef = TypedDict(
    "ProvisionedCapacityDescriptionTypeDef",
    {
        "CapacityId": str,
        "StartDate": str,
        "ExpirationDate": str,
    },
    total=False,
)

_RequiredListTagsForVaultInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalListTagsForVaultInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForVaultInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)


class ListTagsForVaultInputRequestTypeDef(
    _RequiredListTagsForVaultInputRequestTypeDef, _OptionalListTagsForVaultInputRequestTypeDef
):
    pass


ListVaultsInputRequestTypeDef = TypedDict(
    "ListVaultsInputRequestTypeDef",
    {
        "accountId": str,
        "marker": str,
        "limit": str,
    },
    total=False,
)

PurchaseProvisionedCapacityInputRequestTypeDef = TypedDict(
    "PurchaseProvisionedCapacityInputRequestTypeDef",
    {
        "accountId": str,
    },
    total=False,
)

_RequiredRemoveTagsFromVaultInputRequestTypeDef = TypedDict(
    "_RequiredRemoveTagsFromVaultInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalRemoveTagsFromVaultInputRequestTypeDef = TypedDict(
    "_OptionalRemoveTagsFromVaultInputRequestTypeDef",
    {
        "accountId": str,
        "TagKeys": Sequence[str],
    },
    total=False,
)


class RemoveTagsFromVaultInputRequestTypeDef(
    _RequiredRemoveTagsFromVaultInputRequestTypeDef, _OptionalRemoveTagsFromVaultInputRequestTypeDef
):
    pass


ServiceResourceAccountRequestTypeDef = TypedDict(
    "ServiceResourceAccountRequestTypeDef",
    {
        "id": str,
    },
)

ServiceResourceArchiveRequestTypeDef = TypedDict(
    "ServiceResourceArchiveRequestTypeDef",
    {
        "account_id": str,
        "vault_name": str,
        "id": str,
    },
)

ServiceResourceJobRequestTypeDef = TypedDict(
    "ServiceResourceJobRequestTypeDef",
    {
        "account_id": str,
        "vault_name": str,
        "id": str,
    },
)

ServiceResourceMultipartUploadRequestTypeDef = TypedDict(
    "ServiceResourceMultipartUploadRequestTypeDef",
    {
        "account_id": str,
        "vault_name": str,
        "id": str,
    },
)

ServiceResourceNotificationRequestTypeDef = TypedDict(
    "ServiceResourceNotificationRequestTypeDef",
    {
        "account_id": str,
        "vault_name": str,
    },
)

ServiceResourceVaultRequestTypeDef = TypedDict(
    "ServiceResourceVaultRequestTypeDef",
    {
        "account_id": str,
        "name": str,
    },
)

_RequiredUploadArchiveInputRequestTypeDef = TypedDict(
    "_RequiredUploadArchiveInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalUploadArchiveInputRequestTypeDef = TypedDict(
    "_OptionalUploadArchiveInputRequestTypeDef",
    {
        "accountId": str,
        "archiveDescription": str,
        "checksum": str,
        "body": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class UploadArchiveInputRequestTypeDef(
    _RequiredUploadArchiveInputRequestTypeDef, _OptionalUploadArchiveInputRequestTypeDef
):
    pass


UploadArchiveInputVaultUploadArchiveTypeDef = TypedDict(
    "UploadArchiveInputVaultUploadArchiveTypeDef",
    {
        "archiveDescription": str,
        "checksum": str,
        "body": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)

UploadMultipartPartInputMultipartUploadUploadPartTypeDef = TypedDict(
    "UploadMultipartPartInputMultipartUploadUploadPartTypeDef",
    {
        "checksum": str,
        "range": str,
        "body": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)

_RequiredUploadMultipartPartInputRequestTypeDef = TypedDict(
    "_RequiredUploadMultipartPartInputRequestTypeDef",
    {
        "vaultName": str,
        "uploadId": str,
    },
)
_OptionalUploadMultipartPartInputRequestTypeDef = TypedDict(
    "_OptionalUploadMultipartPartInputRequestTypeDef",
    {
        "accountId": str,
        "checksum": str,
        "range": str,
        "body": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class UploadMultipartPartInputRequestTypeDef(
    _RequiredUploadMultipartPartInputRequestTypeDef, _OptionalUploadMultipartPartInputRequestTypeDef
):
    pass


VaultArchiveRequestTypeDef = TypedDict(
    "VaultArchiveRequestTypeDef",
    {
        "id": str,
    },
)

VaultJobRequestTypeDef = TypedDict(
    "VaultJobRequestTypeDef",
    {
        "id": str,
    },
)

VaultMultipartUploadRequestTypeDef = TypedDict(
    "VaultMultipartUploadRequestTypeDef",
    {
        "id": str,
    },
)

ArchiveCreationOutputTypeDef = TypedDict(
    "ArchiveCreationOutputTypeDef",
    {
        "location": str,
        "checksum": str,
        "archiveId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVaultOutputTypeDef = TypedDict(
    "CreateVaultOutputTypeDef",
    {
        "location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVaultOutputResponseMetadataTypeDef = TypedDict(
    "DescribeVaultOutputResponseMetadataTypeDef",
    {
        "VaultARN": str,
        "VaultName": str,
        "CreationDate": str,
        "LastInventoryDate": str,
        "NumberOfArchives": int,
        "SizeInBytes": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobOutputOutputTypeDef = TypedDict(
    "GetJobOutputOutputTypeDef",
    {
        "body": StreamingBody,
        "checksum": str,
        "status": int,
        "contentRange": str,
        "acceptRanges": str,
        "contentType": str,
        "archiveDescription": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVaultLockOutputTypeDef = TypedDict(
    "GetVaultLockOutputTypeDef",
    {
        "Policy": str,
        "State": str,
        "ExpirationDate": str,
        "CreationDate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitiateJobOutputTypeDef = TypedDict(
    "InitiateJobOutputTypeDef",
    {
        "location": str,
        "jobId": str,
        "jobOutputPath": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitiateMultipartUploadOutputTypeDef = TypedDict(
    "InitiateMultipartUploadOutputTypeDef",
    {
        "location": str,
        "uploadId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitiateVaultLockOutputTypeDef = TypedDict(
    "InitiateVaultLockOutputTypeDef",
    {
        "lockId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InventoryRetrievalJobDescriptionResponseMetadataTypeDef = TypedDict(
    "InventoryRetrievalJobDescriptionResponseMetadataTypeDef",
    {
        "Format": str,
        "StartDate": str,
        "EndDate": str,
        "Limit": str,
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForVaultOutputTypeDef = TypedDict(
    "ListTagsForVaultOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PurchaseProvisionedCapacityOutputTypeDef = TypedDict(
    "PurchaseProvisionedCapacityOutputTypeDef",
    {
        "capacityId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UploadMultipartPartOutputTypeDef = TypedDict(
    "UploadMultipartPartOutputTypeDef",
    {
        "checksum": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InputSerializationTypeDef = TypedDict(
    "InputSerializationTypeDef",
    {
        "csv": CSVInputTypeDef,
    },
    total=False,
)

OutputSerializationTypeDef = TypedDict(
    "OutputSerializationTypeDef",
    {
        "csv": CSVOutputTypeDef,
    },
    total=False,
)

DataRetrievalPolicyTypeDef = TypedDict(
    "DataRetrievalPolicyTypeDef",
    {
        "Rules": List[DataRetrievalRuleTypeDef],
    },
    total=False,
)

_RequiredDescribeVaultInputVaultExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeVaultInputVaultExistsWaitTypeDef",
    {
        "accountId": str,
        "vaultName": str,
    },
)
_OptionalDescribeVaultInputVaultExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeVaultInputVaultExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeVaultInputVaultExistsWaitTypeDef(
    _RequiredDescribeVaultInputVaultExistsWaitTypeDef,
    _OptionalDescribeVaultInputVaultExistsWaitTypeDef,
):
    pass


_RequiredDescribeVaultInputVaultNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeVaultInputVaultNotExistsWaitTypeDef",
    {
        "accountId": str,
        "vaultName": str,
    },
)
_OptionalDescribeVaultInputVaultNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeVaultInputVaultNotExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeVaultInputVaultNotExistsWaitTypeDef(
    _RequiredDescribeVaultInputVaultNotExistsWaitTypeDef,
    _OptionalDescribeVaultInputVaultNotExistsWaitTypeDef,
):
    pass


ListVaultsOutputTypeDef = TypedDict(
    "ListVaultsOutputTypeDef",
    {
        "VaultList": List[DescribeVaultOutputTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVaultAccessPolicyOutputTypeDef = TypedDict(
    "GetVaultAccessPolicyOutputTypeDef",
    {
        "policy": VaultAccessPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSetVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_RequiredSetVaultAccessPolicyInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalSetVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_OptionalSetVaultAccessPolicyInputRequestTypeDef",
    {
        "accountId": str,
        "policy": VaultAccessPolicyTypeDef,
    },
    total=False,
)


class SetVaultAccessPolicyInputRequestTypeDef(
    _RequiredSetVaultAccessPolicyInputRequestTypeDef,
    _OptionalSetVaultAccessPolicyInputRequestTypeDef,
):
    pass


GetVaultNotificationsOutputTypeDef = TypedDict(
    "GetVaultNotificationsOutputTypeDef",
    {
        "vaultNotificationConfig": VaultNotificationConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetVaultNotificationsInputNotificationSetTypeDef = TypedDict(
    "SetVaultNotificationsInputNotificationSetTypeDef",
    {
        "vaultNotificationConfig": VaultNotificationConfigTypeDef,
    },
    total=False,
)

_RequiredSetVaultNotificationsInputRequestTypeDef = TypedDict(
    "_RequiredSetVaultNotificationsInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalSetVaultNotificationsInputRequestTypeDef = TypedDict(
    "_OptionalSetVaultNotificationsInputRequestTypeDef",
    {
        "accountId": str,
        "vaultNotificationConfig": VaultNotificationConfigTypeDef,
    },
    total=False,
)


class SetVaultNotificationsInputRequestTypeDef(
    _RequiredSetVaultNotificationsInputRequestTypeDef,
    _OptionalSetVaultNotificationsInputRequestTypeDef,
):
    pass


GrantTypeDef = TypedDict(
    "GrantTypeDef",
    {
        "Grantee": GranteeTypeDef,
        "Permission": PermissionType,
    },
    total=False,
)

_RequiredInitiateVaultLockInputRequestTypeDef = TypedDict(
    "_RequiredInitiateVaultLockInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalInitiateVaultLockInputRequestTypeDef = TypedDict(
    "_OptionalInitiateVaultLockInputRequestTypeDef",
    {
        "accountId": str,
        "policy": VaultLockPolicyTypeDef,
    },
    total=False,
)


class InitiateVaultLockInputRequestTypeDef(
    _RequiredInitiateVaultLockInputRequestTypeDef, _OptionalInitiateVaultLockInputRequestTypeDef
):
    pass


_RequiredListJobsInputListJobsPaginateTypeDef = TypedDict(
    "_RequiredListJobsInputListJobsPaginateTypeDef",
    {
        "accountId": str,
        "vaultName": str,
    },
)
_OptionalListJobsInputListJobsPaginateTypeDef = TypedDict(
    "_OptionalListJobsInputListJobsPaginateTypeDef",
    {
        "statuscode": str,
        "completed": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListJobsInputListJobsPaginateTypeDef(
    _RequiredListJobsInputListJobsPaginateTypeDef, _OptionalListJobsInputListJobsPaginateTypeDef
):
    pass


_RequiredListMultipartUploadsInputListMultipartUploadsPaginateTypeDef = TypedDict(
    "_RequiredListMultipartUploadsInputListMultipartUploadsPaginateTypeDef",
    {
        "accountId": str,
        "vaultName": str,
    },
)
_OptionalListMultipartUploadsInputListMultipartUploadsPaginateTypeDef = TypedDict(
    "_OptionalListMultipartUploadsInputListMultipartUploadsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef(
    _RequiredListMultipartUploadsInputListMultipartUploadsPaginateTypeDef,
    _OptionalListMultipartUploadsInputListMultipartUploadsPaginateTypeDef,
):
    pass


_RequiredListPartsInputListPartsPaginateTypeDef = TypedDict(
    "_RequiredListPartsInputListPartsPaginateTypeDef",
    {
        "accountId": str,
        "vaultName": str,
        "uploadId": str,
    },
)
_OptionalListPartsInputListPartsPaginateTypeDef = TypedDict(
    "_OptionalListPartsInputListPartsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPartsInputListPartsPaginateTypeDef(
    _RequiredListPartsInputListPartsPaginateTypeDef, _OptionalListPartsInputListPartsPaginateTypeDef
):
    pass


_RequiredListVaultsInputListVaultsPaginateTypeDef = TypedDict(
    "_RequiredListVaultsInputListVaultsPaginateTypeDef",
    {
        "accountId": str,
    },
)
_OptionalListVaultsInputListVaultsPaginateTypeDef = TypedDict(
    "_OptionalListVaultsInputListVaultsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListVaultsInputListVaultsPaginateTypeDef(
    _RequiredListVaultsInputListVaultsPaginateTypeDef,
    _OptionalListVaultsInputListVaultsPaginateTypeDef,
):
    pass


ListMultipartUploadsOutputTypeDef = TypedDict(
    "ListMultipartUploadsOutputTypeDef",
    {
        "UploadsList": List[UploadListElementTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPartsOutputTypeDef = TypedDict(
    "ListPartsOutputTypeDef",
    {
        "MultipartUploadId": str,
        "VaultARN": str,
        "ArchiveDescription": str,
        "PartSizeInBytes": int,
        "CreationDate": str,
        "Parts": List[PartListElementTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProvisionedCapacityOutputTypeDef = TypedDict(
    "ListProvisionedCapacityOutputTypeDef",
    {
        "ProvisionedCapacityList": List[ProvisionedCapacityDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SelectParametersResponseMetadataTypeDef = TypedDict(
    "SelectParametersResponseMetadataTypeDef",
    {
        "InputSerialization": InputSerializationTypeDef,
        "ExpressionType": Literal["SQL"],
        "Expression": str,
        "OutputSerialization": OutputSerializationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SelectParametersTypeDef = TypedDict(
    "SelectParametersTypeDef",
    {
        "InputSerialization": InputSerializationTypeDef,
        "ExpressionType": Literal["SQL"],
        "Expression": str,
        "OutputSerialization": OutputSerializationTypeDef,
    },
    total=False,
)

GetDataRetrievalPolicyOutputTypeDef = TypedDict(
    "GetDataRetrievalPolicyOutputTypeDef",
    {
        "Policy": DataRetrievalPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetDataRetrievalPolicyInputRequestTypeDef = TypedDict(
    "SetDataRetrievalPolicyInputRequestTypeDef",
    {
        "accountId": str,
        "Policy": DataRetrievalPolicyTypeDef,
    },
    total=False,
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "BucketName": str,
        "Prefix": str,
        "Encryption": EncryptionTypeDef,
        "CannedACL": CannedACLType,
        "AccessControlList": List[GrantTypeDef],
        "Tagging": Dict[str, str],
        "UserMetadata": Dict[str, str],
        "StorageClass": StorageClassType,
    },
    total=False,
)

OutputLocationResponseMetadataTypeDef = TypedDict(
    "OutputLocationResponseMetadataTypeDef",
    {
        "S3": S3LocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OutputLocationTypeDef = TypedDict(
    "OutputLocationTypeDef",
    {
        "S3": S3LocationTypeDef,
    },
    total=False,
)

GlacierJobDescriptionResponseMetadataTypeDef = TypedDict(
    "GlacierJobDescriptionResponseMetadataTypeDef",
    {
        "JobId": str,
        "JobDescription": str,
        "Action": ActionCodeType,
        "ArchiveId": str,
        "VaultARN": str,
        "CreationDate": str,
        "Completed": bool,
        "StatusCode": StatusCodeType,
        "StatusMessage": str,
        "ArchiveSizeInBytes": int,
        "InventorySizeInBytes": int,
        "SNSTopic": str,
        "CompletionDate": str,
        "SHA256TreeHash": str,
        "ArchiveSHA256TreeHash": str,
        "RetrievalByteRange": str,
        "Tier": str,
        "InventoryRetrievalParameters": InventoryRetrievalJobDescriptionTypeDef,
        "JobOutputPath": str,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GlacierJobDescriptionTypeDef = TypedDict(
    "GlacierJobDescriptionTypeDef",
    {
        "JobId": str,
        "JobDescription": str,
        "Action": ActionCodeType,
        "ArchiveId": str,
        "VaultARN": str,
        "CreationDate": str,
        "Completed": bool,
        "StatusCode": StatusCodeType,
        "StatusMessage": str,
        "ArchiveSizeInBytes": int,
        "InventorySizeInBytes": int,
        "SNSTopic": str,
        "CompletionDate": str,
        "SHA256TreeHash": str,
        "ArchiveSHA256TreeHash": str,
        "RetrievalByteRange": str,
        "Tier": str,
        "InventoryRetrievalParameters": InventoryRetrievalJobDescriptionTypeDef,
        "JobOutputPath": str,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

JobParametersTypeDef = TypedDict(
    "JobParametersTypeDef",
    {
        "Format": str,
        "Type": str,
        "ArchiveId": str,
        "Description": str,
        "SNSTopic": str,
        "RetrievalByteRange": str,
        "Tier": str,
        "InventoryRetrievalParameters": InventoryRetrievalJobInputTypeDef,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

ListJobsOutputTypeDef = TypedDict(
    "ListJobsOutputTypeDef",
    {
        "JobList": List[GlacierJobDescriptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredInitiateJobInputRequestTypeDef = TypedDict(
    "_RequiredInitiateJobInputRequestTypeDef",
    {
        "vaultName": str,
    },
)
_OptionalInitiateJobInputRequestTypeDef = TypedDict(
    "_OptionalInitiateJobInputRequestTypeDef",
    {
        "accountId": str,
        "jobParameters": JobParametersTypeDef,
    },
    total=False,
)


class InitiateJobInputRequestTypeDef(
    _RequiredInitiateJobInputRequestTypeDef, _OptionalInitiateJobInputRequestTypeDef
):
    pass
