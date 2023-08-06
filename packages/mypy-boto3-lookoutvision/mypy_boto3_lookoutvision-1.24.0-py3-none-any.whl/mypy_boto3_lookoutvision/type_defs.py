"""
Type annotations for lookoutvision service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/type_defs/)

Usage::

    ```python
    from mypy_boto3_lookoutvision.type_defs import DatasetMetadataTypeDef

    data: DatasetMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DatasetStatusType,
    ModelHostingStatusType,
    ModelPackagingJobStatusType,
    ModelStatusType,
    TargetPlatformArchType,
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
    "DatasetMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "ProjectMetadataTypeDef",
    "DatasetImageStatsTypeDef",
    "InputS3ObjectTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteModelRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeModelPackagingJobRequestRequestTypeDef",
    "DescribeModelRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DetectAnomaliesRequestRequestTypeDef",
    "ImageSourceTypeDef",
    "S3LocationTypeDef",
    "TargetPlatformTypeDef",
    "GreengrassOutputDetailsTypeDef",
    "PaginatorConfigTypeDef",
    "ListDatasetEntriesRequestRequestTypeDef",
    "ListModelPackagingJobsRequestRequestTypeDef",
    "ModelPackagingJobMetadataTypeDef",
    "ListModelsRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ModelPerformanceTypeDef",
    "OutputS3ObjectTypeDef",
    "StartModelRequestRequestTypeDef",
    "StopModelRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasetEntriesRequestRequestTypeDef",
    "ProjectDescriptionTypeDef",
    "CreateDatasetResponseTypeDef",
    "DeleteModelResponseTypeDef",
    "DeleteProjectResponseTypeDef",
    "ListDatasetEntriesResponseTypeDef",
    "StartModelPackagingJobResponseTypeDef",
    "StartModelResponseTypeDef",
    "StopModelResponseTypeDef",
    "UpdateDatasetEntriesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "ListProjectsResponseTypeDef",
    "DatasetDescriptionTypeDef",
    "DatasetGroundTruthManifestTypeDef",
    "DetectAnomalyResultTypeDef",
    "OutputConfigTypeDef",
    "GreengrassConfigurationTypeDef",
    "ModelPackagingOutputDetailsTypeDef",
    "ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    "ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef",
    "ListModelsRequestListModelsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListModelPackagingJobsResponseTypeDef",
    "ModelMetadataTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DatasetSourceTypeDef",
    "DetectAnomaliesResponseTypeDef",
    "CreateModelRequestRequestTypeDef",
    "ModelDescriptionTypeDef",
    "ModelPackagingConfigurationTypeDef",
    "CreateModelResponseTypeDef",
    "ListModelsResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "DescribeModelResponseTypeDef",
    "ModelPackagingDescriptionTypeDef",
    "StartModelPackagingJobRequestRequestTypeDef",
    "DescribeModelPackagingJobResponseTypeDef",
)

DatasetMetadataTypeDef = TypedDict(
    "DatasetMetadataTypeDef",
    {
        "DatasetType": str,
        "CreationTimestamp": datetime,
        "Status": DatasetStatusType,
        "StatusMessage": str,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


ProjectMetadataTypeDef = TypedDict(
    "ProjectMetadataTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "CreationTimestamp": datetime,
    },
    total=False,
)

DatasetImageStatsTypeDef = TypedDict(
    "DatasetImageStatsTypeDef",
    {
        "Total": int,
        "Labeled": int,
        "Normal": int,
        "Anomaly": int,
    },
    total=False,
)

_RequiredInputS3ObjectTypeDef = TypedDict(
    "_RequiredInputS3ObjectTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)
_OptionalInputS3ObjectTypeDef = TypedDict(
    "_OptionalInputS3ObjectTypeDef",
    {
        "VersionId": str,
    },
    total=False,
)


class InputS3ObjectTypeDef(_RequiredInputS3ObjectTypeDef, _OptionalInputS3ObjectTypeDef):
    pass


_RequiredDeleteDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDatasetRequestRequestTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
    },
)
_OptionalDeleteDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDatasetRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DeleteDatasetRequestRequestTypeDef(
    _RequiredDeleteDatasetRequestRequestTypeDef, _OptionalDeleteDatasetRequestRequestTypeDef
):
    pass


_RequiredDeleteModelRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteModelRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
    },
)
_OptionalDeleteModelRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteModelRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DeleteModelRequestRequestTypeDef(
    _RequiredDeleteModelRequestRequestTypeDef, _OptionalDeleteModelRequestRequestTypeDef
):
    pass


_RequiredDeleteProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteProjectRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalDeleteProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteProjectRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DeleteProjectRequestRequestTypeDef(
    _RequiredDeleteProjectRequestRequestTypeDef, _OptionalDeleteProjectRequestRequestTypeDef
):
    pass


DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
    },
)

DescribeModelPackagingJobRequestRequestTypeDef = TypedDict(
    "DescribeModelPackagingJobRequestRequestTypeDef",
    {
        "ProjectName": str,
        "JobName": str,
    },
)

DescribeModelRequestRequestTypeDef = TypedDict(
    "DescribeModelRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)

DetectAnomaliesRequestRequestTypeDef = TypedDict(
    "DetectAnomaliesRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
        "Body": Union[str, bytes, IO[Any], StreamingBody],
        "ContentType": str,
    },
)

ImageSourceTypeDef = TypedDict(
    "ImageSourceTypeDef",
    {
        "Type": str,
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
        "Prefix": str,
    },
    total=False,
)


class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass


TargetPlatformTypeDef = TypedDict(
    "TargetPlatformTypeDef",
    {
        "Os": Literal["LINUX"],
        "Arch": TargetPlatformArchType,
        "Accelerator": Literal["NVIDIA"],
    },
)

GreengrassOutputDetailsTypeDef = TypedDict(
    "GreengrassOutputDetailsTypeDef",
    {
        "ComponentVersionArn": str,
        "ComponentName": str,
        "ComponentVersion": str,
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

_RequiredListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestRequestTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
    },
)
_OptionalListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestRequestTypeDef",
    {
        "Labeled": bool,
        "AnomalyClass": str,
        "BeforeCreationDate": Union[datetime, str],
        "AfterCreationDate": Union[datetime, str],
        "NextToken": str,
        "MaxResults": int,
        "SourceRefContains": str,
    },
    total=False,
)


class ListDatasetEntriesRequestRequestTypeDef(
    _RequiredListDatasetEntriesRequestRequestTypeDef,
    _OptionalListDatasetEntriesRequestRequestTypeDef,
):
    pass


_RequiredListModelPackagingJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListModelPackagingJobsRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalListModelPackagingJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListModelPackagingJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListModelPackagingJobsRequestRequestTypeDef(
    _RequiredListModelPackagingJobsRequestRequestTypeDef,
    _OptionalListModelPackagingJobsRequestRequestTypeDef,
):
    pass


ModelPackagingJobMetadataTypeDef = TypedDict(
    "ModelPackagingJobMetadataTypeDef",
    {
        "JobName": str,
        "ProjectName": str,
        "ModelVersion": str,
        "ModelPackagingJobDescription": str,
        "ModelPackagingMethod": str,
        "Status": ModelPackagingJobStatusType,
        "StatusMessage": str,
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

_RequiredListModelsRequestRequestTypeDef = TypedDict(
    "_RequiredListModelsRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalListModelsRequestRequestTypeDef = TypedDict(
    "_OptionalListModelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListModelsRequestRequestTypeDef(
    _RequiredListModelsRequestRequestTypeDef, _OptionalListModelsRequestRequestTypeDef
):
    pass


ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ModelPerformanceTypeDef = TypedDict(
    "ModelPerformanceTypeDef",
    {
        "F1Score": float,
        "Recall": float,
        "Precision": float,
    },
    total=False,
)

OutputS3ObjectTypeDef = TypedDict(
    "OutputS3ObjectTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

_RequiredStartModelRequestRequestTypeDef = TypedDict(
    "_RequiredStartModelRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
        "MinInferenceUnits": int,
    },
)
_OptionalStartModelRequestRequestTypeDef = TypedDict(
    "_OptionalStartModelRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class StartModelRequestRequestTypeDef(
    _RequiredStartModelRequestRequestTypeDef, _OptionalStartModelRequestRequestTypeDef
):
    pass


_RequiredStopModelRequestRequestTypeDef = TypedDict(
    "_RequiredStopModelRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
    },
)
_OptionalStopModelRequestRequestTypeDef = TypedDict(
    "_OptionalStopModelRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class StopModelRequestRequestTypeDef(
    _RequiredStopModelRequestRequestTypeDef, _OptionalStopModelRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDatasetEntriesRequestRequestTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
        "Changes": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalUpdateDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDatasetEntriesRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class UpdateDatasetEntriesRequestRequestTypeDef(
    _RequiredUpdateDatasetEntriesRequestRequestTypeDef,
    _OptionalUpdateDatasetEntriesRequestRequestTypeDef,
):
    pass


ProjectDescriptionTypeDef = TypedDict(
    "ProjectDescriptionTypeDef",
    {
        "ProjectArn": str,
        "ProjectName": str,
        "CreationTimestamp": datetime,
        "Datasets": List[DatasetMetadataTypeDef],
    },
    total=False,
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetMetadata": DatasetMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteModelResponseTypeDef = TypedDict(
    "DeleteModelResponseTypeDef",
    {
        "ModelArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {
        "ProjectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetEntriesResponseTypeDef = TypedDict(
    "ListDatasetEntriesResponseTypeDef",
    {
        "DatasetEntries": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartModelPackagingJobResponseTypeDef = TypedDict(
    "StartModelPackagingJobResponseTypeDef",
    {
        "JobName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartModelResponseTypeDef = TypedDict(
    "StartModelResponseTypeDef",
    {
        "Status": ModelHostingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopModelResponseTypeDef = TypedDict(
    "StopModelResponseTypeDef",
    {
        "Status": ModelHostingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDatasetEntriesResponseTypeDef = TypedDict(
    "UpdateDatasetEntriesResponseTypeDef",
    {
        "Status": DatasetStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "ProjectMetadata": ProjectMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "Projects": List[ProjectMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasetDescriptionTypeDef = TypedDict(
    "DatasetDescriptionTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "Status": DatasetStatusType,
        "StatusMessage": str,
        "ImageStats": DatasetImageStatsTypeDef,
    },
    total=False,
)

DatasetGroundTruthManifestTypeDef = TypedDict(
    "DatasetGroundTruthManifestTypeDef",
    {
        "S3Object": InputS3ObjectTypeDef,
    },
    total=False,
)

DetectAnomalyResultTypeDef = TypedDict(
    "DetectAnomalyResultTypeDef",
    {
        "Source": ImageSourceTypeDef,
        "IsAnomalous": bool,
        "Confidence": float,
    },
    total=False,
)

OutputConfigTypeDef = TypedDict(
    "OutputConfigTypeDef",
    {
        "S3Location": S3LocationTypeDef,
    },
)

_RequiredGreengrassConfigurationTypeDef = TypedDict(
    "_RequiredGreengrassConfigurationTypeDef",
    {
        "S3OutputLocation": S3LocationTypeDef,
        "ComponentName": str,
    },
)
_OptionalGreengrassConfigurationTypeDef = TypedDict(
    "_OptionalGreengrassConfigurationTypeDef",
    {
        "CompilerOptions": str,
        "TargetDevice": Literal["jetson_xavier"],
        "TargetPlatform": TargetPlatformTypeDef,
        "ComponentVersion": str,
        "ComponentDescription": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class GreengrassConfigurationTypeDef(
    _RequiredGreengrassConfigurationTypeDef, _OptionalGreengrassConfigurationTypeDef
):
    pass


ModelPackagingOutputDetailsTypeDef = TypedDict(
    "ModelPackagingOutputDetailsTypeDef",
    {
        "Greengrass": GreengrassOutputDetailsTypeDef,
    },
    total=False,
)

_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
    },
)
_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "Labeled": bool,
        "AnomalyClass": str,
        "BeforeCreationDate": Union[datetime, str],
        "AfterCreationDate": Union[datetime, str],
        "SourceRefContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef(
    _RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    _OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
):
    pass


_RequiredListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef = TypedDict(
    "_RequiredListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef = TypedDict(
    "_OptionalListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef(
    _RequiredListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef,
    _OptionalListModelPackagingJobsRequestListModelPackagingJobsPaginateTypeDef,
):
    pass


_RequiredListModelsRequestListModelsPaginateTypeDef = TypedDict(
    "_RequiredListModelsRequestListModelsPaginateTypeDef",
    {
        "ProjectName": str,
    },
)
_OptionalListModelsRequestListModelsPaginateTypeDef = TypedDict(
    "_OptionalListModelsRequestListModelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListModelsRequestListModelsPaginateTypeDef(
    _RequiredListModelsRequestListModelsPaginateTypeDef,
    _OptionalListModelsRequestListModelsPaginateTypeDef,
):
    pass


ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListModelPackagingJobsResponseTypeDef = TypedDict(
    "ListModelPackagingJobsResponseTypeDef",
    {
        "ModelPackagingJobs": List[ModelPackagingJobMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModelMetadataTypeDef = TypedDict(
    "ModelMetadataTypeDef",
    {
        "CreationTimestamp": datetime,
        "ModelVersion": str,
        "ModelArn": str,
        "Description": str,
        "Status": ModelStatusType,
        "StatusMessage": str,
        "Performance": ModelPerformanceTypeDef,
    },
    total=False,
)

DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "ProjectDescription": ProjectDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetDescription": DatasetDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasetSourceTypeDef = TypedDict(
    "DatasetSourceTypeDef",
    {
        "GroundTruthManifest": DatasetGroundTruthManifestTypeDef,
    },
    total=False,
)

DetectAnomaliesResponseTypeDef = TypedDict(
    "DetectAnomaliesResponseTypeDef",
    {
        "DetectAnomalyResult": DetectAnomalyResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateModelRequestRequestTypeDef",
    {
        "ProjectName": str,
        "OutputConfig": OutputConfigTypeDef,
    },
)
_OptionalCreateModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateModelRequestRequestTypeDef",
    {
        "Description": str,
        "ClientToken": str,
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateModelRequestRequestTypeDef(
    _RequiredCreateModelRequestRequestTypeDef, _OptionalCreateModelRequestRequestTypeDef
):
    pass


ModelDescriptionTypeDef = TypedDict(
    "ModelDescriptionTypeDef",
    {
        "ModelVersion": str,
        "ModelArn": str,
        "CreationTimestamp": datetime,
        "Description": str,
        "Status": ModelStatusType,
        "StatusMessage": str,
        "Performance": ModelPerformanceTypeDef,
        "OutputConfig": OutputConfigTypeDef,
        "EvaluationManifest": OutputS3ObjectTypeDef,
        "EvaluationResult": OutputS3ObjectTypeDef,
        "EvaluationEndTimestamp": datetime,
        "KmsKeyId": str,
    },
    total=False,
)

ModelPackagingConfigurationTypeDef = TypedDict(
    "ModelPackagingConfigurationTypeDef",
    {
        "Greengrass": GreengrassConfigurationTypeDef,
    },
)

CreateModelResponseTypeDef = TypedDict(
    "CreateModelResponseTypeDef",
    {
        "ModelMetadata": ModelMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListModelsResponseTypeDef = TypedDict(
    "ListModelsResponseTypeDef",
    {
        "Models": List[ModelMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "ProjectName": str,
        "DatasetType": str,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DatasetSource": DatasetSourceTypeDef,
        "ClientToken": str,
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


DescribeModelResponseTypeDef = TypedDict(
    "DescribeModelResponseTypeDef",
    {
        "ModelDescription": ModelDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModelPackagingDescriptionTypeDef = TypedDict(
    "ModelPackagingDescriptionTypeDef",
    {
        "JobName": str,
        "ProjectName": str,
        "ModelVersion": str,
        "ModelPackagingConfiguration": ModelPackagingConfigurationTypeDef,
        "ModelPackagingJobDescription": str,
        "ModelPackagingMethod": str,
        "ModelPackagingOutputDetails": ModelPackagingOutputDetailsTypeDef,
        "Status": ModelPackagingJobStatusType,
        "StatusMessage": str,
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

_RequiredStartModelPackagingJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartModelPackagingJobRequestRequestTypeDef",
    {
        "ProjectName": str,
        "ModelVersion": str,
        "Configuration": ModelPackagingConfigurationTypeDef,
    },
)
_OptionalStartModelPackagingJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartModelPackagingJobRequestRequestTypeDef",
    {
        "JobName": str,
        "Description": str,
        "ClientToken": str,
    },
    total=False,
)


class StartModelPackagingJobRequestRequestTypeDef(
    _RequiredStartModelPackagingJobRequestRequestTypeDef,
    _OptionalStartModelPackagingJobRequestRequestTypeDef,
):
    pass


DescribeModelPackagingJobResponseTypeDef = TypedDict(
    "DescribeModelPackagingJobResponseTypeDef",
    {
        "ModelPackagingDescription": ModelPackagingDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
