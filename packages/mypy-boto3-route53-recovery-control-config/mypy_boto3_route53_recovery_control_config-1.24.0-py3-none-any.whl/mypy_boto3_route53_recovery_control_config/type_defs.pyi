"""
Type annotations for route53-recovery-control-config service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_control_config.type_defs import RuleConfigTypeDef

    data: RuleConfigTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import RuleTypeType, StatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "RuleConfigTypeDef",
    "AssertionRuleUpdateTypeDef",
    "ClusterEndpointTypeDef",
    "ControlPanelTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateControlPanelRequestRequestTypeDef",
    "CreateRoutingControlRequestRequestTypeDef",
    "RoutingControlTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteControlPanelRequestRequestTypeDef",
    "DeleteRoutingControlRequestRequestTypeDef",
    "DeleteSafetyRuleRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeControlPanelRequestRequestTypeDef",
    "DescribeRoutingControlRequestRequestTypeDef",
    "DescribeSafetyRuleRequestRequestTypeDef",
    "GatingRuleUpdateTypeDef",
    "ListAssociatedRoute53HealthChecksRequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListControlPanelsRequestRequestTypeDef",
    "ListRoutingControlsRequestRequestTypeDef",
    "ListSafetyRulesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateControlPanelRequestRequestTypeDef",
    "UpdateRoutingControlRequestRequestTypeDef",
    "AssertionRuleTypeDef",
    "GatingRuleTypeDef",
    "NewAssertionRuleTypeDef",
    "NewGatingRuleTypeDef",
    "ClusterTypeDef",
    "CreateControlPanelResponseTypeDef",
    "DescribeControlPanelResponseTypeDef",
    "ListAssociatedRoute53HealthChecksResponseTypeDef",
    "ListControlPanelsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateControlPanelResponseTypeDef",
    "CreateRoutingControlResponseTypeDef",
    "DescribeRoutingControlResponseTypeDef",
    "ListRoutingControlsResponseTypeDef",
    "UpdateRoutingControlResponseTypeDef",
    "DescribeClusterRequestClusterCreatedWaitTypeDef",
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    "DescribeControlPanelRequestControlPanelCreatedWaitTypeDef",
    "DescribeControlPanelRequestControlPanelDeletedWaitTypeDef",
    "DescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef",
    "DescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef",
    "UpdateSafetyRuleRequestRequestTypeDef",
    "CreateSafetyRuleResponseTypeDef",
    "DescribeSafetyRuleResponseTypeDef",
    "RuleTypeDef",
    "UpdateSafetyRuleResponseTypeDef",
    "CreateSafetyRuleRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "DescribeClusterResponseTypeDef",
    "ListClustersResponseTypeDef",
    "ListSafetyRulesResponseTypeDef",
)

RuleConfigTypeDef = TypedDict(
    "RuleConfigTypeDef",
    {
        "Inverted": bool,
        "Threshold": int,
        "Type": RuleTypeType,
    },
)

AssertionRuleUpdateTypeDef = TypedDict(
    "AssertionRuleUpdateTypeDef",
    {
        "Name": str,
        "SafetyRuleArn": str,
        "WaitPeriodMs": int,
    },
)

ClusterEndpointTypeDef = TypedDict(
    "ClusterEndpointTypeDef",
    {
        "Endpoint": str,
        "Region": str,
    },
    total=False,
)

ControlPanelTypeDef = TypedDict(
    "ControlPanelTypeDef",
    {
        "ClusterArn": str,
        "ControlPanelArn": str,
        "DefaultControlPanel": bool,
        "Name": str,
        "RoutingControlCount": int,
        "Status": StatusType,
    },
    total=False,
)

_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
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

_RequiredCreateControlPanelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateControlPanelRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "ControlPanelName": str,
    },
)
_OptionalCreateControlPanelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateControlPanelRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateControlPanelRequestRequestTypeDef(
    _RequiredCreateControlPanelRequestRequestTypeDef,
    _OptionalCreateControlPanelRequestRequestTypeDef,
):
    pass

_RequiredCreateRoutingControlRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRoutingControlRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "RoutingControlName": str,
    },
)
_OptionalCreateRoutingControlRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRoutingControlRequestRequestTypeDef",
    {
        "ClientToken": str,
        "ControlPanelArn": str,
    },
    total=False,
)

class CreateRoutingControlRequestRequestTypeDef(
    _RequiredCreateRoutingControlRequestRequestTypeDef,
    _OptionalCreateRoutingControlRequestRequestTypeDef,
):
    pass

RoutingControlTypeDef = TypedDict(
    "RoutingControlTypeDef",
    {
        "ControlPanelArn": str,
        "Name": str,
        "RoutingControlArn": str,
        "Status": StatusType,
    },
    total=False,
)

DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

DeleteControlPanelRequestRequestTypeDef = TypedDict(
    "DeleteControlPanelRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
    },
)

DeleteRoutingControlRequestRequestTypeDef = TypedDict(
    "DeleteRoutingControlRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
    },
)

DeleteSafetyRuleRequestRequestTypeDef = TypedDict(
    "DeleteSafetyRuleRequestRequestTypeDef",
    {
        "SafetyRuleArn": str,
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

DescribeClusterRequestRequestTypeDef = TypedDict(
    "DescribeClusterRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

DescribeControlPanelRequestRequestTypeDef = TypedDict(
    "DescribeControlPanelRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
    },
)

DescribeRoutingControlRequestRequestTypeDef = TypedDict(
    "DescribeRoutingControlRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
    },
)

DescribeSafetyRuleRequestRequestTypeDef = TypedDict(
    "DescribeSafetyRuleRequestRequestTypeDef",
    {
        "SafetyRuleArn": str,
    },
)

GatingRuleUpdateTypeDef = TypedDict(
    "GatingRuleUpdateTypeDef",
    {
        "Name": str,
        "SafetyRuleArn": str,
        "WaitPeriodMs": int,
    },
)

_RequiredListAssociatedRoute53HealthChecksRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedRoute53HealthChecksRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
    },
)
_OptionalListAssociatedRoute53HealthChecksRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedRoute53HealthChecksRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListAssociatedRoute53HealthChecksRequestRequestTypeDef(
    _RequiredListAssociatedRoute53HealthChecksRequestRequestTypeDef,
    _OptionalListAssociatedRoute53HealthChecksRequestRequestTypeDef,
):
    pass

ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListControlPanelsRequestRequestTypeDef = TypedDict(
    "ListControlPanelsRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListRoutingControlsRequestRequestTypeDef = TypedDict(
    "_RequiredListRoutingControlsRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
    },
)
_OptionalListRoutingControlsRequestRequestTypeDef = TypedDict(
    "_OptionalListRoutingControlsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListRoutingControlsRequestRequestTypeDef(
    _RequiredListRoutingControlsRequestRequestTypeDef,
    _OptionalListRoutingControlsRequestRequestTypeDef,
):
    pass

_RequiredListSafetyRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListSafetyRulesRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
    },
)
_OptionalListSafetyRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListSafetyRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListSafetyRulesRequestRequestTypeDef(
    _RequiredListSafetyRulesRequestRequestTypeDef, _OptionalListSafetyRulesRequestRequestTypeDef
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

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

UpdateControlPanelRequestRequestTypeDef = TypedDict(
    "UpdateControlPanelRequestRequestTypeDef",
    {
        "ControlPanelArn": str,
        "ControlPanelName": str,
    },
)

UpdateRoutingControlRequestRequestTypeDef = TypedDict(
    "UpdateRoutingControlRequestRequestTypeDef",
    {
        "RoutingControlArn": str,
        "RoutingControlName": str,
    },
)

AssertionRuleTypeDef = TypedDict(
    "AssertionRuleTypeDef",
    {
        "AssertedControls": List[str],
        "ControlPanelArn": str,
        "Name": str,
        "RuleConfig": RuleConfigTypeDef,
        "SafetyRuleArn": str,
        "Status": StatusType,
        "WaitPeriodMs": int,
    },
)

GatingRuleTypeDef = TypedDict(
    "GatingRuleTypeDef",
    {
        "ControlPanelArn": str,
        "GatingControls": List[str],
        "Name": str,
        "RuleConfig": RuleConfigTypeDef,
        "SafetyRuleArn": str,
        "Status": StatusType,
        "TargetControls": List[str],
        "WaitPeriodMs": int,
    },
)

NewAssertionRuleTypeDef = TypedDict(
    "NewAssertionRuleTypeDef",
    {
        "AssertedControls": Sequence[str],
        "ControlPanelArn": str,
        "Name": str,
        "RuleConfig": RuleConfigTypeDef,
        "WaitPeriodMs": int,
    },
)

NewGatingRuleTypeDef = TypedDict(
    "NewGatingRuleTypeDef",
    {
        "ControlPanelArn": str,
        "GatingControls": Sequence[str],
        "Name": str,
        "RuleConfig": RuleConfigTypeDef,
        "TargetControls": Sequence[str],
        "WaitPeriodMs": int,
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "ClusterArn": str,
        "ClusterEndpoints": List[ClusterEndpointTypeDef],
        "Name": str,
        "Status": StatusType,
    },
    total=False,
)

CreateControlPanelResponseTypeDef = TypedDict(
    "CreateControlPanelResponseTypeDef",
    {
        "ControlPanel": ControlPanelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeControlPanelResponseTypeDef = TypedDict(
    "DescribeControlPanelResponseTypeDef",
    {
        "ControlPanel": ControlPanelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedRoute53HealthChecksResponseTypeDef = TypedDict(
    "ListAssociatedRoute53HealthChecksResponseTypeDef",
    {
        "HealthCheckIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListControlPanelsResponseTypeDef = TypedDict(
    "ListControlPanelsResponseTypeDef",
    {
        "ControlPanels": List[ControlPanelTypeDef],
        "NextToken": str,
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

UpdateControlPanelResponseTypeDef = TypedDict(
    "UpdateControlPanelResponseTypeDef",
    {
        "ControlPanel": ControlPanelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRoutingControlResponseTypeDef = TypedDict(
    "CreateRoutingControlResponseTypeDef",
    {
        "RoutingControl": RoutingControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRoutingControlResponseTypeDef = TypedDict(
    "DescribeRoutingControlResponseTypeDef",
    {
        "RoutingControl": RoutingControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutingControlsResponseTypeDef = TypedDict(
    "ListRoutingControlsResponseTypeDef",
    {
        "NextToken": str,
        "RoutingControls": List[RoutingControlTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRoutingControlResponseTypeDef = TypedDict(
    "UpdateRoutingControlResponseTypeDef",
    {
        "RoutingControl": RoutingControlTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeClusterRequestClusterCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterRequestClusterCreatedWaitTypeDef",
    {
        "ClusterArn": str,
    },
)
_OptionalDescribeClusterRequestClusterCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterRequestClusterCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeClusterRequestClusterCreatedWaitTypeDef(
    _RequiredDescribeClusterRequestClusterCreatedWaitTypeDef,
    _OptionalDescribeClusterRequestClusterCreatedWaitTypeDef,
):
    pass

_RequiredDescribeClusterRequestClusterDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeClusterRequestClusterDeletedWaitTypeDef",
    {
        "ClusterArn": str,
    },
)
_OptionalDescribeClusterRequestClusterDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeClusterRequestClusterDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeClusterRequestClusterDeletedWaitTypeDef(
    _RequiredDescribeClusterRequestClusterDeletedWaitTypeDef,
    _OptionalDescribeClusterRequestClusterDeletedWaitTypeDef,
):
    pass

_RequiredDescribeControlPanelRequestControlPanelCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeControlPanelRequestControlPanelCreatedWaitTypeDef",
    {
        "ControlPanelArn": str,
    },
)
_OptionalDescribeControlPanelRequestControlPanelCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeControlPanelRequestControlPanelCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeControlPanelRequestControlPanelCreatedWaitTypeDef(
    _RequiredDescribeControlPanelRequestControlPanelCreatedWaitTypeDef,
    _OptionalDescribeControlPanelRequestControlPanelCreatedWaitTypeDef,
):
    pass

_RequiredDescribeControlPanelRequestControlPanelDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeControlPanelRequestControlPanelDeletedWaitTypeDef",
    {
        "ControlPanelArn": str,
    },
)
_OptionalDescribeControlPanelRequestControlPanelDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeControlPanelRequestControlPanelDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeControlPanelRequestControlPanelDeletedWaitTypeDef(
    _RequiredDescribeControlPanelRequestControlPanelDeletedWaitTypeDef,
    _OptionalDescribeControlPanelRequestControlPanelDeletedWaitTypeDef,
):
    pass

_RequiredDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef",
    {
        "RoutingControlArn": str,
    },
)
_OptionalDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef(
    _RequiredDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef,
    _OptionalDescribeRoutingControlRequestRoutingControlCreatedWaitTypeDef,
):
    pass

_RequiredDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef",
    {
        "RoutingControlArn": str,
    },
)
_OptionalDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef(
    _RequiredDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef,
    _OptionalDescribeRoutingControlRequestRoutingControlDeletedWaitTypeDef,
):
    pass

UpdateSafetyRuleRequestRequestTypeDef = TypedDict(
    "UpdateSafetyRuleRequestRequestTypeDef",
    {
        "AssertionRuleUpdate": AssertionRuleUpdateTypeDef,
        "GatingRuleUpdate": GatingRuleUpdateTypeDef,
    },
    total=False,
)

CreateSafetyRuleResponseTypeDef = TypedDict(
    "CreateSafetyRuleResponseTypeDef",
    {
        "AssertionRule": AssertionRuleTypeDef,
        "GatingRule": GatingRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSafetyRuleResponseTypeDef = TypedDict(
    "DescribeSafetyRuleResponseTypeDef",
    {
        "AssertionRule": AssertionRuleTypeDef,
        "GatingRule": GatingRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "ASSERTION": AssertionRuleTypeDef,
        "GATING": GatingRuleTypeDef,
    },
    total=False,
)

UpdateSafetyRuleResponseTypeDef = TypedDict(
    "UpdateSafetyRuleResponseTypeDef",
    {
        "AssertionRule": AssertionRuleTypeDef,
        "GatingRule": GatingRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSafetyRuleRequestRequestTypeDef = TypedDict(
    "CreateSafetyRuleRequestRequestTypeDef",
    {
        "AssertionRule": NewAssertionRuleTypeDef,
        "ClientToken": str,
        "GatingRule": NewGatingRuleTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterResponseTypeDef = TypedDict(
    "DescribeClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResponseTypeDef = TypedDict(
    "ListClustersResponseTypeDef",
    {
        "Clusters": List[ClusterTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSafetyRulesResponseTypeDef = TypedDict(
    "ListSafetyRulesResponseTypeDef",
    {
        "NextToken": str,
        "SafetyRules": List[RuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
