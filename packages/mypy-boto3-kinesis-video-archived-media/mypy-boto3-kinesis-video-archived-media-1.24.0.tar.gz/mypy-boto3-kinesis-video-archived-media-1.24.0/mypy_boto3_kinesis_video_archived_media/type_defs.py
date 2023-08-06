"""
Type annotations for kinesis-video-archived-media service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_archived_media.type_defs import ClipTimestampRangeTypeDef

    data: ClipTimestampRangeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ClipFragmentSelectorTypeType,
    ContainerFormatType,
    DASHDisplayFragmentNumberType,
    DASHDisplayFragmentTimestampType,
    DASHFragmentSelectorTypeType,
    DASHPlaybackModeType,
    FormatType,
    FragmentSelectorTypeType,
    HLSDiscontinuityModeType,
    HLSDisplayFragmentTimestampType,
    HLSFragmentSelectorTypeType,
    HLSPlaybackModeType,
    ImageErrorType,
    ImageSelectorTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ClipTimestampRangeTypeDef",
    "DASHTimestampRangeTypeDef",
    "TimestampRangeTypeDef",
    "FragmentTypeDef",
    "ResponseMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "GetImagesInputRequestTypeDef",
    "ImageTypeDef",
    "GetMediaForFragmentListInputRequestTypeDef",
    "HLSTimestampRangeTypeDef",
    "ClipFragmentSelectorTypeDef",
    "DASHFragmentSelectorTypeDef",
    "FragmentSelectorTypeDef",
    "GetClipOutputTypeDef",
    "GetDASHStreamingSessionURLOutputTypeDef",
    "GetHLSStreamingSessionURLOutputTypeDef",
    "GetMediaForFragmentListOutputTypeDef",
    "ListFragmentsOutputTypeDef",
    "GetImagesInputGetImagesPaginateTypeDef",
    "GetImagesOutputTypeDef",
    "HLSFragmentSelectorTypeDef",
    "GetClipInputRequestTypeDef",
    "GetDASHStreamingSessionURLInputRequestTypeDef",
    "ListFragmentsInputListFragmentsPaginateTypeDef",
    "ListFragmentsInputRequestTypeDef",
    "GetHLSStreamingSessionURLInputRequestTypeDef",
)

ClipTimestampRangeTypeDef = TypedDict(
    "ClipTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
)

DASHTimestampRangeTypeDef = TypedDict(
    "DASHTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
    total=False,
)

TimestampRangeTypeDef = TypedDict(
    "TimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
)

FragmentTypeDef = TypedDict(
    "FragmentTypeDef",
    {
        "FragmentNumber": str,
        "FragmentSizeInBytes": int,
        "ProducerTimestamp": datetime,
        "ServerTimestamp": datetime,
        "FragmentLengthInMilliseconds": int,
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

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredGetImagesInputRequestTypeDef = TypedDict(
    "_RequiredGetImagesInputRequestTypeDef",
    {
        "ImageSelectorType": ImageSelectorTypeType,
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
        "SamplingInterval": int,
        "Format": FormatType,
    },
)
_OptionalGetImagesInputRequestTypeDef = TypedDict(
    "_OptionalGetImagesInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FormatConfig": Mapping[Literal["JPEGQuality"], str],
        "WidthPixels": int,
        "HeightPixels": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetImagesInputRequestTypeDef(
    _RequiredGetImagesInputRequestTypeDef, _OptionalGetImagesInputRequestTypeDef
):
    pass


ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "TimeStamp": datetime,
        "Error": ImageErrorType,
        "ImageContent": str,
    },
    total=False,
)

_RequiredGetMediaForFragmentListInputRequestTypeDef = TypedDict(
    "_RequiredGetMediaForFragmentListInputRequestTypeDef",
    {
        "Fragments": Sequence[str],
    },
)
_OptionalGetMediaForFragmentListInputRequestTypeDef = TypedDict(
    "_OptionalGetMediaForFragmentListInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
    },
    total=False,
)


class GetMediaForFragmentListInputRequestTypeDef(
    _RequiredGetMediaForFragmentListInputRequestTypeDef,
    _OptionalGetMediaForFragmentListInputRequestTypeDef,
):
    pass


HLSTimestampRangeTypeDef = TypedDict(
    "HLSTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
    total=False,
)

ClipFragmentSelectorTypeDef = TypedDict(
    "ClipFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": ClipFragmentSelectorTypeType,
        "TimestampRange": ClipTimestampRangeTypeDef,
    },
)

DASHFragmentSelectorTypeDef = TypedDict(
    "DASHFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": DASHFragmentSelectorTypeType,
        "TimestampRange": DASHTimestampRangeTypeDef,
    },
    total=False,
)

FragmentSelectorTypeDef = TypedDict(
    "FragmentSelectorTypeDef",
    {
        "FragmentSelectorType": FragmentSelectorTypeType,
        "TimestampRange": TimestampRangeTypeDef,
    },
)

GetClipOutputTypeDef = TypedDict(
    "GetClipOutputTypeDef",
    {
        "ContentType": str,
        "Payload": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDASHStreamingSessionURLOutputTypeDef = TypedDict(
    "GetDASHStreamingSessionURLOutputTypeDef",
    {
        "DASHStreamingSessionURL": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetHLSStreamingSessionURLOutputTypeDef = TypedDict(
    "GetHLSStreamingSessionURLOutputTypeDef",
    {
        "HLSStreamingSessionURL": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMediaForFragmentListOutputTypeDef = TypedDict(
    "GetMediaForFragmentListOutputTypeDef",
    {
        "ContentType": str,
        "Payload": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFragmentsOutputTypeDef = TypedDict(
    "ListFragmentsOutputTypeDef",
    {
        "Fragments": List[FragmentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetImagesInputGetImagesPaginateTypeDef = TypedDict(
    "_RequiredGetImagesInputGetImagesPaginateTypeDef",
    {
        "ImageSelectorType": ImageSelectorTypeType,
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
        "SamplingInterval": int,
        "Format": FormatType,
    },
)
_OptionalGetImagesInputGetImagesPaginateTypeDef = TypedDict(
    "_OptionalGetImagesInputGetImagesPaginateTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FormatConfig": Mapping[Literal["JPEGQuality"], str],
        "WidthPixels": int,
        "HeightPixels": int,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetImagesInputGetImagesPaginateTypeDef(
    _RequiredGetImagesInputGetImagesPaginateTypeDef, _OptionalGetImagesInputGetImagesPaginateTypeDef
):
    pass


GetImagesOutputTypeDef = TypedDict(
    "GetImagesOutputTypeDef",
    {
        "Images": List[ImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HLSFragmentSelectorTypeDef = TypedDict(
    "HLSFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": HLSFragmentSelectorTypeType,
        "TimestampRange": HLSTimestampRangeTypeDef,
    },
    total=False,
)

_RequiredGetClipInputRequestTypeDef = TypedDict(
    "_RequiredGetClipInputRequestTypeDef",
    {
        "ClipFragmentSelector": ClipFragmentSelectorTypeDef,
    },
)
_OptionalGetClipInputRequestTypeDef = TypedDict(
    "_OptionalGetClipInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
    },
    total=False,
)


class GetClipInputRequestTypeDef(
    _RequiredGetClipInputRequestTypeDef, _OptionalGetClipInputRequestTypeDef
):
    pass


GetDASHStreamingSessionURLInputRequestTypeDef = TypedDict(
    "GetDASHStreamingSessionURLInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "PlaybackMode": DASHPlaybackModeType,
        "DisplayFragmentTimestamp": DASHDisplayFragmentTimestampType,
        "DisplayFragmentNumber": DASHDisplayFragmentNumberType,
        "DASHFragmentSelector": DASHFragmentSelectorTypeDef,
        "Expires": int,
        "MaxManifestFragmentResults": int,
    },
    total=False,
)

ListFragmentsInputListFragmentsPaginateTypeDef = TypedDict(
    "ListFragmentsInputListFragmentsPaginateTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FragmentSelector": FragmentSelectorTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFragmentsInputRequestTypeDef = TypedDict(
    "ListFragmentsInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "MaxResults": int,
        "NextToken": str,
        "FragmentSelector": FragmentSelectorTypeDef,
    },
    total=False,
)

GetHLSStreamingSessionURLInputRequestTypeDef = TypedDict(
    "GetHLSStreamingSessionURLInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "PlaybackMode": HLSPlaybackModeType,
        "HLSFragmentSelector": HLSFragmentSelectorTypeDef,
        "ContainerFormat": ContainerFormatType,
        "DiscontinuityMode": HLSDiscontinuityModeType,
        "DisplayFragmentTimestamp": HLSDisplayFragmentTimestampType,
        "Expires": int,
        "MaxMediaPlaylistFragmentResults": int,
    },
    total=False,
)
