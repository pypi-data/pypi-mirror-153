"""
Type annotations for machinelearning service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_machinelearning.client import MachineLearningClient
    from mypy_boto3_machinelearning.paginator import (
        DescribeBatchPredictionsPaginator,
        DescribeDataSourcesPaginator,
        DescribeEvaluationsPaginator,
        DescribeMLModelsPaginator,
    )

    session = Session()
    client: MachineLearningClient = session.client("machinelearning")

    describe_batch_predictions_paginator: DescribeBatchPredictionsPaginator = client.get_paginator("describe_batch_predictions")
    describe_data_sources_paginator: DescribeDataSourcesPaginator = client.get_paginator("describe_data_sources")
    describe_evaluations_paginator: DescribeEvaluationsPaginator = client.get_paginator("describe_evaluations")
    describe_ml_models_paginator: DescribeMLModelsPaginator = client.get_paginator("describe_ml_models")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    BatchPredictionFilterVariableType,
    DataSourceFilterVariableType,
    EvaluationFilterVariableType,
    MLModelFilterVariableType,
    SortOrderType,
)
from .type_defs import (
    DescribeBatchPredictionsOutputTypeDef,
    DescribeDataSourcesOutputTypeDef,
    DescribeEvaluationsOutputTypeDef,
    DescribeMLModelsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeBatchPredictionsPaginator",
    "DescribeDataSourcesPaginator",
    "DescribeEvaluationsPaginator",
    "DescribeMLModelsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeBatchPredictionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeBatchPredictions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describebatchpredictionspaginator)
    """

    def paginate(
        self,
        *,
        FilterVariable: BatchPredictionFilterVariableType = ...,
        EQ: str = ...,
        GT: str = ...,
        LT: str = ...,
        GE: str = ...,
        LE: str = ...,
        NE: str = ...,
        Prefix: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBatchPredictionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeBatchPredictions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describebatchpredictionspaginator)
        """


class DescribeDataSourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeDataSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describedatasourcespaginator)
    """

    def paginate(
        self,
        *,
        FilterVariable: DataSourceFilterVariableType = ...,
        EQ: str = ...,
        GT: str = ...,
        LT: str = ...,
        GE: str = ...,
        LE: str = ...,
        NE: str = ...,
        Prefix: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDataSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeDataSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describedatasourcespaginator)
        """


class DescribeEvaluationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeEvaluations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describeevaluationspaginator)
    """

    def paginate(
        self,
        *,
        FilterVariable: EvaluationFilterVariableType = ...,
        EQ: str = ...,
        GT: str = ...,
        LT: str = ...,
        GE: str = ...,
        LE: str = ...,
        NE: str = ...,
        Prefix: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEvaluationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeEvaluations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describeevaluationspaginator)
        """


class DescribeMLModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeMLModels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describemlmodelspaginator)
    """

    def paginate(
        self,
        *,
        FilterVariable: MLModelFilterVariableType = ...,
        EQ: str = ...,
        GT: str = ...,
        LT: str = ...,
        GE: str = ...,
        LE: str = ...,
        NE: str = ...,
        Prefix: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMLModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Paginator.DescribeMLModels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describemlmodelspaginator)
        """
