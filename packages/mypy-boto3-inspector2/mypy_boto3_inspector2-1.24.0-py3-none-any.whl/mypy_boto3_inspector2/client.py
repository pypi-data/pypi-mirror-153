"""
Type annotations for inspector2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_inspector2.client import Inspector2Client

    session = Session()
    client: Inspector2Client = session.client("inspector2")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AggregationTypeType,
    FilterActionType,
    GroupKeyType,
    ReportFormatType,
    ResourceScanTypeType,
    ServiceType,
)
from .paginator import (
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
from .type_defs import (
    AggregationRequestTypeDef,
    AssociateMemberResponseTypeDef,
    AutoEnableTypeDef,
    BatchGetAccountStatusResponseTypeDef,
    BatchGetFreeTrialInfoResponseTypeDef,
    CancelFindingsReportResponseTypeDef,
    CoverageFilterCriteriaTypeDef,
    CreateFilterResponseTypeDef,
    CreateFindingsReportResponseTypeDef,
    DeleteFilterResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DestinationTypeDef,
    DisableDelegatedAdminAccountResponseTypeDef,
    DisableResponseTypeDef,
    DisassociateMemberResponseTypeDef,
    EnableDelegatedAdminAccountResponseTypeDef,
    EnableResponseTypeDef,
    FilterCriteriaTypeDef,
    GetDelegatedAdminAccountResponseTypeDef,
    GetFindingsReportStatusResponseTypeDef,
    GetMemberResponseTypeDef,
    ListAccountPermissionsResponseTypeDef,
    ListCoverageResponseTypeDef,
    ListCoverageStatisticsResponseTypeDef,
    ListDelegatedAdminAccountsResponseTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingAggregationsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsageTotalsResponseTypeDef,
    SortCriteriaTypeDef,
    StringFilterTypeDef,
    UpdateFilterResponseTypeDef,
    UpdateOrganizationConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Inspector2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Inspector2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Inspector2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#exceptions)
        """

    def associate_member(self, *, accountId: str) -> AssociateMemberResponseTypeDef:
        """
        Associates an Amazon Web Services account with an Amazon Inspector delegated
        administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.associate_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#associate_member)
        """

    def batch_get_account_status(
        self, *, accountIds: Sequence[str] = ...
    ) -> BatchGetAccountStatusResponseTypeDef:
        """
        Retrieves the Amazon Inspector status of multiple Amazon Web Services accounts
        within your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.batch_get_account_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#batch_get_account_status)
        """

    def batch_get_free_trial_info(
        self, *, accountIds: Sequence[str]
    ) -> BatchGetFreeTrialInfoResponseTypeDef:
        """
        Gets free trial status for multiple Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.batch_get_free_trial_info)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#batch_get_free_trial_info)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#can_paginate)
        """

    def cancel_findings_report(self, *, reportId: str) -> CancelFindingsReportResponseTypeDef:
        """
        Cancels the given findings report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.cancel_findings_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#cancel_findings_report)
        """

    def create_filter(
        self,
        *,
        action: FilterActionType,
        filterCriteria: FilterCriteriaTypeDef,
        name: str,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateFilterResponseTypeDef:
        """
        Creates a filter resource using specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.create_filter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#create_filter)
        """

    def create_findings_report(
        self,
        *,
        reportFormat: ReportFormatType,
        s3Destination: DestinationTypeDef,
        filterCriteria: FilterCriteriaTypeDef = ...
    ) -> CreateFindingsReportResponseTypeDef:
        """
        Creates a finding report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.create_findings_report)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#create_findings_report)
        """

    def delete_filter(self, *, arn: str) -> DeleteFilterResponseTypeDef:
        """
        Deletes a filter resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.delete_filter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#delete_filter)
        """

    def describe_organization_configuration(
        self,
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Describe Amazon Inspector configuration settings for an Amazon Web Services
        organization See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/inspector2-2020-06-08/DescribeOrganizationConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.describe_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#describe_organization_configuration)
        """

    def disable(
        self,
        *,
        accountIds: Sequence[str] = ...,
        resourceTypes: Sequence[ResourceScanTypeType] = ...
    ) -> DisableResponseTypeDef:
        """
        Disables Amazon Inspector scans for one or more Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.disable)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#disable)
        """

    def disable_delegated_admin_account(
        self, *, delegatedAdminAccountId: str
    ) -> DisableDelegatedAdminAccountResponseTypeDef:
        """
        Disables the Amazon Inspector delegated administrator for your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.disable_delegated_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#disable_delegated_admin_account)
        """

    def disassociate_member(self, *, accountId: str) -> DisassociateMemberResponseTypeDef:
        """
        Disassociates a member account from an Amazon Inspector delegated administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.disassociate_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#disassociate_member)
        """

    def enable(
        self,
        *,
        resourceTypes: Sequence[ResourceScanTypeType],
        accountIds: Sequence[str] = ...,
        clientToken: str = ...
    ) -> EnableResponseTypeDef:
        """
        Enables Amazon Inspector scans for one or more Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.enable)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#enable)
        """

    def enable_delegated_admin_account(
        self, *, delegatedAdminAccountId: str, clientToken: str = ...
    ) -> EnableDelegatedAdminAccountResponseTypeDef:
        """
        Enables the Amazon Inspector delegated administrator for your Organizations
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.enable_delegated_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#enable_delegated_admin_account)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#generate_presigned_url)
        """

    def get_delegated_admin_account(self) -> GetDelegatedAdminAccountResponseTypeDef:
        """
        Retrieves information about the Amazon Inspector delegated administrator for
        your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_delegated_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_delegated_admin_account)
        """

    def get_findings_report_status(
        self, *, reportId: str = ...
    ) -> GetFindingsReportStatusResponseTypeDef:
        """
        Gets the status of a findings report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_findings_report_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_findings_report_status)
        """

    def get_member(self, *, accountId: str) -> GetMemberResponseTypeDef:
        """
        Gets member information for your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_member)
        """

    def list_account_permissions(
        self, *, maxResults: int = ..., nextToken: str = ..., service: ServiceType = ...
    ) -> ListAccountPermissionsResponseTypeDef:
        """
        Lists the permissions an account has to configure Amazon Inspector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_account_permissions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_account_permissions)
        """

    def list_coverage(
        self,
        *,
        filterCriteria: CoverageFilterCriteriaTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListCoverageResponseTypeDef:
        """
        Lists coverage details for you environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_coverage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_coverage)
        """

    def list_coverage_statistics(
        self,
        *,
        filterCriteria: CoverageFilterCriteriaTypeDef = ...,
        groupBy: GroupKeyType = ...,
        nextToken: str = ...
    ) -> ListCoverageStatisticsResponseTypeDef:
        """
        Lists Amazon Inspector coverage statistics for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_coverage_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_coverage_statistics)
        """

    def list_delegated_admin_accounts(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListDelegatedAdminAccountsResponseTypeDef:
        """
        Lists information about the Amazon Inspector delegated administrator of your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_delegated_admin_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_delegated_admin_accounts)
        """

    def list_filters(
        self,
        *,
        action: FilterActionType = ...,
        arns: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListFiltersResponseTypeDef:
        """
        Lists the filters associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_filters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_filters)
        """

    def list_finding_aggregations(
        self,
        *,
        aggregationType: AggregationTypeType,
        accountIds: Sequence[StringFilterTypeDef] = ...,
        aggregationRequest: AggregationRequestTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListFindingAggregationsResponseTypeDef:
        """
        Lists aggregated finding data for your environment based on specific criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_finding_aggregations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_finding_aggregations)
        """

    def list_findings(
        self,
        *,
        filterCriteria: FilterCriteriaTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortCriteria: SortCriteriaTypeDef = ...
    ) -> ListFindingsResponseTypeDef:
        """
        Lists findings for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_findings)
        """

    def list_members(
        self, *, maxResults: int = ..., nextToken: str = ..., onlyAssociated: bool = ...
    ) -> ListMembersResponseTypeDef:
        """
        List members associated with the Amazon Inspector delegated administrator for
        your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_members)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags attached to a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_tags_for_resource)
        """

    def list_usage_totals(
        self, *, accountIds: Sequence[str] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListUsageTotalsResponseTypeDef:
        """
        Lists the Amazon Inspector usage totals over the last 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.list_usage_totals)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#list_usage_totals)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#untag_resource)
        """

    def update_filter(
        self,
        *,
        filterArn: str,
        action: FilterActionType = ...,
        description: str = ...,
        filterCriteria: FilterCriteriaTypeDef = ...,
        name: str = ...
    ) -> UpdateFilterResponseTypeDef:
        """
        Specifies the action that is to be applied to the findings that match the
        filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.update_filter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#update_filter)
        """

    def update_organization_configuration(
        self, *, autoEnable: AutoEnableTypeDef
    ) -> UpdateOrganizationConfigurationResponseTypeDef:
        """
        Updates the configurations for your Amazon Inspector organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.update_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#update_organization_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_permissions"]
    ) -> ListAccountPermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_coverage"]) -> ListCoveragePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_coverage_statistics"]
    ) -> ListCoverageStatisticsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_delegated_admin_accounts"]
    ) -> ListDelegatedAdminAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_filters"]) -> ListFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_finding_aggregations"]
    ) -> ListFindingAggregationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_usage_totals"]
    ) -> ListUsageTotalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2.html#Inspector2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/client/#get_paginator)
        """
