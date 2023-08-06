"""
Type annotations for mediastore service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediastore.client import MediaStoreClient

    session = Session()
    client: MediaStoreClient = session.client("mediastore")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListContainersPaginator
from .type_defs import (
    CorsRuleTypeDef,
    CreateContainerOutputTypeDef,
    DescribeContainerOutputTypeDef,
    GetContainerPolicyOutputTypeDef,
    GetCorsPolicyOutputTypeDef,
    GetLifecyclePolicyOutputTypeDef,
    GetMetricPolicyOutputTypeDef,
    ListContainersOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    MetricPolicyTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaStoreClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ContainerInUseException: Type[BotocoreClientError]
    ContainerNotFoundException: Type[BotocoreClientError]
    CorsPolicyNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]


class MediaStoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#can_paginate)
        """

    def create_container(
        self, *, ContainerName: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateContainerOutputTypeDef:
        """
        Creates a storage container to hold objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.create_container)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#create_container)
        """

    def delete_container(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Deletes the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.delete_container)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_container)
        """

    def delete_container_policy(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Deletes the access policy that is associated with the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.delete_container_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_container_policy)
        """

    def delete_cors_policy(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Deletes the cross-origin resource sharing (CORS) configuration information that
        is set for the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.delete_cors_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_cors_policy)
        """

    def delete_lifecycle_policy(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Removes an object lifecycle policy from a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.delete_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_lifecycle_policy)
        """

    def delete_metric_policy(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Deletes the metric policy that is associated with the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.delete_metric_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_metric_policy)
        """

    def describe_container(self, *, ContainerName: str = ...) -> DescribeContainerOutputTypeDef:
        """
        Retrieves the properties of the requested container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.describe_container)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#describe_container)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#generate_presigned_url)
        """

    def get_container_policy(self, *, ContainerName: str) -> GetContainerPolicyOutputTypeDef:
        """
        Retrieves the access policy for the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.get_container_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_container_policy)
        """

    def get_cors_policy(self, *, ContainerName: str) -> GetCorsPolicyOutputTypeDef:
        """
        Returns the cross-origin resource sharing (CORS) configuration information that
        is set for the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.get_cors_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_cors_policy)
        """

    def get_lifecycle_policy(self, *, ContainerName: str) -> GetLifecyclePolicyOutputTypeDef:
        """
        Retrieves the object lifecycle policy that is assigned to a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.get_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_lifecycle_policy)
        """

    def get_metric_policy(self, *, ContainerName: str) -> GetMetricPolicyOutputTypeDef:
        """
        Returns the metric policy for the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.get_metric_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_metric_policy)
        """

    def list_containers(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListContainersOutputTypeDef:
        """
        Lists the properties of all containers in AWS Elemental MediaStore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.list_containers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#list_containers)
        """

    def list_tags_for_resource(self, *, Resource: str) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of the tags assigned to the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#list_tags_for_resource)
        """

    def put_container_policy(self, *, ContainerName: str, Policy: str) -> Dict[str, Any]:
        """
        Creates an access policy for the specified container to restrict the users and
        clients that can access it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.put_container_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_container_policy)
        """

    def put_cors_policy(
        self, *, ContainerName: str, CorsPolicy: Sequence[CorsRuleTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the cross-origin resource sharing (CORS) configuration on a container so
        that the container can service cross-origin requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.put_cors_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_cors_policy)
        """

    def put_lifecycle_policy(self, *, ContainerName: str, LifecyclePolicy: str) -> Dict[str, Any]:
        """
        Writes an object lifecycle policy to a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.put_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_lifecycle_policy)
        """

    def put_metric_policy(
        self, *, ContainerName: str, MetricPolicy: MetricPolicyTypeDef
    ) -> Dict[str, Any]:
        """
        The metric policy that you want to add to the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.put_metric_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_metric_policy)
        """

    def start_access_logging(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Starts access logging on the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.start_access_logging)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#start_access_logging)
        """

    def stop_access_logging(self, *, ContainerName: str) -> Dict[str, Any]:
        """
        Stops access logging on the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.stop_access_logging)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#stop_access_logging)
        """

    def tag_resource(self, *, Resource: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified AWS Elemental MediaStore container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#tag_resource)
        """

    def untag_resource(self, *, Resource: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#untag_resource)
        """

    def get_paginator(self, operation_name: Literal["list_containers"]) -> ListContainersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_paginator)
        """
