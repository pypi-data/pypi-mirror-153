"""
Main interface for macie service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_macie import (
        Client,
        ListMemberAccountsPaginator,
        ListS3ResourcesPaginator,
        MacieClient,
    )

    session = Session()
    client: MacieClient = session.client("macie")

    list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
    list_s3_resources_paginator: ListS3ResourcesPaginator = client.get_paginator("list_s3_resources")
    ```
"""
from .client import MacieClient
from .paginator import ListMemberAccountsPaginator, ListS3ResourcesPaginator

Client = MacieClient


__all__ = ("Client", "ListMemberAccountsPaginator", "ListS3ResourcesPaginator", "MacieClient")
