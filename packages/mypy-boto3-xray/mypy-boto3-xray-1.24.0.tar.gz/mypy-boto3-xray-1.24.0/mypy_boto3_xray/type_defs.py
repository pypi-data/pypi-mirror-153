"""
Type annotations for xray service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/type_defs/)

Usage::

    ```python
    from mypy_boto3_xray.type_defs import AliasTypeDef

    data: AliasTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EncryptionStatusType,
    EncryptionTypeType,
    InsightStateType,
    SamplingStrategyNameType,
    TimeRangeTypeType,
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
    "AliasTypeDef",
    "AnnotationValueTypeDef",
    "ServiceIdTypeDef",
    "AvailabilityZoneDetailTypeDef",
    "BackendConnectionErrorsTypeDef",
    "PaginatorConfigTypeDef",
    "BatchGetTracesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "InsightsConfigurationTypeDef",
    "TagTypeDef",
    "SamplingRuleTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteSamplingRuleRequestRequestTypeDef",
    "ErrorStatisticsTypeDef",
    "FaultStatisticsTypeDef",
    "HistogramEntryTypeDef",
    "EncryptionConfigTypeDef",
    "RootCauseExceptionTypeDef",
    "ForecastStatisticsTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupsRequestRequestTypeDef",
    "GetInsightEventsRequestRequestTypeDef",
    "GetInsightImpactGraphRequestRequestTypeDef",
    "GetInsightRequestRequestTypeDef",
    "GetInsightSummariesRequestRequestTypeDef",
    "GetSamplingRulesRequestRequestTypeDef",
    "GetSamplingStatisticSummariesRequestRequestTypeDef",
    "SamplingStatisticSummaryTypeDef",
    "SamplingStatisticsDocumentTypeDef",
    "SamplingTargetDocumentTypeDef",
    "UnprocessedStatisticsTypeDef",
    "GetServiceGraphRequestRequestTypeDef",
    "GetTimeSeriesServiceStatisticsRequestRequestTypeDef",
    "GetTraceGraphRequestRequestTypeDef",
    "SamplingStrategyTypeDef",
    "HttpTypeDef",
    "RequestImpactStatisticsTypeDef",
    "InsightImpactGraphEdgeTypeDef",
    "InstanceIdDetailTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutEncryptionConfigRequestRequestTypeDef",
    "PutTraceSegmentsRequestRequestTypeDef",
    "UnprocessedTraceSegmentTypeDef",
    "ResourceARNDetailTypeDef",
    "ResponseTimeRootCauseEntityTypeDef",
    "SamplingRuleUpdateTypeDef",
    "SegmentTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AnomalousServiceTypeDef",
    "TraceUserTypeDef",
    "ValueWithServiceIdsTypeDef",
    "TelemetryRecordTypeDef",
    "BatchGetTracesRequestBatchGetTracesPaginateTypeDef",
    "GetGroupsRequestGetGroupsPaginateTypeDef",
    "GetSamplingRulesRequestGetSamplingRulesPaginateTypeDef",
    "GetSamplingStatisticSummariesRequestGetSamplingStatisticSummariesPaginateTypeDef",
    "GetServiceGraphRequestGetServiceGraphPaginateTypeDef",
    "GetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef",
    "GetTraceGraphRequestGetTraceGraphPaginateTypeDef",
    "GroupSummaryTypeDef",
    "GroupTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateSamplingRuleRequestRequestTypeDef",
    "SamplingRuleRecordTypeDef",
    "EdgeStatisticsTypeDef",
    "ServiceStatisticsTypeDef",
    "GetEncryptionConfigResultTypeDef",
    "PutEncryptionConfigResultTypeDef",
    "ErrorRootCauseEntityTypeDef",
    "FaultRootCauseEntityTypeDef",
    "GetSamplingStatisticSummariesResultTypeDef",
    "GetSamplingTargetsRequestRequestTypeDef",
    "GetSamplingTargetsResultTypeDef",
    "GetTraceSummariesRequestGetTraceSummariesPaginateTypeDef",
    "GetTraceSummariesRequestRequestTypeDef",
    "InsightImpactGraphServiceTypeDef",
    "PutTraceSegmentsResultTypeDef",
    "ResponseTimeRootCauseServiceTypeDef",
    "UpdateSamplingRuleRequestRequestTypeDef",
    "TraceTypeDef",
    "InsightEventTypeDef",
    "InsightSummaryTypeDef",
    "InsightTypeDef",
    "PutTelemetryRecordsRequestRequestTypeDef",
    "GetGroupsResultTypeDef",
    "CreateGroupResultTypeDef",
    "GetGroupResultTypeDef",
    "UpdateGroupResultTypeDef",
    "CreateSamplingRuleResultTypeDef",
    "DeleteSamplingRuleResultTypeDef",
    "GetSamplingRulesResultTypeDef",
    "UpdateSamplingRuleResultTypeDef",
    "EdgeTypeDef",
    "TimeSeriesServiceStatisticsTypeDef",
    "ErrorRootCauseServiceTypeDef",
    "FaultRootCauseServiceTypeDef",
    "GetInsightImpactGraphResultTypeDef",
    "ResponseTimeRootCauseTypeDef",
    "BatchGetTracesResultTypeDef",
    "GetInsightEventsResultTypeDef",
    "GetInsightSummariesResultTypeDef",
    "GetInsightResultTypeDef",
    "ServiceTypeDef",
    "GetTimeSeriesServiceStatisticsResultTypeDef",
    "ErrorRootCauseTypeDef",
    "FaultRootCauseTypeDef",
    "GetServiceGraphResultTypeDef",
    "GetTraceGraphResultTypeDef",
    "TraceSummaryTypeDef",
    "GetTraceSummariesResultTypeDef",
)

AliasTypeDef = TypedDict(
    "AliasTypeDef",
    {
        "Name": str,
        "Names": List[str],
        "Type": str,
    },
    total=False,
)

AnnotationValueTypeDef = TypedDict(
    "AnnotationValueTypeDef",
    {
        "NumberValue": float,
        "BooleanValue": bool,
        "StringValue": str,
    },
    total=False,
)

ServiceIdTypeDef = TypedDict(
    "ServiceIdTypeDef",
    {
        "Name": str,
        "Names": List[str],
        "AccountId": str,
        "Type": str,
    },
    total=False,
)

AvailabilityZoneDetailTypeDef = TypedDict(
    "AvailabilityZoneDetailTypeDef",
    {
        "Name": str,
    },
    total=False,
)

BackendConnectionErrorsTypeDef = TypedDict(
    "BackendConnectionErrorsTypeDef",
    {
        "TimeoutCount": int,
        "ConnectionRefusedCount": int,
        "HTTPCode4XXCount": int,
        "HTTPCode5XXCount": int,
        "UnknownHostCount": int,
        "OtherCount": int,
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

_RequiredBatchGetTracesRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetTracesRequestRequestTypeDef",
    {
        "TraceIds": Sequence[str],
    },
)
_OptionalBatchGetTracesRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetTracesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class BatchGetTracesRequestRequestTypeDef(
    _RequiredBatchGetTracesRequestRequestTypeDef, _OptionalBatchGetTracesRequestRequestTypeDef
):
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

InsightsConfigurationTypeDef = TypedDict(
    "InsightsConfigurationTypeDef",
    {
        "InsightsEnabled": bool,
        "NotificationsEnabled": bool,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredSamplingRuleTypeDef = TypedDict(
    "_RequiredSamplingRuleTypeDef",
    {
        "ResourceARN": str,
        "Priority": int,
        "FixedRate": float,
        "ReservoirSize": int,
        "ServiceName": str,
        "ServiceType": str,
        "Host": str,
        "HTTPMethod": str,
        "URLPath": str,
        "Version": int,
    },
)
_OptionalSamplingRuleTypeDef = TypedDict(
    "_OptionalSamplingRuleTypeDef",
    {
        "RuleName": str,
        "RuleARN": str,
        "Attributes": Mapping[str, str],
    },
    total=False,
)


class SamplingRuleTypeDef(_RequiredSamplingRuleTypeDef, _OptionalSamplingRuleTypeDef):
    pass


DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
    },
    total=False,
)

DeleteSamplingRuleRequestRequestTypeDef = TypedDict(
    "DeleteSamplingRuleRequestRequestTypeDef",
    {
        "RuleName": str,
        "RuleARN": str,
    },
    total=False,
)

ErrorStatisticsTypeDef = TypedDict(
    "ErrorStatisticsTypeDef",
    {
        "ThrottleCount": int,
        "OtherCount": int,
        "TotalCount": int,
    },
    total=False,
)

FaultStatisticsTypeDef = TypedDict(
    "FaultStatisticsTypeDef",
    {
        "OtherCount": int,
        "TotalCount": int,
    },
    total=False,
)

HistogramEntryTypeDef = TypedDict(
    "HistogramEntryTypeDef",
    {
        "Value": float,
        "Count": int,
    },
    total=False,
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "KeyId": str,
        "Status": EncryptionStatusType,
        "Type": EncryptionTypeType,
    },
    total=False,
)

RootCauseExceptionTypeDef = TypedDict(
    "RootCauseExceptionTypeDef",
    {
        "Name": str,
        "Message": str,
    },
    total=False,
)

ForecastStatisticsTypeDef = TypedDict(
    "ForecastStatisticsTypeDef",
    {
        "FaultCountHigh": int,
        "FaultCountLow": int,
    },
    total=False,
)

GetGroupRequestRequestTypeDef = TypedDict(
    "GetGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
    },
    total=False,
)

GetGroupsRequestRequestTypeDef = TypedDict(
    "GetGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

_RequiredGetInsightEventsRequestRequestTypeDef = TypedDict(
    "_RequiredGetInsightEventsRequestRequestTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalGetInsightEventsRequestRequestTypeDef = TypedDict(
    "_OptionalGetInsightEventsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetInsightEventsRequestRequestTypeDef(
    _RequiredGetInsightEventsRequestRequestTypeDef, _OptionalGetInsightEventsRequestRequestTypeDef
):
    pass


_RequiredGetInsightImpactGraphRequestRequestTypeDef = TypedDict(
    "_RequiredGetInsightImpactGraphRequestRequestTypeDef",
    {
        "InsightId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetInsightImpactGraphRequestRequestTypeDef = TypedDict(
    "_OptionalGetInsightImpactGraphRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetInsightImpactGraphRequestRequestTypeDef(
    _RequiredGetInsightImpactGraphRequestRequestTypeDef,
    _OptionalGetInsightImpactGraphRequestRequestTypeDef,
):
    pass


GetInsightRequestRequestTypeDef = TypedDict(
    "GetInsightRequestRequestTypeDef",
    {
        "InsightId": str,
    },
)

_RequiredGetInsightSummariesRequestRequestTypeDef = TypedDict(
    "_RequiredGetInsightSummariesRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetInsightSummariesRequestRequestTypeDef = TypedDict(
    "_OptionalGetInsightSummariesRequestRequestTypeDef",
    {
        "States": Sequence[InsightStateType],
        "GroupARN": str,
        "GroupName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetInsightSummariesRequestRequestTypeDef(
    _RequiredGetInsightSummariesRequestRequestTypeDef,
    _OptionalGetInsightSummariesRequestRequestTypeDef,
):
    pass


GetSamplingRulesRequestRequestTypeDef = TypedDict(
    "GetSamplingRulesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

GetSamplingStatisticSummariesRequestRequestTypeDef = TypedDict(
    "GetSamplingStatisticSummariesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

SamplingStatisticSummaryTypeDef = TypedDict(
    "SamplingStatisticSummaryTypeDef",
    {
        "RuleName": str,
        "Timestamp": datetime,
        "RequestCount": int,
        "BorrowCount": int,
        "SampledCount": int,
    },
    total=False,
)

_RequiredSamplingStatisticsDocumentTypeDef = TypedDict(
    "_RequiredSamplingStatisticsDocumentTypeDef",
    {
        "RuleName": str,
        "ClientID": str,
        "Timestamp": Union[datetime, str],
        "RequestCount": int,
        "SampledCount": int,
    },
)
_OptionalSamplingStatisticsDocumentTypeDef = TypedDict(
    "_OptionalSamplingStatisticsDocumentTypeDef",
    {
        "BorrowCount": int,
    },
    total=False,
)


class SamplingStatisticsDocumentTypeDef(
    _RequiredSamplingStatisticsDocumentTypeDef, _OptionalSamplingStatisticsDocumentTypeDef
):
    pass


SamplingTargetDocumentTypeDef = TypedDict(
    "SamplingTargetDocumentTypeDef",
    {
        "RuleName": str,
        "FixedRate": float,
        "ReservoirQuota": int,
        "ReservoirQuotaTTL": datetime,
        "Interval": int,
    },
    total=False,
)

UnprocessedStatisticsTypeDef = TypedDict(
    "UnprocessedStatisticsTypeDef",
    {
        "RuleName": str,
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

_RequiredGetServiceGraphRequestRequestTypeDef = TypedDict(
    "_RequiredGetServiceGraphRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetServiceGraphRequestRequestTypeDef = TypedDict(
    "_OptionalGetServiceGraphRequestRequestTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "NextToken": str,
    },
    total=False,
)


class GetServiceGraphRequestRequestTypeDef(
    _RequiredGetServiceGraphRequestRequestTypeDef, _OptionalGetServiceGraphRequestRequestTypeDef
):
    pass


_RequiredGetTimeSeriesServiceStatisticsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTimeSeriesServiceStatisticsRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetTimeSeriesServiceStatisticsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTimeSeriesServiceStatisticsRequestRequestTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "EntitySelectorExpression": str,
        "Period": int,
        "ForecastStatistics": bool,
        "NextToken": str,
    },
    total=False,
)


class GetTimeSeriesServiceStatisticsRequestRequestTypeDef(
    _RequiredGetTimeSeriesServiceStatisticsRequestRequestTypeDef,
    _OptionalGetTimeSeriesServiceStatisticsRequestRequestTypeDef,
):
    pass


_RequiredGetTraceGraphRequestRequestTypeDef = TypedDict(
    "_RequiredGetTraceGraphRequestRequestTypeDef",
    {
        "TraceIds": Sequence[str],
    },
)
_OptionalGetTraceGraphRequestRequestTypeDef = TypedDict(
    "_OptionalGetTraceGraphRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetTraceGraphRequestRequestTypeDef(
    _RequiredGetTraceGraphRequestRequestTypeDef, _OptionalGetTraceGraphRequestRequestTypeDef
):
    pass


SamplingStrategyTypeDef = TypedDict(
    "SamplingStrategyTypeDef",
    {
        "Name": SamplingStrategyNameType,
        "Value": float,
    },
    total=False,
)

HttpTypeDef = TypedDict(
    "HttpTypeDef",
    {
        "HttpURL": str,
        "HttpStatus": int,
        "HttpMethod": str,
        "UserAgent": str,
        "ClientIp": str,
    },
    total=False,
)

RequestImpactStatisticsTypeDef = TypedDict(
    "RequestImpactStatisticsTypeDef",
    {
        "FaultCount": int,
        "OkCount": int,
        "TotalCount": int,
    },
    total=False,
)

InsightImpactGraphEdgeTypeDef = TypedDict(
    "InsightImpactGraphEdgeTypeDef",
    {
        "ReferenceId": int,
    },
    total=False,
)

InstanceIdDetailTypeDef = TypedDict(
    "InstanceIdDetailTypeDef",
    {
        "Id": str,
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
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


_RequiredPutEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_RequiredPutEncryptionConfigRequestRequestTypeDef",
    {
        "Type": EncryptionTypeType,
    },
)
_OptionalPutEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_OptionalPutEncryptionConfigRequestRequestTypeDef",
    {
        "KeyId": str,
    },
    total=False,
)


class PutEncryptionConfigRequestRequestTypeDef(
    _RequiredPutEncryptionConfigRequestRequestTypeDef,
    _OptionalPutEncryptionConfigRequestRequestTypeDef,
):
    pass


PutTraceSegmentsRequestRequestTypeDef = TypedDict(
    "PutTraceSegmentsRequestRequestTypeDef",
    {
        "TraceSegmentDocuments": Sequence[str],
    },
)

UnprocessedTraceSegmentTypeDef = TypedDict(
    "UnprocessedTraceSegmentTypeDef",
    {
        "Id": str,
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

ResourceARNDetailTypeDef = TypedDict(
    "ResourceARNDetailTypeDef",
    {
        "ARN": str,
    },
    total=False,
)

ResponseTimeRootCauseEntityTypeDef = TypedDict(
    "ResponseTimeRootCauseEntityTypeDef",
    {
        "Name": str,
        "Coverage": float,
        "Remote": bool,
    },
    total=False,
)

SamplingRuleUpdateTypeDef = TypedDict(
    "SamplingRuleUpdateTypeDef",
    {
        "RuleName": str,
        "RuleARN": str,
        "ResourceARN": str,
        "Priority": int,
        "FixedRate": float,
        "ReservoirSize": int,
        "Host": str,
        "ServiceName": str,
        "ServiceType": str,
        "HTTPMethod": str,
        "URLPath": str,
        "Attributes": Mapping[str, str],
    },
    total=False,
)

SegmentTypeDef = TypedDict(
    "SegmentTypeDef",
    {
        "Id": str,
        "Document": str,
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

AnomalousServiceTypeDef = TypedDict(
    "AnomalousServiceTypeDef",
    {
        "ServiceId": ServiceIdTypeDef,
    },
    total=False,
)

TraceUserTypeDef = TypedDict(
    "TraceUserTypeDef",
    {
        "UserName": str,
        "ServiceIds": List[ServiceIdTypeDef],
    },
    total=False,
)

ValueWithServiceIdsTypeDef = TypedDict(
    "ValueWithServiceIdsTypeDef",
    {
        "AnnotationValue": AnnotationValueTypeDef,
        "ServiceIds": List[ServiceIdTypeDef],
    },
    total=False,
)

_RequiredTelemetryRecordTypeDef = TypedDict(
    "_RequiredTelemetryRecordTypeDef",
    {
        "Timestamp": Union[datetime, str],
    },
)
_OptionalTelemetryRecordTypeDef = TypedDict(
    "_OptionalTelemetryRecordTypeDef",
    {
        "SegmentsReceivedCount": int,
        "SegmentsSentCount": int,
        "SegmentsSpilloverCount": int,
        "SegmentsRejectedCount": int,
        "BackendConnectionErrors": BackendConnectionErrorsTypeDef,
    },
    total=False,
)


class TelemetryRecordTypeDef(_RequiredTelemetryRecordTypeDef, _OptionalTelemetryRecordTypeDef):
    pass


_RequiredBatchGetTracesRequestBatchGetTracesPaginateTypeDef = TypedDict(
    "_RequiredBatchGetTracesRequestBatchGetTracesPaginateTypeDef",
    {
        "TraceIds": Sequence[str],
    },
)
_OptionalBatchGetTracesRequestBatchGetTracesPaginateTypeDef = TypedDict(
    "_OptionalBatchGetTracesRequestBatchGetTracesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class BatchGetTracesRequestBatchGetTracesPaginateTypeDef(
    _RequiredBatchGetTracesRequestBatchGetTracesPaginateTypeDef,
    _OptionalBatchGetTracesRequestBatchGetTracesPaginateTypeDef,
):
    pass


GetGroupsRequestGetGroupsPaginateTypeDef = TypedDict(
    "GetGroupsRequestGetGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetSamplingRulesRequestGetSamplingRulesPaginateTypeDef = TypedDict(
    "GetSamplingRulesRequestGetSamplingRulesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetSamplingStatisticSummariesRequestGetSamplingStatisticSummariesPaginateTypeDef = TypedDict(
    "GetSamplingStatisticSummariesRequestGetSamplingStatisticSummariesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetServiceGraphRequestGetServiceGraphPaginateTypeDef = TypedDict(
    "_RequiredGetServiceGraphRequestGetServiceGraphPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetServiceGraphRequestGetServiceGraphPaginateTypeDef = TypedDict(
    "_OptionalGetServiceGraphRequestGetServiceGraphPaginateTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetServiceGraphRequestGetServiceGraphPaginateTypeDef(
    _RequiredGetServiceGraphRequestGetServiceGraphPaginateTypeDef,
    _OptionalGetServiceGraphRequestGetServiceGraphPaginateTypeDef,
):
    pass


_RequiredGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef = TypedDict(
    "_RequiredGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef = TypedDict(
    "_OptionalGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "EntitySelectorExpression": str,
        "Period": int,
        "ForecastStatistics": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef(
    _RequiredGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef,
    _OptionalGetTimeSeriesServiceStatisticsRequestGetTimeSeriesServiceStatisticsPaginateTypeDef,
):
    pass


_RequiredGetTraceGraphRequestGetTraceGraphPaginateTypeDef = TypedDict(
    "_RequiredGetTraceGraphRequestGetTraceGraphPaginateTypeDef",
    {
        "TraceIds": Sequence[str],
    },
)
_OptionalGetTraceGraphRequestGetTraceGraphPaginateTypeDef = TypedDict(
    "_OptionalGetTraceGraphRequestGetTraceGraphPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetTraceGraphRequestGetTraceGraphPaginateTypeDef(
    _RequiredGetTraceGraphRequestGetTraceGraphPaginateTypeDef,
    _OptionalGetTraceGraphRequestGetTraceGraphPaginateTypeDef,
):
    pass


GroupSummaryTypeDef = TypedDict(
    "GroupSummaryTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "FilterExpression": str,
        "InsightsConfiguration": InsightsConfigurationTypeDef,
    },
    total=False,
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "FilterExpression": str,
        "InsightsConfiguration": InsightsConfigurationTypeDef,
    },
    total=False,
)

UpdateGroupRequestRequestTypeDef = TypedDict(
    "UpdateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "GroupARN": str,
        "FilterExpression": str,
        "InsightsConfiguration": InsightsConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "FilterExpression": str,
        "InsightsConfiguration": InsightsConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass


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

_RequiredCreateSamplingRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSamplingRuleRequestRequestTypeDef",
    {
        "SamplingRule": SamplingRuleTypeDef,
    },
)
_OptionalCreateSamplingRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSamplingRuleRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSamplingRuleRequestRequestTypeDef(
    _RequiredCreateSamplingRuleRequestRequestTypeDef,
    _OptionalCreateSamplingRuleRequestRequestTypeDef,
):
    pass


SamplingRuleRecordTypeDef = TypedDict(
    "SamplingRuleRecordTypeDef",
    {
        "SamplingRule": SamplingRuleTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
    },
    total=False,
)

EdgeStatisticsTypeDef = TypedDict(
    "EdgeStatisticsTypeDef",
    {
        "OkCount": int,
        "ErrorStatistics": ErrorStatisticsTypeDef,
        "FaultStatistics": FaultStatisticsTypeDef,
        "TotalCount": int,
        "TotalResponseTime": float,
    },
    total=False,
)

ServiceStatisticsTypeDef = TypedDict(
    "ServiceStatisticsTypeDef",
    {
        "OkCount": int,
        "ErrorStatistics": ErrorStatisticsTypeDef,
        "FaultStatistics": FaultStatisticsTypeDef,
        "TotalCount": int,
        "TotalResponseTime": float,
    },
    total=False,
)

GetEncryptionConfigResultTypeDef = TypedDict(
    "GetEncryptionConfigResultTypeDef",
    {
        "EncryptionConfig": EncryptionConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutEncryptionConfigResultTypeDef = TypedDict(
    "PutEncryptionConfigResultTypeDef",
    {
        "EncryptionConfig": EncryptionConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ErrorRootCauseEntityTypeDef = TypedDict(
    "ErrorRootCauseEntityTypeDef",
    {
        "Name": str,
        "Exceptions": List[RootCauseExceptionTypeDef],
        "Remote": bool,
    },
    total=False,
)

FaultRootCauseEntityTypeDef = TypedDict(
    "FaultRootCauseEntityTypeDef",
    {
        "Name": str,
        "Exceptions": List[RootCauseExceptionTypeDef],
        "Remote": bool,
    },
    total=False,
)

GetSamplingStatisticSummariesResultTypeDef = TypedDict(
    "GetSamplingStatisticSummariesResultTypeDef",
    {
        "SamplingStatisticSummaries": List[SamplingStatisticSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSamplingTargetsRequestRequestTypeDef = TypedDict(
    "GetSamplingTargetsRequestRequestTypeDef",
    {
        "SamplingStatisticsDocuments": Sequence[SamplingStatisticsDocumentTypeDef],
    },
)

GetSamplingTargetsResultTypeDef = TypedDict(
    "GetSamplingTargetsResultTypeDef",
    {
        "SamplingTargetDocuments": List[SamplingTargetDocumentTypeDef],
        "LastRuleModification": datetime,
        "UnprocessedStatistics": List[UnprocessedStatisticsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef = TypedDict(
    "_RequiredGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef = TypedDict(
    "_OptionalGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef",
    {
        "TimeRangeType": TimeRangeTypeType,
        "Sampling": bool,
        "SamplingStrategy": SamplingStrategyTypeDef,
        "FilterExpression": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetTraceSummariesRequestGetTraceSummariesPaginateTypeDef(
    _RequiredGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef,
    _OptionalGetTraceSummariesRequestGetTraceSummariesPaginateTypeDef,
):
    pass


_RequiredGetTraceSummariesRequestRequestTypeDef = TypedDict(
    "_RequiredGetTraceSummariesRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetTraceSummariesRequestRequestTypeDef = TypedDict(
    "_OptionalGetTraceSummariesRequestRequestTypeDef",
    {
        "TimeRangeType": TimeRangeTypeType,
        "Sampling": bool,
        "SamplingStrategy": SamplingStrategyTypeDef,
        "FilterExpression": str,
        "NextToken": str,
    },
    total=False,
)


class GetTraceSummariesRequestRequestTypeDef(
    _RequiredGetTraceSummariesRequestRequestTypeDef, _OptionalGetTraceSummariesRequestRequestTypeDef
):
    pass


InsightImpactGraphServiceTypeDef = TypedDict(
    "InsightImpactGraphServiceTypeDef",
    {
        "ReferenceId": int,
        "Type": str,
        "Name": str,
        "Names": List[str],
        "AccountId": str,
        "Edges": List[InsightImpactGraphEdgeTypeDef],
    },
    total=False,
)

PutTraceSegmentsResultTypeDef = TypedDict(
    "PutTraceSegmentsResultTypeDef",
    {
        "UnprocessedTraceSegments": List[UnprocessedTraceSegmentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResponseTimeRootCauseServiceTypeDef = TypedDict(
    "ResponseTimeRootCauseServiceTypeDef",
    {
        "Name": str,
        "Names": List[str],
        "Type": str,
        "AccountId": str,
        "EntityPath": List[ResponseTimeRootCauseEntityTypeDef],
        "Inferred": bool,
    },
    total=False,
)

UpdateSamplingRuleRequestRequestTypeDef = TypedDict(
    "UpdateSamplingRuleRequestRequestTypeDef",
    {
        "SamplingRuleUpdate": SamplingRuleUpdateTypeDef,
    },
)

TraceTypeDef = TypedDict(
    "TraceTypeDef",
    {
        "Id": str,
        "Duration": float,
        "LimitExceeded": bool,
        "Segments": List[SegmentTypeDef],
    },
    total=False,
)

InsightEventTypeDef = TypedDict(
    "InsightEventTypeDef",
    {
        "Summary": str,
        "EventTime": datetime,
        "ClientRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "RootCauseServiceRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "TopAnomalousServices": List[AnomalousServiceTypeDef],
    },
    total=False,
)

InsightSummaryTypeDef = TypedDict(
    "InsightSummaryTypeDef",
    {
        "InsightId": str,
        "GroupARN": str,
        "GroupName": str,
        "RootCauseServiceId": ServiceIdTypeDef,
        "Categories": List[Literal["FAULT"]],
        "State": InsightStateType,
        "StartTime": datetime,
        "EndTime": datetime,
        "Summary": str,
        "ClientRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "RootCauseServiceRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "TopAnomalousServices": List[AnomalousServiceTypeDef],
        "LastUpdateTime": datetime,
    },
    total=False,
)

InsightTypeDef = TypedDict(
    "InsightTypeDef",
    {
        "InsightId": str,
        "GroupARN": str,
        "GroupName": str,
        "RootCauseServiceId": ServiceIdTypeDef,
        "Categories": List[Literal["FAULT"]],
        "State": InsightStateType,
        "StartTime": datetime,
        "EndTime": datetime,
        "Summary": str,
        "ClientRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "RootCauseServiceRequestImpactStatistics": RequestImpactStatisticsTypeDef,
        "TopAnomalousServices": List[AnomalousServiceTypeDef],
    },
    total=False,
)

_RequiredPutTelemetryRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredPutTelemetryRecordsRequestRequestTypeDef",
    {
        "TelemetryRecords": Sequence[TelemetryRecordTypeDef],
    },
)
_OptionalPutTelemetryRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalPutTelemetryRecordsRequestRequestTypeDef",
    {
        "EC2InstanceId": str,
        "Hostname": str,
        "ResourceARN": str,
    },
    total=False,
)


class PutTelemetryRecordsRequestRequestTypeDef(
    _RequiredPutTelemetryRecordsRequestRequestTypeDef,
    _OptionalPutTelemetryRecordsRequestRequestTypeDef,
):
    pass


GetGroupsResultTypeDef = TypedDict(
    "GetGroupsResultTypeDef",
    {
        "Groups": List[GroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResultTypeDef = TypedDict(
    "CreateGroupResultTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupResultTypeDef = TypedDict(
    "GetGroupResultTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGroupResultTypeDef = TypedDict(
    "UpdateGroupResultTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSamplingRuleResultTypeDef = TypedDict(
    "CreateSamplingRuleResultTypeDef",
    {
        "SamplingRuleRecord": SamplingRuleRecordTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSamplingRuleResultTypeDef = TypedDict(
    "DeleteSamplingRuleResultTypeDef",
    {
        "SamplingRuleRecord": SamplingRuleRecordTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSamplingRulesResultTypeDef = TypedDict(
    "GetSamplingRulesResultTypeDef",
    {
        "SamplingRuleRecords": List[SamplingRuleRecordTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSamplingRuleResultTypeDef = TypedDict(
    "UpdateSamplingRuleResultTypeDef",
    {
        "SamplingRuleRecord": SamplingRuleRecordTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EdgeTypeDef = TypedDict(
    "EdgeTypeDef",
    {
        "ReferenceId": int,
        "StartTime": datetime,
        "EndTime": datetime,
        "SummaryStatistics": EdgeStatisticsTypeDef,
        "ResponseTimeHistogram": List[HistogramEntryTypeDef],
        "Aliases": List[AliasTypeDef],
    },
    total=False,
)

TimeSeriesServiceStatisticsTypeDef = TypedDict(
    "TimeSeriesServiceStatisticsTypeDef",
    {
        "Timestamp": datetime,
        "EdgeSummaryStatistics": EdgeStatisticsTypeDef,
        "ServiceSummaryStatistics": ServiceStatisticsTypeDef,
        "ServiceForecastStatistics": ForecastStatisticsTypeDef,
        "ResponseTimeHistogram": List[HistogramEntryTypeDef],
    },
    total=False,
)

ErrorRootCauseServiceTypeDef = TypedDict(
    "ErrorRootCauseServiceTypeDef",
    {
        "Name": str,
        "Names": List[str],
        "Type": str,
        "AccountId": str,
        "EntityPath": List[ErrorRootCauseEntityTypeDef],
        "Inferred": bool,
    },
    total=False,
)

FaultRootCauseServiceTypeDef = TypedDict(
    "FaultRootCauseServiceTypeDef",
    {
        "Name": str,
        "Names": List[str],
        "Type": str,
        "AccountId": str,
        "EntityPath": List[FaultRootCauseEntityTypeDef],
        "Inferred": bool,
    },
    total=False,
)

GetInsightImpactGraphResultTypeDef = TypedDict(
    "GetInsightImpactGraphResultTypeDef",
    {
        "InsightId": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "ServiceGraphStartTime": datetime,
        "ServiceGraphEndTime": datetime,
        "Services": List[InsightImpactGraphServiceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResponseTimeRootCauseTypeDef = TypedDict(
    "ResponseTimeRootCauseTypeDef",
    {
        "Services": List[ResponseTimeRootCauseServiceTypeDef],
        "ClientImpacting": bool,
    },
    total=False,
)

BatchGetTracesResultTypeDef = TypedDict(
    "BatchGetTracesResultTypeDef",
    {
        "Traces": List[TraceTypeDef],
        "UnprocessedTraceIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightEventsResultTypeDef = TypedDict(
    "GetInsightEventsResultTypeDef",
    {
        "InsightEvents": List[InsightEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightSummariesResultTypeDef = TypedDict(
    "GetInsightSummariesResultTypeDef",
    {
        "InsightSummaries": List[InsightSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightResultTypeDef = TypedDict(
    "GetInsightResultTypeDef",
    {
        "Insight": InsightTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "ReferenceId": int,
        "Name": str,
        "Names": List[str],
        "Root": bool,
        "AccountId": str,
        "Type": str,
        "State": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Edges": List[EdgeTypeDef],
        "SummaryStatistics": ServiceStatisticsTypeDef,
        "DurationHistogram": List[HistogramEntryTypeDef],
        "ResponseTimeHistogram": List[HistogramEntryTypeDef],
    },
    total=False,
)

GetTimeSeriesServiceStatisticsResultTypeDef = TypedDict(
    "GetTimeSeriesServiceStatisticsResultTypeDef",
    {
        "TimeSeriesServiceStatistics": List[TimeSeriesServiceStatisticsTypeDef],
        "ContainsOldGroupVersions": bool,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ErrorRootCauseTypeDef = TypedDict(
    "ErrorRootCauseTypeDef",
    {
        "Services": List[ErrorRootCauseServiceTypeDef],
        "ClientImpacting": bool,
    },
    total=False,
)

FaultRootCauseTypeDef = TypedDict(
    "FaultRootCauseTypeDef",
    {
        "Services": List[FaultRootCauseServiceTypeDef],
        "ClientImpacting": bool,
    },
    total=False,
)

GetServiceGraphResultTypeDef = TypedDict(
    "GetServiceGraphResultTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
        "Services": List[ServiceTypeDef],
        "ContainsOldGroupVersions": bool,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTraceGraphResultTypeDef = TypedDict(
    "GetTraceGraphResultTypeDef",
    {
        "Services": List[ServiceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TraceSummaryTypeDef = TypedDict(
    "TraceSummaryTypeDef",
    {
        "Id": str,
        "Duration": float,
        "ResponseTime": float,
        "HasFault": bool,
        "HasError": bool,
        "HasThrottle": bool,
        "IsPartial": bool,
        "Http": HttpTypeDef,
        "Annotations": Dict[str, List[ValueWithServiceIdsTypeDef]],
        "Users": List[TraceUserTypeDef],
        "ServiceIds": List[ServiceIdTypeDef],
        "ResourceARNs": List[ResourceARNDetailTypeDef],
        "InstanceIds": List[InstanceIdDetailTypeDef],
        "AvailabilityZones": List[AvailabilityZoneDetailTypeDef],
        "EntryPoint": ServiceIdTypeDef,
        "FaultRootCauses": List[FaultRootCauseTypeDef],
        "ErrorRootCauses": List[ErrorRootCauseTypeDef],
        "ResponseTimeRootCauses": List[ResponseTimeRootCauseTypeDef],
        "Revision": int,
        "MatchedEventTime": datetime,
    },
    total=False,
)

GetTraceSummariesResultTypeDef = TypedDict(
    "GetTraceSummariesResultTypeDef",
    {
        "TraceSummaries": List[TraceSummaryTypeDef],
        "ApproximateTime": datetime,
        "TracesProcessedCount": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
