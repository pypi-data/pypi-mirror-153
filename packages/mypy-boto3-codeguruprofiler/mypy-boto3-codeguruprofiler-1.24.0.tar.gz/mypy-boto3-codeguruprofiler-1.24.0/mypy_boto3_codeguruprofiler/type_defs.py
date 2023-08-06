"""
Type annotations for codeguruprofiler service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguruprofiler/type_defs/)

Usage::

    ```python
    from mypy_boto3_codeguruprofiler.type_defs import ChannelTypeDef

    data: ChannelTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AgentParameterFieldType,
    AggregationPeriodType,
    ComputePlatformType,
    FeedbackTypeType,
    MetadataFieldType,
    OrderByType,
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
    "ChannelTypeDef",
    "ResponseMetadataTypeDef",
    "AgentConfigurationTypeDef",
    "AgentOrchestrationConfigTypeDef",
    "AggregatedProfileTimeTypeDef",
    "UserFeedbackTypeDef",
    "MetricTypeDef",
    "FrameMetricTypeDef",
    "TimestampStructureTypeDef",
    "ConfigureAgentRequestRequestTypeDef",
    "DeleteProfilingGroupRequestRequestTypeDef",
    "DescribeProfilingGroupRequestRequestTypeDef",
    "FindingsReportSummaryTypeDef",
    "GetFindingsReportAccountSummaryRequestRequestTypeDef",
    "GetNotificationConfigurationRequestRequestTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetProfileRequestRequestTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "ListFindingsReportsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListProfileTimesRequestRequestTypeDef",
    "ProfileTimeTypeDef",
    "ListProfilingGroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MatchTypeDef",
    "PatternTypeDef",
    "PostAgentProfileRequestRequestTypeDef",
    "PutPermissionRequestRequestTypeDef",
    "RemoveNotificationChannelRequestRequestTypeDef",
    "RemovePermissionRequestRequestTypeDef",
    "SubmitFeedbackRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AddNotificationChannelsRequestRequestTypeDef",
    "NotificationConfigurationTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProfileResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutPermissionResponseTypeDef",
    "RemovePermissionResponseTypeDef",
    "ConfigureAgentResponseTypeDef",
    "CreateProfilingGroupRequestRequestTypeDef",
    "UpdateProfilingGroupRequestRequestTypeDef",
    "ProfilingStatusTypeDef",
    "AnomalyInstanceTypeDef",
    "BatchGetFrameMetricDataRequestRequestTypeDef",
    "FrameMetricDatumTypeDef",
    "GetFindingsReportAccountSummaryResponseTypeDef",
    "ListFindingsReportsResponseTypeDef",
    "ListProfileTimesRequestListProfileTimesPaginateTypeDef",
    "ListProfileTimesResponseTypeDef",
    "RecommendationTypeDef",
    "AddNotificationChannelsResponseTypeDef",
    "GetNotificationConfigurationResponseTypeDef",
    "RemoveNotificationChannelResponseTypeDef",
    "ProfilingGroupDescriptionTypeDef",
    "AnomalyTypeDef",
    "BatchGetFrameMetricDataResponseTypeDef",
    "CreateProfilingGroupResponseTypeDef",
    "DescribeProfilingGroupResponseTypeDef",
    "ListProfilingGroupsResponseTypeDef",
    "UpdateProfilingGroupResponseTypeDef",
    "GetRecommendationsResponseTypeDef",
)

_RequiredChannelTypeDef = TypedDict(
    "_RequiredChannelTypeDef",
    {
        "eventPublishers": Sequence[Literal["AnomalyDetection"]],
        "uri": str,
    },
)
_OptionalChannelTypeDef = TypedDict(
    "_OptionalChannelTypeDef",
    {
        "id": str,
    },
    total=False,
)


class ChannelTypeDef(_RequiredChannelTypeDef, _OptionalChannelTypeDef):
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

_RequiredAgentConfigurationTypeDef = TypedDict(
    "_RequiredAgentConfigurationTypeDef",
    {
        "periodInSeconds": int,
        "shouldProfile": bool,
    },
)
_OptionalAgentConfigurationTypeDef = TypedDict(
    "_OptionalAgentConfigurationTypeDef",
    {
        "agentParameters": Dict[AgentParameterFieldType, str],
    },
    total=False,
)


class AgentConfigurationTypeDef(
    _RequiredAgentConfigurationTypeDef, _OptionalAgentConfigurationTypeDef
):
    pass


AgentOrchestrationConfigTypeDef = TypedDict(
    "AgentOrchestrationConfigTypeDef",
    {
        "profilingEnabled": bool,
    },
)

AggregatedProfileTimeTypeDef = TypedDict(
    "AggregatedProfileTimeTypeDef",
    {
        "period": AggregationPeriodType,
        "start": datetime,
    },
    total=False,
)

UserFeedbackTypeDef = TypedDict(
    "UserFeedbackTypeDef",
    {
        "type": FeedbackTypeType,
    },
)

MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "frameName": str,
        "threadStates": List[str],
        "type": Literal["AggregatedRelativeTotalTime"],
    },
)

FrameMetricTypeDef = TypedDict(
    "FrameMetricTypeDef",
    {
        "frameName": str,
        "threadStates": Sequence[str],
        "type": Literal["AggregatedRelativeTotalTime"],
    },
)

TimestampStructureTypeDef = TypedDict(
    "TimestampStructureTypeDef",
    {
        "value": datetime,
    },
)

_RequiredConfigureAgentRequestRequestTypeDef = TypedDict(
    "_RequiredConfigureAgentRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)
_OptionalConfigureAgentRequestRequestTypeDef = TypedDict(
    "_OptionalConfigureAgentRequestRequestTypeDef",
    {
        "fleetInstanceId": str,
        "metadata": Mapping[MetadataFieldType, str],
    },
    total=False,
)


class ConfigureAgentRequestRequestTypeDef(
    _RequiredConfigureAgentRequestRequestTypeDef, _OptionalConfigureAgentRequestRequestTypeDef
):
    pass


DeleteProfilingGroupRequestRequestTypeDef = TypedDict(
    "DeleteProfilingGroupRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)

DescribeProfilingGroupRequestRequestTypeDef = TypedDict(
    "DescribeProfilingGroupRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)

FindingsReportSummaryTypeDef = TypedDict(
    "FindingsReportSummaryTypeDef",
    {
        "id": str,
        "profileEndTime": datetime,
        "profileStartTime": datetime,
        "profilingGroupName": str,
        "totalNumberOfFindings": int,
    },
    total=False,
)

GetFindingsReportAccountSummaryRequestRequestTypeDef = TypedDict(
    "GetFindingsReportAccountSummaryRequestRequestTypeDef",
    {
        "dailyReportsOnly": bool,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

GetNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "GetNotificationConfigurationRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)

GetPolicyRequestRequestTypeDef = TypedDict(
    "GetPolicyRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)

_RequiredGetProfileRequestRequestTypeDef = TypedDict(
    "_RequiredGetProfileRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)
_OptionalGetProfileRequestRequestTypeDef = TypedDict(
    "_OptionalGetProfileRequestRequestTypeDef",
    {
        "accept": str,
        "endTime": Union[datetime, str],
        "maxDepth": int,
        "period": str,
        "startTime": Union[datetime, str],
    },
    total=False,
)


class GetProfileRequestRequestTypeDef(
    _RequiredGetProfileRequestRequestTypeDef, _OptionalGetProfileRequestRequestTypeDef
):
    pass


_RequiredGetRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredGetRecommendationsRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "profilingGroupName": str,
        "startTime": Union[datetime, str],
    },
)
_OptionalGetRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalGetRecommendationsRequestRequestTypeDef",
    {
        "locale": str,
    },
    total=False,
)


class GetRecommendationsRequestRequestTypeDef(
    _RequiredGetRecommendationsRequestRequestTypeDef,
    _OptionalGetRecommendationsRequestRequestTypeDef,
):
    pass


_RequiredListFindingsReportsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingsReportsRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "profilingGroupName": str,
        "startTime": Union[datetime, str],
    },
)
_OptionalListFindingsReportsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingsReportsRequestRequestTypeDef",
    {
        "dailyReportsOnly": bool,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFindingsReportsRequestRequestTypeDef(
    _RequiredListFindingsReportsRequestRequestTypeDef,
    _OptionalListFindingsReportsRequestRequestTypeDef,
):
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

_RequiredListProfileTimesRequestRequestTypeDef = TypedDict(
    "_RequiredListProfileTimesRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "period": AggregationPeriodType,
        "profilingGroupName": str,
        "startTime": Union[datetime, str],
    },
)
_OptionalListProfileTimesRequestRequestTypeDef = TypedDict(
    "_OptionalListProfileTimesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "orderBy": OrderByType,
    },
    total=False,
)


class ListProfileTimesRequestRequestTypeDef(
    _RequiredListProfileTimesRequestRequestTypeDef, _OptionalListProfileTimesRequestRequestTypeDef
):
    pass


ProfileTimeTypeDef = TypedDict(
    "ProfileTimeTypeDef",
    {
        "start": datetime,
    },
    total=False,
)

ListProfilingGroupsRequestRequestTypeDef = TypedDict(
    "ListProfilingGroupsRequestRequestTypeDef",
    {
        "includeDescription": bool,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

MatchTypeDef = TypedDict(
    "MatchTypeDef",
    {
        "frameAddress": str,
        "targetFramesIndex": int,
        "thresholdBreachValue": float,
    },
    total=False,
)

PatternTypeDef = TypedDict(
    "PatternTypeDef",
    {
        "countersToAggregate": List[str],
        "description": str,
        "id": str,
        "name": str,
        "resolutionSteps": str,
        "targetFrames": List[List[str]],
        "thresholdPercent": float,
    },
    total=False,
)

_RequiredPostAgentProfileRequestRequestTypeDef = TypedDict(
    "_RequiredPostAgentProfileRequestRequestTypeDef",
    {
        "agentProfile": Union[str, bytes, IO[Any], StreamingBody],
        "contentType": str,
        "profilingGroupName": str,
    },
)
_OptionalPostAgentProfileRequestRequestTypeDef = TypedDict(
    "_OptionalPostAgentProfileRequestRequestTypeDef",
    {
        "profileToken": str,
    },
    total=False,
)


class PostAgentProfileRequestRequestTypeDef(
    _RequiredPostAgentProfileRequestRequestTypeDef, _OptionalPostAgentProfileRequestRequestTypeDef
):
    pass


_RequiredPutPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredPutPermissionRequestRequestTypeDef",
    {
        "actionGroup": Literal["agentPermissions"],
        "principals": Sequence[str],
        "profilingGroupName": str,
    },
)
_OptionalPutPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalPutPermissionRequestRequestTypeDef",
    {
        "revisionId": str,
    },
    total=False,
)


class PutPermissionRequestRequestTypeDef(
    _RequiredPutPermissionRequestRequestTypeDef, _OptionalPutPermissionRequestRequestTypeDef
):
    pass


RemoveNotificationChannelRequestRequestTypeDef = TypedDict(
    "RemoveNotificationChannelRequestRequestTypeDef",
    {
        "channelId": str,
        "profilingGroupName": str,
    },
)

RemovePermissionRequestRequestTypeDef = TypedDict(
    "RemovePermissionRequestRequestTypeDef",
    {
        "actionGroup": Literal["agentPermissions"],
        "profilingGroupName": str,
        "revisionId": str,
    },
)

_RequiredSubmitFeedbackRequestRequestTypeDef = TypedDict(
    "_RequiredSubmitFeedbackRequestRequestTypeDef",
    {
        "anomalyInstanceId": str,
        "profilingGroupName": str,
        "type": FeedbackTypeType,
    },
)
_OptionalSubmitFeedbackRequestRequestTypeDef = TypedDict(
    "_OptionalSubmitFeedbackRequestRequestTypeDef",
    {
        "comment": str,
    },
    total=False,
)


class SubmitFeedbackRequestRequestTypeDef(
    _RequiredSubmitFeedbackRequestRequestTypeDef, _OptionalSubmitFeedbackRequestRequestTypeDef
):
    pass


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

AddNotificationChannelsRequestRequestTypeDef = TypedDict(
    "AddNotificationChannelsRequestRequestTypeDef",
    {
        "channels": Sequence[ChannelTypeDef],
        "profilingGroupName": str,
    },
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "channels": List[ChannelTypeDef],
    },
    total=False,
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "policy": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProfileResponseTypeDef = TypedDict(
    "GetProfileResponseTypeDef",
    {
        "contentEncoding": str,
        "contentType": str,
        "profile": StreamingBody,
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

PutPermissionResponseTypeDef = TypedDict(
    "PutPermissionResponseTypeDef",
    {
        "policy": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemovePermissionResponseTypeDef = TypedDict(
    "RemovePermissionResponseTypeDef",
    {
        "policy": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigureAgentResponseTypeDef = TypedDict(
    "ConfigureAgentResponseTypeDef",
    {
        "configuration": AgentConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateProfilingGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProfilingGroupRequestRequestTypeDef",
    {
        "clientToken": str,
        "profilingGroupName": str,
    },
)
_OptionalCreateProfilingGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProfilingGroupRequestRequestTypeDef",
    {
        "agentOrchestrationConfig": AgentOrchestrationConfigTypeDef,
        "computePlatform": ComputePlatformType,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateProfilingGroupRequestRequestTypeDef(
    _RequiredCreateProfilingGroupRequestRequestTypeDef,
    _OptionalCreateProfilingGroupRequestRequestTypeDef,
):
    pass


UpdateProfilingGroupRequestRequestTypeDef = TypedDict(
    "UpdateProfilingGroupRequestRequestTypeDef",
    {
        "agentOrchestrationConfig": AgentOrchestrationConfigTypeDef,
        "profilingGroupName": str,
    },
)

ProfilingStatusTypeDef = TypedDict(
    "ProfilingStatusTypeDef",
    {
        "latestAgentOrchestratedAt": datetime,
        "latestAgentProfileReportedAt": datetime,
        "latestAggregatedProfile": AggregatedProfileTimeTypeDef,
    },
    total=False,
)

_RequiredAnomalyInstanceTypeDef = TypedDict(
    "_RequiredAnomalyInstanceTypeDef",
    {
        "id": str,
        "startTime": datetime,
    },
)
_OptionalAnomalyInstanceTypeDef = TypedDict(
    "_OptionalAnomalyInstanceTypeDef",
    {
        "endTime": datetime,
        "userFeedback": UserFeedbackTypeDef,
    },
    total=False,
)


class AnomalyInstanceTypeDef(_RequiredAnomalyInstanceTypeDef, _OptionalAnomalyInstanceTypeDef):
    pass


_RequiredBatchGetFrameMetricDataRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetFrameMetricDataRequestRequestTypeDef",
    {
        "profilingGroupName": str,
    },
)
_OptionalBatchGetFrameMetricDataRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetFrameMetricDataRequestRequestTypeDef",
    {
        "endTime": Union[datetime, str],
        "frameMetrics": Sequence[FrameMetricTypeDef],
        "period": str,
        "startTime": Union[datetime, str],
        "targetResolution": AggregationPeriodType,
    },
    total=False,
)


class BatchGetFrameMetricDataRequestRequestTypeDef(
    _RequiredBatchGetFrameMetricDataRequestRequestTypeDef,
    _OptionalBatchGetFrameMetricDataRequestRequestTypeDef,
):
    pass


FrameMetricDatumTypeDef = TypedDict(
    "FrameMetricDatumTypeDef",
    {
        "frameMetric": FrameMetricTypeDef,
        "values": List[float],
    },
)

GetFindingsReportAccountSummaryResponseTypeDef = TypedDict(
    "GetFindingsReportAccountSummaryResponseTypeDef",
    {
        "nextToken": str,
        "reportSummaries": List[FindingsReportSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsReportsResponseTypeDef = TypedDict(
    "ListFindingsReportsResponseTypeDef",
    {
        "findingsReportSummaries": List[FindingsReportSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListProfileTimesRequestListProfileTimesPaginateTypeDef = TypedDict(
    "_RequiredListProfileTimesRequestListProfileTimesPaginateTypeDef",
    {
        "endTime": Union[datetime, str],
        "period": AggregationPeriodType,
        "profilingGroupName": str,
        "startTime": Union[datetime, str],
    },
)
_OptionalListProfileTimesRequestListProfileTimesPaginateTypeDef = TypedDict(
    "_OptionalListProfileTimesRequestListProfileTimesPaginateTypeDef",
    {
        "orderBy": OrderByType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListProfileTimesRequestListProfileTimesPaginateTypeDef(
    _RequiredListProfileTimesRequestListProfileTimesPaginateTypeDef,
    _OptionalListProfileTimesRequestListProfileTimesPaginateTypeDef,
):
    pass


ListProfileTimesResponseTypeDef = TypedDict(
    "ListProfileTimesResponseTypeDef",
    {
        "nextToken": str,
        "profileTimes": List[ProfileTimeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "allMatchesCount": int,
        "allMatchesSum": float,
        "endTime": datetime,
        "pattern": PatternTypeDef,
        "startTime": datetime,
        "topMatches": List[MatchTypeDef],
    },
)

AddNotificationChannelsResponseTypeDef = TypedDict(
    "AddNotificationChannelsResponseTypeDef",
    {
        "notificationConfiguration": NotificationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNotificationConfigurationResponseTypeDef = TypedDict(
    "GetNotificationConfigurationResponseTypeDef",
    {
        "notificationConfiguration": NotificationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveNotificationChannelResponseTypeDef = TypedDict(
    "RemoveNotificationChannelResponseTypeDef",
    {
        "notificationConfiguration": NotificationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProfilingGroupDescriptionTypeDef = TypedDict(
    "ProfilingGroupDescriptionTypeDef",
    {
        "agentOrchestrationConfig": AgentOrchestrationConfigTypeDef,
        "arn": str,
        "computePlatform": ComputePlatformType,
        "createdAt": datetime,
        "name": str,
        "profilingStatus": ProfilingStatusTypeDef,
        "tags": Dict[str, str],
        "updatedAt": datetime,
    },
    total=False,
)

AnomalyTypeDef = TypedDict(
    "AnomalyTypeDef",
    {
        "instances": List[AnomalyInstanceTypeDef],
        "metric": MetricTypeDef,
        "reason": str,
    },
)

BatchGetFrameMetricDataResponseTypeDef = TypedDict(
    "BatchGetFrameMetricDataResponseTypeDef",
    {
        "endTime": datetime,
        "endTimes": List[TimestampStructureTypeDef],
        "frameMetricData": List[FrameMetricDatumTypeDef],
        "resolution": AggregationPeriodType,
        "startTime": datetime,
        "unprocessedEndTimes": Dict[str, List[TimestampStructureTypeDef]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProfilingGroupResponseTypeDef = TypedDict(
    "CreateProfilingGroupResponseTypeDef",
    {
        "profilingGroup": ProfilingGroupDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProfilingGroupResponseTypeDef = TypedDict(
    "DescribeProfilingGroupResponseTypeDef",
    {
        "profilingGroup": ProfilingGroupDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProfilingGroupsResponseTypeDef = TypedDict(
    "ListProfilingGroupsResponseTypeDef",
    {
        "nextToken": str,
        "profilingGroupNames": List[str],
        "profilingGroups": List[ProfilingGroupDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProfilingGroupResponseTypeDef = TypedDict(
    "UpdateProfilingGroupResponseTypeDef",
    {
        "profilingGroup": ProfilingGroupDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecommendationsResponseTypeDef = TypedDict(
    "GetRecommendationsResponseTypeDef",
    {
        "anomalies": List[AnomalyTypeDef],
        "profileEndTime": datetime,
        "profileStartTime": datetime,
        "profilingGroupName": str,
        "recommendations": List[RecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
