"""
Type annotations for worklink service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/type_defs/)

Usage::

    ```python
    from mypy_boto3_worklink.type_defs import AssociateDomainRequestRequestTypeDef

    data: AssociateDomainRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import DeviceStatusType, DomainStatusType, FleetStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateDomainRequestRequestTypeDef",
    "AssociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DescribeAuditStreamConfigurationRequestRequestTypeDef",
    "DescribeCompanyNetworkConfigurationRequestRequestTypeDef",
    "DescribeDevicePolicyConfigurationRequestRequestTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeFleetMetadataRequestRequestTypeDef",
    "DescribeIdentityProviderConfigurationRequestRequestTypeDef",
    "DescribeWebsiteCertificateAuthorityRequestRequestTypeDef",
    "DeviceSummaryTypeDef",
    "DisassociateDomainRequestRequestTypeDef",
    "DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    "DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    "DomainSummaryTypeDef",
    "FleetSummaryTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebsiteAuthorizationProvidersRequestRequestTypeDef",
    "WebsiteAuthorizationProviderSummaryTypeDef",
    "ListWebsiteCertificateAuthoritiesRequestRequestTypeDef",
    "WebsiteCaSummaryTypeDef",
    "RestoreDomainAccessRequestRequestTypeDef",
    "RevokeDomainAccessRequestRequestTypeDef",
    "SignOutUserRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAuditStreamConfigurationRequestRequestTypeDef",
    "UpdateCompanyNetworkConfigurationRequestRequestTypeDef",
    "UpdateDevicePolicyConfigurationRequestRequestTypeDef",
    "UpdateDomainMetadataRequestRequestTypeDef",
    "UpdateFleetMetadataRequestRequestTypeDef",
    "UpdateIdentityProviderConfigurationRequestRequestTypeDef",
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    "AssociateWebsiteCertificateAuthorityResponseTypeDef",
    "CreateFleetResponseTypeDef",
    "DescribeAuditStreamConfigurationResponseTypeDef",
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    "DescribeDevicePolicyConfigurationResponseTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeFleetMetadataResponseTypeDef",
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListDevicesResponseTypeDef",
    "ListDomainsResponseTypeDef",
    "ListFleetsResponseTypeDef",
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
)

_RequiredAssociateDomainRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
        "AcmCertificateArn": str,
    },
)
_OptionalAssociateDomainRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateDomainRequestRequestTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class AssociateDomainRequestRequestTypeDef(
    _RequiredAssociateDomainRequestRequestTypeDef, _OptionalAssociateDomainRequestRequestTypeDef
):
    pass


_RequiredAssociateWebsiteAuthorizationProviderRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    {
        "FleetArn": str,
        "AuthorizationProviderType": Literal["SAML"],
    },
)
_OptionalAssociateWebsiteAuthorizationProviderRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    {
        "DomainName": str,
    },
    total=False,
)


class AssociateWebsiteAuthorizationProviderRequestRequestTypeDef(
    _RequiredAssociateWebsiteAuthorizationProviderRequestRequestTypeDef,
    _OptionalAssociateWebsiteAuthorizationProviderRequestRequestTypeDef,
):
    pass


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

_RequiredAssociateWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "Certificate": str,
    },
)
_OptionalAssociateWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class AssociateWebsiteCertificateAuthorityRequestRequestTypeDef(
    _RequiredAssociateWebsiteCertificateAuthorityRequestRequestTypeDef,
    _OptionalAssociateWebsiteCertificateAuthorityRequestRequestTypeDef,
):
    pass


_RequiredCreateFleetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
    },
)
_OptionalCreateFleetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetRequestRequestTypeDef",
    {
        "DisplayName": str,
        "OptimizeForEndUserLocation": bool,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateFleetRequestRequestTypeDef(
    _RequiredCreateFleetRequestRequestTypeDef, _OptionalCreateFleetRequestRequestTypeDef
):
    pass


DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeAuditStreamConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeAuditStreamConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeCompanyNetworkConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeCompanyNetworkConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeDevicePolicyConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeDevicePolicyConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeDeviceRequestRequestTypeDef = TypedDict(
    "DescribeDeviceRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DeviceId": str,
    },
)

DescribeDomainRequestRequestTypeDef = TypedDict(
    "DescribeDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)

DescribeFleetMetadataRequestRequestTypeDef = TypedDict(
    "DescribeFleetMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeIdentityProviderConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeIdentityProviderConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)

DescribeWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "DescribeWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "WebsiteCaId": str,
    },
)

DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "DeviceId": str,
        "DeviceStatus": DeviceStatusType,
    },
    total=False,
)

DisassociateDomainRequestRequestTypeDef = TypedDict(
    "DisassociateDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)

DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef = TypedDict(
    "DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    {
        "FleetArn": str,
        "AuthorizationProviderId": str,
    },
)

DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "WebsiteCaId": str,
    },
)

_RequiredDomainSummaryTypeDef = TypedDict(
    "_RequiredDomainSummaryTypeDef",
    {
        "DomainName": str,
        "CreatedTime": datetime,
        "DomainStatus": DomainStatusType,
    },
)
_OptionalDomainSummaryTypeDef = TypedDict(
    "_OptionalDomainSummaryTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class DomainSummaryTypeDef(_RequiredDomainSummaryTypeDef, _OptionalDomainSummaryTypeDef):
    pass


FleetSummaryTypeDef = TypedDict(
    "FleetSummaryTypeDef",
    {
        "FleetArn": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "FleetName": str,
        "DisplayName": str,
        "CompanyCode": str,
        "FleetStatus": FleetStatusType,
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredListDevicesRequestRequestTypeDef = TypedDict(
    "_RequiredListDevicesRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalListDevicesRequestRequestTypeDef = TypedDict(
    "_OptionalListDevicesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDevicesRequestRequestTypeDef(
    _RequiredListDevicesRequestRequestTypeDef, _OptionalListDevicesRequestRequestTypeDef
):
    pass


_RequiredListDomainsRequestRequestTypeDef = TypedDict(
    "_RequiredListDomainsRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalListDomainsRequestRequestTypeDef = TypedDict(
    "_OptionalListDomainsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDomainsRequestRequestTypeDef(
    _RequiredListDomainsRequestRequestTypeDef, _OptionalListDomainsRequestRequestTypeDef
):
    pass


ListFleetsRequestRequestTypeDef = TypedDict(
    "ListFleetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListWebsiteAuthorizationProvidersRequestRequestTypeDef = TypedDict(
    "_RequiredListWebsiteAuthorizationProvidersRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalListWebsiteAuthorizationProvidersRequestRequestTypeDef = TypedDict(
    "_OptionalListWebsiteAuthorizationProvidersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListWebsiteAuthorizationProvidersRequestRequestTypeDef(
    _RequiredListWebsiteAuthorizationProvidersRequestRequestTypeDef,
    _OptionalListWebsiteAuthorizationProvidersRequestRequestTypeDef,
):
    pass


_RequiredWebsiteAuthorizationProviderSummaryTypeDef = TypedDict(
    "_RequiredWebsiteAuthorizationProviderSummaryTypeDef",
    {
        "AuthorizationProviderType": Literal["SAML"],
    },
)
_OptionalWebsiteAuthorizationProviderSummaryTypeDef = TypedDict(
    "_OptionalWebsiteAuthorizationProviderSummaryTypeDef",
    {
        "AuthorizationProviderId": str,
        "DomainName": str,
        "CreatedTime": datetime,
    },
    total=False,
)


class WebsiteAuthorizationProviderSummaryTypeDef(
    _RequiredWebsiteAuthorizationProviderSummaryTypeDef,
    _OptionalWebsiteAuthorizationProviderSummaryTypeDef,
):
    pass


_RequiredListWebsiteCertificateAuthoritiesRequestRequestTypeDef = TypedDict(
    "_RequiredListWebsiteCertificateAuthoritiesRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalListWebsiteCertificateAuthoritiesRequestRequestTypeDef = TypedDict(
    "_OptionalListWebsiteCertificateAuthoritiesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListWebsiteCertificateAuthoritiesRequestRequestTypeDef(
    _RequiredListWebsiteCertificateAuthoritiesRequestRequestTypeDef,
    _OptionalListWebsiteCertificateAuthoritiesRequestRequestTypeDef,
):
    pass


WebsiteCaSummaryTypeDef = TypedDict(
    "WebsiteCaSummaryTypeDef",
    {
        "WebsiteCaId": str,
        "CreatedTime": datetime,
        "DisplayName": str,
    },
    total=False,
)

RestoreDomainAccessRequestRequestTypeDef = TypedDict(
    "RestoreDomainAccessRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)

RevokeDomainAccessRequestRequestTypeDef = TypedDict(
    "RevokeDomainAccessRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)

SignOutUserRequestRequestTypeDef = TypedDict(
    "SignOutUserRequestRequestTypeDef",
    {
        "FleetArn": str,
        "Username": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAuditStreamConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAuditStreamConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalUpdateAuditStreamConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAuditStreamConfigurationRequestRequestTypeDef",
    {
        "AuditStreamArn": str,
    },
    total=False,
)


class UpdateAuditStreamConfigurationRequestRequestTypeDef(
    _RequiredUpdateAuditStreamConfigurationRequestRequestTypeDef,
    _OptionalUpdateAuditStreamConfigurationRequestRequestTypeDef,
):
    pass


UpdateCompanyNetworkConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateCompanyNetworkConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
)

_RequiredUpdateDevicePolicyConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDevicePolicyConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalUpdateDevicePolicyConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDevicePolicyConfigurationRequestRequestTypeDef",
    {
        "DeviceCaCertificate": str,
    },
    total=False,
)


class UpdateDevicePolicyConfigurationRequestRequestTypeDef(
    _RequiredUpdateDevicePolicyConfigurationRequestRequestTypeDef,
    _OptionalUpdateDevicePolicyConfigurationRequestRequestTypeDef,
):
    pass


_RequiredUpdateDomainMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)
_OptionalUpdateDomainMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainMetadataRequestRequestTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)


class UpdateDomainMetadataRequestRequestTypeDef(
    _RequiredUpdateDomainMetadataRequestRequestTypeDef,
    _OptionalUpdateDomainMetadataRequestRequestTypeDef,
):
    pass


_RequiredUpdateFleetMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFleetMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
_OptionalUpdateFleetMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFleetMetadataRequestRequestTypeDef",
    {
        "DisplayName": str,
        "OptimizeForEndUserLocation": bool,
    },
    total=False,
)


class UpdateFleetMetadataRequestRequestTypeDef(
    _RequiredUpdateFleetMetadataRequestRequestTypeDef,
    _OptionalUpdateFleetMetadataRequestRequestTypeDef,
):
    pass


_RequiredUpdateIdentityProviderConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIdentityProviderConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "IdentityProviderType": Literal["SAML"],
    },
)
_OptionalUpdateIdentityProviderConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIdentityProviderConfigurationRequestRequestTypeDef",
    {
        "IdentityProviderSamlMetadata": str,
    },
    total=False,
)


class UpdateIdentityProviderConfigurationRequestRequestTypeDef(
    _RequiredUpdateIdentityProviderConfigurationRequestRequestTypeDef,
    _OptionalUpdateIdentityProviderConfigurationRequestRequestTypeDef,
):
    pass


AssociateWebsiteAuthorizationProviderResponseTypeDef = TypedDict(
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    {
        "AuthorizationProviderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "AssociateWebsiteCertificateAuthorityResponseTypeDef",
    {
        "WebsiteCaId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFleetResponseTypeDef = TypedDict(
    "CreateFleetResponseTypeDef",
    {
        "FleetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAuditStreamConfigurationResponseTypeDef = TypedDict(
    "DescribeAuditStreamConfigurationResponseTypeDef",
    {
        "AuditStreamArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCompanyNetworkConfigurationResponseTypeDef = TypedDict(
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    {
        "VpcId": str,
        "SubnetIds": List[str],
        "SecurityGroupIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDevicePolicyConfigurationResponseTypeDef = TypedDict(
    "DescribeDevicePolicyConfigurationResponseTypeDef",
    {
        "DeviceCaCertificate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDeviceResponseTypeDef = TypedDict(
    "DescribeDeviceResponseTypeDef",
    {
        "Status": DeviceStatusType,
        "Model": str,
        "Manufacturer": str,
        "OperatingSystem": str,
        "OperatingSystemVersion": str,
        "PatchLevel": str,
        "FirstAccessedTime": datetime,
        "LastAccessedTime": datetime,
        "Username": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "DomainName": str,
        "DisplayName": str,
        "CreatedTime": datetime,
        "DomainStatus": DomainStatusType,
        "AcmCertificateArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetMetadataResponseTypeDef = TypedDict(
    "DescribeFleetMetadataResponseTypeDef",
    {
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "FleetName": str,
        "DisplayName": str,
        "OptimizeForEndUserLocation": bool,
        "CompanyCode": str,
        "FleetStatus": FleetStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIdentityProviderConfigurationResponseTypeDef = TypedDict(
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    {
        "IdentityProviderType": Literal["SAML"],
        "ServiceProviderSamlMetadata": str,
        "IdentityProviderSamlMetadata": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    {
        "Certificate": str,
        "CreatedTime": datetime,
        "DisplayName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDevicesResponseTypeDef = TypedDict(
    "ListDevicesResponseTypeDef",
    {
        "Devices": List[DeviceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "Domains": List[DomainSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFleetsResponseTypeDef = TypedDict(
    "ListFleetsResponseTypeDef",
    {
        "FleetSummaryList": List[FleetSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWebsiteAuthorizationProvidersResponseTypeDef = TypedDict(
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    {
        "WebsiteAuthorizationProviders": List[WebsiteAuthorizationProviderSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWebsiteCertificateAuthoritiesResponseTypeDef = TypedDict(
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
    {
        "WebsiteCertificateAuthorities": List[WebsiteCaSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
