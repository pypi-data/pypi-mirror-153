"""
Type annotations for kinesis service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis.type_defs import AddTagsToStreamInputRequestTypeDef

    data: AddTagsToStreamInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ConsumerStatusType,
    EncryptionTypeType,
    MetricsNameType,
    ShardFilterTypeType,
    ShardIteratorTypeType,
    StreamModeType,
    StreamStatusType,
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
    "AddTagsToStreamInputRequestTypeDef",
    "HashKeyRangeTypeDef",
    "ConsumerDescriptionTypeDef",
    "ConsumerTypeDef",
    "StreamModeDetailsTypeDef",
    "DecreaseStreamRetentionPeriodInputRequestTypeDef",
    "DeleteStreamInputRequestTypeDef",
    "DeregisterStreamConsumerInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeStreamConsumerInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeStreamInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeStreamSummaryInputRequestTypeDef",
    "DisableEnhancedMonitoringInputRequestTypeDef",
    "EnableEnhancedMonitoringInputRequestTypeDef",
    "EnhancedMetricsTypeDef",
    "GetRecordsInputRequestTypeDef",
    "RecordTypeDef",
    "GetShardIteratorInputRequestTypeDef",
    "IncreaseStreamRetentionPeriodInputRequestTypeDef",
    "InternalFailureExceptionTypeDef",
    "KMSAccessDeniedExceptionTypeDef",
    "KMSDisabledExceptionTypeDef",
    "KMSInvalidStateExceptionTypeDef",
    "KMSNotFoundExceptionTypeDef",
    "KMSOptInRequiredTypeDef",
    "KMSThrottlingExceptionTypeDef",
    "ShardFilterTypeDef",
    "ListStreamConsumersInputRequestTypeDef",
    "ListStreamsInputRequestTypeDef",
    "ListTagsForStreamInputRequestTypeDef",
    "TagTypeDef",
    "MergeShardsInputRequestTypeDef",
    "PutRecordInputRequestTypeDef",
    "PutRecordsRequestEntryTypeDef",
    "PutRecordsResultEntryTypeDef",
    "RegisterStreamConsumerInputRequestTypeDef",
    "RemoveTagsFromStreamInputRequestTypeDef",
    "ResourceInUseExceptionTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "SequenceNumberRangeTypeDef",
    "SplitShardInputRequestTypeDef",
    "StartStreamEncryptionInputRequestTypeDef",
    "StartingPositionTypeDef",
    "StopStreamEncryptionInputRequestTypeDef",
    "UpdateShardCountInputRequestTypeDef",
    "ChildShardTypeDef",
    "CreateStreamInputRequestTypeDef",
    "UpdateStreamModeInputRequestTypeDef",
    "DescribeLimitsOutputTypeDef",
    "DescribeStreamConsumerOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnhancedMonitoringOutputTypeDef",
    "GetShardIteratorOutputTypeDef",
    "ListStreamConsumersOutputTypeDef",
    "ListStreamsOutputTypeDef",
    "PutRecordOutputTypeDef",
    "RegisterStreamConsumerOutputTypeDef",
    "UpdateShardCountOutputTypeDef",
    "DescribeStreamInputDescribeStreamPaginateTypeDef",
    "ListStreamConsumersInputListStreamConsumersPaginateTypeDef",
    "ListStreamsInputListStreamsPaginateTypeDef",
    "DescribeStreamInputStreamExistsWaitTypeDef",
    "DescribeStreamInputStreamNotExistsWaitTypeDef",
    "StreamDescriptionSummaryTypeDef",
    "ListShardsInputListShardsPaginateTypeDef",
    "ListShardsInputRequestTypeDef",
    "ListTagsForStreamOutputTypeDef",
    "PutRecordsInputRequestTypeDef",
    "PutRecordsOutputTypeDef",
    "ShardTypeDef",
    "SubscribeToShardInputRequestTypeDef",
    "GetRecordsOutputTypeDef",
    "SubscribeToShardEventTypeDef",
    "DescribeStreamSummaryOutputTypeDef",
    "ListShardsOutputTypeDef",
    "StreamDescriptionTypeDef",
    "SubscribeToShardEventStreamTypeDef",
    "DescribeStreamOutputTypeDef",
    "SubscribeToShardOutputTypeDef",
)

AddTagsToStreamInputRequestTypeDef = TypedDict(
    "AddTagsToStreamInputRequestTypeDef",
    {
        "StreamName": str,
        "Tags": Mapping[str, str],
    },
)

HashKeyRangeTypeDef = TypedDict(
    "HashKeyRangeTypeDef",
    {
        "StartingHashKey": str,
        "EndingHashKey": str,
    },
)

ConsumerDescriptionTypeDef = TypedDict(
    "ConsumerDescriptionTypeDef",
    {
        "ConsumerName": str,
        "ConsumerARN": str,
        "ConsumerStatus": ConsumerStatusType,
        "ConsumerCreationTimestamp": datetime,
        "StreamARN": str,
    },
)

ConsumerTypeDef = TypedDict(
    "ConsumerTypeDef",
    {
        "ConsumerName": str,
        "ConsumerARN": str,
        "ConsumerStatus": ConsumerStatusType,
        "ConsumerCreationTimestamp": datetime,
    },
)

StreamModeDetailsTypeDef = TypedDict(
    "StreamModeDetailsTypeDef",
    {
        "StreamMode": StreamModeType,
    },
)

DecreaseStreamRetentionPeriodInputRequestTypeDef = TypedDict(
    "DecreaseStreamRetentionPeriodInputRequestTypeDef",
    {
        "StreamName": str,
        "RetentionPeriodHours": int,
    },
)

_RequiredDeleteStreamInputRequestTypeDef = TypedDict(
    "_RequiredDeleteStreamInputRequestTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalDeleteStreamInputRequestTypeDef = TypedDict(
    "_OptionalDeleteStreamInputRequestTypeDef",
    {
        "EnforceConsumerDeletion": bool,
    },
    total=False,
)


class DeleteStreamInputRequestTypeDef(
    _RequiredDeleteStreamInputRequestTypeDef, _OptionalDeleteStreamInputRequestTypeDef
):
    pass


DeregisterStreamConsumerInputRequestTypeDef = TypedDict(
    "DeregisterStreamConsumerInputRequestTypeDef",
    {
        "StreamARN": str,
        "ConsumerName": str,
        "ConsumerARN": str,
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

DescribeStreamConsumerInputRequestTypeDef = TypedDict(
    "DescribeStreamConsumerInputRequestTypeDef",
    {
        "StreamARN": str,
        "ConsumerName": str,
        "ConsumerARN": str,
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

_RequiredDescribeStreamInputRequestTypeDef = TypedDict(
    "_RequiredDescribeStreamInputRequestTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalDescribeStreamInputRequestTypeDef = TypedDict(
    "_OptionalDescribeStreamInputRequestTypeDef",
    {
        "Limit": int,
        "ExclusiveStartShardId": str,
    },
    total=False,
)


class DescribeStreamInputRequestTypeDef(
    _RequiredDescribeStreamInputRequestTypeDef, _OptionalDescribeStreamInputRequestTypeDef
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeStreamSummaryInputRequestTypeDef = TypedDict(
    "DescribeStreamSummaryInputRequestTypeDef",
    {
        "StreamName": str,
    },
)

DisableEnhancedMonitoringInputRequestTypeDef = TypedDict(
    "DisableEnhancedMonitoringInputRequestTypeDef",
    {
        "StreamName": str,
        "ShardLevelMetrics": Sequence[MetricsNameType],
    },
)

EnableEnhancedMonitoringInputRequestTypeDef = TypedDict(
    "EnableEnhancedMonitoringInputRequestTypeDef",
    {
        "StreamName": str,
        "ShardLevelMetrics": Sequence[MetricsNameType],
    },
)

EnhancedMetricsTypeDef = TypedDict(
    "EnhancedMetricsTypeDef",
    {
        "ShardLevelMetrics": List[MetricsNameType],
    },
    total=False,
)

_RequiredGetRecordsInputRequestTypeDef = TypedDict(
    "_RequiredGetRecordsInputRequestTypeDef",
    {
        "ShardIterator": str,
    },
)
_OptionalGetRecordsInputRequestTypeDef = TypedDict(
    "_OptionalGetRecordsInputRequestTypeDef",
    {
        "Limit": int,
    },
    total=False,
)


class GetRecordsInputRequestTypeDef(
    _RequiredGetRecordsInputRequestTypeDef, _OptionalGetRecordsInputRequestTypeDef
):
    pass


_RequiredRecordTypeDef = TypedDict(
    "_RequiredRecordTypeDef",
    {
        "SequenceNumber": str,
        "Data": bytes,
        "PartitionKey": str,
    },
)
_OptionalRecordTypeDef = TypedDict(
    "_OptionalRecordTypeDef",
    {
        "ApproximateArrivalTimestamp": datetime,
        "EncryptionType": EncryptionTypeType,
    },
    total=False,
)


class RecordTypeDef(_RequiredRecordTypeDef, _OptionalRecordTypeDef):
    pass


_RequiredGetShardIteratorInputRequestTypeDef = TypedDict(
    "_RequiredGetShardIteratorInputRequestTypeDef",
    {
        "StreamName": str,
        "ShardId": str,
        "ShardIteratorType": ShardIteratorTypeType,
    },
)
_OptionalGetShardIteratorInputRequestTypeDef = TypedDict(
    "_OptionalGetShardIteratorInputRequestTypeDef",
    {
        "StartingSequenceNumber": str,
        "Timestamp": Union[datetime, str],
    },
    total=False,
)


class GetShardIteratorInputRequestTypeDef(
    _RequiredGetShardIteratorInputRequestTypeDef, _OptionalGetShardIteratorInputRequestTypeDef
):
    pass


IncreaseStreamRetentionPeriodInputRequestTypeDef = TypedDict(
    "IncreaseStreamRetentionPeriodInputRequestTypeDef",
    {
        "StreamName": str,
        "RetentionPeriodHours": int,
    },
)

InternalFailureExceptionTypeDef = TypedDict(
    "InternalFailureExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSAccessDeniedExceptionTypeDef = TypedDict(
    "KMSAccessDeniedExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSDisabledExceptionTypeDef = TypedDict(
    "KMSDisabledExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSInvalidStateExceptionTypeDef = TypedDict(
    "KMSInvalidStateExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSNotFoundExceptionTypeDef = TypedDict(
    "KMSNotFoundExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSOptInRequiredTypeDef = TypedDict(
    "KMSOptInRequiredTypeDef",
    {
        "message": str,
    },
    total=False,
)

KMSThrottlingExceptionTypeDef = TypedDict(
    "KMSThrottlingExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

_RequiredShardFilterTypeDef = TypedDict(
    "_RequiredShardFilterTypeDef",
    {
        "Type": ShardFilterTypeType,
    },
)
_OptionalShardFilterTypeDef = TypedDict(
    "_OptionalShardFilterTypeDef",
    {
        "ShardId": str,
        "Timestamp": Union[datetime, str],
    },
    total=False,
)


class ShardFilterTypeDef(_RequiredShardFilterTypeDef, _OptionalShardFilterTypeDef):
    pass


_RequiredListStreamConsumersInputRequestTypeDef = TypedDict(
    "_RequiredListStreamConsumersInputRequestTypeDef",
    {
        "StreamARN": str,
    },
)
_OptionalListStreamConsumersInputRequestTypeDef = TypedDict(
    "_OptionalListStreamConsumersInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StreamCreationTimestamp": Union[datetime, str],
    },
    total=False,
)


class ListStreamConsumersInputRequestTypeDef(
    _RequiredListStreamConsumersInputRequestTypeDef, _OptionalListStreamConsumersInputRequestTypeDef
):
    pass


ListStreamsInputRequestTypeDef = TypedDict(
    "ListStreamsInputRequestTypeDef",
    {
        "Limit": int,
        "ExclusiveStartStreamName": str,
    },
    total=False,
)

_RequiredListTagsForStreamInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForStreamInputRequestTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalListTagsForStreamInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForStreamInputRequestTypeDef",
    {
        "ExclusiveStartTagKey": str,
        "Limit": int,
    },
    total=False,
)


class ListTagsForStreamInputRequestTypeDef(
    _RequiredListTagsForStreamInputRequestTypeDef, _OptionalListTagsForStreamInputRequestTypeDef
):
    pass


_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


MergeShardsInputRequestTypeDef = TypedDict(
    "MergeShardsInputRequestTypeDef",
    {
        "StreamName": str,
        "ShardToMerge": str,
        "AdjacentShardToMerge": str,
    },
)

_RequiredPutRecordInputRequestTypeDef = TypedDict(
    "_RequiredPutRecordInputRequestTypeDef",
    {
        "StreamName": str,
        "Data": Union[str, bytes, IO[Any], StreamingBody],
        "PartitionKey": str,
    },
)
_OptionalPutRecordInputRequestTypeDef = TypedDict(
    "_OptionalPutRecordInputRequestTypeDef",
    {
        "ExplicitHashKey": str,
        "SequenceNumberForOrdering": str,
    },
    total=False,
)


class PutRecordInputRequestTypeDef(
    _RequiredPutRecordInputRequestTypeDef, _OptionalPutRecordInputRequestTypeDef
):
    pass


_RequiredPutRecordsRequestEntryTypeDef = TypedDict(
    "_RequiredPutRecordsRequestEntryTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
        "PartitionKey": str,
    },
)
_OptionalPutRecordsRequestEntryTypeDef = TypedDict(
    "_OptionalPutRecordsRequestEntryTypeDef",
    {
        "ExplicitHashKey": str,
    },
    total=False,
)


class PutRecordsRequestEntryTypeDef(
    _RequiredPutRecordsRequestEntryTypeDef, _OptionalPutRecordsRequestEntryTypeDef
):
    pass


PutRecordsResultEntryTypeDef = TypedDict(
    "PutRecordsResultEntryTypeDef",
    {
        "SequenceNumber": str,
        "ShardId": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

RegisterStreamConsumerInputRequestTypeDef = TypedDict(
    "RegisterStreamConsumerInputRequestTypeDef",
    {
        "StreamARN": str,
        "ConsumerName": str,
    },
)

RemoveTagsFromStreamInputRequestTypeDef = TypedDict(
    "RemoveTagsFromStreamInputRequestTypeDef",
    {
        "StreamName": str,
        "TagKeys": Sequence[str],
    },
)

ResourceInUseExceptionTypeDef = TypedDict(
    "ResourceInUseExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

ResourceNotFoundExceptionTypeDef = TypedDict(
    "ResourceNotFoundExceptionTypeDef",
    {
        "message": str,
    },
    total=False,
)

_RequiredSequenceNumberRangeTypeDef = TypedDict(
    "_RequiredSequenceNumberRangeTypeDef",
    {
        "StartingSequenceNumber": str,
    },
)
_OptionalSequenceNumberRangeTypeDef = TypedDict(
    "_OptionalSequenceNumberRangeTypeDef",
    {
        "EndingSequenceNumber": str,
    },
    total=False,
)


class SequenceNumberRangeTypeDef(
    _RequiredSequenceNumberRangeTypeDef, _OptionalSequenceNumberRangeTypeDef
):
    pass


SplitShardInputRequestTypeDef = TypedDict(
    "SplitShardInputRequestTypeDef",
    {
        "StreamName": str,
        "ShardToSplit": str,
        "NewStartingHashKey": str,
    },
)

StartStreamEncryptionInputRequestTypeDef = TypedDict(
    "StartStreamEncryptionInputRequestTypeDef",
    {
        "StreamName": str,
        "EncryptionType": EncryptionTypeType,
        "KeyId": str,
    },
)

_RequiredStartingPositionTypeDef = TypedDict(
    "_RequiredStartingPositionTypeDef",
    {
        "Type": ShardIteratorTypeType,
    },
)
_OptionalStartingPositionTypeDef = TypedDict(
    "_OptionalStartingPositionTypeDef",
    {
        "SequenceNumber": str,
        "Timestamp": Union[datetime, str],
    },
    total=False,
)


class StartingPositionTypeDef(_RequiredStartingPositionTypeDef, _OptionalStartingPositionTypeDef):
    pass


StopStreamEncryptionInputRequestTypeDef = TypedDict(
    "StopStreamEncryptionInputRequestTypeDef",
    {
        "StreamName": str,
        "EncryptionType": EncryptionTypeType,
        "KeyId": str,
    },
)

UpdateShardCountInputRequestTypeDef = TypedDict(
    "UpdateShardCountInputRequestTypeDef",
    {
        "StreamName": str,
        "TargetShardCount": int,
        "ScalingType": Literal["UNIFORM_SCALING"],
    },
)

ChildShardTypeDef = TypedDict(
    "ChildShardTypeDef",
    {
        "ShardId": str,
        "ParentShards": List[str],
        "HashKeyRange": HashKeyRangeTypeDef,
    },
)

_RequiredCreateStreamInputRequestTypeDef = TypedDict(
    "_RequiredCreateStreamInputRequestTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalCreateStreamInputRequestTypeDef = TypedDict(
    "_OptionalCreateStreamInputRequestTypeDef",
    {
        "ShardCount": int,
        "StreamModeDetails": StreamModeDetailsTypeDef,
    },
    total=False,
)


class CreateStreamInputRequestTypeDef(
    _RequiredCreateStreamInputRequestTypeDef, _OptionalCreateStreamInputRequestTypeDef
):
    pass


UpdateStreamModeInputRequestTypeDef = TypedDict(
    "UpdateStreamModeInputRequestTypeDef",
    {
        "StreamARN": str,
        "StreamModeDetails": StreamModeDetailsTypeDef,
    },
)

DescribeLimitsOutputTypeDef = TypedDict(
    "DescribeLimitsOutputTypeDef",
    {
        "ShardLimit": int,
        "OpenShardCount": int,
        "OnDemandStreamCount": int,
        "OnDemandStreamCountLimit": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStreamConsumerOutputTypeDef = TypedDict(
    "DescribeStreamConsumerOutputTypeDef",
    {
        "ConsumerDescription": ConsumerDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnhancedMonitoringOutputTypeDef = TypedDict(
    "EnhancedMonitoringOutputTypeDef",
    {
        "StreamName": str,
        "CurrentShardLevelMetrics": List[MetricsNameType],
        "DesiredShardLevelMetrics": List[MetricsNameType],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetShardIteratorOutputTypeDef = TypedDict(
    "GetShardIteratorOutputTypeDef",
    {
        "ShardIterator": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStreamConsumersOutputTypeDef = TypedDict(
    "ListStreamConsumersOutputTypeDef",
    {
        "Consumers": List[ConsumerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStreamsOutputTypeDef = TypedDict(
    "ListStreamsOutputTypeDef",
    {
        "StreamNames": List[str],
        "HasMoreStreams": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRecordOutputTypeDef = TypedDict(
    "PutRecordOutputTypeDef",
    {
        "ShardId": str,
        "SequenceNumber": str,
        "EncryptionType": EncryptionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterStreamConsumerOutputTypeDef = TypedDict(
    "RegisterStreamConsumerOutputTypeDef",
    {
        "Consumer": ConsumerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateShardCountOutputTypeDef = TypedDict(
    "UpdateShardCountOutputTypeDef",
    {
        "StreamName": str,
        "CurrentShardCount": int,
        "TargetShardCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeStreamInputDescribeStreamPaginateTypeDef = TypedDict(
    "_RequiredDescribeStreamInputDescribeStreamPaginateTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalDescribeStreamInputDescribeStreamPaginateTypeDef = TypedDict(
    "_OptionalDescribeStreamInputDescribeStreamPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeStreamInputDescribeStreamPaginateTypeDef(
    _RequiredDescribeStreamInputDescribeStreamPaginateTypeDef,
    _OptionalDescribeStreamInputDescribeStreamPaginateTypeDef,
):
    pass


_RequiredListStreamConsumersInputListStreamConsumersPaginateTypeDef = TypedDict(
    "_RequiredListStreamConsumersInputListStreamConsumersPaginateTypeDef",
    {
        "StreamARN": str,
    },
)
_OptionalListStreamConsumersInputListStreamConsumersPaginateTypeDef = TypedDict(
    "_OptionalListStreamConsumersInputListStreamConsumersPaginateTypeDef",
    {
        "StreamCreationTimestamp": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListStreamConsumersInputListStreamConsumersPaginateTypeDef(
    _RequiredListStreamConsumersInputListStreamConsumersPaginateTypeDef,
    _OptionalListStreamConsumersInputListStreamConsumersPaginateTypeDef,
):
    pass


ListStreamsInputListStreamsPaginateTypeDef = TypedDict(
    "ListStreamsInputListStreamsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeStreamInputStreamExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeStreamInputStreamExistsWaitTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalDescribeStreamInputStreamExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeStreamInputStreamExistsWaitTypeDef",
    {
        "Limit": int,
        "ExclusiveStartShardId": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeStreamInputStreamExistsWaitTypeDef(
    _RequiredDescribeStreamInputStreamExistsWaitTypeDef,
    _OptionalDescribeStreamInputStreamExistsWaitTypeDef,
):
    pass


_RequiredDescribeStreamInputStreamNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeStreamInputStreamNotExistsWaitTypeDef",
    {
        "StreamName": str,
    },
)
_OptionalDescribeStreamInputStreamNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeStreamInputStreamNotExistsWaitTypeDef",
    {
        "Limit": int,
        "ExclusiveStartShardId": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeStreamInputStreamNotExistsWaitTypeDef(
    _RequiredDescribeStreamInputStreamNotExistsWaitTypeDef,
    _OptionalDescribeStreamInputStreamNotExistsWaitTypeDef,
):
    pass


_RequiredStreamDescriptionSummaryTypeDef = TypedDict(
    "_RequiredStreamDescriptionSummaryTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "StreamStatus": StreamStatusType,
        "RetentionPeriodHours": int,
        "StreamCreationTimestamp": datetime,
        "EnhancedMonitoring": List[EnhancedMetricsTypeDef],
        "OpenShardCount": int,
    },
)
_OptionalStreamDescriptionSummaryTypeDef = TypedDict(
    "_OptionalStreamDescriptionSummaryTypeDef",
    {
        "StreamModeDetails": StreamModeDetailsTypeDef,
        "EncryptionType": EncryptionTypeType,
        "KeyId": str,
        "ConsumerCount": int,
    },
    total=False,
)


class StreamDescriptionSummaryTypeDef(
    _RequiredStreamDescriptionSummaryTypeDef, _OptionalStreamDescriptionSummaryTypeDef
):
    pass


ListShardsInputListShardsPaginateTypeDef = TypedDict(
    "ListShardsInputListShardsPaginateTypeDef",
    {
        "StreamName": str,
        "ExclusiveStartShardId": str,
        "StreamCreationTimestamp": Union[datetime, str],
        "ShardFilter": ShardFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListShardsInputRequestTypeDef = TypedDict(
    "ListShardsInputRequestTypeDef",
    {
        "StreamName": str,
        "NextToken": str,
        "ExclusiveStartShardId": str,
        "MaxResults": int,
        "StreamCreationTimestamp": Union[datetime, str],
        "ShardFilter": ShardFilterTypeDef,
    },
    total=False,
)

ListTagsForStreamOutputTypeDef = TypedDict(
    "ListTagsForStreamOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "HasMoreTags": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRecordsInputRequestTypeDef = TypedDict(
    "PutRecordsInputRequestTypeDef",
    {
        "Records": Sequence[PutRecordsRequestEntryTypeDef],
        "StreamName": str,
    },
)

PutRecordsOutputTypeDef = TypedDict(
    "PutRecordsOutputTypeDef",
    {
        "FailedRecordCount": int,
        "Records": List[PutRecordsResultEntryTypeDef],
        "EncryptionType": EncryptionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredShardTypeDef = TypedDict(
    "_RequiredShardTypeDef",
    {
        "ShardId": str,
        "HashKeyRange": HashKeyRangeTypeDef,
        "SequenceNumberRange": SequenceNumberRangeTypeDef,
    },
)
_OptionalShardTypeDef = TypedDict(
    "_OptionalShardTypeDef",
    {
        "ParentShardId": str,
        "AdjacentParentShardId": str,
    },
    total=False,
)


class ShardTypeDef(_RequiredShardTypeDef, _OptionalShardTypeDef):
    pass


SubscribeToShardInputRequestTypeDef = TypedDict(
    "SubscribeToShardInputRequestTypeDef",
    {
        "ConsumerARN": str,
        "ShardId": str,
        "StartingPosition": StartingPositionTypeDef,
    },
)

GetRecordsOutputTypeDef = TypedDict(
    "GetRecordsOutputTypeDef",
    {
        "Records": List[RecordTypeDef],
        "NextShardIterator": str,
        "MillisBehindLatest": int,
        "ChildShards": List[ChildShardTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSubscribeToShardEventTypeDef = TypedDict(
    "_RequiredSubscribeToShardEventTypeDef",
    {
        "Records": List[RecordTypeDef],
        "ContinuationSequenceNumber": str,
        "MillisBehindLatest": int,
    },
)
_OptionalSubscribeToShardEventTypeDef = TypedDict(
    "_OptionalSubscribeToShardEventTypeDef",
    {
        "ChildShards": List[ChildShardTypeDef],
    },
    total=False,
)


class SubscribeToShardEventTypeDef(
    _RequiredSubscribeToShardEventTypeDef, _OptionalSubscribeToShardEventTypeDef
):
    pass


DescribeStreamSummaryOutputTypeDef = TypedDict(
    "DescribeStreamSummaryOutputTypeDef",
    {
        "StreamDescriptionSummary": StreamDescriptionSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListShardsOutputTypeDef = TypedDict(
    "ListShardsOutputTypeDef",
    {
        "Shards": List[ShardTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStreamDescriptionTypeDef = TypedDict(
    "_RequiredStreamDescriptionTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "StreamStatus": StreamStatusType,
        "Shards": List[ShardTypeDef],
        "HasMoreShards": bool,
        "RetentionPeriodHours": int,
        "StreamCreationTimestamp": datetime,
        "EnhancedMonitoring": List[EnhancedMetricsTypeDef],
    },
)
_OptionalStreamDescriptionTypeDef = TypedDict(
    "_OptionalStreamDescriptionTypeDef",
    {
        "StreamModeDetails": StreamModeDetailsTypeDef,
        "EncryptionType": EncryptionTypeType,
        "KeyId": str,
    },
    total=False,
)


class StreamDescriptionTypeDef(
    _RequiredStreamDescriptionTypeDef, _OptionalStreamDescriptionTypeDef
):
    pass


_RequiredSubscribeToShardEventStreamTypeDef = TypedDict(
    "_RequiredSubscribeToShardEventStreamTypeDef",
    {
        "SubscribeToShardEvent": SubscribeToShardEventTypeDef,
    },
)
_OptionalSubscribeToShardEventStreamTypeDef = TypedDict(
    "_OptionalSubscribeToShardEventStreamTypeDef",
    {
        "ResourceNotFoundException": ResourceNotFoundExceptionTypeDef,
        "ResourceInUseException": ResourceInUseExceptionTypeDef,
        "KMSDisabledException": KMSDisabledExceptionTypeDef,
        "KMSInvalidStateException": KMSInvalidStateExceptionTypeDef,
        "KMSAccessDeniedException": KMSAccessDeniedExceptionTypeDef,
        "KMSNotFoundException": KMSNotFoundExceptionTypeDef,
        "KMSOptInRequired": KMSOptInRequiredTypeDef,
        "KMSThrottlingException": KMSThrottlingExceptionTypeDef,
        "InternalFailureException": InternalFailureExceptionTypeDef,
    },
    total=False,
)


class SubscribeToShardEventStreamTypeDef(
    _RequiredSubscribeToShardEventStreamTypeDef, _OptionalSubscribeToShardEventStreamTypeDef
):
    pass


DescribeStreamOutputTypeDef = TypedDict(
    "DescribeStreamOutputTypeDef",
    {
        "StreamDescription": StreamDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubscribeToShardOutputTypeDef = TypedDict(
    "SubscribeToShardOutputTypeDef",
    {
        "EventStream": SubscribeToShardEventStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
