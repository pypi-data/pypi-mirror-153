"""
Type annotations for rum service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rum.client import CloudWatchRUMClient
    from mypy_boto3_rum.paginator import (
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
    )

    session = Session()
    client: CloudWatchRUMClient = session.client("rum")

    get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
    list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GetAppMonitorDataResponseTypeDef,
    ListAppMonitorsResponseTypeDef,
    PaginatorConfigTypeDef,
    QueryFilterTypeDef,
    TimeRangeTypeDef,
)

__all__ = ("GetAppMonitorDataPaginator", "ListAppMonitorsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetAppMonitorDataPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.GetAppMonitorData)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#getappmonitordatapaginator)
    """

    def paginate(
        self,
        *,
        Name: str,
        TimeRange: TimeRangeTypeDef,
        Filters: Sequence[QueryFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAppMonitorDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.GetAppMonitorData.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#getappmonitordatapaginator)
        """


class ListAppMonitorsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.ListAppMonitors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listappmonitorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Paginator.ListAppMonitors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/paginators/#listappmonitorspaginator)
        """
