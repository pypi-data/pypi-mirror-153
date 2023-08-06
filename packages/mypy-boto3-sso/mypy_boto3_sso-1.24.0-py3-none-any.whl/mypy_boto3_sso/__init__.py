"""
Main interface for sso service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sso import (
        Client,
        ListAccountRolesPaginator,
        ListAccountsPaginator,
        SSOClient,
    )

    session = Session()
    client: SSOClient = session.client("sso")

    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""
from .client import SSOClient
from .paginator import ListAccountRolesPaginator, ListAccountsPaginator

Client = SSOClient


__all__ = ("Client", "ListAccountRolesPaginator", "ListAccountsPaginator", "SSOClient")
