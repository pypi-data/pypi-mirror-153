"""
Type annotations for kinesis-video-archived-media service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
    from mypy_boto3_kinesis_video_archived_media.paginator import (
        GetImagesPaginator,
        ListFragmentsPaginator,
    )

    session = Session()
    client: KinesisVideoArchivedMediaClient = session.client("kinesis-video-archived-media")

    get_images_paginator: GetImagesPaginator = client.get_paginator("get_images")
    list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Mapping, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import FormatType, ImageSelectorTypeType
from .type_defs import (
    FragmentSelectorTypeDef,
    GetImagesOutputTypeDef,
    ListFragmentsOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GetImagesPaginator", "ListFragmentsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetImagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.GetImages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#getimagespaginator)
    """

    def paginate(
        self,
        *,
        ImageSelectorType: ImageSelectorTypeType,
        StartTimestamp: Union[datetime, str],
        EndTimestamp: Union[datetime, str],
        SamplingInterval: int,
        Format: FormatType,
        StreamName: str = ...,
        StreamARN: str = ...,
        FormatConfig: Mapping[Literal["JPEGQuality"], str] = ...,
        WidthPixels: int = ...,
        HeightPixels: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.GetImages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#getimagespaginator)
        """


class ListFragmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.ListFragments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#listfragmentspaginator)
    """

    def paginate(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        FragmentSelector: FragmentSelectorTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFragmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Paginator.ListFragments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/paginators/#listfragmentspaginator)
        """
