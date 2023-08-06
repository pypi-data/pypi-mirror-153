"""
Type annotations for config service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_config.client import ConfigServiceClient
    from mypy_boto3_config.paginator import (
        DescribeAggregateComplianceByConfigRulesPaginator,
        DescribeAggregateComplianceByConformancePacksPaginator,
        DescribeAggregationAuthorizationsPaginator,
        DescribeComplianceByConfigRulePaginator,
        DescribeComplianceByResourcePaginator,
        DescribeConfigRuleEvaluationStatusPaginator,
        DescribeConfigRulesPaginator,
        DescribeConfigurationAggregatorSourcesStatusPaginator,
        DescribeConfigurationAggregatorsPaginator,
        DescribeConformancePackStatusPaginator,
        DescribeConformancePacksPaginator,
        DescribeOrganizationConfigRuleStatusesPaginator,
        DescribeOrganizationConfigRulesPaginator,
        DescribeOrganizationConformancePackStatusesPaginator,
        DescribeOrganizationConformancePacksPaginator,
        DescribePendingAggregationRequestsPaginator,
        DescribeRemediationExecutionStatusPaginator,
        DescribeRetentionConfigurationsPaginator,
        GetAggregateComplianceDetailsByConfigRulePaginator,
        GetComplianceDetailsByConfigRulePaginator,
        GetComplianceDetailsByResourcePaginator,
        GetConformancePackComplianceSummaryPaginator,
        GetOrganizationConfigRuleDetailedStatusPaginator,
        GetOrganizationConformancePackDetailedStatusPaginator,
        GetResourceConfigHistoryPaginator,
        ListAggregateDiscoveredResourcesPaginator,
        ListDiscoveredResourcesPaginator,
        ListTagsForResourcePaginator,
        SelectAggregateResourceConfigPaginator,
        SelectResourceConfigPaginator,
    )

    session = Session()
    client: ConfigServiceClient = session.client("config")

    describe_aggregate_compliance_by_config_rules_paginator: DescribeAggregateComplianceByConfigRulesPaginator = client.get_paginator("describe_aggregate_compliance_by_config_rules")
    describe_aggregate_compliance_by_conformance_packs_paginator: DescribeAggregateComplianceByConformancePacksPaginator = client.get_paginator("describe_aggregate_compliance_by_conformance_packs")
    describe_aggregation_authorizations_paginator: DescribeAggregationAuthorizationsPaginator = client.get_paginator("describe_aggregation_authorizations")
    describe_compliance_by_config_rule_paginator: DescribeComplianceByConfigRulePaginator = client.get_paginator("describe_compliance_by_config_rule")
    describe_compliance_by_resource_paginator: DescribeComplianceByResourcePaginator = client.get_paginator("describe_compliance_by_resource")
    describe_config_rule_evaluation_status_paginator: DescribeConfigRuleEvaluationStatusPaginator = client.get_paginator("describe_config_rule_evaluation_status")
    describe_config_rules_paginator: DescribeConfigRulesPaginator = client.get_paginator("describe_config_rules")
    describe_configuration_aggregator_sources_status_paginator: DescribeConfigurationAggregatorSourcesStatusPaginator = client.get_paginator("describe_configuration_aggregator_sources_status")
    describe_configuration_aggregators_paginator: DescribeConfigurationAggregatorsPaginator = client.get_paginator("describe_configuration_aggregators")
    describe_conformance_pack_status_paginator: DescribeConformancePackStatusPaginator = client.get_paginator("describe_conformance_pack_status")
    describe_conformance_packs_paginator: DescribeConformancePacksPaginator = client.get_paginator("describe_conformance_packs")
    describe_organization_config_rule_statuses_paginator: DescribeOrganizationConfigRuleStatusesPaginator = client.get_paginator("describe_organization_config_rule_statuses")
    describe_organization_config_rules_paginator: DescribeOrganizationConfigRulesPaginator = client.get_paginator("describe_organization_config_rules")
    describe_organization_conformance_pack_statuses_paginator: DescribeOrganizationConformancePackStatusesPaginator = client.get_paginator("describe_organization_conformance_pack_statuses")
    describe_organization_conformance_packs_paginator: DescribeOrganizationConformancePacksPaginator = client.get_paginator("describe_organization_conformance_packs")
    describe_pending_aggregation_requests_paginator: DescribePendingAggregationRequestsPaginator = client.get_paginator("describe_pending_aggregation_requests")
    describe_remediation_execution_status_paginator: DescribeRemediationExecutionStatusPaginator = client.get_paginator("describe_remediation_execution_status")
    describe_retention_configurations_paginator: DescribeRetentionConfigurationsPaginator = client.get_paginator("describe_retention_configurations")
    get_aggregate_compliance_details_by_config_rule_paginator: GetAggregateComplianceDetailsByConfigRulePaginator = client.get_paginator("get_aggregate_compliance_details_by_config_rule")
    get_compliance_details_by_config_rule_paginator: GetComplianceDetailsByConfigRulePaginator = client.get_paginator("get_compliance_details_by_config_rule")
    get_compliance_details_by_resource_paginator: GetComplianceDetailsByResourcePaginator = client.get_paginator("get_compliance_details_by_resource")
    get_conformance_pack_compliance_summary_paginator: GetConformancePackComplianceSummaryPaginator = client.get_paginator("get_conformance_pack_compliance_summary")
    get_organization_config_rule_detailed_status_paginator: GetOrganizationConfigRuleDetailedStatusPaginator = client.get_paginator("get_organization_config_rule_detailed_status")
    get_organization_conformance_pack_detailed_status_paginator: GetOrganizationConformancePackDetailedStatusPaginator = client.get_paginator("get_organization_conformance_pack_detailed_status")
    get_resource_config_history_paginator: GetResourceConfigHistoryPaginator = client.get_paginator("get_resource_config_history")
    list_aggregate_discovered_resources_paginator: ListAggregateDiscoveredResourcesPaginator = client.get_paginator("list_aggregate_discovered_resources")
    list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    select_aggregate_resource_config_paginator: SelectAggregateResourceConfigPaginator = client.get_paginator("select_aggregate_resource_config")
    select_resource_config_paginator: SelectResourceConfigPaginator = client.get_paginator("select_resource_config")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    AggregatedSourceStatusTypeType,
    ChronologicalOrderType,
    ComplianceTypeType,
    ResourceTypeType,
)
from .type_defs import (
    AggregateConformancePackComplianceFiltersTypeDef,
    ConfigRuleComplianceFiltersTypeDef,
    DescribeAggregateComplianceByConfigRulesResponseTypeDef,
    DescribeAggregateComplianceByConformancePacksResponseTypeDef,
    DescribeAggregationAuthorizationsResponseTypeDef,
    DescribeComplianceByConfigRuleResponseTypeDef,
    DescribeComplianceByResourceResponseTypeDef,
    DescribeConfigRuleEvaluationStatusResponseTypeDef,
    DescribeConfigRulesResponseTypeDef,
    DescribeConfigurationAggregatorSourcesStatusResponseTypeDef,
    DescribeConfigurationAggregatorsResponseTypeDef,
    DescribeConformancePacksResponseTypeDef,
    DescribeConformancePackStatusResponseTypeDef,
    DescribeOrganizationConfigRulesResponseTypeDef,
    DescribeOrganizationConfigRuleStatusesResponseTypeDef,
    DescribeOrganizationConformancePacksResponseTypeDef,
    DescribeOrganizationConformancePackStatusesResponseTypeDef,
    DescribePendingAggregationRequestsResponseTypeDef,
    DescribeRemediationExecutionStatusResponseTypeDef,
    DescribeRetentionConfigurationsResponseTypeDef,
    GetAggregateComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByResourceResponseTypeDef,
    GetConformancePackComplianceSummaryResponseTypeDef,
    GetOrganizationConfigRuleDetailedStatusResponseTypeDef,
    GetOrganizationConformancePackDetailedStatusResponseTypeDef,
    GetResourceConfigHistoryResponseTypeDef,
    ListAggregateDiscoveredResourcesResponseTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OrganizationResourceDetailedStatusFiltersTypeDef,
    PaginatorConfigTypeDef,
    ResourceFiltersTypeDef,
    ResourceKeyTypeDef,
    SelectAggregateResourceConfigResponseTypeDef,
    SelectResourceConfigResponseTypeDef,
    StatusDetailFiltersTypeDef,
)

__all__ = (
    "DescribeAggregateComplianceByConfigRulesPaginator",
    "DescribeAggregateComplianceByConformancePacksPaginator",
    "DescribeAggregationAuthorizationsPaginator",
    "DescribeComplianceByConfigRulePaginator",
    "DescribeComplianceByResourcePaginator",
    "DescribeConfigRuleEvaluationStatusPaginator",
    "DescribeConfigRulesPaginator",
    "DescribeConfigurationAggregatorSourcesStatusPaginator",
    "DescribeConfigurationAggregatorsPaginator",
    "DescribeConformancePackStatusPaginator",
    "DescribeConformancePacksPaginator",
    "DescribeOrganizationConfigRuleStatusesPaginator",
    "DescribeOrganizationConfigRulesPaginator",
    "DescribeOrganizationConformancePackStatusesPaginator",
    "DescribeOrganizationConformancePacksPaginator",
    "DescribePendingAggregationRequestsPaginator",
    "DescribeRemediationExecutionStatusPaginator",
    "DescribeRetentionConfigurationsPaginator",
    "GetAggregateComplianceDetailsByConfigRulePaginator",
    "GetComplianceDetailsByConfigRulePaginator",
    "GetComplianceDetailsByResourcePaginator",
    "GetConformancePackComplianceSummaryPaginator",
    "GetOrganizationConfigRuleDetailedStatusPaginator",
    "GetOrganizationConformancePackDetailedStatusPaginator",
    "GetResourceConfigHistoryPaginator",
    "ListAggregateDiscoveredResourcesPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListTagsForResourcePaginator",
    "SelectAggregateResourceConfigPaginator",
    "SelectResourceConfigPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAggregateComplianceByConfigRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregateComplianceByConfigRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregatecompliancebyconfigrulespaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: ConfigRuleComplianceFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAggregateComplianceByConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregateComplianceByConfigRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregatecompliancebyconfigrulespaginator)
        """


class DescribeAggregateComplianceByConformancePacksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregateComplianceByConformancePacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregatecompliancebyconformancepackspaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: AggregateConformancePackComplianceFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAggregateComplianceByConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregateComplianceByConformancePacks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregatecompliancebyconformancepackspaginator)
        """


class DescribeAggregationAuthorizationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregationAuthorizations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregationauthorizationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAggregationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeAggregationAuthorizations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeaggregationauthorizationspaginator)
        """


class DescribeComplianceByConfigRulePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeComplianceByConfigRule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describecompliancebyconfigrulepaginator)
    """

    def paginate(
        self,
        *,
        ConfigRuleNames: Sequence[str] = ...,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeComplianceByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeComplianceByConfigRule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describecompliancebyconfigrulepaginator)
        """


class DescribeComplianceByResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeComplianceByResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describecompliancebyresourcepaginator)
    """

    def paginate(
        self,
        *,
        ResourceType: str = ...,
        ResourceId: str = ...,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeComplianceByResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeComplianceByResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describecompliancebyresourcepaginator)
        """


class DescribeConfigRuleEvaluationStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigRuleEvaluationStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigruleevaluationstatuspaginator)
    """

    def paginate(
        self,
        *,
        ConfigRuleNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConfigRuleEvaluationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigRuleEvaluationStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigruleevaluationstatuspaginator)
        """


class DescribeConfigRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigrulespaginator)
    """

    def paginate(
        self,
        *,
        ConfigRuleNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigrulespaginator)
        """


class DescribeConfigurationAggregatorSourcesStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigurationAggregatorSourcesStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigurationaggregatorsourcesstatuspaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorName: str,
        UpdateStatus: Sequence[AggregatedSourceStatusTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConfigurationAggregatorSourcesStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigurationAggregatorSourcesStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigurationaggregatorsourcesstatuspaginator)
        """


class DescribeConfigurationAggregatorsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigurationAggregators)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigurationaggregatorspaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConfigurationAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConfigurationAggregators.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconfigurationaggregatorspaginator)
        """


class DescribeConformancePackStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConformancePackStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconformancepackstatuspaginator)
    """

    def paginate(
        self,
        *,
        ConformancePackNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConformancePackStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConformancePackStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconformancepackstatuspaginator)
        """


class DescribeConformancePacksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConformancePacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconformancepackspaginator)
    """

    def paginate(
        self,
        *,
        ConformancePackNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeConformancePacks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeconformancepackspaginator)
        """


class DescribeOrganizationConfigRuleStatusesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConfigRuleStatuses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconfigrulestatusespaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConfigRuleNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOrganizationConfigRuleStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConfigRuleStatuses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconfigrulestatusespaginator)
        """


class DescribeOrganizationConfigRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConfigRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconfigrulespaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConfigRuleNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOrganizationConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConfigRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconfigrulespaginator)
        """


class DescribeOrganizationConformancePackStatusesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConformancePackStatuses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconformancepackstatusespaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConformancePackNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOrganizationConformancePackStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConformancePackStatuses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconformancepackstatusespaginator)
        """


class DescribeOrganizationConformancePacksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConformancePacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconformancepackspaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConformancePackNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeOrganizationConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeOrganizationConformancePacks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeorganizationconformancepackspaginator)
        """


class DescribePendingAggregationRequestsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribePendingAggregationRequests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describependingaggregationrequestspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePendingAggregationRequestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribePendingAggregationRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describependingaggregationrequestspaginator)
        """


class DescribeRemediationExecutionStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeRemediationExecutionStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeremediationexecutionstatuspaginator)
    """

    def paginate(
        self,
        *,
        ConfigRuleName: str,
        ResourceKeys: Sequence[ResourceKeyTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRemediationExecutionStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeRemediationExecutionStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeremediationexecutionstatuspaginator)
        """


class DescribeRetentionConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeRetentionConfigurations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeretentionconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        RetentionConfigurationNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRetentionConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.DescribeRetentionConfigurations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#describeretentionconfigurationspaginator)
        """


class GetAggregateComplianceDetailsByConfigRulePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetAggregateComplianceDetailsByConfigRule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getaggregatecompliancedetailsbyconfigrulepaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorName: str,
        ConfigRuleName: str,
        AccountId: str,
        AwsRegion: str,
        ComplianceType: ComplianceTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAggregateComplianceDetailsByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetAggregateComplianceDetailsByConfigRule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getaggregatecompliancedetailsbyconfigrulepaginator)
        """


class GetComplianceDetailsByConfigRulePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetComplianceDetailsByConfigRule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getcompliancedetailsbyconfigrulepaginator)
    """

    def paginate(
        self,
        *,
        ConfigRuleName: str,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetComplianceDetailsByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetComplianceDetailsByConfigRule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getcompliancedetailsbyconfigrulepaginator)
        """


class GetComplianceDetailsByResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetComplianceDetailsByResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getcompliancedetailsbyresourcepaginator)
    """

    def paginate(
        self,
        *,
        ResourceType: str,
        ResourceId: str,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetComplianceDetailsByResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetComplianceDetailsByResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getcompliancedetailsbyresourcepaginator)
        """


class GetConformancePackComplianceSummaryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetConformancePackComplianceSummary)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getconformancepackcompliancesummarypaginator)
    """

    def paginate(
        self, *, ConformancePackNames: Sequence[str], PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetConformancePackComplianceSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetConformancePackComplianceSummary.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getconformancepackcompliancesummarypaginator)
        """


class GetOrganizationConfigRuleDetailedStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetOrganizationConfigRuleDetailedStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getorganizationconfigruledetailedstatuspaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConfigRuleName: str,
        Filters: StatusDetailFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetOrganizationConfigRuleDetailedStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetOrganizationConfigRuleDetailedStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getorganizationconfigruledetailedstatuspaginator)
        """


class GetOrganizationConformancePackDetailedStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetOrganizationConformancePackDetailedStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getorganizationconformancepackdetailedstatuspaginator)
    """

    def paginate(
        self,
        *,
        OrganizationConformancePackName: str,
        Filters: OrganizationResourceDetailedStatusFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetOrganizationConformancePackDetailedStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetOrganizationConformancePackDetailedStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getorganizationconformancepackdetailedstatuspaginator)
        """


class GetResourceConfigHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetResourceConfigHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getresourceconfighistorypaginator)
    """

    def paginate(
        self,
        *,
        resourceType: ResourceTypeType,
        resourceId: str,
        laterTime: Union[datetime, str] = ...,
        earlierTime: Union[datetime, str] = ...,
        chronologicalOrder: ChronologicalOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetResourceConfigHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.GetResourceConfigHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#getresourceconfighistorypaginator)
        """


class ListAggregateDiscoveredResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListAggregateDiscoveredResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listaggregatediscoveredresourcespaginator)
    """

    def paginate(
        self,
        *,
        ConfigurationAggregatorName: str,
        ResourceType: ResourceTypeType,
        Filters: ResourceFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAggregateDiscoveredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListAggregateDiscoveredResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listaggregatediscoveredresourcespaginator)
        """


class ListDiscoveredResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListDiscoveredResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listdiscoveredresourcespaginator)
    """

    def paginate(
        self,
        *,
        resourceType: ResourceTypeType,
        resourceIds: Sequence[str] = ...,
        resourceName: str = ...,
        includeDeletedResources: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDiscoveredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListDiscoveredResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listdiscoveredresourcespaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#listtagsforresourcepaginator)
        """


class SelectAggregateResourceConfigPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.SelectAggregateResourceConfig)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#selectaggregateresourceconfigpaginator)
    """

    def paginate(
        self,
        *,
        Expression: str,
        ConfigurationAggregatorName: str,
        MaxResults: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SelectAggregateResourceConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.SelectAggregateResourceConfig.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#selectaggregateresourceconfigpaginator)
        """


class SelectResourceConfigPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.SelectResourceConfig)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#selectresourceconfigpaginator)
    """

    def paginate(
        self, *, Expression: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SelectResourceConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Paginator.SelectResourceConfig.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/paginators/#selectresourceconfigpaginator)
        """
