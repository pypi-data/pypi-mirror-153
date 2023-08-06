"""
Type annotations for swf service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/type_defs/)

Usage::

    ```python
    from mypy_boto3_swf.type_defs import ActivityTaskCancelRequestedEventAttributesTypeDef

    data: ActivityTaskCancelRequestedEventAttributesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ActivityTaskTimeoutTypeType,
    CancelTimerFailedCauseType,
    CancelWorkflowExecutionFailedCauseType,
    ChildPolicyType,
    CloseStatusType,
    CompleteWorkflowExecutionFailedCauseType,
    ContinueAsNewWorkflowExecutionFailedCauseType,
    DecisionTypeType,
    EventTypeType,
    ExecutionStatusType,
    FailWorkflowExecutionFailedCauseType,
    RegistrationStatusType,
    RequestCancelActivityTaskFailedCauseType,
    RequestCancelExternalWorkflowExecutionFailedCauseType,
    ScheduleActivityTaskFailedCauseType,
    ScheduleLambdaFunctionFailedCauseType,
    SignalExternalWorkflowExecutionFailedCauseType,
    StartChildWorkflowExecutionFailedCauseType,
    StartTimerFailedCauseType,
    WorkflowExecutionTerminatedCauseType,
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
    "ActivityTaskCancelRequestedEventAttributesTypeDef",
    "ActivityTaskCanceledEventAttributesTypeDef",
    "ActivityTaskCompletedEventAttributesTypeDef",
    "ActivityTaskFailedEventAttributesTypeDef",
    "ActivityTypeTypeDef",
    "TaskListTypeDef",
    "ActivityTaskStartedEventAttributesTypeDef",
    "ResponseMetadataTypeDef",
    "ActivityTaskTimedOutEventAttributesTypeDef",
    "WorkflowExecutionTypeDef",
    "CancelTimerDecisionAttributesTypeDef",
    "CancelTimerFailedEventAttributesTypeDef",
    "CancelWorkflowExecutionDecisionAttributesTypeDef",
    "CancelWorkflowExecutionFailedEventAttributesTypeDef",
    "WorkflowTypeTypeDef",
    "CloseStatusFilterTypeDef",
    "CompleteWorkflowExecutionDecisionAttributesTypeDef",
    "CompleteWorkflowExecutionFailedEventAttributesTypeDef",
    "ContinueAsNewWorkflowExecutionFailedEventAttributesTypeDef",
    "ExecutionTimeFilterTypeDef",
    "TagFilterTypeDef",
    "WorkflowExecutionFilterTypeDef",
    "WorkflowTypeFilterTypeDef",
    "DecisionTaskCompletedEventAttributesTypeDef",
    "DecisionTaskStartedEventAttributesTypeDef",
    "DecisionTaskTimedOutEventAttributesTypeDef",
    "FailWorkflowExecutionDecisionAttributesTypeDef",
    "RecordMarkerDecisionAttributesTypeDef",
    "RequestCancelActivityTaskDecisionAttributesTypeDef",
    "RequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef",
    "ScheduleLambdaFunctionDecisionAttributesTypeDef",
    "SignalExternalWorkflowExecutionDecisionAttributesTypeDef",
    "StartTimerDecisionAttributesTypeDef",
    "DeprecateDomainInputRequestTypeDef",
    "DescribeDomainInputRequestTypeDef",
    "DomainConfigurationTypeDef",
    "DomainInfoTypeDef",
    "FailWorkflowExecutionFailedEventAttributesTypeDef",
    "PaginatorConfigTypeDef",
    "LambdaFunctionCompletedEventAttributesTypeDef",
    "LambdaFunctionFailedEventAttributesTypeDef",
    "LambdaFunctionScheduledEventAttributesTypeDef",
    "LambdaFunctionStartedEventAttributesTypeDef",
    "LambdaFunctionTimedOutEventAttributesTypeDef",
    "MarkerRecordedEventAttributesTypeDef",
    "RecordMarkerFailedEventAttributesTypeDef",
    "RequestCancelActivityTaskFailedEventAttributesTypeDef",
    "RequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef",
    "RequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    "ScheduleLambdaFunctionFailedEventAttributesTypeDef",
    "SignalExternalWorkflowExecutionFailedEventAttributesTypeDef",
    "SignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    "StartLambdaFunctionFailedEventAttributesTypeDef",
    "StartTimerFailedEventAttributesTypeDef",
    "TimerCanceledEventAttributesTypeDef",
    "TimerFiredEventAttributesTypeDef",
    "TimerStartedEventAttributesTypeDef",
    "WorkflowExecutionCanceledEventAttributesTypeDef",
    "WorkflowExecutionCompletedEventAttributesTypeDef",
    "WorkflowExecutionFailedEventAttributesTypeDef",
    "WorkflowExecutionTerminatedEventAttributesTypeDef",
    "WorkflowExecutionTimedOutEventAttributesTypeDef",
    "ListActivityTypesInputRequestTypeDef",
    "ListDomainsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ResourceTagTypeDef",
    "ListWorkflowTypesInputRequestTypeDef",
    "RecordActivityTaskHeartbeatInputRequestTypeDef",
    "RequestCancelWorkflowExecutionInputRequestTypeDef",
    "RespondActivityTaskCanceledInputRequestTypeDef",
    "RespondActivityTaskCompletedInputRequestTypeDef",
    "RespondActivityTaskFailedInputRequestTypeDef",
    "SignalWorkflowExecutionInputRequestTypeDef",
    "TerminateWorkflowExecutionInputRequestTypeDef",
    "UndeprecateDomainInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "WorkflowExecutionOpenCountsTypeDef",
    "ActivityTypeInfoTypeDef",
    "DeprecateActivityTypeInputRequestTypeDef",
    "DescribeActivityTypeInputRequestTypeDef",
    "ScheduleActivityTaskFailedEventAttributesTypeDef",
    "UndeprecateActivityTypeInputRequestTypeDef",
    "ActivityTaskScheduledEventAttributesTypeDef",
    "ActivityTypeConfigurationTypeDef",
    "ContinueAsNewWorkflowExecutionDecisionAttributesTypeDef",
    "CountPendingActivityTasksInputRequestTypeDef",
    "CountPendingDecisionTasksInputRequestTypeDef",
    "DecisionTaskScheduledEventAttributesTypeDef",
    "PollForActivityTaskInputRequestTypeDef",
    "PollForDecisionTaskInputRequestTypeDef",
    "RegisterActivityTypeInputRequestTypeDef",
    "RegisterWorkflowTypeInputRequestTypeDef",
    "ScheduleActivityTaskDecisionAttributesTypeDef",
    "WorkflowExecutionConfigurationTypeDef",
    "WorkflowTypeConfigurationTypeDef",
    "ActivityTaskStatusTypeDef",
    "EmptyResponseMetadataTypeDef",
    "PendingTaskCountTypeDef",
    "RunTypeDef",
    "WorkflowExecutionCountTypeDef",
    "ActivityTaskTypeDef",
    "DescribeWorkflowExecutionInputRequestTypeDef",
    "ExternalWorkflowExecutionCancelRequestedEventAttributesTypeDef",
    "ExternalWorkflowExecutionSignaledEventAttributesTypeDef",
    "GetWorkflowExecutionHistoryInputRequestTypeDef",
    "WorkflowExecutionCancelRequestedEventAttributesTypeDef",
    "WorkflowExecutionSignaledEventAttributesTypeDef",
    "ChildWorkflowExecutionCanceledEventAttributesTypeDef",
    "ChildWorkflowExecutionCompletedEventAttributesTypeDef",
    "ChildWorkflowExecutionFailedEventAttributesTypeDef",
    "ChildWorkflowExecutionStartedEventAttributesTypeDef",
    "ChildWorkflowExecutionTerminatedEventAttributesTypeDef",
    "ChildWorkflowExecutionTimedOutEventAttributesTypeDef",
    "DeprecateWorkflowTypeInputRequestTypeDef",
    "DescribeWorkflowTypeInputRequestTypeDef",
    "StartChildWorkflowExecutionDecisionAttributesTypeDef",
    "StartChildWorkflowExecutionFailedEventAttributesTypeDef",
    "StartChildWorkflowExecutionInitiatedEventAttributesTypeDef",
    "StartWorkflowExecutionInputRequestTypeDef",
    "UndeprecateWorkflowTypeInputRequestTypeDef",
    "WorkflowExecutionContinuedAsNewEventAttributesTypeDef",
    "WorkflowExecutionInfoTypeDef",
    "WorkflowExecutionStartedEventAttributesTypeDef",
    "WorkflowTypeInfoTypeDef",
    "CountClosedWorkflowExecutionsInputRequestTypeDef",
    "CountOpenWorkflowExecutionsInputRequestTypeDef",
    "ListClosedWorkflowExecutionsInputRequestTypeDef",
    "ListOpenWorkflowExecutionsInputRequestTypeDef",
    "DomainDetailTypeDef",
    "DomainInfosTypeDef",
    "GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef",
    "ListActivityTypesInputListActivityTypesPaginateTypeDef",
    "ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef",
    "ListDomainsInputListDomainsPaginateTypeDef",
    "ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef",
    "ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef",
    "PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "RegisterDomainInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "ActivityTypeInfosTypeDef",
    "ActivityTypeDetailTypeDef",
    "DecisionTypeDef",
    "WorkflowExecutionDetailTypeDef",
    "WorkflowExecutionInfosTypeDef",
    "HistoryEventTypeDef",
    "WorkflowTypeDetailTypeDef",
    "WorkflowTypeInfosTypeDef",
    "RespondDecisionTaskCompletedInputRequestTypeDef",
    "DecisionTaskTypeDef",
    "HistoryTypeDef",
)

ActivityTaskCancelRequestedEventAttributesTypeDef = TypedDict(
    "ActivityTaskCancelRequestedEventAttributesTypeDef",
    {
        "decisionTaskCompletedEventId": int,
        "activityId": str,
    },
)

_RequiredActivityTaskCanceledEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskCanceledEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalActivityTaskCanceledEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskCanceledEventAttributesTypeDef",
    {
        "details": str,
        "latestCancelRequestedEventId": int,
    },
    total=False,
)

class ActivityTaskCanceledEventAttributesTypeDef(
    _RequiredActivityTaskCanceledEventAttributesTypeDef,
    _OptionalActivityTaskCanceledEventAttributesTypeDef,
):
    pass

_RequiredActivityTaskCompletedEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskCompletedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalActivityTaskCompletedEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskCompletedEventAttributesTypeDef",
    {
        "result": str,
    },
    total=False,
)

class ActivityTaskCompletedEventAttributesTypeDef(
    _RequiredActivityTaskCompletedEventAttributesTypeDef,
    _OptionalActivityTaskCompletedEventAttributesTypeDef,
):
    pass

_RequiredActivityTaskFailedEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskFailedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalActivityTaskFailedEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskFailedEventAttributesTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

class ActivityTaskFailedEventAttributesTypeDef(
    _RequiredActivityTaskFailedEventAttributesTypeDef,
    _OptionalActivityTaskFailedEventAttributesTypeDef,
):
    pass

ActivityTypeTypeDef = TypedDict(
    "ActivityTypeTypeDef",
    {
        "name": str,
        "version": str,
    },
)

TaskListTypeDef = TypedDict(
    "TaskListTypeDef",
    {
        "name": str,
    },
)

_RequiredActivityTaskStartedEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskStartedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
    },
)
_OptionalActivityTaskStartedEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskStartedEventAttributesTypeDef",
    {
        "identity": str,
    },
    total=False,
)

class ActivityTaskStartedEventAttributesTypeDef(
    _RequiredActivityTaskStartedEventAttributesTypeDef,
    _OptionalActivityTaskStartedEventAttributesTypeDef,
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

_RequiredActivityTaskTimedOutEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskTimedOutEventAttributesTypeDef",
    {
        "timeoutType": ActivityTaskTimeoutTypeType,
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalActivityTaskTimedOutEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskTimedOutEventAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

class ActivityTaskTimedOutEventAttributesTypeDef(
    _RequiredActivityTaskTimedOutEventAttributesTypeDef,
    _OptionalActivityTaskTimedOutEventAttributesTypeDef,
):
    pass

WorkflowExecutionTypeDef = TypedDict(
    "WorkflowExecutionTypeDef",
    {
        "workflowId": str,
        "runId": str,
    },
)

CancelTimerDecisionAttributesTypeDef = TypedDict(
    "CancelTimerDecisionAttributesTypeDef",
    {
        "timerId": str,
    },
)

CancelTimerFailedEventAttributesTypeDef = TypedDict(
    "CancelTimerFailedEventAttributesTypeDef",
    {
        "timerId": str,
        "cause": CancelTimerFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

CancelWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "CancelWorkflowExecutionDecisionAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

CancelWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "CancelWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "cause": CancelWorkflowExecutionFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

WorkflowTypeTypeDef = TypedDict(
    "WorkflowTypeTypeDef",
    {
        "name": str,
        "version": str,
    },
)

CloseStatusFilterTypeDef = TypedDict(
    "CloseStatusFilterTypeDef",
    {
        "status": CloseStatusType,
    },
)

CompleteWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "CompleteWorkflowExecutionDecisionAttributesTypeDef",
    {
        "result": str,
    },
    total=False,
)

CompleteWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "CompleteWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "cause": CompleteWorkflowExecutionFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

ContinueAsNewWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "ContinueAsNewWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "cause": ContinueAsNewWorkflowExecutionFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

_RequiredExecutionTimeFilterTypeDef = TypedDict(
    "_RequiredExecutionTimeFilterTypeDef",
    {
        "oldestDate": Union[datetime, str],
    },
)
_OptionalExecutionTimeFilterTypeDef = TypedDict(
    "_OptionalExecutionTimeFilterTypeDef",
    {
        "latestDate": Union[datetime, str],
    },
    total=False,
)

class ExecutionTimeFilterTypeDef(
    _RequiredExecutionTimeFilterTypeDef, _OptionalExecutionTimeFilterTypeDef
):
    pass

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "tag": str,
    },
)

WorkflowExecutionFilterTypeDef = TypedDict(
    "WorkflowExecutionFilterTypeDef",
    {
        "workflowId": str,
    },
)

_RequiredWorkflowTypeFilterTypeDef = TypedDict(
    "_RequiredWorkflowTypeFilterTypeDef",
    {
        "name": str,
    },
)
_OptionalWorkflowTypeFilterTypeDef = TypedDict(
    "_OptionalWorkflowTypeFilterTypeDef",
    {
        "version": str,
    },
    total=False,
)

class WorkflowTypeFilterTypeDef(
    _RequiredWorkflowTypeFilterTypeDef, _OptionalWorkflowTypeFilterTypeDef
):
    pass

_RequiredDecisionTaskCompletedEventAttributesTypeDef = TypedDict(
    "_RequiredDecisionTaskCompletedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalDecisionTaskCompletedEventAttributesTypeDef = TypedDict(
    "_OptionalDecisionTaskCompletedEventAttributesTypeDef",
    {
        "executionContext": str,
    },
    total=False,
)

class DecisionTaskCompletedEventAttributesTypeDef(
    _RequiredDecisionTaskCompletedEventAttributesTypeDef,
    _OptionalDecisionTaskCompletedEventAttributesTypeDef,
):
    pass

_RequiredDecisionTaskStartedEventAttributesTypeDef = TypedDict(
    "_RequiredDecisionTaskStartedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
    },
)
_OptionalDecisionTaskStartedEventAttributesTypeDef = TypedDict(
    "_OptionalDecisionTaskStartedEventAttributesTypeDef",
    {
        "identity": str,
    },
    total=False,
)

class DecisionTaskStartedEventAttributesTypeDef(
    _RequiredDecisionTaskStartedEventAttributesTypeDef,
    _OptionalDecisionTaskStartedEventAttributesTypeDef,
):
    pass

DecisionTaskTimedOutEventAttributesTypeDef = TypedDict(
    "DecisionTaskTimedOutEventAttributesTypeDef",
    {
        "timeoutType": Literal["START_TO_CLOSE"],
        "scheduledEventId": int,
        "startedEventId": int,
    },
)

FailWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "FailWorkflowExecutionDecisionAttributesTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

_RequiredRecordMarkerDecisionAttributesTypeDef = TypedDict(
    "_RequiredRecordMarkerDecisionAttributesTypeDef",
    {
        "markerName": str,
    },
)
_OptionalRecordMarkerDecisionAttributesTypeDef = TypedDict(
    "_OptionalRecordMarkerDecisionAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

class RecordMarkerDecisionAttributesTypeDef(
    _RequiredRecordMarkerDecisionAttributesTypeDef, _OptionalRecordMarkerDecisionAttributesTypeDef
):
    pass

RequestCancelActivityTaskDecisionAttributesTypeDef = TypedDict(
    "RequestCancelActivityTaskDecisionAttributesTypeDef",
    {
        "activityId": str,
    },
)

_RequiredRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_RequiredRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef",
    {
        "workflowId": str,
    },
)
_OptionalRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_OptionalRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef",
    {
        "runId": str,
        "control": str,
    },
    total=False,
)

class RequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef(
    _RequiredRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef,
    _OptionalRequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef,
):
    pass

_RequiredScheduleLambdaFunctionDecisionAttributesTypeDef = TypedDict(
    "_RequiredScheduleLambdaFunctionDecisionAttributesTypeDef",
    {
        "id": str,
        "name": str,
    },
)
_OptionalScheduleLambdaFunctionDecisionAttributesTypeDef = TypedDict(
    "_OptionalScheduleLambdaFunctionDecisionAttributesTypeDef",
    {
        "control": str,
        "input": str,
        "startToCloseTimeout": str,
    },
    total=False,
)

class ScheduleLambdaFunctionDecisionAttributesTypeDef(
    _RequiredScheduleLambdaFunctionDecisionAttributesTypeDef,
    _OptionalScheduleLambdaFunctionDecisionAttributesTypeDef,
):
    pass

_RequiredSignalExternalWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_RequiredSignalExternalWorkflowExecutionDecisionAttributesTypeDef",
    {
        "workflowId": str,
        "signalName": str,
    },
)
_OptionalSignalExternalWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_OptionalSignalExternalWorkflowExecutionDecisionAttributesTypeDef",
    {
        "runId": str,
        "input": str,
        "control": str,
    },
    total=False,
)

class SignalExternalWorkflowExecutionDecisionAttributesTypeDef(
    _RequiredSignalExternalWorkflowExecutionDecisionAttributesTypeDef,
    _OptionalSignalExternalWorkflowExecutionDecisionAttributesTypeDef,
):
    pass

_RequiredStartTimerDecisionAttributesTypeDef = TypedDict(
    "_RequiredStartTimerDecisionAttributesTypeDef",
    {
        "timerId": str,
        "startToFireTimeout": str,
    },
)
_OptionalStartTimerDecisionAttributesTypeDef = TypedDict(
    "_OptionalStartTimerDecisionAttributesTypeDef",
    {
        "control": str,
    },
    total=False,
)

class StartTimerDecisionAttributesTypeDef(
    _RequiredStartTimerDecisionAttributesTypeDef, _OptionalStartTimerDecisionAttributesTypeDef
):
    pass

DeprecateDomainInputRequestTypeDef = TypedDict(
    "DeprecateDomainInputRequestTypeDef",
    {
        "name": str,
    },
)

DescribeDomainInputRequestTypeDef = TypedDict(
    "DescribeDomainInputRequestTypeDef",
    {
        "name": str,
    },
)

DomainConfigurationTypeDef = TypedDict(
    "DomainConfigurationTypeDef",
    {
        "workflowExecutionRetentionPeriodInDays": str,
    },
)

_RequiredDomainInfoTypeDef = TypedDict(
    "_RequiredDomainInfoTypeDef",
    {
        "name": str,
        "status": RegistrationStatusType,
    },
)
_OptionalDomainInfoTypeDef = TypedDict(
    "_OptionalDomainInfoTypeDef",
    {
        "description": str,
        "arn": str,
    },
    total=False,
)

class DomainInfoTypeDef(_RequiredDomainInfoTypeDef, _OptionalDomainInfoTypeDef):
    pass

FailWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "FailWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "cause": FailWorkflowExecutionFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
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

_RequiredLambdaFunctionCompletedEventAttributesTypeDef = TypedDict(
    "_RequiredLambdaFunctionCompletedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalLambdaFunctionCompletedEventAttributesTypeDef = TypedDict(
    "_OptionalLambdaFunctionCompletedEventAttributesTypeDef",
    {
        "result": str,
    },
    total=False,
)

class LambdaFunctionCompletedEventAttributesTypeDef(
    _RequiredLambdaFunctionCompletedEventAttributesTypeDef,
    _OptionalLambdaFunctionCompletedEventAttributesTypeDef,
):
    pass

_RequiredLambdaFunctionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredLambdaFunctionFailedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalLambdaFunctionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalLambdaFunctionFailedEventAttributesTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

class LambdaFunctionFailedEventAttributesTypeDef(
    _RequiredLambdaFunctionFailedEventAttributesTypeDef,
    _OptionalLambdaFunctionFailedEventAttributesTypeDef,
):
    pass

_RequiredLambdaFunctionScheduledEventAttributesTypeDef = TypedDict(
    "_RequiredLambdaFunctionScheduledEventAttributesTypeDef",
    {
        "id": str,
        "name": str,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalLambdaFunctionScheduledEventAttributesTypeDef = TypedDict(
    "_OptionalLambdaFunctionScheduledEventAttributesTypeDef",
    {
        "control": str,
        "input": str,
        "startToCloseTimeout": str,
    },
    total=False,
)

class LambdaFunctionScheduledEventAttributesTypeDef(
    _RequiredLambdaFunctionScheduledEventAttributesTypeDef,
    _OptionalLambdaFunctionScheduledEventAttributesTypeDef,
):
    pass

LambdaFunctionStartedEventAttributesTypeDef = TypedDict(
    "LambdaFunctionStartedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
    },
)

_RequiredLambdaFunctionTimedOutEventAttributesTypeDef = TypedDict(
    "_RequiredLambdaFunctionTimedOutEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "startedEventId": int,
    },
)
_OptionalLambdaFunctionTimedOutEventAttributesTypeDef = TypedDict(
    "_OptionalLambdaFunctionTimedOutEventAttributesTypeDef",
    {
        "timeoutType": Literal["START_TO_CLOSE"],
    },
    total=False,
)

class LambdaFunctionTimedOutEventAttributesTypeDef(
    _RequiredLambdaFunctionTimedOutEventAttributesTypeDef,
    _OptionalLambdaFunctionTimedOutEventAttributesTypeDef,
):
    pass

_RequiredMarkerRecordedEventAttributesTypeDef = TypedDict(
    "_RequiredMarkerRecordedEventAttributesTypeDef",
    {
        "markerName": str,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalMarkerRecordedEventAttributesTypeDef = TypedDict(
    "_OptionalMarkerRecordedEventAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

class MarkerRecordedEventAttributesTypeDef(
    _RequiredMarkerRecordedEventAttributesTypeDef, _OptionalMarkerRecordedEventAttributesTypeDef
):
    pass

RecordMarkerFailedEventAttributesTypeDef = TypedDict(
    "RecordMarkerFailedEventAttributesTypeDef",
    {
        "markerName": str,
        "cause": Literal["OPERATION_NOT_PERMITTED"],
        "decisionTaskCompletedEventId": int,
    },
)

RequestCancelActivityTaskFailedEventAttributesTypeDef = TypedDict(
    "RequestCancelActivityTaskFailedEventAttributesTypeDef",
    {
        "activityId": str,
        "cause": RequestCancelActivityTaskFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

_RequiredRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "workflowId": str,
        "cause": RequestCancelExternalWorkflowExecutionFailedCauseType,
        "initiatedEventId": int,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "runId": str,
        "control": str,
    },
    total=False,
)

class RequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef(
    _RequiredRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef,
    _OptionalRequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef,
):
    pass

_RequiredRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_RequiredRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "workflowId": str,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_OptionalRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "runId": str,
        "control": str,
    },
    total=False,
)

class RequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef(
    _RequiredRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
    _OptionalRequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
):
    pass

ScheduleLambdaFunctionFailedEventAttributesTypeDef = TypedDict(
    "ScheduleLambdaFunctionFailedEventAttributesTypeDef",
    {
        "id": str,
        "name": str,
        "cause": ScheduleLambdaFunctionFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

_RequiredSignalExternalWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredSignalExternalWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "workflowId": str,
        "cause": SignalExternalWorkflowExecutionFailedCauseType,
        "initiatedEventId": int,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalSignalExternalWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalSignalExternalWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "runId": str,
        "control": str,
    },
    total=False,
)

class SignalExternalWorkflowExecutionFailedEventAttributesTypeDef(
    _RequiredSignalExternalWorkflowExecutionFailedEventAttributesTypeDef,
    _OptionalSignalExternalWorkflowExecutionFailedEventAttributesTypeDef,
):
    pass

_RequiredSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_RequiredSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "workflowId": str,
        "signalName": str,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_OptionalSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "runId": str,
        "input": str,
        "control": str,
    },
    total=False,
)

class SignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef(
    _RequiredSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
    _OptionalSignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
):
    pass

StartLambdaFunctionFailedEventAttributesTypeDef = TypedDict(
    "StartLambdaFunctionFailedEventAttributesTypeDef",
    {
        "scheduledEventId": int,
        "cause": Literal["ASSUME_ROLE_FAILED"],
        "message": str,
    },
    total=False,
)

StartTimerFailedEventAttributesTypeDef = TypedDict(
    "StartTimerFailedEventAttributesTypeDef",
    {
        "timerId": str,
        "cause": StartTimerFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

TimerCanceledEventAttributesTypeDef = TypedDict(
    "TimerCanceledEventAttributesTypeDef",
    {
        "timerId": str,
        "startedEventId": int,
        "decisionTaskCompletedEventId": int,
    },
)

TimerFiredEventAttributesTypeDef = TypedDict(
    "TimerFiredEventAttributesTypeDef",
    {
        "timerId": str,
        "startedEventId": int,
    },
)

_RequiredTimerStartedEventAttributesTypeDef = TypedDict(
    "_RequiredTimerStartedEventAttributesTypeDef",
    {
        "timerId": str,
        "startToFireTimeout": str,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalTimerStartedEventAttributesTypeDef = TypedDict(
    "_OptionalTimerStartedEventAttributesTypeDef",
    {
        "control": str,
    },
    total=False,
)

class TimerStartedEventAttributesTypeDef(
    _RequiredTimerStartedEventAttributesTypeDef, _OptionalTimerStartedEventAttributesTypeDef
):
    pass

_RequiredWorkflowExecutionCanceledEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionCanceledEventAttributesTypeDef",
    {
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalWorkflowExecutionCanceledEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionCanceledEventAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

class WorkflowExecutionCanceledEventAttributesTypeDef(
    _RequiredWorkflowExecutionCanceledEventAttributesTypeDef,
    _OptionalWorkflowExecutionCanceledEventAttributesTypeDef,
):
    pass

_RequiredWorkflowExecutionCompletedEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionCompletedEventAttributesTypeDef",
    {
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalWorkflowExecutionCompletedEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionCompletedEventAttributesTypeDef",
    {
        "result": str,
    },
    total=False,
)

class WorkflowExecutionCompletedEventAttributesTypeDef(
    _RequiredWorkflowExecutionCompletedEventAttributesTypeDef,
    _OptionalWorkflowExecutionCompletedEventAttributesTypeDef,
):
    pass

_RequiredWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

class WorkflowExecutionFailedEventAttributesTypeDef(
    _RequiredWorkflowExecutionFailedEventAttributesTypeDef,
    _OptionalWorkflowExecutionFailedEventAttributesTypeDef,
):
    pass

_RequiredWorkflowExecutionTerminatedEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionTerminatedEventAttributesTypeDef",
    {
        "childPolicy": ChildPolicyType,
    },
)
_OptionalWorkflowExecutionTerminatedEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionTerminatedEventAttributesTypeDef",
    {
        "reason": str,
        "details": str,
        "cause": WorkflowExecutionTerminatedCauseType,
    },
    total=False,
)

class WorkflowExecutionTerminatedEventAttributesTypeDef(
    _RequiredWorkflowExecutionTerminatedEventAttributesTypeDef,
    _OptionalWorkflowExecutionTerminatedEventAttributesTypeDef,
):
    pass

WorkflowExecutionTimedOutEventAttributesTypeDef = TypedDict(
    "WorkflowExecutionTimedOutEventAttributesTypeDef",
    {
        "timeoutType": Literal["START_TO_CLOSE"],
        "childPolicy": ChildPolicyType,
    },
)

_RequiredListActivityTypesInputRequestTypeDef = TypedDict(
    "_RequiredListActivityTypesInputRequestTypeDef",
    {
        "domain": str,
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListActivityTypesInputRequestTypeDef = TypedDict(
    "_OptionalListActivityTypesInputRequestTypeDef",
    {
        "name": str,
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class ListActivityTypesInputRequestTypeDef(
    _RequiredListActivityTypesInputRequestTypeDef, _OptionalListActivityTypesInputRequestTypeDef
):
    pass

_RequiredListDomainsInputRequestTypeDef = TypedDict(
    "_RequiredListDomainsInputRequestTypeDef",
    {
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListDomainsInputRequestTypeDef = TypedDict(
    "_OptionalListDomainsInputRequestTypeDef",
    {
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class ListDomainsInputRequestTypeDef(
    _RequiredListDomainsInputRequestTypeDef, _OptionalListDomainsInputRequestTypeDef
):
    pass

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredResourceTagTypeDef = TypedDict(
    "_RequiredResourceTagTypeDef",
    {
        "key": str,
    },
)
_OptionalResourceTagTypeDef = TypedDict(
    "_OptionalResourceTagTypeDef",
    {
        "value": str,
    },
    total=False,
)

class ResourceTagTypeDef(_RequiredResourceTagTypeDef, _OptionalResourceTagTypeDef):
    pass

_RequiredListWorkflowTypesInputRequestTypeDef = TypedDict(
    "_RequiredListWorkflowTypesInputRequestTypeDef",
    {
        "domain": str,
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListWorkflowTypesInputRequestTypeDef = TypedDict(
    "_OptionalListWorkflowTypesInputRequestTypeDef",
    {
        "name": str,
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class ListWorkflowTypesInputRequestTypeDef(
    _RequiredListWorkflowTypesInputRequestTypeDef, _OptionalListWorkflowTypesInputRequestTypeDef
):
    pass

_RequiredRecordActivityTaskHeartbeatInputRequestTypeDef = TypedDict(
    "_RequiredRecordActivityTaskHeartbeatInputRequestTypeDef",
    {
        "taskToken": str,
    },
)
_OptionalRecordActivityTaskHeartbeatInputRequestTypeDef = TypedDict(
    "_OptionalRecordActivityTaskHeartbeatInputRequestTypeDef",
    {
        "details": str,
    },
    total=False,
)

class RecordActivityTaskHeartbeatInputRequestTypeDef(
    _RequiredRecordActivityTaskHeartbeatInputRequestTypeDef,
    _OptionalRecordActivityTaskHeartbeatInputRequestTypeDef,
):
    pass

_RequiredRequestCancelWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_RequiredRequestCancelWorkflowExecutionInputRequestTypeDef",
    {
        "domain": str,
        "workflowId": str,
    },
)
_OptionalRequestCancelWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_OptionalRequestCancelWorkflowExecutionInputRequestTypeDef",
    {
        "runId": str,
    },
    total=False,
)

class RequestCancelWorkflowExecutionInputRequestTypeDef(
    _RequiredRequestCancelWorkflowExecutionInputRequestTypeDef,
    _OptionalRequestCancelWorkflowExecutionInputRequestTypeDef,
):
    pass

_RequiredRespondActivityTaskCanceledInputRequestTypeDef = TypedDict(
    "_RequiredRespondActivityTaskCanceledInputRequestTypeDef",
    {
        "taskToken": str,
    },
)
_OptionalRespondActivityTaskCanceledInputRequestTypeDef = TypedDict(
    "_OptionalRespondActivityTaskCanceledInputRequestTypeDef",
    {
        "details": str,
    },
    total=False,
)

class RespondActivityTaskCanceledInputRequestTypeDef(
    _RequiredRespondActivityTaskCanceledInputRequestTypeDef,
    _OptionalRespondActivityTaskCanceledInputRequestTypeDef,
):
    pass

_RequiredRespondActivityTaskCompletedInputRequestTypeDef = TypedDict(
    "_RequiredRespondActivityTaskCompletedInputRequestTypeDef",
    {
        "taskToken": str,
    },
)
_OptionalRespondActivityTaskCompletedInputRequestTypeDef = TypedDict(
    "_OptionalRespondActivityTaskCompletedInputRequestTypeDef",
    {
        "result": str,
    },
    total=False,
)

class RespondActivityTaskCompletedInputRequestTypeDef(
    _RequiredRespondActivityTaskCompletedInputRequestTypeDef,
    _OptionalRespondActivityTaskCompletedInputRequestTypeDef,
):
    pass

_RequiredRespondActivityTaskFailedInputRequestTypeDef = TypedDict(
    "_RequiredRespondActivityTaskFailedInputRequestTypeDef",
    {
        "taskToken": str,
    },
)
_OptionalRespondActivityTaskFailedInputRequestTypeDef = TypedDict(
    "_OptionalRespondActivityTaskFailedInputRequestTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

class RespondActivityTaskFailedInputRequestTypeDef(
    _RequiredRespondActivityTaskFailedInputRequestTypeDef,
    _OptionalRespondActivityTaskFailedInputRequestTypeDef,
):
    pass

_RequiredSignalWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_RequiredSignalWorkflowExecutionInputRequestTypeDef",
    {
        "domain": str,
        "workflowId": str,
        "signalName": str,
    },
)
_OptionalSignalWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_OptionalSignalWorkflowExecutionInputRequestTypeDef",
    {
        "runId": str,
        "input": str,
    },
    total=False,
)

class SignalWorkflowExecutionInputRequestTypeDef(
    _RequiredSignalWorkflowExecutionInputRequestTypeDef,
    _OptionalSignalWorkflowExecutionInputRequestTypeDef,
):
    pass

_RequiredTerminateWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_RequiredTerminateWorkflowExecutionInputRequestTypeDef",
    {
        "domain": str,
        "workflowId": str,
    },
)
_OptionalTerminateWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_OptionalTerminateWorkflowExecutionInputRequestTypeDef",
    {
        "runId": str,
        "reason": str,
        "details": str,
        "childPolicy": ChildPolicyType,
    },
    total=False,
)

class TerminateWorkflowExecutionInputRequestTypeDef(
    _RequiredTerminateWorkflowExecutionInputRequestTypeDef,
    _OptionalTerminateWorkflowExecutionInputRequestTypeDef,
):
    pass

UndeprecateDomainInputRequestTypeDef = TypedDict(
    "UndeprecateDomainInputRequestTypeDef",
    {
        "name": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredWorkflowExecutionOpenCountsTypeDef = TypedDict(
    "_RequiredWorkflowExecutionOpenCountsTypeDef",
    {
        "openActivityTasks": int,
        "openDecisionTasks": int,
        "openTimers": int,
        "openChildWorkflowExecutions": int,
    },
)
_OptionalWorkflowExecutionOpenCountsTypeDef = TypedDict(
    "_OptionalWorkflowExecutionOpenCountsTypeDef",
    {
        "openLambdaFunctions": int,
    },
    total=False,
)

class WorkflowExecutionOpenCountsTypeDef(
    _RequiredWorkflowExecutionOpenCountsTypeDef, _OptionalWorkflowExecutionOpenCountsTypeDef
):
    pass

_RequiredActivityTypeInfoTypeDef = TypedDict(
    "_RequiredActivityTypeInfoTypeDef",
    {
        "activityType": ActivityTypeTypeDef,
        "status": RegistrationStatusType,
        "creationDate": datetime,
    },
)
_OptionalActivityTypeInfoTypeDef = TypedDict(
    "_OptionalActivityTypeInfoTypeDef",
    {
        "description": str,
        "deprecationDate": datetime,
    },
    total=False,
)

class ActivityTypeInfoTypeDef(_RequiredActivityTypeInfoTypeDef, _OptionalActivityTypeInfoTypeDef):
    pass

DeprecateActivityTypeInputRequestTypeDef = TypedDict(
    "DeprecateActivityTypeInputRequestTypeDef",
    {
        "domain": str,
        "activityType": ActivityTypeTypeDef,
    },
)

DescribeActivityTypeInputRequestTypeDef = TypedDict(
    "DescribeActivityTypeInputRequestTypeDef",
    {
        "domain": str,
        "activityType": ActivityTypeTypeDef,
    },
)

ScheduleActivityTaskFailedEventAttributesTypeDef = TypedDict(
    "ScheduleActivityTaskFailedEventAttributesTypeDef",
    {
        "activityType": ActivityTypeTypeDef,
        "activityId": str,
        "cause": ScheduleActivityTaskFailedCauseType,
        "decisionTaskCompletedEventId": int,
    },
)

UndeprecateActivityTypeInputRequestTypeDef = TypedDict(
    "UndeprecateActivityTypeInputRequestTypeDef",
    {
        "domain": str,
        "activityType": ActivityTypeTypeDef,
    },
)

_RequiredActivityTaskScheduledEventAttributesTypeDef = TypedDict(
    "_RequiredActivityTaskScheduledEventAttributesTypeDef",
    {
        "activityType": ActivityTypeTypeDef,
        "activityId": str,
        "taskList": TaskListTypeDef,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalActivityTaskScheduledEventAttributesTypeDef = TypedDict(
    "_OptionalActivityTaskScheduledEventAttributesTypeDef",
    {
        "input": str,
        "control": str,
        "scheduleToStartTimeout": str,
        "scheduleToCloseTimeout": str,
        "startToCloseTimeout": str,
        "taskPriority": str,
        "heartbeatTimeout": str,
    },
    total=False,
)

class ActivityTaskScheduledEventAttributesTypeDef(
    _RequiredActivityTaskScheduledEventAttributesTypeDef,
    _OptionalActivityTaskScheduledEventAttributesTypeDef,
):
    pass

ActivityTypeConfigurationTypeDef = TypedDict(
    "ActivityTypeConfigurationTypeDef",
    {
        "defaultTaskStartToCloseTimeout": str,
        "defaultTaskHeartbeatTimeout": str,
        "defaultTaskList": TaskListTypeDef,
        "defaultTaskPriority": str,
        "defaultTaskScheduleToStartTimeout": str,
        "defaultTaskScheduleToCloseTimeout": str,
    },
    total=False,
)

ContinueAsNewWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "ContinueAsNewWorkflowExecutionDecisionAttributesTypeDef",
    {
        "input": str,
        "executionStartToCloseTimeout": str,
        "taskList": TaskListTypeDef,
        "taskPriority": str,
        "taskStartToCloseTimeout": str,
        "childPolicy": ChildPolicyType,
        "tagList": Sequence[str],
        "workflowTypeVersion": str,
        "lambdaRole": str,
    },
    total=False,
)

CountPendingActivityTasksInputRequestTypeDef = TypedDict(
    "CountPendingActivityTasksInputRequestTypeDef",
    {
        "domain": str,
        "taskList": TaskListTypeDef,
    },
)

CountPendingDecisionTasksInputRequestTypeDef = TypedDict(
    "CountPendingDecisionTasksInputRequestTypeDef",
    {
        "domain": str,
        "taskList": TaskListTypeDef,
    },
)

_RequiredDecisionTaskScheduledEventAttributesTypeDef = TypedDict(
    "_RequiredDecisionTaskScheduledEventAttributesTypeDef",
    {
        "taskList": TaskListTypeDef,
    },
)
_OptionalDecisionTaskScheduledEventAttributesTypeDef = TypedDict(
    "_OptionalDecisionTaskScheduledEventAttributesTypeDef",
    {
        "taskPriority": str,
        "startToCloseTimeout": str,
    },
    total=False,
)

class DecisionTaskScheduledEventAttributesTypeDef(
    _RequiredDecisionTaskScheduledEventAttributesTypeDef,
    _OptionalDecisionTaskScheduledEventAttributesTypeDef,
):
    pass

_RequiredPollForActivityTaskInputRequestTypeDef = TypedDict(
    "_RequiredPollForActivityTaskInputRequestTypeDef",
    {
        "domain": str,
        "taskList": TaskListTypeDef,
    },
)
_OptionalPollForActivityTaskInputRequestTypeDef = TypedDict(
    "_OptionalPollForActivityTaskInputRequestTypeDef",
    {
        "identity": str,
    },
    total=False,
)

class PollForActivityTaskInputRequestTypeDef(
    _RequiredPollForActivityTaskInputRequestTypeDef, _OptionalPollForActivityTaskInputRequestTypeDef
):
    pass

_RequiredPollForDecisionTaskInputRequestTypeDef = TypedDict(
    "_RequiredPollForDecisionTaskInputRequestTypeDef",
    {
        "domain": str,
        "taskList": TaskListTypeDef,
    },
)
_OptionalPollForDecisionTaskInputRequestTypeDef = TypedDict(
    "_OptionalPollForDecisionTaskInputRequestTypeDef",
    {
        "identity": str,
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class PollForDecisionTaskInputRequestTypeDef(
    _RequiredPollForDecisionTaskInputRequestTypeDef, _OptionalPollForDecisionTaskInputRequestTypeDef
):
    pass

_RequiredRegisterActivityTypeInputRequestTypeDef = TypedDict(
    "_RequiredRegisterActivityTypeInputRequestTypeDef",
    {
        "domain": str,
        "name": str,
        "version": str,
    },
)
_OptionalRegisterActivityTypeInputRequestTypeDef = TypedDict(
    "_OptionalRegisterActivityTypeInputRequestTypeDef",
    {
        "description": str,
        "defaultTaskStartToCloseTimeout": str,
        "defaultTaskHeartbeatTimeout": str,
        "defaultTaskList": TaskListTypeDef,
        "defaultTaskPriority": str,
        "defaultTaskScheduleToStartTimeout": str,
        "defaultTaskScheduleToCloseTimeout": str,
    },
    total=False,
)

class RegisterActivityTypeInputRequestTypeDef(
    _RequiredRegisterActivityTypeInputRequestTypeDef,
    _OptionalRegisterActivityTypeInputRequestTypeDef,
):
    pass

_RequiredRegisterWorkflowTypeInputRequestTypeDef = TypedDict(
    "_RequiredRegisterWorkflowTypeInputRequestTypeDef",
    {
        "domain": str,
        "name": str,
        "version": str,
    },
)
_OptionalRegisterWorkflowTypeInputRequestTypeDef = TypedDict(
    "_OptionalRegisterWorkflowTypeInputRequestTypeDef",
    {
        "description": str,
        "defaultTaskStartToCloseTimeout": str,
        "defaultExecutionStartToCloseTimeout": str,
        "defaultTaskList": TaskListTypeDef,
        "defaultTaskPriority": str,
        "defaultChildPolicy": ChildPolicyType,
        "defaultLambdaRole": str,
    },
    total=False,
)

class RegisterWorkflowTypeInputRequestTypeDef(
    _RequiredRegisterWorkflowTypeInputRequestTypeDef,
    _OptionalRegisterWorkflowTypeInputRequestTypeDef,
):
    pass

_RequiredScheduleActivityTaskDecisionAttributesTypeDef = TypedDict(
    "_RequiredScheduleActivityTaskDecisionAttributesTypeDef",
    {
        "activityType": ActivityTypeTypeDef,
        "activityId": str,
    },
)
_OptionalScheduleActivityTaskDecisionAttributesTypeDef = TypedDict(
    "_OptionalScheduleActivityTaskDecisionAttributesTypeDef",
    {
        "control": str,
        "input": str,
        "scheduleToCloseTimeout": str,
        "taskList": TaskListTypeDef,
        "taskPriority": str,
        "scheduleToStartTimeout": str,
        "startToCloseTimeout": str,
        "heartbeatTimeout": str,
    },
    total=False,
)

class ScheduleActivityTaskDecisionAttributesTypeDef(
    _RequiredScheduleActivityTaskDecisionAttributesTypeDef,
    _OptionalScheduleActivityTaskDecisionAttributesTypeDef,
):
    pass

_RequiredWorkflowExecutionConfigurationTypeDef = TypedDict(
    "_RequiredWorkflowExecutionConfigurationTypeDef",
    {
        "taskStartToCloseTimeout": str,
        "executionStartToCloseTimeout": str,
        "taskList": TaskListTypeDef,
        "childPolicy": ChildPolicyType,
    },
)
_OptionalWorkflowExecutionConfigurationTypeDef = TypedDict(
    "_OptionalWorkflowExecutionConfigurationTypeDef",
    {
        "taskPriority": str,
        "lambdaRole": str,
    },
    total=False,
)

class WorkflowExecutionConfigurationTypeDef(
    _RequiredWorkflowExecutionConfigurationTypeDef, _OptionalWorkflowExecutionConfigurationTypeDef
):
    pass

WorkflowTypeConfigurationTypeDef = TypedDict(
    "WorkflowTypeConfigurationTypeDef",
    {
        "defaultTaskStartToCloseTimeout": str,
        "defaultExecutionStartToCloseTimeout": str,
        "defaultTaskList": TaskListTypeDef,
        "defaultTaskPriority": str,
        "defaultChildPolicy": ChildPolicyType,
        "defaultLambdaRole": str,
    },
    total=False,
)

ActivityTaskStatusTypeDef = TypedDict(
    "ActivityTaskStatusTypeDef",
    {
        "cancelRequested": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PendingTaskCountTypeDef = TypedDict(
    "PendingTaskCountTypeDef",
    {
        "count": int,
        "truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunTypeDef = TypedDict(
    "RunTypeDef",
    {
        "runId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkflowExecutionCountTypeDef = TypedDict(
    "WorkflowExecutionCountTypeDef",
    {
        "count": int,
        "truncated": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActivityTaskTypeDef = TypedDict(
    "ActivityTaskTypeDef",
    {
        "taskToken": str,
        "activityId": str,
        "startedEventId": int,
        "workflowExecution": WorkflowExecutionTypeDef,
        "activityType": ActivityTypeTypeDef,
        "input": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkflowExecutionInputRequestTypeDef = TypedDict(
    "DescribeWorkflowExecutionInputRequestTypeDef",
    {
        "domain": str,
        "execution": WorkflowExecutionTypeDef,
    },
)

ExternalWorkflowExecutionCancelRequestedEventAttributesTypeDef = TypedDict(
    "ExternalWorkflowExecutionCancelRequestedEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "initiatedEventId": int,
    },
)

ExternalWorkflowExecutionSignaledEventAttributesTypeDef = TypedDict(
    "ExternalWorkflowExecutionSignaledEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "initiatedEventId": int,
    },
)

_RequiredGetWorkflowExecutionHistoryInputRequestTypeDef = TypedDict(
    "_RequiredGetWorkflowExecutionHistoryInputRequestTypeDef",
    {
        "domain": str,
        "execution": WorkflowExecutionTypeDef,
    },
)
_OptionalGetWorkflowExecutionHistoryInputRequestTypeDef = TypedDict(
    "_OptionalGetWorkflowExecutionHistoryInputRequestTypeDef",
    {
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class GetWorkflowExecutionHistoryInputRequestTypeDef(
    _RequiredGetWorkflowExecutionHistoryInputRequestTypeDef,
    _OptionalGetWorkflowExecutionHistoryInputRequestTypeDef,
):
    pass

WorkflowExecutionCancelRequestedEventAttributesTypeDef = TypedDict(
    "WorkflowExecutionCancelRequestedEventAttributesTypeDef",
    {
        "externalWorkflowExecution": WorkflowExecutionTypeDef,
        "externalInitiatedEventId": int,
        "cause": Literal["CHILD_POLICY_APPLIED"],
    },
    total=False,
)

_RequiredWorkflowExecutionSignaledEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionSignaledEventAttributesTypeDef",
    {
        "signalName": str,
    },
)
_OptionalWorkflowExecutionSignaledEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionSignaledEventAttributesTypeDef",
    {
        "input": str,
        "externalWorkflowExecution": WorkflowExecutionTypeDef,
        "externalInitiatedEventId": int,
    },
    total=False,
)

class WorkflowExecutionSignaledEventAttributesTypeDef(
    _RequiredWorkflowExecutionSignaledEventAttributesTypeDef,
    _OptionalWorkflowExecutionSignaledEventAttributesTypeDef,
):
    pass

_RequiredChildWorkflowExecutionCanceledEventAttributesTypeDef = TypedDict(
    "_RequiredChildWorkflowExecutionCanceledEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "initiatedEventId": int,
        "startedEventId": int,
    },
)
_OptionalChildWorkflowExecutionCanceledEventAttributesTypeDef = TypedDict(
    "_OptionalChildWorkflowExecutionCanceledEventAttributesTypeDef",
    {
        "details": str,
    },
    total=False,
)

class ChildWorkflowExecutionCanceledEventAttributesTypeDef(
    _RequiredChildWorkflowExecutionCanceledEventAttributesTypeDef,
    _OptionalChildWorkflowExecutionCanceledEventAttributesTypeDef,
):
    pass

_RequiredChildWorkflowExecutionCompletedEventAttributesTypeDef = TypedDict(
    "_RequiredChildWorkflowExecutionCompletedEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "initiatedEventId": int,
        "startedEventId": int,
    },
)
_OptionalChildWorkflowExecutionCompletedEventAttributesTypeDef = TypedDict(
    "_OptionalChildWorkflowExecutionCompletedEventAttributesTypeDef",
    {
        "result": str,
    },
    total=False,
)

class ChildWorkflowExecutionCompletedEventAttributesTypeDef(
    _RequiredChildWorkflowExecutionCompletedEventAttributesTypeDef,
    _OptionalChildWorkflowExecutionCompletedEventAttributesTypeDef,
):
    pass

_RequiredChildWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredChildWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "initiatedEventId": int,
        "startedEventId": int,
    },
)
_OptionalChildWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalChildWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "reason": str,
        "details": str,
    },
    total=False,
)

class ChildWorkflowExecutionFailedEventAttributesTypeDef(
    _RequiredChildWorkflowExecutionFailedEventAttributesTypeDef,
    _OptionalChildWorkflowExecutionFailedEventAttributesTypeDef,
):
    pass

ChildWorkflowExecutionStartedEventAttributesTypeDef = TypedDict(
    "ChildWorkflowExecutionStartedEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "initiatedEventId": int,
    },
)

ChildWorkflowExecutionTerminatedEventAttributesTypeDef = TypedDict(
    "ChildWorkflowExecutionTerminatedEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "initiatedEventId": int,
        "startedEventId": int,
    },
)

ChildWorkflowExecutionTimedOutEventAttributesTypeDef = TypedDict(
    "ChildWorkflowExecutionTimedOutEventAttributesTypeDef",
    {
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "timeoutType": Literal["START_TO_CLOSE"],
        "initiatedEventId": int,
        "startedEventId": int,
    },
)

DeprecateWorkflowTypeInputRequestTypeDef = TypedDict(
    "DeprecateWorkflowTypeInputRequestTypeDef",
    {
        "domain": str,
        "workflowType": WorkflowTypeTypeDef,
    },
)

DescribeWorkflowTypeInputRequestTypeDef = TypedDict(
    "DescribeWorkflowTypeInputRequestTypeDef",
    {
        "domain": str,
        "workflowType": WorkflowTypeTypeDef,
    },
)

_RequiredStartChildWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_RequiredStartChildWorkflowExecutionDecisionAttributesTypeDef",
    {
        "workflowType": WorkflowTypeTypeDef,
        "workflowId": str,
    },
)
_OptionalStartChildWorkflowExecutionDecisionAttributesTypeDef = TypedDict(
    "_OptionalStartChildWorkflowExecutionDecisionAttributesTypeDef",
    {
        "control": str,
        "input": str,
        "executionStartToCloseTimeout": str,
        "taskList": TaskListTypeDef,
        "taskPriority": str,
        "taskStartToCloseTimeout": str,
        "childPolicy": ChildPolicyType,
        "tagList": Sequence[str],
        "lambdaRole": str,
    },
    total=False,
)

class StartChildWorkflowExecutionDecisionAttributesTypeDef(
    _RequiredStartChildWorkflowExecutionDecisionAttributesTypeDef,
    _OptionalStartChildWorkflowExecutionDecisionAttributesTypeDef,
):
    pass

_RequiredStartChildWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_RequiredStartChildWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "workflowType": WorkflowTypeTypeDef,
        "cause": StartChildWorkflowExecutionFailedCauseType,
        "workflowId": str,
        "initiatedEventId": int,
        "decisionTaskCompletedEventId": int,
    },
)
_OptionalStartChildWorkflowExecutionFailedEventAttributesTypeDef = TypedDict(
    "_OptionalStartChildWorkflowExecutionFailedEventAttributesTypeDef",
    {
        "control": str,
    },
    total=False,
)

class StartChildWorkflowExecutionFailedEventAttributesTypeDef(
    _RequiredStartChildWorkflowExecutionFailedEventAttributesTypeDef,
    _OptionalStartChildWorkflowExecutionFailedEventAttributesTypeDef,
):
    pass

_RequiredStartChildWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_RequiredStartChildWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "workflowId": str,
        "workflowType": WorkflowTypeTypeDef,
        "taskList": TaskListTypeDef,
        "decisionTaskCompletedEventId": int,
        "childPolicy": ChildPolicyType,
    },
)
_OptionalStartChildWorkflowExecutionInitiatedEventAttributesTypeDef = TypedDict(
    "_OptionalStartChildWorkflowExecutionInitiatedEventAttributesTypeDef",
    {
        "control": str,
        "input": str,
        "executionStartToCloseTimeout": str,
        "taskPriority": str,
        "taskStartToCloseTimeout": str,
        "tagList": List[str],
        "lambdaRole": str,
    },
    total=False,
)

class StartChildWorkflowExecutionInitiatedEventAttributesTypeDef(
    _RequiredStartChildWorkflowExecutionInitiatedEventAttributesTypeDef,
    _OptionalStartChildWorkflowExecutionInitiatedEventAttributesTypeDef,
):
    pass

_RequiredStartWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_RequiredStartWorkflowExecutionInputRequestTypeDef",
    {
        "domain": str,
        "workflowId": str,
        "workflowType": WorkflowTypeTypeDef,
    },
)
_OptionalStartWorkflowExecutionInputRequestTypeDef = TypedDict(
    "_OptionalStartWorkflowExecutionInputRequestTypeDef",
    {
        "taskList": TaskListTypeDef,
        "taskPriority": str,
        "input": str,
        "executionStartToCloseTimeout": str,
        "tagList": Sequence[str],
        "taskStartToCloseTimeout": str,
        "childPolicy": ChildPolicyType,
        "lambdaRole": str,
    },
    total=False,
)

class StartWorkflowExecutionInputRequestTypeDef(
    _RequiredStartWorkflowExecutionInputRequestTypeDef,
    _OptionalStartWorkflowExecutionInputRequestTypeDef,
):
    pass

UndeprecateWorkflowTypeInputRequestTypeDef = TypedDict(
    "UndeprecateWorkflowTypeInputRequestTypeDef",
    {
        "domain": str,
        "workflowType": WorkflowTypeTypeDef,
    },
)

_RequiredWorkflowExecutionContinuedAsNewEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionContinuedAsNewEventAttributesTypeDef",
    {
        "decisionTaskCompletedEventId": int,
        "newExecutionRunId": str,
        "taskList": TaskListTypeDef,
        "childPolicy": ChildPolicyType,
        "workflowType": WorkflowTypeTypeDef,
    },
)
_OptionalWorkflowExecutionContinuedAsNewEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionContinuedAsNewEventAttributesTypeDef",
    {
        "input": str,
        "executionStartToCloseTimeout": str,
        "taskPriority": str,
        "taskStartToCloseTimeout": str,
        "tagList": List[str],
        "lambdaRole": str,
    },
    total=False,
)

class WorkflowExecutionContinuedAsNewEventAttributesTypeDef(
    _RequiredWorkflowExecutionContinuedAsNewEventAttributesTypeDef,
    _OptionalWorkflowExecutionContinuedAsNewEventAttributesTypeDef,
):
    pass

_RequiredWorkflowExecutionInfoTypeDef = TypedDict(
    "_RequiredWorkflowExecutionInfoTypeDef",
    {
        "execution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "startTimestamp": datetime,
        "executionStatus": ExecutionStatusType,
    },
)
_OptionalWorkflowExecutionInfoTypeDef = TypedDict(
    "_OptionalWorkflowExecutionInfoTypeDef",
    {
        "closeTimestamp": datetime,
        "closeStatus": CloseStatusType,
        "parent": WorkflowExecutionTypeDef,
        "tagList": List[str],
        "cancelRequested": bool,
    },
    total=False,
)

class WorkflowExecutionInfoTypeDef(
    _RequiredWorkflowExecutionInfoTypeDef, _OptionalWorkflowExecutionInfoTypeDef
):
    pass

_RequiredWorkflowExecutionStartedEventAttributesTypeDef = TypedDict(
    "_RequiredWorkflowExecutionStartedEventAttributesTypeDef",
    {
        "childPolicy": ChildPolicyType,
        "taskList": TaskListTypeDef,
        "workflowType": WorkflowTypeTypeDef,
    },
)
_OptionalWorkflowExecutionStartedEventAttributesTypeDef = TypedDict(
    "_OptionalWorkflowExecutionStartedEventAttributesTypeDef",
    {
        "input": str,
        "executionStartToCloseTimeout": str,
        "taskStartToCloseTimeout": str,
        "taskPriority": str,
        "tagList": List[str],
        "continuedExecutionRunId": str,
        "parentWorkflowExecution": WorkflowExecutionTypeDef,
        "parentInitiatedEventId": int,
        "lambdaRole": str,
    },
    total=False,
)

class WorkflowExecutionStartedEventAttributesTypeDef(
    _RequiredWorkflowExecutionStartedEventAttributesTypeDef,
    _OptionalWorkflowExecutionStartedEventAttributesTypeDef,
):
    pass

_RequiredWorkflowTypeInfoTypeDef = TypedDict(
    "_RequiredWorkflowTypeInfoTypeDef",
    {
        "workflowType": WorkflowTypeTypeDef,
        "status": RegistrationStatusType,
        "creationDate": datetime,
    },
)
_OptionalWorkflowTypeInfoTypeDef = TypedDict(
    "_OptionalWorkflowTypeInfoTypeDef",
    {
        "description": str,
        "deprecationDate": datetime,
    },
    total=False,
)

class WorkflowTypeInfoTypeDef(_RequiredWorkflowTypeInfoTypeDef, _OptionalWorkflowTypeInfoTypeDef):
    pass

_RequiredCountClosedWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_RequiredCountClosedWorkflowExecutionsInputRequestTypeDef",
    {
        "domain": str,
    },
)
_OptionalCountClosedWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_OptionalCountClosedWorkflowExecutionsInputRequestTypeDef",
    {
        "startTimeFilter": ExecutionTimeFilterTypeDef,
        "closeTimeFilter": ExecutionTimeFilterTypeDef,
        "executionFilter": WorkflowExecutionFilterTypeDef,
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "closeStatusFilter": CloseStatusFilterTypeDef,
    },
    total=False,
)

class CountClosedWorkflowExecutionsInputRequestTypeDef(
    _RequiredCountClosedWorkflowExecutionsInputRequestTypeDef,
    _OptionalCountClosedWorkflowExecutionsInputRequestTypeDef,
):
    pass

_RequiredCountOpenWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_RequiredCountOpenWorkflowExecutionsInputRequestTypeDef",
    {
        "domain": str,
        "startTimeFilter": ExecutionTimeFilterTypeDef,
    },
)
_OptionalCountOpenWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_OptionalCountOpenWorkflowExecutionsInputRequestTypeDef",
    {
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "executionFilter": WorkflowExecutionFilterTypeDef,
    },
    total=False,
)

class CountOpenWorkflowExecutionsInputRequestTypeDef(
    _RequiredCountOpenWorkflowExecutionsInputRequestTypeDef,
    _OptionalCountOpenWorkflowExecutionsInputRequestTypeDef,
):
    pass

_RequiredListClosedWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_RequiredListClosedWorkflowExecutionsInputRequestTypeDef",
    {
        "domain": str,
    },
)
_OptionalListClosedWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_OptionalListClosedWorkflowExecutionsInputRequestTypeDef",
    {
        "startTimeFilter": ExecutionTimeFilterTypeDef,
        "closeTimeFilter": ExecutionTimeFilterTypeDef,
        "executionFilter": WorkflowExecutionFilterTypeDef,
        "closeStatusFilter": CloseStatusFilterTypeDef,
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
    },
    total=False,
)

class ListClosedWorkflowExecutionsInputRequestTypeDef(
    _RequiredListClosedWorkflowExecutionsInputRequestTypeDef,
    _OptionalListClosedWorkflowExecutionsInputRequestTypeDef,
):
    pass

_RequiredListOpenWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_RequiredListOpenWorkflowExecutionsInputRequestTypeDef",
    {
        "domain": str,
        "startTimeFilter": ExecutionTimeFilterTypeDef,
    },
)
_OptionalListOpenWorkflowExecutionsInputRequestTypeDef = TypedDict(
    "_OptionalListOpenWorkflowExecutionsInputRequestTypeDef",
    {
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "nextPageToken": str,
        "maximumPageSize": int,
        "reverseOrder": bool,
        "executionFilter": WorkflowExecutionFilterTypeDef,
    },
    total=False,
)

class ListOpenWorkflowExecutionsInputRequestTypeDef(
    _RequiredListOpenWorkflowExecutionsInputRequestTypeDef,
    _OptionalListOpenWorkflowExecutionsInputRequestTypeDef,
):
    pass

DomainDetailTypeDef = TypedDict(
    "DomainDetailTypeDef",
    {
        "domainInfo": DomainInfoTypeDef,
        "configuration": DomainConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DomainInfosTypeDef = TypedDict(
    "DomainInfosTypeDef",
    {
        "domainInfos": List[DomainInfoTypeDef],
        "nextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef = TypedDict(
    "_RequiredGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef",
    {
        "domain": str,
        "execution": WorkflowExecutionTypeDef,
    },
)
_OptionalGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef = TypedDict(
    "_OptionalGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef",
    {
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef(
    _RequiredGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef,
    _OptionalGetWorkflowExecutionHistoryInputGetWorkflowExecutionHistoryPaginateTypeDef,
):
    pass

_RequiredListActivityTypesInputListActivityTypesPaginateTypeDef = TypedDict(
    "_RequiredListActivityTypesInputListActivityTypesPaginateTypeDef",
    {
        "domain": str,
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListActivityTypesInputListActivityTypesPaginateTypeDef = TypedDict(
    "_OptionalListActivityTypesInputListActivityTypesPaginateTypeDef",
    {
        "name": str,
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListActivityTypesInputListActivityTypesPaginateTypeDef(
    _RequiredListActivityTypesInputListActivityTypesPaginateTypeDef,
    _OptionalListActivityTypesInputListActivityTypesPaginateTypeDef,
):
    pass

_RequiredListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef = TypedDict(
    "_RequiredListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef",
    {
        "domain": str,
    },
)
_OptionalListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef = TypedDict(
    "_OptionalListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef",
    {
        "startTimeFilter": ExecutionTimeFilterTypeDef,
        "closeTimeFilter": ExecutionTimeFilterTypeDef,
        "executionFilter": WorkflowExecutionFilterTypeDef,
        "closeStatusFilter": CloseStatusFilterTypeDef,
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef(
    _RequiredListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef,
    _OptionalListClosedWorkflowExecutionsInputListClosedWorkflowExecutionsPaginateTypeDef,
):
    pass

_RequiredListDomainsInputListDomainsPaginateTypeDef = TypedDict(
    "_RequiredListDomainsInputListDomainsPaginateTypeDef",
    {
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListDomainsInputListDomainsPaginateTypeDef = TypedDict(
    "_OptionalListDomainsInputListDomainsPaginateTypeDef",
    {
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDomainsInputListDomainsPaginateTypeDef(
    _RequiredListDomainsInputListDomainsPaginateTypeDef,
    _OptionalListDomainsInputListDomainsPaginateTypeDef,
):
    pass

_RequiredListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef = TypedDict(
    "_RequiredListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef",
    {
        "domain": str,
        "startTimeFilter": ExecutionTimeFilterTypeDef,
    },
)
_OptionalListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef = TypedDict(
    "_OptionalListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef",
    {
        "typeFilter": WorkflowTypeFilterTypeDef,
        "tagFilter": TagFilterTypeDef,
        "reverseOrder": bool,
        "executionFilter": WorkflowExecutionFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef(
    _RequiredListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef,
    _OptionalListOpenWorkflowExecutionsInputListOpenWorkflowExecutionsPaginateTypeDef,
):
    pass

_RequiredListWorkflowTypesInputListWorkflowTypesPaginateTypeDef = TypedDict(
    "_RequiredListWorkflowTypesInputListWorkflowTypesPaginateTypeDef",
    {
        "domain": str,
        "registrationStatus": RegistrationStatusType,
    },
)
_OptionalListWorkflowTypesInputListWorkflowTypesPaginateTypeDef = TypedDict(
    "_OptionalListWorkflowTypesInputListWorkflowTypesPaginateTypeDef",
    {
        "name": str,
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListWorkflowTypesInputListWorkflowTypesPaginateTypeDef(
    _RequiredListWorkflowTypesInputListWorkflowTypesPaginateTypeDef,
    _OptionalListWorkflowTypesInputListWorkflowTypesPaginateTypeDef,
):
    pass

_RequiredPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef = TypedDict(
    "_RequiredPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef",
    {
        "domain": str,
        "taskList": TaskListTypeDef,
    },
)
_OptionalPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef = TypedDict(
    "_OptionalPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef",
    {
        "identity": str,
        "reverseOrder": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class PollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef(
    _RequiredPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef,
    _OptionalPollForDecisionTaskInputPollForDecisionTaskPaginateTypeDef,
):
    pass

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": List[ResourceTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRegisterDomainInputRequestTypeDef = TypedDict(
    "_RequiredRegisterDomainInputRequestTypeDef",
    {
        "name": str,
        "workflowExecutionRetentionPeriodInDays": str,
    },
)
_OptionalRegisterDomainInputRequestTypeDef = TypedDict(
    "_OptionalRegisterDomainInputRequestTypeDef",
    {
        "description": str,
        "tags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)

class RegisterDomainInputRequestTypeDef(
    _RequiredRegisterDomainInputRequestTypeDef, _OptionalRegisterDomainInputRequestTypeDef
):
    pass

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[ResourceTagTypeDef],
    },
)

ActivityTypeInfosTypeDef = TypedDict(
    "ActivityTypeInfosTypeDef",
    {
        "typeInfos": List[ActivityTypeInfoTypeDef],
        "nextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActivityTypeDetailTypeDef = TypedDict(
    "ActivityTypeDetailTypeDef",
    {
        "typeInfo": ActivityTypeInfoTypeDef,
        "configuration": ActivityTypeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDecisionTypeDef = TypedDict(
    "_RequiredDecisionTypeDef",
    {
        "decisionType": DecisionTypeType,
    },
)
_OptionalDecisionTypeDef = TypedDict(
    "_OptionalDecisionTypeDef",
    {
        "scheduleActivityTaskDecisionAttributes": ScheduleActivityTaskDecisionAttributesTypeDef,
        "requestCancelActivityTaskDecisionAttributes": RequestCancelActivityTaskDecisionAttributesTypeDef,
        "completeWorkflowExecutionDecisionAttributes": CompleteWorkflowExecutionDecisionAttributesTypeDef,
        "failWorkflowExecutionDecisionAttributes": FailWorkflowExecutionDecisionAttributesTypeDef,
        "cancelWorkflowExecutionDecisionAttributes": CancelWorkflowExecutionDecisionAttributesTypeDef,
        "continueAsNewWorkflowExecutionDecisionAttributes": ContinueAsNewWorkflowExecutionDecisionAttributesTypeDef,
        "recordMarkerDecisionAttributes": RecordMarkerDecisionAttributesTypeDef,
        "startTimerDecisionAttributes": StartTimerDecisionAttributesTypeDef,
        "cancelTimerDecisionAttributes": CancelTimerDecisionAttributesTypeDef,
        "signalExternalWorkflowExecutionDecisionAttributes": SignalExternalWorkflowExecutionDecisionAttributesTypeDef,
        "requestCancelExternalWorkflowExecutionDecisionAttributes": RequestCancelExternalWorkflowExecutionDecisionAttributesTypeDef,
        "startChildWorkflowExecutionDecisionAttributes": StartChildWorkflowExecutionDecisionAttributesTypeDef,
        "scheduleLambdaFunctionDecisionAttributes": ScheduleLambdaFunctionDecisionAttributesTypeDef,
    },
    total=False,
)

class DecisionTypeDef(_RequiredDecisionTypeDef, _OptionalDecisionTypeDef):
    pass

WorkflowExecutionDetailTypeDef = TypedDict(
    "WorkflowExecutionDetailTypeDef",
    {
        "executionInfo": WorkflowExecutionInfoTypeDef,
        "executionConfiguration": WorkflowExecutionConfigurationTypeDef,
        "openCounts": WorkflowExecutionOpenCountsTypeDef,
        "latestActivityTaskTimestamp": datetime,
        "latestExecutionContext": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkflowExecutionInfosTypeDef = TypedDict(
    "WorkflowExecutionInfosTypeDef",
    {
        "executionInfos": List[WorkflowExecutionInfoTypeDef],
        "nextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredHistoryEventTypeDef = TypedDict(
    "_RequiredHistoryEventTypeDef",
    {
        "eventTimestamp": datetime,
        "eventType": EventTypeType,
        "eventId": int,
    },
)
_OptionalHistoryEventTypeDef = TypedDict(
    "_OptionalHistoryEventTypeDef",
    {
        "workflowExecutionStartedEventAttributes": WorkflowExecutionStartedEventAttributesTypeDef,
        "workflowExecutionCompletedEventAttributes": WorkflowExecutionCompletedEventAttributesTypeDef,
        "completeWorkflowExecutionFailedEventAttributes": CompleteWorkflowExecutionFailedEventAttributesTypeDef,
        "workflowExecutionFailedEventAttributes": WorkflowExecutionFailedEventAttributesTypeDef,
        "failWorkflowExecutionFailedEventAttributes": FailWorkflowExecutionFailedEventAttributesTypeDef,
        "workflowExecutionTimedOutEventAttributes": WorkflowExecutionTimedOutEventAttributesTypeDef,
        "workflowExecutionCanceledEventAttributes": WorkflowExecutionCanceledEventAttributesTypeDef,
        "cancelWorkflowExecutionFailedEventAttributes": CancelWorkflowExecutionFailedEventAttributesTypeDef,
        "workflowExecutionContinuedAsNewEventAttributes": WorkflowExecutionContinuedAsNewEventAttributesTypeDef,
        "continueAsNewWorkflowExecutionFailedEventAttributes": ContinueAsNewWorkflowExecutionFailedEventAttributesTypeDef,
        "workflowExecutionTerminatedEventAttributes": WorkflowExecutionTerminatedEventAttributesTypeDef,
        "workflowExecutionCancelRequestedEventAttributes": WorkflowExecutionCancelRequestedEventAttributesTypeDef,
        "decisionTaskScheduledEventAttributes": DecisionTaskScheduledEventAttributesTypeDef,
        "decisionTaskStartedEventAttributes": DecisionTaskStartedEventAttributesTypeDef,
        "decisionTaskCompletedEventAttributes": DecisionTaskCompletedEventAttributesTypeDef,
        "decisionTaskTimedOutEventAttributes": DecisionTaskTimedOutEventAttributesTypeDef,
        "activityTaskScheduledEventAttributes": ActivityTaskScheduledEventAttributesTypeDef,
        "activityTaskStartedEventAttributes": ActivityTaskStartedEventAttributesTypeDef,
        "activityTaskCompletedEventAttributes": ActivityTaskCompletedEventAttributesTypeDef,
        "activityTaskFailedEventAttributes": ActivityTaskFailedEventAttributesTypeDef,
        "activityTaskTimedOutEventAttributes": ActivityTaskTimedOutEventAttributesTypeDef,
        "activityTaskCanceledEventAttributes": ActivityTaskCanceledEventAttributesTypeDef,
        "activityTaskCancelRequestedEventAttributes": ActivityTaskCancelRequestedEventAttributesTypeDef,
        "workflowExecutionSignaledEventAttributes": WorkflowExecutionSignaledEventAttributesTypeDef,
        "markerRecordedEventAttributes": MarkerRecordedEventAttributesTypeDef,
        "recordMarkerFailedEventAttributes": RecordMarkerFailedEventAttributesTypeDef,
        "timerStartedEventAttributes": TimerStartedEventAttributesTypeDef,
        "timerFiredEventAttributes": TimerFiredEventAttributesTypeDef,
        "timerCanceledEventAttributes": TimerCanceledEventAttributesTypeDef,
        "startChildWorkflowExecutionInitiatedEventAttributes": StartChildWorkflowExecutionInitiatedEventAttributesTypeDef,
        "childWorkflowExecutionStartedEventAttributes": ChildWorkflowExecutionStartedEventAttributesTypeDef,
        "childWorkflowExecutionCompletedEventAttributes": ChildWorkflowExecutionCompletedEventAttributesTypeDef,
        "childWorkflowExecutionFailedEventAttributes": ChildWorkflowExecutionFailedEventAttributesTypeDef,
        "childWorkflowExecutionTimedOutEventAttributes": ChildWorkflowExecutionTimedOutEventAttributesTypeDef,
        "childWorkflowExecutionCanceledEventAttributes": ChildWorkflowExecutionCanceledEventAttributesTypeDef,
        "childWorkflowExecutionTerminatedEventAttributes": ChildWorkflowExecutionTerminatedEventAttributesTypeDef,
        "signalExternalWorkflowExecutionInitiatedEventAttributes": SignalExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
        "externalWorkflowExecutionSignaledEventAttributes": ExternalWorkflowExecutionSignaledEventAttributesTypeDef,
        "signalExternalWorkflowExecutionFailedEventAttributes": SignalExternalWorkflowExecutionFailedEventAttributesTypeDef,
        "externalWorkflowExecutionCancelRequestedEventAttributes": ExternalWorkflowExecutionCancelRequestedEventAttributesTypeDef,
        "requestCancelExternalWorkflowExecutionInitiatedEventAttributes": RequestCancelExternalWorkflowExecutionInitiatedEventAttributesTypeDef,
        "requestCancelExternalWorkflowExecutionFailedEventAttributes": RequestCancelExternalWorkflowExecutionFailedEventAttributesTypeDef,
        "scheduleActivityTaskFailedEventAttributes": ScheduleActivityTaskFailedEventAttributesTypeDef,
        "requestCancelActivityTaskFailedEventAttributes": RequestCancelActivityTaskFailedEventAttributesTypeDef,
        "startTimerFailedEventAttributes": StartTimerFailedEventAttributesTypeDef,
        "cancelTimerFailedEventAttributes": CancelTimerFailedEventAttributesTypeDef,
        "startChildWorkflowExecutionFailedEventAttributes": StartChildWorkflowExecutionFailedEventAttributesTypeDef,
        "lambdaFunctionScheduledEventAttributes": LambdaFunctionScheduledEventAttributesTypeDef,
        "lambdaFunctionStartedEventAttributes": LambdaFunctionStartedEventAttributesTypeDef,
        "lambdaFunctionCompletedEventAttributes": LambdaFunctionCompletedEventAttributesTypeDef,
        "lambdaFunctionFailedEventAttributes": LambdaFunctionFailedEventAttributesTypeDef,
        "lambdaFunctionTimedOutEventAttributes": LambdaFunctionTimedOutEventAttributesTypeDef,
        "scheduleLambdaFunctionFailedEventAttributes": ScheduleLambdaFunctionFailedEventAttributesTypeDef,
        "startLambdaFunctionFailedEventAttributes": StartLambdaFunctionFailedEventAttributesTypeDef,
    },
    total=False,
)

class HistoryEventTypeDef(_RequiredHistoryEventTypeDef, _OptionalHistoryEventTypeDef):
    pass

WorkflowTypeDetailTypeDef = TypedDict(
    "WorkflowTypeDetailTypeDef",
    {
        "typeInfo": WorkflowTypeInfoTypeDef,
        "configuration": WorkflowTypeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkflowTypeInfosTypeDef = TypedDict(
    "WorkflowTypeInfosTypeDef",
    {
        "typeInfos": List[WorkflowTypeInfoTypeDef],
        "nextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRespondDecisionTaskCompletedInputRequestTypeDef = TypedDict(
    "_RequiredRespondDecisionTaskCompletedInputRequestTypeDef",
    {
        "taskToken": str,
    },
)
_OptionalRespondDecisionTaskCompletedInputRequestTypeDef = TypedDict(
    "_OptionalRespondDecisionTaskCompletedInputRequestTypeDef",
    {
        "decisions": Sequence[DecisionTypeDef],
        "executionContext": str,
    },
    total=False,
)

class RespondDecisionTaskCompletedInputRequestTypeDef(
    _RequiredRespondDecisionTaskCompletedInputRequestTypeDef,
    _OptionalRespondDecisionTaskCompletedInputRequestTypeDef,
):
    pass

DecisionTaskTypeDef = TypedDict(
    "DecisionTaskTypeDef",
    {
        "taskToken": str,
        "startedEventId": int,
        "workflowExecution": WorkflowExecutionTypeDef,
        "workflowType": WorkflowTypeTypeDef,
        "events": List[HistoryEventTypeDef],
        "nextPageToken": str,
        "previousStartedEventId": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HistoryTypeDef = TypedDict(
    "HistoryTypeDef",
    {
        "events": List[HistoryEventTypeDef],
        "nextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
