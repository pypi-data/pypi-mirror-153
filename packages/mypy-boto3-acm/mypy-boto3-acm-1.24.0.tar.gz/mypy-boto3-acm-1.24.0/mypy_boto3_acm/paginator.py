"""
Type annotations for acm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.paginator import (
        ListCertificatesPaginator,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import CertificateStatusType
from .type_defs import FiltersTypeDef, ListCertificatesResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListCertificatesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateStatuses: Sequence[CertificateStatusType] = ...,
        Includes: FiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
        """
