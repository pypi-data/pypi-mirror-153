"""
Type annotations for cloudfront service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudfront.type_defs import AliasICPRecordalTypeDef

    data: AliasICPRecordalTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CachePolicyCookieBehaviorType,
    CachePolicyHeaderBehaviorType,
    CachePolicyQueryStringBehaviorType,
    CachePolicyTypeType,
    CertificateSourceType,
    EventTypeType,
    FrameOptionsListType,
    FunctionStageType,
    GeoRestrictionTypeType,
    HttpVersionType,
    ICPRecordalStatusType,
    ItemSelectionType,
    MethodType,
    MinimumProtocolVersionType,
    OriginProtocolPolicyType,
    OriginRequestPolicyCookieBehaviorType,
    OriginRequestPolicyHeaderBehaviorType,
    OriginRequestPolicyQueryStringBehaviorType,
    OriginRequestPolicyTypeType,
    PriceClassType,
    RealtimeMetricsSubscriptionStatusType,
    ReferrerPolicyListType,
    ResponseHeadersPolicyAccessControlAllowMethodsValuesType,
    ResponseHeadersPolicyTypeType,
    SslProtocolType,
    SSLSupportMethodType,
    ViewerProtocolPolicyType,
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
    "AliasICPRecordalTypeDef",
    "AliasesTypeDef",
    "CachedMethodsTypeDef",
    "AssociateAliasRequestRequestTypeDef",
    "TrustedKeyGroupsTypeDef",
    "TrustedSignersTypeDef",
    "CookieNamesTypeDef",
    "HeadersTypeDef",
    "QueryStringNamesTypeDef",
    "CloudFrontOriginAccessIdentityConfigTypeDef",
    "CloudFrontOriginAccessIdentitySummaryTypeDef",
    "ConflictingAliasTypeDef",
    "ContentTypeProfileTypeDef",
    "ResponseMetadataTypeDef",
    "FunctionConfigTypeDef",
    "KeyGroupConfigTypeDef",
    "PublicKeyConfigTypeDef",
    "CustomErrorResponseTypeDef",
    "OriginCustomHeaderTypeDef",
    "OriginSslProtocolsTypeDef",
    "DeleteCachePolicyRequestRequestTypeDef",
    "DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "DeleteDistributionRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteKeyGroupRequestRequestTypeDef",
    "DeleteMonitoringSubscriptionRequestRequestTypeDef",
    "DeleteOriginRequestPolicyRequestRequestTypeDef",
    "DeletePublicKeyRequestRequestTypeDef",
    "DeleteRealtimeLogConfigRequestRequestTypeDef",
    "DeleteResponseHeadersPolicyRequestRequestTypeDef",
    "DeleteStreamingDistributionRequestRequestTypeDef",
    "DescribeFunctionRequestRequestTypeDef",
    "LoggingConfigTypeDef",
    "ViewerCertificateTypeDef",
    "DistributionIdListTypeDef",
    "FieldPatternsTypeDef",
    "KinesisStreamConfigTypeDef",
    "QueryStringCacheKeysTypeDef",
    "FunctionAssociationTypeDef",
    "FunctionMetadataTypeDef",
    "GeoRestrictionTypeDef",
    "GetCachePolicyConfigRequestRequestTypeDef",
    "GetCachePolicyRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "GetDistributionConfigRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetDistributionRequestRequestTypeDef",
    "GetFieldLevelEncryptionConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileRequestRequestTypeDef",
    "GetFieldLevelEncryptionRequestRequestTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetInvalidationRequestRequestTypeDef",
    "GetKeyGroupConfigRequestRequestTypeDef",
    "GetKeyGroupRequestRequestTypeDef",
    "GetMonitoringSubscriptionRequestRequestTypeDef",
    "GetOriginRequestPolicyConfigRequestRequestTypeDef",
    "GetOriginRequestPolicyRequestRequestTypeDef",
    "GetPublicKeyConfigRequestRequestTypeDef",
    "GetPublicKeyRequestRequestTypeDef",
    "GetRealtimeLogConfigRequestRequestTypeDef",
    "GetResponseHeadersPolicyConfigRequestRequestTypeDef",
    "GetResponseHeadersPolicyRequestRequestTypeDef",
    "GetStreamingDistributionConfigRequestRequestTypeDef",
    "GetStreamingDistributionRequestRequestTypeDef",
    "PathsTypeDef",
    "InvalidationSummaryTypeDef",
    "KeyPairIdsTypeDef",
    "LambdaFunctionAssociationTypeDef",
    "ListCachePoliciesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef",
    "ListConflictingAliasesRequestRequestTypeDef",
    "ListDistributionsByCachePolicyIdRequestRequestTypeDef",
    "ListDistributionsByKeyGroupRequestRequestTypeDef",
    "ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    "ListDistributionsByRealtimeLogConfigRequestRequestTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    "ListDistributionsByWebACLIdRequestRequestTypeDef",
    "ListDistributionsRequestRequestTypeDef",
    "ListFieldLevelEncryptionConfigsRequestRequestTypeDef",
    "ListFieldLevelEncryptionProfilesRequestRequestTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListInvalidationsRequestRequestTypeDef",
    "ListKeyGroupsRequestRequestTypeDef",
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    "ListPublicKeysRequestRequestTypeDef",
    "ListRealtimeLogConfigsRequestRequestTypeDef",
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    "ListStreamingDistributionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RealtimeMetricsSubscriptionConfigTypeDef",
    "StatusCodesTypeDef",
    "OriginGroupMemberTypeDef",
    "OriginShieldTypeDef",
    "S3OriginConfigTypeDef",
    "PublicKeySummaryTypeDef",
    "PublishFunctionRequestRequestTypeDef",
    "QueryArgProfileTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    "ResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    "ResponseHeadersPolicyContentSecurityPolicyTypeDef",
    "ResponseHeadersPolicyContentTypeOptionsTypeDef",
    "ResponseHeadersPolicyCustomHeaderTypeDef",
    "ResponseHeadersPolicyFrameOptionsTypeDef",
    "ResponseHeadersPolicyReferrerPolicyTypeDef",
    "ResponseHeadersPolicyStrictTransportSecurityTypeDef",
    "ResponseHeadersPolicyXSSProtectionTypeDef",
    "S3OriginTypeDef",
    "StreamingLoggingConfigTypeDef",
    "TagKeysTypeDef",
    "TagTypeDef",
    "TestFunctionRequestRequestTypeDef",
    "AllowedMethodsTypeDef",
    "CachePolicyCookiesConfigTypeDef",
    "CookiePreferenceTypeDef",
    "OriginRequestPolicyCookiesConfigTypeDef",
    "CachePolicyHeadersConfigTypeDef",
    "OriginRequestPolicyHeadersConfigTypeDef",
    "CachePolicyQueryStringsConfigTypeDef",
    "OriginRequestPolicyQueryStringsConfigTypeDef",
    "CloudFrontOriginAccessIdentityTypeDef",
    "CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "CloudFrontOriginAccessIdentityListTypeDef",
    "ConflictingAliasesListTypeDef",
    "ContentTypeProfilesTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigResultTypeDef",
    "GetFunctionResultTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "UpdateFunctionRequestRequestTypeDef",
    "CreateKeyGroupRequestRequestTypeDef",
    "GetKeyGroupConfigResultTypeDef",
    "KeyGroupTypeDef",
    "UpdateKeyGroupRequestRequestTypeDef",
    "CreatePublicKeyRequestRequestTypeDef",
    "GetPublicKeyConfigResultTypeDef",
    "PublicKeyTypeDef",
    "UpdatePublicKeyRequestRequestTypeDef",
    "CustomErrorResponsesTypeDef",
    "CustomHeadersTypeDef",
    "CustomOriginConfigTypeDef",
    "ListDistributionsByCachePolicyIdResultTypeDef",
    "ListDistributionsByKeyGroupResultTypeDef",
    "ListDistributionsByOriginRequestPolicyIdResultTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdResultTypeDef",
    "EncryptionEntityTypeDef",
    "EndPointTypeDef",
    "FunctionAssociationsTypeDef",
    "FunctionSummaryTypeDef",
    "RestrictionsTypeDef",
    "GetDistributionRequestDistributionDeployedWaitTypeDef",
    "GetInvalidationRequestInvalidationCompletedWaitTypeDef",
    "GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    "InvalidationBatchTypeDef",
    "InvalidationListTypeDef",
    "KGKeyPairIdsTypeDef",
    "SignerTypeDef",
    "LambdaFunctionAssociationsTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef",
    "ListDistributionsRequestListDistributionsPaginateTypeDef",
    "ListInvalidationsRequestListInvalidationsPaginateTypeDef",
    "ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef",
    "MonitoringSubscriptionTypeDef",
    "OriginGroupFailoverCriteriaTypeDef",
    "OriginGroupMembersTypeDef",
    "PublicKeyListTypeDef",
    "QueryArgProfilesTypeDef",
    "ResponseHeadersPolicyCorsConfigTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigTypeDef",
    "ResponseHeadersPolicySecurityHeadersConfigTypeDef",
    "StreamingDistributionSummaryTypeDef",
    "StreamingDistributionConfigTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "TagsTypeDef",
    "ForwardedValuesTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginTypeDef",
    "OriginRequestPolicyConfigTypeDef",
    "CreateCloudFrontOriginAccessIdentityResultTypeDef",
    "GetCloudFrontOriginAccessIdentityResultTypeDef",
    "UpdateCloudFrontOriginAccessIdentityResultTypeDef",
    "ListCloudFrontOriginAccessIdentitiesResultTypeDef",
    "ListConflictingAliasesResultTypeDef",
    "ContentTypeProfileConfigTypeDef",
    "CreateKeyGroupResultTypeDef",
    "GetKeyGroupResultTypeDef",
    "KeyGroupSummaryTypeDef",
    "UpdateKeyGroupResultTypeDef",
    "CreatePublicKeyResultTypeDef",
    "GetPublicKeyResultTypeDef",
    "UpdatePublicKeyResultTypeDef",
    "OriginTypeDef",
    "EncryptionEntitiesTypeDef",
    "CreateRealtimeLogConfigRequestRequestTypeDef",
    "RealtimeLogConfigTypeDef",
    "UpdateRealtimeLogConfigRequestRequestTypeDef",
    "CreateFunctionResultTypeDef",
    "DescribeFunctionResultTypeDef",
    "FunctionListTypeDef",
    "PublishFunctionResultTypeDef",
    "TestResultTypeDef",
    "UpdateFunctionResultTypeDef",
    "CreateInvalidationRequestRequestTypeDef",
    "InvalidationTypeDef",
    "ListInvalidationsResultTypeDef",
    "ActiveTrustedKeyGroupsTypeDef",
    "ActiveTrustedSignersTypeDef",
    "CreateMonitoringSubscriptionRequestRequestTypeDef",
    "CreateMonitoringSubscriptionResultTypeDef",
    "GetMonitoringSubscriptionResultTypeDef",
    "OriginGroupTypeDef",
    "ListPublicKeysResultTypeDef",
    "QueryArgProfileConfigTypeDef",
    "ResponseHeadersPolicyConfigTypeDef",
    "StreamingDistributionListTypeDef",
    "CreateStreamingDistributionRequestRequestTypeDef",
    "GetStreamingDistributionConfigResultTypeDef",
    "UpdateStreamingDistributionRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "StreamingDistributionConfigWithTagsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CacheBehaviorTypeDef",
    "DefaultCacheBehaviorTypeDef",
    "CachePolicyConfigTypeDef",
    "CreateOriginRequestPolicyRequestRequestTypeDef",
    "GetOriginRequestPolicyConfigResultTypeDef",
    "OriginRequestPolicyTypeDef",
    "UpdateOriginRequestPolicyRequestRequestTypeDef",
    "KeyGroupListTypeDef",
    "OriginsTypeDef",
    "FieldLevelEncryptionProfileConfigTypeDef",
    "FieldLevelEncryptionProfileSummaryTypeDef",
    "CreateRealtimeLogConfigResultTypeDef",
    "GetRealtimeLogConfigResultTypeDef",
    "RealtimeLogConfigsTypeDef",
    "UpdateRealtimeLogConfigResultTypeDef",
    "ListFunctionsResultTypeDef",
    "TestFunctionResultTypeDef",
    "CreateInvalidationResultTypeDef",
    "GetInvalidationResultTypeDef",
    "StreamingDistributionTypeDef",
    "OriginGroupsTypeDef",
    "FieldLevelEncryptionConfigTypeDef",
    "FieldLevelEncryptionSummaryTypeDef",
    "CreateResponseHeadersPolicyRequestRequestTypeDef",
    "GetResponseHeadersPolicyConfigResultTypeDef",
    "ResponseHeadersPolicyTypeDef",
    "UpdateResponseHeadersPolicyRequestRequestTypeDef",
    "ListStreamingDistributionsResultTypeDef",
    "CreateStreamingDistributionWithTagsRequestRequestTypeDef",
    "CacheBehaviorsTypeDef",
    "CachePolicyTypeDef",
    "CreateCachePolicyRequestRequestTypeDef",
    "GetCachePolicyConfigResultTypeDef",
    "UpdateCachePolicyRequestRequestTypeDef",
    "CreateOriginRequestPolicyResultTypeDef",
    "GetOriginRequestPolicyResultTypeDef",
    "OriginRequestPolicySummaryTypeDef",
    "UpdateOriginRequestPolicyResultTypeDef",
    "ListKeyGroupsResultTypeDef",
    "CreateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "FieldLevelEncryptionProfileTypeDef",
    "GetFieldLevelEncryptionProfileConfigResultTypeDef",
    "UpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "FieldLevelEncryptionProfileListTypeDef",
    "ListRealtimeLogConfigsResultTypeDef",
    "CreateStreamingDistributionResultTypeDef",
    "CreateStreamingDistributionWithTagsResultTypeDef",
    "GetStreamingDistributionResultTypeDef",
    "UpdateStreamingDistributionResultTypeDef",
    "CreateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "FieldLevelEncryptionTypeDef",
    "GetFieldLevelEncryptionConfigResultTypeDef",
    "UpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "FieldLevelEncryptionListTypeDef",
    "CreateResponseHeadersPolicyResultTypeDef",
    "GetResponseHeadersPolicyResultTypeDef",
    "ResponseHeadersPolicySummaryTypeDef",
    "UpdateResponseHeadersPolicyResultTypeDef",
    "DistributionConfigTypeDef",
    "DistributionSummaryTypeDef",
    "CachePolicySummaryTypeDef",
    "CreateCachePolicyResultTypeDef",
    "GetCachePolicyResultTypeDef",
    "UpdateCachePolicyResultTypeDef",
    "OriginRequestPolicyListTypeDef",
    "CreateFieldLevelEncryptionProfileResultTypeDef",
    "GetFieldLevelEncryptionProfileResultTypeDef",
    "UpdateFieldLevelEncryptionProfileResultTypeDef",
    "ListFieldLevelEncryptionProfilesResultTypeDef",
    "CreateFieldLevelEncryptionConfigResultTypeDef",
    "GetFieldLevelEncryptionResultTypeDef",
    "UpdateFieldLevelEncryptionConfigResultTypeDef",
    "ListFieldLevelEncryptionConfigsResultTypeDef",
    "ResponseHeadersPolicyListTypeDef",
    "CreateDistributionRequestRequestTypeDef",
    "DistributionConfigWithTagsTypeDef",
    "DistributionTypeDef",
    "GetDistributionConfigResultTypeDef",
    "UpdateDistributionRequestRequestTypeDef",
    "DistributionListTypeDef",
    "CachePolicyListTypeDef",
    "ListOriginRequestPoliciesResultTypeDef",
    "ListResponseHeadersPoliciesResultTypeDef",
    "CreateDistributionWithTagsRequestRequestTypeDef",
    "CreateDistributionResultTypeDef",
    "CreateDistributionWithTagsResultTypeDef",
    "GetDistributionResultTypeDef",
    "UpdateDistributionResultTypeDef",
    "ListDistributionsByRealtimeLogConfigResultTypeDef",
    "ListDistributionsByWebACLIdResultTypeDef",
    "ListDistributionsResultTypeDef",
    "ListCachePoliciesResultTypeDef",
)

AliasICPRecordalTypeDef = TypedDict(
    "AliasICPRecordalTypeDef",
    {
        "CNAME": str,
        "ICPRecordalStatus": ICPRecordalStatusType,
    },
    total=False,
)

_RequiredAliasesTypeDef = TypedDict(
    "_RequiredAliasesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalAliasesTypeDef = TypedDict(
    "_OptionalAliasesTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class AliasesTypeDef(_RequiredAliasesTypeDef, _OptionalAliasesTypeDef):
    pass


CachedMethodsTypeDef = TypedDict(
    "CachedMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[MethodType],
    },
)

AssociateAliasRequestRequestTypeDef = TypedDict(
    "AssociateAliasRequestRequestTypeDef",
    {
        "TargetDistributionId": str,
        "Alias": str,
    },
)

_RequiredTrustedKeyGroupsTypeDef = TypedDict(
    "_RequiredTrustedKeyGroupsTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
    },
)
_OptionalTrustedKeyGroupsTypeDef = TypedDict(
    "_OptionalTrustedKeyGroupsTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class TrustedKeyGroupsTypeDef(_RequiredTrustedKeyGroupsTypeDef, _OptionalTrustedKeyGroupsTypeDef):
    pass


_RequiredTrustedSignersTypeDef = TypedDict(
    "_RequiredTrustedSignersTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
    },
)
_OptionalTrustedSignersTypeDef = TypedDict(
    "_OptionalTrustedSignersTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class TrustedSignersTypeDef(_RequiredTrustedSignersTypeDef, _OptionalTrustedSignersTypeDef):
    pass


_RequiredCookieNamesTypeDef = TypedDict(
    "_RequiredCookieNamesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalCookieNamesTypeDef = TypedDict(
    "_OptionalCookieNamesTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class CookieNamesTypeDef(_RequiredCookieNamesTypeDef, _OptionalCookieNamesTypeDef):
    pass


_RequiredHeadersTypeDef = TypedDict(
    "_RequiredHeadersTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalHeadersTypeDef = TypedDict(
    "_OptionalHeadersTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class HeadersTypeDef(_RequiredHeadersTypeDef, _OptionalHeadersTypeDef):
    pass


_RequiredQueryStringNamesTypeDef = TypedDict(
    "_RequiredQueryStringNamesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalQueryStringNamesTypeDef = TypedDict(
    "_OptionalQueryStringNamesTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class QueryStringNamesTypeDef(_RequiredQueryStringNamesTypeDef, _OptionalQueryStringNamesTypeDef):
    pass


CloudFrontOriginAccessIdentityConfigTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentityConfigTypeDef",
    {
        "CallerReference": str,
        "Comment": str,
    },
)

CloudFrontOriginAccessIdentitySummaryTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentitySummaryTypeDef",
    {
        "Id": str,
        "S3CanonicalUserId": str,
        "Comment": str,
    },
)

ConflictingAliasTypeDef = TypedDict(
    "ConflictingAliasTypeDef",
    {
        "Alias": str,
        "DistributionId": str,
        "AccountId": str,
    },
    total=False,
)

_RequiredContentTypeProfileTypeDef = TypedDict(
    "_RequiredContentTypeProfileTypeDef",
    {
        "Format": Literal["URLEncoded"],
        "ContentType": str,
    },
)
_OptionalContentTypeProfileTypeDef = TypedDict(
    "_OptionalContentTypeProfileTypeDef",
    {
        "ProfileId": str,
    },
    total=False,
)


class ContentTypeProfileTypeDef(
    _RequiredContentTypeProfileTypeDef, _OptionalContentTypeProfileTypeDef
):
    pass


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

FunctionConfigTypeDef = TypedDict(
    "FunctionConfigTypeDef",
    {
        "Comment": str,
        "Runtime": Literal["cloudfront-js-1.0"],
    },
)

_RequiredKeyGroupConfigTypeDef = TypedDict(
    "_RequiredKeyGroupConfigTypeDef",
    {
        "Name": str,
        "Items": Sequence[str],
    },
)
_OptionalKeyGroupConfigTypeDef = TypedDict(
    "_OptionalKeyGroupConfigTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class KeyGroupConfigTypeDef(_RequiredKeyGroupConfigTypeDef, _OptionalKeyGroupConfigTypeDef):
    pass


_RequiredPublicKeyConfigTypeDef = TypedDict(
    "_RequiredPublicKeyConfigTypeDef",
    {
        "CallerReference": str,
        "Name": str,
        "EncodedKey": str,
    },
)
_OptionalPublicKeyConfigTypeDef = TypedDict(
    "_OptionalPublicKeyConfigTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class PublicKeyConfigTypeDef(_RequiredPublicKeyConfigTypeDef, _OptionalPublicKeyConfigTypeDef):
    pass


_RequiredCustomErrorResponseTypeDef = TypedDict(
    "_RequiredCustomErrorResponseTypeDef",
    {
        "ErrorCode": int,
    },
)
_OptionalCustomErrorResponseTypeDef = TypedDict(
    "_OptionalCustomErrorResponseTypeDef",
    {
        "ResponsePagePath": str,
        "ResponseCode": str,
        "ErrorCachingMinTTL": int,
    },
    total=False,
)


class CustomErrorResponseTypeDef(
    _RequiredCustomErrorResponseTypeDef, _OptionalCustomErrorResponseTypeDef
):
    pass


OriginCustomHeaderTypeDef = TypedDict(
    "OriginCustomHeaderTypeDef",
    {
        "HeaderName": str,
        "HeaderValue": str,
    },
)

OriginSslProtocolsTypeDef = TypedDict(
    "OriginSslProtocolsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[SslProtocolType],
    },
)

_RequiredDeleteCachePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCachePolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteCachePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCachePolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteCachePolicyRequestRequestTypeDef(
    _RequiredDeleteCachePolicyRequestRequestTypeDef, _OptionalDeleteCachePolicyRequestRequestTypeDef
):
    pass


_RequiredDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef(
    _RequiredDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    _OptionalDeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef,
):
    pass


_RequiredDeleteDistributionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteDistributionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDistributionRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteDistributionRequestRequestTypeDef(
    _RequiredDeleteDistributionRequestRequestTypeDef,
    _OptionalDeleteDistributionRequestRequestTypeDef,
):
    pass


_RequiredDeleteFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteFieldLevelEncryptionConfigRequestRequestTypeDef(
    _RequiredDeleteFieldLevelEncryptionConfigRequestRequestTypeDef,
    _OptionalDeleteFieldLevelEncryptionConfigRequestRequestTypeDef,
):
    pass


_RequiredDeleteFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteFieldLevelEncryptionProfileRequestRequestTypeDef(
    _RequiredDeleteFieldLevelEncryptionProfileRequestRequestTypeDef,
    _OptionalDeleteFieldLevelEncryptionProfileRequestRequestTypeDef,
):
    pass


DeleteFunctionRequestRequestTypeDef = TypedDict(
    "DeleteFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
    },
)

_RequiredDeleteKeyGroupRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteKeyGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteKeyGroupRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteKeyGroupRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteKeyGroupRequestRequestTypeDef(
    _RequiredDeleteKeyGroupRequestRequestTypeDef, _OptionalDeleteKeyGroupRequestRequestTypeDef
):
    pass


DeleteMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
    },
)

_RequiredDeleteOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteOriginRequestPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteOriginRequestPolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteOriginRequestPolicyRequestRequestTypeDef(
    _RequiredDeleteOriginRequestPolicyRequestRequestTypeDef,
    _OptionalDeleteOriginRequestPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeletePublicKeyRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePublicKeyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeletePublicKeyRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePublicKeyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeletePublicKeyRequestRequestTypeDef(
    _RequiredDeletePublicKeyRequestRequestTypeDef, _OptionalDeletePublicKeyRequestRequestTypeDef
):
    pass


DeleteRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "DeleteRealtimeLogConfigRequestRequestTypeDef",
    {
        "Name": str,
        "ARN": str,
    },
    total=False,
)

_RequiredDeleteResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResponseHeadersPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResponseHeadersPolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteResponseHeadersPolicyRequestRequestTypeDef(
    _RequiredDeleteResponseHeadersPolicyRequestRequestTypeDef,
    _OptionalDeleteResponseHeadersPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeleteStreamingDistributionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStreamingDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDeleteStreamingDistributionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStreamingDistributionRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class DeleteStreamingDistributionRequestRequestTypeDef(
    _RequiredDeleteStreamingDistributionRequestRequestTypeDef,
    _OptionalDeleteStreamingDistributionRequestRequestTypeDef,
):
    pass


_RequiredDescribeFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeFunctionRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDescribeFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeFunctionRequestRequestTypeDef",
    {
        "Stage": FunctionStageType,
    },
    total=False,
)


class DescribeFunctionRequestRequestTypeDef(
    _RequiredDescribeFunctionRequestRequestTypeDef, _OptionalDescribeFunctionRequestRequestTypeDef
):
    pass


LoggingConfigTypeDef = TypedDict(
    "LoggingConfigTypeDef",
    {
        "Enabled": bool,
        "IncludeCookies": bool,
        "Bucket": str,
        "Prefix": str,
    },
)

ViewerCertificateTypeDef = TypedDict(
    "ViewerCertificateTypeDef",
    {
        "CloudFrontDefaultCertificate": bool,
        "IAMCertificateId": str,
        "ACMCertificateArn": str,
        "SSLSupportMethod": SSLSupportMethodType,
        "MinimumProtocolVersion": MinimumProtocolVersionType,
        "Certificate": str,
        "CertificateSource": CertificateSourceType,
    },
    total=False,
)

_RequiredDistributionIdListTypeDef = TypedDict(
    "_RequiredDistributionIdListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
    },
)
_OptionalDistributionIdListTypeDef = TypedDict(
    "_OptionalDistributionIdListTypeDef",
    {
        "NextMarker": str,
        "Items": List[str],
    },
    total=False,
)


class DistributionIdListTypeDef(
    _RequiredDistributionIdListTypeDef, _OptionalDistributionIdListTypeDef
):
    pass


_RequiredFieldPatternsTypeDef = TypedDict(
    "_RequiredFieldPatternsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalFieldPatternsTypeDef = TypedDict(
    "_OptionalFieldPatternsTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class FieldPatternsTypeDef(_RequiredFieldPatternsTypeDef, _OptionalFieldPatternsTypeDef):
    pass


KinesisStreamConfigTypeDef = TypedDict(
    "KinesisStreamConfigTypeDef",
    {
        "RoleARN": str,
        "StreamARN": str,
    },
)

_RequiredQueryStringCacheKeysTypeDef = TypedDict(
    "_RequiredQueryStringCacheKeysTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalQueryStringCacheKeysTypeDef = TypedDict(
    "_OptionalQueryStringCacheKeysTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class QueryStringCacheKeysTypeDef(
    _RequiredQueryStringCacheKeysTypeDef, _OptionalQueryStringCacheKeysTypeDef
):
    pass


FunctionAssociationTypeDef = TypedDict(
    "FunctionAssociationTypeDef",
    {
        "FunctionARN": str,
        "EventType": EventTypeType,
    },
)

_RequiredFunctionMetadataTypeDef = TypedDict(
    "_RequiredFunctionMetadataTypeDef",
    {
        "FunctionARN": str,
        "LastModifiedTime": datetime,
    },
)
_OptionalFunctionMetadataTypeDef = TypedDict(
    "_OptionalFunctionMetadataTypeDef",
    {
        "Stage": FunctionStageType,
        "CreatedTime": datetime,
    },
    total=False,
)


class FunctionMetadataTypeDef(_RequiredFunctionMetadataTypeDef, _OptionalFunctionMetadataTypeDef):
    pass


_RequiredGeoRestrictionTypeDef = TypedDict(
    "_RequiredGeoRestrictionTypeDef",
    {
        "RestrictionType": GeoRestrictionTypeType,
        "Quantity": int,
    },
)
_OptionalGeoRestrictionTypeDef = TypedDict(
    "_OptionalGeoRestrictionTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class GeoRestrictionTypeDef(_RequiredGeoRestrictionTypeDef, _OptionalGeoRestrictionTypeDef):
    pass


GetCachePolicyConfigRequestRequestTypeDef = TypedDict(
    "GetCachePolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetCachePolicyRequestRequestTypeDef = TypedDict(
    "GetCachePolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetDistributionConfigRequestRequestTypeDef = TypedDict(
    "GetDistributionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

GetDistributionRequestRequestTypeDef = TypedDict(
    "GetDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetFieldLevelEncryptionRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredGetFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredGetFunctionRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalGetFunctionRequestRequestTypeDef",
    {
        "Stage": FunctionStageType,
    },
    total=False,
)


class GetFunctionRequestRequestTypeDef(
    _RequiredGetFunctionRequestRequestTypeDef, _OptionalGetFunctionRequestRequestTypeDef
):
    pass


GetInvalidationRequestRequestTypeDef = TypedDict(
    "GetInvalidationRequestRequestTypeDef",
    {
        "DistributionId": str,
        "Id": str,
    },
)

GetKeyGroupConfigRequestRequestTypeDef = TypedDict(
    "GetKeyGroupConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetKeyGroupRequestRequestTypeDef = TypedDict(
    "GetKeyGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "GetMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
    },
)

GetOriginRequestPolicyConfigRequestRequestTypeDef = TypedDict(
    "GetOriginRequestPolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "GetOriginRequestPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetPublicKeyConfigRequestRequestTypeDef = TypedDict(
    "GetPublicKeyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetPublicKeyRequestRequestTypeDef = TypedDict(
    "GetPublicKeyRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "GetRealtimeLogConfigRequestRequestTypeDef",
    {
        "Name": str,
        "ARN": str,
    },
    total=False,
)

GetResponseHeadersPolicyConfigRequestRequestTypeDef = TypedDict(
    "GetResponseHeadersPolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "GetResponseHeadersPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetStreamingDistributionConfigRequestRequestTypeDef = TypedDict(
    "GetStreamingDistributionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)

GetStreamingDistributionRequestRequestTypeDef = TypedDict(
    "GetStreamingDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredPathsTypeDef = TypedDict(
    "_RequiredPathsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalPathsTypeDef = TypedDict(
    "_OptionalPathsTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class PathsTypeDef(_RequiredPathsTypeDef, _OptionalPathsTypeDef):
    pass


InvalidationSummaryTypeDef = TypedDict(
    "InvalidationSummaryTypeDef",
    {
        "Id": str,
        "CreateTime": datetime,
        "Status": str,
    },
)

_RequiredKeyPairIdsTypeDef = TypedDict(
    "_RequiredKeyPairIdsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalKeyPairIdsTypeDef = TypedDict(
    "_OptionalKeyPairIdsTypeDef",
    {
        "Items": List[str],
    },
    total=False,
)


class KeyPairIdsTypeDef(_RequiredKeyPairIdsTypeDef, _OptionalKeyPairIdsTypeDef):
    pass


_RequiredLambdaFunctionAssociationTypeDef = TypedDict(
    "_RequiredLambdaFunctionAssociationTypeDef",
    {
        "LambdaFunctionARN": str,
        "EventType": EventTypeType,
    },
)
_OptionalLambdaFunctionAssociationTypeDef = TypedDict(
    "_OptionalLambdaFunctionAssociationTypeDef",
    {
        "IncludeBody": bool,
    },
    total=False,
)


class LambdaFunctionAssociationTypeDef(
    _RequiredLambdaFunctionAssociationTypeDef, _OptionalLambdaFunctionAssociationTypeDef
):
    pass


ListCachePoliciesRequestRequestTypeDef = TypedDict(
    "ListCachePoliciesRequestRequestTypeDef",
    {
        "Type": CachePolicyTypeType,
        "Marker": str,
        "MaxItems": str,
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

ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

_RequiredListConflictingAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListConflictingAliasesRequestRequestTypeDef",
    {
        "DistributionId": str,
        "Alias": str,
    },
)
_OptionalListConflictingAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListConflictingAliasesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListConflictingAliasesRequestRequestTypeDef(
    _RequiredListConflictingAliasesRequestRequestTypeDef,
    _OptionalListConflictingAliasesRequestRequestTypeDef,
):
    pass


_RequiredListDistributionsByCachePolicyIdRequestRequestTypeDef = TypedDict(
    "_RequiredListDistributionsByCachePolicyIdRequestRequestTypeDef",
    {
        "CachePolicyId": str,
    },
)
_OptionalListDistributionsByCachePolicyIdRequestRequestTypeDef = TypedDict(
    "_OptionalListDistributionsByCachePolicyIdRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListDistributionsByCachePolicyIdRequestRequestTypeDef(
    _RequiredListDistributionsByCachePolicyIdRequestRequestTypeDef,
    _OptionalListDistributionsByCachePolicyIdRequestRequestTypeDef,
):
    pass


_RequiredListDistributionsByKeyGroupRequestRequestTypeDef = TypedDict(
    "_RequiredListDistributionsByKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupId": str,
    },
)
_OptionalListDistributionsByKeyGroupRequestRequestTypeDef = TypedDict(
    "_OptionalListDistributionsByKeyGroupRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListDistributionsByKeyGroupRequestRequestTypeDef(
    _RequiredListDistributionsByKeyGroupRequestRequestTypeDef,
    _OptionalListDistributionsByKeyGroupRequestRequestTypeDef,
):
    pass


_RequiredListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef = TypedDict(
    "_RequiredListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    {
        "OriginRequestPolicyId": str,
    },
)
_OptionalListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef = TypedDict(
    "_OptionalListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef(
    _RequiredListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef,
    _OptionalListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef,
):
    pass


ListDistributionsByRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "ListDistributionsByRealtimeLogConfigRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
        "RealtimeLogConfigName": str,
        "RealtimeLogConfigArn": str,
    },
    total=False,
)

_RequiredListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef = TypedDict(
    "_RequiredListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyId": str,
    },
)
_OptionalListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef = TypedDict(
    "_OptionalListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef(
    _RequiredListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef,
    _OptionalListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef,
):
    pass


_RequiredListDistributionsByWebACLIdRequestRequestTypeDef = TypedDict(
    "_RequiredListDistributionsByWebACLIdRequestRequestTypeDef",
    {
        "WebACLId": str,
    },
)
_OptionalListDistributionsByWebACLIdRequestRequestTypeDef = TypedDict(
    "_OptionalListDistributionsByWebACLIdRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListDistributionsByWebACLIdRequestRequestTypeDef(
    _RequiredListDistributionsByWebACLIdRequestRequestTypeDef,
    _OptionalListDistributionsByWebACLIdRequestRequestTypeDef,
):
    pass


ListDistributionsRequestRequestTypeDef = TypedDict(
    "ListDistributionsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListFieldLevelEncryptionConfigsRequestRequestTypeDef = TypedDict(
    "ListFieldLevelEncryptionConfigsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListFieldLevelEncryptionProfilesRequestRequestTypeDef = TypedDict(
    "ListFieldLevelEncryptionProfilesRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListFunctionsRequestRequestTypeDef = TypedDict(
    "ListFunctionsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
        "Stage": FunctionStageType,
    },
    total=False,
)

_RequiredListInvalidationsRequestRequestTypeDef = TypedDict(
    "_RequiredListInvalidationsRequestRequestTypeDef",
    {
        "DistributionId": str,
    },
)
_OptionalListInvalidationsRequestRequestTypeDef = TypedDict(
    "_OptionalListInvalidationsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)


class ListInvalidationsRequestRequestTypeDef(
    _RequiredListInvalidationsRequestRequestTypeDef, _OptionalListInvalidationsRequestRequestTypeDef
):
    pass


ListKeyGroupsRequestRequestTypeDef = TypedDict(
    "ListKeyGroupsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListOriginRequestPoliciesRequestRequestTypeDef = TypedDict(
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    {
        "Type": OriginRequestPolicyTypeType,
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListPublicKeysRequestRequestTypeDef = TypedDict(
    "ListPublicKeysRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListRealtimeLogConfigsRequestRequestTypeDef = TypedDict(
    "ListRealtimeLogConfigsRequestRequestTypeDef",
    {
        "MaxItems": str,
        "Marker": str,
    },
    total=False,
)

ListResponseHeadersPoliciesRequestRequestTypeDef = TypedDict(
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    {
        "Type": ResponseHeadersPolicyTypeType,
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListStreamingDistributionsRequestRequestTypeDef = TypedDict(
    "ListStreamingDistributionsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Resource": str,
    },
)

RealtimeMetricsSubscriptionConfigTypeDef = TypedDict(
    "RealtimeMetricsSubscriptionConfigTypeDef",
    {
        "RealtimeMetricsSubscriptionStatus": RealtimeMetricsSubscriptionStatusType,
    },
)

StatusCodesTypeDef = TypedDict(
    "StatusCodesTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[int],
    },
)

OriginGroupMemberTypeDef = TypedDict(
    "OriginGroupMemberTypeDef",
    {
        "OriginId": str,
    },
)

_RequiredOriginShieldTypeDef = TypedDict(
    "_RequiredOriginShieldTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalOriginShieldTypeDef = TypedDict(
    "_OptionalOriginShieldTypeDef",
    {
        "OriginShieldRegion": str,
    },
    total=False,
)


class OriginShieldTypeDef(_RequiredOriginShieldTypeDef, _OptionalOriginShieldTypeDef):
    pass


S3OriginConfigTypeDef = TypedDict(
    "S3OriginConfigTypeDef",
    {
        "OriginAccessIdentity": str,
    },
)

_RequiredPublicKeySummaryTypeDef = TypedDict(
    "_RequiredPublicKeySummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "CreatedTime": datetime,
        "EncodedKey": str,
    },
)
_OptionalPublicKeySummaryTypeDef = TypedDict(
    "_OptionalPublicKeySummaryTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class PublicKeySummaryTypeDef(_RequiredPublicKeySummaryTypeDef, _OptionalPublicKeySummaryTypeDef):
    pass


PublishFunctionRequestRequestTypeDef = TypedDict(
    "PublishFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
    },
)

QueryArgProfileTypeDef = TypedDict(
    "QueryArgProfileTypeDef",
    {
        "QueryArg": str,
        "ProfileId": str,
    },
)

ResponseHeadersPolicyAccessControlAllowHeadersTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowHeadersTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[str],
    },
)

ResponseHeadersPolicyAccessControlAllowMethodsTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[ResponseHeadersPolicyAccessControlAllowMethodsValuesType],
    },
)

ResponseHeadersPolicyAccessControlAllowOriginsTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowOriginsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[str],
    },
)

_RequiredResponseHeadersPolicyAccessControlExposeHeadersTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalResponseHeadersPolicyAccessControlExposeHeadersTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)


class ResponseHeadersPolicyAccessControlExposeHeadersTypeDef(
    _RequiredResponseHeadersPolicyAccessControlExposeHeadersTypeDef,
    _OptionalResponseHeadersPolicyAccessControlExposeHeadersTypeDef,
):
    pass


_RequiredResponseHeadersPolicyServerTimingHeadersConfigTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalResponseHeadersPolicyServerTimingHeadersConfigTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    {
        "SamplingRate": float,
    },
    total=False,
)


class ResponseHeadersPolicyServerTimingHeadersConfigTypeDef(
    _RequiredResponseHeadersPolicyServerTimingHeadersConfigTypeDef,
    _OptionalResponseHeadersPolicyServerTimingHeadersConfigTypeDef,
):
    pass


ResponseHeadersPolicyContentSecurityPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyContentSecurityPolicyTypeDef",
    {
        "Override": bool,
        "ContentSecurityPolicy": str,
    },
)

ResponseHeadersPolicyContentTypeOptionsTypeDef = TypedDict(
    "ResponseHeadersPolicyContentTypeOptionsTypeDef",
    {
        "Override": bool,
    },
)

ResponseHeadersPolicyCustomHeaderTypeDef = TypedDict(
    "ResponseHeadersPolicyCustomHeaderTypeDef",
    {
        "Header": str,
        "Value": str,
        "Override": bool,
    },
)

ResponseHeadersPolicyFrameOptionsTypeDef = TypedDict(
    "ResponseHeadersPolicyFrameOptionsTypeDef",
    {
        "Override": bool,
        "FrameOption": FrameOptionsListType,
    },
)

ResponseHeadersPolicyReferrerPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyReferrerPolicyTypeDef",
    {
        "Override": bool,
        "ReferrerPolicy": ReferrerPolicyListType,
    },
)

_RequiredResponseHeadersPolicyStrictTransportSecurityTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyStrictTransportSecurityTypeDef",
    {
        "Override": bool,
        "AccessControlMaxAgeSec": int,
    },
)
_OptionalResponseHeadersPolicyStrictTransportSecurityTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyStrictTransportSecurityTypeDef",
    {
        "IncludeSubdomains": bool,
        "Preload": bool,
    },
    total=False,
)


class ResponseHeadersPolicyStrictTransportSecurityTypeDef(
    _RequiredResponseHeadersPolicyStrictTransportSecurityTypeDef,
    _OptionalResponseHeadersPolicyStrictTransportSecurityTypeDef,
):
    pass


_RequiredResponseHeadersPolicyXSSProtectionTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyXSSProtectionTypeDef",
    {
        "Override": bool,
        "Protection": bool,
    },
)
_OptionalResponseHeadersPolicyXSSProtectionTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyXSSProtectionTypeDef",
    {
        "ModeBlock": bool,
        "ReportUri": str,
    },
    total=False,
)


class ResponseHeadersPolicyXSSProtectionTypeDef(
    _RequiredResponseHeadersPolicyXSSProtectionTypeDef,
    _OptionalResponseHeadersPolicyXSSProtectionTypeDef,
):
    pass


S3OriginTypeDef = TypedDict(
    "S3OriginTypeDef",
    {
        "DomainName": str,
        "OriginAccessIdentity": str,
    },
)

StreamingLoggingConfigTypeDef = TypedDict(
    "StreamingLoggingConfigTypeDef",
    {
        "Enabled": bool,
        "Bucket": str,
        "Prefix": str,
    },
)

TagKeysTypeDef = TypedDict(
    "TagKeysTypeDef",
    {
        "Items": Sequence[str],
    },
    total=False,
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


_RequiredTestFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredTestFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
        "EventObject": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalTestFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalTestFunctionRequestRequestTypeDef",
    {
        "Stage": FunctionStageType,
    },
    total=False,
)


class TestFunctionRequestRequestTypeDef(
    _RequiredTestFunctionRequestRequestTypeDef, _OptionalTestFunctionRequestRequestTypeDef
):
    pass


_RequiredAllowedMethodsTypeDef = TypedDict(
    "_RequiredAllowedMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[MethodType],
    },
)
_OptionalAllowedMethodsTypeDef = TypedDict(
    "_OptionalAllowedMethodsTypeDef",
    {
        "CachedMethods": CachedMethodsTypeDef,
    },
    total=False,
)


class AllowedMethodsTypeDef(_RequiredAllowedMethodsTypeDef, _OptionalAllowedMethodsTypeDef):
    pass


_RequiredCachePolicyCookiesConfigTypeDef = TypedDict(
    "_RequiredCachePolicyCookiesConfigTypeDef",
    {
        "CookieBehavior": CachePolicyCookieBehaviorType,
    },
)
_OptionalCachePolicyCookiesConfigTypeDef = TypedDict(
    "_OptionalCachePolicyCookiesConfigTypeDef",
    {
        "Cookies": CookieNamesTypeDef,
    },
    total=False,
)


class CachePolicyCookiesConfigTypeDef(
    _RequiredCachePolicyCookiesConfigTypeDef, _OptionalCachePolicyCookiesConfigTypeDef
):
    pass


_RequiredCookiePreferenceTypeDef = TypedDict(
    "_RequiredCookiePreferenceTypeDef",
    {
        "Forward": ItemSelectionType,
    },
)
_OptionalCookiePreferenceTypeDef = TypedDict(
    "_OptionalCookiePreferenceTypeDef",
    {
        "WhitelistedNames": CookieNamesTypeDef,
    },
    total=False,
)


class CookiePreferenceTypeDef(_RequiredCookiePreferenceTypeDef, _OptionalCookiePreferenceTypeDef):
    pass


_RequiredOriginRequestPolicyCookiesConfigTypeDef = TypedDict(
    "_RequiredOriginRequestPolicyCookiesConfigTypeDef",
    {
        "CookieBehavior": OriginRequestPolicyCookieBehaviorType,
    },
)
_OptionalOriginRequestPolicyCookiesConfigTypeDef = TypedDict(
    "_OptionalOriginRequestPolicyCookiesConfigTypeDef",
    {
        "Cookies": CookieNamesTypeDef,
    },
    total=False,
)


class OriginRequestPolicyCookiesConfigTypeDef(
    _RequiredOriginRequestPolicyCookiesConfigTypeDef,
    _OptionalOriginRequestPolicyCookiesConfigTypeDef,
):
    pass


_RequiredCachePolicyHeadersConfigTypeDef = TypedDict(
    "_RequiredCachePolicyHeadersConfigTypeDef",
    {
        "HeaderBehavior": CachePolicyHeaderBehaviorType,
    },
)
_OptionalCachePolicyHeadersConfigTypeDef = TypedDict(
    "_OptionalCachePolicyHeadersConfigTypeDef",
    {
        "Headers": HeadersTypeDef,
    },
    total=False,
)


class CachePolicyHeadersConfigTypeDef(
    _RequiredCachePolicyHeadersConfigTypeDef, _OptionalCachePolicyHeadersConfigTypeDef
):
    pass


_RequiredOriginRequestPolicyHeadersConfigTypeDef = TypedDict(
    "_RequiredOriginRequestPolicyHeadersConfigTypeDef",
    {
        "HeaderBehavior": OriginRequestPolicyHeaderBehaviorType,
    },
)
_OptionalOriginRequestPolicyHeadersConfigTypeDef = TypedDict(
    "_OptionalOriginRequestPolicyHeadersConfigTypeDef",
    {
        "Headers": HeadersTypeDef,
    },
    total=False,
)


class OriginRequestPolicyHeadersConfigTypeDef(
    _RequiredOriginRequestPolicyHeadersConfigTypeDef,
    _OptionalOriginRequestPolicyHeadersConfigTypeDef,
):
    pass


_RequiredCachePolicyQueryStringsConfigTypeDef = TypedDict(
    "_RequiredCachePolicyQueryStringsConfigTypeDef",
    {
        "QueryStringBehavior": CachePolicyQueryStringBehaviorType,
    },
)
_OptionalCachePolicyQueryStringsConfigTypeDef = TypedDict(
    "_OptionalCachePolicyQueryStringsConfigTypeDef",
    {
        "QueryStrings": QueryStringNamesTypeDef,
    },
    total=False,
)


class CachePolicyQueryStringsConfigTypeDef(
    _RequiredCachePolicyQueryStringsConfigTypeDef, _OptionalCachePolicyQueryStringsConfigTypeDef
):
    pass


_RequiredOriginRequestPolicyQueryStringsConfigTypeDef = TypedDict(
    "_RequiredOriginRequestPolicyQueryStringsConfigTypeDef",
    {
        "QueryStringBehavior": OriginRequestPolicyQueryStringBehaviorType,
    },
)
_OptionalOriginRequestPolicyQueryStringsConfigTypeDef = TypedDict(
    "_OptionalOriginRequestPolicyQueryStringsConfigTypeDef",
    {
        "QueryStrings": QueryStringNamesTypeDef,
    },
    total=False,
)


class OriginRequestPolicyQueryStringsConfigTypeDef(
    _RequiredOriginRequestPolicyQueryStringsConfigTypeDef,
    _OptionalOriginRequestPolicyQueryStringsConfigTypeDef,
):
    pass


_RequiredCloudFrontOriginAccessIdentityTypeDef = TypedDict(
    "_RequiredCloudFrontOriginAccessIdentityTypeDef",
    {
        "Id": str,
        "S3CanonicalUserId": str,
    },
)
_OptionalCloudFrontOriginAccessIdentityTypeDef = TypedDict(
    "_OptionalCloudFrontOriginAccessIdentityTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
    },
    total=False,
)


class CloudFrontOriginAccessIdentityTypeDef(
    _RequiredCloudFrontOriginAccessIdentityTypeDef, _OptionalCloudFrontOriginAccessIdentityTypeDef
):
    pass


CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
    },
)

_RequiredUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef(
    _RequiredUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    _OptionalUpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef,
):
    pass


_RequiredCloudFrontOriginAccessIdentityListTypeDef = TypedDict(
    "_RequiredCloudFrontOriginAccessIdentityListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
    },
)
_OptionalCloudFrontOriginAccessIdentityListTypeDef = TypedDict(
    "_OptionalCloudFrontOriginAccessIdentityListTypeDef",
    {
        "NextMarker": str,
        "Items": List[CloudFrontOriginAccessIdentitySummaryTypeDef],
    },
    total=False,
)


class CloudFrontOriginAccessIdentityListTypeDef(
    _RequiredCloudFrontOriginAccessIdentityListTypeDef,
    _OptionalCloudFrontOriginAccessIdentityListTypeDef,
):
    pass


ConflictingAliasesListTypeDef = TypedDict(
    "ConflictingAliasesListTypeDef",
    {
        "NextMarker": str,
        "MaxItems": int,
        "Quantity": int,
        "Items": List[ConflictingAliasTypeDef],
    },
    total=False,
)

_RequiredContentTypeProfilesTypeDef = TypedDict(
    "_RequiredContentTypeProfilesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalContentTypeProfilesTypeDef = TypedDict(
    "_OptionalContentTypeProfilesTypeDef",
    {
        "Items": Sequence[ContentTypeProfileTypeDef],
    },
    total=False,
)


class ContentTypeProfilesTypeDef(
    _RequiredContentTypeProfilesTypeDef, _OptionalContentTypeProfilesTypeDef
):
    pass


EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCloudFrontOriginAccessIdentityConfigResultTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityConfigResultTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFunctionResultTypeDef = TypedDict(
    "GetFunctionResultTypeDef",
    {
        "FunctionCode": StreamingBody,
        "ETag": str,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFunctionRequestRequestTypeDef = TypedDict(
    "CreateFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "FunctionConfig": FunctionConfigTypeDef,
        "FunctionCode": Union[str, bytes, IO[Any], StreamingBody],
    },
)

UpdateFunctionRequestRequestTypeDef = TypedDict(
    "UpdateFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
        "FunctionConfig": FunctionConfigTypeDef,
        "FunctionCode": Union[str, bytes, IO[Any], StreamingBody],
    },
)

CreateKeyGroupRequestRequestTypeDef = TypedDict(
    "CreateKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigTypeDef,
    },
)

GetKeyGroupConfigResultTypeDef = TypedDict(
    "GetKeyGroupConfigResultTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KeyGroupTypeDef = TypedDict(
    "KeyGroupTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "KeyGroupConfig": KeyGroupConfigTypeDef,
    },
)

_RequiredUpdateKeyGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateKeyGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKeyGroupRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateKeyGroupRequestRequestTypeDef(
    _RequiredUpdateKeyGroupRequestRequestTypeDef, _OptionalUpdateKeyGroupRequestRequestTypeDef
):
    pass


CreatePublicKeyRequestRequestTypeDef = TypedDict(
    "CreatePublicKeyRequestRequestTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
    },
)

GetPublicKeyConfigResultTypeDef = TypedDict(
    "GetPublicKeyConfigResultTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublicKeyTypeDef = TypedDict(
    "PublicKeyTypeDef",
    {
        "Id": str,
        "CreatedTime": datetime,
        "PublicKeyConfig": PublicKeyConfigTypeDef,
    },
)

_RequiredUpdatePublicKeyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePublicKeyRequestRequestTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdatePublicKeyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePublicKeyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdatePublicKeyRequestRequestTypeDef(
    _RequiredUpdatePublicKeyRequestRequestTypeDef, _OptionalUpdatePublicKeyRequestRequestTypeDef
):
    pass


_RequiredCustomErrorResponsesTypeDef = TypedDict(
    "_RequiredCustomErrorResponsesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalCustomErrorResponsesTypeDef = TypedDict(
    "_OptionalCustomErrorResponsesTypeDef",
    {
        "Items": Sequence[CustomErrorResponseTypeDef],
    },
    total=False,
)


class CustomErrorResponsesTypeDef(
    _RequiredCustomErrorResponsesTypeDef, _OptionalCustomErrorResponsesTypeDef
):
    pass


_RequiredCustomHeadersTypeDef = TypedDict(
    "_RequiredCustomHeadersTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalCustomHeadersTypeDef = TypedDict(
    "_OptionalCustomHeadersTypeDef",
    {
        "Items": Sequence[OriginCustomHeaderTypeDef],
    },
    total=False,
)


class CustomHeadersTypeDef(_RequiredCustomHeadersTypeDef, _OptionalCustomHeadersTypeDef):
    pass


_RequiredCustomOriginConfigTypeDef = TypedDict(
    "_RequiredCustomOriginConfigTypeDef",
    {
        "HTTPPort": int,
        "HTTPSPort": int,
        "OriginProtocolPolicy": OriginProtocolPolicyType,
    },
)
_OptionalCustomOriginConfigTypeDef = TypedDict(
    "_OptionalCustomOriginConfigTypeDef",
    {
        "OriginSslProtocols": OriginSslProtocolsTypeDef,
        "OriginReadTimeout": int,
        "OriginKeepaliveTimeout": int,
    },
    total=False,
)


class CustomOriginConfigTypeDef(
    _RequiredCustomOriginConfigTypeDef, _OptionalCustomOriginConfigTypeDef
):
    pass


ListDistributionsByCachePolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByCachePolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsByKeyGroupResultTypeDef = TypedDict(
    "ListDistributionsByKeyGroupResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsByOriginRequestPolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByOriginRequestPolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsByResponseHeadersPolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByResponseHeadersPolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptionEntityTypeDef = TypedDict(
    "EncryptionEntityTypeDef",
    {
        "PublicKeyId": str,
        "ProviderId": str,
        "FieldPatterns": FieldPatternsTypeDef,
    },
)

_RequiredEndPointTypeDef = TypedDict(
    "_RequiredEndPointTypeDef",
    {
        "StreamType": str,
    },
)
_OptionalEndPointTypeDef = TypedDict(
    "_OptionalEndPointTypeDef",
    {
        "KinesisStreamConfig": KinesisStreamConfigTypeDef,
    },
    total=False,
)


class EndPointTypeDef(_RequiredEndPointTypeDef, _OptionalEndPointTypeDef):
    pass


_RequiredFunctionAssociationsTypeDef = TypedDict(
    "_RequiredFunctionAssociationsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalFunctionAssociationsTypeDef = TypedDict(
    "_OptionalFunctionAssociationsTypeDef",
    {
        "Items": Sequence[FunctionAssociationTypeDef],
    },
    total=False,
)


class FunctionAssociationsTypeDef(
    _RequiredFunctionAssociationsTypeDef, _OptionalFunctionAssociationsTypeDef
):
    pass


_RequiredFunctionSummaryTypeDef = TypedDict(
    "_RequiredFunctionSummaryTypeDef",
    {
        "Name": str,
        "FunctionConfig": FunctionConfigTypeDef,
        "FunctionMetadata": FunctionMetadataTypeDef,
    },
)
_OptionalFunctionSummaryTypeDef = TypedDict(
    "_OptionalFunctionSummaryTypeDef",
    {
        "Status": str,
    },
    total=False,
)


class FunctionSummaryTypeDef(_RequiredFunctionSummaryTypeDef, _OptionalFunctionSummaryTypeDef):
    pass


RestrictionsTypeDef = TypedDict(
    "RestrictionsTypeDef",
    {
        "GeoRestriction": GeoRestrictionTypeDef,
    },
)

_RequiredGetDistributionRequestDistributionDeployedWaitTypeDef = TypedDict(
    "_RequiredGetDistributionRequestDistributionDeployedWaitTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetDistributionRequestDistributionDeployedWaitTypeDef = TypedDict(
    "_OptionalGetDistributionRequestDistributionDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetDistributionRequestDistributionDeployedWaitTypeDef(
    _RequiredGetDistributionRequestDistributionDeployedWaitTypeDef,
    _OptionalGetDistributionRequestDistributionDeployedWaitTypeDef,
):
    pass


_RequiredGetInvalidationRequestInvalidationCompletedWaitTypeDef = TypedDict(
    "_RequiredGetInvalidationRequestInvalidationCompletedWaitTypeDef",
    {
        "DistributionId": str,
        "Id": str,
    },
)
_OptionalGetInvalidationRequestInvalidationCompletedWaitTypeDef = TypedDict(
    "_OptionalGetInvalidationRequestInvalidationCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetInvalidationRequestInvalidationCompletedWaitTypeDef(
    _RequiredGetInvalidationRequestInvalidationCompletedWaitTypeDef,
    _OptionalGetInvalidationRequestInvalidationCompletedWaitTypeDef,
):
    pass


_RequiredGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef = TypedDict(
    "_RequiredGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef = TypedDict(
    "_OptionalGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef(
    _RequiredGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef,
    _OptionalGetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef,
):
    pass


InvalidationBatchTypeDef = TypedDict(
    "InvalidationBatchTypeDef",
    {
        "Paths": PathsTypeDef,
        "CallerReference": str,
    },
)

_RequiredInvalidationListTypeDef = TypedDict(
    "_RequiredInvalidationListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
    },
)
_OptionalInvalidationListTypeDef = TypedDict(
    "_OptionalInvalidationListTypeDef",
    {
        "NextMarker": str,
        "Items": List[InvalidationSummaryTypeDef],
    },
    total=False,
)


class InvalidationListTypeDef(_RequiredInvalidationListTypeDef, _OptionalInvalidationListTypeDef):
    pass


KGKeyPairIdsTypeDef = TypedDict(
    "KGKeyPairIdsTypeDef",
    {
        "KeyGroupId": str,
        "KeyPairIds": KeyPairIdsTypeDef,
    },
    total=False,
)

SignerTypeDef = TypedDict(
    "SignerTypeDef",
    {
        "AwsAccountNumber": str,
        "KeyPairIds": KeyPairIdsTypeDef,
    },
    total=False,
)

_RequiredLambdaFunctionAssociationsTypeDef = TypedDict(
    "_RequiredLambdaFunctionAssociationsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalLambdaFunctionAssociationsTypeDef = TypedDict(
    "_OptionalLambdaFunctionAssociationsTypeDef",
    {
        "Items": Sequence[LambdaFunctionAssociationTypeDef],
    },
    total=False,
)


class LambdaFunctionAssociationsTypeDef(
    _RequiredLambdaFunctionAssociationsTypeDef, _OptionalLambdaFunctionAssociationsTypeDef
):
    pass


ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDistributionsRequestListDistributionsPaginateTypeDef = TypedDict(
    "ListDistributionsRequestListDistributionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListInvalidationsRequestListInvalidationsPaginateTypeDef = TypedDict(
    "_RequiredListInvalidationsRequestListInvalidationsPaginateTypeDef",
    {
        "DistributionId": str,
    },
)
_OptionalListInvalidationsRequestListInvalidationsPaginateTypeDef = TypedDict(
    "_OptionalListInvalidationsRequestListInvalidationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListInvalidationsRequestListInvalidationsPaginateTypeDef(
    _RequiredListInvalidationsRequestListInvalidationsPaginateTypeDef,
    _OptionalListInvalidationsRequestListInvalidationsPaginateTypeDef,
):
    pass


ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef = TypedDict(
    "ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

MonitoringSubscriptionTypeDef = TypedDict(
    "MonitoringSubscriptionTypeDef",
    {
        "RealtimeMetricsSubscriptionConfig": RealtimeMetricsSubscriptionConfigTypeDef,
    },
    total=False,
)

OriginGroupFailoverCriteriaTypeDef = TypedDict(
    "OriginGroupFailoverCriteriaTypeDef",
    {
        "StatusCodes": StatusCodesTypeDef,
    },
)

OriginGroupMembersTypeDef = TypedDict(
    "OriginGroupMembersTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[OriginGroupMemberTypeDef],
    },
)

_RequiredPublicKeyListTypeDef = TypedDict(
    "_RequiredPublicKeyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalPublicKeyListTypeDef = TypedDict(
    "_OptionalPublicKeyListTypeDef",
    {
        "NextMarker": str,
        "Items": List[PublicKeySummaryTypeDef],
    },
    total=False,
)


class PublicKeyListTypeDef(_RequiredPublicKeyListTypeDef, _OptionalPublicKeyListTypeDef):
    pass


_RequiredQueryArgProfilesTypeDef = TypedDict(
    "_RequiredQueryArgProfilesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalQueryArgProfilesTypeDef = TypedDict(
    "_OptionalQueryArgProfilesTypeDef",
    {
        "Items": Sequence[QueryArgProfileTypeDef],
    },
    total=False,
)


class QueryArgProfilesTypeDef(_RequiredQueryArgProfilesTypeDef, _OptionalQueryArgProfilesTypeDef):
    pass


_RequiredResponseHeadersPolicyCorsConfigTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyCorsConfigTypeDef",
    {
        "AccessControlAllowOrigins": ResponseHeadersPolicyAccessControlAllowOriginsTypeDef,
        "AccessControlAllowHeaders": ResponseHeadersPolicyAccessControlAllowHeadersTypeDef,
        "AccessControlAllowMethods": ResponseHeadersPolicyAccessControlAllowMethodsTypeDef,
        "AccessControlAllowCredentials": bool,
        "OriginOverride": bool,
    },
)
_OptionalResponseHeadersPolicyCorsConfigTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyCorsConfigTypeDef",
    {
        "AccessControlExposeHeaders": ResponseHeadersPolicyAccessControlExposeHeadersTypeDef,
        "AccessControlMaxAgeSec": int,
    },
    total=False,
)


class ResponseHeadersPolicyCorsConfigTypeDef(
    _RequiredResponseHeadersPolicyCorsConfigTypeDef, _OptionalResponseHeadersPolicyCorsConfigTypeDef
):
    pass


_RequiredResponseHeadersPolicyCustomHeadersConfigTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyCustomHeadersConfigTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalResponseHeadersPolicyCustomHeadersConfigTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyCustomHeadersConfigTypeDef",
    {
        "Items": Sequence[ResponseHeadersPolicyCustomHeaderTypeDef],
    },
    total=False,
)


class ResponseHeadersPolicyCustomHeadersConfigTypeDef(
    _RequiredResponseHeadersPolicyCustomHeadersConfigTypeDef,
    _OptionalResponseHeadersPolicyCustomHeadersConfigTypeDef,
):
    pass


ResponseHeadersPolicySecurityHeadersConfigTypeDef = TypedDict(
    "ResponseHeadersPolicySecurityHeadersConfigTypeDef",
    {
        "XSSProtection": ResponseHeadersPolicyXSSProtectionTypeDef,
        "FrameOptions": ResponseHeadersPolicyFrameOptionsTypeDef,
        "ReferrerPolicy": ResponseHeadersPolicyReferrerPolicyTypeDef,
        "ContentSecurityPolicy": ResponseHeadersPolicyContentSecurityPolicyTypeDef,
        "ContentTypeOptions": ResponseHeadersPolicyContentTypeOptionsTypeDef,
        "StrictTransportSecurity": ResponseHeadersPolicyStrictTransportSecurityTypeDef,
    },
    total=False,
)

StreamingDistributionSummaryTypeDef = TypedDict(
    "StreamingDistributionSummaryTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "DomainName": str,
        "S3Origin": S3OriginTypeDef,
        "Aliases": AliasesTypeDef,
        "TrustedSigners": TrustedSignersTypeDef,
        "Comment": str,
        "PriceClass": PriceClassType,
        "Enabled": bool,
    },
)

_RequiredStreamingDistributionConfigTypeDef = TypedDict(
    "_RequiredStreamingDistributionConfigTypeDef",
    {
        "CallerReference": str,
        "S3Origin": S3OriginTypeDef,
        "Comment": str,
        "TrustedSigners": TrustedSignersTypeDef,
        "Enabled": bool,
    },
)
_OptionalStreamingDistributionConfigTypeDef = TypedDict(
    "_OptionalStreamingDistributionConfigTypeDef",
    {
        "Aliases": AliasesTypeDef,
        "Logging": StreamingLoggingConfigTypeDef,
        "PriceClass": PriceClassType,
    },
    total=False,
)


class StreamingDistributionConfigTypeDef(
    _RequiredStreamingDistributionConfigTypeDef, _OptionalStreamingDistributionConfigTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "TagKeys": TagKeysTypeDef,
    },
)

TagsTypeDef = TypedDict(
    "TagsTypeDef",
    {
        "Items": Sequence[TagTypeDef],
    },
    total=False,
)

_RequiredForwardedValuesTypeDef = TypedDict(
    "_RequiredForwardedValuesTypeDef",
    {
        "QueryString": bool,
        "Cookies": CookiePreferenceTypeDef,
    },
)
_OptionalForwardedValuesTypeDef = TypedDict(
    "_OptionalForwardedValuesTypeDef",
    {
        "Headers": HeadersTypeDef,
        "QueryStringCacheKeys": QueryStringCacheKeysTypeDef,
    },
    total=False,
)


class ForwardedValuesTypeDef(_RequiredForwardedValuesTypeDef, _OptionalForwardedValuesTypeDef):
    pass


_RequiredParametersInCacheKeyAndForwardedToOriginTypeDef = TypedDict(
    "_RequiredParametersInCacheKeyAndForwardedToOriginTypeDef",
    {
        "EnableAcceptEncodingGzip": bool,
        "HeadersConfig": CachePolicyHeadersConfigTypeDef,
        "CookiesConfig": CachePolicyCookiesConfigTypeDef,
        "QueryStringsConfig": CachePolicyQueryStringsConfigTypeDef,
    },
)
_OptionalParametersInCacheKeyAndForwardedToOriginTypeDef = TypedDict(
    "_OptionalParametersInCacheKeyAndForwardedToOriginTypeDef",
    {
        "EnableAcceptEncodingBrotli": bool,
    },
    total=False,
)


class ParametersInCacheKeyAndForwardedToOriginTypeDef(
    _RequiredParametersInCacheKeyAndForwardedToOriginTypeDef,
    _OptionalParametersInCacheKeyAndForwardedToOriginTypeDef,
):
    pass


_RequiredOriginRequestPolicyConfigTypeDef = TypedDict(
    "_RequiredOriginRequestPolicyConfigTypeDef",
    {
        "Name": str,
        "HeadersConfig": OriginRequestPolicyHeadersConfigTypeDef,
        "CookiesConfig": OriginRequestPolicyCookiesConfigTypeDef,
        "QueryStringsConfig": OriginRequestPolicyQueryStringsConfigTypeDef,
    },
)
_OptionalOriginRequestPolicyConfigTypeDef = TypedDict(
    "_OptionalOriginRequestPolicyConfigTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class OriginRequestPolicyConfigTypeDef(
    _RequiredOriginRequestPolicyConfigTypeDef, _OptionalOriginRequestPolicyConfigTypeDef
):
    pass


CreateCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "CreateCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "UpdateCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCloudFrontOriginAccessIdentitiesResultTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesResultTypeDef",
    {
        "CloudFrontOriginAccessIdentityList": CloudFrontOriginAccessIdentityListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConflictingAliasesResultTypeDef = TypedDict(
    "ListConflictingAliasesResultTypeDef",
    {
        "ConflictingAliasesList": ConflictingAliasesListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredContentTypeProfileConfigTypeDef = TypedDict(
    "_RequiredContentTypeProfileConfigTypeDef",
    {
        "ForwardWhenContentTypeIsUnknown": bool,
    },
)
_OptionalContentTypeProfileConfigTypeDef = TypedDict(
    "_OptionalContentTypeProfileConfigTypeDef",
    {
        "ContentTypeProfiles": ContentTypeProfilesTypeDef,
    },
    total=False,
)


class ContentTypeProfileConfigTypeDef(
    _RequiredContentTypeProfileConfigTypeDef, _OptionalContentTypeProfileConfigTypeDef
):
    pass


CreateKeyGroupResultTypeDef = TypedDict(
    "CreateKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKeyGroupResultTypeDef = TypedDict(
    "GetKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KeyGroupSummaryTypeDef = TypedDict(
    "KeyGroupSummaryTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
    },
)

UpdateKeyGroupResultTypeDef = TypedDict(
    "UpdateKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePublicKeyResultTypeDef = TypedDict(
    "CreatePublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPublicKeyResultTypeDef = TypedDict(
    "GetPublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePublicKeyResultTypeDef = TypedDict(
    "UpdatePublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredOriginTypeDef = TypedDict(
    "_RequiredOriginTypeDef",
    {
        "Id": str,
        "DomainName": str,
    },
)
_OptionalOriginTypeDef = TypedDict(
    "_OptionalOriginTypeDef",
    {
        "OriginPath": str,
        "CustomHeaders": CustomHeadersTypeDef,
        "S3OriginConfig": S3OriginConfigTypeDef,
        "CustomOriginConfig": CustomOriginConfigTypeDef,
        "ConnectionAttempts": int,
        "ConnectionTimeout": int,
        "OriginShield": OriginShieldTypeDef,
    },
    total=False,
)


class OriginTypeDef(_RequiredOriginTypeDef, _OptionalOriginTypeDef):
    pass


_RequiredEncryptionEntitiesTypeDef = TypedDict(
    "_RequiredEncryptionEntitiesTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalEncryptionEntitiesTypeDef = TypedDict(
    "_OptionalEncryptionEntitiesTypeDef",
    {
        "Items": Sequence[EncryptionEntityTypeDef],
    },
    total=False,
)


class EncryptionEntitiesTypeDef(
    _RequiredEncryptionEntitiesTypeDef, _OptionalEncryptionEntitiesTypeDef
):
    pass


CreateRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "CreateRealtimeLogConfigRequestRequestTypeDef",
    {
        "EndPoints": Sequence[EndPointTypeDef],
        "Fields": Sequence[str],
        "Name": str,
        "SamplingRate": int,
    },
)

RealtimeLogConfigTypeDef = TypedDict(
    "RealtimeLogConfigTypeDef",
    {
        "ARN": str,
        "Name": str,
        "SamplingRate": int,
        "EndPoints": List[EndPointTypeDef],
        "Fields": List[str],
    },
)

UpdateRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "UpdateRealtimeLogConfigRequestRequestTypeDef",
    {
        "EndPoints": Sequence[EndPointTypeDef],
        "Fields": Sequence[str],
        "Name": str,
        "ARN": str,
        "SamplingRate": int,
    },
    total=False,
)

CreateFunctionResultTypeDef = TypedDict(
    "CreateFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFunctionResultTypeDef = TypedDict(
    "DescribeFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFunctionListTypeDef = TypedDict(
    "_RequiredFunctionListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalFunctionListTypeDef = TypedDict(
    "_OptionalFunctionListTypeDef",
    {
        "NextMarker": str,
        "Items": List[FunctionSummaryTypeDef],
    },
    total=False,
)


class FunctionListTypeDef(_RequiredFunctionListTypeDef, _OptionalFunctionListTypeDef):
    pass


PublishFunctionResultTypeDef = TypedDict(
    "PublishFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestResultTypeDef = TypedDict(
    "TestResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ComputeUtilization": str,
        "FunctionExecutionLogs": List[str],
        "FunctionErrorMessage": str,
        "FunctionOutput": str,
    },
    total=False,
)

UpdateFunctionResultTypeDef = TypedDict(
    "UpdateFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInvalidationRequestRequestTypeDef = TypedDict(
    "CreateInvalidationRequestRequestTypeDef",
    {
        "DistributionId": str,
        "InvalidationBatch": InvalidationBatchTypeDef,
    },
)

InvalidationTypeDef = TypedDict(
    "InvalidationTypeDef",
    {
        "Id": str,
        "Status": str,
        "CreateTime": datetime,
        "InvalidationBatch": InvalidationBatchTypeDef,
    },
)

ListInvalidationsResultTypeDef = TypedDict(
    "ListInvalidationsResultTypeDef",
    {
        "InvalidationList": InvalidationListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredActiveTrustedKeyGroupsTypeDef = TypedDict(
    "_RequiredActiveTrustedKeyGroupsTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
    },
)
_OptionalActiveTrustedKeyGroupsTypeDef = TypedDict(
    "_OptionalActiveTrustedKeyGroupsTypeDef",
    {
        "Items": List[KGKeyPairIdsTypeDef],
    },
    total=False,
)


class ActiveTrustedKeyGroupsTypeDef(
    _RequiredActiveTrustedKeyGroupsTypeDef, _OptionalActiveTrustedKeyGroupsTypeDef
):
    pass


_RequiredActiveTrustedSignersTypeDef = TypedDict(
    "_RequiredActiveTrustedSignersTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
    },
)
_OptionalActiveTrustedSignersTypeDef = TypedDict(
    "_OptionalActiveTrustedSignersTypeDef",
    {
        "Items": List[SignerTypeDef],
    },
    total=False,
)


class ActiveTrustedSignersTypeDef(
    _RequiredActiveTrustedSignersTypeDef, _OptionalActiveTrustedSignersTypeDef
):
    pass


CreateMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
    },
)

CreateMonitoringSubscriptionResultTypeDef = TypedDict(
    "CreateMonitoringSubscriptionResultTypeDef",
    {
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMonitoringSubscriptionResultTypeDef = TypedDict(
    "GetMonitoringSubscriptionResultTypeDef",
    {
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OriginGroupTypeDef = TypedDict(
    "OriginGroupTypeDef",
    {
        "Id": str,
        "FailoverCriteria": OriginGroupFailoverCriteriaTypeDef,
        "Members": OriginGroupMembersTypeDef,
    },
)

ListPublicKeysResultTypeDef = TypedDict(
    "ListPublicKeysResultTypeDef",
    {
        "PublicKeyList": PublicKeyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredQueryArgProfileConfigTypeDef = TypedDict(
    "_RequiredQueryArgProfileConfigTypeDef",
    {
        "ForwardWhenQueryArgProfileIsUnknown": bool,
    },
)
_OptionalQueryArgProfileConfigTypeDef = TypedDict(
    "_OptionalQueryArgProfileConfigTypeDef",
    {
        "QueryArgProfiles": QueryArgProfilesTypeDef,
    },
    total=False,
)


class QueryArgProfileConfigTypeDef(
    _RequiredQueryArgProfileConfigTypeDef, _OptionalQueryArgProfileConfigTypeDef
):
    pass


_RequiredResponseHeadersPolicyConfigTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyConfigTypeDef",
    {
        "Name": str,
    },
)
_OptionalResponseHeadersPolicyConfigTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyConfigTypeDef",
    {
        "Comment": str,
        "CorsConfig": ResponseHeadersPolicyCorsConfigTypeDef,
        "SecurityHeadersConfig": ResponseHeadersPolicySecurityHeadersConfigTypeDef,
        "CustomHeadersConfig": ResponseHeadersPolicyCustomHeadersConfigTypeDef,
        "ServerTimingHeadersConfig": ResponseHeadersPolicyServerTimingHeadersConfigTypeDef,
    },
    total=False,
)


class ResponseHeadersPolicyConfigTypeDef(
    _RequiredResponseHeadersPolicyConfigTypeDef, _OptionalResponseHeadersPolicyConfigTypeDef
):
    pass


_RequiredStreamingDistributionListTypeDef = TypedDict(
    "_RequiredStreamingDistributionListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
    },
)
_OptionalStreamingDistributionListTypeDef = TypedDict(
    "_OptionalStreamingDistributionListTypeDef",
    {
        "NextMarker": str,
        "Items": List[StreamingDistributionSummaryTypeDef],
    },
    total=False,
)


class StreamingDistributionListTypeDef(
    _RequiredStreamingDistributionListTypeDef, _OptionalStreamingDistributionListTypeDef
):
    pass


CreateStreamingDistributionRequestRequestTypeDef = TypedDict(
    "CreateStreamingDistributionRequestRequestTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
    },
)

GetStreamingDistributionConfigResultTypeDef = TypedDict(
    "GetStreamingDistributionConfigResultTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateStreamingDistributionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStreamingDistributionRequestRequestTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateStreamingDistributionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStreamingDistributionRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateStreamingDistributionRequestRequestTypeDef(
    _RequiredUpdateStreamingDistributionRequestRequestTypeDef,
    _OptionalUpdateStreamingDistributionRequestRequestTypeDef,
):
    pass


ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "Tags": TagsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StreamingDistributionConfigWithTagsTypeDef = TypedDict(
    "StreamingDistributionConfigWithTagsTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
        "Tags": TagsTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "Tags": TagsTypeDef,
    },
)

_RequiredCacheBehaviorTypeDef = TypedDict(
    "_RequiredCacheBehaviorTypeDef",
    {
        "PathPattern": str,
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
    },
)
_OptionalCacheBehaviorTypeDef = TypedDict(
    "_OptionalCacheBehaviorTypeDef",
    {
        "TrustedSigners": TrustedSignersTypeDef,
        "TrustedKeyGroups": TrustedKeyGroupsTypeDef,
        "AllowedMethods": AllowedMethodsTypeDef,
        "SmoothStreaming": bool,
        "Compress": bool,
        "LambdaFunctionAssociations": LambdaFunctionAssociationsTypeDef,
        "FunctionAssociations": FunctionAssociationsTypeDef,
        "FieldLevelEncryptionId": str,
        "RealtimeLogConfigArn": str,
        "CachePolicyId": str,
        "OriginRequestPolicyId": str,
        "ResponseHeadersPolicyId": str,
        "ForwardedValues": ForwardedValuesTypeDef,
        "MinTTL": int,
        "DefaultTTL": int,
        "MaxTTL": int,
    },
    total=False,
)


class CacheBehaviorTypeDef(_RequiredCacheBehaviorTypeDef, _OptionalCacheBehaviorTypeDef):
    pass


_RequiredDefaultCacheBehaviorTypeDef = TypedDict(
    "_RequiredDefaultCacheBehaviorTypeDef",
    {
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
    },
)
_OptionalDefaultCacheBehaviorTypeDef = TypedDict(
    "_OptionalDefaultCacheBehaviorTypeDef",
    {
        "TrustedSigners": TrustedSignersTypeDef,
        "TrustedKeyGroups": TrustedKeyGroupsTypeDef,
        "AllowedMethods": AllowedMethodsTypeDef,
        "SmoothStreaming": bool,
        "Compress": bool,
        "LambdaFunctionAssociations": LambdaFunctionAssociationsTypeDef,
        "FunctionAssociations": FunctionAssociationsTypeDef,
        "FieldLevelEncryptionId": str,
        "RealtimeLogConfigArn": str,
        "CachePolicyId": str,
        "OriginRequestPolicyId": str,
        "ResponseHeadersPolicyId": str,
        "ForwardedValues": ForwardedValuesTypeDef,
        "MinTTL": int,
        "DefaultTTL": int,
        "MaxTTL": int,
    },
    total=False,
)


class DefaultCacheBehaviorTypeDef(
    _RequiredDefaultCacheBehaviorTypeDef, _OptionalDefaultCacheBehaviorTypeDef
):
    pass


_RequiredCachePolicyConfigTypeDef = TypedDict(
    "_RequiredCachePolicyConfigTypeDef",
    {
        "Name": str,
        "MinTTL": int,
    },
)
_OptionalCachePolicyConfigTypeDef = TypedDict(
    "_OptionalCachePolicyConfigTypeDef",
    {
        "Comment": str,
        "DefaultTTL": int,
        "MaxTTL": int,
        "ParametersInCacheKeyAndForwardedToOrigin": ParametersInCacheKeyAndForwardedToOriginTypeDef,
    },
    total=False,
)


class CachePolicyConfigTypeDef(
    _RequiredCachePolicyConfigTypeDef, _OptionalCachePolicyConfigTypeDef
):
    pass


CreateOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "CreateOriginRequestPolicyRequestRequestTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
    },
)

GetOriginRequestPolicyConfigResultTypeDef = TypedDict(
    "GetOriginRequestPolicyConfigResultTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OriginRequestPolicyTypeDef = TypedDict(
    "OriginRequestPolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
    },
)

_RequiredUpdateOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOriginRequestPolicyRequestRequestTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOriginRequestPolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateOriginRequestPolicyRequestRequestTypeDef(
    _RequiredUpdateOriginRequestPolicyRequestRequestTypeDef,
    _OptionalUpdateOriginRequestPolicyRequestRequestTypeDef,
):
    pass


_RequiredKeyGroupListTypeDef = TypedDict(
    "_RequiredKeyGroupListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalKeyGroupListTypeDef = TypedDict(
    "_OptionalKeyGroupListTypeDef",
    {
        "NextMarker": str,
        "Items": List[KeyGroupSummaryTypeDef],
    },
    total=False,
)


class KeyGroupListTypeDef(_RequiredKeyGroupListTypeDef, _OptionalKeyGroupListTypeDef):
    pass


OriginsTypeDef = TypedDict(
    "OriginsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[OriginTypeDef],
    },
)

_RequiredFieldLevelEncryptionProfileConfigTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionProfileConfigTypeDef",
    {
        "Name": str,
        "CallerReference": str,
        "EncryptionEntities": EncryptionEntitiesTypeDef,
    },
)
_OptionalFieldLevelEncryptionProfileConfigTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionProfileConfigTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class FieldLevelEncryptionProfileConfigTypeDef(
    _RequiredFieldLevelEncryptionProfileConfigTypeDef,
    _OptionalFieldLevelEncryptionProfileConfigTypeDef,
):
    pass


_RequiredFieldLevelEncryptionProfileSummaryTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionProfileSummaryTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "Name": str,
        "EncryptionEntities": EncryptionEntitiesTypeDef,
    },
)
_OptionalFieldLevelEncryptionProfileSummaryTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionProfileSummaryTypeDef",
    {
        "Comment": str,
    },
    total=False,
)


class FieldLevelEncryptionProfileSummaryTypeDef(
    _RequiredFieldLevelEncryptionProfileSummaryTypeDef,
    _OptionalFieldLevelEncryptionProfileSummaryTypeDef,
):
    pass


CreateRealtimeLogConfigResultTypeDef = TypedDict(
    "CreateRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRealtimeLogConfigResultTypeDef = TypedDict(
    "GetRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRealtimeLogConfigsTypeDef = TypedDict(
    "_RequiredRealtimeLogConfigsTypeDef",
    {
        "MaxItems": int,
        "IsTruncated": bool,
        "Marker": str,
    },
)
_OptionalRealtimeLogConfigsTypeDef = TypedDict(
    "_OptionalRealtimeLogConfigsTypeDef",
    {
        "Items": List[RealtimeLogConfigTypeDef],
        "NextMarker": str,
    },
    total=False,
)


class RealtimeLogConfigsTypeDef(
    _RequiredRealtimeLogConfigsTypeDef, _OptionalRealtimeLogConfigsTypeDef
):
    pass


UpdateRealtimeLogConfigResultTypeDef = TypedDict(
    "UpdateRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFunctionsResultTypeDef = TypedDict(
    "ListFunctionsResultTypeDef",
    {
        "FunctionList": FunctionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestFunctionResultTypeDef = TypedDict(
    "TestFunctionResultTypeDef",
    {
        "TestResult": TestResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInvalidationResultTypeDef = TypedDict(
    "CreateInvalidationResultTypeDef",
    {
        "Location": str,
        "Invalidation": InvalidationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInvalidationResultTypeDef = TypedDict(
    "GetInvalidationResultTypeDef",
    {
        "Invalidation": InvalidationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStreamingDistributionTypeDef = TypedDict(
    "_RequiredStreamingDistributionTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "DomainName": str,
        "ActiveTrustedSigners": ActiveTrustedSignersTypeDef,
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
    },
)
_OptionalStreamingDistributionTypeDef = TypedDict(
    "_OptionalStreamingDistributionTypeDef",
    {
        "LastModifiedTime": datetime,
    },
    total=False,
)


class StreamingDistributionTypeDef(
    _RequiredStreamingDistributionTypeDef, _OptionalStreamingDistributionTypeDef
):
    pass


_RequiredOriginGroupsTypeDef = TypedDict(
    "_RequiredOriginGroupsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalOriginGroupsTypeDef = TypedDict(
    "_OptionalOriginGroupsTypeDef",
    {
        "Items": Sequence[OriginGroupTypeDef],
    },
    total=False,
)


class OriginGroupsTypeDef(_RequiredOriginGroupsTypeDef, _OptionalOriginGroupsTypeDef):
    pass


_RequiredFieldLevelEncryptionConfigTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionConfigTypeDef",
    {
        "CallerReference": str,
    },
)
_OptionalFieldLevelEncryptionConfigTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionConfigTypeDef",
    {
        "Comment": str,
        "QueryArgProfileConfig": QueryArgProfileConfigTypeDef,
        "ContentTypeProfileConfig": ContentTypeProfileConfigTypeDef,
    },
    total=False,
)


class FieldLevelEncryptionConfigTypeDef(
    _RequiredFieldLevelEncryptionConfigTypeDef, _OptionalFieldLevelEncryptionConfigTypeDef
):
    pass


_RequiredFieldLevelEncryptionSummaryTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionSummaryTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
    },
)
_OptionalFieldLevelEncryptionSummaryTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionSummaryTypeDef",
    {
        "Comment": str,
        "QueryArgProfileConfig": QueryArgProfileConfigTypeDef,
        "ContentTypeProfileConfig": ContentTypeProfileConfigTypeDef,
    },
    total=False,
)


class FieldLevelEncryptionSummaryTypeDef(
    _RequiredFieldLevelEncryptionSummaryTypeDef, _OptionalFieldLevelEncryptionSummaryTypeDef
):
    pass


CreateResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "CreateResponseHeadersPolicyRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
    },
)

GetResponseHeadersPolicyConfigResultTypeDef = TypedDict(
    "GetResponseHeadersPolicyConfigResultTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResponseHeadersPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
    },
)

_RequiredUpdateResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResponseHeadersPolicyRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResponseHeadersPolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateResponseHeadersPolicyRequestRequestTypeDef(
    _RequiredUpdateResponseHeadersPolicyRequestRequestTypeDef,
    _OptionalUpdateResponseHeadersPolicyRequestRequestTypeDef,
):
    pass


ListStreamingDistributionsResultTypeDef = TypedDict(
    "ListStreamingDistributionsResultTypeDef",
    {
        "StreamingDistributionList": StreamingDistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamingDistributionWithTagsRequestRequestTypeDef = TypedDict(
    "CreateStreamingDistributionWithTagsRequestRequestTypeDef",
    {
        "StreamingDistributionConfigWithTags": StreamingDistributionConfigWithTagsTypeDef,
    },
)

_RequiredCacheBehaviorsTypeDef = TypedDict(
    "_RequiredCacheBehaviorsTypeDef",
    {
        "Quantity": int,
    },
)
_OptionalCacheBehaviorsTypeDef = TypedDict(
    "_OptionalCacheBehaviorsTypeDef",
    {
        "Items": Sequence[CacheBehaviorTypeDef],
    },
    total=False,
)


class CacheBehaviorsTypeDef(_RequiredCacheBehaviorsTypeDef, _OptionalCacheBehaviorsTypeDef):
    pass


CachePolicyTypeDef = TypedDict(
    "CachePolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "CachePolicyConfig": CachePolicyConfigTypeDef,
    },
)

CreateCachePolicyRequestRequestTypeDef = TypedDict(
    "CreateCachePolicyRequestRequestTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigTypeDef,
    },
)

GetCachePolicyConfigResultTypeDef = TypedDict(
    "GetCachePolicyConfigResultTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateCachePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCachePolicyRequestRequestTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateCachePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCachePolicyRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateCachePolicyRequestRequestTypeDef(
    _RequiredUpdateCachePolicyRequestRequestTypeDef, _OptionalUpdateCachePolicyRequestRequestTypeDef
):
    pass


CreateOriginRequestPolicyResultTypeDef = TypedDict(
    "CreateOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOriginRequestPolicyResultTypeDef = TypedDict(
    "GetOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OriginRequestPolicySummaryTypeDef = TypedDict(
    "OriginRequestPolicySummaryTypeDef",
    {
        "Type": OriginRequestPolicyTypeType,
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
    },
)

UpdateOriginRequestPolicyResultTypeDef = TypedDict(
    "UpdateOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKeyGroupsResultTypeDef = TypedDict(
    "ListKeyGroupsResultTypeDef",
    {
        "KeyGroupList": KeyGroupListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "CreateFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
    },
)

FieldLevelEncryptionProfileTypeDef = TypedDict(
    "FieldLevelEncryptionProfileTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
    },
)

GetFieldLevelEncryptionProfileConfigResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileConfigResultTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateFieldLevelEncryptionProfileRequestRequestTypeDef(
    _RequiredUpdateFieldLevelEncryptionProfileRequestRequestTypeDef,
    _OptionalUpdateFieldLevelEncryptionProfileRequestRequestTypeDef,
):
    pass


_RequiredFieldLevelEncryptionProfileListTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionProfileListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalFieldLevelEncryptionProfileListTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionProfileListTypeDef",
    {
        "NextMarker": str,
        "Items": List[FieldLevelEncryptionProfileSummaryTypeDef],
    },
    total=False,
)


class FieldLevelEncryptionProfileListTypeDef(
    _RequiredFieldLevelEncryptionProfileListTypeDef, _OptionalFieldLevelEncryptionProfileListTypeDef
):
    pass


ListRealtimeLogConfigsResultTypeDef = TypedDict(
    "ListRealtimeLogConfigsResultTypeDef",
    {
        "RealtimeLogConfigs": RealtimeLogConfigsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamingDistributionResultTypeDef = TypedDict(
    "CreateStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamingDistributionWithTagsResultTypeDef = TypedDict(
    "CreateStreamingDistributionWithTagsResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStreamingDistributionResultTypeDef = TypedDict(
    "GetStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStreamingDistributionResultTypeDef = TypedDict(
    "UpdateStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "CreateFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
    },
)

FieldLevelEncryptionTypeDef = TypedDict(
    "FieldLevelEncryptionTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
    },
)

GetFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateFieldLevelEncryptionConfigRequestRequestTypeDef(
    _RequiredUpdateFieldLevelEncryptionConfigRequestRequestTypeDef,
    _OptionalUpdateFieldLevelEncryptionConfigRequestRequestTypeDef,
):
    pass


_RequiredFieldLevelEncryptionListTypeDef = TypedDict(
    "_RequiredFieldLevelEncryptionListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalFieldLevelEncryptionListTypeDef = TypedDict(
    "_OptionalFieldLevelEncryptionListTypeDef",
    {
        "NextMarker": str,
        "Items": List[FieldLevelEncryptionSummaryTypeDef],
    },
    total=False,
)


class FieldLevelEncryptionListTypeDef(
    _RequiredFieldLevelEncryptionListTypeDef, _OptionalFieldLevelEncryptionListTypeDef
):
    pass


CreateResponseHeadersPolicyResultTypeDef = TypedDict(
    "CreateResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResponseHeadersPolicyResultTypeDef = TypedDict(
    "GetResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResponseHeadersPolicySummaryTypeDef = TypedDict(
    "ResponseHeadersPolicySummaryTypeDef",
    {
        "Type": ResponseHeadersPolicyTypeType,
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
    },
)

UpdateResponseHeadersPolicyResultTypeDef = TypedDict(
    "UpdateResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDistributionConfigTypeDef = TypedDict(
    "_RequiredDistributionConfigTypeDef",
    {
        "CallerReference": str,
        "Origins": OriginsTypeDef,
        "DefaultCacheBehavior": DefaultCacheBehaviorTypeDef,
        "Comment": str,
        "Enabled": bool,
    },
)
_OptionalDistributionConfigTypeDef = TypedDict(
    "_OptionalDistributionConfigTypeDef",
    {
        "Aliases": AliasesTypeDef,
        "DefaultRootObject": str,
        "OriginGroups": OriginGroupsTypeDef,
        "CacheBehaviors": CacheBehaviorsTypeDef,
        "CustomErrorResponses": CustomErrorResponsesTypeDef,
        "Logging": LoggingConfigTypeDef,
        "PriceClass": PriceClassType,
        "ViewerCertificate": ViewerCertificateTypeDef,
        "Restrictions": RestrictionsTypeDef,
        "WebACLId": str,
        "HttpVersion": HttpVersionType,
        "IsIPV6Enabled": bool,
    },
    total=False,
)


class DistributionConfigTypeDef(
    _RequiredDistributionConfigTypeDef, _OptionalDistributionConfigTypeDef
):
    pass


_RequiredDistributionSummaryTypeDef = TypedDict(
    "_RequiredDistributionSummaryTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "DomainName": str,
        "Aliases": AliasesTypeDef,
        "Origins": OriginsTypeDef,
        "DefaultCacheBehavior": DefaultCacheBehaviorTypeDef,
        "CacheBehaviors": CacheBehaviorsTypeDef,
        "CustomErrorResponses": CustomErrorResponsesTypeDef,
        "Comment": str,
        "PriceClass": PriceClassType,
        "Enabled": bool,
        "ViewerCertificate": ViewerCertificateTypeDef,
        "Restrictions": RestrictionsTypeDef,
        "WebACLId": str,
        "HttpVersion": HttpVersionType,
        "IsIPV6Enabled": bool,
    },
)
_OptionalDistributionSummaryTypeDef = TypedDict(
    "_OptionalDistributionSummaryTypeDef",
    {
        "OriginGroups": OriginGroupsTypeDef,
        "AliasICPRecordals": List[AliasICPRecordalTypeDef],
    },
    total=False,
)


class DistributionSummaryTypeDef(
    _RequiredDistributionSummaryTypeDef, _OptionalDistributionSummaryTypeDef
):
    pass


CachePolicySummaryTypeDef = TypedDict(
    "CachePolicySummaryTypeDef",
    {
        "Type": CachePolicyTypeType,
        "CachePolicy": CachePolicyTypeDef,
    },
)

CreateCachePolicyResultTypeDef = TypedDict(
    "CreateCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCachePolicyResultTypeDef = TypedDict(
    "GetCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCachePolicyResultTypeDef = TypedDict(
    "UpdateCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredOriginRequestPolicyListTypeDef = TypedDict(
    "_RequiredOriginRequestPolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalOriginRequestPolicyListTypeDef = TypedDict(
    "_OptionalOriginRequestPolicyListTypeDef",
    {
        "NextMarker": str,
        "Items": List[OriginRequestPolicySummaryTypeDef],
    },
    total=False,
)


class OriginRequestPolicyListTypeDef(
    _RequiredOriginRequestPolicyListTypeDef, _OptionalOriginRequestPolicyListTypeDef
):
    pass


CreateFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "CreateFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFieldLevelEncryptionProfilesResultTypeDef = TypedDict(
    "ListFieldLevelEncryptionProfilesResultTypeDef",
    {
        "FieldLevelEncryptionProfileList": FieldLevelEncryptionProfileListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "CreateFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFieldLevelEncryptionResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFieldLevelEncryptionConfigsResultTypeDef = TypedDict(
    "ListFieldLevelEncryptionConfigsResultTypeDef",
    {
        "FieldLevelEncryptionList": FieldLevelEncryptionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResponseHeadersPolicyListTypeDef = TypedDict(
    "_RequiredResponseHeadersPolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalResponseHeadersPolicyListTypeDef = TypedDict(
    "_OptionalResponseHeadersPolicyListTypeDef",
    {
        "NextMarker": str,
        "Items": List[ResponseHeadersPolicySummaryTypeDef],
    },
    total=False,
)


class ResponseHeadersPolicyListTypeDef(
    _RequiredResponseHeadersPolicyListTypeDef, _OptionalResponseHeadersPolicyListTypeDef
):
    pass


CreateDistributionRequestRequestTypeDef = TypedDict(
    "CreateDistributionRequestRequestTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
    },
)

DistributionConfigWithTagsTypeDef = TypedDict(
    "DistributionConfigWithTagsTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
        "Tags": TagsTypeDef,
    },
)

_RequiredDistributionTypeDef = TypedDict(
    "_RequiredDistributionTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "InProgressInvalidationBatches": int,
        "DomainName": str,
        "DistributionConfig": DistributionConfigTypeDef,
    },
)
_OptionalDistributionTypeDef = TypedDict(
    "_OptionalDistributionTypeDef",
    {
        "ActiveTrustedSigners": ActiveTrustedSignersTypeDef,
        "ActiveTrustedKeyGroups": ActiveTrustedKeyGroupsTypeDef,
        "AliasICPRecordals": List[AliasICPRecordalTypeDef],
    },
    total=False,
)


class DistributionTypeDef(_RequiredDistributionTypeDef, _OptionalDistributionTypeDef):
    pass


GetDistributionConfigResultTypeDef = TypedDict(
    "GetDistributionConfigResultTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDistributionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDistributionRequestRequestTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
        "Id": str,
    },
)
_OptionalUpdateDistributionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDistributionRequestRequestTypeDef",
    {
        "IfMatch": str,
    },
    total=False,
)


class UpdateDistributionRequestRequestTypeDef(
    _RequiredUpdateDistributionRequestRequestTypeDef,
    _OptionalUpdateDistributionRequestRequestTypeDef,
):
    pass


_RequiredDistributionListTypeDef = TypedDict(
    "_RequiredDistributionListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
    },
)
_OptionalDistributionListTypeDef = TypedDict(
    "_OptionalDistributionListTypeDef",
    {
        "NextMarker": str,
        "Items": List[DistributionSummaryTypeDef],
    },
    total=False,
)


class DistributionListTypeDef(_RequiredDistributionListTypeDef, _OptionalDistributionListTypeDef):
    pass


_RequiredCachePolicyListTypeDef = TypedDict(
    "_RequiredCachePolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
    },
)
_OptionalCachePolicyListTypeDef = TypedDict(
    "_OptionalCachePolicyListTypeDef",
    {
        "NextMarker": str,
        "Items": List[CachePolicySummaryTypeDef],
    },
    total=False,
)


class CachePolicyListTypeDef(_RequiredCachePolicyListTypeDef, _OptionalCachePolicyListTypeDef):
    pass


ListOriginRequestPoliciesResultTypeDef = TypedDict(
    "ListOriginRequestPoliciesResultTypeDef",
    {
        "OriginRequestPolicyList": OriginRequestPolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResponseHeadersPoliciesResultTypeDef = TypedDict(
    "ListResponseHeadersPoliciesResultTypeDef",
    {
        "ResponseHeadersPolicyList": ResponseHeadersPolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDistributionWithTagsRequestRequestTypeDef = TypedDict(
    "CreateDistributionWithTagsRequestRequestTypeDef",
    {
        "DistributionConfigWithTags": DistributionConfigWithTagsTypeDef,
    },
)

CreateDistributionResultTypeDef = TypedDict(
    "CreateDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDistributionWithTagsResultTypeDef = TypedDict(
    "CreateDistributionWithTagsResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDistributionResultTypeDef = TypedDict(
    "GetDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDistributionResultTypeDef = TypedDict(
    "UpdateDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsByRealtimeLogConfigResultTypeDef = TypedDict(
    "ListDistributionsByRealtimeLogConfigResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsByWebACLIdResultTypeDef = TypedDict(
    "ListDistributionsByWebACLIdResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDistributionsResultTypeDef = TypedDict(
    "ListDistributionsResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCachePoliciesResultTypeDef = TypedDict(
    "ListCachePoliciesResultTypeDef",
    {
        "CachePolicyList": CachePolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
