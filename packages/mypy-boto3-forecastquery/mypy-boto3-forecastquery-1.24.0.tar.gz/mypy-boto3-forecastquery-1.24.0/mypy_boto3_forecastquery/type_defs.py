"""
Type annotations for forecastquery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecastquery/type_defs/)

Usage::

    ```python
    from mypy_boto3_forecastquery.type_defs import DataPointTypeDef

    data: DataPointTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DataPointTypeDef",
    "QueryForecastRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ForecastTypeDef",
    "QueryForecastResponseTypeDef",
)

DataPointTypeDef = TypedDict(
    "DataPointTypeDef",
    {
        "Timestamp": str,
        "Value": float,
    },
    total=False,
)

_RequiredQueryForecastRequestRequestTypeDef = TypedDict(
    "_RequiredQueryForecastRequestRequestTypeDef",
    {
        "ForecastArn": str,
        "Filters": Mapping[str, str],
    },
)
_OptionalQueryForecastRequestRequestTypeDef = TypedDict(
    "_OptionalQueryForecastRequestRequestTypeDef",
    {
        "StartDate": str,
        "EndDate": str,
        "NextToken": str,
    },
    total=False,
)


class QueryForecastRequestRequestTypeDef(
    _RequiredQueryForecastRequestRequestTypeDef, _OptionalQueryForecastRequestRequestTypeDef
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

ForecastTypeDef = TypedDict(
    "ForecastTypeDef",
    {
        "Predictions": Dict[str, List[DataPointTypeDef]],
    },
    total=False,
)

QueryForecastResponseTypeDef = TypedDict(
    "QueryForecastResponseTypeDef",
    {
        "Forecast": ForecastTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
