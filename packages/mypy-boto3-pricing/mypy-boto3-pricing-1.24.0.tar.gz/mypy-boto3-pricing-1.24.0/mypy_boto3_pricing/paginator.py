"""
Type annotations for pricing service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pricing.client import PricingClient
    from mypy_boto3_pricing.paginator import (
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
    )

    session = Session()
    client: PricingClient = session.client("pricing")

    describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
    get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
    get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeServicesResponseTypeDef,
    FilterTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeServicesPaginator", "GetAttributeValuesPaginator", "GetProductsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeServicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.DescribeServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#describeservicespaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        FormatVersion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.DescribeServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#describeservicespaginator)
        """


class GetAttributeValuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetAttributeValues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getattributevaluespaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str,
        AttributeName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAttributeValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetAttributeValues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getattributevaluespaginator)
        """


class GetProductsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetProducts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getproductspaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        FormatVersion: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetProducts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/paginators/#getproductspaginator)
        """
