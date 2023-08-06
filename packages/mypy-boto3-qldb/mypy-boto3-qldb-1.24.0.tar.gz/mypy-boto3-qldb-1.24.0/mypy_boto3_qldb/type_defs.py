"""
Type annotations for qldb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb/type_defs/)

Usage::

    ```python
    from mypy_boto3_qldb.type_defs import CancelJournalKinesisStreamRequestRequestTypeDef

    data: CancelJournalKinesisStreamRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EncryptionStatusType,
    ErrorCauseType,
    ExportStatusType,
    LedgerStateType,
    OutputFormatType,
    PermissionsModeType,
    S3ObjectEncryptionTypeType,
    StreamStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelJournalKinesisStreamRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLedgerRequestRequestTypeDef",
    "DeleteLedgerRequestRequestTypeDef",
    "DescribeJournalKinesisStreamRequestRequestTypeDef",
    "DescribeJournalS3ExportRequestRequestTypeDef",
    "DescribeLedgerRequestRequestTypeDef",
    "LedgerEncryptionDescriptionTypeDef",
    "ValueHolderTypeDef",
    "GetDigestRequestRequestTypeDef",
    "KinesisConfigurationTypeDef",
    "LedgerSummaryTypeDef",
    "ListJournalKinesisStreamsForLedgerRequestRequestTypeDef",
    "ListJournalS3ExportsForLedgerRequestRequestTypeDef",
    "ListJournalS3ExportsRequestRequestTypeDef",
    "ListLedgersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "S3EncryptionConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLedgerPermissionsModeRequestRequestTypeDef",
    "UpdateLedgerRequestRequestTypeDef",
    "CancelJournalKinesisStreamResponseTypeDef",
    "CreateLedgerResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportJournalToS3ResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StreamJournalToKinesisResponseTypeDef",
    "UpdateLedgerPermissionsModeResponseTypeDef",
    "DescribeLedgerResponseTypeDef",
    "UpdateLedgerResponseTypeDef",
    "GetBlockRequestRequestTypeDef",
    "GetBlockResponseTypeDef",
    "GetDigestResponseTypeDef",
    "GetRevisionRequestRequestTypeDef",
    "GetRevisionResponseTypeDef",
    "JournalKinesisStreamDescriptionTypeDef",
    "StreamJournalToKinesisRequestRequestTypeDef",
    "ListLedgersResponseTypeDef",
    "S3ExportConfigurationTypeDef",
    "DescribeJournalKinesisStreamResponseTypeDef",
    "ListJournalKinesisStreamsForLedgerResponseTypeDef",
    "ExportJournalToS3RequestRequestTypeDef",
    "JournalS3ExportDescriptionTypeDef",
    "DescribeJournalS3ExportResponseTypeDef",
    "ListJournalS3ExportsForLedgerResponseTypeDef",
    "ListJournalS3ExportsResponseTypeDef",
)

CancelJournalKinesisStreamRequestRequestTypeDef = TypedDict(
    "CancelJournalKinesisStreamRequestRequestTypeDef",
    {
        "LedgerName": str,
        "StreamId": str,
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

_RequiredCreateLedgerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLedgerRequestRequestTypeDef",
    {
        "Name": str,
        "PermissionsMode": PermissionsModeType,
    },
)
_OptionalCreateLedgerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLedgerRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "DeletionProtection": bool,
        "KmsKey": str,
    },
    total=False,
)


class CreateLedgerRequestRequestTypeDef(
    _RequiredCreateLedgerRequestRequestTypeDef, _OptionalCreateLedgerRequestRequestTypeDef
):
    pass


DeleteLedgerRequestRequestTypeDef = TypedDict(
    "DeleteLedgerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeJournalKinesisStreamRequestRequestTypeDef = TypedDict(
    "DescribeJournalKinesisStreamRequestRequestTypeDef",
    {
        "LedgerName": str,
        "StreamId": str,
    },
)

DescribeJournalS3ExportRequestRequestTypeDef = TypedDict(
    "DescribeJournalS3ExportRequestRequestTypeDef",
    {
        "Name": str,
        "ExportId": str,
    },
)

DescribeLedgerRequestRequestTypeDef = TypedDict(
    "DescribeLedgerRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredLedgerEncryptionDescriptionTypeDef = TypedDict(
    "_RequiredLedgerEncryptionDescriptionTypeDef",
    {
        "KmsKeyArn": str,
        "EncryptionStatus": EncryptionStatusType,
    },
)
_OptionalLedgerEncryptionDescriptionTypeDef = TypedDict(
    "_OptionalLedgerEncryptionDescriptionTypeDef",
    {
        "InaccessibleKmsKeyDateTime": datetime,
    },
    total=False,
)


class LedgerEncryptionDescriptionTypeDef(
    _RequiredLedgerEncryptionDescriptionTypeDef, _OptionalLedgerEncryptionDescriptionTypeDef
):
    pass


ValueHolderTypeDef = TypedDict(
    "ValueHolderTypeDef",
    {
        "IonText": str,
    },
    total=False,
)

GetDigestRequestRequestTypeDef = TypedDict(
    "GetDigestRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredKinesisConfigurationTypeDef = TypedDict(
    "_RequiredKinesisConfigurationTypeDef",
    {
        "StreamArn": str,
    },
)
_OptionalKinesisConfigurationTypeDef = TypedDict(
    "_OptionalKinesisConfigurationTypeDef",
    {
        "AggregationEnabled": bool,
    },
    total=False,
)


class KinesisConfigurationTypeDef(
    _RequiredKinesisConfigurationTypeDef, _OptionalKinesisConfigurationTypeDef
):
    pass


LedgerSummaryTypeDef = TypedDict(
    "LedgerSummaryTypeDef",
    {
        "Name": str,
        "State": LedgerStateType,
        "CreationDateTime": datetime,
    },
    total=False,
)

_RequiredListJournalKinesisStreamsForLedgerRequestRequestTypeDef = TypedDict(
    "_RequiredListJournalKinesisStreamsForLedgerRequestRequestTypeDef",
    {
        "LedgerName": str,
    },
)
_OptionalListJournalKinesisStreamsForLedgerRequestRequestTypeDef = TypedDict(
    "_OptionalListJournalKinesisStreamsForLedgerRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListJournalKinesisStreamsForLedgerRequestRequestTypeDef(
    _RequiredListJournalKinesisStreamsForLedgerRequestRequestTypeDef,
    _OptionalListJournalKinesisStreamsForLedgerRequestRequestTypeDef,
):
    pass


_RequiredListJournalS3ExportsForLedgerRequestRequestTypeDef = TypedDict(
    "_RequiredListJournalS3ExportsForLedgerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalListJournalS3ExportsForLedgerRequestRequestTypeDef = TypedDict(
    "_OptionalListJournalS3ExportsForLedgerRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListJournalS3ExportsForLedgerRequestRequestTypeDef(
    _RequiredListJournalS3ExportsForLedgerRequestRequestTypeDef,
    _OptionalListJournalS3ExportsForLedgerRequestRequestTypeDef,
):
    pass


ListJournalS3ExportsRequestRequestTypeDef = TypedDict(
    "ListJournalS3ExportsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListLedgersRequestRequestTypeDef = TypedDict(
    "ListLedgersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredS3EncryptionConfigurationTypeDef = TypedDict(
    "_RequiredS3EncryptionConfigurationTypeDef",
    {
        "ObjectEncryptionType": S3ObjectEncryptionTypeType,
    },
)
_OptionalS3EncryptionConfigurationTypeDef = TypedDict(
    "_OptionalS3EncryptionConfigurationTypeDef",
    {
        "KmsKeyArn": str,
    },
    total=False,
)


class S3EncryptionConfigurationTypeDef(
    _RequiredS3EncryptionConfigurationTypeDef, _OptionalS3EncryptionConfigurationTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateLedgerPermissionsModeRequestRequestTypeDef = TypedDict(
    "UpdateLedgerPermissionsModeRequestRequestTypeDef",
    {
        "Name": str,
        "PermissionsMode": PermissionsModeType,
    },
)

_RequiredUpdateLedgerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLedgerRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateLedgerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLedgerRequestRequestTypeDef",
    {
        "DeletionProtection": bool,
        "KmsKey": str,
    },
    total=False,
)


class UpdateLedgerRequestRequestTypeDef(
    _RequiredUpdateLedgerRequestRequestTypeDef, _OptionalUpdateLedgerRequestRequestTypeDef
):
    pass


CancelJournalKinesisStreamResponseTypeDef = TypedDict(
    "CancelJournalKinesisStreamResponseTypeDef",
    {
        "StreamId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLedgerResponseTypeDef = TypedDict(
    "CreateLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": LedgerStateType,
        "CreationDateTime": datetime,
        "PermissionsMode": PermissionsModeType,
        "DeletionProtection": bool,
        "KmsKeyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportJournalToS3ResponseTypeDef = TypedDict(
    "ExportJournalToS3ResponseTypeDef",
    {
        "ExportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StreamJournalToKinesisResponseTypeDef = TypedDict(
    "StreamJournalToKinesisResponseTypeDef",
    {
        "StreamId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLedgerPermissionsModeResponseTypeDef = TypedDict(
    "UpdateLedgerPermissionsModeResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "PermissionsMode": PermissionsModeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLedgerResponseTypeDef = TypedDict(
    "DescribeLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": LedgerStateType,
        "CreationDateTime": datetime,
        "PermissionsMode": PermissionsModeType,
        "DeletionProtection": bool,
        "EncryptionDescription": LedgerEncryptionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLedgerResponseTypeDef = TypedDict(
    "UpdateLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": LedgerStateType,
        "CreationDateTime": datetime,
        "DeletionProtection": bool,
        "EncryptionDescription": LedgerEncryptionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetBlockRequestRequestTypeDef = TypedDict(
    "_RequiredGetBlockRequestRequestTypeDef",
    {
        "Name": str,
        "BlockAddress": ValueHolderTypeDef,
    },
)
_OptionalGetBlockRequestRequestTypeDef = TypedDict(
    "_OptionalGetBlockRequestRequestTypeDef",
    {
        "DigestTipAddress": ValueHolderTypeDef,
    },
    total=False,
)


class GetBlockRequestRequestTypeDef(
    _RequiredGetBlockRequestRequestTypeDef, _OptionalGetBlockRequestRequestTypeDef
):
    pass


GetBlockResponseTypeDef = TypedDict(
    "GetBlockResponseTypeDef",
    {
        "Block": ValueHolderTypeDef,
        "Proof": ValueHolderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDigestResponseTypeDef = TypedDict(
    "GetDigestResponseTypeDef",
    {
        "Digest": bytes,
        "DigestTipAddress": ValueHolderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetRevisionRequestRequestTypeDef = TypedDict(
    "_RequiredGetRevisionRequestRequestTypeDef",
    {
        "Name": str,
        "BlockAddress": ValueHolderTypeDef,
        "DocumentId": str,
    },
)
_OptionalGetRevisionRequestRequestTypeDef = TypedDict(
    "_OptionalGetRevisionRequestRequestTypeDef",
    {
        "DigestTipAddress": ValueHolderTypeDef,
    },
    total=False,
)


class GetRevisionRequestRequestTypeDef(
    _RequiredGetRevisionRequestRequestTypeDef, _OptionalGetRevisionRequestRequestTypeDef
):
    pass


GetRevisionResponseTypeDef = TypedDict(
    "GetRevisionResponseTypeDef",
    {
        "Proof": ValueHolderTypeDef,
        "Revision": ValueHolderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJournalKinesisStreamDescriptionTypeDef = TypedDict(
    "_RequiredJournalKinesisStreamDescriptionTypeDef",
    {
        "LedgerName": str,
        "RoleArn": str,
        "StreamId": str,
        "Status": StreamStatusType,
        "KinesisConfiguration": KinesisConfigurationTypeDef,
        "StreamName": str,
    },
)
_OptionalJournalKinesisStreamDescriptionTypeDef = TypedDict(
    "_OptionalJournalKinesisStreamDescriptionTypeDef",
    {
        "CreationTime": datetime,
        "InclusiveStartTime": datetime,
        "ExclusiveEndTime": datetime,
        "Arn": str,
        "ErrorCause": ErrorCauseType,
    },
    total=False,
)


class JournalKinesisStreamDescriptionTypeDef(
    _RequiredJournalKinesisStreamDescriptionTypeDef, _OptionalJournalKinesisStreamDescriptionTypeDef
):
    pass


_RequiredStreamJournalToKinesisRequestRequestTypeDef = TypedDict(
    "_RequiredStreamJournalToKinesisRequestRequestTypeDef",
    {
        "LedgerName": str,
        "RoleArn": str,
        "InclusiveStartTime": Union[datetime, str],
        "KinesisConfiguration": KinesisConfigurationTypeDef,
        "StreamName": str,
    },
)
_OptionalStreamJournalToKinesisRequestRequestTypeDef = TypedDict(
    "_OptionalStreamJournalToKinesisRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "ExclusiveEndTime": Union[datetime, str],
    },
    total=False,
)


class StreamJournalToKinesisRequestRequestTypeDef(
    _RequiredStreamJournalToKinesisRequestRequestTypeDef,
    _OptionalStreamJournalToKinesisRequestRequestTypeDef,
):
    pass


ListLedgersResponseTypeDef = TypedDict(
    "ListLedgersResponseTypeDef",
    {
        "Ledgers": List[LedgerSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3ExportConfigurationTypeDef = TypedDict(
    "S3ExportConfigurationTypeDef",
    {
        "Bucket": str,
        "Prefix": str,
        "EncryptionConfiguration": S3EncryptionConfigurationTypeDef,
    },
)

DescribeJournalKinesisStreamResponseTypeDef = TypedDict(
    "DescribeJournalKinesisStreamResponseTypeDef",
    {
        "Stream": JournalKinesisStreamDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJournalKinesisStreamsForLedgerResponseTypeDef = TypedDict(
    "ListJournalKinesisStreamsForLedgerResponseTypeDef",
    {
        "Streams": List[JournalKinesisStreamDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredExportJournalToS3RequestRequestTypeDef = TypedDict(
    "_RequiredExportJournalToS3RequestRequestTypeDef",
    {
        "Name": str,
        "InclusiveStartTime": Union[datetime, str],
        "ExclusiveEndTime": Union[datetime, str],
        "S3ExportConfiguration": S3ExportConfigurationTypeDef,
        "RoleArn": str,
    },
)
_OptionalExportJournalToS3RequestRequestTypeDef = TypedDict(
    "_OptionalExportJournalToS3RequestRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
    },
    total=False,
)


class ExportJournalToS3RequestRequestTypeDef(
    _RequiredExportJournalToS3RequestRequestTypeDef, _OptionalExportJournalToS3RequestRequestTypeDef
):
    pass


_RequiredJournalS3ExportDescriptionTypeDef = TypedDict(
    "_RequiredJournalS3ExportDescriptionTypeDef",
    {
        "LedgerName": str,
        "ExportId": str,
        "ExportCreationTime": datetime,
        "Status": ExportStatusType,
        "InclusiveStartTime": datetime,
        "ExclusiveEndTime": datetime,
        "S3ExportConfiguration": S3ExportConfigurationTypeDef,
        "RoleArn": str,
    },
)
_OptionalJournalS3ExportDescriptionTypeDef = TypedDict(
    "_OptionalJournalS3ExportDescriptionTypeDef",
    {
        "OutputFormat": OutputFormatType,
    },
    total=False,
)


class JournalS3ExportDescriptionTypeDef(
    _RequiredJournalS3ExportDescriptionTypeDef, _OptionalJournalS3ExportDescriptionTypeDef
):
    pass


DescribeJournalS3ExportResponseTypeDef = TypedDict(
    "DescribeJournalS3ExportResponseTypeDef",
    {
        "ExportDescription": JournalS3ExportDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJournalS3ExportsForLedgerResponseTypeDef = TypedDict(
    "ListJournalS3ExportsForLedgerResponseTypeDef",
    {
        "JournalS3Exports": List[JournalS3ExportDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJournalS3ExportsResponseTypeDef = TypedDict(
    "ListJournalS3ExportsResponseTypeDef",
    {
        "JournalS3Exports": List[JournalS3ExportDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
