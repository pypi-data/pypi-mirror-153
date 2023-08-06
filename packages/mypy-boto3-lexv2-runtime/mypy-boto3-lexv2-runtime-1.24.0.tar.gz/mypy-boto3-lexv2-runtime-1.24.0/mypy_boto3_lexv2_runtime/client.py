"""
Type annotations for lexv2-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lexv2_runtime.client import LexRuntimeV2Client

    session = Session()
    client: LexRuntimeV2Client = session.client("lexv2-runtime")
    ```
"""
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .type_defs import (
    DeleteSessionResponseTypeDef,
    GetSessionResponseTypeDef,
    MessageTypeDef,
    PutSessionResponseTypeDef,
    RecognizeTextResponseTypeDef,
    RecognizeUtteranceResponseTypeDef,
    SessionStateTypeDef,
)

__all__ = ("LexRuntimeV2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadGatewayException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LexRuntimeV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LexRuntimeV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#can_paginate)
        """

    def delete_session(
        self, *, botId: str, botAliasId: str, localeId: str, sessionId: str
    ) -> DeleteSessionResponseTypeDef:
        """
        Removes session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.delete_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#delete_session)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#generate_presigned_url)
        """

    def get_session(
        self, *, botId: str, botAliasId: str, localeId: str, sessionId: str
    ) -> GetSessionResponseTypeDef:
        """
        Returns session information for a specified bot, alias, and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.get_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#get_session)
        """

    def put_session(
        self,
        *,
        botId: str,
        botAliasId: str,
        localeId: str,
        sessionId: str,
        sessionState: SessionStateTypeDef,
        messages: Sequence[MessageTypeDef] = ...,
        requestAttributes: Mapping[str, str] = ...,
        responseContentType: str = ...
    ) -> PutSessionResponseTypeDef:
        """
        Creates a new session or modifies an existing session with an Amazon Lex V2 bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.put_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#put_session)
        """

    def recognize_text(
        self,
        *,
        botId: str,
        botAliasId: str,
        localeId: str,
        sessionId: str,
        text: str,
        sessionState: SessionStateTypeDef = ...,
        requestAttributes: Mapping[str, str] = ...
    ) -> RecognizeTextResponseTypeDef:
        """
        Sends user input to Amazon Lex V2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.recognize_text)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#recognize_text)
        """

    def recognize_utterance(
        self,
        *,
        botId: str,
        botAliasId: str,
        localeId: str,
        sessionId: str,
        requestContentType: str,
        sessionState: str = ...,
        requestAttributes: str = ...,
        responseContentType: str = ...,
        inputStream: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> RecognizeUtteranceResponseTypeDef:
        """
        Sends user input to Amazon Lex V2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client.recognize_utterance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/client/#recognize_utterance)
        """
