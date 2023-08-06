"""
Type annotations for license-manager service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_license_manager/type_defs/)

Usage::

    ```python
    from mypy_boto3_license_manager.type_defs import AcceptGrantRequestRequestTypeDef

    data: AcceptGrantRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AllowedOperationType,
    CheckoutTypeType,
    EntitlementDataUnitType,
    EntitlementUnitType,
    GrantStatusType,
    InventoryFilterConditionType,
    LicenseConfigurationStatusType,
    LicenseConversionTaskStatusType,
    LicenseCountingTypeType,
    LicenseDeletionStatusType,
    LicenseStatusType,
    ReceivedStatusType,
    RenewTypeType,
    ReportFrequencyTypeType,
    ReportTypeType,
    ResourceTypeType,
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
    "AcceptGrantRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AutomatedDiscoveryInformationTypeDef",
    "BorrowConfigurationTypeDef",
    "CheckInLicenseRequestRequestTypeDef",
    "EntitlementDataTypeDef",
    "MetadataTypeDef",
    "ConsumedLicenseSummaryTypeDef",
    "ProvisionalConfigurationTypeDef",
    "CreateGrantRequestRequestTypeDef",
    "CreateGrantVersionRequestRequestTypeDef",
    "TagTypeDef",
    "LicenseConversionContextTypeDef",
    "ReportContextTypeDef",
    "ReportFrequencyTypeDef",
    "DatetimeRangeTypeDef",
    "EntitlementTypeDef",
    "IssuerTypeDef",
    "CreateTokenRequestRequestTypeDef",
    "DeleteGrantRequestRequestTypeDef",
    "DeleteLicenseConfigurationRequestRequestTypeDef",
    "DeleteLicenseManagerReportGeneratorRequestRequestTypeDef",
    "DeleteLicenseRequestRequestTypeDef",
    "DeleteTokenRequestRequestTypeDef",
    "EntitlementUsageTypeDef",
    "ExtendLicenseConsumptionRequestRequestTypeDef",
    "FilterTypeDef",
    "GetAccessTokenRequestRequestTypeDef",
    "GetGrantRequestRequestTypeDef",
    "GrantTypeDef",
    "GetLicenseConfigurationRequestRequestTypeDef",
    "ManagedResourceSummaryTypeDef",
    "GetLicenseConversionTaskRequestRequestTypeDef",
    "GetLicenseManagerReportGeneratorRequestRequestTypeDef",
    "GetLicenseRequestRequestTypeDef",
    "GetLicenseUsageRequestRequestTypeDef",
    "OrganizationConfigurationTypeDef",
    "IssuerDetailsTypeDef",
    "ReceivedMetadataTypeDef",
    "InventoryFilterTypeDef",
    "LicenseConfigurationAssociationTypeDef",
    "LicenseConfigurationUsageTypeDef",
    "LicenseSpecificationTypeDef",
    "PaginatorConfigTypeDef",
    "ListAssociationsForLicenseConfigurationRequestRequestTypeDef",
    "ListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef",
    "ListLicenseSpecificationsForResourceRequestRequestTypeDef",
    "ListLicenseVersionsRequestRequestTypeDef",
    "ResourceInventoryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TokenDataTypeDef",
    "ProductInformationFilterTypeDef",
    "RejectGrantRequestRequestTypeDef",
    "S3LocationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AcceptGrantResponseTypeDef",
    "CreateGrantResponseTypeDef",
    "CreateGrantVersionResponseTypeDef",
    "CreateLicenseConfigurationResponseTypeDef",
    "CreateLicenseConversionTaskForResourceResponseTypeDef",
    "CreateLicenseManagerReportGeneratorResponseTypeDef",
    "CreateLicenseResponseTypeDef",
    "CreateLicenseVersionResponseTypeDef",
    "CreateTokenResponseTypeDef",
    "DeleteGrantResponseTypeDef",
    "DeleteLicenseResponseTypeDef",
    "ExtendLicenseConsumptionResponseTypeDef",
    "GetAccessTokenResponseTypeDef",
    "RejectGrantResponseTypeDef",
    "CheckoutLicenseRequestRequestTypeDef",
    "CheckoutLicenseResponseTypeDef",
    "CheckoutBorrowLicenseRequestRequestTypeDef",
    "CheckoutBorrowLicenseResponseTypeDef",
    "LicenseOperationFailureTypeDef",
    "ConsumptionConfigurationTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateLicenseConversionTaskForResourceRequestRequestTypeDef",
    "GetLicenseConversionTaskResponseTypeDef",
    "LicenseConversionTaskTypeDef",
    "CreateLicenseManagerReportGeneratorRequestRequestTypeDef",
    "UpdateLicenseManagerReportGeneratorRequestRequestTypeDef",
    "LicenseUsageTypeDef",
    "ListDistributedGrantsRequestRequestTypeDef",
    "ListLicenseConfigurationsRequestRequestTypeDef",
    "ListLicenseConversionTasksRequestRequestTypeDef",
    "ListLicenseManagerReportGeneratorsRequestRequestTypeDef",
    "ListLicensesRequestRequestTypeDef",
    "ListReceivedGrantsRequestRequestTypeDef",
    "ListReceivedLicensesRequestRequestTypeDef",
    "ListTokensRequestRequestTypeDef",
    "ListUsageForLicenseConfigurationRequestRequestTypeDef",
    "GetGrantResponseTypeDef",
    "ListDistributedGrantsResponseTypeDef",
    "ListReceivedGrantsResponseTypeDef",
    "GetServiceSettingsResponseTypeDef",
    "UpdateServiceSettingsRequestRequestTypeDef",
    "ListResourceInventoryRequestRequestTypeDef",
    "ListAssociationsForLicenseConfigurationResponseTypeDef",
    "ListUsageForLicenseConfigurationResponseTypeDef",
    "ListLicenseSpecificationsForResourceResponseTypeDef",
    "UpdateLicenseSpecificationsForResourceRequestRequestTypeDef",
    "ListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef",
    "ListLicenseConfigurationsRequestListLicenseConfigurationsPaginateTypeDef",
    "ListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef",
    "ListResourceInventoryRequestListResourceInventoryPaginateTypeDef",
    "ListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef",
    "ListResourceInventoryResponseTypeDef",
    "ListTokensResponseTypeDef",
    "ProductInformationTypeDef",
    "ReportGeneratorTypeDef",
    "ListFailuresForLicenseConfigurationOperationsResponseTypeDef",
    "CreateLicenseRequestRequestTypeDef",
    "CreateLicenseVersionRequestRequestTypeDef",
    "GrantedLicenseTypeDef",
    "LicenseTypeDef",
    "ListLicenseConversionTasksResponseTypeDef",
    "GetLicenseUsageResponseTypeDef",
    "CreateLicenseConfigurationRequestRequestTypeDef",
    "GetLicenseConfigurationResponseTypeDef",
    "LicenseConfigurationTypeDef",
    "UpdateLicenseConfigurationRequestRequestTypeDef",
    "GetLicenseManagerReportGeneratorResponseTypeDef",
    "ListLicenseManagerReportGeneratorsResponseTypeDef",
    "ListReceivedLicensesResponseTypeDef",
    "GetLicenseResponseTypeDef",
    "ListLicenseVersionsResponseTypeDef",
    "ListLicensesResponseTypeDef",
    "ListLicenseConfigurationsResponseTypeDef",
)

AcceptGrantRequestRequestTypeDef = TypedDict(
    "AcceptGrantRequestRequestTypeDef",
    {
        "GrantArn": str,
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

AutomatedDiscoveryInformationTypeDef = TypedDict(
    "AutomatedDiscoveryInformationTypeDef",
    {
        "LastRunTime": datetime,
    },
    total=False,
)

BorrowConfigurationTypeDef = TypedDict(
    "BorrowConfigurationTypeDef",
    {
        "AllowEarlyCheckIn": bool,
        "MaxTimeToLiveInMinutes": int,
    },
)

_RequiredCheckInLicenseRequestRequestTypeDef = TypedDict(
    "_RequiredCheckInLicenseRequestRequestTypeDef",
    {
        "LicenseConsumptionToken": str,
    },
)
_OptionalCheckInLicenseRequestRequestTypeDef = TypedDict(
    "_OptionalCheckInLicenseRequestRequestTypeDef",
    {
        "Beneficiary": str,
    },
    total=False,
)


class CheckInLicenseRequestRequestTypeDef(
    _RequiredCheckInLicenseRequestRequestTypeDef, _OptionalCheckInLicenseRequestRequestTypeDef
):
    pass


_RequiredEntitlementDataTypeDef = TypedDict(
    "_RequiredEntitlementDataTypeDef",
    {
        "Name": str,
        "Unit": EntitlementDataUnitType,
    },
)
_OptionalEntitlementDataTypeDef = TypedDict(
    "_OptionalEntitlementDataTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class EntitlementDataTypeDef(_RequiredEntitlementDataTypeDef, _OptionalEntitlementDataTypeDef):
    pass


MetadataTypeDef = TypedDict(
    "MetadataTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

ConsumedLicenseSummaryTypeDef = TypedDict(
    "ConsumedLicenseSummaryTypeDef",
    {
        "ResourceType": ResourceTypeType,
        "ConsumedLicenses": int,
    },
    total=False,
)

ProvisionalConfigurationTypeDef = TypedDict(
    "ProvisionalConfigurationTypeDef",
    {
        "MaxTimeToLiveInMinutes": int,
    },
)

CreateGrantRequestRequestTypeDef = TypedDict(
    "CreateGrantRequestRequestTypeDef",
    {
        "ClientToken": str,
        "GrantName": str,
        "LicenseArn": str,
        "Principals": Sequence[str],
        "HomeRegion": str,
        "AllowedOperations": Sequence[AllowedOperationType],
    },
)

_RequiredCreateGrantVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGrantVersionRequestRequestTypeDef",
    {
        "ClientToken": str,
        "GrantArn": str,
    },
)
_OptionalCreateGrantVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGrantVersionRequestRequestTypeDef",
    {
        "GrantName": str,
        "AllowedOperations": Sequence[AllowedOperationType],
        "Status": GrantStatusType,
        "StatusReason": str,
        "SourceVersion": str,
    },
    total=False,
)


class CreateGrantVersionRequestRequestTypeDef(
    _RequiredCreateGrantVersionRequestRequestTypeDef,
    _OptionalCreateGrantVersionRequestRequestTypeDef,
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

LicenseConversionContextTypeDef = TypedDict(
    "LicenseConversionContextTypeDef",
    {
        "UsageOperation": str,
    },
    total=False,
)

ReportContextTypeDef = TypedDict(
    "ReportContextTypeDef",
    {
        "licenseConfigurationArns": Sequence[str],
    },
)

ReportFrequencyTypeDef = TypedDict(
    "ReportFrequencyTypeDef",
    {
        "value": int,
        "period": ReportFrequencyTypeType,
    },
    total=False,
)

_RequiredDatetimeRangeTypeDef = TypedDict(
    "_RequiredDatetimeRangeTypeDef",
    {
        "Begin": str,
    },
)
_OptionalDatetimeRangeTypeDef = TypedDict(
    "_OptionalDatetimeRangeTypeDef",
    {
        "End": str,
    },
    total=False,
)


class DatetimeRangeTypeDef(_RequiredDatetimeRangeTypeDef, _OptionalDatetimeRangeTypeDef):
    pass


_RequiredEntitlementTypeDef = TypedDict(
    "_RequiredEntitlementTypeDef",
    {
        "Name": str,
        "Unit": EntitlementUnitType,
    },
)
_OptionalEntitlementTypeDef = TypedDict(
    "_OptionalEntitlementTypeDef",
    {
        "Value": str,
        "MaxCount": int,
        "Overage": bool,
        "AllowCheckIn": bool,
    },
    total=False,
)


class EntitlementTypeDef(_RequiredEntitlementTypeDef, _OptionalEntitlementTypeDef):
    pass


_RequiredIssuerTypeDef = TypedDict(
    "_RequiredIssuerTypeDef",
    {
        "Name": str,
    },
)
_OptionalIssuerTypeDef = TypedDict(
    "_OptionalIssuerTypeDef",
    {
        "SignKey": str,
    },
    total=False,
)


class IssuerTypeDef(_RequiredIssuerTypeDef, _OptionalIssuerTypeDef):
    pass


_RequiredCreateTokenRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTokenRequestRequestTypeDef",
    {
        "LicenseArn": str,
        "ClientToken": str,
    },
)
_OptionalCreateTokenRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTokenRequestRequestTypeDef",
    {
        "RoleArns": Sequence[str],
        "ExpirationInDays": int,
        "TokenProperties": Sequence[str],
    },
    total=False,
)


class CreateTokenRequestRequestTypeDef(
    _RequiredCreateTokenRequestRequestTypeDef, _OptionalCreateTokenRequestRequestTypeDef
):
    pass


_RequiredDeleteGrantRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteGrantRequestRequestTypeDef",
    {
        "GrantArn": str,
        "Version": str,
    },
)
_OptionalDeleteGrantRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteGrantRequestRequestTypeDef",
    {
        "StatusReason": str,
    },
    total=False,
)


class DeleteGrantRequestRequestTypeDef(
    _RequiredDeleteGrantRequestRequestTypeDef, _OptionalDeleteGrantRequestRequestTypeDef
):
    pass


DeleteLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)

DeleteLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "DeleteLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "LicenseManagerReportGeneratorArn": str,
    },
)

DeleteLicenseRequestRequestTypeDef = TypedDict(
    "DeleteLicenseRequestRequestTypeDef",
    {
        "LicenseArn": str,
        "SourceVersion": str,
    },
)

DeleteTokenRequestRequestTypeDef = TypedDict(
    "DeleteTokenRequestRequestTypeDef",
    {
        "TokenId": str,
    },
)

_RequiredEntitlementUsageTypeDef = TypedDict(
    "_RequiredEntitlementUsageTypeDef",
    {
        "Name": str,
        "ConsumedValue": str,
        "Unit": EntitlementDataUnitType,
    },
)
_OptionalEntitlementUsageTypeDef = TypedDict(
    "_OptionalEntitlementUsageTypeDef",
    {
        "MaxCount": str,
    },
    total=False,
)


class EntitlementUsageTypeDef(_RequiredEntitlementUsageTypeDef, _OptionalEntitlementUsageTypeDef):
    pass


_RequiredExtendLicenseConsumptionRequestRequestTypeDef = TypedDict(
    "_RequiredExtendLicenseConsumptionRequestRequestTypeDef",
    {
        "LicenseConsumptionToken": str,
    },
)
_OptionalExtendLicenseConsumptionRequestRequestTypeDef = TypedDict(
    "_OptionalExtendLicenseConsumptionRequestRequestTypeDef",
    {
        "DryRun": bool,
    },
    total=False,
)


class ExtendLicenseConsumptionRequestRequestTypeDef(
    _RequiredExtendLicenseConsumptionRequestRequestTypeDef,
    _OptionalExtendLicenseConsumptionRequestRequestTypeDef,
):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

_RequiredGetAccessTokenRequestRequestTypeDef = TypedDict(
    "_RequiredGetAccessTokenRequestRequestTypeDef",
    {
        "Token": str,
    },
)
_OptionalGetAccessTokenRequestRequestTypeDef = TypedDict(
    "_OptionalGetAccessTokenRequestRequestTypeDef",
    {
        "TokenProperties": Sequence[str],
    },
    total=False,
)


class GetAccessTokenRequestRequestTypeDef(
    _RequiredGetAccessTokenRequestRequestTypeDef, _OptionalGetAccessTokenRequestRequestTypeDef
):
    pass


_RequiredGetGrantRequestRequestTypeDef = TypedDict(
    "_RequiredGetGrantRequestRequestTypeDef",
    {
        "GrantArn": str,
    },
)
_OptionalGetGrantRequestRequestTypeDef = TypedDict(
    "_OptionalGetGrantRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetGrantRequestRequestTypeDef(
    _RequiredGetGrantRequestRequestTypeDef, _OptionalGetGrantRequestRequestTypeDef
):
    pass


_RequiredGrantTypeDef = TypedDict(
    "_RequiredGrantTypeDef",
    {
        "GrantArn": str,
        "GrantName": str,
        "ParentArn": str,
        "LicenseArn": str,
        "GranteePrincipalArn": str,
        "HomeRegion": str,
        "GrantStatus": GrantStatusType,
        "Version": str,
        "GrantedOperations": List[AllowedOperationType],
    },
)
_OptionalGrantTypeDef = TypedDict(
    "_OptionalGrantTypeDef",
    {
        "StatusReason": str,
    },
    total=False,
)


class GrantTypeDef(_RequiredGrantTypeDef, _OptionalGrantTypeDef):
    pass


GetLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "GetLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)

ManagedResourceSummaryTypeDef = TypedDict(
    "ManagedResourceSummaryTypeDef",
    {
        "ResourceType": ResourceTypeType,
        "AssociationCount": int,
    },
    total=False,
)

GetLicenseConversionTaskRequestRequestTypeDef = TypedDict(
    "GetLicenseConversionTaskRequestRequestTypeDef",
    {
        "LicenseConversionTaskId": str,
    },
)

GetLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "GetLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "LicenseManagerReportGeneratorArn": str,
    },
)

_RequiredGetLicenseRequestRequestTypeDef = TypedDict(
    "_RequiredGetLicenseRequestRequestTypeDef",
    {
        "LicenseArn": str,
    },
)
_OptionalGetLicenseRequestRequestTypeDef = TypedDict(
    "_OptionalGetLicenseRequestRequestTypeDef",
    {
        "Version": str,
    },
    total=False,
)


class GetLicenseRequestRequestTypeDef(
    _RequiredGetLicenseRequestRequestTypeDef, _OptionalGetLicenseRequestRequestTypeDef
):
    pass


GetLicenseUsageRequestRequestTypeDef = TypedDict(
    "GetLicenseUsageRequestRequestTypeDef",
    {
        "LicenseArn": str,
    },
)

OrganizationConfigurationTypeDef = TypedDict(
    "OrganizationConfigurationTypeDef",
    {
        "EnableIntegration": bool,
    },
)

IssuerDetailsTypeDef = TypedDict(
    "IssuerDetailsTypeDef",
    {
        "Name": str,
        "SignKey": str,
        "KeyFingerprint": str,
    },
    total=False,
)

ReceivedMetadataTypeDef = TypedDict(
    "ReceivedMetadataTypeDef",
    {
        "ReceivedStatus": ReceivedStatusType,
        "ReceivedStatusReason": str,
        "AllowedOperations": List[AllowedOperationType],
    },
    total=False,
)

_RequiredInventoryFilterTypeDef = TypedDict(
    "_RequiredInventoryFilterTypeDef",
    {
        "Name": str,
        "Condition": InventoryFilterConditionType,
    },
)
_OptionalInventoryFilterTypeDef = TypedDict(
    "_OptionalInventoryFilterTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class InventoryFilterTypeDef(_RequiredInventoryFilterTypeDef, _OptionalInventoryFilterTypeDef):
    pass


LicenseConfigurationAssociationTypeDef = TypedDict(
    "LicenseConfigurationAssociationTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": ResourceTypeType,
        "ResourceOwnerId": str,
        "AssociationTime": datetime,
        "AmiAssociationScope": str,
    },
    total=False,
)

LicenseConfigurationUsageTypeDef = TypedDict(
    "LicenseConfigurationUsageTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": ResourceTypeType,
        "ResourceStatus": str,
        "ResourceOwnerId": str,
        "AssociationTime": datetime,
        "ConsumedLicenses": int,
    },
    total=False,
)

_RequiredLicenseSpecificationTypeDef = TypedDict(
    "_RequiredLicenseSpecificationTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalLicenseSpecificationTypeDef = TypedDict(
    "_OptionalLicenseSpecificationTypeDef",
    {
        "AmiAssociationScope": str,
    },
    total=False,
)


class LicenseSpecificationTypeDef(
    _RequiredLicenseSpecificationTypeDef, _OptionalLicenseSpecificationTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListAssociationsForLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociationsForLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalListAssociationsForLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociationsForLicenseConfigurationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAssociationsForLicenseConfigurationRequestRequestTypeDef(
    _RequiredListAssociationsForLicenseConfigurationRequestRequestTypeDef,
    _OptionalListAssociationsForLicenseConfigurationRequestRequestTypeDef,
):
    pass


_RequiredListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef = TypedDict(
    "_RequiredListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef = TypedDict(
    "_OptionalListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef(
    _RequiredListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef,
    _OptionalListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef,
):
    pass


_RequiredListLicenseSpecificationsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListLicenseSpecificationsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListLicenseSpecificationsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListLicenseSpecificationsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListLicenseSpecificationsForResourceRequestRequestTypeDef(
    _RequiredListLicenseSpecificationsForResourceRequestRequestTypeDef,
    _OptionalListLicenseSpecificationsForResourceRequestRequestTypeDef,
):
    pass


_RequiredListLicenseVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListLicenseVersionsRequestRequestTypeDef",
    {
        "LicenseArn": str,
    },
)
_OptionalListLicenseVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListLicenseVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListLicenseVersionsRequestRequestTypeDef(
    _RequiredListLicenseVersionsRequestRequestTypeDef,
    _OptionalListLicenseVersionsRequestRequestTypeDef,
):
    pass


ResourceInventoryTypeDef = TypedDict(
    "ResourceInventoryTypeDef",
    {
        "ResourceId": str,
        "ResourceType": ResourceTypeType,
        "ResourceArn": str,
        "Platform": str,
        "PlatformVersion": str,
        "ResourceOwningAccountId": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

TokenDataTypeDef = TypedDict(
    "TokenDataTypeDef",
    {
        "TokenId": str,
        "TokenType": str,
        "LicenseArn": str,
        "ExpirationTime": str,
        "TokenProperties": List[str],
        "RoleArns": List[str],
        "Status": str,
    },
    total=False,
)

_RequiredProductInformationFilterTypeDef = TypedDict(
    "_RequiredProductInformationFilterTypeDef",
    {
        "ProductInformationFilterName": str,
        "ProductInformationFilterComparator": str,
    },
)
_OptionalProductInformationFilterTypeDef = TypedDict(
    "_OptionalProductInformationFilterTypeDef",
    {
        "ProductInformationFilterValue": Sequence[str],
    },
    total=False,
)


class ProductInformationFilterTypeDef(
    _RequiredProductInformationFilterTypeDef, _OptionalProductInformationFilterTypeDef
):
    pass


RejectGrantRequestRequestTypeDef = TypedDict(
    "RejectGrantRequestRequestTypeDef",
    {
        "GrantArn": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": str,
        "keyPrefix": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

AcceptGrantResponseTypeDef = TypedDict(
    "AcceptGrantResponseTypeDef",
    {
        "GrantArn": str,
        "Status": GrantStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGrantResponseTypeDef = TypedDict(
    "CreateGrantResponseTypeDef",
    {
        "GrantArn": str,
        "Status": GrantStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGrantVersionResponseTypeDef = TypedDict(
    "CreateGrantVersionResponseTypeDef",
    {
        "GrantArn": str,
        "Status": GrantStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLicenseConfigurationResponseTypeDef = TypedDict(
    "CreateLicenseConfigurationResponseTypeDef",
    {
        "LicenseConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLicenseConversionTaskForResourceResponseTypeDef = TypedDict(
    "CreateLicenseConversionTaskForResourceResponseTypeDef",
    {
        "LicenseConversionTaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLicenseManagerReportGeneratorResponseTypeDef = TypedDict(
    "CreateLicenseManagerReportGeneratorResponseTypeDef",
    {
        "LicenseManagerReportGeneratorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLicenseResponseTypeDef = TypedDict(
    "CreateLicenseResponseTypeDef",
    {
        "LicenseArn": str,
        "Status": LicenseStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLicenseVersionResponseTypeDef = TypedDict(
    "CreateLicenseVersionResponseTypeDef",
    {
        "LicenseArn": str,
        "Version": str,
        "Status": LicenseStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTokenResponseTypeDef = TypedDict(
    "CreateTokenResponseTypeDef",
    {
        "TokenId": str,
        "TokenType": Literal["REFRESH_TOKEN"],
        "Token": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGrantResponseTypeDef = TypedDict(
    "DeleteGrantResponseTypeDef",
    {
        "GrantArn": str,
        "Status": GrantStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteLicenseResponseTypeDef = TypedDict(
    "DeleteLicenseResponseTypeDef",
    {
        "Status": LicenseDeletionStatusType,
        "DeletionDate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExtendLicenseConsumptionResponseTypeDef = TypedDict(
    "ExtendLicenseConsumptionResponseTypeDef",
    {
        "LicenseConsumptionToken": str,
        "Expiration": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessTokenResponseTypeDef = TypedDict(
    "GetAccessTokenResponseTypeDef",
    {
        "AccessToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RejectGrantResponseTypeDef = TypedDict(
    "RejectGrantResponseTypeDef",
    {
        "GrantArn": str,
        "Status": GrantStatusType,
        "Version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCheckoutLicenseRequestRequestTypeDef = TypedDict(
    "_RequiredCheckoutLicenseRequestRequestTypeDef",
    {
        "ProductSKU": str,
        "CheckoutType": CheckoutTypeType,
        "KeyFingerprint": str,
        "Entitlements": Sequence[EntitlementDataTypeDef],
        "ClientToken": str,
    },
)
_OptionalCheckoutLicenseRequestRequestTypeDef = TypedDict(
    "_OptionalCheckoutLicenseRequestRequestTypeDef",
    {
        "Beneficiary": str,
        "NodeId": str,
    },
    total=False,
)


class CheckoutLicenseRequestRequestTypeDef(
    _RequiredCheckoutLicenseRequestRequestTypeDef, _OptionalCheckoutLicenseRequestRequestTypeDef
):
    pass


CheckoutLicenseResponseTypeDef = TypedDict(
    "CheckoutLicenseResponseTypeDef",
    {
        "CheckoutType": CheckoutTypeType,
        "LicenseConsumptionToken": str,
        "EntitlementsAllowed": List[EntitlementDataTypeDef],
        "SignedToken": str,
        "NodeId": str,
        "IssuedAt": str,
        "Expiration": str,
        "LicenseArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCheckoutBorrowLicenseRequestRequestTypeDef = TypedDict(
    "_RequiredCheckoutBorrowLicenseRequestRequestTypeDef",
    {
        "LicenseArn": str,
        "Entitlements": Sequence[EntitlementDataTypeDef],
        "DigitalSignatureMethod": Literal["JWT_PS384"],
        "ClientToken": str,
    },
)
_OptionalCheckoutBorrowLicenseRequestRequestTypeDef = TypedDict(
    "_OptionalCheckoutBorrowLicenseRequestRequestTypeDef",
    {
        "NodeId": str,
        "CheckoutMetadata": Sequence[MetadataTypeDef],
    },
    total=False,
)


class CheckoutBorrowLicenseRequestRequestTypeDef(
    _RequiredCheckoutBorrowLicenseRequestRequestTypeDef,
    _OptionalCheckoutBorrowLicenseRequestRequestTypeDef,
):
    pass


CheckoutBorrowLicenseResponseTypeDef = TypedDict(
    "CheckoutBorrowLicenseResponseTypeDef",
    {
        "LicenseArn": str,
        "LicenseConsumptionToken": str,
        "EntitlementsAllowed": List[EntitlementDataTypeDef],
        "NodeId": str,
        "SignedToken": str,
        "IssuedAt": str,
        "Expiration": str,
        "CheckoutMetadata": List[MetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LicenseOperationFailureTypeDef = TypedDict(
    "LicenseOperationFailureTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": ResourceTypeType,
        "ErrorMessage": str,
        "FailureTime": datetime,
        "OperationName": str,
        "ResourceOwnerId": str,
        "OperationRequestedBy": str,
        "MetadataList": List[MetadataTypeDef],
    },
    total=False,
)

ConsumptionConfigurationTypeDef = TypedDict(
    "ConsumptionConfigurationTypeDef",
    {
        "RenewType": RenewTypeType,
        "ProvisionalConfiguration": ProvisionalConfigurationTypeDef,
        "BorrowConfiguration": BorrowConfigurationTypeDef,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateLicenseConversionTaskForResourceRequestRequestTypeDef = TypedDict(
    "CreateLicenseConversionTaskForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "SourceLicenseContext": LicenseConversionContextTypeDef,
        "DestinationLicenseContext": LicenseConversionContextTypeDef,
    },
)

GetLicenseConversionTaskResponseTypeDef = TypedDict(
    "GetLicenseConversionTaskResponseTypeDef",
    {
        "LicenseConversionTaskId": str,
        "ResourceArn": str,
        "SourceLicenseContext": LicenseConversionContextTypeDef,
        "DestinationLicenseContext": LicenseConversionContextTypeDef,
        "StatusMessage": str,
        "Status": LicenseConversionTaskStatusType,
        "StartTime": datetime,
        "LicenseConversionTime": datetime,
        "EndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LicenseConversionTaskTypeDef = TypedDict(
    "LicenseConversionTaskTypeDef",
    {
        "LicenseConversionTaskId": str,
        "ResourceArn": str,
        "SourceLicenseContext": LicenseConversionContextTypeDef,
        "DestinationLicenseContext": LicenseConversionContextTypeDef,
        "Status": LicenseConversionTaskStatusType,
        "StatusMessage": str,
        "StartTime": datetime,
        "LicenseConversionTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

_RequiredCreateLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "ReportGeneratorName": str,
        "Type": Sequence[ReportTypeType],
        "ReportContext": ReportContextTypeDef,
        "ReportFrequency": ReportFrequencyTypeDef,
        "ClientToken": str,
    },
)
_OptionalCreateLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateLicenseManagerReportGeneratorRequestRequestTypeDef(
    _RequiredCreateLicenseManagerReportGeneratorRequestRequestTypeDef,
    _OptionalCreateLicenseManagerReportGeneratorRequestRequestTypeDef,
):
    pass


_RequiredUpdateLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "LicenseManagerReportGeneratorArn": str,
        "ReportGeneratorName": str,
        "Type": Sequence[ReportTypeType],
        "ReportContext": ReportContextTypeDef,
        "ReportFrequency": ReportFrequencyTypeDef,
        "ClientToken": str,
    },
)
_OptionalUpdateLicenseManagerReportGeneratorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLicenseManagerReportGeneratorRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateLicenseManagerReportGeneratorRequestRequestTypeDef(
    _RequiredUpdateLicenseManagerReportGeneratorRequestRequestTypeDef,
    _OptionalUpdateLicenseManagerReportGeneratorRequestRequestTypeDef,
):
    pass


LicenseUsageTypeDef = TypedDict(
    "LicenseUsageTypeDef",
    {
        "EntitlementUsages": List[EntitlementUsageTypeDef],
    },
    total=False,
)

ListDistributedGrantsRequestRequestTypeDef = TypedDict(
    "ListDistributedGrantsRequestRequestTypeDef",
    {
        "GrantArns": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListLicenseConfigurationsRequestRequestTypeDef = TypedDict(
    "ListLicenseConfigurationsRequestRequestTypeDef",
    {
        "LicenseConfigurationArns": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListLicenseConversionTasksRequestRequestTypeDef = TypedDict(
    "ListLicenseConversionTasksRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListLicenseManagerReportGeneratorsRequestRequestTypeDef = TypedDict(
    "ListLicenseManagerReportGeneratorsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListLicensesRequestRequestTypeDef = TypedDict(
    "ListLicensesRequestRequestTypeDef",
    {
        "LicenseArns": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListReceivedGrantsRequestRequestTypeDef = TypedDict(
    "ListReceivedGrantsRequestRequestTypeDef",
    {
        "GrantArns": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListReceivedLicensesRequestRequestTypeDef = TypedDict(
    "ListReceivedLicensesRequestRequestTypeDef",
    {
        "LicenseArns": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTokensRequestRequestTypeDef = TypedDict(
    "ListTokensRequestRequestTypeDef",
    {
        "TokenIds": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListUsageForLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredListUsageForLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalListUsageForLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalListUsageForLicenseConfigurationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListUsageForLicenseConfigurationRequestRequestTypeDef(
    _RequiredListUsageForLicenseConfigurationRequestRequestTypeDef,
    _OptionalListUsageForLicenseConfigurationRequestRequestTypeDef,
):
    pass


GetGrantResponseTypeDef = TypedDict(
    "GetGrantResponseTypeDef",
    {
        "Grant": GrantTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributedGrantsResponseTypeDef = TypedDict(
    "ListDistributedGrantsResponseTypeDef",
    {
        "Grants": List[GrantTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReceivedGrantsResponseTypeDef = TypedDict(
    "ListReceivedGrantsResponseTypeDef",
    {
        "Grants": List[GrantTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceSettingsResponseTypeDef = TypedDict(
    "GetServiceSettingsResponseTypeDef",
    {
        "S3BucketArn": str,
        "SnsTopicArn": str,
        "OrganizationConfiguration": OrganizationConfigurationTypeDef,
        "EnableCrossAccountsDiscovery": bool,
        "LicenseManagerResourceShareArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceSettingsRequestRequestTypeDef = TypedDict(
    "UpdateServiceSettingsRequestRequestTypeDef",
    {
        "S3BucketArn": str,
        "SnsTopicArn": str,
        "OrganizationConfiguration": OrganizationConfigurationTypeDef,
        "EnableCrossAccountsDiscovery": bool,
    },
    total=False,
)

ListResourceInventoryRequestRequestTypeDef = TypedDict(
    "ListResourceInventoryRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[InventoryFilterTypeDef],
    },
    total=False,
)

ListAssociationsForLicenseConfigurationResponseTypeDef = TypedDict(
    "ListAssociationsForLicenseConfigurationResponseTypeDef",
    {
        "LicenseConfigurationAssociations": List[LicenseConfigurationAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsageForLicenseConfigurationResponseTypeDef = TypedDict(
    "ListUsageForLicenseConfigurationResponseTypeDef",
    {
        "LicenseConfigurationUsageList": List[LicenseConfigurationUsageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLicenseSpecificationsForResourceResponseTypeDef = TypedDict(
    "ListLicenseSpecificationsForResourceResponseTypeDef",
    {
        "LicenseSpecifications": List[LicenseSpecificationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLicenseSpecificationsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLicenseSpecificationsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalUpdateLicenseSpecificationsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLicenseSpecificationsForResourceRequestRequestTypeDef",
    {
        "AddLicenseSpecifications": Sequence[LicenseSpecificationTypeDef],
        "RemoveLicenseSpecifications": Sequence[LicenseSpecificationTypeDef],
    },
    total=False,
)


class UpdateLicenseSpecificationsForResourceRequestRequestTypeDef(
    _RequiredUpdateLicenseSpecificationsForResourceRequestRequestTypeDef,
    _OptionalUpdateLicenseSpecificationsForResourceRequestRequestTypeDef,
):
    pass


_RequiredListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef = TypedDict(
    "_RequiredListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef = TypedDict(
    "_OptionalListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef(
    _RequiredListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef,
    _OptionalListAssociationsForLicenseConfigurationRequestListAssociationsForLicenseConfigurationPaginateTypeDef,
):
    pass


ListLicenseConfigurationsRequestListLicenseConfigurationsPaginateTypeDef = TypedDict(
    "ListLicenseConfigurationsRequestListLicenseConfigurationsPaginateTypeDef",
    {
        "LicenseConfigurationArns": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef(
    _RequiredListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef,
    _OptionalListLicenseSpecificationsForResourceRequestListLicenseSpecificationsForResourcePaginateTypeDef,
):
    pass


ListResourceInventoryRequestListResourceInventoryPaginateTypeDef = TypedDict(
    "ListResourceInventoryRequestListResourceInventoryPaginateTypeDef",
    {
        "Filters": Sequence[InventoryFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef = TypedDict(
    "_RequiredListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef = TypedDict(
    "_OptionalListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef(
    _RequiredListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef,
    _OptionalListUsageForLicenseConfigurationRequestListUsageForLicenseConfigurationPaginateTypeDef,
):
    pass


ListResourceInventoryResponseTypeDef = TypedDict(
    "ListResourceInventoryResponseTypeDef",
    {
        "ResourceInventoryList": List[ResourceInventoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTokensResponseTypeDef = TypedDict(
    "ListTokensResponseTypeDef",
    {
        "Tokens": List[TokenDataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProductInformationTypeDef = TypedDict(
    "ProductInformationTypeDef",
    {
        "ResourceType": str,
        "ProductInformationFilterList": Sequence[ProductInformationFilterTypeDef],
    },
)

ReportGeneratorTypeDef = TypedDict(
    "ReportGeneratorTypeDef",
    {
        "ReportGeneratorName": str,
        "ReportType": List[ReportTypeType],
        "ReportContext": ReportContextTypeDef,
        "ReportFrequency": ReportFrequencyTypeDef,
        "LicenseManagerReportGeneratorArn": str,
        "LastRunStatus": str,
        "LastRunFailureReason": str,
        "LastReportGenerationTime": str,
        "ReportCreatorAccount": str,
        "Description": str,
        "S3Location": S3LocationTypeDef,
        "CreateTime": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ListFailuresForLicenseConfigurationOperationsResponseTypeDef = TypedDict(
    "ListFailuresForLicenseConfigurationOperationsResponseTypeDef",
    {
        "LicenseOperationFailureList": List[LicenseOperationFailureTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLicenseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLicenseRequestRequestTypeDef",
    {
        "LicenseName": str,
        "ProductName": str,
        "ProductSKU": str,
        "Issuer": IssuerTypeDef,
        "HomeRegion": str,
        "Validity": DatetimeRangeTypeDef,
        "Entitlements": Sequence[EntitlementTypeDef],
        "Beneficiary": str,
        "ConsumptionConfiguration": ConsumptionConfigurationTypeDef,
        "ClientToken": str,
    },
)
_OptionalCreateLicenseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLicenseRequestRequestTypeDef",
    {
        "LicenseMetadata": Sequence[MetadataTypeDef],
    },
    total=False,
)


class CreateLicenseRequestRequestTypeDef(
    _RequiredCreateLicenseRequestRequestTypeDef, _OptionalCreateLicenseRequestRequestTypeDef
):
    pass


_RequiredCreateLicenseVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLicenseVersionRequestRequestTypeDef",
    {
        "LicenseArn": str,
        "LicenseName": str,
        "ProductName": str,
        "Issuer": IssuerTypeDef,
        "HomeRegion": str,
        "Validity": DatetimeRangeTypeDef,
        "Entitlements": Sequence[EntitlementTypeDef],
        "ConsumptionConfiguration": ConsumptionConfigurationTypeDef,
        "Status": LicenseStatusType,
        "ClientToken": str,
    },
)
_OptionalCreateLicenseVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLicenseVersionRequestRequestTypeDef",
    {
        "LicenseMetadata": Sequence[MetadataTypeDef],
        "SourceVersion": str,
    },
    total=False,
)


class CreateLicenseVersionRequestRequestTypeDef(
    _RequiredCreateLicenseVersionRequestRequestTypeDef,
    _OptionalCreateLicenseVersionRequestRequestTypeDef,
):
    pass


GrantedLicenseTypeDef = TypedDict(
    "GrantedLicenseTypeDef",
    {
        "LicenseArn": str,
        "LicenseName": str,
        "ProductName": str,
        "ProductSKU": str,
        "Issuer": IssuerDetailsTypeDef,
        "HomeRegion": str,
        "Status": LicenseStatusType,
        "Validity": DatetimeRangeTypeDef,
        "Beneficiary": str,
        "Entitlements": List[EntitlementTypeDef],
        "ConsumptionConfiguration": ConsumptionConfigurationTypeDef,
        "LicenseMetadata": List[MetadataTypeDef],
        "CreateTime": str,
        "Version": str,
        "ReceivedMetadata": ReceivedMetadataTypeDef,
    },
    total=False,
)

LicenseTypeDef = TypedDict(
    "LicenseTypeDef",
    {
        "LicenseArn": str,
        "LicenseName": str,
        "ProductName": str,
        "ProductSKU": str,
        "Issuer": IssuerDetailsTypeDef,
        "HomeRegion": str,
        "Status": LicenseStatusType,
        "Validity": DatetimeRangeTypeDef,
        "Beneficiary": str,
        "Entitlements": List[EntitlementTypeDef],
        "ConsumptionConfiguration": ConsumptionConfigurationTypeDef,
        "LicenseMetadata": List[MetadataTypeDef],
        "CreateTime": str,
        "Version": str,
    },
    total=False,
)

ListLicenseConversionTasksResponseTypeDef = TypedDict(
    "ListLicenseConversionTasksResponseTypeDef",
    {
        "LicenseConversionTasks": List[LicenseConversionTaskTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLicenseUsageResponseTypeDef = TypedDict(
    "GetLicenseUsageResponseTypeDef",
    {
        "LicenseUsage": LicenseUsageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLicenseConfigurationRequestRequestTypeDef",
    {
        "Name": str,
        "LicenseCountingType": LicenseCountingTypeType,
    },
)
_OptionalCreateLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLicenseConfigurationRequestRequestTypeDef",
    {
        "Description": str,
        "LicenseCount": int,
        "LicenseCountHardLimit": bool,
        "LicenseRules": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "DisassociateWhenNotFound": bool,
        "ProductInformationList": Sequence[ProductInformationTypeDef],
    },
    total=False,
)


class CreateLicenseConfigurationRequestRequestTypeDef(
    _RequiredCreateLicenseConfigurationRequestRequestTypeDef,
    _OptionalCreateLicenseConfigurationRequestRequestTypeDef,
):
    pass


GetLicenseConfigurationResponseTypeDef = TypedDict(
    "GetLicenseConfigurationResponseTypeDef",
    {
        "LicenseConfigurationId": str,
        "LicenseConfigurationArn": str,
        "Name": str,
        "Description": str,
        "LicenseCountingType": LicenseCountingTypeType,
        "LicenseRules": List[str],
        "LicenseCount": int,
        "LicenseCountHardLimit": bool,
        "ConsumedLicenses": int,
        "Status": str,
        "OwnerAccountId": str,
        "ConsumedLicenseSummaryList": List[ConsumedLicenseSummaryTypeDef],
        "ManagedResourceSummaryList": List[ManagedResourceSummaryTypeDef],
        "Tags": List[TagTypeDef],
        "ProductInformationList": List[ProductInformationTypeDef],
        "AutomatedDiscoveryInformation": AutomatedDiscoveryInformationTypeDef,
        "DisassociateWhenNotFound": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LicenseConfigurationTypeDef = TypedDict(
    "LicenseConfigurationTypeDef",
    {
        "LicenseConfigurationId": str,
        "LicenseConfigurationArn": str,
        "Name": str,
        "Description": str,
        "LicenseCountingType": LicenseCountingTypeType,
        "LicenseRules": List[str],
        "LicenseCount": int,
        "LicenseCountHardLimit": bool,
        "DisassociateWhenNotFound": bool,
        "ConsumedLicenses": int,
        "Status": str,
        "OwnerAccountId": str,
        "ConsumedLicenseSummaryList": List[ConsumedLicenseSummaryTypeDef],
        "ManagedResourceSummaryList": List[ManagedResourceSummaryTypeDef],
        "ProductInformationList": List[ProductInformationTypeDef],
        "AutomatedDiscoveryInformation": AutomatedDiscoveryInformationTypeDef,
    },
    total=False,
)

_RequiredUpdateLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
)
_OptionalUpdateLicenseConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLicenseConfigurationRequestRequestTypeDef",
    {
        "LicenseConfigurationStatus": LicenseConfigurationStatusType,
        "LicenseRules": Sequence[str],
        "LicenseCount": int,
        "LicenseCountHardLimit": bool,
        "Name": str,
        "Description": str,
        "ProductInformationList": Sequence[ProductInformationTypeDef],
        "DisassociateWhenNotFound": bool,
    },
    total=False,
)


class UpdateLicenseConfigurationRequestRequestTypeDef(
    _RequiredUpdateLicenseConfigurationRequestRequestTypeDef,
    _OptionalUpdateLicenseConfigurationRequestRequestTypeDef,
):
    pass


GetLicenseManagerReportGeneratorResponseTypeDef = TypedDict(
    "GetLicenseManagerReportGeneratorResponseTypeDef",
    {
        "ReportGenerator": ReportGeneratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLicenseManagerReportGeneratorsResponseTypeDef = TypedDict(
    "ListLicenseManagerReportGeneratorsResponseTypeDef",
    {
        "ReportGenerators": List[ReportGeneratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReceivedLicensesResponseTypeDef = TypedDict(
    "ListReceivedLicensesResponseTypeDef",
    {
        "Licenses": List[GrantedLicenseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLicenseResponseTypeDef = TypedDict(
    "GetLicenseResponseTypeDef",
    {
        "License": LicenseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLicenseVersionsResponseTypeDef = TypedDict(
    "ListLicenseVersionsResponseTypeDef",
    {
        "Licenses": List[LicenseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLicensesResponseTypeDef = TypedDict(
    "ListLicensesResponseTypeDef",
    {
        "Licenses": List[LicenseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLicenseConfigurationsResponseTypeDef = TypedDict(
    "ListLicenseConfigurationsResponseTypeDef",
    {
        "LicenseConfigurations": List[LicenseConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
