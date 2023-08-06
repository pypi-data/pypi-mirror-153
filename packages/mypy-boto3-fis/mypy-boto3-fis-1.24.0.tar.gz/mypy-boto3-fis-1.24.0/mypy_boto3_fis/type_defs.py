"""
Type annotations for fis service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fis/type_defs/)

Usage::

    ```python
    from mypy_boto3_fis.type_defs import ActionParameterTypeDef

    data: ActionParameterTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ExperimentActionStatusType, ExperimentStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActionParameterTypeDef",
    "ActionTargetTypeDef",
    "CreateExperimentTemplateActionInputTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef",
    "ExperimentTemplateS3LogConfigurationInputTypeDef",
    "CreateExperimentTemplateStopConditionInputTypeDef",
    "ResponseMetadataTypeDef",
    "ExperimentTemplateTargetInputFilterTypeDef",
    "DeleteExperimentTemplateRequestRequestTypeDef",
    "ExperimentActionStateTypeDef",
    "ExperimentCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentS3LogConfigurationTypeDef",
    "ExperimentStateTypeDef",
    "ExperimentStopConditionTypeDef",
    "ExperimentTargetFilterTypeDef",
    "ExperimentTemplateActionTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentTemplateS3LogConfigurationTypeDef",
    "ExperimentTemplateStopConditionTypeDef",
    "ExperimentTemplateSummaryTypeDef",
    "ExperimentTemplateTargetFilterTypeDef",
    "GetActionRequestRequestTypeDef",
    "GetExperimentRequestRequestTypeDef",
    "GetExperimentTemplateRequestRequestTypeDef",
    "GetTargetResourceTypeRequestRequestTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListExperimentTemplatesRequestRequestTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTargetResourceTypesRequestRequestTypeDef",
    "TargetResourceTypeSummaryTypeDef",
    "StartExperimentRequestRequestTypeDef",
    "StopExperimentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetResourceTypeParameterTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExperimentTemplateActionInputItemTypeDef",
    "UpdateExperimentTemplateStopConditionInputTypeDef",
    "ActionSummaryTypeDef",
    "ActionTypeDef",
    "CreateExperimentTemplateLogConfigurationInputTypeDef",
    "UpdateExperimentTemplateLogConfigurationInputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateExperimentTemplateTargetInputTypeDef",
    "UpdateExperimentTemplateTargetInputTypeDef",
    "ExperimentActionTypeDef",
    "ExperimentLogConfigurationTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTargetTypeDef",
    "ExperimentTemplateLogConfigurationTypeDef",
    "ListExperimentTemplatesResponseTypeDef",
    "ExperimentTemplateTargetTypeDef",
    "ListTargetResourceTypesResponseTypeDef",
    "TargetResourceTypeTypeDef",
    "ListActionsResponseTypeDef",
    "GetActionResponseTypeDef",
    "CreateExperimentTemplateRequestRequestTypeDef",
    "UpdateExperimentTemplateRequestRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ExperimentTypeDef",
    "ExperimentTemplateTypeDef",
    "GetTargetResourceTypeResponseTypeDef",
    "GetExperimentResponseTypeDef",
    "StartExperimentResponseTypeDef",
    "StopExperimentResponseTypeDef",
    "CreateExperimentTemplateResponseTypeDef",
    "DeleteExperimentTemplateResponseTypeDef",
    "GetExperimentTemplateResponseTypeDef",
    "UpdateExperimentTemplateResponseTypeDef",
)

ActionParameterTypeDef = TypedDict(
    "ActionParameterTypeDef",
    {
        "description": str,
        "required": bool,
    },
    total=False,
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef",
    {
        "resourceType": str,
    },
    total=False,
)

_RequiredCreateExperimentTemplateActionInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateActionInputTypeDef",
    {
        "actionId": str,
    },
)
_OptionalCreateExperimentTemplateActionInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateActionInputTypeDef",
    {
        "description": str,
        "parameters": Mapping[str, str],
        "targets": Mapping[str, str],
        "startAfter": Sequence[str],
    },
    total=False,
)


class CreateExperimentTemplateActionInputTypeDef(
    _RequiredCreateExperimentTemplateActionInputTypeDef,
    _OptionalCreateExperimentTemplateActionInputTypeDef,
):
    pass


ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef = TypedDict(
    "ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef",
    {
        "logGroupArn": str,
    },
)

_RequiredExperimentTemplateS3LogConfigurationInputTypeDef = TypedDict(
    "_RequiredExperimentTemplateS3LogConfigurationInputTypeDef",
    {
        "bucketName": str,
    },
)
_OptionalExperimentTemplateS3LogConfigurationInputTypeDef = TypedDict(
    "_OptionalExperimentTemplateS3LogConfigurationInputTypeDef",
    {
        "prefix": str,
    },
    total=False,
)


class ExperimentTemplateS3LogConfigurationInputTypeDef(
    _RequiredExperimentTemplateS3LogConfigurationInputTypeDef,
    _OptionalExperimentTemplateS3LogConfigurationInputTypeDef,
):
    pass


_RequiredCreateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateStopConditionInputTypeDef",
    {
        "source": str,
    },
)
_OptionalCreateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateStopConditionInputTypeDef",
    {
        "value": str,
    },
    total=False,
)


class CreateExperimentTemplateStopConditionInputTypeDef(
    _RequiredCreateExperimentTemplateStopConditionInputTypeDef,
    _OptionalCreateExperimentTemplateStopConditionInputTypeDef,
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

ExperimentTemplateTargetInputFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetInputFilterTypeDef",
    {
        "path": str,
        "values": Sequence[str],
    },
)

DeleteExperimentTemplateRequestRequestTypeDef = TypedDict(
    "DeleteExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

ExperimentActionStateTypeDef = TypedDict(
    "ExperimentActionStateTypeDef",
    {
        "status": ExperimentActionStatusType,
        "reason": str,
    },
    total=False,
)

ExperimentCloudWatchLogsLogConfigurationTypeDef = TypedDict(
    "ExperimentCloudWatchLogsLogConfigurationTypeDef",
    {
        "logGroupArn": str,
    },
    total=False,
)

ExperimentS3LogConfigurationTypeDef = TypedDict(
    "ExperimentS3LogConfigurationTypeDef",
    {
        "bucketName": str,
        "prefix": str,
    },
    total=False,
)

ExperimentStateTypeDef = TypedDict(
    "ExperimentStateTypeDef",
    {
        "status": ExperimentStatusType,
        "reason": str,
    },
    total=False,
)

ExperimentStopConditionTypeDef = TypedDict(
    "ExperimentStopConditionTypeDef",
    {
        "source": str,
        "value": str,
    },
    total=False,
)

ExperimentTargetFilterTypeDef = TypedDict(
    "ExperimentTargetFilterTypeDef",
    {
        "path": str,
        "values": List[str],
    },
    total=False,
)

ExperimentTemplateActionTypeDef = TypedDict(
    "ExperimentTemplateActionTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
    },
    total=False,
)

ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef",
    {
        "logGroupArn": str,
    },
    total=False,
)

ExperimentTemplateS3LogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateS3LogConfigurationTypeDef",
    {
        "bucketName": str,
        "prefix": str,
    },
    total=False,
)

ExperimentTemplateStopConditionTypeDef = TypedDict(
    "ExperimentTemplateStopConditionTypeDef",
    {
        "source": str,
        "value": str,
    },
    total=False,
)

ExperimentTemplateSummaryTypeDef = TypedDict(
    "ExperimentTemplateSummaryTypeDef",
    {
        "id": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentTemplateTargetFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetFilterTypeDef",
    {
        "path": str,
        "values": List[str],
    },
    total=False,
)

GetActionRequestRequestTypeDef = TypedDict(
    "GetActionRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetExperimentRequestRequestTypeDef = TypedDict(
    "GetExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetExperimentTemplateRequestRequestTypeDef = TypedDict(
    "GetExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetTargetResourceTypeRequestRequestTypeDef = TypedDict(
    "GetTargetResourceTypeRequestRequestTypeDef",
    {
        "resourceType": str,
    },
)

ListActionsRequestRequestTypeDef = TypedDict(
    "ListActionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListExperimentTemplatesRequestRequestTypeDef = TypedDict(
    "ListExperimentTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListExperimentsRequestRequestTypeDef = TypedDict(
    "ListExperimentsRequestRequestTypeDef",
    {
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

ListTargetResourceTypesRequestRequestTypeDef = TypedDict(
    "ListTargetResourceTypesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

TargetResourceTypeSummaryTypeDef = TypedDict(
    "TargetResourceTypeSummaryTypeDef",
    {
        "resourceType": str,
        "description": str,
    },
    total=False,
)

_RequiredStartExperimentRequestRequestTypeDef = TypedDict(
    "_RequiredStartExperimentRequestRequestTypeDef",
    {
        "clientToken": str,
        "experimentTemplateId": str,
    },
)
_OptionalStartExperimentRequestRequestTypeDef = TypedDict(
    "_OptionalStartExperimentRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartExperimentRequestRequestTypeDef(
    _RequiredStartExperimentRequestRequestTypeDef, _OptionalStartExperimentRequestRequestTypeDef
):
    pass


StopExperimentRequestRequestTypeDef = TypedDict(
    "StopExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TargetResourceTypeParameterTypeDef = TypedDict(
    "TargetResourceTypeParameterTypeDef",
    {
        "description": str,
        "required": bool,
    },
    total=False,
)

_RequiredUntagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalUntagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUntagResourceRequestRequestTypeDef",
    {
        "tagKeys": Sequence[str],
    },
    total=False,
)


class UntagResourceRequestRequestTypeDef(
    _RequiredUntagResourceRequestRequestTypeDef, _OptionalUntagResourceRequestRequestTypeDef
):
    pass


UpdateExperimentTemplateActionInputItemTypeDef = TypedDict(
    "UpdateExperimentTemplateActionInputItemTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Mapping[str, str],
        "targets": Mapping[str, str],
        "startAfter": Sequence[str],
    },
    total=False,
)

_RequiredUpdateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_RequiredUpdateExperimentTemplateStopConditionInputTypeDef",
    {
        "source": str,
    },
)
_OptionalUpdateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "_OptionalUpdateExperimentTemplateStopConditionInputTypeDef",
    {
        "value": str,
    },
    total=False,
)


class UpdateExperimentTemplateStopConditionInputTypeDef(
    _RequiredUpdateExperimentTemplateStopConditionInputTypeDef,
    _OptionalUpdateExperimentTemplateStopConditionInputTypeDef,
):
    pass


ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "id": str,
        "description": str,
        "targets": Dict[str, ActionTargetTypeDef],
        "tags": Dict[str, str],
    },
    total=False,
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "id": str,
        "description": str,
        "parameters": Dict[str, ActionParameterTypeDef],
        "targets": Dict[str, ActionTargetTypeDef],
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredCreateExperimentTemplateLogConfigurationInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateLogConfigurationInputTypeDef",
    {
        "logSchemaVersion": int,
    },
)
_OptionalCreateExperimentTemplateLogConfigurationInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateLogConfigurationInputTypeDef",
    {
        "cloudWatchLogsConfiguration": ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef,
        "s3Configuration": ExperimentTemplateS3LogConfigurationInputTypeDef,
    },
    total=False,
)


class CreateExperimentTemplateLogConfigurationInputTypeDef(
    _RequiredCreateExperimentTemplateLogConfigurationInputTypeDef,
    _OptionalCreateExperimentTemplateLogConfigurationInputTypeDef,
):
    pass


UpdateExperimentTemplateLogConfigurationInputTypeDef = TypedDict(
    "UpdateExperimentTemplateLogConfigurationInputTypeDef",
    {
        "cloudWatchLogsConfiguration": ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef,
        "s3Configuration": ExperimentTemplateS3LogConfigurationInputTypeDef,
        "logSchemaVersion": int,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateTargetInputTypeDef",
    {
        "resourceType": str,
        "selectionMode": str,
    },
)
_OptionalCreateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateTargetInputTypeDef",
    {
        "resourceArns": Sequence[str],
        "resourceTags": Mapping[str, str],
        "filters": Sequence[ExperimentTemplateTargetInputFilterTypeDef],
        "parameters": Mapping[str, str],
    },
    total=False,
)


class CreateExperimentTemplateTargetInputTypeDef(
    _RequiredCreateExperimentTemplateTargetInputTypeDef,
    _OptionalCreateExperimentTemplateTargetInputTypeDef,
):
    pass


_RequiredUpdateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_RequiredUpdateExperimentTemplateTargetInputTypeDef",
    {
        "resourceType": str,
        "selectionMode": str,
    },
)
_OptionalUpdateExperimentTemplateTargetInputTypeDef = TypedDict(
    "_OptionalUpdateExperimentTemplateTargetInputTypeDef",
    {
        "resourceArns": Sequence[str],
        "resourceTags": Mapping[str, str],
        "filters": Sequence[ExperimentTemplateTargetInputFilterTypeDef],
        "parameters": Mapping[str, str],
    },
    total=False,
)


class UpdateExperimentTemplateTargetInputTypeDef(
    _RequiredUpdateExperimentTemplateTargetInputTypeDef,
    _OptionalUpdateExperimentTemplateTargetInputTypeDef,
):
    pass


ExperimentActionTypeDef = TypedDict(
    "ExperimentActionTypeDef",
    {
        "actionId": str,
        "description": str,
        "parameters": Dict[str, str],
        "targets": Dict[str, str],
        "startAfter": List[str],
        "state": ExperimentActionStateTypeDef,
        "startTime": datetime,
        "endTime": datetime,
    },
    total=False,
)

ExperimentLogConfigurationTypeDef = TypedDict(
    "ExperimentLogConfigurationTypeDef",
    {
        "cloudWatchLogsConfiguration": ExperimentCloudWatchLogsLogConfigurationTypeDef,
        "s3Configuration": ExperimentS3LogConfigurationTypeDef,
        "logSchemaVersion": int,
    },
    total=False,
)

ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "id": str,
        "experimentTemplateId": str,
        "state": ExperimentStateTypeDef,
        "creationTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

ExperimentTargetTypeDef = TypedDict(
    "ExperimentTargetTypeDef",
    {
        "resourceType": str,
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List[ExperimentTargetFilterTypeDef],
        "selectionMode": str,
        "parameters": Dict[str, str],
    },
    total=False,
)

ExperimentTemplateLogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateLogConfigurationTypeDef",
    {
        "cloudWatchLogsConfiguration": ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef,
        "s3Configuration": ExperimentTemplateS3LogConfigurationTypeDef,
        "logSchemaVersion": int,
    },
    total=False,
)

ListExperimentTemplatesResponseTypeDef = TypedDict(
    "ListExperimentTemplatesResponseTypeDef",
    {
        "experimentTemplates": List[ExperimentTemplateSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExperimentTemplateTargetTypeDef = TypedDict(
    "ExperimentTemplateTargetTypeDef",
    {
        "resourceType": str,
        "resourceArns": List[str],
        "resourceTags": Dict[str, str],
        "filters": List[ExperimentTemplateTargetFilterTypeDef],
        "selectionMode": str,
        "parameters": Dict[str, str],
    },
    total=False,
)

ListTargetResourceTypesResponseTypeDef = TypedDict(
    "ListTargetResourceTypesResponseTypeDef",
    {
        "targetResourceTypes": List[TargetResourceTypeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TargetResourceTypeTypeDef = TypedDict(
    "TargetResourceTypeTypeDef",
    {
        "resourceType": str,
        "description": str,
        "parameters": Dict[str, TargetResourceTypeParameterTypeDef],
    },
    total=False,
)

ListActionsResponseTypeDef = TypedDict(
    "ListActionsResponseTypeDef",
    {
        "actions": List[ActionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetActionResponseTypeDef = TypedDict(
    "GetActionResponseTypeDef",
    {
        "action": ActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExperimentTemplateRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "stopConditions": Sequence[CreateExperimentTemplateStopConditionInputTypeDef],
        "actions": Mapping[str, CreateExperimentTemplateActionInputTypeDef],
        "roleArn": str,
    },
)
_OptionalCreateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExperimentTemplateRequestRequestTypeDef",
    {
        "targets": Mapping[str, CreateExperimentTemplateTargetInputTypeDef],
        "tags": Mapping[str, str],
        "logConfiguration": CreateExperimentTemplateLogConfigurationInputTypeDef,
    },
    total=False,
)


class CreateExperimentTemplateRequestRequestTypeDef(
    _RequiredCreateExperimentTemplateRequestRequestTypeDef,
    _OptionalCreateExperimentTemplateRequestRequestTypeDef,
):
    pass


_RequiredUpdateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateExperimentTemplateRequestRequestTypeDef",
    {
        "description": str,
        "stopConditions": Sequence[UpdateExperimentTemplateStopConditionInputTypeDef],
        "targets": Mapping[str, UpdateExperimentTemplateTargetInputTypeDef],
        "actions": Mapping[str, UpdateExperimentTemplateActionInputItemTypeDef],
        "roleArn": str,
        "logConfiguration": UpdateExperimentTemplateLogConfigurationInputTypeDef,
    },
    total=False,
)


class UpdateExperimentTemplateRequestRequestTypeDef(
    _RequiredUpdateExperimentTemplateRequestRequestTypeDef,
    _OptionalUpdateExperimentTemplateRequestRequestTypeDef,
):
    pass


ListExperimentsResponseTypeDef = TypedDict(
    "ListExperimentsResponseTypeDef",
    {
        "experiments": List[ExperimentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "id": str,
        "experimentTemplateId": str,
        "roleArn": str,
        "state": ExperimentStateTypeDef,
        "targets": Dict[str, ExperimentTargetTypeDef],
        "actions": Dict[str, ExperimentActionTypeDef],
        "stopConditions": List[ExperimentStopConditionTypeDef],
        "creationTime": datetime,
        "startTime": datetime,
        "endTime": datetime,
        "tags": Dict[str, str],
        "logConfiguration": ExperimentLogConfigurationTypeDef,
    },
    total=False,
)

ExperimentTemplateTypeDef = TypedDict(
    "ExperimentTemplateTypeDef",
    {
        "id": str,
        "description": str,
        "targets": Dict[str, ExperimentTemplateTargetTypeDef],
        "actions": Dict[str, ExperimentTemplateActionTypeDef],
        "stopConditions": List[ExperimentTemplateStopConditionTypeDef],
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "roleArn": str,
        "tags": Dict[str, str],
        "logConfiguration": ExperimentTemplateLogConfigurationTypeDef,
    },
    total=False,
)

GetTargetResourceTypeResponseTypeDef = TypedDict(
    "GetTargetResourceTypeResponseTypeDef",
    {
        "targetResourceType": TargetResourceTypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExperimentResponseTypeDef = TypedDict(
    "GetExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartExperimentResponseTypeDef = TypedDict(
    "StartExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopExperimentResponseTypeDef = TypedDict(
    "StopExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExperimentTemplateResponseTypeDef = TypedDict(
    "CreateExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteExperimentTemplateResponseTypeDef = TypedDict(
    "DeleteExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExperimentTemplateResponseTypeDef = TypedDict(
    "GetExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateExperimentTemplateResponseTypeDef = TypedDict(
    "UpdateExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
