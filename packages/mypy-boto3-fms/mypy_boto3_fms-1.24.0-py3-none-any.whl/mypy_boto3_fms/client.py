"""
Type annotations for fms service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_fms.client import FMSClient

    session = Session()
    client: FMSClient = session.client("fms")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAppsListsPaginator,
    ListComplianceStatusPaginator,
    ListMemberAccountsPaginator,
    ListPoliciesPaginator,
    ListProtocolsListsPaginator,
    ListThirdPartyFirewallFirewallPoliciesPaginator,
)
from .type_defs import (
    AppsListDataTypeDef,
    AssociateThirdPartyFirewallResponseTypeDef,
    DisassociateThirdPartyFirewallResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAdminAccountResponseTypeDef,
    GetAppsListResponseTypeDef,
    GetComplianceDetailResponseTypeDef,
    GetNotificationChannelResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetProtectionStatusResponseTypeDef,
    GetProtocolsListResponseTypeDef,
    GetThirdPartyFirewallAssociationStatusResponseTypeDef,
    GetViolationDetailsResponseTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
    PolicyTypeDef,
    ProtocolsListDataTypeDef,
    PutAppsListResponseTypeDef,
    PutPolicyResponseTypeDef,
    PutProtocolsListResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("FMSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class FMSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#exceptions)
        """

    def associate_admin_account(self, *, AdminAccount: str) -> EmptyResponseMetadataTypeDef:
        """
        Sets the Firewall Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.associate_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#associate_admin_account)
        """

    def associate_third_party_firewall(
        self, *, ThirdPartyFirewall: Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"]
    ) -> AssociateThirdPartyFirewallResponseTypeDef:
        """
        Sets the Firewall Manager policy administrator as a tenant administrator of a
        third-party firewall service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.associate_third_party_firewall)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#associate_third_party_firewall)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#can_paginate)
        """

    def delete_apps_list(self, *, ListId: str) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_apps_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#delete_apps_list)
        """

    def delete_notification_channel(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Firewall Manager association with the IAM role and the Amazon Simple
        Notification Service (SNS) topic that is used to record Firewall Manager SNS
        logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_notification_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#delete_notification_channel)
        """

    def delete_policy(
        self, *, PolicyId: str, DeleteAllPolicyResources: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#delete_policy)
        """

    def delete_protocols_list(self, *, ListId: str) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_protocols_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#delete_protocols_list)
        """

    def disassociate_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates the account that has been set as the Firewall Manager
        administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.disassociate_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#disassociate_admin_account)
        """

    def disassociate_third_party_firewall(
        self, *, ThirdPartyFirewall: Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"]
    ) -> DisassociateThirdPartyFirewallResponseTypeDef:
        """
        Disassociates a Firewall Manager policy administrator from a third-party
        firewall tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.disassociate_third_party_firewall)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#disassociate_third_party_firewall)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#generate_presigned_url)
        """

    def get_admin_account(self) -> GetAdminAccountResponseTypeDef:
        """
        Returns the Organizations account that is associated with Firewall Manager as
        the Firewall Manager administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_admin_account)
        """

    def get_apps_list(self, *, ListId: str, DefaultList: bool = ...) -> GetAppsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_apps_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_apps_list)
        """

    def get_compliance_detail(
        self, *, PolicyId: str, MemberAccount: str
    ) -> GetComplianceDetailResponseTypeDef:
        """
        Returns detailed compliance information about the specified member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_compliance_detail)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_compliance_detail)
        """

    def get_notification_channel(self) -> GetNotificationChannelResponseTypeDef:
        """
        Information about the Amazon Simple Notification Service (SNS) topic that is
        used to record Firewall Manager SNS logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_notification_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_notification_channel)
        """

    def get_policy(self, *, PolicyId: str) -> GetPolicyResponseTypeDef:
        """
        Returns information about the specified Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_policy)
        """

    def get_protection_status(
        self,
        *,
        PolicyId: str,
        MemberAccountId: str = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetProtectionStatusResponseTypeDef:
        """
        If you created a Shield Advanced policy, returns policy-level attack summary
        information in the event of a potential DDoS attack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_protection_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_protection_status)
        """

    def get_protocols_list(
        self, *, ListId: str, DefaultList: bool = ...
    ) -> GetProtocolsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_protocols_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_protocols_list)
        """

    def get_third_party_firewall_association_status(
        self, *, ThirdPartyFirewall: Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"]
    ) -> GetThirdPartyFirewallAssociationStatusResponseTypeDef:
        """
        The onboarding status of a Firewall Manager admin account to third-party
        firewall vendor tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_third_party_firewall_association_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_third_party_firewall_association_status)
        """

    def get_violation_details(
        self, *, PolicyId: str, MemberAccount: str, ResourceId: str, ResourceType: str
    ) -> GetViolationDetailsResponseTypeDef:
        """
        Retrieves violations for a resource based on the specified Firewall Manager
        policy and Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_violation_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_violation_details)
        """

    def list_apps_lists(
        self, *, MaxResults: int, DefaultLists: bool = ..., NextToken: str = ...
    ) -> ListAppsListsResponseTypeDef:
        """
        Returns an array of `AppsListDataSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_apps_lists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_apps_lists)
        """

    def list_compliance_status(
        self, *, PolicyId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListComplianceStatusResponseTypeDef:
        """
        Returns an array of `PolicyComplianceStatus` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_compliance_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_compliance_status)
        """

    def list_member_accounts(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMemberAccountsResponseTypeDef:
        """
        Returns a `MemberAccounts` object that lists the member accounts in the
        administrator's Amazon Web Services organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_member_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_member_accounts)
        """

    def list_policies(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPoliciesResponseTypeDef:
        """
        Returns an array of `PolicySummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_policies)
        """

    def list_protocols_lists(
        self, *, MaxResults: int, DefaultLists: bool = ..., NextToken: str = ...
    ) -> ListProtocolsListsResponseTypeDef:
        """
        Returns an array of `ProtocolsListDataSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_protocols_lists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_protocols_lists)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_tags_for_resource)
        """

    def list_third_party_firewall_firewall_policies(
        self,
        *,
        ThirdPartyFirewall: Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
        MaxResults: int,
        NextToken: str = ...
    ) -> ListThirdPartyFirewallFirewallPoliciesResponseTypeDef:
        """
        Retrieves a list of all of the third-party firewall policies that are associated
        with the third-party firewall administrator's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_third_party_firewall_firewall_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#list_third_party_firewall_firewall_policies)
        """

    def put_apps_list(
        self, *, AppsList: AppsListDataTypeDef, TagList: Sequence[TagTypeDef] = ...
    ) -> PutAppsListResponseTypeDef:
        """
        Creates an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_apps_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#put_apps_list)
        """

    def put_notification_channel(
        self, *, SnsTopicArn: str, SnsRoleName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the IAM role and Amazon Simple Notification Service (SNS) topic that
        Firewall Manager uses to record SNS logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_notification_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#put_notification_channel)
        """

    def put_policy(
        self, *, Policy: PolicyTypeDef, TagList: Sequence[TagTypeDef] = ...
    ) -> PutPolicyResponseTypeDef:
        """
        Creates an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#put_policy)
        """

    def put_protocols_list(
        self, *, ProtocolsList: ProtocolsListDataTypeDef, TagList: Sequence[TagTypeDef] = ...
    ) -> PutProtocolsListResponseTypeDef:
        """
        Creates an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_protocols_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#put_protocols_list)
        """

    def tag_resource(self, *, ResourceArn: str, TagList: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#untag_resource)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps_lists"]) -> ListAppsListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_status"]
    ) -> ListComplianceStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_member_accounts"]
    ) -> ListMemberAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protocols_lists"]
    ) -> ListProtocolsListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_third_party_firewall_firewall_policies"]
    ) -> ListThirdPartyFirewallFirewallPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/client/#get_paginator)
        """
