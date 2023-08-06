"""
Type annotations for lex-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lex_runtime.client import LexRuntimeServiceClient

    session = Session()
    client: LexRuntimeServiceClient = session.client("lex-runtime")
    ```
"""
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .type_defs import (
    ActiveContextTypeDef,
    DeleteSessionResponseTypeDef,
    DialogActionTypeDef,
    GetSessionResponseTypeDef,
    IntentSummaryTypeDef,
    PostContentResponseTypeDef,
    PostTextResponseTypeDef,
    PutSessionResponseTypeDef,
)

__all__ = ("LexRuntimeServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadGatewayException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LoopDetectedException: Type[BotocoreClientError]
    NotAcceptableException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    UnsupportedMediaTypeException: Type[BotocoreClientError]


class LexRuntimeServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LexRuntimeServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#can_paginate)
        """

    def delete_session(
        self, *, botName: str, botAlias: str, userId: str
    ) -> DeleteSessionResponseTypeDef:
        """
        Removes session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.delete_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#delete_session)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#generate_presigned_url)
        """

    def get_session(
        self, *, botName: str, botAlias: str, userId: str, checkpointLabelFilter: str = ...
    ) -> GetSessionResponseTypeDef:
        """
        Returns session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.get_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#get_session)
        """

    def post_content(
        self,
        *,
        botName: str,
        botAlias: str,
        userId: str,
        contentType: str,
        inputStream: Union[str, bytes, IO[Any], StreamingBody],
        sessionAttributes: str = ...,
        requestAttributes: str = ...,
        accept: str = ...,
        activeContexts: str = ...
    ) -> PostContentResponseTypeDef:
        """
        Sends user input (text or speech) to Amazon Lex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.post_content)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#post_content)
        """

    def post_text(
        self,
        *,
        botName: str,
        botAlias: str,
        userId: str,
        inputText: str,
        sessionAttributes: Mapping[str, str] = ...,
        requestAttributes: Mapping[str, str] = ...,
        activeContexts: Sequence[ActiveContextTypeDef] = ...
    ) -> PostTextResponseTypeDef:
        """
        Sends user input to Amazon Lex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.post_text)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#post_text)
        """

    def put_session(
        self,
        *,
        botName: str,
        botAlias: str,
        userId: str,
        sessionAttributes: Mapping[str, str] = ...,
        dialogAction: DialogActionTypeDef = ...,
        recentIntentSummaryView: Sequence[IntentSummaryTypeDef] = ...,
        accept: str = ...,
        activeContexts: Sequence[ActiveContextTypeDef] = ...
    ) -> PutSessionResponseTypeDef:
        """
        Creates a new session or modifies an existing session with an Amazon Lex bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client.put_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_runtime/client/#put_session)
        """
