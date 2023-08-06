"""
Type annotations for workmailmessageflow service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workmailmessageflow.client import WorkMailMessageFlowClient

    session = Session()
    client: WorkMailMessageFlowClient = session.client("workmailmessageflow")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import GetRawMessageContentResponseTypeDef, RawMessageContentTypeDef

__all__ = ("WorkMailMessageFlowClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidContentLocation: Type[BotocoreClientError]
    MessageFrozen: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class WorkMailMessageFlowClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkMailMessageFlowClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/#generate_presigned_url)
        """

    def get_raw_message_content(self, *, messageId: str) -> GetRawMessageContentResponseTypeDef:
        """
        Retrieves the raw content of an in-transit email message, in MIME format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.get_raw_message_content)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/#get_raw_message_content)
        """

    def put_raw_message_content(
        self, *, messageId: str, content: RawMessageContentTypeDef
    ) -> Dict[str, Any]:
        """
        Updates the raw content of an in-transit email message, in MIME format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.put_raw_message_content)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/client/#put_raw_message_content)
        """
