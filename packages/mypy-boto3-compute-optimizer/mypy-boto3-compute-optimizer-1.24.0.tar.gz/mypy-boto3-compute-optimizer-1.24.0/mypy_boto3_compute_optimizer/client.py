"""
Type annotations for compute-optimizer service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_compute_optimizer.client import ComputeOptimizerClient

    session = Session()
    client: ComputeOptimizerClient = session.client("compute-optimizer")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import (
    EnhancedInfrastructureMetricsType,
    ExportableAutoScalingGroupFieldType,
    ExportableInstanceFieldType,
    ExportableLambdaFunctionFieldType,
    ExportableVolumeFieldType,
    InferredWorkloadTypesPreferenceType,
    MetricStatisticType,
    RecommendationPreferenceNameType,
    ResourceTypeType,
    StatusType,
)
from .type_defs import (
    DescribeRecommendationExportJobsResponseTypeDef,
    EBSFilterTypeDef,
    EnrollmentFilterTypeDef,
    ExportAutoScalingGroupRecommendationsResponseTypeDef,
    ExportEBSVolumeRecommendationsResponseTypeDef,
    ExportEC2InstanceRecommendationsResponseTypeDef,
    ExportLambdaFunctionRecommendationsResponseTypeDef,
    FilterTypeDef,
    GetAutoScalingGroupRecommendationsResponseTypeDef,
    GetEBSVolumeRecommendationsResponseTypeDef,
    GetEC2InstanceRecommendationsResponseTypeDef,
    GetEC2RecommendationProjectedMetricsResponseTypeDef,
    GetEffectiveRecommendationPreferencesResponseTypeDef,
    GetEnrollmentStatusesForOrganizationResponseTypeDef,
    GetEnrollmentStatusResponseTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetRecommendationPreferencesResponseTypeDef,
    GetRecommendationSummariesResponseTypeDef,
    JobFilterTypeDef,
    LambdaFunctionRecommendationFilterTypeDef,
    RecommendationPreferencesTypeDef,
    S3DestinationConfigTypeDef,
    ScopeTypeDef,
    UpdateEnrollmentStatusResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ComputeOptimizerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingAuthenticationToken: Type[BotocoreClientError]
    OptInRequiredException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class ComputeOptimizerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ComputeOptimizerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#can_paginate)
        """

    def delete_recommendation_preferences(
        self,
        *,
        resourceType: ResourceTypeType,
        recommendationPreferenceNames: Sequence[RecommendationPreferenceNameType],
        scope: ScopeTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Deletes a recommendation preference, such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.delete_recommendation_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#delete_recommendation_preferences)
        """

    def describe_recommendation_export_jobs(
        self,
        *,
        jobIds: Sequence[str] = ...,
        filters: Sequence[JobFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeRecommendationExportJobsResponseTypeDef:
        """
        Describes recommendation export jobs created in the last seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.describe_recommendation_export_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#describe_recommendation_export_jobs)
        """

    def export_auto_scaling_group_recommendations(
        self,
        *,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: Sequence[str] = ...,
        filters: Sequence[FilterTypeDef] = ...,
        fieldsToExport: Sequence[ExportableAutoScalingGroupFieldType] = ...,
        fileFormat: Literal["Csv"] = ...,
        includeMemberAccounts: bool = ...,
        recommendationPreferences: RecommendationPreferencesTypeDef = ...
    ) -> ExportAutoScalingGroupRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Auto Scaling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_auto_scaling_group_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#export_auto_scaling_group_recommendations)
        """

    def export_ebs_volume_recommendations(
        self,
        *,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: Sequence[str] = ...,
        filters: Sequence[EBSFilterTypeDef] = ...,
        fieldsToExport: Sequence[ExportableVolumeFieldType] = ...,
        fileFormat: Literal["Csv"] = ...,
        includeMemberAccounts: bool = ...
    ) -> ExportEBSVolumeRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Amazon EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_ebs_volume_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#export_ebs_volume_recommendations)
        """

    def export_ec2_instance_recommendations(
        self,
        *,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: Sequence[str] = ...,
        filters: Sequence[FilterTypeDef] = ...,
        fieldsToExport: Sequence[ExportableInstanceFieldType] = ...,
        fileFormat: Literal["Csv"] = ...,
        includeMemberAccounts: bool = ...,
        recommendationPreferences: RecommendationPreferencesTypeDef = ...
    ) -> ExportEC2InstanceRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_ec2_instance_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#export_ec2_instance_recommendations)
        """

    def export_lambda_function_recommendations(
        self,
        *,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: Sequence[str] = ...,
        filters: Sequence[LambdaFunctionRecommendationFilterTypeDef] = ...,
        fieldsToExport: Sequence[ExportableLambdaFunctionFieldType] = ...,
        fileFormat: Literal["Csv"] = ...,
        includeMemberAccounts: bool = ...
    ) -> ExportLambdaFunctionRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Lambda functions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_lambda_function_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#export_lambda_function_recommendations)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#generate_presigned_url)
        """

    def get_auto_scaling_group_recommendations(
        self,
        *,
        accountIds: Sequence[str] = ...,
        autoScalingGroupArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence[FilterTypeDef] = ...,
        recommendationPreferences: RecommendationPreferencesTypeDef = ...
    ) -> GetAutoScalingGroupRecommendationsResponseTypeDef:
        """
        Returns Auto Scaling group recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_auto_scaling_group_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_auto_scaling_group_recommendations)
        """

    def get_ebs_volume_recommendations(
        self,
        *,
        volumeArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence[EBSFilterTypeDef] = ...,
        accountIds: Sequence[str] = ...
    ) -> GetEBSVolumeRecommendationsResponseTypeDef:
        """
        Returns Amazon Elastic Block Store (Amazon EBS) volume recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ebs_volume_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_ebs_volume_recommendations)
        """

    def get_ec2_instance_recommendations(
        self,
        *,
        instanceArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence[FilterTypeDef] = ...,
        accountIds: Sequence[str] = ...,
        recommendationPreferences: RecommendationPreferencesTypeDef = ...
    ) -> GetEC2InstanceRecommendationsResponseTypeDef:
        """
        Returns Amazon EC2 instance recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ec2_instance_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_ec2_instance_recommendations)
        """

    def get_ec2_recommendation_projected_metrics(
        self,
        *,
        instanceArn: str,
        stat: MetricStatisticType,
        period: int,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        recommendationPreferences: RecommendationPreferencesTypeDef = ...
    ) -> GetEC2RecommendationProjectedMetricsResponseTypeDef:
        """
        Returns the projected utilization metrics of Amazon EC2 instance
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ec2_recommendation_projected_metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_ec2_recommendation_projected_metrics)
        """

    def get_effective_recommendation_preferences(
        self, *, resourceArn: str
    ) -> GetEffectiveRecommendationPreferencesResponseTypeDef:
        """
        Returns the recommendation preferences that are in effect for a given resource,
        such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_effective_recommendation_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_effective_recommendation_preferences)
        """

    def get_enrollment_status(self) -> GetEnrollmentStatusResponseTypeDef:
        """
        Returns the enrollment (opt in) status of an account to the Compute Optimizer
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_enrollment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_enrollment_status)
        """

    def get_enrollment_statuses_for_organization(
        self,
        *,
        filters: Sequence[EnrollmentFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetEnrollmentStatusesForOrganizationResponseTypeDef:
        """
        Returns the Compute Optimizer enrollment (opt-in) status of organization member
        accounts, if your account is an organization management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_enrollment_statuses_for_organization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_enrollment_statuses_for_organization)
        """

    def get_lambda_function_recommendations(
        self,
        *,
        functionArns: Sequence[str] = ...,
        accountIds: Sequence[str] = ...,
        filters: Sequence[LambdaFunctionRecommendationFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetLambdaFunctionRecommendationsResponseTypeDef:
        """
        Returns Lambda function recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_lambda_function_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_lambda_function_recommendations)
        """

    def get_recommendation_preferences(
        self,
        *,
        resourceType: ResourceTypeType,
        scope: ScopeTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetRecommendationPreferencesResponseTypeDef:
        """
        Returns existing recommendation preferences, such as enhanced infrastructure
        metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_recommendation_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_recommendation_preferences)
        """

    def get_recommendation_summaries(
        self, *, accountIds: Sequence[str] = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetRecommendationSummariesResponseTypeDef:
        """
        Returns the optimization findings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_recommendation_summaries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#get_recommendation_summaries)
        """

    def put_recommendation_preferences(
        self,
        *,
        resourceType: ResourceTypeType,
        scope: ScopeTypeDef = ...,
        enhancedInfrastructureMetrics: EnhancedInfrastructureMetricsType = ...,
        inferredWorkloadTypes: InferredWorkloadTypesPreferenceType = ...
    ) -> Dict[str, Any]:
        """
        Creates a new recommendation preference or updates an existing recommendation
        preference, such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.put_recommendation_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#put_recommendation_preferences)
        """

    def update_enrollment_status(
        self, *, status: StatusType, includeMemberAccounts: bool = ...
    ) -> UpdateEnrollmentStatusResponseTypeDef:
        """
        Updates the enrollment (opt in and opt out) status of an account to the Compute
        Optimizer service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client.update_enrollment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client/#update_enrollment_status)
        """
