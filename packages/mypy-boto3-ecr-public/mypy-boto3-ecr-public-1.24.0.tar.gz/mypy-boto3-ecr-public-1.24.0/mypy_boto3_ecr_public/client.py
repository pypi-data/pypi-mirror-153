"""
Type annotations for ecr-public service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ecr_public.client import ECRPublicClient

    session = Session()
    client: ECRPublicClient = session.client("ecr-public")
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .paginator import (
    DescribeImagesPaginator,
    DescribeImageTagsPaginator,
    DescribeRegistriesPaginator,
    DescribeRepositoriesPaginator,
)
from .type_defs import (
    BatchCheckLayerAvailabilityResponseTypeDef,
    BatchDeleteImageResponseTypeDef,
    CompleteLayerUploadResponseTypeDef,
    CreateRepositoryResponseTypeDef,
    DeleteRepositoryPolicyResponseTypeDef,
    DeleteRepositoryResponseTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesResponseTypeDef,
    GetAuthorizationTokenResponseTypeDef,
    GetRegistryCatalogDataResponseTypeDef,
    GetRepositoryCatalogDataResponseTypeDef,
    GetRepositoryPolicyResponseTypeDef,
    ImageIdentifierTypeDef,
    InitiateLayerUploadResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutImageResponseTypeDef,
    PutRegistryCatalogDataResponseTypeDef,
    PutRepositoryCatalogDataResponseTypeDef,
    RepositoryCatalogDataInputTypeDef,
    SetRepositoryPolicyResponseTypeDef,
    TagTypeDef,
    UploadLayerPartResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ECRPublicClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    EmptyUploadException: Type[BotocoreClientError]
    ImageAlreadyExistsException: Type[BotocoreClientError]
    ImageDigestDoesNotMatchException: Type[BotocoreClientError]
    ImageNotFoundException: Type[BotocoreClientError]
    ImageTagAlreadyExistsException: Type[BotocoreClientError]
    InvalidLayerException: Type[BotocoreClientError]
    InvalidLayerPartException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidTagParameterException: Type[BotocoreClientError]
    LayerAlreadyExistsException: Type[BotocoreClientError]
    LayerPartTooSmallException: Type[BotocoreClientError]
    LayersNotFoundException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ReferencedImagesNotFoundException: Type[BotocoreClientError]
    RegistryNotFoundException: Type[BotocoreClientError]
    RepositoryAlreadyExistsException: Type[BotocoreClientError]
    RepositoryNotEmptyException: Type[BotocoreClientError]
    RepositoryNotFoundException: Type[BotocoreClientError]
    RepositoryPolicyNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedCommandException: Type[BotocoreClientError]
    UploadNotFoundException: Type[BotocoreClientError]


class ECRPublicClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECRPublicClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#exceptions)
        """

    def batch_check_layer_availability(
        self, *, repositoryName: str, layerDigests: Sequence[str], registryId: str = ...
    ) -> BatchCheckLayerAvailabilityResponseTypeDef:
        """
        Checks the availability of one or more image layers within a repository in a
        public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.batch_check_layer_availability)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#batch_check_layer_availability)
        """

    def batch_delete_image(
        self,
        *,
        repositoryName: str,
        imageIds: Sequence[ImageIdentifierTypeDef],
        registryId: str = ...
    ) -> BatchDeleteImageResponseTypeDef:
        """
        Deletes a list of specified images within a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.batch_delete_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#batch_delete_image)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#can_paginate)
        """

    def complete_layer_upload(
        self,
        *,
        repositoryName: str,
        uploadId: str,
        layerDigests: Sequence[str],
        registryId: str = ...
    ) -> CompleteLayerUploadResponseTypeDef:
        """
        Informs Amazon ECR that the image layer upload has completed for a specified
        public registry, repository name, and upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.complete_layer_upload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#complete_layer_upload)
        """

    def create_repository(
        self,
        *,
        repositoryName: str,
        catalogData: RepositoryCatalogDataInputTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateRepositoryResponseTypeDef:
        """
        Creates a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.create_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#create_repository)
        """

    def delete_repository(
        self, *, repositoryName: str, registryId: str = ..., force: bool = ...
    ) -> DeleteRepositoryResponseTypeDef:
        """
        Deletes a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.delete_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#delete_repository)
        """

    def delete_repository_policy(
        self, *, repositoryName: str, registryId: str = ...
    ) -> DeleteRepositoryPolicyResponseTypeDef:
        """
        Deletes the repository policy associated with the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.delete_repository_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#delete_repository_policy)
        """

    def describe_image_tags(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeImageTagsResponseTypeDef:
        """
        Returns the image tag details for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_image_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#describe_image_tags)
        """

    def describe_images(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        imageIds: Sequence[ImageIdentifierTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeImagesResponseTypeDef:
        """
        Returns metadata about the images in a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_images)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#describe_images)
        """

    def describe_registries(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> DescribeRegistriesResponseTypeDef:
        """
        Returns details for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_registries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#describe_registries)
        """

    def describe_repositories(
        self,
        *,
        registryId: str = ...,
        repositoryNames: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeRepositoriesResponseTypeDef:
        """
        Describes repositories in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_repositories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#describe_repositories)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#generate_presigned_url)
        """

    def get_authorization_token(self) -> GetAuthorizationTokenResponseTypeDef:
        """
        Retrieves an authorization token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_authorization_token)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_authorization_token)
        """

    def get_registry_catalog_data(self) -> GetRegistryCatalogDataResponseTypeDef:
        """
        Retrieves catalog metadata for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_registry_catalog_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_registry_catalog_data)
        """

    def get_repository_catalog_data(
        self, *, repositoryName: str, registryId: str = ...
    ) -> GetRepositoryCatalogDataResponseTypeDef:
        """
        Retrieve catalog metadata for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_repository_catalog_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_repository_catalog_data)
        """

    def get_repository_policy(
        self, *, repositoryName: str, registryId: str = ...
    ) -> GetRepositoryPolicyResponseTypeDef:
        """
        Retrieves the repository policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_repository_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_repository_policy)
        """

    def initiate_layer_upload(
        self, *, repositoryName: str, registryId: str = ...
    ) -> InitiateLayerUploadResponseTypeDef:
        """
        Notifies Amazon ECR that you intend to upload an image layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.initiate_layer_upload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#initiate_layer_upload)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECR Public resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#list_tags_for_resource)
        """

    def put_image(
        self,
        *,
        repositoryName: str,
        imageManifest: str,
        registryId: str = ...,
        imageManifestMediaType: str = ...,
        imageTag: str = ...,
        imageDigest: str = ...
    ) -> PutImageResponseTypeDef:
        """
        Creates or updates the image manifest and tags associated with an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#put_image)
        """

    def put_registry_catalog_data(
        self, *, displayName: str = ...
    ) -> PutRegistryCatalogDataResponseTypeDef:
        """
        Create or updates the catalog data for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_registry_catalog_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#put_registry_catalog_data)
        """

    def put_repository_catalog_data(
        self,
        *,
        repositoryName: str,
        catalogData: RepositoryCatalogDataInputTypeDef,
        registryId: str = ...
    ) -> PutRepositoryCatalogDataResponseTypeDef:
        """
        Creates or updates the catalog data for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_repository_catalog_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#put_repository_catalog_data)
        """

    def set_repository_policy(
        self, *, repositoryName: str, policyText: str, registryId: str = ..., force: bool = ...
    ) -> SetRepositoryPolicyResponseTypeDef:
        """
        Applies a repository policy to the specified public repository to control access
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.set_repository_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#set_repository_policy)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#untag_resource)
        """

    def upload_layer_part(
        self,
        *,
        repositoryName: str,
        uploadId: str,
        partFirstByte: int,
        partLastByte: int,
        layerPartBlob: Union[str, bytes, IO[Any], StreamingBody],
        registryId: str = ...
    ) -> UploadLayerPartResponseTypeDef:
        """
        Uploads an image layer part to Amazon ECR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.upload_layer_part)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#upload_layer_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_image_tags"]
    ) -> DescribeImageTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_registries"]
    ) -> DescribeRegistriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_repositories"]
    ) -> DescribeRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/client/#get_paginator)
        """
