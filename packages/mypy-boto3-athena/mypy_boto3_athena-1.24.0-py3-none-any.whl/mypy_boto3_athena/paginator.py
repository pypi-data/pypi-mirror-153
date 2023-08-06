"""
Type annotations for athena service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_athena.client import AthenaClient
    from mypy_boto3_athena.paginator import (
        GetQueryResultsPaginator,
        ListDataCatalogsPaginator,
        ListDatabasesPaginator,
        ListNamedQueriesPaginator,
        ListQueryExecutionsPaginator,
        ListTableMetadataPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: AthenaClient = session.client("athena")

    get_query_results_paginator: GetQueryResultsPaginator = client.get_paginator("get_query_results")
    list_data_catalogs_paginator: ListDataCatalogsPaginator = client.get_paginator("list_data_catalogs")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_named_queries_paginator: ListNamedQueriesPaginator = client.get_paginator("list_named_queries")
    list_query_executions_paginator: ListQueryExecutionsPaginator = client.get_paginator("list_query_executions")
    list_table_metadata_paginator: ListTableMetadataPaginator = client.get_paginator("list_table_metadata")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GetQueryResultsOutputTypeDef,
    ListDatabasesOutputTypeDef,
    ListDataCatalogsOutputTypeDef,
    ListNamedQueriesOutputTypeDef,
    ListQueryExecutionsOutputTypeDef,
    ListTableMetadataOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetQueryResultsPaginator",
    "ListDataCatalogsPaginator",
    "ListDatabasesPaginator",
    "ListNamedQueriesPaginator",
    "ListQueryExecutionsPaginator",
    "ListTableMetadataPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetQueryResultsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.GetQueryResults)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#getqueryresultspaginator)
    """

    def paginate(
        self, *, QueryExecutionId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetQueryResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.GetQueryResults.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#getqueryresultspaginator)
        """


class ListDataCatalogsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListDataCatalogs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatacatalogspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataCatalogsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListDataCatalogs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatacatalogspaginator)
        """


class ListDatabasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListDatabases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatabasespaginator)
    """

    def paginate(
        self, *, CatalogName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListDatabases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listdatabasespaginator)
        """


class ListNamedQueriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListNamedQueries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listnamedqueriespaginator)
    """

    def paginate(
        self, *, WorkGroup: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNamedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListNamedQueries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listnamedqueriespaginator)
        """


class ListQueryExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListQueryExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listqueryexecutionspaginator)
    """

    def paginate(
        self, *, WorkGroup: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQueryExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListQueryExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listqueryexecutionspaginator)
        """


class ListTableMetadataPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListTableMetadata)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtablemetadatapaginator)
    """

    def paginate(
        self,
        *,
        CatalogName: str,
        DatabaseName: str,
        Expression: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTableMetadataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListTableMetadata.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtablemetadatapaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceARN: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/paginators/#listtagsforresourcepaginator)
        """
