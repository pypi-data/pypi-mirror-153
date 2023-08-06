"""
Main interface for honeycode service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_honeycode import (
        Client,
        HoneycodeClient,
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
from .client import HoneycodeClient
from .paginator import (
    ListTableColumnsPaginator,
    ListTableRowsPaginator,
    ListTablesPaginator,
    QueryTableRowsPaginator,
)

Client = HoneycodeClient


__all__ = (
    "Client",
    "HoneycodeClient",
    "ListTableColumnsPaginator",
    "ListTableRowsPaginator",
    "ListTablesPaginator",
    "QueryTableRowsPaginator",
)
