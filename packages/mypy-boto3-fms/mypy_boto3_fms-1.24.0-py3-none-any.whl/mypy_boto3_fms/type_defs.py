"""
Type annotations for fms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/type_defs/)

Usage::

    ```python
    from mypy_boto3_fms.type_defs import ActionTargetTypeDef

    data: ActionTargetTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AccountRoleStatusType,
    CustomerPolicyScopeIdTypeType,
    DependentServiceNameType,
    DestinationTypeType,
    FirewallDeploymentModelType,
    MarketplaceSubscriptionOnboardingStatusType,
    PolicyComplianceStatusTypeType,
    RemediationActionTypeType,
    SecurityServiceTypeType,
    TargetTypeType,
    ThirdPartyFirewallAssociationStatusType,
    ViolationReasonType,
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
    "ActionTargetTypeDef",
    "AppTypeDef",
    "AssociateAdminAccountRequestRequestTypeDef",
    "AssociateThirdPartyFirewallRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AwsEc2NetworkInterfaceViolationTypeDef",
    "PartialMatchTypeDef",
    "ComplianceViolatorTypeDef",
    "DeleteAppsListRequestRequestTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeleteProtocolsListRequestRequestTypeDef",
    "DisassociateThirdPartyFirewallRequestRequestTypeDef",
    "DnsDuplicateRuleGroupViolationTypeDef",
    "DnsRuleGroupLimitExceededViolationTypeDef",
    "DnsRuleGroupPriorityConflictViolationTypeDef",
    "EvaluationResultTypeDef",
    "ExpectedRouteTypeDef",
    "FMSPolicyUpdateFirewallCreationConfigActionTypeDef",
    "FirewallSubnetIsOutOfScopeViolationTypeDef",
    "FirewallSubnetMissingVPCEndpointViolationTypeDef",
    "GetAppsListRequestRequestTypeDef",
    "GetComplianceDetailRequestRequestTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetProtectionStatusRequestRequestTypeDef",
    "GetProtocolsListRequestRequestTypeDef",
    "ProtocolsListDataTypeDef",
    "GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef",
    "GetViolationDetailsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAppsListsRequestRequestTypeDef",
    "ListComplianceStatusRequestRequestTypeDef",
    "ListMemberAccountsRequestRequestTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "PolicySummaryTypeDef",
    "ListProtocolsListsRequestRequestTypeDef",
    "ProtocolsListDataSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef",
    "ThirdPartyFirewallFirewallPolicyTypeDef",
    "RouteTypeDef",
    "NetworkFirewallMissingExpectedRTViolationTypeDef",
    "NetworkFirewallMissingFirewallViolationTypeDef",
    "NetworkFirewallMissingSubnetViolationTypeDef",
    "StatefulRuleGroupTypeDef",
    "StatelessRuleGroupTypeDef",
    "NetworkFirewallPolicyTypeDef",
    "ThirdPartyFirewallPolicyTypeDef",
    "ResourceTagTypeDef",
    "PutNotificationChannelRequestRequestTypeDef",
    "ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef",
    "ThirdPartyFirewallMissingFirewallViolationTypeDef",
    "ThirdPartyFirewallMissingSubnetViolationTypeDef",
    "SecurityGroupRuleDescriptionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "EC2AssociateRouteTableActionTypeDef",
    "EC2CopyRouteTableActionTypeDef",
    "EC2CreateRouteActionTypeDef",
    "EC2CreateRouteTableActionTypeDef",
    "EC2DeleteRouteActionTypeDef",
    "EC2ReplaceRouteActionTypeDef",
    "EC2ReplaceRouteTableAssociationActionTypeDef",
    "AppsListDataSummaryTypeDef",
    "AppsListDataTypeDef",
    "AssociateThirdPartyFirewallResponseTypeDef",
    "DisassociateThirdPartyFirewallResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAdminAccountResponseTypeDef",
    "GetNotificationChannelResponseTypeDef",
    "GetProtectionStatusResponseTypeDef",
    "GetThirdPartyFirewallAssociationStatusResponseTypeDef",
    "ListMemberAccountsResponseTypeDef",
    "AwsEc2InstanceViolationTypeDef",
    "PolicyComplianceDetailTypeDef",
    "PolicyComplianceStatusTypeDef",
    "NetworkFirewallMissingExpectedRoutesViolationTypeDef",
    "GetProtocolsListResponseTypeDef",
    "PutProtocolsListResponseTypeDef",
    "ListAppsListsRequestListAppsListsPaginateTypeDef",
    "ListComplianceStatusRequestListComplianceStatusPaginateTypeDef",
    "ListMemberAccountsRequestListMemberAccountsPaginateTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListProtocolsListsRequestListProtocolsListsPaginateTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListProtocolsListsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutProtocolsListRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesResponseTypeDef",
    "NetworkFirewallBlackHoleRouteDetectedViolationTypeDef",
    "NetworkFirewallInternetTrafficNotInspectedViolationTypeDef",
    "NetworkFirewallInvalidRouteConfigurationViolationTypeDef",
    "NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef",
    "NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef",
    "RouteHasOutOfScopeEndpointViolationTypeDef",
    "NetworkFirewallPolicyDescriptionTypeDef",
    "PolicyOptionTypeDef",
    "SecurityGroupRemediationActionTypeDef",
    "RemediationActionTypeDef",
    "ListAppsListsResponseTypeDef",
    "GetAppsListResponseTypeDef",
    "PutAppsListRequestRequestTypeDef",
    "PutAppsListResponseTypeDef",
    "GetComplianceDetailResponseTypeDef",
    "ListComplianceStatusResponseTypeDef",
    "NetworkFirewallPolicyModifiedViolationTypeDef",
    "SecurityServicePolicyDataTypeDef",
    "AwsVPCSecurityGroupViolationTypeDef",
    "RemediationActionWithOrderTypeDef",
    "PolicyTypeDef",
    "PossibleRemediationActionTypeDef",
    "GetPolicyResponseTypeDef",
    "PutPolicyRequestRequestTypeDef",
    "PutPolicyResponseTypeDef",
    "PossibleRemediationActionsTypeDef",
    "ResourceViolationTypeDef",
    "ViolationDetailTypeDef",
    "GetViolationDetailsResponseTypeDef",
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef",
    {
        "ResourceId": str,
        "Description": str,
    },
    total=False,
)

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "AppName": str,
        "Protocol": str,
        "Port": int,
    },
)

AssociateAdminAccountRequestRequestTypeDef = TypedDict(
    "AssociateAdminAccountRequestRequestTypeDef",
    {
        "AdminAccount": str,
    },
)

AssociateThirdPartyFirewallRequestRequestTypeDef = TypedDict(
    "AssociateThirdPartyFirewallRequestRequestTypeDef",
    {
        "ThirdPartyFirewall": Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
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

AwsEc2NetworkInterfaceViolationTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceViolationTypeDef",
    {
        "ViolationTarget": str,
        "ViolatingSecurityGroups": List[str],
    },
    total=False,
)

PartialMatchTypeDef = TypedDict(
    "PartialMatchTypeDef",
    {
        "Reference": str,
        "TargetViolationReasons": List[str],
    },
    total=False,
)

ComplianceViolatorTypeDef = TypedDict(
    "ComplianceViolatorTypeDef",
    {
        "ResourceId": str,
        "ViolationReason": ViolationReasonType,
        "ResourceType": str,
        "Metadata": Dict[str, str],
    },
    total=False,
)

DeleteAppsListRequestRequestTypeDef = TypedDict(
    "DeleteAppsListRequestRequestTypeDef",
    {
        "ListId": str,
    },
)

_RequiredDeletePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalDeletePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePolicyRequestRequestTypeDef",
    {
        "DeleteAllPolicyResources": bool,
    },
    total=False,
)


class DeletePolicyRequestRequestTypeDef(
    _RequiredDeletePolicyRequestRequestTypeDef, _OptionalDeletePolicyRequestRequestTypeDef
):
    pass


DeleteProtocolsListRequestRequestTypeDef = TypedDict(
    "DeleteProtocolsListRequestRequestTypeDef",
    {
        "ListId": str,
    },
)

DisassociateThirdPartyFirewallRequestRequestTypeDef = TypedDict(
    "DisassociateThirdPartyFirewallRequestRequestTypeDef",
    {
        "ThirdPartyFirewall": Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
    },
)

DnsDuplicateRuleGroupViolationTypeDef = TypedDict(
    "DnsDuplicateRuleGroupViolationTypeDef",
    {
        "ViolationTarget": str,
        "ViolationTargetDescription": str,
    },
    total=False,
)

DnsRuleGroupLimitExceededViolationTypeDef = TypedDict(
    "DnsRuleGroupLimitExceededViolationTypeDef",
    {
        "ViolationTarget": str,
        "ViolationTargetDescription": str,
        "NumberOfRuleGroupsAlreadyAssociated": int,
    },
    total=False,
)

DnsRuleGroupPriorityConflictViolationTypeDef = TypedDict(
    "DnsRuleGroupPriorityConflictViolationTypeDef",
    {
        "ViolationTarget": str,
        "ViolationTargetDescription": str,
        "ConflictingPriority": int,
        "ConflictingPolicyId": str,
        "UnavailablePriorities": List[int],
    },
    total=False,
)

EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {
        "ComplianceStatus": PolicyComplianceStatusTypeType,
        "ViolatorCount": int,
        "EvaluationLimitExceeded": bool,
    },
    total=False,
)

ExpectedRouteTypeDef = TypedDict(
    "ExpectedRouteTypeDef",
    {
        "IpV4Cidr": str,
        "PrefixListId": str,
        "IpV6Cidr": str,
        "ContributingSubnets": List[str],
        "AllowedTargets": List[str],
        "RouteTableId": str,
    },
    total=False,
)

FMSPolicyUpdateFirewallCreationConfigActionTypeDef = TypedDict(
    "FMSPolicyUpdateFirewallCreationConfigActionTypeDef",
    {
        "Description": str,
        "FirewallCreationConfig": str,
    },
    total=False,
)

FirewallSubnetIsOutOfScopeViolationTypeDef = TypedDict(
    "FirewallSubnetIsOutOfScopeViolationTypeDef",
    {
        "FirewallSubnetId": str,
        "VpcId": str,
        "SubnetAvailabilityZone": str,
        "SubnetAvailabilityZoneId": str,
        "VpcEndpointId": str,
    },
    total=False,
)

FirewallSubnetMissingVPCEndpointViolationTypeDef = TypedDict(
    "FirewallSubnetMissingVPCEndpointViolationTypeDef",
    {
        "FirewallSubnetId": str,
        "VpcId": str,
        "SubnetAvailabilityZone": str,
        "SubnetAvailabilityZoneId": str,
    },
    total=False,
)

_RequiredGetAppsListRequestRequestTypeDef = TypedDict(
    "_RequiredGetAppsListRequestRequestTypeDef",
    {
        "ListId": str,
    },
)
_OptionalGetAppsListRequestRequestTypeDef = TypedDict(
    "_OptionalGetAppsListRequestRequestTypeDef",
    {
        "DefaultList": bool,
    },
    total=False,
)


class GetAppsListRequestRequestTypeDef(
    _RequiredGetAppsListRequestRequestTypeDef, _OptionalGetAppsListRequestRequestTypeDef
):
    pass


GetComplianceDetailRequestRequestTypeDef = TypedDict(
    "GetComplianceDetailRequestRequestTypeDef",
    {
        "PolicyId": str,
        "MemberAccount": str,
    },
)

GetPolicyRequestRequestTypeDef = TypedDict(
    "GetPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

_RequiredGetProtectionStatusRequestRequestTypeDef = TypedDict(
    "_RequiredGetProtectionStatusRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalGetProtectionStatusRequestRequestTypeDef = TypedDict(
    "_OptionalGetProtectionStatusRequestRequestTypeDef",
    {
        "MemberAccountId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetProtectionStatusRequestRequestTypeDef(
    _RequiredGetProtectionStatusRequestRequestTypeDef,
    _OptionalGetProtectionStatusRequestRequestTypeDef,
):
    pass


_RequiredGetProtocolsListRequestRequestTypeDef = TypedDict(
    "_RequiredGetProtocolsListRequestRequestTypeDef",
    {
        "ListId": str,
    },
)
_OptionalGetProtocolsListRequestRequestTypeDef = TypedDict(
    "_OptionalGetProtocolsListRequestRequestTypeDef",
    {
        "DefaultList": bool,
    },
    total=False,
)


class GetProtocolsListRequestRequestTypeDef(
    _RequiredGetProtocolsListRequestRequestTypeDef, _OptionalGetProtocolsListRequestRequestTypeDef
):
    pass


_RequiredProtocolsListDataTypeDef = TypedDict(
    "_RequiredProtocolsListDataTypeDef",
    {
        "ListName": str,
        "ProtocolsList": List[str],
    },
)
_OptionalProtocolsListDataTypeDef = TypedDict(
    "_OptionalProtocolsListDataTypeDef",
    {
        "ListId": str,
        "ListUpdateToken": str,
        "CreateTime": datetime,
        "LastUpdateTime": datetime,
        "PreviousProtocolsList": Dict[str, List[str]],
    },
    total=False,
)


class ProtocolsListDataTypeDef(
    _RequiredProtocolsListDataTypeDef, _OptionalProtocolsListDataTypeDef
):
    pass


GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef = TypedDict(
    "GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef",
    {
        "ThirdPartyFirewall": Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
    },
)

GetViolationDetailsRequestRequestTypeDef = TypedDict(
    "GetViolationDetailsRequestRequestTypeDef",
    {
        "PolicyId": str,
        "MemberAccount": str,
        "ResourceId": str,
        "ResourceType": str,
    },
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

_RequiredListAppsListsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppsListsRequestRequestTypeDef",
    {
        "MaxResults": int,
    },
)
_OptionalListAppsListsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppsListsRequestRequestTypeDef",
    {
        "DefaultLists": bool,
        "NextToken": str,
    },
    total=False,
)


class ListAppsListsRequestRequestTypeDef(
    _RequiredListAppsListsRequestRequestTypeDef, _OptionalListAppsListsRequestRequestTypeDef
):
    pass


_RequiredListComplianceStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListComplianceStatusRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListComplianceStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListComplianceStatusRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListComplianceStatusRequestRequestTypeDef(
    _RequiredListComplianceStatusRequestRequestTypeDef,
    _OptionalListComplianceStatusRequestRequestTypeDef,
):
    pass


ListMemberAccountsRequestRequestTypeDef = TypedDict(
    "ListMemberAccountsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListPoliciesRequestRequestTypeDef = TypedDict(
    "ListPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "PolicyArn": str,
        "PolicyId": str,
        "PolicyName": str,
        "ResourceType": str,
        "SecurityServiceType": SecurityServiceTypeType,
        "RemediationEnabled": bool,
        "DeleteUnusedFMManagedResources": bool,
    },
    total=False,
)

_RequiredListProtocolsListsRequestRequestTypeDef = TypedDict(
    "_RequiredListProtocolsListsRequestRequestTypeDef",
    {
        "MaxResults": int,
    },
)
_OptionalListProtocolsListsRequestRequestTypeDef = TypedDict(
    "_OptionalListProtocolsListsRequestRequestTypeDef",
    {
        "DefaultLists": bool,
        "NextToken": str,
    },
    total=False,
)


class ListProtocolsListsRequestRequestTypeDef(
    _RequiredListProtocolsListsRequestRequestTypeDef,
    _OptionalListProtocolsListsRequestRequestTypeDef,
):
    pass


ProtocolsListDataSummaryTypeDef = TypedDict(
    "ProtocolsListDataSummaryTypeDef",
    {
        "ListArn": str,
        "ListId": str,
        "ListName": str,
        "ProtocolsList": List[str],
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef",
    {
        "ThirdPartyFirewall": Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
        "MaxResults": int,
    },
)
_OptionalListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef(
    _RequiredListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef,
    _OptionalListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef,
):
    pass


ThirdPartyFirewallFirewallPolicyTypeDef = TypedDict(
    "ThirdPartyFirewallFirewallPolicyTypeDef",
    {
        "FirewallPolicyId": str,
        "FirewallPolicyName": str,
    },
    total=False,
)

RouteTypeDef = TypedDict(
    "RouteTypeDef",
    {
        "DestinationType": DestinationTypeType,
        "TargetType": TargetTypeType,
        "Destination": str,
        "Target": str,
    },
    total=False,
)

NetworkFirewallMissingExpectedRTViolationTypeDef = TypedDict(
    "NetworkFirewallMissingExpectedRTViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "CurrentRouteTable": str,
        "ExpectedRouteTable": str,
    },
    total=False,
)

NetworkFirewallMissingFirewallViolationTypeDef = TypedDict(
    "NetworkFirewallMissingFirewallViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "TargetViolationReason": str,
    },
    total=False,
)

NetworkFirewallMissingSubnetViolationTypeDef = TypedDict(
    "NetworkFirewallMissingSubnetViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "TargetViolationReason": str,
    },
    total=False,
)

StatefulRuleGroupTypeDef = TypedDict(
    "StatefulRuleGroupTypeDef",
    {
        "RuleGroupName": str,
        "ResourceId": str,
    },
    total=False,
)

StatelessRuleGroupTypeDef = TypedDict(
    "StatelessRuleGroupTypeDef",
    {
        "RuleGroupName": str,
        "ResourceId": str,
        "Priority": int,
    },
    total=False,
)

NetworkFirewallPolicyTypeDef = TypedDict(
    "NetworkFirewallPolicyTypeDef",
    {
        "FirewallDeploymentModel": FirewallDeploymentModelType,
    },
    total=False,
)

ThirdPartyFirewallPolicyTypeDef = TypedDict(
    "ThirdPartyFirewallPolicyTypeDef",
    {
        "FirewallDeploymentModel": FirewallDeploymentModelType,
    },
    total=False,
)

_RequiredResourceTagTypeDef = TypedDict(
    "_RequiredResourceTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalResourceTagTypeDef = TypedDict(
    "_OptionalResourceTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class ResourceTagTypeDef(_RequiredResourceTagTypeDef, _OptionalResourceTagTypeDef):
    pass


PutNotificationChannelRequestRequestTypeDef = TypedDict(
    "PutNotificationChannelRequestRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SnsRoleName": str,
    },
)

ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef = TypedDict(
    "ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "CurrentRouteTable": str,
        "ExpectedRouteTable": str,
    },
    total=False,
)

ThirdPartyFirewallMissingFirewallViolationTypeDef = TypedDict(
    "ThirdPartyFirewallMissingFirewallViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "TargetViolationReason": str,
    },
    total=False,
)

ThirdPartyFirewallMissingSubnetViolationTypeDef = TypedDict(
    "ThirdPartyFirewallMissingSubnetViolationTypeDef",
    {
        "ViolationTarget": str,
        "VPC": str,
        "AvailabilityZone": str,
        "TargetViolationReason": str,
    },
    total=False,
)

SecurityGroupRuleDescriptionTypeDef = TypedDict(
    "SecurityGroupRuleDescriptionTypeDef",
    {
        "IPV4Range": str,
        "IPV6Range": str,
        "PrefixListId": str,
        "Protocol": str,
        "FromPort": int,
        "ToPort": int,
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

_RequiredEC2AssociateRouteTableActionTypeDef = TypedDict(
    "_RequiredEC2AssociateRouteTableActionTypeDef",
    {
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2AssociateRouteTableActionTypeDef = TypedDict(
    "_OptionalEC2AssociateRouteTableActionTypeDef",
    {
        "Description": str,
        "SubnetId": ActionTargetTypeDef,
        "GatewayId": ActionTargetTypeDef,
    },
    total=False,
)


class EC2AssociateRouteTableActionTypeDef(
    _RequiredEC2AssociateRouteTableActionTypeDef, _OptionalEC2AssociateRouteTableActionTypeDef
):
    pass


_RequiredEC2CopyRouteTableActionTypeDef = TypedDict(
    "_RequiredEC2CopyRouteTableActionTypeDef",
    {
        "VpcId": ActionTargetTypeDef,
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2CopyRouteTableActionTypeDef = TypedDict(
    "_OptionalEC2CopyRouteTableActionTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class EC2CopyRouteTableActionTypeDef(
    _RequiredEC2CopyRouteTableActionTypeDef, _OptionalEC2CopyRouteTableActionTypeDef
):
    pass


_RequiredEC2CreateRouteActionTypeDef = TypedDict(
    "_RequiredEC2CreateRouteActionTypeDef",
    {
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2CreateRouteActionTypeDef = TypedDict(
    "_OptionalEC2CreateRouteActionTypeDef",
    {
        "Description": str,
        "DestinationCidrBlock": str,
        "DestinationPrefixListId": str,
        "DestinationIpv6CidrBlock": str,
        "VpcEndpointId": ActionTargetTypeDef,
        "GatewayId": ActionTargetTypeDef,
    },
    total=False,
)


class EC2CreateRouteActionTypeDef(
    _RequiredEC2CreateRouteActionTypeDef, _OptionalEC2CreateRouteActionTypeDef
):
    pass


_RequiredEC2CreateRouteTableActionTypeDef = TypedDict(
    "_RequiredEC2CreateRouteTableActionTypeDef",
    {
        "VpcId": ActionTargetTypeDef,
    },
)
_OptionalEC2CreateRouteTableActionTypeDef = TypedDict(
    "_OptionalEC2CreateRouteTableActionTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class EC2CreateRouteTableActionTypeDef(
    _RequiredEC2CreateRouteTableActionTypeDef, _OptionalEC2CreateRouteTableActionTypeDef
):
    pass


_RequiredEC2DeleteRouteActionTypeDef = TypedDict(
    "_RequiredEC2DeleteRouteActionTypeDef",
    {
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2DeleteRouteActionTypeDef = TypedDict(
    "_OptionalEC2DeleteRouteActionTypeDef",
    {
        "Description": str,
        "DestinationCidrBlock": str,
        "DestinationPrefixListId": str,
        "DestinationIpv6CidrBlock": str,
    },
    total=False,
)


class EC2DeleteRouteActionTypeDef(
    _RequiredEC2DeleteRouteActionTypeDef, _OptionalEC2DeleteRouteActionTypeDef
):
    pass


_RequiredEC2ReplaceRouteActionTypeDef = TypedDict(
    "_RequiredEC2ReplaceRouteActionTypeDef",
    {
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2ReplaceRouteActionTypeDef = TypedDict(
    "_OptionalEC2ReplaceRouteActionTypeDef",
    {
        "Description": str,
        "DestinationCidrBlock": str,
        "DestinationPrefixListId": str,
        "DestinationIpv6CidrBlock": str,
        "GatewayId": ActionTargetTypeDef,
    },
    total=False,
)


class EC2ReplaceRouteActionTypeDef(
    _RequiredEC2ReplaceRouteActionTypeDef, _OptionalEC2ReplaceRouteActionTypeDef
):
    pass


_RequiredEC2ReplaceRouteTableAssociationActionTypeDef = TypedDict(
    "_RequiredEC2ReplaceRouteTableAssociationActionTypeDef",
    {
        "AssociationId": ActionTargetTypeDef,
        "RouteTableId": ActionTargetTypeDef,
    },
)
_OptionalEC2ReplaceRouteTableAssociationActionTypeDef = TypedDict(
    "_OptionalEC2ReplaceRouteTableAssociationActionTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class EC2ReplaceRouteTableAssociationActionTypeDef(
    _RequiredEC2ReplaceRouteTableAssociationActionTypeDef,
    _OptionalEC2ReplaceRouteTableAssociationActionTypeDef,
):
    pass


AppsListDataSummaryTypeDef = TypedDict(
    "AppsListDataSummaryTypeDef",
    {
        "ListArn": str,
        "ListId": str,
        "ListName": str,
        "AppsList": List[AppTypeDef],
    },
    total=False,
)

_RequiredAppsListDataTypeDef = TypedDict(
    "_RequiredAppsListDataTypeDef",
    {
        "ListName": str,
        "AppsList": List[AppTypeDef],
    },
)
_OptionalAppsListDataTypeDef = TypedDict(
    "_OptionalAppsListDataTypeDef",
    {
        "ListId": str,
        "ListUpdateToken": str,
        "CreateTime": datetime,
        "LastUpdateTime": datetime,
        "PreviousAppsList": Dict[str, List[AppTypeDef]],
    },
    total=False,
)


class AppsListDataTypeDef(_RequiredAppsListDataTypeDef, _OptionalAppsListDataTypeDef):
    pass


AssociateThirdPartyFirewallResponseTypeDef = TypedDict(
    "AssociateThirdPartyFirewallResponseTypeDef",
    {
        "ThirdPartyFirewallStatus": ThirdPartyFirewallAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateThirdPartyFirewallResponseTypeDef = TypedDict(
    "DisassociateThirdPartyFirewallResponseTypeDef",
    {
        "ThirdPartyFirewallStatus": ThirdPartyFirewallAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAdminAccountResponseTypeDef = TypedDict(
    "GetAdminAccountResponseTypeDef",
    {
        "AdminAccount": str,
        "RoleStatus": AccountRoleStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNotificationChannelResponseTypeDef = TypedDict(
    "GetNotificationChannelResponseTypeDef",
    {
        "SnsTopicArn": str,
        "SnsRoleName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProtectionStatusResponseTypeDef = TypedDict(
    "GetProtectionStatusResponseTypeDef",
    {
        "AdminAccountId": str,
        "ServiceType": SecurityServiceTypeType,
        "Data": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetThirdPartyFirewallAssociationStatusResponseTypeDef = TypedDict(
    "GetThirdPartyFirewallAssociationStatusResponseTypeDef",
    {
        "ThirdPartyFirewallStatus": ThirdPartyFirewallAssociationStatusType,
        "MarketplaceOnboardingStatus": MarketplaceSubscriptionOnboardingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMemberAccountsResponseTypeDef = TypedDict(
    "ListMemberAccountsResponseTypeDef",
    {
        "MemberAccounts": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AwsEc2InstanceViolationTypeDef = TypedDict(
    "AwsEc2InstanceViolationTypeDef",
    {
        "ViolationTarget": str,
        "AwsEc2NetworkInterfaceViolations": List[AwsEc2NetworkInterfaceViolationTypeDef],
    },
    total=False,
)

PolicyComplianceDetailTypeDef = TypedDict(
    "PolicyComplianceDetailTypeDef",
    {
        "PolicyOwner": str,
        "PolicyId": str,
        "MemberAccount": str,
        "Violators": List[ComplianceViolatorTypeDef],
        "EvaluationLimitExceeded": bool,
        "ExpiredAt": datetime,
        "IssueInfoMap": Dict[DependentServiceNameType, str],
    },
    total=False,
)

PolicyComplianceStatusTypeDef = TypedDict(
    "PolicyComplianceStatusTypeDef",
    {
        "PolicyOwner": str,
        "PolicyId": str,
        "PolicyName": str,
        "MemberAccount": str,
        "EvaluationResults": List[EvaluationResultTypeDef],
        "LastUpdated": datetime,
        "IssueInfoMap": Dict[DependentServiceNameType, str],
    },
    total=False,
)

NetworkFirewallMissingExpectedRoutesViolationTypeDef = TypedDict(
    "NetworkFirewallMissingExpectedRoutesViolationTypeDef",
    {
        "ViolationTarget": str,
        "ExpectedRoutes": List[ExpectedRouteTypeDef],
        "VpcId": str,
    },
    total=False,
)

GetProtocolsListResponseTypeDef = TypedDict(
    "GetProtocolsListResponseTypeDef",
    {
        "ProtocolsList": ProtocolsListDataTypeDef,
        "ProtocolsListArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutProtocolsListResponseTypeDef = TypedDict(
    "PutProtocolsListResponseTypeDef",
    {
        "ProtocolsList": ProtocolsListDataTypeDef,
        "ProtocolsListArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppsListsRequestListAppsListsPaginateTypeDef = TypedDict(
    "ListAppsListsRequestListAppsListsPaginateTypeDef",
    {
        "DefaultLists": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListComplianceStatusRequestListComplianceStatusPaginateTypeDef = TypedDict(
    "_RequiredListComplianceStatusRequestListComplianceStatusPaginateTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListComplianceStatusRequestListComplianceStatusPaginateTypeDef = TypedDict(
    "_OptionalListComplianceStatusRequestListComplianceStatusPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListComplianceStatusRequestListComplianceStatusPaginateTypeDef(
    _RequiredListComplianceStatusRequestListComplianceStatusPaginateTypeDef,
    _OptionalListComplianceStatusRequestListComplianceStatusPaginateTypeDef,
):
    pass


ListMemberAccountsRequestListMemberAccountsPaginateTypeDef = TypedDict(
    "ListMemberAccountsRequestListMemberAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProtocolsListsRequestListProtocolsListsPaginateTypeDef = TypedDict(
    "ListProtocolsListsRequestListProtocolsListsPaginateTypeDef",
    {
        "DefaultLists": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef",
    {
        "ThirdPartyFirewall": Literal["PALO_ALTO_NETWORKS_CLOUD_NGFW"],
    },
)
_OptionalListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef(
    _RequiredListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef,
    _OptionalListThirdPartyFirewallFirewallPoliciesRequestListThirdPartyFirewallFirewallPoliciesPaginateTypeDef,
):
    pass


ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {
        "PolicyList": List[PolicySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProtocolsListsResponseTypeDef = TypedDict(
    "ListProtocolsListsResponseTypeDef",
    {
        "ProtocolsLists": List[ProtocolsListDataSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutProtocolsListRequestRequestTypeDef = TypedDict(
    "_RequiredPutProtocolsListRequestRequestTypeDef",
    {
        "ProtocolsList": ProtocolsListDataTypeDef,
    },
)
_OptionalPutProtocolsListRequestRequestTypeDef = TypedDict(
    "_OptionalPutProtocolsListRequestRequestTypeDef",
    {
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)


class PutProtocolsListRequestRequestTypeDef(
    _RequiredPutProtocolsListRequestRequestTypeDef, _OptionalPutProtocolsListRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagList": Sequence[TagTypeDef],
    },
)

ListThirdPartyFirewallFirewallPoliciesResponseTypeDef = TypedDict(
    "ListThirdPartyFirewallFirewallPoliciesResponseTypeDef",
    {
        "ThirdPartyFirewallFirewallPolicies": List[ThirdPartyFirewallFirewallPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkFirewallBlackHoleRouteDetectedViolationTypeDef = TypedDict(
    "NetworkFirewallBlackHoleRouteDetectedViolationTypeDef",
    {
        "ViolationTarget": str,
        "RouteTableId": str,
        "VpcId": str,
        "ViolatingRoutes": List[RouteTypeDef],
    },
    total=False,
)

NetworkFirewallInternetTrafficNotInspectedViolationTypeDef = TypedDict(
    "NetworkFirewallInternetTrafficNotInspectedViolationTypeDef",
    {
        "SubnetId": str,
        "SubnetAvailabilityZone": str,
        "RouteTableId": str,
        "ViolatingRoutes": List[RouteTypeDef],
        "IsRouteTableUsedInDifferentAZ": bool,
        "CurrentFirewallSubnetRouteTable": str,
        "ExpectedFirewallEndpoint": str,
        "FirewallSubnetId": str,
        "ExpectedFirewallSubnetRoutes": List[ExpectedRouteTypeDef],
        "ActualFirewallSubnetRoutes": List[RouteTypeDef],
        "InternetGatewayId": str,
        "CurrentInternetGatewayRouteTable": str,
        "ExpectedInternetGatewayRoutes": List[ExpectedRouteTypeDef],
        "ActualInternetGatewayRoutes": List[RouteTypeDef],
        "VpcId": str,
    },
    total=False,
)

NetworkFirewallInvalidRouteConfigurationViolationTypeDef = TypedDict(
    "NetworkFirewallInvalidRouteConfigurationViolationTypeDef",
    {
        "AffectedSubnets": List[str],
        "RouteTableId": str,
        "IsRouteTableUsedInDifferentAZ": bool,
        "ViolatingRoute": RouteTypeDef,
        "CurrentFirewallSubnetRouteTable": str,
        "ExpectedFirewallEndpoint": str,
        "ActualFirewallEndpoint": str,
        "ExpectedFirewallSubnetId": str,
        "ActualFirewallSubnetId": str,
        "ExpectedFirewallSubnetRoutes": List[ExpectedRouteTypeDef],
        "ActualFirewallSubnetRoutes": List[RouteTypeDef],
        "InternetGatewayId": str,
        "CurrentInternetGatewayRouteTable": str,
        "ExpectedInternetGatewayRoutes": List[ExpectedRouteTypeDef],
        "ActualInternetGatewayRoutes": List[RouteTypeDef],
        "VpcId": str,
    },
    total=False,
)

NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef = TypedDict(
    "NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef",
    {
        "FirewallSubnetId": str,
        "ViolatingRoutes": List[RouteTypeDef],
        "RouteTableId": str,
        "FirewallEndpoint": str,
        "VpcId": str,
    },
    total=False,
)

NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef = TypedDict(
    "NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef",
    {
        "GatewayId": str,
        "ViolatingRoutes": List[RouteTypeDef],
        "RouteTableId": str,
        "VpcId": str,
    },
    total=False,
)

RouteHasOutOfScopeEndpointViolationTypeDef = TypedDict(
    "RouteHasOutOfScopeEndpointViolationTypeDef",
    {
        "SubnetId": str,
        "VpcId": str,
        "RouteTableId": str,
        "ViolatingRoutes": List[RouteTypeDef],
        "SubnetAvailabilityZone": str,
        "SubnetAvailabilityZoneId": str,
        "CurrentFirewallSubnetRouteTable": str,
        "FirewallSubnetId": str,
        "FirewallSubnetRoutes": List[RouteTypeDef],
        "InternetGatewayId": str,
        "CurrentInternetGatewayRouteTable": str,
        "InternetGatewayRoutes": List[RouteTypeDef],
    },
    total=False,
)

NetworkFirewallPolicyDescriptionTypeDef = TypedDict(
    "NetworkFirewallPolicyDescriptionTypeDef",
    {
        "StatelessRuleGroups": List[StatelessRuleGroupTypeDef],
        "StatelessDefaultActions": List[str],
        "StatelessFragmentDefaultActions": List[str],
        "StatelessCustomActions": List[str],
        "StatefulRuleGroups": List[StatefulRuleGroupTypeDef],
    },
    total=False,
)

PolicyOptionTypeDef = TypedDict(
    "PolicyOptionTypeDef",
    {
        "NetworkFirewallPolicy": NetworkFirewallPolicyTypeDef,
        "ThirdPartyFirewallPolicy": ThirdPartyFirewallPolicyTypeDef,
    },
    total=False,
)

SecurityGroupRemediationActionTypeDef = TypedDict(
    "SecurityGroupRemediationActionTypeDef",
    {
        "RemediationActionType": RemediationActionTypeType,
        "Description": str,
        "RemediationResult": SecurityGroupRuleDescriptionTypeDef,
        "IsDefaultAction": bool,
    },
    total=False,
)

RemediationActionTypeDef = TypedDict(
    "RemediationActionTypeDef",
    {
        "Description": str,
        "EC2CreateRouteAction": EC2CreateRouteActionTypeDef,
        "EC2ReplaceRouteAction": EC2ReplaceRouteActionTypeDef,
        "EC2DeleteRouteAction": EC2DeleteRouteActionTypeDef,
        "EC2CopyRouteTableAction": EC2CopyRouteTableActionTypeDef,
        "EC2ReplaceRouteTableAssociationAction": EC2ReplaceRouteTableAssociationActionTypeDef,
        "EC2AssociateRouteTableAction": EC2AssociateRouteTableActionTypeDef,
        "EC2CreateRouteTableAction": EC2CreateRouteTableActionTypeDef,
        "FMSPolicyUpdateFirewallCreationConfigAction": FMSPolicyUpdateFirewallCreationConfigActionTypeDef,
    },
    total=False,
)

ListAppsListsResponseTypeDef = TypedDict(
    "ListAppsListsResponseTypeDef",
    {
        "AppsLists": List[AppsListDataSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppsListResponseTypeDef = TypedDict(
    "GetAppsListResponseTypeDef",
    {
        "AppsList": AppsListDataTypeDef,
        "AppsListArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutAppsListRequestRequestTypeDef = TypedDict(
    "_RequiredPutAppsListRequestRequestTypeDef",
    {
        "AppsList": AppsListDataTypeDef,
    },
)
_OptionalPutAppsListRequestRequestTypeDef = TypedDict(
    "_OptionalPutAppsListRequestRequestTypeDef",
    {
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)


class PutAppsListRequestRequestTypeDef(
    _RequiredPutAppsListRequestRequestTypeDef, _OptionalPutAppsListRequestRequestTypeDef
):
    pass


PutAppsListResponseTypeDef = TypedDict(
    "PutAppsListResponseTypeDef",
    {
        "AppsList": AppsListDataTypeDef,
        "AppsListArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComplianceDetailResponseTypeDef = TypedDict(
    "GetComplianceDetailResponseTypeDef",
    {
        "PolicyComplianceDetail": PolicyComplianceDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComplianceStatusResponseTypeDef = TypedDict(
    "ListComplianceStatusResponseTypeDef",
    {
        "PolicyComplianceStatusList": List[PolicyComplianceStatusTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkFirewallPolicyModifiedViolationTypeDef = TypedDict(
    "NetworkFirewallPolicyModifiedViolationTypeDef",
    {
        "ViolationTarget": str,
        "CurrentPolicyDescription": NetworkFirewallPolicyDescriptionTypeDef,
        "ExpectedPolicyDescription": NetworkFirewallPolicyDescriptionTypeDef,
    },
    total=False,
)

_RequiredSecurityServicePolicyDataTypeDef = TypedDict(
    "_RequiredSecurityServicePolicyDataTypeDef",
    {
        "Type": SecurityServiceTypeType,
    },
)
_OptionalSecurityServicePolicyDataTypeDef = TypedDict(
    "_OptionalSecurityServicePolicyDataTypeDef",
    {
        "ManagedServiceData": str,
        "PolicyOption": PolicyOptionTypeDef,
    },
    total=False,
)


class SecurityServicePolicyDataTypeDef(
    _RequiredSecurityServicePolicyDataTypeDef, _OptionalSecurityServicePolicyDataTypeDef
):
    pass


AwsVPCSecurityGroupViolationTypeDef = TypedDict(
    "AwsVPCSecurityGroupViolationTypeDef",
    {
        "ViolationTarget": str,
        "ViolationTargetDescription": str,
        "PartialMatches": List[PartialMatchTypeDef],
        "PossibleSecurityGroupRemediationActions": List[SecurityGroupRemediationActionTypeDef],
    },
    total=False,
)

RemediationActionWithOrderTypeDef = TypedDict(
    "RemediationActionWithOrderTypeDef",
    {
        "RemediationAction": RemediationActionTypeDef,
        "Order": int,
    },
    total=False,
)

_RequiredPolicyTypeDef = TypedDict(
    "_RequiredPolicyTypeDef",
    {
        "PolicyName": str,
        "SecurityServicePolicyData": SecurityServicePolicyDataTypeDef,
        "ResourceType": str,
        "ExcludeResourceTags": bool,
        "RemediationEnabled": bool,
    },
)
_OptionalPolicyTypeDef = TypedDict(
    "_OptionalPolicyTypeDef",
    {
        "PolicyId": str,
        "PolicyUpdateToken": str,
        "ResourceTypeList": List[str],
        "ResourceTags": List[ResourceTagTypeDef],
        "DeleteUnusedFMManagedResources": bool,
        "IncludeMap": Dict[CustomerPolicyScopeIdTypeType, List[str]],
        "ExcludeMap": Dict[CustomerPolicyScopeIdTypeType, List[str]],
    },
    total=False,
)


class PolicyTypeDef(_RequiredPolicyTypeDef, _OptionalPolicyTypeDef):
    pass


_RequiredPossibleRemediationActionTypeDef = TypedDict(
    "_RequiredPossibleRemediationActionTypeDef",
    {
        "OrderedRemediationActions": List[RemediationActionWithOrderTypeDef],
    },
)
_OptionalPossibleRemediationActionTypeDef = TypedDict(
    "_OptionalPossibleRemediationActionTypeDef",
    {
        "Description": str,
        "IsDefaultAction": bool,
    },
    total=False,
)


class PossibleRemediationActionTypeDef(
    _RequiredPossibleRemediationActionTypeDef, _OptionalPossibleRemediationActionTypeDef
):
    pass


GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "PolicyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutPolicyRequestRequestTypeDef",
    {
        "Policy": PolicyTypeDef,
    },
)
_OptionalPutPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutPolicyRequestRequestTypeDef",
    {
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)


class PutPolicyRequestRequestTypeDef(
    _RequiredPutPolicyRequestRequestTypeDef, _OptionalPutPolicyRequestRequestTypeDef
):
    pass


PutPolicyResponseTypeDef = TypedDict(
    "PutPolicyResponseTypeDef",
    {
        "Policy": PolicyTypeDef,
        "PolicyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PossibleRemediationActionsTypeDef = TypedDict(
    "PossibleRemediationActionsTypeDef",
    {
        "Description": str,
        "Actions": List[PossibleRemediationActionTypeDef],
    },
    total=False,
)

ResourceViolationTypeDef = TypedDict(
    "ResourceViolationTypeDef",
    {
        "AwsVPCSecurityGroupViolation": AwsVPCSecurityGroupViolationTypeDef,
        "AwsEc2NetworkInterfaceViolation": AwsEc2NetworkInterfaceViolationTypeDef,
        "AwsEc2InstanceViolation": AwsEc2InstanceViolationTypeDef,
        "NetworkFirewallMissingFirewallViolation": NetworkFirewallMissingFirewallViolationTypeDef,
        "NetworkFirewallMissingSubnetViolation": NetworkFirewallMissingSubnetViolationTypeDef,
        "NetworkFirewallMissingExpectedRTViolation": NetworkFirewallMissingExpectedRTViolationTypeDef,
        "NetworkFirewallPolicyModifiedViolation": NetworkFirewallPolicyModifiedViolationTypeDef,
        "NetworkFirewallInternetTrafficNotInspectedViolation": NetworkFirewallInternetTrafficNotInspectedViolationTypeDef,
        "NetworkFirewallInvalidRouteConfigurationViolation": NetworkFirewallInvalidRouteConfigurationViolationTypeDef,
        "NetworkFirewallBlackHoleRouteDetectedViolation": NetworkFirewallBlackHoleRouteDetectedViolationTypeDef,
        "NetworkFirewallUnexpectedFirewallRoutesViolation": NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef,
        "NetworkFirewallUnexpectedGatewayRoutesViolation": NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef,
        "NetworkFirewallMissingExpectedRoutesViolation": NetworkFirewallMissingExpectedRoutesViolationTypeDef,
        "DnsRuleGroupPriorityConflictViolation": DnsRuleGroupPriorityConflictViolationTypeDef,
        "DnsDuplicateRuleGroupViolation": DnsDuplicateRuleGroupViolationTypeDef,
        "DnsRuleGroupLimitExceededViolation": DnsRuleGroupLimitExceededViolationTypeDef,
        "PossibleRemediationActions": PossibleRemediationActionsTypeDef,
        "FirewallSubnetIsOutOfScopeViolation": FirewallSubnetIsOutOfScopeViolationTypeDef,
        "RouteHasOutOfScopeEndpointViolation": RouteHasOutOfScopeEndpointViolationTypeDef,
        "ThirdPartyFirewallMissingFirewallViolation": ThirdPartyFirewallMissingFirewallViolationTypeDef,
        "ThirdPartyFirewallMissingSubnetViolation": ThirdPartyFirewallMissingSubnetViolationTypeDef,
        "ThirdPartyFirewallMissingExpectedRouteTableViolation": ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef,
        "FirewallSubnetMissingVPCEndpointViolation": FirewallSubnetMissingVPCEndpointViolationTypeDef,
    },
    total=False,
)

_RequiredViolationDetailTypeDef = TypedDict(
    "_RequiredViolationDetailTypeDef",
    {
        "PolicyId": str,
        "MemberAccount": str,
        "ResourceId": str,
        "ResourceType": str,
        "ResourceViolations": List[ResourceViolationTypeDef],
    },
)
_OptionalViolationDetailTypeDef = TypedDict(
    "_OptionalViolationDetailTypeDef",
    {
        "ResourceTags": List[TagTypeDef],
        "ResourceDescription": str,
    },
    total=False,
)


class ViolationDetailTypeDef(_RequiredViolationDetailTypeDef, _OptionalViolationDetailTypeDef):
    pass


GetViolationDetailsResponseTypeDef = TypedDict(
    "GetViolationDetailsResponseTypeDef",
    {
        "ViolationDetail": ViolationDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
