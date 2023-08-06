"""
Type annotations for sagemaker-a2i-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient

    session = Session()
    client: AugmentedAIRuntimeClient = session.client("sagemaker-a2i-runtime")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import SortOrderType
from .paginator import ListHumanLoopsPaginator
from .type_defs import (
    DescribeHumanLoopResponseTypeDef,
    HumanLoopDataAttributesTypeDef,
    HumanLoopInputTypeDef,
    ListHumanLoopsResponseTypeDef,
    StartHumanLoopResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AugmentedAIRuntimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AugmentedAIRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AugmentedAIRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#can_paginate)
        """

    def delete_human_loop(self, *, HumanLoopName: str) -> Dict[str, Any]:
        """
        Deletes the specified human loop for a flow definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.delete_human_loop)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#delete_human_loop)
        """

    def describe_human_loop(self, *, HumanLoopName: str) -> DescribeHumanLoopResponseTypeDef:
        """
        Returns information about the specified human loop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.describe_human_loop)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#describe_human_loop)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#generate_presigned_url)
        """

    def list_human_loops(
        self,
        *,
        FlowDefinitionArn: str,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        SortOrder: SortOrderType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListHumanLoopsResponseTypeDef:
        """
        Returns information about human loops, given the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.list_human_loops)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#list_human_loops)
        """

    def start_human_loop(
        self,
        *,
        HumanLoopName: str,
        FlowDefinitionArn: str,
        HumanLoopInput: HumanLoopInputTypeDef,
        DataAttributes: HumanLoopDataAttributesTypeDef = ...
    ) -> StartHumanLoopResponseTypeDef:
        """
        Starts a human loop, provided that at least one activation condition is met.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.start_human_loop)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#start_human_loop)
        """

    def stop_human_loop(self, *, HumanLoopName: str) -> Dict[str, Any]:
        """
        Stops the specified human loop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.stop_human_loop)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#stop_human_loop)
        """

    def get_paginator(self, operation_name: Literal["list_human_loops"]) -> ListHumanLoopsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/client/#get_paginator)
        """
