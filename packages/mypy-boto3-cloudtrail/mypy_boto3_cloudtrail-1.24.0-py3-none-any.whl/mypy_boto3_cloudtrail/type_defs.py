"""
Type annotations for cloudtrail service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudtrail.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    EventDataStoreStatusType,
    InsightTypeType,
    LookupAttributeKeyType,
    QueryStatusType,
    ReadWriteTypeType,
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
    "TagTypeDef",
    "AdvancedFieldSelectorTypeDef",
    "CancelQueryRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DataResourceTypeDef",
    "DeleteEventDataStoreRequestRequestTypeDef",
    "DeleteTrailRequestRequestTypeDef",
    "DescribeQueryRequestRequestTypeDef",
    "QueryStatisticsForDescribeQueryTypeDef",
    "DescribeTrailsRequestRequestTypeDef",
    "TrailTypeDef",
    "ResourceTypeDef",
    "GetEventDataStoreRequestRequestTypeDef",
    "GetEventSelectorsRequestRequestTypeDef",
    "GetInsightSelectorsRequestRequestTypeDef",
    "InsightSelectorTypeDef",
    "GetQueryResultsRequestRequestTypeDef",
    "QueryStatisticsTypeDef",
    "GetTrailRequestRequestTypeDef",
    "GetTrailStatusRequestRequestTypeDef",
    "ListEventDataStoresRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListPublicKeysRequestRequestTypeDef",
    "PublicKeyTypeDef",
    "ListQueriesRequestRequestTypeDef",
    "QueryTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTrailsRequestRequestTypeDef",
    "TrailInfoTypeDef",
    "LookupAttributeTypeDef",
    "RestoreEventDataStoreRequestRequestTypeDef",
    "StartLoggingRequestRequestTypeDef",
    "StartQueryRequestRequestTypeDef",
    "StopLoggingRequestRequestTypeDef",
    "UpdateTrailRequestRequestTypeDef",
    "AddTagsRequestRequestTypeDef",
    "CreateTrailRequestRequestTypeDef",
    "RemoveTagsRequestRequestTypeDef",
    "ResourceTagTypeDef",
    "AdvancedEventSelectorTypeDef",
    "CancelQueryResponseTypeDef",
    "CreateTrailResponseTypeDef",
    "GetTrailStatusResponseTypeDef",
    "StartQueryResponseTypeDef",
    "UpdateTrailResponseTypeDef",
    "EventSelectorTypeDef",
    "DescribeQueryResponseTypeDef",
    "DescribeTrailsResponseTypeDef",
    "GetTrailResponseTypeDef",
    "EventTypeDef",
    "GetInsightSelectorsResponseTypeDef",
    "PutInsightSelectorsRequestRequestTypeDef",
    "PutInsightSelectorsResponseTypeDef",
    "GetQueryResultsResponseTypeDef",
    "ListPublicKeysRequestListPublicKeysPaginateTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "ListTrailsRequestListTrailsPaginateTypeDef",
    "ListPublicKeysResponseTypeDef",
    "ListQueriesResponseTypeDef",
    "ListTrailsResponseTypeDef",
    "LookupEventsRequestLookupEventsPaginateTypeDef",
    "LookupEventsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "CreateEventDataStoreRequestRequestTypeDef",
    "CreateEventDataStoreResponseTypeDef",
    "EventDataStoreTypeDef",
    "GetEventDataStoreResponseTypeDef",
    "RestoreEventDataStoreResponseTypeDef",
    "UpdateEventDataStoreRequestRequestTypeDef",
    "UpdateEventDataStoreResponseTypeDef",
    "GetEventSelectorsResponseTypeDef",
    "PutEventSelectorsRequestRequestTypeDef",
    "PutEventSelectorsResponseTypeDef",
    "LookupEventsResponseTypeDef",
    "ListEventDataStoresResponseTypeDef",
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


_RequiredAdvancedFieldSelectorTypeDef = TypedDict(
    "_RequiredAdvancedFieldSelectorTypeDef",
    {
        "Field": str,
    },
)
_OptionalAdvancedFieldSelectorTypeDef = TypedDict(
    "_OptionalAdvancedFieldSelectorTypeDef",
    {
        "Equals": Sequence[str],
        "StartsWith": Sequence[str],
        "EndsWith": Sequence[str],
        "NotEquals": Sequence[str],
        "NotStartsWith": Sequence[str],
        "NotEndsWith": Sequence[str],
    },
    total=False,
)


class AdvancedFieldSelectorTypeDef(
    _RequiredAdvancedFieldSelectorTypeDef, _OptionalAdvancedFieldSelectorTypeDef
):
    pass


CancelQueryRequestRequestTypeDef = TypedDict(
    "CancelQueryRequestRequestTypeDef",
    {
        "EventDataStore": str,
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

DataResourceTypeDef = TypedDict(
    "DataResourceTypeDef",
    {
        "Type": str,
        "Values": List[str],
    },
    total=False,
)

DeleteEventDataStoreRequestRequestTypeDef = TypedDict(
    "DeleteEventDataStoreRequestRequestTypeDef",
    {
        "EventDataStore": str,
    },
)

DeleteTrailRequestRequestTypeDef = TypedDict(
    "DeleteTrailRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeQueryRequestRequestTypeDef = TypedDict(
    "DescribeQueryRequestRequestTypeDef",
    {
        "EventDataStore": str,
        "QueryId": str,
    },
)

QueryStatisticsForDescribeQueryTypeDef = TypedDict(
    "QueryStatisticsForDescribeQueryTypeDef",
    {
        "EventsMatched": int,
        "EventsScanned": int,
        "BytesScanned": int,
        "ExecutionTimeInMillis": int,
        "CreationTime": datetime,
    },
    total=False,
)

DescribeTrailsRequestRequestTypeDef = TypedDict(
    "DescribeTrailsRequestRequestTypeDef",
    {
        "trailNameList": Sequence[str],
        "includeShadowTrails": bool,
    },
    total=False,
)

TrailTypeDef = TypedDict(
    "TrailTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "HomeRegion": str,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "HasCustomEventSelectors": bool,
        "HasInsightSelectors": bool,
        "IsOrganizationTrail": bool,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "ResourceType": str,
        "ResourceName": str,
    },
    total=False,
)

GetEventDataStoreRequestRequestTypeDef = TypedDict(
    "GetEventDataStoreRequestRequestTypeDef",
    {
        "EventDataStore": str,
    },
)

GetEventSelectorsRequestRequestTypeDef = TypedDict(
    "GetEventSelectorsRequestRequestTypeDef",
    {
        "TrailName": str,
    },
)

GetInsightSelectorsRequestRequestTypeDef = TypedDict(
    "GetInsightSelectorsRequestRequestTypeDef",
    {
        "TrailName": str,
    },
)

InsightSelectorTypeDef = TypedDict(
    "InsightSelectorTypeDef",
    {
        "InsightType": InsightTypeType,
    },
    total=False,
)

_RequiredGetQueryResultsRequestRequestTypeDef = TypedDict(
    "_RequiredGetQueryResultsRequestRequestTypeDef",
    {
        "EventDataStore": str,
        "QueryId": str,
    },
)
_OptionalGetQueryResultsRequestRequestTypeDef = TypedDict(
    "_OptionalGetQueryResultsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxQueryResults": int,
    },
    total=False,
)


class GetQueryResultsRequestRequestTypeDef(
    _RequiredGetQueryResultsRequestRequestTypeDef, _OptionalGetQueryResultsRequestRequestTypeDef
):
    pass


QueryStatisticsTypeDef = TypedDict(
    "QueryStatisticsTypeDef",
    {
        "ResultsCount": int,
        "TotalResultsCount": int,
        "BytesScanned": int,
    },
    total=False,
)

GetTrailRequestRequestTypeDef = TypedDict(
    "GetTrailRequestRequestTypeDef",
    {
        "Name": str,
    },
)

GetTrailStatusRequestRequestTypeDef = TypedDict(
    "GetTrailStatusRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ListEventDataStoresRequestRequestTypeDef = TypedDict(
    "ListEventDataStoresRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
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

ListPublicKeysRequestRequestTypeDef = TypedDict(
    "ListPublicKeysRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "NextToken": str,
    },
    total=False,
)

PublicKeyTypeDef = TypedDict(
    "PublicKeyTypeDef",
    {
        "Value": bytes,
        "ValidityStartTime": datetime,
        "ValidityEndTime": datetime,
        "Fingerprint": str,
    },
    total=False,
)

_RequiredListQueriesRequestRequestTypeDef = TypedDict(
    "_RequiredListQueriesRequestRequestTypeDef",
    {
        "EventDataStore": str,
    },
)
_OptionalListQueriesRequestRequestTypeDef = TypedDict(
    "_OptionalListQueriesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "QueryStatus": QueryStatusType,
    },
    total=False,
)


class ListQueriesRequestRequestTypeDef(
    _RequiredListQueriesRequestRequestTypeDef, _OptionalListQueriesRequestRequestTypeDef
):
    pass


QueryTypeDef = TypedDict(
    "QueryTypeDef",
    {
        "QueryId": str,
        "QueryStatus": QueryStatusType,
        "CreationTime": datetime,
    },
    total=False,
)

_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "ResourceIdList": Sequence[str],
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass


ListTrailsRequestRequestTypeDef = TypedDict(
    "ListTrailsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

TrailInfoTypeDef = TypedDict(
    "TrailInfoTypeDef",
    {
        "TrailARN": str,
        "Name": str,
        "HomeRegion": str,
    },
    total=False,
)

LookupAttributeTypeDef = TypedDict(
    "LookupAttributeTypeDef",
    {
        "AttributeKey": LookupAttributeKeyType,
        "AttributeValue": str,
    },
)

RestoreEventDataStoreRequestRequestTypeDef = TypedDict(
    "RestoreEventDataStoreRequestRequestTypeDef",
    {
        "EventDataStore": str,
    },
)

StartLoggingRequestRequestTypeDef = TypedDict(
    "StartLoggingRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StartQueryRequestRequestTypeDef = TypedDict(
    "StartQueryRequestRequestTypeDef",
    {
        "QueryStatement": str,
    },
)

StopLoggingRequestRequestTypeDef = TypedDict(
    "StopLoggingRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredUpdateTrailRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrailRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateTrailRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrailRequestRequestTypeDef",
    {
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "EnableLogFileValidation": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
    },
    total=False,
)


class UpdateTrailRequestRequestTypeDef(
    _RequiredUpdateTrailRequestRequestTypeDef, _OptionalUpdateTrailRequestRequestTypeDef
):
    pass


AddTagsRequestRequestTypeDef = TypedDict(
    "AddTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagsList": Sequence[TagTypeDef],
    },
)

_RequiredCreateTrailRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrailRequestRequestTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
    },
)
_OptionalCreateTrailRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrailRequestRequestTypeDef",
    {
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "EnableLogFileValidation": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
        "TagsList": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateTrailRequestRequestTypeDef(
    _RequiredCreateTrailRequestRequestTypeDef, _OptionalCreateTrailRequestRequestTypeDef
):
    pass


RemoveTagsRequestRequestTypeDef = TypedDict(
    "RemoveTagsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagsList": Sequence[TagTypeDef],
    },
)

ResourceTagTypeDef = TypedDict(
    "ResourceTagTypeDef",
    {
        "ResourceId": str,
        "TagsList": List[TagTypeDef],
    },
    total=False,
)

_RequiredAdvancedEventSelectorTypeDef = TypedDict(
    "_RequiredAdvancedEventSelectorTypeDef",
    {
        "FieldSelectors": Sequence[AdvancedFieldSelectorTypeDef],
    },
)
_OptionalAdvancedEventSelectorTypeDef = TypedDict(
    "_OptionalAdvancedEventSelectorTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class AdvancedEventSelectorTypeDef(
    _RequiredAdvancedEventSelectorTypeDef, _OptionalAdvancedEventSelectorTypeDef
):
    pass


CancelQueryResponseTypeDef = TypedDict(
    "CancelQueryResponseTypeDef",
    {
        "QueryId": str,
        "QueryStatus": QueryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrailResponseTypeDef = TypedDict(
    "CreateTrailResponseTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrailStatusResponseTypeDef = TypedDict(
    "GetTrailStatusResponseTypeDef",
    {
        "IsLogging": bool,
        "LatestDeliveryError": str,
        "LatestNotificationError": str,
        "LatestDeliveryTime": datetime,
        "LatestNotificationTime": datetime,
        "StartLoggingTime": datetime,
        "StopLoggingTime": datetime,
        "LatestCloudWatchLogsDeliveryError": str,
        "LatestCloudWatchLogsDeliveryTime": datetime,
        "LatestDigestDeliveryTime": datetime,
        "LatestDigestDeliveryError": str,
        "LatestDeliveryAttemptTime": str,
        "LatestNotificationAttemptTime": str,
        "LatestNotificationAttemptSucceeded": str,
        "LatestDeliveryAttemptSucceeded": str,
        "TimeLoggingStarted": str,
        "TimeLoggingStopped": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartQueryResponseTypeDef = TypedDict(
    "StartQueryResponseTypeDef",
    {
        "QueryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrailResponseTypeDef = TypedDict(
    "UpdateTrailResponseTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventSelectorTypeDef = TypedDict(
    "EventSelectorTypeDef",
    {
        "ReadWriteType": ReadWriteTypeType,
        "IncludeManagementEvents": bool,
        "DataResources": List[DataResourceTypeDef],
        "ExcludeManagementEventSources": List[str],
    },
    total=False,
)

DescribeQueryResponseTypeDef = TypedDict(
    "DescribeQueryResponseTypeDef",
    {
        "QueryId": str,
        "QueryString": str,
        "QueryStatus": QueryStatusType,
        "QueryStatistics": QueryStatisticsForDescribeQueryTypeDef,
        "ErrorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTrailsResponseTypeDef = TypedDict(
    "DescribeTrailsResponseTypeDef",
    {
        "trailList": List[TrailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTrailResponseTypeDef = TypedDict(
    "GetTrailResponseTypeDef",
    {
        "Trail": TrailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "EventId": str,
        "EventName": str,
        "ReadOnly": str,
        "AccessKeyId": str,
        "EventTime": datetime,
        "EventSource": str,
        "Username": str,
        "Resources": List[ResourceTypeDef],
        "CloudTrailEvent": str,
    },
    total=False,
)

GetInsightSelectorsResponseTypeDef = TypedDict(
    "GetInsightSelectorsResponseTypeDef",
    {
        "TrailARN": str,
        "InsightSelectors": List[InsightSelectorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutInsightSelectorsRequestRequestTypeDef = TypedDict(
    "PutInsightSelectorsRequestRequestTypeDef",
    {
        "TrailName": str,
        "InsightSelectors": Sequence[InsightSelectorTypeDef],
    },
)

PutInsightSelectorsResponseTypeDef = TypedDict(
    "PutInsightSelectorsResponseTypeDef",
    {
        "TrailARN": str,
        "InsightSelectors": List[InsightSelectorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryResultsResponseTypeDef = TypedDict(
    "GetQueryResultsResponseTypeDef",
    {
        "QueryStatus": QueryStatusType,
        "QueryStatistics": QueryStatisticsTypeDef,
        "QueryResultRows": List[List[Dict[str, str]]],
        "NextToken": str,
        "ErrorMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPublicKeysRequestListPublicKeysPaginateTypeDef = TypedDict(
    "ListPublicKeysRequestListPublicKeysPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_RequiredListTagsRequestListTagsPaginateTypeDef",
    {
        "ResourceIdList": Sequence[str],
    },
)
_OptionalListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_OptionalListTagsRequestListTagsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsRequestListTagsPaginateTypeDef(
    _RequiredListTagsRequestListTagsPaginateTypeDef, _OptionalListTagsRequestListTagsPaginateTypeDef
):
    pass


ListTrailsRequestListTrailsPaginateTypeDef = TypedDict(
    "ListTrailsRequestListTrailsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPublicKeysResponseTypeDef = TypedDict(
    "ListPublicKeysResponseTypeDef",
    {
        "PublicKeyList": List[PublicKeyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueriesResponseTypeDef = TypedDict(
    "ListQueriesResponseTypeDef",
    {
        "Queries": List[QueryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrailsResponseTypeDef = TypedDict(
    "ListTrailsResponseTypeDef",
    {
        "Trails": List[TrailInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LookupEventsRequestLookupEventsPaginateTypeDef = TypedDict(
    "LookupEventsRequestLookupEventsPaginateTypeDef",
    {
        "LookupAttributes": Sequence[LookupAttributeTypeDef],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "EventCategory": Literal["insight"],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

LookupEventsRequestRequestTypeDef = TypedDict(
    "LookupEventsRequestRequestTypeDef",
    {
        "LookupAttributes": Sequence[LookupAttributeTypeDef],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "EventCategory": Literal["insight"],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "ResourceTagList": List[ResourceTagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateEventDataStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEventDataStoreRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateEventDataStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEventDataStoreRequestRequestTypeDef",
    {
        "AdvancedEventSelectors": Sequence[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
        "TagsList": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEventDataStoreRequestRequestTypeDef(
    _RequiredCreateEventDataStoreRequestRequestTypeDef,
    _OptionalCreateEventDataStoreRequestRequestTypeDef,
):
    pass


CreateEventDataStoreResponseTypeDef = TypedDict(
    "CreateEventDataStoreResponseTypeDef",
    {
        "EventDataStoreArn": str,
        "Name": str,
        "Status": EventDataStoreStatusType,
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
        "TagsList": List[TagTypeDef],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventDataStoreTypeDef = TypedDict(
    "EventDataStoreTypeDef",
    {
        "EventDataStoreArn": str,
        "Name": str,
        "TerminationProtectionEnabled": bool,
        "Status": EventDataStoreStatusType,
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

GetEventDataStoreResponseTypeDef = TypedDict(
    "GetEventDataStoreResponseTypeDef",
    {
        "EventDataStoreArn": str,
        "Name": str,
        "Status": EventDataStoreStatusType,
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreEventDataStoreResponseTypeDef = TypedDict(
    "RestoreEventDataStoreResponseTypeDef",
    {
        "EventDataStoreArn": str,
        "Name": str,
        "Status": EventDataStoreStatusType,
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateEventDataStoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEventDataStoreRequestRequestTypeDef",
    {
        "EventDataStore": str,
    },
)
_OptionalUpdateEventDataStoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEventDataStoreRequestRequestTypeDef",
    {
        "Name": str,
        "AdvancedEventSelectors": Sequence[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
    },
    total=False,
)


class UpdateEventDataStoreRequestRequestTypeDef(
    _RequiredUpdateEventDataStoreRequestRequestTypeDef,
    _OptionalUpdateEventDataStoreRequestRequestTypeDef,
):
    pass


UpdateEventDataStoreResponseTypeDef = TypedDict(
    "UpdateEventDataStoreResponseTypeDef",
    {
        "EventDataStoreArn": str,
        "Name": str,
        "Status": EventDataStoreStatusType,
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "MultiRegionEnabled": bool,
        "OrganizationEnabled": bool,
        "RetentionPeriod": int,
        "TerminationProtectionEnabled": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEventSelectorsResponseTypeDef = TypedDict(
    "GetEventSelectorsResponseTypeDef",
    {
        "TrailARN": str,
        "EventSelectors": List[EventSelectorTypeDef],
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutEventSelectorsRequestRequestTypeDef = TypedDict(
    "_RequiredPutEventSelectorsRequestRequestTypeDef",
    {
        "TrailName": str,
    },
)
_OptionalPutEventSelectorsRequestRequestTypeDef = TypedDict(
    "_OptionalPutEventSelectorsRequestRequestTypeDef",
    {
        "EventSelectors": Sequence[EventSelectorTypeDef],
        "AdvancedEventSelectors": Sequence[AdvancedEventSelectorTypeDef],
    },
    total=False,
)


class PutEventSelectorsRequestRequestTypeDef(
    _RequiredPutEventSelectorsRequestRequestTypeDef, _OptionalPutEventSelectorsRequestRequestTypeDef
):
    pass


PutEventSelectorsResponseTypeDef = TypedDict(
    "PutEventSelectorsResponseTypeDef",
    {
        "TrailARN": str,
        "EventSelectors": List[EventSelectorTypeDef],
        "AdvancedEventSelectors": List[AdvancedEventSelectorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LookupEventsResponseTypeDef = TypedDict(
    "LookupEventsResponseTypeDef",
    {
        "Events": List[EventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventDataStoresResponseTypeDef = TypedDict(
    "ListEventDataStoresResponseTypeDef",
    {
        "EventDataStores": List[EventDataStoreTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
