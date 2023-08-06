"""
Type annotations for compute-optimizer service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/type_defs/)

Usage::

    ```python
    from mypy_boto3_compute_optimizer.type_defs import AccountEnrollmentStatusTypeDef

    data: AccountEnrollmentStatusTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    CpuVendorArchitectureType,
    CurrencyType,
    CurrentPerformanceRiskType,
    EBSFindingType,
    EBSMetricNameType,
    EnhancedInfrastructureMetricsType,
    ExportableAutoScalingGroupFieldType,
    ExportableInstanceFieldType,
    ExportableLambdaFunctionFieldType,
    ExportableVolumeFieldType,
    FilterNameType,
    FindingReasonCodeType,
    FindingType,
    InferredWorkloadTypesPreferenceType,
    InferredWorkloadTypeType,
    InstanceRecommendationFindingReasonCodeType,
    JobFilterNameType,
    JobStatusType,
    LambdaFunctionMemoryMetricStatisticType,
    LambdaFunctionMetricNameType,
    LambdaFunctionMetricStatisticType,
    LambdaFunctionRecommendationFilterNameType,
    LambdaFunctionRecommendationFindingReasonCodeType,
    LambdaFunctionRecommendationFindingType,
    MetricNameType,
    MetricStatisticType,
    MigrationEffortType,
    PlatformDifferenceType,
    RecommendationPreferenceNameType,
    RecommendationSourceTypeType,
    ResourceTypeType,
    ScopeNameType,
    StatusType,
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
    "AccountEnrollmentStatusTypeDef",
    "AutoScalingGroupConfigurationTypeDef",
    "UtilizationMetricTypeDef",
    "EffectiveRecommendationPreferencesTypeDef",
    "CurrentPerformanceRiskRatingsTypeDef",
    "ScopeTypeDef",
    "JobFilterTypeDef",
    "ResponseMetadataTypeDef",
    "EBSFilterTypeDef",
    "EBSUtilizationMetricTypeDef",
    "EnrollmentFilterTypeDef",
    "EstimatedMonthlySavingsTypeDef",
    "FilterTypeDef",
    "RecommendationPreferencesTypeDef",
    "S3DestinationConfigTypeDef",
    "S3DestinationTypeDef",
    "LambdaFunctionRecommendationFilterTypeDef",
    "GetRecommendationErrorTypeDef",
    "GetEffectiveRecommendationPreferencesRequestRequestTypeDef",
    "GetRecommendationSummariesRequestRequestTypeDef",
    "RecommendationSourceTypeDef",
    "LambdaFunctionMemoryProjectedMetricTypeDef",
    "LambdaFunctionUtilizationMetricTypeDef",
    "ProjectedMetricTypeDef",
    "ReasonCodeSummaryTypeDef",
    "UpdateEnrollmentStatusRequestRequestTypeDef",
    "VolumeConfigurationTypeDef",
    "DeleteRecommendationPreferencesRequestRequestTypeDef",
    "GetRecommendationPreferencesRequestRequestTypeDef",
    "PutRecommendationPreferencesRequestRequestTypeDef",
    "RecommendationPreferencesDetailTypeDef",
    "DescribeRecommendationExportJobsRequestRequestTypeDef",
    "GetEffectiveRecommendationPreferencesResponseTypeDef",
    "GetEnrollmentStatusResponseTypeDef",
    "GetEnrollmentStatusesForOrganizationResponseTypeDef",
    "UpdateEnrollmentStatusResponseTypeDef",
    "GetEBSVolumeRecommendationsRequestRequestTypeDef",
    "GetEnrollmentStatusesForOrganizationRequestRequestTypeDef",
    "SavingsOpportunityTypeDef",
    "GetAutoScalingGroupRecommendationsRequestRequestTypeDef",
    "GetEC2InstanceRecommendationsRequestRequestTypeDef",
    "GetEC2RecommendationProjectedMetricsRequestRequestTypeDef",
    "ExportAutoScalingGroupRecommendationsRequestRequestTypeDef",
    "ExportEBSVolumeRecommendationsRequestRequestTypeDef",
    "ExportEC2InstanceRecommendationsRequestRequestTypeDef",
    "ExportAutoScalingGroupRecommendationsResponseTypeDef",
    "ExportDestinationTypeDef",
    "ExportEBSVolumeRecommendationsResponseTypeDef",
    "ExportEC2InstanceRecommendationsResponseTypeDef",
    "ExportLambdaFunctionRecommendationsResponseTypeDef",
    "ExportLambdaFunctionRecommendationsRequestRequestTypeDef",
    "GetLambdaFunctionRecommendationsRequestRequestTypeDef",
    "RecommendedOptionProjectedMetricTypeDef",
    "SummaryTypeDef",
    "GetRecommendationPreferencesResponseTypeDef",
    "AutoScalingGroupRecommendationOptionTypeDef",
    "InstanceRecommendationOptionTypeDef",
    "LambdaFunctionMemoryRecommendationOptionTypeDef",
    "VolumeRecommendationOptionTypeDef",
    "RecommendationExportJobTypeDef",
    "GetEC2RecommendationProjectedMetricsResponseTypeDef",
    "RecommendationSummaryTypeDef",
    "AutoScalingGroupRecommendationTypeDef",
    "InstanceRecommendationTypeDef",
    "LambdaFunctionRecommendationTypeDef",
    "VolumeRecommendationTypeDef",
    "DescribeRecommendationExportJobsResponseTypeDef",
    "GetRecommendationSummariesResponseTypeDef",
    "GetAutoScalingGroupRecommendationsResponseTypeDef",
    "GetEC2InstanceRecommendationsResponseTypeDef",
    "GetLambdaFunctionRecommendationsResponseTypeDef",
    "GetEBSVolumeRecommendationsResponseTypeDef",
)

AccountEnrollmentStatusTypeDef = TypedDict(
    "AccountEnrollmentStatusTypeDef",
    {
        "accountId": str,
        "status": StatusType,
        "statusReason": str,
        "lastUpdatedTimestamp": datetime,
    },
    total=False,
)

AutoScalingGroupConfigurationTypeDef = TypedDict(
    "AutoScalingGroupConfigurationTypeDef",
    {
        "desiredCapacity": int,
        "minSize": int,
        "maxSize": int,
        "instanceType": str,
    },
    total=False,
)

UtilizationMetricTypeDef = TypedDict(
    "UtilizationMetricTypeDef",
    {
        "name": MetricNameType,
        "statistic": MetricStatisticType,
        "value": float,
    },
    total=False,
)

EffectiveRecommendationPreferencesTypeDef = TypedDict(
    "EffectiveRecommendationPreferencesTypeDef",
    {
        "cpuVendorArchitectures": List[CpuVendorArchitectureType],
        "enhancedInfrastructureMetrics": EnhancedInfrastructureMetricsType,
        "inferredWorkloadTypes": InferredWorkloadTypesPreferenceType,
    },
    total=False,
)

CurrentPerformanceRiskRatingsTypeDef = TypedDict(
    "CurrentPerformanceRiskRatingsTypeDef",
    {
        "high": int,
        "medium": int,
        "low": int,
        "veryLow": int,
    },
    total=False,
)

ScopeTypeDef = TypedDict(
    "ScopeTypeDef",
    {
        "name": ScopeNameType,
        "value": str,
    },
    total=False,
)

JobFilterTypeDef = TypedDict(
    "JobFilterTypeDef",
    {
        "name": JobFilterNameType,
        "values": Sequence[str],
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

EBSFilterTypeDef = TypedDict(
    "EBSFilterTypeDef",
    {
        "name": Literal["Finding"],
        "values": Sequence[str],
    },
    total=False,
)

EBSUtilizationMetricTypeDef = TypedDict(
    "EBSUtilizationMetricTypeDef",
    {
        "name": EBSMetricNameType,
        "statistic": MetricStatisticType,
        "value": float,
    },
    total=False,
)

EnrollmentFilterTypeDef = TypedDict(
    "EnrollmentFilterTypeDef",
    {
        "name": Literal["Status"],
        "values": Sequence[str],
    },
    total=False,
)

EstimatedMonthlySavingsTypeDef = TypedDict(
    "EstimatedMonthlySavingsTypeDef",
    {
        "currency": CurrencyType,
        "value": float,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "name": FilterNameType,
        "values": Sequence[str],
    },
    total=False,
)

RecommendationPreferencesTypeDef = TypedDict(
    "RecommendationPreferencesTypeDef",
    {
        "cpuVendorArchitectures": Sequence[CpuVendorArchitectureType],
    },
    total=False,
)

S3DestinationConfigTypeDef = TypedDict(
    "S3DestinationConfigTypeDef",
    {
        "bucket": str,
        "keyPrefix": str,
    },
    total=False,
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "bucket": str,
        "key": str,
        "metadataKey": str,
    },
    total=False,
)

LambdaFunctionRecommendationFilterTypeDef = TypedDict(
    "LambdaFunctionRecommendationFilterTypeDef",
    {
        "name": LambdaFunctionRecommendationFilterNameType,
        "values": Sequence[str],
    },
    total=False,
)

GetRecommendationErrorTypeDef = TypedDict(
    "GetRecommendationErrorTypeDef",
    {
        "identifier": str,
        "code": str,
        "message": str,
    },
    total=False,
)

GetEffectiveRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "GetEffectiveRecommendationPreferencesRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

GetRecommendationSummariesRequestRequestTypeDef = TypedDict(
    "GetRecommendationSummariesRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

RecommendationSourceTypeDef = TypedDict(
    "RecommendationSourceTypeDef",
    {
        "recommendationSourceArn": str,
        "recommendationSourceType": RecommendationSourceTypeType,
    },
    total=False,
)

LambdaFunctionMemoryProjectedMetricTypeDef = TypedDict(
    "LambdaFunctionMemoryProjectedMetricTypeDef",
    {
        "name": Literal["Duration"],
        "statistic": LambdaFunctionMemoryMetricStatisticType,
        "value": float,
    },
    total=False,
)

LambdaFunctionUtilizationMetricTypeDef = TypedDict(
    "LambdaFunctionUtilizationMetricTypeDef",
    {
        "name": LambdaFunctionMetricNameType,
        "statistic": LambdaFunctionMetricStatisticType,
        "value": float,
    },
    total=False,
)

ProjectedMetricTypeDef = TypedDict(
    "ProjectedMetricTypeDef",
    {
        "name": MetricNameType,
        "timestamps": List[datetime],
        "values": List[float],
    },
    total=False,
)

ReasonCodeSummaryTypeDef = TypedDict(
    "ReasonCodeSummaryTypeDef",
    {
        "name": FindingReasonCodeType,
        "value": float,
    },
    total=False,
)

_RequiredUpdateEnrollmentStatusRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEnrollmentStatusRequestRequestTypeDef",
    {
        "status": StatusType,
    },
)
_OptionalUpdateEnrollmentStatusRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEnrollmentStatusRequestRequestTypeDef",
    {
        "includeMemberAccounts": bool,
    },
    total=False,
)


class UpdateEnrollmentStatusRequestRequestTypeDef(
    _RequiredUpdateEnrollmentStatusRequestRequestTypeDef,
    _OptionalUpdateEnrollmentStatusRequestRequestTypeDef,
):
    pass


VolumeConfigurationTypeDef = TypedDict(
    "VolumeConfigurationTypeDef",
    {
        "volumeType": str,
        "volumeSize": int,
        "volumeBaselineIOPS": int,
        "volumeBurstIOPS": int,
        "volumeBaselineThroughput": int,
        "volumeBurstThroughput": int,
    },
    total=False,
)

_RequiredDeleteRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRecommendationPreferencesRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
        "recommendationPreferenceNames": Sequence[RecommendationPreferenceNameType],
    },
)
_OptionalDeleteRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRecommendationPreferencesRequestRequestTypeDef",
    {
        "scope": ScopeTypeDef,
    },
    total=False,
)


class DeleteRecommendationPreferencesRequestRequestTypeDef(
    _RequiredDeleteRecommendationPreferencesRequestRequestTypeDef,
    _OptionalDeleteRecommendationPreferencesRequestRequestTypeDef,
):
    pass


_RequiredGetRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_RequiredGetRecommendationPreferencesRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
    },
)
_OptionalGetRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_OptionalGetRecommendationPreferencesRequestRequestTypeDef",
    {
        "scope": ScopeTypeDef,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetRecommendationPreferencesRequestRequestTypeDef(
    _RequiredGetRecommendationPreferencesRequestRequestTypeDef,
    _OptionalGetRecommendationPreferencesRequestRequestTypeDef,
):
    pass


_RequiredPutRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_RequiredPutRecommendationPreferencesRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
    },
)
_OptionalPutRecommendationPreferencesRequestRequestTypeDef = TypedDict(
    "_OptionalPutRecommendationPreferencesRequestRequestTypeDef",
    {
        "scope": ScopeTypeDef,
        "enhancedInfrastructureMetrics": EnhancedInfrastructureMetricsType,
        "inferredWorkloadTypes": InferredWorkloadTypesPreferenceType,
    },
    total=False,
)


class PutRecommendationPreferencesRequestRequestTypeDef(
    _RequiredPutRecommendationPreferencesRequestRequestTypeDef,
    _OptionalPutRecommendationPreferencesRequestRequestTypeDef,
):
    pass


RecommendationPreferencesDetailTypeDef = TypedDict(
    "RecommendationPreferencesDetailTypeDef",
    {
        "scope": ScopeTypeDef,
        "resourceType": ResourceTypeType,
        "enhancedInfrastructureMetrics": EnhancedInfrastructureMetricsType,
        "inferredWorkloadTypes": InferredWorkloadTypesPreferenceType,
    },
    total=False,
)

DescribeRecommendationExportJobsRequestRequestTypeDef = TypedDict(
    "DescribeRecommendationExportJobsRequestRequestTypeDef",
    {
        "jobIds": Sequence[str],
        "filters": Sequence[JobFilterTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetEffectiveRecommendationPreferencesResponseTypeDef = TypedDict(
    "GetEffectiveRecommendationPreferencesResponseTypeDef",
    {
        "enhancedInfrastructureMetrics": EnhancedInfrastructureMetricsType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnrollmentStatusResponseTypeDef = TypedDict(
    "GetEnrollmentStatusResponseTypeDef",
    {
        "status": StatusType,
        "statusReason": str,
        "memberAccountsEnrolled": bool,
        "lastUpdatedTimestamp": datetime,
        "numberOfMemberAccountsOptedIn": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnrollmentStatusesForOrganizationResponseTypeDef = TypedDict(
    "GetEnrollmentStatusesForOrganizationResponseTypeDef",
    {
        "accountEnrollmentStatuses": List[AccountEnrollmentStatusTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnrollmentStatusResponseTypeDef = TypedDict(
    "UpdateEnrollmentStatusResponseTypeDef",
    {
        "status": StatusType,
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEBSVolumeRecommendationsRequestRequestTypeDef = TypedDict(
    "GetEBSVolumeRecommendationsRequestRequestTypeDef",
    {
        "volumeArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[EBSFilterTypeDef],
        "accountIds": Sequence[str],
    },
    total=False,
)

GetEnrollmentStatusesForOrganizationRequestRequestTypeDef = TypedDict(
    "GetEnrollmentStatusesForOrganizationRequestRequestTypeDef",
    {
        "filters": Sequence[EnrollmentFilterTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SavingsOpportunityTypeDef = TypedDict(
    "SavingsOpportunityTypeDef",
    {
        "savingsOpportunityPercentage": float,
        "estimatedMonthlySavings": EstimatedMonthlySavingsTypeDef,
    },
    total=False,
)

GetAutoScalingGroupRecommendationsRequestRequestTypeDef = TypedDict(
    "GetAutoScalingGroupRecommendationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "autoScalingGroupArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
        "recommendationPreferences": RecommendationPreferencesTypeDef,
    },
    total=False,
)

GetEC2InstanceRecommendationsRequestRequestTypeDef = TypedDict(
    "GetEC2InstanceRecommendationsRequestRequestTypeDef",
    {
        "instanceArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
        "accountIds": Sequence[str],
        "recommendationPreferences": RecommendationPreferencesTypeDef,
    },
    total=False,
)

_RequiredGetEC2RecommendationProjectedMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredGetEC2RecommendationProjectedMetricsRequestRequestTypeDef",
    {
        "instanceArn": str,
        "stat": MetricStatisticType,
        "period": int,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
)
_OptionalGetEC2RecommendationProjectedMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalGetEC2RecommendationProjectedMetricsRequestRequestTypeDef",
    {
        "recommendationPreferences": RecommendationPreferencesTypeDef,
    },
    total=False,
)


class GetEC2RecommendationProjectedMetricsRequestRequestTypeDef(
    _RequiredGetEC2RecommendationProjectedMetricsRequestRequestTypeDef,
    _OptionalGetEC2RecommendationProjectedMetricsRequestRequestTypeDef,
):
    pass


_RequiredExportAutoScalingGroupRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredExportAutoScalingGroupRecommendationsRequestRequestTypeDef",
    {
        "s3DestinationConfig": S3DestinationConfigTypeDef,
    },
)
_OptionalExportAutoScalingGroupRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalExportAutoScalingGroupRecommendationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "filters": Sequence[FilterTypeDef],
        "fieldsToExport": Sequence[ExportableAutoScalingGroupFieldType],
        "fileFormat": Literal["Csv"],
        "includeMemberAccounts": bool,
        "recommendationPreferences": RecommendationPreferencesTypeDef,
    },
    total=False,
)


class ExportAutoScalingGroupRecommendationsRequestRequestTypeDef(
    _RequiredExportAutoScalingGroupRecommendationsRequestRequestTypeDef,
    _OptionalExportAutoScalingGroupRecommendationsRequestRequestTypeDef,
):
    pass


_RequiredExportEBSVolumeRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredExportEBSVolumeRecommendationsRequestRequestTypeDef",
    {
        "s3DestinationConfig": S3DestinationConfigTypeDef,
    },
)
_OptionalExportEBSVolumeRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalExportEBSVolumeRecommendationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "filters": Sequence[EBSFilterTypeDef],
        "fieldsToExport": Sequence[ExportableVolumeFieldType],
        "fileFormat": Literal["Csv"],
        "includeMemberAccounts": bool,
    },
    total=False,
)


class ExportEBSVolumeRecommendationsRequestRequestTypeDef(
    _RequiredExportEBSVolumeRecommendationsRequestRequestTypeDef,
    _OptionalExportEBSVolumeRecommendationsRequestRequestTypeDef,
):
    pass


_RequiredExportEC2InstanceRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredExportEC2InstanceRecommendationsRequestRequestTypeDef",
    {
        "s3DestinationConfig": S3DestinationConfigTypeDef,
    },
)
_OptionalExportEC2InstanceRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalExportEC2InstanceRecommendationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "filters": Sequence[FilterTypeDef],
        "fieldsToExport": Sequence[ExportableInstanceFieldType],
        "fileFormat": Literal["Csv"],
        "includeMemberAccounts": bool,
        "recommendationPreferences": RecommendationPreferencesTypeDef,
    },
    total=False,
)


class ExportEC2InstanceRecommendationsRequestRequestTypeDef(
    _RequiredExportEC2InstanceRecommendationsRequestRequestTypeDef,
    _OptionalExportEC2InstanceRecommendationsRequestRequestTypeDef,
):
    pass


ExportAutoScalingGroupRecommendationsResponseTypeDef = TypedDict(
    "ExportAutoScalingGroupRecommendationsResponseTypeDef",
    {
        "jobId": str,
        "s3Destination": S3DestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportDestinationTypeDef = TypedDict(
    "ExportDestinationTypeDef",
    {
        "s3": S3DestinationTypeDef,
    },
    total=False,
)

ExportEBSVolumeRecommendationsResponseTypeDef = TypedDict(
    "ExportEBSVolumeRecommendationsResponseTypeDef",
    {
        "jobId": str,
        "s3Destination": S3DestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportEC2InstanceRecommendationsResponseTypeDef = TypedDict(
    "ExportEC2InstanceRecommendationsResponseTypeDef",
    {
        "jobId": str,
        "s3Destination": S3DestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportLambdaFunctionRecommendationsResponseTypeDef = TypedDict(
    "ExportLambdaFunctionRecommendationsResponseTypeDef",
    {
        "jobId": str,
        "s3Destination": S3DestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredExportLambdaFunctionRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredExportLambdaFunctionRecommendationsRequestRequestTypeDef",
    {
        "s3DestinationConfig": S3DestinationConfigTypeDef,
    },
)
_OptionalExportLambdaFunctionRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalExportLambdaFunctionRecommendationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "filters": Sequence[LambdaFunctionRecommendationFilterTypeDef],
        "fieldsToExport": Sequence[ExportableLambdaFunctionFieldType],
        "fileFormat": Literal["Csv"],
        "includeMemberAccounts": bool,
    },
    total=False,
)


class ExportLambdaFunctionRecommendationsRequestRequestTypeDef(
    _RequiredExportLambdaFunctionRecommendationsRequestRequestTypeDef,
    _OptionalExportLambdaFunctionRecommendationsRequestRequestTypeDef,
):
    pass


GetLambdaFunctionRecommendationsRequestRequestTypeDef = TypedDict(
    "GetLambdaFunctionRecommendationsRequestRequestTypeDef",
    {
        "functionArns": Sequence[str],
        "accountIds": Sequence[str],
        "filters": Sequence[LambdaFunctionRecommendationFilterTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

RecommendedOptionProjectedMetricTypeDef = TypedDict(
    "RecommendedOptionProjectedMetricTypeDef",
    {
        "recommendedInstanceType": str,
        "rank": int,
        "projectedMetrics": List[ProjectedMetricTypeDef],
    },
    total=False,
)

SummaryTypeDef = TypedDict(
    "SummaryTypeDef",
    {
        "name": FindingType,
        "value": float,
        "reasonCodeSummaries": List[ReasonCodeSummaryTypeDef],
    },
    total=False,
)

GetRecommendationPreferencesResponseTypeDef = TypedDict(
    "GetRecommendationPreferencesResponseTypeDef",
    {
        "nextToken": str,
        "recommendationPreferencesDetails": List[RecommendationPreferencesDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AutoScalingGroupRecommendationOptionTypeDef = TypedDict(
    "AutoScalingGroupRecommendationOptionTypeDef",
    {
        "configuration": AutoScalingGroupConfigurationTypeDef,
        "projectedUtilizationMetrics": List[UtilizationMetricTypeDef],
        "performanceRisk": float,
        "rank": int,
        "savingsOpportunity": SavingsOpportunityTypeDef,
        "migrationEffort": MigrationEffortType,
    },
    total=False,
)

InstanceRecommendationOptionTypeDef = TypedDict(
    "InstanceRecommendationOptionTypeDef",
    {
        "instanceType": str,
        "projectedUtilizationMetrics": List[UtilizationMetricTypeDef],
        "platformDifferences": List[PlatformDifferenceType],
        "performanceRisk": float,
        "rank": int,
        "savingsOpportunity": SavingsOpportunityTypeDef,
        "migrationEffort": MigrationEffortType,
    },
    total=False,
)

LambdaFunctionMemoryRecommendationOptionTypeDef = TypedDict(
    "LambdaFunctionMemoryRecommendationOptionTypeDef",
    {
        "rank": int,
        "memorySize": int,
        "projectedUtilizationMetrics": List[LambdaFunctionMemoryProjectedMetricTypeDef],
        "savingsOpportunity": SavingsOpportunityTypeDef,
    },
    total=False,
)

VolumeRecommendationOptionTypeDef = TypedDict(
    "VolumeRecommendationOptionTypeDef",
    {
        "configuration": VolumeConfigurationTypeDef,
        "performanceRisk": float,
        "rank": int,
        "savingsOpportunity": SavingsOpportunityTypeDef,
    },
    total=False,
)

RecommendationExportJobTypeDef = TypedDict(
    "RecommendationExportJobTypeDef",
    {
        "jobId": str,
        "destination": ExportDestinationTypeDef,
        "resourceType": ResourceTypeType,
        "status": JobStatusType,
        "creationTimestamp": datetime,
        "lastUpdatedTimestamp": datetime,
        "failureReason": str,
    },
    total=False,
)

GetEC2RecommendationProjectedMetricsResponseTypeDef = TypedDict(
    "GetEC2RecommendationProjectedMetricsResponseTypeDef",
    {
        "recommendedOptionProjectedMetrics": List[RecommendedOptionProjectedMetricTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecommendationSummaryTypeDef = TypedDict(
    "RecommendationSummaryTypeDef",
    {
        "summaries": List[SummaryTypeDef],
        "recommendationResourceType": RecommendationSourceTypeType,
        "accountId": str,
        "savingsOpportunity": SavingsOpportunityTypeDef,
        "currentPerformanceRiskRatings": CurrentPerformanceRiskRatingsTypeDef,
    },
    total=False,
)

AutoScalingGroupRecommendationTypeDef = TypedDict(
    "AutoScalingGroupRecommendationTypeDef",
    {
        "accountId": str,
        "autoScalingGroupArn": str,
        "autoScalingGroupName": str,
        "finding": FindingType,
        "utilizationMetrics": List[UtilizationMetricTypeDef],
        "lookBackPeriodInDays": float,
        "currentConfiguration": AutoScalingGroupConfigurationTypeDef,
        "recommendationOptions": List[AutoScalingGroupRecommendationOptionTypeDef],
        "lastRefreshTimestamp": datetime,
        "currentPerformanceRisk": CurrentPerformanceRiskType,
        "effectiveRecommendationPreferences": EffectiveRecommendationPreferencesTypeDef,
        "inferredWorkloadTypes": List[InferredWorkloadTypeType],
    },
    total=False,
)

InstanceRecommendationTypeDef = TypedDict(
    "InstanceRecommendationTypeDef",
    {
        "instanceArn": str,
        "accountId": str,
        "instanceName": str,
        "currentInstanceType": str,
        "finding": FindingType,
        "findingReasonCodes": List[InstanceRecommendationFindingReasonCodeType],
        "utilizationMetrics": List[UtilizationMetricTypeDef],
        "lookBackPeriodInDays": float,
        "recommendationOptions": List[InstanceRecommendationOptionTypeDef],
        "recommendationSources": List[RecommendationSourceTypeDef],
        "lastRefreshTimestamp": datetime,
        "currentPerformanceRisk": CurrentPerformanceRiskType,
        "effectiveRecommendationPreferences": EffectiveRecommendationPreferencesTypeDef,
        "inferredWorkloadTypes": List[InferredWorkloadTypeType],
    },
    total=False,
)

LambdaFunctionRecommendationTypeDef = TypedDict(
    "LambdaFunctionRecommendationTypeDef",
    {
        "functionArn": str,
        "functionVersion": str,
        "accountId": str,
        "currentMemorySize": int,
        "numberOfInvocations": int,
        "utilizationMetrics": List[LambdaFunctionUtilizationMetricTypeDef],
        "lookbackPeriodInDays": float,
        "lastRefreshTimestamp": datetime,
        "finding": LambdaFunctionRecommendationFindingType,
        "findingReasonCodes": List[LambdaFunctionRecommendationFindingReasonCodeType],
        "memorySizeRecommendationOptions": List[LambdaFunctionMemoryRecommendationOptionTypeDef],
        "currentPerformanceRisk": CurrentPerformanceRiskType,
    },
    total=False,
)

VolumeRecommendationTypeDef = TypedDict(
    "VolumeRecommendationTypeDef",
    {
        "volumeArn": str,
        "accountId": str,
        "currentConfiguration": VolumeConfigurationTypeDef,
        "finding": EBSFindingType,
        "utilizationMetrics": List[EBSUtilizationMetricTypeDef],
        "lookBackPeriodInDays": float,
        "volumeRecommendationOptions": List[VolumeRecommendationOptionTypeDef],
        "lastRefreshTimestamp": datetime,
        "currentPerformanceRisk": CurrentPerformanceRiskType,
    },
    total=False,
)

DescribeRecommendationExportJobsResponseTypeDef = TypedDict(
    "DescribeRecommendationExportJobsResponseTypeDef",
    {
        "recommendationExportJobs": List[RecommendationExportJobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecommendationSummariesResponseTypeDef = TypedDict(
    "GetRecommendationSummariesResponseTypeDef",
    {
        "nextToken": str,
        "recommendationSummaries": List[RecommendationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAutoScalingGroupRecommendationsResponseTypeDef = TypedDict(
    "GetAutoScalingGroupRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "autoScalingGroupRecommendations": List[AutoScalingGroupRecommendationTypeDef],
        "errors": List[GetRecommendationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEC2InstanceRecommendationsResponseTypeDef = TypedDict(
    "GetEC2InstanceRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "instanceRecommendations": List[InstanceRecommendationTypeDef],
        "errors": List[GetRecommendationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLambdaFunctionRecommendationsResponseTypeDef = TypedDict(
    "GetLambdaFunctionRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "lambdaFunctionRecommendations": List[LambdaFunctionRecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEBSVolumeRecommendationsResponseTypeDef = TypedDict(
    "GetEBSVolumeRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "volumeRecommendations": List[VolumeRecommendationTypeDef],
        "errors": List[GetRecommendationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
