"""
Type annotations for dynamodb service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dynamodb.client import DynamoDBClient
    from mypy_boto3_dynamodb.paginator import (
        ListBackupsPaginator,
        ListTablesPaginator,
        ListTagsOfResourcePaginator,
        QueryPaginator,
        ScanPaginator,
    )

    session = Session()
    client: DynamoDBClient = session.client("dynamodb")

    list_backups_paginator: ListBackupsPaginator = client.get_paginator("list_backups")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    list_tags_of_resource_paginator: ListTagsOfResourcePaginator = client.get_paginator("list_tags_of_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    scan_paginator: ScanPaginator = client.get_paginator("scan")
    ```
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, Iterator, Mapping, Sequence, Set, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    BackupTypeFilterType,
    ConditionalOperatorType,
    ReturnConsumedCapacityType,
    SelectType,
)
from .type_defs import (
    ConditionTableTypeDef,
    ListBackupsOutputTableTypeDef,
    ListTablesOutputTableTypeDef,
    ListTagsOfResourceOutputTableTypeDef,
    PaginatorConfigTypeDef,
    QueryOutputTableTypeDef,
    ScanOutputTableTypeDef,
)

__all__ = (
    "ListBackupsPaginator",
    "ListTablesPaginator",
    "ListTagsOfResourcePaginator",
    "QueryPaginator",
    "ScanPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBackupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListBackups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listbackupspaginator)
    """

    def paginate(
        self,
        *,
        TableName: str = ...,
        TimeRangeLowerBound: Union[datetime, str] = ...,
        TimeRangeUpperBound: Union[datetime, str] = ...,
        BackupType: BackupTypeFilterType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackupsOutputTableTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListBackups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listbackupspaginator)
        """

class ListTablesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTables)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listtablespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTablesOutputTableTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTables.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listtablespaginator)
        """

class ListTagsOfResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTagsOfResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listtagsofresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsOfResourceOutputTableTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.ListTagsOfResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#listtagsofresourcepaginator)
        """

class QueryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Query)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#querypaginator)
    """

    def paginate(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        Select: SelectType = ...,
        AttributesToGet: Sequence[str] = ...,
        ConsistentRead: bool = ...,
        KeyConditions: Mapping[str, ConditionTableTypeDef] = ...,
        QueryFilter: Mapping[str, ConditionTableTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ScanIndexForward: bool = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        KeyConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                Sequence[Any],
                Mapping[str, Any],
                None,
            ],
        ] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryOutputTableTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Query.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#querypaginator)
        """

class ScanPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Scan)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#scanpaginator)
    """

    def paginate(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        AttributesToGet: Sequence[str] = ...,
        Select: SelectType = ...,
        ScanFilter: Mapping[str, ConditionTableTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        TotalSegments: int = ...,
        Segment: int = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                Sequence[Any],
                Mapping[str, Any],
                None,
            ],
        ] = ...,
        ConsistentRead: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ScanOutputTableTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Scan.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/paginators/#scanpaginator)
        """
