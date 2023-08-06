"""
Type annotations for rbin service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/type_defs/)

Usage::

    ```python
    from mypy_boto3_rbin.type_defs import ResourceTagTypeDef

    data: ResourceTagTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import ResourceTypeType, RuleStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ResourceTagTypeDef",
    "RetentionPeriodTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "GetRuleRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ListRulesRequestRequestTypeDef",
    "RuleSummaryTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "GetRuleResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateRuleResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesResponseTypeDef",
)

_RequiredResourceTagTypeDef = TypedDict(
    "_RequiredResourceTagTypeDef",
    {
        "ResourceTagKey": str,
    },
)
_OptionalResourceTagTypeDef = TypedDict(
    "_OptionalResourceTagTypeDef",
    {
        "ResourceTagValue": str,
    },
    total=False,
)

class ResourceTagTypeDef(_RequiredResourceTagTypeDef, _OptionalResourceTagTypeDef):
    pass

RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "RetentionPeriodValue": int,
        "RetentionPeriodUnit": Literal["DAYS"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
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

DeleteRuleRequestRequestTypeDef = TypedDict(
    "DeleteRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetRuleRequestRequestTypeDef = TypedDict(
    "GetRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
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

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredListRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListRulesRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
)
_OptionalListRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)

class ListRulesRequestRequestTypeDef(
    _RequiredListRulesRequestRequestTypeDef, _OptionalListRulesRequestRequestTypeDef
):
    pass

RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
    },
    total=False,
)

_RequiredUpdateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)
_OptionalUpdateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRuleRequestRequestTypeDef",
    {
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)

class UpdateRuleRequestRequestTypeDef(
    _RequiredUpdateRuleRequestRequestTypeDef, _OptionalUpdateRuleRequestRequestTypeDef
):
    pass

_RequiredCreateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleRequestRequestTypeDef",
    {
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceType": ResourceTypeType,
    },
)
_OptionalCreateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)

class CreateRuleRequestRequestTypeDef(
    _RequiredCreateRuleRequestRequestTypeDef, _OptionalCreateRuleRequestRequestTypeDef
):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "Identifier": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "Tags": List[TagTypeDef],
        "ResourceType": ResourceTypeType,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRuleResponseTypeDef = TypedDict(
    "GetRuleResponseTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
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

UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef",
    {
        "Identifier": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_RequiredListRulesRequestListRulesPaginateTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
)
_OptionalListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_OptionalListRulesRequestListRulesPaginateTypeDef",
    {
        "ResourceTags": Sequence[ResourceTagTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRulesRequestListRulesPaginateTypeDef(
    _RequiredListRulesRequestListRulesPaginateTypeDef,
    _OptionalListRulesRequestListRulesPaginateTypeDef,
):
    pass

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "Rules": List[RuleSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
