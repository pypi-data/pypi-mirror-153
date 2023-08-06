"""
Type annotations for pi service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/type_defs/)

Usage::

    ```python
    from mypy_boto3_pi.type_defs import DataPointTypeDef

    data: DataPointTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import DetailStatusType, FeatureStatusType, ServiceTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DataPointTypeDef",
    "DimensionGroupTypeDef",
    "DimensionKeyDescriptionTypeDef",
    "ResponseMetadataTypeDef",
    "ResponsePartitionKeyTypeDef",
    "DimensionDetailTypeDef",
    "DimensionKeyDetailTypeDef",
    "FeatureMetadataTypeDef",
    "GetDimensionKeyDetailsRequestRequestTypeDef",
    "GetResourceMetadataRequestRequestTypeDef",
    "ListAvailableResourceDimensionsRequestRequestTypeDef",
    "ListAvailableResourceMetricsRequestRequestTypeDef",
    "ResponseResourceMetricTypeDef",
    "ResponseResourceMetricKeyTypeDef",
    "DescribeDimensionKeysRequestRequestTypeDef",
    "MetricQueryTypeDef",
    "DescribeDimensionKeysResponseTypeDef",
    "DimensionGroupDetailTypeDef",
    "GetDimensionKeyDetailsResponseTypeDef",
    "GetResourceMetadataResponseTypeDef",
    "ListAvailableResourceMetricsResponseTypeDef",
    "MetricKeyDataPointsTypeDef",
    "GetResourceMetricsRequestRequestTypeDef",
    "MetricDimensionGroupsTypeDef",
    "GetResourceMetricsResponseTypeDef",
    "ListAvailableResourceDimensionsResponseTypeDef",
)

DataPointTypeDef = TypedDict(
    "DataPointTypeDef",
    {
        "Timestamp": datetime,
        "Value": float,
    },
)

_RequiredDimensionGroupTypeDef = TypedDict(
    "_RequiredDimensionGroupTypeDef",
    {
        "Group": str,
    },
)
_OptionalDimensionGroupTypeDef = TypedDict(
    "_OptionalDimensionGroupTypeDef",
    {
        "Dimensions": Sequence[str],
        "Limit": int,
    },
    total=False,
)

class DimensionGroupTypeDef(_RequiredDimensionGroupTypeDef, _OptionalDimensionGroupTypeDef):
    pass

DimensionKeyDescriptionTypeDef = TypedDict(
    "DimensionKeyDescriptionTypeDef",
    {
        "Dimensions": Dict[str, str],
        "Total": float,
        "AdditionalMetrics": Dict[str, float],
        "Partitions": List[float],
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

ResponsePartitionKeyTypeDef = TypedDict(
    "ResponsePartitionKeyTypeDef",
    {
        "Dimensions": Dict[str, str],
    },
)

DimensionDetailTypeDef = TypedDict(
    "DimensionDetailTypeDef",
    {
        "Identifier": str,
    },
    total=False,
)

DimensionKeyDetailTypeDef = TypedDict(
    "DimensionKeyDetailTypeDef",
    {
        "Value": str,
        "Dimension": str,
        "Status": DetailStatusType,
    },
    total=False,
)

FeatureMetadataTypeDef = TypedDict(
    "FeatureMetadataTypeDef",
    {
        "Status": FeatureStatusType,
    },
    total=False,
)

_RequiredGetDimensionKeyDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGetDimensionKeyDetailsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "Group": str,
        "GroupIdentifier": str,
    },
)
_OptionalGetDimensionKeyDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGetDimensionKeyDetailsRequestRequestTypeDef",
    {
        "RequestedDimensions": Sequence[str],
    },
    total=False,
)

class GetDimensionKeyDetailsRequestRequestTypeDef(
    _RequiredGetDimensionKeyDetailsRequestRequestTypeDef,
    _OptionalGetDimensionKeyDetailsRequestRequestTypeDef,
):
    pass

GetResourceMetadataRequestRequestTypeDef = TypedDict(
    "GetResourceMetadataRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
    },
)

_RequiredListAvailableResourceDimensionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableResourceDimensionsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "Metrics": Sequence[str],
    },
)
_OptionalListAvailableResourceDimensionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableResourceDimensionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListAvailableResourceDimensionsRequestRequestTypeDef(
    _RequiredListAvailableResourceDimensionsRequestRequestTypeDef,
    _OptionalListAvailableResourceDimensionsRequestRequestTypeDef,
):
    pass

_RequiredListAvailableResourceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableResourceMetricsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "MetricTypes": Sequence[str],
    },
)
_OptionalListAvailableResourceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableResourceMetricsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListAvailableResourceMetricsRequestRequestTypeDef(
    _RequiredListAvailableResourceMetricsRequestRequestTypeDef,
    _OptionalListAvailableResourceMetricsRequestRequestTypeDef,
):
    pass

ResponseResourceMetricTypeDef = TypedDict(
    "ResponseResourceMetricTypeDef",
    {
        "Metric": str,
        "Description": str,
        "Unit": str,
    },
    total=False,
)

_RequiredResponseResourceMetricKeyTypeDef = TypedDict(
    "_RequiredResponseResourceMetricKeyTypeDef",
    {
        "Metric": str,
    },
)
_OptionalResponseResourceMetricKeyTypeDef = TypedDict(
    "_OptionalResponseResourceMetricKeyTypeDef",
    {
        "Dimensions": Dict[str, str],
    },
    total=False,
)

class ResponseResourceMetricKeyTypeDef(
    _RequiredResponseResourceMetricKeyTypeDef, _OptionalResponseResourceMetricKeyTypeDef
):
    pass

_RequiredDescribeDimensionKeysRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDimensionKeysRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Metric": str,
        "GroupBy": DimensionGroupTypeDef,
    },
)
_OptionalDescribeDimensionKeysRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDimensionKeysRequestRequestTypeDef",
    {
        "PeriodInSeconds": int,
        "AdditionalMetrics": Sequence[str],
        "PartitionBy": DimensionGroupTypeDef,
        "Filter": Mapping[str, str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class DescribeDimensionKeysRequestRequestTypeDef(
    _RequiredDescribeDimensionKeysRequestRequestTypeDef,
    _OptionalDescribeDimensionKeysRequestRequestTypeDef,
):
    pass

_RequiredMetricQueryTypeDef = TypedDict(
    "_RequiredMetricQueryTypeDef",
    {
        "Metric": str,
    },
)
_OptionalMetricQueryTypeDef = TypedDict(
    "_OptionalMetricQueryTypeDef",
    {
        "GroupBy": DimensionGroupTypeDef,
        "Filter": Mapping[str, str],
    },
    total=False,
)

class MetricQueryTypeDef(_RequiredMetricQueryTypeDef, _OptionalMetricQueryTypeDef):
    pass

DescribeDimensionKeysResponseTypeDef = TypedDict(
    "DescribeDimensionKeysResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "PartitionKeys": List[ResponsePartitionKeyTypeDef],
        "Keys": List[DimensionKeyDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DimensionGroupDetailTypeDef = TypedDict(
    "DimensionGroupDetailTypeDef",
    {
        "Group": str,
        "Dimensions": List[DimensionDetailTypeDef],
    },
    total=False,
)

GetDimensionKeyDetailsResponseTypeDef = TypedDict(
    "GetDimensionKeyDetailsResponseTypeDef",
    {
        "Dimensions": List[DimensionKeyDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceMetadataResponseTypeDef = TypedDict(
    "GetResourceMetadataResponseTypeDef",
    {
        "Identifier": str,
        "Features": Dict[str, FeatureMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableResourceMetricsResponseTypeDef = TypedDict(
    "ListAvailableResourceMetricsResponseTypeDef",
    {
        "Metrics": List[ResponseResourceMetricTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricKeyDataPointsTypeDef = TypedDict(
    "MetricKeyDataPointsTypeDef",
    {
        "Key": ResponseResourceMetricKeyTypeDef,
        "DataPoints": List[DataPointTypeDef],
    },
    total=False,
)

_RequiredGetResourceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceMetricsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "MetricQueries": Sequence[MetricQueryTypeDef],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalGetResourceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceMetricsRequestRequestTypeDef",
    {
        "PeriodInSeconds": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetResourceMetricsRequestRequestTypeDef(
    _RequiredGetResourceMetricsRequestRequestTypeDef,
    _OptionalGetResourceMetricsRequestRequestTypeDef,
):
    pass

MetricDimensionGroupsTypeDef = TypedDict(
    "MetricDimensionGroupsTypeDef",
    {
        "Metric": str,
        "Groups": List[DimensionGroupDetailTypeDef],
    },
    total=False,
)

GetResourceMetricsResponseTypeDef = TypedDict(
    "GetResourceMetricsResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "Identifier": str,
        "MetricList": List[MetricKeyDataPointsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableResourceDimensionsResponseTypeDef = TypedDict(
    "ListAvailableResourceDimensionsResponseTypeDef",
    {
        "MetricDimensions": List[MetricDimensionGroupsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
