"""
Type annotations for keyspaces service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_keyspaces.client import KeyspacesClient

    session = Session()
    client: KeyspacesClient = session.client("keyspaces")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListKeyspacesPaginator, ListTablesPaginator, ListTagsForResourcePaginator
from .type_defs import (
    CapacitySpecificationTypeDef,
    ColumnDefinitionTypeDef,
    CommentTypeDef,
    CreateKeyspaceResponseTypeDef,
    CreateTableResponseTypeDef,
    EncryptionSpecificationTypeDef,
    GetKeyspaceResponseTypeDef,
    GetTableResponseTypeDef,
    ListKeyspacesResponseTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PointInTimeRecoveryTypeDef,
    RestoreTableResponseTypeDef,
    SchemaDefinitionTypeDef,
    TagTypeDef,
    TimeToLiveTypeDef,
    UpdateTableResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KeyspacesClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class KeyspacesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KeyspacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#can_paginate)
        """

    def create_keyspace(
        self, *, keyspaceName: str, tags: Sequence[TagTypeDef] = ...
    ) -> CreateKeyspaceResponseTypeDef:
        """
        The `CreateKeyspace` operation adds a new keyspace to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.create_keyspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#create_keyspace)
        """

    def create_table(
        self,
        *,
        keyspaceName: str,
        tableName: str,
        schemaDefinition: SchemaDefinitionTypeDef,
        comment: CommentTypeDef = ...,
        capacitySpecification: CapacitySpecificationTypeDef = ...,
        encryptionSpecification: EncryptionSpecificationTypeDef = ...,
        pointInTimeRecovery: PointInTimeRecoveryTypeDef = ...,
        ttl: TimeToLiveTypeDef = ...,
        defaultTimeToLive: int = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateTableResponseTypeDef:
        """
        The `CreateTable` operation adds a new table to the specified keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.create_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#create_table)
        """

    def delete_keyspace(self, *, keyspaceName: str) -> Dict[str, Any]:
        """
        The `DeleteKeyspace` operation deletes a keyspace and all of its tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.delete_keyspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#delete_keyspace)
        """

    def delete_table(self, *, keyspaceName: str, tableName: str) -> Dict[str, Any]:
        """
        The `DeleteTable` operation deletes a table and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.delete_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#delete_table)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#generate_presigned_url)
        """

    def get_keyspace(self, *, keyspaceName: str) -> GetKeyspaceResponseTypeDef:
        """
        Returns the name and the Amazon Resource Name (ARN) of the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.get_keyspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#get_keyspace)
        """

    def get_table(self, *, keyspaceName: str, tableName: str) -> GetTableResponseTypeDef:
        """
        Returns information about the table, including the table's name and current
        status, the keyspace name, configuration settings, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.get_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#get_table)
        """

    def list_keyspaces(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListKeyspacesResponseTypeDef:
        """
        Returns a list of keyspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.list_keyspaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#list_keyspaces)
        """

    def list_tables(
        self, *, keyspaceName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTablesResponseTypeDef:
        """
        Returns a list of tables for a specified keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.list_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#list_tables)
        """

    def list_tags_for_resource(
        self, *, resourceArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags associated with the specified Amazon Keyspaces
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#list_tags_for_resource)
        """

    def restore_table(
        self,
        *,
        sourceKeyspaceName: str,
        sourceTableName: str,
        targetKeyspaceName: str,
        targetTableName: str,
        restoreTimestamp: Union[datetime, str] = ...,
        capacitySpecificationOverride: CapacitySpecificationTypeDef = ...,
        encryptionSpecificationOverride: EncryptionSpecificationTypeDef = ...,
        pointInTimeRecoveryOverride: PointInTimeRecoveryTypeDef = ...,
        tagsOverride: Sequence[TagTypeDef] = ...
    ) -> RestoreTableResponseTypeDef:
        """
        Restores the specified table to the specified point in time within the
        `earliest_restorable_timestamp` and the current time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.restore_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#restore_table)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Removes the association of tags from a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#untag_resource)
        """

    def update_table(
        self,
        *,
        keyspaceName: str,
        tableName: str,
        addColumns: Sequence[ColumnDefinitionTypeDef] = ...,
        capacitySpecification: CapacitySpecificationTypeDef = ...,
        encryptionSpecification: EncryptionSpecificationTypeDef = ...,
        pointInTimeRecovery: PointInTimeRecoveryTypeDef = ...,
        ttl: TimeToLiveTypeDef = ...,
        defaultTimeToLive: int = ...
    ) -> UpdateTableResponseTypeDef:
        """
        Adds new columns to the table or updates one of the table's settings, for
        example capacity mode, encryption, point-in-time recovery, or ttl settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.update_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#update_table)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keyspaces"]) -> ListKeyspacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/client/#get_paginator)
        """
