"""
Type annotations for honeycode service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_honeycode.client import HoneycodeClient
    from mypy_boto3_honeycode.paginator import (
        ListTableColumnsPaginator,
        ListTableRowsPaginator,
        ListTablesPaginator,
        QueryTableRowsPaginator,
    )

    session = Session()
    client: HoneycodeClient = session.client("honeycode")

    list_table_columns_paginator: ListTableColumnsPaginator = client.get_paginator("list_table_columns")
    list_table_rows_paginator: ListTableRowsPaginator = client.get_paginator("list_table_rows")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    query_table_rows_paginator: QueryTableRowsPaginator = client.get_paginator("query_table_rows")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    FilterTypeDef,
    ListTableColumnsResultTypeDef,
    ListTableRowsResultTypeDef,
    ListTablesResultTypeDef,
    PaginatorConfigTypeDef,
    QueryTableRowsResultTypeDef,
)

__all__ = (
    "ListTableColumnsPaginator",
    "ListTableRowsPaginator",
    "ListTablesPaginator",
    "QueryTableRowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListTableColumnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTableColumns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablecolumnspaginator)
    """

    def paginate(
        self, *, workbookId: str, tableId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTableColumnsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTableColumns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablecolumnspaginator)
        """


class ListTableRowsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTableRows)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablerowspaginator)
    """

    def paginate(
        self,
        *,
        workbookId: str,
        tableId: str,
        rowIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTableRowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTableRows.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablerowspaginator)
        """


class ListTablesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTables)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablespaginator)
    """

    def paginate(
        self, *, workbookId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTablesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.ListTables.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#listtablespaginator)
        """


class QueryTableRowsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.QueryTableRows)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#querytablerowspaginator)
    """

    def paginate(
        self,
        *,
        workbookId: str,
        tableId: str,
        filterFormula: FilterTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[QueryTableRowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Paginator.QueryTableRows.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/paginators/#querytablerowspaginator)
        """
