"""
Type annotations for support service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_support.client import SupportClient
    from mypy_boto3_support.paginator import (
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
    )

    session = Session()
    client: SupportClient = session.client("support")

    describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
    describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeCasesPaginator", "DescribeCommunicationsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecasespaginator)
    """

    def paginate(
        self,
        *,
        caseIdList: Sequence[str] = ...,
        displayId: str = ...,
        afterTime: str = ...,
        beforeTime: str = ...,
        includeResolvedCases: bool = ...,
        language: str = ...,
        includeCommunications: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecasespaginator)
        """


class DescribeCommunicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCommunications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecommunicationspaginator)
    """

    def paginate(
        self,
        *,
        caseId: str,
        beforeTime: str = ...,
        afterTime: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeCommunicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Paginator.DescribeCommunications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support/paginators/#describecommunicationspaginator)
        """
