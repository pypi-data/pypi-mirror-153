"""
Type annotations for rds-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_rds_data.type_defs import ArrayValueTypeDef

    data: ArrayValueTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import DecimalReturnTypeType, LongReturnTypeType, RecordsFormatTypeType, TypeHintType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ArrayValueTypeDef",
    "ResponseMetadataTypeDef",
    "BeginTransactionRequestRequestTypeDef",
    "ColumnMetadataTypeDef",
    "CommitTransactionRequestRequestTypeDef",
    "ExecuteSqlRequestRequestTypeDef",
    "ResultSetOptionsTypeDef",
    "FieldTypeDef",
    "RecordTypeDef",
    "RollbackTransactionRequestRequestTypeDef",
    "StructValueTypeDef",
    "ValueTypeDef",
    "BeginTransactionResponseTypeDef",
    "CommitTransactionResponseTypeDef",
    "RollbackTransactionResponseTypeDef",
    "ResultSetMetadataTypeDef",
    "ExecuteStatementResponseTypeDef",
    "SqlParameterTypeDef",
    "UpdateResultTypeDef",
    "ResultFrameTypeDef",
    "BatchExecuteStatementRequestRequestTypeDef",
    "ExecuteStatementRequestRequestTypeDef",
    "BatchExecuteStatementResponseTypeDef",
    "SqlStatementResultTypeDef",
    "ExecuteSqlResponseTypeDef",
)

ArrayValueTypeDef = TypedDict(
    "ArrayValueTypeDef",
    {
        "arrayValues": Sequence[Dict[str, Any]],
        "booleanValues": Sequence[bool],
        "doubleValues": Sequence[float],
        "longValues": Sequence[int],
        "stringValues": Sequence[str],
    },
    total=False,
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

_RequiredBeginTransactionRequestRequestTypeDef = TypedDict(
    "_RequiredBeginTransactionRequestRequestTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
    },
)
_OptionalBeginTransactionRequestRequestTypeDef = TypedDict(
    "_OptionalBeginTransactionRequestRequestTypeDef",
    {
        "database": str,
        "schema": str,
    },
    total=False,
)


class BeginTransactionRequestRequestTypeDef(
    _RequiredBeginTransactionRequestRequestTypeDef, _OptionalBeginTransactionRequestRequestTypeDef
):
    pass


ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "arrayBaseColumnType": int,
        "isAutoIncrement": bool,
        "isCaseSensitive": bool,
        "isCurrency": bool,
        "isSigned": bool,
        "label": str,
        "name": str,
        "nullable": int,
        "precision": int,
        "scale": int,
        "schemaName": str,
        "tableName": str,
        "type": int,
        "typeName": str,
    },
    total=False,
)

CommitTransactionRequestRequestTypeDef = TypedDict(
    "CommitTransactionRequestRequestTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
        "transactionId": str,
    },
)

_RequiredExecuteSqlRequestRequestTypeDef = TypedDict(
    "_RequiredExecuteSqlRequestRequestTypeDef",
    {
        "awsSecretStoreArn": str,
        "dbClusterOrInstanceArn": str,
        "sqlStatements": str,
    },
)
_OptionalExecuteSqlRequestRequestTypeDef = TypedDict(
    "_OptionalExecuteSqlRequestRequestTypeDef",
    {
        "database": str,
        "schema": str,
    },
    total=False,
)


class ExecuteSqlRequestRequestTypeDef(
    _RequiredExecuteSqlRequestRequestTypeDef, _OptionalExecuteSqlRequestRequestTypeDef
):
    pass


ResultSetOptionsTypeDef = TypedDict(
    "ResultSetOptionsTypeDef",
    {
        "decimalReturnType": DecimalReturnTypeType,
        "longReturnType": LongReturnTypeType,
    },
    total=False,
)

FieldTypeDef = TypedDict(
    "FieldTypeDef",
    {
        "arrayValue": "ArrayValueTypeDef",
        "blobValue": Union[str, bytes, IO[Any], StreamingBody],
        "booleanValue": bool,
        "doubleValue": float,
        "isNull": bool,
        "longValue": int,
        "stringValue": str,
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "values": List["ValueTypeDef"],
    },
    total=False,
)

RollbackTransactionRequestRequestTypeDef = TypedDict(
    "RollbackTransactionRequestRequestTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
        "transactionId": str,
    },
)

StructValueTypeDef = TypedDict(
    "StructValueTypeDef",
    {
        "attributes": List[Dict[str, Any]],
    },
    total=False,
)

ValueTypeDef = TypedDict(
    "ValueTypeDef",
    {
        "arrayValues": List[Dict[str, Any]],
        "bigIntValue": int,
        "bitValue": bool,
        "blobValue": bytes,
        "doubleValue": float,
        "intValue": int,
        "isNull": bool,
        "realValue": float,
        "stringValue": str,
        "structValue": Dict[str, Any],
    },
    total=False,
)

BeginTransactionResponseTypeDef = TypedDict(
    "BeginTransactionResponseTypeDef",
    {
        "transactionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CommitTransactionResponseTypeDef = TypedDict(
    "CommitTransactionResponseTypeDef",
    {
        "transactionStatus": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RollbackTransactionResponseTypeDef = TypedDict(
    "RollbackTransactionResponseTypeDef",
    {
        "transactionStatus": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResultSetMetadataTypeDef = TypedDict(
    "ResultSetMetadataTypeDef",
    {
        "columnCount": int,
        "columnMetadata": List[ColumnMetadataTypeDef],
    },
    total=False,
)

ExecuteStatementResponseTypeDef = TypedDict(
    "ExecuteStatementResponseTypeDef",
    {
        "columnMetadata": List[ColumnMetadataTypeDef],
        "formattedRecords": str,
        "generatedFields": List[FieldTypeDef],
        "numberOfRecordsUpdated": int,
        "records": List[List[FieldTypeDef]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SqlParameterTypeDef = TypedDict(
    "SqlParameterTypeDef",
    {
        "name": str,
        "typeHint": TypeHintType,
        "value": FieldTypeDef,
    },
    total=False,
)

UpdateResultTypeDef = TypedDict(
    "UpdateResultTypeDef",
    {
        "generatedFields": List[FieldTypeDef],
    },
    total=False,
)

ResultFrameTypeDef = TypedDict(
    "ResultFrameTypeDef",
    {
        "records": List[RecordTypeDef],
        "resultSetMetadata": ResultSetMetadataTypeDef,
    },
    total=False,
)

_RequiredBatchExecuteStatementRequestRequestTypeDef = TypedDict(
    "_RequiredBatchExecuteStatementRequestRequestTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
        "sql": str,
    },
)
_OptionalBatchExecuteStatementRequestRequestTypeDef = TypedDict(
    "_OptionalBatchExecuteStatementRequestRequestTypeDef",
    {
        "database": str,
        "parameterSets": Sequence[Sequence[SqlParameterTypeDef]],
        "schema": str,
        "transactionId": str,
    },
    total=False,
)


class BatchExecuteStatementRequestRequestTypeDef(
    _RequiredBatchExecuteStatementRequestRequestTypeDef,
    _OptionalBatchExecuteStatementRequestRequestTypeDef,
):
    pass


_RequiredExecuteStatementRequestRequestTypeDef = TypedDict(
    "_RequiredExecuteStatementRequestRequestTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
        "sql": str,
    },
)
_OptionalExecuteStatementRequestRequestTypeDef = TypedDict(
    "_OptionalExecuteStatementRequestRequestTypeDef",
    {
        "continueAfterTimeout": bool,
        "database": str,
        "formatRecordsAs": RecordsFormatTypeType,
        "includeResultMetadata": bool,
        "parameters": Sequence[SqlParameterTypeDef],
        "resultSetOptions": ResultSetOptionsTypeDef,
        "schema": str,
        "transactionId": str,
    },
    total=False,
)


class ExecuteStatementRequestRequestTypeDef(
    _RequiredExecuteStatementRequestRequestTypeDef, _OptionalExecuteStatementRequestRequestTypeDef
):
    pass


BatchExecuteStatementResponseTypeDef = TypedDict(
    "BatchExecuteStatementResponseTypeDef",
    {
        "updateResults": List[UpdateResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SqlStatementResultTypeDef = TypedDict(
    "SqlStatementResultTypeDef",
    {
        "numberOfRecordsUpdated": int,
        "resultFrame": ResultFrameTypeDef,
    },
    total=False,
)

ExecuteSqlResponseTypeDef = TypedDict(
    "ExecuteSqlResponseTypeDef",
    {
        "sqlStatementResults": List[SqlStatementResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
