"""
Type annotations for shield service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_shield.client import ShieldClient
    from mypy_boto3_shield.paginator import (
        ListAttacksPaginator,
        ListProtectionsPaginator,
    )

    session = Session()
    client: ShieldClient = session.client("shield")

    list_attacks_paginator: ListAttacksPaginator = client.get_paginator("list_attacks")
    list_protections_paginator: ListProtectionsPaginator = client.get_paginator("list_protections")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAttacksResponseTypeDef,
    ListProtectionsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimeRangeTypeDef,
)

__all__ = ("ListAttacksPaginator", "ListProtectionsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAttacksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListAttacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listattackspaginator)
    """

    def paginate(
        self,
        *,
        ResourceArns: Sequence[str] = ...,
        StartTime: TimeRangeTypeDef = ...,
        EndTime: TimeRangeTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListAttacks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listattackspaginator)
        """


class ListProtectionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListProtections)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listprotectionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProtectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield.Paginator.ListProtections.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/paginators/#listprotectionspaginator)
        """
