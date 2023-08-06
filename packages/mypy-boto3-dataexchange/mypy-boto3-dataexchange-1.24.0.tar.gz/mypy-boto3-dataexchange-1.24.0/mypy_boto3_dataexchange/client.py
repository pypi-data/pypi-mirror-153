"""
Type annotations for dataexchange service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dataexchange.client import DataExchangeClient

    session = Session()
    client: DataExchangeClient = session.client("dataexchange")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import AssetTypeType, TypeType
from .paginator import (
    ListDataSetRevisionsPaginator,
    ListDataSetsPaginator,
    ListEventActionsPaginator,
    ListJobsPaginator,
    ListRevisionAssetsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    CreateDataSetResponseTypeDef,
    CreateEventActionResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateRevisionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EventTypeDef,
    GetAssetResponseTypeDef,
    GetDataSetResponseTypeDef,
    GetEventActionResponseTypeDef,
    GetJobResponseTypeDef,
    GetRevisionResponseTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListRevisionAssetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RequestDetailsTypeDef,
    RevokeRevisionResponseTypeDef,
    SendApiAssetResponseTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateEventActionResponseTypeDef,
    UpdateRevisionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DataExchangeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DataExchangeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataExchangeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#can_paginate)
        """

    def cancel_job(self, *, JobId: str) -> EmptyResponseMetadataTypeDef:
        """
        This operation cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.cancel_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#cancel_job)
        """

    def create_data_set(
        self,
        *,
        AssetType: AssetTypeType,
        Description: str,
        Name: str,
        Tags: Mapping[str, str] = ...
    ) -> CreateDataSetResponseTypeDef:
        """
        This operation creates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#create_data_set)
        """

    def create_event_action(
        self, *, Action: ActionTypeDef, Event: EventTypeDef
    ) -> CreateEventActionResponseTypeDef:
        """
        This operation creates an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_event_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#create_event_action)
        """

    def create_job(
        self, *, Details: RequestDetailsTypeDef, Type: TypeType
    ) -> CreateJobResponseTypeDef:
        """
        This operation creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#create_job)
        """

    def create_revision(
        self, *, DataSetId: str, Comment: str = ..., Tags: Mapping[str, str] = ...
    ) -> CreateRevisionResponseTypeDef:
        """
        This operation creates a revision for a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#create_revision)
        """

    def delete_asset(
        self, *, AssetId: str, DataSetId: str, RevisionId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_asset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#delete_asset)
        """

    def delete_data_set(self, *, DataSetId: str) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#delete_data_set)
        """

    def delete_event_action(self, *, EventActionId: str) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_event_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#delete_event_action)
        """

    def delete_revision(self, *, DataSetId: str, RevisionId: str) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#delete_revision)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#generate_presigned_url)
        """

    def get_asset(
        self, *, AssetId: str, DataSetId: str, RevisionId: str
    ) -> GetAssetResponseTypeDef:
        """
        This operation returns information about an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_asset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_asset)
        """

    def get_data_set(self, *, DataSetId: str) -> GetDataSetResponseTypeDef:
        """
        This operation returns information about a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_data_set)
        """

    def get_event_action(self, *, EventActionId: str) -> GetEventActionResponseTypeDef:
        """
        This operation retrieves information about an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_event_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_event_action)
        """

    def get_job(self, *, JobId: str) -> GetJobResponseTypeDef:
        """
        This operation returns information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_job)
        """

    def get_revision(self, *, DataSetId: str, RevisionId: str) -> GetRevisionResponseTypeDef:
        """
        This operation returns information about a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_revision)
        """

    def list_data_set_revisions(
        self, *, DataSetId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDataSetRevisionsResponseTypeDef:
        """
        This operation lists a data set's revisions sorted by CreatedAt in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_data_set_revisions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_data_set_revisions)
        """

    def list_data_sets(
        self, *, MaxResults: int = ..., NextToken: str = ..., Origin: str = ...
    ) -> ListDataSetsResponseTypeDef:
        """
        This operation lists your data sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_data_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_data_sets)
        """

    def list_event_actions(
        self, *, EventSourceId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListEventActionsResponseTypeDef:
        """
        This operation lists your event actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_event_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_event_actions)
        """

    def list_jobs(
        self,
        *,
        DataSetId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        RevisionId: str = ...
    ) -> ListJobsResponseTypeDef:
        """
        This operation lists your jobs sorted by CreatedAt in descending order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_jobs)
        """

    def list_revision_assets(
        self, *, DataSetId: str, RevisionId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRevisionAssetsResponseTypeDef:
        """
        This operation lists a revision's assets sorted alphabetically in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_revision_assets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_revision_assets)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        This operation lists the tags on the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#list_tags_for_resource)
        """

    def revoke_revision(
        self, *, DataSetId: str, RevisionId: str, RevocationComment: str
    ) -> RevokeRevisionResponseTypeDef:
        """
        This operation revokes subscribers' access to a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.revoke_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#revoke_revision)
        """

    def send_api_asset(
        self,
        *,
        AssetId: str,
        DataSetId: str,
        RevisionId: str,
        Body: str = ...,
        QueryStringParameters: Mapping[str, str] = ...,
        RequestHeaders: Mapping[str, str] = ...,
        Method: str = ...,
        Path: str = ...
    ) -> SendApiAssetResponseTypeDef:
        """
        This operation invokes an API Gateway API asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.send_api_asset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#send_api_asset)
        """

    def start_job(self, *, JobId: str) -> Dict[str, Any]:
        """
        This operation starts a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.start_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#start_job)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#untag_resource)
        """

    def update_asset(
        self, *, AssetId: str, DataSetId: str, Name: str, RevisionId: str
    ) -> UpdateAssetResponseTypeDef:
        """
        This operation updates an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_asset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#update_asset)
        """

    def update_data_set(
        self, *, DataSetId: str, Description: str = ..., Name: str = ...
    ) -> UpdateDataSetResponseTypeDef:
        """
        This operation updates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#update_data_set)
        """

    def update_event_action(
        self, *, EventActionId: str, Action: ActionTypeDef = ...
    ) -> UpdateEventActionResponseTypeDef:
        """
        This operation updates the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_event_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#update_event_action)
        """

    def update_revision(
        self, *, DataSetId: str, RevisionId: str, Comment: str = ..., Finalized: bool = ...
    ) -> UpdateRevisionResponseTypeDef:
        """
        This operation updates a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#update_revision)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_set_revisions"]
    ) -> ListDataSetRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_sets"]) -> ListDataSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_actions"]
    ) -> ListEventActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_revision_assets"]
    ) -> ListRevisionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client/#get_paginator)
        """
