"""
Type annotations for route53resolver service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53resolver.type_defs import TagTypeDef

    data: TagTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import (
    ActionType,
    AutodefinedReverseFlagType,
    BlockResponseType,
    FirewallDomainListStatusType,
    FirewallDomainUpdateOperationType,
    FirewallFailOpenStatusType,
    FirewallRuleGroupAssociationStatusType,
    FirewallRuleGroupStatusType,
    IpAddressStatusType,
    MutationProtectionStatusType,
    ResolverAutodefinedReverseStatusType,
    ResolverDNSSECValidationStatusType,
    ResolverEndpointDirectionType,
    ResolverEndpointStatusType,
    ResolverQueryLogConfigAssociationErrorType,
    ResolverQueryLogConfigAssociationStatusType,
    ResolverQueryLogConfigStatusType,
    ResolverRuleAssociationStatusType,
    ResolverRuleStatusType,
    RuleTypeOptionType,
    ShareStatusType,
    SortOrderType,
    ValidationType,
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
    "TagTypeDef",
    "FirewallRuleGroupAssociationTypeDef",
    "ResponseMetadataTypeDef",
    "IpAddressUpdateTypeDef",
    "ResolverEndpointTypeDef",
    "AssociateResolverQueryLogConfigRequestRequestTypeDef",
    "ResolverQueryLogConfigAssociationTypeDef",
    "AssociateResolverRuleRequestRequestTypeDef",
    "ResolverRuleAssociationTypeDef",
    "FirewallDomainListTypeDef",
    "FirewallRuleGroupTypeDef",
    "CreateFirewallRuleRequestRequestTypeDef",
    "FirewallRuleTypeDef",
    "IpAddressRequestTypeDef",
    "ResolverQueryLogConfigTypeDef",
    "TargetAddressTypeDef",
    "DeleteFirewallDomainListRequestRequestTypeDef",
    "DeleteFirewallRuleGroupRequestRequestTypeDef",
    "DeleteFirewallRuleRequestRequestTypeDef",
    "DeleteResolverEndpointRequestRequestTypeDef",
    "DeleteResolverQueryLogConfigRequestRequestTypeDef",
    "DeleteResolverRuleRequestRequestTypeDef",
    "DisassociateFirewallRuleGroupRequestRequestTypeDef",
    "DisassociateResolverQueryLogConfigRequestRequestTypeDef",
    "DisassociateResolverRuleRequestRequestTypeDef",
    "FilterTypeDef",
    "FirewallConfigTypeDef",
    "FirewallDomainListMetadataTypeDef",
    "FirewallRuleGroupMetadataTypeDef",
    "GetFirewallConfigRequestRequestTypeDef",
    "GetFirewallDomainListRequestRequestTypeDef",
    "GetFirewallRuleGroupAssociationRequestRequestTypeDef",
    "GetFirewallRuleGroupPolicyRequestRequestTypeDef",
    "GetFirewallRuleGroupRequestRequestTypeDef",
    "GetResolverConfigRequestRequestTypeDef",
    "ResolverConfigTypeDef",
    "GetResolverDnssecConfigRequestRequestTypeDef",
    "ResolverDnssecConfigTypeDef",
    "GetResolverEndpointRequestRequestTypeDef",
    "GetResolverQueryLogConfigAssociationRequestRequestTypeDef",
    "GetResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "GetResolverQueryLogConfigRequestRequestTypeDef",
    "GetResolverRuleAssociationRequestRequestTypeDef",
    "GetResolverRulePolicyRequestRequestTypeDef",
    "GetResolverRuleRequestRequestTypeDef",
    "ImportFirewallDomainsRequestRequestTypeDef",
    "IpAddressResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ListFirewallConfigsRequestRequestTypeDef",
    "ListFirewallDomainListsRequestRequestTypeDef",
    "ListFirewallDomainsRequestRequestTypeDef",
    "ListFirewallRuleGroupAssociationsRequestRequestTypeDef",
    "ListFirewallRuleGroupsRequestRequestTypeDef",
    "ListFirewallRulesRequestRequestTypeDef",
    "ListResolverConfigsRequestRequestTypeDef",
    "ListResolverEndpointIpAddressesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutFirewallRuleGroupPolicyRequestRequestTypeDef",
    "PutResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "PutResolverRulePolicyRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallConfigRequestRequestTypeDef",
    "UpdateFirewallDomainsRequestRequestTypeDef",
    "UpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    "UpdateFirewallRuleRequestRequestTypeDef",
    "UpdateResolverConfigRequestRequestTypeDef",
    "UpdateResolverDnssecConfigRequestRequestTypeDef",
    "UpdateResolverEndpointRequestRequestTypeDef",
    "AssociateFirewallRuleGroupRequestRequestTypeDef",
    "CreateFirewallDomainListRequestRequestTypeDef",
    "CreateFirewallRuleGroupRequestRequestTypeDef",
    "CreateResolverQueryLogConfigRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "AssociateFirewallRuleGroupResponseTypeDef",
    "DisassociateFirewallRuleGroupResponseTypeDef",
    "GetFirewallRuleGroupAssociationResponseTypeDef",
    "GetFirewallRuleGroupPolicyResponseTypeDef",
    "GetResolverQueryLogConfigPolicyResponseTypeDef",
    "GetResolverRulePolicyResponseTypeDef",
    "ImportFirewallDomainsResponseTypeDef",
    "ListFirewallDomainsResponseTypeDef",
    "ListFirewallRuleGroupAssociationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutFirewallRuleGroupPolicyResponseTypeDef",
    "PutResolverQueryLogConfigPolicyResponseTypeDef",
    "PutResolverRulePolicyResponseTypeDef",
    "UpdateFirewallDomainsResponseTypeDef",
    "UpdateFirewallRuleGroupAssociationResponseTypeDef",
    "AssociateResolverEndpointIpAddressRequestRequestTypeDef",
    "DisassociateResolverEndpointIpAddressRequestRequestTypeDef",
    "AssociateResolverEndpointIpAddressResponseTypeDef",
    "CreateResolverEndpointResponseTypeDef",
    "DeleteResolverEndpointResponseTypeDef",
    "DisassociateResolverEndpointIpAddressResponseTypeDef",
    "GetResolverEndpointResponseTypeDef",
    "ListResolverEndpointsResponseTypeDef",
    "UpdateResolverEndpointResponseTypeDef",
    "AssociateResolverQueryLogConfigResponseTypeDef",
    "DisassociateResolverQueryLogConfigResponseTypeDef",
    "GetResolverQueryLogConfigAssociationResponseTypeDef",
    "ListResolverQueryLogConfigAssociationsResponseTypeDef",
    "AssociateResolverRuleResponseTypeDef",
    "DisassociateResolverRuleResponseTypeDef",
    "GetResolverRuleAssociationResponseTypeDef",
    "ListResolverRuleAssociationsResponseTypeDef",
    "CreateFirewallDomainListResponseTypeDef",
    "DeleteFirewallDomainListResponseTypeDef",
    "GetFirewallDomainListResponseTypeDef",
    "CreateFirewallRuleGroupResponseTypeDef",
    "DeleteFirewallRuleGroupResponseTypeDef",
    "GetFirewallRuleGroupResponseTypeDef",
    "CreateFirewallRuleResponseTypeDef",
    "DeleteFirewallRuleResponseTypeDef",
    "ListFirewallRulesResponseTypeDef",
    "UpdateFirewallRuleResponseTypeDef",
    "CreateResolverEndpointRequestRequestTypeDef",
    "CreateResolverQueryLogConfigResponseTypeDef",
    "DeleteResolverQueryLogConfigResponseTypeDef",
    "GetResolverQueryLogConfigResponseTypeDef",
    "ListResolverQueryLogConfigsResponseTypeDef",
    "CreateResolverRuleRequestRequestTypeDef",
    "ResolverRuleConfigTypeDef",
    "ResolverRuleTypeDef",
    "ListResolverDnssecConfigsRequestRequestTypeDef",
    "ListResolverEndpointsRequestRequestTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestRequestTypeDef",
    "ListResolverQueryLogConfigsRequestRequestTypeDef",
    "ListResolverRuleAssociationsRequestRequestTypeDef",
    "ListResolverRulesRequestRequestTypeDef",
    "GetFirewallConfigResponseTypeDef",
    "ListFirewallConfigsResponseTypeDef",
    "UpdateFirewallConfigResponseTypeDef",
    "ListFirewallDomainListsResponseTypeDef",
    "ListFirewallRuleGroupsResponseTypeDef",
    "GetResolverConfigResponseTypeDef",
    "ListResolverConfigsResponseTypeDef",
    "UpdateResolverConfigResponseTypeDef",
    "GetResolverDnssecConfigResponseTypeDef",
    "ListResolverDnssecConfigsResponseTypeDef",
    "UpdateResolverDnssecConfigResponseTypeDef",
    "ListResolverEndpointIpAddressesResponseTypeDef",
    "ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef",
    "ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef",
    "ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    "ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef",
    "ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef",
    "ListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    "ListResolverConfigsRequestListResolverConfigsPaginateTypeDef",
    "ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef",
    "ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    "ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef",
    "ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef",
    "ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef",
    "ListResolverRulesRequestListResolverRulesPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "UpdateResolverRuleRequestRequestTypeDef",
    "CreateResolverRuleResponseTypeDef",
    "DeleteResolverRuleResponseTypeDef",
    "GetResolverRuleResponseTypeDef",
    "ListResolverRulesResponseTypeDef",
    "UpdateResolverRuleResponseTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

FirewallRuleGroupAssociationTypeDef = TypedDict(
    "FirewallRuleGroupAssociationTypeDef",
    {
        "Id": str,
        "Arn": str,
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Name": str,
        "Priority": int,
        "MutationProtection": MutationProtectionStatusType,
        "ManagedOwnerName": str,
        "Status": FirewallRuleGroupAssociationStatusType,
        "StatusMessage": str,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
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

IpAddressUpdateTypeDef = TypedDict(
    "IpAddressUpdateTypeDef",
    {
        "IpId": str,
        "SubnetId": str,
        "Ip": str,
    },
    total=False,
)

ResolverEndpointTypeDef = TypedDict(
    "ResolverEndpointTypeDef",
    {
        "Id": str,
        "CreatorRequestId": str,
        "Arn": str,
        "Name": str,
        "SecurityGroupIds": List[str],
        "Direction": ResolverEndpointDirectionType,
        "IpAddressCount": int,
        "HostVPCId": str,
        "Status": ResolverEndpointStatusType,
        "StatusMessage": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

AssociateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "AssociateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
    },
)

ResolverQueryLogConfigAssociationTypeDef = TypedDict(
    "ResolverQueryLogConfigAssociationTypeDef",
    {
        "Id": str,
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
        "Status": ResolverQueryLogConfigAssociationStatusType,
        "Error": ResolverQueryLogConfigAssociationErrorType,
        "ErrorMessage": str,
        "CreationTime": str,
    },
    total=False,
)

_RequiredAssociateResolverRuleRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
        "VPCId": str,
    },
)
_OptionalAssociateResolverRuleRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateResolverRuleRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class AssociateResolverRuleRequestRequestTypeDef(
    _RequiredAssociateResolverRuleRequestRequestTypeDef,
    _OptionalAssociateResolverRuleRequestRequestTypeDef,
):
    pass


ResolverRuleAssociationTypeDef = TypedDict(
    "ResolverRuleAssociationTypeDef",
    {
        "Id": str,
        "ResolverRuleId": str,
        "Name": str,
        "VPCId": str,
        "Status": ResolverRuleAssociationStatusType,
        "StatusMessage": str,
    },
    total=False,
)

FirewallDomainListTypeDef = TypedDict(
    "FirewallDomainListTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "DomainCount": int,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ManagedOwnerName": str,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

FirewallRuleGroupTypeDef = TypedDict(
    "FirewallRuleGroupTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "RuleCount": int,
        "Status": FirewallRuleGroupStatusType,
        "StatusMessage": str,
        "OwnerId": str,
        "CreatorRequestId": str,
        "ShareStatus": ShareStatusType,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

_RequiredCreateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallRuleRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
        "Priority": int,
        "Action": ActionType,
        "Name": str,
    },
)
_OptionalCreateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallRuleRequestRequestTypeDef",
    {
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
    },
    total=False,
)


class CreateFirewallRuleRequestRequestTypeDef(
    _RequiredCreateFirewallRuleRequestRequestTypeDef,
    _OptionalCreateFirewallRuleRequestRequestTypeDef,
):
    pass


FirewallRuleTypeDef = TypedDict(
    "FirewallRuleTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
        "Name": str,
        "Priority": int,
        "Action": ActionType,
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

_RequiredIpAddressRequestTypeDef = TypedDict(
    "_RequiredIpAddressRequestTypeDef",
    {
        "SubnetId": str,
    },
)
_OptionalIpAddressRequestTypeDef = TypedDict(
    "_OptionalIpAddressRequestTypeDef",
    {
        "Ip": str,
    },
    total=False,
)


class IpAddressRequestTypeDef(_RequiredIpAddressRequestTypeDef, _OptionalIpAddressRequestTypeDef):
    pass


ResolverQueryLogConfigTypeDef = TypedDict(
    "ResolverQueryLogConfigTypeDef",
    {
        "Id": str,
        "OwnerId": str,
        "Status": ResolverQueryLogConfigStatusType,
        "ShareStatus": ShareStatusType,
        "AssociationCount": int,
        "Arn": str,
        "Name": str,
        "DestinationArn": str,
        "CreatorRequestId": str,
        "CreationTime": str,
    },
    total=False,
)

_RequiredTargetAddressTypeDef = TypedDict(
    "_RequiredTargetAddressTypeDef",
    {
        "Ip": str,
    },
)
_OptionalTargetAddressTypeDef = TypedDict(
    "_OptionalTargetAddressTypeDef",
    {
        "Port": int,
    },
    total=False,
)


class TargetAddressTypeDef(_RequiredTargetAddressTypeDef, _OptionalTargetAddressTypeDef):
    pass


DeleteFirewallDomainListRequestRequestTypeDef = TypedDict(
    "DeleteFirewallDomainListRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)

DeleteFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)

DeleteFirewallRuleRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRuleRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
    },
)

DeleteResolverEndpointRequestRequestTypeDef = TypedDict(
    "DeleteResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)

DeleteResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "DeleteResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
    },
)

DeleteResolverRuleRequestRequestTypeDef = TypedDict(
    "DeleteResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
    },
)

DisassociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "DisassociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)

DisassociateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "DisassociateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
    },
)

DisassociateResolverRuleRequestRequestTypeDef = TypedDict(
    "DisassociateResolverRuleRequestRequestTypeDef",
    {
        "VPCId": str,
        "ResolverRuleId": str,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

FirewallConfigTypeDef = TypedDict(
    "FirewallConfigTypeDef",
    {
        "Id": str,
        "ResourceId": str,
        "OwnerId": str,
        "FirewallFailOpen": FirewallFailOpenStatusType,
    },
    total=False,
)

FirewallDomainListMetadataTypeDef = TypedDict(
    "FirewallDomainListMetadataTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "CreatorRequestId": str,
        "ManagedOwnerName": str,
    },
    total=False,
)

FirewallRuleGroupMetadataTypeDef = TypedDict(
    "FirewallRuleGroupMetadataTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "OwnerId": str,
        "CreatorRequestId": str,
        "ShareStatus": ShareStatusType,
    },
    total=False,
)

GetFirewallConfigRequestRequestTypeDef = TypedDict(
    "GetFirewallConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

GetFirewallDomainListRequestRequestTypeDef = TypedDict(
    "GetFirewallDomainListRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)

GetFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)

GetFirewallRuleGroupPolicyRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupPolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)

GetResolverConfigRequestRequestTypeDef = TypedDict(
    "GetResolverConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

ResolverConfigTypeDef = TypedDict(
    "ResolverConfigTypeDef",
    {
        "Id": str,
        "ResourceId": str,
        "OwnerId": str,
        "AutodefinedReverse": ResolverAutodefinedReverseStatusType,
    },
    total=False,
)

GetResolverDnssecConfigRequestRequestTypeDef = TypedDict(
    "GetResolverDnssecConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

ResolverDnssecConfigTypeDef = TypedDict(
    "ResolverDnssecConfigTypeDef",
    {
        "Id": str,
        "OwnerId": str,
        "ResourceId": str,
        "ValidationStatus": ResolverDNSSECValidationStatusType,
    },
    total=False,
)

GetResolverEndpointRequestRequestTypeDef = TypedDict(
    "GetResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)

GetResolverQueryLogConfigAssociationRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigAssociationRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigAssociationId": str,
    },
)

GetResolverQueryLogConfigPolicyRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigPolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
    },
)

GetResolverRuleAssociationRequestRequestTypeDef = TypedDict(
    "GetResolverRuleAssociationRequestRequestTypeDef",
    {
        "ResolverRuleAssociationId": str,
    },
)

GetResolverRulePolicyRequestRequestTypeDef = TypedDict(
    "GetResolverRulePolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetResolverRuleRequestRequestTypeDef = TypedDict(
    "GetResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
    },
)

ImportFirewallDomainsRequestRequestTypeDef = TypedDict(
    "ImportFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
        "Operation": Literal["REPLACE"],
        "DomainFileUrl": str,
    },
)

IpAddressResponseTypeDef = TypedDict(
    "IpAddressResponseTypeDef",
    {
        "IpId": str,
        "SubnetId": str,
        "Ip": str,
        "Status": IpAddressStatusType,
        "StatusMessage": str,
        "CreationTime": str,
        "ModificationTime": str,
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

ListFirewallConfigsRequestRequestTypeDef = TypedDict(
    "ListFirewallConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallDomainListsRequestRequestTypeDef = TypedDict(
    "ListFirewallDomainListsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListFirewallDomainsRequestRequestTypeDef = TypedDict(
    "_RequiredListFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)
_OptionalListFirewallDomainsRequestRequestTypeDef = TypedDict(
    "_OptionalListFirewallDomainsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListFirewallDomainsRequestRequestTypeDef(
    _RequiredListFirewallDomainsRequestRequestTypeDef,
    _OptionalListFirewallDomainsRequestRequestTypeDef,
):
    pass


ListFirewallRuleGroupAssociationsRequestRequestTypeDef = TypedDict(
    "ListFirewallRuleGroupAssociationsRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Priority": int,
        "Status": FirewallRuleGroupAssociationStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListFirewallRuleGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListFirewallRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListFirewallRulesRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)
_OptionalListFirewallRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListFirewallRulesRequestRequestTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListFirewallRulesRequestRequestTypeDef(
    _RequiredListFirewallRulesRequestRequestTypeDef, _OptionalListFirewallRulesRequestRequestTypeDef
):
    pass


ListResolverConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListResolverEndpointIpAddressesRequestRequestTypeDef = TypedDict(
    "_RequiredListResolverEndpointIpAddressesRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalListResolverEndpointIpAddressesRequestRequestTypeDef = TypedDict(
    "_OptionalListResolverEndpointIpAddressesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListResolverEndpointIpAddressesRequestRequestTypeDef(
    _RequiredListResolverEndpointIpAddressesRequestRequestTypeDef,
    _OptionalListResolverEndpointIpAddressesRequestRequestTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


PutFirewallRuleGroupPolicyRequestRequestTypeDef = TypedDict(
    "PutFirewallRuleGroupPolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "FirewallRuleGroupPolicy": str,
    },
)

PutResolverQueryLogConfigPolicyRequestRequestTypeDef = TypedDict(
    "PutResolverQueryLogConfigPolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "ResolverQueryLogConfigPolicy": str,
    },
)

PutResolverRulePolicyRequestRequestTypeDef = TypedDict(
    "PutResolverRulePolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "ResolverRulePolicy": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateFirewallConfigRequestRequestTypeDef = TypedDict(
    "UpdateFirewallConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "FirewallFailOpen": FirewallFailOpenStatusType,
    },
)

UpdateFirewallDomainsRequestRequestTypeDef = TypedDict(
    "UpdateFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
        "Operation": FirewallDomainUpdateOperationType,
        "Domains": Sequence[str],
    },
)

_RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)
_OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "Priority": int,
        "MutationProtection": MutationProtectionStatusType,
        "Name": str,
    },
    total=False,
)


class UpdateFirewallRuleGroupAssociationRequestRequestTypeDef(
    _RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef,
    _OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef,
):
    pass


_RequiredUpdateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallRuleRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
    },
)
_OptionalUpdateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallRuleRequestRequestTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
        "Name": str,
    },
    total=False,
)


class UpdateFirewallRuleRequestRequestTypeDef(
    _RequiredUpdateFirewallRuleRequestRequestTypeDef,
    _OptionalUpdateFirewallRuleRequestRequestTypeDef,
):
    pass


UpdateResolverConfigRequestRequestTypeDef = TypedDict(
    "UpdateResolverConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "AutodefinedReverseFlag": AutodefinedReverseFlagType,
    },
)

UpdateResolverDnssecConfigRequestRequestTypeDef = TypedDict(
    "UpdateResolverDnssecConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Validation": ValidationType,
    },
)

_RequiredUpdateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalUpdateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResolverEndpointRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateResolverEndpointRequestRequestTypeDef(
    _RequiredUpdateResolverEndpointRequestRequestTypeDef,
    _OptionalUpdateResolverEndpointRequestRequestTypeDef,
):
    pass


_RequiredAssociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Priority": int,
        "Name": str,
    },
)
_OptionalAssociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "MutationProtection": MutationProtectionStatusType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class AssociateFirewallRuleGroupRequestRequestTypeDef(
    _RequiredAssociateFirewallRuleGroupRequestRequestTypeDef,
    _OptionalAssociateFirewallRuleGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateFirewallDomainListRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallDomainListRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Name": str,
    },
)
_OptionalCreateFirewallDomainListRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallDomainListRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFirewallDomainListRequestRequestTypeDef(
    _RequiredCreateFirewallDomainListRequestRequestTypeDef,
    _OptionalCreateFirewallDomainListRequestRequestTypeDef,
):
    pass


_RequiredCreateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallRuleGroupRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Name": str,
    },
)
_OptionalCreateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallRuleGroupRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFirewallRuleGroupRequestRequestTypeDef(
    _RequiredCreateFirewallRuleGroupRequestRequestTypeDef,
    _OptionalCreateFirewallRuleGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "Name": str,
        "DestinationArn": str,
        "CreatorRequestId": str,
    },
)
_OptionalCreateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateResolverQueryLogConfigRequestRequestTypeDef(
    _RequiredCreateResolverQueryLogConfigRequestRequestTypeDef,
    _OptionalCreateResolverQueryLogConfigRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

AssociateFirewallRuleGroupResponseTypeDef = TypedDict(
    "AssociateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": FirewallRuleGroupAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateFirewallRuleGroupResponseTypeDef = TypedDict(
    "DisassociateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": FirewallRuleGroupAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFirewallRuleGroupAssociationResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupAssociationResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": FirewallRuleGroupAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFirewallRuleGroupPolicyResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupPolicyResponseTypeDef",
    {
        "FirewallRuleGroupPolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverQueryLogConfigPolicyResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigPolicyResponseTypeDef",
    {
        "ResolverQueryLogConfigPolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverRulePolicyResponseTypeDef = TypedDict(
    "GetResolverRulePolicyResponseTypeDef",
    {
        "ResolverRulePolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportFirewallDomainsResponseTypeDef = TypedDict(
    "ImportFirewallDomainsResponseTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallDomainsResponseTypeDef = TypedDict(
    "ListFirewallDomainsResponseTypeDef",
    {
        "NextToken": str,
        "Domains": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallRuleGroupAssociationsResponseTypeDef = TypedDict(
    "ListFirewallRuleGroupAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRuleGroupAssociations": List[FirewallRuleGroupAssociationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutFirewallRuleGroupPolicyResponseTypeDef = TypedDict(
    "PutFirewallRuleGroupPolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResolverQueryLogConfigPolicyResponseTypeDef = TypedDict(
    "PutResolverQueryLogConfigPolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResolverRulePolicyResponseTypeDef = TypedDict(
    "PutResolverRulePolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallDomainsResponseTypeDef = TypedDict(
    "UpdateFirewallDomainsResponseTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallRuleGroupAssociationResponseTypeDef = TypedDict(
    "UpdateFirewallRuleGroupAssociationResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": FirewallRuleGroupAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResolverEndpointIpAddressRequestRequestTypeDef = TypedDict(
    "AssociateResolverEndpointIpAddressRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
        "IpAddress": IpAddressUpdateTypeDef,
    },
)

DisassociateResolverEndpointIpAddressRequestRequestTypeDef = TypedDict(
    "DisassociateResolverEndpointIpAddressRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
        "IpAddress": IpAddressUpdateTypeDef,
    },
)

AssociateResolverEndpointIpAddressResponseTypeDef = TypedDict(
    "AssociateResolverEndpointIpAddressResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResolverEndpointResponseTypeDef = TypedDict(
    "CreateResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResolverEndpointResponseTypeDef = TypedDict(
    "DeleteResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateResolverEndpointIpAddressResponseTypeDef = TypedDict(
    "DisassociateResolverEndpointIpAddressResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverEndpointResponseTypeDef = TypedDict(
    "GetResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverEndpointsResponseTypeDef = TypedDict(
    "ListResolverEndpointsResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverEndpoints": List[ResolverEndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResolverEndpointResponseTypeDef = TypedDict(
    "UpdateResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": ResolverEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "AssociateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": ResolverQueryLogConfigAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "DisassociateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": ResolverQueryLogConfigAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverQueryLogConfigAssociationResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigAssociationResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": ResolverQueryLogConfigAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverQueryLogConfigAssociationsResponseTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "TotalCount": int,
        "TotalFilteredCount": int,
        "ResolverQueryLogConfigAssociations": List[ResolverQueryLogConfigAssociationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResolverRuleResponseTypeDef = TypedDict(
    "AssociateResolverRuleResponseTypeDef",
    {
        "ResolverRuleAssociation": ResolverRuleAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateResolverRuleResponseTypeDef = TypedDict(
    "DisassociateResolverRuleResponseTypeDef",
    {
        "ResolverRuleAssociation": ResolverRuleAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverRuleAssociationResponseTypeDef = TypedDict(
    "GetResolverRuleAssociationResponseTypeDef",
    {
        "ResolverRuleAssociation": ResolverRuleAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverRuleAssociationsResponseTypeDef = TypedDict(
    "ListResolverRuleAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverRuleAssociations": List[ResolverRuleAssociationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFirewallDomainListResponseTypeDef = TypedDict(
    "CreateFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": FirewallDomainListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallDomainListResponseTypeDef = TypedDict(
    "DeleteFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": FirewallDomainListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFirewallDomainListResponseTypeDef = TypedDict(
    "GetFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": FirewallDomainListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFirewallRuleGroupResponseTypeDef = TypedDict(
    "CreateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": FirewallRuleGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallRuleGroupResponseTypeDef = TypedDict(
    "DeleteFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": FirewallRuleGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFirewallRuleGroupResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": FirewallRuleGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFirewallRuleResponseTypeDef = TypedDict(
    "CreateFirewallRuleResponseTypeDef",
    {
        "FirewallRule": FirewallRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallRuleResponseTypeDef = TypedDict(
    "DeleteFirewallRuleResponseTypeDef",
    {
        "FirewallRule": FirewallRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallRulesResponseTypeDef = TypedDict(
    "ListFirewallRulesResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRules": List[FirewallRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallRuleResponseTypeDef = TypedDict(
    "UpdateFirewallRuleResponseTypeDef",
    {
        "FirewallRule": FirewallRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverEndpointRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "SecurityGroupIds": Sequence[str],
        "Direction": ResolverEndpointDirectionType,
        "IpAddresses": Sequence[IpAddressRequestTypeDef],
    },
)
_OptionalCreateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverEndpointRequestRequestTypeDef",
    {
        "Name": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateResolverEndpointRequestRequestTypeDef(
    _RequiredCreateResolverEndpointRequestRequestTypeDef,
    _OptionalCreateResolverEndpointRequestRequestTypeDef,
):
    pass


CreateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "CreateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": ResolverQueryLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResolverQueryLogConfigResponseTypeDef = TypedDict(
    "DeleteResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": ResolverQueryLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverQueryLogConfigResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": ResolverQueryLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverQueryLogConfigsResponseTypeDef = TypedDict(
    "ListResolverQueryLogConfigsResponseTypeDef",
    {
        "NextToken": str,
        "TotalCount": int,
        "TotalFilteredCount": int,
        "ResolverQueryLogConfigs": List[ResolverQueryLogConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateResolverRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverRuleRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "RuleType": RuleTypeOptionType,
        "DomainName": str,
    },
)
_OptionalCreateResolverRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverRuleRequestRequestTypeDef",
    {
        "Name": str,
        "TargetIps": Sequence[TargetAddressTypeDef],
        "ResolverEndpointId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateResolverRuleRequestRequestTypeDef(
    _RequiredCreateResolverRuleRequestRequestTypeDef,
    _OptionalCreateResolverRuleRequestRequestTypeDef,
):
    pass


ResolverRuleConfigTypeDef = TypedDict(
    "ResolverRuleConfigTypeDef",
    {
        "Name": str,
        "TargetIps": Sequence[TargetAddressTypeDef],
        "ResolverEndpointId": str,
    },
    total=False,
)

ResolverRuleTypeDef = TypedDict(
    "ResolverRuleTypeDef",
    {
        "Id": str,
        "CreatorRequestId": str,
        "Arn": str,
        "DomainName": str,
        "Status": ResolverRuleStatusType,
        "StatusMessage": str,
        "RuleType": RuleTypeOptionType,
        "Name": str,
        "TargetIps": List[TargetAddressTypeDef],
        "ResolverEndpointId": str,
        "OwnerId": str,
        "ShareStatus": ShareStatusType,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

ListResolverDnssecConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverDnssecConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListResolverEndpointsRequestRequestTypeDef = TypedDict(
    "ListResolverEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListResolverQueryLogConfigAssociationsRequestRequestTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
        "SortBy": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListResolverQueryLogConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverQueryLogConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
        "SortBy": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListResolverRuleAssociationsRequestRequestTypeDef = TypedDict(
    "ListResolverRuleAssociationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListResolverRulesRequestRequestTypeDef = TypedDict(
    "ListResolverRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

GetFirewallConfigResponseTypeDef = TypedDict(
    "GetFirewallConfigResponseTypeDef",
    {
        "FirewallConfig": FirewallConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallConfigsResponseTypeDef = TypedDict(
    "ListFirewallConfigsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallConfigs": List[FirewallConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallConfigResponseTypeDef = TypedDict(
    "UpdateFirewallConfigResponseTypeDef",
    {
        "FirewallConfig": FirewallConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallDomainListsResponseTypeDef = TypedDict(
    "ListFirewallDomainListsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallDomainLists": List[FirewallDomainListMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallRuleGroupsResponseTypeDef = TypedDict(
    "ListFirewallRuleGroupsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRuleGroups": List[FirewallRuleGroupMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverConfigResponseTypeDef = TypedDict(
    "GetResolverConfigResponseTypeDef",
    {
        "ResolverConfig": ResolverConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverConfigsResponseTypeDef = TypedDict(
    "ListResolverConfigsResponseTypeDef",
    {
        "NextToken": str,
        "ResolverConfigs": List[ResolverConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResolverConfigResponseTypeDef = TypedDict(
    "UpdateResolverConfigResponseTypeDef",
    {
        "ResolverConfig": ResolverConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverDnssecConfigResponseTypeDef = TypedDict(
    "GetResolverDnssecConfigResponseTypeDef",
    {
        "ResolverDNSSECConfig": ResolverDnssecConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverDnssecConfigsResponseTypeDef = TypedDict(
    "ListResolverDnssecConfigsResponseTypeDef",
    {
        "NextToken": str,
        "ResolverDnssecConfigs": List[ResolverDnssecConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResolverDnssecConfigResponseTypeDef = TypedDict(
    "UpdateResolverDnssecConfigResponseTypeDef",
    {
        "ResolverDNSSECConfig": ResolverDnssecConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverEndpointIpAddressesResponseTypeDef = TypedDict(
    "ListResolverEndpointIpAddressesResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "IpAddresses": List[IpAddressResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef = TypedDict(
    "ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef = TypedDict(
    "ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef = TypedDict(
    "_RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    {
        "FirewallDomainListId": str,
    },
)
_OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef = TypedDict(
    "_OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef(
    _RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
    _OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
):
    pass


ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef = (
    TypedDict(
        "ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef",
        {
            "FirewallRuleGroupId": str,
            "VpcId": str,
            "Priority": int,
            "Status": FirewallRuleGroupAssociationStatusType,
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef = TypedDict(
    "ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef = TypedDict(
    "_RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)
_OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef = TypedDict(
    "_OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFirewallRulesRequestListFirewallRulesPaginateTypeDef(
    _RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
    _OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
):
    pass


ListResolverConfigsRequestListResolverConfigsPaginateTypeDef = TypedDict(
    "ListResolverConfigsRequestListResolverConfigsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef = TypedDict(
    "ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef = TypedDict(
    "_RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef = TypedDict(
    "_OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef(
    _RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
    _OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
):
    pass


ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef = TypedDict(
    "ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortBy": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef = TypedDict(
    "ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "SortBy": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef = TypedDict(
    "ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListResolverRulesRequestListResolverRulesPaginateTypeDef = TypedDict(
    "ListResolverRulesRequestListResolverRulesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


UpdateResolverRuleRequestRequestTypeDef = TypedDict(
    "UpdateResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
        "Config": ResolverRuleConfigTypeDef,
    },
)

CreateResolverRuleResponseTypeDef = TypedDict(
    "CreateResolverRuleResponseTypeDef",
    {
        "ResolverRule": ResolverRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResolverRuleResponseTypeDef = TypedDict(
    "DeleteResolverRuleResponseTypeDef",
    {
        "ResolverRule": ResolverRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResolverRuleResponseTypeDef = TypedDict(
    "GetResolverRuleResponseTypeDef",
    {
        "ResolverRule": ResolverRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResolverRulesResponseTypeDef = TypedDict(
    "ListResolverRulesResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverRules": List[ResolverRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResolverRuleResponseTypeDef = TypedDict(
    "UpdateResolverRuleResponseTypeDef",
    {
        "ResolverRule": ResolverRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
