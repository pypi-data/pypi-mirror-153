"""
Type annotations for cloudwatch service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudwatch.type_defs import AlarmHistoryItemTypeDef

    data: AlarmHistoryItemTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AlarmTypeType,
    AnomalyDetectorStateValueType,
    AnomalyDetectorTypeType,
    ComparisonOperatorType,
    HistoryItemTypeType,
    MetricStreamOutputFormatType,
    ScanByType,
    StandardUnitType,
    StateValueType,
    StatisticType,
    StatusCodeType,
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
    "AlarmHistoryItemTypeDef",
    "RangeTypeDef",
    "DimensionTypeDef",
    "CompositeAlarmTypeDef",
    "DashboardEntryTypeDef",
    "DashboardValidationMessageTypeDef",
    "DatapointTypeDef",
    "DeleteAlarmsInputRequestTypeDef",
    "DeleteDashboardsInputRequestTypeDef",
    "DeleteInsightRulesInputRequestTypeDef",
    "PartialFailureTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteMetricStreamInputRequestTypeDef",
    "DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAlarmHistoryInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAlarmsInputRequestTypeDef",
    "DescribeInsightRulesInputRequestTypeDef",
    "InsightRuleTypeDef",
    "DimensionFilterTypeDef",
    "DisableAlarmActionsInputRequestTypeDef",
    "DisableInsightRulesInputRequestTypeDef",
    "EnableAlarmActionsInputRequestTypeDef",
    "EnableInsightRulesInputRequestTypeDef",
    "GetDashboardInputRequestTypeDef",
    "GetInsightRuleReportInputRequestTypeDef",
    "InsightRuleMetricDatapointTypeDef",
    "LabelOptionsTypeDef",
    "MessageDataTypeDef",
    "GetMetricStreamInputRequestTypeDef",
    "MetricStreamFilterTypeDef",
    "GetMetricWidgetImageInputRequestTypeDef",
    "InsightRuleContributorDatapointTypeDef",
    "ListDashboardsInputRequestTypeDef",
    "ListMetricStreamsInputRequestTypeDef",
    "MetricStreamEntryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "TagTypeDef",
    "StatisticSetTypeDef",
    "MetricStreamStatisticsMetricTypeDef",
    "PutDashboardInputRequestTypeDef",
    "ServiceResourceAlarmRequestTypeDef",
    "ServiceResourceMetricRequestTypeDef",
    "SetAlarmStateInputAlarmSetStateTypeDef",
    "SetAlarmStateInputRequestTypeDef",
    "StartMetricStreamsInputRequestTypeDef",
    "StopMetricStreamsInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "AnomalyDetectorConfigurationTypeDef",
    "DescribeAlarmsForMetricInputRequestTypeDef",
    "DescribeAnomalyDetectorsInputRequestTypeDef",
    "GetMetricStatisticsInputMetricGetStatisticsTypeDef",
    "GetMetricStatisticsInputRequestTypeDef",
    "MetricTypeDef",
    "SingleMetricAnomalyDetectorTypeDef",
    "DeleteInsightRulesOutputTypeDef",
    "DescribeAlarmHistoryOutputTypeDef",
    "DisableInsightRulesOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableInsightRulesOutputTypeDef",
    "GetDashboardOutputTypeDef",
    "GetMetricStatisticsOutputTypeDef",
    "GetMetricWidgetImageOutputTypeDef",
    "ListDashboardsOutputTypeDef",
    "PutDashboardOutputTypeDef",
    "PutMetricStreamOutputTypeDef",
    "DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef",
    "DescribeAlarmsInputDescribeAlarmsPaginateTypeDef",
    "ListDashboardsInputListDashboardsPaginateTypeDef",
    "DescribeAlarmsInputAlarmExistsWaitTypeDef",
    "DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef",
    "DescribeInsightRulesOutputTypeDef",
    "ListMetricsInputListMetricsPaginateTypeDef",
    "ListMetricsInputRequestTypeDef",
    "MetricDataResultTypeDef",
    "InsightRuleContributorTypeDef",
    "ListMetricStreamsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PutCompositeAlarmInputRequestTypeDef",
    "PutInsightRuleInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "MetricDatumTypeDef",
    "MetricStreamStatisticsConfigurationTypeDef",
    "ListMetricsOutputTypeDef",
    "MetricStatTypeDef",
    "GetMetricDataOutputTypeDef",
    "GetInsightRuleReportOutputTypeDef",
    "PutMetricDataInputRequestTypeDef",
    "GetMetricStreamOutputTypeDef",
    "PutMetricStreamInputRequestTypeDef",
    "MetricDataQueryTypeDef",
    "GetMetricDataInputGetMetricDataPaginateTypeDef",
    "GetMetricDataInputRequestTypeDef",
    "MetricAlarmTypeDef",
    "MetricMathAnomalyDetectorTypeDef",
    "PutMetricAlarmInputMetricPutAlarmTypeDef",
    "PutMetricAlarmInputRequestTypeDef",
    "DescribeAlarmsForMetricOutputTypeDef",
    "DescribeAlarmsOutputTypeDef",
    "AnomalyDetectorTypeDef",
    "DeleteAnomalyDetectorInputRequestTypeDef",
    "PutAnomalyDetectorInputRequestTypeDef",
    "DescribeAnomalyDetectorsOutputTypeDef",
)

AlarmHistoryItemTypeDef = TypedDict(
    "AlarmHistoryItemTypeDef",
    {
        "AlarmName": str,
        "AlarmType": AlarmTypeType,
        "Timestamp": datetime,
        "HistoryItemType": HistoryItemTypeType,
        "HistorySummary": str,
        "HistoryData": str,
    },
    total=False,
)

RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
)

DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

CompositeAlarmTypeDef = TypedDict(
    "CompositeAlarmTypeDef",
    {
        "ActionsEnabled": bool,
        "AlarmActions": List[str],
        "AlarmArn": str,
        "AlarmConfigurationUpdatedTimestamp": datetime,
        "AlarmDescription": str,
        "AlarmName": str,
        "AlarmRule": str,
        "InsufficientDataActions": List[str],
        "OKActions": List[str],
        "StateReason": str,
        "StateReasonData": str,
        "StateUpdatedTimestamp": datetime,
        "StateValue": StateValueType,
    },
    total=False,
)

DashboardEntryTypeDef = TypedDict(
    "DashboardEntryTypeDef",
    {
        "DashboardName": str,
        "DashboardArn": str,
        "LastModified": datetime,
        "Size": int,
    },
    total=False,
)

DashboardValidationMessageTypeDef = TypedDict(
    "DashboardValidationMessageTypeDef",
    {
        "DataPath": str,
        "Message": str,
    },
    total=False,
)

DatapointTypeDef = TypedDict(
    "DatapointTypeDef",
    {
        "Timestamp": datetime,
        "SampleCount": float,
        "Average": float,
        "Sum": float,
        "Minimum": float,
        "Maximum": float,
        "Unit": StandardUnitType,
        "ExtendedStatistics": Dict[str, float],
    },
    total=False,
)

DeleteAlarmsInputRequestTypeDef = TypedDict(
    "DeleteAlarmsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)

DeleteDashboardsInputRequestTypeDef = TypedDict(
    "DeleteDashboardsInputRequestTypeDef",
    {
        "DashboardNames": Sequence[str],
    },
)

DeleteInsightRulesInputRequestTypeDef = TypedDict(
    "DeleteInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)

PartialFailureTypeDef = TypedDict(
    "PartialFailureTypeDef",
    {
        "FailureResource": str,
        "ExceptionType": str,
        "FailureCode": str,
        "FailureDescription": str,
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

DeleteMetricStreamInputRequestTypeDef = TypedDict(
    "DeleteMetricStreamInputRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef = TypedDict(
    "DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef",
    {
        "AlarmTypes": Sequence[AlarmTypeType],
        "HistoryItemType": HistoryItemTypeType,
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "MaxRecords": int,
        "NextToken": str,
        "ScanBy": ScanByType,
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

DescribeAlarmHistoryInputRequestTypeDef = TypedDict(
    "DescribeAlarmHistoryInputRequestTypeDef",
    {
        "AlarmName": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "HistoryItemType": HistoryItemTypeType,
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "MaxRecords": int,
        "NextToken": str,
        "ScanBy": ScanByType,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeAlarmsInputRequestTypeDef = TypedDict(
    "DescribeAlarmsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
        "AlarmNamePrefix": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "ChildrenOfAlarmName": str,
        "ParentsOfAlarmName": str,
        "StateValue": StateValueType,
        "ActionPrefix": str,
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeInsightRulesInputRequestTypeDef = TypedDict(
    "DescribeInsightRulesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

InsightRuleTypeDef = TypedDict(
    "InsightRuleTypeDef",
    {
        "Name": str,
        "State": str,
        "Schema": str,
        "Definition": str,
    },
)

_RequiredDimensionFilterTypeDef = TypedDict(
    "_RequiredDimensionFilterTypeDef",
    {
        "Name": str,
    },
)
_OptionalDimensionFilterTypeDef = TypedDict(
    "_OptionalDimensionFilterTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class DimensionFilterTypeDef(_RequiredDimensionFilterTypeDef, _OptionalDimensionFilterTypeDef):
    pass


DisableAlarmActionsInputRequestTypeDef = TypedDict(
    "DisableAlarmActionsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)

DisableInsightRulesInputRequestTypeDef = TypedDict(
    "DisableInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)

EnableAlarmActionsInputRequestTypeDef = TypedDict(
    "EnableAlarmActionsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)

EnableInsightRulesInputRequestTypeDef = TypedDict(
    "EnableInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)

GetDashboardInputRequestTypeDef = TypedDict(
    "GetDashboardInputRequestTypeDef",
    {
        "DashboardName": str,
    },
)

_RequiredGetInsightRuleReportInputRequestTypeDef = TypedDict(
    "_RequiredGetInsightRuleReportInputRequestTypeDef",
    {
        "RuleName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Period": int,
    },
)
_OptionalGetInsightRuleReportInputRequestTypeDef = TypedDict(
    "_OptionalGetInsightRuleReportInputRequestTypeDef",
    {
        "MaxContributorCount": int,
        "Metrics": Sequence[str],
        "OrderBy": str,
    },
    total=False,
)


class GetInsightRuleReportInputRequestTypeDef(
    _RequiredGetInsightRuleReportInputRequestTypeDef,
    _OptionalGetInsightRuleReportInputRequestTypeDef,
):
    pass


_RequiredInsightRuleMetricDatapointTypeDef = TypedDict(
    "_RequiredInsightRuleMetricDatapointTypeDef",
    {
        "Timestamp": datetime,
    },
)
_OptionalInsightRuleMetricDatapointTypeDef = TypedDict(
    "_OptionalInsightRuleMetricDatapointTypeDef",
    {
        "UniqueContributors": float,
        "MaxContributorValue": float,
        "SampleCount": float,
        "Average": float,
        "Sum": float,
        "Minimum": float,
        "Maximum": float,
    },
    total=False,
)


class InsightRuleMetricDatapointTypeDef(
    _RequiredInsightRuleMetricDatapointTypeDef, _OptionalInsightRuleMetricDatapointTypeDef
):
    pass


LabelOptionsTypeDef = TypedDict(
    "LabelOptionsTypeDef",
    {
        "Timezone": str,
    },
    total=False,
)

MessageDataTypeDef = TypedDict(
    "MessageDataTypeDef",
    {
        "Code": str,
        "Value": str,
    },
    total=False,
)

GetMetricStreamInputRequestTypeDef = TypedDict(
    "GetMetricStreamInputRequestTypeDef",
    {
        "Name": str,
    },
)

MetricStreamFilterTypeDef = TypedDict(
    "MetricStreamFilterTypeDef",
    {
        "Namespace": str,
    },
    total=False,
)

_RequiredGetMetricWidgetImageInputRequestTypeDef = TypedDict(
    "_RequiredGetMetricWidgetImageInputRequestTypeDef",
    {
        "MetricWidget": str,
    },
)
_OptionalGetMetricWidgetImageInputRequestTypeDef = TypedDict(
    "_OptionalGetMetricWidgetImageInputRequestTypeDef",
    {
        "OutputFormat": str,
    },
    total=False,
)


class GetMetricWidgetImageInputRequestTypeDef(
    _RequiredGetMetricWidgetImageInputRequestTypeDef,
    _OptionalGetMetricWidgetImageInputRequestTypeDef,
):
    pass


InsightRuleContributorDatapointTypeDef = TypedDict(
    "InsightRuleContributorDatapointTypeDef",
    {
        "Timestamp": datetime,
        "ApproximateValue": float,
    },
)

ListDashboardsInputRequestTypeDef = TypedDict(
    "ListDashboardsInputRequestTypeDef",
    {
        "DashboardNamePrefix": str,
        "NextToken": str,
    },
    total=False,
)

ListMetricStreamsInputRequestTypeDef = TypedDict(
    "ListMetricStreamsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MetricStreamEntryTypeDef = TypedDict(
    "MetricStreamEntryTypeDef",
    {
        "Arn": str,
        "CreationDate": datetime,
        "LastUpdateDate": datetime,
        "Name": str,
        "FirehoseArn": str,
        "State": str,
        "OutputFormat": MetricStreamOutputFormatType,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

StatisticSetTypeDef = TypedDict(
    "StatisticSetTypeDef",
    {
        "SampleCount": float,
        "Sum": float,
        "Minimum": float,
        "Maximum": float,
    },
)

MetricStreamStatisticsMetricTypeDef = TypedDict(
    "MetricStreamStatisticsMetricTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
    },
)

PutDashboardInputRequestTypeDef = TypedDict(
    "PutDashboardInputRequestTypeDef",
    {
        "DashboardName": str,
        "DashboardBody": str,
    },
)

ServiceResourceAlarmRequestTypeDef = TypedDict(
    "ServiceResourceAlarmRequestTypeDef",
    {
        "name": str,
    },
)

ServiceResourceMetricRequestTypeDef = TypedDict(
    "ServiceResourceMetricRequestTypeDef",
    {
        "namespace": str,
        "name": str,
    },
)

_RequiredSetAlarmStateInputAlarmSetStateTypeDef = TypedDict(
    "_RequiredSetAlarmStateInputAlarmSetStateTypeDef",
    {
        "StateValue": StateValueType,
        "StateReason": str,
    },
)
_OptionalSetAlarmStateInputAlarmSetStateTypeDef = TypedDict(
    "_OptionalSetAlarmStateInputAlarmSetStateTypeDef",
    {
        "StateReasonData": str,
    },
    total=False,
)


class SetAlarmStateInputAlarmSetStateTypeDef(
    _RequiredSetAlarmStateInputAlarmSetStateTypeDef, _OptionalSetAlarmStateInputAlarmSetStateTypeDef
):
    pass


_RequiredSetAlarmStateInputRequestTypeDef = TypedDict(
    "_RequiredSetAlarmStateInputRequestTypeDef",
    {
        "AlarmName": str,
        "StateValue": StateValueType,
        "StateReason": str,
    },
)
_OptionalSetAlarmStateInputRequestTypeDef = TypedDict(
    "_OptionalSetAlarmStateInputRequestTypeDef",
    {
        "StateReasonData": str,
    },
    total=False,
)


class SetAlarmStateInputRequestTypeDef(
    _RequiredSetAlarmStateInputRequestTypeDef, _OptionalSetAlarmStateInputRequestTypeDef
):
    pass


StartMetricStreamsInputRequestTypeDef = TypedDict(
    "StartMetricStreamsInputRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)

StopMetricStreamsInputRequestTypeDef = TypedDict(
    "StopMetricStreamsInputRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

AnomalyDetectorConfigurationTypeDef = TypedDict(
    "AnomalyDetectorConfigurationTypeDef",
    {
        "ExcludedTimeRanges": List[RangeTypeDef],
        "MetricTimezone": str,
    },
    total=False,
)

_RequiredDescribeAlarmsForMetricInputRequestTypeDef = TypedDict(
    "_RequiredDescribeAlarmsForMetricInputRequestTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
    },
)
_OptionalDescribeAlarmsForMetricInputRequestTypeDef = TypedDict(
    "_OptionalDescribeAlarmsForMetricInputRequestTypeDef",
    {
        "Statistic": StatisticType,
        "ExtendedStatistic": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Period": int,
        "Unit": StandardUnitType,
    },
    total=False,
)


class DescribeAlarmsForMetricInputRequestTypeDef(
    _RequiredDescribeAlarmsForMetricInputRequestTypeDef,
    _OptionalDescribeAlarmsForMetricInputRequestTypeDef,
):
    pass


DescribeAnomalyDetectorsInputRequestTypeDef = TypedDict(
    "DescribeAnomalyDetectorsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "AnomalyDetectorTypes": Sequence[AnomalyDetectorTypeType],
    },
    total=False,
)

_RequiredGetMetricStatisticsInputMetricGetStatisticsTypeDef = TypedDict(
    "_RequiredGetMetricStatisticsInputMetricGetStatisticsTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Period": int,
    },
)
_OptionalGetMetricStatisticsInputMetricGetStatisticsTypeDef = TypedDict(
    "_OptionalGetMetricStatisticsInputMetricGetStatisticsTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "Statistics": Sequence[StatisticType],
        "ExtendedStatistics": Sequence[str],
        "Unit": StandardUnitType,
    },
    total=False,
)


class GetMetricStatisticsInputMetricGetStatisticsTypeDef(
    _RequiredGetMetricStatisticsInputMetricGetStatisticsTypeDef,
    _OptionalGetMetricStatisticsInputMetricGetStatisticsTypeDef,
):
    pass


_RequiredGetMetricStatisticsInputRequestTypeDef = TypedDict(
    "_RequiredGetMetricStatisticsInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Period": int,
    },
)
_OptionalGetMetricStatisticsInputRequestTypeDef = TypedDict(
    "_OptionalGetMetricStatisticsInputRequestTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "Statistics": Sequence[StatisticType],
        "ExtendedStatistics": Sequence[str],
        "Unit": StandardUnitType,
    },
    total=False,
)


class GetMetricStatisticsInputRequestTypeDef(
    _RequiredGetMetricStatisticsInputRequestTypeDef, _OptionalGetMetricStatisticsInputRequestTypeDef
):
    pass


MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionTypeDef],
    },
    total=False,
)

SingleMetricAnomalyDetectorTypeDef = TypedDict(
    "SingleMetricAnomalyDetectorTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Stat": str,
    },
    total=False,
)

DeleteInsightRulesOutputTypeDef = TypedDict(
    "DeleteInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAlarmHistoryOutputTypeDef = TypedDict(
    "DescribeAlarmHistoryOutputTypeDef",
    {
        "AlarmHistoryItems": List[AlarmHistoryItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableInsightRulesOutputTypeDef = TypedDict(
    "DisableInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableInsightRulesOutputTypeDef = TypedDict(
    "EnableInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDashboardOutputTypeDef = TypedDict(
    "GetDashboardOutputTypeDef",
    {
        "DashboardArn": str,
        "DashboardBody": str,
        "DashboardName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMetricStatisticsOutputTypeDef = TypedDict(
    "GetMetricStatisticsOutputTypeDef",
    {
        "Label": str,
        "Datapoints": List[DatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMetricWidgetImageOutputTypeDef = TypedDict(
    "GetMetricWidgetImageOutputTypeDef",
    {
        "MetricWidgetImage": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDashboardsOutputTypeDef = TypedDict(
    "ListDashboardsOutputTypeDef",
    {
        "DashboardEntries": List[DashboardEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDashboardOutputTypeDef = TypedDict(
    "PutDashboardOutputTypeDef",
    {
        "DashboardValidationMessages": List[DashboardValidationMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMetricStreamOutputTypeDef = TypedDict(
    "PutMetricStreamOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef = TypedDict(
    "DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef",
    {
        "AlarmName": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "HistoryItemType": HistoryItemTypeType,
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "ScanBy": ScanByType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAlarmsInputDescribeAlarmsPaginateTypeDef = TypedDict(
    "DescribeAlarmsInputDescribeAlarmsPaginateTypeDef",
    {
        "AlarmNames": Sequence[str],
        "AlarmNamePrefix": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "ChildrenOfAlarmName": str,
        "ParentsOfAlarmName": str,
        "StateValue": StateValueType,
        "ActionPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDashboardsInputListDashboardsPaginateTypeDef = TypedDict(
    "ListDashboardsInputListDashboardsPaginateTypeDef",
    {
        "DashboardNamePrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeAlarmsInputAlarmExistsWaitTypeDef = TypedDict(
    "DescribeAlarmsInputAlarmExistsWaitTypeDef",
    {
        "AlarmNames": Sequence[str],
        "AlarmNamePrefix": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "ChildrenOfAlarmName": str,
        "ParentsOfAlarmName": str,
        "StateValue": StateValueType,
        "ActionPrefix": str,
        "MaxRecords": int,
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef = TypedDict(
    "DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef",
    {
        "AlarmNames": Sequence[str],
        "AlarmNamePrefix": str,
        "AlarmTypes": Sequence[AlarmTypeType],
        "ChildrenOfAlarmName": str,
        "ParentsOfAlarmName": str,
        "StateValue": StateValueType,
        "ActionPrefix": str,
        "MaxRecords": int,
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeInsightRulesOutputTypeDef = TypedDict(
    "DescribeInsightRulesOutputTypeDef",
    {
        "NextToken": str,
        "InsightRules": List[InsightRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMetricsInputListMetricsPaginateTypeDef = TypedDict(
    "ListMetricsInputListMetricsPaginateTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionFilterTypeDef],
        "RecentlyActive": Literal["PT3H"],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMetricsInputRequestTypeDef = TypedDict(
    "ListMetricsInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionFilterTypeDef],
        "NextToken": str,
        "RecentlyActive": Literal["PT3H"],
    },
    total=False,
)

MetricDataResultTypeDef = TypedDict(
    "MetricDataResultTypeDef",
    {
        "Id": str,
        "Label": str,
        "Timestamps": List[datetime],
        "Values": List[float],
        "StatusCode": StatusCodeType,
        "Messages": List[MessageDataTypeDef],
    },
    total=False,
)

InsightRuleContributorTypeDef = TypedDict(
    "InsightRuleContributorTypeDef",
    {
        "Keys": List[str],
        "ApproximateAggregateValue": float,
        "Datapoints": List[InsightRuleContributorDatapointTypeDef],
    },
)

ListMetricStreamsOutputTypeDef = TypedDict(
    "ListMetricStreamsOutputTypeDef",
    {
        "NextToken": str,
        "Entries": List[MetricStreamEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutCompositeAlarmInputRequestTypeDef = TypedDict(
    "_RequiredPutCompositeAlarmInputRequestTypeDef",
    {
        "AlarmName": str,
        "AlarmRule": str,
    },
)
_OptionalPutCompositeAlarmInputRequestTypeDef = TypedDict(
    "_OptionalPutCompositeAlarmInputRequestTypeDef",
    {
        "ActionsEnabled": bool,
        "AlarmActions": Sequence[str],
        "AlarmDescription": str,
        "InsufficientDataActions": Sequence[str],
        "OKActions": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class PutCompositeAlarmInputRequestTypeDef(
    _RequiredPutCompositeAlarmInputRequestTypeDef, _OptionalPutCompositeAlarmInputRequestTypeDef
):
    pass


_RequiredPutInsightRuleInputRequestTypeDef = TypedDict(
    "_RequiredPutInsightRuleInputRequestTypeDef",
    {
        "RuleName": str,
        "RuleDefinition": str,
    },
)
_OptionalPutInsightRuleInputRequestTypeDef = TypedDict(
    "_OptionalPutInsightRuleInputRequestTypeDef",
    {
        "RuleState": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class PutInsightRuleInputRequestTypeDef(
    _RequiredPutInsightRuleInputRequestTypeDef, _OptionalPutInsightRuleInputRequestTypeDef
):
    pass


TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredMetricDatumTypeDef = TypedDict(
    "_RequiredMetricDatumTypeDef",
    {
        "MetricName": str,
    },
)
_OptionalMetricDatumTypeDef = TypedDict(
    "_OptionalMetricDatumTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "Timestamp": Union[datetime, str],
        "Value": float,
        "StatisticValues": StatisticSetTypeDef,
        "Values": Sequence[float],
        "Counts": Sequence[float],
        "Unit": StandardUnitType,
        "StorageResolution": int,
    },
    total=False,
)


class MetricDatumTypeDef(_RequiredMetricDatumTypeDef, _OptionalMetricDatumTypeDef):
    pass


MetricStreamStatisticsConfigurationTypeDef = TypedDict(
    "MetricStreamStatisticsConfigurationTypeDef",
    {
        "IncludeMetrics": List[MetricStreamStatisticsMetricTypeDef],
        "AdditionalStatistics": List[str],
    },
)

ListMetricsOutputTypeDef = TypedDict(
    "ListMetricsOutputTypeDef",
    {
        "Metrics": List[MetricTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMetricStatTypeDef = TypedDict(
    "_RequiredMetricStatTypeDef",
    {
        "Metric": MetricTypeDef,
        "Period": int,
        "Stat": str,
    },
)
_OptionalMetricStatTypeDef = TypedDict(
    "_OptionalMetricStatTypeDef",
    {
        "Unit": StandardUnitType,
    },
    total=False,
)


class MetricStatTypeDef(_RequiredMetricStatTypeDef, _OptionalMetricStatTypeDef):
    pass


GetMetricDataOutputTypeDef = TypedDict(
    "GetMetricDataOutputTypeDef",
    {
        "MetricDataResults": List[MetricDataResultTypeDef],
        "NextToken": str,
        "Messages": List[MessageDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightRuleReportOutputTypeDef = TypedDict(
    "GetInsightRuleReportOutputTypeDef",
    {
        "KeyLabels": List[str],
        "AggregationStatistic": str,
        "AggregateValue": float,
        "ApproximateUniqueCount": int,
        "Contributors": List[InsightRuleContributorTypeDef],
        "MetricDatapoints": List[InsightRuleMetricDatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMetricDataInputRequestTypeDef = TypedDict(
    "PutMetricDataInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricData": Sequence[MetricDatumTypeDef],
    },
)

GetMetricStreamOutputTypeDef = TypedDict(
    "GetMetricStreamOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "IncludeFilters": List[MetricStreamFilterTypeDef],
        "ExcludeFilters": List[MetricStreamFilterTypeDef],
        "FirehoseArn": str,
        "RoleArn": str,
        "State": str,
        "CreationDate": datetime,
        "LastUpdateDate": datetime,
        "OutputFormat": MetricStreamOutputFormatType,
        "StatisticsConfigurations": List[MetricStreamStatisticsConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutMetricStreamInputRequestTypeDef = TypedDict(
    "_RequiredPutMetricStreamInputRequestTypeDef",
    {
        "Name": str,
        "FirehoseArn": str,
        "RoleArn": str,
        "OutputFormat": MetricStreamOutputFormatType,
    },
)
_OptionalPutMetricStreamInputRequestTypeDef = TypedDict(
    "_OptionalPutMetricStreamInputRequestTypeDef",
    {
        "IncludeFilters": Sequence[MetricStreamFilterTypeDef],
        "ExcludeFilters": Sequence[MetricStreamFilterTypeDef],
        "Tags": Sequence[TagTypeDef],
        "StatisticsConfigurations": Sequence[MetricStreamStatisticsConfigurationTypeDef],
    },
    total=False,
)


class PutMetricStreamInputRequestTypeDef(
    _RequiredPutMetricStreamInputRequestTypeDef, _OptionalPutMetricStreamInputRequestTypeDef
):
    pass


_RequiredMetricDataQueryTypeDef = TypedDict(
    "_RequiredMetricDataQueryTypeDef",
    {
        "Id": str,
    },
)
_OptionalMetricDataQueryTypeDef = TypedDict(
    "_OptionalMetricDataQueryTypeDef",
    {
        "MetricStat": MetricStatTypeDef,
        "Expression": str,
        "Label": str,
        "ReturnData": bool,
        "Period": int,
        "AccountId": str,
    },
    total=False,
)


class MetricDataQueryTypeDef(_RequiredMetricDataQueryTypeDef, _OptionalMetricDataQueryTypeDef):
    pass


_RequiredGetMetricDataInputGetMetricDataPaginateTypeDef = TypedDict(
    "_RequiredGetMetricDataInputGetMetricDataPaginateTypeDef",
    {
        "MetricDataQueries": Sequence[MetricDataQueryTypeDef],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetMetricDataInputGetMetricDataPaginateTypeDef = TypedDict(
    "_OptionalGetMetricDataInputGetMetricDataPaginateTypeDef",
    {
        "ScanBy": ScanByType,
        "LabelOptions": LabelOptionsTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetMetricDataInputGetMetricDataPaginateTypeDef(
    _RequiredGetMetricDataInputGetMetricDataPaginateTypeDef,
    _OptionalGetMetricDataInputGetMetricDataPaginateTypeDef,
):
    pass


_RequiredGetMetricDataInputRequestTypeDef = TypedDict(
    "_RequiredGetMetricDataInputRequestTypeDef",
    {
        "MetricDataQueries": Sequence[MetricDataQueryTypeDef],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetMetricDataInputRequestTypeDef = TypedDict(
    "_OptionalGetMetricDataInputRequestTypeDef",
    {
        "NextToken": str,
        "ScanBy": ScanByType,
        "MaxDatapoints": int,
        "LabelOptions": LabelOptionsTypeDef,
    },
    total=False,
)


class GetMetricDataInputRequestTypeDef(
    _RequiredGetMetricDataInputRequestTypeDef, _OptionalGetMetricDataInputRequestTypeDef
):
    pass


MetricAlarmTypeDef = TypedDict(
    "MetricAlarmTypeDef",
    {
        "AlarmName": str,
        "AlarmArn": str,
        "AlarmDescription": str,
        "AlarmConfigurationUpdatedTimestamp": datetime,
        "ActionsEnabled": bool,
        "OKActions": List[str],
        "AlarmActions": List[str],
        "InsufficientDataActions": List[str],
        "StateValue": StateValueType,
        "StateReason": str,
        "StateReasonData": str,
        "StateUpdatedTimestamp": datetime,
        "MetricName": str,
        "Namespace": str,
        "Statistic": StatisticType,
        "ExtendedStatistic": str,
        "Dimensions": List[DimensionTypeDef],
        "Period": int,
        "Unit": StandardUnitType,
        "EvaluationPeriods": int,
        "DatapointsToAlarm": int,
        "Threshold": float,
        "ComparisonOperator": ComparisonOperatorType,
        "TreatMissingData": str,
        "EvaluateLowSampleCountPercentile": str,
        "Metrics": List[MetricDataQueryTypeDef],
        "ThresholdMetricId": str,
    },
    total=False,
)

MetricMathAnomalyDetectorTypeDef = TypedDict(
    "MetricMathAnomalyDetectorTypeDef",
    {
        "MetricDataQueries": Sequence[MetricDataQueryTypeDef],
    },
    total=False,
)

_RequiredPutMetricAlarmInputMetricPutAlarmTypeDef = TypedDict(
    "_RequiredPutMetricAlarmInputMetricPutAlarmTypeDef",
    {
        "AlarmName": str,
        "EvaluationPeriods": int,
        "ComparisonOperator": ComparisonOperatorType,
    },
)
_OptionalPutMetricAlarmInputMetricPutAlarmTypeDef = TypedDict(
    "_OptionalPutMetricAlarmInputMetricPutAlarmTypeDef",
    {
        "AlarmDescription": str,
        "ActionsEnabled": bool,
        "OKActions": Sequence[str],
        "AlarmActions": Sequence[str],
        "InsufficientDataActions": Sequence[str],
        "Statistic": StatisticType,
        "ExtendedStatistic": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Period": int,
        "Unit": StandardUnitType,
        "DatapointsToAlarm": int,
        "Threshold": float,
        "TreatMissingData": str,
        "EvaluateLowSampleCountPercentile": str,
        "Metrics": Sequence[MetricDataQueryTypeDef],
        "Tags": Sequence[TagTypeDef],
        "ThresholdMetricId": str,
    },
    total=False,
)


class PutMetricAlarmInputMetricPutAlarmTypeDef(
    _RequiredPutMetricAlarmInputMetricPutAlarmTypeDef,
    _OptionalPutMetricAlarmInputMetricPutAlarmTypeDef,
):
    pass


_RequiredPutMetricAlarmInputRequestTypeDef = TypedDict(
    "_RequiredPutMetricAlarmInputRequestTypeDef",
    {
        "AlarmName": str,
        "EvaluationPeriods": int,
        "ComparisonOperator": ComparisonOperatorType,
    },
)
_OptionalPutMetricAlarmInputRequestTypeDef = TypedDict(
    "_OptionalPutMetricAlarmInputRequestTypeDef",
    {
        "AlarmDescription": str,
        "ActionsEnabled": bool,
        "OKActions": Sequence[str],
        "AlarmActions": Sequence[str],
        "InsufficientDataActions": Sequence[str],
        "MetricName": str,
        "Namespace": str,
        "Statistic": StatisticType,
        "ExtendedStatistic": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Period": int,
        "Unit": StandardUnitType,
        "DatapointsToAlarm": int,
        "Threshold": float,
        "TreatMissingData": str,
        "EvaluateLowSampleCountPercentile": str,
        "Metrics": Sequence[MetricDataQueryTypeDef],
        "Tags": Sequence[TagTypeDef],
        "ThresholdMetricId": str,
    },
    total=False,
)


class PutMetricAlarmInputRequestTypeDef(
    _RequiredPutMetricAlarmInputRequestTypeDef, _OptionalPutMetricAlarmInputRequestTypeDef
):
    pass


DescribeAlarmsForMetricOutputTypeDef = TypedDict(
    "DescribeAlarmsForMetricOutputTypeDef",
    {
        "MetricAlarms": List[MetricAlarmTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAlarmsOutputTypeDef = TypedDict(
    "DescribeAlarmsOutputTypeDef",
    {
        "CompositeAlarms": List[CompositeAlarmTypeDef],
        "MetricAlarms": List[MetricAlarmTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AnomalyDetectorTypeDef = TypedDict(
    "AnomalyDetectorTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": List[DimensionTypeDef],
        "Stat": str,
        "Configuration": AnomalyDetectorConfigurationTypeDef,
        "StateValue": AnomalyDetectorStateValueType,
        "SingleMetricAnomalyDetector": SingleMetricAnomalyDetectorTypeDef,
        "MetricMathAnomalyDetector": MetricMathAnomalyDetectorTypeDef,
    },
    total=False,
)

DeleteAnomalyDetectorInputRequestTypeDef = TypedDict(
    "DeleteAnomalyDetectorInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Stat": str,
        "SingleMetricAnomalyDetector": SingleMetricAnomalyDetectorTypeDef,
        "MetricMathAnomalyDetector": MetricMathAnomalyDetectorTypeDef,
    },
    total=False,
)

PutAnomalyDetectorInputRequestTypeDef = TypedDict(
    "PutAnomalyDetectorInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "Dimensions": Sequence[DimensionTypeDef],
        "Stat": str,
        "Configuration": AnomalyDetectorConfigurationTypeDef,
        "SingleMetricAnomalyDetector": SingleMetricAnomalyDetectorTypeDef,
        "MetricMathAnomalyDetector": MetricMathAnomalyDetectorTypeDef,
    },
    total=False,
)

DescribeAnomalyDetectorsOutputTypeDef = TypedDict(
    "DescribeAnomalyDetectorsOutputTypeDef",
    {
        "AnomalyDetectors": List[AnomalyDetectorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
