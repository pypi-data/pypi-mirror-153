"""
Type annotations for codecommit service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codecommit.client import CodeCommitClient
    from mypy_boto3_codecommit.paginator import (
        DescribePullRequestEventsPaginator,
        GetCommentsForComparedCommitPaginator,
        GetCommentsForPullRequestPaginator,
        GetDifferencesPaginator,
        ListBranchesPaginator,
        ListPullRequestsPaginator,
        ListRepositoriesPaginator,
    )

    session = Session()
    client: CodeCommitClient = session.client("codecommit")

    describe_pull_request_events_paginator: DescribePullRequestEventsPaginator = client.get_paginator("describe_pull_request_events")
    get_comments_for_compared_commit_paginator: GetCommentsForComparedCommitPaginator = client.get_paginator("get_comments_for_compared_commit")
    get_comments_for_pull_request_paginator: GetCommentsForPullRequestPaginator = client.get_paginator("get_comments_for_pull_request")
    get_differences_paginator: GetDifferencesPaginator = client.get_paginator("get_differences")
    list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
    list_pull_requests_paginator: ListPullRequestsPaginator = client.get_paginator("list_pull_requests")
    list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    OrderEnumType,
    PullRequestEventTypeType,
    PullRequestStatusEnumType,
    SortByEnumType,
)
from .type_defs import (
    DescribePullRequestEventsOutputTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetDifferencesOutputTypeDef,
    ListBranchesOutputTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribePullRequestEventsPaginator",
    "GetCommentsForComparedCommitPaginator",
    "GetCommentsForPullRequestPaginator",
    "GetDifferencesPaginator",
    "ListBranchesPaginator",
    "ListPullRequestsPaginator",
    "ListRepositoriesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribePullRequestEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.DescribePullRequestEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
    """

    def paginate(
        self,
        *,
        pullRequestId: str,
        pullRequestEventType: PullRequestEventTypeType = ...,
        actorArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePullRequestEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.DescribePullRequestEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
        """


class GetCommentsForComparedCommitPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        afterCommitId: str,
        beforeCommitId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCommentsForComparedCommitOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
        """


class GetCommentsForPullRequestPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForPullRequest)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
    """

    def paginate(
        self,
        *,
        pullRequestId: str,
        repositoryName: str = ...,
        beforeCommitId: str = ...,
        afterCommitId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetCommentsForPullRequestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForPullRequest.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
        """


class GetDifferencesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetDifferences)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        afterCommitSpecifier: str,
        beforeCommitSpecifier: str = ...,
        beforePath: str = ...,
        afterPath: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDifferencesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.GetDifferences.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
        """


class ListBranchesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListBranches)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
    """

    def paginate(
        self, *, repositoryName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBranchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListBranches.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
        """


class ListPullRequestsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListPullRequests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        authorArn: str = ...,
        pullRequestStatus: PullRequestStatusEnumType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPullRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListPullRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
        """


class ListRepositoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListRepositories)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
    """

    def paginate(
        self,
        *,
        sortBy: SortByEnumType = ...,
        order: OrderEnumType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Paginator.ListRepositories.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
        """
