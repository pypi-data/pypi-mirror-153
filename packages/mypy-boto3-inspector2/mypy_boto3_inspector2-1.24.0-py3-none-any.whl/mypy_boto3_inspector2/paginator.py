"""
Type annotations for inspector2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_inspector2.client import Inspector2Client
    from mypy_boto3_inspector2.paginator import (
        ListAccountPermissionsPaginator,
        ListCoveragePaginator,
        ListCoverageStatisticsPaginator,
        ListDelegatedAdminAccountsPaginator,
        ListFiltersPaginator,
        ListFindingAggregationsPaginator,
        ListFindingsPaginator,
        ListMembersPaginator,
        ListUsageTotalsPaginator,
    )

    session = Session()
    client: Inspector2Client = session.client("inspector2")

    list_account_permissions_paginator: ListAccountPermissionsPaginator = client.get_paginator("list_account_permissions")
    list_coverage_paginator: ListCoveragePaginator = client.get_paginator("list_coverage")
    list_coverage_statistics_paginator: ListCoverageStatisticsPaginator = client.get_paginator("list_coverage_statistics")
    list_delegated_admin_accounts_paginator: ListDelegatedAdminAccountsPaginator = client.get_paginator("list_delegated_admin_accounts")
    list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
    list_finding_aggregations_paginator: ListFindingAggregationsPaginator = client.get_paginator("list_finding_aggregations")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_usage_totals_paginator: ListUsageTotalsPaginator = client.get_paginator("list_usage_totals")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import AggregationTypeType, FilterActionType, GroupKeyType, ServiceType
from .type_defs import (
    AggregationRequestTypeDef,
    CoverageFilterCriteriaTypeDef,
    FilterCriteriaTypeDef,
    ListAccountPermissionsResponseTypeDef,
    ListCoverageResponseTypeDef,
    ListCoverageStatisticsResponseTypeDef,
    ListDelegatedAdminAccountsResponseTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingAggregationsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListUsageTotalsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
    StringFilterTypeDef,
)

__all__ = (
    "ListAccountPermissionsPaginator",
    "ListCoveragePaginator",
    "ListCoverageStatisticsPaginator",
    "ListDelegatedAdminAccountsPaginator",
    "ListFiltersPaginator",
    "ListFindingAggregationsPaginator",
    "ListFindingsPaginator",
    "ListMembersPaginator",
    "ListUsageTotalsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountPermissionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListAccountPermissions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listaccountpermissionspaginator)
    """

    def paginate(
        self, *, service: ServiceType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccountPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListAccountPermissions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listaccountpermissionspaginator)
        """


class ListCoveragePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListCoverage)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listcoveragepaginator)
    """

    def paginate(
        self,
        *,
        filterCriteria: CoverageFilterCriteriaTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCoverageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListCoverage.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listcoveragepaginator)
        """


class ListCoverageStatisticsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListCoverageStatistics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listcoveragestatisticspaginator)
    """

    def paginate(
        self,
        *,
        filterCriteria: CoverageFilterCriteriaTypeDef = ...,
        groupBy: GroupKeyType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCoverageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListCoverageStatistics.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listcoveragestatisticspaginator)
        """


class ListDelegatedAdminAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListDelegatedAdminAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listdelegatedadminaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDelegatedAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListDelegatedAdminAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listdelegatedadminaccountspaginator)
        """


class ListFiltersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFilters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfilterspaginator)
    """

    def paginate(
        self,
        *,
        action: FilterActionType = ...,
        arns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFilters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfilterspaginator)
        """


class ListFindingAggregationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFindingAggregations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfindingaggregationspaginator)
    """

    def paginate(
        self,
        *,
        aggregationType: AggregationTypeType,
        accountIds: Sequence[StringFilterTypeDef] = ...,
        aggregationRequest: AggregationRequestTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingAggregationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFindingAggregations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfindingaggregationspaginator)
        """


class ListFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        filterCriteria: FilterCriteriaTypeDef = ...,
        sortCriteria: SortCriteriaTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listfindingspaginator)
        """


class ListMembersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listmemberspaginator)
    """

    def paginate(
        self, *, onlyAssociated: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listmemberspaginator)
        """


class ListUsageTotalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListUsageTotals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listusagetotalspaginator)
    """

    def paginate(
        self, *, accountIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsageTotalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Paginator.ListUsageTotals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/paginators/#listusagetotalspaginator)
        """
