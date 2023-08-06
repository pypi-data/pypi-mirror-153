"""
Type annotations for shield service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_shield/type_defs/)

Usage::

    ```python
    from mypy_boto3_shield.type_defs import ResponseActionTypeDef

    data: ResponseActionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    ApplicationLayerAutomaticResponseStatusType,
    AttackLayerType,
    AttackPropertyIdentifierType,
    AutoRenewType,
    ProactiveEngagementStatusType,
    ProtectedResourceTypeType,
    ProtectionGroupAggregationType,
    ProtectionGroupPatternType,
    SubResourceTypeType,
    SubscriptionStateType,
    UnitType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseActionTypeDef",
    "AssociateDRTLogBucketRequestRequestTypeDef",
    "AssociateDRTRoleRequestRequestTypeDef",
    "AssociateHealthCheckRequestRequestTypeDef",
    "EmergencyContactTypeDef",
    "MitigationTypeDef",
    "SummarizedCounterTypeDef",
    "ContributorTypeDef",
    "AttackVectorDescriptionTypeDef",
    "AttackVolumeStatisticsTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteProtectionGroupRequestRequestTypeDef",
    "DeleteProtectionRequestRequestTypeDef",
    "DescribeAttackRequestRequestTypeDef",
    "TimeRangeTypeDef",
    "DescribeProtectionGroupRequestRequestTypeDef",
    "ProtectionGroupTypeDef",
    "DescribeProtectionRequestRequestTypeDef",
    "DisableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "DisassociateDRTLogBucketRequestRequestTypeDef",
    "DisassociateHealthCheckRequestRequestTypeDef",
    "LimitTypeDef",
    "PaginatorConfigTypeDef",
    "ListProtectionGroupsRequestRequestTypeDef",
    "ListProtectionsRequestRequestTypeDef",
    "ListResourcesInProtectionGroupRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ProtectionGroupArbitraryPatternLimitsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateProtectionGroupRequestRequestTypeDef",
    "UpdateSubscriptionRequestRequestTypeDef",
    "ApplicationLayerAutomaticResponseConfigurationTypeDef",
    "EnableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "UpdateApplicationLayerAutomaticResponseRequestRequestTypeDef",
    "AssociateProactiveEngagementDetailsRequestRequestTypeDef",
    "UpdateEmergencyContactSettingsRequestRequestTypeDef",
    "SummarizedAttackVectorTypeDef",
    "AttackPropertyTypeDef",
    "AttackSummaryTypeDef",
    "AttackVolumeTypeDef",
    "CreateProtectionGroupRequestRequestTypeDef",
    "CreateProtectionRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateProtectionResponseTypeDef",
    "DescribeDRTAccessResponseTypeDef",
    "DescribeEmergencyContactSettingsResponseTypeDef",
    "GetSubscriptionStateResponseTypeDef",
    "ListResourcesInProtectionGroupResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListAttacksRequestRequestTypeDef",
    "DescribeProtectionGroupResponseTypeDef",
    "ListProtectionGroupsResponseTypeDef",
    "ProtectionLimitsTypeDef",
    "ListAttacksRequestListAttacksPaginateTypeDef",
    "ListProtectionsRequestListProtectionsPaginateTypeDef",
    "ProtectionGroupPatternTypeLimitsTypeDef",
    "ProtectionTypeDef",
    "SubResourceSummaryTypeDef",
    "ListAttacksResponseTypeDef",
    "AttackStatisticsDataItemTypeDef",
    "ProtectionGroupLimitsTypeDef",
    "DescribeProtectionResponseTypeDef",
    "ListProtectionsResponseTypeDef",
    "AttackDetailTypeDef",
    "DescribeAttackStatisticsResponseTypeDef",
    "SubscriptionLimitsTypeDef",
    "DescribeAttackResponseTypeDef",
    "SubscriptionTypeDef",
    "DescribeSubscriptionResponseTypeDef",
)

ResponseActionTypeDef = TypedDict(
    "ResponseActionTypeDef",
    {
        "Block": Dict[str, Any],
        "Count": Dict[str, Any],
    },
    total=False,
)

AssociateDRTLogBucketRequestRequestTypeDef = TypedDict(
    "AssociateDRTLogBucketRequestRequestTypeDef",
    {
        "LogBucket": str,
    },
)

AssociateDRTRoleRequestRequestTypeDef = TypedDict(
    "AssociateDRTRoleRequestRequestTypeDef",
    {
        "RoleArn": str,
    },
)

AssociateHealthCheckRequestRequestTypeDef = TypedDict(
    "AssociateHealthCheckRequestRequestTypeDef",
    {
        "ProtectionId": str,
        "HealthCheckArn": str,
    },
)

_RequiredEmergencyContactTypeDef = TypedDict(
    "_RequiredEmergencyContactTypeDef",
    {
        "EmailAddress": str,
    },
)
_OptionalEmergencyContactTypeDef = TypedDict(
    "_OptionalEmergencyContactTypeDef",
    {
        "PhoneNumber": str,
        "ContactNotes": str,
    },
    total=False,
)


class EmergencyContactTypeDef(_RequiredEmergencyContactTypeDef, _OptionalEmergencyContactTypeDef):
    pass


MitigationTypeDef = TypedDict(
    "MitigationTypeDef",
    {
        "MitigationName": str,
    },
    total=False,
)

SummarizedCounterTypeDef = TypedDict(
    "SummarizedCounterTypeDef",
    {
        "Name": str,
        "Max": float,
        "Average": float,
        "Sum": float,
        "N": int,
        "Unit": str,
    },
    total=False,
)

ContributorTypeDef = TypedDict(
    "ContributorTypeDef",
    {
        "Name": str,
        "Value": int,
    },
    total=False,
)

AttackVectorDescriptionTypeDef = TypedDict(
    "AttackVectorDescriptionTypeDef",
    {
        "VectorType": str,
    },
)

AttackVolumeStatisticsTypeDef = TypedDict(
    "AttackVolumeStatisticsTypeDef",
    {
        "Max": float,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

DeleteProtectionGroupRequestRequestTypeDef = TypedDict(
    "DeleteProtectionGroupRequestRequestTypeDef",
    {
        "ProtectionGroupId": str,
    },
)

DeleteProtectionRequestRequestTypeDef = TypedDict(
    "DeleteProtectionRequestRequestTypeDef",
    {
        "ProtectionId": str,
    },
)

DescribeAttackRequestRequestTypeDef = TypedDict(
    "DescribeAttackRequestRequestTypeDef",
    {
        "AttackId": str,
    },
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef",
    {
        "FromInclusive": datetime,
        "ToExclusive": datetime,
    },
    total=False,
)

DescribeProtectionGroupRequestRequestTypeDef = TypedDict(
    "DescribeProtectionGroupRequestRequestTypeDef",
    {
        "ProtectionGroupId": str,
    },
)

_RequiredProtectionGroupTypeDef = TypedDict(
    "_RequiredProtectionGroupTypeDef",
    {
        "ProtectionGroupId": str,
        "Aggregation": ProtectionGroupAggregationType,
        "Pattern": ProtectionGroupPatternType,
        "Members": List[str],
    },
)
_OptionalProtectionGroupTypeDef = TypedDict(
    "_OptionalProtectionGroupTypeDef",
    {
        "ResourceType": ProtectedResourceTypeType,
        "ProtectionGroupArn": str,
    },
    total=False,
)


class ProtectionGroupTypeDef(_RequiredProtectionGroupTypeDef, _OptionalProtectionGroupTypeDef):
    pass


DescribeProtectionRequestRequestTypeDef = TypedDict(
    "DescribeProtectionRequestRequestTypeDef",
    {
        "ProtectionId": str,
        "ResourceArn": str,
    },
    total=False,
)

DisableApplicationLayerAutomaticResponseRequestRequestTypeDef = TypedDict(
    "DisableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DisassociateDRTLogBucketRequestRequestTypeDef = TypedDict(
    "DisassociateDRTLogBucketRequestRequestTypeDef",
    {
        "LogBucket": str,
    },
)

DisassociateHealthCheckRequestRequestTypeDef = TypedDict(
    "DisassociateHealthCheckRequestRequestTypeDef",
    {
        "ProtectionId": str,
        "HealthCheckArn": str,
    },
)

LimitTypeDef = TypedDict(
    "LimitTypeDef",
    {
        "Type": str,
        "Max": int,
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

ListProtectionGroupsRequestRequestTypeDef = TypedDict(
    "ListProtectionGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListProtectionsRequestRequestTypeDef = TypedDict(
    "ListProtectionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListResourcesInProtectionGroupRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesInProtectionGroupRequestRequestTypeDef",
    {
        "ProtectionGroupId": str,
    },
)
_OptionalListResourcesInProtectionGroupRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesInProtectionGroupRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListResourcesInProtectionGroupRequestRequestTypeDef(
    _RequiredListResourcesInProtectionGroupRequestRequestTypeDef,
    _OptionalListResourcesInProtectionGroupRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

ProtectionGroupArbitraryPatternLimitsTypeDef = TypedDict(
    "ProtectionGroupArbitraryPatternLimitsTypeDef",
    {
        "MaxMembers": int,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateProtectionGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProtectionGroupRequestRequestTypeDef",
    {
        "ProtectionGroupId": str,
        "Aggregation": ProtectionGroupAggregationType,
        "Pattern": ProtectionGroupPatternType,
    },
)
_OptionalUpdateProtectionGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProtectionGroupRequestRequestTypeDef",
    {
        "ResourceType": ProtectedResourceTypeType,
        "Members": Sequence[str],
    },
    total=False,
)


class UpdateProtectionGroupRequestRequestTypeDef(
    _RequiredUpdateProtectionGroupRequestRequestTypeDef,
    _OptionalUpdateProtectionGroupRequestRequestTypeDef,
):
    pass


UpdateSubscriptionRequestRequestTypeDef = TypedDict(
    "UpdateSubscriptionRequestRequestTypeDef",
    {
        "AutoRenew": AutoRenewType,
    },
    total=False,
)

ApplicationLayerAutomaticResponseConfigurationTypeDef = TypedDict(
    "ApplicationLayerAutomaticResponseConfigurationTypeDef",
    {
        "Status": ApplicationLayerAutomaticResponseStatusType,
        "Action": ResponseActionTypeDef,
    },
)

EnableApplicationLayerAutomaticResponseRequestRequestTypeDef = TypedDict(
    "EnableApplicationLayerAutomaticResponseRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Action": ResponseActionTypeDef,
    },
)

UpdateApplicationLayerAutomaticResponseRequestRequestTypeDef = TypedDict(
    "UpdateApplicationLayerAutomaticResponseRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Action": ResponseActionTypeDef,
    },
)

AssociateProactiveEngagementDetailsRequestRequestTypeDef = TypedDict(
    "AssociateProactiveEngagementDetailsRequestRequestTypeDef",
    {
        "EmergencyContactList": Sequence[EmergencyContactTypeDef],
    },
)

UpdateEmergencyContactSettingsRequestRequestTypeDef = TypedDict(
    "UpdateEmergencyContactSettingsRequestRequestTypeDef",
    {
        "EmergencyContactList": Sequence[EmergencyContactTypeDef],
    },
    total=False,
)

_RequiredSummarizedAttackVectorTypeDef = TypedDict(
    "_RequiredSummarizedAttackVectorTypeDef",
    {
        "VectorType": str,
    },
)
_OptionalSummarizedAttackVectorTypeDef = TypedDict(
    "_OptionalSummarizedAttackVectorTypeDef",
    {
        "VectorCounters": List[SummarizedCounterTypeDef],
    },
    total=False,
)


class SummarizedAttackVectorTypeDef(
    _RequiredSummarizedAttackVectorTypeDef, _OptionalSummarizedAttackVectorTypeDef
):
    pass


AttackPropertyTypeDef = TypedDict(
    "AttackPropertyTypeDef",
    {
        "AttackLayer": AttackLayerType,
        "AttackPropertyIdentifier": AttackPropertyIdentifierType,
        "TopContributors": List[ContributorTypeDef],
        "Unit": UnitType,
        "Total": int,
    },
    total=False,
)

AttackSummaryTypeDef = TypedDict(
    "AttackSummaryTypeDef",
    {
        "AttackId": str,
        "ResourceArn": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "AttackVectors": List[AttackVectorDescriptionTypeDef],
    },
    total=False,
)

AttackVolumeTypeDef = TypedDict(
    "AttackVolumeTypeDef",
    {
        "BitsPerSecond": AttackVolumeStatisticsTypeDef,
        "PacketsPerSecond": AttackVolumeStatisticsTypeDef,
        "RequestsPerSecond": AttackVolumeStatisticsTypeDef,
    },
    total=False,
)

_RequiredCreateProtectionGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProtectionGroupRequestRequestTypeDef",
    {
        "ProtectionGroupId": str,
        "Aggregation": ProtectionGroupAggregationType,
        "Pattern": ProtectionGroupPatternType,
    },
)
_OptionalCreateProtectionGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProtectionGroupRequestRequestTypeDef",
    {
        "ResourceType": ProtectedResourceTypeType,
        "Members": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateProtectionGroupRequestRequestTypeDef(
    _RequiredCreateProtectionGroupRequestRequestTypeDef,
    _OptionalCreateProtectionGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateProtectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProtectionRequestRequestTypeDef",
    {
        "Name": str,
        "ResourceArn": str,
    },
)
_OptionalCreateProtectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProtectionRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateProtectionRequestRequestTypeDef(
    _RequiredCreateProtectionRequestRequestTypeDef, _OptionalCreateProtectionRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateProtectionResponseTypeDef = TypedDict(
    "CreateProtectionResponseTypeDef",
    {
        "ProtectionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDRTAccessResponseTypeDef = TypedDict(
    "DescribeDRTAccessResponseTypeDef",
    {
        "RoleArn": str,
        "LogBucketList": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEmergencyContactSettingsResponseTypeDef = TypedDict(
    "DescribeEmergencyContactSettingsResponseTypeDef",
    {
        "EmergencyContactList": List[EmergencyContactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriptionStateResponseTypeDef = TypedDict(
    "GetSubscriptionStateResponseTypeDef",
    {
        "SubscriptionState": SubscriptionStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResourcesInProtectionGroupResponseTypeDef = TypedDict(
    "ListResourcesInProtectionGroupResponseTypeDef",
    {
        "ResourceArns": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttacksRequestRequestTypeDef = TypedDict(
    "ListAttacksRequestRequestTypeDef",
    {
        "ResourceArns": Sequence[str],
        "StartTime": TimeRangeTypeDef,
        "EndTime": TimeRangeTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeProtectionGroupResponseTypeDef = TypedDict(
    "DescribeProtectionGroupResponseTypeDef",
    {
        "ProtectionGroup": ProtectionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProtectionGroupsResponseTypeDef = TypedDict(
    "ListProtectionGroupsResponseTypeDef",
    {
        "ProtectionGroups": List[ProtectionGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProtectionLimitsTypeDef = TypedDict(
    "ProtectionLimitsTypeDef",
    {
        "ProtectedResourceTypeLimits": List[LimitTypeDef],
    },
)

ListAttacksRequestListAttacksPaginateTypeDef = TypedDict(
    "ListAttacksRequestListAttacksPaginateTypeDef",
    {
        "ResourceArns": Sequence[str],
        "StartTime": TimeRangeTypeDef,
        "EndTime": TimeRangeTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProtectionsRequestListProtectionsPaginateTypeDef = TypedDict(
    "ListProtectionsRequestListProtectionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ProtectionGroupPatternTypeLimitsTypeDef = TypedDict(
    "ProtectionGroupPatternTypeLimitsTypeDef",
    {
        "ArbitraryPatternLimits": ProtectionGroupArbitraryPatternLimitsTypeDef,
    },
)

ProtectionTypeDef = TypedDict(
    "ProtectionTypeDef",
    {
        "Id": str,
        "Name": str,
        "ResourceArn": str,
        "HealthCheckIds": List[str],
        "ProtectionArn": str,
        "ApplicationLayerAutomaticResponseConfiguration": ApplicationLayerAutomaticResponseConfigurationTypeDef,
    },
    total=False,
)

SubResourceSummaryTypeDef = TypedDict(
    "SubResourceSummaryTypeDef",
    {
        "Type": SubResourceTypeType,
        "Id": str,
        "AttackVectors": List[SummarizedAttackVectorTypeDef],
        "Counters": List[SummarizedCounterTypeDef],
    },
    total=False,
)

ListAttacksResponseTypeDef = TypedDict(
    "ListAttacksResponseTypeDef",
    {
        "AttackSummaries": List[AttackSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAttackStatisticsDataItemTypeDef = TypedDict(
    "_RequiredAttackStatisticsDataItemTypeDef",
    {
        "AttackCount": int,
    },
)
_OptionalAttackStatisticsDataItemTypeDef = TypedDict(
    "_OptionalAttackStatisticsDataItemTypeDef",
    {
        "AttackVolume": AttackVolumeTypeDef,
    },
    total=False,
)


class AttackStatisticsDataItemTypeDef(
    _RequiredAttackStatisticsDataItemTypeDef, _OptionalAttackStatisticsDataItemTypeDef
):
    pass


ProtectionGroupLimitsTypeDef = TypedDict(
    "ProtectionGroupLimitsTypeDef",
    {
        "MaxProtectionGroups": int,
        "PatternTypeLimits": ProtectionGroupPatternTypeLimitsTypeDef,
    },
)

DescribeProtectionResponseTypeDef = TypedDict(
    "DescribeProtectionResponseTypeDef",
    {
        "Protection": ProtectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProtectionsResponseTypeDef = TypedDict(
    "ListProtectionsResponseTypeDef",
    {
        "Protections": List[ProtectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AttackDetailTypeDef = TypedDict(
    "AttackDetailTypeDef",
    {
        "AttackId": str,
        "ResourceArn": str,
        "SubResources": List[SubResourceSummaryTypeDef],
        "StartTime": datetime,
        "EndTime": datetime,
        "AttackCounters": List[SummarizedCounterTypeDef],
        "AttackProperties": List[AttackPropertyTypeDef],
        "Mitigations": List[MitigationTypeDef],
    },
    total=False,
)

DescribeAttackStatisticsResponseTypeDef = TypedDict(
    "DescribeAttackStatisticsResponseTypeDef",
    {
        "TimeRange": TimeRangeTypeDef,
        "DataItems": List[AttackStatisticsDataItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubscriptionLimitsTypeDef = TypedDict(
    "SubscriptionLimitsTypeDef",
    {
        "ProtectionLimits": ProtectionLimitsTypeDef,
        "ProtectionGroupLimits": ProtectionGroupLimitsTypeDef,
    },
)

DescribeAttackResponseTypeDef = TypedDict(
    "DescribeAttackResponseTypeDef",
    {
        "Attack": AttackDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSubscriptionTypeDef = TypedDict(
    "_RequiredSubscriptionTypeDef",
    {
        "SubscriptionLimits": SubscriptionLimitsTypeDef,
    },
)
_OptionalSubscriptionTypeDef = TypedDict(
    "_OptionalSubscriptionTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
        "TimeCommitmentInSeconds": int,
        "AutoRenew": AutoRenewType,
        "Limits": List[LimitTypeDef],
        "ProactiveEngagementStatus": ProactiveEngagementStatusType,
        "SubscriptionArn": str,
    },
    total=False,
)


class SubscriptionTypeDef(_RequiredSubscriptionTypeDef, _OptionalSubscriptionTypeDef):
    pass


DescribeSubscriptionResponseTypeDef = TypedDict(
    "DescribeSubscriptionResponseTypeDef",
    {
        "Subscription": SubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
