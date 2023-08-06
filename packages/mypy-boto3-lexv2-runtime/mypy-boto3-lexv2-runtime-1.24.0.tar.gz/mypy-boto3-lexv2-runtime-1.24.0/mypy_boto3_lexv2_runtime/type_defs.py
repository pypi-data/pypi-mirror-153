"""
Type annotations for lexv2-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_lexv2_runtime.type_defs import ActiveContextTimeToLiveTypeDef

    data: ActiveContextTimeToLiveTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ConfirmationStateType,
    DialogActionTypeType,
    IntentStateType,
    MessageContentTypeType,
    SentimentTypeType,
    ShapeType,
    StyleTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActiveContextTimeToLiveTypeDef",
    "ButtonTypeDef",
    "ConfidenceScoreTypeDef",
    "DeleteSessionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DialogActionTypeDef",
    "GetSessionRequestRequestTypeDef",
    "IntentTypeDef",
    "RecognizeUtteranceRequestRequestTypeDef",
    "RuntimeHintValueTypeDef",
    "SentimentScoreTypeDef",
    "ValueTypeDef",
    "ActiveContextTypeDef",
    "ImageResponseCardTypeDef",
    "DeleteSessionResponseTypeDef",
    "PutSessionResponseTypeDef",
    "RecognizeUtteranceResponseTypeDef",
    "RuntimeHintDetailsTypeDef",
    "SentimentResponseTypeDef",
    "SlotTypeDef",
    "MessageTypeDef",
    "RuntimeHintsTypeDef",
    "InterpretationTypeDef",
    "SessionStateTypeDef",
    "GetSessionResponseTypeDef",
    "PutSessionRequestRequestTypeDef",
    "RecognizeTextRequestRequestTypeDef",
    "RecognizeTextResponseTypeDef",
)

ActiveContextTimeToLiveTypeDef = TypedDict(
    "ActiveContextTimeToLiveTypeDef",
    {
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)

ButtonTypeDef = TypedDict(
    "ButtonTypeDef",
    {
        "text": str,
        "value": str,
    },
)

ConfidenceScoreTypeDef = TypedDict(
    "ConfidenceScoreTypeDef",
    {
        "score": float,
    },
    total=False,
)

DeleteSessionRequestRequestTypeDef = TypedDict(
    "DeleteSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
    },
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

_RequiredDialogActionTypeDef = TypedDict(
    "_RequiredDialogActionTypeDef",
    {
        "type": DialogActionTypeType,
    },
)
_OptionalDialogActionTypeDef = TypedDict(
    "_OptionalDialogActionTypeDef",
    {
        "slotToElicit": str,
        "slotElicitationStyle": StyleTypeType,
    },
    total=False,
)


class DialogActionTypeDef(_RequiredDialogActionTypeDef, _OptionalDialogActionTypeDef):
    pass


GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
    },
)

_RequiredIntentTypeDef = TypedDict(
    "_RequiredIntentTypeDef",
    {
        "name": str,
    },
)
_OptionalIntentTypeDef = TypedDict(
    "_OptionalIntentTypeDef",
    {
        "slots": Dict[str, "SlotTypeDef"],
        "state": IntentStateType,
        "confirmationState": ConfirmationStateType,
    },
    total=False,
)


class IntentTypeDef(_RequiredIntentTypeDef, _OptionalIntentTypeDef):
    pass


_RequiredRecognizeUtteranceRequestRequestTypeDef = TypedDict(
    "_RequiredRecognizeUtteranceRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "requestContentType": str,
    },
)
_OptionalRecognizeUtteranceRequestRequestTypeDef = TypedDict(
    "_OptionalRecognizeUtteranceRequestRequestTypeDef",
    {
        "sessionState": str,
        "requestAttributes": str,
        "responseContentType": str,
        "inputStream": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class RecognizeUtteranceRequestRequestTypeDef(
    _RequiredRecognizeUtteranceRequestRequestTypeDef,
    _OptionalRecognizeUtteranceRequestRequestTypeDef,
):
    pass


RuntimeHintValueTypeDef = TypedDict(
    "RuntimeHintValueTypeDef",
    {
        "phrase": str,
    },
)

SentimentScoreTypeDef = TypedDict(
    "SentimentScoreTypeDef",
    {
        "positive": float,
        "negative": float,
        "neutral": float,
        "mixed": float,
    },
    total=False,
)

_RequiredValueTypeDef = TypedDict(
    "_RequiredValueTypeDef",
    {
        "interpretedValue": str,
    },
)
_OptionalValueTypeDef = TypedDict(
    "_OptionalValueTypeDef",
    {
        "originalValue": str,
        "resolvedValues": List[str],
    },
    total=False,
)


class ValueTypeDef(_RequiredValueTypeDef, _OptionalValueTypeDef):
    pass


ActiveContextTypeDef = TypedDict(
    "ActiveContextTypeDef",
    {
        "name": str,
        "timeToLive": ActiveContextTimeToLiveTypeDef,
        "contextAttributes": Dict[str, str],
    },
)

_RequiredImageResponseCardTypeDef = TypedDict(
    "_RequiredImageResponseCardTypeDef",
    {
        "title": str,
    },
)
_OptionalImageResponseCardTypeDef = TypedDict(
    "_OptionalImageResponseCardTypeDef",
    {
        "subtitle": str,
        "imageUrl": str,
        "buttons": List[ButtonTypeDef],
    },
    total=False,
)


class ImageResponseCardTypeDef(
    _RequiredImageResponseCardTypeDef, _OptionalImageResponseCardTypeDef
):
    pass


DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSessionResponseTypeDef = TypedDict(
    "PutSessionResponseTypeDef",
    {
        "contentType": str,
        "messages": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "audioStream": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecognizeUtteranceResponseTypeDef = TypedDict(
    "RecognizeUtteranceResponseTypeDef",
    {
        "inputMode": str,
        "contentType": str,
        "messages": str,
        "interpretations": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "inputTranscript": str,
        "audioStream": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuntimeHintDetailsTypeDef = TypedDict(
    "RuntimeHintDetailsTypeDef",
    {
        "runtimeHintValues": List[RuntimeHintValueTypeDef],
    },
)

SentimentResponseTypeDef = TypedDict(
    "SentimentResponseTypeDef",
    {
        "sentiment": SentimentTypeType,
        "sentimentScore": SentimentScoreTypeDef,
    },
    total=False,
)

SlotTypeDef = TypedDict(
    "SlotTypeDef",
    {
        "value": ValueTypeDef,
        "shape": ShapeType,
        "values": List[Dict[str, Any]],
    },
    total=False,
)

_RequiredMessageTypeDef = TypedDict(
    "_RequiredMessageTypeDef",
    {
        "contentType": MessageContentTypeType,
    },
)
_OptionalMessageTypeDef = TypedDict(
    "_OptionalMessageTypeDef",
    {
        "content": str,
        "imageResponseCard": ImageResponseCardTypeDef,
    },
    total=False,
)


class MessageTypeDef(_RequiredMessageTypeDef, _OptionalMessageTypeDef):
    pass


RuntimeHintsTypeDef = TypedDict(
    "RuntimeHintsTypeDef",
    {
        "slotHints": Dict[str, Dict[str, RuntimeHintDetailsTypeDef]],
    },
    total=False,
)

InterpretationTypeDef = TypedDict(
    "InterpretationTypeDef",
    {
        "nluConfidence": ConfidenceScoreTypeDef,
        "sentimentResponse": SentimentResponseTypeDef,
        "intent": IntentTypeDef,
    },
    total=False,
)

SessionStateTypeDef = TypedDict(
    "SessionStateTypeDef",
    {
        "dialogAction": DialogActionTypeDef,
        "intent": IntentTypeDef,
        "activeContexts": List[ActiveContextTypeDef],
        "sessionAttributes": Dict[str, str],
        "originatingRequestId": str,
        "runtimeHints": RuntimeHintsTypeDef,
    },
    total=False,
)

GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "sessionId": str,
        "messages": List[MessageTypeDef],
        "interpretations": List[InterpretationTypeDef],
        "sessionState": SessionStateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutSessionRequestRequestTypeDef = TypedDict(
    "_RequiredPutSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "sessionState": SessionStateTypeDef,
    },
)
_OptionalPutSessionRequestRequestTypeDef = TypedDict(
    "_OptionalPutSessionRequestRequestTypeDef",
    {
        "messages": Sequence[MessageTypeDef],
        "requestAttributes": Mapping[str, str],
        "responseContentType": str,
    },
    total=False,
)


class PutSessionRequestRequestTypeDef(
    _RequiredPutSessionRequestRequestTypeDef, _OptionalPutSessionRequestRequestTypeDef
):
    pass


_RequiredRecognizeTextRequestRequestTypeDef = TypedDict(
    "_RequiredRecognizeTextRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "text": str,
    },
)
_OptionalRecognizeTextRequestRequestTypeDef = TypedDict(
    "_OptionalRecognizeTextRequestRequestTypeDef",
    {
        "sessionState": SessionStateTypeDef,
        "requestAttributes": Mapping[str, str],
    },
    total=False,
)


class RecognizeTextRequestRequestTypeDef(
    _RequiredRecognizeTextRequestRequestTypeDef, _OptionalRecognizeTextRequestRequestTypeDef
):
    pass


RecognizeTextResponseTypeDef = TypedDict(
    "RecognizeTextResponseTypeDef",
    {
        "messages": List[MessageTypeDef],
        "sessionState": SessionStateTypeDef,
        "interpretations": List[InterpretationTypeDef],
        "requestAttributes": Dict[str, str],
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
