"""
Type annotations for inspector2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector2.type_defs import SeverityCountsTypeDef

    data: SeverityCountsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountSortByType,
    AggregationFindingTypeType,
    AggregationResourceTypeType,
    AggregationTypeType,
    AmiSortByType,
    AwsEcrContainerSortByType,
    CoverageResourceTypeType,
    CoverageStringComparisonType,
    DelegatedAdminStatusType,
    Ec2InstanceSortByType,
    Ec2PlatformType,
    EcrScanFrequencyType,
    ErrorCodeType,
    ExternalReportStatusType,
    FilterActionType,
    FindingStatusType,
    FindingTypeSortByType,
    FindingTypeType,
    FreeTrialInfoErrorCodeType,
    FreeTrialStatusType,
    FreeTrialTypeType,
    GroupKeyType,
    ImageLayerSortByType,
    NetworkProtocolType,
    OperationType,
    PackageManagerType,
    PackageSortByType,
    RelationshipStatusType,
    ReportFormatType,
    ReportingErrorCodeType,
    RepositorySortByType,
    ResourceScanTypeType,
    ResourceTypeType,
    ScanStatusCodeType,
    ScanStatusReasonType,
    ScanTypeType,
    ServiceType,
    SeverityType,
    SortFieldType,
    SortOrderType,
    StatusType,
    StringComparisonType,
    TitleSortByType,
    UsageTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "SeverityCountsTypeDef",
    "AccountAggregationTypeDef",
    "StateTypeDef",
    "ResourceStatusTypeDef",
    "FindingTypeAggregationTypeDef",
    "StringFilterTypeDef",
    "AssociateMemberRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AutoEnableTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "BatchGetAccountStatusRequestRequestTypeDef",
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    "FreeTrialInfoErrorTypeDef",
    "CancelFindingsReportRequestRequestTypeDef",
    "CountsTypeDef",
    "CoverageMapFilterTypeDef",
    "CoverageStringFilterTypeDef",
    "ScanStatusTypeDef",
    "DestinationTypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreTypeDef",
    "DateFilterTypeDef",
    "DelegatedAdminAccountTypeDef",
    "DelegatedAdminTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    "DisableRequestRequestTypeDef",
    "DisassociateMemberRequestRequestTypeDef",
    "MapFilterTypeDef",
    "Ec2MetadataTypeDef",
    "EcrContainerImageMetadataTypeDef",
    "EcrRepositoryMetadataTypeDef",
    "EnableDelegatedAdminAccountRequestRequestTypeDef",
    "EnableRequestRequestTypeDef",
    "NumberFilterTypeDef",
    "PortRangeFilterTypeDef",
    "FreeTrialInfoTypeDef",
    "GetFindingsReportStatusRequestRequestTypeDef",
    "GetMemberRequestRequestTypeDef",
    "MemberTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccountPermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "SortCriteriaTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListUsageTotalsRequestRequestTypeDef",
    "StepTypeDef",
    "PortRangeTypeDef",
    "VulnerablePackageTypeDef",
    "RecommendationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UsageTypeDef",
    "AccountAggregationResponseTypeDef",
    "AmiAggregationResponseTypeDef",
    "AwsEcrContainerAggregationResponseTypeDef",
    "Ec2InstanceAggregationResponseTypeDef",
    "FindingTypeAggregationResponseTypeDef",
    "ImageLayerAggregationResponseTypeDef",
    "PackageAggregationResponseTypeDef",
    "RepositoryAggregationResponseTypeDef",
    "TitleAggregationResponseTypeDef",
    "ResourceStateTypeDef",
    "AccountTypeDef",
    "FailedAccountTypeDef",
    "AmiAggregationTypeDef",
    "AwsEcrContainerAggregationTypeDef",
    "ImageLayerAggregationTypeDef",
    "PackageAggregationTypeDef",
    "RepositoryAggregationTypeDef",
    "TitleAggregationTypeDef",
    "AssociateMemberResponseTypeDef",
    "CancelFindingsReportResponseTypeDef",
    "CreateFilterResponseTypeDef",
    "CreateFindingsReportResponseTypeDef",
    "DeleteFilterResponseTypeDef",
    "DisableDelegatedAdminAccountResponseTypeDef",
    "DisassociateMemberResponseTypeDef",
    "EnableDelegatedAdminAccountResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateFilterResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateOrganizationConfigurationResponseTypeDef",
    "ResourceDetailsTypeDef",
    "ListCoverageStatisticsResponseTypeDef",
    "CoverageFilterCriteriaTypeDef",
    "CvssScoreDetailsTypeDef",
    "ListDelegatedAdminAccountsResponseTypeDef",
    "GetDelegatedAdminAccountResponseTypeDef",
    "Ec2InstanceAggregationTypeDef",
    "ResourceScanMetadataTypeDef",
    "PackageFilterTypeDef",
    "FreeTrialAccountInfoTypeDef",
    "GetMemberResponseTypeDef",
    "ListMembersResponseTypeDef",
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    "ListAccountPermissionsResponseTypeDef",
    "NetworkPathTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "RemediationTypeDef",
    "UsageTotalTypeDef",
    "AggregationResponseTypeDef",
    "AccountStateTypeDef",
    "DisableResponseTypeDef",
    "EnableResponseTypeDef",
    "ResourceTypeDef",
    "ListCoverageRequestListCoveragePaginateTypeDef",
    "ListCoverageRequestRequestTypeDef",
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    "ListCoverageStatisticsRequestRequestTypeDef",
    "InspectorScoreDetailsTypeDef",
    "AggregationRequestTypeDef",
    "CoveredResourceTypeDef",
    "FilterCriteriaTypeDef",
    "BatchGetFreeTrialInfoResponseTypeDef",
    "NetworkReachabilityDetailsTypeDef",
    "ListUsageTotalsResponseTypeDef",
    "ListFindingAggregationsResponseTypeDef",
    "BatchGetAccountStatusResponseTypeDef",
    "ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    "ListFindingAggregationsRequestRequestTypeDef",
    "ListCoverageResponseTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateFindingsReportRequestRequestTypeDef",
    "FilterTypeDef",
    "GetFindingsReportStatusResponseTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "UpdateFilterRequestRequestTypeDef",
    "FindingTypeDef",
    "ListFiltersResponseTypeDef",
    "ListFindingsResponseTypeDef",
)

SeverityCountsTypeDef = TypedDict(
    "SeverityCountsTypeDef",
    {
        "all": int,
        "critical": int,
        "high": int,
        "medium": int,
    },
    total=False,
)

AccountAggregationTypeDef = TypedDict(
    "AccountAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": AccountSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

StateTypeDef = TypedDict(
    "StateTypeDef",
    {
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "status": StatusType,
    },
)

ResourceStatusTypeDef = TypedDict(
    "ResourceStatusTypeDef",
    {
        "ec2": StatusType,
        "ecr": StatusType,
    },
)

FindingTypeAggregationTypeDef = TypedDict(
    "FindingTypeAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": FindingTypeSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "comparison": StringComparisonType,
        "value": str,
    },
)

AssociateMemberRequestRequestTypeDef = TypedDict(
    "AssociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

AutoEnableTypeDef = TypedDict(
    "AutoEnableTypeDef",
    {
        "ec2": bool,
        "ecr": bool,
    },
)

AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "iamInstanceProfileArn": str,
        "imageId": str,
        "ipV4Addresses": List[str],
        "ipV6Addresses": List[str],
        "keyName": str,
        "launchedAt": datetime,
        "platform": str,
        "subnetId": str,
        "type": str,
        "vpcId": str,
    },
    total=False,
)

_RequiredAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_RequiredAwsEcrContainerImageDetailsTypeDef",
    {
        "imageHash": str,
        "registry": str,
        "repositoryName": str,
    },
)
_OptionalAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_OptionalAwsEcrContainerImageDetailsTypeDef",
    {
        "architecture": str,
        "author": str,
        "imageTags": List[str],
        "platform": str,
        "pushedAt": datetime,
    },
    total=False,
)


class AwsEcrContainerImageDetailsTypeDef(
    _RequiredAwsEcrContainerImageDetailsTypeDef, _OptionalAwsEcrContainerImageDetailsTypeDef
):
    pass


BatchGetAccountStatusRequestRequestTypeDef = TypedDict(
    "BatchGetAccountStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
    total=False,
)

BatchGetFreeTrialInfoRequestRequestTypeDef = TypedDict(
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
)

FreeTrialInfoErrorTypeDef = TypedDict(
    "FreeTrialInfoErrorTypeDef",
    {
        "accountId": str,
        "code": FreeTrialInfoErrorCodeType,
        "message": str,
    },
)

CancelFindingsReportRequestRequestTypeDef = TypedDict(
    "CancelFindingsReportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)

CountsTypeDef = TypedDict(
    "CountsTypeDef",
    {
        "count": int,
        "groupKey": GroupKeyType,
    },
    total=False,
)

_RequiredCoverageMapFilterTypeDef = TypedDict(
    "_RequiredCoverageMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalCoverageMapFilterTypeDef = TypedDict(
    "_OptionalCoverageMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class CoverageMapFilterTypeDef(
    _RequiredCoverageMapFilterTypeDef, _OptionalCoverageMapFilterTypeDef
):
    pass


CoverageStringFilterTypeDef = TypedDict(
    "CoverageStringFilterTypeDef",
    {
        "comparison": CoverageStringComparisonType,
        "value": str,
    },
)

ScanStatusTypeDef = TypedDict(
    "ScanStatusTypeDef",
    {
        "reason": ScanStatusReasonType,
        "statusCode": ScanStatusCodeType,
    },
)

_RequiredDestinationTypeDef = TypedDict(
    "_RequiredDestinationTypeDef",
    {
        "bucketName": str,
        "kmsKeyArn": str,
    },
)
_OptionalDestinationTypeDef = TypedDict(
    "_OptionalDestinationTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class DestinationTypeDef(_RequiredDestinationTypeDef, _OptionalDestinationTypeDef):
    pass


CvssScoreAdjustmentTypeDef = TypedDict(
    "CvssScoreAdjustmentTypeDef",
    {
        "metric": str,
        "reason": str,
    },
)

CvssScoreTypeDef = TypedDict(
    "CvssScoreTypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
        "source": str,
        "version": str,
    },
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "endInclusive": Union[datetime, str],
        "startInclusive": Union[datetime, str],
    },
    total=False,
)

DelegatedAdminAccountTypeDef = TypedDict(
    "DelegatedAdminAccountTypeDef",
    {
        "accountId": str,
        "status": DelegatedAdminStatusType,
    },
    total=False,
)

DelegatedAdminTypeDef = TypedDict(
    "DelegatedAdminTypeDef",
    {
        "accountId": str,
        "relationshipStatus": RelationshipStatusType,
    },
    total=False,
)

DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DisableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)

DisableRequestRequestTypeDef = TypedDict(
    "DisableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
    total=False,
)

DisassociateMemberRequestRequestTypeDef = TypedDict(
    "DisassociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

_RequiredMapFilterTypeDef = TypedDict(
    "_RequiredMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalMapFilterTypeDef = TypedDict(
    "_OptionalMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class MapFilterTypeDef(_RequiredMapFilterTypeDef, _OptionalMapFilterTypeDef):
    pass


Ec2MetadataTypeDef = TypedDict(
    "Ec2MetadataTypeDef",
    {
        "amiId": str,
        "platform": Ec2PlatformType,
        "tags": Dict[str, str],
    },
    total=False,
)

EcrContainerImageMetadataTypeDef = TypedDict(
    "EcrContainerImageMetadataTypeDef",
    {
        "tags": List[str],
    },
    total=False,
)

EcrRepositoryMetadataTypeDef = TypedDict(
    "EcrRepositoryMetadataTypeDef",
    {
        "name": str,
        "scanFrequency": EcrScanFrequencyType,
    },
    total=False,
)

_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)
_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class EnableDelegatedAdminAccountRequestRequestTypeDef(
    _RequiredEnableDelegatedAdminAccountRequestRequestTypeDef,
    _OptionalEnableDelegatedAdminAccountRequestRequestTypeDef,
):
    pass


_RequiredEnableRequestRequestTypeDef = TypedDict(
    "_RequiredEnableRequestRequestTypeDef",
    {
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
)
_OptionalEnableRequestRequestTypeDef = TypedDict(
    "_OptionalEnableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class EnableRequestRequestTypeDef(
    _RequiredEnableRequestRequestTypeDef, _OptionalEnableRequestRequestTypeDef
):
    pass


NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "lowerInclusive": float,
        "upperInclusive": float,
    },
    total=False,
)

PortRangeFilterTypeDef = TypedDict(
    "PortRangeFilterTypeDef",
    {
        "beginInclusive": int,
        "endInclusive": int,
    },
    total=False,
)

FreeTrialInfoTypeDef = TypedDict(
    "FreeTrialInfoTypeDef",
    {
        "end": datetime,
        "start": datetime,
        "status": FreeTrialStatusType,
        "type": FreeTrialTypeType,
    },
)

GetFindingsReportStatusRequestRequestTypeDef = TypedDict(
    "GetFindingsReportStatusRequestRequestTypeDef",
    {
        "reportId": str,
    },
    total=False,
)

GetMemberRequestRequestTypeDef = TypedDict(
    "GetMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "accountId": str,
        "delegatedAdminAccountId": str,
        "relationshipStatus": RelationshipStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListAccountPermissionsRequestRequestTypeDef = TypedDict(
    "ListAccountPermissionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "service": ServiceType,
    },
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "operation": OperationType,
        "service": ServiceType,
    },
)

ListDelegatedAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListFiltersRequestRequestTypeDef = TypedDict(
    "ListFiltersRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "field": SortFieldType,
        "sortOrder": SortOrderType,
    },
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "onlyAssociated": bool,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListUsageTotalsRequestRequestTypeDef = TypedDict(
    "ListUsageTotalsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "componentId": str,
        "componentType": str,
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "begin": int,
        "end": int,
    },
)

_RequiredVulnerablePackageTypeDef = TypedDict(
    "_RequiredVulnerablePackageTypeDef",
    {
        "name": str,
        "version": str,
    },
)
_OptionalVulnerablePackageTypeDef = TypedDict(
    "_OptionalVulnerablePackageTypeDef",
    {
        "arch": str,
        "epoch": int,
        "filePath": str,
        "fixedInVersion": str,
        "packageManager": PackageManagerType,
        "release": str,
        "sourceLayerHash": str,
    },
    total=False,
)


class VulnerablePackageTypeDef(
    _RequiredVulnerablePackageTypeDef, _OptionalVulnerablePackageTypeDef
):
    pass


RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Url": str,
        "text": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UsageTypeDef = TypedDict(
    "UsageTypeDef",
    {
        "currency": Literal["USD"],
        "estimatedMonthlyCost": float,
        "total": float,
        "type": UsageTypeType,
    },
    total=False,
)

AccountAggregationResponseTypeDef = TypedDict(
    "AccountAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)

_RequiredAmiAggregationResponseTypeDef = TypedDict(
    "_RequiredAmiAggregationResponseTypeDef",
    {
        "ami": str,
    },
)
_OptionalAmiAggregationResponseTypeDef = TypedDict(
    "_OptionalAmiAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedInstances": int,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class AmiAggregationResponseTypeDef(
    _RequiredAmiAggregationResponseTypeDef, _OptionalAmiAggregationResponseTypeDef
):
    pass


_RequiredAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_RequiredAwsEcrContainerAggregationResponseTypeDef",
    {
        "resourceId": str,
    },
)
_OptionalAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_OptionalAwsEcrContainerAggregationResponseTypeDef",
    {
        "accountId": str,
        "architecture": str,
        "imageSha": str,
        "imageTags": List[str],
        "repository": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class AwsEcrContainerAggregationResponseTypeDef(
    _RequiredAwsEcrContainerAggregationResponseTypeDef,
    _OptionalAwsEcrContainerAggregationResponseTypeDef,
):
    pass


_RequiredEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_RequiredEc2InstanceAggregationResponseTypeDef",
    {
        "instanceId": str,
    },
)
_OptionalEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_OptionalEc2InstanceAggregationResponseTypeDef",
    {
        "accountId": str,
        "ami": str,
        "instanceTags": Dict[str, str],
        "networkFindings": int,
        "operatingSystem": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class Ec2InstanceAggregationResponseTypeDef(
    _RequiredEc2InstanceAggregationResponseTypeDef, _OptionalEc2InstanceAggregationResponseTypeDef
):
    pass


FindingTypeAggregationResponseTypeDef = TypedDict(
    "FindingTypeAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)

_RequiredImageLayerAggregationResponseTypeDef = TypedDict(
    "_RequiredImageLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "layerHash": str,
        "repository": str,
        "resourceId": str,
    },
)
_OptionalImageLayerAggregationResponseTypeDef = TypedDict(
    "_OptionalImageLayerAggregationResponseTypeDef",
    {
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class ImageLayerAggregationResponseTypeDef(
    _RequiredImageLayerAggregationResponseTypeDef, _OptionalImageLayerAggregationResponseTypeDef
):
    pass


_RequiredPackageAggregationResponseTypeDef = TypedDict(
    "_RequiredPackageAggregationResponseTypeDef",
    {
        "packageName": str,
    },
)
_OptionalPackageAggregationResponseTypeDef = TypedDict(
    "_OptionalPackageAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class PackageAggregationResponseTypeDef(
    _RequiredPackageAggregationResponseTypeDef, _OptionalPackageAggregationResponseTypeDef
):
    pass


_RequiredRepositoryAggregationResponseTypeDef = TypedDict(
    "_RequiredRepositoryAggregationResponseTypeDef",
    {
        "repository": str,
    },
)
_OptionalRepositoryAggregationResponseTypeDef = TypedDict(
    "_OptionalRepositoryAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedImages": int,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class RepositoryAggregationResponseTypeDef(
    _RequiredRepositoryAggregationResponseTypeDef, _OptionalRepositoryAggregationResponseTypeDef
):
    pass


_RequiredTitleAggregationResponseTypeDef = TypedDict(
    "_RequiredTitleAggregationResponseTypeDef",
    {
        "title": str,
    },
)
_OptionalTitleAggregationResponseTypeDef = TypedDict(
    "_OptionalTitleAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
        "vulnerabilityId": str,
    },
    total=False,
)


class TitleAggregationResponseTypeDef(
    _RequiredTitleAggregationResponseTypeDef, _OptionalTitleAggregationResponseTypeDef
):
    pass


ResourceStateTypeDef = TypedDict(
    "ResourceStateTypeDef",
    {
        "ec2": StateTypeDef,
        "ecr": StateTypeDef,
    },
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "accountId": str,
        "resourceStatus": ResourceStatusTypeDef,
        "status": StatusType,
    },
)

_RequiredFailedAccountTypeDef = TypedDict(
    "_RequiredFailedAccountTypeDef",
    {
        "accountId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
)
_OptionalFailedAccountTypeDef = TypedDict(
    "_OptionalFailedAccountTypeDef",
    {
        "resourceStatus": ResourceStatusTypeDef,
        "status": StatusType,
    },
    total=False,
)


class FailedAccountTypeDef(_RequiredFailedAccountTypeDef, _OptionalFailedAccountTypeDef):
    pass


AmiAggregationTypeDef = TypedDict(
    "AmiAggregationTypeDef",
    {
        "amis": Sequence[StringFilterTypeDef],
        "sortBy": AmiSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

AwsEcrContainerAggregationTypeDef = TypedDict(
    "AwsEcrContainerAggregationTypeDef",
    {
        "architectures": Sequence[StringFilterTypeDef],
        "imageShas": Sequence[StringFilterTypeDef],
        "imageTags": Sequence[StringFilterTypeDef],
        "repositories": Sequence[StringFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "sortBy": AwsEcrContainerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

ImageLayerAggregationTypeDef = TypedDict(
    "ImageLayerAggregationTypeDef",
    {
        "layerHashes": Sequence[StringFilterTypeDef],
        "repositories": Sequence[StringFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "sortBy": ImageLayerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

PackageAggregationTypeDef = TypedDict(
    "PackageAggregationTypeDef",
    {
        "packageNames": Sequence[StringFilterTypeDef],
        "sortBy": PackageSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

RepositoryAggregationTypeDef = TypedDict(
    "RepositoryAggregationTypeDef",
    {
        "repositories": Sequence[StringFilterTypeDef],
        "sortBy": RepositorySortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

TitleAggregationTypeDef = TypedDict(
    "TitleAggregationTypeDef",
    {
        "resourceType": AggregationResourceTypeType,
        "sortBy": TitleSortByType,
        "sortOrder": SortOrderType,
        "titles": Sequence[StringFilterTypeDef],
        "vulnerabilityIds": Sequence[StringFilterTypeDef],
    },
    total=False,
)

AssociateMemberResponseTypeDef = TypedDict(
    "AssociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelFindingsReportResponseTypeDef = TypedDict(
    "CancelFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFindingsReportResponseTypeDef = TypedDict(
    "CreateFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFilterResponseTypeDef = TypedDict(
    "DeleteFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "DisableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateMemberResponseTypeDef = TypedDict(
    "DisassociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "EnableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFilterResponseTypeDef = TypedDict(
    "UpdateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "maxAccountLimitReached": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
    },
)

UpdateOrganizationConfigurationResponseTypeDef = TypedDict(
    "UpdateOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "awsEc2Instance": AwsEc2InstanceDetailsTypeDef,
        "awsEcrContainerImage": AwsEcrContainerImageDetailsTypeDef,
    },
    total=False,
)

ListCoverageStatisticsResponseTypeDef = TypedDict(
    "ListCoverageStatisticsResponseTypeDef",
    {
        "countsByGroup": List[CountsTypeDef],
        "nextToken": str,
        "totalCounts": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CoverageFilterCriteriaTypeDef = TypedDict(
    "CoverageFilterCriteriaTypeDef",
    {
        "accountId": Sequence[CoverageStringFilterTypeDef],
        "ec2InstanceTags": Sequence[CoverageMapFilterTypeDef],
        "ecrImageTags": Sequence[CoverageStringFilterTypeDef],
        "ecrRepositoryName": Sequence[CoverageStringFilterTypeDef],
        "resourceId": Sequence[CoverageStringFilterTypeDef],
        "resourceType": Sequence[CoverageStringFilterTypeDef],
        "scanStatusCode": Sequence[CoverageStringFilterTypeDef],
        "scanStatusReason": Sequence[CoverageStringFilterTypeDef],
        "scanType": Sequence[CoverageStringFilterTypeDef],
    },
    total=False,
)

_RequiredCvssScoreDetailsTypeDef = TypedDict(
    "_RequiredCvssScoreDetailsTypeDef",
    {
        "score": float,
        "scoreSource": str,
        "scoringVector": str,
        "version": str,
    },
)
_OptionalCvssScoreDetailsTypeDef = TypedDict(
    "_OptionalCvssScoreDetailsTypeDef",
    {
        "adjustments": List[CvssScoreAdjustmentTypeDef],
        "cvssSource": str,
    },
    total=False,
)


class CvssScoreDetailsTypeDef(_RequiredCvssScoreDetailsTypeDef, _OptionalCvssScoreDetailsTypeDef):
    pass


ListDelegatedAdminAccountsResponseTypeDef = TypedDict(
    "ListDelegatedAdminAccountsResponseTypeDef",
    {
        "delegatedAdminAccounts": List[DelegatedAdminAccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDelegatedAdminAccountResponseTypeDef = TypedDict(
    "GetDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdmin": DelegatedAdminTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

Ec2InstanceAggregationTypeDef = TypedDict(
    "Ec2InstanceAggregationTypeDef",
    {
        "amis": Sequence[StringFilterTypeDef],
        "instanceIds": Sequence[StringFilterTypeDef],
        "instanceTags": Sequence[MapFilterTypeDef],
        "operatingSystems": Sequence[StringFilterTypeDef],
        "sortBy": Ec2InstanceSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

ResourceScanMetadataTypeDef = TypedDict(
    "ResourceScanMetadataTypeDef",
    {
        "ec2": Ec2MetadataTypeDef,
        "ecrImage": EcrContainerImageMetadataTypeDef,
        "ecrRepository": EcrRepositoryMetadataTypeDef,
    },
    total=False,
)

PackageFilterTypeDef = TypedDict(
    "PackageFilterTypeDef",
    {
        "architecture": StringFilterTypeDef,
        "epoch": NumberFilterTypeDef,
        "name": StringFilterTypeDef,
        "release": StringFilterTypeDef,
        "sourceLayerHash": StringFilterTypeDef,
        "version": StringFilterTypeDef,
    },
    total=False,
)

FreeTrialAccountInfoTypeDef = TypedDict(
    "FreeTrialAccountInfoTypeDef",
    {
        "accountId": str,
        "freeTrialInfo": List[FreeTrialInfoTypeDef],
    },
)

GetMemberResponseTypeDef = TypedDict(
    "GetMemberResponseTypeDef",
    {
        "member": MemberTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "members": List[MemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef = TypedDict(
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    {
        "service": ServiceType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "ListFiltersRequestListFiltersPaginateTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "onlyAssociated": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListUsageTotalsRequestListUsageTotalsPaginateTypeDef = TypedDict(
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    {
        "accountIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAccountPermissionsResponseTypeDef = TypedDict(
    "ListAccountPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List[PermissionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkPathTypeDef = TypedDict(
    "NetworkPathTypeDef",
    {
        "steps": List[StepTypeDef],
    },
    total=False,
)

_RequiredPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_RequiredPackageVulnerabilityDetailsTypeDef",
    {
        "source": str,
        "vulnerabilityId": str,
        "vulnerablePackages": List[VulnerablePackageTypeDef],
    },
)
_OptionalPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_OptionalPackageVulnerabilityDetailsTypeDef",
    {
        "cvss": List[CvssScoreTypeDef],
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
        "sourceUrl": str,
        "vendorCreatedAt": datetime,
        "vendorSeverity": str,
        "vendorUpdatedAt": datetime,
    },
    total=False,
)


class PackageVulnerabilityDetailsTypeDef(
    _RequiredPackageVulnerabilityDetailsTypeDef, _OptionalPackageVulnerabilityDetailsTypeDef
):
    pass


RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": RecommendationTypeDef,
    },
    total=False,
)

UsageTotalTypeDef = TypedDict(
    "UsageTotalTypeDef",
    {
        "accountId": str,
        "usage": List[UsageTypeDef],
    },
    total=False,
)

AggregationResponseTypeDef = TypedDict(
    "AggregationResponseTypeDef",
    {
        "accountAggregation": AccountAggregationResponseTypeDef,
        "amiAggregation": AmiAggregationResponseTypeDef,
        "awsEcrContainerAggregation": AwsEcrContainerAggregationResponseTypeDef,
        "ec2InstanceAggregation": Ec2InstanceAggregationResponseTypeDef,
        "findingTypeAggregation": FindingTypeAggregationResponseTypeDef,
        "imageLayerAggregation": ImageLayerAggregationResponseTypeDef,
        "packageAggregation": PackageAggregationResponseTypeDef,
        "repositoryAggregation": RepositoryAggregationResponseTypeDef,
        "titleAggregation": TitleAggregationResponseTypeDef,
    },
    total=False,
)

AccountStateTypeDef = TypedDict(
    "AccountStateTypeDef",
    {
        "accountId": str,
        "resourceState": ResourceStateTypeDef,
        "state": StateTypeDef,
    },
)

DisableResponseTypeDef = TypedDict(
    "DisableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableResponseTypeDef = TypedDict(
    "EnableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResourceTypeDef = TypedDict(
    "_RequiredResourceTypeDef",
    {
        "id": str,
        "type": ResourceTypeType,
    },
)
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "details": ResourceDetailsTypeDef,
        "partition": str,
        "region": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


ListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "ListCoverageRequestListCoveragePaginateTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCoverageRequestRequestTypeDef = TypedDict(
    "ListCoverageRequestRequestTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef = TypedDict(
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "groupBy": GroupKeyType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "ListCoverageStatisticsRequestRequestTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "groupBy": GroupKeyType,
        "nextToken": str,
    },
    total=False,
)

InspectorScoreDetailsTypeDef = TypedDict(
    "InspectorScoreDetailsTypeDef",
    {
        "adjustedCvss": CvssScoreDetailsTypeDef,
    },
    total=False,
)

AggregationRequestTypeDef = TypedDict(
    "AggregationRequestTypeDef",
    {
        "accountAggregation": AccountAggregationTypeDef,
        "amiAggregation": AmiAggregationTypeDef,
        "awsEcrContainerAggregation": AwsEcrContainerAggregationTypeDef,
        "ec2InstanceAggregation": Ec2InstanceAggregationTypeDef,
        "findingTypeAggregation": FindingTypeAggregationTypeDef,
        "imageLayerAggregation": ImageLayerAggregationTypeDef,
        "packageAggregation": PackageAggregationTypeDef,
        "repositoryAggregation": RepositoryAggregationTypeDef,
        "titleAggregation": TitleAggregationTypeDef,
    },
    total=False,
)

_RequiredCoveredResourceTypeDef = TypedDict(
    "_RequiredCoveredResourceTypeDef",
    {
        "accountId": str,
        "resourceId": str,
        "resourceType": CoverageResourceTypeType,
        "scanType": ScanTypeType,
    },
)
_OptionalCoveredResourceTypeDef = TypedDict(
    "_OptionalCoveredResourceTypeDef",
    {
        "resourceMetadata": ResourceScanMetadataTypeDef,
        "scanStatus": ScanStatusTypeDef,
    },
    total=False,
)


class CoveredResourceTypeDef(_RequiredCoveredResourceTypeDef, _OptionalCoveredResourceTypeDef):
    pass


FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "awsAccountId": Sequence[StringFilterTypeDef],
        "componentId": Sequence[StringFilterTypeDef],
        "componentType": Sequence[StringFilterTypeDef],
        "ec2InstanceImageId": Sequence[StringFilterTypeDef],
        "ec2InstanceSubnetId": Sequence[StringFilterTypeDef],
        "ec2InstanceVpcId": Sequence[StringFilterTypeDef],
        "ecrImageArchitecture": Sequence[StringFilterTypeDef],
        "ecrImageHash": Sequence[StringFilterTypeDef],
        "ecrImagePushedAt": Sequence[DateFilterTypeDef],
        "ecrImageRegistry": Sequence[StringFilterTypeDef],
        "ecrImageRepositoryName": Sequence[StringFilterTypeDef],
        "ecrImageTags": Sequence[StringFilterTypeDef],
        "findingArn": Sequence[StringFilterTypeDef],
        "findingStatus": Sequence[StringFilterTypeDef],
        "findingType": Sequence[StringFilterTypeDef],
        "firstObservedAt": Sequence[DateFilterTypeDef],
        "inspectorScore": Sequence[NumberFilterTypeDef],
        "lastObservedAt": Sequence[DateFilterTypeDef],
        "networkProtocol": Sequence[StringFilterTypeDef],
        "portRange": Sequence[PortRangeFilterTypeDef],
        "relatedVulnerabilities": Sequence[StringFilterTypeDef],
        "resourceId": Sequence[StringFilterTypeDef],
        "resourceTags": Sequence[MapFilterTypeDef],
        "resourceType": Sequence[StringFilterTypeDef],
        "severity": Sequence[StringFilterTypeDef],
        "title": Sequence[StringFilterTypeDef],
        "updatedAt": Sequence[DateFilterTypeDef],
        "vendorSeverity": Sequence[StringFilterTypeDef],
        "vulnerabilityId": Sequence[StringFilterTypeDef],
        "vulnerabilitySource": Sequence[StringFilterTypeDef],
        "vulnerablePackages": Sequence[PackageFilterTypeDef],
    },
    total=False,
)

BatchGetFreeTrialInfoResponseTypeDef = TypedDict(
    "BatchGetFreeTrialInfoResponseTypeDef",
    {
        "accounts": List[FreeTrialAccountInfoTypeDef],
        "failedAccounts": List[FreeTrialInfoErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkReachabilityDetailsTypeDef = TypedDict(
    "NetworkReachabilityDetailsTypeDef",
    {
        "networkPath": NetworkPathTypeDef,
        "openPortRange": PortRangeTypeDef,
        "protocol": NetworkProtocolType,
    },
)

ListUsageTotalsResponseTypeDef = TypedDict(
    "ListUsageTotalsResponseTypeDef",
    {
        "nextToken": str,
        "totals": List[UsageTotalTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingAggregationsResponseTypeDef = TypedDict(
    "ListFindingAggregationsResponseTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "nextToken": str,
        "responses": List[AggregationResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAccountStatusResponseTypeDef = TypedDict(
    "BatchGetAccountStatusResponseTypeDef",
    {
        "accounts": List[AccountStateTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "accountIds": Sequence[StringFilterTypeDef],
        "aggregationRequest": AggregationRequestTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef(
    _RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
    _OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
):
    pass


_RequiredListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestRequestTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[StringFilterTypeDef],
        "aggregationRequest": AggregationRequestTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFindingAggregationsRequestRequestTypeDef(
    _RequiredListFindingAggregationsRequestRequestTypeDef,
    _OptionalListFindingAggregationsRequestRequestTypeDef,
):
    pass


ListCoverageResponseTypeDef = TypedDict(
    "ListCoverageResponseTypeDef",
    {
        "coveredResources": List[CoveredResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "filterCriteria": FilterCriteriaTypeDef,
        "name": str,
    },
)
_OptionalCreateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFilterRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateFilterRequestRequestTypeDef(
    _RequiredCreateFilterRequestRequestTypeDef, _OptionalCreateFilterRequestRequestTypeDef
):
    pass


_RequiredCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFindingsReportRequestRequestTypeDef",
    {
        "reportFormat": ReportFormatType,
        "s3Destination": DestinationTypeDef,
    },
)
_OptionalCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFindingsReportRequestRequestTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
    },
    total=False,
)


class CreateFindingsReportRequestRequestTypeDef(
    _RequiredCreateFindingsReportRequestRequestTypeDef,
    _OptionalCreateFindingsReportRequestRequestTypeDef,
):
    pass


_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "action": FilterActionType,
        "arn": str,
        "createdAt": datetime,
        "criteria": FilterCriteriaTypeDef,
        "name": str,
        "ownerId": str,
        "updatedAt": datetime,
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "description": str,
        "reason": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


GetFindingsReportStatusResponseTypeDef = TypedDict(
    "GetFindingsReportStatusResponseTypeDef",
    {
        "destination": DestinationTypeDef,
        "errorCode": ReportingErrorCodeType,
        "errorMessage": str,
        "filterCriteria": FilterCriteriaTypeDef,
        "reportId": str,
        "status": ExternalReportStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
        "sortCriteria": SortCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
        "maxResults": int,
        "nextToken": str,
        "sortCriteria": SortCriteriaTypeDef,
    },
    total=False,
)

_RequiredUpdateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFilterRequestRequestTypeDef",
    {
        "filterArn": str,
    },
)
_OptionalUpdateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "description": str,
        "filterCriteria": FilterCriteriaTypeDef,
        "name": str,
    },
    total=False,
)


class UpdateFilterRequestRequestTypeDef(
    _RequiredUpdateFilterRequestRequestTypeDef, _OptionalUpdateFilterRequestRequestTypeDef
):
    pass


_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "awsAccountId": str,
        "description": str,
        "findingArn": str,
        "firstObservedAt": datetime,
        "lastObservedAt": datetime,
        "remediation": RemediationTypeDef,
        "resources": List[ResourceTypeDef],
        "severity": SeverityType,
        "status": FindingStatusType,
        "type": FindingTypeType,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "inspectorScore": float,
        "inspectorScoreDetails": InspectorScoreDetailsTypeDef,
        "networkReachabilityDetails": NetworkReachabilityDetailsTypeDef,
        "packageVulnerabilityDetails": PackageVulnerabilityDetailsTypeDef,
        "title": str,
        "updatedAt": datetime,
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "filters": List[FilterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findings": List[FindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
