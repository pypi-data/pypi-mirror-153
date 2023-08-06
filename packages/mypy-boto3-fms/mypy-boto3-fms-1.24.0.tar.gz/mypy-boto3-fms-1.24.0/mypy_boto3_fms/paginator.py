"""
Type annotations for fms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_fms.client import FMSClient
    from mypy_boto3_fms.paginator import (
        ListAppsListsPaginator,
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
        ListProtocolsListsPaginator,
        ListThirdPartyFirewallFirewallPoliciesPaginator,
    )

    session = Session()
    client: FMSClient = session.client("fms")

    list_apps_lists_paginator: ListAppsListsPaginator = client.get_paginator("list_apps_lists")
    list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
    list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_protocols_lists_paginator: ListProtocolsListsPaginator = client.get_paginator("list_protocols_lists")
    list_third_party_firewall_firewall_policies_paginator: ListThirdPartyFirewallFirewallPoliciesPaginator = client.get_paginator("list_third_party_firewall_firewall_policies")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAppsListsResponseTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAppsListsPaginator",
    "ListComplianceStatusPaginator",
    "ListMemberAccountsPaginator",
    "ListPoliciesPaginator",
    "ListProtocolsListsPaginator",
    "ListThirdPartyFirewallFirewallPoliciesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppsListsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListAppsLists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listappslistspaginator)
    """

    def paginate(
        self, *, DefaultLists: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListAppsLists.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listappslistspaginator)
        """


class ListComplianceStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListComplianceStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listcompliancestatuspaginator)
    """

    def paginate(
        self, *, PolicyId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listcompliancestatuspaginator)
        """


class ListMemberAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListMemberAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listmemberaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listmemberaccountspaginator)
        """


class ListPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listpoliciespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listpoliciespaginator)
        """


class ListProtocolsListsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListProtocolsLists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listprotocolslistspaginator)
    """

    def paginate(
        self, *, DefaultLists: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProtocolsListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListProtocolsLists.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listprotocolslistspaginator)
        """


class ListThirdPartyFirewallFirewallPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
    """

    def paginate(
        self,
        *,
        ThirdPartyFirewall: Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListThirdPartyFirewallFirewallPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Paginator.ListThirdPartyFirewallFirewallPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/paginators/#listthirdpartyfirewallfirewallpoliciespaginator)
        """
