"""
Type annotations for ecr-public service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/type_defs/)

Usage::

    ```python
    from mypy_boto3_ecr_public.type_defs import AuthorizationDataTypeDef

    data: AuthorizationDataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ImageFailureCodeType,
    LayerAvailabilityType,
    LayerFailureCodeType,
    RegistryAliasStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AuthorizationDataTypeDef",
    "BatchCheckLayerAvailabilityRequestRequestTypeDef",
    "LayerFailureTypeDef",
    "LayerTypeDef",
    "ResponseMetadataTypeDef",
    "ImageIdentifierTypeDef",
    "CompleteLayerUploadRequestRequestTypeDef",
    "RepositoryCatalogDataInputTypeDef",
    "TagTypeDef",
    "RepositoryCatalogDataTypeDef",
    "RepositoryTypeDef",
    "DeleteRepositoryPolicyRequestRequestTypeDef",
    "DeleteRepositoryRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeImageTagsRequestRequestTypeDef",
    "ImageDetailTypeDef",
    "DescribeRegistriesRequestRequestTypeDef",
    "DescribeRepositoriesRequestRequestTypeDef",
    "RegistryCatalogDataTypeDef",
    "GetRepositoryCatalogDataRequestRequestTypeDef",
    "GetRepositoryPolicyRequestRequestTypeDef",
    "ReferencedImageDetailTypeDef",
    "InitiateLayerUploadRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutImageRequestRequestTypeDef",
    "PutRegistryCatalogDataRequestRequestTypeDef",
    "RegistryAliasTypeDef",
    "SetRepositoryPolicyRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UploadLayerPartRequestRequestTypeDef",
    "BatchCheckLayerAvailabilityResponseTypeDef",
    "CompleteLayerUploadResponseTypeDef",
    "DeleteRepositoryPolicyResponseTypeDef",
    "GetAuthorizationTokenResponseTypeDef",
    "GetRepositoryPolicyResponseTypeDef",
    "InitiateLayerUploadResponseTypeDef",
    "SetRepositoryPolicyResponseTypeDef",
    "UploadLayerPartResponseTypeDef",
    "BatchDeleteImageRequestRequestTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "ImageFailureTypeDef",
    "ImageTypeDef",
    "PutRepositoryCatalogDataRequestRequestTypeDef",
    "CreateRepositoryRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "GetRepositoryCatalogDataResponseTypeDef",
    "PutRepositoryCatalogDataResponseTypeDef",
    "CreateRepositoryResponseTypeDef",
    "DeleteRepositoryResponseTypeDef",
    "DescribeRepositoriesResponseTypeDef",
    "DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef",
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    "DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef",
    "DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef",
    "DescribeImagesResponseTypeDef",
    "GetRegistryCatalogDataResponseTypeDef",
    "PutRegistryCatalogDataResponseTypeDef",
    "ImageTagDetailTypeDef",
    "RegistryTypeDef",
    "BatchDeleteImageResponseTypeDef",
    "PutImageResponseTypeDef",
    "DescribeImageTagsResponseTypeDef",
    "DescribeRegistriesResponseTypeDef",
)

AuthorizationDataTypeDef = TypedDict(
    "AuthorizationDataTypeDef",
    {
        "authorizationToken": str,
        "expiresAt": datetime,
    },
    total=False,
)

_RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef = TypedDict(
    "_RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef",
    {
        "repositoryName": str,
        "layerDigests": Sequence[str],
    },
)
_OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef = TypedDict(
    "_OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class BatchCheckLayerAvailabilityRequestRequestTypeDef(
    _RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef,
    _OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef,
):
    pass


LayerFailureTypeDef = TypedDict(
    "LayerFailureTypeDef",
    {
        "layerDigest": str,
        "failureCode": LayerFailureCodeType,
        "failureReason": str,
    },
    total=False,
)

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "layerDigest": str,
        "layerAvailability": LayerAvailabilityType,
        "layerSize": int,
        "mediaType": str,
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

ImageIdentifierTypeDef = TypedDict(
    "ImageIdentifierTypeDef",
    {
        "imageDigest": str,
        "imageTag": str,
    },
    total=False,
)

_RequiredCompleteLayerUploadRequestRequestTypeDef = TypedDict(
    "_RequiredCompleteLayerUploadRequestRequestTypeDef",
    {
        "repositoryName": str,
        "uploadId": str,
        "layerDigests": Sequence[str],
    },
)
_OptionalCompleteLayerUploadRequestRequestTypeDef = TypedDict(
    "_OptionalCompleteLayerUploadRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class CompleteLayerUploadRequestRequestTypeDef(
    _RequiredCompleteLayerUploadRequestRequestTypeDef,
    _OptionalCompleteLayerUploadRequestRequestTypeDef,
):
    pass


RepositoryCatalogDataInputTypeDef = TypedDict(
    "RepositoryCatalogDataInputTypeDef",
    {
        "description": str,
        "architectures": Sequence[str],
        "operatingSystems": Sequence[str],
        "logoImageBlob": Union[str, bytes, IO[Any], StreamingBody],
        "aboutText": str,
        "usageText": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

RepositoryCatalogDataTypeDef = TypedDict(
    "RepositoryCatalogDataTypeDef",
    {
        "description": str,
        "architectures": List[str],
        "operatingSystems": List[str],
        "logoUrl": str,
        "aboutText": str,
        "usageText": str,
        "marketplaceCertified": bool,
    },
    total=False,
)

RepositoryTypeDef = TypedDict(
    "RepositoryTypeDef",
    {
        "repositoryArn": str,
        "registryId": str,
        "repositoryName": str,
        "repositoryUri": str,
        "createdAt": datetime,
    },
    total=False,
)

_RequiredDeleteRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDeleteRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class DeleteRepositoryPolicyRequestRequestTypeDef(
    _RequiredDeleteRepositoryPolicyRequestRequestTypeDef,
    _OptionalDeleteRepositoryPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeleteRepositoryRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRepositoryRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDeleteRepositoryRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRepositoryRequestRequestTypeDef",
    {
        "registryId": str,
        "force": bool,
    },
    total=False,
)


class DeleteRepositoryRequestRequestTypeDef(
    _RequiredDeleteRepositoryRequestRequestTypeDef, _OptionalDeleteRepositoryRequestRequestTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredDescribeImageTagsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImageTagsRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImageTagsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImageTagsRequestRequestTypeDef",
    {
        "registryId": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class DescribeImageTagsRequestRequestTypeDef(
    _RequiredDescribeImageTagsRequestRequestTypeDef, _OptionalDescribeImageTagsRequestRequestTypeDef
):
    pass


ImageDetailTypeDef = TypedDict(
    "ImageDetailTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageDigest": str,
        "imageTags": List[str],
        "imageSizeInBytes": int,
        "imagePushedAt": datetime,
        "imageManifestMediaType": str,
        "artifactMediaType": str,
    },
    total=False,
)

DescribeRegistriesRequestRequestTypeDef = TypedDict(
    "DescribeRegistriesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

DescribeRepositoriesRequestRequestTypeDef = TypedDict(
    "DescribeRepositoriesRequestRequestTypeDef",
    {
        "registryId": str,
        "repositoryNames": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

RegistryCatalogDataTypeDef = TypedDict(
    "RegistryCatalogDataTypeDef",
    {
        "displayName": str,
    },
    total=False,
)

_RequiredGetRepositoryCatalogDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetRepositoryCatalogDataRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetRepositoryCatalogDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetRepositoryCatalogDataRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class GetRepositoryCatalogDataRequestRequestTypeDef(
    _RequiredGetRepositoryCatalogDataRequestRequestTypeDef,
    _OptionalGetRepositoryCatalogDataRequestRequestTypeDef,
):
    pass


_RequiredGetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class GetRepositoryPolicyRequestRequestTypeDef(
    _RequiredGetRepositoryPolicyRequestRequestTypeDef,
    _OptionalGetRepositoryPolicyRequestRequestTypeDef,
):
    pass


ReferencedImageDetailTypeDef = TypedDict(
    "ReferencedImageDetailTypeDef",
    {
        "imageDigest": str,
        "imageSizeInBytes": int,
        "imagePushedAt": datetime,
        "imageManifestMediaType": str,
        "artifactMediaType": str,
    },
    total=False,
)

_RequiredInitiateLayerUploadRequestRequestTypeDef = TypedDict(
    "_RequiredInitiateLayerUploadRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalInitiateLayerUploadRequestRequestTypeDef = TypedDict(
    "_OptionalInitiateLayerUploadRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class InitiateLayerUploadRequestRequestTypeDef(
    _RequiredInitiateLayerUploadRequestRequestTypeDef,
    _OptionalInitiateLayerUploadRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredPutImageRequestRequestTypeDef = TypedDict(
    "_RequiredPutImageRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageManifest": str,
    },
)
_OptionalPutImageRequestRequestTypeDef = TypedDict(
    "_OptionalPutImageRequestRequestTypeDef",
    {
        "registryId": str,
        "imageManifestMediaType": str,
        "imageTag": str,
        "imageDigest": str,
    },
    total=False,
)


class PutImageRequestRequestTypeDef(
    _RequiredPutImageRequestRequestTypeDef, _OptionalPutImageRequestRequestTypeDef
):
    pass


PutRegistryCatalogDataRequestRequestTypeDef = TypedDict(
    "PutRegistryCatalogDataRequestRequestTypeDef",
    {
        "displayName": str,
    },
    total=False,
)

RegistryAliasTypeDef = TypedDict(
    "RegistryAliasTypeDef",
    {
        "name": str,
        "status": RegistryAliasStatusType,
        "primaryRegistryAlias": bool,
        "defaultRegistryAlias": bool,
    },
)

_RequiredSetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredSetRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
        "policyText": str,
    },
)
_OptionalSetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalSetRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
        "force": bool,
    },
    total=False,
)


class SetRepositoryPolicyRequestRequestTypeDef(
    _RequiredSetRepositoryPolicyRequestRequestTypeDef,
    _OptionalSetRepositoryPolicyRequestRequestTypeDef,
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUploadLayerPartRequestRequestTypeDef = TypedDict(
    "_RequiredUploadLayerPartRequestRequestTypeDef",
    {
        "repositoryName": str,
        "uploadId": str,
        "partFirstByte": int,
        "partLastByte": int,
        "layerPartBlob": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalUploadLayerPartRequestRequestTypeDef = TypedDict(
    "_OptionalUploadLayerPartRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class UploadLayerPartRequestRequestTypeDef(
    _RequiredUploadLayerPartRequestRequestTypeDef, _OptionalUploadLayerPartRequestRequestTypeDef
):
    pass


BatchCheckLayerAvailabilityResponseTypeDef = TypedDict(
    "BatchCheckLayerAvailabilityResponseTypeDef",
    {
        "layers": List[LayerTypeDef],
        "failures": List[LayerFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CompleteLayerUploadResponseTypeDef = TypedDict(
    "CompleteLayerUploadResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "uploadId": str,
        "layerDigest": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryPolicyResponseTypeDef = TypedDict(
    "DeleteRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAuthorizationTokenResponseTypeDef = TypedDict(
    "GetAuthorizationTokenResponseTypeDef",
    {
        "authorizationData": AuthorizationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositoryPolicyResponseTypeDef = TypedDict(
    "GetRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitiateLayerUploadResponseTypeDef = TypedDict(
    "InitiateLayerUploadResponseTypeDef",
    {
        "uploadId": str,
        "partSize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetRepositoryPolicyResponseTypeDef = TypedDict(
    "SetRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UploadLayerPartResponseTypeDef = TypedDict(
    "UploadLayerPartResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "uploadId": str,
        "lastByteReceived": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchDeleteImageRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteImageRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
    },
)
_OptionalBatchDeleteImageRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteImageRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class BatchDeleteImageRequestRequestTypeDef(
    _RequiredBatchDeleteImageRequestRequestTypeDef, _OptionalBatchDeleteImageRequestRequestTypeDef
):
    pass


_RequiredDescribeImagesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImagesRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImagesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImagesRequestRequestTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class DescribeImagesRequestRequestTypeDef(
    _RequiredDescribeImagesRequestRequestTypeDef, _OptionalDescribeImagesRequestRequestTypeDef
):
    pass


ImageFailureTypeDef = TypedDict(
    "ImageFailureTypeDef",
    {
        "imageId": ImageIdentifierTypeDef,
        "failureCode": ImageFailureCodeType,
        "failureReason": str,
    },
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageManifest": str,
        "imageManifestMediaType": str,
    },
    total=False,
)

_RequiredPutRepositoryCatalogDataRequestRequestTypeDef = TypedDict(
    "_RequiredPutRepositoryCatalogDataRequestRequestTypeDef",
    {
        "repositoryName": str,
        "catalogData": RepositoryCatalogDataInputTypeDef,
    },
)
_OptionalPutRepositoryCatalogDataRequestRequestTypeDef = TypedDict(
    "_OptionalPutRepositoryCatalogDataRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class PutRepositoryCatalogDataRequestRequestTypeDef(
    _RequiredPutRepositoryCatalogDataRequestRequestTypeDef,
    _OptionalPutRepositoryCatalogDataRequestRequestTypeDef,
):
    pass


_RequiredCreateRepositoryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalCreateRepositoryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryRequestRequestTypeDef",
    {
        "catalogData": RepositoryCatalogDataInputTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRepositoryRequestRequestTypeDef(
    _RequiredCreateRepositoryRequestRequestTypeDef, _OptionalCreateRepositoryRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

GetRepositoryCatalogDataResponseTypeDef = TypedDict(
    "GetRepositoryCatalogDataResponseTypeDef",
    {
        "catalogData": RepositoryCatalogDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRepositoryCatalogDataResponseTypeDef = TypedDict(
    "PutRepositoryCatalogDataResponseTypeDef",
    {
        "catalogData": RepositoryCatalogDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRepositoryResponseTypeDef = TypedDict(
    "CreateRepositoryResponseTypeDef",
    {
        "repository": RepositoryTypeDef,
        "catalogData": RepositoryCatalogDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryResponseTypeDef = TypedDict(
    "DeleteRepositoryResponseTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRepositoriesResponseTypeDef = TypedDict(
    "DescribeRepositoriesResponseTypeDef",
    {
        "repositories": List[RepositoryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef = TypedDict(
    "_RequiredDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef = TypedDict(
    "_OptionalDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef",
    {
        "registryId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef(
    _RequiredDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef,
    _OptionalDescribeImageTagsRequestDescribeImageTagsPaginateTypeDef,
):
    pass


_RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "_RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "_OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeImagesRequestDescribeImagesPaginateTypeDef(
    _RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef,
    _OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef,
):
    pass


DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef = TypedDict(
    "DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef = TypedDict(
    "DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef",
    {
        "registryId": str,
        "repositoryNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeImagesResponseTypeDef = TypedDict(
    "DescribeImagesResponseTypeDef",
    {
        "imageDetails": List[ImageDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRegistryCatalogDataResponseTypeDef = TypedDict(
    "GetRegistryCatalogDataResponseTypeDef",
    {
        "registryCatalogData": RegistryCatalogDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRegistryCatalogDataResponseTypeDef = TypedDict(
    "PutRegistryCatalogDataResponseTypeDef",
    {
        "registryCatalogData": RegistryCatalogDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImageTagDetailTypeDef = TypedDict(
    "ImageTagDetailTypeDef",
    {
        "imageTag": str,
        "createdAt": datetime,
        "imageDetail": ReferencedImageDetailTypeDef,
    },
    total=False,
)

RegistryTypeDef = TypedDict(
    "RegistryTypeDef",
    {
        "registryId": str,
        "registryArn": str,
        "registryUri": str,
        "verified": bool,
        "aliases": List[RegistryAliasTypeDef],
    },
)

BatchDeleteImageResponseTypeDef = TypedDict(
    "BatchDeleteImageResponseTypeDef",
    {
        "imageIds": List[ImageIdentifierTypeDef],
        "failures": List[ImageFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutImageResponseTypeDef = TypedDict(
    "PutImageResponseTypeDef",
    {
        "image": ImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImageTagsResponseTypeDef = TypedDict(
    "DescribeImageTagsResponseTypeDef",
    {
        "imageTagDetails": List[ImageTagDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRegistriesResponseTypeDef = TypedDict(
    "DescribeRegistriesResponseTypeDef",
    {
        "registries": List[RegistryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
