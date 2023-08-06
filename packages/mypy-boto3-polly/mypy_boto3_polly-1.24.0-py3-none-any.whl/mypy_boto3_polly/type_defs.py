"""
Type annotations for polly service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/type_defs/)

Usage::

    ```python
    from mypy_boto3_polly.type_defs import DeleteLexiconInputRequestTypeDef

    data: DeleteLexiconInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from botocore.response import StreamingBody

from .literals import (
    EngineType,
    GenderType,
    LanguageCodeType,
    OutputFormatType,
    SpeechMarkTypeType,
    TaskStatusType,
    TextTypeType,
    VoiceIdType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteLexiconInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeVoicesInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "VoiceTypeDef",
    "GetLexiconInputRequestTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconTypeDef",
    "GetSpeechSynthesisTaskInputRequestTypeDef",
    "SynthesisTaskTypeDef",
    "ListLexiconsInputRequestTypeDef",
    "ListSpeechSynthesisTasksInputRequestTypeDef",
    "PutLexiconInputRequestTypeDef",
    "StartSpeechSynthesisTaskInputRequestTypeDef",
    "SynthesizeSpeechInputRequestTypeDef",
    "DescribeVoicesInputDescribeVoicesPaginateTypeDef",
    "ListLexiconsInputListLexiconsPaginateTypeDef",
    "ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef",
    "SynthesizeSpeechOutputTypeDef",
    "DescribeVoicesOutputTypeDef",
    "LexiconDescriptionTypeDef",
    "GetLexiconOutputTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "ListLexiconsOutputTypeDef",
)

DeleteLexiconInputRequestTypeDef = TypedDict(
    "DeleteLexiconInputRequestTypeDef",
    {
        "Name": str,
    },
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

DescribeVoicesInputRequestTypeDef = TypedDict(
    "DescribeVoicesInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "IncludeAdditionalLanguageCodes": bool,
        "NextToken": str,
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

VoiceTypeDef = TypedDict(
    "VoiceTypeDef",
    {
        "Gender": GenderType,
        "Id": VoiceIdType,
        "LanguageCode": LanguageCodeType,
        "LanguageName": str,
        "Name": str,
        "AdditionalLanguageCodes": List[LanguageCodeType],
        "SupportedEngines": List[EngineType],
    },
    total=False,
)

GetLexiconInputRequestTypeDef = TypedDict(
    "GetLexiconInputRequestTypeDef",
    {
        "Name": str,
    },
)

LexiconAttributesTypeDef = TypedDict(
    "LexiconAttributesTypeDef",
    {
        "Alphabet": str,
        "LanguageCode": LanguageCodeType,
        "LastModified": datetime,
        "LexiconArn": str,
        "LexemesCount": int,
        "Size": int,
    },
    total=False,
)

LexiconTypeDef = TypedDict(
    "LexiconTypeDef",
    {
        "Content": str,
        "Name": str,
    },
    total=False,
)

GetSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "GetSpeechSynthesisTaskInputRequestTypeDef",
    {
        "TaskId": str,
    },
)

SynthesisTaskTypeDef = TypedDict(
    "SynthesisTaskTypeDef",
    {
        "Engine": EngineType,
        "TaskId": str,
        "TaskStatus": TaskStatusType,
        "TaskStatusReason": str,
        "OutputUri": str,
        "CreationTime": datetime,
        "RequestCharacters": int,
        "SnsTopicArn": str,
        "LexiconNames": List[str],
        "OutputFormat": OutputFormatType,
        "SampleRate": str,
        "SpeechMarkTypes": List[SpeechMarkTypeType],
        "TextType": TextTypeType,
        "VoiceId": VoiceIdType,
        "LanguageCode": LanguageCodeType,
    },
    total=False,
)

ListLexiconsInputRequestTypeDef = TypedDict(
    "ListLexiconsInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListSpeechSynthesisTasksInputRequestTypeDef = TypedDict(
    "ListSpeechSynthesisTasksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Status": TaskStatusType,
    },
    total=False,
)

PutLexiconInputRequestTypeDef = TypedDict(
    "PutLexiconInputRequestTypeDef",
    {
        "Name": str,
        "Content": str,
    },
)

_RequiredStartSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "_RequiredStartSpeechSynthesisTaskInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "OutputS3BucketName": str,
        "Text": str,
        "VoiceId": VoiceIdType,
    },
)
_OptionalStartSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "_OptionalStartSpeechSynthesisTaskInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "LexiconNames": Sequence[str],
        "OutputS3KeyPrefix": str,
        "SampleRate": str,
        "SnsTopicArn": str,
        "SpeechMarkTypes": Sequence[SpeechMarkTypeType],
        "TextType": TextTypeType,
    },
    total=False,
)


class StartSpeechSynthesisTaskInputRequestTypeDef(
    _RequiredStartSpeechSynthesisTaskInputRequestTypeDef,
    _OptionalStartSpeechSynthesisTaskInputRequestTypeDef,
):
    pass


_RequiredSynthesizeSpeechInputRequestTypeDef = TypedDict(
    "_RequiredSynthesizeSpeechInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "Text": str,
        "VoiceId": VoiceIdType,
    },
)
_OptionalSynthesizeSpeechInputRequestTypeDef = TypedDict(
    "_OptionalSynthesizeSpeechInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "LexiconNames": Sequence[str],
        "SampleRate": str,
        "SpeechMarkTypes": Sequence[SpeechMarkTypeType],
        "TextType": TextTypeType,
    },
    total=False,
)


class SynthesizeSpeechInputRequestTypeDef(
    _RequiredSynthesizeSpeechInputRequestTypeDef, _OptionalSynthesizeSpeechInputRequestTypeDef
):
    pass


DescribeVoicesInputDescribeVoicesPaginateTypeDef = TypedDict(
    "DescribeVoicesInputDescribeVoicesPaginateTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "IncludeAdditionalLanguageCodes": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListLexiconsInputListLexiconsPaginateTypeDef = TypedDict(
    "ListLexiconsInputListLexiconsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef = TypedDict(
    "ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef",
    {
        "Status": TaskStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SynthesizeSpeechOutputTypeDef = TypedDict(
    "SynthesizeSpeechOutputTypeDef",
    {
        "AudioStream": StreamingBody,
        "ContentType": str,
        "RequestCharacters": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVoicesOutputTypeDef = TypedDict(
    "DescribeVoicesOutputTypeDef",
    {
        "Voices": List[VoiceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LexiconDescriptionTypeDef = TypedDict(
    "LexiconDescriptionTypeDef",
    {
        "Name": str,
        "Attributes": LexiconAttributesTypeDef,
    },
    total=False,
)

GetLexiconOutputTypeDef = TypedDict(
    "GetLexiconOutputTypeDef",
    {
        "Lexicon": LexiconTypeDef,
        "LexiconAttributes": LexiconAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "GetSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": SynthesisTaskTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSpeechSynthesisTasksOutputTypeDef = TypedDict(
    "ListSpeechSynthesisTasksOutputTypeDef",
    {
        "NextToken": str,
        "SynthesisTasks": List[SynthesisTaskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "StartSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": SynthesisTaskTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLexiconsOutputTypeDef = TypedDict(
    "ListLexiconsOutputTypeDef",
    {
        "Lexicons": List[LexiconDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
