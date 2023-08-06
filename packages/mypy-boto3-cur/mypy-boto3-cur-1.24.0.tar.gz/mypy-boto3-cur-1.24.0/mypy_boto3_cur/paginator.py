"""
Type annotations for cur service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cur.client import CostandUsageReportServiceClient
    from mypy_boto3_cur.paginator import (
        DescribeReportDefinitionsPaginator,
    )

    session = Session()
    client: CostandUsageReportServiceClient = session.client("cur")

    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import DescribeReportDefinitionsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("DescribeReportDefinitionsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeReportDefinitionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html#CostandUsageReportService.Paginator.DescribeReportDefinitions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/paginators/#describereportdefinitionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeReportDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html#CostandUsageReportService.Paginator.DescribeReportDefinitions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/paginators/#describereportdefinitionspaginator)
        """
