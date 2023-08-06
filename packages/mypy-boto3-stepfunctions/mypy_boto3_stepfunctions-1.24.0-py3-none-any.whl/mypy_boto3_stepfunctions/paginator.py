"""
Type annotations for stepfunctions service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_stepfunctions.client import SFNClient
    from mypy_boto3_stepfunctions.paginator import (
        GetExecutionHistoryPaginator,
        ListActivitiesPaginator,
        ListExecutionsPaginator,
        ListStateMachinesPaginator,
    )

    session = Session()
    client: SFNClient = session.client("stepfunctions")

    get_execution_history_paginator: GetExecutionHistoryPaginator = client.get_paginator("get_execution_history")
    list_activities_paginator: ListActivitiesPaginator = client.get_paginator("list_activities")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_state_machines_paginator: ListStateMachinesPaginator = client.get_paginator("list_state_machines")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ExecutionStatusType
from .type_defs import (
    GetExecutionHistoryOutputTypeDef,
    ListActivitiesOutputTypeDef,
    ListExecutionsOutputTypeDef,
    ListStateMachinesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetExecutionHistoryPaginator",
    "ListActivitiesPaginator",
    "ListExecutionsPaginator",
    "ListStateMachinesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetExecutionHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.GetExecutionHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#getexecutionhistorypaginator)
    """

    def paginate(
        self,
        *,
        executionArn: str,
        reverseOrder: bool = ...,
        includeExecutionData: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetExecutionHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.GetExecutionHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#getexecutionhistorypaginator)
        """


class ListActivitiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListActivities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listactivitiespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListActivities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listactivitiespaginator)
        """


class ListExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listexecutionspaginator)
    """

    def paginate(
        self,
        *,
        stateMachineArn: str,
        statusFilter: ExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listexecutionspaginator)
        """


class ListStateMachinesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListStateMachines)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#liststatemachinespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStateMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Paginator.ListStateMachines.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#liststatemachinespaginator)
        """
