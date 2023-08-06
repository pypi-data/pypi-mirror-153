"""
Type annotations for rum service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/type_defs/)

Usage::

    ```python
    from mypy_boto3_rum.type_defs import AppMonitorConfigurationTypeDef

    data: AppMonitorConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import StateEnumType, TelemetryType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AppMonitorConfigurationTypeDef",
    "AppMonitorDetailsTypeDef",
    "AppMonitorSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "CwLogTypeDef",
    "DeleteAppMonitorRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "QueryFilterTypeDef",
    "TimeRangeTypeDef",
    "GetAppMonitorRequestRequestTypeDef",
    "ListAppMonitorsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RumEventTypeDef",
    "UserDetailsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateAppMonitorRequestRequestTypeDef",
    "UpdateAppMonitorRequestRequestTypeDef",
    "CreateAppMonitorResponseTypeDef",
    "GetAppMonitorDataResponseTypeDef",
    "ListAppMonitorsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DataStorageTypeDef",
    "ListAppMonitorsRequestListAppMonitorsPaginateTypeDef",
    "GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    "GetAppMonitorDataRequestRequestTypeDef",
    "PutRumEventsRequestRequestTypeDef",
    "AppMonitorTypeDef",
    "GetAppMonitorResponseTypeDef",
)

AppMonitorConfigurationTypeDef = TypedDict(
    "AppMonitorConfigurationTypeDef",
    {
        "AllowCookies": bool,
        "EnableXRay": bool,
        "ExcludedPages": Sequence[str],
        "FavoritePages": Sequence[str],
        "GuestRoleArn": str,
        "IdentityPoolId": str,
        "IncludedPages": Sequence[str],
        "SessionSampleRate": float,
        "Telemetries": Sequence[TelemetryType],
    },
    total=False,
)

AppMonitorDetailsTypeDef = TypedDict(
    "AppMonitorDetailsTypeDef",
    {
        "id": str,
        "name": str,
        "version": str,
    },
    total=False,
)

AppMonitorSummaryTypeDef = TypedDict(
    "AppMonitorSummaryTypeDef",
    {
        "Created": str,
        "Id": str,
        "LastModified": str,
        "Name": str,
        "State": StateEnumType,
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

CwLogTypeDef = TypedDict(
    "CwLogTypeDef",
    {
        "CwLogEnabled": bool,
        "CwLogGroup": str,
    },
    total=False,
)

DeleteAppMonitorRequestRequestTypeDef = TypedDict(
    "DeleteAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
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

QueryFilterTypeDef = TypedDict(
    "QueryFilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

_RequiredTimeRangeTypeDef = TypedDict(
    "_RequiredTimeRangeTypeDef",
    {
        "After": int,
    },
)
_OptionalTimeRangeTypeDef = TypedDict(
    "_OptionalTimeRangeTypeDef",
    {
        "Before": int,
    },
    total=False,
)


class TimeRangeTypeDef(_RequiredTimeRangeTypeDef, _OptionalTimeRangeTypeDef):
    pass


GetAppMonitorRequestRequestTypeDef = TypedDict(
    "GetAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ListAppMonitorsRequestRequestTypeDef = TypedDict(
    "ListAppMonitorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredRumEventTypeDef = TypedDict(
    "_RequiredRumEventTypeDef",
    {
        "details": str,
        "id": str,
        "timestamp": Union[datetime, str],
        "type": str,
    },
)
_OptionalRumEventTypeDef = TypedDict(
    "_OptionalRumEventTypeDef",
    {
        "metadata": str,
    },
    total=False,
)


class RumEventTypeDef(_RequiredRumEventTypeDef, _OptionalRumEventTypeDef):
    pass


UserDetailsTypeDef = TypedDict(
    "UserDetailsTypeDef",
    {
        "sessionId": str,
        "userId": str,
    },
    total=False,
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

_RequiredCreateAppMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppMonitorRequestRequestTypeDef",
    {
        "Domain": str,
        "Name": str,
    },
)
_OptionalCreateAppMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppMonitorRequestRequestTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "CwLogEnabled": bool,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateAppMonitorRequestRequestTypeDef(
    _RequiredCreateAppMonitorRequestRequestTypeDef, _OptionalCreateAppMonitorRequestRequestTypeDef
):
    pass


_RequiredUpdateAppMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateAppMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppMonitorRequestRequestTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "CwLogEnabled": bool,
        "Domain": str,
    },
    total=False,
)


class UpdateAppMonitorRequestRequestTypeDef(
    _RequiredUpdateAppMonitorRequestRequestTypeDef, _OptionalUpdateAppMonitorRequestRequestTypeDef
):
    pass


CreateAppMonitorResponseTypeDef = TypedDict(
    "CreateAppMonitorResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppMonitorDataResponseTypeDef = TypedDict(
    "GetAppMonitorDataResponseTypeDef",
    {
        "Events": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppMonitorsResponseTypeDef = TypedDict(
    "ListAppMonitorsResponseTypeDef",
    {
        "AppMonitorSummaries": List[AppMonitorSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataStorageTypeDef = TypedDict(
    "DataStorageTypeDef",
    {
        "CwLog": CwLogTypeDef,
    },
    total=False,
)

ListAppMonitorsRequestListAppMonitorsPaginateTypeDef = TypedDict(
    "ListAppMonitorsRequestListAppMonitorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef = TypedDict(
    "_RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    {
        "Name": str,
        "TimeRange": TimeRangeTypeDef,
    },
)
_OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef = TypedDict(
    "_OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    {
        "Filters": Sequence[QueryFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef(
    _RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
    _OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
):
    pass


_RequiredGetAppMonitorDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetAppMonitorDataRequestRequestTypeDef",
    {
        "Name": str,
        "TimeRange": TimeRangeTypeDef,
    },
)
_OptionalGetAppMonitorDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetAppMonitorDataRequestRequestTypeDef",
    {
        "Filters": Sequence[QueryFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetAppMonitorDataRequestRequestTypeDef(
    _RequiredGetAppMonitorDataRequestRequestTypeDef, _OptionalGetAppMonitorDataRequestRequestTypeDef
):
    pass


PutRumEventsRequestRequestTypeDef = TypedDict(
    "PutRumEventsRequestRequestTypeDef",
    {
        "AppMonitorDetails": AppMonitorDetailsTypeDef,
        "BatchId": str,
        "Id": str,
        "RumEvents": Sequence[RumEventTypeDef],
        "UserDetails": UserDetailsTypeDef,
    },
)

AppMonitorTypeDef = TypedDict(
    "AppMonitorTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "Created": str,
        "DataStorage": DataStorageTypeDef,
        "Domain": str,
        "Id": str,
        "LastModified": str,
        "Name": str,
        "State": StateEnumType,
        "Tags": Dict[str, str],
    },
    total=False,
)

GetAppMonitorResponseTypeDef = TypedDict(
    "GetAppMonitorResponseTypeDef",
    {
        "AppMonitor": AppMonitorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
