"""
Type annotations for ssm-incidents service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_incidents.type_defs import AddRegionActionTypeDef

    data: AddRegionActionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    IncidentRecordStatusType,
    ItemTypeType,
    RegionStatusType,
    ReplicationSetStatusType,
    SortOrderType,
    SsmTargetAccountType,
    VariableTypeType,
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
    "AddRegionActionTypeDef",
    "AttributeValueListTypeDef",
    "AutomationExecutionTypeDef",
    "ChatChannelTypeDef",
    "RegionMapInputValueTypeDef",
    "ResponseMetadataTypeDef",
    "CreateTimelineEventInputRequestTypeDef",
    "DeleteIncidentRecordInputRequestTypeDef",
    "DeleteRegionActionTypeDef",
    "DeleteReplicationSetInputRequestTypeDef",
    "DeleteResourcePolicyInputRequestTypeDef",
    "DeleteResponsePlanInputRequestTypeDef",
    "DeleteTimelineEventInputRequestTypeDef",
    "DynamicSsmParameterValueTypeDef",
    "EventSummaryTypeDef",
    "GetIncidentRecordInputRequestTypeDef",
    "GetReplicationSetInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "PaginatorConfigTypeDef",
    "GetResourcePoliciesInputRequestTypeDef",
    "ResourcePolicyTypeDef",
    "GetResponsePlanInputRequestTypeDef",
    "GetTimelineEventInputRequestTypeDef",
    "TimelineEventTypeDef",
    "IncidentRecordSourceTypeDef",
    "NotificationTargetItemTypeDef",
    "ItemValueTypeDef",
    "ListRelatedItemsInputRequestTypeDef",
    "ListReplicationSetsInputRequestTypeDef",
    "ListResponsePlansInputRequestTypeDef",
    "ResponsePlanSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutResourcePolicyInputRequestTypeDef",
    "RegionInfoTypeDef",
    "TriggerDetailsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeletionProtectionInputRequestTypeDef",
    "UpdateTimelineEventInputRequestTypeDef",
    "ConditionTypeDef",
    "CreateReplicationSetInputRequestTypeDef",
    "CreateReplicationSetOutputTypeDef",
    "CreateResponsePlanOutputTypeDef",
    "CreateTimelineEventOutputTypeDef",
    "ListReplicationSetsOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "StartIncidentOutputTypeDef",
    "UpdateReplicationSetActionTypeDef",
    "SsmAutomationTypeDef",
    "ListTimelineEventsOutputTypeDef",
    "GetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef",
    "GetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef",
    "GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef",
    "ListRelatedItemsInputListRelatedItemsPaginateTypeDef",
    "ListReplicationSetsInputListReplicationSetsPaginateTypeDef",
    "ListResponsePlansInputListResponsePlansPaginateTypeDef",
    "GetResourcePoliciesOutputTypeDef",
    "GetTimelineEventOutputTypeDef",
    "IncidentRecordSummaryTypeDef",
    "IncidentRecordTypeDef",
    "IncidentTemplateTypeDef",
    "UpdateIncidentRecordInputRequestTypeDef",
    "ItemIdentifierTypeDef",
    "ListResponsePlansOutputTypeDef",
    "ReplicationSetTypeDef",
    "FilterTypeDef",
    "UpdateReplicationSetInputRequestTypeDef",
    "ActionTypeDef",
    "ListIncidentRecordsOutputTypeDef",
    "GetIncidentRecordOutputTypeDef",
    "RelatedItemTypeDef",
    "GetReplicationSetOutputTypeDef",
    "ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef",
    "ListIncidentRecordsInputRequestTypeDef",
    "ListTimelineEventsInputListTimelineEventsPaginateTypeDef",
    "ListTimelineEventsInputRequestTypeDef",
    "CreateResponsePlanInputRequestTypeDef",
    "GetResponsePlanOutputTypeDef",
    "UpdateResponsePlanInputRequestTypeDef",
    "ListRelatedItemsOutputTypeDef",
    "RelatedItemsUpdateTypeDef",
    "StartIncidentInputRequestTypeDef",
    "UpdateRelatedItemsInputRequestTypeDef",
)

_RequiredAddRegionActionTypeDef = TypedDict(
    "_RequiredAddRegionActionTypeDef",
    {
        "regionName": str,
    },
)
_OptionalAddRegionActionTypeDef = TypedDict(
    "_OptionalAddRegionActionTypeDef",
    {
        "sseKmsKeyId": str,
    },
    total=False,
)


class AddRegionActionTypeDef(_RequiredAddRegionActionTypeDef, _OptionalAddRegionActionTypeDef):
    pass


AttributeValueListTypeDef = TypedDict(
    "AttributeValueListTypeDef",
    {
        "integerValues": Sequence[int],
        "stringValues": Sequence[str],
    },
    total=False,
)

AutomationExecutionTypeDef = TypedDict(
    "AutomationExecutionTypeDef",
    {
        "ssmExecutionArn": str,
    },
    total=False,
)

ChatChannelTypeDef = TypedDict(
    "ChatChannelTypeDef",
    {
        "chatbotSns": Sequence[str],
        "empty": Mapping[str, Any],
    },
    total=False,
)

RegionMapInputValueTypeDef = TypedDict(
    "RegionMapInputValueTypeDef",
    {
        "sseKmsKeyId": str,
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

_RequiredCreateTimelineEventInputRequestTypeDef = TypedDict(
    "_RequiredCreateTimelineEventInputRequestTypeDef",
    {
        "eventData": str,
        "eventTime": Union[datetime, str],
        "eventType": str,
        "incidentRecordArn": str,
    },
)
_OptionalCreateTimelineEventInputRequestTypeDef = TypedDict(
    "_OptionalCreateTimelineEventInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateTimelineEventInputRequestTypeDef(
    _RequiredCreateTimelineEventInputRequestTypeDef, _OptionalCreateTimelineEventInputRequestTypeDef
):
    pass


DeleteIncidentRecordInputRequestTypeDef = TypedDict(
    "DeleteIncidentRecordInputRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteRegionActionTypeDef = TypedDict(
    "DeleteRegionActionTypeDef",
    {
        "regionName": str,
    },
)

DeleteReplicationSetInputRequestTypeDef = TypedDict(
    "DeleteReplicationSetInputRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteResourcePolicyInputRequestTypeDef = TypedDict(
    "DeleteResourcePolicyInputRequestTypeDef",
    {
        "policyId": str,
        "resourceArn": str,
    },
)

DeleteResponsePlanInputRequestTypeDef = TypedDict(
    "DeleteResponsePlanInputRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteTimelineEventInputRequestTypeDef = TypedDict(
    "DeleteTimelineEventInputRequestTypeDef",
    {
        "eventId": str,
        "incidentRecordArn": str,
    },
)

DynamicSsmParameterValueTypeDef = TypedDict(
    "DynamicSsmParameterValueTypeDef",
    {
        "variable": VariableTypeType,
    },
    total=False,
)

EventSummaryTypeDef = TypedDict(
    "EventSummaryTypeDef",
    {
        "eventId": str,
        "eventTime": datetime,
        "eventType": str,
        "eventUpdatedTime": datetime,
        "incidentRecordArn": str,
    },
)

GetIncidentRecordInputRequestTypeDef = TypedDict(
    "GetIncidentRecordInputRequestTypeDef",
    {
        "arn": str,
    },
)

GetReplicationSetInputRequestTypeDef = TypedDict(
    "GetReplicationSetInputRequestTypeDef",
    {
        "arn": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
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

_RequiredGetResourcePoliciesInputRequestTypeDef = TypedDict(
    "_RequiredGetResourcePoliciesInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalGetResourcePoliciesInputRequestTypeDef = TypedDict(
    "_OptionalGetResourcePoliciesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class GetResourcePoliciesInputRequestTypeDef(
    _RequiredGetResourcePoliciesInputRequestTypeDef, _OptionalGetResourcePoliciesInputRequestTypeDef
):
    pass


ResourcePolicyTypeDef = TypedDict(
    "ResourcePolicyTypeDef",
    {
        "policyDocument": str,
        "policyId": str,
        "ramResourceShareRegion": str,
    },
)

GetResponsePlanInputRequestTypeDef = TypedDict(
    "GetResponsePlanInputRequestTypeDef",
    {
        "arn": str,
    },
)

GetTimelineEventInputRequestTypeDef = TypedDict(
    "GetTimelineEventInputRequestTypeDef",
    {
        "eventId": str,
        "incidentRecordArn": str,
    },
)

TimelineEventTypeDef = TypedDict(
    "TimelineEventTypeDef",
    {
        "eventData": str,
        "eventId": str,
        "eventTime": datetime,
        "eventType": str,
        "eventUpdatedTime": datetime,
        "incidentRecordArn": str,
    },
)

_RequiredIncidentRecordSourceTypeDef = TypedDict(
    "_RequiredIncidentRecordSourceTypeDef",
    {
        "createdBy": str,
        "source": str,
    },
)
_OptionalIncidentRecordSourceTypeDef = TypedDict(
    "_OptionalIncidentRecordSourceTypeDef",
    {
        "invokedBy": str,
        "resourceArn": str,
    },
    total=False,
)


class IncidentRecordSourceTypeDef(
    _RequiredIncidentRecordSourceTypeDef, _OptionalIncidentRecordSourceTypeDef
):
    pass


NotificationTargetItemTypeDef = TypedDict(
    "NotificationTargetItemTypeDef",
    {
        "snsTopicArn": str,
    },
    total=False,
)

ItemValueTypeDef = TypedDict(
    "ItemValueTypeDef",
    {
        "arn": str,
        "metricDefinition": str,
        "url": str,
    },
    total=False,
)

_RequiredListRelatedItemsInputRequestTypeDef = TypedDict(
    "_RequiredListRelatedItemsInputRequestTypeDef",
    {
        "incidentRecordArn": str,
    },
)
_OptionalListRelatedItemsInputRequestTypeDef = TypedDict(
    "_OptionalListRelatedItemsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListRelatedItemsInputRequestTypeDef(
    _RequiredListRelatedItemsInputRequestTypeDef, _OptionalListRelatedItemsInputRequestTypeDef
):
    pass


ListReplicationSetsInputRequestTypeDef = TypedDict(
    "ListReplicationSetsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListResponsePlansInputRequestTypeDef = TypedDict(
    "ListResponsePlansInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredResponsePlanSummaryTypeDef = TypedDict(
    "_RequiredResponsePlanSummaryTypeDef",
    {
        "arn": str,
        "name": str,
    },
)
_OptionalResponsePlanSummaryTypeDef = TypedDict(
    "_OptionalResponsePlanSummaryTypeDef",
    {
        "displayName": str,
    },
    total=False,
)


class ResponsePlanSummaryTypeDef(
    _RequiredResponsePlanSummaryTypeDef, _OptionalResponsePlanSummaryTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

PutResourcePolicyInputRequestTypeDef = TypedDict(
    "PutResourcePolicyInputRequestTypeDef",
    {
        "policy": str,
        "resourceArn": str,
    },
)

_RequiredRegionInfoTypeDef = TypedDict(
    "_RequiredRegionInfoTypeDef",
    {
        "status": RegionStatusType,
        "statusUpdateDateTime": datetime,
    },
)
_OptionalRegionInfoTypeDef = TypedDict(
    "_OptionalRegionInfoTypeDef",
    {
        "sseKmsKeyId": str,
        "statusMessage": str,
    },
    total=False,
)


class RegionInfoTypeDef(_RequiredRegionInfoTypeDef, _OptionalRegionInfoTypeDef):
    pass


_RequiredTriggerDetailsTypeDef = TypedDict(
    "_RequiredTriggerDetailsTypeDef",
    {
        "source": str,
        "timestamp": Union[datetime, str],
    },
)
_OptionalTriggerDetailsTypeDef = TypedDict(
    "_OptionalTriggerDetailsTypeDef",
    {
        "rawData": str,
        "triggerArn": str,
    },
    total=False,
)


class TriggerDetailsTypeDef(_RequiredTriggerDetailsTypeDef, _OptionalTriggerDetailsTypeDef):
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

_RequiredUpdateDeletionProtectionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateDeletionProtectionInputRequestTypeDef",
    {
        "arn": str,
        "deletionProtected": bool,
    },
)
_OptionalUpdateDeletionProtectionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateDeletionProtectionInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateDeletionProtectionInputRequestTypeDef(
    _RequiredUpdateDeletionProtectionInputRequestTypeDef,
    _OptionalUpdateDeletionProtectionInputRequestTypeDef,
):
    pass


_RequiredUpdateTimelineEventInputRequestTypeDef = TypedDict(
    "_RequiredUpdateTimelineEventInputRequestTypeDef",
    {
        "eventId": str,
        "incidentRecordArn": str,
    },
)
_OptionalUpdateTimelineEventInputRequestTypeDef = TypedDict(
    "_OptionalUpdateTimelineEventInputRequestTypeDef",
    {
        "clientToken": str,
        "eventData": str,
        "eventTime": Union[datetime, str],
        "eventType": str,
    },
    total=False,
)


class UpdateTimelineEventInputRequestTypeDef(
    _RequiredUpdateTimelineEventInputRequestTypeDef, _OptionalUpdateTimelineEventInputRequestTypeDef
):
    pass


ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "after": Union[datetime, str],
        "before": Union[datetime, str],
        "equals": AttributeValueListTypeDef,
    },
    total=False,
)

_RequiredCreateReplicationSetInputRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationSetInputRequestTypeDef",
    {
        "regions": Mapping[str, RegionMapInputValueTypeDef],
    },
)
_OptionalCreateReplicationSetInputRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationSetInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateReplicationSetInputRequestTypeDef(
    _RequiredCreateReplicationSetInputRequestTypeDef,
    _OptionalCreateReplicationSetInputRequestTypeDef,
):
    pass


CreateReplicationSetOutputTypeDef = TypedDict(
    "CreateReplicationSetOutputTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResponsePlanOutputTypeDef = TypedDict(
    "CreateResponsePlanOutputTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTimelineEventOutputTypeDef = TypedDict(
    "CreateTimelineEventOutputTypeDef",
    {
        "eventId": str,
        "incidentRecordArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReplicationSetsOutputTypeDef = TypedDict(
    "ListReplicationSetsOutputTypeDef",
    {
        "nextToken": str,
        "replicationSetArns": List[str],
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

PutResourcePolicyOutputTypeDef = TypedDict(
    "PutResourcePolicyOutputTypeDef",
    {
        "policyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartIncidentOutputTypeDef = TypedDict(
    "StartIncidentOutputTypeDef",
    {
        "incidentRecordArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateReplicationSetActionTypeDef = TypedDict(
    "UpdateReplicationSetActionTypeDef",
    {
        "addRegionAction": AddRegionActionTypeDef,
        "deleteRegionAction": DeleteRegionActionTypeDef,
    },
    total=False,
)

_RequiredSsmAutomationTypeDef = TypedDict(
    "_RequiredSsmAutomationTypeDef",
    {
        "documentName": str,
        "roleArn": str,
    },
)
_OptionalSsmAutomationTypeDef = TypedDict(
    "_OptionalSsmAutomationTypeDef",
    {
        "documentVersion": str,
        "dynamicParameters": Mapping[str, DynamicSsmParameterValueTypeDef],
        "parameters": Mapping[str, Sequence[str]],
        "targetAccount": SsmTargetAccountType,
    },
    total=False,
)


class SsmAutomationTypeDef(_RequiredSsmAutomationTypeDef, _OptionalSsmAutomationTypeDef):
    pass


ListTimelineEventsOutputTypeDef = TypedDict(
    "ListTimelineEventsOutputTypeDef",
    {
        "eventSummaries": List[EventSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef = TypedDict(
    "_RequiredGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef",
    {
        "arn": str,
    },
)
_OptionalGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef = TypedDict(
    "_OptionalGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef(
    _RequiredGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef,
    _OptionalGetReplicationSetInputWaitForReplicationSetActiveWaitTypeDef,
):
    pass


_RequiredGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef = TypedDict(
    "_RequiredGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef",
    {
        "arn": str,
    },
)
_OptionalGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef = TypedDict(
    "_OptionalGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef(
    _RequiredGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef,
    _OptionalGetReplicationSetInputWaitForReplicationSetDeletedWaitTypeDef,
):
    pass


_RequiredGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef = TypedDict(
    "_RequiredGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef = TypedDict(
    "_OptionalGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef(
    _RequiredGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef,
    _OptionalGetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef,
):
    pass


_RequiredListRelatedItemsInputListRelatedItemsPaginateTypeDef = TypedDict(
    "_RequiredListRelatedItemsInputListRelatedItemsPaginateTypeDef",
    {
        "incidentRecordArn": str,
    },
)
_OptionalListRelatedItemsInputListRelatedItemsPaginateTypeDef = TypedDict(
    "_OptionalListRelatedItemsInputListRelatedItemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRelatedItemsInputListRelatedItemsPaginateTypeDef(
    _RequiredListRelatedItemsInputListRelatedItemsPaginateTypeDef,
    _OptionalListRelatedItemsInputListRelatedItemsPaginateTypeDef,
):
    pass


ListReplicationSetsInputListReplicationSetsPaginateTypeDef = TypedDict(
    "ListReplicationSetsInputListReplicationSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResponsePlansInputListResponsePlansPaginateTypeDef = TypedDict(
    "ListResponsePlansInputListResponsePlansPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetResourcePoliciesOutputTypeDef = TypedDict(
    "GetResourcePoliciesOutputTypeDef",
    {
        "nextToken": str,
        "resourcePolicies": List[ResourcePolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTimelineEventOutputTypeDef = TypedDict(
    "GetTimelineEventOutputTypeDef",
    {
        "event": TimelineEventTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredIncidentRecordSummaryTypeDef = TypedDict(
    "_RequiredIncidentRecordSummaryTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "impact": int,
        "incidentRecordSource": IncidentRecordSourceTypeDef,
        "status": IncidentRecordStatusType,
        "title": str,
    },
)
_OptionalIncidentRecordSummaryTypeDef = TypedDict(
    "_OptionalIncidentRecordSummaryTypeDef",
    {
        "resolvedTime": datetime,
    },
    total=False,
)


class IncidentRecordSummaryTypeDef(
    _RequiredIncidentRecordSummaryTypeDef, _OptionalIncidentRecordSummaryTypeDef
):
    pass


_RequiredIncidentRecordTypeDef = TypedDict(
    "_RequiredIncidentRecordTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "dedupeString": str,
        "impact": int,
        "incidentRecordSource": IncidentRecordSourceTypeDef,
        "lastModifiedBy": str,
        "lastModifiedTime": datetime,
        "status": IncidentRecordStatusType,
        "title": str,
    },
)
_OptionalIncidentRecordTypeDef = TypedDict(
    "_OptionalIncidentRecordTypeDef",
    {
        "automationExecutions": List[AutomationExecutionTypeDef],
        "chatChannel": ChatChannelTypeDef,
        "notificationTargets": List[NotificationTargetItemTypeDef],
        "resolvedTime": datetime,
        "summary": str,
    },
    total=False,
)


class IncidentRecordTypeDef(_RequiredIncidentRecordTypeDef, _OptionalIncidentRecordTypeDef):
    pass


_RequiredIncidentTemplateTypeDef = TypedDict(
    "_RequiredIncidentTemplateTypeDef",
    {
        "impact": int,
        "title": str,
    },
)
_OptionalIncidentTemplateTypeDef = TypedDict(
    "_OptionalIncidentTemplateTypeDef",
    {
        "dedupeString": str,
        "notificationTargets": Sequence[NotificationTargetItemTypeDef],
        "summary": str,
    },
    total=False,
)


class IncidentTemplateTypeDef(_RequiredIncidentTemplateTypeDef, _OptionalIncidentTemplateTypeDef):
    pass


_RequiredUpdateIncidentRecordInputRequestTypeDef = TypedDict(
    "_RequiredUpdateIncidentRecordInputRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateIncidentRecordInputRequestTypeDef = TypedDict(
    "_OptionalUpdateIncidentRecordInputRequestTypeDef",
    {
        "chatChannel": ChatChannelTypeDef,
        "clientToken": str,
        "impact": int,
        "notificationTargets": Sequence[NotificationTargetItemTypeDef],
        "status": IncidentRecordStatusType,
        "summary": str,
        "title": str,
    },
    total=False,
)


class UpdateIncidentRecordInputRequestTypeDef(
    _RequiredUpdateIncidentRecordInputRequestTypeDef,
    _OptionalUpdateIncidentRecordInputRequestTypeDef,
):
    pass


ItemIdentifierTypeDef = TypedDict(
    "ItemIdentifierTypeDef",
    {
        "type": ItemTypeType,
        "value": ItemValueTypeDef,
    },
)

ListResponsePlansOutputTypeDef = TypedDict(
    "ListResponsePlansOutputTypeDef",
    {
        "nextToken": str,
        "responsePlanSummaries": List[ResponsePlanSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredReplicationSetTypeDef = TypedDict(
    "_RequiredReplicationSetTypeDef",
    {
        "createdBy": str,
        "createdTime": datetime,
        "deletionProtected": bool,
        "lastModifiedBy": str,
        "lastModifiedTime": datetime,
        "regionMap": Dict[str, RegionInfoTypeDef],
        "status": ReplicationSetStatusType,
    },
)
_OptionalReplicationSetTypeDef = TypedDict(
    "_OptionalReplicationSetTypeDef",
    {
        "arn": str,
    },
    total=False,
)


class ReplicationSetTypeDef(_RequiredReplicationSetTypeDef, _OptionalReplicationSetTypeDef):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "condition": ConditionTypeDef,
        "key": str,
    },
)

_RequiredUpdateReplicationSetInputRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationSetInputRequestTypeDef",
    {
        "actions": Sequence[UpdateReplicationSetActionTypeDef],
        "arn": str,
    },
)
_OptionalUpdateReplicationSetInputRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationSetInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateReplicationSetInputRequestTypeDef(
    _RequiredUpdateReplicationSetInputRequestTypeDef,
    _OptionalUpdateReplicationSetInputRequestTypeDef,
):
    pass


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ssmAutomation": SsmAutomationTypeDef,
    },
    total=False,
)

ListIncidentRecordsOutputTypeDef = TypedDict(
    "ListIncidentRecordsOutputTypeDef",
    {
        "incidentRecordSummaries": List[IncidentRecordSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIncidentRecordOutputTypeDef = TypedDict(
    "GetIncidentRecordOutputTypeDef",
    {
        "incidentRecord": IncidentRecordTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRelatedItemTypeDef = TypedDict(
    "_RequiredRelatedItemTypeDef",
    {
        "identifier": ItemIdentifierTypeDef,
    },
)
_OptionalRelatedItemTypeDef = TypedDict(
    "_OptionalRelatedItemTypeDef",
    {
        "title": str,
    },
    total=False,
)


class RelatedItemTypeDef(_RequiredRelatedItemTypeDef, _OptionalRelatedItemTypeDef):
    pass


GetReplicationSetOutputTypeDef = TypedDict(
    "GetReplicationSetOutputTypeDef",
    {
        "replicationSet": ReplicationSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef = TypedDict(
    "ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListIncidentRecordsInputRequestTypeDef = TypedDict(
    "ListIncidentRecordsInputRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListTimelineEventsInputListTimelineEventsPaginateTypeDef = TypedDict(
    "_RequiredListTimelineEventsInputListTimelineEventsPaginateTypeDef",
    {
        "incidentRecordArn": str,
    },
)
_OptionalListTimelineEventsInputListTimelineEventsPaginateTypeDef = TypedDict(
    "_OptionalListTimelineEventsInputListTimelineEventsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "sortBy": Literal["EVENT_TIME"],
        "sortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTimelineEventsInputListTimelineEventsPaginateTypeDef(
    _RequiredListTimelineEventsInputListTimelineEventsPaginateTypeDef,
    _OptionalListTimelineEventsInputListTimelineEventsPaginateTypeDef,
):
    pass


_RequiredListTimelineEventsInputRequestTypeDef = TypedDict(
    "_RequiredListTimelineEventsInputRequestTypeDef",
    {
        "incidentRecordArn": str,
    },
)
_OptionalListTimelineEventsInputRequestTypeDef = TypedDict(
    "_OptionalListTimelineEventsInputRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
        "sortBy": Literal["EVENT_TIME"],
        "sortOrder": SortOrderType,
    },
    total=False,
)


class ListTimelineEventsInputRequestTypeDef(
    _RequiredListTimelineEventsInputRequestTypeDef, _OptionalListTimelineEventsInputRequestTypeDef
):
    pass


_RequiredCreateResponsePlanInputRequestTypeDef = TypedDict(
    "_RequiredCreateResponsePlanInputRequestTypeDef",
    {
        "incidentTemplate": IncidentTemplateTypeDef,
        "name": str,
    },
)
_OptionalCreateResponsePlanInputRequestTypeDef = TypedDict(
    "_OptionalCreateResponsePlanInputRequestTypeDef",
    {
        "actions": Sequence[ActionTypeDef],
        "chatChannel": ChatChannelTypeDef,
        "clientToken": str,
        "displayName": str,
        "engagements": Sequence[str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateResponsePlanInputRequestTypeDef(
    _RequiredCreateResponsePlanInputRequestTypeDef, _OptionalCreateResponsePlanInputRequestTypeDef
):
    pass


GetResponsePlanOutputTypeDef = TypedDict(
    "GetResponsePlanOutputTypeDef",
    {
        "actions": List[ActionTypeDef],
        "arn": str,
        "chatChannel": ChatChannelTypeDef,
        "displayName": str,
        "engagements": List[str],
        "incidentTemplate": IncidentTemplateTypeDef,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateResponsePlanInputRequestTypeDef = TypedDict(
    "_RequiredUpdateResponsePlanInputRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateResponsePlanInputRequestTypeDef = TypedDict(
    "_OptionalUpdateResponsePlanInputRequestTypeDef",
    {
        "actions": Sequence[ActionTypeDef],
        "chatChannel": ChatChannelTypeDef,
        "clientToken": str,
        "displayName": str,
        "engagements": Sequence[str],
        "incidentTemplateDedupeString": str,
        "incidentTemplateImpact": int,
        "incidentTemplateNotificationTargets": Sequence[NotificationTargetItemTypeDef],
        "incidentTemplateSummary": str,
        "incidentTemplateTitle": str,
    },
    total=False,
)


class UpdateResponsePlanInputRequestTypeDef(
    _RequiredUpdateResponsePlanInputRequestTypeDef, _OptionalUpdateResponsePlanInputRequestTypeDef
):
    pass


ListRelatedItemsOutputTypeDef = TypedDict(
    "ListRelatedItemsOutputTypeDef",
    {
        "nextToken": str,
        "relatedItems": List[RelatedItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RelatedItemsUpdateTypeDef = TypedDict(
    "RelatedItemsUpdateTypeDef",
    {
        "itemToAdd": RelatedItemTypeDef,
        "itemToRemove": ItemIdentifierTypeDef,
    },
    total=False,
)

_RequiredStartIncidentInputRequestTypeDef = TypedDict(
    "_RequiredStartIncidentInputRequestTypeDef",
    {
        "responsePlanArn": str,
    },
)
_OptionalStartIncidentInputRequestTypeDef = TypedDict(
    "_OptionalStartIncidentInputRequestTypeDef",
    {
        "clientToken": str,
        "impact": int,
        "relatedItems": Sequence[RelatedItemTypeDef],
        "title": str,
        "triggerDetails": TriggerDetailsTypeDef,
    },
    total=False,
)


class StartIncidentInputRequestTypeDef(
    _RequiredStartIncidentInputRequestTypeDef, _OptionalStartIncidentInputRequestTypeDef
):
    pass


_RequiredUpdateRelatedItemsInputRequestTypeDef = TypedDict(
    "_RequiredUpdateRelatedItemsInputRequestTypeDef",
    {
        "incidentRecordArn": str,
        "relatedItemsUpdate": RelatedItemsUpdateTypeDef,
    },
)
_OptionalUpdateRelatedItemsInputRequestTypeDef = TypedDict(
    "_OptionalUpdateRelatedItemsInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateRelatedItemsInputRequestTypeDef(
    _RequiredUpdateRelatedItemsInputRequestTypeDef, _OptionalUpdateRelatedItemsInputRequestTypeDef
):
    pass
