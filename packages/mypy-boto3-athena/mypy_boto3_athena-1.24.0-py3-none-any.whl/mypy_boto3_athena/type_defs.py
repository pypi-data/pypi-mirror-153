"""
Type annotations for athena service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_athena/type_defs/)

Usage::

    ```python
    from mypy_boto3_athena.type_defs import AclConfigurationTypeDef

    data: AclConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ColumnNullableType,
    DataCatalogTypeType,
    EncryptionOptionType,
    QueryExecutionStateType,
    StatementTypeType,
    WorkGroupStateType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AclConfigurationTypeDef",
    "AthenaErrorTypeDef",
    "BatchGetNamedQueryInputRequestTypeDef",
    "NamedQueryTypeDef",
    "ResponseMetadataTypeDef",
    "UnprocessedNamedQueryIdTypeDef",
    "BatchGetQueryExecutionInputRequestTypeDef",
    "UnprocessedQueryExecutionIdTypeDef",
    "ColumnInfoTypeDef",
    "ColumnTypeDef",
    "TagTypeDef",
    "CreateNamedQueryInputRequestTypeDef",
    "CreatePreparedStatementInputRequestTypeDef",
    "DataCatalogSummaryTypeDef",
    "DataCatalogTypeDef",
    "DatabaseTypeDef",
    "DatumTypeDef",
    "DeleteDataCatalogInputRequestTypeDef",
    "DeleteNamedQueryInputRequestTypeDef",
    "DeletePreparedStatementInputRequestTypeDef",
    "DeleteWorkGroupInputRequestTypeDef",
    "EncryptionConfigurationTypeDef",
    "EngineVersionTypeDef",
    "GetDataCatalogInputRequestTypeDef",
    "GetDatabaseInputRequestTypeDef",
    "GetNamedQueryInputRequestTypeDef",
    "GetPreparedStatementInputRequestTypeDef",
    "PreparedStatementTypeDef",
    "GetQueryExecutionInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetQueryResultsInputRequestTypeDef",
    "GetTableMetadataInputRequestTypeDef",
    "GetWorkGroupInputRequestTypeDef",
    "ListDataCatalogsInputRequestTypeDef",
    "ListDatabasesInputRequestTypeDef",
    "ListEngineVersionsInputRequestTypeDef",
    "ListNamedQueriesInputRequestTypeDef",
    "ListPreparedStatementsInputRequestTypeDef",
    "PreparedStatementSummaryTypeDef",
    "ListQueryExecutionsInputRequestTypeDef",
    "ListTableMetadataInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListWorkGroupsInputRequestTypeDef",
    "QueryExecutionContextTypeDef",
    "QueryExecutionStatisticsTypeDef",
    "StopQueryExecutionInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateDataCatalogInputRequestTypeDef",
    "UpdateNamedQueryInputRequestTypeDef",
    "UpdatePreparedStatementInputRequestTypeDef",
    "QueryExecutionStatusTypeDef",
    "CreateNamedQueryOutputTypeDef",
    "GetNamedQueryOutputTypeDef",
    "ListNamedQueriesOutputTypeDef",
    "ListQueryExecutionsOutputTypeDef",
    "StartQueryExecutionOutputTypeDef",
    "BatchGetNamedQueryOutputTypeDef",
    "ResultSetMetadataTypeDef",
    "TableMetadataTypeDef",
    "CreateDataCatalogInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "ListDataCatalogsOutputTypeDef",
    "GetDataCatalogOutputTypeDef",
    "GetDatabaseOutputTypeDef",
    "ListDatabasesOutputTypeDef",
    "RowTypeDef",
    "ResultConfigurationTypeDef",
    "ResultConfigurationUpdatesTypeDef",
    "ListEngineVersionsOutputTypeDef",
    "WorkGroupSummaryTypeDef",
    "GetPreparedStatementOutputTypeDef",
    "GetQueryResultsInputGetQueryResultsPaginateTypeDef",
    "ListDataCatalogsInputListDataCatalogsPaginateTypeDef",
    "ListDatabasesInputListDatabasesPaginateTypeDef",
    "ListNamedQueriesInputListNamedQueriesPaginateTypeDef",
    "ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef",
    "ListTableMetadataInputListTableMetadataPaginateTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListPreparedStatementsOutputTypeDef",
    "GetTableMetadataOutputTypeDef",
    "ListTableMetadataOutputTypeDef",
    "ResultSetTypeDef",
    "QueryExecutionTypeDef",
    "StartQueryExecutionInputRequestTypeDef",
    "WorkGroupConfigurationTypeDef",
    "WorkGroupConfigurationUpdatesTypeDef",
    "ListWorkGroupsOutputTypeDef",
    "GetQueryResultsOutputTypeDef",
    "BatchGetQueryExecutionOutputTypeDef",
    "GetQueryExecutionOutputTypeDef",
    "CreateWorkGroupInputRequestTypeDef",
    "WorkGroupTypeDef",
    "UpdateWorkGroupInputRequestTypeDef",
    "GetWorkGroupOutputTypeDef",
)

AclConfigurationTypeDef = TypedDict(
    "AclConfigurationTypeDef",
    {
        "S3AclOption": Literal["BUCKET_OWNER_FULL_CONTROL"],
    },
)

AthenaErrorTypeDef = TypedDict(
    "AthenaErrorTypeDef",
    {
        "ErrorCategory": int,
        "ErrorType": int,
        "Retryable": bool,
        "ErrorMessage": str,
    },
    total=False,
)

BatchGetNamedQueryInputRequestTypeDef = TypedDict(
    "BatchGetNamedQueryInputRequestTypeDef",
    {
        "NamedQueryIds": Sequence[str],
    },
)

_RequiredNamedQueryTypeDef = TypedDict(
    "_RequiredNamedQueryTypeDef",
    {
        "Name": str,
        "Database": str,
        "QueryString": str,
    },
)
_OptionalNamedQueryTypeDef = TypedDict(
    "_OptionalNamedQueryTypeDef",
    {
        "Description": str,
        "NamedQueryId": str,
        "WorkGroup": str,
    },
    total=False,
)


class NamedQueryTypeDef(_RequiredNamedQueryTypeDef, _OptionalNamedQueryTypeDef):
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

UnprocessedNamedQueryIdTypeDef = TypedDict(
    "UnprocessedNamedQueryIdTypeDef",
    {
        "NamedQueryId": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

BatchGetQueryExecutionInputRequestTypeDef = TypedDict(
    "BatchGetQueryExecutionInputRequestTypeDef",
    {
        "QueryExecutionIds": Sequence[str],
    },
)

UnprocessedQueryExecutionIdTypeDef = TypedDict(
    "UnprocessedQueryExecutionIdTypeDef",
    {
        "QueryExecutionId": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredColumnInfoTypeDef = TypedDict(
    "_RequiredColumnInfoTypeDef",
    {
        "Name": str,
        "Type": str,
    },
)
_OptionalColumnInfoTypeDef = TypedDict(
    "_OptionalColumnInfoTypeDef",
    {
        "CatalogName": str,
        "SchemaName": str,
        "TableName": str,
        "Label": str,
        "Precision": int,
        "Scale": int,
        "Nullable": ColumnNullableType,
        "CaseSensitive": bool,
    },
    total=False,
)


class ColumnInfoTypeDef(_RequiredColumnInfoTypeDef, _OptionalColumnInfoTypeDef):
    pass


_RequiredColumnTypeDef = TypedDict(
    "_RequiredColumnTypeDef",
    {
        "Name": str,
    },
)
_OptionalColumnTypeDef = TypedDict(
    "_OptionalColumnTypeDef",
    {
        "Type": str,
        "Comment": str,
    },
    total=False,
)


class ColumnTypeDef(_RequiredColumnTypeDef, _OptionalColumnTypeDef):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

_RequiredCreateNamedQueryInputRequestTypeDef = TypedDict(
    "_RequiredCreateNamedQueryInputRequestTypeDef",
    {
        "Name": str,
        "Database": str,
        "QueryString": str,
    },
)
_OptionalCreateNamedQueryInputRequestTypeDef = TypedDict(
    "_OptionalCreateNamedQueryInputRequestTypeDef",
    {
        "Description": str,
        "ClientRequestToken": str,
        "WorkGroup": str,
    },
    total=False,
)


class CreateNamedQueryInputRequestTypeDef(
    _RequiredCreateNamedQueryInputRequestTypeDef, _OptionalCreateNamedQueryInputRequestTypeDef
):
    pass


_RequiredCreatePreparedStatementInputRequestTypeDef = TypedDict(
    "_RequiredCreatePreparedStatementInputRequestTypeDef",
    {
        "StatementName": str,
        "WorkGroup": str,
        "QueryStatement": str,
    },
)
_OptionalCreatePreparedStatementInputRequestTypeDef = TypedDict(
    "_OptionalCreatePreparedStatementInputRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreatePreparedStatementInputRequestTypeDef(
    _RequiredCreatePreparedStatementInputRequestTypeDef,
    _OptionalCreatePreparedStatementInputRequestTypeDef,
):
    pass


DataCatalogSummaryTypeDef = TypedDict(
    "DataCatalogSummaryTypeDef",
    {
        "CatalogName": str,
        "Type": DataCatalogTypeType,
    },
    total=False,
)

_RequiredDataCatalogTypeDef = TypedDict(
    "_RequiredDataCatalogTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
    },
)
_OptionalDataCatalogTypeDef = TypedDict(
    "_OptionalDataCatalogTypeDef",
    {
        "Description": str,
        "Parameters": Dict[str, str],
    },
    total=False,
)


class DataCatalogTypeDef(_RequiredDataCatalogTypeDef, _OptionalDataCatalogTypeDef):
    pass


_RequiredDatabaseTypeDef = TypedDict(
    "_RequiredDatabaseTypeDef",
    {
        "Name": str,
    },
)
_OptionalDatabaseTypeDef = TypedDict(
    "_OptionalDatabaseTypeDef",
    {
        "Description": str,
        "Parameters": Dict[str, str],
    },
    total=False,
)


class DatabaseTypeDef(_RequiredDatabaseTypeDef, _OptionalDatabaseTypeDef):
    pass


DatumTypeDef = TypedDict(
    "DatumTypeDef",
    {
        "VarCharValue": str,
    },
    total=False,
)

DeleteDataCatalogInputRequestTypeDef = TypedDict(
    "DeleteDataCatalogInputRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteNamedQueryInputRequestTypeDef = TypedDict(
    "DeleteNamedQueryInputRequestTypeDef",
    {
        "NamedQueryId": str,
    },
)

DeletePreparedStatementInputRequestTypeDef = TypedDict(
    "DeletePreparedStatementInputRequestTypeDef",
    {
        "StatementName": str,
        "WorkGroup": str,
    },
)

_RequiredDeleteWorkGroupInputRequestTypeDef = TypedDict(
    "_RequiredDeleteWorkGroupInputRequestTypeDef",
    {
        "WorkGroup": str,
    },
)
_OptionalDeleteWorkGroupInputRequestTypeDef = TypedDict(
    "_OptionalDeleteWorkGroupInputRequestTypeDef",
    {
        "RecursiveDeleteOption": bool,
    },
    total=False,
)


class DeleteWorkGroupInputRequestTypeDef(
    _RequiredDeleteWorkGroupInputRequestTypeDef, _OptionalDeleteWorkGroupInputRequestTypeDef
):
    pass


_RequiredEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredEncryptionConfigurationTypeDef",
    {
        "EncryptionOption": EncryptionOptionType,
    },
)
_OptionalEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalEncryptionConfigurationTypeDef",
    {
        "KmsKey": str,
    },
    total=False,
)


class EncryptionConfigurationTypeDef(
    _RequiredEncryptionConfigurationTypeDef, _OptionalEncryptionConfigurationTypeDef
):
    pass


EngineVersionTypeDef = TypedDict(
    "EngineVersionTypeDef",
    {
        "SelectedEngineVersion": str,
        "EffectiveEngineVersion": str,
    },
    total=False,
)

GetDataCatalogInputRequestTypeDef = TypedDict(
    "GetDataCatalogInputRequestTypeDef",
    {
        "Name": str,
    },
)

GetDatabaseInputRequestTypeDef = TypedDict(
    "GetDatabaseInputRequestTypeDef",
    {
        "CatalogName": str,
        "DatabaseName": str,
    },
)

GetNamedQueryInputRequestTypeDef = TypedDict(
    "GetNamedQueryInputRequestTypeDef",
    {
        "NamedQueryId": str,
    },
)

GetPreparedStatementInputRequestTypeDef = TypedDict(
    "GetPreparedStatementInputRequestTypeDef",
    {
        "StatementName": str,
        "WorkGroup": str,
    },
)

PreparedStatementTypeDef = TypedDict(
    "PreparedStatementTypeDef",
    {
        "StatementName": str,
        "QueryStatement": str,
        "WorkGroupName": str,
        "Description": str,
        "LastModifiedTime": datetime,
    },
    total=False,
)

GetQueryExecutionInputRequestTypeDef = TypedDict(
    "GetQueryExecutionInputRequestTypeDef",
    {
        "QueryExecutionId": str,
    },
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

_RequiredGetQueryResultsInputRequestTypeDef = TypedDict(
    "_RequiredGetQueryResultsInputRequestTypeDef",
    {
        "QueryExecutionId": str,
    },
)
_OptionalGetQueryResultsInputRequestTypeDef = TypedDict(
    "_OptionalGetQueryResultsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetQueryResultsInputRequestTypeDef(
    _RequiredGetQueryResultsInputRequestTypeDef, _OptionalGetQueryResultsInputRequestTypeDef
):
    pass


GetTableMetadataInputRequestTypeDef = TypedDict(
    "GetTableMetadataInputRequestTypeDef",
    {
        "CatalogName": str,
        "DatabaseName": str,
        "TableName": str,
    },
)

GetWorkGroupInputRequestTypeDef = TypedDict(
    "GetWorkGroupInputRequestTypeDef",
    {
        "WorkGroup": str,
    },
)

ListDataCatalogsInputRequestTypeDef = TypedDict(
    "ListDataCatalogsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListDatabasesInputRequestTypeDef = TypedDict(
    "_RequiredListDatabasesInputRequestTypeDef",
    {
        "CatalogName": str,
    },
)
_OptionalListDatabasesInputRequestTypeDef = TypedDict(
    "_OptionalListDatabasesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatabasesInputRequestTypeDef(
    _RequiredListDatabasesInputRequestTypeDef, _OptionalListDatabasesInputRequestTypeDef
):
    pass


ListEngineVersionsInputRequestTypeDef = TypedDict(
    "ListEngineVersionsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListNamedQueriesInputRequestTypeDef = TypedDict(
    "ListNamedQueriesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "WorkGroup": str,
    },
    total=False,
)

_RequiredListPreparedStatementsInputRequestTypeDef = TypedDict(
    "_RequiredListPreparedStatementsInputRequestTypeDef",
    {
        "WorkGroup": str,
    },
)
_OptionalListPreparedStatementsInputRequestTypeDef = TypedDict(
    "_OptionalListPreparedStatementsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPreparedStatementsInputRequestTypeDef(
    _RequiredListPreparedStatementsInputRequestTypeDef,
    _OptionalListPreparedStatementsInputRequestTypeDef,
):
    pass


PreparedStatementSummaryTypeDef = TypedDict(
    "PreparedStatementSummaryTypeDef",
    {
        "StatementName": str,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ListQueryExecutionsInputRequestTypeDef = TypedDict(
    "ListQueryExecutionsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "WorkGroup": str,
    },
    total=False,
)

_RequiredListTableMetadataInputRequestTypeDef = TypedDict(
    "_RequiredListTableMetadataInputRequestTypeDef",
    {
        "CatalogName": str,
        "DatabaseName": str,
    },
)
_OptionalListTableMetadataInputRequestTypeDef = TypedDict(
    "_OptionalListTableMetadataInputRequestTypeDef",
    {
        "Expression": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTableMetadataInputRequestTypeDef(
    _RequiredListTableMetadataInputRequestTypeDef, _OptionalListTableMetadataInputRequestTypeDef
):
    pass


_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


ListWorkGroupsInputRequestTypeDef = TypedDict(
    "ListWorkGroupsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

QueryExecutionContextTypeDef = TypedDict(
    "QueryExecutionContextTypeDef",
    {
        "Database": str,
        "Catalog": str,
    },
    total=False,
)

QueryExecutionStatisticsTypeDef = TypedDict(
    "QueryExecutionStatisticsTypeDef",
    {
        "EngineExecutionTimeInMillis": int,
        "DataScannedInBytes": int,
        "DataManifestLocation": str,
        "TotalExecutionTimeInMillis": int,
        "QueryQueueTimeInMillis": int,
        "QueryPlanningTimeInMillis": int,
        "ServiceProcessingTimeInMillis": int,
    },
    total=False,
)

StopQueryExecutionInputRequestTypeDef = TypedDict(
    "StopQueryExecutionInputRequestTypeDef",
    {
        "QueryExecutionId": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateDataCatalogInputRequestTypeDef = TypedDict(
    "_RequiredUpdateDataCatalogInputRequestTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
    },
)
_OptionalUpdateDataCatalogInputRequestTypeDef = TypedDict(
    "_OptionalUpdateDataCatalogInputRequestTypeDef",
    {
        "Description": str,
        "Parameters": Mapping[str, str],
    },
    total=False,
)


class UpdateDataCatalogInputRequestTypeDef(
    _RequiredUpdateDataCatalogInputRequestTypeDef, _OptionalUpdateDataCatalogInputRequestTypeDef
):
    pass


_RequiredUpdateNamedQueryInputRequestTypeDef = TypedDict(
    "_RequiredUpdateNamedQueryInputRequestTypeDef",
    {
        "NamedQueryId": str,
        "Name": str,
        "QueryString": str,
    },
)
_OptionalUpdateNamedQueryInputRequestTypeDef = TypedDict(
    "_OptionalUpdateNamedQueryInputRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateNamedQueryInputRequestTypeDef(
    _RequiredUpdateNamedQueryInputRequestTypeDef, _OptionalUpdateNamedQueryInputRequestTypeDef
):
    pass


_RequiredUpdatePreparedStatementInputRequestTypeDef = TypedDict(
    "_RequiredUpdatePreparedStatementInputRequestTypeDef",
    {
        "StatementName": str,
        "WorkGroup": str,
        "QueryStatement": str,
    },
)
_OptionalUpdatePreparedStatementInputRequestTypeDef = TypedDict(
    "_OptionalUpdatePreparedStatementInputRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdatePreparedStatementInputRequestTypeDef(
    _RequiredUpdatePreparedStatementInputRequestTypeDef,
    _OptionalUpdatePreparedStatementInputRequestTypeDef,
):
    pass


QueryExecutionStatusTypeDef = TypedDict(
    "QueryExecutionStatusTypeDef",
    {
        "State": QueryExecutionStateType,
        "StateChangeReason": str,
        "SubmissionDateTime": datetime,
        "CompletionDateTime": datetime,
        "AthenaError": AthenaErrorTypeDef,
    },
    total=False,
)

CreateNamedQueryOutputTypeDef = TypedDict(
    "CreateNamedQueryOutputTypeDef",
    {
        "NamedQueryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNamedQueryOutputTypeDef = TypedDict(
    "GetNamedQueryOutputTypeDef",
    {
        "NamedQuery": NamedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNamedQueriesOutputTypeDef = TypedDict(
    "ListNamedQueriesOutputTypeDef",
    {
        "NamedQueryIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueryExecutionsOutputTypeDef = TypedDict(
    "ListQueryExecutionsOutputTypeDef",
    {
        "QueryExecutionIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartQueryExecutionOutputTypeDef = TypedDict(
    "StartQueryExecutionOutputTypeDef",
    {
        "QueryExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetNamedQueryOutputTypeDef = TypedDict(
    "BatchGetNamedQueryOutputTypeDef",
    {
        "NamedQueries": List[NamedQueryTypeDef],
        "UnprocessedNamedQueryIds": List[UnprocessedNamedQueryIdTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResultSetMetadataTypeDef = TypedDict(
    "ResultSetMetadataTypeDef",
    {
        "ColumnInfo": List[ColumnInfoTypeDef],
    },
    total=False,
)

_RequiredTableMetadataTypeDef = TypedDict(
    "_RequiredTableMetadataTypeDef",
    {
        "Name": str,
    },
)
_OptionalTableMetadataTypeDef = TypedDict(
    "_OptionalTableMetadataTypeDef",
    {
        "CreateTime": datetime,
        "LastAccessTime": datetime,
        "TableType": str,
        "Columns": List[ColumnTypeDef],
        "PartitionKeys": List[ColumnTypeDef],
        "Parameters": Dict[str, str],
    },
    total=False,
)


class TableMetadataTypeDef(_RequiredTableMetadataTypeDef, _OptionalTableMetadataTypeDef):
    pass


_RequiredCreateDataCatalogInputRequestTypeDef = TypedDict(
    "_RequiredCreateDataCatalogInputRequestTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
    },
)
_OptionalCreateDataCatalogInputRequestTypeDef = TypedDict(
    "_OptionalCreateDataCatalogInputRequestTypeDef",
    {
        "Description": str,
        "Parameters": Mapping[str, str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDataCatalogInputRequestTypeDef(
    _RequiredCreateDataCatalogInputRequestTypeDef, _OptionalCreateDataCatalogInputRequestTypeDef
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListDataCatalogsOutputTypeDef = TypedDict(
    "ListDataCatalogsOutputTypeDef",
    {
        "DataCatalogsSummary": List[DataCatalogSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataCatalogOutputTypeDef = TypedDict(
    "GetDataCatalogOutputTypeDef",
    {
        "DataCatalog": DataCatalogTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDatabaseOutputTypeDef = TypedDict(
    "GetDatabaseOutputTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatabasesOutputTypeDef = TypedDict(
    "ListDatabasesOutputTypeDef",
    {
        "DatabaseList": List[DatabaseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RowTypeDef = TypedDict(
    "RowTypeDef",
    {
        "Data": List[DatumTypeDef],
    },
    total=False,
)

ResultConfigurationTypeDef = TypedDict(
    "ResultConfigurationTypeDef",
    {
        "OutputLocation": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "ExpectedBucketOwner": str,
        "AclConfiguration": AclConfigurationTypeDef,
    },
    total=False,
)

ResultConfigurationUpdatesTypeDef = TypedDict(
    "ResultConfigurationUpdatesTypeDef",
    {
        "OutputLocation": str,
        "RemoveOutputLocation": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "RemoveEncryptionConfiguration": bool,
        "ExpectedBucketOwner": str,
        "RemoveExpectedBucketOwner": bool,
        "AclConfiguration": AclConfigurationTypeDef,
        "RemoveAclConfiguration": bool,
    },
    total=False,
)

ListEngineVersionsOutputTypeDef = TypedDict(
    "ListEngineVersionsOutputTypeDef",
    {
        "EngineVersions": List[EngineVersionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkGroupSummaryTypeDef = TypedDict(
    "WorkGroupSummaryTypeDef",
    {
        "Name": str,
        "State": WorkGroupStateType,
        "Description": str,
        "CreationTime": datetime,
        "EngineVersion": EngineVersionTypeDef,
    },
    total=False,
)

GetPreparedStatementOutputTypeDef = TypedDict(
    "GetPreparedStatementOutputTypeDef",
    {
        "PreparedStatement": PreparedStatementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetQueryResultsInputGetQueryResultsPaginateTypeDef = TypedDict(
    "_RequiredGetQueryResultsInputGetQueryResultsPaginateTypeDef",
    {
        "QueryExecutionId": str,
    },
)
_OptionalGetQueryResultsInputGetQueryResultsPaginateTypeDef = TypedDict(
    "_OptionalGetQueryResultsInputGetQueryResultsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetQueryResultsInputGetQueryResultsPaginateTypeDef(
    _RequiredGetQueryResultsInputGetQueryResultsPaginateTypeDef,
    _OptionalGetQueryResultsInputGetQueryResultsPaginateTypeDef,
):
    pass


ListDataCatalogsInputListDataCatalogsPaginateTypeDef = TypedDict(
    "ListDataCatalogsInputListDataCatalogsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDatabasesInputListDatabasesPaginateTypeDef = TypedDict(
    "_RequiredListDatabasesInputListDatabasesPaginateTypeDef",
    {
        "CatalogName": str,
    },
)
_OptionalListDatabasesInputListDatabasesPaginateTypeDef = TypedDict(
    "_OptionalListDatabasesInputListDatabasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDatabasesInputListDatabasesPaginateTypeDef(
    _RequiredListDatabasesInputListDatabasesPaginateTypeDef,
    _OptionalListDatabasesInputListDatabasesPaginateTypeDef,
):
    pass


ListNamedQueriesInputListNamedQueriesPaginateTypeDef = TypedDict(
    "ListNamedQueriesInputListNamedQueriesPaginateTypeDef",
    {
        "WorkGroup": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef = TypedDict(
    "ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef",
    {
        "WorkGroup": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTableMetadataInputListTableMetadataPaginateTypeDef = TypedDict(
    "_RequiredListTableMetadataInputListTableMetadataPaginateTypeDef",
    {
        "CatalogName": str,
        "DatabaseName": str,
    },
)
_OptionalListTableMetadataInputListTableMetadataPaginateTypeDef = TypedDict(
    "_OptionalListTableMetadataInputListTableMetadataPaginateTypeDef",
    {
        "Expression": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTableMetadataInputListTableMetadataPaginateTypeDef(
    _RequiredListTableMetadataInputListTableMetadataPaginateTypeDef,
    _OptionalListTableMetadataInputListTableMetadataPaginateTypeDef,
):
    pass


_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass


ListPreparedStatementsOutputTypeDef = TypedDict(
    "ListPreparedStatementsOutputTypeDef",
    {
        "PreparedStatements": List[PreparedStatementSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTableMetadataOutputTypeDef = TypedDict(
    "GetTableMetadataOutputTypeDef",
    {
        "TableMetadata": TableMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTableMetadataOutputTypeDef = TypedDict(
    "ListTableMetadataOutputTypeDef",
    {
        "TableMetadataList": List[TableMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResultSetTypeDef = TypedDict(
    "ResultSetTypeDef",
    {
        "Rows": List[RowTypeDef],
        "ResultSetMetadata": ResultSetMetadataTypeDef,
    },
    total=False,
)

QueryExecutionTypeDef = TypedDict(
    "QueryExecutionTypeDef",
    {
        "QueryExecutionId": str,
        "Query": str,
        "StatementType": StatementTypeType,
        "ResultConfiguration": ResultConfigurationTypeDef,
        "QueryExecutionContext": QueryExecutionContextTypeDef,
        "Status": QueryExecutionStatusTypeDef,
        "Statistics": QueryExecutionStatisticsTypeDef,
        "WorkGroup": str,
        "EngineVersion": EngineVersionTypeDef,
    },
    total=False,
)

_RequiredStartQueryExecutionInputRequestTypeDef = TypedDict(
    "_RequiredStartQueryExecutionInputRequestTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalStartQueryExecutionInputRequestTypeDef = TypedDict(
    "_OptionalStartQueryExecutionInputRequestTypeDef",
    {
        "ClientRequestToken": str,
        "QueryExecutionContext": QueryExecutionContextTypeDef,
        "ResultConfiguration": ResultConfigurationTypeDef,
        "WorkGroup": str,
    },
    total=False,
)


class StartQueryExecutionInputRequestTypeDef(
    _RequiredStartQueryExecutionInputRequestTypeDef, _OptionalStartQueryExecutionInputRequestTypeDef
):
    pass


WorkGroupConfigurationTypeDef = TypedDict(
    "WorkGroupConfigurationTypeDef",
    {
        "ResultConfiguration": ResultConfigurationTypeDef,
        "EnforceWorkGroupConfiguration": bool,
        "PublishCloudWatchMetricsEnabled": bool,
        "BytesScannedCutoffPerQuery": int,
        "RequesterPaysEnabled": bool,
        "EngineVersion": EngineVersionTypeDef,
    },
    total=False,
)

WorkGroupConfigurationUpdatesTypeDef = TypedDict(
    "WorkGroupConfigurationUpdatesTypeDef",
    {
        "EnforceWorkGroupConfiguration": bool,
        "ResultConfigurationUpdates": ResultConfigurationUpdatesTypeDef,
        "PublishCloudWatchMetricsEnabled": bool,
        "BytesScannedCutoffPerQuery": int,
        "RemoveBytesScannedCutoffPerQuery": bool,
        "RequesterPaysEnabled": bool,
        "EngineVersion": EngineVersionTypeDef,
    },
    total=False,
)

ListWorkGroupsOutputTypeDef = TypedDict(
    "ListWorkGroupsOutputTypeDef",
    {
        "WorkGroups": List[WorkGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryResultsOutputTypeDef = TypedDict(
    "GetQueryResultsOutputTypeDef",
    {
        "UpdateCount": int,
        "ResultSet": ResultSetTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetQueryExecutionOutputTypeDef = TypedDict(
    "BatchGetQueryExecutionOutputTypeDef",
    {
        "QueryExecutions": List[QueryExecutionTypeDef],
        "UnprocessedQueryExecutionIds": List[UnprocessedQueryExecutionIdTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryExecutionOutputTypeDef = TypedDict(
    "GetQueryExecutionOutputTypeDef",
    {
        "QueryExecution": QueryExecutionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateWorkGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateWorkGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateWorkGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateWorkGroupInputRequestTypeDef",
    {
        "Configuration": WorkGroupConfigurationTypeDef,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWorkGroupInputRequestTypeDef(
    _RequiredCreateWorkGroupInputRequestTypeDef, _OptionalCreateWorkGroupInputRequestTypeDef
):
    pass


_RequiredWorkGroupTypeDef = TypedDict(
    "_RequiredWorkGroupTypeDef",
    {
        "Name": str,
    },
)
_OptionalWorkGroupTypeDef = TypedDict(
    "_OptionalWorkGroupTypeDef",
    {
        "State": WorkGroupStateType,
        "Configuration": WorkGroupConfigurationTypeDef,
        "Description": str,
        "CreationTime": datetime,
    },
    total=False,
)


class WorkGroupTypeDef(_RequiredWorkGroupTypeDef, _OptionalWorkGroupTypeDef):
    pass


_RequiredUpdateWorkGroupInputRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkGroupInputRequestTypeDef",
    {
        "WorkGroup": str,
    },
)
_OptionalUpdateWorkGroupInputRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkGroupInputRequestTypeDef",
    {
        "Description": str,
        "ConfigurationUpdates": WorkGroupConfigurationUpdatesTypeDef,
        "State": WorkGroupStateType,
    },
    total=False,
)


class UpdateWorkGroupInputRequestTypeDef(
    _RequiredUpdateWorkGroupInputRequestTypeDef, _OptionalUpdateWorkGroupInputRequestTypeDef
):
    pass


GetWorkGroupOutputTypeDef = TypedDict(
    "GetWorkGroupOutputTypeDef",
    {
        "WorkGroup": WorkGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
