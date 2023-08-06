"""
Type annotations for signer service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/type_defs/)

Usage::

    ```python
    from mypy_boto3_signer.type_defs import AddProfilePermissionRequestRequestTypeDef

    data: AddProfilePermissionRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EncryptionAlgorithmType,
    HashAlgorithmType,
    ImageFormatType,
    SigningProfileStatusType,
    SigningStatusType,
    ValidityTypeType,
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
    "AddProfilePermissionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CancelSigningProfileRequestRequestTypeDef",
    "DescribeSigningJobRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "SigningJobRevocationRecordTypeDef",
    "SigningMaterialTypeDef",
    "S3DestinationTypeDef",
    "EncryptionAlgorithmOptionsTypeDef",
    "GetSigningPlatformRequestRequestTypeDef",
    "SigningImageFormatTypeDef",
    "GetSigningProfileRequestRequestTypeDef",
    "SignatureValidityPeriodTypeDef",
    "SigningProfileRevocationRecordTypeDef",
    "HashAlgorithmOptionsTypeDef",
    "ListProfilePermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "PaginatorConfigTypeDef",
    "ListSigningJobsRequestRequestTypeDef",
    "ListSigningPlatformsRequestRequestTypeDef",
    "ListSigningProfilesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RemoveProfilePermissionRequestRequestTypeDef",
    "RevokeSignatureRequestRequestTypeDef",
    "RevokeSigningProfileRequestRequestTypeDef",
    "S3SignedObjectTypeDef",
    "S3SourceTypeDef",
    "SigningConfigurationOverridesTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AddProfilePermissionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutSigningProfileResponseTypeDef",
    "RemoveProfilePermissionResponseTypeDef",
    "StartSigningJobResponseTypeDef",
    "DescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef",
    "DestinationTypeDef",
    "SigningProfileTypeDef",
    "SigningConfigurationTypeDef",
    "ListProfilePermissionsResponseTypeDef",
    "ListSigningJobsRequestListSigningJobsPaginateTypeDef",
    "ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef",
    "ListSigningProfilesRequestListSigningProfilesPaginateTypeDef",
    "SignedObjectTypeDef",
    "SourceTypeDef",
    "SigningPlatformOverridesTypeDef",
    "ListSigningProfilesResponseTypeDef",
    "GetSigningPlatformResponseTypeDef",
    "SigningPlatformTypeDef",
    "SigningJobTypeDef",
    "StartSigningJobRequestRequestTypeDef",
    "DescribeSigningJobResponseTypeDef",
    "GetSigningProfileResponseTypeDef",
    "PutSigningProfileRequestRequestTypeDef",
    "ListSigningPlatformsResponseTypeDef",
    "ListSigningJobsResponseTypeDef",
)

_RequiredAddProfilePermissionRequestRequestTypeDef = TypedDict(
    "_RequiredAddProfilePermissionRequestRequestTypeDef",
    {
        "profileName": str,
        "action": str,
        "principal": str,
        "statementId": str,
    },
)
_OptionalAddProfilePermissionRequestRequestTypeDef = TypedDict(
    "_OptionalAddProfilePermissionRequestRequestTypeDef",
    {
        "profileVersion": str,
        "revisionId": str,
    },
    total=False,
)


class AddProfilePermissionRequestRequestTypeDef(
    _RequiredAddProfilePermissionRequestRequestTypeDef,
    _OptionalAddProfilePermissionRequestRequestTypeDef,
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

CancelSigningProfileRequestRequestTypeDef = TypedDict(
    "CancelSigningProfileRequestRequestTypeDef",
    {
        "profileName": str,
    },
)

DescribeSigningJobRequestRequestTypeDef = TypedDict(
    "DescribeSigningJobRequestRequestTypeDef",
    {
        "jobId": str,
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

SigningJobRevocationRecordTypeDef = TypedDict(
    "SigningJobRevocationRecordTypeDef",
    {
        "reason": str,
        "revokedAt": datetime,
        "revokedBy": str,
    },
    total=False,
)

SigningMaterialTypeDef = TypedDict(
    "SigningMaterialTypeDef",
    {
        "certificateArn": str,
    },
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "bucketName": str,
        "prefix": str,
    },
    total=False,
)

EncryptionAlgorithmOptionsTypeDef = TypedDict(
    "EncryptionAlgorithmOptionsTypeDef",
    {
        "allowedValues": List[EncryptionAlgorithmType],
        "defaultValue": EncryptionAlgorithmType,
    },
)

GetSigningPlatformRequestRequestTypeDef = TypedDict(
    "GetSigningPlatformRequestRequestTypeDef",
    {
        "platformId": str,
    },
)

SigningImageFormatTypeDef = TypedDict(
    "SigningImageFormatTypeDef",
    {
        "supportedFormats": List[ImageFormatType],
        "defaultFormat": ImageFormatType,
    },
)

_RequiredGetSigningProfileRequestRequestTypeDef = TypedDict(
    "_RequiredGetSigningProfileRequestRequestTypeDef",
    {
        "profileName": str,
    },
)
_OptionalGetSigningProfileRequestRequestTypeDef = TypedDict(
    "_OptionalGetSigningProfileRequestRequestTypeDef",
    {
        "profileOwner": str,
    },
    total=False,
)


class GetSigningProfileRequestRequestTypeDef(
    _RequiredGetSigningProfileRequestRequestTypeDef, _OptionalGetSigningProfileRequestRequestTypeDef
):
    pass


SignatureValidityPeriodTypeDef = TypedDict(
    "SignatureValidityPeriodTypeDef",
    {
        "value": int,
        "type": ValidityTypeType,
    },
    total=False,
)

SigningProfileRevocationRecordTypeDef = TypedDict(
    "SigningProfileRevocationRecordTypeDef",
    {
        "revocationEffectiveFrom": datetime,
        "revokedAt": datetime,
        "revokedBy": str,
    },
    total=False,
)

HashAlgorithmOptionsTypeDef = TypedDict(
    "HashAlgorithmOptionsTypeDef",
    {
        "allowedValues": List[HashAlgorithmType],
        "defaultValue": HashAlgorithmType,
    },
)

_RequiredListProfilePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListProfilePermissionsRequestRequestTypeDef",
    {
        "profileName": str,
    },
)
_OptionalListProfilePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListProfilePermissionsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListProfilePermissionsRequestRequestTypeDef(
    _RequiredListProfilePermissionsRequestRequestTypeDef,
    _OptionalListProfilePermissionsRequestRequestTypeDef,
):
    pass


PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "action": str,
        "principal": str,
        "statementId": str,
        "profileVersion": str,
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

ListSigningJobsRequestRequestTypeDef = TypedDict(
    "ListSigningJobsRequestRequestTypeDef",
    {
        "status": SigningStatusType,
        "platformId": str,
        "requestedBy": str,
        "maxResults": int,
        "nextToken": str,
        "isRevoked": bool,
        "signatureExpiresBefore": Union[datetime, str],
        "signatureExpiresAfter": Union[datetime, str],
        "jobInvoker": str,
    },
    total=False,
)

ListSigningPlatformsRequestRequestTypeDef = TypedDict(
    "ListSigningPlatformsRequestRequestTypeDef",
    {
        "category": str,
        "partner": str,
        "target": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSigningProfilesRequestRequestTypeDef = TypedDict(
    "ListSigningProfilesRequestRequestTypeDef",
    {
        "includeCanceled": bool,
        "maxResults": int,
        "nextToken": str,
        "platformId": str,
        "statuses": Sequence[SigningProfileStatusType],
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

RemoveProfilePermissionRequestRequestTypeDef = TypedDict(
    "RemoveProfilePermissionRequestRequestTypeDef",
    {
        "profileName": str,
        "revisionId": str,
        "statementId": str,
    },
)

_RequiredRevokeSignatureRequestRequestTypeDef = TypedDict(
    "_RequiredRevokeSignatureRequestRequestTypeDef",
    {
        "jobId": str,
        "reason": str,
    },
)
_OptionalRevokeSignatureRequestRequestTypeDef = TypedDict(
    "_OptionalRevokeSignatureRequestRequestTypeDef",
    {
        "jobOwner": str,
    },
    total=False,
)


class RevokeSignatureRequestRequestTypeDef(
    _RequiredRevokeSignatureRequestRequestTypeDef, _OptionalRevokeSignatureRequestRequestTypeDef
):
    pass


RevokeSigningProfileRequestRequestTypeDef = TypedDict(
    "RevokeSigningProfileRequestRequestTypeDef",
    {
        "profileName": str,
        "profileVersion": str,
        "reason": str,
        "effectiveTime": Union[datetime, str],
    },
)

S3SignedObjectTypeDef = TypedDict(
    "S3SignedObjectTypeDef",
    {
        "bucketName": str,
        "key": str,
    },
    total=False,
)

S3SourceTypeDef = TypedDict(
    "S3SourceTypeDef",
    {
        "bucketName": str,
        "key": str,
        "version": str,
    },
)

SigningConfigurationOverridesTypeDef = TypedDict(
    "SigningConfigurationOverridesTypeDef",
    {
        "encryptionAlgorithm": EncryptionAlgorithmType,
        "hashAlgorithm": HashAlgorithmType,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AddProfilePermissionResponseTypeDef = TypedDict(
    "AddProfilePermissionResponseTypeDef",
    {
        "revisionId": str,
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
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSigningProfileResponseTypeDef = TypedDict(
    "PutSigningProfileResponseTypeDef",
    {
        "arn": str,
        "profileVersion": str,
        "profileVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveProfilePermissionResponseTypeDef = TypedDict(
    "RemoveProfilePermissionResponseTypeDef",
    {
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSigningJobResponseTypeDef = TypedDict(
    "StartSigningJobResponseTypeDef",
    {
        "jobId": str,
        "jobOwner": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef = TypedDict(
    "_RequiredDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef",
    {
        "jobId": str,
    },
)
_OptionalDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef = TypedDict(
    "_OptionalDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef(
    _RequiredDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef,
    _OptionalDescribeSigningJobRequestSuccessfulSigningJobWaitTypeDef,
):
    pass


DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "s3": S3DestinationTypeDef,
    },
    total=False,
)

SigningProfileTypeDef = TypedDict(
    "SigningProfileTypeDef",
    {
        "profileName": str,
        "profileVersion": str,
        "profileVersionArn": str,
        "signingMaterial": SigningMaterialTypeDef,
        "signatureValidityPeriod": SignatureValidityPeriodTypeDef,
        "platformId": str,
        "platformDisplayName": str,
        "signingParameters": Dict[str, str],
        "status": SigningProfileStatusType,
        "arn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

SigningConfigurationTypeDef = TypedDict(
    "SigningConfigurationTypeDef",
    {
        "encryptionAlgorithmOptions": EncryptionAlgorithmOptionsTypeDef,
        "hashAlgorithmOptions": HashAlgorithmOptionsTypeDef,
    },
)

ListProfilePermissionsResponseTypeDef = TypedDict(
    "ListProfilePermissionsResponseTypeDef",
    {
        "revisionId": str,
        "policySizeBytes": int,
        "permissions": List[PermissionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSigningJobsRequestListSigningJobsPaginateTypeDef = TypedDict(
    "ListSigningJobsRequestListSigningJobsPaginateTypeDef",
    {
        "status": SigningStatusType,
        "platformId": str,
        "requestedBy": str,
        "isRevoked": bool,
        "signatureExpiresBefore": Union[datetime, str],
        "signatureExpiresAfter": Union[datetime, str],
        "jobInvoker": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef = TypedDict(
    "ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef",
    {
        "category": str,
        "partner": str,
        "target": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSigningProfilesRequestListSigningProfilesPaginateTypeDef = TypedDict(
    "ListSigningProfilesRequestListSigningProfilesPaginateTypeDef",
    {
        "includeCanceled": bool,
        "platformId": str,
        "statuses": Sequence[SigningProfileStatusType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SignedObjectTypeDef = TypedDict(
    "SignedObjectTypeDef",
    {
        "s3": S3SignedObjectTypeDef,
    },
    total=False,
)

SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "s3": S3SourceTypeDef,
    },
    total=False,
)

SigningPlatformOverridesTypeDef = TypedDict(
    "SigningPlatformOverridesTypeDef",
    {
        "signingConfiguration": SigningConfigurationOverridesTypeDef,
        "signingImageFormat": ImageFormatType,
    },
    total=False,
)

ListSigningProfilesResponseTypeDef = TypedDict(
    "ListSigningProfilesResponseTypeDef",
    {
        "profiles": List[SigningProfileTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSigningPlatformResponseTypeDef = TypedDict(
    "GetSigningPlatformResponseTypeDef",
    {
        "platformId": str,
        "displayName": str,
        "partner": str,
        "target": str,
        "category": Literal["AWSIoT"],
        "signingConfiguration": SigningConfigurationTypeDef,
        "signingImageFormat": SigningImageFormatTypeDef,
        "maxSizeInMB": int,
        "revocationSupported": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SigningPlatformTypeDef = TypedDict(
    "SigningPlatformTypeDef",
    {
        "platformId": str,
        "displayName": str,
        "partner": str,
        "target": str,
        "category": Literal["AWSIoT"],
        "signingConfiguration": SigningConfigurationTypeDef,
        "signingImageFormat": SigningImageFormatTypeDef,
        "maxSizeInMB": int,
        "revocationSupported": bool,
    },
    total=False,
)

SigningJobTypeDef = TypedDict(
    "SigningJobTypeDef",
    {
        "jobId": str,
        "source": SourceTypeDef,
        "signedObject": SignedObjectTypeDef,
        "signingMaterial": SigningMaterialTypeDef,
        "createdAt": datetime,
        "status": SigningStatusType,
        "isRevoked": bool,
        "profileName": str,
        "profileVersion": str,
        "platformId": str,
        "platformDisplayName": str,
        "signatureExpiresAt": datetime,
        "jobOwner": str,
        "jobInvoker": str,
    },
    total=False,
)

_RequiredStartSigningJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartSigningJobRequestRequestTypeDef",
    {
        "source": SourceTypeDef,
        "destination": DestinationTypeDef,
        "profileName": str,
        "clientRequestToken": str,
    },
)
_OptionalStartSigningJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartSigningJobRequestRequestTypeDef",
    {
        "profileOwner": str,
    },
    total=False,
)


class StartSigningJobRequestRequestTypeDef(
    _RequiredStartSigningJobRequestRequestTypeDef, _OptionalStartSigningJobRequestRequestTypeDef
):
    pass


DescribeSigningJobResponseTypeDef = TypedDict(
    "DescribeSigningJobResponseTypeDef",
    {
        "jobId": str,
        "source": SourceTypeDef,
        "signingMaterial": SigningMaterialTypeDef,
        "platformId": str,
        "platformDisplayName": str,
        "profileName": str,
        "profileVersion": str,
        "overrides": SigningPlatformOverridesTypeDef,
        "signingParameters": Dict[str, str],
        "createdAt": datetime,
        "completedAt": datetime,
        "signatureExpiresAt": datetime,
        "requestedBy": str,
        "status": SigningStatusType,
        "statusReason": str,
        "revocationRecord": SigningJobRevocationRecordTypeDef,
        "signedObject": SignedObjectTypeDef,
        "jobOwner": str,
        "jobInvoker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSigningProfileResponseTypeDef = TypedDict(
    "GetSigningProfileResponseTypeDef",
    {
        "profileName": str,
        "profileVersion": str,
        "profileVersionArn": str,
        "revocationRecord": SigningProfileRevocationRecordTypeDef,
        "signingMaterial": SigningMaterialTypeDef,
        "platformId": str,
        "platformDisplayName": str,
        "signatureValidityPeriod": SignatureValidityPeriodTypeDef,
        "overrides": SigningPlatformOverridesTypeDef,
        "signingParameters": Dict[str, str],
        "status": SigningProfileStatusType,
        "statusReason": str,
        "arn": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutSigningProfileRequestRequestTypeDef = TypedDict(
    "_RequiredPutSigningProfileRequestRequestTypeDef",
    {
        "profileName": str,
        "platformId": str,
    },
)
_OptionalPutSigningProfileRequestRequestTypeDef = TypedDict(
    "_OptionalPutSigningProfileRequestRequestTypeDef",
    {
        "signingMaterial": SigningMaterialTypeDef,
        "signatureValidityPeriod": SignatureValidityPeriodTypeDef,
        "overrides": SigningPlatformOverridesTypeDef,
        "signingParameters": Mapping[str, str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class PutSigningProfileRequestRequestTypeDef(
    _RequiredPutSigningProfileRequestRequestTypeDef, _OptionalPutSigningProfileRequestRequestTypeDef
):
    pass


ListSigningPlatformsResponseTypeDef = TypedDict(
    "ListSigningPlatformsResponseTypeDef",
    {
        "platforms": List[SigningPlatformTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSigningJobsResponseTypeDef = TypedDict(
    "ListSigningJobsResponseTypeDef",
    {
        "jobs": List[SigningJobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
