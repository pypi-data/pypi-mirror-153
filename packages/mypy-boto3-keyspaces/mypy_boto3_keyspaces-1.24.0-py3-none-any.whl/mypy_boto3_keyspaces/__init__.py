"""
Main interface for keyspaces service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_keyspaces import (
        Client,
        KeyspacesClient,
        ListKeyspacesPaginator,
        ListTablesPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: KeyspacesClient = session.client("keyspaces")

    list_keyspaces_paginator: ListKeyspacesPaginator = client.get_paginator("list_keyspaces")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from .client import KeyspacesClient
from .paginator import ListKeyspacesPaginator, ListTablesPaginator, ListTagsForResourcePaginator

Client = KeyspacesClient


__all__ = (
    "Client",
    "KeyspacesClient",
    "ListKeyspacesPaginator",
    "ListTablesPaginator",
    "ListTagsForResourcePaginator",
)
