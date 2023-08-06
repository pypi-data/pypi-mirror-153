"""
Type annotations for marketplace-catalog service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplace_catalog.type_defs import CancelChangeSetRequestRequestTypeDef

    data: CancelChangeSetRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import ChangeStatusType, FailureCodeType, SortOrderType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CancelChangeSetRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ChangeSetSummaryListItemTypeDef",
    "EntityTypeDef",
    "ErrorDetailTypeDef",
    "DescribeChangeSetRequestRequestTypeDef",
    "DescribeEntityRequestRequestTypeDef",
    "EntitySummaryTypeDef",
    "FilterTypeDef",
    "SortTypeDef",
    "CancelChangeSetResponseTypeDef",
    "DescribeEntityResponseTypeDef",
    "StartChangeSetResponseTypeDef",
    "ListChangeSetsResponseTypeDef",
    "ChangeTypeDef",
    "ChangeSummaryTypeDef",
    "ListEntitiesResponseTypeDef",
    "ListChangeSetsRequestRequestTypeDef",
    "ListEntitiesRequestRequestTypeDef",
    "StartChangeSetRequestRequestTypeDef",
    "DescribeChangeSetResponseTypeDef",
)

CancelChangeSetRequestRequestTypeDef = TypedDict(
    "CancelChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSetId": str,
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

ChangeSetSummaryListItemTypeDef = TypedDict(
    "ChangeSetSummaryListItemTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ChangeSetName": str,
        "StartTime": str,
        "EndTime": str,
        "Status": ChangeStatusType,
        "EntityIdList": List[str],
        "FailureCode": FailureCodeType,
    },
    total=False,
)

_RequiredEntityTypeDef = TypedDict(
    "_RequiredEntityTypeDef",
    {
        "Type": str,
    },
)
_OptionalEntityTypeDef = TypedDict(
    "_OptionalEntityTypeDef",
    {
        "Identifier": str,
    },
    total=False,
)

class EntityTypeDef(_RequiredEntityTypeDef, _OptionalEntityTypeDef):
    pass

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

DescribeChangeSetRequestRequestTypeDef = TypedDict(
    "DescribeChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSetId": str,
    },
)

DescribeEntityRequestRequestTypeDef = TypedDict(
    "DescribeEntityRequestRequestTypeDef",
    {
        "Catalog": str,
        "EntityId": str,
    },
)

EntitySummaryTypeDef = TypedDict(
    "EntitySummaryTypeDef",
    {
        "Name": str,
        "EntityType": str,
        "EntityId": str,
        "EntityArn": str,
        "LastModifiedDate": str,
        "Visibility": str,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "ValueList": Sequence[str],
    },
    total=False,
)

SortTypeDef = TypedDict(
    "SortTypeDef",
    {
        "SortBy": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

CancelChangeSetResponseTypeDef = TypedDict(
    "CancelChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEntityResponseTypeDef = TypedDict(
    "DescribeEntityResponseTypeDef",
    {
        "EntityType": str,
        "EntityIdentifier": str,
        "EntityArn": str,
        "LastModifiedDate": str,
        "Details": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartChangeSetResponseTypeDef = TypedDict(
    "StartChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChangeSetsResponseTypeDef = TypedDict(
    "ListChangeSetsResponseTypeDef",
    {
        "ChangeSetSummaryList": List[ChangeSetSummaryListItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredChangeTypeDef = TypedDict(
    "_RequiredChangeTypeDef",
    {
        "ChangeType": str,
        "Entity": EntityTypeDef,
        "Details": str,
    },
)
_OptionalChangeTypeDef = TypedDict(
    "_OptionalChangeTypeDef",
    {
        "ChangeName": str,
    },
    total=False,
)

class ChangeTypeDef(_RequiredChangeTypeDef, _OptionalChangeTypeDef):
    pass

ChangeSummaryTypeDef = TypedDict(
    "ChangeSummaryTypeDef",
    {
        "ChangeType": str,
        "Entity": EntityTypeDef,
        "Details": str,
        "ErrorDetailList": List[ErrorDetailTypeDef],
        "ChangeName": str,
    },
    total=False,
)

ListEntitiesResponseTypeDef = TypedDict(
    "ListEntitiesResponseTypeDef",
    {
        "EntitySummaryList": List[EntitySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListChangeSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListChangeSetsRequestRequestTypeDef",
    {
        "Catalog": str,
    },
)
_OptionalListChangeSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListChangeSetsRequestRequestTypeDef",
    {
        "FilterList": Sequence[FilterTypeDef],
        "Sort": SortTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListChangeSetsRequestRequestTypeDef(
    _RequiredListChangeSetsRequestRequestTypeDef, _OptionalListChangeSetsRequestRequestTypeDef
):
    pass

_RequiredListEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredListEntitiesRequestRequestTypeDef",
    {
        "Catalog": str,
        "EntityType": str,
    },
)
_OptionalListEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalListEntitiesRequestRequestTypeDef",
    {
        "FilterList": Sequence[FilterTypeDef],
        "Sort": SortTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListEntitiesRequestRequestTypeDef(
    _RequiredListEntitiesRequestRequestTypeDef, _OptionalListEntitiesRequestRequestTypeDef
):
    pass

_RequiredStartChangeSetRequestRequestTypeDef = TypedDict(
    "_RequiredStartChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSet": Sequence[ChangeTypeDef],
    },
)
_OptionalStartChangeSetRequestRequestTypeDef = TypedDict(
    "_OptionalStartChangeSetRequestRequestTypeDef",
    {
        "ChangeSetName": str,
        "ClientRequestToken": str,
    },
    total=False,
)

class StartChangeSetRequestRequestTypeDef(
    _RequiredStartChangeSetRequestRequestTypeDef, _OptionalStartChangeSetRequestRequestTypeDef
):
    pass

DescribeChangeSetResponseTypeDef = TypedDict(
    "DescribeChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ChangeSetName": str,
        "StartTime": str,
        "EndTime": str,
        "Status": ChangeStatusType,
        "FailureCode": FailureCodeType,
        "FailureDescription": str,
        "ChangeSet": List[ChangeSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
