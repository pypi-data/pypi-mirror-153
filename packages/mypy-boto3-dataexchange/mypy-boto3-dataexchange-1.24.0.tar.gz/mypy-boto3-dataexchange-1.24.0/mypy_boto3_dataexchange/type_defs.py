"""
Type annotations for dataexchange service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/type_defs/)

Usage::

    ```python
    from mypy_boto3_dataexchange.type_defs import ApiGatewayApiAssetTypeDef

    data: ApiGatewayApiAssetTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AssetTypeType,
    CodeType,
    JobErrorLimitNameType,
    JobErrorResourceTypesType,
    OriginType,
    ServerSideEncryptionTypesType,
    StateType,
    TypeType,
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
    "ApiGatewayApiAssetTypeDef",
    "AssetDestinationEntryTypeDef",
    "RedshiftDataShareAssetTypeDef",
    "S3SnapshotAssetTypeDef",
    "AssetSourceEntryTypeDef",
    "AutoExportRevisionDestinationEntryTypeDef",
    "ExportServerSideEncryptionTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "OriginDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "CreateRevisionRequestRequestTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteEventActionRequestRequestTypeDef",
    "DeleteRevisionRequestRequestTypeDef",
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef",
    "RevisionPublishedTypeDef",
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    "ExportAssetToSignedUrlResponseDetailsTypeDef",
    "RevisionDestinationEntryTypeDef",
    "GetAssetRequestRequestTypeDef",
    "GetDataSetRequestRequestTypeDef",
    "GetEventActionRequestRequestTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetRevisionRequestRequestTypeDef",
    "ImportAssetFromApiGatewayApiRequestDetailsTypeDef",
    "ImportAssetFromApiGatewayApiResponseDetailsTypeDef",
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    "ImportAssetFromSignedUrlResponseDetailsTypeDef",
    "RedshiftDataShareAssetSourceEntryTypeDef",
    "PaginatorConfigTypeDef",
    "ListDataSetRevisionsRequestRequestTypeDef",
    "RevisionEntryTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListEventActionsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListRevisionAssetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RevokeRevisionRequestRequestTypeDef",
    "SendApiAssetRequestRequestTypeDef",
    "StartJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "UpdateRevisionRequestRequestTypeDef",
    "AssetDetailsTypeDef",
    "ImportAssetsFromS3RequestDetailsTypeDef",
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    "AutoExportRevisionToS3RequestDetailsTypeDef",
    "ExportAssetsToS3RequestDetailsTypeDef",
    "ExportAssetsToS3ResponseDetailsTypeDef",
    "DataSetEntryTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateRevisionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDataSetResponseTypeDef",
    "GetRevisionResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RevokeRevisionResponseTypeDef",
    "SendApiAssetResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateRevisionResponseTypeDef",
    "DetailsTypeDef",
    "EventTypeDef",
    "ExportRevisionsToS3RequestDetailsTypeDef",
    "ExportRevisionsToS3ResponseDetailsTypeDef",
    "ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef",
    "ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef",
    "ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListEventActionsRequestListEventActionsPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef",
    "ListDataSetRevisionsResponseTypeDef",
    "AssetEntryTypeDef",
    "GetAssetResponseTypeDef",
    "UpdateAssetResponseTypeDef",
    "ActionTypeDef",
    "ListDataSetsResponseTypeDef",
    "JobErrorTypeDef",
    "RequestDetailsTypeDef",
    "ResponseDetailsTypeDef",
    "ListRevisionAssetsResponseTypeDef",
    "CreateEventActionRequestRequestTypeDef",
    "CreateEventActionResponseTypeDef",
    "EventActionEntryTypeDef",
    "GetEventActionResponseTypeDef",
    "UpdateEventActionRequestRequestTypeDef",
    "UpdateEventActionResponseTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "GetJobResponseTypeDef",
    "JobEntryTypeDef",
    "ListEventActionsResponseTypeDef",
    "ListJobsResponseTypeDef",
)

ApiGatewayApiAssetTypeDef = TypedDict(
    "ApiGatewayApiAssetTypeDef",
    {
        "ApiDescription": str,
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKey": str,
        "ApiName": str,
        "ApiSpecificationDownloadUrl": str,
        "ApiSpecificationDownloadUrlExpiresAt": datetime,
        "ProtocolType": Literal["REST"],
        "Stage": str,
    },
    total=False,
)

_RequiredAssetDestinationEntryTypeDef = TypedDict(
    "_RequiredAssetDestinationEntryTypeDef",
    {
        "AssetId": str,
        "Bucket": str,
    },
)
_OptionalAssetDestinationEntryTypeDef = TypedDict(
    "_OptionalAssetDestinationEntryTypeDef",
    {
        "Key": str,
    },
    total=False,
)


class AssetDestinationEntryTypeDef(
    _RequiredAssetDestinationEntryTypeDef, _OptionalAssetDestinationEntryTypeDef
):
    pass


RedshiftDataShareAssetTypeDef = TypedDict(
    "RedshiftDataShareAssetTypeDef",
    {
        "Arn": str,
    },
)

S3SnapshotAssetTypeDef = TypedDict(
    "S3SnapshotAssetTypeDef",
    {
        "Size": float,
    },
)

AssetSourceEntryTypeDef = TypedDict(
    "AssetSourceEntryTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

_RequiredAutoExportRevisionDestinationEntryTypeDef = TypedDict(
    "_RequiredAutoExportRevisionDestinationEntryTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalAutoExportRevisionDestinationEntryTypeDef = TypedDict(
    "_OptionalAutoExportRevisionDestinationEntryTypeDef",
    {
        "KeyPattern": str,
    },
    total=False,
)


class AutoExportRevisionDestinationEntryTypeDef(
    _RequiredAutoExportRevisionDestinationEntryTypeDef,
    _OptionalAutoExportRevisionDestinationEntryTypeDef,
):
    pass


_RequiredExportServerSideEncryptionTypeDef = TypedDict(
    "_RequiredExportServerSideEncryptionTypeDef",
    {
        "Type": ServerSideEncryptionTypesType,
    },
)
_OptionalExportServerSideEncryptionTypeDef = TypedDict(
    "_OptionalExportServerSideEncryptionTypeDef",
    {
        "KmsKeyArn": str,
    },
    total=False,
)


class ExportServerSideEncryptionTypeDef(
    _RequiredExportServerSideEncryptionTypeDef, _OptionalExportServerSideEncryptionTypeDef
):
    pass


CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

_RequiredCreateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSetRequestRequestTypeDef",
    {
        "AssetType": AssetTypeType,
        "Description": str,
        "Name": str,
    },
)
_OptionalCreateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSetRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateDataSetRequestRequestTypeDef(
    _RequiredCreateDataSetRequestRequestTypeDef, _OptionalCreateDataSetRequestRequestTypeDef
):
    pass


OriginDetailsTypeDef = TypedDict(
    "OriginDetailsTypeDef",
    {
        "ProductId": str,
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

_RequiredCreateRevisionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)
_OptionalCreateRevisionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRevisionRequestRequestTypeDef",
    {
        "Comment": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRevisionRequestRequestTypeDef(
    _RequiredCreateRevisionRequestRequestTypeDef, _OptionalCreateRevisionRequestRequestTypeDef
):
    pass


DeleteAssetRequestRequestTypeDef = TypedDict(
    "DeleteAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

DeleteDataSetRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)

DeleteEventActionRequestRequestTypeDef = TypedDict(
    "DeleteEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
    },
)

DeleteRevisionRequestRequestTypeDef = TypedDict(
    "DeleteRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetFromSignedUrlJobErrorDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef",
    {
        "AssetName": str,
    },
)

RevisionPublishedTypeDef = TypedDict(
    "RevisionPublishedTypeDef",
    {
        "DataSetId": str,
    },
)

ExportAssetToSignedUrlRequestDetailsTypeDef = TypedDict(
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

_RequiredExportAssetToSignedUrlResponseDetailsTypeDef = TypedDict(
    "_RequiredExportAssetToSignedUrlResponseDetailsTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalExportAssetToSignedUrlResponseDetailsTypeDef = TypedDict(
    "_OptionalExportAssetToSignedUrlResponseDetailsTypeDef",
    {
        "SignedUrl": str,
        "SignedUrlExpiresAt": datetime,
    },
    total=False,
)


class ExportAssetToSignedUrlResponseDetailsTypeDef(
    _RequiredExportAssetToSignedUrlResponseDetailsTypeDef,
    _OptionalExportAssetToSignedUrlResponseDetailsTypeDef,
):
    pass


_RequiredRevisionDestinationEntryTypeDef = TypedDict(
    "_RequiredRevisionDestinationEntryTypeDef",
    {
        "Bucket": str,
        "RevisionId": str,
    },
)
_OptionalRevisionDestinationEntryTypeDef = TypedDict(
    "_OptionalRevisionDestinationEntryTypeDef",
    {
        "KeyPattern": str,
    },
    total=False,
)


class RevisionDestinationEntryTypeDef(
    _RequiredRevisionDestinationEntryTypeDef, _OptionalRevisionDestinationEntryTypeDef
):
    pass


GetAssetRequestRequestTypeDef = TypedDict(
    "GetAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

GetDataSetRequestRequestTypeDef = TypedDict(
    "GetDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)

GetEventActionRequestRequestTypeDef = TypedDict(
    "GetEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetRevisionRequestRequestTypeDef = TypedDict(
    "GetRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)

_RequiredImportAssetFromApiGatewayApiRequestDetailsTypeDef = TypedDict(
    "_RequiredImportAssetFromApiGatewayApiRequestDetailsTypeDef",
    {
        "ApiId": str,
        "ApiName": str,
        "ApiSpecificationMd5Hash": str,
        "DataSetId": str,
        "ProtocolType": Literal["REST"],
        "RevisionId": str,
        "Stage": str,
    },
)
_OptionalImportAssetFromApiGatewayApiRequestDetailsTypeDef = TypedDict(
    "_OptionalImportAssetFromApiGatewayApiRequestDetailsTypeDef",
    {
        "ApiDescription": str,
        "ApiKey": str,
    },
    total=False,
)


class ImportAssetFromApiGatewayApiRequestDetailsTypeDef(
    _RequiredImportAssetFromApiGatewayApiRequestDetailsTypeDef,
    _OptionalImportAssetFromApiGatewayApiRequestDetailsTypeDef,
):
    pass


_RequiredImportAssetFromApiGatewayApiResponseDetailsTypeDef = TypedDict(
    "_RequiredImportAssetFromApiGatewayApiResponseDetailsTypeDef",
    {
        "ApiId": str,
        "ApiName": str,
        "ApiSpecificationMd5Hash": str,
        "ApiSpecificationUploadUrl": str,
        "ApiSpecificationUploadUrlExpiresAt": datetime,
        "DataSetId": str,
        "ProtocolType": Literal["REST"],
        "RevisionId": str,
        "Stage": str,
    },
)
_OptionalImportAssetFromApiGatewayApiResponseDetailsTypeDef = TypedDict(
    "_OptionalImportAssetFromApiGatewayApiResponseDetailsTypeDef",
    {
        "ApiDescription": str,
        "ApiKey": str,
    },
    total=False,
)


class ImportAssetFromApiGatewayApiResponseDetailsTypeDef(
    _RequiredImportAssetFromApiGatewayApiResponseDetailsTypeDef,
    _OptionalImportAssetFromApiGatewayApiResponseDetailsTypeDef,
):
    pass


ImportAssetFromSignedUrlRequestDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    {
        "AssetName": str,
        "DataSetId": str,
        "Md5Hash": str,
        "RevisionId": str,
    },
)

_RequiredImportAssetFromSignedUrlResponseDetailsTypeDef = TypedDict(
    "_RequiredImportAssetFromSignedUrlResponseDetailsTypeDef",
    {
        "AssetName": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalImportAssetFromSignedUrlResponseDetailsTypeDef = TypedDict(
    "_OptionalImportAssetFromSignedUrlResponseDetailsTypeDef",
    {
        "Md5Hash": str,
        "SignedUrl": str,
        "SignedUrlExpiresAt": datetime,
    },
    total=False,
)


class ImportAssetFromSignedUrlResponseDetailsTypeDef(
    _RequiredImportAssetFromSignedUrlResponseDetailsTypeDef,
    _OptionalImportAssetFromSignedUrlResponseDetailsTypeDef,
):
    pass


RedshiftDataShareAssetSourceEntryTypeDef = TypedDict(
    "RedshiftDataShareAssetSourceEntryTypeDef",
    {
        "DataShareArn": str,
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

_RequiredListDataSetRevisionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSetRevisionsRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)
_OptionalListDataSetRevisionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSetRevisionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListDataSetRevisionsRequestRequestTypeDef(
    _RequiredListDataSetRevisionsRequestRequestTypeDef,
    _OptionalListDataSetRevisionsRequestRequestTypeDef,
):
    pass


_RequiredRevisionEntryTypeDef = TypedDict(
    "_RequiredRevisionEntryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "UpdatedAt": datetime,
    },
)
_OptionalRevisionEntryTypeDef = TypedDict(
    "_OptionalRevisionEntryTypeDef",
    {
        "Comment": str,
        "Finalized": bool,
        "SourceId": str,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
    },
    total=False,
)


class RevisionEntryTypeDef(_RequiredRevisionEntryTypeDef, _OptionalRevisionEntryTypeDef):
    pass


ListDataSetsRequestRequestTypeDef = TypedDict(
    "ListDataSetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Origin": str,
    },
    total=False,
)

ListEventActionsRequestRequestTypeDef = TypedDict(
    "ListEventActionsRequestRequestTypeDef",
    {
        "EventSourceId": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "MaxResults": int,
        "NextToken": str,
        "RevisionId": str,
    },
    total=False,
)

_RequiredListRevisionAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredListRevisionAssetsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalListRevisionAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalListRevisionAssetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListRevisionAssetsRequestRequestTypeDef(
    _RequiredListRevisionAssetsRequestRequestTypeDef,
    _OptionalListRevisionAssetsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

RevokeRevisionRequestRequestTypeDef = TypedDict(
    "RevokeRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "RevocationComment": str,
    },
)

_RequiredSendApiAssetRequestRequestTypeDef = TypedDict(
    "_RequiredSendApiAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalSendApiAssetRequestRequestTypeDef = TypedDict(
    "_OptionalSendApiAssetRequestRequestTypeDef",
    {
        "Body": str,
        "QueryStringParameters": Mapping[str, str],
        "RequestHeaders": Mapping[str, str],
        "Method": str,
        "Path": str,
    },
    total=False,
)


class SendApiAssetRequestRequestTypeDef(
    _RequiredSendApiAssetRequestRequestTypeDef, _OptionalSendApiAssetRequestRequestTypeDef
):
    pass


StartJobRequestRequestTypeDef = TypedDict(
    "StartJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

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

UpdateAssetRequestRequestTypeDef = TypedDict(
    "UpdateAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "Name": str,
        "RevisionId": str,
    },
)

_RequiredUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)
_OptionalUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSetRequestRequestTypeDef",
    {
        "Description": str,
        "Name": str,
    },
    total=False,
)


class UpdateDataSetRequestRequestTypeDef(
    _RequiredUpdateDataSetRequestRequestTypeDef, _OptionalUpdateDataSetRequestRequestTypeDef
):
    pass


_RequiredUpdateRevisionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalUpdateRevisionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRevisionRequestRequestTypeDef",
    {
        "Comment": str,
        "Finalized": bool,
    },
    total=False,
)


class UpdateRevisionRequestRequestTypeDef(
    _RequiredUpdateRevisionRequestRequestTypeDef, _OptionalUpdateRevisionRequestRequestTypeDef
):
    pass


AssetDetailsTypeDef = TypedDict(
    "AssetDetailsTypeDef",
    {
        "S3SnapshotAsset": S3SnapshotAssetTypeDef,
        "RedshiftDataShareAsset": RedshiftDataShareAssetTypeDef,
        "ApiGatewayApiAsset": ApiGatewayApiAssetTypeDef,
    },
    total=False,
)

ImportAssetsFromS3RequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3RequestDetailsTypeDef",
    {
        "AssetSources": Sequence[AssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetsFromS3ResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    {
        "AssetSources": List[AssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

_RequiredAutoExportRevisionToS3RequestDetailsTypeDef = TypedDict(
    "_RequiredAutoExportRevisionToS3RequestDetailsTypeDef",
    {
        "RevisionDestination": AutoExportRevisionDestinationEntryTypeDef,
    },
)
_OptionalAutoExportRevisionToS3RequestDetailsTypeDef = TypedDict(
    "_OptionalAutoExportRevisionToS3RequestDetailsTypeDef",
    {
        "Encryption": ExportServerSideEncryptionTypeDef,
    },
    total=False,
)


class AutoExportRevisionToS3RequestDetailsTypeDef(
    _RequiredAutoExportRevisionToS3RequestDetailsTypeDef,
    _OptionalAutoExportRevisionToS3RequestDetailsTypeDef,
):
    pass


_RequiredExportAssetsToS3RequestDetailsTypeDef = TypedDict(
    "_RequiredExportAssetsToS3RequestDetailsTypeDef",
    {
        "AssetDestinations": Sequence[AssetDestinationEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalExportAssetsToS3RequestDetailsTypeDef = TypedDict(
    "_OptionalExportAssetsToS3RequestDetailsTypeDef",
    {
        "Encryption": ExportServerSideEncryptionTypeDef,
    },
    total=False,
)


class ExportAssetsToS3RequestDetailsTypeDef(
    _RequiredExportAssetsToS3RequestDetailsTypeDef, _OptionalExportAssetsToS3RequestDetailsTypeDef
):
    pass


_RequiredExportAssetsToS3ResponseDetailsTypeDef = TypedDict(
    "_RequiredExportAssetsToS3ResponseDetailsTypeDef",
    {
        "AssetDestinations": List[AssetDestinationEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalExportAssetsToS3ResponseDetailsTypeDef = TypedDict(
    "_OptionalExportAssetsToS3ResponseDetailsTypeDef",
    {
        "Encryption": ExportServerSideEncryptionTypeDef,
    },
    total=False,
)


class ExportAssetsToS3ResponseDetailsTypeDef(
    _RequiredExportAssetsToS3ResponseDetailsTypeDef, _OptionalExportAssetsToS3ResponseDetailsTypeDef
):
    pass


_RequiredDataSetEntryTypeDef = TypedDict(
    "_RequiredDataSetEntryTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "UpdatedAt": datetime,
    },
)
_OptionalDataSetEntryTypeDef = TypedDict(
    "_OptionalDataSetEntryTypeDef",
    {
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
    },
    total=False,
)


class DataSetEntryTypeDef(_RequiredDataSetEntryTypeDef, _OptionalDataSetEntryTypeDef):
    pass


CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRevisionResponseTypeDef = TypedDict(
    "CreateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataSetResponseTypeDef = TypedDict(
    "GetDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRevisionResponseTypeDef = TypedDict(
    "GetRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
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

RevokeRevisionResponseTypeDef = TypedDict(
    "RevokeRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendApiAssetResponseTypeDef = TypedDict(
    "SendApiAssetResponseTypeDef",
    {
        "Body": str,
        "ResponseHeaders": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRevisionResponseTypeDef = TypedDict(
    "UpdateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetailsTypeDef = TypedDict(
    "DetailsTypeDef",
    {
        "ImportAssetFromSignedUrlJobErrorDetails": ImportAssetFromSignedUrlJobErrorDetailsTypeDef,
        "ImportAssetsFromS3JobErrorDetails": List[AssetSourceEntryTypeDef],
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "RevisionPublished": RevisionPublishedTypeDef,
    },
    total=False,
)

_RequiredExportRevisionsToS3RequestDetailsTypeDef = TypedDict(
    "_RequiredExportRevisionsToS3RequestDetailsTypeDef",
    {
        "DataSetId": str,
        "RevisionDestinations": Sequence[RevisionDestinationEntryTypeDef],
    },
)
_OptionalExportRevisionsToS3RequestDetailsTypeDef = TypedDict(
    "_OptionalExportRevisionsToS3RequestDetailsTypeDef",
    {
        "Encryption": ExportServerSideEncryptionTypeDef,
    },
    total=False,
)


class ExportRevisionsToS3RequestDetailsTypeDef(
    _RequiredExportRevisionsToS3RequestDetailsTypeDef,
    _OptionalExportRevisionsToS3RequestDetailsTypeDef,
):
    pass


_RequiredExportRevisionsToS3ResponseDetailsTypeDef = TypedDict(
    "_RequiredExportRevisionsToS3ResponseDetailsTypeDef",
    {
        "DataSetId": str,
        "RevisionDestinations": List[RevisionDestinationEntryTypeDef],
    },
)
_OptionalExportRevisionsToS3ResponseDetailsTypeDef = TypedDict(
    "_OptionalExportRevisionsToS3ResponseDetailsTypeDef",
    {
        "Encryption": ExportServerSideEncryptionTypeDef,
        "EventActionArn": str,
    },
    total=False,
)


class ExportRevisionsToS3ResponseDetailsTypeDef(
    _RequiredExportRevisionsToS3ResponseDetailsTypeDef,
    _OptionalExportRevisionsToS3ResponseDetailsTypeDef,
):
    pass


ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef",
    {
        "AssetSources": Sequence[RedshiftDataShareAssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef",
    {
        "AssetSources": List[RedshiftDataShareAssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

_RequiredListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef = TypedDict(
    "_RequiredListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef",
    {
        "DataSetId": str,
    },
)
_OptionalListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef = TypedDict(
    "_OptionalListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef(
    _RequiredListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef,
    _OptionalListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef,
):
    pass


ListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "Origin": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEventActionsRequestListEventActionsPaginateTypeDef = TypedDict(
    "ListEventActionsRequestListEventActionsPaginateTypeDef",
    {
        "EventSourceId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef = TypedDict(
    "_RequiredListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)
_OptionalListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef = TypedDict(
    "_OptionalListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef(
    _RequiredListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef,
    _OptionalListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef,
):
    pass


ListDataSetRevisionsResponseTypeDef = TypedDict(
    "ListDataSetRevisionsResponseTypeDef",
    {
        "NextToken": str,
        "Revisions": List[RevisionEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetEntryTypeDef = TypedDict(
    "_RequiredAssetEntryTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "UpdatedAt": datetime,
    },
)
_OptionalAssetEntryTypeDef = TypedDict(
    "_OptionalAssetEntryTypeDef",
    {
        "SourceId": str,
    },
    total=False,
)


class AssetEntryTypeDef(_RequiredAssetEntryTypeDef, _OptionalAssetEntryTypeDef):
    pass


GetAssetResponseTypeDef = TypedDict(
    "GetAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ExportRevisionToS3": AutoExportRevisionToS3RequestDetailsTypeDef,
    },
    total=False,
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSets": List[DataSetEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJobErrorTypeDef = TypedDict(
    "_RequiredJobErrorTypeDef",
    {
        "Code": CodeType,
        "Message": str,
    },
)
_OptionalJobErrorTypeDef = TypedDict(
    "_OptionalJobErrorTypeDef",
    {
        "Details": DetailsTypeDef,
        "LimitName": JobErrorLimitNameType,
        "LimitValue": float,
        "ResourceId": str,
        "ResourceType": JobErrorResourceTypesType,
    },
    total=False,
)


class JobErrorTypeDef(_RequiredJobErrorTypeDef, _OptionalJobErrorTypeDef):
    pass


RequestDetailsTypeDef = TypedDict(
    "RequestDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": ExportAssetToSignedUrlRequestDetailsTypeDef,
        "ExportAssetsToS3": ExportAssetsToS3RequestDetailsTypeDef,
        "ExportRevisionsToS3": ExportRevisionsToS3RequestDetailsTypeDef,
        "ImportAssetFromSignedUrl": ImportAssetFromSignedUrlRequestDetailsTypeDef,
        "ImportAssetsFromS3": ImportAssetsFromS3RequestDetailsTypeDef,
        "ImportAssetsFromRedshiftDataShares": ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef,
        "ImportAssetFromApiGatewayApi": ImportAssetFromApiGatewayApiRequestDetailsTypeDef,
    },
    total=False,
)

ResponseDetailsTypeDef = TypedDict(
    "ResponseDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": ExportAssetToSignedUrlResponseDetailsTypeDef,
        "ExportAssetsToS3": ExportAssetsToS3ResponseDetailsTypeDef,
        "ExportRevisionsToS3": ExportRevisionsToS3ResponseDetailsTypeDef,
        "ImportAssetFromSignedUrl": ImportAssetFromSignedUrlResponseDetailsTypeDef,
        "ImportAssetsFromS3": ImportAssetsFromS3ResponseDetailsTypeDef,
        "ImportAssetsFromRedshiftDataShares": ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef,
        "ImportAssetFromApiGatewayApi": ImportAssetFromApiGatewayApiResponseDetailsTypeDef,
    },
    total=False,
)

ListRevisionAssetsResponseTypeDef = TypedDict(
    "ListRevisionAssetsResponseTypeDef",
    {
        "Assets": List[AssetEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEventActionRequestRequestTypeDef = TypedDict(
    "CreateEventActionRequestRequestTypeDef",
    {
        "Action": ActionTypeDef,
        "Event": EventTypeDef,
    },
)

CreateEventActionResponseTypeDef = TypedDict(
    "CreateEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventActionEntryTypeDef = TypedDict(
    "EventActionEntryTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
    },
)

GetEventActionResponseTypeDef = TypedDict(
    "GetEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateEventActionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
    },
)
_OptionalUpdateEventActionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEventActionRequestRequestTypeDef",
    {
        "Action": ActionTypeDef,
    },
    total=False,
)


class UpdateEventActionRequestRequestTypeDef(
    _RequiredUpdateEventActionRequestRequestTypeDef, _OptionalUpdateEventActionRequestRequestTypeDef
):
    pass


UpdateEventActionResponseTypeDef = TypedDict(
    "UpdateEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "Details": RequestDetailsTypeDef,
        "Type": TypeType,
    },
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJobEntryTypeDef = TypedDict(
    "_RequiredJobEntryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
    },
)
_OptionalJobEntryTypeDef = TypedDict(
    "_OptionalJobEntryTypeDef",
    {
        "Errors": List[JobErrorTypeDef],
    },
    total=False,
)


class JobEntryTypeDef(_RequiredJobEntryTypeDef, _OptionalJobEntryTypeDef):
    pass


ListEventActionsResponseTypeDef = TypedDict(
    "ListEventActionsResponseTypeDef",
    {
        "EventActions": List[EventActionEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "Jobs": List[JobEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
