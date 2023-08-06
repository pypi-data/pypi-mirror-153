"""
Type annotations for accessanalyzer service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/type_defs/)

Usage::

    ```python
    from mypy_boto3_accessanalyzer.type_defs import AccessPreviewStatusReasonTypeDef

    data: AccessPreviewStatusReasonTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessPreviewStatusReasonCodeType,
    AccessPreviewStatusType,
    AclPermissionType,
    AnalyzerStatusType,
    FindingChangeTypeType,
    FindingSourceTypeType,
    FindingStatusType,
    FindingStatusUpdateType,
    JobErrorCodeType,
    JobStatusType,
    KmsGrantOperationType,
    LocaleType,
    OrderByType,
    PolicyTypeType,
    ReasonCodeType,
    ResourceTypeType,
    TypeType,
    ValidatePolicyFindingTypeType,
    ValidatePolicyResourceTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessPreviewStatusReasonTypeDef",
    "AclGranteeTypeDef",
    "AnalyzedResourceSummaryTypeDef",
    "AnalyzedResourceTypeDef",
    "StatusReasonTypeDef",
    "ApplyArchiveRuleRequestRequestTypeDef",
    "CriterionTypeDef",
    "CancelPolicyGenerationRequestRequestTypeDef",
    "TrailTypeDef",
    "TrailPropertiesTypeDef",
    "IamRoleConfigurationTypeDef",
    "SecretsManagerSecretConfigurationTypeDef",
    "SqsQueueConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteAnalyzerRequestRequestTypeDef",
    "DeleteArchiveRuleRequestRequestTypeDef",
    "FindingSourceDetailTypeDef",
    "GeneratedPolicyTypeDef",
    "GetAccessPreviewRequestRequestTypeDef",
    "GetAnalyzedResourceRequestRequestTypeDef",
    "GetAnalyzerRequestRequestTypeDef",
    "GetArchiveRuleRequestRequestTypeDef",
    "GetFindingRequestRequestTypeDef",
    "GetGeneratedPolicyRequestRequestTypeDef",
    "JobErrorTypeDef",
    "KmsGrantConstraintsTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccessPreviewsRequestRequestTypeDef",
    "ListAnalyzedResourcesRequestRequestTypeDef",
    "ListAnalyzersRequestRequestTypeDef",
    "ListArchiveRulesRequestRequestTypeDef",
    "SortCriteriaTypeDef",
    "ListPolicyGenerationsRequestRequestTypeDef",
    "PolicyGenerationTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "VpcConfigurationTypeDef",
    "SubstringTypeDef",
    "PolicyGenerationDetailsTypeDef",
    "PositionTypeDef",
    "S3PublicAccessBlockConfigurationTypeDef",
    "StartResourceScanRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFindingsRequestRequestTypeDef",
    "ValidatePolicyRequestRequestTypeDef",
    "AccessPreviewSummaryTypeDef",
    "S3BucketAclGrantConfigurationTypeDef",
    "AnalyzerSummaryTypeDef",
    "ArchiveRuleSummaryTypeDef",
    "CreateArchiveRuleRequestRequestTypeDef",
    "InlineArchiveRuleTypeDef",
    "ListAccessPreviewFindingsRequestRequestTypeDef",
    "UpdateArchiveRuleRequestRequestTypeDef",
    "CloudTrailDetailsTypeDef",
    "CloudTrailPropertiesTypeDef",
    "CreateAccessPreviewResponseTypeDef",
    "CreateAnalyzerResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAnalyzedResourceResponseTypeDef",
    "ListAnalyzedResourcesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartPolicyGenerationResponseTypeDef",
    "FindingSourceTypeDef",
    "JobDetailsTypeDef",
    "KmsGrantConfigurationTypeDef",
    "ListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef",
    "ListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef",
    "ListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef",
    "ListAnalyzersRequestListAnalyzersPaginateTypeDef",
    "ListArchiveRulesRequestListArchiveRulesPaginateTypeDef",
    "ListPolicyGenerationsRequestListPolicyGenerationsPaginateTypeDef",
    "ValidatePolicyRequestValidatePolicyPaginateTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "ListPolicyGenerationsResponseTypeDef",
    "NetworkOriginConfigurationTypeDef",
    "PathElementTypeDef",
    "SpanTypeDef",
    "ListAccessPreviewsResponseTypeDef",
    "GetAnalyzerResponseTypeDef",
    "ListAnalyzersResponseTypeDef",
    "GetArchiveRuleResponseTypeDef",
    "ListArchiveRulesResponseTypeDef",
    "CreateAnalyzerRequestRequestTypeDef",
    "StartPolicyGenerationRequestRequestTypeDef",
    "GeneratedPolicyPropertiesTypeDef",
    "AccessPreviewFindingTypeDef",
    "FindingSummaryTypeDef",
    "FindingTypeDef",
    "KmsKeyConfigurationTypeDef",
    "S3AccessPointConfigurationTypeDef",
    "LocationTypeDef",
    "GeneratedPolicyResultTypeDef",
    "ListAccessPreviewFindingsResponseTypeDef",
    "ListFindingsResponseTypeDef",
    "GetFindingResponseTypeDef",
    "S3BucketConfigurationTypeDef",
    "ValidatePolicyFindingTypeDef",
    "GetGeneratedPolicyResponseTypeDef",
    "ConfigurationTypeDef",
    "ValidatePolicyResponseTypeDef",
    "AccessPreviewTypeDef",
    "CreateAccessPreviewRequestRequestTypeDef",
    "GetAccessPreviewResponseTypeDef",
)

AccessPreviewStatusReasonTypeDef = TypedDict(
    "AccessPreviewStatusReasonTypeDef",
    {
        "code": AccessPreviewStatusReasonCodeType,
    },
)

AclGranteeTypeDef = TypedDict(
    "AclGranteeTypeDef",
    {
        "id": str,
        "uri": str,
    },
    total=False,
)

AnalyzedResourceSummaryTypeDef = TypedDict(
    "AnalyzedResourceSummaryTypeDef",
    {
        "resourceArn": str,
        "resourceOwnerAccount": str,
        "resourceType": ResourceTypeType,
    },
)

_RequiredAnalyzedResourceTypeDef = TypedDict(
    "_RequiredAnalyzedResourceTypeDef",
    {
        "analyzedAt": datetime,
        "createdAt": datetime,
        "isPublic": bool,
        "resourceArn": str,
        "resourceOwnerAccount": str,
        "resourceType": ResourceTypeType,
        "updatedAt": datetime,
    },
)
_OptionalAnalyzedResourceTypeDef = TypedDict(
    "_OptionalAnalyzedResourceTypeDef",
    {
        "actions": List[str],
        "error": str,
        "sharedVia": List[str],
        "status": FindingStatusType,
    },
    total=False,
)


class AnalyzedResourceTypeDef(_RequiredAnalyzedResourceTypeDef, _OptionalAnalyzedResourceTypeDef):
    pass


StatusReasonTypeDef = TypedDict(
    "StatusReasonTypeDef",
    {
        "code": ReasonCodeType,
    },
)

_RequiredApplyArchiveRuleRequestRequestTypeDef = TypedDict(
    "_RequiredApplyArchiveRuleRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "ruleName": str,
    },
)
_OptionalApplyArchiveRuleRequestRequestTypeDef = TypedDict(
    "_OptionalApplyArchiveRuleRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class ApplyArchiveRuleRequestRequestTypeDef(
    _RequiredApplyArchiveRuleRequestRequestTypeDef, _OptionalApplyArchiveRuleRequestRequestTypeDef
):
    pass


CriterionTypeDef = TypedDict(
    "CriterionTypeDef",
    {
        "contains": Sequence[str],
        "eq": Sequence[str],
        "exists": bool,
        "neq": Sequence[str],
    },
    total=False,
)

CancelPolicyGenerationRequestRequestTypeDef = TypedDict(
    "CancelPolicyGenerationRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

_RequiredTrailTypeDef = TypedDict(
    "_RequiredTrailTypeDef",
    {
        "cloudTrailArn": str,
    },
)
_OptionalTrailTypeDef = TypedDict(
    "_OptionalTrailTypeDef",
    {
        "allRegions": bool,
        "regions": Sequence[str],
    },
    total=False,
)


class TrailTypeDef(_RequiredTrailTypeDef, _OptionalTrailTypeDef):
    pass


_RequiredTrailPropertiesTypeDef = TypedDict(
    "_RequiredTrailPropertiesTypeDef",
    {
        "cloudTrailArn": str,
    },
)
_OptionalTrailPropertiesTypeDef = TypedDict(
    "_OptionalTrailPropertiesTypeDef",
    {
        "allRegions": bool,
        "regions": List[str],
    },
    total=False,
)


class TrailPropertiesTypeDef(_RequiredTrailPropertiesTypeDef, _OptionalTrailPropertiesTypeDef):
    pass


IamRoleConfigurationTypeDef = TypedDict(
    "IamRoleConfigurationTypeDef",
    {
        "trustPolicy": str,
    },
    total=False,
)

SecretsManagerSecretConfigurationTypeDef = TypedDict(
    "SecretsManagerSecretConfigurationTypeDef",
    {
        "kmsKeyId": str,
        "secretPolicy": str,
    },
    total=False,
)

SqsQueueConfigurationTypeDef = TypedDict(
    "SqsQueueConfigurationTypeDef",
    {
        "queuePolicy": str,
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

_RequiredDeleteAnalyzerRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAnalyzerRequestRequestTypeDef",
    {
        "analyzerName": str,
    },
)
_OptionalDeleteAnalyzerRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAnalyzerRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAnalyzerRequestRequestTypeDef(
    _RequiredDeleteAnalyzerRequestRequestTypeDef, _OptionalDeleteAnalyzerRequestRequestTypeDef
):
    pass


_RequiredDeleteArchiveRuleRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteArchiveRuleRequestRequestTypeDef",
    {
        "analyzerName": str,
        "ruleName": str,
    },
)
_OptionalDeleteArchiveRuleRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteArchiveRuleRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteArchiveRuleRequestRequestTypeDef(
    _RequiredDeleteArchiveRuleRequestRequestTypeDef, _OptionalDeleteArchiveRuleRequestRequestTypeDef
):
    pass


FindingSourceDetailTypeDef = TypedDict(
    "FindingSourceDetailTypeDef",
    {
        "accessPointArn": str,
    },
    total=False,
)

GeneratedPolicyTypeDef = TypedDict(
    "GeneratedPolicyTypeDef",
    {
        "policy": str,
    },
)

GetAccessPreviewRequestRequestTypeDef = TypedDict(
    "GetAccessPreviewRequestRequestTypeDef",
    {
        "accessPreviewId": str,
        "analyzerArn": str,
    },
)

GetAnalyzedResourceRequestRequestTypeDef = TypedDict(
    "GetAnalyzedResourceRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "resourceArn": str,
    },
)

GetAnalyzerRequestRequestTypeDef = TypedDict(
    "GetAnalyzerRequestRequestTypeDef",
    {
        "analyzerName": str,
    },
)

GetArchiveRuleRequestRequestTypeDef = TypedDict(
    "GetArchiveRuleRequestRequestTypeDef",
    {
        "analyzerName": str,
        "ruleName": str,
    },
)

GetFindingRequestRequestTypeDef = TypedDict(
    "GetFindingRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "id": str,
    },
)

_RequiredGetGeneratedPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetGeneratedPolicyRequestRequestTypeDef",
    {
        "jobId": str,
    },
)
_OptionalGetGeneratedPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetGeneratedPolicyRequestRequestTypeDef",
    {
        "includeResourcePlaceholders": bool,
        "includeServiceLevelTemplate": bool,
    },
    total=False,
)


class GetGeneratedPolicyRequestRequestTypeDef(
    _RequiredGetGeneratedPolicyRequestRequestTypeDef,
    _OptionalGetGeneratedPolicyRequestRequestTypeDef,
):
    pass


JobErrorTypeDef = TypedDict(
    "JobErrorTypeDef",
    {
        "code": JobErrorCodeType,
        "message": str,
    },
)

KmsGrantConstraintsTypeDef = TypedDict(
    "KmsGrantConstraintsTypeDef",
    {
        "encryptionContextEquals": Mapping[str, str],
        "encryptionContextSubset": Mapping[str, str],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListAccessPreviewsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessPreviewsRequestRequestTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListAccessPreviewsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessPreviewsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAccessPreviewsRequestRequestTypeDef(
    _RequiredListAccessPreviewsRequestRequestTypeDef,
    _OptionalListAccessPreviewsRequestRequestTypeDef,
):
    pass


_RequiredListAnalyzedResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListAnalyzedResourcesRequestRequestTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListAnalyzedResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListAnalyzedResourcesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "resourceType": ResourceTypeType,
    },
    total=False,
)


class ListAnalyzedResourcesRequestRequestTypeDef(
    _RequiredListAnalyzedResourcesRequestRequestTypeDef,
    _OptionalListAnalyzedResourcesRequestRequestTypeDef,
):
    pass


ListAnalyzersRequestRequestTypeDef = TypedDict(
    "ListAnalyzersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "type": TypeType,
    },
    total=False,
)

_RequiredListArchiveRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListArchiveRulesRequestRequestTypeDef",
    {
        "analyzerName": str,
    },
)
_OptionalListArchiveRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListArchiveRulesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListArchiveRulesRequestRequestTypeDef(
    _RequiredListArchiveRulesRequestRequestTypeDef, _OptionalListArchiveRulesRequestRequestTypeDef
):
    pass


SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "attributeName": str,
        "orderBy": OrderByType,
    },
    total=False,
)

ListPolicyGenerationsRequestRequestTypeDef = TypedDict(
    "ListPolicyGenerationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "principalArn": str,
    },
    total=False,
)

_RequiredPolicyGenerationTypeDef = TypedDict(
    "_RequiredPolicyGenerationTypeDef",
    {
        "jobId": str,
        "principalArn": str,
        "startedOn": datetime,
        "status": JobStatusType,
    },
)
_OptionalPolicyGenerationTypeDef = TypedDict(
    "_OptionalPolicyGenerationTypeDef",
    {
        "completedOn": datetime,
    },
    total=False,
)


class PolicyGenerationTypeDef(_RequiredPolicyGenerationTypeDef, _OptionalPolicyGenerationTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "vpcId": str,
    },
)

SubstringTypeDef = TypedDict(
    "SubstringTypeDef",
    {
        "length": int,
        "start": int,
    },
)

PolicyGenerationDetailsTypeDef = TypedDict(
    "PolicyGenerationDetailsTypeDef",
    {
        "principalArn": str,
    },
)

PositionTypeDef = TypedDict(
    "PositionTypeDef",
    {
        "column": int,
        "line": int,
        "offset": int,
    },
)

S3PublicAccessBlockConfigurationTypeDef = TypedDict(
    "S3PublicAccessBlockConfigurationTypeDef",
    {
        "ignorePublicAcls": bool,
        "restrictPublicBuckets": bool,
    },
)

StartResourceScanRequestRequestTypeDef = TypedDict(
    "StartResourceScanRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "resourceArn": str,
    },
)

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

_RequiredUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingsRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "status": FindingStatusUpdateType,
    },
)
_OptionalUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingsRequestRequestTypeDef",
    {
        "clientToken": str,
        "ids": Sequence[str],
        "resourceArn": str,
    },
    total=False,
)


class UpdateFindingsRequestRequestTypeDef(
    _RequiredUpdateFindingsRequestRequestTypeDef, _OptionalUpdateFindingsRequestRequestTypeDef
):
    pass


_RequiredValidatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredValidatePolicyRequestRequestTypeDef",
    {
        "policyDocument": str,
        "policyType": PolicyTypeType,
    },
)
_OptionalValidatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalValidatePolicyRequestRequestTypeDef",
    {
        "locale": LocaleType,
        "maxResults": int,
        "nextToken": str,
        "validatePolicyResourceType": ValidatePolicyResourceTypeType,
    },
    total=False,
)


class ValidatePolicyRequestRequestTypeDef(
    _RequiredValidatePolicyRequestRequestTypeDef, _OptionalValidatePolicyRequestRequestTypeDef
):
    pass


_RequiredAccessPreviewSummaryTypeDef = TypedDict(
    "_RequiredAccessPreviewSummaryTypeDef",
    {
        "analyzerArn": str,
        "createdAt": datetime,
        "id": str,
        "status": AccessPreviewStatusType,
    },
)
_OptionalAccessPreviewSummaryTypeDef = TypedDict(
    "_OptionalAccessPreviewSummaryTypeDef",
    {
        "statusReason": AccessPreviewStatusReasonTypeDef,
    },
    total=False,
)


class AccessPreviewSummaryTypeDef(
    _RequiredAccessPreviewSummaryTypeDef, _OptionalAccessPreviewSummaryTypeDef
):
    pass


S3BucketAclGrantConfigurationTypeDef = TypedDict(
    "S3BucketAclGrantConfigurationTypeDef",
    {
        "grantee": AclGranteeTypeDef,
        "permission": AclPermissionType,
    },
)

_RequiredAnalyzerSummaryTypeDef = TypedDict(
    "_RequiredAnalyzerSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "name": str,
        "status": AnalyzerStatusType,
        "type": TypeType,
    },
)
_OptionalAnalyzerSummaryTypeDef = TypedDict(
    "_OptionalAnalyzerSummaryTypeDef",
    {
        "lastResourceAnalyzed": str,
        "lastResourceAnalyzedAt": datetime,
        "statusReason": StatusReasonTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)


class AnalyzerSummaryTypeDef(_RequiredAnalyzerSummaryTypeDef, _OptionalAnalyzerSummaryTypeDef):
    pass


ArchiveRuleSummaryTypeDef = TypedDict(
    "ArchiveRuleSummaryTypeDef",
    {
        "createdAt": datetime,
        "filter": Dict[str, CriterionTypeDef],
        "ruleName": str,
        "updatedAt": datetime,
    },
)

_RequiredCreateArchiveRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateArchiveRuleRequestRequestTypeDef",
    {
        "analyzerName": str,
        "filter": Mapping[str, CriterionTypeDef],
        "ruleName": str,
    },
)
_OptionalCreateArchiveRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateArchiveRuleRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateArchiveRuleRequestRequestTypeDef(
    _RequiredCreateArchiveRuleRequestRequestTypeDef, _OptionalCreateArchiveRuleRequestRequestTypeDef
):
    pass


InlineArchiveRuleTypeDef = TypedDict(
    "InlineArchiveRuleTypeDef",
    {
        "filter": Mapping[str, CriterionTypeDef],
        "ruleName": str,
    },
)

_RequiredListAccessPreviewFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessPreviewFindingsRequestRequestTypeDef",
    {
        "accessPreviewId": str,
        "analyzerArn": str,
    },
)
_OptionalListAccessPreviewFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessPreviewFindingsRequestRequestTypeDef",
    {
        "filter": Mapping[str, CriterionTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAccessPreviewFindingsRequestRequestTypeDef(
    _RequiredListAccessPreviewFindingsRequestRequestTypeDef,
    _OptionalListAccessPreviewFindingsRequestRequestTypeDef,
):
    pass


_RequiredUpdateArchiveRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateArchiveRuleRequestRequestTypeDef",
    {
        "analyzerName": str,
        "filter": Mapping[str, CriterionTypeDef],
        "ruleName": str,
    },
)
_OptionalUpdateArchiveRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateArchiveRuleRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateArchiveRuleRequestRequestTypeDef(
    _RequiredUpdateArchiveRuleRequestRequestTypeDef, _OptionalUpdateArchiveRuleRequestRequestTypeDef
):
    pass


_RequiredCloudTrailDetailsTypeDef = TypedDict(
    "_RequiredCloudTrailDetailsTypeDef",
    {
        "accessRole": str,
        "startTime": Union[datetime, str],
        "trails": Sequence[TrailTypeDef],
    },
)
_OptionalCloudTrailDetailsTypeDef = TypedDict(
    "_OptionalCloudTrailDetailsTypeDef",
    {
        "endTime": Union[datetime, str],
    },
    total=False,
)


class CloudTrailDetailsTypeDef(
    _RequiredCloudTrailDetailsTypeDef, _OptionalCloudTrailDetailsTypeDef
):
    pass


CloudTrailPropertiesTypeDef = TypedDict(
    "CloudTrailPropertiesTypeDef",
    {
        "endTime": datetime,
        "startTime": datetime,
        "trailProperties": List[TrailPropertiesTypeDef],
    },
)

CreateAccessPreviewResponseTypeDef = TypedDict(
    "CreateAccessPreviewResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAnalyzerResponseTypeDef = TypedDict(
    "CreateAnalyzerResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnalyzedResourceResponseTypeDef = TypedDict(
    "GetAnalyzedResourceResponseTypeDef",
    {
        "resource": AnalyzedResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnalyzedResourcesResponseTypeDef = TypedDict(
    "ListAnalyzedResourcesResponseTypeDef",
    {
        "analyzedResources": List[AnalyzedResourceSummaryTypeDef],
        "nextToken": str,
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

StartPolicyGenerationResponseTypeDef = TypedDict(
    "StartPolicyGenerationResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFindingSourceTypeDef = TypedDict(
    "_RequiredFindingSourceTypeDef",
    {
        "type": FindingSourceTypeType,
    },
)
_OptionalFindingSourceTypeDef = TypedDict(
    "_OptionalFindingSourceTypeDef",
    {
        "detail": FindingSourceDetailTypeDef,
    },
    total=False,
)


class FindingSourceTypeDef(_RequiredFindingSourceTypeDef, _OptionalFindingSourceTypeDef):
    pass


_RequiredJobDetailsTypeDef = TypedDict(
    "_RequiredJobDetailsTypeDef",
    {
        "jobId": str,
        "startedOn": datetime,
        "status": JobStatusType,
    },
)
_OptionalJobDetailsTypeDef = TypedDict(
    "_OptionalJobDetailsTypeDef",
    {
        "completedOn": datetime,
        "jobError": JobErrorTypeDef,
    },
    total=False,
)


class JobDetailsTypeDef(_RequiredJobDetailsTypeDef, _OptionalJobDetailsTypeDef):
    pass


_RequiredKmsGrantConfigurationTypeDef = TypedDict(
    "_RequiredKmsGrantConfigurationTypeDef",
    {
        "granteePrincipal": str,
        "issuingAccount": str,
        "operations": Sequence[KmsGrantOperationType],
    },
)
_OptionalKmsGrantConfigurationTypeDef = TypedDict(
    "_OptionalKmsGrantConfigurationTypeDef",
    {
        "constraints": KmsGrantConstraintsTypeDef,
        "retiringPrincipal": str,
    },
    total=False,
)


class KmsGrantConfigurationTypeDef(
    _RequiredKmsGrantConfigurationTypeDef, _OptionalKmsGrantConfigurationTypeDef
):
    pass


_RequiredListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef = TypedDict(
    "_RequiredListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef",
    {
        "accessPreviewId": str,
        "analyzerArn": str,
    },
)
_OptionalListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef = TypedDict(
    "_OptionalListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef",
    {
        "filter": Mapping[str, CriterionTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef(
    _RequiredListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef,
    _OptionalListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef,
):
    pass


_RequiredListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef = TypedDict(
    "_RequiredListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef = TypedDict(
    "_OptionalListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef(
    _RequiredListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef,
    _OptionalListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef,
):
    pass


_RequiredListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef",
    {
        "resourceType": ResourceTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef(
    _RequiredListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef,
    _OptionalListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef,
):
    pass


ListAnalyzersRequestListAnalyzersPaginateTypeDef = TypedDict(
    "ListAnalyzersRequestListAnalyzersPaginateTypeDef",
    {
        "type": TypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListArchiveRulesRequestListArchiveRulesPaginateTypeDef = TypedDict(
    "_RequiredListArchiveRulesRequestListArchiveRulesPaginateTypeDef",
    {
        "analyzerName": str,
    },
)
_OptionalListArchiveRulesRequestListArchiveRulesPaginateTypeDef = TypedDict(
    "_OptionalListArchiveRulesRequestListArchiveRulesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListArchiveRulesRequestListArchiveRulesPaginateTypeDef(
    _RequiredListArchiveRulesRequestListArchiveRulesPaginateTypeDef,
    _OptionalListArchiveRulesRequestListArchiveRulesPaginateTypeDef,
):
    pass


ListPolicyGenerationsRequestListPolicyGenerationsPaginateTypeDef = TypedDict(
    "ListPolicyGenerationsRequestListPolicyGenerationsPaginateTypeDef",
    {
        "principalArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredValidatePolicyRequestValidatePolicyPaginateTypeDef = TypedDict(
    "_RequiredValidatePolicyRequestValidatePolicyPaginateTypeDef",
    {
        "policyDocument": str,
        "policyType": PolicyTypeType,
    },
)
_OptionalValidatePolicyRequestValidatePolicyPaginateTypeDef = TypedDict(
    "_OptionalValidatePolicyRequestValidatePolicyPaginateTypeDef",
    {
        "locale": LocaleType,
        "validatePolicyResourceType": ValidatePolicyResourceTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ValidatePolicyRequestValidatePolicyPaginateTypeDef(
    _RequiredValidatePolicyRequestValidatePolicyPaginateTypeDef,
    _OptionalValidatePolicyRequestValidatePolicyPaginateTypeDef,
):
    pass


_RequiredListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "_RequiredListFindingsRequestListFindingsPaginateTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "_OptionalListFindingsRequestListFindingsPaginateTypeDef",
    {
        "filter": Mapping[str, CriterionTypeDef],
        "sort": SortCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFindingsRequestListFindingsPaginateTypeDef(
    _RequiredListFindingsRequestListFindingsPaginateTypeDef,
    _OptionalListFindingsRequestListFindingsPaginateTypeDef,
):
    pass


_RequiredListFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingsRequestRequestTypeDef",
    {
        "analyzerArn": str,
    },
)
_OptionalListFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingsRequestRequestTypeDef",
    {
        "filter": Mapping[str, CriterionTypeDef],
        "maxResults": int,
        "nextToken": str,
        "sort": SortCriteriaTypeDef,
    },
    total=False,
)


class ListFindingsRequestRequestTypeDef(
    _RequiredListFindingsRequestRequestTypeDef, _OptionalListFindingsRequestRequestTypeDef
):
    pass


ListPolicyGenerationsResponseTypeDef = TypedDict(
    "ListPolicyGenerationsResponseTypeDef",
    {
        "nextToken": str,
        "policyGenerations": List[PolicyGenerationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkOriginConfigurationTypeDef = TypedDict(
    "NetworkOriginConfigurationTypeDef",
    {
        "internetConfiguration": Mapping[str, Any],
        "vpcConfiguration": VpcConfigurationTypeDef,
    },
    total=False,
)

PathElementTypeDef = TypedDict(
    "PathElementTypeDef",
    {
        "index": int,
        "key": str,
        "substring": SubstringTypeDef,
        "value": str,
    },
    total=False,
)

SpanTypeDef = TypedDict(
    "SpanTypeDef",
    {
        "end": PositionTypeDef,
        "start": PositionTypeDef,
    },
)

ListAccessPreviewsResponseTypeDef = TypedDict(
    "ListAccessPreviewsResponseTypeDef",
    {
        "accessPreviews": List[AccessPreviewSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnalyzerResponseTypeDef = TypedDict(
    "GetAnalyzerResponseTypeDef",
    {
        "analyzer": AnalyzerSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnalyzersResponseTypeDef = TypedDict(
    "ListAnalyzersResponseTypeDef",
    {
        "analyzers": List[AnalyzerSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetArchiveRuleResponseTypeDef = TypedDict(
    "GetArchiveRuleResponseTypeDef",
    {
        "archiveRule": ArchiveRuleSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListArchiveRulesResponseTypeDef = TypedDict(
    "ListArchiveRulesResponseTypeDef",
    {
        "archiveRules": List[ArchiveRuleSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAnalyzerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnalyzerRequestRequestTypeDef",
    {
        "analyzerName": str,
        "type": TypeType,
    },
)
_OptionalCreateAnalyzerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnalyzerRequestRequestTypeDef",
    {
        "archiveRules": Sequence[InlineArchiveRuleTypeDef],
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAnalyzerRequestRequestTypeDef(
    _RequiredCreateAnalyzerRequestRequestTypeDef, _OptionalCreateAnalyzerRequestRequestTypeDef
):
    pass


_RequiredStartPolicyGenerationRequestRequestTypeDef = TypedDict(
    "_RequiredStartPolicyGenerationRequestRequestTypeDef",
    {
        "policyGenerationDetails": PolicyGenerationDetailsTypeDef,
    },
)
_OptionalStartPolicyGenerationRequestRequestTypeDef = TypedDict(
    "_OptionalStartPolicyGenerationRequestRequestTypeDef",
    {
        "clientToken": str,
        "cloudTrailDetails": CloudTrailDetailsTypeDef,
    },
    total=False,
)


class StartPolicyGenerationRequestRequestTypeDef(
    _RequiredStartPolicyGenerationRequestRequestTypeDef,
    _OptionalStartPolicyGenerationRequestRequestTypeDef,
):
    pass


_RequiredGeneratedPolicyPropertiesTypeDef = TypedDict(
    "_RequiredGeneratedPolicyPropertiesTypeDef",
    {
        "principalArn": str,
    },
)
_OptionalGeneratedPolicyPropertiesTypeDef = TypedDict(
    "_OptionalGeneratedPolicyPropertiesTypeDef",
    {
        "cloudTrailProperties": CloudTrailPropertiesTypeDef,
        "isComplete": bool,
    },
    total=False,
)


class GeneratedPolicyPropertiesTypeDef(
    _RequiredGeneratedPolicyPropertiesTypeDef, _OptionalGeneratedPolicyPropertiesTypeDef
):
    pass


_RequiredAccessPreviewFindingTypeDef = TypedDict(
    "_RequiredAccessPreviewFindingTypeDef",
    {
        "changeType": FindingChangeTypeType,
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": ResourceTypeType,
        "status": FindingStatusType,
    },
)
_OptionalAccessPreviewFindingTypeDef = TypedDict(
    "_OptionalAccessPreviewFindingTypeDef",
    {
        "action": List[str],
        "condition": Dict[str, str],
        "error": str,
        "existingFindingId": str,
        "existingFindingStatus": FindingStatusType,
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List[FindingSourceTypeDef],
    },
    total=False,
)


class AccessPreviewFindingTypeDef(
    _RequiredAccessPreviewFindingTypeDef, _OptionalAccessPreviewFindingTypeDef
):
    pass


_RequiredFindingSummaryTypeDef = TypedDict(
    "_RequiredFindingSummaryTypeDef",
    {
        "analyzedAt": datetime,
        "condition": Dict[str, str],
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": ResourceTypeType,
        "status": FindingStatusType,
        "updatedAt": datetime,
    },
)
_OptionalFindingSummaryTypeDef = TypedDict(
    "_OptionalFindingSummaryTypeDef",
    {
        "action": List[str],
        "error": str,
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List[FindingSourceTypeDef],
    },
    total=False,
)


class FindingSummaryTypeDef(_RequiredFindingSummaryTypeDef, _OptionalFindingSummaryTypeDef):
    pass


_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "analyzedAt": datetime,
        "condition": Dict[str, str],
        "createdAt": datetime,
        "id": str,
        "resourceOwnerAccount": str,
        "resourceType": ResourceTypeType,
        "status": FindingStatusType,
        "updatedAt": datetime,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "action": List[str],
        "error": str,
        "isPublic": bool,
        "principal": Dict[str, str],
        "resource": str,
        "sources": List[FindingSourceTypeDef],
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


KmsKeyConfigurationTypeDef = TypedDict(
    "KmsKeyConfigurationTypeDef",
    {
        "grants": Sequence[KmsGrantConfigurationTypeDef],
        "keyPolicies": Mapping[str, str],
    },
    total=False,
)

S3AccessPointConfigurationTypeDef = TypedDict(
    "S3AccessPointConfigurationTypeDef",
    {
        "accessPointPolicy": str,
        "networkOrigin": NetworkOriginConfigurationTypeDef,
        "publicAccessBlock": S3PublicAccessBlockConfigurationTypeDef,
    },
    total=False,
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "path": List[PathElementTypeDef],
        "span": SpanTypeDef,
    },
)

_RequiredGeneratedPolicyResultTypeDef = TypedDict(
    "_RequiredGeneratedPolicyResultTypeDef",
    {
        "properties": GeneratedPolicyPropertiesTypeDef,
    },
)
_OptionalGeneratedPolicyResultTypeDef = TypedDict(
    "_OptionalGeneratedPolicyResultTypeDef",
    {
        "generatedPolicies": List[GeneratedPolicyTypeDef],
    },
    total=False,
)


class GeneratedPolicyResultTypeDef(
    _RequiredGeneratedPolicyResultTypeDef, _OptionalGeneratedPolicyResultTypeDef
):
    pass


ListAccessPreviewFindingsResponseTypeDef = TypedDict(
    "ListAccessPreviewFindingsResponseTypeDef",
    {
        "findings": List[AccessPreviewFindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findings": List[FindingSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFindingResponseTypeDef = TypedDict(
    "GetFindingResponseTypeDef",
    {
        "finding": FindingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3BucketConfigurationTypeDef = TypedDict(
    "S3BucketConfigurationTypeDef",
    {
        "accessPoints": Mapping[str, S3AccessPointConfigurationTypeDef],
        "bucketAclGrants": Sequence[S3BucketAclGrantConfigurationTypeDef],
        "bucketPolicy": str,
        "bucketPublicAccessBlock": S3PublicAccessBlockConfigurationTypeDef,
    },
    total=False,
)

ValidatePolicyFindingTypeDef = TypedDict(
    "ValidatePolicyFindingTypeDef",
    {
        "findingDetails": str,
        "findingType": ValidatePolicyFindingTypeType,
        "issueCode": str,
        "learnMoreLink": str,
        "locations": List[LocationTypeDef],
    },
)

GetGeneratedPolicyResponseTypeDef = TypedDict(
    "GetGeneratedPolicyResponseTypeDef",
    {
        "generatedPolicyResult": GeneratedPolicyResultTypeDef,
        "jobDetails": JobDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "iamRole": IamRoleConfigurationTypeDef,
        "kmsKey": KmsKeyConfigurationTypeDef,
        "s3Bucket": S3BucketConfigurationTypeDef,
        "secretsManagerSecret": SecretsManagerSecretConfigurationTypeDef,
        "sqsQueue": SqsQueueConfigurationTypeDef,
    },
    total=False,
)

ValidatePolicyResponseTypeDef = TypedDict(
    "ValidatePolicyResponseTypeDef",
    {
        "findings": List[ValidatePolicyFindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAccessPreviewTypeDef = TypedDict(
    "_RequiredAccessPreviewTypeDef",
    {
        "analyzerArn": str,
        "configurations": Dict[str, ConfigurationTypeDef],
        "createdAt": datetime,
        "id": str,
        "status": AccessPreviewStatusType,
    },
)
_OptionalAccessPreviewTypeDef = TypedDict(
    "_OptionalAccessPreviewTypeDef",
    {
        "statusReason": AccessPreviewStatusReasonTypeDef,
    },
    total=False,
)


class AccessPreviewTypeDef(_RequiredAccessPreviewTypeDef, _OptionalAccessPreviewTypeDef):
    pass


_RequiredCreateAccessPreviewRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPreviewRequestRequestTypeDef",
    {
        "analyzerArn": str,
        "configurations": Mapping[str, ConfigurationTypeDef],
    },
)
_OptionalCreateAccessPreviewRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPreviewRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateAccessPreviewRequestRequestTypeDef(
    _RequiredCreateAccessPreviewRequestRequestTypeDef,
    _OptionalCreateAccessPreviewRequestRequestTypeDef,
):
    pass


GetAccessPreviewResponseTypeDef = TypedDict(
    "GetAccessPreviewResponseTypeDef",
    {
        "accessPreview": AccessPreviewTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
