"""
Type annotations for sso service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sso.client import SSOClient
    from mypy_boto3_sso.paginator import (
        ListAccountRolesPaginator,
        ListAccountsPaginator,
    )

    session = Session()
    client: SSOClient = session.client("sso")

    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAccountRolesResponseTypeDef,
    ListAccountsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListAccountRolesPaginator", "ListAccountsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountRolesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccountRoles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountrolespaginator)
    """

    def paginate(
        self, *, accessToken: str, accountId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccountRoles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountrolespaginator)
        """


class ListAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountspaginator)
    """

    def paginate(
        self, *, accessToken: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO.Paginator.ListAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/paginators/#listaccountspaginator)
        """
