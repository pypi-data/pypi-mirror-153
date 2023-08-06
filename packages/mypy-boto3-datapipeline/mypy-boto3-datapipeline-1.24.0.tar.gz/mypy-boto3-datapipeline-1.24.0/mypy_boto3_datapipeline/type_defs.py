"""
Type annotations for datapipeline service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/type_defs/)

Usage::

    ```python
    from mypy_boto3_datapipeline.type_defs import ParameterValueTypeDef

    data: ParameterValueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import OperatorTypeType, TaskStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ParameterValueTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeactivatePipelineInputRequestTypeDef",
    "DeletePipelineInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeObjectsInputRequestTypeDef",
    "DescribePipelinesInputRequestTypeDef",
    "EvaluateExpressionInputRequestTypeDef",
    "FieldTypeDef",
    "GetPipelineDefinitionInputRequestTypeDef",
    "InstanceIdentityTypeDef",
    "ListPipelinesInputRequestTypeDef",
    "PipelineIdNameTypeDef",
    "OperatorTypeDef",
    "ParameterAttributeTypeDef",
    "ValidationErrorTypeDef",
    "ValidationWarningTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "ReportTaskRunnerHeartbeatInputRequestTypeDef",
    "SetStatusInputRequestTypeDef",
    "SetTaskStatusInputRequestTypeDef",
    "ActivatePipelineInputRequestTypeDef",
    "AddTagsInputRequestTypeDef",
    "CreatePipelineInputRequestTypeDef",
    "CreatePipelineOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EvaluateExpressionOutputTypeDef",
    "QueryObjectsOutputTypeDef",
    "ReportTaskProgressOutputTypeDef",
    "ReportTaskRunnerHeartbeatOutputTypeDef",
    "DescribeObjectsInputDescribeObjectsPaginateTypeDef",
    "ListPipelinesInputListPipelinesPaginateTypeDef",
    "PipelineDescriptionTypeDef",
    "PipelineObjectTypeDef",
    "ReportTaskProgressInputRequestTypeDef",
    "PollForTaskInputRequestTypeDef",
    "ListPipelinesOutputTypeDef",
    "SelectorTypeDef",
    "ParameterObjectTypeDef",
    "PutPipelineDefinitionOutputTypeDef",
    "ValidatePipelineDefinitionOutputTypeDef",
    "DescribePipelinesOutputTypeDef",
    "DescribeObjectsOutputTypeDef",
    "TaskObjectTypeDef",
    "QueryTypeDef",
    "GetPipelineDefinitionOutputTypeDef",
    "PutPipelineDefinitionInputRequestTypeDef",
    "ValidatePipelineDefinitionInputRequestTypeDef",
    "PollForTaskOutputTypeDef",
    "QueryObjectsInputQueryObjectsPaginateTypeDef",
    "QueryObjectsInputRequestTypeDef",
)

ParameterValueTypeDef = TypedDict(
    "ParameterValueTypeDef",
    {
        "id": str,
        "stringValue": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
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

_RequiredDeactivatePipelineInputRequestTypeDef = TypedDict(
    "_RequiredDeactivatePipelineInputRequestTypeDef",
    {
        "pipelineId": str,
    },
)
_OptionalDeactivatePipelineInputRequestTypeDef = TypedDict(
    "_OptionalDeactivatePipelineInputRequestTypeDef",
    {
        "cancelActive": bool,
    },
    total=False,
)


class DeactivatePipelineInputRequestTypeDef(
    _RequiredDeactivatePipelineInputRequestTypeDef, _OptionalDeactivatePipelineInputRequestTypeDef
):
    pass


DeletePipelineInputRequestTypeDef = TypedDict(
    "DeletePipelineInputRequestTypeDef",
    {
        "pipelineId": str,
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

_RequiredDescribeObjectsInputRequestTypeDef = TypedDict(
    "_RequiredDescribeObjectsInputRequestTypeDef",
    {
        "pipelineId": str,
        "objectIds": Sequence[str],
    },
)
_OptionalDescribeObjectsInputRequestTypeDef = TypedDict(
    "_OptionalDescribeObjectsInputRequestTypeDef",
    {
        "evaluateExpressions": bool,
        "marker": str,
    },
    total=False,
)


class DescribeObjectsInputRequestTypeDef(
    _RequiredDescribeObjectsInputRequestTypeDef, _OptionalDescribeObjectsInputRequestTypeDef
):
    pass


DescribePipelinesInputRequestTypeDef = TypedDict(
    "DescribePipelinesInputRequestTypeDef",
    {
        "pipelineIds": Sequence[str],
    },
)

EvaluateExpressionInputRequestTypeDef = TypedDict(
    "EvaluateExpressionInputRequestTypeDef",
    {
        "pipelineId": str,
        "objectId": str,
        "expression": str,
    },
)

_RequiredFieldTypeDef = TypedDict(
    "_RequiredFieldTypeDef",
    {
        "key": str,
    },
)
_OptionalFieldTypeDef = TypedDict(
    "_OptionalFieldTypeDef",
    {
        "stringValue": str,
        "refValue": str,
    },
    total=False,
)


class FieldTypeDef(_RequiredFieldTypeDef, _OptionalFieldTypeDef):
    pass


_RequiredGetPipelineDefinitionInputRequestTypeDef = TypedDict(
    "_RequiredGetPipelineDefinitionInputRequestTypeDef",
    {
        "pipelineId": str,
    },
)
_OptionalGetPipelineDefinitionInputRequestTypeDef = TypedDict(
    "_OptionalGetPipelineDefinitionInputRequestTypeDef",
    {
        "version": str,
    },
    total=False,
)


class GetPipelineDefinitionInputRequestTypeDef(
    _RequiredGetPipelineDefinitionInputRequestTypeDef,
    _OptionalGetPipelineDefinitionInputRequestTypeDef,
):
    pass


InstanceIdentityTypeDef = TypedDict(
    "InstanceIdentityTypeDef",
    {
        "document": str,
        "signature": str,
    },
    total=False,
)

ListPipelinesInputRequestTypeDef = TypedDict(
    "ListPipelinesInputRequestTypeDef",
    {
        "marker": str,
    },
    total=False,
)

PipelineIdNameTypeDef = TypedDict(
    "PipelineIdNameTypeDef",
    {
        "id": str,
        "name": str,
    },
    total=False,
)

OperatorTypeDef = TypedDict(
    "OperatorTypeDef",
    {
        "type": OperatorTypeType,
        "values": Sequence[str],
    },
    total=False,
)

ParameterAttributeTypeDef = TypedDict(
    "ParameterAttributeTypeDef",
    {
        "key": str,
        "stringValue": str,
    },
)

ValidationErrorTypeDef = TypedDict(
    "ValidationErrorTypeDef",
    {
        "id": str,
        "errors": List[str],
    },
    total=False,
)

ValidationWarningTypeDef = TypedDict(
    "ValidationWarningTypeDef",
    {
        "id": str,
        "warnings": List[str],
    },
    total=False,
)

RemoveTagsInputRequestTypeDef = TypedDict(
    "RemoveTagsInputRequestTypeDef",
    {
        "pipelineId": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredReportTaskRunnerHeartbeatInputRequestTypeDef = TypedDict(
    "_RequiredReportTaskRunnerHeartbeatInputRequestTypeDef",
    {
        "taskrunnerId": str,
    },
)
_OptionalReportTaskRunnerHeartbeatInputRequestTypeDef = TypedDict(
    "_OptionalReportTaskRunnerHeartbeatInputRequestTypeDef",
    {
        "workerGroup": str,
        "hostname": str,
    },
    total=False,
)


class ReportTaskRunnerHeartbeatInputRequestTypeDef(
    _RequiredReportTaskRunnerHeartbeatInputRequestTypeDef,
    _OptionalReportTaskRunnerHeartbeatInputRequestTypeDef,
):
    pass


SetStatusInputRequestTypeDef = TypedDict(
    "SetStatusInputRequestTypeDef",
    {
        "pipelineId": str,
        "objectIds": Sequence[str],
        "status": str,
    },
)

_RequiredSetTaskStatusInputRequestTypeDef = TypedDict(
    "_RequiredSetTaskStatusInputRequestTypeDef",
    {
        "taskId": str,
        "taskStatus": TaskStatusType,
    },
)
_OptionalSetTaskStatusInputRequestTypeDef = TypedDict(
    "_OptionalSetTaskStatusInputRequestTypeDef",
    {
        "errorId": str,
        "errorMessage": str,
        "errorStackTrace": str,
    },
    total=False,
)


class SetTaskStatusInputRequestTypeDef(
    _RequiredSetTaskStatusInputRequestTypeDef, _OptionalSetTaskStatusInputRequestTypeDef
):
    pass


_RequiredActivatePipelineInputRequestTypeDef = TypedDict(
    "_RequiredActivatePipelineInputRequestTypeDef",
    {
        "pipelineId": str,
    },
)
_OptionalActivatePipelineInputRequestTypeDef = TypedDict(
    "_OptionalActivatePipelineInputRequestTypeDef",
    {
        "parameterValues": Sequence[ParameterValueTypeDef],
        "startTimestamp": Union[datetime, str],
    },
    total=False,
)


class ActivatePipelineInputRequestTypeDef(
    _RequiredActivatePipelineInputRequestTypeDef, _OptionalActivatePipelineInputRequestTypeDef
):
    pass


AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "pipelineId": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredCreatePipelineInputRequestTypeDef = TypedDict(
    "_RequiredCreatePipelineInputRequestTypeDef",
    {
        "name": str,
        "uniqueId": str,
    },
)
_OptionalCreatePipelineInputRequestTypeDef = TypedDict(
    "_OptionalCreatePipelineInputRequestTypeDef",
    {
        "description": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePipelineInputRequestTypeDef(
    _RequiredCreatePipelineInputRequestTypeDef, _OptionalCreatePipelineInputRequestTypeDef
):
    pass


CreatePipelineOutputTypeDef = TypedDict(
    "CreatePipelineOutputTypeDef",
    {
        "pipelineId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EvaluateExpressionOutputTypeDef = TypedDict(
    "EvaluateExpressionOutputTypeDef",
    {
        "evaluatedExpression": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

QueryObjectsOutputTypeDef = TypedDict(
    "QueryObjectsOutputTypeDef",
    {
        "ids": List[str],
        "marker": str,
        "hasMoreResults": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReportTaskProgressOutputTypeDef = TypedDict(
    "ReportTaskProgressOutputTypeDef",
    {
        "canceled": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReportTaskRunnerHeartbeatOutputTypeDef = TypedDict(
    "ReportTaskRunnerHeartbeatOutputTypeDef",
    {
        "terminate": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeObjectsInputDescribeObjectsPaginateTypeDef = TypedDict(
    "_RequiredDescribeObjectsInputDescribeObjectsPaginateTypeDef",
    {
        "pipelineId": str,
        "objectIds": Sequence[str],
    },
)
_OptionalDescribeObjectsInputDescribeObjectsPaginateTypeDef = TypedDict(
    "_OptionalDescribeObjectsInputDescribeObjectsPaginateTypeDef",
    {
        "evaluateExpressions": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeObjectsInputDescribeObjectsPaginateTypeDef(
    _RequiredDescribeObjectsInputDescribeObjectsPaginateTypeDef,
    _OptionalDescribeObjectsInputDescribeObjectsPaginateTypeDef,
):
    pass


ListPipelinesInputListPipelinesPaginateTypeDef = TypedDict(
    "ListPipelinesInputListPipelinesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredPipelineDescriptionTypeDef = TypedDict(
    "_RequiredPipelineDescriptionTypeDef",
    {
        "pipelineId": str,
        "name": str,
        "fields": List[FieldTypeDef],
    },
)
_OptionalPipelineDescriptionTypeDef = TypedDict(
    "_OptionalPipelineDescriptionTypeDef",
    {
        "description": str,
        "tags": List[TagTypeDef],
    },
    total=False,
)


class PipelineDescriptionTypeDef(
    _RequiredPipelineDescriptionTypeDef, _OptionalPipelineDescriptionTypeDef
):
    pass


PipelineObjectTypeDef = TypedDict(
    "PipelineObjectTypeDef",
    {
        "id": str,
        "name": str,
        "fields": List[FieldTypeDef],
    },
)

_RequiredReportTaskProgressInputRequestTypeDef = TypedDict(
    "_RequiredReportTaskProgressInputRequestTypeDef",
    {
        "taskId": str,
    },
)
_OptionalReportTaskProgressInputRequestTypeDef = TypedDict(
    "_OptionalReportTaskProgressInputRequestTypeDef",
    {
        "fields": Sequence[FieldTypeDef],
    },
    total=False,
)


class ReportTaskProgressInputRequestTypeDef(
    _RequiredReportTaskProgressInputRequestTypeDef, _OptionalReportTaskProgressInputRequestTypeDef
):
    pass


_RequiredPollForTaskInputRequestTypeDef = TypedDict(
    "_RequiredPollForTaskInputRequestTypeDef",
    {
        "workerGroup": str,
    },
)
_OptionalPollForTaskInputRequestTypeDef = TypedDict(
    "_OptionalPollForTaskInputRequestTypeDef",
    {
        "hostname": str,
        "instanceIdentity": InstanceIdentityTypeDef,
    },
    total=False,
)


class PollForTaskInputRequestTypeDef(
    _RequiredPollForTaskInputRequestTypeDef, _OptionalPollForTaskInputRequestTypeDef
):
    pass


ListPipelinesOutputTypeDef = TypedDict(
    "ListPipelinesOutputTypeDef",
    {
        "pipelineIdList": List[PipelineIdNameTypeDef],
        "marker": str,
        "hasMoreResults": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SelectorTypeDef = TypedDict(
    "SelectorTypeDef",
    {
        "fieldName": str,
        "operator": OperatorTypeDef,
    },
    total=False,
)

ParameterObjectTypeDef = TypedDict(
    "ParameterObjectTypeDef",
    {
        "id": str,
        "attributes": List[ParameterAttributeTypeDef],
    },
)

PutPipelineDefinitionOutputTypeDef = TypedDict(
    "PutPipelineDefinitionOutputTypeDef",
    {
        "validationErrors": List[ValidationErrorTypeDef],
        "validationWarnings": List[ValidationWarningTypeDef],
        "errored": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidatePipelineDefinitionOutputTypeDef = TypedDict(
    "ValidatePipelineDefinitionOutputTypeDef",
    {
        "validationErrors": List[ValidationErrorTypeDef],
        "validationWarnings": List[ValidationWarningTypeDef],
        "errored": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePipelinesOutputTypeDef = TypedDict(
    "DescribePipelinesOutputTypeDef",
    {
        "pipelineDescriptionList": List[PipelineDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeObjectsOutputTypeDef = TypedDict(
    "DescribeObjectsOutputTypeDef",
    {
        "pipelineObjects": List[PipelineObjectTypeDef],
        "marker": str,
        "hasMoreResults": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TaskObjectTypeDef = TypedDict(
    "TaskObjectTypeDef",
    {
        "taskId": str,
        "pipelineId": str,
        "attemptId": str,
        "objects": Dict[str, PipelineObjectTypeDef],
    },
    total=False,
)

QueryTypeDef = TypedDict(
    "QueryTypeDef",
    {
        "selectors": Sequence[SelectorTypeDef],
    },
    total=False,
)

GetPipelineDefinitionOutputTypeDef = TypedDict(
    "GetPipelineDefinitionOutputTypeDef",
    {
        "pipelineObjects": List[PipelineObjectTypeDef],
        "parameterObjects": List[ParameterObjectTypeDef],
        "parameterValues": List[ParameterValueTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutPipelineDefinitionInputRequestTypeDef = TypedDict(
    "_RequiredPutPipelineDefinitionInputRequestTypeDef",
    {
        "pipelineId": str,
        "pipelineObjects": Sequence[PipelineObjectTypeDef],
    },
)
_OptionalPutPipelineDefinitionInputRequestTypeDef = TypedDict(
    "_OptionalPutPipelineDefinitionInputRequestTypeDef",
    {
        "parameterObjects": Sequence[ParameterObjectTypeDef],
        "parameterValues": Sequence[ParameterValueTypeDef],
    },
    total=False,
)


class PutPipelineDefinitionInputRequestTypeDef(
    _RequiredPutPipelineDefinitionInputRequestTypeDef,
    _OptionalPutPipelineDefinitionInputRequestTypeDef,
):
    pass


_RequiredValidatePipelineDefinitionInputRequestTypeDef = TypedDict(
    "_RequiredValidatePipelineDefinitionInputRequestTypeDef",
    {
        "pipelineId": str,
        "pipelineObjects": Sequence[PipelineObjectTypeDef],
    },
)
_OptionalValidatePipelineDefinitionInputRequestTypeDef = TypedDict(
    "_OptionalValidatePipelineDefinitionInputRequestTypeDef",
    {
        "parameterObjects": Sequence[ParameterObjectTypeDef],
        "parameterValues": Sequence[ParameterValueTypeDef],
    },
    total=False,
)


class ValidatePipelineDefinitionInputRequestTypeDef(
    _RequiredValidatePipelineDefinitionInputRequestTypeDef,
    _OptionalValidatePipelineDefinitionInputRequestTypeDef,
):
    pass


PollForTaskOutputTypeDef = TypedDict(
    "PollForTaskOutputTypeDef",
    {
        "taskObject": TaskObjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredQueryObjectsInputQueryObjectsPaginateTypeDef = TypedDict(
    "_RequiredQueryObjectsInputQueryObjectsPaginateTypeDef",
    {
        "pipelineId": str,
        "sphere": str,
    },
)
_OptionalQueryObjectsInputQueryObjectsPaginateTypeDef = TypedDict(
    "_OptionalQueryObjectsInputQueryObjectsPaginateTypeDef",
    {
        "query": QueryTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class QueryObjectsInputQueryObjectsPaginateTypeDef(
    _RequiredQueryObjectsInputQueryObjectsPaginateTypeDef,
    _OptionalQueryObjectsInputQueryObjectsPaginateTypeDef,
):
    pass


_RequiredQueryObjectsInputRequestTypeDef = TypedDict(
    "_RequiredQueryObjectsInputRequestTypeDef",
    {
        "pipelineId": str,
        "sphere": str,
    },
)
_OptionalQueryObjectsInputRequestTypeDef = TypedDict(
    "_OptionalQueryObjectsInputRequestTypeDef",
    {
        "query": QueryTypeDef,
        "marker": str,
        "limit": int,
    },
    total=False,
)


class QueryObjectsInputRequestTypeDef(
    _RequiredQueryObjectsInputRequestTypeDef, _OptionalQueryObjectsInputRequestTypeDef
):
    pass
