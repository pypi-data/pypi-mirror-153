"""
Type annotations for cognito-sync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_sync/type_defs/)

Usage::

    ```python
    from mypy_boto3_cognito_sync.type_defs import BulkPublishRequestRequestTypeDef

    data: BulkPublishRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import BulkPublishStatusType, OperationType, PlatformType, StreamingStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BulkPublishRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CognitoStreamsTypeDef",
    "DatasetTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeIdentityPoolUsageRequestRequestTypeDef",
    "IdentityPoolUsageTypeDef",
    "DescribeIdentityUsageRequestRequestTypeDef",
    "IdentityUsageTypeDef",
    "GetBulkPublishDetailsRequestRequestTypeDef",
    "GetCognitoEventsRequestRequestTypeDef",
    "GetIdentityPoolConfigurationRequestRequestTypeDef",
    "PushSyncTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListIdentityPoolUsageRequestRequestTypeDef",
    "ListRecordsRequestRequestTypeDef",
    "RecordTypeDef",
    "RecordPatchTypeDef",
    "RegisterDeviceRequestRequestTypeDef",
    "SetCognitoEventsRequestRequestTypeDef",
    "SubscribeToDatasetRequestRequestTypeDef",
    "UnsubscribeFromDatasetRequestRequestTypeDef",
    "BulkPublishResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetBulkPublishDetailsResponseTypeDef",
    "GetCognitoEventsResponseTypeDef",
    "RegisterDeviceResponseTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DescribeDatasetResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "DescribeIdentityPoolUsageResponseTypeDef",
    "ListIdentityPoolUsageResponseTypeDef",
    "DescribeIdentityUsageResponseTypeDef",
    "GetIdentityPoolConfigurationResponseTypeDef",
    "SetIdentityPoolConfigurationRequestRequestTypeDef",
    "SetIdentityPoolConfigurationResponseTypeDef",
    "ListRecordsResponseTypeDef",
    "UpdateRecordsResponseTypeDef",
    "UpdateRecordsRequestRequestTypeDef",
)

BulkPublishRequestRequestTypeDef = TypedDict(
    "BulkPublishRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
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

CognitoStreamsTypeDef = TypedDict(
    "CognitoStreamsTypeDef",
    {
        "StreamName": str,
        "RoleArn": str,
        "StreamingStatus": StreamingStatusType,
    },
    total=False,
)

DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "IdentityId": str,
        "DatasetName": str,
        "CreationDate": datetime,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "DataStorage": int,
        "NumRecords": int,
    },
    total=False,
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
    },
)

DescribeIdentityPoolUsageRequestRequestTypeDef = TypedDict(
    "DescribeIdentityPoolUsageRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
)

IdentityPoolUsageTypeDef = TypedDict(
    "IdentityPoolUsageTypeDef",
    {
        "IdentityPoolId": str,
        "SyncSessionsCount": int,
        "DataStorage": int,
        "LastModifiedDate": datetime,
    },
    total=False,
)

DescribeIdentityUsageRequestRequestTypeDef = TypedDict(
    "DescribeIdentityUsageRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
    },
)

IdentityUsageTypeDef = TypedDict(
    "IdentityUsageTypeDef",
    {
        "IdentityId": str,
        "IdentityPoolId": str,
        "LastModifiedDate": datetime,
        "DatasetCount": int,
        "DataStorage": int,
    },
    total=False,
)

GetBulkPublishDetailsRequestRequestTypeDef = TypedDict(
    "GetBulkPublishDetailsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
)

GetCognitoEventsRequestRequestTypeDef = TypedDict(
    "GetCognitoEventsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
)

GetIdentityPoolConfigurationRequestRequestTypeDef = TypedDict(
    "GetIdentityPoolConfigurationRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
)

PushSyncTypeDef = TypedDict(
    "PushSyncTypeDef",
    {
        "ApplicationArns": List[str],
        "RoleArn": str,
    },
    total=False,
)

_RequiredListDatasetsRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
    },
)
_OptionalListDatasetsRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatasetsRequestRequestTypeDef(
    _RequiredListDatasetsRequestRequestTypeDef, _OptionalListDatasetsRequestRequestTypeDef
):
    pass


ListIdentityPoolUsageRequestRequestTypeDef = TypedDict(
    "ListIdentityPoolUsageRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredListRecordsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
    },
)
_OptionalListRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalListRecordsRequestRequestTypeDef",
    {
        "LastSyncCount": int,
        "NextToken": str,
        "MaxResults": int,
        "SyncSessionToken": str,
    },
    total=False,
)


class ListRecordsRequestRequestTypeDef(
    _RequiredListRecordsRequestRequestTypeDef, _OptionalListRecordsRequestRequestTypeDef
):
    pass


RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "Key": str,
        "Value": str,
        "SyncCount": int,
        "LastModifiedDate": datetime,
        "LastModifiedBy": str,
        "DeviceLastModifiedDate": datetime,
    },
    total=False,
)

_RequiredRecordPatchTypeDef = TypedDict(
    "_RequiredRecordPatchTypeDef",
    {
        "Op": OperationType,
        "Key": str,
        "SyncCount": int,
    },
)
_OptionalRecordPatchTypeDef = TypedDict(
    "_OptionalRecordPatchTypeDef",
    {
        "Value": str,
        "DeviceLastModifiedDate": Union[datetime, str],
    },
    total=False,
)


class RecordPatchTypeDef(_RequiredRecordPatchTypeDef, _OptionalRecordPatchTypeDef):
    pass


RegisterDeviceRequestRequestTypeDef = TypedDict(
    "RegisterDeviceRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "Platform": PlatformType,
        "Token": str,
    },
)

SetCognitoEventsRequestRequestTypeDef = TypedDict(
    "SetCognitoEventsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "Events": Mapping[str, str],
    },
)

SubscribeToDatasetRequestRequestTypeDef = TypedDict(
    "SubscribeToDatasetRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
        "DeviceId": str,
    },
)

UnsubscribeFromDatasetRequestRequestTypeDef = TypedDict(
    "UnsubscribeFromDatasetRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
        "DeviceId": str,
    },
)

BulkPublishResponseTypeDef = TypedDict(
    "BulkPublishResponseTypeDef",
    {
        "IdentityPoolId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBulkPublishDetailsResponseTypeDef = TypedDict(
    "GetBulkPublishDetailsResponseTypeDef",
    {
        "IdentityPoolId": str,
        "BulkPublishStartTime": datetime,
        "BulkPublishCompleteTime": datetime,
        "BulkPublishStatus": BulkPublishStatusType,
        "FailureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCognitoEventsResponseTypeDef = TypedDict(
    "GetCognitoEventsResponseTypeDef",
    {
        "Events": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterDeviceResponseTypeDef = TypedDict(
    "RegisterDeviceResponseTypeDef",
    {
        "DeviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDatasetResponseTypeDef = TypedDict(
    "DeleteDatasetResponseTypeDef",
    {
        "Dataset": DatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "Dataset": DatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "Datasets": List[DatasetTypeDef],
        "Count": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIdentityPoolUsageResponseTypeDef = TypedDict(
    "DescribeIdentityPoolUsageResponseTypeDef",
    {
        "IdentityPoolUsage": IdentityPoolUsageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIdentityPoolUsageResponseTypeDef = TypedDict(
    "ListIdentityPoolUsageResponseTypeDef",
    {
        "IdentityPoolUsages": List[IdentityPoolUsageTypeDef],
        "MaxResults": int,
        "Count": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIdentityUsageResponseTypeDef = TypedDict(
    "DescribeIdentityUsageResponseTypeDef",
    {
        "IdentityUsage": IdentityUsageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIdentityPoolConfigurationResponseTypeDef = TypedDict(
    "GetIdentityPoolConfigurationResponseTypeDef",
    {
        "IdentityPoolId": str,
        "PushSync": PushSyncTypeDef,
        "CognitoStreams": CognitoStreamsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSetIdentityPoolConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredSetIdentityPoolConfigurationRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
)
_OptionalSetIdentityPoolConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalSetIdentityPoolConfigurationRequestRequestTypeDef",
    {
        "PushSync": PushSyncTypeDef,
        "CognitoStreams": CognitoStreamsTypeDef,
    },
    total=False,
)


class SetIdentityPoolConfigurationRequestRequestTypeDef(
    _RequiredSetIdentityPoolConfigurationRequestRequestTypeDef,
    _OptionalSetIdentityPoolConfigurationRequestRequestTypeDef,
):
    pass


SetIdentityPoolConfigurationResponseTypeDef = TypedDict(
    "SetIdentityPoolConfigurationResponseTypeDef",
    {
        "IdentityPoolId": str,
        "PushSync": PushSyncTypeDef,
        "CognitoStreams": CognitoStreamsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecordsResponseTypeDef = TypedDict(
    "ListRecordsResponseTypeDef",
    {
        "Records": List[RecordTypeDef],
        "NextToken": str,
        "Count": int,
        "DatasetSyncCount": int,
        "LastModifiedBy": str,
        "MergedDatasetNames": List[str],
        "DatasetExists": bool,
        "DatasetDeletedAfterRequestedSyncCount": bool,
        "SyncSessionToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRecordsResponseTypeDef = TypedDict(
    "UpdateRecordsResponseTypeDef",
    {
        "Records": List[RecordTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRecordsRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
        "IdentityId": str,
        "DatasetName": str,
        "SyncSessionToken": str,
    },
)
_OptionalUpdateRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRecordsRequestRequestTypeDef",
    {
        "DeviceId": str,
        "RecordPatches": Sequence[RecordPatchTypeDef],
        "ClientContext": str,
    },
    total=False,
)


class UpdateRecordsRequestRequestTypeDef(
    _RequiredUpdateRecordsRequestRequestTypeDef, _OptionalUpdateRecordsRequestRequestTypeDef
):
    pass
