"""
Type annotations for waf-regional service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_waf_regional/type_defs/)

Usage::

    ```python
    from mypy_boto3_waf_regional.type_defs import ExcludedRuleTypeDef

    data: ExcludedRuleTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ChangeActionType,
    ChangeTokenStatusType,
    ComparisonOperatorType,
    GeoMatchConstraintValueType,
    IPSetDescriptorTypeType,
    MatchFieldTypeType,
    PositionalConstraintType,
    PredicateTypeType,
    ResourceTypeType,
    TextTransformationType,
    WafActionTypeType,
    WafOverrideActionTypeType,
    WafRuleTypeType,
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
    "ExcludedRuleTypeDef",
    "WafActionTypeDef",
    "WafOverrideActionTypeDef",
    "AssociateWebACLRequestRequestTypeDef",
    "ByteMatchSetSummaryTypeDef",
    "FieldToMatchTypeDef",
    "CreateByteMatchSetRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateGeoMatchSetRequestRequestTypeDef",
    "CreateIPSetRequestRequestTypeDef",
    "TagTypeDef",
    "CreateRegexMatchSetRequestRequestTypeDef",
    "CreateRegexPatternSetRequestRequestTypeDef",
    "RegexPatternSetTypeDef",
    "RuleGroupTypeDef",
    "CreateSizeConstraintSetRequestRequestTypeDef",
    "CreateSqlInjectionMatchSetRequestRequestTypeDef",
    "CreateWebACLMigrationStackRequestRequestTypeDef",
    "CreateXssMatchSetRequestRequestTypeDef",
    "DeleteByteMatchSetRequestRequestTypeDef",
    "DeleteGeoMatchSetRequestRequestTypeDef",
    "DeleteIPSetRequestRequestTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeletePermissionPolicyRequestRequestTypeDef",
    "DeleteRateBasedRuleRequestRequestTypeDef",
    "DeleteRegexMatchSetRequestRequestTypeDef",
    "DeleteRegexPatternSetRequestRequestTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteSizeConstraintSetRequestRequestTypeDef",
    "DeleteSqlInjectionMatchSetRequestRequestTypeDef",
    "DeleteWebACLRequestRequestTypeDef",
    "DeleteXssMatchSetRequestRequestTypeDef",
    "DisassociateWebACLRequestRequestTypeDef",
    "GeoMatchConstraintTypeDef",
    "GeoMatchSetSummaryTypeDef",
    "GetByteMatchSetRequestRequestTypeDef",
    "GetChangeTokenStatusRequestRequestTypeDef",
    "GetGeoMatchSetRequestRequestTypeDef",
    "GetIPSetRequestRequestTypeDef",
    "GetLoggingConfigurationRequestRequestTypeDef",
    "GetPermissionPolicyRequestRequestTypeDef",
    "GetRateBasedRuleManagedKeysRequestRequestTypeDef",
    "GetRateBasedRuleRequestRequestTypeDef",
    "GetRegexMatchSetRequestRequestTypeDef",
    "GetRegexPatternSetRequestRequestTypeDef",
    "GetRuleGroupRequestRequestTypeDef",
    "GetRuleRequestRequestTypeDef",
    "TimeWindowTypeDef",
    "GetSizeConstraintSetRequestRequestTypeDef",
    "GetSqlInjectionMatchSetRequestRequestTypeDef",
    "GetWebACLForResourceRequestRequestTypeDef",
    "WebACLSummaryTypeDef",
    "GetWebACLRequestRequestTypeDef",
    "GetXssMatchSetRequestRequestTypeDef",
    "HTTPHeaderTypeDef",
    "IPSetDescriptorTypeDef",
    "IPSetSummaryTypeDef",
    "ListActivatedRulesInRuleGroupRequestRequestTypeDef",
    "ListByteMatchSetsRequestRequestTypeDef",
    "ListGeoMatchSetsRequestRequestTypeDef",
    "ListIPSetsRequestRequestTypeDef",
    "ListLoggingConfigurationsRequestRequestTypeDef",
    "ListRateBasedRulesRequestRequestTypeDef",
    "RuleSummaryTypeDef",
    "ListRegexMatchSetsRequestRequestTypeDef",
    "RegexMatchSetSummaryTypeDef",
    "ListRegexPatternSetsRequestRequestTypeDef",
    "RegexPatternSetSummaryTypeDef",
    "ListResourcesForWebACLRequestRequestTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "RuleGroupSummaryTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListSizeConstraintSetsRequestRequestTypeDef",
    "SizeConstraintSetSummaryTypeDef",
    "ListSqlInjectionMatchSetsRequestRequestTypeDef",
    "SqlInjectionMatchSetSummaryTypeDef",
    "ListSubscribedRuleGroupsRequestRequestTypeDef",
    "SubscribedRuleGroupSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebACLsRequestRequestTypeDef",
    "ListXssMatchSetsRequestRequestTypeDef",
    "XssMatchSetSummaryTypeDef",
    "PredicateTypeDef",
    "PutPermissionPolicyRequestRequestTypeDef",
    "RegexPatternSetUpdateTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ActivatedRuleTypeDef",
    "ByteMatchTupleTypeDef",
    "LoggingConfigurationTypeDef",
    "RegexMatchTupleTypeDef",
    "SizeConstraintTypeDef",
    "SqlInjectionMatchTupleTypeDef",
    "XssMatchTupleTypeDef",
    "CreateWebACLMigrationStackResponseTypeDef",
    "DeleteByteMatchSetResponseTypeDef",
    "DeleteGeoMatchSetResponseTypeDef",
    "DeleteIPSetResponseTypeDef",
    "DeleteRateBasedRuleResponseTypeDef",
    "DeleteRegexMatchSetResponseTypeDef",
    "DeleteRegexPatternSetResponseTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "DeleteRuleResponseTypeDef",
    "DeleteSizeConstraintSetResponseTypeDef",
    "DeleteSqlInjectionMatchSetResponseTypeDef",
    "DeleteWebACLResponseTypeDef",
    "DeleteXssMatchSetResponseTypeDef",
    "GetChangeTokenResponseTypeDef",
    "GetChangeTokenStatusResponseTypeDef",
    "GetPermissionPolicyResponseTypeDef",
    "GetRateBasedRuleManagedKeysResponseTypeDef",
    "ListByteMatchSetsResponseTypeDef",
    "ListResourcesForWebACLResponseTypeDef",
    "UpdateByteMatchSetResponseTypeDef",
    "UpdateGeoMatchSetResponseTypeDef",
    "UpdateIPSetResponseTypeDef",
    "UpdateRateBasedRuleResponseTypeDef",
    "UpdateRegexMatchSetResponseTypeDef",
    "UpdateRegexPatternSetResponseTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateRuleResponseTypeDef",
    "UpdateSizeConstraintSetResponseTypeDef",
    "UpdateSqlInjectionMatchSetResponseTypeDef",
    "UpdateWebACLResponseTypeDef",
    "UpdateXssMatchSetResponseTypeDef",
    "CreateRateBasedRuleRequestRequestTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateWebACLRequestRequestTypeDef",
    "TagInfoForResourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateRegexPatternSetResponseTypeDef",
    "GetRegexPatternSetResponseTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "GetRuleGroupResponseTypeDef",
    "GeoMatchSetTypeDef",
    "GeoMatchSetUpdateTypeDef",
    "ListGeoMatchSetsResponseTypeDef",
    "GetSampledRequestsRequestRequestTypeDef",
    "GetWebACLForResourceResponseTypeDef",
    "ListWebACLsResponseTypeDef",
    "HTTPRequestTypeDef",
    "IPSetTypeDef",
    "IPSetUpdateTypeDef",
    "ListIPSetsResponseTypeDef",
    "ListRateBasedRulesResponseTypeDef",
    "ListRulesResponseTypeDef",
    "ListRegexMatchSetsResponseTypeDef",
    "ListRegexPatternSetsResponseTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListSizeConstraintSetsResponseTypeDef",
    "ListSqlInjectionMatchSetsResponseTypeDef",
    "ListSubscribedRuleGroupsResponseTypeDef",
    "ListXssMatchSetsResponseTypeDef",
    "RateBasedRuleTypeDef",
    "RuleTypeDef",
    "RuleUpdateTypeDef",
    "UpdateRegexPatternSetRequestRequestTypeDef",
    "ListActivatedRulesInRuleGroupResponseTypeDef",
    "RuleGroupUpdateTypeDef",
    "WebACLTypeDef",
    "WebACLUpdateTypeDef",
    "ByteMatchSetTypeDef",
    "ByteMatchSetUpdateTypeDef",
    "GetLoggingConfigurationResponseTypeDef",
    "ListLoggingConfigurationsResponseTypeDef",
    "PutLoggingConfigurationRequestRequestTypeDef",
    "PutLoggingConfigurationResponseTypeDef",
    "RegexMatchSetTypeDef",
    "RegexMatchSetUpdateTypeDef",
    "SizeConstraintSetTypeDef",
    "SizeConstraintSetUpdateTypeDef",
    "SqlInjectionMatchSetTypeDef",
    "SqlInjectionMatchSetUpdateTypeDef",
    "XssMatchSetTypeDef",
    "XssMatchSetUpdateTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateGeoMatchSetResponseTypeDef",
    "GetGeoMatchSetResponseTypeDef",
    "UpdateGeoMatchSetRequestRequestTypeDef",
    "SampledHTTPRequestTypeDef",
    "CreateIPSetResponseTypeDef",
    "GetIPSetResponseTypeDef",
    "UpdateIPSetRequestRequestTypeDef",
    "CreateRateBasedRuleResponseTypeDef",
    "GetRateBasedRuleResponseTypeDef",
    "CreateRuleResponseTypeDef",
    "GetRuleResponseTypeDef",
    "UpdateRateBasedRuleRequestRequestTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
    "CreateWebACLResponseTypeDef",
    "GetWebACLResponseTypeDef",
    "UpdateWebACLRequestRequestTypeDef",
    "CreateByteMatchSetResponseTypeDef",
    "GetByteMatchSetResponseTypeDef",
    "UpdateByteMatchSetRequestRequestTypeDef",
    "CreateRegexMatchSetResponseTypeDef",
    "GetRegexMatchSetResponseTypeDef",
    "UpdateRegexMatchSetRequestRequestTypeDef",
    "CreateSizeConstraintSetResponseTypeDef",
    "GetSizeConstraintSetResponseTypeDef",
    "UpdateSizeConstraintSetRequestRequestTypeDef",
    "CreateSqlInjectionMatchSetResponseTypeDef",
    "GetSqlInjectionMatchSetResponseTypeDef",
    "UpdateSqlInjectionMatchSetRequestRequestTypeDef",
    "CreateXssMatchSetResponseTypeDef",
    "GetXssMatchSetResponseTypeDef",
    "UpdateXssMatchSetRequestRequestTypeDef",
    "GetSampledRequestsResponseTypeDef",
)

ExcludedRuleTypeDef = TypedDict(
    "ExcludedRuleTypeDef",
    {
        "RuleId": str,
    },
)

WafActionTypeDef = TypedDict(
    "WafActionTypeDef",
    {
        "Type": WafActionTypeType,
    },
)

WafOverrideActionTypeDef = TypedDict(
    "WafOverrideActionTypeDef",
    {
        "Type": WafOverrideActionTypeType,
    },
)

AssociateWebACLRequestRequestTypeDef = TypedDict(
    "AssociateWebACLRequestRequestTypeDef",
    {
        "WebACLId": str,
        "ResourceArn": str,
    },
)

ByteMatchSetSummaryTypeDef = TypedDict(
    "ByteMatchSetSummaryTypeDef",
    {
        "ByteMatchSetId": str,
        "Name": str,
    },
)

_RequiredFieldToMatchTypeDef = TypedDict(
    "_RequiredFieldToMatchTypeDef",
    {
        "Type": MatchFieldTypeType,
    },
)
_OptionalFieldToMatchTypeDef = TypedDict(
    "_OptionalFieldToMatchTypeDef",
    {
        "Data": str,
    },
    total=False,
)


class FieldToMatchTypeDef(_RequiredFieldToMatchTypeDef, _OptionalFieldToMatchTypeDef):
    pass


CreateByteMatchSetRequestRequestTypeDef = TypedDict(
    "CreateByteMatchSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
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

CreateGeoMatchSetRequestRequestTypeDef = TypedDict(
    "CreateGeoMatchSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

CreateIPSetRequestRequestTypeDef = TypedDict(
    "CreateIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CreateRegexMatchSetRequestRequestTypeDef = TypedDict(
    "CreateRegexMatchSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

CreateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "CreateRegexPatternSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

_RequiredRegexPatternSetTypeDef = TypedDict(
    "_RequiredRegexPatternSetTypeDef",
    {
        "RegexPatternSetId": str,
        "RegexPatternStrings": List[str],
    },
)
_OptionalRegexPatternSetTypeDef = TypedDict(
    "_OptionalRegexPatternSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class RegexPatternSetTypeDef(_RequiredRegexPatternSetTypeDef, _OptionalRegexPatternSetTypeDef):
    pass


_RequiredRuleGroupTypeDef = TypedDict(
    "_RequiredRuleGroupTypeDef",
    {
        "RuleGroupId": str,
    },
)
_OptionalRuleGroupTypeDef = TypedDict(
    "_OptionalRuleGroupTypeDef",
    {
        "Name": str,
        "MetricName": str,
    },
    total=False,
)


class RuleGroupTypeDef(_RequiredRuleGroupTypeDef, _OptionalRuleGroupTypeDef):
    pass


CreateSizeConstraintSetRequestRequestTypeDef = TypedDict(
    "CreateSizeConstraintSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

CreateSqlInjectionMatchSetRequestRequestTypeDef = TypedDict(
    "CreateSqlInjectionMatchSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

CreateWebACLMigrationStackRequestRequestTypeDef = TypedDict(
    "CreateWebACLMigrationStackRequestRequestTypeDef",
    {
        "WebACLId": str,
        "S3BucketName": str,
        "IgnoreUnsupportedType": bool,
    },
)

CreateXssMatchSetRequestRequestTypeDef = TypedDict(
    "CreateXssMatchSetRequestRequestTypeDef",
    {
        "Name": str,
        "ChangeToken": str,
    },
)

DeleteByteMatchSetRequestRequestTypeDef = TypedDict(
    "DeleteByteMatchSetRequestRequestTypeDef",
    {
        "ByteMatchSetId": str,
        "ChangeToken": str,
    },
)

DeleteGeoMatchSetRequestRequestTypeDef = TypedDict(
    "DeleteGeoMatchSetRequestRequestTypeDef",
    {
        "GeoMatchSetId": str,
        "ChangeToken": str,
    },
)

DeleteIPSetRequestRequestTypeDef = TypedDict(
    "DeleteIPSetRequestRequestTypeDef",
    {
        "IPSetId": str,
        "ChangeToken": str,
    },
)

DeleteLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeletePermissionPolicyRequestRequestTypeDef = TypedDict(
    "DeletePermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeleteRateBasedRuleRequestRequestTypeDef = TypedDict(
    "DeleteRateBasedRuleRequestRequestTypeDef",
    {
        "RuleId": str,
        "ChangeToken": str,
    },
)

DeleteRegexMatchSetRequestRequestTypeDef = TypedDict(
    "DeleteRegexMatchSetRequestRequestTypeDef",
    {
        "RegexMatchSetId": str,
        "ChangeToken": str,
    },
)

DeleteRegexPatternSetRequestRequestTypeDef = TypedDict(
    "DeleteRegexPatternSetRequestRequestTypeDef",
    {
        "RegexPatternSetId": str,
        "ChangeToken": str,
    },
)

DeleteRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupId": str,
        "ChangeToken": str,
    },
)

DeleteRuleRequestRequestTypeDef = TypedDict(
    "DeleteRuleRequestRequestTypeDef",
    {
        "RuleId": str,
        "ChangeToken": str,
    },
)

DeleteSizeConstraintSetRequestRequestTypeDef = TypedDict(
    "DeleteSizeConstraintSetRequestRequestTypeDef",
    {
        "SizeConstraintSetId": str,
        "ChangeToken": str,
    },
)

DeleteSqlInjectionMatchSetRequestRequestTypeDef = TypedDict(
    "DeleteSqlInjectionMatchSetRequestRequestTypeDef",
    {
        "SqlInjectionMatchSetId": str,
        "ChangeToken": str,
    },
)

DeleteWebACLRequestRequestTypeDef = TypedDict(
    "DeleteWebACLRequestRequestTypeDef",
    {
        "WebACLId": str,
        "ChangeToken": str,
    },
)

DeleteXssMatchSetRequestRequestTypeDef = TypedDict(
    "DeleteXssMatchSetRequestRequestTypeDef",
    {
        "XssMatchSetId": str,
        "ChangeToken": str,
    },
)

DisassociateWebACLRequestRequestTypeDef = TypedDict(
    "DisassociateWebACLRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GeoMatchConstraintTypeDef = TypedDict(
    "GeoMatchConstraintTypeDef",
    {
        "Type": Literal["Country"],
        "Value": GeoMatchConstraintValueType,
    },
)

GeoMatchSetSummaryTypeDef = TypedDict(
    "GeoMatchSetSummaryTypeDef",
    {
        "GeoMatchSetId": str,
        "Name": str,
    },
)

GetByteMatchSetRequestRequestTypeDef = TypedDict(
    "GetByteMatchSetRequestRequestTypeDef",
    {
        "ByteMatchSetId": str,
    },
)

GetChangeTokenStatusRequestRequestTypeDef = TypedDict(
    "GetChangeTokenStatusRequestRequestTypeDef",
    {
        "ChangeToken": str,
    },
)

GetGeoMatchSetRequestRequestTypeDef = TypedDict(
    "GetGeoMatchSetRequestRequestTypeDef",
    {
        "GeoMatchSetId": str,
    },
)

GetIPSetRequestRequestTypeDef = TypedDict(
    "GetIPSetRequestRequestTypeDef",
    {
        "IPSetId": str,
    },
)

GetLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "GetLoggingConfigurationRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GetPermissionPolicyRequestRequestTypeDef = TypedDict(
    "GetPermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredGetRateBasedRuleManagedKeysRequestRequestTypeDef = TypedDict(
    "_RequiredGetRateBasedRuleManagedKeysRequestRequestTypeDef",
    {
        "RuleId": str,
    },
)
_OptionalGetRateBasedRuleManagedKeysRequestRequestTypeDef = TypedDict(
    "_OptionalGetRateBasedRuleManagedKeysRequestRequestTypeDef",
    {
        "NextMarker": str,
    },
    total=False,
)


class GetRateBasedRuleManagedKeysRequestRequestTypeDef(
    _RequiredGetRateBasedRuleManagedKeysRequestRequestTypeDef,
    _OptionalGetRateBasedRuleManagedKeysRequestRequestTypeDef,
):
    pass


GetRateBasedRuleRequestRequestTypeDef = TypedDict(
    "GetRateBasedRuleRequestRequestTypeDef",
    {
        "RuleId": str,
    },
)

GetRegexMatchSetRequestRequestTypeDef = TypedDict(
    "GetRegexMatchSetRequestRequestTypeDef",
    {
        "RegexMatchSetId": str,
    },
)

GetRegexPatternSetRequestRequestTypeDef = TypedDict(
    "GetRegexPatternSetRequestRequestTypeDef",
    {
        "RegexPatternSetId": str,
    },
)

GetRuleGroupRequestRequestTypeDef = TypedDict(
    "GetRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupId": str,
    },
)

GetRuleRequestRequestTypeDef = TypedDict(
    "GetRuleRequestRequestTypeDef",
    {
        "RuleId": str,
    },
)

TimeWindowTypeDef = TypedDict(
    "TimeWindowTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)

GetSizeConstraintSetRequestRequestTypeDef = TypedDict(
    "GetSizeConstraintSetRequestRequestTypeDef",
    {
        "SizeConstraintSetId": str,
    },
)

GetSqlInjectionMatchSetRequestRequestTypeDef = TypedDict(
    "GetSqlInjectionMatchSetRequestRequestTypeDef",
    {
        "SqlInjectionMatchSetId": str,
    },
)

GetWebACLForResourceRequestRequestTypeDef = TypedDict(
    "GetWebACLForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

WebACLSummaryTypeDef = TypedDict(
    "WebACLSummaryTypeDef",
    {
        "WebACLId": str,
        "Name": str,
    },
)

GetWebACLRequestRequestTypeDef = TypedDict(
    "GetWebACLRequestRequestTypeDef",
    {
        "WebACLId": str,
    },
)

GetXssMatchSetRequestRequestTypeDef = TypedDict(
    "GetXssMatchSetRequestRequestTypeDef",
    {
        "XssMatchSetId": str,
    },
)

HTTPHeaderTypeDef = TypedDict(
    "HTTPHeaderTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

IPSetDescriptorTypeDef = TypedDict(
    "IPSetDescriptorTypeDef",
    {
        "Type": IPSetDescriptorTypeType,
        "Value": str,
    },
)

IPSetSummaryTypeDef = TypedDict(
    "IPSetSummaryTypeDef",
    {
        "IPSetId": str,
        "Name": str,
    },
)

ListActivatedRulesInRuleGroupRequestRequestTypeDef = TypedDict(
    "ListActivatedRulesInRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupId": str,
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListByteMatchSetsRequestRequestTypeDef = TypedDict(
    "ListByteMatchSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListGeoMatchSetsRequestRequestTypeDef = TypedDict(
    "ListGeoMatchSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListIPSetsRequestRequestTypeDef = TypedDict(
    "ListIPSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListLoggingConfigurationsRequestRequestTypeDef = TypedDict(
    "ListLoggingConfigurationsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListRateBasedRulesRequestRequestTypeDef = TypedDict(
    "ListRateBasedRulesRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "RuleId": str,
        "Name": str,
    },
)

ListRegexMatchSetsRequestRequestTypeDef = TypedDict(
    "ListRegexMatchSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

RegexMatchSetSummaryTypeDef = TypedDict(
    "RegexMatchSetSummaryTypeDef",
    {
        "RegexMatchSetId": str,
        "Name": str,
    },
)

ListRegexPatternSetsRequestRequestTypeDef = TypedDict(
    "ListRegexPatternSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

RegexPatternSetSummaryTypeDef = TypedDict(
    "RegexPatternSetSummaryTypeDef",
    {
        "RegexPatternSetId": str,
        "Name": str,
    },
)

_RequiredListResourcesForWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesForWebACLRequestRequestTypeDef",
    {
        "WebACLId": str,
    },
)
_OptionalListResourcesForWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesForWebACLRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
    total=False,
)


class ListResourcesForWebACLRequestRequestTypeDef(
    _RequiredListResourcesForWebACLRequestRequestTypeDef,
    _OptionalListResourcesForWebACLRequestRequestTypeDef,
):
    pass


ListRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

RuleGroupSummaryTypeDef = TypedDict(
    "RuleGroupSummaryTypeDef",
    {
        "RuleGroupId": str,
        "Name": str,
    },
)

ListRulesRequestRequestTypeDef = TypedDict(
    "ListRulesRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListSizeConstraintSetsRequestRequestTypeDef = TypedDict(
    "ListSizeConstraintSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

SizeConstraintSetSummaryTypeDef = TypedDict(
    "SizeConstraintSetSummaryTypeDef",
    {
        "SizeConstraintSetId": str,
        "Name": str,
    },
)

ListSqlInjectionMatchSetsRequestRequestTypeDef = TypedDict(
    "ListSqlInjectionMatchSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

SqlInjectionMatchSetSummaryTypeDef = TypedDict(
    "SqlInjectionMatchSetSummaryTypeDef",
    {
        "SqlInjectionMatchSetId": str,
        "Name": str,
    },
)

ListSubscribedRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListSubscribedRuleGroupsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

SubscribedRuleGroupSummaryTypeDef = TypedDict(
    "SubscribedRuleGroupSummaryTypeDef",
    {
        "RuleGroupId": str,
        "Name": str,
        "MetricName": str,
    },
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


ListWebACLsRequestRequestTypeDef = TypedDict(
    "ListWebACLsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

ListXssMatchSetsRequestRequestTypeDef = TypedDict(
    "ListXssMatchSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

XssMatchSetSummaryTypeDef = TypedDict(
    "XssMatchSetSummaryTypeDef",
    {
        "XssMatchSetId": str,
        "Name": str,
    },
)

PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "Negated": bool,
        "Type": PredicateTypeType,
        "DataId": str,
    },
)

PutPermissionPolicyRequestRequestTypeDef = TypedDict(
    "PutPermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
    },
)

RegexPatternSetUpdateTypeDef = TypedDict(
    "RegexPatternSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "RegexPatternString": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredActivatedRuleTypeDef = TypedDict(
    "_RequiredActivatedRuleTypeDef",
    {
        "Priority": int,
        "RuleId": str,
    },
)
_OptionalActivatedRuleTypeDef = TypedDict(
    "_OptionalActivatedRuleTypeDef",
    {
        "Action": WafActionTypeDef,
        "OverrideAction": WafOverrideActionTypeDef,
        "Type": WafRuleTypeType,
        "ExcludedRules": List[ExcludedRuleTypeDef],
    },
    total=False,
)


class ActivatedRuleTypeDef(_RequiredActivatedRuleTypeDef, _OptionalActivatedRuleTypeDef):
    pass


ByteMatchTupleTypeDef = TypedDict(
    "ByteMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TargetString": bytes,
        "TextTransformation": TextTransformationType,
        "PositionalConstraint": PositionalConstraintType,
    },
)

_RequiredLoggingConfigurationTypeDef = TypedDict(
    "_RequiredLoggingConfigurationTypeDef",
    {
        "ResourceArn": str,
        "LogDestinationConfigs": List[str],
    },
)
_OptionalLoggingConfigurationTypeDef = TypedDict(
    "_OptionalLoggingConfigurationTypeDef",
    {
        "RedactedFields": List[FieldToMatchTypeDef],
    },
    total=False,
)


class LoggingConfigurationTypeDef(
    _RequiredLoggingConfigurationTypeDef, _OptionalLoggingConfigurationTypeDef
):
    pass


RegexMatchTupleTypeDef = TypedDict(
    "RegexMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": TextTransformationType,
        "RegexPatternSetId": str,
    },
)

SizeConstraintTypeDef = TypedDict(
    "SizeConstraintTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": TextTransformationType,
        "ComparisonOperator": ComparisonOperatorType,
        "Size": int,
    },
)

SqlInjectionMatchTupleTypeDef = TypedDict(
    "SqlInjectionMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": TextTransformationType,
    },
)

XssMatchTupleTypeDef = TypedDict(
    "XssMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": TextTransformationType,
    },
)

CreateWebACLMigrationStackResponseTypeDef = TypedDict(
    "CreateWebACLMigrationStackResponseTypeDef",
    {
        "S3ObjectUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteByteMatchSetResponseTypeDef = TypedDict(
    "DeleteByteMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGeoMatchSetResponseTypeDef = TypedDict(
    "DeleteGeoMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteIPSetResponseTypeDef = TypedDict(
    "DeleteIPSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRateBasedRuleResponseTypeDef = TypedDict(
    "DeleteRateBasedRuleResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRegexMatchSetResponseTypeDef = TypedDict(
    "DeleteRegexMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRegexPatternSetResponseTypeDef = TypedDict(
    "DeleteRegexPatternSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRuleGroupResponseTypeDef = TypedDict(
    "DeleteRuleGroupResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRuleResponseTypeDef = TypedDict(
    "DeleteRuleResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSizeConstraintSetResponseTypeDef = TypedDict(
    "DeleteSizeConstraintSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "DeleteSqlInjectionMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWebACLResponseTypeDef = TypedDict(
    "DeleteWebACLResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteXssMatchSetResponseTypeDef = TypedDict(
    "DeleteXssMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChangeTokenResponseTypeDef = TypedDict(
    "GetChangeTokenResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChangeTokenStatusResponseTypeDef = TypedDict(
    "GetChangeTokenStatusResponseTypeDef",
    {
        "ChangeTokenStatus": ChangeTokenStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPermissionPolicyResponseTypeDef = TypedDict(
    "GetPermissionPolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRateBasedRuleManagedKeysResponseTypeDef = TypedDict(
    "GetRateBasedRuleManagedKeysResponseTypeDef",
    {
        "ManagedKeys": List[str],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListByteMatchSetsResponseTypeDef = TypedDict(
    "ListByteMatchSetsResponseTypeDef",
    {
        "NextMarker": str,
        "ByteMatchSets": List[ByteMatchSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesForWebACLResponseTypeDef = TypedDict(
    "ListResourcesForWebACLResponseTypeDef",
    {
        "ResourceArns": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateByteMatchSetResponseTypeDef = TypedDict(
    "UpdateByteMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGeoMatchSetResponseTypeDef = TypedDict(
    "UpdateGeoMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIPSetResponseTypeDef = TypedDict(
    "UpdateIPSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRateBasedRuleResponseTypeDef = TypedDict(
    "UpdateRateBasedRuleResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRegexMatchSetResponseTypeDef = TypedDict(
    "UpdateRegexMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRegexPatternSetResponseTypeDef = TypedDict(
    "UpdateRegexPatternSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuleGroupResponseTypeDef = TypedDict(
    "UpdateRuleGroupResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSizeConstraintSetResponseTypeDef = TypedDict(
    "UpdateSizeConstraintSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "UpdateSqlInjectionMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWebACLResponseTypeDef = TypedDict(
    "UpdateWebACLResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateXssMatchSetResponseTypeDef = TypedDict(
    "UpdateXssMatchSetResponseTypeDef",
    {
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateRateBasedRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRateBasedRuleRequestRequestTypeDef",
    {
        "Name": str,
        "MetricName": str,
        "RateKey": Literal["IP"],
        "RateLimit": int,
        "ChangeToken": str,
    },
)
_OptionalCreateRateBasedRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRateBasedRuleRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRateBasedRuleRequestRequestTypeDef(
    _RequiredCreateRateBasedRuleRequestRequestTypeDef,
    _OptionalCreateRateBasedRuleRequestRequestTypeDef,
):
    pass


_RequiredCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleGroupRequestRequestTypeDef",
    {
        "Name": str,
        "MetricName": str,
        "ChangeToken": str,
    },
)
_OptionalCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleGroupRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRuleGroupRequestRequestTypeDef(
    _RequiredCreateRuleGroupRequestRequestTypeDef, _OptionalCreateRuleGroupRequestRequestTypeDef
):
    pass


_RequiredCreateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleRequestRequestTypeDef",
    {
        "Name": str,
        "MetricName": str,
        "ChangeToken": str,
    },
)
_OptionalCreateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateRuleRequestRequestTypeDef(
    _RequiredCreateRuleRequestRequestTypeDef, _OptionalCreateRuleRequestRequestTypeDef
):
    pass


_RequiredCreateWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWebACLRequestRequestTypeDef",
    {
        "Name": str,
        "MetricName": str,
        "DefaultAction": WafActionTypeDef,
        "ChangeToken": str,
    },
)
_OptionalCreateWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWebACLRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWebACLRequestRequestTypeDef(
    _RequiredCreateWebACLRequestRequestTypeDef, _OptionalCreateWebACLRequestRequestTypeDef
):
    pass


TagInfoForResourceTypeDef = TypedDict(
    "TagInfoForResourceTypeDef",
    {
        "ResourceARN": str,
        "TagList": List[TagTypeDef],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateRegexPatternSetResponseTypeDef = TypedDict(
    "CreateRegexPatternSetResponseTypeDef",
    {
        "RegexPatternSet": RegexPatternSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRegexPatternSetResponseTypeDef = TypedDict(
    "GetRegexPatternSetResponseTypeDef",
    {
        "RegexPatternSet": RegexPatternSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleGroupResponseTypeDef = TypedDict(
    "CreateRuleGroupResponseTypeDef",
    {
        "RuleGroup": RuleGroupTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRuleGroupResponseTypeDef = TypedDict(
    "GetRuleGroupResponseTypeDef",
    {
        "RuleGroup": RuleGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGeoMatchSetTypeDef = TypedDict(
    "_RequiredGeoMatchSetTypeDef",
    {
        "GeoMatchSetId": str,
        "GeoMatchConstraints": List[GeoMatchConstraintTypeDef],
    },
)
_OptionalGeoMatchSetTypeDef = TypedDict(
    "_OptionalGeoMatchSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class GeoMatchSetTypeDef(_RequiredGeoMatchSetTypeDef, _OptionalGeoMatchSetTypeDef):
    pass


GeoMatchSetUpdateTypeDef = TypedDict(
    "GeoMatchSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "GeoMatchConstraint": GeoMatchConstraintTypeDef,
    },
)

ListGeoMatchSetsResponseTypeDef = TypedDict(
    "ListGeoMatchSetsResponseTypeDef",
    {
        "NextMarker": str,
        "GeoMatchSets": List[GeoMatchSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSampledRequestsRequestRequestTypeDef = TypedDict(
    "GetSampledRequestsRequestRequestTypeDef",
    {
        "WebAclId": str,
        "RuleId": str,
        "TimeWindow": TimeWindowTypeDef,
        "MaxItems": int,
    },
)

GetWebACLForResourceResponseTypeDef = TypedDict(
    "GetWebACLForResourceResponseTypeDef",
    {
        "WebACLSummary": WebACLSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWebACLsResponseTypeDef = TypedDict(
    "ListWebACLsResponseTypeDef",
    {
        "NextMarker": str,
        "WebACLs": List[WebACLSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HTTPRequestTypeDef = TypedDict(
    "HTTPRequestTypeDef",
    {
        "ClientIP": str,
        "Country": str,
        "URI": str,
        "Method": str,
        "HTTPVersion": str,
        "Headers": List[HTTPHeaderTypeDef],
    },
    total=False,
)

_RequiredIPSetTypeDef = TypedDict(
    "_RequiredIPSetTypeDef",
    {
        "IPSetId": str,
        "IPSetDescriptors": List[IPSetDescriptorTypeDef],
    },
)
_OptionalIPSetTypeDef = TypedDict(
    "_OptionalIPSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class IPSetTypeDef(_RequiredIPSetTypeDef, _OptionalIPSetTypeDef):
    pass


IPSetUpdateTypeDef = TypedDict(
    "IPSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "IPSetDescriptor": IPSetDescriptorTypeDef,
    },
)

ListIPSetsResponseTypeDef = TypedDict(
    "ListIPSetsResponseTypeDef",
    {
        "NextMarker": str,
        "IPSets": List[IPSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRateBasedRulesResponseTypeDef = TypedDict(
    "ListRateBasedRulesResponseTypeDef",
    {
        "NextMarker": str,
        "Rules": List[RuleSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "NextMarker": str,
        "Rules": List[RuleSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRegexMatchSetsResponseTypeDef = TypedDict(
    "ListRegexMatchSetsResponseTypeDef",
    {
        "NextMarker": str,
        "RegexMatchSets": List[RegexMatchSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRegexPatternSetsResponseTypeDef = TypedDict(
    "ListRegexPatternSetsResponseTypeDef",
    {
        "NextMarker": str,
        "RegexPatternSets": List[RegexPatternSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRuleGroupsResponseTypeDef = TypedDict(
    "ListRuleGroupsResponseTypeDef",
    {
        "NextMarker": str,
        "RuleGroups": List[RuleGroupSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSizeConstraintSetsResponseTypeDef = TypedDict(
    "ListSizeConstraintSetsResponseTypeDef",
    {
        "NextMarker": str,
        "SizeConstraintSets": List[SizeConstraintSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSqlInjectionMatchSetsResponseTypeDef = TypedDict(
    "ListSqlInjectionMatchSetsResponseTypeDef",
    {
        "NextMarker": str,
        "SqlInjectionMatchSets": List[SqlInjectionMatchSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscribedRuleGroupsResponseTypeDef = TypedDict(
    "ListSubscribedRuleGroupsResponseTypeDef",
    {
        "NextMarker": str,
        "RuleGroups": List[SubscribedRuleGroupSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListXssMatchSetsResponseTypeDef = TypedDict(
    "ListXssMatchSetsResponseTypeDef",
    {
        "NextMarker": str,
        "XssMatchSets": List[XssMatchSetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRateBasedRuleTypeDef = TypedDict(
    "_RequiredRateBasedRuleTypeDef",
    {
        "RuleId": str,
        "MatchPredicates": List[PredicateTypeDef],
        "RateKey": Literal["IP"],
        "RateLimit": int,
    },
)
_OptionalRateBasedRuleTypeDef = TypedDict(
    "_OptionalRateBasedRuleTypeDef",
    {
        "Name": str,
        "MetricName": str,
    },
    total=False,
)


class RateBasedRuleTypeDef(_RequiredRateBasedRuleTypeDef, _OptionalRateBasedRuleTypeDef):
    pass


_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef",
    {
        "RuleId": str,
        "Predicates": List[PredicateTypeDef],
    },
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef",
    {
        "Name": str,
        "MetricName": str,
    },
    total=False,
)


class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass


RuleUpdateTypeDef = TypedDict(
    "RuleUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "Predicate": PredicateTypeDef,
    },
)

UpdateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "UpdateRegexPatternSetRequestRequestTypeDef",
    {
        "RegexPatternSetId": str,
        "Updates": Sequence[RegexPatternSetUpdateTypeDef],
        "ChangeToken": str,
    },
)

ListActivatedRulesInRuleGroupResponseTypeDef = TypedDict(
    "ListActivatedRulesInRuleGroupResponseTypeDef",
    {
        "NextMarker": str,
        "ActivatedRules": List[ActivatedRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleGroupUpdateTypeDef = TypedDict(
    "RuleGroupUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "ActivatedRule": ActivatedRuleTypeDef,
    },
)

_RequiredWebACLTypeDef = TypedDict(
    "_RequiredWebACLTypeDef",
    {
        "WebACLId": str,
        "DefaultAction": WafActionTypeDef,
        "Rules": List[ActivatedRuleTypeDef],
    },
)
_OptionalWebACLTypeDef = TypedDict(
    "_OptionalWebACLTypeDef",
    {
        "Name": str,
        "MetricName": str,
        "WebACLArn": str,
    },
    total=False,
)


class WebACLTypeDef(_RequiredWebACLTypeDef, _OptionalWebACLTypeDef):
    pass


WebACLUpdateTypeDef = TypedDict(
    "WebACLUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "ActivatedRule": ActivatedRuleTypeDef,
    },
)

_RequiredByteMatchSetTypeDef = TypedDict(
    "_RequiredByteMatchSetTypeDef",
    {
        "ByteMatchSetId": str,
        "ByteMatchTuples": List[ByteMatchTupleTypeDef],
    },
)
_OptionalByteMatchSetTypeDef = TypedDict(
    "_OptionalByteMatchSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class ByteMatchSetTypeDef(_RequiredByteMatchSetTypeDef, _OptionalByteMatchSetTypeDef):
    pass


ByteMatchSetUpdateTypeDef = TypedDict(
    "ByteMatchSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "ByteMatchTuple": ByteMatchTupleTypeDef,
    },
)

GetLoggingConfigurationResponseTypeDef = TypedDict(
    "GetLoggingConfigurationResponseTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLoggingConfigurationsResponseTypeDef = TypedDict(
    "ListLoggingConfigurationsResponseTypeDef",
    {
        "LoggingConfigurations": List[LoggingConfigurationTypeDef],
        "NextMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "PutLoggingConfigurationRequestRequestTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
    },
)

PutLoggingConfigurationResponseTypeDef = TypedDict(
    "PutLoggingConfigurationResponseTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegexMatchSetTypeDef = TypedDict(
    "RegexMatchSetTypeDef",
    {
        "RegexMatchSetId": str,
        "Name": str,
        "RegexMatchTuples": List[RegexMatchTupleTypeDef],
    },
    total=False,
)

RegexMatchSetUpdateTypeDef = TypedDict(
    "RegexMatchSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "RegexMatchTuple": RegexMatchTupleTypeDef,
    },
)

_RequiredSizeConstraintSetTypeDef = TypedDict(
    "_RequiredSizeConstraintSetTypeDef",
    {
        "SizeConstraintSetId": str,
        "SizeConstraints": List[SizeConstraintTypeDef],
    },
)
_OptionalSizeConstraintSetTypeDef = TypedDict(
    "_OptionalSizeConstraintSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class SizeConstraintSetTypeDef(
    _RequiredSizeConstraintSetTypeDef, _OptionalSizeConstraintSetTypeDef
):
    pass


SizeConstraintSetUpdateTypeDef = TypedDict(
    "SizeConstraintSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "SizeConstraint": SizeConstraintTypeDef,
    },
)

_RequiredSqlInjectionMatchSetTypeDef = TypedDict(
    "_RequiredSqlInjectionMatchSetTypeDef",
    {
        "SqlInjectionMatchSetId": str,
        "SqlInjectionMatchTuples": List[SqlInjectionMatchTupleTypeDef],
    },
)
_OptionalSqlInjectionMatchSetTypeDef = TypedDict(
    "_OptionalSqlInjectionMatchSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class SqlInjectionMatchSetTypeDef(
    _RequiredSqlInjectionMatchSetTypeDef, _OptionalSqlInjectionMatchSetTypeDef
):
    pass


SqlInjectionMatchSetUpdateTypeDef = TypedDict(
    "SqlInjectionMatchSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "SqlInjectionMatchTuple": SqlInjectionMatchTupleTypeDef,
    },
)

_RequiredXssMatchSetTypeDef = TypedDict(
    "_RequiredXssMatchSetTypeDef",
    {
        "XssMatchSetId": str,
        "XssMatchTuples": List[XssMatchTupleTypeDef],
    },
)
_OptionalXssMatchSetTypeDef = TypedDict(
    "_OptionalXssMatchSetTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class XssMatchSetTypeDef(_RequiredXssMatchSetTypeDef, _OptionalXssMatchSetTypeDef):
    pass


XssMatchSetUpdateTypeDef = TypedDict(
    "XssMatchSetUpdateTypeDef",
    {
        "Action": ChangeActionType,
        "XssMatchTuple": XssMatchTupleTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "NextMarker": str,
        "TagInfoForResource": TagInfoForResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGeoMatchSetResponseTypeDef = TypedDict(
    "CreateGeoMatchSetResponseTypeDef",
    {
        "GeoMatchSet": GeoMatchSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGeoMatchSetResponseTypeDef = TypedDict(
    "GetGeoMatchSetResponseTypeDef",
    {
        "GeoMatchSet": GeoMatchSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGeoMatchSetRequestRequestTypeDef = TypedDict(
    "UpdateGeoMatchSetRequestRequestTypeDef",
    {
        "GeoMatchSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[GeoMatchSetUpdateTypeDef],
    },
)

_RequiredSampledHTTPRequestTypeDef = TypedDict(
    "_RequiredSampledHTTPRequestTypeDef",
    {
        "Request": HTTPRequestTypeDef,
        "Weight": int,
    },
)
_OptionalSampledHTTPRequestTypeDef = TypedDict(
    "_OptionalSampledHTTPRequestTypeDef",
    {
        "Timestamp": datetime,
        "Action": str,
        "RuleWithinRuleGroup": str,
    },
    total=False,
)


class SampledHTTPRequestTypeDef(
    _RequiredSampledHTTPRequestTypeDef, _OptionalSampledHTTPRequestTypeDef
):
    pass


CreateIPSetResponseTypeDef = TypedDict(
    "CreateIPSetResponseTypeDef",
    {
        "IPSet": IPSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIPSetResponseTypeDef = TypedDict(
    "GetIPSetResponseTypeDef",
    {
        "IPSet": IPSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIPSetRequestRequestTypeDef = TypedDict(
    "UpdateIPSetRequestRequestTypeDef",
    {
        "IPSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[IPSetUpdateTypeDef],
    },
)

CreateRateBasedRuleResponseTypeDef = TypedDict(
    "CreateRateBasedRuleResponseTypeDef",
    {
        "Rule": RateBasedRuleTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRateBasedRuleResponseTypeDef = TypedDict(
    "GetRateBasedRuleResponseTypeDef",
    {
        "Rule": RateBasedRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "Rule": RuleTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRuleResponseTypeDef = TypedDict(
    "GetRuleResponseTypeDef",
    {
        "Rule": RuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRateBasedRuleRequestRequestTypeDef = TypedDict(
    "UpdateRateBasedRuleRequestRequestTypeDef",
    {
        "RuleId": str,
        "ChangeToken": str,
        "Updates": Sequence[RuleUpdateTypeDef],
        "RateLimit": int,
    },
)

UpdateRuleRequestRequestTypeDef = TypedDict(
    "UpdateRuleRequestRequestTypeDef",
    {
        "RuleId": str,
        "ChangeToken": str,
        "Updates": Sequence[RuleUpdateTypeDef],
    },
)

UpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "UpdateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupId": str,
        "Updates": Sequence[RuleGroupUpdateTypeDef],
        "ChangeToken": str,
    },
)

CreateWebACLResponseTypeDef = TypedDict(
    "CreateWebACLResponseTypeDef",
    {
        "WebACL": WebACLTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWebACLResponseTypeDef = TypedDict(
    "GetWebACLResponseTypeDef",
    {
        "WebACL": WebACLTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWebACLRequestRequestTypeDef",
    {
        "WebACLId": str,
        "ChangeToken": str,
    },
)
_OptionalUpdateWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWebACLRequestRequestTypeDef",
    {
        "Updates": Sequence[WebACLUpdateTypeDef],
        "DefaultAction": WafActionTypeDef,
    },
    total=False,
)


class UpdateWebACLRequestRequestTypeDef(
    _RequiredUpdateWebACLRequestRequestTypeDef, _OptionalUpdateWebACLRequestRequestTypeDef
):
    pass


CreateByteMatchSetResponseTypeDef = TypedDict(
    "CreateByteMatchSetResponseTypeDef",
    {
        "ByteMatchSet": ByteMatchSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetByteMatchSetResponseTypeDef = TypedDict(
    "GetByteMatchSetResponseTypeDef",
    {
        "ByteMatchSet": ByteMatchSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateByteMatchSetRequestRequestTypeDef = TypedDict(
    "UpdateByteMatchSetRequestRequestTypeDef",
    {
        "ByteMatchSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[ByteMatchSetUpdateTypeDef],
    },
)

CreateRegexMatchSetResponseTypeDef = TypedDict(
    "CreateRegexMatchSetResponseTypeDef",
    {
        "RegexMatchSet": RegexMatchSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRegexMatchSetResponseTypeDef = TypedDict(
    "GetRegexMatchSetResponseTypeDef",
    {
        "RegexMatchSet": RegexMatchSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRegexMatchSetRequestRequestTypeDef = TypedDict(
    "UpdateRegexMatchSetRequestRequestTypeDef",
    {
        "RegexMatchSetId": str,
        "Updates": Sequence[RegexMatchSetUpdateTypeDef],
        "ChangeToken": str,
    },
)

CreateSizeConstraintSetResponseTypeDef = TypedDict(
    "CreateSizeConstraintSetResponseTypeDef",
    {
        "SizeConstraintSet": SizeConstraintSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSizeConstraintSetResponseTypeDef = TypedDict(
    "GetSizeConstraintSetResponseTypeDef",
    {
        "SizeConstraintSet": SizeConstraintSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSizeConstraintSetRequestRequestTypeDef = TypedDict(
    "UpdateSizeConstraintSetRequestRequestTypeDef",
    {
        "SizeConstraintSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[SizeConstraintSetUpdateTypeDef],
    },
)

CreateSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "CreateSqlInjectionMatchSetResponseTypeDef",
    {
        "SqlInjectionMatchSet": SqlInjectionMatchSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "GetSqlInjectionMatchSetResponseTypeDef",
    {
        "SqlInjectionMatchSet": SqlInjectionMatchSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSqlInjectionMatchSetRequestRequestTypeDef = TypedDict(
    "UpdateSqlInjectionMatchSetRequestRequestTypeDef",
    {
        "SqlInjectionMatchSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[SqlInjectionMatchSetUpdateTypeDef],
    },
)

CreateXssMatchSetResponseTypeDef = TypedDict(
    "CreateXssMatchSetResponseTypeDef",
    {
        "XssMatchSet": XssMatchSetTypeDef,
        "ChangeToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetXssMatchSetResponseTypeDef = TypedDict(
    "GetXssMatchSetResponseTypeDef",
    {
        "XssMatchSet": XssMatchSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateXssMatchSetRequestRequestTypeDef = TypedDict(
    "UpdateXssMatchSetRequestRequestTypeDef",
    {
        "XssMatchSetId": str,
        "ChangeToken": str,
        "Updates": Sequence[XssMatchSetUpdateTypeDef],
    },
)

GetSampledRequestsResponseTypeDef = TypedDict(
    "GetSampledRequestsResponseTypeDef",
    {
        "SampledRequests": List[SampledHTTPRequestTypeDef],
        "PopulationSize": int,
        "TimeWindow": TimeWindowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
