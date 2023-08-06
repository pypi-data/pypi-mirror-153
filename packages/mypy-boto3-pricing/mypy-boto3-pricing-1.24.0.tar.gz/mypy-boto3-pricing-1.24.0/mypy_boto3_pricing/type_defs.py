"""
Type annotations for pricing service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/type_defs/)

Usage::

    ```python
    from mypy_boto3_pricing.type_defs import AttributeValueTypeDef

    data: AttributeValueTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AttributeValueTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceTypeDef",
    "FilterTypeDef",
    "GetAttributeValuesRequestRequestTypeDef",
    "DescribeServicesRequestDescribeServicesPaginateTypeDef",
    "GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    "GetAttributeValuesResponseTypeDef",
    "GetProductsResponseTypeDef",
    "DescribeServicesResponseTypeDef",
    "GetProductsRequestGetProductsPaginateTypeDef",
    "GetProductsRequestRequestTypeDef",
)

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "Value": str,
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

DescribeServicesRequestRequestTypeDef = TypedDict(
    "DescribeServicesRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "FormatVersion": str,
        "NextToken": str,
        "MaxResults": int,
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

ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "ServiceCode": str,
        "AttributeNames": List[str],
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Type": Literal["TERM_MATCH"],
        "Field": str,
        "Value": str,
    },
)

_RequiredGetAttributeValuesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAttributeValuesRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "AttributeName": str,
    },
)
_OptionalGetAttributeValuesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAttributeValuesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetAttributeValuesRequestRequestTypeDef(
    _RequiredGetAttributeValuesRequestRequestTypeDef,
    _OptionalGetAttributeValuesRequestRequestTypeDef,
):
    pass


DescribeServicesRequestDescribeServicesPaginateTypeDef = TypedDict(
    "DescribeServicesRequestDescribeServicesPaginateTypeDef",
    {
        "ServiceCode": str,
        "FormatVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef = TypedDict(
    "_RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    {
        "ServiceCode": str,
        "AttributeName": str,
    },
)
_OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef = TypedDict(
    "_OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef(
    _RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
    _OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
):
    pass


GetAttributeValuesResponseTypeDef = TypedDict(
    "GetAttributeValuesResponseTypeDef",
    {
        "AttributeValues": List[AttributeValueTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProductsResponseTypeDef = TypedDict(
    "GetProductsResponseTypeDef",
    {
        "FormatVersion": str,
        "PriceList": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeServicesResponseTypeDef = TypedDict(
    "DescribeServicesResponseTypeDef",
    {
        "Services": List[ServiceTypeDef],
        "FormatVersion": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProductsRequestGetProductsPaginateTypeDef = TypedDict(
    "GetProductsRequestGetProductsPaginateTypeDef",
    {
        "ServiceCode": str,
        "Filters": Sequence[FilterTypeDef],
        "FormatVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetProductsRequestRequestTypeDef = TypedDict(
    "GetProductsRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "Filters": Sequence[FilterTypeDef],
        "FormatVersion": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)
