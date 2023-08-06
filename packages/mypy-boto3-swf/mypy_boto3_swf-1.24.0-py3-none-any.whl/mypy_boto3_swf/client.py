"""
Type annotations for swf service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_swf.client import SWFClient

    session = Session()
    client: SWFClient = session.client("swf")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ChildPolicyType, RegistrationStatusType
from .paginator import (
    GetWorkflowExecutionHistoryPaginator,
    ListActivityTypesPaginator,
    ListClosedWorkflowExecutionsPaginator,
    ListDomainsPaginator,
    ListOpenWorkflowExecutionsPaginator,
    ListWorkflowTypesPaginator,
    PollForDecisionTaskPaginator,
)
from .type_defs import (
    ActivityTaskStatusTypeDef,
    ActivityTaskTypeDef,
    ActivityTypeDetailTypeDef,
    ActivityTypeInfosTypeDef,
    ActivityTypeTypeDef,
    CloseStatusFilterTypeDef,
    DecisionTaskTypeDef,
    DecisionTypeDef,
    DomainDetailTypeDef,
    DomainInfosTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecutionTimeFilterTypeDef,
    HistoryTypeDef,
    ListTagsForResourceOutputTypeDef,
    PendingTaskCountTypeDef,
    ResourceTagTypeDef,
    RunTypeDef,
    TagFilterTypeDef,
    TaskListTypeDef,
    WorkflowExecutionCountTypeDef,
    WorkflowExecutionDetailTypeDef,
    WorkflowExecutionFilterTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowExecutionTypeDef,
    WorkflowTypeDetailTypeDef,
    WorkflowTypeFilterTypeDef,
    WorkflowTypeInfosTypeDef,
    WorkflowTypeTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SWFClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DefaultUndefinedFault: Type[BotocoreClientError]
    DomainAlreadyExistsFault: Type[BotocoreClientError]
    DomainDeprecatedFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    OperationNotPermittedFault: Type[BotocoreClientError]
    TooManyTagsFault: Type[BotocoreClientError]
    TypeAlreadyExistsFault: Type[BotocoreClientError]
    TypeDeprecatedFault: Type[BotocoreClientError]
    UnknownResourceFault: Type[BotocoreClientError]
    WorkflowExecutionAlreadyStartedFault: Type[BotocoreClientError]


class SWFClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SWFClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#can_paginate)
        """

    def count_closed_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: ExecutionTimeFilterTypeDef = ...,
        closeTimeFilter: ExecutionTimeFilterTypeDef = ...,
        executionFilter: WorkflowExecutionFilterTypeDef = ...,
        typeFilter: WorkflowTypeFilterTypeDef = ...,
        tagFilter: TagFilterTypeDef = ...,
        closeStatusFilter: CloseStatusFilterTypeDef = ...
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of closed workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_closed_workflow_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#count_closed_workflow_executions)
        """

    def count_open_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: ExecutionTimeFilterTypeDef,
        typeFilter: WorkflowTypeFilterTypeDef = ...,
        tagFilter: TagFilterTypeDef = ...,
        executionFilter: WorkflowExecutionFilterTypeDef = ...
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of open workflow executions within the given domain that meet
        the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_open_workflow_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#count_open_workflow_executions)
        """

    def count_pending_activity_tasks(
        self, *, domain: str, taskList: TaskListTypeDef
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of activity tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_pending_activity_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#count_pending_activity_tasks)
        """

    def count_pending_decision_tasks(
        self, *, domain: str, taskList: TaskListTypeDef
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of decision tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_pending_decision_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#count_pending_decision_tasks)
        """

    def deprecate_activity_type(
        self, *, domain: str, activityType: ActivityTypeTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified *activity type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_activity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#deprecate_activity_type)
        """

    def deprecate_domain(self, *, name: str) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#deprecate_domain)
        """

    def deprecate_workflow_type(
        self, *, domain: str, workflowType: WorkflowTypeTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_workflow_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#deprecate_workflow_type)
        """

    def describe_activity_type(
        self, *, domain: str, activityType: ActivityTypeTypeDef
    ) -> ActivityTypeDetailTypeDef:
        """
        Returns information about the specified activity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_activity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#describe_activity_type)
        """

    def describe_domain(self, *, name: str) -> DomainDetailTypeDef:
        """
        Returns information about the specified domain, including description and
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#describe_domain)
        """

    def describe_workflow_execution(
        self, *, domain: str, execution: WorkflowExecutionTypeDef
    ) -> WorkflowExecutionDetailTypeDef:
        """
        Returns information about the specified workflow execution including its type
        and some statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_workflow_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#describe_workflow_execution)
        """

    def describe_workflow_type(
        self, *, domain: str, workflowType: WorkflowTypeTypeDef
    ) -> WorkflowTypeDetailTypeDef:
        """
        Returns information about the specified *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_workflow_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#describe_workflow_type)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#generate_presigned_url)
        """

    def get_workflow_execution_history(
        self,
        *,
        domain: str,
        execution: WorkflowExecutionTypeDef,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> HistoryTypeDef:
        """
        Returns the history of the specified workflow execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_workflow_execution_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_workflow_execution_history)
        """

    def list_activity_types(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> ActivityTypeInfosTypeDef:
        """
        Returns information about all activities registered in the specified domain that
        match the specified name and registration status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_activity_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_activity_types)
        """

    def list_closed_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: ExecutionTimeFilterTypeDef = ...,
        closeTimeFilter: ExecutionTimeFilterTypeDef = ...,
        executionFilter: WorkflowExecutionFilterTypeDef = ...,
        closeStatusFilter: CloseStatusFilterTypeDef = ...,
        typeFilter: WorkflowTypeFilterTypeDef = ...,
        tagFilter: TagFilterTypeDef = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of closed workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_closed_workflow_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_closed_workflow_executions)
        """

    def list_domains(
        self,
        *,
        registrationStatus: RegistrationStatusType,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> DomainInfosTypeDef:
        """
        Returns the list of domains registered in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_domains)
        """

    def list_open_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: ExecutionTimeFilterTypeDef,
        typeFilter: WorkflowTypeFilterTypeDef = ...,
        tagFilter: TagFilterTypeDef = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...,
        executionFilter: WorkflowExecutionFilterTypeDef = ...
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of open workflow executions in the specified domain that meet the
        filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_open_workflow_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_open_workflow_executions)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a given domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_tags_for_resource)
        """

    def list_workflow_types(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> WorkflowTypeInfosTypeDef:
        """
        Returns information about workflow types in the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_workflow_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#list_workflow_types)
        """

    def poll_for_activity_task(
        self, *, domain: str, taskList: TaskListTypeDef, identity: str = ...
    ) -> ActivityTaskTypeDef:
        """
        Used by workers to get an  ActivityTask from the specified activity `taskList`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.poll_for_activity_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#poll_for_activity_task)
        """

    def poll_for_decision_task(
        self,
        *,
        domain: str,
        taskList: TaskListTypeDef,
        identity: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> DecisionTaskTypeDef:
        """
        Used by deciders to get a  DecisionTask from the specified decision `taskList`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.poll_for_decision_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#poll_for_decision_task)
        """

    def record_activity_task_heartbeat(
        self, *, taskToken: str, details: str = ...
    ) -> ActivityTaskStatusTypeDef:
        """
        Used by activity workers to report to the service that the  ActivityTask
        represented by the specified `taskToken` is still making progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.record_activity_task_heartbeat)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#record_activity_task_heartbeat)
        """

    def register_activity_type(
        self,
        *,
        domain: str,
        name: str,
        version: str,
        description: str = ...,
        defaultTaskStartToCloseTimeout: str = ...,
        defaultTaskHeartbeatTimeout: str = ...,
        defaultTaskList: TaskListTypeDef = ...,
        defaultTaskPriority: str = ...,
        defaultTaskScheduleToStartTimeout: str = ...,
        defaultTaskScheduleToCloseTimeout: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new *activity type* along with its configuration settings in the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_activity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#register_activity_type)
        """

    def register_domain(
        self,
        *,
        name: str,
        workflowExecutionRetentionPeriodInDays: str,
        description: str = ...,
        tags: Sequence[ResourceTagTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#register_domain)
        """

    def register_workflow_type(
        self,
        *,
        domain: str,
        name: str,
        version: str,
        description: str = ...,
        defaultTaskStartToCloseTimeout: str = ...,
        defaultExecutionStartToCloseTimeout: str = ...,
        defaultTaskList: TaskListTypeDef = ...,
        defaultTaskPriority: str = ...,
        defaultChildPolicy: ChildPolicyType = ...,
        defaultLambdaRole: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new *workflow type* and its configuration settings in the specified
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_workflow_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#register_workflow_type)
        """

    def request_cancel_workflow_execution(
        self, *, domain: str, workflowId: str, runId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a `WorkflowExecutionCancelRequested` event in the currently running
        workflow execution identified by the given domain, workflowId, and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.request_cancel_workflow_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#request_cancel_workflow_execution)
        """

    def respond_activity_task_canceled(
        self, *, taskToken: str, details: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` was successfully canceled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_canceled)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#respond_activity_task_canceled)
        """

    def respond_activity_task_completed(
        self, *, taskToken: str, result: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` completed successfully with a `result` (if provided).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_completed)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#respond_activity_task_completed)
        """

    def respond_activity_task_failed(
        self, *, taskToken: str, reason: str = ..., details: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` has failed with `reason` (if specified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_failed)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#respond_activity_task_failed)
        """

    def respond_decision_task_completed(
        self,
        *,
        taskToken: str,
        decisions: Sequence[DecisionTypeDef] = ...,
        executionContext: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by deciders to tell the service that the  DecisionTask identified by the
        `taskToken` has successfully completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_decision_task_completed)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#respond_decision_task_completed)
        """

    def signal_workflow_execution(
        self, *, domain: str, workflowId: str, signalName: str, runId: str = ..., input: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a `WorkflowExecutionSignaled` event in the workflow execution history
        and creates a decision task for the workflow execution identified by the given
        domain, workflowId and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.signal_workflow_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#signal_workflow_execution)
        """

    def start_workflow_execution(
        self,
        *,
        domain: str,
        workflowId: str,
        workflowType: WorkflowTypeTypeDef,
        taskList: TaskListTypeDef = ...,
        taskPriority: str = ...,
        input: str = ...,
        executionStartToCloseTimeout: str = ...,
        tagList: Sequence[str] = ...,
        taskStartToCloseTimeout: str = ...,
        childPolicy: ChildPolicyType = ...,
        lambdaRole: str = ...
    ) -> RunTypeDef:
        """
        Starts an execution of the workflow type in the specified domain using the
        provided `workflowId` and input data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.start_workflow_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#start_workflow_execution)
        """

    def tag_resource(
        self, *, resourceArn: str, tags: Sequence[ResourceTagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#tag_resource)
        """

    def terminate_workflow_execution(
        self,
        *,
        domain: str,
        workflowId: str,
        runId: str = ...,
        reason: str = ...,
        details: str = ...,
        childPolicy: ChildPolicyType = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a `WorkflowExecutionTerminated` event and forces closure of the workflow
        execution identified by the given domain, runId, and workflowId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.terminate_workflow_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#terminate_workflow_execution)
        """

    def undeprecate_activity_type(
        self, *, domain: str, activityType: ActivityTypeTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated *activity type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_activity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#undeprecate_activity_type)
        """

    def undeprecate_domain(self, *, name: str) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#undeprecate_domain)
        """

    def undeprecate_workflow_type(
        self, *, domain: str, workflowType: WorkflowTypeTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_workflow_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#undeprecate_workflow_type)
        """

    def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a tag from a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_workflow_execution_history"]
    ) -> GetWorkflowExecutionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_activity_types"]
    ) -> ListActivityTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_closed_workflow_executions"]
    ) -> ListClosedWorkflowExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_open_workflow_executions"]
    ) -> ListOpenWorkflowExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workflow_types"]
    ) -> ListWorkflowTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["poll_for_decision_task"]
    ) -> PollForDecisionTaskPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_swf/client/#get_paginator)
        """
