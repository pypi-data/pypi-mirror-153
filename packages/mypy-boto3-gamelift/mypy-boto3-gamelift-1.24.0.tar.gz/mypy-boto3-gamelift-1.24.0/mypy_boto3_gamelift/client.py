"""
Type annotations for gamelift service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_gamelift.client import GameLiftClient

    session = Session()
    client: GameLiftClient = session.client("gamelift")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import (
    AcceptanceTypeType,
    BackfillModeType,
    BalancingStrategyType,
    BuildStatusType,
    ComparisonOperatorTypeType,
    EC2InstanceTypeType,
    FleetTypeType,
    FlexMatchModeType,
    GameServerGroupDeleteOptionType,
    GameServerProtectionPolicyType,
    GameServerUtilizationStatusType,
    MetricNameType,
    OperatingSystemType,
    PlayerSessionCreationPolicyType,
    PolicyTypeType,
    ProtectionPolicyType,
    RoutingStrategyTypeType,
    ScalingAdjustmentTypeType,
    ScalingStatusTypeType,
    SortOrderType,
)
from .paginator import (
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
from .type_defs import (
    CertificateConfigurationTypeDef,
    ClaimGameServerOutputTypeDef,
    CreateAliasOutputTypeDef,
    CreateBuildOutputTypeDef,
    CreateFleetLocationsOutputTypeDef,
    CreateFleetOutputTypeDef,
    CreateGameServerGroupOutputTypeDef,
    CreateGameSessionOutputTypeDef,
    CreateGameSessionQueueOutputTypeDef,
    CreateMatchmakingConfigurationOutputTypeDef,
    CreateMatchmakingRuleSetOutputTypeDef,
    CreatePlayerSessionOutputTypeDef,
    CreatePlayerSessionsOutputTypeDef,
    CreateScriptOutputTypeDef,
    CreateVpcPeeringAuthorizationOutputTypeDef,
    DeleteFleetLocationsOutputTypeDef,
    DeleteGameServerGroupOutputTypeDef,
    DescribeAliasOutputTypeDef,
    DescribeBuildOutputTypeDef,
    DescribeEC2InstanceLimitsOutputTypeDef,
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetLocationAttributesOutputTypeDef,
    DescribeFleetLocationCapacityOutputTypeDef,
    DescribeFleetLocationUtilizationOutputTypeDef,
    DescribeFleetPortSettingsOutputTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerGroupOutputTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameServerOutputTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionPlacementOutputTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingOutputTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeRuntimeConfigurationOutputTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    DescribeScriptOutputTypeDef,
    DescribeVpcPeeringAuthorizationsOutputTypeDef,
    DescribeVpcPeeringConnectionsOutputTypeDef,
    DesiredPlayerSessionTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterConfigurationTypeDef,
    GamePropertyTypeDef,
    GameServerGroupAutoScalingPolicyTypeDef,
    GameSessionQueueDestinationTypeDef,
    GetGameSessionLogUrlOutputTypeDef,
    GetInstanceAccessOutputTypeDef,
    InstanceDefinitionTypeDef,
    IpPermissionTypeDef,
    LaunchTemplateSpecificationTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersOutputTypeDef,
    ListScriptsOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    LocationConfigurationTypeDef,
    PlayerLatencyPolicyTypeDef,
    PlayerLatencyTypeDef,
    PlayerTypeDef,
    PriorityConfigurationTypeDef,
    PutScalingPolicyOutputTypeDef,
    RegisterGameServerOutputTypeDef,
    RequestUploadCredentialsOutputTypeDef,
    ResolveAliasOutputTypeDef,
    ResourceCreationLimitPolicyTypeDef,
    ResumeGameServerGroupOutputTypeDef,
    RoutingStrategyTypeDef,
    RuntimeConfigurationTypeDef,
    S3LocationTypeDef,
    SearchGameSessionsOutputTypeDef,
    StartFleetActionsOutputTypeDef,
    StartGameSessionPlacementOutputTypeDef,
    StartMatchBackfillOutputTypeDef,
    StartMatchmakingOutputTypeDef,
    StopFleetActionsOutputTypeDef,
    StopGameSessionPlacementOutputTypeDef,
    SuspendGameServerGroupOutputTypeDef,
    TagTypeDef,
    TargetConfigurationTypeDef,
    UpdateAliasOutputTypeDef,
    UpdateBuildOutputTypeDef,
    UpdateFleetAttributesOutputTypeDef,
    UpdateFleetCapacityOutputTypeDef,
    UpdateFleetPortSettingsOutputTypeDef,
    UpdateGameServerGroupOutputTypeDef,
    UpdateGameServerOutputTypeDef,
    UpdateGameSessionOutputTypeDef,
    UpdateGameSessionQueueOutputTypeDef,
    UpdateMatchmakingConfigurationOutputTypeDef,
    UpdateRuntimeConfigurationOutputTypeDef,
    UpdateScriptOutputTypeDef,
    ValidateMatchmakingRuleSetOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GameLiftClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FleetCapacityExceededException: Type[BotocoreClientError]
    GameSessionFullException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidFleetStatusException: Type[BotocoreClientError]
    InvalidGameSessionStatusException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    OutOfCapacityException: Type[BotocoreClientError]
    TaggingFailedException: Type[BotocoreClientError]
    TerminalRoutingStrategyException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnsupportedRegionException: Type[BotocoreClientError]


class GameLiftClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GameLiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#exceptions)
        """

    def accept_match(
        self, *, TicketId: str, PlayerIds: Sequence[str], AcceptanceType: AcceptanceTypeType
    ) -> Dict[str, Any]:
        """
        Registers a player's acceptance or rejection of a proposed FlexMatch match.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.accept_match)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#accept_match)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#can_paginate)
        """

    def claim_game_server(
        self, *, GameServerGroupName: str, GameServerId: str = ..., GameServerData: str = ...
    ) -> ClaimGameServerOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Locates an available game server and temporarily reserves it to host
        gameplay and players.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.claim_game_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#claim_game_server)
        """

    def create_alias(
        self,
        *,
        Name: str,
        RoutingStrategy: RoutingStrategyTypeDef,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateAliasOutputTypeDef:
        """
        Creates an alias for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_alias)
        """

    def create_build(
        self,
        *,
        Name: str = ...,
        Version: str = ...,
        StorageLocation: S3LocationTypeDef = ...,
        OperatingSystem: OperatingSystemType = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateBuildOutputTypeDef:
        """
        Creates a new Amazon GameLift build resource for your game server binary files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_build)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_build)
        """

    def create_fleet(
        self,
        *,
        Name: str,
        EC2InstanceType: EC2InstanceTypeType,
        Description: str = ...,
        BuildId: str = ...,
        ScriptId: str = ...,
        ServerLaunchPath: str = ...,
        ServerLaunchParameters: str = ...,
        LogPaths: Sequence[str] = ...,
        EC2InboundPermissions: Sequence[IpPermissionTypeDef] = ...,
        NewGameSessionProtectionPolicy: ProtectionPolicyType = ...,
        RuntimeConfiguration: RuntimeConfigurationTypeDef = ...,
        ResourceCreationLimitPolicy: ResourceCreationLimitPolicyTypeDef = ...,
        MetricGroups: Sequence[str] = ...,
        PeerVpcAwsAccountId: str = ...,
        PeerVpcId: str = ...,
        FleetType: FleetTypeType = ...,
        InstanceRoleArn: str = ...,
        CertificateConfiguration: CertificateConfigurationTypeDef = ...,
        Locations: Sequence[LocationConfigurationTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateFleetOutputTypeDef:
        """
        Creates a fleet of Amazon Elastic Compute Cloud (Amazon Elastic Compute Cloud)
        instances to host your custom game server or Realtime Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_fleet)
        """

    def create_fleet_locations(
        self, *, FleetId: str, Locations: Sequence[LocationConfigurationTypeDef]
    ) -> CreateFleetLocationsOutputTypeDef:
        """
        Adds remote locations to a fleet and begins populating the new locations with
        EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_fleet_locations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_fleet_locations)
        """

    def create_game_server_group(
        self,
        *,
        GameServerGroupName: str,
        RoleArn: str,
        MinSize: int,
        MaxSize: int,
        LaunchTemplate: LaunchTemplateSpecificationTypeDef,
        InstanceDefinitions: Sequence[InstanceDefinitionTypeDef],
        AutoScalingPolicy: GameServerGroupAutoScalingPolicyTypeDef = ...,
        BalancingStrategy: BalancingStrategyType = ...,
        GameServerProtectionPolicy: GameServerProtectionPolicyType = ...,
        VpcSubnets: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Creates a GameLift FleetIQ game server group for managing game hosting
        on a collection of Amazon Elastic Compute Cloud instances for game hosting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_server_group)
        """

    def create_game_session(
        self,
        *,
        MaximumPlayerSessionCount: int,
        FleetId: str = ...,
        AliasId: str = ...,
        Name: str = ...,
        GameProperties: Sequence[GamePropertyTypeDef] = ...,
        CreatorId: str = ...,
        GameSessionId: str = ...,
        IdempotencyToken: str = ...,
        GameSessionData: str = ...,
        Location: str = ...
    ) -> CreateGameSessionOutputTypeDef:
        """
        Creates a multiplayer game session for players in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_game_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_session)
        """

    def create_game_session_queue(
        self,
        *,
        Name: str,
        TimeoutInSeconds: int = ...,
        PlayerLatencyPolicies: Sequence[PlayerLatencyPolicyTypeDef] = ...,
        Destinations: Sequence[GameSessionQueueDestinationTypeDef] = ...,
        FilterConfiguration: FilterConfigurationTypeDef = ...,
        PriorityConfiguration: PriorityConfigurationTypeDef = ...,
        CustomEventData: str = ...,
        NotificationTarget: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateGameSessionQueueOutputTypeDef:
        """
        Creates a placement queue that processes requests for new game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_game_session_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_session_queue)
        """

    def create_matchmaking_configuration(
        self,
        *,
        Name: str,
        RequestTimeoutSeconds: int,
        AcceptanceRequired: bool,
        RuleSetName: str,
        Description: str = ...,
        GameSessionQueueArns: Sequence[str] = ...,
        AcceptanceTimeoutSeconds: int = ...,
        NotificationTarget: str = ...,
        AdditionalPlayerCount: int = ...,
        CustomEventData: str = ...,
        GameProperties: Sequence[GamePropertyTypeDef] = ...,
        GameSessionData: str = ...,
        BackfillMode: BackfillModeType = ...,
        FlexMatchMode: FlexMatchModeType = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMatchmakingConfigurationOutputTypeDef:
        """
        Defines a new matchmaking configuration for use with FlexMatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_matchmaking_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_matchmaking_configuration)
        """

    def create_matchmaking_rule_set(
        self, *, Name: str, RuleSetBody: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMatchmakingRuleSetOutputTypeDef:
        """
        Creates a new rule set for FlexMatch matchmaking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_matchmaking_rule_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_matchmaking_rule_set)
        """

    def create_player_session(
        self, *, GameSessionId: str, PlayerId: str, PlayerData: str = ...
    ) -> CreatePlayerSessionOutputTypeDef:
        """
        Reserves an open player slot in a game session for a player.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_player_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_player_session)
        """

    def create_player_sessions(
        self,
        *,
        GameSessionId: str,
        PlayerIds: Sequence[str],
        PlayerDataMap: Mapping[str, str] = ...
    ) -> CreatePlayerSessionsOutputTypeDef:
        """
        Reserves open slots in a game session for a group of players.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_player_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_player_sessions)
        """

    def create_script(
        self,
        *,
        Name: str = ...,
        Version: str = ...,
        StorageLocation: S3LocationTypeDef = ...,
        ZipFile: Union[str, bytes, IO[Any], StreamingBody] = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateScriptOutputTypeDef:
        """
        Creates a new script record for your Realtime Servers script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_script)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_script)
        """

    def create_vpc_peering_authorization(
        self, *, GameLiftAwsAccountId: str, PeerVpcId: str
    ) -> CreateVpcPeeringAuthorizationOutputTypeDef:
        """
        Requests authorization to create or delete a peer connection between the VPC for
        your Amazon GameLift fleet and a virtual private cloud (VPC) in your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_vpc_peering_authorization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_vpc_peering_authorization)
        """

    def create_vpc_peering_connection(
        self, *, FleetId: str, PeerVpcAwsAccountId: str, PeerVpcId: str
    ) -> Dict[str, Any]:
        """
        Establishes a VPC peering connection between a virtual private cloud (VPC) in an
        Amazon Web Services account with the VPC for your Amazon GameLift fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.create_vpc_peering_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_vpc_peering_connection)
        """

    def delete_alias(self, *, AliasId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_alias)
        """

    def delete_build(self, *, BuildId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_build)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_build)
        """

    def delete_fleet(self, *, FleetId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes all resources and information related a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_fleet)
        """

    def delete_fleet_locations(
        self, *, FleetId: str, Locations: Sequence[str]
    ) -> DeleteFleetLocationsOutputTypeDef:
        """
        Removes locations from a multi-location fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_fleet_locations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_fleet_locations)
        """

    def delete_game_server_group(
        self, *, GameServerGroupName: str, DeleteOption: GameServerGroupDeleteOptionType = ...
    ) -> DeleteGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Terminates a game server group and permanently deletes the game server
        group record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_game_server_group)
        """

    def delete_game_session_queue(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a game session queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_game_session_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_game_session_queue)
        """

    def delete_matchmaking_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Permanently removes a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_matchmaking_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_matchmaking_configuration)
        """

    def delete_matchmaking_rule_set(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an existing matchmaking rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_matchmaking_rule_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_matchmaking_rule_set)
        """

    def delete_scaling_policy(self, *, Name: str, FleetId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a fleet scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_scaling_policy)
        """

    def delete_script(self, *, ScriptId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_script)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_script)
        """

    def delete_vpc_peering_authorization(
        self, *, GameLiftAwsAccountId: str, PeerVpcId: str
    ) -> Dict[str, Any]:
        """
        Cancels a pending VPC peering authorization for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_vpc_peering_authorization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_vpc_peering_authorization)
        """

    def delete_vpc_peering_connection(
        self, *, FleetId: str, VpcPeeringConnectionId: str
    ) -> Dict[str, Any]:
        """
        Removes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.delete_vpc_peering_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_vpc_peering_connection)
        """

    def deregister_game_server(
        self, *, GameServerGroupName: str, GameServerId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Removes the game server from a game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.deregister_game_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#deregister_game_server)
        """

    def describe_alias(self, *, AliasId: str) -> DescribeAliasOutputTypeDef:
        """
        Retrieves properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_alias)
        """

    def describe_build(self, *, BuildId: str) -> DescribeBuildOutputTypeDef:
        """
        Retrieves properties for a custom game build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_build)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_build)
        """

    def describe_ec2_instance_limits(
        self, *, EC2InstanceType: EC2InstanceTypeType = ..., Location: str = ...
    ) -> DescribeEC2InstanceLimitsOutputTypeDef:
        """
        Retrieves the instance limits and current utilization for an Amazon Web Services
        Region or location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_ec2_instance_limits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_ec2_instance_limits)
        """

    def describe_fleet_attributes(
        self, *, FleetIds: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeFleetAttributesOutputTypeDef:
        """
        Retrieves core fleet-wide properties, including the computing hardware and
        deployment configuration for all instances in the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_attributes)
        """

    def describe_fleet_capacity(
        self, *, FleetIds: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeFleetCapacityOutputTypeDef:
        """
        Retrieves the resource capacity settings for one or more fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_capacity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_capacity)
        """

    def describe_fleet_events(
        self,
        *,
        FleetId: str,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeFleetEventsOutputTypeDef:
        """
        Retrieves entries from a fleet's event log.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_events)
        """

    def describe_fleet_location_attributes(
        self,
        *,
        FleetId: str,
        Locations: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeFleetLocationAttributesOutputTypeDef:
        """
        Retrieves information on a fleet's remote locations, including life-cycle status
        and any suspended fleet activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_location_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_attributes)
        """

    def describe_fleet_location_capacity(
        self, *, FleetId: str, Location: str
    ) -> DescribeFleetLocationCapacityOutputTypeDef:
        """
        Retrieves the resource capacity settings for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_location_capacity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_capacity)
        """

    def describe_fleet_location_utilization(
        self, *, FleetId: str, Location: str
    ) -> DescribeFleetLocationUtilizationOutputTypeDef:
        """
        Retrieves current usage data for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_location_utilization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_utilization)
        """

    def describe_fleet_port_settings(
        self, *, FleetId: str, Location: str = ...
    ) -> DescribeFleetPortSettingsOutputTypeDef:
        """
        Retrieves a fleet's inbound connection permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_port_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_port_settings)
        """

    def describe_fleet_utilization(
        self, *, FleetIds: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeFleetUtilizationOutputTypeDef:
        """
        Retrieves utilization statistics for one or more fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_fleet_utilization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_utilization)
        """

    def describe_game_server(
        self, *, GameServerGroupName: str, GameServerId: str
    ) -> DescribeGameServerOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Retrieves information for a registered game server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server)
        """

    def describe_game_server_group(
        self, *, GameServerGroupName: str
    ) -> DescribeGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Retrieves information on a game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server_group)
        """

    def describe_game_server_instances(
        self,
        *,
        GameServerGroupName: str,
        InstanceIds: Sequence[str] = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeGameServerInstancesOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Retrieves status information about the Amazon EC2 instances associated
        with a GameLift FleetIQ game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_server_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server_instances)
        """

    def describe_game_session_details(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeGameSessionDetailsOutputTypeDef:
        """
        Retrieves additional game session properties, including the game session
        protection policy in force, a set of one or more game sessions in a specific
        fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_session_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_details)
        """

    def describe_game_session_placement(
        self, *, PlacementId: str
    ) -> DescribeGameSessionPlacementOutputTypeDef:
        """
        Retrieves information, including current status, about a game session placement
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_session_placement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_placement)
        """

    def describe_game_session_queues(
        self, *, Names: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeGameSessionQueuesOutputTypeDef:
        """
        Retrieves the properties for one or more game session queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_session_queues)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_queues)
        """

    def describe_game_sessions(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeGameSessionsOutputTypeDef:
        """
        Retrieves a set of one or more game sessions in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_game_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_sessions)
        """

    def describe_instances(
        self,
        *,
        FleetId: str,
        InstanceId: str = ...,
        Limit: int = ...,
        NextToken: str = ...,
        Location: str = ...
    ) -> DescribeInstancesOutputTypeDef:
        """
        Retrieves information about a fleet's instances, including instance IDs,
        connection data, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_instances)
        """

    def describe_matchmaking(self, *, TicketIds: Sequence[str]) -> DescribeMatchmakingOutputTypeDef:
        """
        Retrieves one or more matchmaking tickets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_matchmaking)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking)
        """

    def describe_matchmaking_configurations(
        self,
        *,
        Names: Sequence[str] = ...,
        RuleSetName: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeMatchmakingConfigurationsOutputTypeDef:
        """
        Retrieves the details of FlexMatch matchmaking configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_matchmaking_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking_configurations)
        """

    def describe_matchmaking_rule_sets(
        self, *, Names: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeMatchmakingRuleSetsOutputTypeDef:
        """
        Retrieves the details for FlexMatch matchmaking rule sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_matchmaking_rule_sets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking_rule_sets)
        """

    def describe_player_sessions(
        self,
        *,
        GameSessionId: str = ...,
        PlayerId: str = ...,
        PlayerSessionId: str = ...,
        PlayerSessionStatusFilter: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribePlayerSessionsOutputTypeDef:
        """
        Retrieves properties for one or more player sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_player_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_player_sessions)
        """

    def describe_runtime_configuration(
        self, *, FleetId: str
    ) -> DescribeRuntimeConfigurationOutputTypeDef:
        """
        Retrieves a fleet's runtime configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_runtime_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_runtime_configuration)
        """

    def describe_scaling_policies(
        self,
        *,
        FleetId: str,
        StatusFilter: ScalingStatusTypeType = ...,
        Limit: int = ...,
        NextToken: str = ...,
        Location: str = ...
    ) -> DescribeScalingPoliciesOutputTypeDef:
        """
        Retrieves all scaling policies applied to a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_scaling_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_scaling_policies)
        """

    def describe_script(self, *, ScriptId: str) -> DescribeScriptOutputTypeDef:
        """
        Retrieves properties for a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_script)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_script)
        """

    def describe_vpc_peering_authorizations(self) -> DescribeVpcPeeringAuthorizationsOutputTypeDef:
        """
        Retrieves valid VPC peering authorizations that are pending for the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_vpc_peering_authorizations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_vpc_peering_authorizations)
        """

    def describe_vpc_peering_connections(
        self, *, FleetId: str = ...
    ) -> DescribeVpcPeeringConnectionsOutputTypeDef:
        """
        Retrieves information on VPC peering connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.describe_vpc_peering_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_vpc_peering_connections)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#generate_presigned_url)
        """

    def get_game_session_log_url(self, *, GameSessionId: str) -> GetGameSessionLogUrlOutputTypeDef:
        """
        Retrieves the location of stored game session logs for a specified game session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_game_session_log_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_game_session_log_url)
        """

    def get_instance_access(
        self, *, FleetId: str, InstanceId: str
    ) -> GetInstanceAccessOutputTypeDef:
        """
        Requests remote access to a fleet instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_instance_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_instance_access)
        """

    def list_aliases(
        self,
        *,
        RoutingStrategyType: RoutingStrategyTypeType = ...,
        Name: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> ListAliasesOutputTypeDef:
        """
        Retrieves all aliases for this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_aliases)
        """

    def list_builds(
        self, *, Status: BuildStatusType = ..., Limit: int = ..., NextToken: str = ...
    ) -> ListBuildsOutputTypeDef:
        """
        Retrieves build resources for all builds associated with the Amazon Web Services
        account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_builds)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_builds)
        """

    def list_fleets(
        self, *, BuildId: str = ..., ScriptId: str = ..., Limit: int = ..., NextToken: str = ...
    ) -> ListFleetsOutputTypeDef:
        """
        Retrieves a collection of fleet resources in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_fleets)
        """

    def list_game_server_groups(
        self, *, Limit: int = ..., NextToken: str = ...
    ) -> ListGameServerGroupsOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Retrieves information on all game servers groups that exist in the
        current Amazon Web Services account for the selected Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_game_server_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_game_server_groups)
        """

    def list_game_servers(
        self,
        *,
        GameServerGroupName: str,
        SortOrder: SortOrderType = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> ListGameServersOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Retrieves information on all game servers that are currently active in
        a specified game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_game_servers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_game_servers)
        """

    def list_scripts(self, *, Limit: int = ..., NextToken: str = ...) -> ListScriptsOutputTypeDef:
        """
        Retrieves script records for all Realtime scripts that are associated with the
        Amazon Web Services account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_scripts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_scripts)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all tags that are assigned to a GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_tags_for_resource)
        """

    def put_scaling_policy(
        self,
        *,
        Name: str,
        FleetId: str,
        MetricName: MetricNameType,
        ScalingAdjustment: int = ...,
        ScalingAdjustmentType: ScalingAdjustmentTypeType = ...,
        Threshold: float = ...,
        ComparisonOperator: ComparisonOperatorTypeType = ...,
        EvaluationPeriods: int = ...,
        PolicyType: PolicyTypeType = ...,
        TargetConfiguration: TargetConfigurationTypeDef = ...
    ) -> PutScalingPolicyOutputTypeDef:
        """
        Creates or updates a scaling policy for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.put_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#put_scaling_policy)
        """

    def register_game_server(
        self,
        *,
        GameServerGroupName: str,
        GameServerId: str,
        InstanceId: str,
        ConnectionInfo: str = ...,
        GameServerData: str = ...
    ) -> RegisterGameServerOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Creates a new game server resource and notifies GameLift FleetIQ that
        the game server is ready to host gameplay and players.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.register_game_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#register_game_server)
        """

    def request_upload_credentials(self, *, BuildId: str) -> RequestUploadCredentialsOutputTypeDef:
        """
        Retrieves a fresh set of credentials for use when uploading a new set of game
        build files to Amazon GameLift's Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.request_upload_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#request_upload_credentials)
        """

    def resolve_alias(self, *, AliasId: str) -> ResolveAliasOutputTypeDef:
        """
        Retrieves the fleet ID that an alias is currently pointing to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.resolve_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#resolve_alias)
        """

    def resume_game_server_group(
        self,
        *,
        GameServerGroupName: str,
        ResumeActions: Sequence[Literal["REPLACE_INSTANCE_TYPES"]]
    ) -> ResumeGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Reinstates activity on a game server group after it has been
        suspended.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.resume_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#resume_game_server_group)
        """

    def search_game_sessions(
        self,
        *,
        FleetId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        FilterExpression: str = ...,
        SortExpression: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> SearchGameSessionsOutputTypeDef:
        """
        Retrieves all active game sessions that match a set of search criteria and sorts
        them into a specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.search_game_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#search_game_sessions)
        """

    def start_fleet_actions(
        self, *, FleetId: str, Actions: Sequence[Literal["AUTO_SCALING"]], Location: str = ...
    ) -> StartFleetActionsOutputTypeDef:
        """
        Resumes certain types of activity on fleet instances that were suspended with
        StopFleetActions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.start_fleet_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_fleet_actions)
        """

    def start_game_session_placement(
        self,
        *,
        PlacementId: str,
        GameSessionQueueName: str,
        MaximumPlayerSessionCount: int,
        GameProperties: Sequence[GamePropertyTypeDef] = ...,
        GameSessionName: str = ...,
        PlayerLatencies: Sequence[PlayerLatencyTypeDef] = ...,
        DesiredPlayerSessions: Sequence[DesiredPlayerSessionTypeDef] = ...,
        GameSessionData: str = ...
    ) -> StartGameSessionPlacementOutputTypeDef:
        """
        Places a request for a new game session in a queue (see  CreateGameSessionQueue
        ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.start_game_session_placement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_game_session_placement)
        """

    def start_match_backfill(
        self,
        *,
        ConfigurationName: str,
        Players: Sequence[PlayerTypeDef],
        TicketId: str = ...,
        GameSessionArn: str = ...
    ) -> StartMatchBackfillOutputTypeDef:
        """
        Finds new players to fill open slots in currently running game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.start_match_backfill)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_match_backfill)
        """

    def start_matchmaking(
        self, *, ConfigurationName: str, Players: Sequence[PlayerTypeDef], TicketId: str = ...
    ) -> StartMatchmakingOutputTypeDef:
        """
        Uses FlexMatch to create a game match for a group of players based on custom
        matchmaking rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.start_matchmaking)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_matchmaking)
        """

    def stop_fleet_actions(
        self, *, FleetId: str, Actions: Sequence[Literal["AUTO_SCALING"]], Location: str = ...
    ) -> StopFleetActionsOutputTypeDef:
        """
        Suspends certain types of activity in a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.stop_fleet_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_fleet_actions)
        """

    def stop_game_session_placement(
        self, *, PlacementId: str
    ) -> StopGameSessionPlacementOutputTypeDef:
        """
        Cancels a game session placement that is in `PENDING` status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.stop_game_session_placement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_game_session_placement)
        """

    def stop_matchmaking(self, *, TicketId: str) -> Dict[str, Any]:
        """
        Cancels a matchmaking ticket or match backfill ticket that is currently being
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.stop_matchmaking)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_matchmaking)
        """

    def suspend_game_server_group(
        self,
        *,
        GameServerGroupName: str,
        SuspendActions: Sequence[Literal["REPLACE_INSTANCE_TYPES"]]
    ) -> SuspendGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Temporarily stops activity on a game server group without terminating
        instances or the game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.suspend_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#suspend_game_server_group)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Assigns a tag to a GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag that is assigned to a GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#untag_resource)
        """

    def update_alias(
        self,
        *,
        AliasId: str,
        Name: str = ...,
        Description: str = ...,
        RoutingStrategy: RoutingStrategyTypeDef = ...
    ) -> UpdateAliasOutputTypeDef:
        """
        Updates properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_alias)
        """

    def update_build(
        self, *, BuildId: str, Name: str = ..., Version: str = ...
    ) -> UpdateBuildOutputTypeDef:
        """
        Updates metadata in a build resource, including the build name and version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_build)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_build)
        """

    def update_fleet_attributes(
        self,
        *,
        FleetId: str,
        Name: str = ...,
        Description: str = ...,
        NewGameSessionProtectionPolicy: ProtectionPolicyType = ...,
        ResourceCreationLimitPolicy: ResourceCreationLimitPolicyTypeDef = ...,
        MetricGroups: Sequence[str] = ...
    ) -> UpdateFleetAttributesOutputTypeDef:
        """
        Updates a fleet's mutable attributes, including game session protection and
        resource creation limits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_fleet_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_attributes)
        """

    def update_fleet_capacity(
        self,
        *,
        FleetId: str,
        DesiredInstances: int = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        Location: str = ...
    ) -> UpdateFleetCapacityOutputTypeDef:
        """
        Updates capacity settings for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_fleet_capacity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_capacity)
        """

    def update_fleet_port_settings(
        self,
        *,
        FleetId: str,
        InboundPermissionAuthorizations: Sequence[IpPermissionTypeDef] = ...,
        InboundPermissionRevocations: Sequence[IpPermissionTypeDef] = ...
    ) -> UpdateFleetPortSettingsOutputTypeDef:
        """
        Updates permissions that allow inbound traffic to connect to game sessions that
        are being hosted on instances in the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_fleet_port_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_port_settings)
        """

    def update_game_server(
        self,
        *,
        GameServerGroupName: str,
        GameServerId: str,
        GameServerData: str = ...,
        UtilizationStatus: GameServerUtilizationStatusType = ...,
        HealthCheck: Literal["HEALTHY"] = ...
    ) -> UpdateGameServerOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Updates information about a registered game server to help GameLift
        FleetIQ to track game server availability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_game_server)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_server)
        """

    def update_game_server_group(
        self,
        *,
        GameServerGroupName: str,
        RoleArn: str = ...,
        InstanceDefinitions: Sequence[InstanceDefinitionTypeDef] = ...,
        GameServerProtectionPolicy: GameServerProtectionPolicyType = ...,
        BalancingStrategy: BalancingStrategyType = ...
    ) -> UpdateGameServerGroupOutputTypeDef:
        """
        **This operation is used with the GameLift FleetIQ solution and game server
        groups.** Updates GameLift FleetIQ-specific properties for a game server group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_game_server_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_server_group)
        """

    def update_game_session(
        self,
        *,
        GameSessionId: str,
        MaximumPlayerSessionCount: int = ...,
        Name: str = ...,
        PlayerSessionCreationPolicy: PlayerSessionCreationPolicyType = ...,
        ProtectionPolicy: ProtectionPolicyType = ...
    ) -> UpdateGameSessionOutputTypeDef:
        """
        Updates the mutable properties of a game session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_game_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_session)
        """

    def update_game_session_queue(
        self,
        *,
        Name: str,
        TimeoutInSeconds: int = ...,
        PlayerLatencyPolicies: Sequence[PlayerLatencyPolicyTypeDef] = ...,
        Destinations: Sequence[GameSessionQueueDestinationTypeDef] = ...,
        FilterConfiguration: FilterConfigurationTypeDef = ...,
        PriorityConfiguration: PriorityConfigurationTypeDef = ...,
        CustomEventData: str = ...,
        NotificationTarget: str = ...
    ) -> UpdateGameSessionQueueOutputTypeDef:
        """
        Updates the configuration of a game session queue, which determines how the
        queue processes new game session requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_game_session_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_session_queue)
        """

    def update_matchmaking_configuration(
        self,
        *,
        Name: str,
        Description: str = ...,
        GameSessionQueueArns: Sequence[str] = ...,
        RequestTimeoutSeconds: int = ...,
        AcceptanceTimeoutSeconds: int = ...,
        AcceptanceRequired: bool = ...,
        RuleSetName: str = ...,
        NotificationTarget: str = ...,
        AdditionalPlayerCount: int = ...,
        CustomEventData: str = ...,
        GameProperties: Sequence[GamePropertyTypeDef] = ...,
        GameSessionData: str = ...,
        BackfillMode: BackfillModeType = ...,
        FlexMatchMode: FlexMatchModeType = ...
    ) -> UpdateMatchmakingConfigurationOutputTypeDef:
        """
        Updates settings for a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_matchmaking_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_matchmaking_configuration)
        """

    def update_runtime_configuration(
        self, *, FleetId: str, RuntimeConfiguration: RuntimeConfigurationTypeDef
    ) -> UpdateRuntimeConfigurationOutputTypeDef:
        """
        Updates the current runtime configuration for the specified fleet, which tells
        GameLift how to launch server processes on all instances in the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_runtime_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_runtime_configuration)
        """

    def update_script(
        self,
        *,
        ScriptId: str,
        Name: str = ...,
        Version: str = ...,
        StorageLocation: S3LocationTypeDef = ...,
        ZipFile: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> UpdateScriptOutputTypeDef:
        """
        Updates Realtime script metadata and content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.update_script)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_script)
        """

    def validate_matchmaking_rule_set(
        self, *, RuleSetBody: str
    ) -> ValidateMatchmakingRuleSetOutputTypeDef:
        """
        Validates the syntax of a matchmaking rule or rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.validate_matchmaking_rule_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#validate_matchmaking_rule_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_attributes"]
    ) -> DescribeFleetAttributesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_capacity"]
    ) -> DescribeFleetCapacityPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_events"]
    ) -> DescribeFleetEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fleet_utilization"]
    ) -> DescribeFleetUtilizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_server_instances"]
    ) -> DescribeGameServerInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_session_details"]
    ) -> DescribeGameSessionDetailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_session_queues"]
    ) -> DescribeGameSessionQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_game_sessions"]
    ) -> DescribeGameSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instances"]
    ) -> DescribeInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_matchmaking_configurations"]
    ) -> DescribeMatchmakingConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_matchmaking_rule_sets"]
    ) -> DescribeMatchmakingRuleSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_player_sessions"]
    ) -> DescribePlayerSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_builds"]) -> ListBuildsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_game_server_groups"]
    ) -> ListGameServerGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_game_servers"]
    ) -> ListGameServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_scripts"]) -> ListScriptsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_game_sessions"]
    ) -> SearchGameSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """
