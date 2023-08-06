"""
Type annotations for sagemaker-a2i-runtime service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
    from mypy_boto3_sagemaker_a2i_runtime.paginator import (
        ListHumanLoopsPaginator,
    )

    session = Session()
    client: AugmentedAIRuntimeClient = session.client("sagemaker-a2i-runtime")

    list_human_loops_paginator: ListHumanLoopsPaginator = client.get_paginator("list_human_loops")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import SortOrderType
from .type_defs import ListHumanLoopsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListHumanLoopsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListHumanLoopsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Paginator.ListHumanLoops)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
    """

    def paginate(
        self,
        *,
        FlowDefinitionArn: str,
        CreationTimeAfter: Union[datetime, str] = ...,
        CreationTimeBefore: Union[datetime, str] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHumanLoopsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Paginator.ListHumanLoops.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
        """
