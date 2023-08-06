"""
Type annotations for worklink service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_worklink.client import WorkLinkClient

    session = Session()
    client: WorkLinkClient = session.client("worklink")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateWebsiteAuthorizationProviderResponseTypeDef,
    AssociateWebsiteCertificateAuthorityResponseTypeDef,
    CreateFleetResponseTypeDef,
    DescribeAuditStreamConfigurationResponseTypeDef,
    DescribeCompanyNetworkConfigurationResponseTypeDef,
    DescribeDevicePolicyConfigurationResponseTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeFleetMetadataResponseTypeDef,
    DescribeIdentityProviderConfigurationResponseTypeDef,
    DescribeWebsiteCertificateAuthorityResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebsiteAuthorizationProvidersResponseTypeDef,
    ListWebsiteCertificateAuthoritiesResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("WorkLinkClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class WorkLinkClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkLinkClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#exceptions)
        """

    def associate_domain(
        self, *, FleetArn: str, DomainName: str, AcmCertificateArn: str, DisplayName: str = ...
    ) -> Dict[str, Any]:
        """
        Specifies a domain to be associated to Amazon WorkLink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.associate_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#associate_domain)
        """

    def associate_website_authorization_provider(
        self, *, FleetArn: str, AuthorizationProviderType: Literal["SAML"], DomainName: str = ...
    ) -> AssociateWebsiteAuthorizationProviderResponseTypeDef:
        """
        Associates a website authorization provider with a specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.associate_website_authorization_provider)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#associate_website_authorization_provider)
        """

    def associate_website_certificate_authority(
        self, *, FleetArn: str, Certificate: str, DisplayName: str = ...
    ) -> AssociateWebsiteCertificateAuthorityResponseTypeDef:
        """
        Imports the root certificate of a certificate authority (CA) used to obtain TLS
        certificates used by associated websites within the company network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.associate_website_certificate_authority)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#associate_website_certificate_authority)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#can_paginate)
        """

    def create_fleet(
        self,
        *,
        FleetName: str,
        DisplayName: str = ...,
        OptimizeForEndUserLocation: bool = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.create_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#create_fleet)
        """

    def delete_fleet(self, *, FleetArn: str) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.delete_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#delete_fleet)
        """

    def describe_audit_stream_configuration(
        self, *, FleetArn: str
    ) -> DescribeAuditStreamConfigurationResponseTypeDef:
        """
        Describes the configuration for delivering audit streams to the customer
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_audit_stream_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_audit_stream_configuration)
        """

    def describe_company_network_configuration(
        self, *, FleetArn: str
    ) -> DescribeCompanyNetworkConfigurationResponseTypeDef:
        """
        Describes the networking configuration to access the internal websites
        associated with the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_company_network_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_company_network_configuration)
        """

    def describe_device(self, *, FleetArn: str, DeviceId: str) -> DescribeDeviceResponseTypeDef:
        """
        Provides information about a user's device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_device)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_device)
        """

    def describe_device_policy_configuration(
        self, *, FleetArn: str
    ) -> DescribeDevicePolicyConfigurationResponseTypeDef:
        """
        Describes the device policy configuration for the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_device_policy_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_device_policy_configuration)
        """

    def describe_domain(self, *, FleetArn: str, DomainName: str) -> DescribeDomainResponseTypeDef:
        """
        Provides information about the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_domain)
        """

    def describe_fleet_metadata(self, *, FleetArn: str) -> DescribeFleetMetadataResponseTypeDef:
        """
        Provides basic information for the specified fleet, excluding identity provider,
        networking, and device configuration details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_fleet_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_fleet_metadata)
        """

    def describe_identity_provider_configuration(
        self, *, FleetArn: str
    ) -> DescribeIdentityProviderConfigurationResponseTypeDef:
        """
        Describes the identity provider configuration of the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_identity_provider_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_identity_provider_configuration)
        """

    def describe_website_certificate_authority(
        self, *, FleetArn: str, WebsiteCaId: str
    ) -> DescribeWebsiteCertificateAuthorityResponseTypeDef:
        """
        Provides information about the certificate authority.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.describe_website_certificate_authority)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#describe_website_certificate_authority)
        """

    def disassociate_domain(self, *, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        Disassociates a domain from Amazon WorkLink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.disassociate_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#disassociate_domain)
        """

    def disassociate_website_authorization_provider(
        self, *, FleetArn: str, AuthorizationProviderId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a website authorization provider from a specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.disassociate_website_authorization_provider)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#disassociate_website_authorization_provider)
        """

    def disassociate_website_certificate_authority(
        self, *, FleetArn: str, WebsiteCaId: str
    ) -> Dict[str, Any]:
        """
        Removes a certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.disassociate_website_certificate_authority)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#disassociate_website_certificate_authority)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#generate_presigned_url)
        """

    def list_devices(
        self, *, FleetArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDevicesResponseTypeDef:
        """
        Retrieves a list of devices registered with the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_devices)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_devices)
        """

    def list_domains(
        self, *, FleetArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDomainsResponseTypeDef:
        """
        Retrieves a list of domains associated to a specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_domains)
        """

    def list_fleets(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFleetsResponseTypeDef:
        """
        Retrieves a list of fleets for the current account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_fleets)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_tags_for_resource)
        """

    def list_website_authorization_providers(
        self, *, FleetArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWebsiteAuthorizationProvidersResponseTypeDef:
        """
        Retrieves a list of website authorization providers associated with a specified
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_website_authorization_providers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_website_authorization_providers)
        """

    def list_website_certificate_authorities(
        self, *, FleetArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListWebsiteCertificateAuthoritiesResponseTypeDef:
        """
        Retrieves a list of certificate authorities added for the current account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.list_website_certificate_authorities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#list_website_certificate_authorities)
        """

    def restore_domain_access(self, *, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        Moves a domain to ACTIVE status if it was in the INACTIVE status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.restore_domain_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#restore_domain_access)
        """

    def revoke_domain_access(self, *, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        Moves a domain to INACTIVE status if it was in the ACTIVE status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.revoke_domain_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#revoke_domain_access)
        """

    def sign_out_user(self, *, FleetArn: str, Username: str) -> Dict[str, Any]:
        """
        Signs the user out from all of their devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.sign_out_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#sign_out_user)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource, such as a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#untag_resource)
        """

    def update_audit_stream_configuration(
        self, *, FleetArn: str, AuditStreamArn: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the audit stream configuration for the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_audit_stream_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_audit_stream_configuration)
        """

    def update_company_network_configuration(
        self,
        *,
        FleetArn: str,
        VpcId: str,
        SubnetIds: Sequence[str],
        SecurityGroupIds: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Updates the company network configuration for the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_company_network_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_company_network_configuration)
        """

    def update_device_policy_configuration(
        self, *, FleetArn: str, DeviceCaCertificate: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the device policy configuration for the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_device_policy_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_device_policy_configuration)
        """

    def update_domain_metadata(
        self, *, FleetArn: str, DomainName: str, DisplayName: str = ...
    ) -> Dict[str, Any]:
        """
        Updates domain metadata, such as DisplayName.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_domain_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_domain_metadata)
        """

    def update_fleet_metadata(
        self, *, FleetArn: str, DisplayName: str = ..., OptimizeForEndUserLocation: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates fleet metadata, such as DisplayName.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_fleet_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_fleet_metadata)
        """

    def update_identity_provider_configuration(
        self,
        *,
        FleetArn: str,
        IdentityProviderType: Literal["SAML"],
        IdentityProviderSamlMetadata: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the identity provider configuration for the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink.Client.update_identity_provider_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_worklink/client/#update_identity_provider_configuration)
        """
