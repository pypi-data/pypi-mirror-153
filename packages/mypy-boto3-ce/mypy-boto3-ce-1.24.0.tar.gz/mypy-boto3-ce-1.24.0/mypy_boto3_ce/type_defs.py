"""
Type annotations for ce service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/type_defs/)

Usage::

    ```python
    from mypy_boto3_ce.type_defs import AnomalyDateIntervalTypeDef

    data: AnomalyDateIntervalTypeDef = {...}
    ```
"""
import sys
from typing import Any, Dict, List, Sequence

from .literals import (
    AccountScopeType,
    AnomalyFeedbackTypeType,
    AnomalySubscriptionFrequencyType,
    ContextType,
    CostCategoryInheritedValueDimensionNameType,
    CostCategoryRuleTypeType,
    CostCategorySplitChargeMethodType,
    CostCategoryStatusType,
    DimensionType,
    FindingReasonCodeType,
    GranularityType,
    GroupDefinitionTypeType,
    LookbackPeriodInDaysType,
    MatchOptionType,
    MetricType,
    MonitorTypeType,
    NumericOperatorType,
    OfferingClassType,
    PaymentOptionType,
    PlatformDifferenceType,
    RecommendationTargetType,
    RightsizingTypeType,
    SavingsPlansDataTypeType,
    SortOrderType,
    SubscriberStatusType,
    SubscriberTypeType,
    SupportedSavingsPlansTypeType,
    TermInYearsType,
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
    "AnomalyDateIntervalTypeDef",
    "AnomalyMonitorTypeDef",
    "AnomalyScoreTypeDef",
    "SubscriberTypeDef",
    "ImpactTypeDef",
    "RootCauseTypeDef",
    "CostCategoryInheritedValueDimensionTypeDef",
    "CostCategoryProcessingStatusTypeDef",
    "CostCategorySplitChargeRuleParameterTypeDef",
    "CostCategoryValuesTypeDef",
    "DateIntervalTypeDef",
    "CoverageCostTypeDef",
    "CoverageHoursTypeDef",
    "CoverageNormalizedUnitsTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "TagValuesTypeDef",
    "DeleteAnomalyMonitorRequestRequestTypeDef",
    "DeleteAnomalySubscriptionRequestRequestTypeDef",
    "DeleteCostCategoryDefinitionRequestRequestTypeDef",
    "DescribeCostCategoryDefinitionRequestRequestTypeDef",
    "DimensionValuesTypeDef",
    "DimensionValuesWithAttributesTypeDef",
    "DiskResourceUtilizationTypeDef",
    "EBSResourceUtilizationTypeDef",
    "EC2InstanceDetailsTypeDef",
    "EC2ResourceDetailsTypeDef",
    "NetworkResourceUtilizationTypeDef",
    "EC2SpecificationTypeDef",
    "ESInstanceDetailsTypeDef",
    "ElastiCacheInstanceDetailsTypeDef",
    "TotalImpactFilterTypeDef",
    "GetAnomalyMonitorsRequestRequestTypeDef",
    "GetAnomalySubscriptionsRequestRequestTypeDef",
    "GroupDefinitionTypeDef",
    "SortDefinitionTypeDef",
    "MetricValueTypeDef",
    "ReservationPurchaseRecommendationMetadataTypeDef",
    "ReservationAggregatesTypeDef",
    "RightsizingRecommendationConfigurationTypeDef",
    "RightsizingRecommendationMetadataTypeDef",
    "RightsizingRecommendationSummaryTypeDef",
    "GetSavingsPlansPurchaseRecommendationRequestRequestTypeDef",
    "SavingsPlansPurchaseRecommendationMetadataTypeDef",
    "RDSInstanceDetailsTypeDef",
    "RedshiftInstanceDetailsTypeDef",
    "ListCostCategoryDefinitionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ProvideAnomalyFeedbackRequestRequestTypeDef",
    "ReservationPurchaseRecommendationSummaryTypeDef",
    "TerminateRecommendationDetailTypeDef",
    "SavingsPlansAmortizedCommitmentTypeDef",
    "SavingsPlansCoverageDataTypeDef",
    "SavingsPlansDetailsTypeDef",
    "SavingsPlansPurchaseRecommendationSummaryTypeDef",
    "SavingsPlansSavingsTypeDef",
    "SavingsPlansUtilizationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAnomalyMonitorRequestRequestTypeDef",
    "AnomalySubscriptionTypeDef",
    "UpdateAnomalySubscriptionRequestRequestTypeDef",
    "AnomalyTypeDef",
    "CostCategoryRuleTypeDef",
    "CostCategoryReferenceTypeDef",
    "CostCategorySplitChargeRuleTypeDef",
    "ForecastResultTypeDef",
    "GetCostForecastRequestRequestTypeDef",
    "GetUsageForecastRequestRequestTypeDef",
    "CoverageTypeDef",
    "CreateAnomalyMonitorRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAnomalyMonitorResponseTypeDef",
    "CreateAnomalySubscriptionResponseTypeDef",
    "CreateCostCategoryDefinitionResponseTypeDef",
    "DeleteCostCategoryDefinitionResponseTypeDef",
    "GetAnomalyMonitorsResponseTypeDef",
    "GetCostCategoriesResponseTypeDef",
    "GetTagsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ProvideAnomalyFeedbackResponseTypeDef",
    "UpdateAnomalyMonitorResponseTypeDef",
    "UpdateAnomalySubscriptionResponseTypeDef",
    "UpdateCostCategoryDefinitionResponseTypeDef",
    "ExpressionTypeDef",
    "GetDimensionValuesResponseTypeDef",
    "ResourceDetailsTypeDef",
    "EC2ResourceUtilizationTypeDef",
    "ServiceSpecificationTypeDef",
    "GetAnomaliesRequestRequestTypeDef",
    "GetCostAndUsageRequestRequestTypeDef",
    "GetCostAndUsageWithResourcesRequestRequestTypeDef",
    "GetCostCategoriesRequestRequestTypeDef",
    "GetDimensionValuesRequestRequestTypeDef",
    "GetReservationCoverageRequestRequestTypeDef",
    "GetReservationUtilizationRequestRequestTypeDef",
    "GetSavingsPlansCoverageRequestRequestTypeDef",
    "GetSavingsPlansUtilizationDetailsRequestRequestTypeDef",
    "GetSavingsPlansUtilizationRequestRequestTypeDef",
    "GetTagsRequestRequestTypeDef",
    "GroupTypeDef",
    "ReservationUtilizationGroupTypeDef",
    "GetRightsizingRecommendationRequestRequestTypeDef",
    "InstanceDetailsTypeDef",
    "SavingsPlansCoverageTypeDef",
    "SavingsPlansPurchaseRecommendationDetailTypeDef",
    "SavingsPlansUtilizationAggregatesTypeDef",
    "SavingsPlansUtilizationByTimeTypeDef",
    "SavingsPlansUtilizationDetailTypeDef",
    "CreateAnomalySubscriptionRequestRequestTypeDef",
    "GetAnomalySubscriptionsResponseTypeDef",
    "GetAnomaliesResponseTypeDef",
    "ListCostCategoryDefinitionsResponseTypeDef",
    "CostCategoryTypeDef",
    "CreateCostCategoryDefinitionRequestRequestTypeDef",
    "UpdateCostCategoryDefinitionRequestRequestTypeDef",
    "GetCostForecastResponseTypeDef",
    "GetUsageForecastResponseTypeDef",
    "ReservationCoverageGroupTypeDef",
    "ResourceUtilizationTypeDef",
    "GetReservationPurchaseRecommendationRequestRequestTypeDef",
    "ResultByTimeTypeDef",
    "UtilizationByTimeTypeDef",
    "ReservationPurchaseRecommendationDetailTypeDef",
    "GetSavingsPlansCoverageResponseTypeDef",
    "SavingsPlansPurchaseRecommendationTypeDef",
    "GetSavingsPlansUtilizationResponseTypeDef",
    "GetSavingsPlansUtilizationDetailsResponseTypeDef",
    "DescribeCostCategoryDefinitionResponseTypeDef",
    "CoverageByTimeTypeDef",
    "CurrentInstanceTypeDef",
    "TargetInstanceTypeDef",
    "GetCostAndUsageResponseTypeDef",
    "GetCostAndUsageWithResourcesResponseTypeDef",
    "GetReservationUtilizationResponseTypeDef",
    "ReservationPurchaseRecommendationTypeDef",
    "GetSavingsPlansPurchaseRecommendationResponseTypeDef",
    "GetReservationCoverageResponseTypeDef",
    "ModifyRecommendationDetailTypeDef",
    "GetReservationPurchaseRecommendationResponseTypeDef",
    "RightsizingRecommendationTypeDef",
    "GetRightsizingRecommendationResponseTypeDef",
)

_RequiredAnomalyDateIntervalTypeDef = TypedDict(
    "_RequiredAnomalyDateIntervalTypeDef",
    {
        "StartDate": str,
    },
)
_OptionalAnomalyDateIntervalTypeDef = TypedDict(
    "_OptionalAnomalyDateIntervalTypeDef",
    {
        "EndDate": str,
    },
    total=False,
)


class AnomalyDateIntervalTypeDef(
    _RequiredAnomalyDateIntervalTypeDef, _OptionalAnomalyDateIntervalTypeDef
):
    pass


_RequiredAnomalyMonitorTypeDef = TypedDict(
    "_RequiredAnomalyMonitorTypeDef",
    {
        "MonitorName": str,
        "MonitorType": MonitorTypeType,
    },
)
_OptionalAnomalyMonitorTypeDef = TypedDict(
    "_OptionalAnomalyMonitorTypeDef",
    {
        "MonitorArn": str,
        "CreationDate": str,
        "LastUpdatedDate": str,
        "LastEvaluatedDate": str,
        "MonitorDimension": Literal["SERVICE"],
        "MonitorSpecification": "ExpressionTypeDef",
        "DimensionalValueCount": int,
    },
    total=False,
)


class AnomalyMonitorTypeDef(_RequiredAnomalyMonitorTypeDef, _OptionalAnomalyMonitorTypeDef):
    pass


AnomalyScoreTypeDef = TypedDict(
    "AnomalyScoreTypeDef",
    {
        "MaxScore": float,
        "CurrentScore": float,
    },
)

SubscriberTypeDef = TypedDict(
    "SubscriberTypeDef",
    {
        "Address": str,
        "Type": SubscriberTypeType,
        "Status": SubscriberStatusType,
    },
    total=False,
)

_RequiredImpactTypeDef = TypedDict(
    "_RequiredImpactTypeDef",
    {
        "MaxImpact": float,
    },
)
_OptionalImpactTypeDef = TypedDict(
    "_OptionalImpactTypeDef",
    {
        "TotalImpact": float,
    },
    total=False,
)


class ImpactTypeDef(_RequiredImpactTypeDef, _OptionalImpactTypeDef):
    pass


RootCauseTypeDef = TypedDict(
    "RootCauseTypeDef",
    {
        "Service": str,
        "Region": str,
        "LinkedAccount": str,
        "UsageType": str,
    },
    total=False,
)

CostCategoryInheritedValueDimensionTypeDef = TypedDict(
    "CostCategoryInheritedValueDimensionTypeDef",
    {
        "DimensionName": CostCategoryInheritedValueDimensionNameType,
        "DimensionKey": str,
    },
    total=False,
)

CostCategoryProcessingStatusTypeDef = TypedDict(
    "CostCategoryProcessingStatusTypeDef",
    {
        "Component": Literal["COST_EXPLORER"],
        "Status": CostCategoryStatusType,
    },
    total=False,
)

CostCategorySplitChargeRuleParameterTypeDef = TypedDict(
    "CostCategorySplitChargeRuleParameterTypeDef",
    {
        "Type": Literal["ALLOCATION_PERCENTAGES"],
        "Values": Sequence[str],
    },
)

CostCategoryValuesTypeDef = TypedDict(
    "CostCategoryValuesTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "MatchOptions": Sequence[MatchOptionType],
    },
    total=False,
)

DateIntervalTypeDef = TypedDict(
    "DateIntervalTypeDef",
    {
        "Start": str,
        "End": str,
    },
)

CoverageCostTypeDef = TypedDict(
    "CoverageCostTypeDef",
    {
        "OnDemandCost": str,
    },
    total=False,
)

CoverageHoursTypeDef = TypedDict(
    "CoverageHoursTypeDef",
    {
        "OnDemandHours": str,
        "ReservedHours": str,
        "TotalRunningHours": str,
        "CoverageHoursPercentage": str,
    },
    total=False,
)

CoverageNormalizedUnitsTypeDef = TypedDict(
    "CoverageNormalizedUnitsTypeDef",
    {
        "OnDemandNormalizedUnits": str,
        "ReservedNormalizedUnits": str,
        "TotalRunningNormalizedUnits": str,
        "CoverageNormalizedUnitsPercentage": str,
    },
    total=False,
)

ResourceTagTypeDef = TypedDict(
    "ResourceTagTypeDef",
    {
        "Key": str,
        "Value": str,
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

TagValuesTypeDef = TypedDict(
    "TagValuesTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "MatchOptions": Sequence[MatchOptionType],
    },
    total=False,
)

DeleteAnomalyMonitorRequestRequestTypeDef = TypedDict(
    "DeleteAnomalyMonitorRequestRequestTypeDef",
    {
        "MonitorArn": str,
    },
)

DeleteAnomalySubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteAnomalySubscriptionRequestRequestTypeDef",
    {
        "SubscriptionArn": str,
    },
)

DeleteCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteCostCategoryDefinitionRequestRequestTypeDef",
    {
        "CostCategoryArn": str,
    },
)

_RequiredDescribeCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeCostCategoryDefinitionRequestRequestTypeDef",
    {
        "CostCategoryArn": str,
    },
)
_OptionalDescribeCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeCostCategoryDefinitionRequestRequestTypeDef",
    {
        "EffectiveOn": str,
    },
    total=False,
)


class DescribeCostCategoryDefinitionRequestRequestTypeDef(
    _RequiredDescribeCostCategoryDefinitionRequestRequestTypeDef,
    _OptionalDescribeCostCategoryDefinitionRequestRequestTypeDef,
):
    pass


DimensionValuesTypeDef = TypedDict(
    "DimensionValuesTypeDef",
    {
        "Key": DimensionType,
        "Values": Sequence[str],
        "MatchOptions": Sequence[MatchOptionType],
    },
    total=False,
)

DimensionValuesWithAttributesTypeDef = TypedDict(
    "DimensionValuesWithAttributesTypeDef",
    {
        "Value": str,
        "Attributes": Dict[str, str],
    },
    total=False,
)

DiskResourceUtilizationTypeDef = TypedDict(
    "DiskResourceUtilizationTypeDef",
    {
        "DiskReadOpsPerSecond": str,
        "DiskWriteOpsPerSecond": str,
        "DiskReadBytesPerSecond": str,
        "DiskWriteBytesPerSecond": str,
    },
    total=False,
)

EBSResourceUtilizationTypeDef = TypedDict(
    "EBSResourceUtilizationTypeDef",
    {
        "EbsReadOpsPerSecond": str,
        "EbsWriteOpsPerSecond": str,
        "EbsReadBytesPerSecond": str,
        "EbsWriteBytesPerSecond": str,
    },
    total=False,
)

EC2InstanceDetailsTypeDef = TypedDict(
    "EC2InstanceDetailsTypeDef",
    {
        "Family": str,
        "InstanceType": str,
        "Region": str,
        "AvailabilityZone": str,
        "Platform": str,
        "Tenancy": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

EC2ResourceDetailsTypeDef = TypedDict(
    "EC2ResourceDetailsTypeDef",
    {
        "HourlyOnDemandRate": str,
        "InstanceType": str,
        "Platform": str,
        "Region": str,
        "Sku": str,
        "Memory": str,
        "NetworkPerformance": str,
        "Storage": str,
        "Vcpu": str,
    },
    total=False,
)

NetworkResourceUtilizationTypeDef = TypedDict(
    "NetworkResourceUtilizationTypeDef",
    {
        "NetworkInBytesPerSecond": str,
        "NetworkOutBytesPerSecond": str,
        "NetworkPacketsInPerSecond": str,
        "NetworkPacketsOutPerSecond": str,
    },
    total=False,
)

EC2SpecificationTypeDef = TypedDict(
    "EC2SpecificationTypeDef",
    {
        "OfferingClass": OfferingClassType,
    },
    total=False,
)

ESInstanceDetailsTypeDef = TypedDict(
    "ESInstanceDetailsTypeDef",
    {
        "InstanceClass": str,
        "InstanceSize": str,
        "Region": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

ElastiCacheInstanceDetailsTypeDef = TypedDict(
    "ElastiCacheInstanceDetailsTypeDef",
    {
        "Family": str,
        "NodeType": str,
        "Region": str,
        "ProductDescription": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

_RequiredTotalImpactFilterTypeDef = TypedDict(
    "_RequiredTotalImpactFilterTypeDef",
    {
        "NumericOperator": NumericOperatorType,
        "StartValue": float,
    },
)
_OptionalTotalImpactFilterTypeDef = TypedDict(
    "_OptionalTotalImpactFilterTypeDef",
    {
        "EndValue": float,
    },
    total=False,
)


class TotalImpactFilterTypeDef(
    _RequiredTotalImpactFilterTypeDef, _OptionalTotalImpactFilterTypeDef
):
    pass


GetAnomalyMonitorsRequestRequestTypeDef = TypedDict(
    "GetAnomalyMonitorsRequestRequestTypeDef",
    {
        "MonitorArnList": Sequence[str],
        "NextPageToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetAnomalySubscriptionsRequestRequestTypeDef = TypedDict(
    "GetAnomalySubscriptionsRequestRequestTypeDef",
    {
        "SubscriptionArnList": Sequence[str],
        "MonitorArn": str,
        "NextPageToken": str,
        "MaxResults": int,
    },
    total=False,
)

GroupDefinitionTypeDef = TypedDict(
    "GroupDefinitionTypeDef",
    {
        "Type": GroupDefinitionTypeType,
        "Key": str,
    },
    total=False,
)

_RequiredSortDefinitionTypeDef = TypedDict(
    "_RequiredSortDefinitionTypeDef",
    {
        "Key": str,
    },
)
_OptionalSortDefinitionTypeDef = TypedDict(
    "_OptionalSortDefinitionTypeDef",
    {
        "SortOrder": SortOrderType,
    },
    total=False,
)


class SortDefinitionTypeDef(_RequiredSortDefinitionTypeDef, _OptionalSortDefinitionTypeDef):
    pass


MetricValueTypeDef = TypedDict(
    "MetricValueTypeDef",
    {
        "Amount": str,
        "Unit": str,
    },
    total=False,
)

ReservationPurchaseRecommendationMetadataTypeDef = TypedDict(
    "ReservationPurchaseRecommendationMetadataTypeDef",
    {
        "RecommendationId": str,
        "GenerationTimestamp": str,
    },
    total=False,
)

ReservationAggregatesTypeDef = TypedDict(
    "ReservationAggregatesTypeDef",
    {
        "UtilizationPercentage": str,
        "UtilizationPercentageInUnits": str,
        "PurchasedHours": str,
        "PurchasedUnits": str,
        "TotalActualHours": str,
        "TotalActualUnits": str,
        "UnusedHours": str,
        "UnusedUnits": str,
        "OnDemandCostOfRIHoursUsed": str,
        "NetRISavings": str,
        "TotalPotentialRISavings": str,
        "AmortizedUpfrontFee": str,
        "AmortizedRecurringFee": str,
        "TotalAmortizedFee": str,
        "RICostForUnusedHours": str,
        "RealizedSavings": str,
        "UnrealizedSavings": str,
    },
    total=False,
)

RightsizingRecommendationConfigurationTypeDef = TypedDict(
    "RightsizingRecommendationConfigurationTypeDef",
    {
        "RecommendationTarget": RecommendationTargetType,
        "BenefitsConsidered": bool,
    },
)

RightsizingRecommendationMetadataTypeDef = TypedDict(
    "RightsizingRecommendationMetadataTypeDef",
    {
        "RecommendationId": str,
        "GenerationTimestamp": str,
        "LookbackPeriodInDays": LookbackPeriodInDaysType,
        "AdditionalMetadata": str,
    },
    total=False,
)

RightsizingRecommendationSummaryTypeDef = TypedDict(
    "RightsizingRecommendationSummaryTypeDef",
    {
        "TotalRecommendationCount": str,
        "EstimatedTotalMonthlySavingsAmount": str,
        "SavingsCurrencyCode": str,
        "SavingsPercentage": str,
    },
    total=False,
)

_RequiredGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef = TypedDict(
    "_RequiredGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef",
    {
        "SavingsPlansType": SupportedSavingsPlansTypeType,
        "TermInYears": TermInYearsType,
        "PaymentOption": PaymentOptionType,
        "LookbackPeriodInDays": LookbackPeriodInDaysType,
    },
)
_OptionalGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef = TypedDict(
    "_OptionalGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef",
    {
        "AccountScope": AccountScopeType,
        "NextPageToken": str,
        "PageSize": int,
        "Filter": "ExpressionTypeDef",
    },
    total=False,
)


class GetSavingsPlansPurchaseRecommendationRequestRequestTypeDef(
    _RequiredGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef,
    _OptionalGetSavingsPlansPurchaseRecommendationRequestRequestTypeDef,
):
    pass


SavingsPlansPurchaseRecommendationMetadataTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationMetadataTypeDef",
    {
        "RecommendationId": str,
        "GenerationTimestamp": str,
        "AdditionalMetadata": str,
    },
    total=False,
)

RDSInstanceDetailsTypeDef = TypedDict(
    "RDSInstanceDetailsTypeDef",
    {
        "Family": str,
        "InstanceType": str,
        "Region": str,
        "DatabaseEngine": str,
        "DatabaseEdition": str,
        "DeploymentOption": str,
        "LicenseModel": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

RedshiftInstanceDetailsTypeDef = TypedDict(
    "RedshiftInstanceDetailsTypeDef",
    {
        "Family": str,
        "NodeType": str,
        "Region": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

ListCostCategoryDefinitionsRequestRequestTypeDef = TypedDict(
    "ListCostCategoryDefinitionsRequestRequestTypeDef",
    {
        "EffectiveOn": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ProvideAnomalyFeedbackRequestRequestTypeDef = TypedDict(
    "ProvideAnomalyFeedbackRequestRequestTypeDef",
    {
        "AnomalyId": str,
        "Feedback": AnomalyFeedbackTypeType,
    },
)

ReservationPurchaseRecommendationSummaryTypeDef = TypedDict(
    "ReservationPurchaseRecommendationSummaryTypeDef",
    {
        "TotalEstimatedMonthlySavingsAmount": str,
        "TotalEstimatedMonthlySavingsPercentage": str,
        "CurrencyCode": str,
    },
    total=False,
)

TerminateRecommendationDetailTypeDef = TypedDict(
    "TerminateRecommendationDetailTypeDef",
    {
        "EstimatedMonthlySavings": str,
        "CurrencyCode": str,
    },
    total=False,
)

SavingsPlansAmortizedCommitmentTypeDef = TypedDict(
    "SavingsPlansAmortizedCommitmentTypeDef",
    {
        "AmortizedRecurringCommitment": str,
        "AmortizedUpfrontCommitment": str,
        "TotalAmortizedCommitment": str,
    },
    total=False,
)

SavingsPlansCoverageDataTypeDef = TypedDict(
    "SavingsPlansCoverageDataTypeDef",
    {
        "SpendCoveredBySavingsPlans": str,
        "OnDemandCost": str,
        "TotalCost": str,
        "CoveragePercentage": str,
    },
    total=False,
)

SavingsPlansDetailsTypeDef = TypedDict(
    "SavingsPlansDetailsTypeDef",
    {
        "Region": str,
        "InstanceFamily": str,
        "OfferingId": str,
    },
    total=False,
)

SavingsPlansPurchaseRecommendationSummaryTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationSummaryTypeDef",
    {
        "EstimatedROI": str,
        "CurrencyCode": str,
        "EstimatedTotalCost": str,
        "CurrentOnDemandSpend": str,
        "EstimatedSavingsAmount": str,
        "TotalRecommendationCount": str,
        "DailyCommitmentToPurchase": str,
        "HourlyCommitmentToPurchase": str,
        "EstimatedSavingsPercentage": str,
        "EstimatedMonthlySavingsAmount": str,
        "EstimatedOnDemandCostWithCurrentCommitment": str,
    },
    total=False,
)

SavingsPlansSavingsTypeDef = TypedDict(
    "SavingsPlansSavingsTypeDef",
    {
        "NetSavings": str,
        "OnDemandCostEquivalent": str,
    },
    total=False,
)

SavingsPlansUtilizationTypeDef = TypedDict(
    "SavingsPlansUtilizationTypeDef",
    {
        "TotalCommitment": str,
        "UsedCommitment": str,
        "UnusedCommitment": str,
        "UtilizationPercentage": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "ResourceTagKeys": Sequence[str],
    },
)

_RequiredUpdateAnomalyMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnomalyMonitorRequestRequestTypeDef",
    {
        "MonitorArn": str,
    },
)
_OptionalUpdateAnomalyMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnomalyMonitorRequestRequestTypeDef",
    {
        "MonitorName": str,
    },
    total=False,
)


class UpdateAnomalyMonitorRequestRequestTypeDef(
    _RequiredUpdateAnomalyMonitorRequestRequestTypeDef,
    _OptionalUpdateAnomalyMonitorRequestRequestTypeDef,
):
    pass


_RequiredAnomalySubscriptionTypeDef = TypedDict(
    "_RequiredAnomalySubscriptionTypeDef",
    {
        "MonitorArnList": Sequence[str],
        "Subscribers": Sequence[SubscriberTypeDef],
        "Threshold": float,
        "Frequency": AnomalySubscriptionFrequencyType,
        "SubscriptionName": str,
    },
)
_OptionalAnomalySubscriptionTypeDef = TypedDict(
    "_OptionalAnomalySubscriptionTypeDef",
    {
        "SubscriptionArn": str,
        "AccountId": str,
    },
    total=False,
)


class AnomalySubscriptionTypeDef(
    _RequiredAnomalySubscriptionTypeDef, _OptionalAnomalySubscriptionTypeDef
):
    pass


_RequiredUpdateAnomalySubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnomalySubscriptionRequestRequestTypeDef",
    {
        "SubscriptionArn": str,
    },
)
_OptionalUpdateAnomalySubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnomalySubscriptionRequestRequestTypeDef",
    {
        "Threshold": float,
        "Frequency": AnomalySubscriptionFrequencyType,
        "MonitorArnList": Sequence[str],
        "Subscribers": Sequence[SubscriberTypeDef],
        "SubscriptionName": str,
    },
    total=False,
)


class UpdateAnomalySubscriptionRequestRequestTypeDef(
    _RequiredUpdateAnomalySubscriptionRequestRequestTypeDef,
    _OptionalUpdateAnomalySubscriptionRequestRequestTypeDef,
):
    pass


_RequiredAnomalyTypeDef = TypedDict(
    "_RequiredAnomalyTypeDef",
    {
        "AnomalyId": str,
        "AnomalyScore": AnomalyScoreTypeDef,
        "Impact": ImpactTypeDef,
        "MonitorArn": str,
    },
)
_OptionalAnomalyTypeDef = TypedDict(
    "_OptionalAnomalyTypeDef",
    {
        "AnomalyStartDate": str,
        "AnomalyEndDate": str,
        "DimensionValue": str,
        "RootCauses": List[RootCauseTypeDef],
        "Feedback": AnomalyFeedbackTypeType,
    },
    total=False,
)


class AnomalyTypeDef(_RequiredAnomalyTypeDef, _OptionalAnomalyTypeDef):
    pass


CostCategoryRuleTypeDef = TypedDict(
    "CostCategoryRuleTypeDef",
    {
        "Value": str,
        "Rule": "ExpressionTypeDef",
        "InheritedValue": CostCategoryInheritedValueDimensionTypeDef,
        "Type": CostCategoryRuleTypeType,
    },
    total=False,
)

CostCategoryReferenceTypeDef = TypedDict(
    "CostCategoryReferenceTypeDef",
    {
        "CostCategoryArn": str,
        "Name": str,
        "EffectiveStart": str,
        "EffectiveEnd": str,
        "NumberOfRules": int,
        "ProcessingStatus": List[CostCategoryProcessingStatusTypeDef],
        "Values": List[str],
        "DefaultValue": str,
    },
    total=False,
)

_RequiredCostCategorySplitChargeRuleTypeDef = TypedDict(
    "_RequiredCostCategorySplitChargeRuleTypeDef",
    {
        "Source": str,
        "Targets": Sequence[str],
        "Method": CostCategorySplitChargeMethodType,
    },
)
_OptionalCostCategorySplitChargeRuleTypeDef = TypedDict(
    "_OptionalCostCategorySplitChargeRuleTypeDef",
    {
        "Parameters": Sequence[CostCategorySplitChargeRuleParameterTypeDef],
    },
    total=False,
)


class CostCategorySplitChargeRuleTypeDef(
    _RequiredCostCategorySplitChargeRuleTypeDef, _OptionalCostCategorySplitChargeRuleTypeDef
):
    pass


ForecastResultTypeDef = TypedDict(
    "ForecastResultTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "MeanValue": str,
        "PredictionIntervalLowerBound": str,
        "PredictionIntervalUpperBound": str,
    },
    total=False,
)

_RequiredGetCostForecastRequestRequestTypeDef = TypedDict(
    "_RequiredGetCostForecastRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Metric": MetricType,
        "Granularity": GranularityType,
    },
)
_OptionalGetCostForecastRequestRequestTypeDef = TypedDict(
    "_OptionalGetCostForecastRequestRequestTypeDef",
    {
        "Filter": "ExpressionTypeDef",
        "PredictionIntervalLevel": int,
    },
    total=False,
)


class GetCostForecastRequestRequestTypeDef(
    _RequiredGetCostForecastRequestRequestTypeDef, _OptionalGetCostForecastRequestRequestTypeDef
):
    pass


_RequiredGetUsageForecastRequestRequestTypeDef = TypedDict(
    "_RequiredGetUsageForecastRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Metric": MetricType,
        "Granularity": GranularityType,
    },
)
_OptionalGetUsageForecastRequestRequestTypeDef = TypedDict(
    "_OptionalGetUsageForecastRequestRequestTypeDef",
    {
        "Filter": "ExpressionTypeDef",
        "PredictionIntervalLevel": int,
    },
    total=False,
)


class GetUsageForecastRequestRequestTypeDef(
    _RequiredGetUsageForecastRequestRequestTypeDef, _OptionalGetUsageForecastRequestRequestTypeDef
):
    pass


CoverageTypeDef = TypedDict(
    "CoverageTypeDef",
    {
        "CoverageHours": CoverageHoursTypeDef,
        "CoverageNormalizedUnits": CoverageNormalizedUnitsTypeDef,
        "CoverageCost": CoverageCostTypeDef,
    },
    total=False,
)

_RequiredCreateAnomalyMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnomalyMonitorRequestRequestTypeDef",
    {
        "AnomalyMonitor": AnomalyMonitorTypeDef,
    },
)
_OptionalCreateAnomalyMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnomalyMonitorRequestRequestTypeDef",
    {
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)


class CreateAnomalyMonitorRequestRequestTypeDef(
    _RequiredCreateAnomalyMonitorRequestRequestTypeDef,
    _OptionalCreateAnomalyMonitorRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
)

CreateAnomalyMonitorResponseTypeDef = TypedDict(
    "CreateAnomalyMonitorResponseTypeDef",
    {
        "MonitorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAnomalySubscriptionResponseTypeDef = TypedDict(
    "CreateAnomalySubscriptionResponseTypeDef",
    {
        "SubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCostCategoryDefinitionResponseTypeDef = TypedDict(
    "CreateCostCategoryDefinitionResponseTypeDef",
    {
        "CostCategoryArn": str,
        "EffectiveStart": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCostCategoryDefinitionResponseTypeDef = TypedDict(
    "DeleteCostCategoryDefinitionResponseTypeDef",
    {
        "CostCategoryArn": str,
        "EffectiveEnd": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnomalyMonitorsResponseTypeDef = TypedDict(
    "GetAnomalyMonitorsResponseTypeDef",
    {
        "AnomalyMonitors": List[AnomalyMonitorTypeDef],
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCostCategoriesResponseTypeDef = TypedDict(
    "GetCostCategoriesResponseTypeDef",
    {
        "NextPageToken": str,
        "CostCategoryNames": List[str],
        "CostCategoryValues": List[str],
        "ReturnSize": int,
        "TotalSize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTagsResponseTypeDef = TypedDict(
    "GetTagsResponseTypeDef",
    {
        "NextPageToken": str,
        "Tags": List[str],
        "ReturnSize": int,
        "TotalSize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceTags": List[ResourceTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProvideAnomalyFeedbackResponseTypeDef = TypedDict(
    "ProvideAnomalyFeedbackResponseTypeDef",
    {
        "AnomalyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnomalyMonitorResponseTypeDef = TypedDict(
    "UpdateAnomalyMonitorResponseTypeDef",
    {
        "MonitorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnomalySubscriptionResponseTypeDef = TypedDict(
    "UpdateAnomalySubscriptionResponseTypeDef",
    {
        "SubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCostCategoryDefinitionResponseTypeDef = TypedDict(
    "UpdateCostCategoryDefinitionResponseTypeDef",
    {
        "CostCategoryArn": str,
        "EffectiveStart": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExpressionTypeDef = TypedDict(
    "ExpressionTypeDef",
    {
        "Or": Sequence[Dict[str, Any]],
        "And": Sequence[Dict[str, Any]],
        "Not": Dict[str, Any],
        "Dimensions": DimensionValuesTypeDef,
        "Tags": TagValuesTypeDef,
        "CostCategories": CostCategoryValuesTypeDef,
    },
    total=False,
)

GetDimensionValuesResponseTypeDef = TypedDict(
    "GetDimensionValuesResponseTypeDef",
    {
        "DimensionValues": List[DimensionValuesWithAttributesTypeDef],
        "ReturnSize": int,
        "TotalSize": int,
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "EC2ResourceDetails": EC2ResourceDetailsTypeDef,
    },
    total=False,
)

EC2ResourceUtilizationTypeDef = TypedDict(
    "EC2ResourceUtilizationTypeDef",
    {
        "MaxCpuUtilizationPercentage": str,
        "MaxMemoryUtilizationPercentage": str,
        "MaxStorageUtilizationPercentage": str,
        "EBSResourceUtilization": EBSResourceUtilizationTypeDef,
        "DiskResourceUtilization": DiskResourceUtilizationTypeDef,
        "NetworkResourceUtilization": NetworkResourceUtilizationTypeDef,
    },
    total=False,
)

ServiceSpecificationTypeDef = TypedDict(
    "ServiceSpecificationTypeDef",
    {
        "EC2Specification": EC2SpecificationTypeDef,
    },
    total=False,
)

_RequiredGetAnomaliesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAnomaliesRequestRequestTypeDef",
    {
        "DateInterval": AnomalyDateIntervalTypeDef,
    },
)
_OptionalGetAnomaliesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAnomaliesRequestRequestTypeDef",
    {
        "MonitorArn": str,
        "Feedback": AnomalyFeedbackTypeType,
        "TotalImpact": TotalImpactFilterTypeDef,
        "NextPageToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetAnomaliesRequestRequestTypeDef(
    _RequiredGetAnomaliesRequestRequestTypeDef, _OptionalGetAnomaliesRequestRequestTypeDef
):
    pass


_RequiredGetCostAndUsageRequestRequestTypeDef = TypedDict(
    "_RequiredGetCostAndUsageRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Granularity": GranularityType,
        "Metrics": Sequence[str],
    },
)
_OptionalGetCostAndUsageRequestRequestTypeDef = TypedDict(
    "_OptionalGetCostAndUsageRequestRequestTypeDef",
    {
        "Filter": "ExpressionTypeDef",
        "GroupBy": Sequence[GroupDefinitionTypeDef],
        "NextPageToken": str,
    },
    total=False,
)


class GetCostAndUsageRequestRequestTypeDef(
    _RequiredGetCostAndUsageRequestRequestTypeDef, _OptionalGetCostAndUsageRequestRequestTypeDef
):
    pass


_RequiredGetCostAndUsageWithResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredGetCostAndUsageWithResourcesRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Granularity": GranularityType,
        "Filter": "ExpressionTypeDef",
    },
)
_OptionalGetCostAndUsageWithResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalGetCostAndUsageWithResourcesRequestRequestTypeDef",
    {
        "Metrics": Sequence[str],
        "GroupBy": Sequence[GroupDefinitionTypeDef],
        "NextPageToken": str,
    },
    total=False,
)


class GetCostAndUsageWithResourcesRequestRequestTypeDef(
    _RequiredGetCostAndUsageWithResourcesRequestRequestTypeDef,
    _OptionalGetCostAndUsageWithResourcesRequestRequestTypeDef,
):
    pass


_RequiredGetCostCategoriesRequestRequestTypeDef = TypedDict(
    "_RequiredGetCostCategoriesRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetCostCategoriesRequestRequestTypeDef = TypedDict(
    "_OptionalGetCostCategoriesRequestRequestTypeDef",
    {
        "SearchString": str,
        "CostCategoryName": str,
        "Filter": "ExpressionTypeDef",
        "SortBy": Sequence[SortDefinitionTypeDef],
        "MaxResults": int,
        "NextPageToken": str,
    },
    total=False,
)


class GetCostCategoriesRequestRequestTypeDef(
    _RequiredGetCostCategoriesRequestRequestTypeDef, _OptionalGetCostCategoriesRequestRequestTypeDef
):
    pass


_RequiredGetDimensionValuesRequestRequestTypeDef = TypedDict(
    "_RequiredGetDimensionValuesRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Dimension": DimensionType,
    },
)
_OptionalGetDimensionValuesRequestRequestTypeDef = TypedDict(
    "_OptionalGetDimensionValuesRequestRequestTypeDef",
    {
        "SearchString": str,
        "Context": ContextType,
        "Filter": "ExpressionTypeDef",
        "SortBy": Sequence[SortDefinitionTypeDef],
        "MaxResults": int,
        "NextPageToken": str,
    },
    total=False,
)


class GetDimensionValuesRequestRequestTypeDef(
    _RequiredGetDimensionValuesRequestRequestTypeDef,
    _OptionalGetDimensionValuesRequestRequestTypeDef,
):
    pass


_RequiredGetReservationCoverageRequestRequestTypeDef = TypedDict(
    "_RequiredGetReservationCoverageRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetReservationCoverageRequestRequestTypeDef = TypedDict(
    "_OptionalGetReservationCoverageRequestRequestTypeDef",
    {
        "GroupBy": Sequence[GroupDefinitionTypeDef],
        "Granularity": GranularityType,
        "Filter": "ExpressionTypeDef",
        "Metrics": Sequence[str],
        "NextPageToken": str,
        "SortBy": SortDefinitionTypeDef,
        "MaxResults": int,
    },
    total=False,
)


class GetReservationCoverageRequestRequestTypeDef(
    _RequiredGetReservationCoverageRequestRequestTypeDef,
    _OptionalGetReservationCoverageRequestRequestTypeDef,
):
    pass


_RequiredGetReservationUtilizationRequestRequestTypeDef = TypedDict(
    "_RequiredGetReservationUtilizationRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetReservationUtilizationRequestRequestTypeDef = TypedDict(
    "_OptionalGetReservationUtilizationRequestRequestTypeDef",
    {
        "GroupBy": Sequence[GroupDefinitionTypeDef],
        "Granularity": GranularityType,
        "Filter": "ExpressionTypeDef",
        "SortBy": SortDefinitionTypeDef,
        "NextPageToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetReservationUtilizationRequestRequestTypeDef(
    _RequiredGetReservationUtilizationRequestRequestTypeDef,
    _OptionalGetReservationUtilizationRequestRequestTypeDef,
):
    pass


_RequiredGetSavingsPlansCoverageRequestRequestTypeDef = TypedDict(
    "_RequiredGetSavingsPlansCoverageRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetSavingsPlansCoverageRequestRequestTypeDef = TypedDict(
    "_OptionalGetSavingsPlansCoverageRequestRequestTypeDef",
    {
        "GroupBy": Sequence[GroupDefinitionTypeDef],
        "Granularity": GranularityType,
        "Filter": "ExpressionTypeDef",
        "Metrics": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
        "SortBy": SortDefinitionTypeDef,
    },
    total=False,
)


class GetSavingsPlansCoverageRequestRequestTypeDef(
    _RequiredGetSavingsPlansCoverageRequestRequestTypeDef,
    _OptionalGetSavingsPlansCoverageRequestRequestTypeDef,
):
    pass


_RequiredGetSavingsPlansUtilizationDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSavingsPlansUtilizationDetailsRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetSavingsPlansUtilizationDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSavingsPlansUtilizationDetailsRequestRequestTypeDef",
    {
        "Filter": "ExpressionTypeDef",
        "DataType": Sequence[SavingsPlansDataTypeType],
        "NextToken": str,
        "MaxResults": int,
        "SortBy": SortDefinitionTypeDef,
    },
    total=False,
)


class GetSavingsPlansUtilizationDetailsRequestRequestTypeDef(
    _RequiredGetSavingsPlansUtilizationDetailsRequestRequestTypeDef,
    _OptionalGetSavingsPlansUtilizationDetailsRequestRequestTypeDef,
):
    pass


_RequiredGetSavingsPlansUtilizationRequestRequestTypeDef = TypedDict(
    "_RequiredGetSavingsPlansUtilizationRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetSavingsPlansUtilizationRequestRequestTypeDef = TypedDict(
    "_OptionalGetSavingsPlansUtilizationRequestRequestTypeDef",
    {
        "Granularity": GranularityType,
        "Filter": "ExpressionTypeDef",
        "SortBy": SortDefinitionTypeDef,
    },
    total=False,
)


class GetSavingsPlansUtilizationRequestRequestTypeDef(
    _RequiredGetSavingsPlansUtilizationRequestRequestTypeDef,
    _OptionalGetSavingsPlansUtilizationRequestRequestTypeDef,
):
    pass


_RequiredGetTagsRequestRequestTypeDef = TypedDict(
    "_RequiredGetTagsRequestRequestTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetTagsRequestRequestTypeDef = TypedDict(
    "_OptionalGetTagsRequestRequestTypeDef",
    {
        "SearchString": str,
        "TagKey": str,
        "Filter": "ExpressionTypeDef",
        "SortBy": Sequence[SortDefinitionTypeDef],
        "MaxResults": int,
        "NextPageToken": str,
    },
    total=False,
)


class GetTagsRequestRequestTypeDef(
    _RequiredGetTagsRequestRequestTypeDef, _OptionalGetTagsRequestRequestTypeDef
):
    pass


GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Keys": List[str],
        "Metrics": Dict[str, MetricValueTypeDef],
    },
    total=False,
)

ReservationUtilizationGroupTypeDef = TypedDict(
    "ReservationUtilizationGroupTypeDef",
    {
        "Key": str,
        "Value": str,
        "Attributes": Dict[str, str],
        "Utilization": ReservationAggregatesTypeDef,
    },
    total=False,
)

_RequiredGetRightsizingRecommendationRequestRequestTypeDef = TypedDict(
    "_RequiredGetRightsizingRecommendationRequestRequestTypeDef",
    {
        "Service": str,
    },
)
_OptionalGetRightsizingRecommendationRequestRequestTypeDef = TypedDict(
    "_OptionalGetRightsizingRecommendationRequestRequestTypeDef",
    {
        "Filter": "ExpressionTypeDef",
        "Configuration": RightsizingRecommendationConfigurationTypeDef,
        "PageSize": int,
        "NextPageToken": str,
    },
    total=False,
)


class GetRightsizingRecommendationRequestRequestTypeDef(
    _RequiredGetRightsizingRecommendationRequestRequestTypeDef,
    _OptionalGetRightsizingRecommendationRequestRequestTypeDef,
):
    pass


InstanceDetailsTypeDef = TypedDict(
    "InstanceDetailsTypeDef",
    {
        "EC2InstanceDetails": EC2InstanceDetailsTypeDef,
        "RDSInstanceDetails": RDSInstanceDetailsTypeDef,
        "RedshiftInstanceDetails": RedshiftInstanceDetailsTypeDef,
        "ElastiCacheInstanceDetails": ElastiCacheInstanceDetailsTypeDef,
        "ESInstanceDetails": ESInstanceDetailsTypeDef,
    },
    total=False,
)

SavingsPlansCoverageTypeDef = TypedDict(
    "SavingsPlansCoverageTypeDef",
    {
        "Attributes": Dict[str, str],
        "Coverage": SavingsPlansCoverageDataTypeDef,
        "TimePeriod": DateIntervalTypeDef,
    },
    total=False,
)

SavingsPlansPurchaseRecommendationDetailTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationDetailTypeDef",
    {
        "SavingsPlansDetails": SavingsPlansDetailsTypeDef,
        "AccountId": str,
        "UpfrontCost": str,
        "EstimatedROI": str,
        "CurrencyCode": str,
        "EstimatedSPCost": str,
        "EstimatedOnDemandCost": str,
        "EstimatedOnDemandCostWithCurrentCommitment": str,
        "EstimatedSavingsAmount": str,
        "EstimatedSavingsPercentage": str,
        "HourlyCommitmentToPurchase": str,
        "EstimatedAverageUtilization": str,
        "EstimatedMonthlySavingsAmount": str,
        "CurrentMinimumHourlyOnDemandSpend": str,
        "CurrentMaximumHourlyOnDemandSpend": str,
        "CurrentAverageHourlyOnDemandSpend": str,
    },
    total=False,
)

_RequiredSavingsPlansUtilizationAggregatesTypeDef = TypedDict(
    "_RequiredSavingsPlansUtilizationAggregatesTypeDef",
    {
        "Utilization": SavingsPlansUtilizationTypeDef,
    },
)
_OptionalSavingsPlansUtilizationAggregatesTypeDef = TypedDict(
    "_OptionalSavingsPlansUtilizationAggregatesTypeDef",
    {
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)


class SavingsPlansUtilizationAggregatesTypeDef(
    _RequiredSavingsPlansUtilizationAggregatesTypeDef,
    _OptionalSavingsPlansUtilizationAggregatesTypeDef,
):
    pass


_RequiredSavingsPlansUtilizationByTimeTypeDef = TypedDict(
    "_RequiredSavingsPlansUtilizationByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Utilization": SavingsPlansUtilizationTypeDef,
    },
)
_OptionalSavingsPlansUtilizationByTimeTypeDef = TypedDict(
    "_OptionalSavingsPlansUtilizationByTimeTypeDef",
    {
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)


class SavingsPlansUtilizationByTimeTypeDef(
    _RequiredSavingsPlansUtilizationByTimeTypeDef, _OptionalSavingsPlansUtilizationByTimeTypeDef
):
    pass


SavingsPlansUtilizationDetailTypeDef = TypedDict(
    "SavingsPlansUtilizationDetailTypeDef",
    {
        "SavingsPlanArn": str,
        "Attributes": Dict[str, str],
        "Utilization": SavingsPlansUtilizationTypeDef,
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)

_RequiredCreateAnomalySubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnomalySubscriptionRequestRequestTypeDef",
    {
        "AnomalySubscription": AnomalySubscriptionTypeDef,
    },
)
_OptionalCreateAnomalySubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnomalySubscriptionRequestRequestTypeDef",
    {
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)


class CreateAnomalySubscriptionRequestRequestTypeDef(
    _RequiredCreateAnomalySubscriptionRequestRequestTypeDef,
    _OptionalCreateAnomalySubscriptionRequestRequestTypeDef,
):
    pass


GetAnomalySubscriptionsResponseTypeDef = TypedDict(
    "GetAnomalySubscriptionsResponseTypeDef",
    {
        "AnomalySubscriptions": List[AnomalySubscriptionTypeDef],
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnomaliesResponseTypeDef = TypedDict(
    "GetAnomaliesResponseTypeDef",
    {
        "Anomalies": List[AnomalyTypeDef],
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCostCategoryDefinitionsResponseTypeDef = TypedDict(
    "ListCostCategoryDefinitionsResponseTypeDef",
    {
        "CostCategoryReferences": List[CostCategoryReferenceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCostCategoryTypeDef = TypedDict(
    "_RequiredCostCategoryTypeDef",
    {
        "CostCategoryArn": str,
        "EffectiveStart": str,
        "Name": str,
        "RuleVersion": Literal["CostCategoryExpression.v1"],
        "Rules": List[CostCategoryRuleTypeDef],
    },
)
_OptionalCostCategoryTypeDef = TypedDict(
    "_OptionalCostCategoryTypeDef",
    {
        "EffectiveEnd": str,
        "SplitChargeRules": List[CostCategorySplitChargeRuleTypeDef],
        "ProcessingStatus": List[CostCategoryProcessingStatusTypeDef],
        "DefaultValue": str,
    },
    total=False,
)


class CostCategoryTypeDef(_RequiredCostCategoryTypeDef, _OptionalCostCategoryTypeDef):
    pass


_RequiredCreateCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCostCategoryDefinitionRequestRequestTypeDef",
    {
        "Name": str,
        "RuleVersion": Literal["CostCategoryExpression.v1"],
        "Rules": Sequence[CostCategoryRuleTypeDef],
    },
)
_OptionalCreateCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCostCategoryDefinitionRequestRequestTypeDef",
    {
        "DefaultValue": str,
        "SplitChargeRules": Sequence[CostCategorySplitChargeRuleTypeDef],
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)


class CreateCostCategoryDefinitionRequestRequestTypeDef(
    _RequiredCreateCostCategoryDefinitionRequestRequestTypeDef,
    _OptionalCreateCostCategoryDefinitionRequestRequestTypeDef,
):
    pass


_RequiredUpdateCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCostCategoryDefinitionRequestRequestTypeDef",
    {
        "CostCategoryArn": str,
        "RuleVersion": Literal["CostCategoryExpression.v1"],
        "Rules": Sequence[CostCategoryRuleTypeDef],
    },
)
_OptionalUpdateCostCategoryDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCostCategoryDefinitionRequestRequestTypeDef",
    {
        "DefaultValue": str,
        "SplitChargeRules": Sequence[CostCategorySplitChargeRuleTypeDef],
    },
    total=False,
)


class UpdateCostCategoryDefinitionRequestRequestTypeDef(
    _RequiredUpdateCostCategoryDefinitionRequestRequestTypeDef,
    _OptionalUpdateCostCategoryDefinitionRequestRequestTypeDef,
):
    pass


GetCostForecastResponseTypeDef = TypedDict(
    "GetCostForecastResponseTypeDef",
    {
        "Total": MetricValueTypeDef,
        "ForecastResultsByTime": List[ForecastResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUsageForecastResponseTypeDef = TypedDict(
    "GetUsageForecastResponseTypeDef",
    {
        "Total": MetricValueTypeDef,
        "ForecastResultsByTime": List[ForecastResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservationCoverageGroupTypeDef = TypedDict(
    "ReservationCoverageGroupTypeDef",
    {
        "Attributes": Dict[str, str],
        "Coverage": CoverageTypeDef,
    },
    total=False,
)

ResourceUtilizationTypeDef = TypedDict(
    "ResourceUtilizationTypeDef",
    {
        "EC2ResourceUtilization": EC2ResourceUtilizationTypeDef,
    },
    total=False,
)

_RequiredGetReservationPurchaseRecommendationRequestRequestTypeDef = TypedDict(
    "_RequiredGetReservationPurchaseRecommendationRequestRequestTypeDef",
    {
        "Service": str,
    },
)
_OptionalGetReservationPurchaseRecommendationRequestRequestTypeDef = TypedDict(
    "_OptionalGetReservationPurchaseRecommendationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Filter": "ExpressionTypeDef",
        "AccountScope": AccountScopeType,
        "LookbackPeriodInDays": LookbackPeriodInDaysType,
        "TermInYears": TermInYearsType,
        "PaymentOption": PaymentOptionType,
        "ServiceSpecification": ServiceSpecificationTypeDef,
        "PageSize": int,
        "NextPageToken": str,
    },
    total=False,
)


class GetReservationPurchaseRecommendationRequestRequestTypeDef(
    _RequiredGetReservationPurchaseRecommendationRequestRequestTypeDef,
    _OptionalGetReservationPurchaseRecommendationRequestRequestTypeDef,
):
    pass


ResultByTimeTypeDef = TypedDict(
    "ResultByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Total": Dict[str, MetricValueTypeDef],
        "Groups": List[GroupTypeDef],
        "Estimated": bool,
    },
    total=False,
)

UtilizationByTimeTypeDef = TypedDict(
    "UtilizationByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Groups": List[ReservationUtilizationGroupTypeDef],
        "Total": ReservationAggregatesTypeDef,
    },
    total=False,
)

ReservationPurchaseRecommendationDetailTypeDef = TypedDict(
    "ReservationPurchaseRecommendationDetailTypeDef",
    {
        "AccountId": str,
        "InstanceDetails": InstanceDetailsTypeDef,
        "RecommendedNumberOfInstancesToPurchase": str,
        "RecommendedNormalizedUnitsToPurchase": str,
        "MinimumNumberOfInstancesUsedPerHour": str,
        "MinimumNormalizedUnitsUsedPerHour": str,
        "MaximumNumberOfInstancesUsedPerHour": str,
        "MaximumNormalizedUnitsUsedPerHour": str,
        "AverageNumberOfInstancesUsedPerHour": str,
        "AverageNormalizedUnitsUsedPerHour": str,
        "AverageUtilization": str,
        "EstimatedBreakEvenInMonths": str,
        "CurrencyCode": str,
        "EstimatedMonthlySavingsAmount": str,
        "EstimatedMonthlySavingsPercentage": str,
        "EstimatedMonthlyOnDemandCost": str,
        "EstimatedReservationCostForLookbackPeriod": str,
        "UpfrontCost": str,
        "RecurringStandardMonthlyCost": str,
    },
    total=False,
)

GetSavingsPlansCoverageResponseTypeDef = TypedDict(
    "GetSavingsPlansCoverageResponseTypeDef",
    {
        "SavingsPlansCoverages": List[SavingsPlansCoverageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SavingsPlansPurchaseRecommendationTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationTypeDef",
    {
        "AccountScope": AccountScopeType,
        "SavingsPlansType": SupportedSavingsPlansTypeType,
        "TermInYears": TermInYearsType,
        "PaymentOption": PaymentOptionType,
        "LookbackPeriodInDays": LookbackPeriodInDaysType,
        "SavingsPlansPurchaseRecommendationDetails": List[
            SavingsPlansPurchaseRecommendationDetailTypeDef
        ],
        "SavingsPlansPurchaseRecommendationSummary": SavingsPlansPurchaseRecommendationSummaryTypeDef,
    },
    total=False,
)

GetSavingsPlansUtilizationResponseTypeDef = TypedDict(
    "GetSavingsPlansUtilizationResponseTypeDef",
    {
        "SavingsPlansUtilizationsByTime": List[SavingsPlansUtilizationByTimeTypeDef],
        "Total": SavingsPlansUtilizationAggregatesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSavingsPlansUtilizationDetailsResponseTypeDef = TypedDict(
    "GetSavingsPlansUtilizationDetailsResponseTypeDef",
    {
        "SavingsPlansUtilizationDetails": List[SavingsPlansUtilizationDetailTypeDef],
        "Total": SavingsPlansUtilizationAggregatesTypeDef,
        "TimePeriod": DateIntervalTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCostCategoryDefinitionResponseTypeDef = TypedDict(
    "DescribeCostCategoryDefinitionResponseTypeDef",
    {
        "CostCategory": CostCategoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CoverageByTimeTypeDef = TypedDict(
    "CoverageByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Groups": List[ReservationCoverageGroupTypeDef],
        "Total": CoverageTypeDef,
    },
    total=False,
)

CurrentInstanceTypeDef = TypedDict(
    "CurrentInstanceTypeDef",
    {
        "ResourceId": str,
        "InstanceName": str,
        "Tags": List[TagValuesTypeDef],
        "ResourceDetails": ResourceDetailsTypeDef,
        "ResourceUtilization": ResourceUtilizationTypeDef,
        "ReservationCoveredHoursInLookbackPeriod": str,
        "SavingsPlansCoveredHoursInLookbackPeriod": str,
        "OnDemandHoursInLookbackPeriod": str,
        "TotalRunningHoursInLookbackPeriod": str,
        "MonthlyCost": str,
        "CurrencyCode": str,
    },
    total=False,
)

TargetInstanceTypeDef = TypedDict(
    "TargetInstanceTypeDef",
    {
        "EstimatedMonthlyCost": str,
        "EstimatedMonthlySavings": str,
        "CurrencyCode": str,
        "DefaultTargetInstance": bool,
        "ResourceDetails": ResourceDetailsTypeDef,
        "ExpectedResourceUtilization": ResourceUtilizationTypeDef,
        "PlatformDifferences": List[PlatformDifferenceType],
    },
    total=False,
)

GetCostAndUsageResponseTypeDef = TypedDict(
    "GetCostAndUsageResponseTypeDef",
    {
        "NextPageToken": str,
        "GroupDefinitions": List[GroupDefinitionTypeDef],
        "ResultsByTime": List[ResultByTimeTypeDef],
        "DimensionValueAttributes": List[DimensionValuesWithAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCostAndUsageWithResourcesResponseTypeDef = TypedDict(
    "GetCostAndUsageWithResourcesResponseTypeDef",
    {
        "NextPageToken": str,
        "GroupDefinitions": List[GroupDefinitionTypeDef],
        "ResultsByTime": List[ResultByTimeTypeDef],
        "DimensionValueAttributes": List[DimensionValuesWithAttributesTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReservationUtilizationResponseTypeDef = TypedDict(
    "GetReservationUtilizationResponseTypeDef",
    {
        "UtilizationsByTime": List[UtilizationByTimeTypeDef],
        "Total": ReservationAggregatesTypeDef,
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservationPurchaseRecommendationTypeDef = TypedDict(
    "ReservationPurchaseRecommendationTypeDef",
    {
        "AccountScope": AccountScopeType,
        "LookbackPeriodInDays": LookbackPeriodInDaysType,
        "TermInYears": TermInYearsType,
        "PaymentOption": PaymentOptionType,
        "ServiceSpecification": ServiceSpecificationTypeDef,
        "RecommendationDetails": List[ReservationPurchaseRecommendationDetailTypeDef],
        "RecommendationSummary": ReservationPurchaseRecommendationSummaryTypeDef,
    },
    total=False,
)

GetSavingsPlansPurchaseRecommendationResponseTypeDef = TypedDict(
    "GetSavingsPlansPurchaseRecommendationResponseTypeDef",
    {
        "Metadata": SavingsPlansPurchaseRecommendationMetadataTypeDef,
        "SavingsPlansPurchaseRecommendation": SavingsPlansPurchaseRecommendationTypeDef,
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReservationCoverageResponseTypeDef = TypedDict(
    "GetReservationCoverageResponseTypeDef",
    {
        "CoveragesByTime": List[CoverageByTimeTypeDef],
        "Total": CoverageTypeDef,
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyRecommendationDetailTypeDef = TypedDict(
    "ModifyRecommendationDetailTypeDef",
    {
        "TargetInstances": List[TargetInstanceTypeDef],
    },
    total=False,
)

GetReservationPurchaseRecommendationResponseTypeDef = TypedDict(
    "GetReservationPurchaseRecommendationResponseTypeDef",
    {
        "Metadata": ReservationPurchaseRecommendationMetadataTypeDef,
        "Recommendations": List[ReservationPurchaseRecommendationTypeDef],
        "NextPageToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RightsizingRecommendationTypeDef = TypedDict(
    "RightsizingRecommendationTypeDef",
    {
        "AccountId": str,
        "CurrentInstance": CurrentInstanceTypeDef,
        "RightsizingType": RightsizingTypeType,
        "ModifyRecommendationDetail": ModifyRecommendationDetailTypeDef,
        "TerminateRecommendationDetail": TerminateRecommendationDetailTypeDef,
        "FindingReasonCodes": List[FindingReasonCodeType],
    },
    total=False,
)

GetRightsizingRecommendationResponseTypeDef = TypedDict(
    "GetRightsizingRecommendationResponseTypeDef",
    {
        "Metadata": RightsizingRecommendationMetadataTypeDef,
        "Summary": RightsizingRecommendationSummaryTypeDef,
        "RightsizingRecommendations": List[RightsizingRecommendationTypeDef],
        "NextPageToken": str,
        "Configuration": RightsizingRecommendationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
