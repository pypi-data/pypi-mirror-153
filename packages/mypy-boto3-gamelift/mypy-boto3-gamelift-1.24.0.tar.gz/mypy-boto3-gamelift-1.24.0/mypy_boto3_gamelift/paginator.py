"""
Type annotations for gamelift service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_gamelift.client import GameLiftClient
    from mypy_boto3_gamelift.paginator import (
        DescribeFleetAttributesPaginator,
        DescribeFleetCapacityPaginator,
        DescribeFleetEventsPaginator,
        DescribeFleetUtilizationPaginator,
        DescribeGameServerInstancesPaginator,
        DescribeGameSessionDetailsPaginator,
        DescribeGameSessionQueuesPaginator,
        DescribeGameSessionsPaginator,
        DescribeInstancesPaginator,
        DescribeMatchmakingConfigurationsPaginator,
        DescribeMatchmakingRuleSetsPaginator,
        DescribePlayerSessionsPaginator,
        DescribeScalingPoliciesPaginator,
        ListAliasesPaginator,
        ListBuildsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    session = Session()
    client: GameLiftClient = session.client("gamelift")

    describe_fleet_attributes_paginator: DescribeFleetAttributesPaginator = client.get_paginator("describe_fleet_attributes")
    describe_fleet_capacity_paginator: DescribeFleetCapacityPaginator = client.get_paginator("describe_fleet_capacity")
    describe_fleet_events_paginator: DescribeFleetEventsPaginator = client.get_paginator("describe_fleet_events")
    describe_fleet_utilization_paginator: DescribeFleetUtilizationPaginator = client.get_paginator("describe_fleet_utilization")
    describe_game_server_instances_paginator: DescribeGameServerInstancesPaginator = client.get_paginator("describe_game_server_instances")
    describe_game_session_details_paginator: DescribeGameSessionDetailsPaginator = client.get_paginator("describe_game_session_details")
    describe_game_session_queues_paginator: DescribeGameSessionQueuesPaginator = client.get_paginator("describe_game_session_queues")
    describe_game_sessions_paginator: DescribeGameSessionsPaginator = client.get_paginator("describe_game_sessions")
    describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
    describe_matchmaking_configurations_paginator: DescribeMatchmakingConfigurationsPaginator = client.get_paginator("describe_matchmaking_configurations")
    describe_matchmaking_rule_sets_paginator: DescribeMatchmakingRuleSetsPaginator = client.get_paginator("describe_matchmaking_rule_sets")
    describe_player_sessions_paginator: DescribePlayerSessionsPaginator = client.get_paginator("describe_player_sessions")
    describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_game_server_groups_paginator: ListGameServerGroupsPaginator = client.get_paginator("list_game_server_groups")
    list_game_servers_paginator: ListGameServersPaginator = client.get_paginator("list_game_servers")
    list_scripts_paginator: ListScriptsPaginator = client.get_paginator("list_scripts")
    search_game_sessions_paginator: SearchGameSessionsPaginator = client.get_paginator("search_game_sessions")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import BuildStatusType, RoutingStrategyTypeType, ScalingStatusTypeType, SortOrderType
from .type_defs import (
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersOutputTypeDef,
    ListScriptsOutputTypeDef,
    PaginatorConfigTypeDef,
    SearchGameSessionsOutputTypeDef,
)

__all__ = (
    "DescribeFleetAttributesPaginator",
    "DescribeFleetCapacityPaginator",
    "DescribeFleetEventsPaginator",
    "DescribeFleetUtilizationPaginator",
    "DescribeGameServerInstancesPaginator",
    "DescribeGameSessionDetailsPaginator",
    "DescribeGameSessionQueuesPaginator",
    "DescribeGameSessionsPaginator",
    "DescribeInstancesPaginator",
    "DescribeMatchmakingConfigurationsPaginator",
    "DescribeMatchmakingRuleSetsPaginator",
    "DescribePlayerSessionsPaginator",
    "DescribeScalingPoliciesPaginator",
    "ListAliasesPaginator",
    "ListBuildsPaginator",
    "ListFleetsPaginator",
    "ListGameServerGroupsPaginator",
    "ListGameServersPaginator",
    "ListScriptsPaginator",
    "SearchGameSessionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeFleetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
        """


class DescribeFleetCapacityPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
        """


class DescribeFleetEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
        """


class DescribeFleetUtilizationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
        """


class DescribeGameServerInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
    """

    def paginate(
        self,
        *,
        GameServerGroupName: str,
        InstanceIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
        """


class DescribeGameSessionDetailsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
        """


class DescribeGameSessionQueuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
    """

    def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
        """


class DescribeGameSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
        """


class DescribeInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        InstanceId: str = ...,
        Location: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
        """


class DescribeMatchmakingConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        Names: Sequence[str] = ...,
        RuleSetName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """


class DescribeMatchmakingRuleSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
    """

    def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
        """


class DescribePlayerSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
    """

    def paginate(
        self,
        *,
        GameSessionId: str = ...,
        PlayerId: str = ...,
        PlayerSessionId: str = ...,
        PlayerSessionStatusFilter: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
        """


class DescribeScalingPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        StatusFilter: ScalingStatusTypeType = ...,
        Location: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
        """


class ListAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListAliases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
    """

    def paginate(
        self,
        *,
        RoutingStrategyType: RoutingStrategyTypeType = ...,
        Name: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListAliases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
        """


class ListBuildsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListBuilds)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
    """

    def paginate(
        self, *, Status: BuildStatusType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListBuilds.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
        """


class ListFleetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListFleets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
    """

    def paginate(
        self,
        *,
        BuildId: str = ...,
        ScriptId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListFleets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
        """


class ListGameServerGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
        """


class ListGameServersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
    """

    def paginate(
        self,
        *,
        GameServerGroupName: str,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
        """


class ListScriptsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListScripts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListScripts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
        """


class SearchGameSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        FilterExpression: str = ...,
        SortExpression: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
        """
