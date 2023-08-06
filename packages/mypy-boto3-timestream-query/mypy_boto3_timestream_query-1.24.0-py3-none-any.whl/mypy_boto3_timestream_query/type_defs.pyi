"""
Type annotations for timestream-query service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/type_defs/)

Usage::

    ```python
    from mypy_boto3_timestream_query.type_defs import CancelQueryRequestRequestTypeDef

    data: CancelQueryRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence, Union

from .literals import (
    MeasureValueTypeType,
    S3EncryptionOptionType,
    ScalarMeasureValueTypeType,
    ScalarTypeType,
    ScheduledQueryRunStatusType,
    ScheduledQueryStateType,
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
    "CancelQueryRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ColumnInfoTypeDef",
    "ScheduleConfigurationTypeDef",
    "TagTypeDef",
    "RowTypeDef",
    "TimeSeriesDataPointTypeDef",
    "DeleteScheduledQueryRequestRequestTypeDef",
    "EndpointTypeDef",
    "DescribeScheduledQueryRequestRequestTypeDef",
    "DimensionMappingTypeDef",
    "S3ConfigurationTypeDef",
    "S3ReportLocationTypeDef",
    "ExecuteScheduledQueryRequestRequestTypeDef",
    "ExecutionStatsTypeDef",
    "PaginatorConfigTypeDef",
    "ListScheduledQueriesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MultiMeasureAttributeMappingTypeDef",
    "SnsConfigurationTypeDef",
    "ParameterMappingTypeDef",
    "PrepareQueryRequestRequestTypeDef",
    "SelectColumnTypeDef",
    "QueryRequestRequestTypeDef",
    "QueryStatusTypeDef",
    "TimestreamDestinationTypeDef",
    "TypeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateScheduledQueryRequestRequestTypeDef",
    "CancelQueryResponseTypeDef",
    "CreateScheduledQueryResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DatumTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "ErrorReportConfigurationTypeDef",
    "ErrorReportLocationTypeDef",
    "ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "QueryRequestQueryPaginateTypeDef",
    "MixedMeasureMappingTypeDef",
    "MultiMeasureMappingsTypeDef",
    "NotificationConfigurationTypeDef",
    "PrepareQueryResponseTypeDef",
    "QueryResponseTypeDef",
    "TargetDestinationTypeDef",
    "ScheduledQueryRunSummaryTypeDef",
    "TimestreamConfigurationTypeDef",
    "ScheduledQueryTypeDef",
    "TargetConfigurationTypeDef",
    "ListScheduledQueriesResponseTypeDef",
    "CreateScheduledQueryRequestRequestTypeDef",
    "ScheduledQueryDescriptionTypeDef",
    "DescribeScheduledQueryResponseTypeDef",
)

CancelQueryRequestRequestTypeDef = TypedDict(
    "CancelQueryRequestRequestTypeDef",
    {
        "QueryId": str,
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

_RequiredColumnInfoTypeDef = TypedDict(
    "_RequiredColumnInfoTypeDef",
    {
        "Type": Dict[str, Any],
    },
)
_OptionalColumnInfoTypeDef = TypedDict(
    "_OptionalColumnInfoTypeDef",
    {
        "Name": str,
    },
    total=False,
)

class ColumnInfoTypeDef(_RequiredColumnInfoTypeDef, _OptionalColumnInfoTypeDef):
    pass

ScheduleConfigurationTypeDef = TypedDict(
    "ScheduleConfigurationTypeDef",
    {
        "ScheduleExpression": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

RowTypeDef = TypedDict(
    "RowTypeDef",
    {
        "Data": List["DatumTypeDef"],
    },
)

TimeSeriesDataPointTypeDef = TypedDict(
    "TimeSeriesDataPointTypeDef",
    {
        "Time": str,
        "Value": "DatumTypeDef",
    },
)

DeleteScheduledQueryRequestRequestTypeDef = TypedDict(
    "DeleteScheduledQueryRequestRequestTypeDef",
    {
        "ScheduledQueryArn": str,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "CachePeriodInMinutes": int,
    },
)

DescribeScheduledQueryRequestRequestTypeDef = TypedDict(
    "DescribeScheduledQueryRequestRequestTypeDef",
    {
        "ScheduledQueryArn": str,
    },
)

DimensionMappingTypeDef = TypedDict(
    "DimensionMappingTypeDef",
    {
        "Name": str,
        "DimensionValueType": Literal["VARCHAR"],
    },
)

_RequiredS3ConfigurationTypeDef = TypedDict(
    "_RequiredS3ConfigurationTypeDef",
    {
        "BucketName": str,
    },
)
_OptionalS3ConfigurationTypeDef = TypedDict(
    "_OptionalS3ConfigurationTypeDef",
    {
        "ObjectKeyPrefix": str,
        "EncryptionOption": S3EncryptionOptionType,
    },
    total=False,
)

class S3ConfigurationTypeDef(_RequiredS3ConfigurationTypeDef, _OptionalS3ConfigurationTypeDef):
    pass

S3ReportLocationTypeDef = TypedDict(
    "S3ReportLocationTypeDef",
    {
        "BucketName": str,
        "ObjectKey": str,
    },
    total=False,
)

_RequiredExecuteScheduledQueryRequestRequestTypeDef = TypedDict(
    "_RequiredExecuteScheduledQueryRequestRequestTypeDef",
    {
        "ScheduledQueryArn": str,
        "InvocationTime": Union[datetime, str],
    },
)
_OptionalExecuteScheduledQueryRequestRequestTypeDef = TypedDict(
    "_OptionalExecuteScheduledQueryRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class ExecuteScheduledQueryRequestRequestTypeDef(
    _RequiredExecuteScheduledQueryRequestRequestTypeDef,
    _OptionalExecuteScheduledQueryRequestRequestTypeDef,
):
    pass

ExecutionStatsTypeDef = TypedDict(
    "ExecutionStatsTypeDef",
    {
        "ExecutionTimeInMillis": int,
        "DataWrites": int,
        "BytesMetered": int,
        "RecordsIngested": int,
        "QueryResultRows": int,
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

ListScheduledQueriesRequestRequestTypeDef = TypedDict(
    "ListScheduledQueriesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass

_RequiredMultiMeasureAttributeMappingTypeDef = TypedDict(
    "_RequiredMultiMeasureAttributeMappingTypeDef",
    {
        "SourceColumn": str,
        "MeasureValueType": ScalarMeasureValueTypeType,
    },
)
_OptionalMultiMeasureAttributeMappingTypeDef = TypedDict(
    "_OptionalMultiMeasureAttributeMappingTypeDef",
    {
        "TargetMultiMeasureAttributeName": str,
    },
    total=False,
)

class MultiMeasureAttributeMappingTypeDef(
    _RequiredMultiMeasureAttributeMappingTypeDef, _OptionalMultiMeasureAttributeMappingTypeDef
):
    pass

SnsConfigurationTypeDef = TypedDict(
    "SnsConfigurationTypeDef",
    {
        "TopicArn": str,
    },
)

ParameterMappingTypeDef = TypedDict(
    "ParameterMappingTypeDef",
    {
        "Name": str,
        "Type": "TypeTypeDef",
    },
)

_RequiredPrepareQueryRequestRequestTypeDef = TypedDict(
    "_RequiredPrepareQueryRequestRequestTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalPrepareQueryRequestRequestTypeDef = TypedDict(
    "_OptionalPrepareQueryRequestRequestTypeDef",
    {
        "ValidateOnly": bool,
    },
    total=False,
)

class PrepareQueryRequestRequestTypeDef(
    _RequiredPrepareQueryRequestRequestTypeDef, _OptionalPrepareQueryRequestRequestTypeDef
):
    pass

SelectColumnTypeDef = TypedDict(
    "SelectColumnTypeDef",
    {
        "Name": str,
        "Type": "TypeTypeDef",
        "DatabaseName": str,
        "TableName": str,
        "Aliased": bool,
    },
    total=False,
)

_RequiredQueryRequestRequestTypeDef = TypedDict(
    "_RequiredQueryRequestRequestTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalQueryRequestRequestTypeDef = TypedDict(
    "_OptionalQueryRequestRequestTypeDef",
    {
        "ClientToken": str,
        "NextToken": str,
        "MaxRows": int,
    },
    total=False,
)

class QueryRequestRequestTypeDef(
    _RequiredQueryRequestRequestTypeDef, _OptionalQueryRequestRequestTypeDef
):
    pass

QueryStatusTypeDef = TypedDict(
    "QueryStatusTypeDef",
    {
        "ProgressPercentage": float,
        "CumulativeBytesScanned": int,
        "CumulativeBytesMetered": int,
    },
    total=False,
)

TimestreamDestinationTypeDef = TypedDict(
    "TimestreamDestinationTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
    total=False,
)

TypeTypeDef = TypedDict(
    "TypeTypeDef",
    {
        "ScalarType": ScalarTypeType,
        "ArrayColumnInfo": Dict[str, Any],
        "TimeSeriesMeasureValueColumnInfo": Dict[str, Any],
        "RowColumnInfo": List[Dict[str, Any]],
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateScheduledQueryRequestRequestTypeDef = TypedDict(
    "UpdateScheduledQueryRequestRequestTypeDef",
    {
        "ScheduledQueryArn": str,
        "State": ScheduledQueryStateType,
    },
)

CancelQueryResponseTypeDef = TypedDict(
    "CancelQueryResponseTypeDef",
    {
        "CancellationMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateScheduledQueryResponseTypeDef = TypedDict(
    "CreateScheduledQueryResponseTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

DatumTypeDef = TypedDict(
    "DatumTypeDef",
    {
        "ScalarValue": str,
        "TimeSeriesValue": List[Dict[str, Any]],
        "ArrayValue": List[Dict[str, Any]],
        "RowValue": Dict[str, Any],
        "NullValue": bool,
    },
    total=False,
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ErrorReportConfigurationTypeDef = TypedDict(
    "ErrorReportConfigurationTypeDef",
    {
        "S3Configuration": S3ConfigurationTypeDef,
    },
)

ErrorReportLocationTypeDef = TypedDict(
    "ErrorReportLocationTypeDef",
    {
        "S3ReportLocation": S3ReportLocationTypeDef,
    },
    total=False,
)

ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef = TypedDict(
    "ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass

_RequiredQueryRequestQueryPaginateTypeDef = TypedDict(
    "_RequiredQueryRequestQueryPaginateTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalQueryRequestQueryPaginateTypeDef = TypedDict(
    "_OptionalQueryRequestQueryPaginateTypeDef",
    {
        "ClientToken": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class QueryRequestQueryPaginateTypeDef(
    _RequiredQueryRequestQueryPaginateTypeDef, _OptionalQueryRequestQueryPaginateTypeDef
):
    pass

_RequiredMixedMeasureMappingTypeDef = TypedDict(
    "_RequiredMixedMeasureMappingTypeDef",
    {
        "MeasureValueType": MeasureValueTypeType,
    },
)
_OptionalMixedMeasureMappingTypeDef = TypedDict(
    "_OptionalMixedMeasureMappingTypeDef",
    {
        "MeasureName": str,
        "SourceColumn": str,
        "TargetMeasureName": str,
        "MultiMeasureAttributeMappings": Sequence[MultiMeasureAttributeMappingTypeDef],
    },
    total=False,
)

class MixedMeasureMappingTypeDef(
    _RequiredMixedMeasureMappingTypeDef, _OptionalMixedMeasureMappingTypeDef
):
    pass

_RequiredMultiMeasureMappingsTypeDef = TypedDict(
    "_RequiredMultiMeasureMappingsTypeDef",
    {
        "MultiMeasureAttributeMappings": Sequence[MultiMeasureAttributeMappingTypeDef],
    },
)
_OptionalMultiMeasureMappingsTypeDef = TypedDict(
    "_OptionalMultiMeasureMappingsTypeDef",
    {
        "TargetMultiMeasureName": str,
    },
    total=False,
)

class MultiMeasureMappingsTypeDef(
    _RequiredMultiMeasureMappingsTypeDef, _OptionalMultiMeasureMappingsTypeDef
):
    pass

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "SnsConfiguration": SnsConfigurationTypeDef,
    },
)

PrepareQueryResponseTypeDef = TypedDict(
    "PrepareQueryResponseTypeDef",
    {
        "QueryString": str,
        "Columns": List[SelectColumnTypeDef],
        "Parameters": List[ParameterMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

QueryResponseTypeDef = TypedDict(
    "QueryResponseTypeDef",
    {
        "QueryId": str,
        "NextToken": str,
        "Rows": List[RowTypeDef],
        "ColumnInfo": List["ColumnInfoTypeDef"],
        "QueryStatus": QueryStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TargetDestinationTypeDef = TypedDict(
    "TargetDestinationTypeDef",
    {
        "TimestreamDestination": TimestreamDestinationTypeDef,
    },
    total=False,
)

ScheduledQueryRunSummaryTypeDef = TypedDict(
    "ScheduledQueryRunSummaryTypeDef",
    {
        "InvocationTime": datetime,
        "TriggerTime": datetime,
        "RunStatus": ScheduledQueryRunStatusType,
        "ExecutionStats": ExecutionStatsTypeDef,
        "ErrorReportLocation": ErrorReportLocationTypeDef,
        "FailureReason": str,
    },
    total=False,
)

_RequiredTimestreamConfigurationTypeDef = TypedDict(
    "_RequiredTimestreamConfigurationTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "TimeColumn": str,
        "DimensionMappings": Sequence[DimensionMappingTypeDef],
    },
)
_OptionalTimestreamConfigurationTypeDef = TypedDict(
    "_OptionalTimestreamConfigurationTypeDef",
    {
        "MultiMeasureMappings": MultiMeasureMappingsTypeDef,
        "MixedMeasureMappings": Sequence[MixedMeasureMappingTypeDef],
        "MeasureNameColumn": str,
    },
    total=False,
)

class TimestreamConfigurationTypeDef(
    _RequiredTimestreamConfigurationTypeDef, _OptionalTimestreamConfigurationTypeDef
):
    pass

_RequiredScheduledQueryTypeDef = TypedDict(
    "_RequiredScheduledQueryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "State": ScheduledQueryStateType,
    },
)
_OptionalScheduledQueryTypeDef = TypedDict(
    "_OptionalScheduledQueryTypeDef",
    {
        "CreationTime": datetime,
        "PreviousInvocationTime": datetime,
        "NextInvocationTime": datetime,
        "ErrorReportConfiguration": ErrorReportConfigurationTypeDef,
        "TargetDestination": TargetDestinationTypeDef,
        "LastRunStatus": ScheduledQueryRunStatusType,
    },
    total=False,
)

class ScheduledQueryTypeDef(_RequiredScheduledQueryTypeDef, _OptionalScheduledQueryTypeDef):
    pass

TargetConfigurationTypeDef = TypedDict(
    "TargetConfigurationTypeDef",
    {
        "TimestreamConfiguration": TimestreamConfigurationTypeDef,
    },
)

ListScheduledQueriesResponseTypeDef = TypedDict(
    "ListScheduledQueriesResponseTypeDef",
    {
        "ScheduledQueries": List[ScheduledQueryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateScheduledQueryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateScheduledQueryRequestRequestTypeDef",
    {
        "Name": str,
        "QueryString": str,
        "ScheduleConfiguration": ScheduleConfigurationTypeDef,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
        "ScheduledQueryExecutionRoleArn": str,
        "ErrorReportConfiguration": ErrorReportConfigurationTypeDef,
    },
)
_OptionalCreateScheduledQueryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateScheduledQueryRequestRequestTypeDef",
    {
        "TargetConfiguration": TargetConfigurationTypeDef,
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
    },
    total=False,
)

class CreateScheduledQueryRequestRequestTypeDef(
    _RequiredCreateScheduledQueryRequestRequestTypeDef,
    _OptionalCreateScheduledQueryRequestRequestTypeDef,
):
    pass

_RequiredScheduledQueryDescriptionTypeDef = TypedDict(
    "_RequiredScheduledQueryDescriptionTypeDef",
    {
        "Arn": str,
        "Name": str,
        "QueryString": str,
        "State": ScheduledQueryStateType,
        "ScheduleConfiguration": ScheduleConfigurationTypeDef,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
)
_OptionalScheduledQueryDescriptionTypeDef = TypedDict(
    "_OptionalScheduledQueryDescriptionTypeDef",
    {
        "CreationTime": datetime,
        "PreviousInvocationTime": datetime,
        "NextInvocationTime": datetime,
        "TargetConfiguration": TargetConfigurationTypeDef,
        "ScheduledQueryExecutionRoleArn": str,
        "KmsKeyId": str,
        "ErrorReportConfiguration": ErrorReportConfigurationTypeDef,
        "LastRunSummary": ScheduledQueryRunSummaryTypeDef,
        "RecentlyFailedRuns": List[ScheduledQueryRunSummaryTypeDef],
    },
    total=False,
)

class ScheduledQueryDescriptionTypeDef(
    _RequiredScheduledQueryDescriptionTypeDef, _OptionalScheduledQueryDescriptionTypeDef
):
    pass

DescribeScheduledQueryResponseTypeDef = TypedDict(
    "DescribeScheduledQueryResponseTypeDef",
    {
        "ScheduledQuery": ScheduledQueryDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
