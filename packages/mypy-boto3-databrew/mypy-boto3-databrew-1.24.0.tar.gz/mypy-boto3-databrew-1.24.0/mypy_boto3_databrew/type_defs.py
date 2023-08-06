"""
Type annotations for databrew service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/type_defs/)

Usage::

    ```python
    from mypy_boto3_databrew.type_defs import AllowedStatisticsTypeDef

    data: AllowedStatisticsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AnalyticsModeType,
    CompressionFormatType,
    EncryptionModeType,
    InputFormatType,
    JobRunStateType,
    JobTypeType,
    LogSubscriptionType,
    OrderType,
    OutputFormatType,
    ParameterTypeType,
    SampleModeType,
    SampleTypeType,
    SessionStatusType,
    SourceType,
    ThresholdTypeType,
    ThresholdUnitType,
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
    "AllowedStatisticsTypeDef",
    "BatchDeleteRecipeVersionRequestRequestTypeDef",
    "RecipeVersionErrorDetailTypeDef",
    "ResponseMetadataTypeDef",
    "ColumnSelectorTypeDef",
    "ConditionExpressionTypeDef",
    "JobSampleTypeDef",
    "S3LocationTypeDef",
    "ValidationConfigurationTypeDef",
    "SampleTypeDef",
    "RecipeReferenceTypeDef",
    "CreateScheduleRequestRequestTypeDef",
    "CsvOptionsTypeDef",
    "CsvOutputOptionsTypeDef",
    "DatetimeOptionsTypeDef",
    "FilterExpressionTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteRecipeVersionRequestRequestTypeDef",
    "DeleteRulesetRequestRequestTypeDef",
    "DeleteScheduleRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeJobRunRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeRecipeRequestRequestTypeDef",
    "DescribeRulesetRequestRequestTypeDef",
    "DescribeScheduleRequestRequestTypeDef",
    "ExcelOptionsTypeDef",
    "FilesLimitTypeDef",
    "JsonOptionsTypeDef",
    "MetadataTypeDef",
    "PaginatorConfigTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListJobRunsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListRecipeVersionsRequestRequestTypeDef",
    "ListRecipesRequestRequestTypeDef",
    "ListRulesetsRequestRequestTypeDef",
    "RulesetItemTypeDef",
    "ListSchedulesRequestRequestTypeDef",
    "ScheduleTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PublishRecipeRequestRequestTypeDef",
    "RecipeActionTypeDef",
    "ThresholdTypeDef",
    "ViewFrameTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "StartProjectSessionRequestRequestTypeDef",
    "StatisticOverrideTypeDef",
    "StopJobRunRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateScheduleRequestRequestTypeDef",
    "EntityDetectorConfigurationTypeDef",
    "BatchDeleteRecipeVersionResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateProfileJobResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateRecipeJobResponseTypeDef",
    "CreateRecipeResponseTypeDef",
    "CreateRulesetResponseTypeDef",
    "CreateScheduleResponseTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DeleteJobResponseTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteRecipeVersionResponseTypeDef",
    "DeleteRulesetResponseTypeDef",
    "DeleteScheduleResponseTypeDef",
    "DescribeScheduleResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PublishRecipeResponseTypeDef",
    "SendProjectSessionActionResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "StartProjectSessionResponseTypeDef",
    "StopJobRunResponseTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateProfileJobResponseTypeDef",
    "UpdateProjectResponseTypeDef",
    "UpdateRecipeJobResponseTypeDef",
    "UpdateRecipeResponseTypeDef",
    "UpdateRulesetResponseTypeDef",
    "UpdateScheduleResponseTypeDef",
    "DataCatalogInputDefinitionTypeDef",
    "DatabaseInputDefinitionTypeDef",
    "DatabaseTableOutputOptionsTypeDef",
    "S3TableOutputOptionsTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "ProjectTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "OutputFormatOptionsTypeDef",
    "DatasetParameterTypeDef",
    "FormatOptionsTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListJobRunsRequestListJobRunsPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef",
    "ListRecipesRequestListRecipesPaginateTypeDef",
    "ListRulesetsRequestListRulesetsPaginateTypeDef",
    "ListSchedulesRequestListSchedulesPaginateTypeDef",
    "ListRulesetsResponseTypeDef",
    "ListSchedulesResponseTypeDef",
    "RecipeStepTypeDef",
    "RuleTypeDef",
    "StatisticsConfigurationTypeDef",
    "InputTypeDef",
    "DatabaseOutputTypeDef",
    "DataCatalogOutputTypeDef",
    "ListProjectsResponseTypeDef",
    "OutputTypeDef",
    "PathOptionsTypeDef",
    "CreateRecipeRequestRequestTypeDef",
    "DescribeRecipeResponseTypeDef",
    "RecipeTypeDef",
    "SendProjectSessionActionRequestRequestTypeDef",
    "UpdateRecipeRequestRequestTypeDef",
    "CreateRulesetRequestRequestTypeDef",
    "DescribeRulesetResponseTypeDef",
    "UpdateRulesetRequestRequestTypeDef",
    "ColumnStatisticsConfigurationTypeDef",
    "CreateRecipeJobRequestRequestTypeDef",
    "JobRunTypeDef",
    "JobTypeDef",
    "UpdateRecipeJobRequestRequestTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "DatasetTypeDef",
    "DescribeDatasetResponseTypeDef",
    "UpdateDatasetRequestRequestTypeDef",
    "ListRecipeVersionsResponseTypeDef",
    "ListRecipesResponseTypeDef",
    "ProfileConfigurationTypeDef",
    "ListJobRunsResponseTypeDef",
    "ListJobsResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "CreateProfileJobRequestRequestTypeDef",
    "DescribeJobResponseTypeDef",
    "DescribeJobRunResponseTypeDef",
    "UpdateProfileJobRequestRequestTypeDef",
)

AllowedStatisticsTypeDef = TypedDict(
    "AllowedStatisticsTypeDef",
    {
        "Statistics": Sequence[str],
    },
)

BatchDeleteRecipeVersionRequestRequestTypeDef = TypedDict(
    "BatchDeleteRecipeVersionRequestRequestTypeDef",
    {
        "Name": str,
        "RecipeVersions": Sequence[str],
    },
)

RecipeVersionErrorDetailTypeDef = TypedDict(
    "RecipeVersionErrorDetailTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
        "RecipeVersion": str,
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

ColumnSelectorTypeDef = TypedDict(
    "ColumnSelectorTypeDef",
    {
        "Regex": str,
        "Name": str,
    },
    total=False,
)

_RequiredConditionExpressionTypeDef = TypedDict(
    "_RequiredConditionExpressionTypeDef",
    {
        "Condition": str,
        "TargetColumn": str,
    },
)
_OptionalConditionExpressionTypeDef = TypedDict(
    "_OptionalConditionExpressionTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class ConditionExpressionTypeDef(
    _RequiredConditionExpressionTypeDef, _OptionalConditionExpressionTypeDef
):
    pass


JobSampleTypeDef = TypedDict(
    "JobSampleTypeDef",
    {
        "Mode": SampleModeType,
        "Size": int,
    },
    total=False,
)

_RequiredS3LocationTypeDef = TypedDict(
    "_RequiredS3LocationTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalS3LocationTypeDef = TypedDict(
    "_OptionalS3LocationTypeDef",
    {
        "Key": str,
        "BucketOwner": str,
    },
    total=False,
)


class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass


_RequiredValidationConfigurationTypeDef = TypedDict(
    "_RequiredValidationConfigurationTypeDef",
    {
        "RulesetArn": str,
    },
)
_OptionalValidationConfigurationTypeDef = TypedDict(
    "_OptionalValidationConfigurationTypeDef",
    {
        "ValidationMode": Literal["CHECK_ALL"],
    },
    total=False,
)


class ValidationConfigurationTypeDef(
    _RequiredValidationConfigurationTypeDef, _OptionalValidationConfigurationTypeDef
):
    pass


_RequiredSampleTypeDef = TypedDict(
    "_RequiredSampleTypeDef",
    {
        "Type": SampleTypeType,
    },
)
_OptionalSampleTypeDef = TypedDict(
    "_OptionalSampleTypeDef",
    {
        "Size": int,
    },
    total=False,
)


class SampleTypeDef(_RequiredSampleTypeDef, _OptionalSampleTypeDef):
    pass


_RequiredRecipeReferenceTypeDef = TypedDict(
    "_RequiredRecipeReferenceTypeDef",
    {
        "Name": str,
    },
)
_OptionalRecipeReferenceTypeDef = TypedDict(
    "_OptionalRecipeReferenceTypeDef",
    {
        "RecipeVersion": str,
    },
    total=False,
)


class RecipeReferenceTypeDef(_RequiredRecipeReferenceTypeDef, _OptionalRecipeReferenceTypeDef):
    pass


_RequiredCreateScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateScheduleRequestRequestTypeDef",
    {
        "CronExpression": str,
        "Name": str,
    },
)
_OptionalCreateScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateScheduleRequestRequestTypeDef",
    {
        "JobNames": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateScheduleRequestRequestTypeDef(
    _RequiredCreateScheduleRequestRequestTypeDef, _OptionalCreateScheduleRequestRequestTypeDef
):
    pass


CsvOptionsTypeDef = TypedDict(
    "CsvOptionsTypeDef",
    {
        "Delimiter": str,
        "HeaderRow": bool,
    },
    total=False,
)

CsvOutputOptionsTypeDef = TypedDict(
    "CsvOutputOptionsTypeDef",
    {
        "Delimiter": str,
    },
    total=False,
)

_RequiredDatetimeOptionsTypeDef = TypedDict(
    "_RequiredDatetimeOptionsTypeDef",
    {
        "Format": str,
    },
)
_OptionalDatetimeOptionsTypeDef = TypedDict(
    "_OptionalDatetimeOptionsTypeDef",
    {
        "TimezoneOffset": str,
        "LocaleCode": str,
    },
    total=False,
)


class DatetimeOptionsTypeDef(_RequiredDatetimeOptionsTypeDef, _OptionalDatetimeOptionsTypeDef):
    pass


FilterExpressionTypeDef = TypedDict(
    "FilterExpressionTypeDef",
    {
        "Expression": str,
        "ValuesMap": Mapping[str, str],
    },
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteRecipeVersionRequestRequestTypeDef = TypedDict(
    "DeleteRecipeVersionRequestRequestTypeDef",
    {
        "Name": str,
        "RecipeVersion": str,
    },
)

DeleteRulesetRequestRequestTypeDef = TypedDict(
    "DeleteRulesetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteScheduleRequestRequestTypeDef = TypedDict(
    "DeleteScheduleRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeJobRequestRequestTypeDef = TypedDict(
    "DescribeJobRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeJobRunRequestRequestTypeDef = TypedDict(
    "DescribeJobRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDescribeRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRecipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDescribeRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRecipeRequestRequestTypeDef",
    {
        "RecipeVersion": str,
    },
    total=False,
)


class DescribeRecipeRequestRequestTypeDef(
    _RequiredDescribeRecipeRequestRequestTypeDef, _OptionalDescribeRecipeRequestRequestTypeDef
):
    pass


DescribeRulesetRequestRequestTypeDef = TypedDict(
    "DescribeRulesetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeScheduleRequestRequestTypeDef = TypedDict(
    "DescribeScheduleRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ExcelOptionsTypeDef = TypedDict(
    "ExcelOptionsTypeDef",
    {
        "SheetNames": Sequence[str],
        "SheetIndexes": Sequence[int],
        "HeaderRow": bool,
    },
    total=False,
)

_RequiredFilesLimitTypeDef = TypedDict(
    "_RequiredFilesLimitTypeDef",
    {
        "MaxFiles": int,
    },
)
_OptionalFilesLimitTypeDef = TypedDict(
    "_OptionalFilesLimitTypeDef",
    {
        "OrderedBy": Literal["LAST_MODIFIED_DATE"],
        "Order": OrderType,
    },
    total=False,
)


class FilesLimitTypeDef(_RequiredFilesLimitTypeDef, _OptionalFilesLimitTypeDef):
    pass


JsonOptionsTypeDef = TypedDict(
    "JsonOptionsTypeDef",
    {
        "MultiLine": bool,
    },
    total=False,
)

MetadataTypeDef = TypedDict(
    "MetadataTypeDef",
    {
        "SourceArn": str,
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

ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListJobRunsRequestRequestTypeDef = TypedDict(
    "_RequiredListJobRunsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalListJobRunsRequestRequestTypeDef = TypedDict(
    "_OptionalListJobRunsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListJobRunsRequestRequestTypeDef(
    _RequiredListJobRunsRequestRequestTypeDef, _OptionalListJobRunsRequestRequestTypeDef
):
    pass


ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "DatasetName": str,
        "MaxResults": int,
        "NextToken": str,
        "ProjectName": str,
    },
    total=False,
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListRecipeVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListRecipeVersionsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalListRecipeVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListRecipeVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListRecipeVersionsRequestRequestTypeDef(
    _RequiredListRecipeVersionsRequestRequestTypeDef,
    _OptionalListRecipeVersionsRequestRequestTypeDef,
):
    pass


ListRecipesRequestRequestTypeDef = TypedDict(
    "ListRecipesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "RecipeVersion": str,
    },
    total=False,
)

ListRulesetsRequestRequestTypeDef = TypedDict(
    "ListRulesetsRequestRequestTypeDef",
    {
        "TargetArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredRulesetItemTypeDef = TypedDict(
    "_RequiredRulesetItemTypeDef",
    {
        "Name": str,
        "TargetArn": str,
    },
)
_OptionalRulesetItemTypeDef = TypedDict(
    "_OptionalRulesetItemTypeDef",
    {
        "AccountId": str,
        "CreatedBy": str,
        "CreateDate": datetime,
        "Description": str,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ResourceArn": str,
        "RuleCount": int,
        "Tags": Dict[str, str],
    },
    total=False,
)


class RulesetItemTypeDef(_RequiredRulesetItemTypeDef, _OptionalRulesetItemTypeDef):
    pass


ListSchedulesRequestRequestTypeDef = TypedDict(
    "ListSchedulesRequestRequestTypeDef",
    {
        "JobName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredScheduleTypeDef = TypedDict(
    "_RequiredScheduleTypeDef",
    {
        "Name": str,
    },
)
_OptionalScheduleTypeDef = TypedDict(
    "_OptionalScheduleTypeDef",
    {
        "AccountId": str,
        "CreatedBy": str,
        "CreateDate": datetime,
        "JobNames": List[str],
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ResourceArn": str,
        "CronExpression": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ScheduleTypeDef(_RequiredScheduleTypeDef, _OptionalScheduleTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredPublishRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredPublishRecipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalPublishRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalPublishRecipeRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class PublishRecipeRequestRequestTypeDef(
    _RequiredPublishRecipeRequestRequestTypeDef, _OptionalPublishRecipeRequestRequestTypeDef
):
    pass


_RequiredRecipeActionTypeDef = TypedDict(
    "_RequiredRecipeActionTypeDef",
    {
        "Operation": str,
    },
)
_OptionalRecipeActionTypeDef = TypedDict(
    "_OptionalRecipeActionTypeDef",
    {
        "Parameters": Mapping[str, str],
    },
    total=False,
)


class RecipeActionTypeDef(_RequiredRecipeActionTypeDef, _OptionalRecipeActionTypeDef):
    pass


_RequiredThresholdTypeDef = TypedDict(
    "_RequiredThresholdTypeDef",
    {
        "Value": float,
    },
)
_OptionalThresholdTypeDef = TypedDict(
    "_OptionalThresholdTypeDef",
    {
        "Type": ThresholdTypeType,
        "Unit": ThresholdUnitType,
    },
    total=False,
)


class ThresholdTypeDef(_RequiredThresholdTypeDef, _OptionalThresholdTypeDef):
    pass


_RequiredViewFrameTypeDef = TypedDict(
    "_RequiredViewFrameTypeDef",
    {
        "StartColumnIndex": int,
    },
)
_OptionalViewFrameTypeDef = TypedDict(
    "_OptionalViewFrameTypeDef",
    {
        "ColumnRange": int,
        "HiddenColumns": Sequence[str],
        "StartRowIndex": int,
        "RowRange": int,
        "Analytics": AnalyticsModeType,
    },
    total=False,
)


class ViewFrameTypeDef(_RequiredViewFrameTypeDef, _OptionalViewFrameTypeDef):
    pass


StartJobRunRequestRequestTypeDef = TypedDict(
    "StartJobRunRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredStartProjectSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStartProjectSessionRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartProjectSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStartProjectSessionRequestRequestTypeDef",
    {
        "AssumeControl": bool,
    },
    total=False,
)


class StartProjectSessionRequestRequestTypeDef(
    _RequiredStartProjectSessionRequestRequestTypeDef,
    _OptionalStartProjectSessionRequestRequestTypeDef,
):
    pass


StatisticOverrideTypeDef = TypedDict(
    "StatisticOverrideTypeDef",
    {
        "Statistic": str,
        "Parameters": Mapping[str, str],
    },
)

StopJobRunRequestRequestTypeDef = TypedDict(
    "StopJobRunRequestRequestTypeDef",
    {
        "Name": str,
        "RunId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateScheduleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateScheduleRequestRequestTypeDef",
    {
        "CronExpression": str,
        "Name": str,
    },
)
_OptionalUpdateScheduleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateScheduleRequestRequestTypeDef",
    {
        "JobNames": Sequence[str],
    },
    total=False,
)


class UpdateScheduleRequestRequestTypeDef(
    _RequiredUpdateScheduleRequestRequestTypeDef, _OptionalUpdateScheduleRequestRequestTypeDef
):
    pass


_RequiredEntityDetectorConfigurationTypeDef = TypedDict(
    "_RequiredEntityDetectorConfigurationTypeDef",
    {
        "EntityTypes": Sequence[str],
    },
)
_OptionalEntityDetectorConfigurationTypeDef = TypedDict(
    "_OptionalEntityDetectorConfigurationTypeDef",
    {
        "AllowedStatistics": Sequence[AllowedStatisticsTypeDef],
    },
    total=False,
)


class EntityDetectorConfigurationTypeDef(
    _RequiredEntityDetectorConfigurationTypeDef, _OptionalEntityDetectorConfigurationTypeDef
):
    pass


BatchDeleteRecipeVersionResponseTypeDef = TypedDict(
    "BatchDeleteRecipeVersionResponseTypeDef",
    {
        "Name": str,
        "Errors": List[RecipeVersionErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProfileJobResponseTypeDef = TypedDict(
    "CreateProfileJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecipeJobResponseTypeDef = TypedDict(
    "CreateRecipeJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecipeResponseTypeDef = TypedDict(
    "CreateRecipeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRulesetResponseTypeDef = TypedDict(
    "CreateRulesetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateScheduleResponseTypeDef = TypedDict(
    "CreateScheduleResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDatasetResponseTypeDef = TypedDict(
    "DeleteDatasetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJobResponseTypeDef = TypedDict(
    "DeleteJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRecipeVersionResponseTypeDef = TypedDict(
    "DeleteRecipeVersionResponseTypeDef",
    {
        "Name": str,
        "RecipeVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRulesetResponseTypeDef = TypedDict(
    "DeleteRulesetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteScheduleResponseTypeDef = TypedDict(
    "DeleteScheduleResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeScheduleResponseTypeDef = TypedDict(
    "DescribeScheduleResponseTypeDef",
    {
        "CreateDate": datetime,
        "CreatedBy": str,
        "JobNames": List[str],
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ResourceArn": str,
        "CronExpression": str,
        "Tags": Dict[str, str],
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishRecipeResponseTypeDef = TypedDict(
    "PublishRecipeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendProjectSessionActionResponseTypeDef = TypedDict(
    "SendProjectSessionActionResponseTypeDef",
    {
        "Result": str,
        "Name": str,
        "ActionId": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartJobRunResponseTypeDef = TypedDict(
    "StartJobRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartProjectSessionResponseTypeDef = TypedDict(
    "StartProjectSessionResponseTypeDef",
    {
        "Name": str,
        "ClientSessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopJobRunResponseTypeDef = TypedDict(
    "StopJobRunResponseTypeDef",
    {
        "RunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDatasetResponseTypeDef = TypedDict(
    "UpdateDatasetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProfileJobResponseTypeDef = TypedDict(
    "UpdateProfileJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProjectResponseTypeDef = TypedDict(
    "UpdateProjectResponseTypeDef",
    {
        "LastModifiedDate": datetime,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRecipeJobResponseTypeDef = TypedDict(
    "UpdateRecipeJobResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRecipeResponseTypeDef = TypedDict(
    "UpdateRecipeResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRulesetResponseTypeDef = TypedDict(
    "UpdateRulesetResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateScheduleResponseTypeDef = TypedDict(
    "UpdateScheduleResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDataCatalogInputDefinitionTypeDef = TypedDict(
    "_RequiredDataCatalogInputDefinitionTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalDataCatalogInputDefinitionTypeDef = TypedDict(
    "_OptionalDataCatalogInputDefinitionTypeDef",
    {
        "CatalogId": str,
        "TempDirectory": S3LocationTypeDef,
    },
    total=False,
)


class DataCatalogInputDefinitionTypeDef(
    _RequiredDataCatalogInputDefinitionTypeDef, _OptionalDataCatalogInputDefinitionTypeDef
):
    pass


_RequiredDatabaseInputDefinitionTypeDef = TypedDict(
    "_RequiredDatabaseInputDefinitionTypeDef",
    {
        "GlueConnectionName": str,
    },
)
_OptionalDatabaseInputDefinitionTypeDef = TypedDict(
    "_OptionalDatabaseInputDefinitionTypeDef",
    {
        "DatabaseTableName": str,
        "TempDirectory": S3LocationTypeDef,
        "QueryString": str,
    },
    total=False,
)


class DatabaseInputDefinitionTypeDef(
    _RequiredDatabaseInputDefinitionTypeDef, _OptionalDatabaseInputDefinitionTypeDef
):
    pass


_RequiredDatabaseTableOutputOptionsTypeDef = TypedDict(
    "_RequiredDatabaseTableOutputOptionsTypeDef",
    {
        "TableName": str,
    },
)
_OptionalDatabaseTableOutputOptionsTypeDef = TypedDict(
    "_OptionalDatabaseTableOutputOptionsTypeDef",
    {
        "TempDirectory": S3LocationTypeDef,
    },
    total=False,
)


class DatabaseTableOutputOptionsTypeDef(
    _RequiredDatabaseTableOutputOptionsTypeDef, _OptionalDatabaseTableOutputOptionsTypeDef
):
    pass


S3TableOutputOptionsTypeDef = TypedDict(
    "S3TableOutputOptionsTypeDef",
    {
        "Location": S3LocationTypeDef,
    },
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "DatasetName": str,
        "Name": str,
        "RecipeName": str,
        "RoleArn": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "Sample": SampleTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "CreateDate": datetime,
        "CreatedBy": str,
        "DatasetName": str,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "Name": str,
        "RecipeName": str,
        "ResourceArn": str,
        "Sample": SampleTypeDef,
        "RoleArn": str,
        "Tags": Dict[str, str],
        "SessionStatus": SessionStatusType,
        "OpenedBy": str,
        "OpenDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredProjectTypeDef = TypedDict(
    "_RequiredProjectTypeDef",
    {
        "Name": str,
        "RecipeName": str,
    },
)
_OptionalProjectTypeDef = TypedDict(
    "_OptionalProjectTypeDef",
    {
        "AccountId": str,
        "CreateDate": datetime,
        "CreatedBy": str,
        "DatasetName": str,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "ResourceArn": str,
        "Sample": SampleTypeDef,
        "Tags": Dict[str, str],
        "RoleArn": str,
        "OpenedBy": str,
        "OpenDate": datetime,
    },
    total=False,
)


class ProjectTypeDef(_RequiredProjectTypeDef, _OptionalProjectTypeDef):
    pass


_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "RoleArn": str,
        "Name": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "Sample": SampleTypeDef,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


OutputFormatOptionsTypeDef = TypedDict(
    "OutputFormatOptionsTypeDef",
    {
        "Csv": CsvOutputOptionsTypeDef,
    },
    total=False,
)

_RequiredDatasetParameterTypeDef = TypedDict(
    "_RequiredDatasetParameterTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
    },
)
_OptionalDatasetParameterTypeDef = TypedDict(
    "_OptionalDatasetParameterTypeDef",
    {
        "DatetimeOptions": DatetimeOptionsTypeDef,
        "CreateColumn": bool,
        "Filter": FilterExpressionTypeDef,
    },
    total=False,
)


class DatasetParameterTypeDef(_RequiredDatasetParameterTypeDef, _OptionalDatasetParameterTypeDef):
    pass


FormatOptionsTypeDef = TypedDict(
    "FormatOptionsTypeDef",
    {
        "Json": JsonOptionsTypeDef,
        "Excel": ExcelOptionsTypeDef,
        "Csv": CsvOptionsTypeDef,
    },
    total=False,
)

ListDatasetsRequestListDatasetsPaginateTypeDef = TypedDict(
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListJobRunsRequestListJobRunsPaginateTypeDef = TypedDict(
    "_RequiredListJobRunsRequestListJobRunsPaginateTypeDef",
    {
        "Name": str,
    },
)
_OptionalListJobRunsRequestListJobRunsPaginateTypeDef = TypedDict(
    "_OptionalListJobRunsRequestListJobRunsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListJobRunsRequestListJobRunsPaginateTypeDef(
    _RequiredListJobRunsRequestListJobRunsPaginateTypeDef,
    _OptionalListJobRunsRequestListJobRunsPaginateTypeDef,
):
    pass


ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "DatasetName": str,
        "ProjectName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef = TypedDict(
    "_RequiredListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef",
    {
        "Name": str,
    },
)
_OptionalListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef = TypedDict(
    "_OptionalListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef(
    _RequiredListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef,
    _OptionalListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef,
):
    pass


ListRecipesRequestListRecipesPaginateTypeDef = TypedDict(
    "ListRecipesRequestListRecipesPaginateTypeDef",
    {
        "RecipeVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRulesetsRequestListRulesetsPaginateTypeDef = TypedDict(
    "ListRulesetsRequestListRulesetsPaginateTypeDef",
    {
        "TargetArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSchedulesRequestListSchedulesPaginateTypeDef = TypedDict(
    "ListSchedulesRequestListSchedulesPaginateTypeDef",
    {
        "JobName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRulesetsResponseTypeDef = TypedDict(
    "ListRulesetsResponseTypeDef",
    {
        "Rulesets": List[RulesetItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchedulesResponseTypeDef = TypedDict(
    "ListSchedulesResponseTypeDef",
    {
        "Schedules": List[ScheduleTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRecipeStepTypeDef = TypedDict(
    "_RequiredRecipeStepTypeDef",
    {
        "Action": RecipeActionTypeDef,
    },
)
_OptionalRecipeStepTypeDef = TypedDict(
    "_OptionalRecipeStepTypeDef",
    {
        "ConditionExpressions": Sequence[ConditionExpressionTypeDef],
    },
    total=False,
)


class RecipeStepTypeDef(_RequiredRecipeStepTypeDef, _OptionalRecipeStepTypeDef):
    pass


_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef",
    {
        "Name": str,
        "CheckExpression": str,
    },
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef",
    {
        "Disabled": bool,
        "SubstitutionMap": Mapping[str, str],
        "Threshold": ThresholdTypeDef,
        "ColumnSelectors": Sequence[ColumnSelectorTypeDef],
    },
    total=False,
)


class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass


StatisticsConfigurationTypeDef = TypedDict(
    "StatisticsConfigurationTypeDef",
    {
        "IncludedStatistics": Sequence[str],
        "Overrides": Sequence[StatisticOverrideTypeDef],
    },
    total=False,
)

InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "S3InputDefinition": S3LocationTypeDef,
        "DataCatalogInputDefinition": DataCatalogInputDefinitionTypeDef,
        "DatabaseInputDefinition": DatabaseInputDefinitionTypeDef,
        "Metadata": MetadataTypeDef,
    },
    total=False,
)

_RequiredDatabaseOutputTypeDef = TypedDict(
    "_RequiredDatabaseOutputTypeDef",
    {
        "GlueConnectionName": str,
        "DatabaseOptions": DatabaseTableOutputOptionsTypeDef,
    },
)
_OptionalDatabaseOutputTypeDef = TypedDict(
    "_OptionalDatabaseOutputTypeDef",
    {
        "DatabaseOutputMode": Literal["NEW_TABLE"],
    },
    total=False,
)


class DatabaseOutputTypeDef(_RequiredDatabaseOutputTypeDef, _OptionalDatabaseOutputTypeDef):
    pass


_RequiredDataCatalogOutputTypeDef = TypedDict(
    "_RequiredDataCatalogOutputTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalDataCatalogOutputTypeDef = TypedDict(
    "_OptionalDataCatalogOutputTypeDef",
    {
        "CatalogId": str,
        "S3Options": S3TableOutputOptionsTypeDef,
        "DatabaseOptions": DatabaseTableOutputOptionsTypeDef,
        "Overwrite": bool,
    },
    total=False,
)


class DataCatalogOutputTypeDef(
    _RequiredDataCatalogOutputTypeDef, _OptionalDataCatalogOutputTypeDef
):
    pass


ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "Projects": List[ProjectTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredOutputTypeDef = TypedDict(
    "_RequiredOutputTypeDef",
    {
        "Location": S3LocationTypeDef,
    },
)
_OptionalOutputTypeDef = TypedDict(
    "_OptionalOutputTypeDef",
    {
        "CompressionFormat": CompressionFormatType,
        "Format": OutputFormatType,
        "PartitionColumns": Sequence[str],
        "Overwrite": bool,
        "FormatOptions": OutputFormatOptionsTypeDef,
        "MaxOutputFiles": int,
    },
    total=False,
)


class OutputTypeDef(_RequiredOutputTypeDef, _OptionalOutputTypeDef):
    pass


PathOptionsTypeDef = TypedDict(
    "PathOptionsTypeDef",
    {
        "LastModifiedDateCondition": FilterExpressionTypeDef,
        "FilesLimit": FilesLimitTypeDef,
        "Parameters": Mapping[str, DatasetParameterTypeDef],
    },
    total=False,
)

_RequiredCreateRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecipeRequestRequestTypeDef",
    {
        "Name": str,
        "Steps": Sequence[RecipeStepTypeDef],
    },
)
_OptionalCreateRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecipeRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRecipeRequestRequestTypeDef(
    _RequiredCreateRecipeRequestRequestTypeDef, _OptionalCreateRecipeRequestRequestTypeDef
):
    pass


DescribeRecipeResponseTypeDef = TypedDict(
    "DescribeRecipeResponseTypeDef",
    {
        "CreatedBy": str,
        "CreateDate": datetime,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ProjectName": str,
        "PublishedBy": str,
        "PublishedDate": datetime,
        "Description": str,
        "Name": str,
        "Steps": List[RecipeStepTypeDef],
        "Tags": Dict[str, str],
        "ResourceArn": str,
        "RecipeVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRecipeTypeDef = TypedDict(
    "_RequiredRecipeTypeDef",
    {
        "Name": str,
    },
)
_OptionalRecipeTypeDef = TypedDict(
    "_OptionalRecipeTypeDef",
    {
        "CreatedBy": str,
        "CreateDate": datetime,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ProjectName": str,
        "PublishedBy": str,
        "PublishedDate": datetime,
        "Description": str,
        "ResourceArn": str,
        "Steps": List[RecipeStepTypeDef],
        "Tags": Dict[str, str],
        "RecipeVersion": str,
    },
    total=False,
)


class RecipeTypeDef(_RequiredRecipeTypeDef, _OptionalRecipeTypeDef):
    pass


_RequiredSendProjectSessionActionRequestRequestTypeDef = TypedDict(
    "_RequiredSendProjectSessionActionRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalSendProjectSessionActionRequestRequestTypeDef = TypedDict(
    "_OptionalSendProjectSessionActionRequestRequestTypeDef",
    {
        "Preview": bool,
        "RecipeStep": RecipeStepTypeDef,
        "StepIndex": int,
        "ClientSessionId": str,
        "ViewFrame": ViewFrameTypeDef,
    },
    total=False,
)


class SendProjectSessionActionRequestRequestTypeDef(
    _RequiredSendProjectSessionActionRequestRequestTypeDef,
    _OptionalSendProjectSessionActionRequestRequestTypeDef,
):
    pass


_RequiredUpdateRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRecipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRecipeRequestRequestTypeDef",
    {
        "Description": str,
        "Steps": Sequence[RecipeStepTypeDef],
    },
    total=False,
)


class UpdateRecipeRequestRequestTypeDef(
    _RequiredUpdateRecipeRequestRequestTypeDef, _OptionalUpdateRecipeRequestRequestTypeDef
):
    pass


_RequiredCreateRulesetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRulesetRequestRequestTypeDef",
    {
        "Name": str,
        "TargetArn": str,
        "Rules": Sequence[RuleTypeDef],
    },
)
_OptionalCreateRulesetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRulesetRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRulesetRequestRequestTypeDef(
    _RequiredCreateRulesetRequestRequestTypeDef, _OptionalCreateRulesetRequestRequestTypeDef
):
    pass


DescribeRulesetResponseTypeDef = TypedDict(
    "DescribeRulesetResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "TargetArn": str,
        "Rules": List[RuleTypeDef],
        "CreateDate": datetime,
        "CreatedBy": str,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "ResourceArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateRulesetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRulesetRequestRequestTypeDef",
    {
        "Name": str,
        "Rules": Sequence[RuleTypeDef],
    },
)
_OptionalUpdateRulesetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRulesetRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateRulesetRequestRequestTypeDef(
    _RequiredUpdateRulesetRequestRequestTypeDef, _OptionalUpdateRulesetRequestRequestTypeDef
):
    pass


_RequiredColumnStatisticsConfigurationTypeDef = TypedDict(
    "_RequiredColumnStatisticsConfigurationTypeDef",
    {
        "Statistics": StatisticsConfigurationTypeDef,
    },
)
_OptionalColumnStatisticsConfigurationTypeDef = TypedDict(
    "_OptionalColumnStatisticsConfigurationTypeDef",
    {
        "Selectors": Sequence[ColumnSelectorTypeDef],
    },
    total=False,
)


class ColumnStatisticsConfigurationTypeDef(
    _RequiredColumnStatisticsConfigurationTypeDef, _OptionalColumnStatisticsConfigurationTypeDef
):
    pass


_RequiredCreateRecipeJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecipeJobRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
    },
)
_OptionalCreateRecipeJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecipeJobRequestRequestTypeDef",
    {
        "DatasetName": str,
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Outputs": Sequence[OutputTypeDef],
        "DataCatalogOutputs": Sequence[DataCatalogOutputTypeDef],
        "DatabaseOutputs": Sequence[DatabaseOutputTypeDef],
        "ProjectName": str,
        "RecipeReference": RecipeReferenceTypeDef,
        "Tags": Mapping[str, str],
        "Timeout": int,
    },
    total=False,
)


class CreateRecipeJobRequestRequestTypeDef(
    _RequiredCreateRecipeJobRequestRequestTypeDef, _OptionalCreateRecipeJobRequestRequestTypeDef
):
    pass


JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "Attempt": int,
        "CompletedOn": datetime,
        "DatasetName": str,
        "ErrorMessage": str,
        "ExecutionTime": int,
        "JobName": str,
        "RunId": str,
        "State": JobRunStateType,
        "LogSubscription": LogSubscriptionType,
        "LogGroupName": str,
        "Outputs": List[OutputTypeDef],
        "DataCatalogOutputs": List[DataCatalogOutputTypeDef],
        "DatabaseOutputs": List[DatabaseOutputTypeDef],
        "RecipeReference": RecipeReferenceTypeDef,
        "StartedBy": str,
        "StartedOn": datetime,
        "JobSample": JobSampleTypeDef,
        "ValidationConfigurations": List[ValidationConfigurationTypeDef],
    },
    total=False,
)

_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "Name": str,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "AccountId": str,
        "CreatedBy": str,
        "CreateDate": datetime,
        "DatasetName": str,
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "Type": JobTypeType,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Outputs": List[OutputTypeDef],
        "DataCatalogOutputs": List[DataCatalogOutputTypeDef],
        "DatabaseOutputs": List[DatabaseOutputTypeDef],
        "ProjectName": str,
        "RecipeReference": RecipeReferenceTypeDef,
        "ResourceArn": str,
        "RoleArn": str,
        "Timeout": int,
        "Tags": Dict[str, str],
        "JobSample": JobSampleTypeDef,
        "ValidationConfigurations": List[ValidationConfigurationTypeDef],
    },
    total=False,
)


class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass


_RequiredUpdateRecipeJobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRecipeJobRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
    },
)
_OptionalUpdateRecipeJobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRecipeJobRequestRequestTypeDef",
    {
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Outputs": Sequence[OutputTypeDef],
        "DataCatalogOutputs": Sequence[DataCatalogOutputTypeDef],
        "DatabaseOutputs": Sequence[DatabaseOutputTypeDef],
        "Timeout": int,
    },
    total=False,
)


class UpdateRecipeJobRequestRequestTypeDef(
    _RequiredUpdateRecipeJobRequestRequestTypeDef, _OptionalUpdateRecipeJobRequestRequestTypeDef
):
    pass


_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "Name": str,
        "Input": InputTypeDef,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "Format": InputFormatType,
        "FormatOptions": FormatOptionsTypeDef,
        "PathOptions": PathOptionsTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


_RequiredDatasetTypeDef = TypedDict(
    "_RequiredDatasetTypeDef",
    {
        "Name": str,
        "Input": InputTypeDef,
    },
)
_OptionalDatasetTypeDef = TypedDict(
    "_OptionalDatasetTypeDef",
    {
        "AccountId": str,
        "CreatedBy": str,
        "CreateDate": datetime,
        "Format": InputFormatType,
        "FormatOptions": FormatOptionsTypeDef,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "Source": SourceType,
        "PathOptions": PathOptionsTypeDef,
        "Tags": Dict[str, str],
        "ResourceArn": str,
    },
    total=False,
)


class DatasetTypeDef(_RequiredDatasetTypeDef, _OptionalDatasetTypeDef):
    pass


DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "CreatedBy": str,
        "CreateDate": datetime,
        "Name": str,
        "Format": InputFormatType,
        "FormatOptions": FormatOptionsTypeDef,
        "Input": InputTypeDef,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "Source": SourceType,
        "PathOptions": PathOptionsTypeDef,
        "Tags": Dict[str, str],
        "ResourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDatasetRequestRequestTypeDef",
    {
        "Name": str,
        "Input": InputTypeDef,
    },
)
_OptionalUpdateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDatasetRequestRequestTypeDef",
    {
        "Format": InputFormatType,
        "FormatOptions": FormatOptionsTypeDef,
        "PathOptions": PathOptionsTypeDef,
    },
    total=False,
)


class UpdateDatasetRequestRequestTypeDef(
    _RequiredUpdateDatasetRequestRequestTypeDef, _OptionalUpdateDatasetRequestRequestTypeDef
):
    pass


ListRecipeVersionsResponseTypeDef = TypedDict(
    "ListRecipeVersionsResponseTypeDef",
    {
        "NextToken": str,
        "Recipes": List[RecipeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecipesResponseTypeDef = TypedDict(
    "ListRecipesResponseTypeDef",
    {
        "Recipes": List[RecipeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProfileConfigurationTypeDef = TypedDict(
    "ProfileConfigurationTypeDef",
    {
        "DatasetStatisticsConfiguration": StatisticsConfigurationTypeDef,
        "ProfileColumns": Sequence[ColumnSelectorTypeDef],
        "ColumnStatisticsConfigurations": Sequence[ColumnStatisticsConfigurationTypeDef],
        "EntityDetectorConfiguration": EntityDetectorConfigurationTypeDef,
    },
    total=False,
)

ListJobRunsResponseTypeDef = TypedDict(
    "ListJobRunsResponseTypeDef",
    {
        "JobRuns": List[JobRunTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "Jobs": List[JobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "Datasets": List[DatasetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateProfileJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProfileJobRequestRequestTypeDef",
    {
        "DatasetName": str,
        "Name": str,
        "OutputLocation": S3LocationTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateProfileJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProfileJobRequestRequestTypeDef",
    {
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Configuration": ProfileConfigurationTypeDef,
        "ValidationConfigurations": Sequence[ValidationConfigurationTypeDef],
        "Tags": Mapping[str, str],
        "Timeout": int,
        "JobSample": JobSampleTypeDef,
    },
    total=False,
)


class CreateProfileJobRequestRequestTypeDef(
    _RequiredCreateProfileJobRequestRequestTypeDef, _OptionalCreateProfileJobRequestRequestTypeDef
):
    pass


DescribeJobResponseTypeDef = TypedDict(
    "DescribeJobResponseTypeDef",
    {
        "CreateDate": datetime,
        "CreatedBy": str,
        "DatasetName": str,
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "Name": str,
        "Type": JobTypeType,
        "LastModifiedBy": str,
        "LastModifiedDate": datetime,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "Outputs": List[OutputTypeDef],
        "DataCatalogOutputs": List[DataCatalogOutputTypeDef],
        "DatabaseOutputs": List[DatabaseOutputTypeDef],
        "ProjectName": str,
        "ProfileConfiguration": ProfileConfigurationTypeDef,
        "ValidationConfigurations": List[ValidationConfigurationTypeDef],
        "RecipeReference": RecipeReferenceTypeDef,
        "ResourceArn": str,
        "RoleArn": str,
        "Tags": Dict[str, str],
        "Timeout": int,
        "JobSample": JobSampleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeJobRunResponseTypeDef = TypedDict(
    "DescribeJobRunResponseTypeDef",
    {
        "Attempt": int,
        "CompletedOn": datetime,
        "DatasetName": str,
        "ErrorMessage": str,
        "ExecutionTime": int,
        "JobName": str,
        "ProfileConfiguration": ProfileConfigurationTypeDef,
        "ValidationConfigurations": List[ValidationConfigurationTypeDef],
        "RunId": str,
        "State": JobRunStateType,
        "LogSubscription": LogSubscriptionType,
        "LogGroupName": str,
        "Outputs": List[OutputTypeDef],
        "DataCatalogOutputs": List[DataCatalogOutputTypeDef],
        "DatabaseOutputs": List[DatabaseOutputTypeDef],
        "RecipeReference": RecipeReferenceTypeDef,
        "StartedBy": str,
        "StartedOn": datetime,
        "JobSample": JobSampleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateProfileJobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProfileJobRequestRequestTypeDef",
    {
        "Name": str,
        "OutputLocation": S3LocationTypeDef,
        "RoleArn": str,
    },
)
_OptionalUpdateProfileJobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProfileJobRequestRequestTypeDef",
    {
        "Configuration": ProfileConfigurationTypeDef,
        "EncryptionKeyArn": str,
        "EncryptionMode": EncryptionModeType,
        "LogSubscription": LogSubscriptionType,
        "MaxCapacity": int,
        "MaxRetries": int,
        "ValidationConfigurations": Sequence[ValidationConfigurationTypeDef],
        "Timeout": int,
        "JobSample": JobSampleTypeDef,
    },
    total=False,
)


class UpdateProfileJobRequestRequestTypeDef(
    _RequiredUpdateProfileJobRequestRequestTypeDef, _OptionalUpdateProfileJobRequestRequestTypeDef
):
    pass
