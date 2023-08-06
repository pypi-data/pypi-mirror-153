"""
Type annotations for marketplace-entitlement service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_entitlement/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplace_entitlement.type_defs import EntitlementValueTypeDef

    data: EntitlementValueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import GetEntitlementFilterNameType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EntitlementValueTypeDef",
    "PaginatorConfigTypeDef",
    "GetEntitlementsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "EntitlementTypeDef",
    "GetEntitlementsRequestGetEntitlementsPaginateTypeDef",
    "GetEntitlementsResultTypeDef",
)

EntitlementValueTypeDef = TypedDict(
    "EntitlementValueTypeDef",
    {
        "IntegerValue": int,
        "DoubleValue": float,
        "BooleanValue": bool,
        "StringValue": str,
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

_RequiredGetEntitlementsRequestRequestTypeDef = TypedDict(
    "_RequiredGetEntitlementsRequestRequestTypeDef",
    {
        "ProductCode": str,
    },
)
_OptionalGetEntitlementsRequestRequestTypeDef = TypedDict(
    "_OptionalGetEntitlementsRequestRequestTypeDef",
    {
        "Filter": Mapping[GetEntitlementFilterNameType, Sequence[str]],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetEntitlementsRequestRequestTypeDef(
    _RequiredGetEntitlementsRequestRequestTypeDef, _OptionalGetEntitlementsRequestRequestTypeDef
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

EntitlementTypeDef = TypedDict(
    "EntitlementTypeDef",
    {
        "ProductCode": str,
        "Dimension": str,
        "CustomerIdentifier": str,
        "Value": EntitlementValueTypeDef,
        "ExpirationDate": datetime,
    },
    total=False,
)

_RequiredGetEntitlementsRequestGetEntitlementsPaginateTypeDef = TypedDict(
    "_RequiredGetEntitlementsRequestGetEntitlementsPaginateTypeDef",
    {
        "ProductCode": str,
    },
)
_OptionalGetEntitlementsRequestGetEntitlementsPaginateTypeDef = TypedDict(
    "_OptionalGetEntitlementsRequestGetEntitlementsPaginateTypeDef",
    {
        "Filter": Mapping[GetEntitlementFilterNameType, Sequence[str]],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetEntitlementsRequestGetEntitlementsPaginateTypeDef(
    _RequiredGetEntitlementsRequestGetEntitlementsPaginateTypeDef,
    _OptionalGetEntitlementsRequestGetEntitlementsPaginateTypeDef,
):
    pass


GetEntitlementsResultTypeDef = TypedDict(
    "GetEntitlementsResultTypeDef",
    {
        "Entitlements": List[EntitlementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
