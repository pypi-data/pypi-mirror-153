"""
Type annotations for signer service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_signer.client import signerClient

    session = Session()
    client: signerClient = session.client("signer")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import SigningProfileStatusType, SigningStatusType
from .paginator import (
    ListSigningJobsPaginator,
    ListSigningPlatformsPaginator,
    ListSigningProfilesPaginator,
)
from .type_defs import (
    AddProfilePermissionResponseTypeDef,
    DescribeSigningJobResponseTypeDef,
    DestinationTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSigningPlatformResponseTypeDef,
    GetSigningProfileResponseTypeDef,
    ListProfilePermissionsResponseTypeDef,
    ListSigningJobsResponseTypeDef,
    ListSigningPlatformsResponseTypeDef,
    ListSigningProfilesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutSigningProfileResponseTypeDef,
    RemoveProfilePermissionResponseTypeDef,
    SignatureValidityPeriodTypeDef,
    SigningMaterialTypeDef,
    SigningPlatformOverridesTypeDef,
    SourceTypeDef,
    StartSigningJobResponseTypeDef,
)
from .waiter import SuccessfulSigningJobWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("signerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class signerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        signerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#exceptions)
        """

    def add_profile_permission(
        self,
        *,
        profileName: str,
        action: str,
        principal: str,
        statementId: str,
        profileVersion: str = ...,
        revisionId: str = ...
    ) -> AddProfilePermissionResponseTypeDef:
        """
        Adds cross-account permissions to a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.add_profile_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#add_profile_permission)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#can_paginate)
        """

    def cancel_signing_profile(self, *, profileName: str) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of an `ACTIVE` signing profile to `CANCELED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.cancel_signing_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#cancel_signing_profile)
        """

    def describe_signing_job(self, *, jobId: str) -> DescribeSigningJobResponseTypeDef:
        """
        Returns information about a specific code signing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.describe_signing_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#describe_signing_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#generate_presigned_url)
        """

    def get_signing_platform(self, *, platformId: str) -> GetSigningPlatformResponseTypeDef:
        """
        Returns information on a specific signing platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_signing_platform)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_signing_platform)
        """

    def get_signing_profile(
        self, *, profileName: str, profileOwner: str = ...
    ) -> GetSigningProfileResponseTypeDef:
        """
        Returns information on a specific signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_signing_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_signing_profile)
        """

    def list_profile_permissions(
        self, *, profileName: str, nextToken: str = ...
    ) -> ListProfilePermissionsResponseTypeDef:
        """
        Lists the cross-account permissions associated with a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.list_profile_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_profile_permissions)
        """

    def list_signing_jobs(
        self,
        *,
        status: SigningStatusType = ...,
        platformId: str = ...,
        requestedBy: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        isRevoked: bool = ...,
        signatureExpiresBefore: Union[datetime, str] = ...,
        signatureExpiresAfter: Union[datetime, str] = ...,
        jobInvoker: str = ...
    ) -> ListSigningJobsResponseTypeDef:
        """
        Lists all your signing jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.list_signing_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_jobs)
        """

    def list_signing_platforms(
        self,
        *,
        category: str = ...,
        partner: str = ...,
        target: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListSigningPlatformsResponseTypeDef:
        """
        Lists all signing platforms available in code signing that match the request
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.list_signing_platforms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_platforms)
        """

    def list_signing_profiles(
        self,
        *,
        includeCanceled: bool = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        platformId: str = ...,
        statuses: Sequence[SigningProfileStatusType] = ...
    ) -> ListSigningProfilesResponseTypeDef:
        """
        Lists all available signing profiles in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.list_signing_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_signing_profiles)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags associated with a signing profile resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#list_tags_for_resource)
        """

    def put_signing_profile(
        self,
        *,
        profileName: str,
        platformId: str,
        signingMaterial: SigningMaterialTypeDef = ...,
        signatureValidityPeriod: SignatureValidityPeriodTypeDef = ...,
        overrides: SigningPlatformOverridesTypeDef = ...,
        signingParameters: Mapping[str, str] = ...,
        tags: Mapping[str, str] = ...
    ) -> PutSigningProfileResponseTypeDef:
        """
        Creates a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.put_signing_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#put_signing_profile)
        """

    def remove_profile_permission(
        self, *, profileName: str, revisionId: str, statementId: str
    ) -> RemoveProfilePermissionResponseTypeDef:
        """
        Removes cross-account permissions from a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.remove_profile_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#remove_profile_permission)
        """

    def revoke_signature(
        self, *, jobId: str, reason: str, jobOwner: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a signing job to REVOKED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.revoke_signature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#revoke_signature)
        """

    def revoke_signing_profile(
        self,
        *,
        profileName: str,
        profileVersion: str,
        reason: str,
        effectiveTime: Union[datetime, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a signing profile to REVOKED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.revoke_signing_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#revoke_signing_profile)
        """

    def start_signing_job(
        self,
        *,
        source: SourceTypeDef,
        destination: DestinationTypeDef,
        profileName: str,
        clientRequestToken: str,
        profileOwner: str = ...
    ) -> StartSigningJobResponseTypeDef:
        """
        Initiates a signing job to be performed on the code provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.start_signing_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#start_signing_job)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a signing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_jobs"]
    ) -> ListSigningJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_platforms"]
    ) -> ListSigningPlatformsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_profiles"]
    ) -> ListSigningProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["successful_signing_job"]
    ) -> SuccessfulSigningJobWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signer/client/#get_waiter)
        """
