"""
Type annotations for machinelearning service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_machinelearning.client import MachineLearningClient
    from mypy_boto3_machinelearning.waiter import (
        BatchPredictionAvailableWaiter,
        DataSourceAvailableWaiter,
        EvaluationAvailableWaiter,
        MLModelAvailableWaiter,
    )

    session = Session()
    client: MachineLearningClient = session.client("machinelearning")

    batch_prediction_available_waiter: BatchPredictionAvailableWaiter = client.get_waiter("batch_prediction_available")
    data_source_available_waiter: DataSourceAvailableWaiter = client.get_waiter("data_source_available")
    evaluation_available_waiter: EvaluationAvailableWaiter = client.get_waiter("evaluation_available")
    ml_model_available_waiter: MLModelAvailableWaiter = client.get_waiter("ml_model_available")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .literals import (
    BatchPredictionFilterVariableType,
    DataSourceFilterVariableType,
    EvaluationFilterVariableType,
    MLModelFilterVariableType,
    SortOrderType,
)
from .type_defs import WaiterConfigTypeDef

__all__ = (
    "BatchPredictionAvailableWaiter",
    "DataSourceAvailableWaiter",
    "EvaluationAvailableWaiter",
    "MLModelAvailableWaiter",
)


class BatchPredictionAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.BatchPredictionAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#batchpredictionavailablewaiter)
    """

    def wait(
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
        NextToken: str = ...,
        Limit: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.BatchPredictionAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#batchpredictionavailablewaiter)
        """


class DataSourceAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.DataSourceAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#datasourceavailablewaiter)
    """

    def wait(
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
        NextToken: str = ...,
        Limit: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.DataSourceAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#datasourceavailablewaiter)
        """


class EvaluationAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.EvaluationAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#evaluationavailablewaiter)
    """

    def wait(
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
        NextToken: str = ...,
        Limit: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.EvaluationAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#evaluationavailablewaiter)
        """


class MLModelAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.MLModelAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#mlmodelavailablewaiter)
    """

    def wait(
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
        NextToken: str = ...,
        Limit: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning.Waiter.MLModelAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/waiters/#mlmodelavailablewaiter)
        """
