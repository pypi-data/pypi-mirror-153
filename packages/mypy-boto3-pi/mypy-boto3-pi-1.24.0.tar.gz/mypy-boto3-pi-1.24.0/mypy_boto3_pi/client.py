"""
Type annotations for pi service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pi.client import PIClient

    session = Session()
    client: PIClient = session.client("pi")
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import ServiceTypeType
from .type_defs import (
    DescribeDimensionKeysResponseTypeDef,
    DimensionGroupTypeDef,
    GetDimensionKeyDetailsResponseTypeDef,
    GetResourceMetadataResponseTypeDef,
    GetResourceMetricsResponseTypeDef,
    ListAvailableResourceDimensionsResponseTypeDef,
    ListAvailableResourceMetricsResponseTypeDef,
    MetricQueryTypeDef,
)

__all__ = ("PIClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]


class PIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#can_paginate)
        """

    def describe_dimension_keys(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        Metric: str,
        GroupBy: DimensionGroupTypeDef,
        PeriodInSeconds: int = ...,
        AdditionalMetrics: Sequence[str] = ...,
        PartitionBy: DimensionGroupTypeDef = ...,
        Filter: Mapping[str, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeDimensionKeysResponseTypeDef:
        """
        For a specific time period, retrieve the top `N` dimension keys for a metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.describe_dimension_keys)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#describe_dimension_keys)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#generate_presigned_url)
        """

    def get_dimension_key_details(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        Group: str,
        GroupIdentifier: str,
        RequestedDimensions: Sequence[str] = ...
    ) -> GetDimensionKeyDetailsResponseTypeDef:
        """
        Get the attributes of the specified dimension group for a DB instance or data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_dimension_key_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#get_dimension_key_details)
        """

    def get_resource_metadata(
        self, *, ServiceType: ServiceTypeType, Identifier: str
    ) -> GetResourceMetadataResponseTypeDef:
        """
        Retrieve the metadata for different features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_resource_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#get_resource_metadata)
        """

    def get_resource_metrics(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        MetricQueries: Sequence[MetricQueryTypeDef],
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        PeriodInSeconds: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetResourceMetricsResponseTypeDef:
        """
        Retrieve Performance Insights metrics for a set of data sources over a time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_resource_metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#get_resource_metrics)
        """

    def list_available_resource_dimensions(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        Metrics: Sequence[str],
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAvailableResourceDimensionsResponseTypeDef:
        """
        Retrieve the dimensions that can be queried for each specified metric type on a
        specified DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_available_resource_dimensions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#list_available_resource_dimensions)
        """

    def list_available_resource_metrics(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        MetricTypes: Sequence[str],
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListAvailableResourceMetricsResponseTypeDef:
        """
        Retrieve metrics of the specified types that can be queried for a specified DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_available_resource_metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/client/#list_available_resource_metrics)
        """
