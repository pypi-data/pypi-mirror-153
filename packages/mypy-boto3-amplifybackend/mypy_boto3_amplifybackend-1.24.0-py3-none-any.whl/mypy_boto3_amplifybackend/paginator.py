"""
Type annotations for amplifybackend service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_amplifybackend.client import AmplifyBackendClient
    from mypy_boto3_amplifybackend.paginator import (
        ListBackendJobsPaginator,
    )

    session = Session()
    client: AmplifyBackendClient = session.client("amplifybackend")

    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListBackendJobsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListBackendJobsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBackendJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/#listbackendjobspaginator)
    """

    def paginate(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str = ...,
        Operation: str = ...,
        Status: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBackendJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/paginators/#listbackendjobspaginator)
        """
