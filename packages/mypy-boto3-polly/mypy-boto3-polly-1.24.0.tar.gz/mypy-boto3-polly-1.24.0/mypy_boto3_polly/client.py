"""
Type annotations for polly service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_polly.client import PollyClient

    session = Session()
    client: PollyClient = session.client("polly")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    EngineType,
    LanguageCodeType,
    OutputFormatType,
    SpeechMarkTypeType,
    TaskStatusType,
    TextTypeType,
    VoiceIdType,
)
from .paginator import (
    DescribeVoicesPaginator,
    ListLexiconsPaginator,
    ListSpeechSynthesisTasksPaginator,
)
from .type_defs import (
    DescribeVoicesOutputTypeDef,
    GetLexiconOutputTypeDef,
    GetSpeechSynthesisTaskOutputTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
    StartSpeechSynthesisTaskOutputTypeDef,
    SynthesizeSpeechOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("PollyClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    EngineNotSupportedException: Type[BotocoreClientError]
    InvalidLexiconException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidS3BucketException: Type[BotocoreClientError]
    InvalidS3KeyException: Type[BotocoreClientError]
    InvalidSampleRateException: Type[BotocoreClientError]
    InvalidSnsTopicArnException: Type[BotocoreClientError]
    InvalidSsmlException: Type[BotocoreClientError]
    InvalidTaskIdException: Type[BotocoreClientError]
    LanguageNotSupportedException: Type[BotocoreClientError]
    LexiconNotFoundException: Type[BotocoreClientError]
    LexiconSizeExceededException: Type[BotocoreClientError]
    MarksNotSupportedForFormatException: Type[BotocoreClientError]
    MaxLexemeLengthExceededException: Type[BotocoreClientError]
    MaxLexiconsNumberExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    SsmlMarksNotSupportedForTextTypeException: Type[BotocoreClientError]
    SynthesisTaskNotFoundException: Type[BotocoreClientError]
    TextLengthExceededException: Type[BotocoreClientError]
    UnsupportedPlsAlphabetException: Type[BotocoreClientError]
    UnsupportedPlsLanguageException: Type[BotocoreClientError]


class PollyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PollyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#can_paginate)
        """

    def delete_lexicon(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified pronunciation lexicon stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.delete_lexicon)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#delete_lexicon)
        """

    def describe_voices(
        self,
        *,
        Engine: EngineType = ...,
        LanguageCode: LanguageCodeType = ...,
        IncludeAdditionalLanguageCodes: bool = ...,
        NextToken: str = ...
    ) -> DescribeVoicesOutputTypeDef:
        """
        Returns the list of voices that are available for use when requesting speech
        synthesis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.describe_voices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#describe_voices)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#generate_presigned_url)
        """

    def get_lexicon(self, *, Name: str) -> GetLexiconOutputTypeDef:
        """
        Returns the content of the specified pronunciation lexicon stored in an Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.get_lexicon)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#get_lexicon)
        """

    def get_speech_synthesis_task(self, *, TaskId: str) -> GetSpeechSynthesisTaskOutputTypeDef:
        """
        Retrieves a specific SpeechSynthesisTask object based on its TaskID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.get_speech_synthesis_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#get_speech_synthesis_task)
        """

    def list_lexicons(self, *, NextToken: str = ...) -> ListLexiconsOutputTypeDef:
        """
        Returns a list of pronunciation lexicons stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.list_lexicons)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#list_lexicons)
        """

    def list_speech_synthesis_tasks(
        self, *, MaxResults: int = ..., NextToken: str = ..., Status: TaskStatusType = ...
    ) -> ListSpeechSynthesisTasksOutputTypeDef:
        """
        Returns a list of SpeechSynthesisTask objects ordered by their creation date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.list_speech_synthesis_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#list_speech_synthesis_tasks)
        """

    def put_lexicon(self, *, Name: str, Content: str) -> Dict[str, Any]:
        """
        Stores a pronunciation lexicon in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.put_lexicon)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#put_lexicon)
        """

    def start_speech_synthesis_task(
        self,
        *,
        OutputFormat: OutputFormatType,
        OutputS3BucketName: str,
        Text: str,
        VoiceId: VoiceIdType,
        Engine: EngineType = ...,
        LanguageCode: LanguageCodeType = ...,
        LexiconNames: Sequence[str] = ...,
        OutputS3KeyPrefix: str = ...,
        SampleRate: str = ...,
        SnsTopicArn: str = ...,
        SpeechMarkTypes: Sequence[SpeechMarkTypeType] = ...,
        TextType: TextTypeType = ...
    ) -> StartSpeechSynthesisTaskOutputTypeDef:
        """
        Allows the creation of an asynchronous synthesis task, by starting a new
        `SpeechSynthesisTask`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.start_speech_synthesis_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#start_speech_synthesis_task)
        """

    def synthesize_speech(
        self,
        *,
        OutputFormat: OutputFormatType,
        Text: str,
        VoiceId: VoiceIdType,
        Engine: EngineType = ...,
        LanguageCode: LanguageCodeType = ...,
        LexiconNames: Sequence[str] = ...,
        SampleRate: str = ...,
        SpeechMarkTypes: Sequence[SpeechMarkTypeType] = ...,
        TextType: TextTypeType = ...
    ) -> SynthesizeSpeechOutputTypeDef:
        """
        Synthesizes UTF-8 input, plain text or SSML, to a stream of bytes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.synthesize_speech)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#synthesize_speech)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_voices"]) -> DescribeVoicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_lexicons"]) -> ListLexiconsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_speech_synthesis_tasks"]
    ) -> ListSpeechSynthesisTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/client/#get_paginator)
        """
