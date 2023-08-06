"""
Type annotations for dlm service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dlm.client import DLMClient

    session = Session()
    client: DLMClient = session.client("dlm")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    GettablePolicyStateValuesType,
    ResourceTypeValuesType,
    SettablePolicyStateValuesType,
)
from .type_defs import (
    CreateLifecyclePolicyResponseTypeDef,
    GetLifecyclePoliciesResponseTypeDef,
    GetLifecyclePolicyResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PolicyDetailsTypeDef,
)

__all__ = ("DLMClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class DLMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DLMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#can_paginate)
        """

    def create_lifecycle_policy(
        self,
        *,
        ExecutionRoleArn: str,
        Description: str,
        State: SettablePolicyStateValuesType,
        PolicyDetails: PolicyDetailsTypeDef,
        Tags: Mapping[str, str] = ...
    ) -> CreateLifecyclePolicyResponseTypeDef:
        """
        Creates a policy to manage the lifecycle of the specified Amazon Web Services
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.create_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#create_lifecycle_policy)
        """

    def delete_lifecycle_policy(self, *, PolicyId: str) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle policy and halts the automated operations that
        the policy specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.delete_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#delete_lifecycle_policy)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#generate_presigned_url)
        """

    def get_lifecycle_policies(
        self,
        *,
        PolicyIds: Sequence[str] = ...,
        State: GettablePolicyStateValuesType = ...,
        ResourceTypes: Sequence[ResourceTypeValuesType] = ...,
        TargetTags: Sequence[str] = ...,
        TagsToAdd: Sequence[str] = ...
    ) -> GetLifecyclePoliciesResponseTypeDef:
        """
        Gets summary information about all or the specified data lifecycle policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.get_lifecycle_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#get_lifecycle_policies)
        """

    def get_lifecycle_policy(self, *, PolicyId: str) -> GetLifecyclePolicyResponseTypeDef:
        """
        Gets detailed information about the specified lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.get_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#get_lifecycle_policy)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#untag_resource)
        """

    def update_lifecycle_policy(
        self,
        *,
        PolicyId: str,
        ExecutionRoleArn: str = ...,
        State: SettablePolicyStateValuesType = ...,
        Description: str = ...,
        PolicyDetails: PolicyDetailsTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Updates the specified lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM.Client.update_lifecycle_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/client/#update_lifecycle_policy)
        """
