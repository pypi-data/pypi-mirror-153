"""
Type annotations for resiliencehub service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resiliencehub.client import ResilienceHubClient

    session = Session()
    client: ResilienceHubClient = session.client("resiliencehub")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AppAssessmentScheduleTypeType,
    AssessmentInvokerType,
    AssessmentStatusType,
    ComplianceStatusType,
    DataLocationConstraintType,
    DisruptionTypeType,
    RecommendationTemplateStatusType,
    RenderRecommendationTypeType,
    ResiliencyPolicyTierType,
    TemplateFormatType,
)
from .type_defs import (
    AddDraftAppVersionResourceMappingsResponseTypeDef,
    CreateAppResponseTypeDef,
    CreateRecommendationTemplateResponseTypeDef,
    CreateResiliencyPolicyResponseTypeDef,
    DeleteAppAssessmentResponseTypeDef,
    DeleteAppResponseTypeDef,
    DeleteRecommendationTemplateResponseTypeDef,
    DeleteResiliencyPolicyResponseTypeDef,
    DescribeAppAssessmentResponseTypeDef,
    DescribeAppResponseTypeDef,
    DescribeAppVersionResourcesResolutionStatusResponseTypeDef,
    DescribeAppVersionTemplateResponseTypeDef,
    DescribeDraftAppVersionResourcesImportStatusResponseTypeDef,
    DescribeResiliencyPolicyResponseTypeDef,
    FailurePolicyTypeDef,
    ImportResourcesToDraftAppVersionResponseTypeDef,
    ListAlarmRecommendationsResponseTypeDef,
    ListAppAssessmentsResponseTypeDef,
    ListAppComponentCompliancesResponseTypeDef,
    ListAppComponentRecommendationsResponseTypeDef,
    ListAppsResponseTypeDef,
    ListAppVersionResourceMappingsResponseTypeDef,
    ListAppVersionResourcesResponseTypeDef,
    ListAppVersionsResponseTypeDef,
    ListRecommendationTemplatesResponseTypeDef,
    ListResiliencyPoliciesResponseTypeDef,
    ListSopRecommendationsResponseTypeDef,
    ListSuggestedResiliencyPoliciesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestRecommendationsResponseTypeDef,
    ListUnsupportedAppVersionResourcesResponseTypeDef,
    PublishAppVersionResponseTypeDef,
    PutDraftAppVersionTemplateResponseTypeDef,
    RemoveDraftAppVersionResourceMappingsResponseTypeDef,
    ResolveAppVersionResourcesResponseTypeDef,
    ResourceMappingTypeDef,
    StartAppAssessmentResponseTypeDef,
    TerraformSourceTypeDef,
    UpdateAppResponseTypeDef,
    UpdateResiliencyPolicyResponseTypeDef,
)

__all__ = ("ResilienceHubClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ResilienceHubClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResilienceHubClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#exceptions)
        """

    def add_draft_app_version_resource_mappings(
        self, *, appArn: str, resourceMappings: Sequence[ResourceMappingTypeDef]
    ) -> AddDraftAppVersionResourceMappingsResponseTypeDef:
        """
        Adds the resource mapping for the draft application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.add_draft_app_version_resource_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#add_draft_app_version_resource_mappings)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#can_paginate)
        """

    def create_app(
        self,
        *,
        name: str,
        assessmentSchedule: AppAssessmentScheduleTypeType = ...,
        clientToken: str = ...,
        description: str = ...,
        policyArn: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAppResponseTypeDef:
        """
        Creates a Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.create_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#create_app)
        """

    def create_recommendation_template(
        self,
        *,
        assessmentArn: str,
        name: str,
        bucketName: str = ...,
        clientToken: str = ...,
        format: TemplateFormatType = ...,
        recommendationIds: Sequence[str] = ...,
        recommendationTypes: Sequence[RenderRecommendationTypeType] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateRecommendationTemplateResponseTypeDef:
        """
        Creates a new recommendation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.create_recommendation_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#create_recommendation_template)
        """

    def create_resiliency_policy(
        self,
        *,
        policy: Mapping[DisruptionTypeType, FailurePolicyTypeDef],
        policyName: str,
        tier: ResiliencyPolicyTierType,
        clientToken: str = ...,
        dataLocationConstraint: DataLocationConstraintType = ...,
        policyDescription: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateResiliencyPolicyResponseTypeDef:
        """
        Creates a resiliency policy for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.create_resiliency_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#create_resiliency_policy)
        """

    def delete_app(
        self, *, appArn: str, clientToken: str = ..., forceDelete: bool = ...
    ) -> DeleteAppResponseTypeDef:
        """
        Deletes an AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.delete_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#delete_app)
        """

    def delete_app_assessment(
        self, *, assessmentArn: str, clientToken: str = ...
    ) -> DeleteAppAssessmentResponseTypeDef:
        """
        Deletes an AWS Resilience Hub application assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.delete_app_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#delete_app_assessment)
        """

    def delete_recommendation_template(
        self, *, recommendationTemplateArn: str, clientToken: str = ...
    ) -> DeleteRecommendationTemplateResponseTypeDef:
        """
        Deletes a recommendation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.delete_recommendation_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#delete_recommendation_template)
        """

    def delete_resiliency_policy(
        self, *, policyArn: str, clientToken: str = ...
    ) -> DeleteResiliencyPolicyResponseTypeDef:
        """
        Deletes a resiliency policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.delete_resiliency_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#delete_resiliency_policy)
        """

    def describe_app(self, *, appArn: str) -> DescribeAppResponseTypeDef:
        """
        Describes an AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_app)
        """

    def describe_app_assessment(
        self, *, assessmentArn: str
    ) -> DescribeAppAssessmentResponseTypeDef:
        """
        Describes an assessment for an AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_app_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_app_assessment)
        """

    def describe_app_version_resources_resolution_status(
        self, *, appArn: str, appVersion: str, resolutionId: str = ...
    ) -> DescribeAppVersionResourcesResolutionStatusResponseTypeDef:
        """
        Returns the resolution status for the specified resolution identifier for an
        application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_app_version_resources_resolution_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_app_version_resources_resolution_status)
        """

    def describe_app_version_template(
        self, *, appArn: str, appVersion: str
    ) -> DescribeAppVersionTemplateResponseTypeDef:
        """
        Describes details about an AWS Resilience Hub See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/resiliencehub-2020-04-30/DescribeAppVersionTemplate).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_app_version_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_app_version_template)
        """

    def describe_draft_app_version_resources_import_status(
        self, *, appArn: str
    ) -> DescribeDraftAppVersionResourcesImportStatusResponseTypeDef:
        """
        Describes the status of importing resources to an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_draft_app_version_resources_import_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_draft_app_version_resources_import_status)
        """

    def describe_resiliency_policy(
        self, *, policyArn: str
    ) -> DescribeResiliencyPolicyResponseTypeDef:
        """
        Describes a specified resiliency policy for an AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.describe_resiliency_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#describe_resiliency_policy)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#generate_presigned_url)
        """

    def import_resources_to_draft_app_version(
        self,
        *,
        appArn: str,
        sourceArns: Sequence[str] = ...,
        terraformSources: Sequence[TerraformSourceTypeDef] = ...
    ) -> ImportResourcesToDraftAppVersionResponseTypeDef:
        """
        Imports resources from sources such as a CloudFormation stack, resource-groups,
        or application registry app to a draft application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.import_resources_to_draft_app_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#import_resources_to_draft_app_version)
        """

    def list_alarm_recommendations(
        self, *, assessmentArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAlarmRecommendationsResponseTypeDef:
        """
        Lists the alarm recommendations for a AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_alarm_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_alarm_recommendations)
        """

    def list_app_assessments(
        self,
        *,
        appArn: str = ...,
        assessmentName: str = ...,
        assessmentStatus: Sequence[AssessmentStatusType] = ...,
        complianceStatus: ComplianceStatusType = ...,
        invoker: AssessmentInvokerType = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        reverseOrder: bool = ...
    ) -> ListAppAssessmentsResponseTypeDef:
        """
        Lists the assessments for an AWS Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_assessments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_assessments)
        """

    def list_app_component_compliances(
        self, *, assessmentArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAppComponentCompliancesResponseTypeDef:
        """
        Lists the compliances for an AWS Resilience Hub component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_component_compliances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_component_compliances)
        """

    def list_app_component_recommendations(
        self, *, assessmentArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAppComponentRecommendationsResponseTypeDef:
        """
        Lists the recommendations for an AWS Resilience Hub component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_component_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_component_recommendations)
        """

    def list_app_version_resource_mappings(
        self, *, appArn: str, appVersion: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAppVersionResourceMappingsResponseTypeDef:
        """
        Lists how the resources in an application version are mapped/sourced from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_version_resource_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_version_resource_mappings)
        """

    def list_app_version_resources(
        self,
        *,
        appArn: str,
        appVersion: str,
        maxResults: int = ...,
        nextToken: str = ...,
        resolutionId: str = ...
    ) -> ListAppVersionResourcesResponseTypeDef:
        """
        Lists all the resources in an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_version_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_version_resources)
        """

    def list_app_versions(
        self, *, appArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAppVersionsResponseTypeDef:
        """
        Lists the different versions for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_app_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_app_versions)
        """

    def list_apps(
        self, *, appArn: str = ..., maxResults: int = ..., name: str = ..., nextToken: str = ...
    ) -> ListAppsResponseTypeDef:
        """
        Lists your Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_apps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_apps)
        """

    def list_recommendation_templates(
        self,
        *,
        assessmentArn: str,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
        recommendationTemplateArn: str = ...,
        reverseOrder: bool = ...,
        status: Sequence[RecommendationTemplateStatusType] = ...
    ) -> ListRecommendationTemplatesResponseTypeDef:
        """
        Lists the recommendation templates for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_recommendation_templates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_recommendation_templates)
        """

    def list_resiliency_policies(
        self, *, maxResults: int = ..., nextToken: str = ..., policyName: str = ...
    ) -> ListResiliencyPoliciesResponseTypeDef:
        """
        Lists the resiliency policies for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_resiliency_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_resiliency_policies)
        """

    def list_sop_recommendations(
        self, *, assessmentArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListSopRecommendationsResponseTypeDef:
        """
        Lists the standard operating procedure (SOP) recommendations for the Resilience
        Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_sop_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_sop_recommendations)
        """

    def list_suggested_resiliency_policies(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSuggestedResiliencyPoliciesResponseTypeDef:
        """
        Lists the suggested resiliency policies for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_suggested_resiliency_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_suggested_resiliency_policies)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for your resources in your Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_tags_for_resource)
        """

    def list_test_recommendations(
        self, *, assessmentArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTestRecommendationsResponseTypeDef:
        """
        Lists the test recommendations for the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_test_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_test_recommendations)
        """

    def list_unsupported_app_version_resources(
        self,
        *,
        appArn: str,
        appVersion: str,
        maxResults: int = ...,
        nextToken: str = ...,
        resolutionId: str = ...
    ) -> ListUnsupportedAppVersionResourcesResponseTypeDef:
        """
        Lists the resources that are not currently supported in AWS Resilience Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.list_unsupported_app_version_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#list_unsupported_app_version_resources)
        """

    def publish_app_version(self, *, appArn: str) -> PublishAppVersionResponseTypeDef:
        """
        Publishes a new version of a specific Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.publish_app_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#publish_app_version)
        """

    def put_draft_app_version_template(
        self, *, appArn: str, appTemplateBody: str
    ) -> PutDraftAppVersionTemplateResponseTypeDef:
        """
        Adds or updates the app template for a draft version of a Resilience Hub app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.put_draft_app_version_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#put_draft_app_version_template)
        """

    def remove_draft_app_version_resource_mappings(
        self,
        *,
        appArn: str,
        appRegistryAppNames: Sequence[str] = ...,
        logicalStackNames: Sequence[str] = ...,
        resourceGroupNames: Sequence[str] = ...,
        resourceNames: Sequence[str] = ...,
        terraformSourceNames: Sequence[str] = ...
    ) -> RemoveDraftAppVersionResourceMappingsResponseTypeDef:
        """
        Removes resource mappings from a draft application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.remove_draft_app_version_resource_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#remove_draft_app_version_resource_mappings)
        """

    def resolve_app_version_resources(
        self, *, appArn: str, appVersion: str
    ) -> ResolveAppVersionResourcesResponseTypeDef:
        """
        Resolves the resources for an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.resolve_app_version_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#resolve_app_version_resources)
        """

    def start_app_assessment(
        self,
        *,
        appArn: str,
        appVersion: str,
        assessmentName: str,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> StartAppAssessmentResponseTypeDef:
        """
        Creates a new application assessment for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.start_app_assessment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#start_app_assessment)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#untag_resource)
        """

    def update_app(
        self,
        *,
        appArn: str,
        assessmentSchedule: AppAssessmentScheduleTypeType = ...,
        clearResiliencyPolicyArn: bool = ...,
        description: str = ...,
        policyArn: str = ...
    ) -> UpdateAppResponseTypeDef:
        """
        Updates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.update_app)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#update_app)
        """

    def update_resiliency_policy(
        self,
        *,
        policyArn: str,
        dataLocationConstraint: DataLocationConstraintType = ...,
        policy: Mapping[DisruptionTypeType, FailurePolicyTypeDef] = ...,
        policyDescription: str = ...,
        policyName: str = ...,
        tier: ResiliencyPolicyTierType = ...
    ) -> UpdateResiliencyPolicyResponseTypeDef:
        """
        Updates a resiliency policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client.update_resiliency_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/client/#update_resiliency_policy)
        """
