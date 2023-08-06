"""
Type annotations for kinesis-video-media service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_media/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_media.type_defs import StartSelectorTypeDef

    data: StartSelectorTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, Union

from botocore.response import StreamingBody

from .literals import StartSelectorTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "StartSelectorTypeDef",
    "ResponseMetadataTypeDef",
    "GetMediaInputRequestTypeDef",
    "GetMediaOutputTypeDef",
)

_RequiredStartSelectorTypeDef = TypedDict(
    "_RequiredStartSelectorTypeDef",
    {
        "StartSelectorType": StartSelectorTypeType,
    },
)
_OptionalStartSelectorTypeDef = TypedDict(
    "_OptionalStartSelectorTypeDef",
    {
        "AfterFragmentNumber": str,
        "StartTimestamp": Union[datetime, str],
        "ContinuationToken": str,
    },
    total=False,
)

class StartSelectorTypeDef(_RequiredStartSelectorTypeDef, _OptionalStartSelectorTypeDef):
    pass

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

_RequiredGetMediaInputRequestTypeDef = TypedDict(
    "_RequiredGetMediaInputRequestTypeDef",
    {
        "StartSelector": StartSelectorTypeDef,
    },
)
_OptionalGetMediaInputRequestTypeDef = TypedDict(
    "_OptionalGetMediaInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
    },
    total=False,
)

class GetMediaInputRequestTypeDef(
    _RequiredGetMediaInputRequestTypeDef, _OptionalGetMediaInputRequestTypeDef
):
    pass

GetMediaOutputTypeDef = TypedDict(
    "GetMediaOutputTypeDef",
    {
        "ContentType": str,
        "Payload": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
