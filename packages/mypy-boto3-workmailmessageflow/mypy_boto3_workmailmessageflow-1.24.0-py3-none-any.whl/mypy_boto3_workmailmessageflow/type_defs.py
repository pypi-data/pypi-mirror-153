"""
Type annotations for workmailmessageflow service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workmailmessageflow/type_defs/)

Usage::

    ```python
    from mypy_boto3_workmailmessageflow.type_defs import GetRawMessageContentRequestRequestTypeDef

    data: GetRawMessageContentRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "GetRawMessageContentRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "S3ReferenceTypeDef",
    "GetRawMessageContentResponseTypeDef",
    "RawMessageContentTypeDef",
    "PutRawMessageContentRequestRequestTypeDef",
)

GetRawMessageContentRequestRequestTypeDef = TypedDict(
    "GetRawMessageContentRequestRequestTypeDef",
    {
        "messageId": str,
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

_RequiredS3ReferenceTypeDef = TypedDict(
    "_RequiredS3ReferenceTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)
_OptionalS3ReferenceTypeDef = TypedDict(
    "_OptionalS3ReferenceTypeDef",
    {
        "objectVersion": str,
    },
    total=False,
)


class S3ReferenceTypeDef(_RequiredS3ReferenceTypeDef, _OptionalS3ReferenceTypeDef):
    pass


GetRawMessageContentResponseTypeDef = TypedDict(
    "GetRawMessageContentResponseTypeDef",
    {
        "messageContent": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RawMessageContentTypeDef = TypedDict(
    "RawMessageContentTypeDef",
    {
        "s3Reference": S3ReferenceTypeDef,
    },
)

PutRawMessageContentRequestRequestTypeDef = TypedDict(
    "PutRawMessageContentRequestRequestTypeDef",
    {
        "messageId": str,
        "content": RawMessageContentTypeDef,
    },
)
