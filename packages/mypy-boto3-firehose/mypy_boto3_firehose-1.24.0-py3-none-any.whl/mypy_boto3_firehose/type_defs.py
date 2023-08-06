"""
Type annotations for firehose service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/type_defs/)

Usage::

    ```python
    from mypy_boto3_firehose.type_defs import AmazonopensearchserviceBufferingHintsTypeDef

    data: AmazonopensearchserviceBufferingHintsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AmazonopensearchserviceIndexRotationPeriodType,
    AmazonopensearchserviceS3BackupModeType,
    CompressionFormatType,
    ContentEncodingType,
    DeliveryStreamEncryptionStatusType,
    DeliveryStreamFailureTypeType,
    DeliveryStreamStatusType,
    DeliveryStreamTypeType,
    ElasticsearchIndexRotationPeriodType,
    ElasticsearchS3BackupModeType,
    HECEndpointTypeType,
    HttpEndpointS3BackupModeType,
    KeyTypeType,
    OrcCompressionType,
    OrcFormatVersionType,
    ParquetCompressionType,
    ParquetWriterVersionType,
    ProcessorParameterNameType,
    ProcessorTypeType,
    RedshiftS3BackupModeType,
    S3BackupModeType,
    SplunkS3BackupModeType,
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
    "AmazonopensearchserviceBufferingHintsTypeDef",
    "AmazonopensearchserviceRetryOptionsTypeDef",
    "CloudWatchLoggingOptionsTypeDef",
    "VpcConfigurationTypeDef",
    "VpcConfigurationDescriptionTypeDef",
    "BufferingHintsTypeDef",
    "CopyCommandTypeDef",
    "DeliveryStreamEncryptionConfigurationInputTypeDef",
    "KinesisStreamSourceConfigurationTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "SchemaConfigurationTypeDef",
    "DeleteDeliveryStreamInputRequestTypeDef",
    "FailureDescriptionTypeDef",
    "DescribeDeliveryStreamInputRequestTypeDef",
    "HiveJsonSerDeTypeDef",
    "OpenXJsonSerDeTypeDef",
    "RetryOptionsTypeDef",
    "ElasticsearchBufferingHintsTypeDef",
    "ElasticsearchRetryOptionsTypeDef",
    "KMSEncryptionConfigTypeDef",
    "HttpEndpointBufferingHintsTypeDef",
    "HttpEndpointCommonAttributeTypeDef",
    "HttpEndpointConfigurationTypeDef",
    "HttpEndpointDescriptionTypeDef",
    "HttpEndpointRetryOptionsTypeDef",
    "KinesisStreamSourceDescriptionTypeDef",
    "ListDeliveryStreamsInputRequestTypeDef",
    "ListTagsForDeliveryStreamInputRequestTypeDef",
    "OrcSerDeTypeDef",
    "ParquetSerDeTypeDef",
    "ProcessorParameterTypeDef",
    "RecordTypeDef",
    "PutRecordBatchResponseEntryTypeDef",
    "RedshiftRetryOptionsTypeDef",
    "SplunkRetryOptionsTypeDef",
    "StopDeliveryStreamEncryptionInputRequestTypeDef",
    "UntagDeliveryStreamInputRequestTypeDef",
    "StartDeliveryStreamEncryptionInputRequestTypeDef",
    "TagDeliveryStreamInputRequestTypeDef",
    "CreateDeliveryStreamOutputTypeDef",
    "ListDeliveryStreamsOutputTypeDef",
    "ListTagsForDeliveryStreamOutputTypeDef",
    "PutRecordOutputTypeDef",
    "DeliveryStreamEncryptionConfigurationTypeDef",
    "DeserializerTypeDef",
    "DynamicPartitioningConfigurationTypeDef",
    "EncryptionConfigurationTypeDef",
    "HttpEndpointRequestConfigurationTypeDef",
    "SourceDescriptionTypeDef",
    "SerializerTypeDef",
    "ProcessorTypeDef",
    "PutRecordBatchInputRequestTypeDef",
    "PutRecordInputRequestTypeDef",
    "PutRecordBatchOutputTypeDef",
    "InputFormatConfigurationTypeDef",
    "S3DestinationConfigurationTypeDef",
    "S3DestinationDescriptionTypeDef",
    "S3DestinationUpdateTypeDef",
    "OutputFormatConfigurationTypeDef",
    "ProcessingConfigurationTypeDef",
    "DataFormatConversionConfigurationTypeDef",
    "AmazonopensearchserviceDestinationConfigurationTypeDef",
    "AmazonopensearchserviceDestinationDescriptionTypeDef",
    "AmazonopensearchserviceDestinationUpdateTypeDef",
    "ElasticsearchDestinationConfigurationTypeDef",
    "ElasticsearchDestinationDescriptionTypeDef",
    "ElasticsearchDestinationUpdateTypeDef",
    "HttpEndpointDestinationConfigurationTypeDef",
    "HttpEndpointDestinationDescriptionTypeDef",
    "HttpEndpointDestinationUpdateTypeDef",
    "RedshiftDestinationConfigurationTypeDef",
    "RedshiftDestinationDescriptionTypeDef",
    "RedshiftDestinationUpdateTypeDef",
    "SplunkDestinationConfigurationTypeDef",
    "SplunkDestinationDescriptionTypeDef",
    "SplunkDestinationUpdateTypeDef",
    "ExtendedS3DestinationConfigurationTypeDef",
    "ExtendedS3DestinationDescriptionTypeDef",
    "ExtendedS3DestinationUpdateTypeDef",
    "CreateDeliveryStreamInputRequestTypeDef",
    "DestinationDescriptionTypeDef",
    "UpdateDestinationInputRequestTypeDef",
    "DeliveryStreamDescriptionTypeDef",
    "DescribeDeliveryStreamOutputTypeDef",
)

AmazonopensearchserviceBufferingHintsTypeDef = TypedDict(
    "AmazonopensearchserviceBufferingHintsTypeDef",
    {
        "IntervalInSeconds": int,
        "SizeInMBs": int,
    },
    total=False,
)

AmazonopensearchserviceRetryOptionsTypeDef = TypedDict(
    "AmazonopensearchserviceRetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

CloudWatchLoggingOptionsTypeDef = TypedDict(
    "CloudWatchLoggingOptionsTypeDef",
    {
        "Enabled": bool,
        "LogGroupName": str,
        "LogStreamName": str,
    },
    total=False,
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "SubnetIds": Sequence[str],
        "RoleARN": str,
        "SecurityGroupIds": Sequence[str],
    },
)

VpcConfigurationDescriptionTypeDef = TypedDict(
    "VpcConfigurationDescriptionTypeDef",
    {
        "SubnetIds": List[str],
        "RoleARN": str,
        "SecurityGroupIds": List[str],
        "VpcId": str,
    },
)

BufferingHintsTypeDef = TypedDict(
    "BufferingHintsTypeDef",
    {
        "SizeInMBs": int,
        "IntervalInSeconds": int,
    },
    total=False,
)

_RequiredCopyCommandTypeDef = TypedDict(
    "_RequiredCopyCommandTypeDef",
    {
        "DataTableName": str,
    },
)
_OptionalCopyCommandTypeDef = TypedDict(
    "_OptionalCopyCommandTypeDef",
    {
        "DataTableColumns": str,
        "CopyOptions": str,
    },
    total=False,
)


class CopyCommandTypeDef(_RequiredCopyCommandTypeDef, _OptionalCopyCommandTypeDef):
    pass


_RequiredDeliveryStreamEncryptionConfigurationInputTypeDef = TypedDict(
    "_RequiredDeliveryStreamEncryptionConfigurationInputTypeDef",
    {
        "KeyType": KeyTypeType,
    },
)
_OptionalDeliveryStreamEncryptionConfigurationInputTypeDef = TypedDict(
    "_OptionalDeliveryStreamEncryptionConfigurationInputTypeDef",
    {
        "KeyARN": str,
    },
    total=False,
)


class DeliveryStreamEncryptionConfigurationInputTypeDef(
    _RequiredDeliveryStreamEncryptionConfigurationInputTypeDef,
    _OptionalDeliveryStreamEncryptionConfigurationInputTypeDef,
):
    pass


KinesisStreamSourceConfigurationTypeDef = TypedDict(
    "KinesisStreamSourceConfigurationTypeDef",
    {
        "KinesisStreamARN": str,
        "RoleARN": str,
    },
)

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

SchemaConfigurationTypeDef = TypedDict(
    "SchemaConfigurationTypeDef",
    {
        "RoleARN": str,
        "CatalogId": str,
        "DatabaseName": str,
        "TableName": str,
        "Region": str,
        "VersionId": str,
    },
    total=False,
)

_RequiredDeleteDeliveryStreamInputRequestTypeDef = TypedDict(
    "_RequiredDeleteDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)
_OptionalDeleteDeliveryStreamInputRequestTypeDef = TypedDict(
    "_OptionalDeleteDeliveryStreamInputRequestTypeDef",
    {
        "AllowForceDelete": bool,
    },
    total=False,
)


class DeleteDeliveryStreamInputRequestTypeDef(
    _RequiredDeleteDeliveryStreamInputRequestTypeDef,
    _OptionalDeleteDeliveryStreamInputRequestTypeDef,
):
    pass


FailureDescriptionTypeDef = TypedDict(
    "FailureDescriptionTypeDef",
    {
        "Type": DeliveryStreamFailureTypeType,
        "Details": str,
    },
)

_RequiredDescribeDeliveryStreamInputRequestTypeDef = TypedDict(
    "_RequiredDescribeDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)
_OptionalDescribeDeliveryStreamInputRequestTypeDef = TypedDict(
    "_OptionalDescribeDeliveryStreamInputRequestTypeDef",
    {
        "Limit": int,
        "ExclusiveStartDestinationId": str,
    },
    total=False,
)


class DescribeDeliveryStreamInputRequestTypeDef(
    _RequiredDescribeDeliveryStreamInputRequestTypeDef,
    _OptionalDescribeDeliveryStreamInputRequestTypeDef,
):
    pass


HiveJsonSerDeTypeDef = TypedDict(
    "HiveJsonSerDeTypeDef",
    {
        "TimestampFormats": Sequence[str],
    },
    total=False,
)

OpenXJsonSerDeTypeDef = TypedDict(
    "OpenXJsonSerDeTypeDef",
    {
        "ConvertDotsInJsonKeysToUnderscores": bool,
        "CaseInsensitive": bool,
        "ColumnToJsonKeyMappings": Mapping[str, str],
    },
    total=False,
)

RetryOptionsTypeDef = TypedDict(
    "RetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

ElasticsearchBufferingHintsTypeDef = TypedDict(
    "ElasticsearchBufferingHintsTypeDef",
    {
        "IntervalInSeconds": int,
        "SizeInMBs": int,
    },
    total=False,
)

ElasticsearchRetryOptionsTypeDef = TypedDict(
    "ElasticsearchRetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

KMSEncryptionConfigTypeDef = TypedDict(
    "KMSEncryptionConfigTypeDef",
    {
        "AWSKMSKeyARN": str,
    },
)

HttpEndpointBufferingHintsTypeDef = TypedDict(
    "HttpEndpointBufferingHintsTypeDef",
    {
        "SizeInMBs": int,
        "IntervalInSeconds": int,
    },
    total=False,
)

HttpEndpointCommonAttributeTypeDef = TypedDict(
    "HttpEndpointCommonAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValue": str,
    },
)

_RequiredHttpEndpointConfigurationTypeDef = TypedDict(
    "_RequiredHttpEndpointConfigurationTypeDef",
    {
        "Url": str,
    },
)
_OptionalHttpEndpointConfigurationTypeDef = TypedDict(
    "_OptionalHttpEndpointConfigurationTypeDef",
    {
        "Name": str,
        "AccessKey": str,
    },
    total=False,
)


class HttpEndpointConfigurationTypeDef(
    _RequiredHttpEndpointConfigurationTypeDef, _OptionalHttpEndpointConfigurationTypeDef
):
    pass


HttpEndpointDescriptionTypeDef = TypedDict(
    "HttpEndpointDescriptionTypeDef",
    {
        "Url": str,
        "Name": str,
    },
    total=False,
)

HttpEndpointRetryOptionsTypeDef = TypedDict(
    "HttpEndpointRetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

KinesisStreamSourceDescriptionTypeDef = TypedDict(
    "KinesisStreamSourceDescriptionTypeDef",
    {
        "KinesisStreamARN": str,
        "RoleARN": str,
        "DeliveryStartTimestamp": datetime,
    },
    total=False,
)

ListDeliveryStreamsInputRequestTypeDef = TypedDict(
    "ListDeliveryStreamsInputRequestTypeDef",
    {
        "Limit": int,
        "DeliveryStreamType": DeliveryStreamTypeType,
        "ExclusiveStartDeliveryStreamName": str,
    },
    total=False,
)

_RequiredListTagsForDeliveryStreamInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)
_OptionalListTagsForDeliveryStreamInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForDeliveryStreamInputRequestTypeDef",
    {
        "ExclusiveStartTagKey": str,
        "Limit": int,
    },
    total=False,
)


class ListTagsForDeliveryStreamInputRequestTypeDef(
    _RequiredListTagsForDeliveryStreamInputRequestTypeDef,
    _OptionalListTagsForDeliveryStreamInputRequestTypeDef,
):
    pass


OrcSerDeTypeDef = TypedDict(
    "OrcSerDeTypeDef",
    {
        "StripeSizeBytes": int,
        "BlockSizeBytes": int,
        "RowIndexStride": int,
        "EnablePadding": bool,
        "PaddingTolerance": float,
        "Compression": OrcCompressionType,
        "BloomFilterColumns": Sequence[str],
        "BloomFilterFalsePositiveProbability": float,
        "DictionaryKeyThreshold": float,
        "FormatVersion": OrcFormatVersionType,
    },
    total=False,
)

ParquetSerDeTypeDef = TypedDict(
    "ParquetSerDeTypeDef",
    {
        "BlockSizeBytes": int,
        "PageSizeBytes": int,
        "Compression": ParquetCompressionType,
        "EnableDictionaryCompression": bool,
        "MaxPaddingBytes": int,
        "WriterVersion": ParquetWriterVersionType,
    },
    total=False,
)

ProcessorParameterTypeDef = TypedDict(
    "ProcessorParameterTypeDef",
    {
        "ParameterName": ProcessorParameterNameType,
        "ParameterValue": str,
    },
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "Data": Union[str, bytes, IO[Any], StreamingBody],
    },
)

PutRecordBatchResponseEntryTypeDef = TypedDict(
    "PutRecordBatchResponseEntryTypeDef",
    {
        "RecordId": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

RedshiftRetryOptionsTypeDef = TypedDict(
    "RedshiftRetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

SplunkRetryOptionsTypeDef = TypedDict(
    "SplunkRetryOptionsTypeDef",
    {
        "DurationInSeconds": int,
    },
    total=False,
)

StopDeliveryStreamEncryptionInputRequestTypeDef = TypedDict(
    "StopDeliveryStreamEncryptionInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)

UntagDeliveryStreamInputRequestTypeDef = TypedDict(
    "UntagDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredStartDeliveryStreamEncryptionInputRequestTypeDef = TypedDict(
    "_RequiredStartDeliveryStreamEncryptionInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)
_OptionalStartDeliveryStreamEncryptionInputRequestTypeDef = TypedDict(
    "_OptionalStartDeliveryStreamEncryptionInputRequestTypeDef",
    {
        "DeliveryStreamEncryptionConfigurationInput": DeliveryStreamEncryptionConfigurationInputTypeDef,
    },
    total=False,
)


class StartDeliveryStreamEncryptionInputRequestTypeDef(
    _RequiredStartDeliveryStreamEncryptionInputRequestTypeDef,
    _OptionalStartDeliveryStreamEncryptionInputRequestTypeDef,
):
    pass


TagDeliveryStreamInputRequestTypeDef = TypedDict(
    "TagDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateDeliveryStreamOutputTypeDef = TypedDict(
    "CreateDeliveryStreamOutputTypeDef",
    {
        "DeliveryStreamARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeliveryStreamsOutputTypeDef = TypedDict(
    "ListDeliveryStreamsOutputTypeDef",
    {
        "DeliveryStreamNames": List[str],
        "HasMoreDeliveryStreams": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForDeliveryStreamOutputTypeDef = TypedDict(
    "ListTagsForDeliveryStreamOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "HasMoreTags": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRecordOutputTypeDef = TypedDict(
    "PutRecordOutputTypeDef",
    {
        "RecordId": str,
        "Encrypted": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeliveryStreamEncryptionConfigurationTypeDef = TypedDict(
    "DeliveryStreamEncryptionConfigurationTypeDef",
    {
        "KeyARN": str,
        "KeyType": KeyTypeType,
        "Status": DeliveryStreamEncryptionStatusType,
        "FailureDescription": FailureDescriptionTypeDef,
    },
    total=False,
)

DeserializerTypeDef = TypedDict(
    "DeserializerTypeDef",
    {
        "OpenXJsonSerDe": OpenXJsonSerDeTypeDef,
        "HiveJsonSerDe": HiveJsonSerDeTypeDef,
    },
    total=False,
)

DynamicPartitioningConfigurationTypeDef = TypedDict(
    "DynamicPartitioningConfigurationTypeDef",
    {
        "RetryOptions": RetryOptionsTypeDef,
        "Enabled": bool,
    },
    total=False,
)

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "NoEncryptionConfig": Literal["NoEncryption"],
        "KMSEncryptionConfig": KMSEncryptionConfigTypeDef,
    },
    total=False,
)

HttpEndpointRequestConfigurationTypeDef = TypedDict(
    "HttpEndpointRequestConfigurationTypeDef",
    {
        "ContentEncoding": ContentEncodingType,
        "CommonAttributes": Sequence[HttpEndpointCommonAttributeTypeDef],
    },
    total=False,
)

SourceDescriptionTypeDef = TypedDict(
    "SourceDescriptionTypeDef",
    {
        "KinesisStreamSourceDescription": KinesisStreamSourceDescriptionTypeDef,
    },
    total=False,
)

SerializerTypeDef = TypedDict(
    "SerializerTypeDef",
    {
        "ParquetSerDe": ParquetSerDeTypeDef,
        "OrcSerDe": OrcSerDeTypeDef,
    },
    total=False,
)

_RequiredProcessorTypeDef = TypedDict(
    "_RequiredProcessorTypeDef",
    {
        "Type": ProcessorTypeType,
    },
)
_OptionalProcessorTypeDef = TypedDict(
    "_OptionalProcessorTypeDef",
    {
        "Parameters": Sequence[ProcessorParameterTypeDef],
    },
    total=False,
)


class ProcessorTypeDef(_RequiredProcessorTypeDef, _OptionalProcessorTypeDef):
    pass


PutRecordBatchInputRequestTypeDef = TypedDict(
    "PutRecordBatchInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
        "Records": Sequence[RecordTypeDef],
    },
)

PutRecordInputRequestTypeDef = TypedDict(
    "PutRecordInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
        "Record": RecordTypeDef,
    },
)

PutRecordBatchOutputTypeDef = TypedDict(
    "PutRecordBatchOutputTypeDef",
    {
        "FailedPutCount": int,
        "Encrypted": bool,
        "RequestResponses": List[PutRecordBatchResponseEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InputFormatConfigurationTypeDef = TypedDict(
    "InputFormatConfigurationTypeDef",
    {
        "Deserializer": DeserializerTypeDef,
    },
    total=False,
)

_RequiredS3DestinationConfigurationTypeDef = TypedDict(
    "_RequiredS3DestinationConfigurationTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
    },
)
_OptionalS3DestinationConfigurationTypeDef = TypedDict(
    "_OptionalS3DestinationConfigurationTypeDef",
    {
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)


class S3DestinationConfigurationTypeDef(
    _RequiredS3DestinationConfigurationTypeDef, _OptionalS3DestinationConfigurationTypeDef
):
    pass


_RequiredS3DestinationDescriptionTypeDef = TypedDict(
    "_RequiredS3DestinationDescriptionTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
)
_OptionalS3DestinationDescriptionTypeDef = TypedDict(
    "_OptionalS3DestinationDescriptionTypeDef",
    {
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)


class S3DestinationDescriptionTypeDef(
    _RequiredS3DestinationDescriptionTypeDef, _OptionalS3DestinationDescriptionTypeDef
):
    pass


S3DestinationUpdateTypeDef = TypedDict(
    "S3DestinationUpdateTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

OutputFormatConfigurationTypeDef = TypedDict(
    "OutputFormatConfigurationTypeDef",
    {
        "Serializer": SerializerTypeDef,
    },
    total=False,
)

ProcessingConfigurationTypeDef = TypedDict(
    "ProcessingConfigurationTypeDef",
    {
        "Enabled": bool,
        "Processors": Sequence[ProcessorTypeDef],
    },
    total=False,
)

DataFormatConversionConfigurationTypeDef = TypedDict(
    "DataFormatConversionConfigurationTypeDef",
    {
        "SchemaConfiguration": SchemaConfigurationTypeDef,
        "InputFormatConfiguration": InputFormatConfigurationTypeDef,
        "OutputFormatConfiguration": OutputFormatConfigurationTypeDef,
        "Enabled": bool,
    },
    total=False,
)

_RequiredAmazonopensearchserviceDestinationConfigurationTypeDef = TypedDict(
    "_RequiredAmazonopensearchserviceDestinationConfigurationTypeDef",
    {
        "RoleARN": str,
        "IndexName": str,
        "S3Configuration": S3DestinationConfigurationTypeDef,
    },
)
_OptionalAmazonopensearchserviceDestinationConfigurationTypeDef = TypedDict(
    "_OptionalAmazonopensearchserviceDestinationConfigurationTypeDef",
    {
        "DomainARN": str,
        "ClusterEndpoint": str,
        "TypeName": str,
        "IndexRotationPeriod": AmazonopensearchserviceIndexRotationPeriodType,
        "BufferingHints": AmazonopensearchserviceBufferingHintsTypeDef,
        "RetryOptions": AmazonopensearchserviceRetryOptionsTypeDef,
        "S3BackupMode": AmazonopensearchserviceS3BackupModeType,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "VpcConfiguration": VpcConfigurationTypeDef,
    },
    total=False,
)


class AmazonopensearchserviceDestinationConfigurationTypeDef(
    _RequiredAmazonopensearchserviceDestinationConfigurationTypeDef,
    _OptionalAmazonopensearchserviceDestinationConfigurationTypeDef,
):
    pass


AmazonopensearchserviceDestinationDescriptionTypeDef = TypedDict(
    "AmazonopensearchserviceDestinationDescriptionTypeDef",
    {
        "RoleARN": str,
        "DomainARN": str,
        "ClusterEndpoint": str,
        "IndexName": str,
        "TypeName": str,
        "IndexRotationPeriod": AmazonopensearchserviceIndexRotationPeriodType,
        "BufferingHints": AmazonopensearchserviceBufferingHintsTypeDef,
        "RetryOptions": AmazonopensearchserviceRetryOptionsTypeDef,
        "S3BackupMode": AmazonopensearchserviceS3BackupModeType,
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "VpcConfigurationDescription": VpcConfigurationDescriptionTypeDef,
    },
    total=False,
)

AmazonopensearchserviceDestinationUpdateTypeDef = TypedDict(
    "AmazonopensearchserviceDestinationUpdateTypeDef",
    {
        "RoleARN": str,
        "DomainARN": str,
        "ClusterEndpoint": str,
        "IndexName": str,
        "TypeName": str,
        "IndexRotationPeriod": AmazonopensearchserviceIndexRotationPeriodType,
        "BufferingHints": AmazonopensearchserviceBufferingHintsTypeDef,
        "RetryOptions": AmazonopensearchserviceRetryOptionsTypeDef,
        "S3Update": S3DestinationUpdateTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

_RequiredElasticsearchDestinationConfigurationTypeDef = TypedDict(
    "_RequiredElasticsearchDestinationConfigurationTypeDef",
    {
        "RoleARN": str,
        "IndexName": str,
        "S3Configuration": S3DestinationConfigurationTypeDef,
    },
)
_OptionalElasticsearchDestinationConfigurationTypeDef = TypedDict(
    "_OptionalElasticsearchDestinationConfigurationTypeDef",
    {
        "DomainARN": str,
        "ClusterEndpoint": str,
        "TypeName": str,
        "IndexRotationPeriod": ElasticsearchIndexRotationPeriodType,
        "BufferingHints": ElasticsearchBufferingHintsTypeDef,
        "RetryOptions": ElasticsearchRetryOptionsTypeDef,
        "S3BackupMode": ElasticsearchS3BackupModeType,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "VpcConfiguration": VpcConfigurationTypeDef,
    },
    total=False,
)


class ElasticsearchDestinationConfigurationTypeDef(
    _RequiredElasticsearchDestinationConfigurationTypeDef,
    _OptionalElasticsearchDestinationConfigurationTypeDef,
):
    pass


ElasticsearchDestinationDescriptionTypeDef = TypedDict(
    "ElasticsearchDestinationDescriptionTypeDef",
    {
        "RoleARN": str,
        "DomainARN": str,
        "ClusterEndpoint": str,
        "IndexName": str,
        "TypeName": str,
        "IndexRotationPeriod": ElasticsearchIndexRotationPeriodType,
        "BufferingHints": ElasticsearchBufferingHintsTypeDef,
        "RetryOptions": ElasticsearchRetryOptionsTypeDef,
        "S3BackupMode": ElasticsearchS3BackupModeType,
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "VpcConfigurationDescription": VpcConfigurationDescriptionTypeDef,
    },
    total=False,
)

ElasticsearchDestinationUpdateTypeDef = TypedDict(
    "ElasticsearchDestinationUpdateTypeDef",
    {
        "RoleARN": str,
        "DomainARN": str,
        "ClusterEndpoint": str,
        "IndexName": str,
        "TypeName": str,
        "IndexRotationPeriod": ElasticsearchIndexRotationPeriodType,
        "BufferingHints": ElasticsearchBufferingHintsTypeDef,
        "RetryOptions": ElasticsearchRetryOptionsTypeDef,
        "S3Update": S3DestinationUpdateTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

_RequiredHttpEndpointDestinationConfigurationTypeDef = TypedDict(
    "_RequiredHttpEndpointDestinationConfigurationTypeDef",
    {
        "EndpointConfiguration": HttpEndpointConfigurationTypeDef,
        "S3Configuration": S3DestinationConfigurationTypeDef,
    },
)
_OptionalHttpEndpointDestinationConfigurationTypeDef = TypedDict(
    "_OptionalHttpEndpointDestinationConfigurationTypeDef",
    {
        "BufferingHints": HttpEndpointBufferingHintsTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "RequestConfiguration": HttpEndpointRequestConfigurationTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "RoleARN": str,
        "RetryOptions": HttpEndpointRetryOptionsTypeDef,
        "S3BackupMode": HttpEndpointS3BackupModeType,
    },
    total=False,
)


class HttpEndpointDestinationConfigurationTypeDef(
    _RequiredHttpEndpointDestinationConfigurationTypeDef,
    _OptionalHttpEndpointDestinationConfigurationTypeDef,
):
    pass


HttpEndpointDestinationDescriptionTypeDef = TypedDict(
    "HttpEndpointDestinationDescriptionTypeDef",
    {
        "EndpointConfiguration": HttpEndpointDescriptionTypeDef,
        "BufferingHints": HttpEndpointBufferingHintsTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "RequestConfiguration": HttpEndpointRequestConfigurationTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "RoleARN": str,
        "RetryOptions": HttpEndpointRetryOptionsTypeDef,
        "S3BackupMode": HttpEndpointS3BackupModeType,
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
    },
    total=False,
)

HttpEndpointDestinationUpdateTypeDef = TypedDict(
    "HttpEndpointDestinationUpdateTypeDef",
    {
        "EndpointConfiguration": HttpEndpointConfigurationTypeDef,
        "BufferingHints": HttpEndpointBufferingHintsTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "RequestConfiguration": HttpEndpointRequestConfigurationTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "RoleARN": str,
        "RetryOptions": HttpEndpointRetryOptionsTypeDef,
        "S3BackupMode": HttpEndpointS3BackupModeType,
        "S3Update": S3DestinationUpdateTypeDef,
    },
    total=False,
)

_RequiredRedshiftDestinationConfigurationTypeDef = TypedDict(
    "_RequiredRedshiftDestinationConfigurationTypeDef",
    {
        "RoleARN": str,
        "ClusterJDBCURL": str,
        "CopyCommand": CopyCommandTypeDef,
        "Username": str,
        "Password": str,
        "S3Configuration": S3DestinationConfigurationTypeDef,
    },
)
_OptionalRedshiftDestinationConfigurationTypeDef = TypedDict(
    "_OptionalRedshiftDestinationConfigurationTypeDef",
    {
        "RetryOptions": RedshiftRetryOptionsTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": RedshiftS3BackupModeType,
        "S3BackupConfiguration": S3DestinationConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)


class RedshiftDestinationConfigurationTypeDef(
    _RequiredRedshiftDestinationConfigurationTypeDef,
    _OptionalRedshiftDestinationConfigurationTypeDef,
):
    pass


_RequiredRedshiftDestinationDescriptionTypeDef = TypedDict(
    "_RequiredRedshiftDestinationDescriptionTypeDef",
    {
        "RoleARN": str,
        "ClusterJDBCURL": str,
        "CopyCommand": CopyCommandTypeDef,
        "Username": str,
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
    },
)
_OptionalRedshiftDestinationDescriptionTypeDef = TypedDict(
    "_OptionalRedshiftDestinationDescriptionTypeDef",
    {
        "RetryOptions": RedshiftRetryOptionsTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": RedshiftS3BackupModeType,
        "S3BackupDescription": S3DestinationDescriptionTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)


class RedshiftDestinationDescriptionTypeDef(
    _RequiredRedshiftDestinationDescriptionTypeDef, _OptionalRedshiftDestinationDescriptionTypeDef
):
    pass


RedshiftDestinationUpdateTypeDef = TypedDict(
    "RedshiftDestinationUpdateTypeDef",
    {
        "RoleARN": str,
        "ClusterJDBCURL": str,
        "CopyCommand": CopyCommandTypeDef,
        "Username": str,
        "Password": str,
        "RetryOptions": RedshiftRetryOptionsTypeDef,
        "S3Update": S3DestinationUpdateTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": RedshiftS3BackupModeType,
        "S3BackupUpdate": S3DestinationUpdateTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

_RequiredSplunkDestinationConfigurationTypeDef = TypedDict(
    "_RequiredSplunkDestinationConfigurationTypeDef",
    {
        "HECEndpoint": str,
        "HECEndpointType": HECEndpointTypeType,
        "HECToken": str,
        "S3Configuration": S3DestinationConfigurationTypeDef,
    },
)
_OptionalSplunkDestinationConfigurationTypeDef = TypedDict(
    "_OptionalSplunkDestinationConfigurationTypeDef",
    {
        "HECAcknowledgmentTimeoutInSeconds": int,
        "RetryOptions": SplunkRetryOptionsTypeDef,
        "S3BackupMode": SplunkS3BackupModeType,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)


class SplunkDestinationConfigurationTypeDef(
    _RequiredSplunkDestinationConfigurationTypeDef, _OptionalSplunkDestinationConfigurationTypeDef
):
    pass


SplunkDestinationDescriptionTypeDef = TypedDict(
    "SplunkDestinationDescriptionTypeDef",
    {
        "HECEndpoint": str,
        "HECEndpointType": HECEndpointTypeType,
        "HECToken": str,
        "HECAcknowledgmentTimeoutInSeconds": int,
        "RetryOptions": SplunkRetryOptionsTypeDef,
        "S3BackupMode": SplunkS3BackupModeType,
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

SplunkDestinationUpdateTypeDef = TypedDict(
    "SplunkDestinationUpdateTypeDef",
    {
        "HECEndpoint": str,
        "HECEndpointType": HECEndpointTypeType,
        "HECToken": str,
        "HECAcknowledgmentTimeoutInSeconds": int,
        "RetryOptions": SplunkRetryOptionsTypeDef,
        "S3BackupMode": SplunkS3BackupModeType,
        "S3Update": S3DestinationUpdateTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
    },
    total=False,
)

_RequiredExtendedS3DestinationConfigurationTypeDef = TypedDict(
    "_RequiredExtendedS3DestinationConfigurationTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
    },
)
_OptionalExtendedS3DestinationConfigurationTypeDef = TypedDict(
    "_OptionalExtendedS3DestinationConfigurationTypeDef",
    {
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": S3BackupModeType,
        "S3BackupConfiguration": S3DestinationConfigurationTypeDef,
        "DataFormatConversionConfiguration": DataFormatConversionConfigurationTypeDef,
        "DynamicPartitioningConfiguration": DynamicPartitioningConfigurationTypeDef,
    },
    total=False,
)


class ExtendedS3DestinationConfigurationTypeDef(
    _RequiredExtendedS3DestinationConfigurationTypeDef,
    _OptionalExtendedS3DestinationConfigurationTypeDef,
):
    pass


_RequiredExtendedS3DestinationDescriptionTypeDef = TypedDict(
    "_RequiredExtendedS3DestinationDescriptionTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
)
_OptionalExtendedS3DestinationDescriptionTypeDef = TypedDict(
    "_OptionalExtendedS3DestinationDescriptionTypeDef",
    {
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": S3BackupModeType,
        "S3BackupDescription": S3DestinationDescriptionTypeDef,
        "DataFormatConversionConfiguration": DataFormatConversionConfigurationTypeDef,
        "DynamicPartitioningConfiguration": DynamicPartitioningConfigurationTypeDef,
    },
    total=False,
)


class ExtendedS3DestinationDescriptionTypeDef(
    _RequiredExtendedS3DestinationDescriptionTypeDef,
    _OptionalExtendedS3DestinationDescriptionTypeDef,
):
    pass


ExtendedS3DestinationUpdateTypeDef = TypedDict(
    "ExtendedS3DestinationUpdateTypeDef",
    {
        "RoleARN": str,
        "BucketARN": str,
        "Prefix": str,
        "ErrorOutputPrefix": str,
        "BufferingHints": BufferingHintsTypeDef,
        "CompressionFormat": CompressionFormatType,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "CloudWatchLoggingOptions": CloudWatchLoggingOptionsTypeDef,
        "ProcessingConfiguration": ProcessingConfigurationTypeDef,
        "S3BackupMode": S3BackupModeType,
        "S3BackupUpdate": S3DestinationUpdateTypeDef,
        "DataFormatConversionConfiguration": DataFormatConversionConfigurationTypeDef,
        "DynamicPartitioningConfiguration": DynamicPartitioningConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateDeliveryStreamInputRequestTypeDef = TypedDict(
    "_RequiredCreateDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
    },
)
_OptionalCreateDeliveryStreamInputRequestTypeDef = TypedDict(
    "_OptionalCreateDeliveryStreamInputRequestTypeDef",
    {
        "DeliveryStreamType": DeliveryStreamTypeType,
        "KinesisStreamSourceConfiguration": KinesisStreamSourceConfigurationTypeDef,
        "DeliveryStreamEncryptionConfigurationInput": DeliveryStreamEncryptionConfigurationInputTypeDef,
        "S3DestinationConfiguration": S3DestinationConfigurationTypeDef,
        "ExtendedS3DestinationConfiguration": ExtendedS3DestinationConfigurationTypeDef,
        "RedshiftDestinationConfiguration": RedshiftDestinationConfigurationTypeDef,
        "ElasticsearchDestinationConfiguration": ElasticsearchDestinationConfigurationTypeDef,
        "AmazonopensearchserviceDestinationConfiguration": AmazonopensearchserviceDestinationConfigurationTypeDef,
        "SplunkDestinationConfiguration": SplunkDestinationConfigurationTypeDef,
        "HttpEndpointDestinationConfiguration": HttpEndpointDestinationConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDeliveryStreamInputRequestTypeDef(
    _RequiredCreateDeliveryStreamInputRequestTypeDef,
    _OptionalCreateDeliveryStreamInputRequestTypeDef,
):
    pass


_RequiredDestinationDescriptionTypeDef = TypedDict(
    "_RequiredDestinationDescriptionTypeDef",
    {
        "DestinationId": str,
    },
)
_OptionalDestinationDescriptionTypeDef = TypedDict(
    "_OptionalDestinationDescriptionTypeDef",
    {
        "S3DestinationDescription": S3DestinationDescriptionTypeDef,
        "ExtendedS3DestinationDescription": ExtendedS3DestinationDescriptionTypeDef,
        "RedshiftDestinationDescription": RedshiftDestinationDescriptionTypeDef,
        "ElasticsearchDestinationDescription": ElasticsearchDestinationDescriptionTypeDef,
        "AmazonopensearchserviceDestinationDescription": AmazonopensearchserviceDestinationDescriptionTypeDef,
        "SplunkDestinationDescription": SplunkDestinationDescriptionTypeDef,
        "HttpEndpointDestinationDescription": HttpEndpointDestinationDescriptionTypeDef,
    },
    total=False,
)


class DestinationDescriptionTypeDef(
    _RequiredDestinationDescriptionTypeDef, _OptionalDestinationDescriptionTypeDef
):
    pass


_RequiredUpdateDestinationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateDestinationInputRequestTypeDef",
    {
        "DeliveryStreamName": str,
        "CurrentDeliveryStreamVersionId": str,
        "DestinationId": str,
    },
)
_OptionalUpdateDestinationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateDestinationInputRequestTypeDef",
    {
        "S3DestinationUpdate": S3DestinationUpdateTypeDef,
        "ExtendedS3DestinationUpdate": ExtendedS3DestinationUpdateTypeDef,
        "RedshiftDestinationUpdate": RedshiftDestinationUpdateTypeDef,
        "ElasticsearchDestinationUpdate": ElasticsearchDestinationUpdateTypeDef,
        "AmazonopensearchserviceDestinationUpdate": AmazonopensearchserviceDestinationUpdateTypeDef,
        "SplunkDestinationUpdate": SplunkDestinationUpdateTypeDef,
        "HttpEndpointDestinationUpdate": HttpEndpointDestinationUpdateTypeDef,
    },
    total=False,
)


class UpdateDestinationInputRequestTypeDef(
    _RequiredUpdateDestinationInputRequestTypeDef, _OptionalUpdateDestinationInputRequestTypeDef
):
    pass


_RequiredDeliveryStreamDescriptionTypeDef = TypedDict(
    "_RequiredDeliveryStreamDescriptionTypeDef",
    {
        "DeliveryStreamName": str,
        "DeliveryStreamARN": str,
        "DeliveryStreamStatus": DeliveryStreamStatusType,
        "DeliveryStreamType": DeliveryStreamTypeType,
        "VersionId": str,
        "Destinations": List[DestinationDescriptionTypeDef],
        "HasMoreDestinations": bool,
    },
)
_OptionalDeliveryStreamDescriptionTypeDef = TypedDict(
    "_OptionalDeliveryStreamDescriptionTypeDef",
    {
        "FailureDescription": FailureDescriptionTypeDef,
        "DeliveryStreamEncryptionConfiguration": DeliveryStreamEncryptionConfigurationTypeDef,
        "CreateTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "Source": SourceDescriptionTypeDef,
    },
    total=False,
)


class DeliveryStreamDescriptionTypeDef(
    _RequiredDeliveryStreamDescriptionTypeDef, _OptionalDeliveryStreamDescriptionTypeDef
):
    pass


DescribeDeliveryStreamOutputTypeDef = TypedDict(
    "DescribeDeliveryStreamOutputTypeDef",
    {
        "DeliveryStreamDescription": DeliveryStreamDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
