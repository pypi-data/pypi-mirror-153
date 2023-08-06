"""
Type annotations for iotanalytics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotanalytics/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotanalytics.type_defs import AddAttributesActivityTypeDef

    data: AddAttributesActivityTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ChannelStatusType,
    ComputeTypeType,
    DatasetActionTypeType,
    DatasetContentStateType,
    DatasetStatusType,
    DatastoreStatusType,
    FileFormatTypeType,
    ReprocessingStatusType,
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
    "AddAttributesActivityTypeDef",
    "BatchPutMessageErrorEntryTypeDef",
    "MessageTypeDef",
    "ResponseMetadataTypeDef",
    "CancelPipelineReprocessingRequestRequestTypeDef",
    "ChannelActivityTypeDef",
    "ChannelMessagesTypeDef",
    "EstimatedResourceSizeTypeDef",
    "CustomerManagedChannelS3StorageSummaryTypeDef",
    "CustomerManagedChannelS3StorageTypeDef",
    "RetentionPeriodTypeDef",
    "ColumnTypeDef",
    "ResourceConfigurationTypeDef",
    "TagTypeDef",
    "CreateDatasetContentRequestRequestTypeDef",
    "VersioningConfigurationTypeDef",
    "CustomerManagedDatastoreS3StorageSummaryTypeDef",
    "CustomerManagedDatastoreS3StorageTypeDef",
    "DatasetActionSummaryTypeDef",
    "IotEventsDestinationConfigurationTypeDef",
    "DatasetContentStatusTypeDef",
    "DatasetContentVersionValueTypeDef",
    "DatasetEntryTypeDef",
    "ScheduleTypeDef",
    "TriggeringDatasetTypeDef",
    "DatastoreActivityTypeDef",
    "IotSiteWiseCustomerManagedDatastoreS3StorageSummaryTypeDef",
    "IotSiteWiseCustomerManagedDatastoreS3StorageTypeDef",
    "PartitionTypeDef",
    "TimestampPartitionTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteDatasetContentRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteDatastoreRequestRequestTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "DeltaTimeSessionWindowConfigurationTypeDef",
    "DeltaTimeTypeDef",
    "DescribeChannelRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatastoreRequestRequestTypeDef",
    "LoggingOptionsTypeDef",
    "DescribePipelineRequestRequestTypeDef",
    "DeviceRegistryEnrichActivityTypeDef",
    "DeviceShadowEnrichActivityTypeDef",
    "FilterActivityTypeDef",
    "GetDatasetContentRequestRequestTypeDef",
    "GlueConfigurationTypeDef",
    "LambdaActivityTypeDef",
    "PaginatorConfigTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListDatasetContentsRequestRequestTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatastoresRequestRequestTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MathActivityTypeDef",
    "OutputFileUriValueTypeDef",
    "RemoveAttributesActivityTypeDef",
    "SelectAttributesActivityTypeDef",
    "ReprocessingSummaryTypeDef",
    "SampleChannelDataRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "BatchPutMessageRequestRequestTypeDef",
    "BatchPutMessageResponseTypeDef",
    "CreateDatasetContentResponseTypeDef",
    "CreatePipelineResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "RunPipelineActivityResponseTypeDef",
    "SampleChannelDataResponseTypeDef",
    "StartPipelineReprocessingResponseTypeDef",
    "StartPipelineReprocessingRequestRequestTypeDef",
    "ChannelStatisticsTypeDef",
    "DatastoreStatisticsTypeDef",
    "ChannelStorageSummaryTypeDef",
    "ChannelStorageTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateDatastoreResponseTypeDef",
    "SchemaDefinitionTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DatasetContentSummaryTypeDef",
    "GetDatasetContentResponseTypeDef",
    "DatasetTriggerTypeDef",
    "DatastoreIotSiteWiseMultiLayerStorageSummaryTypeDef",
    "DatastoreIotSiteWiseMultiLayerStorageTypeDef",
    "DatastorePartitionTypeDef",
    "LateDataRuleConfigurationTypeDef",
    "QueryFilterTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "S3DestinationConfigurationTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListDatasetContentsRequestListDatasetContentsPaginateTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatastoresRequestListDatastoresPaginateTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "VariableTypeDef",
    "PipelineActivityTypeDef",
    "PipelineSummaryTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "ParquetConfigurationTypeDef",
    "ListDatasetContentsResponseTypeDef",
    "DatasetSummaryTypeDef",
    "DatastoreStorageSummaryTypeDef",
    "DatastoreStorageTypeDef",
    "DatastorePartitionsTypeDef",
    "LateDataRuleTypeDef",
    "SqlQueryDatasetActionTypeDef",
    "DatasetContentDeliveryDestinationTypeDef",
    "ContainerDatasetActionTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "PipelineTypeDef",
    "RunPipelineActivityRequestRequestTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "DescribeChannelResponseTypeDef",
    "FileFormatConfigurationTypeDef",
    "ListDatasetsResponseTypeDef",
    "DatastoreSummaryTypeDef",
    "DatasetContentDeliveryRuleTypeDef",
    "DatasetActionTypeDef",
    "DescribePipelineResponseTypeDef",
    "CreateDatastoreRequestRequestTypeDef",
    "DatastoreTypeDef",
    "UpdateDatastoreRequestRequestTypeDef",
    "ListDatastoresResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "DatasetTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "DescribeDatastoreResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
)

_RequiredAddAttributesActivityTypeDef = TypedDict(
    "_RequiredAddAttributesActivityTypeDef",
    {
        "name": str,
        "attributes": Mapping[str, str],
    },
)
_OptionalAddAttributesActivityTypeDef = TypedDict(
    "_OptionalAddAttributesActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class AddAttributesActivityTypeDef(
    _RequiredAddAttributesActivityTypeDef, _OptionalAddAttributesActivityTypeDef
):
    pass


BatchPutMessageErrorEntryTypeDef = TypedDict(
    "BatchPutMessageErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "messageId": str,
        "payload": Union[str, bytes, IO[Any], StreamingBody],
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

CancelPipelineReprocessingRequestRequestTypeDef = TypedDict(
    "CancelPipelineReprocessingRequestRequestTypeDef",
    {
        "pipelineName": str,
        "reprocessingId": str,
    },
)

_RequiredChannelActivityTypeDef = TypedDict(
    "_RequiredChannelActivityTypeDef",
    {
        "name": str,
        "channelName": str,
    },
)
_OptionalChannelActivityTypeDef = TypedDict(
    "_OptionalChannelActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class ChannelActivityTypeDef(_RequiredChannelActivityTypeDef, _OptionalChannelActivityTypeDef):
    pass


ChannelMessagesTypeDef = TypedDict(
    "ChannelMessagesTypeDef",
    {
        "s3Paths": Sequence[str],
    },
    total=False,
)

EstimatedResourceSizeTypeDef = TypedDict(
    "EstimatedResourceSizeTypeDef",
    {
        "estimatedSizeInBytes": float,
        "estimatedOn": datetime,
    },
    total=False,
)

CustomerManagedChannelS3StorageSummaryTypeDef = TypedDict(
    "CustomerManagedChannelS3StorageSummaryTypeDef",
    {
        "bucket": str,
        "keyPrefix": str,
        "roleArn": str,
    },
    total=False,
)

_RequiredCustomerManagedChannelS3StorageTypeDef = TypedDict(
    "_RequiredCustomerManagedChannelS3StorageTypeDef",
    {
        "bucket": str,
        "roleArn": str,
    },
)
_OptionalCustomerManagedChannelS3StorageTypeDef = TypedDict(
    "_OptionalCustomerManagedChannelS3StorageTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class CustomerManagedChannelS3StorageTypeDef(
    _RequiredCustomerManagedChannelS3StorageTypeDef, _OptionalCustomerManagedChannelS3StorageTypeDef
):
    pass


RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "unlimited": bool,
        "numberOfDays": int,
    },
    total=False,
)

ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "name": str,
        "type": str,
    },
)

ResourceConfigurationTypeDef = TypedDict(
    "ResourceConfigurationTypeDef",
    {
        "computeType": ComputeTypeType,
        "volumeSizeInGB": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredCreateDatasetContentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetContentRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)
_OptionalCreateDatasetContentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetContentRequestRequestTypeDef",
    {
        "versionId": str,
    },
    total=False,
)


class CreateDatasetContentRequestRequestTypeDef(
    _RequiredCreateDatasetContentRequestRequestTypeDef,
    _OptionalCreateDatasetContentRequestRequestTypeDef,
):
    pass


VersioningConfigurationTypeDef = TypedDict(
    "VersioningConfigurationTypeDef",
    {
        "unlimited": bool,
        "maxVersions": int,
    },
    total=False,
)

CustomerManagedDatastoreS3StorageSummaryTypeDef = TypedDict(
    "CustomerManagedDatastoreS3StorageSummaryTypeDef",
    {
        "bucket": str,
        "keyPrefix": str,
        "roleArn": str,
    },
    total=False,
)

_RequiredCustomerManagedDatastoreS3StorageTypeDef = TypedDict(
    "_RequiredCustomerManagedDatastoreS3StorageTypeDef",
    {
        "bucket": str,
        "roleArn": str,
    },
)
_OptionalCustomerManagedDatastoreS3StorageTypeDef = TypedDict(
    "_OptionalCustomerManagedDatastoreS3StorageTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class CustomerManagedDatastoreS3StorageTypeDef(
    _RequiredCustomerManagedDatastoreS3StorageTypeDef,
    _OptionalCustomerManagedDatastoreS3StorageTypeDef,
):
    pass


DatasetActionSummaryTypeDef = TypedDict(
    "DatasetActionSummaryTypeDef",
    {
        "actionName": str,
        "actionType": DatasetActionTypeType,
    },
    total=False,
)

IotEventsDestinationConfigurationTypeDef = TypedDict(
    "IotEventsDestinationConfigurationTypeDef",
    {
        "inputName": str,
        "roleArn": str,
    },
)

DatasetContentStatusTypeDef = TypedDict(
    "DatasetContentStatusTypeDef",
    {
        "state": DatasetContentStateType,
        "reason": str,
    },
    total=False,
)

DatasetContentVersionValueTypeDef = TypedDict(
    "DatasetContentVersionValueTypeDef",
    {
        "datasetName": str,
    },
)

DatasetEntryTypeDef = TypedDict(
    "DatasetEntryTypeDef",
    {
        "entryName": str,
        "dataURI": str,
    },
    total=False,
)

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "expression": str,
    },
    total=False,
)

TriggeringDatasetTypeDef = TypedDict(
    "TriggeringDatasetTypeDef",
    {
        "name": str,
    },
)

DatastoreActivityTypeDef = TypedDict(
    "DatastoreActivityTypeDef",
    {
        "name": str,
        "datastoreName": str,
    },
)

IotSiteWiseCustomerManagedDatastoreS3StorageSummaryTypeDef = TypedDict(
    "IotSiteWiseCustomerManagedDatastoreS3StorageSummaryTypeDef",
    {
        "bucket": str,
        "keyPrefix": str,
    },
    total=False,
)

_RequiredIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef = TypedDict(
    "_RequiredIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef",
    {
        "bucket": str,
    },
)
_OptionalIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef = TypedDict(
    "_OptionalIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class IotSiteWiseCustomerManagedDatastoreS3StorageTypeDef(
    _RequiredIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef,
    _OptionalIotSiteWiseCustomerManagedDatastoreS3StorageTypeDef,
):
    pass


PartitionTypeDef = TypedDict(
    "PartitionTypeDef",
    {
        "attributeName": str,
    },
)

_RequiredTimestampPartitionTypeDef = TypedDict(
    "_RequiredTimestampPartitionTypeDef",
    {
        "attributeName": str,
    },
)
_OptionalTimestampPartitionTypeDef = TypedDict(
    "_OptionalTimestampPartitionTypeDef",
    {
        "timestampFormat": str,
    },
    total=False,
)


class TimestampPartitionTypeDef(
    _RequiredTimestampPartitionTypeDef, _OptionalTimestampPartitionTypeDef
):
    pass


DeleteChannelRequestRequestTypeDef = TypedDict(
    "DeleteChannelRequestRequestTypeDef",
    {
        "channelName": str,
    },
)

_RequiredDeleteDatasetContentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDatasetContentRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)
_OptionalDeleteDatasetContentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDatasetContentRequestRequestTypeDef",
    {
        "versionId": str,
    },
    total=False,
)


class DeleteDatasetContentRequestRequestTypeDef(
    _RequiredDeleteDatasetContentRequestRequestTypeDef,
    _OptionalDeleteDatasetContentRequestRequestTypeDef,
):
    pass


DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)

DeleteDatastoreRequestRequestTypeDef = TypedDict(
    "DeleteDatastoreRequestRequestTypeDef",
    {
        "datastoreName": str,
    },
)

DeletePipelineRequestRequestTypeDef = TypedDict(
    "DeletePipelineRequestRequestTypeDef",
    {
        "pipelineName": str,
    },
)

DeltaTimeSessionWindowConfigurationTypeDef = TypedDict(
    "DeltaTimeSessionWindowConfigurationTypeDef",
    {
        "timeoutInMinutes": int,
    },
)

DeltaTimeTypeDef = TypedDict(
    "DeltaTimeTypeDef",
    {
        "offsetSeconds": int,
        "timeExpression": str,
    },
)

_RequiredDescribeChannelRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeChannelRequestRequestTypeDef",
    {
        "channelName": str,
    },
)
_OptionalDescribeChannelRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeChannelRequestRequestTypeDef",
    {
        "includeStatistics": bool,
    },
    total=False,
)


class DescribeChannelRequestRequestTypeDef(
    _RequiredDescribeChannelRequestRequestTypeDef, _OptionalDescribeChannelRequestRequestTypeDef
):
    pass


DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)

_RequiredDescribeDatastoreRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDatastoreRequestRequestTypeDef",
    {
        "datastoreName": str,
    },
)
_OptionalDescribeDatastoreRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDatastoreRequestRequestTypeDef",
    {
        "includeStatistics": bool,
    },
    total=False,
)


class DescribeDatastoreRequestRequestTypeDef(
    _RequiredDescribeDatastoreRequestRequestTypeDef, _OptionalDescribeDatastoreRequestRequestTypeDef
):
    pass


LoggingOptionsTypeDef = TypedDict(
    "LoggingOptionsTypeDef",
    {
        "roleArn": str,
        "level": Literal["ERROR"],
        "enabled": bool,
    },
)

DescribePipelineRequestRequestTypeDef = TypedDict(
    "DescribePipelineRequestRequestTypeDef",
    {
        "pipelineName": str,
    },
)

_RequiredDeviceRegistryEnrichActivityTypeDef = TypedDict(
    "_RequiredDeviceRegistryEnrichActivityTypeDef",
    {
        "name": str,
        "attribute": str,
        "thingName": str,
        "roleArn": str,
    },
)
_OptionalDeviceRegistryEnrichActivityTypeDef = TypedDict(
    "_OptionalDeviceRegistryEnrichActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class DeviceRegistryEnrichActivityTypeDef(
    _RequiredDeviceRegistryEnrichActivityTypeDef, _OptionalDeviceRegistryEnrichActivityTypeDef
):
    pass


_RequiredDeviceShadowEnrichActivityTypeDef = TypedDict(
    "_RequiredDeviceShadowEnrichActivityTypeDef",
    {
        "name": str,
        "attribute": str,
        "thingName": str,
        "roleArn": str,
    },
)
_OptionalDeviceShadowEnrichActivityTypeDef = TypedDict(
    "_OptionalDeviceShadowEnrichActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class DeviceShadowEnrichActivityTypeDef(
    _RequiredDeviceShadowEnrichActivityTypeDef, _OptionalDeviceShadowEnrichActivityTypeDef
):
    pass


_RequiredFilterActivityTypeDef = TypedDict(
    "_RequiredFilterActivityTypeDef",
    {
        "name": str,
        "filter": str,
    },
)
_OptionalFilterActivityTypeDef = TypedDict(
    "_OptionalFilterActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class FilterActivityTypeDef(_RequiredFilterActivityTypeDef, _OptionalFilterActivityTypeDef):
    pass


_RequiredGetDatasetContentRequestRequestTypeDef = TypedDict(
    "_RequiredGetDatasetContentRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)
_OptionalGetDatasetContentRequestRequestTypeDef = TypedDict(
    "_OptionalGetDatasetContentRequestRequestTypeDef",
    {
        "versionId": str,
    },
    total=False,
)


class GetDatasetContentRequestRequestTypeDef(
    _RequiredGetDatasetContentRequestRequestTypeDef, _OptionalGetDatasetContentRequestRequestTypeDef
):
    pass


GlueConfigurationTypeDef = TypedDict(
    "GlueConfigurationTypeDef",
    {
        "tableName": str,
        "databaseName": str,
    },
)

_RequiredLambdaActivityTypeDef = TypedDict(
    "_RequiredLambdaActivityTypeDef",
    {
        "name": str,
        "lambdaName": str,
        "batchSize": int,
    },
)
_OptionalLambdaActivityTypeDef = TypedDict(
    "_OptionalLambdaActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class LambdaActivityTypeDef(_RequiredLambdaActivityTypeDef, _OptionalLambdaActivityTypeDef):
    pass


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
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListDatasetContentsRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetContentsRequestRequestTypeDef",
    {
        "datasetName": str,
    },
)
_OptionalListDatasetContentsRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetContentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "scheduledOnOrAfter": Union[datetime, str],
        "scheduledBefore": Union[datetime, str],
    },
    total=False,
)


class ListDatasetContentsRequestRequestTypeDef(
    _RequiredListDatasetContentsRequestRequestTypeDef,
    _OptionalListDatasetContentsRequestRequestTypeDef,
):
    pass


ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListDatastoresRequestRequestTypeDef = TypedDict(
    "ListDatastoresRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListPipelinesRequestRequestTypeDef = TypedDict(
    "ListPipelinesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredMathActivityTypeDef = TypedDict(
    "_RequiredMathActivityTypeDef",
    {
        "name": str,
        "attribute": str,
        "math": str,
    },
)
_OptionalMathActivityTypeDef = TypedDict(
    "_OptionalMathActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class MathActivityTypeDef(_RequiredMathActivityTypeDef, _OptionalMathActivityTypeDef):
    pass


OutputFileUriValueTypeDef = TypedDict(
    "OutputFileUriValueTypeDef",
    {
        "fileName": str,
    },
)

_RequiredRemoveAttributesActivityTypeDef = TypedDict(
    "_RequiredRemoveAttributesActivityTypeDef",
    {
        "name": str,
        "attributes": Sequence[str],
    },
)
_OptionalRemoveAttributesActivityTypeDef = TypedDict(
    "_OptionalRemoveAttributesActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class RemoveAttributesActivityTypeDef(
    _RequiredRemoveAttributesActivityTypeDef, _OptionalRemoveAttributesActivityTypeDef
):
    pass


_RequiredSelectAttributesActivityTypeDef = TypedDict(
    "_RequiredSelectAttributesActivityTypeDef",
    {
        "name": str,
        "attributes": Sequence[str],
    },
)
_OptionalSelectAttributesActivityTypeDef = TypedDict(
    "_OptionalSelectAttributesActivityTypeDef",
    {
        "next": str,
    },
    total=False,
)


class SelectAttributesActivityTypeDef(
    _RequiredSelectAttributesActivityTypeDef, _OptionalSelectAttributesActivityTypeDef
):
    pass


ReprocessingSummaryTypeDef = TypedDict(
    "ReprocessingSummaryTypeDef",
    {
        "id": str,
        "status": ReprocessingStatusType,
        "creationTime": datetime,
    },
    total=False,
)

_RequiredSampleChannelDataRequestRequestTypeDef = TypedDict(
    "_RequiredSampleChannelDataRequestRequestTypeDef",
    {
        "channelName": str,
    },
)
_OptionalSampleChannelDataRequestRequestTypeDef = TypedDict(
    "_OptionalSampleChannelDataRequestRequestTypeDef",
    {
        "maxMessages": int,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
    total=False,
)


class SampleChannelDataRequestRequestTypeDef(
    _RequiredSampleChannelDataRequestRequestTypeDef, _OptionalSampleChannelDataRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

BatchPutMessageRequestRequestTypeDef = TypedDict(
    "BatchPutMessageRequestRequestTypeDef",
    {
        "channelName": str,
        "messages": Sequence[MessageTypeDef],
    },
)

BatchPutMessageResponseTypeDef = TypedDict(
    "BatchPutMessageResponseTypeDef",
    {
        "batchPutMessageErrorEntries": List[BatchPutMessageErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatasetContentResponseTypeDef = TypedDict(
    "CreateDatasetContentResponseTypeDef",
    {
        "versionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {
        "pipelineName": str,
        "pipelineArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunPipelineActivityResponseTypeDef = TypedDict(
    "RunPipelineActivityResponseTypeDef",
    {
        "payloads": List[bytes],
        "logResult": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SampleChannelDataResponseTypeDef = TypedDict(
    "SampleChannelDataResponseTypeDef",
    {
        "payloads": List[bytes],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartPipelineReprocessingResponseTypeDef = TypedDict(
    "StartPipelineReprocessingResponseTypeDef",
    {
        "reprocessingId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartPipelineReprocessingRequestRequestTypeDef = TypedDict(
    "_RequiredStartPipelineReprocessingRequestRequestTypeDef",
    {
        "pipelineName": str,
    },
)
_OptionalStartPipelineReprocessingRequestRequestTypeDef = TypedDict(
    "_OptionalStartPipelineReprocessingRequestRequestTypeDef",
    {
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
        "channelMessages": ChannelMessagesTypeDef,
    },
    total=False,
)


class StartPipelineReprocessingRequestRequestTypeDef(
    _RequiredStartPipelineReprocessingRequestRequestTypeDef,
    _OptionalStartPipelineReprocessingRequestRequestTypeDef,
):
    pass


ChannelStatisticsTypeDef = TypedDict(
    "ChannelStatisticsTypeDef",
    {
        "size": EstimatedResourceSizeTypeDef,
    },
    total=False,
)

DatastoreStatisticsTypeDef = TypedDict(
    "DatastoreStatisticsTypeDef",
    {
        "size": EstimatedResourceSizeTypeDef,
    },
    total=False,
)

ChannelStorageSummaryTypeDef = TypedDict(
    "ChannelStorageSummaryTypeDef",
    {
        "serviceManagedS3": Dict[str, Any],
        "customerManagedS3": CustomerManagedChannelS3StorageSummaryTypeDef,
    },
    total=False,
)

ChannelStorageTypeDef = TypedDict(
    "ChannelStorageTypeDef",
    {
        "serviceManagedS3": Mapping[str, Any],
        "customerManagedS3": CustomerManagedChannelS3StorageTypeDef,
    },
    total=False,
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "channelName": str,
        "channelArn": str,
        "retentionPeriod": RetentionPeriodTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "datasetName": str,
        "datasetArn": str,
        "retentionPeriod": RetentionPeriodTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatastoreResponseTypeDef = TypedDict(
    "CreateDatastoreResponseTypeDef",
    {
        "datastoreName": str,
        "datastoreArn": str,
        "retentionPeriod": RetentionPeriodTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SchemaDefinitionTypeDef = TypedDict(
    "SchemaDefinitionTypeDef",
    {
        "columns": Sequence[ColumnTypeDef],
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

DatasetContentSummaryTypeDef = TypedDict(
    "DatasetContentSummaryTypeDef",
    {
        "version": str,
        "status": DatasetContentStatusTypeDef,
        "creationTime": datetime,
        "scheduleTime": datetime,
        "completionTime": datetime,
    },
    total=False,
)

GetDatasetContentResponseTypeDef = TypedDict(
    "GetDatasetContentResponseTypeDef",
    {
        "entries": List[DatasetEntryTypeDef],
        "timestamp": datetime,
        "status": DatasetContentStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasetTriggerTypeDef = TypedDict(
    "DatasetTriggerTypeDef",
    {
        "schedule": ScheduleTypeDef,
        "dataset": TriggeringDatasetTypeDef,
    },
    total=False,
)

DatastoreIotSiteWiseMultiLayerStorageSummaryTypeDef = TypedDict(
    "DatastoreIotSiteWiseMultiLayerStorageSummaryTypeDef",
    {
        "customerManagedS3Storage": IotSiteWiseCustomerManagedDatastoreS3StorageSummaryTypeDef,
    },
    total=False,
)

DatastoreIotSiteWiseMultiLayerStorageTypeDef = TypedDict(
    "DatastoreIotSiteWiseMultiLayerStorageTypeDef",
    {
        "customerManagedS3Storage": IotSiteWiseCustomerManagedDatastoreS3StorageTypeDef,
    },
)

DatastorePartitionTypeDef = TypedDict(
    "DatastorePartitionTypeDef",
    {
        "attributePartition": PartitionTypeDef,
        "timestampPartition": TimestampPartitionTypeDef,
    },
    total=False,
)

LateDataRuleConfigurationTypeDef = TypedDict(
    "LateDataRuleConfigurationTypeDef",
    {
        "deltaTimeSessionWindowConfiguration": DeltaTimeSessionWindowConfigurationTypeDef,
    },
    total=False,
)

QueryFilterTypeDef = TypedDict(
    "QueryFilterTypeDef",
    {
        "deltaTime": DeltaTimeTypeDef,
    },
    total=False,
)

DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLoggingOptionsRequestRequestTypeDef = TypedDict(
    "PutLoggingOptionsRequestRequestTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
    },
)

_RequiredS3DestinationConfigurationTypeDef = TypedDict(
    "_RequiredS3DestinationConfigurationTypeDef",
    {
        "bucket": str,
        "key": str,
        "roleArn": str,
    },
)
_OptionalS3DestinationConfigurationTypeDef = TypedDict(
    "_OptionalS3DestinationConfigurationTypeDef",
    {
        "glueConfiguration": GlueConfigurationTypeDef,
    },
    total=False,
)


class S3DestinationConfigurationTypeDef(
    _RequiredS3DestinationConfigurationTypeDef, _OptionalS3DestinationConfigurationTypeDef
):
    pass


ListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "ListChannelsRequestListChannelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDatasetContentsRequestListDatasetContentsPaginateTypeDef = TypedDict(
    "_RequiredListDatasetContentsRequestListDatasetContentsPaginateTypeDef",
    {
        "datasetName": str,
    },
)
_OptionalListDatasetContentsRequestListDatasetContentsPaginateTypeDef = TypedDict(
    "_OptionalListDatasetContentsRequestListDatasetContentsPaginateTypeDef",
    {
        "scheduledOnOrAfter": Union[datetime, str],
        "scheduledBefore": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDatasetContentsRequestListDatasetContentsPaginateTypeDef(
    _RequiredListDatasetContentsRequestListDatasetContentsPaginateTypeDef,
    _OptionalListDatasetContentsRequestListDatasetContentsPaginateTypeDef,
):
    pass


ListDatasetsRequestListDatasetsPaginateTypeDef = TypedDict(
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDatastoresRequestListDatastoresPaginateTypeDef = TypedDict(
    "ListDatastoresRequestListDatastoresPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPipelinesRequestListPipelinesPaginateTypeDef = TypedDict(
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredVariableTypeDef = TypedDict(
    "_RequiredVariableTypeDef",
    {
        "name": str,
    },
)
_OptionalVariableTypeDef = TypedDict(
    "_OptionalVariableTypeDef",
    {
        "stringValue": str,
        "doubleValue": float,
        "datasetContentVersionValue": DatasetContentVersionValueTypeDef,
        "outputFileUriValue": OutputFileUriValueTypeDef,
    },
    total=False,
)


class VariableTypeDef(_RequiredVariableTypeDef, _OptionalVariableTypeDef):
    pass


PipelineActivityTypeDef = TypedDict(
    "PipelineActivityTypeDef",
    {
        "channel": ChannelActivityTypeDef,
        "lambda": LambdaActivityTypeDef,
        "datastore": DatastoreActivityTypeDef,
        "addAttributes": AddAttributesActivityTypeDef,
        "removeAttributes": RemoveAttributesActivityTypeDef,
        "selectAttributes": SelectAttributesActivityTypeDef,
        "filter": FilterActivityTypeDef,
        "math": MathActivityTypeDef,
        "deviceRegistryEnrich": DeviceRegistryEnrichActivityTypeDef,
        "deviceShadowEnrich": DeviceShadowEnrichActivityTypeDef,
    },
    total=False,
)

PipelineSummaryTypeDef = TypedDict(
    "PipelineSummaryTypeDef",
    {
        "pipelineName": str,
        "reprocessingSummaries": List[ReprocessingSummaryTypeDef],
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "channelName": str,
        "channelStorage": ChannelStorageSummaryTypeDef,
        "status": ChannelStatusType,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "lastMessageArrivalTime": datetime,
    },
    total=False,
)

ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "name": str,
        "storage": ChannelStorageTypeDef,
        "arn": str,
        "status": ChannelStatusType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "lastMessageArrivalTime": datetime,
    },
    total=False,
)

_RequiredCreateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateChannelRequestRequestTypeDef",
    {
        "channelName": str,
    },
)
_OptionalCreateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateChannelRequestRequestTypeDef",
    {
        "channelStorage": ChannelStorageTypeDef,
        "retentionPeriod": RetentionPeriodTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateChannelRequestRequestTypeDef(
    _RequiredCreateChannelRequestRequestTypeDef, _OptionalCreateChannelRequestRequestTypeDef
):
    pass


_RequiredUpdateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateChannelRequestRequestTypeDef",
    {
        "channelName": str,
    },
)
_OptionalUpdateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateChannelRequestRequestTypeDef",
    {
        "channelStorage": ChannelStorageTypeDef,
        "retentionPeriod": RetentionPeriodTypeDef,
    },
    total=False,
)


class UpdateChannelRequestRequestTypeDef(
    _RequiredUpdateChannelRequestRequestTypeDef, _OptionalUpdateChannelRequestRequestTypeDef
):
    pass


ParquetConfigurationTypeDef = TypedDict(
    "ParquetConfigurationTypeDef",
    {
        "schemaDefinition": SchemaDefinitionTypeDef,
    },
    total=False,
)

ListDatasetContentsResponseTypeDef = TypedDict(
    "ListDatasetContentsResponseTypeDef",
    {
        "datasetContentSummaries": List[DatasetContentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "datasetName": str,
        "status": DatasetStatusType,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "triggers": List[DatasetTriggerTypeDef],
        "actions": List[DatasetActionSummaryTypeDef],
    },
    total=False,
)

DatastoreStorageSummaryTypeDef = TypedDict(
    "DatastoreStorageSummaryTypeDef",
    {
        "serviceManagedS3": Dict[str, Any],
        "customerManagedS3": CustomerManagedDatastoreS3StorageSummaryTypeDef,
        "iotSiteWiseMultiLayerStorage": DatastoreIotSiteWiseMultiLayerStorageSummaryTypeDef,
    },
    total=False,
)

DatastoreStorageTypeDef = TypedDict(
    "DatastoreStorageTypeDef",
    {
        "serviceManagedS3": Mapping[str, Any],
        "customerManagedS3": CustomerManagedDatastoreS3StorageTypeDef,
        "iotSiteWiseMultiLayerStorage": DatastoreIotSiteWiseMultiLayerStorageTypeDef,
    },
    total=False,
)

DatastorePartitionsTypeDef = TypedDict(
    "DatastorePartitionsTypeDef",
    {
        "partitions": Sequence[DatastorePartitionTypeDef],
    },
    total=False,
)

_RequiredLateDataRuleTypeDef = TypedDict(
    "_RequiredLateDataRuleTypeDef",
    {
        "ruleConfiguration": LateDataRuleConfigurationTypeDef,
    },
)
_OptionalLateDataRuleTypeDef = TypedDict(
    "_OptionalLateDataRuleTypeDef",
    {
        "ruleName": str,
    },
    total=False,
)


class LateDataRuleTypeDef(_RequiredLateDataRuleTypeDef, _OptionalLateDataRuleTypeDef):
    pass


_RequiredSqlQueryDatasetActionTypeDef = TypedDict(
    "_RequiredSqlQueryDatasetActionTypeDef",
    {
        "sqlQuery": str,
    },
)
_OptionalSqlQueryDatasetActionTypeDef = TypedDict(
    "_OptionalSqlQueryDatasetActionTypeDef",
    {
        "filters": Sequence[QueryFilterTypeDef],
    },
    total=False,
)


class SqlQueryDatasetActionTypeDef(
    _RequiredSqlQueryDatasetActionTypeDef, _OptionalSqlQueryDatasetActionTypeDef
):
    pass


DatasetContentDeliveryDestinationTypeDef = TypedDict(
    "DatasetContentDeliveryDestinationTypeDef",
    {
        "iotEventsDestinationConfiguration": IotEventsDestinationConfigurationTypeDef,
        "s3DestinationConfiguration": S3DestinationConfigurationTypeDef,
    },
    total=False,
)

_RequiredContainerDatasetActionTypeDef = TypedDict(
    "_RequiredContainerDatasetActionTypeDef",
    {
        "image": str,
        "executionRoleArn": str,
        "resourceConfiguration": ResourceConfigurationTypeDef,
    },
)
_OptionalContainerDatasetActionTypeDef = TypedDict(
    "_OptionalContainerDatasetActionTypeDef",
    {
        "variables": Sequence[VariableTypeDef],
    },
    total=False,
)


class ContainerDatasetActionTypeDef(
    _RequiredContainerDatasetActionTypeDef, _OptionalContainerDatasetActionTypeDef
):
    pass


_RequiredCreatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePipelineRequestRequestTypeDef",
    {
        "pipelineName": str,
        "pipelineActivities": Sequence[PipelineActivityTypeDef],
    },
)
_OptionalCreatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePipelineRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePipelineRequestRequestTypeDef(
    _RequiredCreatePipelineRequestRequestTypeDef, _OptionalCreatePipelineRequestRequestTypeDef
):
    pass


PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "name": str,
        "arn": str,
        "activities": List[PipelineActivityTypeDef],
        "reprocessingSummaries": List[ReprocessingSummaryTypeDef],
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

RunPipelineActivityRequestRequestTypeDef = TypedDict(
    "RunPipelineActivityRequestRequestTypeDef",
    {
        "pipelineActivity": PipelineActivityTypeDef,
        "payloads": Sequence[Union[str, bytes, IO[Any], StreamingBody]],
    },
)

UpdatePipelineRequestRequestTypeDef = TypedDict(
    "UpdatePipelineRequestRequestTypeDef",
    {
        "pipelineName": str,
        "pipelineActivities": Sequence[PipelineActivityTypeDef],
    },
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {
        "pipelineSummaries": List[PipelineSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {
        "channelSummaries": List[ChannelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeChannelResponseTypeDef = TypedDict(
    "DescribeChannelResponseTypeDef",
    {
        "channel": ChannelTypeDef,
        "statistics": ChannelStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FileFormatConfigurationTypeDef = TypedDict(
    "FileFormatConfigurationTypeDef",
    {
        "jsonConfiguration": Mapping[str, Any],
        "parquetConfiguration": ParquetConfigurationTypeDef,
    },
    total=False,
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "datasetSummaries": List[DatasetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatastoreSummaryTypeDef = TypedDict(
    "DatastoreSummaryTypeDef",
    {
        "datastoreName": str,
        "datastoreStorage": DatastoreStorageSummaryTypeDef,
        "status": DatastoreStatusType,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "lastMessageArrivalTime": datetime,
        "fileFormatType": FileFormatTypeType,
        "datastorePartitions": DatastorePartitionsTypeDef,
    },
    total=False,
)

_RequiredDatasetContentDeliveryRuleTypeDef = TypedDict(
    "_RequiredDatasetContentDeliveryRuleTypeDef",
    {
        "destination": DatasetContentDeliveryDestinationTypeDef,
    },
)
_OptionalDatasetContentDeliveryRuleTypeDef = TypedDict(
    "_OptionalDatasetContentDeliveryRuleTypeDef",
    {
        "entryName": str,
    },
    total=False,
)


class DatasetContentDeliveryRuleTypeDef(
    _RequiredDatasetContentDeliveryRuleTypeDef, _OptionalDatasetContentDeliveryRuleTypeDef
):
    pass


DatasetActionTypeDef = TypedDict(
    "DatasetActionTypeDef",
    {
        "actionName": str,
        "queryAction": SqlQueryDatasetActionTypeDef,
        "containerAction": ContainerDatasetActionTypeDef,
    },
    total=False,
)

DescribePipelineResponseTypeDef = TypedDict(
    "DescribePipelineResponseTypeDef",
    {
        "pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDatastoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatastoreRequestRequestTypeDef",
    {
        "datastoreName": str,
    },
)
_OptionalCreateDatastoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatastoreRequestRequestTypeDef",
    {
        "datastoreStorage": DatastoreStorageTypeDef,
        "retentionPeriod": RetentionPeriodTypeDef,
        "tags": Sequence[TagTypeDef],
        "fileFormatConfiguration": FileFormatConfigurationTypeDef,
        "datastorePartitions": DatastorePartitionsTypeDef,
    },
    total=False,
)


class CreateDatastoreRequestRequestTypeDef(
    _RequiredCreateDatastoreRequestRequestTypeDef, _OptionalCreateDatastoreRequestRequestTypeDef
):
    pass


DatastoreTypeDef = TypedDict(
    "DatastoreTypeDef",
    {
        "name": str,
        "storage": DatastoreStorageTypeDef,
        "arn": str,
        "status": DatastoreStatusType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "lastMessageArrivalTime": datetime,
        "fileFormatConfiguration": FileFormatConfigurationTypeDef,
        "datastorePartitions": DatastorePartitionsTypeDef,
    },
    total=False,
)

_RequiredUpdateDatastoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDatastoreRequestRequestTypeDef",
    {
        "datastoreName": str,
    },
)
_OptionalUpdateDatastoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDatastoreRequestRequestTypeDef",
    {
        "retentionPeriod": RetentionPeriodTypeDef,
        "datastoreStorage": DatastoreStorageTypeDef,
        "fileFormatConfiguration": FileFormatConfigurationTypeDef,
    },
    total=False,
)


class UpdateDatastoreRequestRequestTypeDef(
    _RequiredUpdateDatastoreRequestRequestTypeDef, _OptionalUpdateDatastoreRequestRequestTypeDef
):
    pass


ListDatastoresResponseTypeDef = TypedDict(
    "ListDatastoresResponseTypeDef",
    {
        "datastoreSummaries": List[DatastoreSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "datasetName": str,
        "actions": Sequence[DatasetActionTypeDef],
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "triggers": Sequence[DatasetTriggerTypeDef],
        "contentDeliveryRules": Sequence[DatasetContentDeliveryRuleTypeDef],
        "retentionPeriod": RetentionPeriodTypeDef,
        "versioningConfiguration": VersioningConfigurationTypeDef,
        "tags": Sequence[TagTypeDef],
        "lateDataRules": Sequence[LateDataRuleTypeDef],
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "name": str,
        "arn": str,
        "actions": List[DatasetActionTypeDef],
        "triggers": List[DatasetTriggerTypeDef],
        "contentDeliveryRules": List[DatasetContentDeliveryRuleTypeDef],
        "status": DatasetStatusType,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "retentionPeriod": RetentionPeriodTypeDef,
        "versioningConfiguration": VersioningConfigurationTypeDef,
        "lateDataRules": List[LateDataRuleTypeDef],
    },
    total=False,
)

_RequiredUpdateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDatasetRequestRequestTypeDef",
    {
        "datasetName": str,
        "actions": Sequence[DatasetActionTypeDef],
    },
)
_OptionalUpdateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDatasetRequestRequestTypeDef",
    {
        "triggers": Sequence[DatasetTriggerTypeDef],
        "contentDeliveryRules": Sequence[DatasetContentDeliveryRuleTypeDef],
        "retentionPeriod": RetentionPeriodTypeDef,
        "versioningConfiguration": VersioningConfigurationTypeDef,
        "lateDataRules": Sequence[LateDataRuleTypeDef],
    },
    total=False,
)


class UpdateDatasetRequestRequestTypeDef(
    _RequiredUpdateDatasetRequestRequestTypeDef, _OptionalUpdateDatasetRequestRequestTypeDef
):
    pass


DescribeDatastoreResponseTypeDef = TypedDict(
    "DescribeDatastoreResponseTypeDef",
    {
        "datastore": DatastoreTypeDef,
        "statistics": DatastoreStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "dataset": DatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
