"""
Type annotations for dlm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/type_defs/)

Usage::

    ```python
    from mypy_boto3_dlm.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    GettablePolicyStateValuesType,
    LocationValuesType,
    PolicyTypeValuesType,
    ResourceLocationValuesType,
    ResourceTypeValuesType,
    RetentionIntervalUnitValuesType,
    SettablePolicyStateValuesType,
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
    "CreateRuleTypeDef",
    "CrossRegionCopyRetainRuleTypeDef",
    "EncryptionConfigurationTypeDef",
    "CrossRegionCopyDeprecateRuleTypeDef",
    "DeleteLifecyclePolicyRequestRequestTypeDef",
    "DeprecateRuleTypeDef",
    "EventParametersTypeDef",
    "FastRestoreRuleTypeDef",
    "GetLifecyclePoliciesRequestRequestTypeDef",
    "LifecyclePolicySummaryTypeDef",
    "GetLifecyclePolicyRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ParametersTypeDef",
    "TagTypeDef",
    "RetainRuleTypeDef",
    "ShareRuleTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateLifecyclePolicyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CrossRegionCopyActionTypeDef",
    "CrossRegionCopyRuleTypeDef",
    "EventSourceTypeDef",
    "GetLifecyclePoliciesResponseTypeDef",
    "ActionTypeDef",
    "ScheduleTypeDef",
    "PolicyDetailsTypeDef",
    "CreateLifecyclePolicyRequestRequestTypeDef",
    "LifecyclePolicyTypeDef",
    "UpdateLifecyclePolicyRequestRequestTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
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

CreateRuleTypeDef = TypedDict(
    "CreateRuleTypeDef",
    {
        "Location": LocationValuesType,
        "Interval": int,
        "IntervalUnit": Literal["HOURS"],
        "Times": Sequence[str],
        "CronExpression": str,
    },
    total=False,
)

CrossRegionCopyRetainRuleTypeDef = TypedDict(
    "CrossRegionCopyRetainRuleTypeDef",
    {
        "Interval": int,
        "IntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)

_RequiredEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredEncryptionConfigurationTypeDef",
    {
        "Encrypted": bool,
    },
)
_OptionalEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalEncryptionConfigurationTypeDef",
    {
        "CmkArn": str,
    },
    total=False,
)


class EncryptionConfigurationTypeDef(
    _RequiredEncryptionConfigurationTypeDef, _OptionalEncryptionConfigurationTypeDef
):
    pass


CrossRegionCopyDeprecateRuleTypeDef = TypedDict(
    "CrossRegionCopyDeprecateRuleTypeDef",
    {
        "Interval": int,
        "IntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)

DeleteLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "DeleteLifecyclePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

DeprecateRuleTypeDef = TypedDict(
    "DeprecateRuleTypeDef",
    {
        "Count": int,
        "Interval": int,
        "IntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)

EventParametersTypeDef = TypedDict(
    "EventParametersTypeDef",
    {
        "EventType": Literal["shareSnapshot"],
        "SnapshotOwner": Sequence[str],
        "DescriptionRegex": str,
    },
)

_RequiredFastRestoreRuleTypeDef = TypedDict(
    "_RequiredFastRestoreRuleTypeDef",
    {
        "AvailabilityZones": Sequence[str],
    },
)
_OptionalFastRestoreRuleTypeDef = TypedDict(
    "_OptionalFastRestoreRuleTypeDef",
    {
        "Count": int,
        "Interval": int,
        "IntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)


class FastRestoreRuleTypeDef(_RequiredFastRestoreRuleTypeDef, _OptionalFastRestoreRuleTypeDef):
    pass


GetLifecyclePoliciesRequestRequestTypeDef = TypedDict(
    "GetLifecyclePoliciesRequestRequestTypeDef",
    {
        "PolicyIds": Sequence[str],
        "State": GettablePolicyStateValuesType,
        "ResourceTypes": Sequence[ResourceTypeValuesType],
        "TargetTags": Sequence[str],
        "TagsToAdd": Sequence[str],
    },
    total=False,
)

LifecyclePolicySummaryTypeDef = TypedDict(
    "LifecyclePolicySummaryTypeDef",
    {
        "PolicyId": str,
        "Description": str,
        "State": GettablePolicyStateValuesType,
        "Tags": Dict[str, str],
        "PolicyType": PolicyTypeValuesType,
    },
    total=False,
)

GetLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "GetLifecyclePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ParametersTypeDef = TypedDict(
    "ParametersTypeDef",
    {
        "ExcludeBootVolume": bool,
        "NoReboot": bool,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

RetainRuleTypeDef = TypedDict(
    "RetainRuleTypeDef",
    {
        "Count": int,
        "Interval": int,
        "IntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)

_RequiredShareRuleTypeDef = TypedDict(
    "_RequiredShareRuleTypeDef",
    {
        "TargetAccounts": Sequence[str],
    },
)
_OptionalShareRuleTypeDef = TypedDict(
    "_OptionalShareRuleTypeDef",
    {
        "UnshareInterval": int,
        "UnshareIntervalUnit": RetentionIntervalUnitValuesType,
    },
    total=False,
)


class ShareRuleTypeDef(_RequiredShareRuleTypeDef, _OptionalShareRuleTypeDef):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

CreateLifecyclePolicyResponseTypeDef = TypedDict(
    "CreateLifecyclePolicyResponseTypeDef",
    {
        "PolicyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCrossRegionCopyActionTypeDef = TypedDict(
    "_RequiredCrossRegionCopyActionTypeDef",
    {
        "Target": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
)
_OptionalCrossRegionCopyActionTypeDef = TypedDict(
    "_OptionalCrossRegionCopyActionTypeDef",
    {
        "RetainRule": CrossRegionCopyRetainRuleTypeDef,
    },
    total=False,
)


class CrossRegionCopyActionTypeDef(
    _RequiredCrossRegionCopyActionTypeDef, _OptionalCrossRegionCopyActionTypeDef
):
    pass


_RequiredCrossRegionCopyRuleTypeDef = TypedDict(
    "_RequiredCrossRegionCopyRuleTypeDef",
    {
        "Encrypted": bool,
    },
)
_OptionalCrossRegionCopyRuleTypeDef = TypedDict(
    "_OptionalCrossRegionCopyRuleTypeDef",
    {
        "TargetRegion": str,
        "Target": str,
        "CmkArn": str,
        "CopyTags": bool,
        "RetainRule": CrossRegionCopyRetainRuleTypeDef,
        "DeprecateRule": CrossRegionCopyDeprecateRuleTypeDef,
    },
    total=False,
)


class CrossRegionCopyRuleTypeDef(
    _RequiredCrossRegionCopyRuleTypeDef, _OptionalCrossRegionCopyRuleTypeDef
):
    pass


_RequiredEventSourceTypeDef = TypedDict(
    "_RequiredEventSourceTypeDef",
    {
        "Type": Literal["MANAGED_CWE"],
    },
)
_OptionalEventSourceTypeDef = TypedDict(
    "_OptionalEventSourceTypeDef",
    {
        "Parameters": EventParametersTypeDef,
    },
    total=False,
)


class EventSourceTypeDef(_RequiredEventSourceTypeDef, _OptionalEventSourceTypeDef):
    pass


GetLifecyclePoliciesResponseTypeDef = TypedDict(
    "GetLifecyclePoliciesResponseTypeDef",
    {
        "Policies": List[LifecyclePolicySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "Name": str,
        "CrossRegionCopy": Sequence[CrossRegionCopyActionTypeDef],
    },
)

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "Name": str,
        "CopyTags": bool,
        "TagsToAdd": Sequence[TagTypeDef],
        "VariableTags": Sequence[TagTypeDef],
        "CreateRule": CreateRuleTypeDef,
        "RetainRule": RetainRuleTypeDef,
        "FastRestoreRule": FastRestoreRuleTypeDef,
        "CrossRegionCopyRules": Sequence[CrossRegionCopyRuleTypeDef],
        "ShareRules": Sequence[ShareRuleTypeDef],
        "DeprecateRule": DeprecateRuleTypeDef,
    },
    total=False,
)

PolicyDetailsTypeDef = TypedDict(
    "PolicyDetailsTypeDef",
    {
        "PolicyType": PolicyTypeValuesType,
        "ResourceTypes": Sequence[ResourceTypeValuesType],
        "ResourceLocations": Sequence[ResourceLocationValuesType],
        "TargetTags": Sequence[TagTypeDef],
        "Schedules": Sequence[ScheduleTypeDef],
        "Parameters": ParametersTypeDef,
        "EventSource": EventSourceTypeDef,
        "Actions": Sequence[ActionTypeDef],
    },
    total=False,
)

_RequiredCreateLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLifecyclePolicyRequestRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "Description": str,
        "State": SettablePolicyStateValuesType,
        "PolicyDetails": PolicyDetailsTypeDef,
    },
)
_OptionalCreateLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLifecyclePolicyRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateLifecyclePolicyRequestRequestTypeDef(
    _RequiredCreateLifecyclePolicyRequestRequestTypeDef,
    _OptionalCreateLifecyclePolicyRequestRequestTypeDef,
):
    pass


LifecyclePolicyTypeDef = TypedDict(
    "LifecyclePolicyTypeDef",
    {
        "PolicyId": str,
        "Description": str,
        "State": GettablePolicyStateValuesType,
        "StatusMessage": str,
        "ExecutionRoleArn": str,
        "DateCreated": datetime,
        "DateModified": datetime,
        "PolicyDetails": PolicyDetailsTypeDef,
        "Tags": Dict[str, str],
        "PolicyArn": str,
    },
    total=False,
)

_RequiredUpdateLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLifecyclePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalUpdateLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLifecyclePolicyRequestRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "State": SettablePolicyStateValuesType,
        "Description": str,
        "PolicyDetails": PolicyDetailsTypeDef,
    },
    total=False,
)


class UpdateLifecyclePolicyRequestRequestTypeDef(
    _RequiredUpdateLifecyclePolicyRequestRequestTypeDef,
    _OptionalUpdateLifecyclePolicyRequestRequestTypeDef,
):
    pass


GetLifecyclePolicyResponseTypeDef = TypedDict(
    "GetLifecyclePolicyResponseTypeDef",
    {
        "Policy": LifecyclePolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
