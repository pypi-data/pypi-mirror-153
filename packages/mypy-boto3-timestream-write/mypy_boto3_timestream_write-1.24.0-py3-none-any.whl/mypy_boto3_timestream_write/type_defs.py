"""
Type annotations for timestream-write service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_write/type_defs/)

Usage::

    ```python
    from mypy_boto3_timestream_write.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import MeasureValueTypeType, S3EncryptionOptionType, TableStatusType, TimeUnitType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TagTypeDef",
    "DatabaseTypeDef",
    "ResponseMetadataTypeDef",
    "RetentionPropertiesTypeDef",
    "DeleteDatabaseRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "DescribeDatabaseRequestRequestTypeDef",
    "EndpointTypeDef",
    "DescribeTableRequestRequestTypeDef",
    "DimensionTypeDef",
    "ListDatabasesRequestRequestTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "S3ConfigurationTypeDef",
    "MeasureValueTypeDef",
    "RecordsIngestedTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatabaseRequestRequestTypeDef",
    "CreateDatabaseRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateDatabaseResponseTypeDef",
    "DescribeDatabaseResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListDatabasesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateDatabaseResponseTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "MagneticStoreRejectedDataLocationTypeDef",
    "RecordTypeDef",
    "WriteRecordsResponseTypeDef",
    "MagneticStoreWritePropertiesTypeDef",
    "WriteRecordsRequestRequestTypeDef",
    "CreateTableRequestRequestTypeDef",
    "TableTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "CreateTableResponseTypeDef",
    "DescribeTableResponseTypeDef",
    "ListTablesResponseTypeDef",
    "UpdateTableResponseTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DatabaseTypeDef = TypedDict(
    "DatabaseTypeDef",
    {
        "Arn": str,
        "DatabaseName": str,
        "TableCount": int,
        "KmsKeyId": str,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
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

RetentionPropertiesTypeDef = TypedDict(
    "RetentionPropertiesTypeDef",
    {
        "MemoryStoreRetentionPeriodInHours": int,
        "MagneticStoreRetentionPeriodInDays": int,
    },
)

DeleteDatabaseRequestRequestTypeDef = TypedDict(
    "DeleteDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)

DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)

DescribeDatabaseRequestRequestTypeDef = TypedDict(
    "DescribeDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "CachePeriodInMinutes": int,
    },
)

DescribeTableRequestRequestTypeDef = TypedDict(
    "DescribeTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)

_RequiredDimensionTypeDef = TypedDict(
    "_RequiredDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalDimensionTypeDef = TypedDict(
    "_OptionalDimensionTypeDef",
    {
        "DimensionValueType": Literal["VARCHAR"],
    },
    total=False,
)


class DimensionTypeDef(_RequiredDimensionTypeDef, _OptionalDimensionTypeDef):
    pass


ListDatabasesRequestRequestTypeDef = TypedDict(
    "ListDatabasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTablesRequestRequestTypeDef = TypedDict(
    "ListTablesRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

S3ConfigurationTypeDef = TypedDict(
    "S3ConfigurationTypeDef",
    {
        "BucketName": str,
        "ObjectKeyPrefix": str,
        "EncryptionOption": S3EncryptionOptionType,
        "KmsKeyId": str,
    },
    total=False,
)

MeasureValueTypeDef = TypedDict(
    "MeasureValueTypeDef",
    {
        "Name": str,
        "Value": str,
        "Type": MeasureValueTypeType,
    },
)

RecordsIngestedTypeDef = TypedDict(
    "RecordsIngestedTypeDef",
    {
        "Total": int,
        "MemoryStore": int,
        "MagneticStore": int,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateDatabaseRequestRequestTypeDef = TypedDict(
    "UpdateDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "KmsKeyId": str,
    },
)

_RequiredCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatabaseRequestRequestTypeDef",
    {
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDatabaseRequestRequestTypeDef(
    _RequiredCreateDatabaseRequestRequestTypeDef, _OptionalCreateDatabaseRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateDatabaseResponseTypeDef = TypedDict(
    "CreateDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatabaseResponseTypeDef = TypedDict(
    "DescribeDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatabasesResponseTypeDef = TypedDict(
    "ListDatabasesResponseTypeDef",
    {
        "Databases": List[DatabaseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDatabaseResponseTypeDef = TypedDict(
    "UpdateDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MagneticStoreRejectedDataLocationTypeDef = TypedDict(
    "MagneticStoreRejectedDataLocationTypeDef",
    {
        "S3Configuration": S3ConfigurationTypeDef,
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "MeasureName": str,
        "MeasureValue": str,
        "MeasureValueType": MeasureValueTypeType,
        "Time": str,
        "TimeUnit": TimeUnitType,
        "Version": int,
        "MeasureValues": Sequence[MeasureValueTypeDef],
    },
    total=False,
)

WriteRecordsResponseTypeDef = TypedDict(
    "WriteRecordsResponseTypeDef",
    {
        "RecordsIngested": RecordsIngestedTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMagneticStoreWritePropertiesTypeDef = TypedDict(
    "_RequiredMagneticStoreWritePropertiesTypeDef",
    {
        "EnableMagneticStoreWrites": bool,
    },
)
_OptionalMagneticStoreWritePropertiesTypeDef = TypedDict(
    "_OptionalMagneticStoreWritePropertiesTypeDef",
    {
        "MagneticStoreRejectedDataLocation": MagneticStoreRejectedDataLocationTypeDef,
    },
    total=False,
)


class MagneticStoreWritePropertiesTypeDef(
    _RequiredMagneticStoreWritePropertiesTypeDef, _OptionalMagneticStoreWritePropertiesTypeDef
):
    pass


_RequiredWriteRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredWriteRecordsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "Records": Sequence[RecordTypeDef],
    },
)
_OptionalWriteRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalWriteRecordsRequestRequestTypeDef",
    {
        "CommonAttributes": RecordTypeDef,
    },
    total=False,
)


class WriteRecordsRequestRequestTypeDef(
    _RequiredWriteRecordsRequestRequestTypeDef, _OptionalWriteRecordsRequestRequestTypeDef
):
    pass


_RequiredCreateTableRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalCreateTableRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTableRequestRequestTypeDef",
    {
        "RetentionProperties": RetentionPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
    },
    total=False,
)


class CreateTableRequestRequestTypeDef(
    _RequiredCreateTableRequestRequestTypeDef, _OptionalCreateTableRequestRequestTypeDef
):
    pass


TableTypeDef = TypedDict(
    "TableTypeDef",
    {
        "Arn": str,
        "TableName": str,
        "DatabaseName": str,
        "TableStatus": TableStatusType,
        "RetentionProperties": RetentionPropertiesTypeDef,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
    },
    total=False,
)

_RequiredUpdateTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalUpdateTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableRequestRequestTypeDef",
    {
        "RetentionProperties": RetentionPropertiesTypeDef,
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
    },
    total=False,
)


class UpdateTableRequestRequestTypeDef(
    _RequiredUpdateTableRequestRequestTypeDef, _OptionalUpdateTableRequestRequestTypeDef
):
    pass


CreateTableResponseTypeDef = TypedDict(
    "CreateTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTableResponseTypeDef = TypedDict(
    "DescribeTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "Tables": List[TableTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTableResponseTypeDef = TypedDict(
    "UpdateTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
