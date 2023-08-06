"""
Type annotations for config service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_config.client import ConfigServiceClient

    session = Session()
    client: ConfigServiceClient = session.client("config")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AggregateConformancePackComplianceSummaryGroupKeyType,
    AggregatedSourceStatusTypeType,
    ChronologicalOrderType,
    ComplianceTypeType,
    ConfigRuleComplianceSummaryGroupKeyType,
    ResourceCountGroupKeyType,
    ResourceTypeType,
)
from .paginator import (
    DescribeAggregateComplianceByConfigRulesPaginator,
    DescribeAggregateComplianceByConformancePacksPaginator,
    DescribeAggregationAuthorizationsPaginator,
    DescribeComplianceByConfigRulePaginator,
    DescribeComplianceByResourcePaginator,
    DescribeConfigRuleEvaluationStatusPaginator,
    DescribeConfigRulesPaginator,
    DescribeConfigurationAggregatorSourcesStatusPaginator,
    DescribeConfigurationAggregatorsPaginator,
    DescribeConformancePacksPaginator,
    DescribeConformancePackStatusPaginator,
    DescribeOrganizationConfigRulesPaginator,
    DescribeOrganizationConfigRuleStatusesPaginator,
    DescribeOrganizationConformancePacksPaginator,
    DescribeOrganizationConformancePackStatusesPaginator,
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
from .type_defs import (
    AccountAggregationSourceTypeDef,
    AggregateConformancePackComplianceFiltersTypeDef,
    AggregateConformancePackComplianceSummaryFiltersTypeDef,
    AggregateResourceIdentifierTypeDef,
    BatchGetAggregateResourceConfigResponseTypeDef,
    BatchGetResourceConfigResponseTypeDef,
    ConfigRuleComplianceFiltersTypeDef,
    ConfigRuleComplianceSummaryFiltersTypeDef,
    ConfigRuleTypeDef,
    ConfigurationRecorderTypeDef,
    ConformancePackComplianceFiltersTypeDef,
    ConformancePackEvaluationFiltersTypeDef,
    ConformancePackInputParameterTypeDef,
    DeleteRemediationExceptionsResponseTypeDef,
    DeliverConfigSnapshotResponseTypeDef,
    DeliveryChannelTypeDef,
    DescribeAggregateComplianceByConfigRulesResponseTypeDef,
    DescribeAggregateComplianceByConformancePacksResponseTypeDef,
    DescribeAggregationAuthorizationsResponseTypeDef,
    DescribeComplianceByConfigRuleResponseTypeDef,
    DescribeComplianceByResourceResponseTypeDef,
    DescribeConfigRuleEvaluationStatusResponseTypeDef,
    DescribeConfigRulesResponseTypeDef,
    DescribeConfigurationAggregatorSourcesStatusResponseTypeDef,
    DescribeConfigurationAggregatorsResponseTypeDef,
    DescribeConfigurationRecordersResponseTypeDef,
    DescribeConfigurationRecorderStatusResponseTypeDef,
    DescribeConformancePackComplianceResponseTypeDef,
    DescribeConformancePacksResponseTypeDef,
    DescribeConformancePackStatusResponseTypeDef,
    DescribeDeliveryChannelsResponseTypeDef,
    DescribeDeliveryChannelStatusResponseTypeDef,
    DescribeOrganizationConfigRulesResponseTypeDef,
    DescribeOrganizationConfigRuleStatusesResponseTypeDef,
    DescribeOrganizationConformancePacksResponseTypeDef,
    DescribeOrganizationConformancePackStatusesResponseTypeDef,
    DescribePendingAggregationRequestsResponseTypeDef,
    DescribeRemediationConfigurationsResponseTypeDef,
    DescribeRemediationExceptionsResponseTypeDef,
    DescribeRemediationExecutionStatusResponseTypeDef,
    DescribeRetentionConfigurationsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluationTypeDef,
    ExternalEvaluationTypeDef,
    GetAggregateComplianceDetailsByConfigRuleResponseTypeDef,
    GetAggregateConfigRuleComplianceSummaryResponseTypeDef,
    GetAggregateConformancePackComplianceSummaryResponseTypeDef,
    GetAggregateDiscoveredResourceCountsResponseTypeDef,
    GetAggregateResourceConfigResponseTypeDef,
    GetComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByResourceResponseTypeDef,
    GetComplianceSummaryByConfigRuleResponseTypeDef,
    GetComplianceSummaryByResourceTypeResponseTypeDef,
    GetConformancePackComplianceDetailsResponseTypeDef,
    GetConformancePackComplianceSummaryResponseTypeDef,
    GetCustomRulePolicyResponseTypeDef,
    GetDiscoveredResourceCountsResponseTypeDef,
    GetOrganizationConfigRuleDetailedStatusResponseTypeDef,
    GetOrganizationConformancePackDetailedStatusResponseTypeDef,
    GetOrganizationCustomRulePolicyResponseTypeDef,
    GetResourceConfigHistoryResponseTypeDef,
    GetStoredQueryResponseTypeDef,
    ListAggregateDiscoveredResourcesResponseTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListStoredQueriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OrganizationAggregationSourceTypeDef,
    OrganizationCustomPolicyRuleMetadataTypeDef,
    OrganizationCustomRuleMetadataTypeDef,
    OrganizationManagedRuleMetadataTypeDef,
    OrganizationResourceDetailedStatusFiltersTypeDef,
    PutAggregationAuthorizationResponseTypeDef,
    PutConfigurationAggregatorResponseTypeDef,
    PutConformancePackResponseTypeDef,
    PutEvaluationsResponseTypeDef,
    PutOrganizationConfigRuleResponseTypeDef,
    PutOrganizationConformancePackResponseTypeDef,
    PutRemediationConfigurationsResponseTypeDef,
    PutRemediationExceptionsResponseTypeDef,
    PutRetentionConfigurationResponseTypeDef,
    PutStoredQueryResponseTypeDef,
    RemediationConfigurationTypeDef,
    RemediationExceptionResourceKeyTypeDef,
    ResourceCountFiltersTypeDef,
    ResourceFiltersTypeDef,
    ResourceKeyTypeDef,
    SelectAggregateResourceConfigResponseTypeDef,
    SelectResourceConfigResponseTypeDef,
    StartRemediationExecutionResponseTypeDef,
    StatusDetailFiltersTypeDef,
    StoredQueryTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ConfigServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConformancePackTemplateValidationException: Type[BotocoreClientError]
    InsufficientDeliveryPolicyException: Type[BotocoreClientError]
    InsufficientPermissionsException: Type[BotocoreClientError]
    InvalidConfigurationRecorderNameException: Type[BotocoreClientError]
    InvalidDeliveryChannelNameException: Type[BotocoreClientError]
    InvalidExpressionException: Type[BotocoreClientError]
    InvalidLimitException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRecordingGroupException: Type[BotocoreClientError]
    InvalidResultTokenException: Type[BotocoreClientError]
    InvalidRoleException: Type[BotocoreClientError]
    InvalidS3KeyPrefixException: Type[BotocoreClientError]
    InvalidS3KmsKeyArnException: Type[BotocoreClientError]
    InvalidSNSTopicARNException: Type[BotocoreClientError]
    InvalidTimeRangeException: Type[BotocoreClientError]
    LastDeliveryChannelDeleteFailedException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MaxActiveResourcesExceededException: Type[BotocoreClientError]
    MaxNumberOfConfigRulesExceededException: Type[BotocoreClientError]
    MaxNumberOfConfigurationRecordersExceededException: Type[BotocoreClientError]
    MaxNumberOfConformancePacksExceededException: Type[BotocoreClientError]
    MaxNumberOfDeliveryChannelsExceededException: Type[BotocoreClientError]
    MaxNumberOfOrganizationConfigRulesExceededException: Type[BotocoreClientError]
    MaxNumberOfOrganizationConformancePacksExceededException: Type[BotocoreClientError]
    MaxNumberOfRetentionConfigurationsExceededException: Type[BotocoreClientError]
    NoAvailableConfigurationRecorderException: Type[BotocoreClientError]
    NoAvailableDeliveryChannelException: Type[BotocoreClientError]
    NoAvailableOrganizationException: Type[BotocoreClientError]
    NoRunningConfigurationRecorderException: Type[BotocoreClientError]
    NoSuchBucketException: Type[BotocoreClientError]
    NoSuchConfigRuleException: Type[BotocoreClientError]
    NoSuchConfigRuleInConformancePackException: Type[BotocoreClientError]
    NoSuchConfigurationAggregatorException: Type[BotocoreClientError]
    NoSuchConfigurationRecorderException: Type[BotocoreClientError]
    NoSuchConformancePackException: Type[BotocoreClientError]
    NoSuchDeliveryChannelException: Type[BotocoreClientError]
    NoSuchOrganizationConfigRuleException: Type[BotocoreClientError]
    NoSuchOrganizationConformancePackException: Type[BotocoreClientError]
    NoSuchRemediationConfigurationException: Type[BotocoreClientError]
    NoSuchRemediationExceptionException: Type[BotocoreClientError]
    NoSuchRetentionConfigurationException: Type[BotocoreClientError]
    OrganizationAccessDeniedException: Type[BotocoreClientError]
    OrganizationAllFeaturesNotEnabledException: Type[BotocoreClientError]
    OrganizationConformancePackTemplateValidationException: Type[BotocoreClientError]
    OversizedConfigurationItemException: Type[BotocoreClientError]
    RemediationInProgressException: Type[BotocoreClientError]
    ResourceConcurrentModificationException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotDiscoveredException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConfigServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConfigServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#exceptions)
        """

    def batch_get_aggregate_resource_config(
        self,
        *,
        ConfigurationAggregatorName: str,
        ResourceIdentifiers: Sequence[AggregateResourceIdentifierTypeDef]
    ) -> BatchGetAggregateResourceConfigResponseTypeDef:
        """
        Returns the current configuration items for resources that are present in your
        Config aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.batch_get_aggregate_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#batch_get_aggregate_resource_config)
        """

    def batch_get_resource_config(
        self, *, resourceKeys: Sequence[ResourceKeyTypeDef]
    ) -> BatchGetResourceConfigResponseTypeDef:
        """
        Returns the `BaseConfigurationItem` for one or more requested resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.batch_get_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#batch_get_resource_config)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#can_paginate)
        """

    def delete_aggregation_authorization(
        self, *, AuthorizedAccountId: str, AuthorizedAwsRegion: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the authorization granted to the specified configuration aggregator
        account in a specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_aggregation_authorization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_aggregation_authorization)
        """

    def delete_config_rule(self, *, ConfigRuleName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Config rule and all of its evaluation results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_config_rule)
        """

    def delete_configuration_aggregator(
        self, *, ConfigurationAggregatorName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configuration aggregator and the aggregated data
        associated with the aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_configuration_aggregator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_configuration_aggregator)
        """

    def delete_configuration_recorder(
        self, *, ConfigurationRecorderName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_configuration_recorder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_configuration_recorder)
        """

    def delete_conformance_pack(self, *, ConformancePackName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified conformance pack and all the Config rules, remediation
        actions, and all evaluation results within that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_conformance_pack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_conformance_pack)
        """

    def delete_delivery_channel(self, *, DeliveryChannelName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_delivery_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_delivery_channel)
        """

    def delete_evaluation_results(self, *, ConfigRuleName: str) -> Dict[str, Any]:
        """
        Deletes the evaluation results for the specified Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_evaluation_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_evaluation_results)
        """

    def delete_organization_config_rule(
        self, *, OrganizationConfigRuleName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified organization Config rule and all of its evaluation results
        from all member accounts in that organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_organization_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_organization_config_rule)
        """

    def delete_organization_conformance_pack(
        self, *, OrganizationConformancePackName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified organization conformance pack and all of the Config rules
        and remediation actions from all member accounts in that organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_organization_conformance_pack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_organization_conformance_pack)
        """

    def delete_pending_aggregation_request(
        self, *, RequesterAccountId: str, RequesterAwsRegion: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes pending authorization requests for a specified aggregator account in a
        specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_pending_aggregation_request)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_pending_aggregation_request)
        """

    def delete_remediation_configuration(
        self, *, ConfigRuleName: str, ResourceType: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes the remediation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_remediation_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_remediation_configuration)
        """

    def delete_remediation_exceptions(
        self, *, ConfigRuleName: str, ResourceKeys: Sequence[RemediationExceptionResourceKeyTypeDef]
    ) -> DeleteRemediationExceptionsResponseTypeDef:
        """
        Deletes one or more remediation exceptions mentioned in the resource keys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_remediation_exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_remediation_exceptions)
        """

    def delete_resource_config(
        self, *, ResourceType: str, ResourceId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records the configuration state for a custom resource that has been deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_resource_config)
        """

    def delete_retention_configuration(
        self, *, RetentionConfigurationName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the retention configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_retention_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_retention_configuration)
        """

    def delete_stored_query(self, *, QueryName: str) -> Dict[str, Any]:
        """
        Deletes the stored query for a single Amazon Web Services account and a single
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.delete_stored_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_stored_query)
        """

    def deliver_config_snapshot(
        self, *, deliveryChannelName: str
    ) -> DeliverConfigSnapshotResponseTypeDef:
        """
        Schedules delivery of a configuration snapshot to the Amazon S3 bucket in the
        specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.deliver_config_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#deliver_config_snapshot)
        """

    def describe_aggregate_compliance_by_config_rules(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: ConfigRuleComplianceFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeAggregateComplianceByConfigRulesResponseTypeDef:
        """
        Returns a list of compliant and noncompliant rules with the number of resources
        for compliant and noncompliant rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_aggregate_compliance_by_config_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregate_compliance_by_config_rules)
        """

    def describe_aggregate_compliance_by_conformance_packs(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: AggregateConformancePackComplianceFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeAggregateComplianceByConformancePacksResponseTypeDef:
        """
        Returns a list of the conformance packs and their associated compliance status
        with the count of compliant and noncompliant Config rules within each
        conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_aggregate_compliance_by_conformance_packs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregate_compliance_by_conformance_packs)
        """

    def describe_aggregation_authorizations(
        self, *, Limit: int = ..., NextToken: str = ...
    ) -> DescribeAggregationAuthorizationsResponseTypeDef:
        """
        Returns a list of authorizations granted to various aggregator accounts and
        regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_aggregation_authorizations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregation_authorizations)
        """

    def describe_compliance_by_config_rule(
        self,
        *,
        ConfigRuleNames: Sequence[str] = ...,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        NextToken: str = ...
    ) -> DescribeComplianceByConfigRuleResponseTypeDef:
        """
        Indicates whether the specified Config rules are compliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_compliance_by_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_compliance_by_config_rule)
        """

    def describe_compliance_by_resource(
        self,
        *,
        ResourceType: str = ...,
        ResourceId: str = ...,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeComplianceByResourceResponseTypeDef:
        """
        Indicates whether the specified Amazon Web Services resources are compliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_compliance_by_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_compliance_by_resource)
        """

    def describe_config_rule_evaluation_status(
        self, *, ConfigRuleNames: Sequence[str] = ..., NextToken: str = ..., Limit: int = ...
    ) -> DescribeConfigRuleEvaluationStatusResponseTypeDef:
        """
        Returns status information for each of your Config managed rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_config_rule_evaluation_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_config_rule_evaluation_status)
        """

    def describe_config_rules(
        self, *, ConfigRuleNames: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeConfigRulesResponseTypeDef:
        """
        Returns details about your Config rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_config_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_config_rules)
        """

    def describe_configuration_aggregator_sources_status(
        self,
        *,
        ConfigurationAggregatorName: str,
        UpdateStatus: Sequence[AggregatedSourceStatusTypeType] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeConfigurationAggregatorSourcesStatusResponseTypeDef:
        """
        Returns status information for sources within an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_aggregator_sources_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_aggregator_sources_status)
        """

    def describe_configuration_aggregators(
        self,
        *,
        ConfigurationAggregatorNames: Sequence[str] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeConfigurationAggregatorsResponseTypeDef:
        """
        Returns the details of one or more configuration aggregators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_aggregators)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_aggregators)
        """

    def describe_configuration_recorder_status(
        self, *, ConfigurationRecorderNames: Sequence[str] = ...
    ) -> DescribeConfigurationRecorderStatusResponseTypeDef:
        """
        Returns the current status of the specified configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_recorder_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_recorder_status)
        """

    def describe_configuration_recorders(
        self, *, ConfigurationRecorderNames: Sequence[str] = ...
    ) -> DescribeConfigurationRecordersResponseTypeDef:
        """
        Returns the details for the specified configuration recorders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_recorders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_recorders)
        """

    def describe_conformance_pack_compliance(
        self,
        *,
        ConformancePackName: str,
        Filters: ConformancePackComplianceFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeConformancePackComplianceResponseTypeDef:
        """
        Returns compliance details for each rule in that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_conformance_pack_compliance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_pack_compliance)
        """

    def describe_conformance_pack_status(
        self, *, ConformancePackNames: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeConformancePackStatusResponseTypeDef:
        """
        Provides one or more conformance packs deployment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_conformance_pack_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_pack_status)
        """

    def describe_conformance_packs(
        self, *, ConformancePackNames: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeConformancePacksResponseTypeDef:
        """
        Returns a list of one or more conformance packs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_conformance_packs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_packs)
        """

    def describe_delivery_channel_status(
        self, *, DeliveryChannelNames: Sequence[str] = ...
    ) -> DescribeDeliveryChannelStatusResponseTypeDef:
        """
        Returns the current status of the specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_delivery_channel_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_delivery_channel_status)
        """

    def describe_delivery_channels(
        self, *, DeliveryChannelNames: Sequence[str] = ...
    ) -> DescribeDeliveryChannelsResponseTypeDef:
        """
        Returns details about the specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_delivery_channels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_delivery_channels)
        """

    def describe_organization_config_rule_statuses(
        self,
        *,
        OrganizationConfigRuleNames: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeOrganizationConfigRuleStatusesResponseTypeDef:
        """
        Provides organization Config rule deployment status for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_organization_config_rule_statuses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_config_rule_statuses)
        """

    def describe_organization_config_rules(
        self,
        *,
        OrganizationConfigRuleNames: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeOrganizationConfigRulesResponseTypeDef:
        """
        Returns a list of organization Config rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_organization_config_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_config_rules)
        """

    def describe_organization_conformance_pack_statuses(
        self,
        *,
        OrganizationConformancePackNames: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeOrganizationConformancePackStatusesResponseTypeDef:
        """
        Provides organization conformance pack deployment status for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_organization_conformance_pack_statuses)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_conformance_pack_statuses)
        """

    def describe_organization_conformance_packs(
        self,
        *,
        OrganizationConformancePackNames: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeOrganizationConformancePacksResponseTypeDef:
        """
        Returns a list of organization conformance packs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_organization_conformance_packs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_conformance_packs)
        """

    def describe_pending_aggregation_requests(
        self, *, Limit: int = ..., NextToken: str = ...
    ) -> DescribePendingAggregationRequestsResponseTypeDef:
        """
        Returns a list of all pending aggregation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_pending_aggregation_requests)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_pending_aggregation_requests)
        """

    def describe_remediation_configurations(
        self, *, ConfigRuleNames: Sequence[str]
    ) -> DescribeRemediationConfigurationsResponseTypeDef:
        """
        Returns the details of one or more remediation configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_remediation_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_configurations)
        """

    def describe_remediation_exceptions(
        self,
        *,
        ConfigRuleName: str,
        ResourceKeys: Sequence[RemediationExceptionResourceKeyTypeDef] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeRemediationExceptionsResponseTypeDef:
        """
        Returns the details of one or more remediation exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_remediation_exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_exceptions)
        """

    def describe_remediation_execution_status(
        self,
        *,
        ConfigRuleName: str,
        ResourceKeys: Sequence[ResourceKeyTypeDef] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeRemediationExecutionStatusResponseTypeDef:
        """
        Provides a detailed view of a Remediation Execution for a set of resources
        including state, timestamps for when steps for the remediation execution occur,
        and any error messages for steps that have failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_remediation_execution_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_execution_status)
        """

    def describe_retention_configurations(
        self, *, RetentionConfigurationNames: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeRetentionConfigurationsResponseTypeDef:
        """
        Returns the details of one or more retention configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_retention_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_retention_configurations)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#generate_presigned_url)
        """

    def get_aggregate_compliance_details_by_config_rule(
        self,
        *,
        ConfigurationAggregatorName: str,
        ConfigRuleName: str,
        AccountId: str,
        AwsRegion: str,
        ComplianceType: ComplianceTypeType = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetAggregateComplianceDetailsByConfigRuleResponseTypeDef:
        """
        Returns the evaluation results for the specified Config rule for a specific
        resource in a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_aggregate_compliance_details_by_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_compliance_details_by_config_rule)
        """

    def get_aggregate_config_rule_compliance_summary(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: ConfigRuleComplianceSummaryFiltersTypeDef = ...,
        GroupByKey: ConfigRuleComplianceSummaryGroupKeyType = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetAggregateConfigRuleComplianceSummaryResponseTypeDef:
        """
        Returns the number of compliant and noncompliant rules for one or more accounts
        and regions in an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_aggregate_config_rule_compliance_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_config_rule_compliance_summary)
        """

    def get_aggregate_conformance_pack_compliance_summary(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: AggregateConformancePackComplianceSummaryFiltersTypeDef = ...,
        GroupByKey: AggregateConformancePackComplianceSummaryGroupKeyType = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetAggregateConformancePackComplianceSummaryResponseTypeDef:
        """
        Returns the count of compliant and noncompliant conformance packs across all
        Amazon Web Services accounts and Amazon Web Services Regions in an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_aggregate_conformance_pack_compliance_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_conformance_pack_compliance_summary)
        """

    def get_aggregate_discovered_resource_counts(
        self,
        *,
        ConfigurationAggregatorName: str,
        Filters: ResourceCountFiltersTypeDef = ...,
        GroupByKey: ResourceCountGroupKeyType = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetAggregateDiscoveredResourceCountsResponseTypeDef:
        """
        Returns the resource counts across accounts and regions that are present in your
        Config aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_aggregate_discovered_resource_counts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_discovered_resource_counts)
        """

    def get_aggregate_resource_config(
        self,
        *,
        ConfigurationAggregatorName: str,
        ResourceIdentifier: AggregateResourceIdentifierTypeDef
    ) -> GetAggregateResourceConfigResponseTypeDef:
        """
        Returns configuration item that is aggregated for your specific resource in a
        specific source account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_aggregate_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_resource_config)
        """

    def get_compliance_details_by_config_rule(
        self,
        *,
        ConfigRuleName: str,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetComplianceDetailsByConfigRuleResponseTypeDef:
        """
        Returns the evaluation results for the specified Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_compliance_details_by_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_details_by_config_rule)
        """

    def get_compliance_details_by_resource(
        self,
        *,
        ResourceType: str,
        ResourceId: str,
        ComplianceTypes: Sequence[ComplianceTypeType] = ...,
        NextToken: str = ...
    ) -> GetComplianceDetailsByResourceResponseTypeDef:
        """
        Returns the evaluation results for the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_compliance_details_by_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_details_by_resource)
        """

    def get_compliance_summary_by_config_rule(
        self,
    ) -> GetComplianceSummaryByConfigRuleResponseTypeDef:
        """
        Returns the number of Config rules that are compliant and noncompliant, up to a
        maximum of 25 for each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_compliance_summary_by_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_summary_by_config_rule)
        """

    def get_compliance_summary_by_resource_type(
        self, *, ResourceTypes: Sequence[str] = ...
    ) -> GetComplianceSummaryByResourceTypeResponseTypeDef:
        """
        Returns the number of resources that are compliant and the number that are
        noncompliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_compliance_summary_by_resource_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_summary_by_resource_type)
        """

    def get_conformance_pack_compliance_details(
        self,
        *,
        ConformancePackName: str,
        Filters: ConformancePackEvaluationFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetConformancePackComplianceDetailsResponseTypeDef:
        """
        Returns compliance details of a conformance pack for all Amazon Web Services
        resources that are monitered by conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_conformance_pack_compliance_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_conformance_pack_compliance_details)
        """

    def get_conformance_pack_compliance_summary(
        self, *, ConformancePackNames: Sequence[str], Limit: int = ..., NextToken: str = ...
    ) -> GetConformancePackComplianceSummaryResponseTypeDef:
        """
        Returns compliance details for the conformance pack based on the cumulative
        compliance results of all the rules in that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_conformance_pack_compliance_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_conformance_pack_compliance_summary)
        """

    def get_custom_rule_policy(
        self, *, ConfigRuleName: str = ...
    ) -> GetCustomRulePolicyResponseTypeDef:
        """
        Returns the policy definition containing the logic for your Config Custom Policy
        rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_custom_rule_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_custom_rule_policy)
        """

    def get_discovered_resource_counts(
        self, *, resourceTypes: Sequence[str] = ..., limit: int = ..., nextToken: str = ...
    ) -> GetDiscoveredResourceCountsResponseTypeDef:
        """
        Returns the resource types, the number of each resource type, and the total
        number of resources that Config is recording in this region for your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_discovered_resource_counts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_discovered_resource_counts)
        """

    def get_organization_config_rule_detailed_status(
        self,
        *,
        OrganizationConfigRuleName: str,
        Filters: StatusDetailFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetOrganizationConfigRuleDetailedStatusResponseTypeDef:
        """
        Returns detailed status for each member account within an organization for a
        given organization Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_organization_config_rule_detailed_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_config_rule_detailed_status)
        """

    def get_organization_conformance_pack_detailed_status(
        self,
        *,
        OrganizationConformancePackName: str,
        Filters: OrganizationResourceDetailedStatusFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> GetOrganizationConformancePackDetailedStatusResponseTypeDef:
        """
        Returns detailed status for each member account within an organization for a
        given organization conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_organization_conformance_pack_detailed_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_conformance_pack_detailed_status)
        """

    def get_organization_custom_rule_policy(
        self, *, OrganizationConfigRuleName: str
    ) -> GetOrganizationCustomRulePolicyResponseTypeDef:
        """
        Returns the policy definition containing the logic for your organization Config
        Custom Policy rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_organization_custom_rule_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_custom_rule_policy)
        """

    def get_resource_config_history(
        self,
        *,
        resourceType: ResourceTypeType,
        resourceId: str,
        laterTime: Union[datetime, str] = ...,
        earlierTime: Union[datetime, str] = ...,
        chronologicalOrder: ChronologicalOrderType = ...,
        limit: int = ...,
        nextToken: str = ...
    ) -> GetResourceConfigHistoryResponseTypeDef:
        """
        Returns a list of `ConfigurationItems` for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_resource_config_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_resource_config_history)
        """

    def get_stored_query(self, *, QueryName: str) -> GetStoredQueryResponseTypeDef:
        """
        Returns the details of a specific stored query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_stored_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_stored_query)
        """

    def list_aggregate_discovered_resources(
        self,
        *,
        ConfigurationAggregatorName: str,
        ResourceType: ResourceTypeType,
        Filters: ResourceFiltersTypeDef = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> ListAggregateDiscoveredResourcesResponseTypeDef:
        """
        Accepts a resource type and returns a list of resource identifiers that are
        aggregated for a specific resource type across accounts and regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.list_aggregate_discovered_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_aggregate_discovered_resources)
        """

    def list_discovered_resources(
        self,
        *,
        resourceType: ResourceTypeType,
        resourceIds: Sequence[str] = ...,
        resourceName: str = ...,
        limit: int = ...,
        includeDeletedResources: bool = ...,
        nextToken: str = ...
    ) -> ListDiscoveredResourcesResponseTypeDef:
        """
        Accepts a resource type and returns a list of resource identifiers for the
        resources of that type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.list_discovered_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_discovered_resources)
        """

    def list_stored_queries(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListStoredQueriesResponseTypeDef:
        """
        Lists the stored queries for a single Amazon Web Services account and a single
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.list_stored_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_stored_queries)
        """

    def list_tags_for_resource(
        self, *, ResourceArn: str, Limit: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for Config resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_tags_for_resource)
        """

    def put_aggregation_authorization(
        self,
        *,
        AuthorizedAccountId: str,
        AuthorizedAwsRegion: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> PutAggregationAuthorizationResponseTypeDef:
        """
        Authorizes the aggregator account and region to collect data from the source
        account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_aggregation_authorization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_aggregation_authorization)
        """

    def put_config_rule(
        self, *, ConfigRule: ConfigRuleTypeDef, Tags: Sequence[TagTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an Config rule for evaluating whether your Amazon Web Services
        resources comply with your desired configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_config_rule)
        """

    def put_configuration_aggregator(
        self,
        *,
        ConfigurationAggregatorName: str,
        AccountAggregationSources: Sequence[AccountAggregationSourceTypeDef] = ...,
        OrganizationAggregationSource: OrganizationAggregationSourceTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> PutConfigurationAggregatorResponseTypeDef:
        """
        Creates and updates the configuration aggregator with the selected source
        accounts and regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_configuration_aggregator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_configuration_aggregator)
        """

    def put_configuration_recorder(
        self, *, ConfigurationRecorder: ConfigurationRecorderTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new configuration recorder to record the selected resource
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_configuration_recorder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_configuration_recorder)
        """

    def put_conformance_pack(
        self,
        *,
        ConformancePackName: str,
        TemplateS3Uri: str = ...,
        TemplateBody: str = ...,
        DeliveryS3Bucket: str = ...,
        DeliveryS3KeyPrefix: str = ...,
        ConformancePackInputParameters: Sequence[ConformancePackInputParameterTypeDef] = ...
    ) -> PutConformancePackResponseTypeDef:
        """
        Creates or updates a conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_conformance_pack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_conformance_pack)
        """

    def put_delivery_channel(
        self, *, DeliveryChannel: DeliveryChannelTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a delivery channel object to deliver configuration information to an
        Amazon S3 bucket and Amazon SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_delivery_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_delivery_channel)
        """

    def put_evaluations(
        self,
        *,
        ResultToken: str,
        Evaluations: Sequence[EvaluationTypeDef] = ...,
        TestMode: bool = ...
    ) -> PutEvaluationsResponseTypeDef:
        """
        Used by an Lambda function to deliver evaluation results to Config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_evaluations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_evaluations)
        """

    def put_external_evaluation(
        self, *, ConfigRuleName: str, ExternalEvaluation: ExternalEvaluationTypeDef
    ) -> Dict[str, Any]:
        """
        Add or updates the evaluations for process checks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_external_evaluation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_external_evaluation)
        """

    def put_organization_config_rule(
        self,
        *,
        OrganizationConfigRuleName: str,
        OrganizationManagedRuleMetadata: OrganizationManagedRuleMetadataTypeDef = ...,
        OrganizationCustomRuleMetadata: OrganizationCustomRuleMetadataTypeDef = ...,
        ExcludedAccounts: Sequence[str] = ...,
        OrganizationCustomPolicyRuleMetadata: OrganizationCustomPolicyRuleMetadataTypeDef = ...
    ) -> PutOrganizationConfigRuleResponseTypeDef:
        """
        Adds or updates organization Config rule for your entire organization evaluating
        whether your Amazon Web Services resources comply with your desired
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_organization_config_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_organization_config_rule)
        """

    def put_organization_conformance_pack(
        self,
        *,
        OrganizationConformancePackName: str,
        TemplateS3Uri: str = ...,
        TemplateBody: str = ...,
        DeliveryS3Bucket: str = ...,
        DeliveryS3KeyPrefix: str = ...,
        ConformancePackInputParameters: Sequence[ConformancePackInputParameterTypeDef] = ...,
        ExcludedAccounts: Sequence[str] = ...
    ) -> PutOrganizationConformancePackResponseTypeDef:
        """
        Deploys conformance packs across member accounts in an Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_organization_conformance_pack)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_organization_conformance_pack)
        """

    def put_remediation_configurations(
        self, *, RemediationConfigurations: Sequence[RemediationConfigurationTypeDef]
    ) -> PutRemediationConfigurationsResponseTypeDef:
        """
        Adds or updates the remediation configuration with a specific Config rule with
        the selected target or action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_remediation_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_remediation_configurations)
        """

    def put_remediation_exceptions(
        self,
        *,
        ConfigRuleName: str,
        ResourceKeys: Sequence[RemediationExceptionResourceKeyTypeDef],
        Message: str = ...,
        ExpirationTime: Union[datetime, str] = ...
    ) -> PutRemediationExceptionsResponseTypeDef:
        """
        A remediation exception is when a specific resource is no longer considered for
        auto-remediation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_remediation_exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_remediation_exceptions)
        """

    def put_resource_config(
        self,
        *,
        ResourceType: str,
        SchemaVersionId: str,
        ResourceId: str,
        Configuration: str,
        ResourceName: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records the configuration state for the resource provided in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_resource_config)
        """

    def put_retention_configuration(
        self, *, RetentionPeriodInDays: int
    ) -> PutRetentionConfigurationResponseTypeDef:
        """
        Creates and updates the retention configuration with details about retention
        period (number of days) that Config stores your historical information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_retention_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_retention_configuration)
        """

    def put_stored_query(
        self, *, StoredQuery: StoredQueryTypeDef, Tags: Sequence[TagTypeDef] = ...
    ) -> PutStoredQueryResponseTypeDef:
        """
        Saves a new query or updates an existing saved query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_stored_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_stored_query)
        """

    def select_aggregate_resource_config(
        self,
        *,
        Expression: str,
        ConfigurationAggregatorName: str,
        Limit: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SelectAggregateResourceConfigResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.select_aggregate_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#select_aggregate_resource_config)
        """

    def select_resource_config(
        self, *, Expression: str, Limit: int = ..., NextToken: str = ...
    ) -> SelectResourceConfigResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.select_resource_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#select_resource_config)
        """

    def start_config_rules_evaluation(
        self, *, ConfigRuleNames: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Runs an on-demand evaluation for the specified Config rules against the last
        known configuration state of the resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.start_config_rules_evaluation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_config_rules_evaluation)
        """

    def start_configuration_recorder(
        self, *, ConfigurationRecorderName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts recording configurations of the Amazon Web Services resources you have
        selected to record in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.start_configuration_recorder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_configuration_recorder)
        """

    def start_remediation_execution(
        self, *, ConfigRuleName: str, ResourceKeys: Sequence[ResourceKeyTypeDef]
    ) -> StartRemediationExecutionResponseTypeDef:
        """
        Runs an on-demand remediation for the specified Config rules against the last
        known remediation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.start_remediation_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_remediation_execution)
        """

    def stop_configuration_recorder(
        self, *, ConfigurationRecorderName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops recording configurations of the Amazon Web Services resources you have
        selected to record in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.stop_configuration_recorder)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#stop_configuration_recorder)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to a resource with the specified resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregate_compliance_by_config_rules"]
    ) -> DescribeAggregateComplianceByConfigRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregate_compliance_by_conformance_packs"]
    ) -> DescribeAggregateComplianceByConformancePacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregation_authorizations"]
    ) -> DescribeAggregationAuthorizationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compliance_by_config_rule"]
    ) -> DescribeComplianceByConfigRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compliance_by_resource"]
    ) -> DescribeComplianceByResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_config_rule_evaluation_status"]
    ) -> DescribeConfigRuleEvaluationStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_config_rules"]
    ) -> DescribeConfigRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_aggregator_sources_status"]
    ) -> DescribeConfigurationAggregatorSourcesStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_aggregators"]
    ) -> DescribeConfigurationAggregatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_conformance_pack_status"]
    ) -> DescribeConformancePackStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_conformance_packs"]
    ) -> DescribeConformancePacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_config_rule_statuses"]
    ) -> DescribeOrganizationConfigRuleStatusesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_config_rules"]
    ) -> DescribeOrganizationConfigRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_conformance_pack_statuses"]
    ) -> DescribeOrganizationConformancePackStatusesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_conformance_packs"]
    ) -> DescribeOrganizationConformancePacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_aggregation_requests"]
    ) -> DescribePendingAggregationRequestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_remediation_execution_status"]
    ) -> DescribeRemediationExecutionStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_retention_configurations"]
    ) -> DescribeRetentionConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_aggregate_compliance_details_by_config_rule"]
    ) -> GetAggregateComplianceDetailsByConfigRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_details_by_config_rule"]
    ) -> GetComplianceDetailsByConfigRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_details_by_resource"]
    ) -> GetComplianceDetailsByResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_conformance_pack_compliance_summary"]
    ) -> GetConformancePackComplianceSummaryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_organization_config_rule_detailed_status"]
    ) -> GetOrganizationConfigRuleDetailedStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_organization_conformance_pack_detailed_status"]
    ) -> GetOrganizationConformancePackDetailedStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_config_history"]
    ) -> GetResourceConfigHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_aggregate_discovered_resources"]
    ) -> ListAggregateDiscoveredResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_discovered_resources"]
    ) -> ListDiscoveredResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["select_aggregate_resource_config"]
    ) -> SelectAggregateResourceConfigPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["select_resource_config"]
    ) -> SelectResourceConfigPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """
