"""
Type annotations for route53resolver service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53resolver.client import Route53ResolverClient

    session = Session()
    client: Route53ResolverClient = session.client("route53resolver")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ActionType,
    AutodefinedReverseFlagType,
    BlockResponseType,
    FirewallDomainUpdateOperationType,
    FirewallFailOpenStatusType,
    FirewallRuleGroupAssociationStatusType,
    MutationProtectionStatusType,
    ResolverEndpointDirectionType,
    RuleTypeOptionType,
    SortOrderType,
    ValidationType,
)
from .paginator import (
    ListFirewallConfigsPaginator,
    ListFirewallDomainListsPaginator,
    ListFirewallDomainsPaginator,
    ListFirewallRuleGroupAssociationsPaginator,
    ListFirewallRuleGroupsPaginator,
    ListFirewallRulesPaginator,
    ListResolverConfigsPaginator,
    ListResolverDnssecConfigsPaginator,
    ListResolverEndpointIpAddressesPaginator,
    ListResolverEndpointsPaginator,
    ListResolverQueryLogConfigAssociationsPaginator,
    ListResolverQueryLogConfigsPaginator,
    ListResolverRuleAssociationsPaginator,
    ListResolverRulesPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AssociateFirewallRuleGroupResponseTypeDef,
    AssociateResolverEndpointIpAddressResponseTypeDef,
    AssociateResolverQueryLogConfigResponseTypeDef,
    AssociateResolverRuleResponseTypeDef,
    CreateFirewallDomainListResponseTypeDef,
    CreateFirewallRuleGroupResponseTypeDef,
    CreateFirewallRuleResponseTypeDef,
    CreateResolverEndpointResponseTypeDef,
    CreateResolverQueryLogConfigResponseTypeDef,
    CreateResolverRuleResponseTypeDef,
    DeleteFirewallDomainListResponseTypeDef,
    DeleteFirewallRuleGroupResponseTypeDef,
    DeleteFirewallRuleResponseTypeDef,
    DeleteResolverEndpointResponseTypeDef,
    DeleteResolverQueryLogConfigResponseTypeDef,
    DeleteResolverRuleResponseTypeDef,
    DisassociateFirewallRuleGroupResponseTypeDef,
    DisassociateResolverEndpointIpAddressResponseTypeDef,
    DisassociateResolverQueryLogConfigResponseTypeDef,
    DisassociateResolverRuleResponseTypeDef,
    FilterTypeDef,
    GetFirewallConfigResponseTypeDef,
    GetFirewallDomainListResponseTypeDef,
    GetFirewallRuleGroupAssociationResponseTypeDef,
    GetFirewallRuleGroupPolicyResponseTypeDef,
    GetFirewallRuleGroupResponseTypeDef,
    GetResolverConfigResponseTypeDef,
    GetResolverDnssecConfigResponseTypeDef,
    GetResolverEndpointResponseTypeDef,
    GetResolverQueryLogConfigAssociationResponseTypeDef,
    GetResolverQueryLogConfigPolicyResponseTypeDef,
    GetResolverQueryLogConfigResponseTypeDef,
    GetResolverRuleAssociationResponseTypeDef,
    GetResolverRulePolicyResponseTypeDef,
    GetResolverRuleResponseTypeDef,
    ImportFirewallDomainsResponseTypeDef,
    IpAddressRequestTypeDef,
    IpAddressUpdateTypeDef,
    ListFirewallConfigsResponseTypeDef,
    ListFirewallDomainListsResponseTypeDef,
    ListFirewallDomainsResponseTypeDef,
    ListFirewallRuleGroupAssociationsResponseTypeDef,
    ListFirewallRuleGroupsResponseTypeDef,
    ListFirewallRulesResponseTypeDef,
    ListResolverConfigsResponseTypeDef,
    ListResolverDnssecConfigsResponseTypeDef,
    ListResolverEndpointIpAddressesResponseTypeDef,
    ListResolverEndpointsResponseTypeDef,
    ListResolverQueryLogConfigAssociationsResponseTypeDef,
    ListResolverQueryLogConfigsResponseTypeDef,
    ListResolverRuleAssociationsResponseTypeDef,
    ListResolverRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFirewallRuleGroupPolicyResponseTypeDef,
    PutResolverQueryLogConfigPolicyResponseTypeDef,
    PutResolverRulePolicyResponseTypeDef,
    ResolverRuleConfigTypeDef,
    TagTypeDef,
    TargetAddressTypeDef,
    UpdateFirewallConfigResponseTypeDef,
    UpdateFirewallDomainsResponseTypeDef,
    UpdateFirewallRuleGroupAssociationResponseTypeDef,
    UpdateFirewallRuleResponseTypeDef,
    UpdateResolverConfigResponseTypeDef,
    UpdateResolverDnssecConfigResponseTypeDef,
    UpdateResolverEndpointResponseTypeDef,
    UpdateResolverRuleResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Route53ResolverClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPolicyDocument: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnknownResourceException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53ResolverClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53ResolverClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#exceptions)
        """

    def associate_firewall_rule_group(
        self,
        *,
        CreatorRequestId: str,
        FirewallRuleGroupId: str,
        VpcId: str,
        Priority: int,
        Name: str,
        MutationProtection: MutationProtectionStatusType = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> AssociateFirewallRuleGroupResponseTypeDef:
        """
        Associates a  FirewallRuleGroup with a VPC, to provide DNS filtering for the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.associate_firewall_rule_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_firewall_rule_group)
        """

    def associate_resolver_endpoint_ip_address(
        self, *, ResolverEndpointId: str, IpAddress: IpAddressUpdateTypeDef
    ) -> AssociateResolverEndpointIpAddressResponseTypeDef:
        """
        Adds IP addresses to an inbound or an outbound Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.associate_resolver_endpoint_ip_address)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_endpoint_ip_address)
        """

    def associate_resolver_query_log_config(
        self, *, ResolverQueryLogConfigId: str, ResourceId: str
    ) -> AssociateResolverQueryLogConfigResponseTypeDef:
        """
        Associates an Amazon VPC with a specified query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.associate_resolver_query_log_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_query_log_config)
        """

    def associate_resolver_rule(
        self, *, ResolverRuleId: str, VPCId: str, Name: str = ...
    ) -> AssociateResolverRuleResponseTypeDef:
        """
        Associates a Resolver rule with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.associate_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#associate_resolver_rule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#can_paginate)
        """

    def create_firewall_domain_list(
        self, *, CreatorRequestId: str, Name: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateFirewallDomainListResponseTypeDef:
        """
        Creates an empty firewall domain list for use in DNS Firewall rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_firewall_domain_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_domain_list)
        """

    def create_firewall_rule(
        self,
        *,
        CreatorRequestId: str,
        FirewallRuleGroupId: str,
        FirewallDomainListId: str,
        Priority: int,
        Action: ActionType,
        Name: str,
        BlockResponse: BlockResponseType = ...,
        BlockOverrideDomain: str = ...,
        BlockOverrideDnsType: Literal["CNAME"] = ...,
        BlockOverrideTtl: int = ...
    ) -> CreateFirewallRuleResponseTypeDef:
        """
        Creates a single DNS Firewall rule in the specified rule group, using the
        specified domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_firewall_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_rule)
        """

    def create_firewall_rule_group(
        self, *, CreatorRequestId: str, Name: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateFirewallRuleGroupResponseTypeDef:
        """
        Creates an empty DNS Firewall rule group for filtering DNS network traffic in a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_firewall_rule_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_firewall_rule_group)
        """

    def create_resolver_endpoint(
        self,
        *,
        CreatorRequestId: str,
        SecurityGroupIds: Sequence[str],
        Direction: ResolverEndpointDirectionType,
        IpAddresses: Sequence[IpAddressRequestTypeDef],
        Name: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateResolverEndpointResponseTypeDef:
        """
        Creates a Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_resolver_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_endpoint)
        """

    def create_resolver_query_log_config(
        self,
        *,
        Name: str,
        DestinationArn: str,
        CreatorRequestId: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateResolverQueryLogConfigResponseTypeDef:
        """
        Creates a Resolver query logging configuration, which defines where you want
        Resolver to save DNS query logs that originate in your VPCs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_resolver_query_log_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_query_log_config)
        """

    def create_resolver_rule(
        self,
        *,
        CreatorRequestId: str,
        RuleType: RuleTypeOptionType,
        DomainName: str,
        Name: str = ...,
        TargetIps: Sequence[TargetAddressTypeDef] = ...,
        ResolverEndpointId: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateResolverRuleResponseTypeDef:
        """
        For DNS queries that originate in your VPCs, specifies which Resolver endpoint
        the queries pass through, one domain name that you want to forward to your
        network, and the IP addresses of the DNS resolvers in your network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.create_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#create_resolver_rule)
        """

    def delete_firewall_domain_list(
        self, *, FirewallDomainListId: str
    ) -> DeleteFirewallDomainListResponseTypeDef:
        """
        Deletes the specified domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_firewall_domain_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_domain_list)
        """

    def delete_firewall_rule(
        self, *, FirewallRuleGroupId: str, FirewallDomainListId: str
    ) -> DeleteFirewallRuleResponseTypeDef:
        """
        Deletes the specified firewall rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_firewall_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_rule)
        """

    def delete_firewall_rule_group(
        self, *, FirewallRuleGroupId: str
    ) -> DeleteFirewallRuleGroupResponseTypeDef:
        """
        Deletes the specified firewall rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_firewall_rule_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_firewall_rule_group)
        """

    def delete_resolver_endpoint(
        self, *, ResolverEndpointId: str
    ) -> DeleteResolverEndpointResponseTypeDef:
        """
        Deletes a Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_resolver_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_endpoint)
        """

    def delete_resolver_query_log_config(
        self, *, ResolverQueryLogConfigId: str
    ) -> DeleteResolverQueryLogConfigResponseTypeDef:
        """
        Deletes a query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_resolver_query_log_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_query_log_config)
        """

    def delete_resolver_rule(self, *, ResolverRuleId: str) -> DeleteResolverRuleResponseTypeDef:
        """
        Deletes a Resolver rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.delete_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#delete_resolver_rule)
        """

    def disassociate_firewall_rule_group(
        self, *, FirewallRuleGroupAssociationId: str
    ) -> DisassociateFirewallRuleGroupResponseTypeDef:
        """
        Disassociates a  FirewallRuleGroup from a VPC, to remove DNS filtering from the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.disassociate_firewall_rule_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_firewall_rule_group)
        """

    def disassociate_resolver_endpoint_ip_address(
        self, *, ResolverEndpointId: str, IpAddress: IpAddressUpdateTypeDef
    ) -> DisassociateResolverEndpointIpAddressResponseTypeDef:
        """
        Removes IP addresses from an inbound or an outbound Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.disassociate_resolver_endpoint_ip_address)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_endpoint_ip_address)
        """

    def disassociate_resolver_query_log_config(
        self, *, ResolverQueryLogConfigId: str, ResourceId: str
    ) -> DisassociateResolverQueryLogConfigResponseTypeDef:
        """
        Disassociates a VPC from a query logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.disassociate_resolver_query_log_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_query_log_config)
        """

    def disassociate_resolver_rule(
        self, *, VPCId: str, ResolverRuleId: str
    ) -> DisassociateResolverRuleResponseTypeDef:
        """
        Removes the association between a specified Resolver rule and a specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.disassociate_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#disassociate_resolver_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#generate_presigned_url)
        """

    def get_firewall_config(self, *, ResourceId: str) -> GetFirewallConfigResponseTypeDef:
        """
        Retrieves the configuration of the firewall behavior provided by DNS Firewall
        for a single VPC from Amazon Virtual Private Cloud (Amazon VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_firewall_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_config)
        """

    def get_firewall_domain_list(
        self, *, FirewallDomainListId: str
    ) -> GetFirewallDomainListResponseTypeDef:
        """
        Retrieves the specified firewall domain list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_firewall_domain_list)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_domain_list)
        """

    def get_firewall_rule_group(
        self, *, FirewallRuleGroupId: str
    ) -> GetFirewallRuleGroupResponseTypeDef:
        """
        Retrieves the specified firewall rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_firewall_rule_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group)
        """

    def get_firewall_rule_group_association(
        self, *, FirewallRuleGroupAssociationId: str
    ) -> GetFirewallRuleGroupAssociationResponseTypeDef:
        """
        Retrieves a firewall rule group association, which enables DNS filtering for a
        VPC with one rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_firewall_rule_group_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group_association)
        """

    def get_firewall_rule_group_policy(
        self, *, Arn: str
    ) -> GetFirewallRuleGroupPolicyResponseTypeDef:
        """
        Returns the Identity and Access Management (Amazon Web Services IAM) policy for
        sharing the specified rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_firewall_rule_group_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_firewall_rule_group_policy)
        """

    def get_resolver_config(self, *, ResourceId: str) -> GetResolverConfigResponseTypeDef:
        """
        Retrieves the behavior configuration of Route 53 Resolver behavior for a single
        VPC from Amazon Virtual Private Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_config)
        """

    def get_resolver_dnssec_config(
        self, *, ResourceId: str
    ) -> GetResolverDnssecConfigResponseTypeDef:
        """
        Gets DNSSEC validation information for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_dnssec_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_dnssec_config)
        """

    def get_resolver_endpoint(
        self, *, ResolverEndpointId: str
    ) -> GetResolverEndpointResponseTypeDef:
        """
        Gets information about a specified Resolver endpoint, such as whether it's an
        inbound or an outbound Resolver endpoint, and the current status of the
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_endpoint)
        """

    def get_resolver_query_log_config(
        self, *, ResolverQueryLogConfigId: str
    ) -> GetResolverQueryLogConfigResponseTypeDef:
        """
        Gets information about a specified Resolver query logging configuration, such as
        the number of VPCs that the configuration is logging queries for and the
        location that logs are sent to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_query_log_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config)
        """

    def get_resolver_query_log_config_association(
        self, *, ResolverQueryLogConfigAssociationId: str
    ) -> GetResolverQueryLogConfigAssociationResponseTypeDef:
        """
        Gets information about a specified association between a Resolver query logging
        configuration and an Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_query_log_config_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config_association)
        """

    def get_resolver_query_log_config_policy(
        self, *, Arn: str
    ) -> GetResolverQueryLogConfigPolicyResponseTypeDef:
        """
        Gets information about a query logging policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_query_log_config_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_query_log_config_policy)
        """

    def get_resolver_rule(self, *, ResolverRuleId: str) -> GetResolverRuleResponseTypeDef:
        """
        Gets information about a specified Resolver rule, such as the domain name that
        the rule forwards DNS queries for and the ID of the outbound Resolver endpoint
        that the rule is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule)
        """

    def get_resolver_rule_association(
        self, *, ResolverRuleAssociationId: str
    ) -> GetResolverRuleAssociationResponseTypeDef:
        """
        Gets information about an association between a specified Resolver rule and a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_rule_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule_association)
        """

    def get_resolver_rule_policy(self, *, Arn: str) -> GetResolverRulePolicyResponseTypeDef:
        """
        Gets information about the Resolver rule policy for a specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_resolver_rule_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_resolver_rule_policy)
        """

    def import_firewall_domains(
        self, *, FirewallDomainListId: str, Operation: Literal["REPLACE"], DomainFileUrl: str
    ) -> ImportFirewallDomainsResponseTypeDef:
        """
        Imports domain names from a file into a domain list, for use in a DNS firewall
        rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.import_firewall_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#import_firewall_domains)
        """

    def list_firewall_configs(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFirewallConfigsResponseTypeDef:
        """
        Retrieves the firewall configurations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_configs)
        """

    def list_firewall_domain_lists(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFirewallDomainListsResponseTypeDef:
        """
        Retrieves the firewall domain lists that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_domain_lists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_domain_lists)
        """

    def list_firewall_domains(
        self, *, FirewallDomainListId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFirewallDomainsResponseTypeDef:
        """
        Retrieves the domains that you have defined for the specified firewall domain
        list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_domains)
        """

    def list_firewall_rule_group_associations(
        self,
        *,
        FirewallRuleGroupId: str = ...,
        VpcId: str = ...,
        Priority: int = ...,
        Status: FirewallRuleGroupAssociationStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListFirewallRuleGroupAssociationsResponseTypeDef:
        """
        Retrieves the firewall rule group associations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_rule_group_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rule_group_associations)
        """

    def list_firewall_rule_groups(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFirewallRuleGroupsResponseTypeDef:
        """
        Retrieves the minimal high-level information for the rule groups that you have
        defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_rule_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rule_groups)
        """

    def list_firewall_rules(
        self,
        *,
        FirewallRuleGroupId: str,
        Priority: int = ...,
        Action: ActionType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListFirewallRulesResponseTypeDef:
        """
        Retrieves the firewall rules that you have defined for the specified firewall
        rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_firewall_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_firewall_rules)
        """

    def list_resolver_configs(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListResolverConfigsResponseTypeDef:
        """
        Retrieves the Resolver configurations that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_configs)
        """

    def list_resolver_dnssec_configs(
        self, *, MaxResults: int = ..., NextToken: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> ListResolverDnssecConfigsResponseTypeDef:
        """
        Lists the configurations for DNSSEC validation that are associated with the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_dnssec_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_dnssec_configs)
        """

    def list_resolver_endpoint_ip_addresses(
        self, *, ResolverEndpointId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListResolverEndpointIpAddressesResponseTypeDef:
        """
        Gets the IP addresses for a specified Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_endpoint_ip_addresses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_endpoint_ip_addresses)
        """

    def list_resolver_endpoints(
        self, *, MaxResults: int = ..., NextToken: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> ListResolverEndpointsResponseTypeDef:
        """
        Lists all the Resolver endpoints that were created using the current Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_endpoints)
        """

    def list_resolver_query_log_config_associations(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...
    ) -> ListResolverQueryLogConfigAssociationsResponseTypeDef:
        """
        Lists information about associations between Amazon VPCs and query logging
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_query_log_config_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_query_log_config_associations)
        """

    def list_resolver_query_log_configs(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...
    ) -> ListResolverQueryLogConfigsResponseTypeDef:
        """
        Lists information about the specified query logging configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_query_log_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_query_log_configs)
        """

    def list_resolver_rule_associations(
        self, *, MaxResults: int = ..., NextToken: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> ListResolverRuleAssociationsResponseTypeDef:
        """
        Lists the associations that were created between Resolver rules and VPCs using
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_rule_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_rule_associations)
        """

    def list_resolver_rules(
        self, *, MaxResults: int = ..., NextToken: str = ..., Filters: Sequence[FilterTypeDef] = ...
    ) -> ListResolverRulesResponseTypeDef:
        """
        Lists the Resolver rules that were created using the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_resolver_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_resolver_rules)
        """

    def list_tags_for_resource(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that you associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#list_tags_for_resource)
        """

    def put_firewall_rule_group_policy(
        self, *, Arn: str, FirewallRuleGroupPolicy: str
    ) -> PutFirewallRuleGroupPolicyResponseTypeDef:
        """
        Attaches an Identity and Access Management (Amazon Web Services IAM) policy for
        sharing the rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.put_firewall_rule_group_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_firewall_rule_group_policy)
        """

    def put_resolver_query_log_config_policy(
        self, *, Arn: str, ResolverQueryLogConfigPolicy: str
    ) -> PutResolverQueryLogConfigPolicyResponseTypeDef:
        """
        Specifies an Amazon Web Services account that you want to share a query logging
        configuration with, the query logging configuration that you want to share, and
        the operations that you want the account to be able to perform on the
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.put_resolver_query_log_config_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_resolver_query_log_config_policy)
        """

    def put_resolver_rule_policy(
        self, *, Arn: str, ResolverRulePolicy: str
    ) -> PutResolverRulePolicyResponseTypeDef:
        """
        Specifies an Amazon Web Services rule that you want to share with another
        account, the account that you want to share the rule with, and the operations
        that you want the account to be able to perform on the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.put_resolver_rule_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#put_resolver_rule_policy)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#untag_resource)
        """

    def update_firewall_config(
        self, *, ResourceId: str, FirewallFailOpen: FirewallFailOpenStatusType
    ) -> UpdateFirewallConfigResponseTypeDef:
        """
        Updates the configuration of the firewall behavior provided by DNS Firewall for
        a single VPC from Amazon Virtual Private Cloud (Amazon VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_firewall_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_config)
        """

    def update_firewall_domains(
        self,
        *,
        FirewallDomainListId: str,
        Operation: FirewallDomainUpdateOperationType,
        Domains: Sequence[str]
    ) -> UpdateFirewallDomainsResponseTypeDef:
        """
        Updates the firewall domain list from an array of domain specifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_firewall_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_domains)
        """

    def update_firewall_rule(
        self,
        *,
        FirewallRuleGroupId: str,
        FirewallDomainListId: str,
        Priority: int = ...,
        Action: ActionType = ...,
        BlockResponse: BlockResponseType = ...,
        BlockOverrideDomain: str = ...,
        BlockOverrideDnsType: Literal["CNAME"] = ...,
        BlockOverrideTtl: int = ...,
        Name: str = ...
    ) -> UpdateFirewallRuleResponseTypeDef:
        """
        Updates the specified firewall rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_firewall_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_rule)
        """

    def update_firewall_rule_group_association(
        self,
        *,
        FirewallRuleGroupAssociationId: str,
        Priority: int = ...,
        MutationProtection: MutationProtectionStatusType = ...,
        Name: str = ...
    ) -> UpdateFirewallRuleGroupAssociationResponseTypeDef:
        """
        Changes the association of a  FirewallRuleGroup with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_firewall_rule_group_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_firewall_rule_group_association)
        """

    def update_resolver_config(
        self, *, ResourceId: str, AutodefinedReverseFlag: AutodefinedReverseFlagType
    ) -> UpdateResolverConfigResponseTypeDef:
        """
        Updates the behavior configuration of Route 53 Resolver behavior for a single
        VPC from Amazon Virtual Private Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_resolver_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_config)
        """

    def update_resolver_dnssec_config(
        self, *, ResourceId: str, Validation: ValidationType
    ) -> UpdateResolverDnssecConfigResponseTypeDef:
        """
        Updates an existing DNSSEC validation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_resolver_dnssec_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_dnssec_config)
        """

    def update_resolver_endpoint(
        self, *, ResolverEndpointId: str, Name: str = ...
    ) -> UpdateResolverEndpointResponseTypeDef:
        """
        Updates the name of an inbound or an outbound Resolver endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_resolver_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_endpoint)
        """

    def update_resolver_rule(
        self, *, ResolverRuleId: str, Config: ResolverRuleConfigTypeDef
    ) -> UpdateResolverRuleResponseTypeDef:
        """
        Updates settings for a specified Resolver rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.update_resolver_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#update_resolver_rule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_configs"]
    ) -> ListFirewallConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_domain_lists"]
    ) -> ListFirewallDomainListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_domains"]
    ) -> ListFirewallDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rule_group_associations"]
    ) -> ListFirewallRuleGroupAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rule_groups"]
    ) -> ListFirewallRuleGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_rules"]
    ) -> ListFirewallRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_configs"]
    ) -> ListResolverConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_dnssec_configs"]
    ) -> ListResolverDnssecConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_endpoint_ip_addresses"]
    ) -> ListResolverEndpointIpAddressesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_endpoints"]
    ) -> ListResolverEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_query_log_config_associations"]
    ) -> ListResolverQueryLogConfigAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_query_log_configs"]
    ) -> ListResolverQueryLogConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_rule_associations"]
    ) -> ListResolverRuleAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolver_rules"]
    ) -> ListResolverRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/client/#get_paginator)
        """
