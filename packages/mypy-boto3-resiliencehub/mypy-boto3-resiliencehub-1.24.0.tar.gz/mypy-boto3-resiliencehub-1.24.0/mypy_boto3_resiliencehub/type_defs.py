"""
Type annotations for resiliencehub service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/type_defs/)

Usage::

    ```python
    from mypy_boto3_resiliencehub.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AlarmTypeType,
    AppAssessmentScheduleTypeType,
    AppComplianceStatusTypeType,
    AppStatusTypeType,
    AssessmentInvokerType,
    AssessmentStatusType,
    ComplianceStatusType,
    ConfigRecommendationOptimizationTypeType,
    CostFrequencyType,
    DataLocationConstraintType,
    DisruptionTypeType,
    EstimatedCostTierType,
    HaArchitectureType,
    PhysicalIdentifierTypeType,
    RecommendationComplianceStatusType,
    RecommendationTemplateStatusType,
    RenderRecommendationTypeType,
    ResiliencyPolicyTierType,
    ResourceImportStatusTypeType,
    ResourceMappingTypeType,
    ResourceResolutionStatusTypeType,
    TemplateFormatType,
    TestRiskType,
    TestTypeType,
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
    "ResponseMetadataTypeDef",
    "RecommendationItemTypeDef",
    "CostTypeDef",
    "DisruptionComplianceTypeDef",
    "ResiliencyScoreTypeDef",
    "AppComponentTypeDef",
    "AppSummaryTypeDef",
    "AppTypeDef",
    "AppVersionSummaryTypeDef",
    "RecommendationDisruptionComplianceTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateRecommendationTemplateRequestRequestTypeDef",
    "FailurePolicyTypeDef",
    "DeleteAppAssessmentRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteRecommendationTemplateRequestRequestTypeDef",
    "DeleteResiliencyPolicyRequestRequestTypeDef",
    "DescribeAppAssessmentRequestRequestTypeDef",
    "DescribeAppRequestRequestTypeDef",
    "DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef",
    "DescribeAppVersionTemplateRequestRequestTypeDef",
    "DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef",
    "DescribeResiliencyPolicyRequestRequestTypeDef",
    "TerraformSourceTypeDef",
    "ListAlarmRecommendationsRequestRequestTypeDef",
    "ListAppAssessmentsRequestRequestTypeDef",
    "ListAppComponentCompliancesRequestRequestTypeDef",
    "ListAppComponentRecommendationsRequestRequestTypeDef",
    "ListAppVersionResourceMappingsRequestRequestTypeDef",
    "ListAppVersionResourcesRequestRequestTypeDef",
    "ListAppVersionsRequestRequestTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListRecommendationTemplatesRequestRequestTypeDef",
    "ListResiliencyPoliciesRequestRequestTypeDef",
    "ListSopRecommendationsRequestRequestTypeDef",
    "ListSuggestedResiliencyPoliciesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTestRecommendationsRequestRequestTypeDef",
    "ListUnsupportedAppVersionResourcesRequestRequestTypeDef",
    "LogicalResourceIdTypeDef",
    "PhysicalResourceIdTypeDef",
    "PublishAppVersionRequestRequestTypeDef",
    "PutDraftAppVersionTemplateRequestRequestTypeDef",
    "S3LocationTypeDef",
    "RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef",
    "ResolveAppVersionResourcesRequestRequestTypeDef",
    "ResourceErrorTypeDef",
    "StartAppAssessmentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "DeleteAppAssessmentResponseTypeDef",
    "DeleteAppResponseTypeDef",
    "DeleteRecommendationTemplateResponseTypeDef",
    "DeleteResiliencyPolicyResponseTypeDef",
    "DescribeAppVersionResourcesResolutionStatusResponseTypeDef",
    "DescribeAppVersionTemplateResponseTypeDef",
    "DescribeDraftAppVersionResourcesImportStatusResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PublishAppVersionResponseTypeDef",
    "PutDraftAppVersionTemplateResponseTypeDef",
    "RemoveDraftAppVersionResourceMappingsResponseTypeDef",
    "ResolveAppVersionResourcesResponseTypeDef",
    "AlarmRecommendationTypeDef",
    "SopRecommendationTypeDef",
    "TestRecommendationTypeDef",
    "AppAssessmentSummaryTypeDef",
    "AppComponentComplianceTypeDef",
    "ListAppsResponseTypeDef",
    "CreateAppResponseTypeDef",
    "DescribeAppResponseTypeDef",
    "UpdateAppResponseTypeDef",
    "ListAppVersionsResponseTypeDef",
    "ConfigRecommendationTypeDef",
    "CreateResiliencyPolicyRequestRequestTypeDef",
    "ResiliencyPolicyTypeDef",
    "UpdateResiliencyPolicyRequestRequestTypeDef",
    "ImportResourcesToDraftAppVersionRequestRequestTypeDef",
    "ImportResourcesToDraftAppVersionResponseTypeDef",
    "PhysicalResourceTypeDef",
    "ResourceMappingTypeDef",
    "UnsupportedResourceTypeDef",
    "RecommendationTemplateTypeDef",
    "ResourceErrorsDetailsTypeDef",
    "ListAlarmRecommendationsResponseTypeDef",
    "ListSopRecommendationsResponseTypeDef",
    "ListTestRecommendationsResponseTypeDef",
    "ListAppAssessmentsResponseTypeDef",
    "ListAppComponentCompliancesResponseTypeDef",
    "ComponentRecommendationTypeDef",
    "CreateResiliencyPolicyResponseTypeDef",
    "DescribeResiliencyPolicyResponseTypeDef",
    "ListResiliencyPoliciesResponseTypeDef",
    "ListSuggestedResiliencyPoliciesResponseTypeDef",
    "UpdateResiliencyPolicyResponseTypeDef",
    "ListAppVersionResourcesResponseTypeDef",
    "AddDraftAppVersionResourceMappingsRequestRequestTypeDef",
    "AddDraftAppVersionResourceMappingsResponseTypeDef",
    "ListAppVersionResourceMappingsResponseTypeDef",
    "ListUnsupportedAppVersionResourcesResponseTypeDef",
    "CreateRecommendationTemplateResponseTypeDef",
    "ListRecommendationTemplatesResponseTypeDef",
    "AppAssessmentTypeDef",
    "ListAppComponentRecommendationsResponseTypeDef",
    "DescribeAppAssessmentResponseTypeDef",
    "StartAppAssessmentResponseTypeDef",
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

RecommendationItemTypeDef = TypedDict(
    "RecommendationItemTypeDef",
    {
        "alreadyImplemented": bool,
        "resourceId": str,
        "targetAccountId": str,
        "targetRegion": str,
    },
    total=False,
)

CostTypeDef = TypedDict(
    "CostTypeDef",
    {
        "amount": float,
        "currency": str,
        "frequency": CostFrequencyType,
    },
)

_RequiredDisruptionComplianceTypeDef = TypedDict(
    "_RequiredDisruptionComplianceTypeDef",
    {
        "complianceStatus": ComplianceStatusType,
    },
)
_OptionalDisruptionComplianceTypeDef = TypedDict(
    "_OptionalDisruptionComplianceTypeDef",
    {
        "achievableRpoInSecs": int,
        "achievableRtoInSecs": int,
        "currentRpoInSecs": int,
        "currentRtoInSecs": int,
        "message": str,
        "rpoDescription": str,
        "rpoReferenceId": str,
        "rtoDescription": str,
        "rtoReferenceId": str,
    },
    total=False,
)


class DisruptionComplianceTypeDef(
    _RequiredDisruptionComplianceTypeDef, _OptionalDisruptionComplianceTypeDef
):
    pass


ResiliencyScoreTypeDef = TypedDict(
    "ResiliencyScoreTypeDef",
    {
        "disruptionScore": Dict[DisruptionTypeType, float],
        "score": float,
    },
)

AppComponentTypeDef = TypedDict(
    "AppComponentTypeDef",
    {
        "name": str,
        "type": str,
    },
)

_RequiredAppSummaryTypeDef = TypedDict(
    "_RequiredAppSummaryTypeDef",
    {
        "appArn": str,
        "creationTime": datetime,
        "name": str,
    },
)
_OptionalAppSummaryTypeDef = TypedDict(
    "_OptionalAppSummaryTypeDef",
    {
        "assessmentSchedule": AppAssessmentScheduleTypeType,
        "complianceStatus": AppComplianceStatusTypeType,
        "description": str,
        "resiliencyScore": float,
    },
    total=False,
)


class AppSummaryTypeDef(_RequiredAppSummaryTypeDef, _OptionalAppSummaryTypeDef):
    pass


_RequiredAppTypeDef = TypedDict(
    "_RequiredAppTypeDef",
    {
        "appArn": str,
        "creationTime": datetime,
        "name": str,
    },
)
_OptionalAppTypeDef = TypedDict(
    "_OptionalAppTypeDef",
    {
        "assessmentSchedule": AppAssessmentScheduleTypeType,
        "complianceStatus": AppComplianceStatusTypeType,
        "description": str,
        "lastAppComplianceEvaluationTime": datetime,
        "lastResiliencyScoreEvaluationTime": datetime,
        "policyArn": str,
        "resiliencyScore": float,
        "status": AppStatusTypeType,
        "tags": Dict[str, str],
    },
    total=False,
)


class AppTypeDef(_RequiredAppTypeDef, _OptionalAppTypeDef):
    pass


AppVersionSummaryTypeDef = TypedDict(
    "AppVersionSummaryTypeDef",
    {
        "appVersion": str,
    },
)

_RequiredRecommendationDisruptionComplianceTypeDef = TypedDict(
    "_RequiredRecommendationDisruptionComplianceTypeDef",
    {
        "expectedComplianceStatus": ComplianceStatusType,
    },
)
_OptionalRecommendationDisruptionComplianceTypeDef = TypedDict(
    "_OptionalRecommendationDisruptionComplianceTypeDef",
    {
        "expectedRpoDescription": str,
        "expectedRpoInSecs": int,
        "expectedRtoDescription": str,
        "expectedRtoInSecs": int,
    },
    total=False,
)


class RecommendationDisruptionComplianceTypeDef(
    _RequiredRecommendationDisruptionComplianceTypeDef,
    _OptionalRecommendationDisruptionComplianceTypeDef,
):
    pass


_RequiredCreateAppRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateAppRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppRequestRequestTypeDef",
    {
        "assessmentSchedule": AppAssessmentScheduleTypeType,
        "clientToken": str,
        "description": str,
        "policyArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAppRequestRequestTypeDef(
    _RequiredCreateAppRequestRequestTypeDef, _OptionalCreateAppRequestRequestTypeDef
):
    pass


_RequiredCreateRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRecommendationTemplateRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "name": str,
    },
)
_OptionalCreateRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRecommendationTemplateRequestRequestTypeDef",
    {
        "bucketName": str,
        "clientToken": str,
        "format": TemplateFormatType,
        "recommendationIds": Sequence[str],
        "recommendationTypes": Sequence[RenderRecommendationTypeType],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateRecommendationTemplateRequestRequestTypeDef(
    _RequiredCreateRecommendationTemplateRequestRequestTypeDef,
    _OptionalCreateRecommendationTemplateRequestRequestTypeDef,
):
    pass


FailurePolicyTypeDef = TypedDict(
    "FailurePolicyTypeDef",
    {
        "rpoInSecs": int,
        "rtoInSecs": int,
    },
)

_RequiredDeleteAppAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAppAssessmentRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalDeleteAppAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAppAssessmentRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAppAssessmentRequestRequestTypeDef(
    _RequiredDeleteAppAssessmentRequestRequestTypeDef,
    _OptionalDeleteAppAssessmentRequestRequestTypeDef,
):
    pass


_RequiredDeleteAppRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAppRequestRequestTypeDef",
    {
        "appArn": str,
    },
)
_OptionalDeleteAppRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAppRequestRequestTypeDef",
    {
        "clientToken": str,
        "forceDelete": bool,
    },
    total=False,
)


class DeleteAppRequestRequestTypeDef(
    _RequiredDeleteAppRequestRequestTypeDef, _OptionalDeleteAppRequestRequestTypeDef
):
    pass


_RequiredDeleteRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRecommendationTemplateRequestRequestTypeDef",
    {
        "recommendationTemplateArn": str,
    },
)
_OptionalDeleteRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRecommendationTemplateRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteRecommendationTemplateRequestRequestTypeDef(
    _RequiredDeleteRecommendationTemplateRequestRequestTypeDef,
    _OptionalDeleteRecommendationTemplateRequestRequestTypeDef,
):
    pass


_RequiredDeleteResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
    },
)
_OptionalDeleteResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResiliencyPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteResiliencyPolicyRequestRequestTypeDef(
    _RequiredDeleteResiliencyPolicyRequestRequestTypeDef,
    _OptionalDeleteResiliencyPolicyRequestRequestTypeDef,
):
    pass


DescribeAppAssessmentRequestRequestTypeDef = TypedDict(
    "DescribeAppAssessmentRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)

DescribeAppRequestRequestTypeDef = TypedDict(
    "DescribeAppRequestRequestTypeDef",
    {
        "appArn": str,
    },
)

_RequiredDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)
_OptionalDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef",
    {
        "resolutionId": str,
    },
    total=False,
)


class DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef(
    _RequiredDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef,
    _OptionalDescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef,
):
    pass


DescribeAppVersionTemplateRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionTemplateRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)

DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef = TypedDict(
    "DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef",
    {
        "appArn": str,
    },
)

DescribeResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "DescribeResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
    },
)

TerraformSourceTypeDef = TypedDict(
    "TerraformSourceTypeDef",
    {
        "s3StateFileUrl": str,
    },
)

_RequiredListAlarmRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListAlarmRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListAlarmRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListAlarmRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAlarmRecommendationsRequestRequestTypeDef(
    _RequiredListAlarmRecommendationsRequestRequestTypeDef,
    _OptionalListAlarmRecommendationsRequestRequestTypeDef,
):
    pass


ListAppAssessmentsRequestRequestTypeDef = TypedDict(
    "ListAppAssessmentsRequestRequestTypeDef",
    {
        "appArn": str,
        "assessmentName": str,
        "assessmentStatus": Sequence[AssessmentStatusType],
        "complianceStatus": ComplianceStatusType,
        "invoker": AssessmentInvokerType,
        "maxResults": int,
        "nextToken": str,
        "reverseOrder": bool,
    },
    total=False,
)

_RequiredListAppComponentCompliancesRequestRequestTypeDef = TypedDict(
    "_RequiredListAppComponentCompliancesRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListAppComponentCompliancesRequestRequestTypeDef = TypedDict(
    "_OptionalListAppComponentCompliancesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAppComponentCompliancesRequestRequestTypeDef(
    _RequiredListAppComponentCompliancesRequestRequestTypeDef,
    _OptionalListAppComponentCompliancesRequestRequestTypeDef,
):
    pass


_RequiredListAppComponentRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppComponentRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListAppComponentRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppComponentRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAppComponentRecommendationsRequestRequestTypeDef(
    _RequiredListAppComponentRecommendationsRequestRequestTypeDef,
    _OptionalListAppComponentRecommendationsRequestRequestTypeDef,
):
    pass


_RequiredListAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)
_OptionalListAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAppVersionResourceMappingsRequestRequestTypeDef(
    _RequiredListAppVersionResourceMappingsRequestRequestTypeDef,
    _OptionalListAppVersionResourceMappingsRequestRequestTypeDef,
):
    pass


_RequiredListAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)
_OptionalListAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListAppVersionResourcesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "resolutionId": str,
    },
    total=False,
)


class ListAppVersionResourcesRequestRequestTypeDef(
    _RequiredListAppVersionResourcesRequestRequestTypeDef,
    _OptionalListAppVersionResourcesRequestRequestTypeDef,
):
    pass


_RequiredListAppVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppVersionsRequestRequestTypeDef",
    {
        "appArn": str,
    },
)
_OptionalListAppVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppVersionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAppVersionsRequestRequestTypeDef(
    _RequiredListAppVersionsRequestRequestTypeDef, _OptionalListAppVersionsRequestRequestTypeDef
):
    pass


ListAppsRequestRequestTypeDef = TypedDict(
    "ListAppsRequestRequestTypeDef",
    {
        "appArn": str,
        "maxResults": int,
        "name": str,
        "nextToken": str,
    },
    total=False,
)

_RequiredListRecommendationTemplatesRequestRequestTypeDef = TypedDict(
    "_RequiredListRecommendationTemplatesRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListRecommendationTemplatesRequestRequestTypeDef = TypedDict(
    "_OptionalListRecommendationTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "name": str,
        "nextToken": str,
        "recommendationTemplateArn": str,
        "reverseOrder": bool,
        "status": Sequence[RecommendationTemplateStatusType],
    },
    total=False,
)


class ListRecommendationTemplatesRequestRequestTypeDef(
    _RequiredListRecommendationTemplatesRequestRequestTypeDef,
    _OptionalListRecommendationTemplatesRequestRequestTypeDef,
):
    pass


ListResiliencyPoliciesRequestRequestTypeDef = TypedDict(
    "ListResiliencyPoliciesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "policyName": str,
    },
    total=False,
)

_RequiredListSopRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListSopRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListSopRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListSopRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListSopRecommendationsRequestRequestTypeDef(
    _RequiredListSopRecommendationsRequestRequestTypeDef,
    _OptionalListSopRecommendationsRequestRequestTypeDef,
):
    pass


ListSuggestedResiliencyPoliciesRequestRequestTypeDef = TypedDict(
    "ListSuggestedResiliencyPoliciesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredListTestRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)
_OptionalListTestRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTestRecommendationsRequestRequestTypeDef(
    _RequiredListTestRecommendationsRequestRequestTypeDef,
    _OptionalListTestRecommendationsRequestRequestTypeDef,
):
    pass


_RequiredListUnsupportedAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListUnsupportedAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)
_OptionalListUnsupportedAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListUnsupportedAppVersionResourcesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "resolutionId": str,
    },
    total=False,
)


class ListUnsupportedAppVersionResourcesRequestRequestTypeDef(
    _RequiredListUnsupportedAppVersionResourcesRequestRequestTypeDef,
    _OptionalListUnsupportedAppVersionResourcesRequestRequestTypeDef,
):
    pass


_RequiredLogicalResourceIdTypeDef = TypedDict(
    "_RequiredLogicalResourceIdTypeDef",
    {
        "identifier": str,
    },
)
_OptionalLogicalResourceIdTypeDef = TypedDict(
    "_OptionalLogicalResourceIdTypeDef",
    {
        "logicalStackName": str,
        "resourceGroupName": str,
        "terraformSourceName": str,
    },
    total=False,
)


class LogicalResourceIdTypeDef(
    _RequiredLogicalResourceIdTypeDef, _OptionalLogicalResourceIdTypeDef
):
    pass


_RequiredPhysicalResourceIdTypeDef = TypedDict(
    "_RequiredPhysicalResourceIdTypeDef",
    {
        "identifier": str,
        "type": PhysicalIdentifierTypeType,
    },
)
_OptionalPhysicalResourceIdTypeDef = TypedDict(
    "_OptionalPhysicalResourceIdTypeDef",
    {
        "awsAccountId": str,
        "awsRegion": str,
    },
    total=False,
)


class PhysicalResourceIdTypeDef(
    _RequiredPhysicalResourceIdTypeDef, _OptionalPhysicalResourceIdTypeDef
):
    pass


PublishAppVersionRequestRequestTypeDef = TypedDict(
    "PublishAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
    },
)

PutDraftAppVersionTemplateRequestRequestTypeDef = TypedDict(
    "PutDraftAppVersionTemplateRequestRequestTypeDef",
    {
        "appArn": str,
        "appTemplateBody": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": str,
        "prefix": str,
    },
    total=False,
)

_RequiredRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
    },
)
_OptionalRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appRegistryAppNames": Sequence[str],
        "logicalStackNames": Sequence[str],
        "resourceGroupNames": Sequence[str],
        "resourceNames": Sequence[str],
        "terraformSourceNames": Sequence[str],
    },
    total=False,
)


class RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef(
    _RequiredRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef,
    _OptionalRemoveDraftAppVersionResourceMappingsRequestRequestTypeDef,
):
    pass


ResolveAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "ResolveAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)

ResourceErrorTypeDef = TypedDict(
    "ResourceErrorTypeDef",
    {
        "logicalResourceId": str,
        "physicalResourceId": str,
        "reason": str,
    },
    total=False,
)

_RequiredStartAppAssessmentRequestRequestTypeDef = TypedDict(
    "_RequiredStartAppAssessmentRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "assessmentName": str,
    },
)
_OptionalStartAppAssessmentRequestRequestTypeDef = TypedDict(
    "_OptionalStartAppAssessmentRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartAppAssessmentRequestRequestTypeDef(
    _RequiredStartAppAssessmentRequestRequestTypeDef,
    _OptionalStartAppAssessmentRequestRequestTypeDef,
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAppRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppRequestRequestTypeDef",
    {
        "appArn": str,
    },
)
_OptionalUpdateAppRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppRequestRequestTypeDef",
    {
        "assessmentSchedule": AppAssessmentScheduleTypeType,
        "clearResiliencyPolicyArn": bool,
        "description": str,
        "policyArn": str,
    },
    total=False,
)


class UpdateAppRequestRequestTypeDef(
    _RequiredUpdateAppRequestRequestTypeDef, _OptionalUpdateAppRequestRequestTypeDef
):
    pass


DeleteAppAssessmentResponseTypeDef = TypedDict(
    "DeleteAppAssessmentResponseTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppResponseTypeDef = TypedDict(
    "DeleteAppResponseTypeDef",
    {
        "appArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRecommendationTemplateResponseTypeDef = TypedDict(
    "DeleteRecommendationTemplateResponseTypeDef",
    {
        "recommendationTemplateArn": str,
        "status": RecommendationTemplateStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResiliencyPolicyResponseTypeDef = TypedDict(
    "DeleteResiliencyPolicyResponseTypeDef",
    {
        "policyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionResourcesResolutionStatusResponseTypeDef = TypedDict(
    "DescribeAppVersionResourcesResolutionStatusResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "errorMessage": str,
        "resolutionId": str,
        "status": ResourceResolutionStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionTemplateResponseTypeDef = TypedDict(
    "DescribeAppVersionTemplateResponseTypeDef",
    {
        "appArn": str,
        "appTemplateBody": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDraftAppVersionResourcesImportStatusResponseTypeDef = TypedDict(
    "DescribeDraftAppVersionResourcesImportStatusResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "errorMessage": str,
        "status": ResourceImportStatusTypeType,
        "statusChangeTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishAppVersionResponseTypeDef = TypedDict(
    "PublishAppVersionResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDraftAppVersionTemplateResponseTypeDef = TypedDict(
    "PutDraftAppVersionTemplateResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveDraftAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "RemoveDraftAppVersionResourceMappingsResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResolveAppVersionResourcesResponseTypeDef = TypedDict(
    "ResolveAppVersionResourcesResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "resolutionId": str,
        "status": ResourceResolutionStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAlarmRecommendationTypeDef = TypedDict(
    "_RequiredAlarmRecommendationTypeDef",
    {
        "name": str,
        "recommendationId": str,
        "referenceId": str,
        "type": AlarmTypeType,
    },
)
_OptionalAlarmRecommendationTypeDef = TypedDict(
    "_OptionalAlarmRecommendationTypeDef",
    {
        "appComponentName": str,
        "description": str,
        "items": List[RecommendationItemTypeDef],
        "prerequisite": str,
    },
    total=False,
)


class AlarmRecommendationTypeDef(
    _RequiredAlarmRecommendationTypeDef, _OptionalAlarmRecommendationTypeDef
):
    pass


_RequiredSopRecommendationTypeDef = TypedDict(
    "_RequiredSopRecommendationTypeDef",
    {
        "recommendationId": str,
        "referenceId": str,
        "serviceType": Literal["SSM"],
    },
)
_OptionalSopRecommendationTypeDef = TypedDict(
    "_OptionalSopRecommendationTypeDef",
    {
        "appComponentName": str,
        "description": str,
        "items": List[RecommendationItemTypeDef],
        "name": str,
        "prerequisite": str,
    },
    total=False,
)


class SopRecommendationTypeDef(
    _RequiredSopRecommendationTypeDef, _OptionalSopRecommendationTypeDef
):
    pass


_RequiredTestRecommendationTypeDef = TypedDict(
    "_RequiredTestRecommendationTypeDef",
    {
        "referenceId": str,
    },
)
_OptionalTestRecommendationTypeDef = TypedDict(
    "_OptionalTestRecommendationTypeDef",
    {
        "appComponentName": str,
        "dependsOnAlarms": List[str],
        "description": str,
        "intent": str,
        "items": List[RecommendationItemTypeDef],
        "name": str,
        "prerequisite": str,
        "recommendationId": str,
        "risk": TestRiskType,
        "type": TestTypeType,
    },
    total=False,
)


class TestRecommendationTypeDef(
    _RequiredTestRecommendationTypeDef, _OptionalTestRecommendationTypeDef
):
    pass


_RequiredAppAssessmentSummaryTypeDef = TypedDict(
    "_RequiredAppAssessmentSummaryTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
    },
)
_OptionalAppAssessmentSummaryTypeDef = TypedDict(
    "_OptionalAppAssessmentSummaryTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "assessmentName": str,
        "complianceStatus": ComplianceStatusType,
        "cost": CostTypeDef,
        "endTime": datetime,
        "invoker": AssessmentInvokerType,
        "message": str,
        "resiliencyScore": float,
        "startTime": datetime,
    },
    total=False,
)


class AppAssessmentSummaryTypeDef(
    _RequiredAppAssessmentSummaryTypeDef, _OptionalAppAssessmentSummaryTypeDef
):
    pass


AppComponentComplianceTypeDef = TypedDict(
    "AppComponentComplianceTypeDef",
    {
        "appComponentName": str,
        "compliance": Dict[DisruptionTypeType, DisruptionComplianceTypeDef],
        "cost": CostTypeDef,
        "message": str,
        "resiliencyScore": ResiliencyScoreTypeDef,
        "status": ComplianceStatusType,
    },
    total=False,
)

ListAppsResponseTypeDef = TypedDict(
    "ListAppsResponseTypeDef",
    {
        "appSummaries": List[AppSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppResponseTypeDef = TypedDict(
    "CreateAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppResponseTypeDef = TypedDict(
    "DescribeAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppResponseTypeDef = TypedDict(
    "UpdateAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionsResponseTypeDef = TypedDict(
    "ListAppVersionsResponseTypeDef",
    {
        "appVersions": List[AppVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredConfigRecommendationTypeDef = TypedDict(
    "_RequiredConfigRecommendationTypeDef",
    {
        "name": str,
        "optimizationType": ConfigRecommendationOptimizationTypeType,
        "referenceId": str,
    },
)
_OptionalConfigRecommendationTypeDef = TypedDict(
    "_OptionalConfigRecommendationTypeDef",
    {
        "appComponentName": str,
        "compliance": Dict[DisruptionTypeType, DisruptionComplianceTypeDef],
        "cost": CostTypeDef,
        "description": str,
        "haArchitecture": HaArchitectureType,
        "recommendationCompliance": Dict[
            DisruptionTypeType, RecommendationDisruptionComplianceTypeDef
        ],
        "suggestedChanges": List[str],
    },
    total=False,
)


class ConfigRecommendationTypeDef(
    _RequiredConfigRecommendationTypeDef, _OptionalConfigRecommendationTypeDef
):
    pass


_RequiredCreateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResiliencyPolicyRequestRequestTypeDef",
    {
        "policy": Mapping[DisruptionTypeType, FailurePolicyTypeDef],
        "policyName": str,
        "tier": ResiliencyPolicyTierType,
    },
)
_OptionalCreateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResiliencyPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "dataLocationConstraint": DataLocationConstraintType,
        "policyDescription": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateResiliencyPolicyRequestRequestTypeDef(
    _RequiredCreateResiliencyPolicyRequestRequestTypeDef,
    _OptionalCreateResiliencyPolicyRequestRequestTypeDef,
):
    pass


ResiliencyPolicyTypeDef = TypedDict(
    "ResiliencyPolicyTypeDef",
    {
        "creationTime": datetime,
        "dataLocationConstraint": DataLocationConstraintType,
        "estimatedCostTier": EstimatedCostTierType,
        "policy": Dict[DisruptionTypeType, FailurePolicyTypeDef],
        "policyArn": str,
        "policyDescription": str,
        "policyName": str,
        "tags": Dict[str, str],
        "tier": ResiliencyPolicyTierType,
    },
    total=False,
)

_RequiredUpdateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
    },
)
_OptionalUpdateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResiliencyPolicyRequestRequestTypeDef",
    {
        "dataLocationConstraint": DataLocationConstraintType,
        "policy": Mapping[DisruptionTypeType, FailurePolicyTypeDef],
        "policyDescription": str,
        "policyName": str,
        "tier": ResiliencyPolicyTierType,
    },
    total=False,
)


class UpdateResiliencyPolicyRequestRequestTypeDef(
    _RequiredUpdateResiliencyPolicyRequestRequestTypeDef,
    _OptionalUpdateResiliencyPolicyRequestRequestTypeDef,
):
    pass


_RequiredImportResourcesToDraftAppVersionRequestRequestTypeDef = TypedDict(
    "_RequiredImportResourcesToDraftAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
    },
)
_OptionalImportResourcesToDraftAppVersionRequestRequestTypeDef = TypedDict(
    "_OptionalImportResourcesToDraftAppVersionRequestRequestTypeDef",
    {
        "sourceArns": Sequence[str],
        "terraformSources": Sequence[TerraformSourceTypeDef],
    },
    total=False,
)


class ImportResourcesToDraftAppVersionRequestRequestTypeDef(
    _RequiredImportResourcesToDraftAppVersionRequestRequestTypeDef,
    _OptionalImportResourcesToDraftAppVersionRequestRequestTypeDef,
):
    pass


ImportResourcesToDraftAppVersionResponseTypeDef = TypedDict(
    "ImportResourcesToDraftAppVersionResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "sourceArns": List[str],
        "status": ResourceImportStatusTypeType,
        "terraformSources": List[TerraformSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPhysicalResourceTypeDef = TypedDict(
    "_RequiredPhysicalResourceTypeDef",
    {
        "logicalResourceId": LogicalResourceIdTypeDef,
        "physicalResourceId": PhysicalResourceIdTypeDef,
        "resourceType": str,
    },
)
_OptionalPhysicalResourceTypeDef = TypedDict(
    "_OptionalPhysicalResourceTypeDef",
    {
        "appComponents": List[AppComponentTypeDef],
        "resourceName": str,
    },
    total=False,
)


class PhysicalResourceTypeDef(_RequiredPhysicalResourceTypeDef, _OptionalPhysicalResourceTypeDef):
    pass


_RequiredResourceMappingTypeDef = TypedDict(
    "_RequiredResourceMappingTypeDef",
    {
        "mappingType": ResourceMappingTypeType,
        "physicalResourceId": PhysicalResourceIdTypeDef,
    },
)
_OptionalResourceMappingTypeDef = TypedDict(
    "_OptionalResourceMappingTypeDef",
    {
        "appRegistryAppName": str,
        "logicalStackName": str,
        "resourceGroupName": str,
        "resourceName": str,
        "terraformSourceName": str,
    },
    total=False,
)


class ResourceMappingTypeDef(_RequiredResourceMappingTypeDef, _OptionalResourceMappingTypeDef):
    pass


UnsupportedResourceTypeDef = TypedDict(
    "UnsupportedResourceTypeDef",
    {
        "logicalResourceId": LogicalResourceIdTypeDef,
        "physicalResourceId": PhysicalResourceIdTypeDef,
        "resourceType": str,
    },
)

_RequiredRecommendationTemplateTypeDef = TypedDict(
    "_RequiredRecommendationTemplateTypeDef",
    {
        "assessmentArn": str,
        "format": TemplateFormatType,
        "name": str,
        "recommendationTemplateArn": str,
        "recommendationTypes": List[RenderRecommendationTypeType],
        "status": RecommendationTemplateStatusType,
    },
)
_OptionalRecommendationTemplateTypeDef = TypedDict(
    "_OptionalRecommendationTemplateTypeDef",
    {
        "appArn": str,
        "endTime": datetime,
        "message": str,
        "needsReplacements": bool,
        "recommendationIds": List[str],
        "startTime": datetime,
        "tags": Dict[str, str],
        "templatesLocation": S3LocationTypeDef,
    },
    total=False,
)


class RecommendationTemplateTypeDef(
    _RequiredRecommendationTemplateTypeDef, _OptionalRecommendationTemplateTypeDef
):
    pass


ResourceErrorsDetailsTypeDef = TypedDict(
    "ResourceErrorsDetailsTypeDef",
    {
        "hasMoreErrors": bool,
        "resourceErrors": List[ResourceErrorTypeDef],
    },
    total=False,
)

ListAlarmRecommendationsResponseTypeDef = TypedDict(
    "ListAlarmRecommendationsResponseTypeDef",
    {
        "alarmRecommendations": List[AlarmRecommendationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSopRecommendationsResponseTypeDef = TypedDict(
    "ListSopRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "sopRecommendations": List[SopRecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestRecommendationsResponseTypeDef = TypedDict(
    "ListTestRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "testRecommendations": List[TestRecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppAssessmentsResponseTypeDef = TypedDict(
    "ListAppAssessmentsResponseTypeDef",
    {
        "assessmentSummaries": List[AppAssessmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppComponentCompliancesResponseTypeDef = TypedDict(
    "ListAppComponentCompliancesResponseTypeDef",
    {
        "componentCompliances": List[AppComponentComplianceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComponentRecommendationTypeDef = TypedDict(
    "ComponentRecommendationTypeDef",
    {
        "appComponentName": str,
        "configRecommendations": List[ConfigRecommendationTypeDef],
        "recommendationStatus": RecommendationComplianceStatusType,
    },
)

CreateResiliencyPolicyResponseTypeDef = TypedDict(
    "CreateResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResiliencyPolicyResponseTypeDef = TypedDict(
    "DescribeResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResiliencyPoliciesResponseTypeDef = TypedDict(
    "ListResiliencyPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "resiliencyPolicies": List[ResiliencyPolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSuggestedResiliencyPoliciesResponseTypeDef = TypedDict(
    "ListSuggestedResiliencyPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "resiliencyPolicies": List[ResiliencyPolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResiliencyPolicyResponseTypeDef = TypedDict(
    "UpdateResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionResourcesResponseTypeDef = TypedDict(
    "ListAppVersionResourcesResponseTypeDef",
    {
        "nextToken": str,
        "physicalResources": List[PhysicalResourceTypeDef],
        "resolutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddDraftAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "AddDraftAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
        "resourceMappings": Sequence[ResourceMappingTypeDef],
    },
)

AddDraftAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "AddDraftAppVersionResourceMappingsResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "resourceMappings": List[ResourceMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "ListAppVersionResourceMappingsResponseTypeDef",
    {
        "nextToken": str,
        "resourceMappings": List[ResourceMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUnsupportedAppVersionResourcesResponseTypeDef = TypedDict(
    "ListUnsupportedAppVersionResourcesResponseTypeDef",
    {
        "nextToken": str,
        "resolutionId": str,
        "unsupportedResources": List[UnsupportedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecommendationTemplateResponseTypeDef = TypedDict(
    "CreateRecommendationTemplateResponseTypeDef",
    {
        "recommendationTemplate": RecommendationTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecommendationTemplatesResponseTypeDef = TypedDict(
    "ListRecommendationTemplatesResponseTypeDef",
    {
        "nextToken": str,
        "recommendationTemplates": List[RecommendationTemplateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAppAssessmentTypeDef = TypedDict(
    "_RequiredAppAssessmentTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
        "invoker": AssessmentInvokerType,
    },
)
_OptionalAppAssessmentTypeDef = TypedDict(
    "_OptionalAppAssessmentTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "assessmentName": str,
        "compliance": Dict[DisruptionTypeType, DisruptionComplianceTypeDef],
        "complianceStatus": ComplianceStatusType,
        "cost": CostTypeDef,
        "endTime": datetime,
        "message": str,
        "policy": ResiliencyPolicyTypeDef,
        "resiliencyScore": ResiliencyScoreTypeDef,
        "resourceErrorsDetails": ResourceErrorsDetailsTypeDef,
        "startTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)


class AppAssessmentTypeDef(_RequiredAppAssessmentTypeDef, _OptionalAppAssessmentTypeDef):
    pass


ListAppComponentRecommendationsResponseTypeDef = TypedDict(
    "ListAppComponentRecommendationsResponseTypeDef",
    {
        "componentRecommendations": List[ComponentRecommendationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppAssessmentResponseTypeDef = TypedDict(
    "DescribeAppAssessmentResponseTypeDef",
    {
        "assessment": AppAssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAppAssessmentResponseTypeDef = TypedDict(
    "StartAppAssessmentResponseTypeDef",
    {
        "assessment": AppAssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
