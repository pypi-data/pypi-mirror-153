"""
Type annotations for xray service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_xray.client import XRayClient
    from mypy_boto3_xray.paginator import (
        BatchGetTracesPaginator,
        GetGroupsPaginator,
        GetSamplingRulesPaginator,
        GetSamplingStatisticSummariesPaginator,
        GetServiceGraphPaginator,
        GetTimeSeriesServiceStatisticsPaginator,
        GetTraceGraphPaginator,
        GetTraceSummariesPaginator,
    )

    session = Session()
    client: XRayClient = session.client("xray")

    batch_get_traces_paginator: BatchGetTracesPaginator = client.get_paginator("batch_get_traces")
    get_groups_paginator: GetGroupsPaginator = client.get_paginator("get_groups")
    get_sampling_rules_paginator: GetSamplingRulesPaginator = client.get_paginator("get_sampling_rules")
    get_sampling_statistic_summaries_paginator: GetSamplingStatisticSummariesPaginator = client.get_paginator("get_sampling_statistic_summaries")
    get_service_graph_paginator: GetServiceGraphPaginator = client.get_paginator("get_service_graph")
    get_time_series_service_statistics_paginator: GetTimeSeriesServiceStatisticsPaginator = client.get_paginator("get_time_series_service_statistics")
    get_trace_graph_paginator: GetTraceGraphPaginator = client.get_paginator("get_trace_graph")
    get_trace_summaries_paginator: GetTraceSummariesPaginator = client.get_paginator("get_trace_summaries")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import TimeRangeTypeType
from .type_defs import (
    BatchGetTracesResultTypeDef,
    GetGroupsResultTypeDef,
    GetSamplingRulesResultTypeDef,
    GetSamplingStatisticSummariesResultTypeDef,
    GetServiceGraphResultTypeDef,
    GetTimeSeriesServiceStatisticsResultTypeDef,
    GetTraceGraphResultTypeDef,
    GetTraceSummariesResultTypeDef,
    PaginatorConfigTypeDef,
    SamplingStrategyTypeDef,
)

__all__ = (
    "BatchGetTracesPaginator",
    "GetGroupsPaginator",
    "GetSamplingRulesPaginator",
    "GetSamplingStatisticSummariesPaginator",
    "GetServiceGraphPaginator",
    "GetTimeSeriesServiceStatisticsPaginator",
    "GetTraceGraphPaginator",
    "GetTraceSummariesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class BatchGetTracesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.BatchGetTraces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#batchgettracespaginator)
    """

    def paginate(
        self, *, TraceIds: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[BatchGetTracesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.BatchGetTraces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#batchgettracespaginator)
        """


class GetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getgroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getgroupspaginator)
        """


class GetSamplingRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetSamplingRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingrulespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSamplingRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetSamplingRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingrulespaginator)
        """


class GetSamplingStatisticSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetSamplingStatisticSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingstatisticsummariespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSamplingStatisticSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetSamplingStatisticSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getsamplingstatisticsummariespaginator)
        """


class GetServiceGraphPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetServiceGraph)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getservicegraphpaginator)
    """

    def paginate(
        self,
        *,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        GroupName: str = ...,
        GroupARN: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetServiceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetServiceGraph.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#getservicegraphpaginator)
        """


class GetTimeSeriesServiceStatisticsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTimeSeriesServiceStatistics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettimeseriesservicestatisticspaginator)
    """

    def paginate(
        self,
        *,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        GroupName: str = ...,
        GroupARN: str = ...,
        EntitySelectorExpression: str = ...,
        Period: int = ...,
        ForecastStatistics: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTimeSeriesServiceStatisticsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTimeSeriesServiceStatistics.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettimeseriesservicestatisticspaginator)
        """


class GetTraceGraphPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTraceGraph)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracegraphpaginator)
    """

    def paginate(
        self, *, TraceIds: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTraceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTraceGraph.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracegraphpaginator)
        """


class GetTraceSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTraceSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracesummariespaginator)
    """

    def paginate(
        self,
        *,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        TimeRangeType: TimeRangeTypeType = ...,
        Sampling: bool = ...,
        SamplingStrategy: SamplingStrategyTypeDef = ...,
        FilterExpression: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetTraceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay.Paginator.GetTraceSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_xray/paginators/#gettracesummariespaginator)
        """
