"""
Type annotations for athena service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_athena.client import AthenaClient

    session = Session()
    client: AthenaClient = session.client("athena")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import DataCatalogTypeType, WorkGroupStateType
from .paginator import (
    GetQueryResultsPaginator,
    ListDatabasesPaginator,
    ListDataCatalogsPaginator,
    ListNamedQueriesPaginator,
    ListQueryExecutionsPaginator,
    ListTableMetadataPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    BatchGetNamedQueryOutputTypeDef,
    BatchGetQueryExecutionOutputTypeDef,
    CreateNamedQueryOutputTypeDef,
    GetDatabaseOutputTypeDef,
    GetDataCatalogOutputTypeDef,
    GetNamedQueryOutputTypeDef,
    GetPreparedStatementOutputTypeDef,
    GetQueryExecutionOutputTypeDef,
    GetQueryResultsOutputTypeDef,
    GetTableMetadataOutputTypeDef,
    GetWorkGroupOutputTypeDef,
    ListDatabasesOutputTypeDef,
    ListDataCatalogsOutputTypeDef,
    ListEngineVersionsOutputTypeDef,
    ListNamedQueriesOutputTypeDef,
    ListPreparedStatementsOutputTypeDef,
    ListQueryExecutionsOutputTypeDef,
    ListTableMetadataOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkGroupsOutputTypeDef,
    QueryExecutionContextTypeDef,
    ResultConfigurationTypeDef,
    StartQueryExecutionOutputTypeDef,
    TagTypeDef,
    WorkGroupConfigurationTypeDef,
    WorkGroupConfigurationUpdatesTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AthenaClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    MetadataException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class AthenaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AthenaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#exceptions)
        """

    def batch_get_named_query(
        self, *, NamedQueryIds: Sequence[str]
    ) -> BatchGetNamedQueryOutputTypeDef:
        """
        Returns the details of a single named query or a list of up to 50 queries, which
        you provide as an array of query ID strings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.batch_get_named_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#batch_get_named_query)
        """

    def batch_get_query_execution(
        self, *, QueryExecutionIds: Sequence[str]
    ) -> BatchGetQueryExecutionOutputTypeDef:
        """
        Returns the details of a single query execution or a list of up to 50 query
        executions, which you provide as an array of query execution ID strings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.batch_get_query_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#batch_get_query_execution)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#can_paginate)
        """

    def create_data_catalog(
        self,
        *,
        Name: str,
        Type: DataCatalogTypeType,
        Description: str = ...,
        Parameters: Mapping[str, str] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates (registers) a data catalog with the specified name and properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.create_data_catalog)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#create_data_catalog)
        """

    def create_named_query(
        self,
        *,
        Name: str,
        Database: str,
        QueryString: str,
        Description: str = ...,
        ClientRequestToken: str = ...,
        WorkGroup: str = ...
    ) -> CreateNamedQueryOutputTypeDef:
        """
        Creates a named query in the specified workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.create_named_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#create_named_query)
        """

    def create_prepared_statement(
        self, *, StatementName: str, WorkGroup: str, QueryStatement: str, Description: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a prepared statement for use with SQL queries in Athena.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.create_prepared_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#create_prepared_statement)
        """

    def create_work_group(
        self,
        *,
        Name: str,
        Configuration: WorkGroupConfigurationTypeDef = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates a workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.create_work_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#create_work_group)
        """

    def delete_data_catalog(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.delete_data_catalog)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#delete_data_catalog)
        """

    def delete_named_query(self, *, NamedQueryId: str) -> Dict[str, Any]:
        """
        Deletes the named query if you have access to the workgroup in which the query
        was saved.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.delete_named_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#delete_named_query)
        """

    def delete_prepared_statement(self, *, StatementName: str, WorkGroup: str) -> Dict[str, Any]:
        """
        Deletes the prepared statement with the specified name from the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.delete_prepared_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#delete_prepared_statement)
        """

    def delete_work_group(
        self, *, WorkGroup: str, RecursiveDeleteOption: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.delete_work_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#delete_work_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#generate_presigned_url)
        """

    def get_data_catalog(self, *, Name: str) -> GetDataCatalogOutputTypeDef:
        """
        Returns the specified data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_data_catalog)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_data_catalog)
        """

    def get_database(self, *, CatalogName: str, DatabaseName: str) -> GetDatabaseOutputTypeDef:
        """
        Returns a database object for the specified database and data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_database)
        """

    def get_named_query(self, *, NamedQueryId: str) -> GetNamedQueryOutputTypeDef:
        """
        Returns information about a single query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_named_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_named_query)
        """

    def get_prepared_statement(
        self, *, StatementName: str, WorkGroup: str
    ) -> GetPreparedStatementOutputTypeDef:
        """
        Retrieves the prepared statement with the specified name from the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_prepared_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_prepared_statement)
        """

    def get_query_execution(self, *, QueryExecutionId: str) -> GetQueryExecutionOutputTypeDef:
        """
        Returns information about a single execution of a query if you have access to
        the workgroup in which the query ran.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_query_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_query_execution)
        """

    def get_query_results(
        self, *, QueryExecutionId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetQueryResultsOutputTypeDef:
        """
        Streams the results of a single query execution specified by `QueryExecutionId`
        from the Athena query results location in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_query_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_query_results)
        """

    def get_table_metadata(
        self, *, CatalogName: str, DatabaseName: str, TableName: str
    ) -> GetTableMetadataOutputTypeDef:
        """
        Returns table metadata for the specified catalog, database, and table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_table_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_table_metadata)
        """

    def get_work_group(self, *, WorkGroup: str) -> GetWorkGroupOutputTypeDef:
        """
        Returns information about the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_work_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_work_group)
        """

    def list_data_catalogs(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDataCatalogsOutputTypeDef:
        """
        Lists the data catalogs in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_data_catalogs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_data_catalogs)
        """

    def list_databases(
        self, *, CatalogName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDatabasesOutputTypeDef:
        """
        Lists the databases in the specified data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_databases)
        """

    def list_engine_versions(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEngineVersionsOutputTypeDef:
        """
        Returns a list of engine versions that are available to choose from, including
        the Auto option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_engine_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_engine_versions)
        """

    def list_named_queries(
        self, *, NextToken: str = ..., MaxResults: int = ..., WorkGroup: str = ...
    ) -> ListNamedQueriesOutputTypeDef:
        """
        Provides a list of available query IDs only for queries saved in the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_named_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_named_queries)
        """

    def list_prepared_statements(
        self, *, WorkGroup: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPreparedStatementsOutputTypeDef:
        """
        Lists the prepared statements in the specfied workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_prepared_statements)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_prepared_statements)
        """

    def list_query_executions(
        self, *, NextToken: str = ..., MaxResults: int = ..., WorkGroup: str = ...
    ) -> ListQueryExecutionsOutputTypeDef:
        """
        Provides a list of available query execution IDs for the queries in the
        specified workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_query_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_query_executions)
        """

    def list_table_metadata(
        self,
        *,
        CatalogName: str,
        DatabaseName: str,
        Expression: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListTableMetadataOutputTypeDef:
        """
        Lists the metadata for the tables in the specified data catalog database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_table_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_table_metadata)
        """

    def list_tags_for_resource(
        self, *, ResourceARN: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with an Athena workgroup or data catalog resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_tags_for_resource)
        """

    def list_work_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkGroupsOutputTypeDef:
        """
        Lists available workgroups for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.list_work_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#list_work_groups)
        """

    def start_query_execution(
        self,
        *,
        QueryString: str,
        ClientRequestToken: str = ...,
        QueryExecutionContext: QueryExecutionContextTypeDef = ...,
        ResultConfiguration: ResultConfigurationTypeDef = ...,
        WorkGroup: str = ...
    ) -> StartQueryExecutionOutputTypeDef:
        """
        Runs the SQL query statements contained in the `Query`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.start_query_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#start_query_execution)
        """

    def stop_query_execution(self, *, QueryExecutionId: str) -> Dict[str, Any]:
        """
        Stops a query execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.stop_query_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#stop_query_execution)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to an Athena resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a data catalog or workgroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#untag_resource)
        """

    def update_data_catalog(
        self,
        *,
        Name: str,
        Type: DataCatalogTypeType,
        Description: str = ...,
        Parameters: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Updates the data catalog that has the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.update_data_catalog)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#update_data_catalog)
        """

    def update_named_query(
        self, *, NamedQueryId: str, Name: str, QueryString: str, Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a  NamedQuery object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.update_named_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#update_named_query)
        """

    def update_prepared_statement(
        self, *, StatementName: str, WorkGroup: str, QueryStatement: str, Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a prepared statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.update_prepared_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#update_prepared_statement)
        """

    def update_work_group(
        self,
        *,
        WorkGroup: str,
        Description: str = ...,
        ConfigurationUpdates: WorkGroupConfigurationUpdatesTypeDef = ...,
        State: WorkGroupStateType = ...
    ) -> Dict[str, Any]:
        """
        Updates the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.update_work_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#update_work_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_query_results"]
    ) -> GetQueryResultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_catalogs"]
    ) -> ListDataCatalogsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_databases"]) -> ListDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_named_queries"]
    ) -> ListNamedQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_query_executions"]
    ) -> ListQueryExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_table_metadata"]
    ) -> ListTableMetadataPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/client/#get_paginator)
        """
