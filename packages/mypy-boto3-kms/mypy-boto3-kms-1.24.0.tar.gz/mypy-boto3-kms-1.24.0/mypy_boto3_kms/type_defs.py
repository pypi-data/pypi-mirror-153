"""
Type annotations for kms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kms/type_defs/)

Usage::

    ```python
    from mypy_boto3_kms.type_defs import AliasListEntryTypeDef

    data: AliasListEntryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlgorithmSpecType,
    ConnectionErrorCodeTypeType,
    ConnectionStateTypeType,
    CustomerMasterKeySpecType,
    DataKeyPairSpecType,
    DataKeySpecType,
    EncryptionAlgorithmSpecType,
    ExpirationModelTypeType,
    GrantOperationType,
    KeyManagerTypeType,
    KeySpecType,
    KeyStateType,
    KeyUsageTypeType,
    MacAlgorithmSpecType,
    MessageTypeType,
    MultiRegionKeyTypeType,
    OriginTypeType,
    SigningAlgorithmSpecType,
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
    "AliasListEntryTypeDef",
    "CancelKeyDeletionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ConnectCustomKeyStoreRequestRequestTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateCustomKeyStoreRequestRequestTypeDef",
    "GrantConstraintsTypeDef",
    "TagTypeDef",
    "CustomKeyStoresListEntryTypeDef",
    "DecryptRequestRequestTypeDef",
    "DeleteAliasRequestRequestTypeDef",
    "DeleteCustomKeyStoreRequestRequestTypeDef",
    "DeleteImportedKeyMaterialRequestRequestTypeDef",
    "DescribeCustomKeyStoresRequestRequestTypeDef",
    "DescribeKeyRequestRequestTypeDef",
    "DisableKeyRequestRequestTypeDef",
    "DisableKeyRotationRequestRequestTypeDef",
    "DisconnectCustomKeyStoreRequestRequestTypeDef",
    "EnableKeyRequestRequestTypeDef",
    "EnableKeyRotationRequestRequestTypeDef",
    "EncryptRequestRequestTypeDef",
    "GenerateDataKeyPairRequestRequestTypeDef",
    "GenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef",
    "GenerateDataKeyRequestRequestTypeDef",
    "GenerateDataKeyWithoutPlaintextRequestRequestTypeDef",
    "GenerateMacRequestRequestTypeDef",
    "GenerateRandomRequestRequestTypeDef",
    "GetKeyPolicyRequestRequestTypeDef",
    "GetKeyRotationStatusRequestRequestTypeDef",
    "GetParametersForImportRequestRequestTypeDef",
    "GetPublicKeyRequestRequestTypeDef",
    "ImportKeyMaterialRequestRequestTypeDef",
    "KeyListEntryTypeDef",
    "PaginatorConfigTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListGrantsRequestRequestTypeDef",
    "ListKeyPoliciesRequestRequestTypeDef",
    "ListKeysRequestRequestTypeDef",
    "ListResourceTagsRequestRequestTypeDef",
    "ListRetirableGrantsRequestRequestTypeDef",
    "MultiRegionKeyTypeDef",
    "PutKeyPolicyRequestRequestTypeDef",
    "ReEncryptRequestRequestTypeDef",
    "RetireGrantRequestRequestTypeDef",
    "RevokeGrantRequestRequestTypeDef",
    "ScheduleKeyDeletionRequestRequestTypeDef",
    "SignRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAliasRequestRequestTypeDef",
    "UpdateCustomKeyStoreRequestRequestTypeDef",
    "UpdateKeyDescriptionRequestRequestTypeDef",
    "UpdatePrimaryRegionRequestRequestTypeDef",
    "VerifyMacRequestRequestTypeDef",
    "VerifyRequestRequestTypeDef",
    "CancelKeyDeletionResponseTypeDef",
    "CreateCustomKeyStoreResponseTypeDef",
    "CreateGrantResponseTypeDef",
    "DecryptResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptResponseTypeDef",
    "GenerateDataKeyPairResponseTypeDef",
    "GenerateDataKeyPairWithoutPlaintextResponseTypeDef",
    "GenerateDataKeyResponseTypeDef",
    "GenerateDataKeyWithoutPlaintextResponseTypeDef",
    "GenerateMacResponseTypeDef",
    "GenerateRandomResponseTypeDef",
    "GetKeyPolicyResponseTypeDef",
    "GetKeyRotationStatusResponseTypeDef",
    "GetParametersForImportResponseTypeDef",
    "GetPublicKeyResponseTypeDef",
    "ListAliasesResponseTypeDef",
    "ListKeyPoliciesResponseTypeDef",
    "ReEncryptResponseTypeDef",
    "ScheduleKeyDeletionResponseTypeDef",
    "SignResponseTypeDef",
    "VerifyMacResponseTypeDef",
    "VerifyResponseTypeDef",
    "CreateGrantRequestRequestTypeDef",
    "GrantListEntryTypeDef",
    "CreateKeyRequestRequestTypeDef",
    "ListResourceTagsResponseTypeDef",
    "ReplicateKeyRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DescribeCustomKeyStoresResponseTypeDef",
    "ListKeysResponseTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListGrantsRequestListGrantsPaginateTypeDef",
    "ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef",
    "ListKeysRequestListKeysPaginateTypeDef",
    "MultiRegionConfigurationTypeDef",
    "ListGrantsResponseTypeDef",
    "KeyMetadataTypeDef",
    "CreateKeyResponseTypeDef",
    "DescribeKeyResponseTypeDef",
    "ReplicateKeyResponseTypeDef",
)

AliasListEntryTypeDef = TypedDict(
    "AliasListEntryTypeDef",
    {
        "AliasName": str,
        "AliasArn": str,
        "TargetKeyId": str,
        "CreationDate": datetime,
        "LastUpdatedDate": datetime,
    },
    total=False,
)

CancelKeyDeletionRequestRequestTypeDef = TypedDict(
    "CancelKeyDeletionRequestRequestTypeDef",
    {
        "KeyId": str,
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

ConnectCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "ConnectCustomKeyStoreRequestRequestTypeDef",
    {
        "CustomKeyStoreId": str,
    },
)

CreateAliasRequestRequestTypeDef = TypedDict(
    "CreateAliasRequestRequestTypeDef",
    {
        "AliasName": str,
        "TargetKeyId": str,
    },
)

CreateCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "CreateCustomKeyStoreRequestRequestTypeDef",
    {
        "CustomKeyStoreName": str,
        "CloudHsmClusterId": str,
        "TrustAnchorCertificate": str,
        "KeyStorePassword": str,
    },
)

GrantConstraintsTypeDef = TypedDict(
    "GrantConstraintsTypeDef",
    {
        "EncryptionContextSubset": Mapping[str, str],
        "EncryptionContextEquals": Mapping[str, str],
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "TagKey": str,
        "TagValue": str,
    },
)

CustomKeyStoresListEntryTypeDef = TypedDict(
    "CustomKeyStoresListEntryTypeDef",
    {
        "CustomKeyStoreId": str,
        "CustomKeyStoreName": str,
        "CloudHsmClusterId": str,
        "TrustAnchorCertificate": str,
        "ConnectionState": ConnectionStateTypeType,
        "ConnectionErrorCode": ConnectionErrorCodeTypeType,
        "CreationDate": datetime,
    },
    total=False,
)

_RequiredDecryptRequestRequestTypeDef = TypedDict(
    "_RequiredDecryptRequestRequestTypeDef",
    {
        "CiphertextBlob": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalDecryptRequestRequestTypeDef = TypedDict(
    "_OptionalDecryptRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "GrantTokens": Sequence[str],
        "KeyId": str,
        "EncryptionAlgorithm": EncryptionAlgorithmSpecType,
    },
    total=False,
)


class DecryptRequestRequestTypeDef(
    _RequiredDecryptRequestRequestTypeDef, _OptionalDecryptRequestRequestTypeDef
):
    pass


DeleteAliasRequestRequestTypeDef = TypedDict(
    "DeleteAliasRequestRequestTypeDef",
    {
        "AliasName": str,
    },
)

DeleteCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "DeleteCustomKeyStoreRequestRequestTypeDef",
    {
        "CustomKeyStoreId": str,
    },
)

DeleteImportedKeyMaterialRequestRequestTypeDef = TypedDict(
    "DeleteImportedKeyMaterialRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

DescribeCustomKeyStoresRequestRequestTypeDef = TypedDict(
    "DescribeCustomKeyStoresRequestRequestTypeDef",
    {
        "CustomKeyStoreId": str,
        "CustomKeyStoreName": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeKeyRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeKeyRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalDescribeKeyRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeKeyRequestRequestTypeDef",
    {
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class DescribeKeyRequestRequestTypeDef(
    _RequiredDescribeKeyRequestRequestTypeDef, _OptionalDescribeKeyRequestRequestTypeDef
):
    pass


DisableKeyRequestRequestTypeDef = TypedDict(
    "DisableKeyRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

DisableKeyRotationRequestRequestTypeDef = TypedDict(
    "DisableKeyRotationRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

DisconnectCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "DisconnectCustomKeyStoreRequestRequestTypeDef",
    {
        "CustomKeyStoreId": str,
    },
)

EnableKeyRequestRequestTypeDef = TypedDict(
    "EnableKeyRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

EnableKeyRotationRequestRequestTypeDef = TypedDict(
    "EnableKeyRotationRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

_RequiredEncryptRequestRequestTypeDef = TypedDict(
    "_RequiredEncryptRequestRequestTypeDef",
    {
        "KeyId": str,
        "Plaintext": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalEncryptRequestRequestTypeDef = TypedDict(
    "_OptionalEncryptRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "GrantTokens": Sequence[str],
        "EncryptionAlgorithm": EncryptionAlgorithmSpecType,
    },
    total=False,
)


class EncryptRequestRequestTypeDef(
    _RequiredEncryptRequestRequestTypeDef, _OptionalEncryptRequestRequestTypeDef
):
    pass


_RequiredGenerateDataKeyPairRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateDataKeyPairRequestRequestTypeDef",
    {
        "KeyId": str,
        "KeyPairSpec": DataKeyPairSpecType,
    },
)
_OptionalGenerateDataKeyPairRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateDataKeyPairRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GenerateDataKeyPairRequestRequestTypeDef(
    _RequiredGenerateDataKeyPairRequestRequestTypeDef,
    _OptionalGenerateDataKeyPairRequestRequestTypeDef,
):
    pass


_RequiredGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef",
    {
        "KeyId": str,
        "KeyPairSpec": DataKeyPairSpecType,
    },
)
_OptionalGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef(
    _RequiredGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef,
    _OptionalGenerateDataKeyPairWithoutPlaintextRequestRequestTypeDef,
):
    pass


_RequiredGenerateDataKeyRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateDataKeyRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalGenerateDataKeyRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateDataKeyRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "NumberOfBytes": int,
        "KeySpec": DataKeySpecType,
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GenerateDataKeyRequestRequestTypeDef(
    _RequiredGenerateDataKeyRequestRequestTypeDef, _OptionalGenerateDataKeyRequestRequestTypeDef
):
    pass


_RequiredGenerateDataKeyWithoutPlaintextRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateDataKeyWithoutPlaintextRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalGenerateDataKeyWithoutPlaintextRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateDataKeyWithoutPlaintextRequestRequestTypeDef",
    {
        "EncryptionContext": Mapping[str, str],
        "KeySpec": DataKeySpecType,
        "NumberOfBytes": int,
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GenerateDataKeyWithoutPlaintextRequestRequestTypeDef(
    _RequiredGenerateDataKeyWithoutPlaintextRequestRequestTypeDef,
    _OptionalGenerateDataKeyWithoutPlaintextRequestRequestTypeDef,
):
    pass


_RequiredGenerateMacRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateMacRequestRequestTypeDef",
    {
        "Message": Union[str, bytes, IO[Any], StreamingBody],
        "KeyId": str,
        "MacAlgorithm": MacAlgorithmSpecType,
    },
)
_OptionalGenerateMacRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateMacRequestRequestTypeDef",
    {
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GenerateMacRequestRequestTypeDef(
    _RequiredGenerateMacRequestRequestTypeDef, _OptionalGenerateMacRequestRequestTypeDef
):
    pass


GenerateRandomRequestRequestTypeDef = TypedDict(
    "GenerateRandomRequestRequestTypeDef",
    {
        "NumberOfBytes": int,
        "CustomKeyStoreId": str,
    },
    total=False,
)

GetKeyPolicyRequestRequestTypeDef = TypedDict(
    "GetKeyPolicyRequestRequestTypeDef",
    {
        "KeyId": str,
        "PolicyName": str,
    },
)

GetKeyRotationStatusRequestRequestTypeDef = TypedDict(
    "GetKeyRotationStatusRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)

GetParametersForImportRequestRequestTypeDef = TypedDict(
    "GetParametersForImportRequestRequestTypeDef",
    {
        "KeyId": str,
        "WrappingAlgorithm": AlgorithmSpecType,
        "WrappingKeySpec": Literal["RSA_2048"],
    },
)

_RequiredGetPublicKeyRequestRequestTypeDef = TypedDict(
    "_RequiredGetPublicKeyRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalGetPublicKeyRequestRequestTypeDef = TypedDict(
    "_OptionalGetPublicKeyRequestRequestTypeDef",
    {
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class GetPublicKeyRequestRequestTypeDef(
    _RequiredGetPublicKeyRequestRequestTypeDef, _OptionalGetPublicKeyRequestRequestTypeDef
):
    pass


_RequiredImportKeyMaterialRequestRequestTypeDef = TypedDict(
    "_RequiredImportKeyMaterialRequestRequestTypeDef",
    {
        "KeyId": str,
        "ImportToken": Union[str, bytes, IO[Any], StreamingBody],
        "EncryptedKeyMaterial": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalImportKeyMaterialRequestRequestTypeDef = TypedDict(
    "_OptionalImportKeyMaterialRequestRequestTypeDef",
    {
        "ValidTo": Union[datetime, str],
        "ExpirationModel": ExpirationModelTypeType,
    },
    total=False,
)


class ImportKeyMaterialRequestRequestTypeDef(
    _RequiredImportKeyMaterialRequestRequestTypeDef, _OptionalImportKeyMaterialRequestRequestTypeDef
):
    pass


KeyListEntryTypeDef = TypedDict(
    "KeyListEntryTypeDef",
    {
        "KeyId": str,
        "KeyArn": str,
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

ListAliasesRequestRequestTypeDef = TypedDict(
    "ListAliasesRequestRequestTypeDef",
    {
        "KeyId": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

_RequiredListGrantsRequestRequestTypeDef = TypedDict(
    "_RequiredListGrantsRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalListGrantsRequestRequestTypeDef = TypedDict(
    "_OptionalListGrantsRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
        "GrantId": str,
        "GranteePrincipal": str,
    },
    total=False,
)


class ListGrantsRequestRequestTypeDef(
    _RequiredListGrantsRequestRequestTypeDef, _OptionalListGrantsRequestRequestTypeDef
):
    pass


_RequiredListKeyPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListKeyPoliciesRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalListKeyPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListKeyPoliciesRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
    },
    total=False,
)


class ListKeyPoliciesRequestRequestTypeDef(
    _RequiredListKeyPoliciesRequestRequestTypeDef, _OptionalListKeyPoliciesRequestRequestTypeDef
):
    pass


ListKeysRequestRequestTypeDef = TypedDict(
    "ListKeysRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

_RequiredListResourceTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListResourceTagsRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalListResourceTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListResourceTagsRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
    },
    total=False,
)


class ListResourceTagsRequestRequestTypeDef(
    _RequiredListResourceTagsRequestRequestTypeDef, _OptionalListResourceTagsRequestRequestTypeDef
):
    pass


_RequiredListRetirableGrantsRequestRequestTypeDef = TypedDict(
    "_RequiredListRetirableGrantsRequestRequestTypeDef",
    {
        "RetiringPrincipal": str,
    },
)
_OptionalListRetirableGrantsRequestRequestTypeDef = TypedDict(
    "_OptionalListRetirableGrantsRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
    },
    total=False,
)


class ListRetirableGrantsRequestRequestTypeDef(
    _RequiredListRetirableGrantsRequestRequestTypeDef,
    _OptionalListRetirableGrantsRequestRequestTypeDef,
):
    pass


MultiRegionKeyTypeDef = TypedDict(
    "MultiRegionKeyTypeDef",
    {
        "Arn": str,
        "Region": str,
    },
    total=False,
)

_RequiredPutKeyPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutKeyPolicyRequestRequestTypeDef",
    {
        "KeyId": str,
        "PolicyName": str,
        "Policy": str,
    },
)
_OptionalPutKeyPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutKeyPolicyRequestRequestTypeDef",
    {
        "BypassPolicyLockoutSafetyCheck": bool,
    },
    total=False,
)


class PutKeyPolicyRequestRequestTypeDef(
    _RequiredPutKeyPolicyRequestRequestTypeDef, _OptionalPutKeyPolicyRequestRequestTypeDef
):
    pass


_RequiredReEncryptRequestRequestTypeDef = TypedDict(
    "_RequiredReEncryptRequestRequestTypeDef",
    {
        "CiphertextBlob": Union[str, bytes, IO[Any], StreamingBody],
        "DestinationKeyId": str,
    },
)
_OptionalReEncryptRequestRequestTypeDef = TypedDict(
    "_OptionalReEncryptRequestRequestTypeDef",
    {
        "SourceEncryptionContext": Mapping[str, str],
        "SourceKeyId": str,
        "DestinationEncryptionContext": Mapping[str, str],
        "SourceEncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "DestinationEncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class ReEncryptRequestRequestTypeDef(
    _RequiredReEncryptRequestRequestTypeDef, _OptionalReEncryptRequestRequestTypeDef
):
    pass


RetireGrantRequestRequestTypeDef = TypedDict(
    "RetireGrantRequestRequestTypeDef",
    {
        "GrantToken": str,
        "KeyId": str,
        "GrantId": str,
    },
    total=False,
)

RevokeGrantRequestRequestTypeDef = TypedDict(
    "RevokeGrantRequestRequestTypeDef",
    {
        "KeyId": str,
        "GrantId": str,
    },
)

_RequiredScheduleKeyDeletionRequestRequestTypeDef = TypedDict(
    "_RequiredScheduleKeyDeletionRequestRequestTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalScheduleKeyDeletionRequestRequestTypeDef = TypedDict(
    "_OptionalScheduleKeyDeletionRequestRequestTypeDef",
    {
        "PendingWindowInDays": int,
    },
    total=False,
)


class ScheduleKeyDeletionRequestRequestTypeDef(
    _RequiredScheduleKeyDeletionRequestRequestTypeDef,
    _OptionalScheduleKeyDeletionRequestRequestTypeDef,
):
    pass


_RequiredSignRequestRequestTypeDef = TypedDict(
    "_RequiredSignRequestRequestTypeDef",
    {
        "KeyId": str,
        "Message": Union[str, bytes, IO[Any], StreamingBody],
        "SigningAlgorithm": SigningAlgorithmSpecType,
    },
)
_OptionalSignRequestRequestTypeDef = TypedDict(
    "_OptionalSignRequestRequestTypeDef",
    {
        "MessageType": MessageTypeType,
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class SignRequestRequestTypeDef(
    _RequiredSignRequestRequestTypeDef, _OptionalSignRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "KeyId": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAliasRequestRequestTypeDef = TypedDict(
    "UpdateAliasRequestRequestTypeDef",
    {
        "AliasName": str,
        "TargetKeyId": str,
    },
)

_RequiredUpdateCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCustomKeyStoreRequestRequestTypeDef",
    {
        "CustomKeyStoreId": str,
    },
)
_OptionalUpdateCustomKeyStoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCustomKeyStoreRequestRequestTypeDef",
    {
        "NewCustomKeyStoreName": str,
        "KeyStorePassword": str,
        "CloudHsmClusterId": str,
    },
    total=False,
)


class UpdateCustomKeyStoreRequestRequestTypeDef(
    _RequiredUpdateCustomKeyStoreRequestRequestTypeDef,
    _OptionalUpdateCustomKeyStoreRequestRequestTypeDef,
):
    pass


UpdateKeyDescriptionRequestRequestTypeDef = TypedDict(
    "UpdateKeyDescriptionRequestRequestTypeDef",
    {
        "KeyId": str,
        "Description": str,
    },
)

UpdatePrimaryRegionRequestRequestTypeDef = TypedDict(
    "UpdatePrimaryRegionRequestRequestTypeDef",
    {
        "KeyId": str,
        "PrimaryRegion": str,
    },
)

_RequiredVerifyMacRequestRequestTypeDef = TypedDict(
    "_RequiredVerifyMacRequestRequestTypeDef",
    {
        "Message": Union[str, bytes, IO[Any], StreamingBody],
        "KeyId": str,
        "MacAlgorithm": MacAlgorithmSpecType,
        "Mac": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalVerifyMacRequestRequestTypeDef = TypedDict(
    "_OptionalVerifyMacRequestRequestTypeDef",
    {
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class VerifyMacRequestRequestTypeDef(
    _RequiredVerifyMacRequestRequestTypeDef, _OptionalVerifyMacRequestRequestTypeDef
):
    pass


_RequiredVerifyRequestRequestTypeDef = TypedDict(
    "_RequiredVerifyRequestRequestTypeDef",
    {
        "KeyId": str,
        "Message": Union[str, bytes, IO[Any], StreamingBody],
        "Signature": Union[str, bytes, IO[Any], StreamingBody],
        "SigningAlgorithm": SigningAlgorithmSpecType,
    },
)
_OptionalVerifyRequestRequestTypeDef = TypedDict(
    "_OptionalVerifyRequestRequestTypeDef",
    {
        "MessageType": MessageTypeType,
        "GrantTokens": Sequence[str],
    },
    total=False,
)


class VerifyRequestRequestTypeDef(
    _RequiredVerifyRequestRequestTypeDef, _OptionalVerifyRequestRequestTypeDef
):
    pass


CancelKeyDeletionResponseTypeDef = TypedDict(
    "CancelKeyDeletionResponseTypeDef",
    {
        "KeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomKeyStoreResponseTypeDef = TypedDict(
    "CreateCustomKeyStoreResponseTypeDef",
    {
        "CustomKeyStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGrantResponseTypeDef = TypedDict(
    "CreateGrantResponseTypeDef",
    {
        "GrantToken": str,
        "GrantId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DecryptResponseTypeDef = TypedDict(
    "DecryptResponseTypeDef",
    {
        "KeyId": str,
        "Plaintext": bytes,
        "EncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptResponseTypeDef = TypedDict(
    "EncryptResponseTypeDef",
    {
        "CiphertextBlob": bytes,
        "KeyId": str,
        "EncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateDataKeyPairResponseTypeDef = TypedDict(
    "GenerateDataKeyPairResponseTypeDef",
    {
        "PrivateKeyCiphertextBlob": bytes,
        "PrivateKeyPlaintext": bytes,
        "PublicKey": bytes,
        "KeyId": str,
        "KeyPairSpec": DataKeyPairSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateDataKeyPairWithoutPlaintextResponseTypeDef = TypedDict(
    "GenerateDataKeyPairWithoutPlaintextResponseTypeDef",
    {
        "PrivateKeyCiphertextBlob": bytes,
        "PublicKey": bytes,
        "KeyId": str,
        "KeyPairSpec": DataKeyPairSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateDataKeyResponseTypeDef = TypedDict(
    "GenerateDataKeyResponseTypeDef",
    {
        "CiphertextBlob": bytes,
        "Plaintext": bytes,
        "KeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateDataKeyWithoutPlaintextResponseTypeDef = TypedDict(
    "GenerateDataKeyWithoutPlaintextResponseTypeDef",
    {
        "CiphertextBlob": bytes,
        "KeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateMacResponseTypeDef = TypedDict(
    "GenerateMacResponseTypeDef",
    {
        "Mac": bytes,
        "MacAlgorithm": MacAlgorithmSpecType,
        "KeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateRandomResponseTypeDef = TypedDict(
    "GenerateRandomResponseTypeDef",
    {
        "Plaintext": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKeyPolicyResponseTypeDef = TypedDict(
    "GetKeyPolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKeyRotationStatusResponseTypeDef = TypedDict(
    "GetKeyRotationStatusResponseTypeDef",
    {
        "KeyRotationEnabled": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParametersForImportResponseTypeDef = TypedDict(
    "GetParametersForImportResponseTypeDef",
    {
        "KeyId": str,
        "ImportToken": bytes,
        "PublicKey": bytes,
        "ParametersValidTo": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPublicKeyResponseTypeDef = TypedDict(
    "GetPublicKeyResponseTypeDef",
    {
        "KeyId": str,
        "PublicKey": bytes,
        "CustomerMasterKeySpec": CustomerMasterKeySpecType,
        "KeySpec": KeySpecType,
        "KeyUsage": KeyUsageTypeType,
        "EncryptionAlgorithms": List[EncryptionAlgorithmSpecType],
        "SigningAlgorithms": List[SigningAlgorithmSpecType],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {
        "Aliases": List[AliasListEntryTypeDef],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKeyPoliciesResponseTypeDef = TypedDict(
    "ListKeyPoliciesResponseTypeDef",
    {
        "PolicyNames": List[str],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReEncryptResponseTypeDef = TypedDict(
    "ReEncryptResponseTypeDef",
    {
        "CiphertextBlob": bytes,
        "SourceKeyId": str,
        "KeyId": str,
        "SourceEncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "DestinationEncryptionAlgorithm": EncryptionAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduleKeyDeletionResponseTypeDef = TypedDict(
    "ScheduleKeyDeletionResponseTypeDef",
    {
        "KeyId": str,
        "DeletionDate": datetime,
        "KeyState": KeyStateType,
        "PendingWindowInDays": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SignResponseTypeDef = TypedDict(
    "SignResponseTypeDef",
    {
        "KeyId": str,
        "Signature": bytes,
        "SigningAlgorithm": SigningAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyMacResponseTypeDef = TypedDict(
    "VerifyMacResponseTypeDef",
    {
        "KeyId": str,
        "MacValid": bool,
        "MacAlgorithm": MacAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyResponseTypeDef = TypedDict(
    "VerifyResponseTypeDef",
    {
        "KeyId": str,
        "SignatureValid": bool,
        "SigningAlgorithm": SigningAlgorithmSpecType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateGrantRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGrantRequestRequestTypeDef",
    {
        "KeyId": str,
        "GranteePrincipal": str,
        "Operations": Sequence[GrantOperationType],
    },
)
_OptionalCreateGrantRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGrantRequestRequestTypeDef",
    {
        "RetiringPrincipal": str,
        "Constraints": GrantConstraintsTypeDef,
        "GrantTokens": Sequence[str],
        "Name": str,
    },
    total=False,
)


class CreateGrantRequestRequestTypeDef(
    _RequiredCreateGrantRequestRequestTypeDef, _OptionalCreateGrantRequestRequestTypeDef
):
    pass


GrantListEntryTypeDef = TypedDict(
    "GrantListEntryTypeDef",
    {
        "KeyId": str,
        "GrantId": str,
        "Name": str,
        "CreationDate": datetime,
        "GranteePrincipal": str,
        "RetiringPrincipal": str,
        "IssuingAccount": str,
        "Operations": List[GrantOperationType],
        "Constraints": GrantConstraintsTypeDef,
    },
    total=False,
)

CreateKeyRequestRequestTypeDef = TypedDict(
    "CreateKeyRequestRequestTypeDef",
    {
        "Policy": str,
        "Description": str,
        "KeyUsage": KeyUsageTypeType,
        "CustomerMasterKeySpec": CustomerMasterKeySpecType,
        "KeySpec": KeySpecType,
        "Origin": OriginTypeType,
        "CustomKeyStoreId": str,
        "BypassPolicyLockoutSafetyCheck": bool,
        "Tags": Sequence[TagTypeDef],
        "MultiRegion": bool,
    },
    total=False,
)

ListResourceTagsResponseTypeDef = TypedDict(
    "ListResourceTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredReplicateKeyRequestRequestTypeDef = TypedDict(
    "_RequiredReplicateKeyRequestRequestTypeDef",
    {
        "KeyId": str,
        "ReplicaRegion": str,
    },
)
_OptionalReplicateKeyRequestRequestTypeDef = TypedDict(
    "_OptionalReplicateKeyRequestRequestTypeDef",
    {
        "Policy": str,
        "BypassPolicyLockoutSafetyCheck": bool,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ReplicateKeyRequestRequestTypeDef(
    _RequiredReplicateKeyRequestRequestTypeDef, _OptionalReplicateKeyRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "KeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
)

DescribeCustomKeyStoresResponseTypeDef = TypedDict(
    "DescribeCustomKeyStoresResponseTypeDef",
    {
        "CustomKeyStores": List[CustomKeyStoresListEntryTypeDef],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKeysResponseTypeDef = TypedDict(
    "ListKeysResponseTypeDef",
    {
        "Keys": List[KeyListEntryTypeDef],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "ListAliasesRequestListAliasesPaginateTypeDef",
    {
        "KeyId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListGrantsRequestListGrantsPaginateTypeDef = TypedDict(
    "_RequiredListGrantsRequestListGrantsPaginateTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalListGrantsRequestListGrantsPaginateTypeDef = TypedDict(
    "_OptionalListGrantsRequestListGrantsPaginateTypeDef",
    {
        "GrantId": str,
        "GranteePrincipal": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGrantsRequestListGrantsPaginateTypeDef(
    _RequiredListGrantsRequestListGrantsPaginateTypeDef,
    _OptionalListGrantsRequestListGrantsPaginateTypeDef,
):
    pass


_RequiredListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef(
    _RequiredListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef,
    _OptionalListKeyPoliciesRequestListKeyPoliciesPaginateTypeDef,
):
    pass


ListKeysRequestListKeysPaginateTypeDef = TypedDict(
    "ListKeysRequestListKeysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

MultiRegionConfigurationTypeDef = TypedDict(
    "MultiRegionConfigurationTypeDef",
    {
        "MultiRegionKeyType": MultiRegionKeyTypeType,
        "PrimaryKey": MultiRegionKeyTypeDef,
        "ReplicaKeys": List[MultiRegionKeyTypeDef],
    },
    total=False,
)

ListGrantsResponseTypeDef = TypedDict(
    "ListGrantsResponseTypeDef",
    {
        "Grants": List[GrantListEntryTypeDef],
        "NextMarker": str,
        "Truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredKeyMetadataTypeDef = TypedDict(
    "_RequiredKeyMetadataTypeDef",
    {
        "KeyId": str,
    },
)
_OptionalKeyMetadataTypeDef = TypedDict(
    "_OptionalKeyMetadataTypeDef",
    {
        "AWSAccountId": str,
        "Arn": str,
        "CreationDate": datetime,
        "Enabled": bool,
        "Description": str,
        "KeyUsage": KeyUsageTypeType,
        "KeyState": KeyStateType,
        "DeletionDate": datetime,
        "ValidTo": datetime,
        "Origin": OriginTypeType,
        "CustomKeyStoreId": str,
        "CloudHsmClusterId": str,
        "ExpirationModel": ExpirationModelTypeType,
        "KeyManager": KeyManagerTypeType,
        "CustomerMasterKeySpec": CustomerMasterKeySpecType,
        "KeySpec": KeySpecType,
        "EncryptionAlgorithms": List[EncryptionAlgorithmSpecType],
        "SigningAlgorithms": List[SigningAlgorithmSpecType],
        "MultiRegion": bool,
        "MultiRegionConfiguration": MultiRegionConfigurationTypeDef,
        "PendingDeletionWindowInDays": int,
        "MacAlgorithms": List[MacAlgorithmSpecType],
    },
    total=False,
)


class KeyMetadataTypeDef(_RequiredKeyMetadataTypeDef, _OptionalKeyMetadataTypeDef):
    pass


CreateKeyResponseTypeDef = TypedDict(
    "CreateKeyResponseTypeDef",
    {
        "KeyMetadata": KeyMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeKeyResponseTypeDef = TypedDict(
    "DescribeKeyResponseTypeDef",
    {
        "KeyMetadata": KeyMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicateKeyResponseTypeDef = TypedDict(
    "ReplicateKeyResponseTypeDef",
    {
        "ReplicaKeyMetadata": KeyMetadataTypeDef,
        "ReplicaPolicy": str,
        "ReplicaTags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
