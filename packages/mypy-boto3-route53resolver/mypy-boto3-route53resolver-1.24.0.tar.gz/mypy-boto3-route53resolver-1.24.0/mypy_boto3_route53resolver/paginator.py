"""
Type annotations for route53resolver service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53resolver.client import Route53ResolverClient
    from mypy_boto3_route53resolver.paginator import (
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

    session = Session()
    client: Route53ResolverClient = session.client("route53resolver")

    list_firewall_configs_paginator: ListFirewallConfigsPaginator = client.get_paginator("list_firewall_configs")
    list_firewall_domain_lists_paginator: ListFirewallDomainListsPaginator = client.get_paginator("list_firewall_domain_lists")
    list_firewall_domains_paginator: ListFirewallDomainsPaginator = client.get_paginator("list_firewall_domains")
    list_firewall_rule_group_associations_paginator: ListFirewallRuleGroupAssociationsPaginator = client.get_paginator("list_firewall_rule_group_associations")
    list_firewall_rule_groups_paginator: ListFirewallRuleGroupsPaginator = client.get_paginator("list_firewall_rule_groups")
    list_firewall_rules_paginator: ListFirewallRulesPaginator = client.get_paginator("list_firewall_rules")
    list_resolver_configs_paginator: ListResolverConfigsPaginator = client.get_paginator("list_resolver_configs")
    list_resolver_dnssec_configs_paginator: ListResolverDnssecConfigsPaginator = client.get_paginator("list_resolver_dnssec_configs")
    list_resolver_endpoint_ip_addresses_paginator: ListResolverEndpointIpAddressesPaginator = client.get_paginator("list_resolver_endpoint_ip_addresses")
    list_resolver_endpoints_paginator: ListResolverEndpointsPaginator = client.get_paginator("list_resolver_endpoints")
    list_resolver_query_log_config_associations_paginator: ListResolverQueryLogConfigAssociationsPaginator = client.get_paginator("list_resolver_query_log_config_associations")
    list_resolver_query_log_configs_paginator: ListResolverQueryLogConfigsPaginator = client.get_paginator("list_resolver_query_log_configs")
    list_resolver_rule_associations_paginator: ListResolverRuleAssociationsPaginator = client.get_paginator("list_resolver_rule_associations")
    list_resolver_rules_paginator: ListResolverRulesPaginator = client.get_paginator("list_resolver_rules")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ActionType, FirewallRuleGroupAssociationStatusType, SortOrderType
from .type_defs import (
    FilterTypeDef,
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
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListFirewallConfigsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRuleGroupAssociationsPaginator",
    "ListFirewallRuleGroupsPaginator",
    "ListFirewallRulesPaginator",
    "ListResolverConfigsPaginator",
    "ListResolverDnssecConfigsPaginator",
    "ListResolverEndpointIpAddressesPaginator",
    "ListResolverEndpointsPaginator",
    "ListResolverQueryLogConfigAssociationsPaginator",
    "ListResolverQueryLogConfigsPaginator",
    "ListResolverRuleAssociationsPaginator",
    "ListResolverRulesPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListFirewallConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallconfigspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallconfigspaginator)
        """


class ListFirewallDomainListsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomainLists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainlistspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallDomainListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomainLists.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainlistspaginator)
        """


class ListFirewallDomainsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomains)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainspaginator)
    """

    def paginate(
        self, *, FirewallDomainListId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomains.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewalldomainspaginator)
        """


class ListFirewallRuleGroupAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
    """

    def paginate(
        self,
        *,
        FirewallRuleGroupId: str = ...,
        VpcId: str = ...,
        Priority: int = ...,
        Status: FirewallRuleGroupAssociationStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallRuleGroupAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
        """


class ListFirewallRuleGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulegroupspaginator)
        """


class ListFirewallRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulespaginator)
    """

    def paginate(
        self,
        *,
        FirewallRuleGroupId: str,
        Priority: int = ...,
        Action: ActionType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFirewallRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listfirewallrulespaginator)
        """


class ListResolverConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverconfigspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverconfigspaginator)
        """


class ListResolverDnssecConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverDnssecConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverdnssecconfigspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverDnssecConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverDnssecConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverdnssecconfigspaginator)
        """


class ListResolverEndpointIpAddressesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointipaddressespaginator)
    """

    def paginate(
        self, *, ResolverEndpointId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverEndpointIpAddressesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointipaddressespaginator)
        """


class ListResolverEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverendpointspaginator)
        """


class ListResolverQueryLogConfigAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverQueryLogConfigAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
        """


class ListResolverQueryLogConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverQueryLogConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverquerylogconfigspaginator)
        """


class ListResolverRuleAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRuleAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverruleassociationspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverRuleAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRuleAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverruleassociationspaginator)
        """


class ListResolverRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverrulespaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListResolverRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listresolverrulespaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/paginators/#listtagsforresourcepaginator)
        """
