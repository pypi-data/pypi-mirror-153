"""
Type annotations for ivs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/type_defs/)

Usage::

    ```python
    from mypy_boto3_ivs.type_defs import AudioConfigurationTypeDef

    data: AudioConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ChannelLatencyModeType,
    ChannelTypeType,
    RecordingConfigurationStateType,
    RecordingModeType,
    StreamHealthType,
    StreamStateType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AudioConfigurationTypeDef",
    "BatchErrorTypeDef",
    "BatchGetChannelRequestRequestTypeDef",
    "ChannelTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetStreamKeyRequestRequestTypeDef",
    "StreamKeyTypeDef",
    "ChannelSummaryTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "ThumbnailConfigurationTypeDef",
    "CreateStreamKeyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeletePlaybackKeyPairRequestRequestTypeDef",
    "DeleteRecordingConfigurationRequestRequestTypeDef",
    "DeleteStreamKeyRequestRequestTypeDef",
    "S3DestinationConfigurationTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetPlaybackKeyPairRequestRequestTypeDef",
    "PlaybackKeyPairTypeDef",
    "GetRecordingConfigurationRequestRequestTypeDef",
    "GetStreamKeyRequestRequestTypeDef",
    "GetStreamRequestRequestTypeDef",
    "StreamTypeDef",
    "GetStreamSessionRequestRequestTypeDef",
    "ImportPlaybackKeyPairRequestRequestTypeDef",
    "VideoConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListPlaybackKeyPairsRequestRequestTypeDef",
    "PlaybackKeyPairSummaryTypeDef",
    "ListRecordingConfigurationsRequestRequestTypeDef",
    "ListStreamKeysRequestRequestTypeDef",
    "StreamKeySummaryTypeDef",
    "ListStreamSessionsRequestRequestTypeDef",
    "StreamSessionSummaryTypeDef",
    "StreamFiltersTypeDef",
    "StreamSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutMetadataRequestRequestTypeDef",
    "StopStreamRequestRequestTypeDef",
    "StreamEventTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "BatchGetChannelResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateChannelResponseTypeDef",
    "BatchGetStreamKeyResponseTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateStreamKeyResponseTypeDef",
    "GetStreamKeyResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "DestinationConfigurationTypeDef",
    "GetPlaybackKeyPairResponseTypeDef",
    "ImportPlaybackKeyPairResponseTypeDef",
    "GetStreamResponseTypeDef",
    "IngestConfigurationTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef",
    "ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef",
    "ListStreamKeysRequestListStreamKeysPaginateTypeDef",
    "ListPlaybackKeyPairsResponseTypeDef",
    "ListStreamKeysResponseTypeDef",
    "ListStreamSessionsResponseTypeDef",
    "ListStreamsRequestListStreamsPaginateTypeDef",
    "ListStreamsRequestRequestTypeDef",
    "ListStreamsResponseTypeDef",
    "CreateRecordingConfigurationRequestRequestTypeDef",
    "RecordingConfigurationSummaryTypeDef",
    "RecordingConfigurationTypeDef",
    "ListRecordingConfigurationsResponseTypeDef",
    "CreateRecordingConfigurationResponseTypeDef",
    "GetRecordingConfigurationResponseTypeDef",
    "StreamSessionTypeDef",
    "GetStreamSessionResponseTypeDef",
)

AudioConfigurationTypeDef = TypedDict(
    "AudioConfigurationTypeDef",
    {
        "channels": int,
        "codec": str,
        "sampleRate": int,
        "targetBitrate": int,
    },
    total=False,
)

BatchErrorTypeDef = TypedDict(
    "BatchErrorTypeDef",
    {
        "arn": str,
        "code": str,
        "message": str,
    },
    total=False,
)

BatchGetChannelRequestRequestTypeDef = TypedDict(
    "BatchGetChannelRequestRequestTypeDef",
    {
        "arns": Sequence[str],
    },
)

ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "arn": str,
        "authorized": bool,
        "ingestEndpoint": str,
        "latencyMode": ChannelLatencyModeType,
        "name": str,
        "playbackUrl": str,
        "recordingConfigurationArn": str,
        "tags": Dict[str, str],
        "type": ChannelTypeType,
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

BatchGetStreamKeyRequestRequestTypeDef = TypedDict(
    "BatchGetStreamKeyRequestRequestTypeDef",
    {
        "arns": Sequence[str],
    },
)

StreamKeyTypeDef = TypedDict(
    "StreamKeyTypeDef",
    {
        "arn": str,
        "channelArn": str,
        "tags": Dict[str, str],
        "value": str,
    },
    total=False,
)

ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "arn": str,
        "authorized": bool,
        "latencyMode": ChannelLatencyModeType,
        "name": str,
        "recordingConfigurationArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

CreateChannelRequestRequestTypeDef = TypedDict(
    "CreateChannelRequestRequestTypeDef",
    {
        "authorized": bool,
        "latencyMode": ChannelLatencyModeType,
        "name": str,
        "recordingConfigurationArn": str,
        "tags": Mapping[str, str],
        "type": ChannelTypeType,
    },
    total=False,
)

ThumbnailConfigurationTypeDef = TypedDict(
    "ThumbnailConfigurationTypeDef",
    {
        "recordingMode": RecordingModeType,
        "targetIntervalSeconds": int,
    },
    total=False,
)

_RequiredCreateStreamKeyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamKeyRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)
_OptionalCreateStreamKeyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamKeyRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateStreamKeyRequestRequestTypeDef(
    _RequiredCreateStreamKeyRequestRequestTypeDef, _OptionalCreateStreamKeyRequestRequestTypeDef
):
    pass


DeleteChannelRequestRequestTypeDef = TypedDict(
    "DeleteChannelRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeletePlaybackKeyPairRequestRequestTypeDef = TypedDict(
    "DeletePlaybackKeyPairRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteRecordingConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteRecordingConfigurationRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteStreamKeyRequestRequestTypeDef = TypedDict(
    "DeleteStreamKeyRequestRequestTypeDef",
    {
        "arn": str,
    },
)

S3DestinationConfigurationTypeDef = TypedDict(
    "S3DestinationConfigurationTypeDef",
    {
        "bucketName": str,
    },
)

GetChannelRequestRequestTypeDef = TypedDict(
    "GetChannelRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetPlaybackKeyPairRequestRequestTypeDef = TypedDict(
    "GetPlaybackKeyPairRequestRequestTypeDef",
    {
        "arn": str,
    },
)

PlaybackKeyPairTypeDef = TypedDict(
    "PlaybackKeyPairTypeDef",
    {
        "arn": str,
        "fingerprint": str,
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)

GetRecordingConfigurationRequestRequestTypeDef = TypedDict(
    "GetRecordingConfigurationRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetStreamKeyRequestRequestTypeDef = TypedDict(
    "GetStreamKeyRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetStreamRequestRequestTypeDef = TypedDict(
    "GetStreamRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)

StreamTypeDef = TypedDict(
    "StreamTypeDef",
    {
        "channelArn": str,
        "health": StreamHealthType,
        "playbackUrl": str,
        "startTime": datetime,
        "state": StreamStateType,
        "streamId": str,
        "viewerCount": int,
    },
    total=False,
)

_RequiredGetStreamSessionRequestRequestTypeDef = TypedDict(
    "_RequiredGetStreamSessionRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)
_OptionalGetStreamSessionRequestRequestTypeDef = TypedDict(
    "_OptionalGetStreamSessionRequestRequestTypeDef",
    {
        "streamId": str,
    },
    total=False,
)


class GetStreamSessionRequestRequestTypeDef(
    _RequiredGetStreamSessionRequestRequestTypeDef, _OptionalGetStreamSessionRequestRequestTypeDef
):
    pass


_RequiredImportPlaybackKeyPairRequestRequestTypeDef = TypedDict(
    "_RequiredImportPlaybackKeyPairRequestRequestTypeDef",
    {
        "publicKeyMaterial": str,
    },
)
_OptionalImportPlaybackKeyPairRequestRequestTypeDef = TypedDict(
    "_OptionalImportPlaybackKeyPairRequestRequestTypeDef",
    {
        "name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class ImportPlaybackKeyPairRequestRequestTypeDef(
    _RequiredImportPlaybackKeyPairRequestRequestTypeDef,
    _OptionalImportPlaybackKeyPairRequestRequestTypeDef,
):
    pass


VideoConfigurationTypeDef = TypedDict(
    "VideoConfigurationTypeDef",
    {
        "avcLevel": str,
        "avcProfile": str,
        "codec": str,
        "encoder": str,
        "targetBitrate": int,
        "targetFramerate": int,
        "videoHeight": int,
        "videoWidth": int,
    },
    total=False,
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

ListChannelsRequestRequestTypeDef = TypedDict(
    "ListChannelsRequestRequestTypeDef",
    {
        "filterByName": str,
        "filterByRecordingConfigurationArn": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListPlaybackKeyPairsRequestRequestTypeDef = TypedDict(
    "ListPlaybackKeyPairsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

PlaybackKeyPairSummaryTypeDef = TypedDict(
    "PlaybackKeyPairSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ListRecordingConfigurationsRequestRequestTypeDef = TypedDict(
    "ListRecordingConfigurationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListStreamKeysRequestRequestTypeDef = TypedDict(
    "_RequiredListStreamKeysRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)
_OptionalListStreamKeysRequestRequestTypeDef = TypedDict(
    "_OptionalListStreamKeysRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListStreamKeysRequestRequestTypeDef(
    _RequiredListStreamKeysRequestRequestTypeDef, _OptionalListStreamKeysRequestRequestTypeDef
):
    pass


StreamKeySummaryTypeDef = TypedDict(
    "StreamKeySummaryTypeDef",
    {
        "arn": str,
        "channelArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredListStreamSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredListStreamSessionsRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)
_OptionalListStreamSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalListStreamSessionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListStreamSessionsRequestRequestTypeDef(
    _RequiredListStreamSessionsRequestRequestTypeDef,
    _OptionalListStreamSessionsRequestRequestTypeDef,
):
    pass


StreamSessionSummaryTypeDef = TypedDict(
    "StreamSessionSummaryTypeDef",
    {
        "endTime": datetime,
        "hasErrorEvent": bool,
        "startTime": datetime,
        "streamId": str,
    },
    total=False,
)

StreamFiltersTypeDef = TypedDict(
    "StreamFiltersTypeDef",
    {
        "health": StreamHealthType,
    },
    total=False,
)

StreamSummaryTypeDef = TypedDict(
    "StreamSummaryTypeDef",
    {
        "channelArn": str,
        "health": StreamHealthType,
        "startTime": datetime,
        "state": StreamStateType,
        "streamId": str,
        "viewerCount": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

PutMetadataRequestRequestTypeDef = TypedDict(
    "PutMetadataRequestRequestTypeDef",
    {
        "channelArn": str,
        "metadata": str,
    },
)

StopStreamRequestRequestTypeDef = TypedDict(
    "StopStreamRequestRequestTypeDef",
    {
        "channelArn": str,
    },
)

StreamEventTypeDef = TypedDict(
    "StreamEventTypeDef",
    {
        "eventTime": datetime,
        "name": str,
        "type": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateChannelRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateChannelRequestRequestTypeDef",
    {
        "authorized": bool,
        "latencyMode": ChannelLatencyModeType,
        "name": str,
        "recordingConfigurationArn": str,
        "type": ChannelTypeType,
    },
    total=False,
)


class UpdateChannelRequestRequestTypeDef(
    _RequiredUpdateChannelRequestRequestTypeDef, _OptionalUpdateChannelRequestRequestTypeDef
):
    pass


BatchGetChannelResponseTypeDef = TypedDict(
    "BatchGetChannelResponseTypeDef",
    {
        "channels": List[ChannelTypeDef],
        "errors": List[BatchErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChannelResponseTypeDef = TypedDict(
    "GetChannelResponseTypeDef",
    {
        "channel": ChannelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "channel": ChannelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetStreamKeyResponseTypeDef = TypedDict(
    "BatchGetStreamKeyResponseTypeDef",
    {
        "errors": List[BatchErrorTypeDef],
        "streamKeys": List[StreamKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "channel": ChannelTypeDef,
        "streamKey": StreamKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamKeyResponseTypeDef = TypedDict(
    "CreateStreamKeyResponseTypeDef",
    {
        "streamKey": StreamKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStreamKeyResponseTypeDef = TypedDict(
    "GetStreamKeyResponseTypeDef",
    {
        "streamKey": StreamKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {
        "channels": List[ChannelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DestinationConfigurationTypeDef = TypedDict(
    "DestinationConfigurationTypeDef",
    {
        "s3": S3DestinationConfigurationTypeDef,
    },
    total=False,
)

GetPlaybackKeyPairResponseTypeDef = TypedDict(
    "GetPlaybackKeyPairResponseTypeDef",
    {
        "keyPair": PlaybackKeyPairTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportPlaybackKeyPairResponseTypeDef = TypedDict(
    "ImportPlaybackKeyPairResponseTypeDef",
    {
        "keyPair": PlaybackKeyPairTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStreamResponseTypeDef = TypedDict(
    "GetStreamResponseTypeDef",
    {
        "stream": StreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IngestConfigurationTypeDef = TypedDict(
    "IngestConfigurationTypeDef",
    {
        "audio": AudioConfigurationTypeDef,
        "video": VideoConfigurationTypeDef,
    },
    total=False,
)

ListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "ListChannelsRequestListChannelsPaginateTypeDef",
    {
        "filterByName": str,
        "filterByRecordingConfigurationArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef = TypedDict(
    "ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef = TypedDict(
    "ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListStreamKeysRequestListStreamKeysPaginateTypeDef = TypedDict(
    "_RequiredListStreamKeysRequestListStreamKeysPaginateTypeDef",
    {
        "channelArn": str,
    },
)
_OptionalListStreamKeysRequestListStreamKeysPaginateTypeDef = TypedDict(
    "_OptionalListStreamKeysRequestListStreamKeysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListStreamKeysRequestListStreamKeysPaginateTypeDef(
    _RequiredListStreamKeysRequestListStreamKeysPaginateTypeDef,
    _OptionalListStreamKeysRequestListStreamKeysPaginateTypeDef,
):
    pass


ListPlaybackKeyPairsResponseTypeDef = TypedDict(
    "ListPlaybackKeyPairsResponseTypeDef",
    {
        "keyPairs": List[PlaybackKeyPairSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStreamKeysResponseTypeDef = TypedDict(
    "ListStreamKeysResponseTypeDef",
    {
        "nextToken": str,
        "streamKeys": List[StreamKeySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStreamSessionsResponseTypeDef = TypedDict(
    "ListStreamSessionsResponseTypeDef",
    {
        "nextToken": str,
        "streamSessions": List[StreamSessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStreamsRequestListStreamsPaginateTypeDef = TypedDict(
    "ListStreamsRequestListStreamsPaginateTypeDef",
    {
        "filterBy": StreamFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListStreamsRequestRequestTypeDef = TypedDict(
    "ListStreamsRequestRequestTypeDef",
    {
        "filterBy": StreamFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListStreamsResponseTypeDef = TypedDict(
    "ListStreamsResponseTypeDef",
    {
        "nextToken": str,
        "streams": List[StreamSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateRecordingConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecordingConfigurationRequestRequestTypeDef",
    {
        "destinationConfiguration": DestinationConfigurationTypeDef,
    },
)
_OptionalCreateRecordingConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecordingConfigurationRequestRequestTypeDef",
    {
        "name": str,
        "tags": Mapping[str, str],
        "thumbnailConfiguration": ThumbnailConfigurationTypeDef,
    },
    total=False,
)


class CreateRecordingConfigurationRequestRequestTypeDef(
    _RequiredCreateRecordingConfigurationRequestRequestTypeDef,
    _OptionalCreateRecordingConfigurationRequestRequestTypeDef,
):
    pass


_RequiredRecordingConfigurationSummaryTypeDef = TypedDict(
    "_RequiredRecordingConfigurationSummaryTypeDef",
    {
        "arn": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
        "state": RecordingConfigurationStateType,
    },
)
_OptionalRecordingConfigurationSummaryTypeDef = TypedDict(
    "_OptionalRecordingConfigurationSummaryTypeDef",
    {
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class RecordingConfigurationSummaryTypeDef(
    _RequiredRecordingConfigurationSummaryTypeDef, _OptionalRecordingConfigurationSummaryTypeDef
):
    pass


_RequiredRecordingConfigurationTypeDef = TypedDict(
    "_RequiredRecordingConfigurationTypeDef",
    {
        "arn": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
        "state": RecordingConfigurationStateType,
    },
)
_OptionalRecordingConfigurationTypeDef = TypedDict(
    "_OptionalRecordingConfigurationTypeDef",
    {
        "name": str,
        "tags": Dict[str, str],
        "thumbnailConfiguration": ThumbnailConfigurationTypeDef,
    },
    total=False,
)


class RecordingConfigurationTypeDef(
    _RequiredRecordingConfigurationTypeDef, _OptionalRecordingConfigurationTypeDef
):
    pass


ListRecordingConfigurationsResponseTypeDef = TypedDict(
    "ListRecordingConfigurationsResponseTypeDef",
    {
        "nextToken": str,
        "recordingConfigurations": List[RecordingConfigurationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecordingConfigurationResponseTypeDef = TypedDict(
    "CreateRecordingConfigurationResponseTypeDef",
    {
        "recordingConfiguration": RecordingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecordingConfigurationResponseTypeDef = TypedDict(
    "GetRecordingConfigurationResponseTypeDef",
    {
        "recordingConfiguration": RecordingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StreamSessionTypeDef = TypedDict(
    "StreamSessionTypeDef",
    {
        "channel": ChannelTypeDef,
        "endTime": datetime,
        "ingestConfiguration": IngestConfigurationTypeDef,
        "recordingConfiguration": RecordingConfigurationTypeDef,
        "startTime": datetime,
        "streamId": str,
        "truncatedEvents": List[StreamEventTypeDef],
    },
    total=False,
)

GetStreamSessionResponseTypeDef = TypedDict(
    "GetStreamSessionResponseTypeDef",
    {
        "streamSession": StreamSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
