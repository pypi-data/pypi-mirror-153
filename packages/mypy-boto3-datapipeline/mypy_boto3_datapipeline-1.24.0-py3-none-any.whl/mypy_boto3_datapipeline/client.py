"""
Type annotations for datapipeline service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_datapipeline.client import DataPipelineClient

    session = Session()
    client: DataPipelineClient = session.client("datapipeline")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import TaskStatusType
from .paginator import DescribeObjectsPaginator, ListPipelinesPaginator, QueryObjectsPaginator
from .type_defs import (
    CreatePipelineOutputTypeDef,
    DescribeObjectsOutputTypeDef,
    DescribePipelinesOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluateExpressionOutputTypeDef,
    FieldTypeDef,
    GetPipelineDefinitionOutputTypeDef,
    InstanceIdentityTypeDef,
    ListPipelinesOutputTypeDef,
    ParameterObjectTypeDef,
    ParameterValueTypeDef,
    PipelineObjectTypeDef,
    PollForTaskOutputTypeDef,
    PutPipelineDefinitionOutputTypeDef,
    QueryObjectsOutputTypeDef,
    QueryTypeDef,
    ReportTaskProgressOutputTypeDef,
    ReportTaskRunnerHeartbeatOutputTypeDef,
    TagTypeDef,
    ValidatePipelineDefinitionOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DataPipelineClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    PipelineDeletedException: Type[BotocoreClientError]
    PipelineNotFoundException: Type[BotocoreClientError]
    TaskNotFoundException: Type[BotocoreClientError]


class DataPipelineClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataPipelineClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#exceptions)
        """

    def activate_pipeline(
        self,
        *,
        pipelineId: str,
        parameterValues: Sequence[ParameterValueTypeDef] = ...,
        startTimestamp: Union[datetime, str] = ...
    ) -> Dict[str, Any]:
        """
        Validates the specified pipeline and starts processing pipeline tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.activate_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#activate_pipeline)
        """

    def add_tags(self, *, pipelineId: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds or modifies tags for the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#add_tags)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#can_paginate)
        """

    def create_pipeline(
        self, *, name: str, uniqueId: str, description: str = ..., tags: Sequence[TagTypeDef] = ...
    ) -> CreatePipelineOutputTypeDef:
        """
        Creates a new, empty pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.create_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#create_pipeline)
        """

    def deactivate_pipeline(self, *, pipelineId: str, cancelActive: bool = ...) -> Dict[str, Any]:
        """
        Deactivates the specified running pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.deactivate_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#deactivate_pipeline)
        """

    def delete_pipeline(self, *, pipelineId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a pipeline, its pipeline definition, and its run history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.delete_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#delete_pipeline)
        """

    def describe_objects(
        self,
        *,
        pipelineId: str,
        objectIds: Sequence[str],
        evaluateExpressions: bool = ...,
        marker: str = ...
    ) -> DescribeObjectsOutputTypeDef:
        """
        Gets the object definitions for a set of objects associated with the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.describe_objects)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#describe_objects)
        """

    def describe_pipelines(self, *, pipelineIds: Sequence[str]) -> DescribePipelinesOutputTypeDef:
        """
        Retrieves metadata about one or more pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.describe_pipelines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#describe_pipelines)
        """

    def evaluate_expression(
        self, *, pipelineId: str, objectId: str, expression: str
    ) -> EvaluateExpressionOutputTypeDef:
        """
        Task runners call `EvaluateExpression` to evaluate a string in the context of
        the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.evaluate_expression)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#evaluate_expression)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#generate_presigned_url)
        """

    def get_pipeline_definition(
        self, *, pipelineId: str, version: str = ...
    ) -> GetPipelineDefinitionOutputTypeDef:
        """
        Gets the definition of the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.get_pipeline_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#get_pipeline_definition)
        """

    def list_pipelines(self, *, marker: str = ...) -> ListPipelinesOutputTypeDef:
        """
        Lists the pipeline identifiers for all active pipelines that you have permission
        to access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.list_pipelines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#list_pipelines)
        """

    def poll_for_task(
        self,
        *,
        workerGroup: str,
        hostname: str = ...,
        instanceIdentity: InstanceIdentityTypeDef = ...
    ) -> PollForTaskOutputTypeDef:
        """
        Task runners call `PollForTask` to receive a task to perform from AWS Data
        Pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.poll_for_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#poll_for_task)
        """

    def put_pipeline_definition(
        self,
        *,
        pipelineId: str,
        pipelineObjects: Sequence[PipelineObjectTypeDef],
        parameterObjects: Sequence[ParameterObjectTypeDef] = ...,
        parameterValues: Sequence[ParameterValueTypeDef] = ...
    ) -> PutPipelineDefinitionOutputTypeDef:
        """
        Adds tasks, schedules, and preconditions to the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.put_pipeline_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#put_pipeline_definition)
        """

    def query_objects(
        self,
        *,
        pipelineId: str,
        sphere: str,
        query: QueryTypeDef = ...,
        marker: str = ...,
        limit: int = ...
    ) -> QueryObjectsOutputTypeDef:
        """
        Queries the specified pipeline for the names of objects that match the specified
        set of conditions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.query_objects)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#query_objects)
        """

    def remove_tags(self, *, pipelineId: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes existing tags from the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#remove_tags)
        """

    def report_task_progress(
        self, *, taskId: str, fields: Sequence[FieldTypeDef] = ...
    ) -> ReportTaskProgressOutputTypeDef:
        """
        Task runners call `ReportTaskProgress` when assigned a task to acknowledge that
        it has the task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.report_task_progress)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#report_task_progress)
        """

    def report_task_runner_heartbeat(
        self, *, taskrunnerId: str, workerGroup: str = ..., hostname: str = ...
    ) -> ReportTaskRunnerHeartbeatOutputTypeDef:
        """
        Task runners call `ReportTaskRunnerHeartbeat` every 15 minutes to indicate that
        they are operational.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.report_task_runner_heartbeat)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#report_task_runner_heartbeat)
        """

    def set_status(
        self, *, pipelineId: str, objectIds: Sequence[str], status: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Requests that the status of the specified physical or logical pipeline objects
        be updated in the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.set_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#set_status)
        """

    def set_task_status(
        self,
        *,
        taskId: str,
        taskStatus: TaskStatusType,
        errorId: str = ...,
        errorMessage: str = ...,
        errorStackTrace: str = ...
    ) -> Dict[str, Any]:
        """
        Task runners call `SetTaskStatus` to notify AWS Data Pipeline that a task is
        completed and provide information about the final status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.set_task_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#set_task_status)
        """

    def validate_pipeline_definition(
        self,
        *,
        pipelineId: str,
        pipelineObjects: Sequence[PipelineObjectTypeDef],
        parameterObjects: Sequence[ParameterObjectTypeDef] = ...,
        parameterValues: Sequence[ParameterValueTypeDef] = ...
    ) -> ValidatePipelineDefinitionOutputTypeDef:
        """
        Validates the specified pipeline definition to ensure that it is well formed and
        can be run without error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.validate_pipeline_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#validate_pipeline_definition)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_objects"]
    ) -> DescribeObjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_objects"]) -> QueryObjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/client/#get_paginator)
        """
