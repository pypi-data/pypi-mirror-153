"""
Type annotations for honeycode service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_honeycode.client import HoneycodeClient

    session = Session()
    client: HoneycodeClient = session.client("honeycode")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListTableColumnsPaginator,
    ListTableRowsPaginator,
    ListTablesPaginator,
    QueryTableRowsPaginator,
)
from .type_defs import (
    BatchCreateTableRowsResultTypeDef,
    BatchDeleteTableRowsResultTypeDef,
    BatchUpdateTableRowsResultTypeDef,
    BatchUpsertTableRowsResultTypeDef,
    CreateRowDataTypeDef,
    DescribeTableDataImportJobResultTypeDef,
    FilterTypeDef,
    GetScreenDataResultTypeDef,
    ImportDataSourceTypeDef,
    ImportOptionsTypeDef,
    InvokeScreenAutomationResultTypeDef,
    ListTableColumnsResultTypeDef,
    ListTableRowsResultTypeDef,
    ListTablesResultTypeDef,
    ListTagsForResourceResultTypeDef,
    QueryTableRowsResultTypeDef,
    StartTableDataImportJobResultTypeDef,
    UpdateRowDataTypeDef,
    UpsertRowDataTypeDef,
    VariableValueTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("HoneycodeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AutomationExecutionException: Type[BotocoreClientError]
    AutomationExecutionTimeoutException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class HoneycodeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HoneycodeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#exceptions)
        """

    def batch_create_table_rows(
        self,
        *,
        workbookId: str,
        tableId: str,
        rowsToCreate: Sequence[CreateRowDataTypeDef],
        clientRequestToken: str = ...
    ) -> BatchCreateTableRowsResultTypeDef:
        """
        The BatchCreateTableRows API allows you to create one or more rows at the end of
        a table in a workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.batch_create_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#batch_create_table_rows)
        """

    def batch_delete_table_rows(
        self, *, workbookId: str, tableId: str, rowIds: Sequence[str], clientRequestToken: str = ...
    ) -> BatchDeleteTableRowsResultTypeDef:
        """
        The BatchDeleteTableRows API allows you to delete one or more rows from a table
        in a workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.batch_delete_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#batch_delete_table_rows)
        """

    def batch_update_table_rows(
        self,
        *,
        workbookId: str,
        tableId: str,
        rowsToUpdate: Sequence[UpdateRowDataTypeDef],
        clientRequestToken: str = ...
    ) -> BatchUpdateTableRowsResultTypeDef:
        """
        The BatchUpdateTableRows API allows you to update one or more rows in a table in
        a workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.batch_update_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#batch_update_table_rows)
        """

    def batch_upsert_table_rows(
        self,
        *,
        workbookId: str,
        tableId: str,
        rowsToUpsert: Sequence[UpsertRowDataTypeDef],
        clientRequestToken: str = ...
    ) -> BatchUpsertTableRowsResultTypeDef:
        """
        The BatchUpsertTableRows API allows you to upsert one or more rows in a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.batch_upsert_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#batch_upsert_table_rows)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#can_paginate)
        """

    def describe_table_data_import_job(
        self, *, workbookId: str, tableId: str, jobId: str
    ) -> DescribeTableDataImportJobResultTypeDef:
        """
        The DescribeTableDataImportJob API allows you to retrieve the status and details
        of a table data import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.describe_table_data_import_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#describe_table_data_import_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#generate_presigned_url)
        """

    def get_screen_data(
        self,
        *,
        workbookId: str,
        appId: str,
        screenId: str,
        variables: Mapping[str, VariableValueTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> GetScreenDataResultTypeDef:
        """
        The GetScreenData API allows retrieval of data from a screen in a Honeycode app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.get_screen_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#get_screen_data)
        """

    def invoke_screen_automation(
        self,
        *,
        workbookId: str,
        appId: str,
        screenId: str,
        screenAutomationId: str,
        variables: Mapping[str, VariableValueTypeDef] = ...,
        rowId: str = ...,
        clientRequestToken: str = ...
    ) -> InvokeScreenAutomationResultTypeDef:
        """
        The InvokeScreenAutomation API allows invoking an action defined in a screen in
        a Honeycode app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.invoke_screen_automation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#invoke_screen_automation)
        """

    def list_table_columns(
        self, *, workbookId: str, tableId: str, nextToken: str = ...
    ) -> ListTableColumnsResultTypeDef:
        """
        The ListTableColumns API allows you to retrieve a list of all the columns in a
        table in a workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.list_table_columns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#list_table_columns)
        """

    def list_table_rows(
        self,
        *,
        workbookId: str,
        tableId: str,
        rowIds: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListTableRowsResultTypeDef:
        """
        The ListTableRows API allows you to retrieve a list of all the rows in a table
        in a workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.list_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#list_table_rows)
        """

    def list_tables(
        self, *, workbookId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTablesResultTypeDef:
        """
        The ListTables API allows you to retrieve a list of all the tables in a
        workbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.list_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#list_tables)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResultTypeDef:
        """
        The ListTagsForResource API allows you to return a resource's tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#list_tags_for_resource)
        """

    def query_table_rows(
        self,
        *,
        workbookId: str,
        tableId: str,
        filterFormula: FilterTypeDef,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> QueryTableRowsResultTypeDef:
        """
        The QueryTableRows API allows you to use a filter formula to query for specific
        rows in a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.query_table_rows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#query_table_rows)
        """

    def start_table_data_import_job(
        self,
        *,
        workbookId: str,
        dataSource: ImportDataSourceTypeDef,
        dataFormat: Literal["DELIMITED_TEXT"],
        destinationTableId: str,
        importOptions: ImportOptionsTypeDef,
        clientRequestToken: str
    ) -> StartTableDataImportJobResultTypeDef:
        """
        The StartTableDataImportJob API allows you to start an import job on a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.start_table_data_import_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#start_table_data_import_job)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        The TagResource API allows you to add tags to an ARN-able resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        The UntagResource API allows you to removes tags from an ARN-able resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_table_columns"]
    ) -> ListTableColumnsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_table_rows"]) -> ListTableRowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_table_rows"]) -> QueryTableRowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/honeycode.html#Honeycode.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_honeycode/client/#get_paginator)
        """
