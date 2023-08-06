"""
Type annotations for importexport service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_importexport.client import ImportExportClient
    from mypy_boto3_importexport.paginator import (
        ListJobsPaginator,
    )

    session = Session()
    client: ImportExportClient = session.client("importexport")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListJobsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListJobsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Paginator.ListJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/#listjobspaginator)
    """

    def paginate(
        self, *, APIVersion: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/paginators/#listjobspaginator)
        """
