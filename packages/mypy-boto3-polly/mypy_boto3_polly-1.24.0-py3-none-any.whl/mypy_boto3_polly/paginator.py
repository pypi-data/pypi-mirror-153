"""
Type annotations for polly service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_polly.client import PollyClient
    from mypy_boto3_polly.paginator import (
        DescribeVoicesPaginator,
        ListLexiconsPaginator,
        ListSpeechSynthesisTasksPaginator,
    )

    session = Session()
    client: PollyClient = session.client("polly")

    describe_voices_paginator: DescribeVoicesPaginator = client.get_paginator("describe_voices")
    list_lexicons_paginator: ListLexiconsPaginator = client.get_paginator("list_lexicons")
    list_speech_synthesis_tasks_paginator: ListSpeechSynthesisTasksPaginator = client.get_paginator("list_speech_synthesis_tasks")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import EngineType, LanguageCodeType, TaskStatusType
from .type_defs import (
    DescribeVoicesOutputTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeVoicesPaginator", "ListLexiconsPaginator", "ListSpeechSynthesisTasksPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeVoicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.DescribeVoices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#describevoicespaginator)
    """

    def paginate(
        self,
        *,
        Engine: EngineType = ...,
        LanguageCode: LanguageCodeType = ...,
        IncludeAdditionalLanguageCodes: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeVoicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.DescribeVoices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#describevoicespaginator)
        """


class ListLexiconsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.ListLexicons)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listlexiconspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLexiconsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.ListLexicons.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listlexiconspaginator)
        """


class ListSpeechSynthesisTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.ListSpeechSynthesisTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listspeechsynthesistaskspaginator)
    """

    def paginate(
        self, *, Status: TaskStatusType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSpeechSynthesisTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Paginator.ListSpeechSynthesisTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/paginators/#listspeechsynthesistaskspaginator)
        """
