"""
Type annotations for sdb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sdb/type_defs/)

Usage::

    ```python
    from mypy_boto3_sdb.type_defs import AttributeTypeDef

    data: AttributeTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AttributeTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "UpdateConditionTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DomainMetadataRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetAttributesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ReplaceableAttributeTypeDef",
    "SelectRequestRequestTypeDef",
    "DeletableItemTypeDef",
    "ItemTypeDef",
    "DeleteAttributesRequestRequestTypeDef",
    "DomainMetadataResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAttributesResultTypeDef",
    "ListDomainsResultTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "SelectRequestSelectPaginateTypeDef",
    "PutAttributesRequestRequestTypeDef",
    "ReplaceableItemTypeDef",
    "BatchDeleteAttributesRequestRequestTypeDef",
    "SelectResultTypeDef",
    "BatchPutAttributesRequestRequestTypeDef",
)

_RequiredAttributeTypeDef = TypedDict(
    "_RequiredAttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalAttributeTypeDef = TypedDict(
    "_OptionalAttributeTypeDef",
    {
        "AlternateNameEncoding": str,
        "AlternateValueEncoding": str,
    },
    total=False,
)

class AttributeTypeDef(_RequiredAttributeTypeDef, _OptionalAttributeTypeDef):
    pass

CreateDomainRequestRequestTypeDef = TypedDict(
    "CreateDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

UpdateConditionTypeDef = TypedDict(
    "UpdateConditionTypeDef",
    {
        "Name": str,
        "Value": str,
        "Exists": bool,
    },
    total=False,
)

DeleteDomainRequestRequestTypeDef = TypedDict(
    "DeleteDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DomainMetadataRequestRequestTypeDef = TypedDict(
    "DomainMetadataRequestRequestTypeDef",
    {
        "DomainName": str,
    },
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

_RequiredGetAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAttributesRequestRequestTypeDef",
    {
        "DomainName": str,
        "ItemName": str,
    },
)
_OptionalGetAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAttributesRequestRequestTypeDef",
    {
        "AttributeNames": Sequence[str],
        "ConsistentRead": bool,
    },
    total=False,
)

class GetAttributesRequestRequestTypeDef(
    _RequiredGetAttributesRequestRequestTypeDef, _OptionalGetAttributesRequestRequestTypeDef
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "MaxNumberOfDomains": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredReplaceableAttributeTypeDef = TypedDict(
    "_RequiredReplaceableAttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalReplaceableAttributeTypeDef = TypedDict(
    "_OptionalReplaceableAttributeTypeDef",
    {
        "Replace": bool,
    },
    total=False,
)

class ReplaceableAttributeTypeDef(
    _RequiredReplaceableAttributeTypeDef, _OptionalReplaceableAttributeTypeDef
):
    pass

_RequiredSelectRequestRequestTypeDef = TypedDict(
    "_RequiredSelectRequestRequestTypeDef",
    {
        "SelectExpression": str,
    },
)
_OptionalSelectRequestRequestTypeDef = TypedDict(
    "_OptionalSelectRequestRequestTypeDef",
    {
        "NextToken": str,
        "ConsistentRead": bool,
    },
    total=False,
)

class SelectRequestRequestTypeDef(
    _RequiredSelectRequestRequestTypeDef, _OptionalSelectRequestRequestTypeDef
):
    pass

_RequiredDeletableItemTypeDef = TypedDict(
    "_RequiredDeletableItemTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeletableItemTypeDef = TypedDict(
    "_OptionalDeletableItemTypeDef",
    {
        "Attributes": Sequence[AttributeTypeDef],
    },
    total=False,
)

class DeletableItemTypeDef(_RequiredDeletableItemTypeDef, _OptionalDeletableItemTypeDef):
    pass

_RequiredItemTypeDef = TypedDict(
    "_RequiredItemTypeDef",
    {
        "Name": str,
        "Attributes": List[AttributeTypeDef],
    },
)
_OptionalItemTypeDef = TypedDict(
    "_OptionalItemTypeDef",
    {
        "AlternateNameEncoding": str,
    },
    total=False,
)

class ItemTypeDef(_RequiredItemTypeDef, _OptionalItemTypeDef):
    pass

_RequiredDeleteAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAttributesRequestRequestTypeDef",
    {
        "DomainName": str,
        "ItemName": str,
    },
)
_OptionalDeleteAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAttributesRequestRequestTypeDef",
    {
        "Attributes": Sequence[AttributeTypeDef],
        "Expected": UpdateConditionTypeDef,
    },
    total=False,
)

class DeleteAttributesRequestRequestTypeDef(
    _RequiredDeleteAttributesRequestRequestTypeDef, _OptionalDeleteAttributesRequestRequestTypeDef
):
    pass

DomainMetadataResultTypeDef = TypedDict(
    "DomainMetadataResultTypeDef",
    {
        "ItemCount": int,
        "ItemNamesSizeBytes": int,
        "AttributeNameCount": int,
        "AttributeNamesSizeBytes": int,
        "AttributeValueCount": int,
        "AttributeValuesSizeBytes": int,
        "Timestamp": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAttributesResultTypeDef = TypedDict(
    "GetAttributesResultTypeDef",
    {
        "Attributes": List[AttributeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsResultTypeDef = TypedDict(
    "ListDomainsResultTypeDef",
    {
        "DomainNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsRequestListDomainsPaginateTypeDef = TypedDict(
    "ListDomainsRequestListDomainsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredSelectRequestSelectPaginateTypeDef = TypedDict(
    "_RequiredSelectRequestSelectPaginateTypeDef",
    {
        "SelectExpression": str,
    },
)
_OptionalSelectRequestSelectPaginateTypeDef = TypedDict(
    "_OptionalSelectRequestSelectPaginateTypeDef",
    {
        "ConsistentRead": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SelectRequestSelectPaginateTypeDef(
    _RequiredSelectRequestSelectPaginateTypeDef, _OptionalSelectRequestSelectPaginateTypeDef
):
    pass

_RequiredPutAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredPutAttributesRequestRequestTypeDef",
    {
        "DomainName": str,
        "ItemName": str,
        "Attributes": Sequence[ReplaceableAttributeTypeDef],
    },
)
_OptionalPutAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalPutAttributesRequestRequestTypeDef",
    {
        "Expected": UpdateConditionTypeDef,
    },
    total=False,
)

class PutAttributesRequestRequestTypeDef(
    _RequiredPutAttributesRequestRequestTypeDef, _OptionalPutAttributesRequestRequestTypeDef
):
    pass

ReplaceableItemTypeDef = TypedDict(
    "ReplaceableItemTypeDef",
    {
        "Name": str,
        "Attributes": Sequence[ReplaceableAttributeTypeDef],
    },
)

BatchDeleteAttributesRequestRequestTypeDef = TypedDict(
    "BatchDeleteAttributesRequestRequestTypeDef",
    {
        "DomainName": str,
        "Items": Sequence[DeletableItemTypeDef],
    },
)

SelectResultTypeDef = TypedDict(
    "SelectResultTypeDef",
    {
        "Items": List[ItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutAttributesRequestRequestTypeDef = TypedDict(
    "BatchPutAttributesRequestRequestTypeDef",
    {
        "DomainName": str,
        "Items": Sequence[ReplaceableItemTypeDef],
    },
)
