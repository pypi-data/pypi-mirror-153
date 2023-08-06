"""
Type annotations for qldb-session service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/type_defs/)

Usage::

    ```python
    from mypy_boto3_qldb_session.type_defs import TimingInformationTypeDef

    data: TimingInformationTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TimingInformationTypeDef",
    "CommitTransactionRequestTypeDef",
    "IOUsageTypeDef",
    "ValueHolderTypeDef",
    "FetchPageRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StartSessionRequestTypeDef",
    "AbortTransactionResultTypeDef",
    "EndSessionResultTypeDef",
    "StartSessionResultTypeDef",
    "StartTransactionResultTypeDef",
    "CommitTransactionResultTypeDef",
    "ExecuteStatementRequestTypeDef",
    "PageTypeDef",
    "SendCommandRequestRequestTypeDef",
    "ExecuteStatementResultTypeDef",
    "FetchPageResultTypeDef",
    "SendCommandResultTypeDef",
)

TimingInformationTypeDef = TypedDict(
    "TimingInformationTypeDef",
    {
        "ProcessingTimeMilliseconds": int,
    },
    total=False,
)

CommitTransactionRequestTypeDef = TypedDict(
    "CommitTransactionRequestTypeDef",
    {
        "TransactionId": str,
        "CommitDigest": Union[str, bytes, IO[Any], StreamingBody],
    },
)

IOUsageTypeDef = TypedDict(
    "IOUsageTypeDef",
    {
        "ReadIOs": int,
        "WriteIOs": int,
    },
    total=False,
)

ValueHolderTypeDef = TypedDict(
    "ValueHolderTypeDef",
    {
        "IonBinary": Union[str, bytes, IO[Any], StreamingBody],
        "IonText": str,
    },
    total=False,
)

FetchPageRequestTypeDef = TypedDict(
    "FetchPageRequestTypeDef",
    {
        "TransactionId": str,
        "NextPageToken": str,
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

StartSessionRequestTypeDef = TypedDict(
    "StartSessionRequestTypeDef",
    {
        "LedgerName": str,
    },
)

AbortTransactionResultTypeDef = TypedDict(
    "AbortTransactionResultTypeDef",
    {
        "TimingInformation": TimingInformationTypeDef,
    },
    total=False,
)

EndSessionResultTypeDef = TypedDict(
    "EndSessionResultTypeDef",
    {
        "TimingInformation": TimingInformationTypeDef,
    },
    total=False,
)

StartSessionResultTypeDef = TypedDict(
    "StartSessionResultTypeDef",
    {
        "SessionToken": str,
        "TimingInformation": TimingInformationTypeDef,
    },
    total=False,
)

StartTransactionResultTypeDef = TypedDict(
    "StartTransactionResultTypeDef",
    {
        "TransactionId": str,
        "TimingInformation": TimingInformationTypeDef,
    },
    total=False,
)

CommitTransactionResultTypeDef = TypedDict(
    "CommitTransactionResultTypeDef",
    {
        "TransactionId": str,
        "CommitDigest": bytes,
        "TimingInformation": TimingInformationTypeDef,
        "ConsumedIOs": IOUsageTypeDef,
    },
    total=False,
)

_RequiredExecuteStatementRequestTypeDef = TypedDict(
    "_RequiredExecuteStatementRequestTypeDef",
    {
        "TransactionId": str,
        "Statement": str,
    },
)
_OptionalExecuteStatementRequestTypeDef = TypedDict(
    "_OptionalExecuteStatementRequestTypeDef",
    {
        "Parameters": Sequence[ValueHolderTypeDef],
    },
    total=False,
)


class ExecuteStatementRequestTypeDef(
    _RequiredExecuteStatementRequestTypeDef, _OptionalExecuteStatementRequestTypeDef
):
    pass


PageTypeDef = TypedDict(
    "PageTypeDef",
    {
        "Values": List[ValueHolderTypeDef],
        "NextPageToken": str,
    },
    total=False,
)

SendCommandRequestRequestTypeDef = TypedDict(
    "SendCommandRequestRequestTypeDef",
    {
        "SessionToken": str,
        "StartSession": StartSessionRequestTypeDef,
        "StartTransaction": Mapping[str, Any],
        "EndSession": Mapping[str, Any],
        "CommitTransaction": CommitTransactionRequestTypeDef,
        "AbortTransaction": Mapping[str, Any],
        "ExecuteStatement": ExecuteStatementRequestTypeDef,
        "FetchPage": FetchPageRequestTypeDef,
    },
    total=False,
)

ExecuteStatementResultTypeDef = TypedDict(
    "ExecuteStatementResultTypeDef",
    {
        "FirstPage": PageTypeDef,
        "TimingInformation": TimingInformationTypeDef,
        "ConsumedIOs": IOUsageTypeDef,
    },
    total=False,
)

FetchPageResultTypeDef = TypedDict(
    "FetchPageResultTypeDef",
    {
        "Page": PageTypeDef,
        "TimingInformation": TimingInformationTypeDef,
        "ConsumedIOs": IOUsageTypeDef,
    },
    total=False,
)

SendCommandResultTypeDef = TypedDict(
    "SendCommandResultTypeDef",
    {
        "StartSession": StartSessionResultTypeDef,
        "StartTransaction": StartTransactionResultTypeDef,
        "EndSession": EndSessionResultTypeDef,
        "CommitTransaction": CommitTransactionResultTypeDef,
        "AbortTransaction": AbortTransactionResultTypeDef,
        "ExecuteStatement": ExecuteStatementResultTypeDef,
        "FetchPage": FetchPageResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
