"""
Type annotations for s3outposts service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_s3outposts.client import S3OutpostsClient
    from mypy_boto3_s3outposts.paginator import (
        ListEndpointsPaginator,
        ListSharedEndpointsPaginator,
    )

    session = Session()
    client: S3OutpostsClient = session.client("s3outposts")

    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListEndpointsResultTypeDef,
    ListSharedEndpointsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListEndpointsPaginator", "ListSharedEndpointsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listendpointspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listendpointspaginator)
        """


class ListSharedEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListSharedEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listsharedendpointspaginator)
    """

    def paginate(
        self, *, OutpostId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSharedEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListSharedEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/paginators/#listsharedendpointspaginator)
        """
