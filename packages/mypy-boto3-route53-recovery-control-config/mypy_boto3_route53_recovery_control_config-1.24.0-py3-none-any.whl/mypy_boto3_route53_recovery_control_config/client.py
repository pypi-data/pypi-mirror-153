"""
Type annotations for route53-recovery-control-config service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53_recovery_control_config.client import Route53RecoveryControlConfigClient

    session = Session()
    client: Route53RecoveryControlConfigClient = session.client("route53-recovery-control-config")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssertionRuleUpdateTypeDef,
    CreateClusterResponseTypeDef,
    CreateControlPanelResponseTypeDef,
    CreateRoutingControlResponseTypeDef,
    CreateSafetyRuleResponseTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeControlPanelResponseTypeDef,
    DescribeRoutingControlResponseTypeDef,
    DescribeSafetyRuleResponseTypeDef,
    GatingRuleUpdateTypeDef,
    ListAssociatedRoute53HealthChecksResponseTypeDef,
    ListClustersResponseTypeDef,
    ListControlPanelsResponseTypeDef,
    ListRoutingControlsResponseTypeDef,
    ListSafetyRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NewAssertionRuleTypeDef,
    NewGatingRuleTypeDef,
    UpdateControlPanelResponseTypeDef,
    UpdateRoutingControlResponseTypeDef,
    UpdateSafetyRuleResponseTypeDef,
)
from .waiter import (
    ClusterCreatedWaiter,
    ClusterDeletedWaiter,
    ControlPanelCreatedWaiter,
    ControlPanelDeletedWaiter,
    RoutingControlCreatedWaiter,
    RoutingControlDeletedWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Route53RecoveryControlConfigClient",)


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


class Route53RecoveryControlConfigClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryControlConfigClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#can_paginate)
        """

    def create_cluster(
        self, *, ClusterName: str, ClientToken: str = ..., Tags: Mapping[str, str] = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Create a new cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.create_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#create_cluster)
        """

    def create_control_panel(
        self,
        *,
        ClusterArn: str,
        ControlPanelName: str,
        ClientToken: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateControlPanelResponseTypeDef:
        """
        Creates a new control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.create_control_panel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#create_control_panel)
        """

    def create_routing_control(
        self,
        *,
        ClusterArn: str,
        RoutingControlName: str,
        ClientToken: str = ...,
        ControlPanelArn: str = ...
    ) -> CreateRoutingControlResponseTypeDef:
        """
        Creates a new routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.create_routing_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#create_routing_control)
        """

    def create_safety_rule(
        self,
        *,
        AssertionRule: NewAssertionRuleTypeDef = ...,
        ClientToken: str = ...,
        GatingRule: NewGatingRuleTypeDef = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateSafetyRuleResponseTypeDef:
        """
        Creates a safety rule in a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.create_safety_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#create_safety_rule)
        """

    def delete_cluster(self, *, ClusterArn: str) -> Dict[str, Any]:
        """
        Delete a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.delete_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#delete_cluster)
        """

    def delete_control_panel(self, *, ControlPanelArn: str) -> Dict[str, Any]:
        """
        Deletes a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.delete_control_panel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#delete_control_panel)
        """

    def delete_routing_control(self, *, RoutingControlArn: str) -> Dict[str, Any]:
        """
        Deletes a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.delete_routing_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#delete_routing_control)
        """

    def delete_safety_rule(self, *, SafetyRuleArn: str) -> Dict[str, Any]:
        """
        Deletes a safety rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.delete_safety_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#delete_safety_rule)
        """

    def describe_cluster(self, *, ClusterArn: str) -> DescribeClusterResponseTypeDef:
        """
        Display the details about a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.describe_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#describe_cluster)
        """

    def describe_control_panel(
        self, *, ControlPanelArn: str
    ) -> DescribeControlPanelResponseTypeDef:
        """
        Displays details about a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.describe_control_panel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#describe_control_panel)
        """

    def describe_routing_control(
        self, *, RoutingControlArn: str
    ) -> DescribeRoutingControlResponseTypeDef:
        """
        Displays details about a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.describe_routing_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#describe_routing_control)
        """

    def describe_safety_rule(self, *, SafetyRuleArn: str) -> DescribeSafetyRuleResponseTypeDef:
        """
        Returns information about a safety rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.describe_safety_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#describe_safety_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#generate_presigned_url)
        """

    def list_associated_route53_health_checks(
        self, *, RoutingControlArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAssociatedRoute53HealthChecksResponseTypeDef:
        """
        Returns an array of all Amazon Route 53 health checks associated with a specific
        routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_associated_route53_health_checks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_associated_route53_health_checks)
        """

    def list_clusters(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListClustersResponseTypeDef:
        """
        Returns an array of all the clusters in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_clusters)
        """

    def list_control_panels(
        self, *, ClusterArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListControlPanelsResponseTypeDef:
        """
        Returns an array of control panels in an account or in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_control_panels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_control_panels)
        """

    def list_routing_controls(
        self, *, ControlPanelArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRoutingControlsResponseTypeDef:
        """
        Returns an array of routing controls for a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_routing_controls)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_routing_controls)
        """

    def list_safety_rules(
        self, *, ControlPanelArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSafetyRulesResponseTypeDef:
        """
        List the safety rules (the assertion rules and gating rules) that you've defined
        for the routing controls in a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_safety_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_safety_rules)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#untag_resource)
        """

    def update_control_panel(
        self, *, ControlPanelArn: str, ControlPanelName: str
    ) -> UpdateControlPanelResponseTypeDef:
        """
        Updates a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.update_control_panel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#update_control_panel)
        """

    def update_routing_control(
        self, *, RoutingControlArn: str, RoutingControlName: str
    ) -> UpdateRoutingControlResponseTypeDef:
        """
        Updates a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.update_routing_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#update_routing_control)
        """

    def update_safety_rule(
        self,
        *,
        AssertionRuleUpdate: AssertionRuleUpdateTypeDef = ...,
        GatingRuleUpdate: GatingRuleUpdateTypeDef = ...
    ) -> UpdateSafetyRuleResponseTypeDef:
        """
        Update a safety rule (an assertion rule or gating rule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.update_safety_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#update_safety_rule)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_created"]) -> ClusterCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_deleted"]) -> ClusterDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["control_panel_created"]
    ) -> ControlPanelCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["control_panel_deleted"]
    ) -> ControlPanelDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["routing_control_created"]
    ) -> RoutingControlCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["routing_control_deleted"]
    ) -> RoutingControlDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/client/#get_waiter)
        """
