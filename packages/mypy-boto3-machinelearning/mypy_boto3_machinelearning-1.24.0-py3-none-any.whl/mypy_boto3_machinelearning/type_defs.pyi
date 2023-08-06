"""
Type annotations for machinelearning service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/type_defs/)

Usage::

    ```python
    from mypy_boto3_machinelearning.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BatchPredictionFilterVariableType,
    DataSourceFilterVariableType,
    DetailsAttributesType,
    EntityStatusType,
    EvaluationFilterVariableType,
    MLModelFilterVariableType,
    MLModelTypeType,
    RealtimeEndpointStatusType,
    SortOrderType,
    TaggableResourceTypeType,
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
    "ResponseMetadataTypeDef",
    "BatchPredictionTypeDef",
    "CreateBatchPredictionInputRequestTypeDef",
    "S3DataSpecTypeDef",
    "CreateEvaluationInputRequestTypeDef",
    "CreateMLModelInputRequestTypeDef",
    "CreateRealtimeEndpointInputRequestTypeDef",
    "RealtimeEndpointInfoTypeDef",
    "DeleteBatchPredictionInputRequestTypeDef",
    "DeleteDataSourceInputRequestTypeDef",
    "DeleteEvaluationInputRequestTypeDef",
    "DeleteMLModelInputRequestTypeDef",
    "DeleteRealtimeEndpointInputRequestTypeDef",
    "DeleteTagsInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeBatchPredictionsInputRequestTypeDef",
    "DescribeDataSourcesInputRequestTypeDef",
    "DescribeEvaluationsInputRequestTypeDef",
    "DescribeMLModelsInputRequestTypeDef",
    "DescribeTagsInputRequestTypeDef",
    "PerformanceMetricsTypeDef",
    "GetBatchPredictionInputRequestTypeDef",
    "GetDataSourceInputRequestTypeDef",
    "GetEvaluationInputRequestTypeDef",
    "GetMLModelInputRequestTypeDef",
    "PredictInputRequestTypeDef",
    "PredictionTypeDef",
    "RDSDatabaseCredentialsTypeDef",
    "RDSDatabaseTypeDef",
    "RedshiftDatabaseCredentialsTypeDef",
    "RedshiftDatabaseTypeDef",
    "UpdateBatchPredictionInputRequestTypeDef",
    "UpdateDataSourceInputRequestTypeDef",
    "UpdateEvaluationInputRequestTypeDef",
    "UpdateMLModelInputRequestTypeDef",
    "AddTagsInputRequestTypeDef",
    "AddTagsOutputTypeDef",
    "CreateBatchPredictionOutputTypeDef",
    "CreateDataSourceFromRDSOutputTypeDef",
    "CreateDataSourceFromRedshiftOutputTypeDef",
    "CreateDataSourceFromS3OutputTypeDef",
    "CreateEvaluationOutputTypeDef",
    "CreateMLModelOutputTypeDef",
    "DeleteBatchPredictionOutputTypeDef",
    "DeleteDataSourceOutputTypeDef",
    "DeleteEvaluationOutputTypeDef",
    "DeleteMLModelOutputTypeDef",
    "DeleteTagsOutputTypeDef",
    "DescribeTagsOutputTypeDef",
    "GetBatchPredictionOutputTypeDef",
    "UpdateBatchPredictionOutputTypeDef",
    "UpdateDataSourceOutputTypeDef",
    "UpdateEvaluationOutputTypeDef",
    "UpdateMLModelOutputTypeDef",
    "DescribeBatchPredictionsOutputTypeDef",
    "CreateDataSourceFromS3InputRequestTypeDef",
    "CreateRealtimeEndpointOutputTypeDef",
    "DeleteRealtimeEndpointOutputTypeDef",
    "GetMLModelOutputTypeDef",
    "MLModelTypeDef",
    "DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef",
    "DescribeDataSourcesInputDataSourceAvailableWaitTypeDef",
    "DescribeEvaluationsInputEvaluationAvailableWaitTypeDef",
    "DescribeMLModelsInputMLModelAvailableWaitTypeDef",
    "DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef",
    "DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef",
    "DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef",
    "DescribeMLModelsInputDescribeMLModelsPaginateTypeDef",
    "EvaluationTypeDef",
    "GetEvaluationOutputTypeDef",
    "PredictOutputTypeDef",
    "RDSDataSpecTypeDef",
    "RDSMetadataTypeDef",
    "RedshiftDataSpecTypeDef",
    "RedshiftMetadataTypeDef",
    "DescribeMLModelsOutputTypeDef",
    "DescribeEvaluationsOutputTypeDef",
    "CreateDataSourceFromRDSInputRequestTypeDef",
    "CreateDataSourceFromRedshiftInputRequestTypeDef",
    "DataSourceTypeDef",
    "GetDataSourceOutputTypeDef",
    "DescribeDataSourcesOutputTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

BatchPredictionTypeDef = TypedDict(
    "BatchPredictionTypeDef",
    {
        "BatchPredictionId": str,
        "MLModelId": str,
        "BatchPredictionDataSourceId": str,
        "InputDataLocationS3": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "OutputUri": str,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
        "TotalRecordCount": int,
        "InvalidRecordCount": int,
    },
    total=False,
)

_RequiredCreateBatchPredictionInputRequestTypeDef = TypedDict(
    "_RequiredCreateBatchPredictionInputRequestTypeDef",
    {
        "BatchPredictionId": str,
        "MLModelId": str,
        "BatchPredictionDataSourceId": str,
        "OutputUri": str,
    },
)
_OptionalCreateBatchPredictionInputRequestTypeDef = TypedDict(
    "_OptionalCreateBatchPredictionInputRequestTypeDef",
    {
        "BatchPredictionName": str,
    },
    total=False,
)

class CreateBatchPredictionInputRequestTypeDef(
    _RequiredCreateBatchPredictionInputRequestTypeDef,
    _OptionalCreateBatchPredictionInputRequestTypeDef,
):
    pass

_RequiredS3DataSpecTypeDef = TypedDict(
    "_RequiredS3DataSpecTypeDef",
    {
        "DataLocationS3": str,
    },
)
_OptionalS3DataSpecTypeDef = TypedDict(
    "_OptionalS3DataSpecTypeDef",
    {
        "DataRearrangement": str,
        "DataSchema": str,
        "DataSchemaLocationS3": str,
    },
    total=False,
)

class S3DataSpecTypeDef(_RequiredS3DataSpecTypeDef, _OptionalS3DataSpecTypeDef):
    pass

_RequiredCreateEvaluationInputRequestTypeDef = TypedDict(
    "_RequiredCreateEvaluationInputRequestTypeDef",
    {
        "EvaluationId": str,
        "MLModelId": str,
        "EvaluationDataSourceId": str,
    },
)
_OptionalCreateEvaluationInputRequestTypeDef = TypedDict(
    "_OptionalCreateEvaluationInputRequestTypeDef",
    {
        "EvaluationName": str,
    },
    total=False,
)

class CreateEvaluationInputRequestTypeDef(
    _RequiredCreateEvaluationInputRequestTypeDef, _OptionalCreateEvaluationInputRequestTypeDef
):
    pass

_RequiredCreateMLModelInputRequestTypeDef = TypedDict(
    "_RequiredCreateMLModelInputRequestTypeDef",
    {
        "MLModelId": str,
        "MLModelType": MLModelTypeType,
        "TrainingDataSourceId": str,
    },
)
_OptionalCreateMLModelInputRequestTypeDef = TypedDict(
    "_OptionalCreateMLModelInputRequestTypeDef",
    {
        "MLModelName": str,
        "Parameters": Mapping[str, str],
        "Recipe": str,
        "RecipeUri": str,
    },
    total=False,
)

class CreateMLModelInputRequestTypeDef(
    _RequiredCreateMLModelInputRequestTypeDef, _OptionalCreateMLModelInputRequestTypeDef
):
    pass

CreateRealtimeEndpointInputRequestTypeDef = TypedDict(
    "CreateRealtimeEndpointInputRequestTypeDef",
    {
        "MLModelId": str,
    },
)

RealtimeEndpointInfoTypeDef = TypedDict(
    "RealtimeEndpointInfoTypeDef",
    {
        "PeakRequestsPerSecond": int,
        "CreatedAt": datetime,
        "EndpointUrl": str,
        "EndpointStatus": RealtimeEndpointStatusType,
    },
    total=False,
)

DeleteBatchPredictionInputRequestTypeDef = TypedDict(
    "DeleteBatchPredictionInputRequestTypeDef",
    {
        "BatchPredictionId": str,
    },
)

DeleteDataSourceInputRequestTypeDef = TypedDict(
    "DeleteDataSourceInputRequestTypeDef",
    {
        "DataSourceId": str,
    },
)

DeleteEvaluationInputRequestTypeDef = TypedDict(
    "DeleteEvaluationInputRequestTypeDef",
    {
        "EvaluationId": str,
    },
)

DeleteMLModelInputRequestTypeDef = TypedDict(
    "DeleteMLModelInputRequestTypeDef",
    {
        "MLModelId": str,
    },
)

DeleteRealtimeEndpointInputRequestTypeDef = TypedDict(
    "DeleteRealtimeEndpointInputRequestTypeDef",
    {
        "MLModelId": str,
    },
)

DeleteTagsInputRequestTypeDef = TypedDict(
    "DeleteTagsInputRequestTypeDef",
    {
        "TagKeys": Sequence[str],
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
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

DescribeBatchPredictionsInputRequestTypeDef = TypedDict(
    "DescribeBatchPredictionsInputRequestTypeDef",
    {
        "FilterVariable": BatchPredictionFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

DescribeDataSourcesInputRequestTypeDef = TypedDict(
    "DescribeDataSourcesInputRequestTypeDef",
    {
        "FilterVariable": DataSourceFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

DescribeEvaluationsInputRequestTypeDef = TypedDict(
    "DescribeEvaluationsInputRequestTypeDef",
    {
        "FilterVariable": EvaluationFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

DescribeMLModelsInputRequestTypeDef = TypedDict(
    "DescribeMLModelsInputRequestTypeDef",
    {
        "FilterVariable": MLModelFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
    },
    total=False,
)

DescribeTagsInputRequestTypeDef = TypedDict(
    "DescribeTagsInputRequestTypeDef",
    {
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
    },
)

PerformanceMetricsTypeDef = TypedDict(
    "PerformanceMetricsTypeDef",
    {
        "Properties": Dict[str, str],
    },
    total=False,
)

GetBatchPredictionInputRequestTypeDef = TypedDict(
    "GetBatchPredictionInputRequestTypeDef",
    {
        "BatchPredictionId": str,
    },
)

_RequiredGetDataSourceInputRequestTypeDef = TypedDict(
    "_RequiredGetDataSourceInputRequestTypeDef",
    {
        "DataSourceId": str,
    },
)
_OptionalGetDataSourceInputRequestTypeDef = TypedDict(
    "_OptionalGetDataSourceInputRequestTypeDef",
    {
        "Verbose": bool,
    },
    total=False,
)

class GetDataSourceInputRequestTypeDef(
    _RequiredGetDataSourceInputRequestTypeDef, _OptionalGetDataSourceInputRequestTypeDef
):
    pass

GetEvaluationInputRequestTypeDef = TypedDict(
    "GetEvaluationInputRequestTypeDef",
    {
        "EvaluationId": str,
    },
)

_RequiredGetMLModelInputRequestTypeDef = TypedDict(
    "_RequiredGetMLModelInputRequestTypeDef",
    {
        "MLModelId": str,
    },
)
_OptionalGetMLModelInputRequestTypeDef = TypedDict(
    "_OptionalGetMLModelInputRequestTypeDef",
    {
        "Verbose": bool,
    },
    total=False,
)

class GetMLModelInputRequestTypeDef(
    _RequiredGetMLModelInputRequestTypeDef, _OptionalGetMLModelInputRequestTypeDef
):
    pass

PredictInputRequestTypeDef = TypedDict(
    "PredictInputRequestTypeDef",
    {
        "MLModelId": str,
        "Record": Mapping[str, str],
        "PredictEndpoint": str,
    },
)

PredictionTypeDef = TypedDict(
    "PredictionTypeDef",
    {
        "predictedLabel": str,
        "predictedValue": float,
        "predictedScores": Dict[str, float],
        "details": Dict[DetailsAttributesType, str],
    },
    total=False,
)

RDSDatabaseCredentialsTypeDef = TypedDict(
    "RDSDatabaseCredentialsTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)

RDSDatabaseTypeDef = TypedDict(
    "RDSDatabaseTypeDef",
    {
        "InstanceIdentifier": str,
        "DatabaseName": str,
    },
)

RedshiftDatabaseCredentialsTypeDef = TypedDict(
    "RedshiftDatabaseCredentialsTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)

RedshiftDatabaseTypeDef = TypedDict(
    "RedshiftDatabaseTypeDef",
    {
        "DatabaseName": str,
        "ClusterIdentifier": str,
    },
)

UpdateBatchPredictionInputRequestTypeDef = TypedDict(
    "UpdateBatchPredictionInputRequestTypeDef",
    {
        "BatchPredictionId": str,
        "BatchPredictionName": str,
    },
)

UpdateDataSourceInputRequestTypeDef = TypedDict(
    "UpdateDataSourceInputRequestTypeDef",
    {
        "DataSourceId": str,
        "DataSourceName": str,
    },
)

UpdateEvaluationInputRequestTypeDef = TypedDict(
    "UpdateEvaluationInputRequestTypeDef",
    {
        "EvaluationId": str,
        "EvaluationName": str,
    },
)

_RequiredUpdateMLModelInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMLModelInputRequestTypeDef",
    {
        "MLModelId": str,
    },
)
_OptionalUpdateMLModelInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMLModelInputRequestTypeDef",
    {
        "MLModelName": str,
        "ScoreThreshold": float,
    },
    total=False,
)

class UpdateMLModelInputRequestTypeDef(
    _RequiredUpdateMLModelInputRequestTypeDef, _OptionalUpdateMLModelInputRequestTypeDef
):
    pass

AddTagsInputRequestTypeDef = TypedDict(
    "AddTagsInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
    },
)

AddTagsOutputTypeDef = TypedDict(
    "AddTagsOutputTypeDef",
    {
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBatchPredictionOutputTypeDef = TypedDict(
    "CreateBatchPredictionOutputTypeDef",
    {
        "BatchPredictionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceFromRDSOutputTypeDef = TypedDict(
    "CreateDataSourceFromRDSOutputTypeDef",
    {
        "DataSourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceFromRedshiftOutputTypeDef = TypedDict(
    "CreateDataSourceFromRedshiftOutputTypeDef",
    {
        "DataSourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceFromS3OutputTypeDef = TypedDict(
    "CreateDataSourceFromS3OutputTypeDef",
    {
        "DataSourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEvaluationOutputTypeDef = TypedDict(
    "CreateEvaluationOutputTypeDef",
    {
        "EvaluationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMLModelOutputTypeDef = TypedDict(
    "CreateMLModelOutputTypeDef",
    {
        "MLModelId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBatchPredictionOutputTypeDef = TypedDict(
    "DeleteBatchPredictionOutputTypeDef",
    {
        "BatchPredictionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSourceOutputTypeDef = TypedDict(
    "DeleteDataSourceOutputTypeDef",
    {
        "DataSourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEvaluationOutputTypeDef = TypedDict(
    "DeleteEvaluationOutputTypeDef",
    {
        "EvaluationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMLModelOutputTypeDef = TypedDict(
    "DeleteMLModelOutputTypeDef",
    {
        "MLModelId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTagsOutputTypeDef = TypedDict(
    "DeleteTagsOutputTypeDef",
    {
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTagsOutputTypeDef = TypedDict(
    "DescribeTagsOutputTypeDef",
    {
        "ResourceId": str,
        "ResourceType": TaggableResourceTypeType,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBatchPredictionOutputTypeDef = TypedDict(
    "GetBatchPredictionOutputTypeDef",
    {
        "BatchPredictionId": str,
        "MLModelId": str,
        "BatchPredictionDataSourceId": str,
        "InputDataLocationS3": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "OutputUri": str,
        "LogUri": str,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
        "TotalRecordCount": int,
        "InvalidRecordCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBatchPredictionOutputTypeDef = TypedDict(
    "UpdateBatchPredictionOutputTypeDef",
    {
        "BatchPredictionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourceOutputTypeDef = TypedDict(
    "UpdateDataSourceOutputTypeDef",
    {
        "DataSourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEvaluationOutputTypeDef = TypedDict(
    "UpdateEvaluationOutputTypeDef",
    {
        "EvaluationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMLModelOutputTypeDef = TypedDict(
    "UpdateMLModelOutputTypeDef",
    {
        "MLModelId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBatchPredictionsOutputTypeDef = TypedDict(
    "DescribeBatchPredictionsOutputTypeDef",
    {
        "Results": List[BatchPredictionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDataSourceFromS3InputRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceFromS3InputRequestTypeDef",
    {
        "DataSourceId": str,
        "DataSpec": S3DataSpecTypeDef,
    },
)
_OptionalCreateDataSourceFromS3InputRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceFromS3InputRequestTypeDef",
    {
        "DataSourceName": str,
        "ComputeStatistics": bool,
    },
    total=False,
)

class CreateDataSourceFromS3InputRequestTypeDef(
    _RequiredCreateDataSourceFromS3InputRequestTypeDef,
    _OptionalCreateDataSourceFromS3InputRequestTypeDef,
):
    pass

CreateRealtimeEndpointOutputTypeDef = TypedDict(
    "CreateRealtimeEndpointOutputTypeDef",
    {
        "MLModelId": str,
        "RealtimeEndpointInfo": RealtimeEndpointInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRealtimeEndpointOutputTypeDef = TypedDict(
    "DeleteRealtimeEndpointOutputTypeDef",
    {
        "MLModelId": str,
        "RealtimeEndpointInfo": RealtimeEndpointInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMLModelOutputTypeDef = TypedDict(
    "GetMLModelOutputTypeDef",
    {
        "MLModelId": str,
        "TrainingDataSourceId": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "SizeInBytes": int,
        "EndpointInfo": RealtimeEndpointInfoTypeDef,
        "TrainingParameters": Dict[str, str],
        "InputDataLocationS3": str,
        "MLModelType": MLModelTypeType,
        "ScoreThreshold": float,
        "ScoreThresholdLastUpdatedAt": datetime,
        "LogUri": str,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
        "Recipe": str,
        "Schema": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MLModelTypeDef = TypedDict(
    "MLModelTypeDef",
    {
        "MLModelId": str,
        "TrainingDataSourceId": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "SizeInBytes": int,
        "EndpointInfo": RealtimeEndpointInfoTypeDef,
        "TrainingParameters": Dict[str, str],
        "InputDataLocationS3": str,
        "Algorithm": Literal["sgd"],
        "MLModelType": MLModelTypeType,
        "ScoreThreshold": float,
        "ScoreThresholdLastUpdatedAt": datetime,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
    },
    total=False,
)

DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef = TypedDict(
    "DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef",
    {
        "FilterVariable": BatchPredictionFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDataSourcesInputDataSourceAvailableWaitTypeDef = TypedDict(
    "DescribeDataSourcesInputDataSourceAvailableWaitTypeDef",
    {
        "FilterVariable": DataSourceFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEvaluationsInputEvaluationAvailableWaitTypeDef = TypedDict(
    "DescribeEvaluationsInputEvaluationAvailableWaitTypeDef",
    {
        "FilterVariable": EvaluationFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeMLModelsInputMLModelAvailableWaitTypeDef = TypedDict(
    "DescribeMLModelsInputMLModelAvailableWaitTypeDef",
    {
        "FilterVariable": MLModelFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "NextToken": str,
        "Limit": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef = TypedDict(
    "DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef",
    {
        "FilterVariable": BatchPredictionFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef = TypedDict(
    "DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef",
    {
        "FilterVariable": DataSourceFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef = TypedDict(
    "DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef",
    {
        "FilterVariable": EvaluationFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeMLModelsInputDescribeMLModelsPaginateTypeDef = TypedDict(
    "DescribeMLModelsInputDescribeMLModelsPaginateTypeDef",
    {
        "FilterVariable": MLModelFilterVariableType,
        "EQ": str,
        "GT": str,
        "LT": str,
        "GE": str,
        "LE": str,
        "NE": str,
        "Prefix": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

EvaluationTypeDef = TypedDict(
    "EvaluationTypeDef",
    {
        "EvaluationId": str,
        "MLModelId": str,
        "EvaluationDataSourceId": str,
        "InputDataLocationS3": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "PerformanceMetrics": PerformanceMetricsTypeDef,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
    },
    total=False,
)

GetEvaluationOutputTypeDef = TypedDict(
    "GetEvaluationOutputTypeDef",
    {
        "EvaluationId": str,
        "MLModelId": str,
        "EvaluationDataSourceId": str,
        "InputDataLocationS3": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "Name": str,
        "Status": EntityStatusType,
        "PerformanceMetrics": PerformanceMetricsTypeDef,
        "LogUri": str,
        "Message": str,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PredictOutputTypeDef = TypedDict(
    "PredictOutputTypeDef",
    {
        "Prediction": PredictionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRDSDataSpecTypeDef = TypedDict(
    "_RequiredRDSDataSpecTypeDef",
    {
        "DatabaseInformation": RDSDatabaseTypeDef,
        "SelectSqlQuery": str,
        "DatabaseCredentials": RDSDatabaseCredentialsTypeDef,
        "S3StagingLocation": str,
        "ResourceRole": str,
        "ServiceRole": str,
        "SubnetId": str,
        "SecurityGroupIds": Sequence[str],
    },
)
_OptionalRDSDataSpecTypeDef = TypedDict(
    "_OptionalRDSDataSpecTypeDef",
    {
        "DataRearrangement": str,
        "DataSchema": str,
        "DataSchemaUri": str,
    },
    total=False,
)

class RDSDataSpecTypeDef(_RequiredRDSDataSpecTypeDef, _OptionalRDSDataSpecTypeDef):
    pass

RDSMetadataTypeDef = TypedDict(
    "RDSMetadataTypeDef",
    {
        "Database": RDSDatabaseTypeDef,
        "DatabaseUserName": str,
        "SelectSqlQuery": str,
        "ResourceRole": str,
        "ServiceRole": str,
        "DataPipelineId": str,
    },
    total=False,
)

_RequiredRedshiftDataSpecTypeDef = TypedDict(
    "_RequiredRedshiftDataSpecTypeDef",
    {
        "DatabaseInformation": RedshiftDatabaseTypeDef,
        "SelectSqlQuery": str,
        "DatabaseCredentials": RedshiftDatabaseCredentialsTypeDef,
        "S3StagingLocation": str,
    },
)
_OptionalRedshiftDataSpecTypeDef = TypedDict(
    "_OptionalRedshiftDataSpecTypeDef",
    {
        "DataRearrangement": str,
        "DataSchema": str,
        "DataSchemaUri": str,
    },
    total=False,
)

class RedshiftDataSpecTypeDef(_RequiredRedshiftDataSpecTypeDef, _OptionalRedshiftDataSpecTypeDef):
    pass

RedshiftMetadataTypeDef = TypedDict(
    "RedshiftMetadataTypeDef",
    {
        "RedshiftDatabase": RedshiftDatabaseTypeDef,
        "DatabaseUserName": str,
        "SelectSqlQuery": str,
    },
    total=False,
)

DescribeMLModelsOutputTypeDef = TypedDict(
    "DescribeMLModelsOutputTypeDef",
    {
        "Results": List[MLModelTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEvaluationsOutputTypeDef = TypedDict(
    "DescribeEvaluationsOutputTypeDef",
    {
        "Results": List[EvaluationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDataSourceFromRDSInputRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceFromRDSInputRequestTypeDef",
    {
        "DataSourceId": str,
        "RDSData": RDSDataSpecTypeDef,
        "RoleARN": str,
    },
)
_OptionalCreateDataSourceFromRDSInputRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceFromRDSInputRequestTypeDef",
    {
        "DataSourceName": str,
        "ComputeStatistics": bool,
    },
    total=False,
)

class CreateDataSourceFromRDSInputRequestTypeDef(
    _RequiredCreateDataSourceFromRDSInputRequestTypeDef,
    _OptionalCreateDataSourceFromRDSInputRequestTypeDef,
):
    pass

_RequiredCreateDataSourceFromRedshiftInputRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceFromRedshiftInputRequestTypeDef",
    {
        "DataSourceId": str,
        "DataSpec": RedshiftDataSpecTypeDef,
        "RoleARN": str,
    },
)
_OptionalCreateDataSourceFromRedshiftInputRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceFromRedshiftInputRequestTypeDef",
    {
        "DataSourceName": str,
        "ComputeStatistics": bool,
    },
    total=False,
)

class CreateDataSourceFromRedshiftInputRequestTypeDef(
    _RequiredCreateDataSourceFromRedshiftInputRequestTypeDef,
    _OptionalCreateDataSourceFromRedshiftInputRequestTypeDef,
):
    pass

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "DataSourceId": str,
        "DataLocationS3": str,
        "DataRearrangement": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "DataSizeInBytes": int,
        "NumberOfFiles": int,
        "Name": str,
        "Status": EntityStatusType,
        "Message": str,
        "RedshiftMetadata": RedshiftMetadataTypeDef,
        "RDSMetadata": RDSMetadataTypeDef,
        "RoleARN": str,
        "ComputeStatistics": bool,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
    },
    total=False,
)

GetDataSourceOutputTypeDef = TypedDict(
    "GetDataSourceOutputTypeDef",
    {
        "DataSourceId": str,
        "DataLocationS3": str,
        "DataRearrangement": str,
        "CreatedByIamUser": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "DataSizeInBytes": int,
        "NumberOfFiles": int,
        "Name": str,
        "Status": EntityStatusType,
        "LogUri": str,
        "Message": str,
        "RedshiftMetadata": RedshiftMetadataTypeDef,
        "RDSMetadata": RDSMetadataTypeDef,
        "RoleARN": str,
        "ComputeStatistics": bool,
        "ComputeTime": int,
        "FinishedAt": datetime,
        "StartedAt": datetime,
        "DataSourceSchema": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSourcesOutputTypeDef = TypedDict(
    "DescribeDataSourcesOutputTypeDef",
    {
        "Results": List[DataSourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
