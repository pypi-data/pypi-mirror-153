"""
Type annotations for iotevents-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotevents_data.type_defs import AcknowledgeActionConfigurationTypeDef

    data: AcknowledgeActionConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlarmStateNameType,
    ComparisonOperatorType,
    CustomerActionNameType,
    ErrorCodeType,
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
    "AcknowledgeActionConfigurationTypeDef",
    "AcknowledgeAlarmActionRequestTypeDef",
    "AlarmSummaryTypeDef",
    "BatchAlarmActionErrorEntryTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteDetectorErrorEntryTypeDef",
    "DeleteDetectorRequestTypeDef",
    "DisableAlarmActionRequestTypeDef",
    "EnableAlarmActionRequestTypeDef",
    "BatchPutMessageErrorEntryTypeDef",
    "ResetAlarmActionRequestTypeDef",
    "SnoozeAlarmActionRequestTypeDef",
    "BatchUpdateDetectorErrorEntryTypeDef",
    "DisableActionConfigurationTypeDef",
    "EnableActionConfigurationTypeDef",
    "ResetActionConfigurationTypeDef",
    "SnoozeActionConfigurationTypeDef",
    "DescribeAlarmRequestRequestTypeDef",
    "DescribeDetectorRequestRequestTypeDef",
    "TimerDefinitionTypeDef",
    "VariableDefinitionTypeDef",
    "DetectorStateSummaryTypeDef",
    "TimerTypeDef",
    "VariableTypeDef",
    "ListAlarmsRequestRequestTypeDef",
    "ListDetectorsRequestRequestTypeDef",
    "TimestampValueTypeDef",
    "SimpleRuleEvaluationTypeDef",
    "StateChangeConfigurationTypeDef",
    "BatchAcknowledgeAlarmRequestRequestTypeDef",
    "BatchAcknowledgeAlarmResponseTypeDef",
    "BatchDisableAlarmResponseTypeDef",
    "BatchEnableAlarmResponseTypeDef",
    "BatchResetAlarmResponseTypeDef",
    "BatchSnoozeAlarmResponseTypeDef",
    "ListAlarmsResponseTypeDef",
    "BatchDeleteDetectorResponseTypeDef",
    "BatchDeleteDetectorRequestRequestTypeDef",
    "BatchDisableAlarmRequestRequestTypeDef",
    "BatchEnableAlarmRequestRequestTypeDef",
    "BatchPutMessageResponseTypeDef",
    "BatchResetAlarmRequestRequestTypeDef",
    "BatchSnoozeAlarmRequestRequestTypeDef",
    "BatchUpdateDetectorResponseTypeDef",
    "CustomerActionTypeDef",
    "DetectorStateDefinitionTypeDef",
    "DetectorSummaryTypeDef",
    "DetectorStateTypeDef",
    "MessageTypeDef",
    "RuleEvaluationTypeDef",
    "SystemEventTypeDef",
    "UpdateDetectorRequestTypeDef",
    "ListDetectorsResponseTypeDef",
    "DetectorTypeDef",
    "BatchPutMessageRequestRequestTypeDef",
    "AlarmStateTypeDef",
    "BatchUpdateDetectorRequestRequestTypeDef",
    "DescribeDetectorResponseTypeDef",
    "AlarmTypeDef",
    "DescribeAlarmResponseTypeDef",
)

AcknowledgeActionConfigurationTypeDef = TypedDict(
    "AcknowledgeActionConfigurationTypeDef",
    {
        "note": str,
    },
    total=False,
)

_RequiredAcknowledgeAlarmActionRequestTypeDef = TypedDict(
    "_RequiredAcknowledgeAlarmActionRequestTypeDef",
    {
        "requestId": str,
        "alarmModelName": str,
    },
)
_OptionalAcknowledgeAlarmActionRequestTypeDef = TypedDict(
    "_OptionalAcknowledgeAlarmActionRequestTypeDef",
    {
        "keyValue": str,
        "note": str,
    },
    total=False,
)


class AcknowledgeAlarmActionRequestTypeDef(
    _RequiredAcknowledgeAlarmActionRequestTypeDef, _OptionalAcknowledgeAlarmActionRequestTypeDef
):
    pass


AlarmSummaryTypeDef = TypedDict(
    "AlarmSummaryTypeDef",
    {
        "alarmModelName": str,
        "alarmModelVersion": str,
        "keyValue": str,
        "stateName": AlarmStateNameType,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

BatchAlarmActionErrorEntryTypeDef = TypedDict(
    "BatchAlarmActionErrorEntryTypeDef",
    {
        "requestId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
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

BatchDeleteDetectorErrorEntryTypeDef = TypedDict(
    "BatchDeleteDetectorErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
    total=False,
)

_RequiredDeleteDetectorRequestTypeDef = TypedDict(
    "_RequiredDeleteDetectorRequestTypeDef",
    {
        "messageId": str,
        "detectorModelName": str,
    },
)
_OptionalDeleteDetectorRequestTypeDef = TypedDict(
    "_OptionalDeleteDetectorRequestTypeDef",
    {
        "keyValue": str,
    },
    total=False,
)


class DeleteDetectorRequestTypeDef(
    _RequiredDeleteDetectorRequestTypeDef, _OptionalDeleteDetectorRequestTypeDef
):
    pass


_RequiredDisableAlarmActionRequestTypeDef = TypedDict(
    "_RequiredDisableAlarmActionRequestTypeDef",
    {
        "requestId": str,
        "alarmModelName": str,
    },
)
_OptionalDisableAlarmActionRequestTypeDef = TypedDict(
    "_OptionalDisableAlarmActionRequestTypeDef",
    {
        "keyValue": str,
        "note": str,
    },
    total=False,
)


class DisableAlarmActionRequestTypeDef(
    _RequiredDisableAlarmActionRequestTypeDef, _OptionalDisableAlarmActionRequestTypeDef
):
    pass


_RequiredEnableAlarmActionRequestTypeDef = TypedDict(
    "_RequiredEnableAlarmActionRequestTypeDef",
    {
        "requestId": str,
        "alarmModelName": str,
    },
)
_OptionalEnableAlarmActionRequestTypeDef = TypedDict(
    "_OptionalEnableAlarmActionRequestTypeDef",
    {
        "keyValue": str,
        "note": str,
    },
    total=False,
)


class EnableAlarmActionRequestTypeDef(
    _RequiredEnableAlarmActionRequestTypeDef, _OptionalEnableAlarmActionRequestTypeDef
):
    pass


BatchPutMessageErrorEntryTypeDef = TypedDict(
    "BatchPutMessageErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
    total=False,
)

_RequiredResetAlarmActionRequestTypeDef = TypedDict(
    "_RequiredResetAlarmActionRequestTypeDef",
    {
        "requestId": str,
        "alarmModelName": str,
    },
)
_OptionalResetAlarmActionRequestTypeDef = TypedDict(
    "_OptionalResetAlarmActionRequestTypeDef",
    {
        "keyValue": str,
        "note": str,
    },
    total=False,
)


class ResetAlarmActionRequestTypeDef(
    _RequiredResetAlarmActionRequestTypeDef, _OptionalResetAlarmActionRequestTypeDef
):
    pass


_RequiredSnoozeAlarmActionRequestTypeDef = TypedDict(
    "_RequiredSnoozeAlarmActionRequestTypeDef",
    {
        "requestId": str,
        "alarmModelName": str,
        "snoozeDuration": int,
    },
)
_OptionalSnoozeAlarmActionRequestTypeDef = TypedDict(
    "_OptionalSnoozeAlarmActionRequestTypeDef",
    {
        "keyValue": str,
        "note": str,
    },
    total=False,
)


class SnoozeAlarmActionRequestTypeDef(
    _RequiredSnoozeAlarmActionRequestTypeDef, _OptionalSnoozeAlarmActionRequestTypeDef
):
    pass


BatchUpdateDetectorErrorEntryTypeDef = TypedDict(
    "BatchUpdateDetectorErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
    total=False,
)

DisableActionConfigurationTypeDef = TypedDict(
    "DisableActionConfigurationTypeDef",
    {
        "note": str,
    },
    total=False,
)

EnableActionConfigurationTypeDef = TypedDict(
    "EnableActionConfigurationTypeDef",
    {
        "note": str,
    },
    total=False,
)

ResetActionConfigurationTypeDef = TypedDict(
    "ResetActionConfigurationTypeDef",
    {
        "note": str,
    },
    total=False,
)

SnoozeActionConfigurationTypeDef = TypedDict(
    "SnoozeActionConfigurationTypeDef",
    {
        "snoozeDuration": int,
        "note": str,
    },
    total=False,
)

_RequiredDescribeAlarmRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAlarmRequestRequestTypeDef",
    {
        "alarmModelName": str,
    },
)
_OptionalDescribeAlarmRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAlarmRequestRequestTypeDef",
    {
        "keyValue": str,
    },
    total=False,
)


class DescribeAlarmRequestRequestTypeDef(
    _RequiredDescribeAlarmRequestRequestTypeDef, _OptionalDescribeAlarmRequestRequestTypeDef
):
    pass


_RequiredDescribeDetectorRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDetectorRequestRequestTypeDef",
    {
        "detectorModelName": str,
    },
)
_OptionalDescribeDetectorRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDetectorRequestRequestTypeDef",
    {
        "keyValue": str,
    },
    total=False,
)


class DescribeDetectorRequestRequestTypeDef(
    _RequiredDescribeDetectorRequestRequestTypeDef, _OptionalDescribeDetectorRequestRequestTypeDef
):
    pass


TimerDefinitionTypeDef = TypedDict(
    "TimerDefinitionTypeDef",
    {
        "name": str,
        "seconds": int,
    },
)

VariableDefinitionTypeDef = TypedDict(
    "VariableDefinitionTypeDef",
    {
        "name": str,
        "value": str,
    },
)

DetectorStateSummaryTypeDef = TypedDict(
    "DetectorStateSummaryTypeDef",
    {
        "stateName": str,
    },
    total=False,
)

TimerTypeDef = TypedDict(
    "TimerTypeDef",
    {
        "name": str,
        "timestamp": datetime,
    },
)

VariableTypeDef = TypedDict(
    "VariableTypeDef",
    {
        "name": str,
        "value": str,
    },
)

_RequiredListAlarmsRequestRequestTypeDef = TypedDict(
    "_RequiredListAlarmsRequestRequestTypeDef",
    {
        "alarmModelName": str,
    },
)
_OptionalListAlarmsRequestRequestTypeDef = TypedDict(
    "_OptionalListAlarmsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAlarmsRequestRequestTypeDef(
    _RequiredListAlarmsRequestRequestTypeDef, _OptionalListAlarmsRequestRequestTypeDef
):
    pass


_RequiredListDetectorsRequestRequestTypeDef = TypedDict(
    "_RequiredListDetectorsRequestRequestTypeDef",
    {
        "detectorModelName": str,
    },
)
_OptionalListDetectorsRequestRequestTypeDef = TypedDict(
    "_OptionalListDetectorsRequestRequestTypeDef",
    {
        "stateName": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDetectorsRequestRequestTypeDef(
    _RequiredListDetectorsRequestRequestTypeDef, _OptionalListDetectorsRequestRequestTypeDef
):
    pass


TimestampValueTypeDef = TypedDict(
    "TimestampValueTypeDef",
    {
        "timeInMillis": int,
    },
    total=False,
)

SimpleRuleEvaluationTypeDef = TypedDict(
    "SimpleRuleEvaluationTypeDef",
    {
        "inputPropertyValue": str,
        "operator": ComparisonOperatorType,
        "thresholdValue": str,
    },
    total=False,
)

StateChangeConfigurationTypeDef = TypedDict(
    "StateChangeConfigurationTypeDef",
    {
        "triggerType": Literal["SNOOZE_TIMEOUT"],
    },
    total=False,
)

BatchAcknowledgeAlarmRequestRequestTypeDef = TypedDict(
    "BatchAcknowledgeAlarmRequestRequestTypeDef",
    {
        "acknowledgeActionRequests": Sequence[AcknowledgeAlarmActionRequestTypeDef],
    },
)

BatchAcknowledgeAlarmResponseTypeDef = TypedDict(
    "BatchAcknowledgeAlarmResponseTypeDef",
    {
        "errorEntries": List[BatchAlarmActionErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisableAlarmResponseTypeDef = TypedDict(
    "BatchDisableAlarmResponseTypeDef",
    {
        "errorEntries": List[BatchAlarmActionErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEnableAlarmResponseTypeDef = TypedDict(
    "BatchEnableAlarmResponseTypeDef",
    {
        "errorEntries": List[BatchAlarmActionErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchResetAlarmResponseTypeDef = TypedDict(
    "BatchResetAlarmResponseTypeDef",
    {
        "errorEntries": List[BatchAlarmActionErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchSnoozeAlarmResponseTypeDef = TypedDict(
    "BatchSnoozeAlarmResponseTypeDef",
    {
        "errorEntries": List[BatchAlarmActionErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAlarmsResponseTypeDef = TypedDict(
    "ListAlarmsResponseTypeDef",
    {
        "alarmSummaries": List[AlarmSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteDetectorResponseTypeDef = TypedDict(
    "BatchDeleteDetectorResponseTypeDef",
    {
        "batchDeleteDetectorErrorEntries": List[BatchDeleteDetectorErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteDetectorRequestRequestTypeDef = TypedDict(
    "BatchDeleteDetectorRequestRequestTypeDef",
    {
        "detectors": Sequence[DeleteDetectorRequestTypeDef],
    },
)

BatchDisableAlarmRequestRequestTypeDef = TypedDict(
    "BatchDisableAlarmRequestRequestTypeDef",
    {
        "disableActionRequests": Sequence[DisableAlarmActionRequestTypeDef],
    },
)

BatchEnableAlarmRequestRequestTypeDef = TypedDict(
    "BatchEnableAlarmRequestRequestTypeDef",
    {
        "enableActionRequests": Sequence[EnableAlarmActionRequestTypeDef],
    },
)

BatchPutMessageResponseTypeDef = TypedDict(
    "BatchPutMessageResponseTypeDef",
    {
        "BatchPutMessageErrorEntries": List[BatchPutMessageErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchResetAlarmRequestRequestTypeDef = TypedDict(
    "BatchResetAlarmRequestRequestTypeDef",
    {
        "resetActionRequests": Sequence[ResetAlarmActionRequestTypeDef],
    },
)

BatchSnoozeAlarmRequestRequestTypeDef = TypedDict(
    "BatchSnoozeAlarmRequestRequestTypeDef",
    {
        "snoozeActionRequests": Sequence[SnoozeAlarmActionRequestTypeDef],
    },
)

BatchUpdateDetectorResponseTypeDef = TypedDict(
    "BatchUpdateDetectorResponseTypeDef",
    {
        "batchUpdateDetectorErrorEntries": List[BatchUpdateDetectorErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomerActionTypeDef = TypedDict(
    "CustomerActionTypeDef",
    {
        "actionName": CustomerActionNameType,
        "snoozeActionConfiguration": SnoozeActionConfigurationTypeDef,
        "enableActionConfiguration": EnableActionConfigurationTypeDef,
        "disableActionConfiguration": DisableActionConfigurationTypeDef,
        "acknowledgeActionConfiguration": AcknowledgeActionConfigurationTypeDef,
        "resetActionConfiguration": ResetActionConfigurationTypeDef,
    },
    total=False,
)

DetectorStateDefinitionTypeDef = TypedDict(
    "DetectorStateDefinitionTypeDef",
    {
        "stateName": str,
        "variables": Sequence[VariableDefinitionTypeDef],
        "timers": Sequence[TimerDefinitionTypeDef],
    },
)

DetectorSummaryTypeDef = TypedDict(
    "DetectorSummaryTypeDef",
    {
        "detectorModelName": str,
        "keyValue": str,
        "detectorModelVersion": str,
        "state": DetectorStateSummaryTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

DetectorStateTypeDef = TypedDict(
    "DetectorStateTypeDef",
    {
        "stateName": str,
        "variables": List[VariableTypeDef],
        "timers": List[TimerTypeDef],
    },
)

_RequiredMessageTypeDef = TypedDict(
    "_RequiredMessageTypeDef",
    {
        "messageId": str,
        "inputName": str,
        "payload": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalMessageTypeDef = TypedDict(
    "_OptionalMessageTypeDef",
    {
        "timestamp": TimestampValueTypeDef,
    },
    total=False,
)


class MessageTypeDef(_RequiredMessageTypeDef, _OptionalMessageTypeDef):
    pass


RuleEvaluationTypeDef = TypedDict(
    "RuleEvaluationTypeDef",
    {
        "simpleRuleEvaluation": SimpleRuleEvaluationTypeDef,
    },
    total=False,
)

SystemEventTypeDef = TypedDict(
    "SystemEventTypeDef",
    {
        "eventType": Literal["STATE_CHANGE"],
        "stateChangeConfiguration": StateChangeConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateDetectorRequestTypeDef = TypedDict(
    "_RequiredUpdateDetectorRequestTypeDef",
    {
        "messageId": str,
        "detectorModelName": str,
        "state": DetectorStateDefinitionTypeDef,
    },
)
_OptionalUpdateDetectorRequestTypeDef = TypedDict(
    "_OptionalUpdateDetectorRequestTypeDef",
    {
        "keyValue": str,
    },
    total=False,
)


class UpdateDetectorRequestTypeDef(
    _RequiredUpdateDetectorRequestTypeDef, _OptionalUpdateDetectorRequestTypeDef
):
    pass


ListDetectorsResponseTypeDef = TypedDict(
    "ListDetectorsResponseTypeDef",
    {
        "detectorSummaries": List[DetectorSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectorTypeDef = TypedDict(
    "DetectorTypeDef",
    {
        "detectorModelName": str,
        "keyValue": str,
        "detectorModelVersion": str,
        "state": DetectorStateTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

BatchPutMessageRequestRequestTypeDef = TypedDict(
    "BatchPutMessageRequestRequestTypeDef",
    {
        "messages": Sequence[MessageTypeDef],
    },
)

AlarmStateTypeDef = TypedDict(
    "AlarmStateTypeDef",
    {
        "stateName": AlarmStateNameType,
        "ruleEvaluation": RuleEvaluationTypeDef,
        "customerAction": CustomerActionTypeDef,
        "systemEvent": SystemEventTypeDef,
    },
    total=False,
)

BatchUpdateDetectorRequestRequestTypeDef = TypedDict(
    "BatchUpdateDetectorRequestRequestTypeDef",
    {
        "detectors": Sequence[UpdateDetectorRequestTypeDef],
    },
)

DescribeDetectorResponseTypeDef = TypedDict(
    "DescribeDetectorResponseTypeDef",
    {
        "detector": DetectorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AlarmTypeDef = TypedDict(
    "AlarmTypeDef",
    {
        "alarmModelName": str,
        "alarmModelVersion": str,
        "keyValue": str,
        "alarmState": AlarmStateTypeDef,
        "severity": int,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

DescribeAlarmResponseTypeDef = TypedDict(
    "DescribeAlarmResponseTypeDef",
    {
        "alarm": AlarmTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
