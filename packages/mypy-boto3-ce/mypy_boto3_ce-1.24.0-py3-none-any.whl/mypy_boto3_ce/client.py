"""
Type annotations for ce service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ce.client import CostExplorerClient

    session = Session()
    client: CostExplorerClient = session.client("ce")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AccountScopeType,
    AnomalyFeedbackTypeType,
    AnomalySubscriptionFrequencyType,
    ContextType,
    DimensionType,
    GranularityType,
    LookbackPeriodInDaysType,
    MetricType,
    PaymentOptionType,
    SavingsPlansDataTypeType,
    SupportedSavingsPlansTypeType,
    TermInYearsType,
)
from .type_defs import (
    AnomalyDateIntervalTypeDef,
    AnomalyMonitorTypeDef,
    AnomalySubscriptionTypeDef,
    CostCategoryRuleTypeDef,
    CostCategorySplitChargeRuleTypeDef,
    CreateAnomalyMonitorResponseTypeDef,
    CreateAnomalySubscriptionResponseTypeDef,
    CreateCostCategoryDefinitionResponseTypeDef,
    DateIntervalTypeDef,
    DeleteCostCategoryDefinitionResponseTypeDef,
    DescribeCostCategoryDefinitionResponseTypeDef,
    ExpressionTypeDef,
    GetAnomaliesResponseTypeDef,
    GetAnomalyMonitorsResponseTypeDef,
    GetAnomalySubscriptionsResponseTypeDef,
    GetCostAndUsageResponseTypeDef,
    GetCostAndUsageWithResourcesResponseTypeDef,
    GetCostCategoriesResponseTypeDef,
    GetCostForecastResponseTypeDef,
    GetDimensionValuesResponseTypeDef,
    GetReservationCoverageResponseTypeDef,
    GetReservationPurchaseRecommendationResponseTypeDef,
    GetReservationUtilizationResponseTypeDef,
    GetRightsizingRecommendationResponseTypeDef,
    GetSavingsPlansCoverageResponseTypeDef,
    GetSavingsPlansPurchaseRecommendationResponseTypeDef,
    GetSavingsPlansUtilizationDetailsResponseTypeDef,
    GetSavingsPlansUtilizationResponseTypeDef,
    GetTagsResponseTypeDef,
    GetUsageForecastResponseTypeDef,
    GroupDefinitionTypeDef,
    ListCostCategoryDefinitionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvideAnomalyFeedbackResponseTypeDef,
    ResourceTagTypeDef,
    RightsizingRecommendationConfigurationTypeDef,
    ServiceSpecificationTypeDef,
    SortDefinitionTypeDef,
    SubscriberTypeDef,
    TotalImpactFilterTypeDef,
    UpdateAnomalyMonitorResponseTypeDef,
    UpdateAnomalySubscriptionResponseTypeDef,
    UpdateCostCategoryDefinitionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CostExplorerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BillExpirationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DataUnavailableException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestChangedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnknownMonitorException: Type[BotocoreClientError]
    UnknownSubscriptionException: Type[BotocoreClientError]
    UnresolvableUsageUnitException: Type[BotocoreClientError]


class CostExplorerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CostExplorerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#can_paginate)
        """

    def create_anomaly_monitor(
        self,
        *,
        AnomalyMonitor: AnomalyMonitorTypeDef,
        ResourceTags: Sequence[ResourceTagTypeDef] = ...
    ) -> CreateAnomalyMonitorResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.create_anomaly_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#create_anomaly_monitor)
        """

    def create_anomaly_subscription(
        self,
        *,
        AnomalySubscription: AnomalySubscriptionTypeDef,
        ResourceTags: Sequence[ResourceTagTypeDef] = ...
    ) -> CreateAnomalySubscriptionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.create_anomaly_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#create_anomaly_subscription)
        """

    def create_cost_category_definition(
        self,
        *,
        Name: str,
        RuleVersion: Literal["CostCategoryExpression.v1"],
        Rules: Sequence[CostCategoryRuleTypeDef],
        DefaultValue: str = ...,
        SplitChargeRules: Sequence[CostCategorySplitChargeRuleTypeDef] = ...,
        ResourceTags: Sequence[ResourceTagTypeDef] = ...
    ) -> CreateCostCategoryDefinitionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.create_cost_category_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#create_cost_category_definition)
        """

    def delete_anomaly_monitor(self, *, MonitorArn: str) -> Dict[str, Any]:
        """
        Deletes a cost anomaly monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.delete_anomaly_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#delete_anomaly_monitor)
        """

    def delete_anomaly_subscription(self, *, SubscriptionArn: str) -> Dict[str, Any]:
        """
        Deletes a cost anomaly subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.delete_anomaly_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#delete_anomaly_subscription)
        """

    def delete_cost_category_definition(
        self, *, CostCategoryArn: str
    ) -> DeleteCostCategoryDefinitionResponseTypeDef:
        """
        Deletes a Cost Category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.delete_cost_category_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#delete_cost_category_definition)
        """

    def describe_cost_category_definition(
        self, *, CostCategoryArn: str, EffectiveOn: str = ...
    ) -> DescribeCostCategoryDefinitionResponseTypeDef:
        """
        Returns the name, ARN, rules, definition, and effective dates of a Cost Category
        that's defined in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.describe_cost_category_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#describe_cost_category_definition)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#generate_presigned_url)
        """

    def get_anomalies(
        self,
        *,
        DateInterval: AnomalyDateIntervalTypeDef,
        MonitorArn: str = ...,
        Feedback: AnomalyFeedbackTypeType = ...,
        TotalImpact: TotalImpactFilterTypeDef = ...,
        NextPageToken: str = ...,
        MaxResults: int = ...
    ) -> GetAnomaliesResponseTypeDef:
        """
        Retrieves all of the cost anomalies detected on your account during the time
        period that's specified by the `DateInterval` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_anomalies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_anomalies)
        """

    def get_anomaly_monitors(
        self,
        *,
        MonitorArnList: Sequence[str] = ...,
        NextPageToken: str = ...,
        MaxResults: int = ...
    ) -> GetAnomalyMonitorsResponseTypeDef:
        """
        Retrieves the cost anomaly monitor definitions for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_anomaly_monitors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_anomaly_monitors)
        """

    def get_anomaly_subscriptions(
        self,
        *,
        SubscriptionArnList: Sequence[str] = ...,
        MonitorArn: str = ...,
        NextPageToken: str = ...,
        MaxResults: int = ...
    ) -> GetAnomalySubscriptionsResponseTypeDef:
        """
        Retrieves the cost anomaly subscription objects for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_anomaly_subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_anomaly_subscriptions)
        """

    def get_cost_and_usage(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Granularity: GranularityType,
        Metrics: Sequence[str],
        Filter: "ExpressionTypeDef" = ...,
        GroupBy: Sequence[GroupDefinitionTypeDef] = ...,
        NextPageToken: str = ...
    ) -> GetCostAndUsageResponseTypeDef:
        """
        Retrieves cost and usage metrics for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_cost_and_usage)
        """

    def get_cost_and_usage_with_resources(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Granularity: GranularityType,
        Filter: "ExpressionTypeDef",
        Metrics: Sequence[str] = ...,
        GroupBy: Sequence[GroupDefinitionTypeDef] = ...,
        NextPageToken: str = ...
    ) -> GetCostAndUsageWithResourcesResponseTypeDef:
        """
        Retrieves cost and usage metrics with resources for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage_with_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_cost_and_usage_with_resources)
        """

    def get_cost_categories(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        SearchString: str = ...,
        CostCategoryName: str = ...,
        Filter: "ExpressionTypeDef" = ...,
        SortBy: Sequence[SortDefinitionTypeDef] = ...,
        MaxResults: int = ...,
        NextPageToken: str = ...
    ) -> GetCostCategoriesResponseTypeDef:
        """
        Retrieves an array of Cost Category names and values incurred cost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_categories)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_cost_categories)
        """

    def get_cost_forecast(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Metric: MetricType,
        Granularity: GranularityType,
        Filter: "ExpressionTypeDef" = ...,
        PredictionIntervalLevel: int = ...
    ) -> GetCostForecastResponseTypeDef:
        """
        Retrieves a forecast for how much Amazon Web Services predicts that you will
        spend over the forecast time period that you select, based on your past costs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_forecast)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_cost_forecast)
        """

    def get_dimension_values(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Dimension: DimensionType,
        SearchString: str = ...,
        Context: ContextType = ...,
        Filter: "ExpressionTypeDef" = ...,
        SortBy: Sequence[SortDefinitionTypeDef] = ...,
        MaxResults: int = ...,
        NextPageToken: str = ...
    ) -> GetDimensionValuesResponseTypeDef:
        """
        Retrieves all available filter values for a specified filter over a period of
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_dimension_values)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_dimension_values)
        """

    def get_reservation_coverage(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        GroupBy: Sequence[GroupDefinitionTypeDef] = ...,
        Granularity: GranularityType = ...,
        Filter: "ExpressionTypeDef" = ...,
        Metrics: Sequence[str] = ...,
        NextPageToken: str = ...,
        SortBy: SortDefinitionTypeDef = ...,
        MaxResults: int = ...
    ) -> GetReservationCoverageResponseTypeDef:
        """
        Retrieves the reservation coverage for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_reservation_coverage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_reservation_coverage)
        """

    def get_reservation_purchase_recommendation(
        self,
        *,
        Service: str,
        AccountId: str = ...,
        Filter: "ExpressionTypeDef" = ...,
        AccountScope: AccountScopeType = ...,
        LookbackPeriodInDays: LookbackPeriodInDaysType = ...,
        TermInYears: TermInYearsType = ...,
        PaymentOption: PaymentOptionType = ...,
        ServiceSpecification: ServiceSpecificationTypeDef = ...,
        PageSize: int = ...,
        NextPageToken: str = ...
    ) -> GetReservationPurchaseRecommendationResponseTypeDef:
        """
        Gets recommendations for which reservations to purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_reservation_purchase_recommendation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_reservation_purchase_recommendation)
        """

    def get_reservation_utilization(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        GroupBy: Sequence[GroupDefinitionTypeDef] = ...,
        Granularity: GranularityType = ...,
        Filter: "ExpressionTypeDef" = ...,
        SortBy: SortDefinitionTypeDef = ...,
        NextPageToken: str = ...,
        MaxResults: int = ...
    ) -> GetReservationUtilizationResponseTypeDef:
        """
        Retrieves the reservation utilization for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_reservation_utilization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_reservation_utilization)
        """

    def get_rightsizing_recommendation(
        self,
        *,
        Service: str,
        Filter: "ExpressionTypeDef" = ...,
        Configuration: RightsizingRecommendationConfigurationTypeDef = ...,
        PageSize: int = ...,
        NextPageToken: str = ...
    ) -> GetRightsizingRecommendationResponseTypeDef:
        """
        Creates recommendations that help you save cost by identifying idle and
        underutilized Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_rightsizing_recommendation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_rightsizing_recommendation)
        """

    def get_savings_plans_coverage(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        GroupBy: Sequence[GroupDefinitionTypeDef] = ...,
        Granularity: GranularityType = ...,
        Filter: "ExpressionTypeDef" = ...,
        Metrics: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        SortBy: SortDefinitionTypeDef = ...
    ) -> GetSavingsPlansCoverageResponseTypeDef:
        """
        Retrieves the Savings Plans covered for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_savings_plans_coverage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_savings_plans_coverage)
        """

    def get_savings_plans_purchase_recommendation(
        self,
        *,
        SavingsPlansType: SupportedSavingsPlansTypeType,
        TermInYears: TermInYearsType,
        PaymentOption: PaymentOptionType,
        LookbackPeriodInDays: LookbackPeriodInDaysType,
        AccountScope: AccountScopeType = ...,
        NextPageToken: str = ...,
        PageSize: int = ...,
        Filter: "ExpressionTypeDef" = ...
    ) -> GetSavingsPlansPurchaseRecommendationResponseTypeDef:
        """
        Retrieves your request parameters, Savings Plan Recommendations Summary and
        Details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_savings_plans_purchase_recommendation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_savings_plans_purchase_recommendation)
        """

    def get_savings_plans_utilization(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Granularity: GranularityType = ...,
        Filter: "ExpressionTypeDef" = ...,
        SortBy: SortDefinitionTypeDef = ...
    ) -> GetSavingsPlansUtilizationResponseTypeDef:
        """
        Retrieves the Savings Plans utilization for your account across date ranges with
        daily or monthly granularity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_savings_plans_utilization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_savings_plans_utilization)
        """

    def get_savings_plans_utilization_details(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Filter: "ExpressionTypeDef" = ...,
        DataType: Sequence[SavingsPlansDataTypeType] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        SortBy: SortDefinitionTypeDef = ...
    ) -> GetSavingsPlansUtilizationDetailsResponseTypeDef:
        """
        Retrieves attribute data along with aggregate utilization and savings data for a
        given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_savings_plans_utilization_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_savings_plans_utilization_details)
        """

    def get_tags(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        SearchString: str = ...,
        TagKey: str = ...,
        Filter: "ExpressionTypeDef" = ...,
        SortBy: Sequence[SortDefinitionTypeDef] = ...,
        MaxResults: int = ...,
        NextPageToken: str = ...
    ) -> GetTagsResponseTypeDef:
        """
        Queries for available tag keys and tag values for a specified period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_tags)
        """

    def get_usage_forecast(
        self,
        *,
        TimePeriod: DateIntervalTypeDef,
        Metric: MetricType,
        Granularity: GranularityType,
        Filter: "ExpressionTypeDef" = ...,
        PredictionIntervalLevel: int = ...
    ) -> GetUsageForecastResponseTypeDef:
        """
        Retrieves a forecast for how much Amazon Web Services predicts that you will use
        over the forecast time period that you select, based on your past usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_usage_forecast)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#get_usage_forecast)
        """

    def list_cost_category_definitions(
        self, *, EffectiveOn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListCostCategoryDefinitionsResponseTypeDef:
        """
        Returns the name, ARN, `NumberOfRules` and effective dates of all Cost
        Categories defined in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.list_cost_category_definitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#list_cost_category_definitions)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#list_tags_for_resource)
        """

    def provide_anomaly_feedback(
        self, *, AnomalyId: str, Feedback: AnomalyFeedbackTypeType
    ) -> ProvideAnomalyFeedbackResponseTypeDef:
        """
        Modifies the feedback property of a given cost anomaly.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.provide_anomaly_feedback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#provide_anomaly_feedback)
        """

    def tag_resource(
        self, *, ResourceArn: str, ResourceTags: Sequence[ResourceTagTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, ResourceTagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#untag_resource)
        """

    def update_anomaly_monitor(
        self, *, MonitorArn: str, MonitorName: str = ...
    ) -> UpdateAnomalyMonitorResponseTypeDef:
        """
        Updates an existing cost anomaly monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.update_anomaly_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#update_anomaly_monitor)
        """

    def update_anomaly_subscription(
        self,
        *,
        SubscriptionArn: str,
        Threshold: float = ...,
        Frequency: AnomalySubscriptionFrequencyType = ...,
        MonitorArnList: Sequence[str] = ...,
        Subscribers: Sequence[SubscriberTypeDef] = ...,
        SubscriptionName: str = ...
    ) -> UpdateAnomalySubscriptionResponseTypeDef:
        """
        Updates an existing cost anomaly monitor subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.update_anomaly_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#update_anomaly_subscription)
        """

    def update_cost_category_definition(
        self,
        *,
        CostCategoryArn: str,
        RuleVersion: Literal["CostCategoryExpression.v1"],
        Rules: Sequence[CostCategoryRuleTypeDef],
        DefaultValue: str = ...,
        SplitChargeRules: Sequence[CostCategorySplitChargeRuleTypeDef] = ...
    ) -> UpdateCostCategoryDefinitionResponseTypeDef:
        """
        Updates an existing Cost Category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.update_cost_category_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/client/#update_cost_category_definition)
        """
