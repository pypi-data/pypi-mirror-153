"""
Type annotations for mwaa service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mwaa.client import MWAAClient
    from mypy_boto3_mwaa.paginator import (
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: MWAAClient = session.client("mwaa")

    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListEnvironmentsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEnvironmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnvironmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/paginators/#listenvironmentspaginator)
        """
