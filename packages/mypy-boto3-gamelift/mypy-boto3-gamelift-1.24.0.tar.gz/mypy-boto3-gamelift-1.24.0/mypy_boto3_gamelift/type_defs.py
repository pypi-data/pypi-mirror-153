"""
Type annotations for gamelift service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/type_defs/)

Usage::

    ```python
    from mypy_boto3_gamelift.type_defs import AcceptMatchInputRequestTypeDef

    data: AcceptMatchInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AcceptanceTypeType,
    BackfillModeType,
    BalancingStrategyType,
    BuildStatusType,
    CertificateTypeType,
    ComparisonOperatorTypeType,
    EC2InstanceTypeType,
    EventCodeType,
    FleetStatusType,
    FleetTypeType,
    FlexMatchModeType,
    GameServerGroupDeleteOptionType,
    GameServerGroupInstanceTypeType,
    GameServerGroupStatusType,
    GameServerInstanceStatusType,
    GameServerProtectionPolicyType,
    GameServerUtilizationStatusType,
    GameSessionPlacementStateType,
    GameSessionStatusType,
    InstanceStatusType,
    IpProtocolType,
    MatchmakingConfigurationStatusType,
    MetricNameType,
    OperatingSystemType,
    PlayerSessionCreationPolicyType,
    PlayerSessionStatusType,
    PolicyTypeType,
    PriorityTypeType,
    ProtectionPolicyType,
    RoutingStrategyTypeType,
    ScalingAdjustmentTypeType,
    ScalingStatusTypeType,
    SortOrderType,
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
    "AcceptMatchInputRequestTypeDef",
    "RoutingStrategyTypeDef",
    "AttributeValueTypeDef",
    "AwsCredentialsTypeDef",
    "BuildTypeDef",
    "CertificateConfigurationTypeDef",
    "ClaimGameServerInputRequestTypeDef",
    "GameServerTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "S3LocationTypeDef",
    "IpPermissionTypeDef",
    "LocationConfigurationTypeDef",
    "ResourceCreationLimitPolicyTypeDef",
    "LocationStateTypeDef",
    "InstanceDefinitionTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "GamePropertyTypeDef",
    "FilterConfigurationTypeDef",
    "GameSessionQueueDestinationTypeDef",
    "PlayerLatencyPolicyTypeDef",
    "PriorityConfigurationTypeDef",
    "MatchmakingRuleSetTypeDef",
    "CreatePlayerSessionInputRequestTypeDef",
    "PlayerSessionTypeDef",
    "CreatePlayerSessionsInputRequestTypeDef",
    "CreateVpcPeeringAuthorizationInputRequestTypeDef",
    "VpcPeeringAuthorizationTypeDef",
    "CreateVpcPeeringConnectionInputRequestTypeDef",
    "DeleteAliasInputRequestTypeDef",
    "DeleteBuildInputRequestTypeDef",
    "DeleteFleetInputRequestTypeDef",
    "DeleteFleetLocationsInputRequestTypeDef",
    "DeleteGameServerGroupInputRequestTypeDef",
    "DeleteGameSessionQueueInputRequestTypeDef",
    "DeleteMatchmakingConfigurationInputRequestTypeDef",
    "DeleteMatchmakingRuleSetInputRequestTypeDef",
    "DeleteScalingPolicyInputRequestTypeDef",
    "DeleteScriptInputRequestTypeDef",
    "DeleteVpcPeeringAuthorizationInputRequestTypeDef",
    "DeleteVpcPeeringConnectionInputRequestTypeDef",
    "DeregisterGameServerInputRequestTypeDef",
    "DescribeAliasInputRequestTypeDef",
    "DescribeBuildInputRequestTypeDef",
    "DescribeEC2InstanceLimitsInputRequestTypeDef",
    "EC2InstanceLimitTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeFleetAttributesInputRequestTypeDef",
    "DescribeFleetCapacityInputRequestTypeDef",
    "DescribeFleetEventsInputRequestTypeDef",
    "EventTypeDef",
    "DescribeFleetLocationAttributesInputRequestTypeDef",
    "DescribeFleetLocationCapacityInputRequestTypeDef",
    "DescribeFleetLocationUtilizationInputRequestTypeDef",
    "FleetUtilizationTypeDef",
    "DescribeFleetPortSettingsInputRequestTypeDef",
    "DescribeFleetUtilizationInputRequestTypeDef",
    "DescribeGameServerGroupInputRequestTypeDef",
    "DescribeGameServerInputRequestTypeDef",
    "DescribeGameServerInstancesInputRequestTypeDef",
    "GameServerInstanceTypeDef",
    "DescribeGameSessionDetailsInputRequestTypeDef",
    "DescribeGameSessionPlacementInputRequestTypeDef",
    "DescribeGameSessionQueuesInputRequestTypeDef",
    "DescribeGameSessionsInputRequestTypeDef",
    "DescribeInstancesInputRequestTypeDef",
    "InstanceTypeDef",
    "DescribeMatchmakingConfigurationsInputRequestTypeDef",
    "DescribeMatchmakingInputRequestTypeDef",
    "DescribeMatchmakingRuleSetsInputRequestTypeDef",
    "DescribePlayerSessionsInputRequestTypeDef",
    "DescribeRuntimeConfigurationInputRequestTypeDef",
    "DescribeScalingPoliciesInputRequestTypeDef",
    "DescribeScriptInputRequestTypeDef",
    "DescribeVpcPeeringConnectionsInputRequestTypeDef",
    "DesiredPlayerSessionTypeDef",
    "EC2InstanceCountsTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "MatchedPlayerSessionTypeDef",
    "PlacedPlayerSessionTypeDef",
    "PlayerLatencyTypeDef",
    "GetGameSessionLogUrlInputRequestTypeDef",
    "GetInstanceAccessInputRequestTypeDef",
    "InstanceCredentialsTypeDef",
    "ListAliasesInputRequestTypeDef",
    "ListBuildsInputRequestTypeDef",
    "ListFleetsInputRequestTypeDef",
    "ListGameServerGroupsInputRequestTypeDef",
    "ListGameServersInputRequestTypeDef",
    "ListScriptsInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TargetConfigurationTypeDef",
    "RegisterGameServerInputRequestTypeDef",
    "RequestUploadCredentialsInputRequestTypeDef",
    "ResolveAliasInputRequestTypeDef",
    "ResumeGameServerGroupInputRequestTypeDef",
    "ServerProcessTypeDef",
    "SearchGameSessionsInputRequestTypeDef",
    "StartFleetActionsInputRequestTypeDef",
    "StopFleetActionsInputRequestTypeDef",
    "StopGameSessionPlacementInputRequestTypeDef",
    "StopMatchmakingInputRequestTypeDef",
    "SuspendGameServerGroupInputRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBuildInputRequestTypeDef",
    "UpdateFleetCapacityInputRequestTypeDef",
    "UpdateGameServerInputRequestTypeDef",
    "UpdateGameSessionInputRequestTypeDef",
    "ValidateMatchmakingRuleSetInputRequestTypeDef",
    "VpcPeeringConnectionStatusTypeDef",
    "AliasTypeDef",
    "UpdateAliasInputRequestTypeDef",
    "PlayerTypeDef",
    "ClaimGameServerOutputTypeDef",
    "DescribeBuildOutputTypeDef",
    "DescribeGameServerOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetGameSessionLogUrlOutputTypeDef",
    "ListBuildsOutputTypeDef",
    "ListFleetsOutputTypeDef",
    "ListGameServersOutputTypeDef",
    "PutScalingPolicyOutputTypeDef",
    "RegisterGameServerOutputTypeDef",
    "ResolveAliasOutputTypeDef",
    "StartFleetActionsOutputTypeDef",
    "StopFleetActionsOutputTypeDef",
    "UpdateBuildOutputTypeDef",
    "UpdateFleetAttributesOutputTypeDef",
    "UpdateFleetCapacityOutputTypeDef",
    "UpdateFleetPortSettingsOutputTypeDef",
    "UpdateGameServerOutputTypeDef",
    "ValidateMatchmakingRuleSetOutputTypeDef",
    "CreateAliasInputRequestTypeDef",
    "CreateMatchmakingRuleSetInputRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateBuildInputRequestTypeDef",
    "CreateBuildOutputTypeDef",
    "CreateScriptInputRequestTypeDef",
    "RequestUploadCredentialsOutputTypeDef",
    "ScriptTypeDef",
    "UpdateScriptInputRequestTypeDef",
    "DescribeFleetPortSettingsOutputTypeDef",
    "UpdateFleetPortSettingsInputRequestTypeDef",
    "CreateFleetLocationsInputRequestTypeDef",
    "FleetAttributesTypeDef",
    "UpdateFleetAttributesInputRequestTypeDef",
    "CreateFleetLocationsOutputTypeDef",
    "DeleteFleetLocationsOutputTypeDef",
    "LocationAttributesTypeDef",
    "GameServerGroupTypeDef",
    "UpdateGameServerGroupInputRequestTypeDef",
    "CreateGameSessionInputRequestTypeDef",
    "CreateMatchmakingConfigurationInputRequestTypeDef",
    "GameSessionTypeDef",
    "MatchmakingConfigurationTypeDef",
    "UpdateMatchmakingConfigurationInputRequestTypeDef",
    "CreateGameSessionQueueInputRequestTypeDef",
    "GameSessionQueueTypeDef",
    "UpdateGameSessionQueueInputRequestTypeDef",
    "CreateMatchmakingRuleSetOutputTypeDef",
    "DescribeMatchmakingRuleSetsOutputTypeDef",
    "CreatePlayerSessionOutputTypeDef",
    "CreatePlayerSessionsOutputTypeDef",
    "DescribePlayerSessionsOutputTypeDef",
    "CreateVpcPeeringAuthorizationOutputTypeDef",
    "DescribeVpcPeeringAuthorizationsOutputTypeDef",
    "DescribeEC2InstanceLimitsOutputTypeDef",
    "DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef",
    "DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef",
    "DescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef",
    "DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef",
    "DescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef",
    "DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef",
    "DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef",
    "DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef",
    "DescribeInstancesInputDescribeInstancesPaginateTypeDef",
    "DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef",
    "DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef",
    "DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef",
    "DescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef",
    "ListAliasesInputListAliasesPaginateTypeDef",
    "ListBuildsInputListBuildsPaginateTypeDef",
    "ListFleetsInputListFleetsPaginateTypeDef",
    "ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef",
    "ListGameServersInputListGameServersPaginateTypeDef",
    "ListScriptsInputListScriptsPaginateTypeDef",
    "SearchGameSessionsInputSearchGameSessionsPaginateTypeDef",
    "DescribeFleetEventsOutputTypeDef",
    "DescribeFleetLocationUtilizationOutputTypeDef",
    "DescribeFleetUtilizationOutputTypeDef",
    "DescribeGameServerInstancesOutputTypeDef",
    "DescribeInstancesOutputTypeDef",
    "FleetCapacityTypeDef",
    "GameServerGroupAutoScalingPolicyTypeDef",
    "GameSessionConnectionInfoTypeDef",
    "GameSessionPlacementTypeDef",
    "StartGameSessionPlacementInputRequestTypeDef",
    "InstanceAccessTypeDef",
    "PutScalingPolicyInputRequestTypeDef",
    "ScalingPolicyTypeDef",
    "RuntimeConfigurationTypeDef",
    "VpcPeeringConnectionTypeDef",
    "CreateAliasOutputTypeDef",
    "DescribeAliasOutputTypeDef",
    "ListAliasesOutputTypeDef",
    "UpdateAliasOutputTypeDef",
    "StartMatchBackfillInputRequestTypeDef",
    "StartMatchmakingInputRequestTypeDef",
    "CreateScriptOutputTypeDef",
    "DescribeScriptOutputTypeDef",
    "ListScriptsOutputTypeDef",
    "UpdateScriptOutputTypeDef",
    "CreateFleetOutputTypeDef",
    "DescribeFleetAttributesOutputTypeDef",
    "DescribeFleetLocationAttributesOutputTypeDef",
    "CreateGameServerGroupOutputTypeDef",
    "DeleteGameServerGroupOutputTypeDef",
    "DescribeGameServerGroupOutputTypeDef",
    "ListGameServerGroupsOutputTypeDef",
    "ResumeGameServerGroupOutputTypeDef",
    "SuspendGameServerGroupOutputTypeDef",
    "UpdateGameServerGroupOutputTypeDef",
    "CreateGameSessionOutputTypeDef",
    "DescribeGameSessionsOutputTypeDef",
    "GameSessionDetailTypeDef",
    "SearchGameSessionsOutputTypeDef",
    "UpdateGameSessionOutputTypeDef",
    "CreateMatchmakingConfigurationOutputTypeDef",
    "DescribeMatchmakingConfigurationsOutputTypeDef",
    "UpdateMatchmakingConfigurationOutputTypeDef",
    "CreateGameSessionQueueOutputTypeDef",
    "DescribeGameSessionQueuesOutputTypeDef",
    "UpdateGameSessionQueueOutputTypeDef",
    "DescribeFleetCapacityOutputTypeDef",
    "DescribeFleetLocationCapacityOutputTypeDef",
    "CreateGameServerGroupInputRequestTypeDef",
    "MatchmakingTicketTypeDef",
    "DescribeGameSessionPlacementOutputTypeDef",
    "StartGameSessionPlacementOutputTypeDef",
    "StopGameSessionPlacementOutputTypeDef",
    "GetInstanceAccessOutputTypeDef",
    "DescribeScalingPoliciesOutputTypeDef",
    "CreateFleetInputRequestTypeDef",
    "DescribeRuntimeConfigurationOutputTypeDef",
    "UpdateRuntimeConfigurationInputRequestTypeDef",
    "UpdateRuntimeConfigurationOutputTypeDef",
    "DescribeVpcPeeringConnectionsOutputTypeDef",
    "DescribeGameSessionDetailsOutputTypeDef",
    "DescribeMatchmakingOutputTypeDef",
    "StartMatchBackfillOutputTypeDef",
    "StartMatchmakingOutputTypeDef",
)

AcceptMatchInputRequestTypeDef = TypedDict(
    "AcceptMatchInputRequestTypeDef",
    {
        "TicketId": str,
        "PlayerIds": Sequence[str],
        "AcceptanceType": AcceptanceTypeType,
    },
)

RoutingStrategyTypeDef = TypedDict(
    "RoutingStrategyTypeDef",
    {
        "Type": RoutingStrategyTypeType,
        "FleetId": str,
        "Message": str,
    },
    total=False,
)

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "S": str,
        "N": float,
        "SL": List[str],
        "SDM": Dict[str, float],
    },
    total=False,
)

AwsCredentialsTypeDef = TypedDict(
    "AwsCredentialsTypeDef",
    {
        "AccessKeyId": str,
        "SecretAccessKey": str,
        "SessionToken": str,
    },
    total=False,
)

BuildTypeDef = TypedDict(
    "BuildTypeDef",
    {
        "BuildId": str,
        "BuildArn": str,
        "Name": str,
        "Version": str,
        "Status": BuildStatusType,
        "SizeOnDisk": int,
        "OperatingSystem": OperatingSystemType,
        "CreationTime": datetime,
    },
    total=False,
)

CertificateConfigurationTypeDef = TypedDict(
    "CertificateConfigurationTypeDef",
    {
        "CertificateType": CertificateTypeType,
    },
)

_RequiredClaimGameServerInputRequestTypeDef = TypedDict(
    "_RequiredClaimGameServerInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalClaimGameServerInputRequestTypeDef = TypedDict(
    "_OptionalClaimGameServerInputRequestTypeDef",
    {
        "GameServerId": str,
        "GameServerData": str,
    },
    total=False,
)


class ClaimGameServerInputRequestTypeDef(
    _RequiredClaimGameServerInputRequestTypeDef, _OptionalClaimGameServerInputRequestTypeDef
):
    pass


GameServerTypeDef = TypedDict(
    "GameServerTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerGroupArn": str,
        "GameServerId": str,
        "InstanceId": str,
        "ConnectionInfo": str,
        "GameServerData": str,
        "ClaimStatus": Literal["CLAIMED"],
        "UtilizationStatus": GameServerUtilizationStatusType,
        "RegistrationTime": datetime,
        "LastClaimTime": datetime,
        "LastHealthCheckTime": datetime,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "Bucket": str,
        "Key": str,
        "RoleArn": str,
        "ObjectVersion": str,
    },
    total=False,
)

IpPermissionTypeDef = TypedDict(
    "IpPermissionTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "IpRange": str,
        "Protocol": IpProtocolType,
    },
)

LocationConfigurationTypeDef = TypedDict(
    "LocationConfigurationTypeDef",
    {
        "Location": str,
    },
    total=False,
)

ResourceCreationLimitPolicyTypeDef = TypedDict(
    "ResourceCreationLimitPolicyTypeDef",
    {
        "NewGameSessionsPerCreator": int,
        "PolicyPeriodInMinutes": int,
    },
    total=False,
)

LocationStateTypeDef = TypedDict(
    "LocationStateTypeDef",
    {
        "Location": str,
        "Status": FleetStatusType,
    },
    total=False,
)

_RequiredInstanceDefinitionTypeDef = TypedDict(
    "_RequiredInstanceDefinitionTypeDef",
    {
        "InstanceType": GameServerGroupInstanceTypeType,
    },
)
_OptionalInstanceDefinitionTypeDef = TypedDict(
    "_OptionalInstanceDefinitionTypeDef",
    {
        "WeightedCapacity": str,
    },
    total=False,
)


class InstanceDefinitionTypeDef(
    _RequiredInstanceDefinitionTypeDef, _OptionalInstanceDefinitionTypeDef
):
    pass


LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

GamePropertyTypeDef = TypedDict(
    "GamePropertyTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

FilterConfigurationTypeDef = TypedDict(
    "FilterConfigurationTypeDef",
    {
        "AllowedLocations": Sequence[str],
    },
    total=False,
)

GameSessionQueueDestinationTypeDef = TypedDict(
    "GameSessionQueueDestinationTypeDef",
    {
        "DestinationArn": str,
    },
    total=False,
)

PlayerLatencyPolicyTypeDef = TypedDict(
    "PlayerLatencyPolicyTypeDef",
    {
        "MaximumIndividualPlayerLatencyMilliseconds": int,
        "PolicyDurationSeconds": int,
    },
    total=False,
)

PriorityConfigurationTypeDef = TypedDict(
    "PriorityConfigurationTypeDef",
    {
        "PriorityOrder": Sequence[PriorityTypeType],
        "LocationOrder": Sequence[str],
    },
    total=False,
)

_RequiredMatchmakingRuleSetTypeDef = TypedDict(
    "_RequiredMatchmakingRuleSetTypeDef",
    {
        "RuleSetBody": str,
    },
)
_OptionalMatchmakingRuleSetTypeDef = TypedDict(
    "_OptionalMatchmakingRuleSetTypeDef",
    {
        "RuleSetName": str,
        "RuleSetArn": str,
        "CreationTime": datetime,
    },
    total=False,
)


class MatchmakingRuleSetTypeDef(
    _RequiredMatchmakingRuleSetTypeDef, _OptionalMatchmakingRuleSetTypeDef
):
    pass


_RequiredCreatePlayerSessionInputRequestTypeDef = TypedDict(
    "_RequiredCreatePlayerSessionInputRequestTypeDef",
    {
        "GameSessionId": str,
        "PlayerId": str,
    },
)
_OptionalCreatePlayerSessionInputRequestTypeDef = TypedDict(
    "_OptionalCreatePlayerSessionInputRequestTypeDef",
    {
        "PlayerData": str,
    },
    total=False,
)


class CreatePlayerSessionInputRequestTypeDef(
    _RequiredCreatePlayerSessionInputRequestTypeDef, _OptionalCreatePlayerSessionInputRequestTypeDef
):
    pass


PlayerSessionTypeDef = TypedDict(
    "PlayerSessionTypeDef",
    {
        "PlayerSessionId": str,
        "PlayerId": str,
        "GameSessionId": str,
        "FleetId": str,
        "FleetArn": str,
        "CreationTime": datetime,
        "TerminationTime": datetime,
        "Status": PlayerSessionStatusType,
        "IpAddress": str,
        "DnsName": str,
        "Port": int,
        "PlayerData": str,
    },
    total=False,
)

_RequiredCreatePlayerSessionsInputRequestTypeDef = TypedDict(
    "_RequiredCreatePlayerSessionsInputRequestTypeDef",
    {
        "GameSessionId": str,
        "PlayerIds": Sequence[str],
    },
)
_OptionalCreatePlayerSessionsInputRequestTypeDef = TypedDict(
    "_OptionalCreatePlayerSessionsInputRequestTypeDef",
    {
        "PlayerDataMap": Mapping[str, str],
    },
    total=False,
)


class CreatePlayerSessionsInputRequestTypeDef(
    _RequiredCreatePlayerSessionsInputRequestTypeDef,
    _OptionalCreatePlayerSessionsInputRequestTypeDef,
):
    pass


CreateVpcPeeringAuthorizationInputRequestTypeDef = TypedDict(
    "CreateVpcPeeringAuthorizationInputRequestTypeDef",
    {
        "GameLiftAwsAccountId": str,
        "PeerVpcId": str,
    },
)

VpcPeeringAuthorizationTypeDef = TypedDict(
    "VpcPeeringAuthorizationTypeDef",
    {
        "GameLiftAwsAccountId": str,
        "PeerVpcAwsAccountId": str,
        "PeerVpcId": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
    },
    total=False,
)

CreateVpcPeeringConnectionInputRequestTypeDef = TypedDict(
    "CreateVpcPeeringConnectionInputRequestTypeDef",
    {
        "FleetId": str,
        "PeerVpcAwsAccountId": str,
        "PeerVpcId": str,
    },
)

DeleteAliasInputRequestTypeDef = TypedDict(
    "DeleteAliasInputRequestTypeDef",
    {
        "AliasId": str,
    },
)

DeleteBuildInputRequestTypeDef = TypedDict(
    "DeleteBuildInputRequestTypeDef",
    {
        "BuildId": str,
    },
)

DeleteFleetInputRequestTypeDef = TypedDict(
    "DeleteFleetInputRequestTypeDef",
    {
        "FleetId": str,
    },
)

DeleteFleetLocationsInputRequestTypeDef = TypedDict(
    "DeleteFleetLocationsInputRequestTypeDef",
    {
        "FleetId": str,
        "Locations": Sequence[str],
    },
)

_RequiredDeleteGameServerGroupInputRequestTypeDef = TypedDict(
    "_RequiredDeleteGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalDeleteGameServerGroupInputRequestTypeDef = TypedDict(
    "_OptionalDeleteGameServerGroupInputRequestTypeDef",
    {
        "DeleteOption": GameServerGroupDeleteOptionType,
    },
    total=False,
)


class DeleteGameServerGroupInputRequestTypeDef(
    _RequiredDeleteGameServerGroupInputRequestTypeDef,
    _OptionalDeleteGameServerGroupInputRequestTypeDef,
):
    pass


DeleteGameSessionQueueInputRequestTypeDef = TypedDict(
    "DeleteGameSessionQueueInputRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteMatchmakingConfigurationInputRequestTypeDef = TypedDict(
    "DeleteMatchmakingConfigurationInputRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteMatchmakingRuleSetInputRequestTypeDef = TypedDict(
    "DeleteMatchmakingRuleSetInputRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteScalingPolicyInputRequestTypeDef = TypedDict(
    "DeleteScalingPolicyInputRequestTypeDef",
    {
        "Name": str,
        "FleetId": str,
    },
)

DeleteScriptInputRequestTypeDef = TypedDict(
    "DeleteScriptInputRequestTypeDef",
    {
        "ScriptId": str,
    },
)

DeleteVpcPeeringAuthorizationInputRequestTypeDef = TypedDict(
    "DeleteVpcPeeringAuthorizationInputRequestTypeDef",
    {
        "GameLiftAwsAccountId": str,
        "PeerVpcId": str,
    },
)

DeleteVpcPeeringConnectionInputRequestTypeDef = TypedDict(
    "DeleteVpcPeeringConnectionInputRequestTypeDef",
    {
        "FleetId": str,
        "VpcPeeringConnectionId": str,
    },
)

DeregisterGameServerInputRequestTypeDef = TypedDict(
    "DeregisterGameServerInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerId": str,
    },
)

DescribeAliasInputRequestTypeDef = TypedDict(
    "DescribeAliasInputRequestTypeDef",
    {
        "AliasId": str,
    },
)

DescribeBuildInputRequestTypeDef = TypedDict(
    "DescribeBuildInputRequestTypeDef",
    {
        "BuildId": str,
    },
)

DescribeEC2InstanceLimitsInputRequestTypeDef = TypedDict(
    "DescribeEC2InstanceLimitsInputRequestTypeDef",
    {
        "EC2InstanceType": EC2InstanceTypeType,
        "Location": str,
    },
    total=False,
)

EC2InstanceLimitTypeDef = TypedDict(
    "EC2InstanceLimitTypeDef",
    {
        "EC2InstanceType": EC2InstanceTypeType,
        "CurrentInstances": int,
        "InstanceLimit": int,
        "Location": str,
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

DescribeFleetAttributesInputRequestTypeDef = TypedDict(
    "DescribeFleetAttributesInputRequestTypeDef",
    {
        "FleetIds": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetCapacityInputRequestTypeDef = TypedDict(
    "DescribeFleetCapacityInputRequestTypeDef",
    {
        "FleetIds": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeFleetEventsInputRequestTypeDef = TypedDict(
    "_RequiredDescribeFleetEventsInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeFleetEventsInputRequestTypeDef = TypedDict(
    "_OptionalDescribeFleetEventsInputRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeFleetEventsInputRequestTypeDef(
    _RequiredDescribeFleetEventsInputRequestTypeDef, _OptionalDescribeFleetEventsInputRequestTypeDef
):
    pass


EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "EventId": str,
        "ResourceId": str,
        "EventCode": EventCodeType,
        "Message": str,
        "EventTime": datetime,
        "PreSignedLogUrl": str,
    },
    total=False,
)

_RequiredDescribeFleetLocationAttributesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeFleetLocationAttributesInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeFleetLocationAttributesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeFleetLocationAttributesInputRequestTypeDef",
    {
        "Locations": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeFleetLocationAttributesInputRequestTypeDef(
    _RequiredDescribeFleetLocationAttributesInputRequestTypeDef,
    _OptionalDescribeFleetLocationAttributesInputRequestTypeDef,
):
    pass


DescribeFleetLocationCapacityInputRequestTypeDef = TypedDict(
    "DescribeFleetLocationCapacityInputRequestTypeDef",
    {
        "FleetId": str,
        "Location": str,
    },
)

DescribeFleetLocationUtilizationInputRequestTypeDef = TypedDict(
    "DescribeFleetLocationUtilizationInputRequestTypeDef",
    {
        "FleetId": str,
        "Location": str,
    },
)

FleetUtilizationTypeDef = TypedDict(
    "FleetUtilizationTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "ActiveServerProcessCount": int,
        "ActiveGameSessionCount": int,
        "CurrentPlayerSessionCount": int,
        "MaximumPlayerSessionCount": int,
        "Location": str,
    },
    total=False,
)

_RequiredDescribeFleetPortSettingsInputRequestTypeDef = TypedDict(
    "_RequiredDescribeFleetPortSettingsInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeFleetPortSettingsInputRequestTypeDef = TypedDict(
    "_OptionalDescribeFleetPortSettingsInputRequestTypeDef",
    {
        "Location": str,
    },
    total=False,
)


class DescribeFleetPortSettingsInputRequestTypeDef(
    _RequiredDescribeFleetPortSettingsInputRequestTypeDef,
    _OptionalDescribeFleetPortSettingsInputRequestTypeDef,
):
    pass


DescribeFleetUtilizationInputRequestTypeDef = TypedDict(
    "DescribeFleetUtilizationInputRequestTypeDef",
    {
        "FleetIds": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeGameServerGroupInputRequestTypeDef = TypedDict(
    "DescribeGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)

DescribeGameServerInputRequestTypeDef = TypedDict(
    "DescribeGameServerInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerId": str,
    },
)

_RequiredDescribeGameServerInstancesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeGameServerInstancesInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalDescribeGameServerInstancesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeGameServerInstancesInputRequestTypeDef",
    {
        "InstanceIds": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeGameServerInstancesInputRequestTypeDef(
    _RequiredDescribeGameServerInstancesInputRequestTypeDef,
    _OptionalDescribeGameServerInstancesInputRequestTypeDef,
):
    pass


GameServerInstanceTypeDef = TypedDict(
    "GameServerInstanceTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerGroupArn": str,
        "InstanceId": str,
        "InstanceStatus": GameServerInstanceStatusType,
    },
    total=False,
)

DescribeGameSessionDetailsInputRequestTypeDef = TypedDict(
    "DescribeGameSessionDetailsInputRequestTypeDef",
    {
        "FleetId": str,
        "GameSessionId": str,
        "AliasId": str,
        "Location": str,
        "StatusFilter": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeGameSessionPlacementInputRequestTypeDef = TypedDict(
    "DescribeGameSessionPlacementInputRequestTypeDef",
    {
        "PlacementId": str,
    },
)

DescribeGameSessionQueuesInputRequestTypeDef = TypedDict(
    "DescribeGameSessionQueuesInputRequestTypeDef",
    {
        "Names": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeGameSessionsInputRequestTypeDef = TypedDict(
    "DescribeGameSessionsInputRequestTypeDef",
    {
        "FleetId": str,
        "GameSessionId": str,
        "AliasId": str,
        "Location": str,
        "StatusFilter": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeInstancesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeInstancesInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeInstancesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeInstancesInputRequestTypeDef",
    {
        "InstanceId": str,
        "Limit": int,
        "NextToken": str,
        "Location": str,
    },
    total=False,
)


class DescribeInstancesInputRequestTypeDef(
    _RequiredDescribeInstancesInputRequestTypeDef, _OptionalDescribeInstancesInputRequestTypeDef
):
    pass


InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "InstanceId": str,
        "IpAddress": str,
        "DnsName": str,
        "OperatingSystem": OperatingSystemType,
        "Type": EC2InstanceTypeType,
        "Status": InstanceStatusType,
        "CreationTime": datetime,
        "Location": str,
    },
    total=False,
)

DescribeMatchmakingConfigurationsInputRequestTypeDef = TypedDict(
    "DescribeMatchmakingConfigurationsInputRequestTypeDef",
    {
        "Names": Sequence[str],
        "RuleSetName": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeMatchmakingInputRequestTypeDef = TypedDict(
    "DescribeMatchmakingInputRequestTypeDef",
    {
        "TicketIds": Sequence[str],
    },
)

DescribeMatchmakingRuleSetsInputRequestTypeDef = TypedDict(
    "DescribeMatchmakingRuleSetsInputRequestTypeDef",
    {
        "Names": Sequence[str],
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribePlayerSessionsInputRequestTypeDef = TypedDict(
    "DescribePlayerSessionsInputRequestTypeDef",
    {
        "GameSessionId": str,
        "PlayerId": str,
        "PlayerSessionId": str,
        "PlayerSessionStatusFilter": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

DescribeRuntimeConfigurationInputRequestTypeDef = TypedDict(
    "DescribeRuntimeConfigurationInputRequestTypeDef",
    {
        "FleetId": str,
    },
)

_RequiredDescribeScalingPoliciesInputRequestTypeDef = TypedDict(
    "_RequiredDescribeScalingPoliciesInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeScalingPoliciesInputRequestTypeDef = TypedDict(
    "_OptionalDescribeScalingPoliciesInputRequestTypeDef",
    {
        "StatusFilter": ScalingStatusTypeType,
        "Limit": int,
        "NextToken": str,
        "Location": str,
    },
    total=False,
)


class DescribeScalingPoliciesInputRequestTypeDef(
    _RequiredDescribeScalingPoliciesInputRequestTypeDef,
    _OptionalDescribeScalingPoliciesInputRequestTypeDef,
):
    pass


DescribeScriptInputRequestTypeDef = TypedDict(
    "DescribeScriptInputRequestTypeDef",
    {
        "ScriptId": str,
    },
)

DescribeVpcPeeringConnectionsInputRequestTypeDef = TypedDict(
    "DescribeVpcPeeringConnectionsInputRequestTypeDef",
    {
        "FleetId": str,
    },
    total=False,
)

DesiredPlayerSessionTypeDef = TypedDict(
    "DesiredPlayerSessionTypeDef",
    {
        "PlayerId": str,
        "PlayerData": str,
    },
    total=False,
)

EC2InstanceCountsTypeDef = TypedDict(
    "EC2InstanceCountsTypeDef",
    {
        "DESIRED": int,
        "MINIMUM": int,
        "MAXIMUM": int,
        "PENDING": int,
        "ACTIVE": int,
        "IDLE": int,
        "TERMINATING": int,
    },
    total=False,
)

TargetTrackingConfigurationTypeDef = TypedDict(
    "TargetTrackingConfigurationTypeDef",
    {
        "TargetValue": float,
    },
)

MatchedPlayerSessionTypeDef = TypedDict(
    "MatchedPlayerSessionTypeDef",
    {
        "PlayerId": str,
        "PlayerSessionId": str,
    },
    total=False,
)

PlacedPlayerSessionTypeDef = TypedDict(
    "PlacedPlayerSessionTypeDef",
    {
        "PlayerId": str,
        "PlayerSessionId": str,
    },
    total=False,
)

PlayerLatencyTypeDef = TypedDict(
    "PlayerLatencyTypeDef",
    {
        "PlayerId": str,
        "RegionIdentifier": str,
        "LatencyInMilliseconds": float,
    },
    total=False,
)

GetGameSessionLogUrlInputRequestTypeDef = TypedDict(
    "GetGameSessionLogUrlInputRequestTypeDef",
    {
        "GameSessionId": str,
    },
)

GetInstanceAccessInputRequestTypeDef = TypedDict(
    "GetInstanceAccessInputRequestTypeDef",
    {
        "FleetId": str,
        "InstanceId": str,
    },
)

InstanceCredentialsTypeDef = TypedDict(
    "InstanceCredentialsTypeDef",
    {
        "UserName": str,
        "Secret": str,
    },
    total=False,
)

ListAliasesInputRequestTypeDef = TypedDict(
    "ListAliasesInputRequestTypeDef",
    {
        "RoutingStrategyType": RoutingStrategyTypeType,
        "Name": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

ListBuildsInputRequestTypeDef = TypedDict(
    "ListBuildsInputRequestTypeDef",
    {
        "Status": BuildStatusType,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

ListFleetsInputRequestTypeDef = TypedDict(
    "ListFleetsInputRequestTypeDef",
    {
        "BuildId": str,
        "ScriptId": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

ListGameServerGroupsInputRequestTypeDef = TypedDict(
    "ListGameServerGroupsInputRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListGameServersInputRequestTypeDef = TypedDict(
    "_RequiredListGameServersInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalListGameServersInputRequestTypeDef = TypedDict(
    "_OptionalListGameServersInputRequestTypeDef",
    {
        "SortOrder": SortOrderType,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)


class ListGameServersInputRequestTypeDef(
    _RequiredListGameServersInputRequestTypeDef, _OptionalListGameServersInputRequestTypeDef
):
    pass


ListScriptsInputRequestTypeDef = TypedDict(
    "ListScriptsInputRequestTypeDef",
    {
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

TargetConfigurationTypeDef = TypedDict(
    "TargetConfigurationTypeDef",
    {
        "TargetValue": float,
    },
)

_RequiredRegisterGameServerInputRequestTypeDef = TypedDict(
    "_RequiredRegisterGameServerInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerId": str,
        "InstanceId": str,
    },
)
_OptionalRegisterGameServerInputRequestTypeDef = TypedDict(
    "_OptionalRegisterGameServerInputRequestTypeDef",
    {
        "ConnectionInfo": str,
        "GameServerData": str,
    },
    total=False,
)


class RegisterGameServerInputRequestTypeDef(
    _RequiredRegisterGameServerInputRequestTypeDef, _OptionalRegisterGameServerInputRequestTypeDef
):
    pass


RequestUploadCredentialsInputRequestTypeDef = TypedDict(
    "RequestUploadCredentialsInputRequestTypeDef",
    {
        "BuildId": str,
    },
)

ResolveAliasInputRequestTypeDef = TypedDict(
    "ResolveAliasInputRequestTypeDef",
    {
        "AliasId": str,
    },
)

ResumeGameServerGroupInputRequestTypeDef = TypedDict(
    "ResumeGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "ResumeActions": Sequence[Literal["REPLACE_INSTANCE_TYPES"]],
    },
)

_RequiredServerProcessTypeDef = TypedDict(
    "_RequiredServerProcessTypeDef",
    {
        "LaunchPath": str,
        "ConcurrentExecutions": int,
    },
)
_OptionalServerProcessTypeDef = TypedDict(
    "_OptionalServerProcessTypeDef",
    {
        "Parameters": str,
    },
    total=False,
)


class ServerProcessTypeDef(_RequiredServerProcessTypeDef, _OptionalServerProcessTypeDef):
    pass


SearchGameSessionsInputRequestTypeDef = TypedDict(
    "SearchGameSessionsInputRequestTypeDef",
    {
        "FleetId": str,
        "AliasId": str,
        "Location": str,
        "FilterExpression": str,
        "SortExpression": str,
        "Limit": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredStartFleetActionsInputRequestTypeDef = TypedDict(
    "_RequiredStartFleetActionsInputRequestTypeDef",
    {
        "FleetId": str,
        "Actions": Sequence[Literal["AUTO_SCALING"]],
    },
)
_OptionalStartFleetActionsInputRequestTypeDef = TypedDict(
    "_OptionalStartFleetActionsInputRequestTypeDef",
    {
        "Location": str,
    },
    total=False,
)


class StartFleetActionsInputRequestTypeDef(
    _RequiredStartFleetActionsInputRequestTypeDef, _OptionalStartFleetActionsInputRequestTypeDef
):
    pass


_RequiredStopFleetActionsInputRequestTypeDef = TypedDict(
    "_RequiredStopFleetActionsInputRequestTypeDef",
    {
        "FleetId": str,
        "Actions": Sequence[Literal["AUTO_SCALING"]],
    },
)
_OptionalStopFleetActionsInputRequestTypeDef = TypedDict(
    "_OptionalStopFleetActionsInputRequestTypeDef",
    {
        "Location": str,
    },
    total=False,
)


class StopFleetActionsInputRequestTypeDef(
    _RequiredStopFleetActionsInputRequestTypeDef, _OptionalStopFleetActionsInputRequestTypeDef
):
    pass


StopGameSessionPlacementInputRequestTypeDef = TypedDict(
    "StopGameSessionPlacementInputRequestTypeDef",
    {
        "PlacementId": str,
    },
)

StopMatchmakingInputRequestTypeDef = TypedDict(
    "StopMatchmakingInputRequestTypeDef",
    {
        "TicketId": str,
    },
)

SuspendGameServerGroupInputRequestTypeDef = TypedDict(
    "SuspendGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "SuspendActions": Sequence[Literal["REPLACE_INSTANCE_TYPES"]],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateBuildInputRequestTypeDef = TypedDict(
    "_RequiredUpdateBuildInputRequestTypeDef",
    {
        "BuildId": str,
    },
)
_OptionalUpdateBuildInputRequestTypeDef = TypedDict(
    "_OptionalUpdateBuildInputRequestTypeDef",
    {
        "Name": str,
        "Version": str,
    },
    total=False,
)


class UpdateBuildInputRequestTypeDef(
    _RequiredUpdateBuildInputRequestTypeDef, _OptionalUpdateBuildInputRequestTypeDef
):
    pass


_RequiredUpdateFleetCapacityInputRequestTypeDef = TypedDict(
    "_RequiredUpdateFleetCapacityInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalUpdateFleetCapacityInputRequestTypeDef = TypedDict(
    "_OptionalUpdateFleetCapacityInputRequestTypeDef",
    {
        "DesiredInstances": int,
        "MinSize": int,
        "MaxSize": int,
        "Location": str,
    },
    total=False,
)


class UpdateFleetCapacityInputRequestTypeDef(
    _RequiredUpdateFleetCapacityInputRequestTypeDef, _OptionalUpdateFleetCapacityInputRequestTypeDef
):
    pass


_RequiredUpdateGameServerInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGameServerInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerId": str,
    },
)
_OptionalUpdateGameServerInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGameServerInputRequestTypeDef",
    {
        "GameServerData": str,
        "UtilizationStatus": GameServerUtilizationStatusType,
        "HealthCheck": Literal["HEALTHY"],
    },
    total=False,
)


class UpdateGameServerInputRequestTypeDef(
    _RequiredUpdateGameServerInputRequestTypeDef, _OptionalUpdateGameServerInputRequestTypeDef
):
    pass


_RequiredUpdateGameSessionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGameSessionInputRequestTypeDef",
    {
        "GameSessionId": str,
    },
)
_OptionalUpdateGameSessionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGameSessionInputRequestTypeDef",
    {
        "MaximumPlayerSessionCount": int,
        "Name": str,
        "PlayerSessionCreationPolicy": PlayerSessionCreationPolicyType,
        "ProtectionPolicy": ProtectionPolicyType,
    },
    total=False,
)


class UpdateGameSessionInputRequestTypeDef(
    _RequiredUpdateGameSessionInputRequestTypeDef, _OptionalUpdateGameSessionInputRequestTypeDef
):
    pass


ValidateMatchmakingRuleSetInputRequestTypeDef = TypedDict(
    "ValidateMatchmakingRuleSetInputRequestTypeDef",
    {
        "RuleSetBody": str,
    },
)

VpcPeeringConnectionStatusTypeDef = TypedDict(
    "VpcPeeringConnectionStatusTypeDef",
    {
        "Code": str,
        "Message": str,
    },
    total=False,
)

AliasTypeDef = TypedDict(
    "AliasTypeDef",
    {
        "AliasId": str,
        "Name": str,
        "AliasArn": str,
        "Description": str,
        "RoutingStrategy": RoutingStrategyTypeDef,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredUpdateAliasInputRequestTypeDef = TypedDict(
    "_RequiredUpdateAliasInputRequestTypeDef",
    {
        "AliasId": str,
    },
)
_OptionalUpdateAliasInputRequestTypeDef = TypedDict(
    "_OptionalUpdateAliasInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "RoutingStrategy": RoutingStrategyTypeDef,
    },
    total=False,
)


class UpdateAliasInputRequestTypeDef(
    _RequiredUpdateAliasInputRequestTypeDef, _OptionalUpdateAliasInputRequestTypeDef
):
    pass


PlayerTypeDef = TypedDict(
    "PlayerTypeDef",
    {
        "PlayerId": str,
        "PlayerAttributes": Dict[str, AttributeValueTypeDef],
        "Team": str,
        "LatencyInMs": Dict[str, int],
    },
    total=False,
)

ClaimGameServerOutputTypeDef = TypedDict(
    "ClaimGameServerOutputTypeDef",
    {
        "GameServer": GameServerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBuildOutputTypeDef = TypedDict(
    "DescribeBuildOutputTypeDef",
    {
        "Build": BuildTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameServerOutputTypeDef = TypedDict(
    "DescribeGameServerOutputTypeDef",
    {
        "GameServer": GameServerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGameSessionLogUrlOutputTypeDef = TypedDict(
    "GetGameSessionLogUrlOutputTypeDef",
    {
        "PreSignedUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBuildsOutputTypeDef = TypedDict(
    "ListBuildsOutputTypeDef",
    {
        "Builds": List[BuildTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFleetsOutputTypeDef = TypedDict(
    "ListFleetsOutputTypeDef",
    {
        "FleetIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGameServersOutputTypeDef = TypedDict(
    "ListGameServersOutputTypeDef",
    {
        "GameServers": List[GameServerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutScalingPolicyOutputTypeDef = TypedDict(
    "PutScalingPolicyOutputTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterGameServerOutputTypeDef = TypedDict(
    "RegisterGameServerOutputTypeDef",
    {
        "GameServer": GameServerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResolveAliasOutputTypeDef = TypedDict(
    "ResolveAliasOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFleetActionsOutputTypeDef = TypedDict(
    "StartFleetActionsOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopFleetActionsOutputTypeDef = TypedDict(
    "StopFleetActionsOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBuildOutputTypeDef = TypedDict(
    "UpdateBuildOutputTypeDef",
    {
        "Build": BuildTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFleetAttributesOutputTypeDef = TypedDict(
    "UpdateFleetAttributesOutputTypeDef",
    {
        "FleetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFleetCapacityOutputTypeDef = TypedDict(
    "UpdateFleetCapacityOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFleetPortSettingsOutputTypeDef = TypedDict(
    "UpdateFleetPortSettingsOutputTypeDef",
    {
        "FleetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameServerOutputTypeDef = TypedDict(
    "UpdateGameServerOutputTypeDef",
    {
        "GameServer": GameServerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidateMatchmakingRuleSetOutputTypeDef = TypedDict(
    "ValidateMatchmakingRuleSetOutputTypeDef",
    {
        "Valid": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAliasInputRequestTypeDef = TypedDict(
    "_RequiredCreateAliasInputRequestTypeDef",
    {
        "Name": str,
        "RoutingStrategy": RoutingStrategyTypeDef,
    },
)
_OptionalCreateAliasInputRequestTypeDef = TypedDict(
    "_OptionalCreateAliasInputRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAliasInputRequestTypeDef(
    _RequiredCreateAliasInputRequestTypeDef, _OptionalCreateAliasInputRequestTypeDef
):
    pass


_RequiredCreateMatchmakingRuleSetInputRequestTypeDef = TypedDict(
    "_RequiredCreateMatchmakingRuleSetInputRequestTypeDef",
    {
        "Name": str,
        "RuleSetBody": str,
    },
)
_OptionalCreateMatchmakingRuleSetInputRequestTypeDef = TypedDict(
    "_OptionalCreateMatchmakingRuleSetInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMatchmakingRuleSetInputRequestTypeDef(
    _RequiredCreateMatchmakingRuleSetInputRequestTypeDef,
    _OptionalCreateMatchmakingRuleSetInputRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateBuildInputRequestTypeDef = TypedDict(
    "CreateBuildInputRequestTypeDef",
    {
        "Name": str,
        "Version": str,
        "StorageLocation": S3LocationTypeDef,
        "OperatingSystem": OperatingSystemType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

CreateBuildOutputTypeDef = TypedDict(
    "CreateBuildOutputTypeDef",
    {
        "Build": BuildTypeDef,
        "UploadCredentials": AwsCredentialsTypeDef,
        "StorageLocation": S3LocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateScriptInputRequestTypeDef = TypedDict(
    "CreateScriptInputRequestTypeDef",
    {
        "Name": str,
        "Version": str,
        "StorageLocation": S3LocationTypeDef,
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

RequestUploadCredentialsOutputTypeDef = TypedDict(
    "RequestUploadCredentialsOutputTypeDef",
    {
        "UploadCredentials": AwsCredentialsTypeDef,
        "StorageLocation": S3LocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScriptTypeDef = TypedDict(
    "ScriptTypeDef",
    {
        "ScriptId": str,
        "ScriptArn": str,
        "Name": str,
        "Version": str,
        "SizeOnDisk": int,
        "CreationTime": datetime,
        "StorageLocation": S3LocationTypeDef,
    },
    total=False,
)

_RequiredUpdateScriptInputRequestTypeDef = TypedDict(
    "_RequiredUpdateScriptInputRequestTypeDef",
    {
        "ScriptId": str,
    },
)
_OptionalUpdateScriptInputRequestTypeDef = TypedDict(
    "_OptionalUpdateScriptInputRequestTypeDef",
    {
        "Name": str,
        "Version": str,
        "StorageLocation": S3LocationTypeDef,
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class UpdateScriptInputRequestTypeDef(
    _RequiredUpdateScriptInputRequestTypeDef, _OptionalUpdateScriptInputRequestTypeDef
):
    pass


DescribeFleetPortSettingsOutputTypeDef = TypedDict(
    "DescribeFleetPortSettingsOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "InboundPermissions": List[IpPermissionTypeDef],
        "UpdateStatus": Literal["PENDING_UPDATE"],
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateFleetPortSettingsInputRequestTypeDef = TypedDict(
    "_RequiredUpdateFleetPortSettingsInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalUpdateFleetPortSettingsInputRequestTypeDef = TypedDict(
    "_OptionalUpdateFleetPortSettingsInputRequestTypeDef",
    {
        "InboundPermissionAuthorizations": Sequence[IpPermissionTypeDef],
        "InboundPermissionRevocations": Sequence[IpPermissionTypeDef],
    },
    total=False,
)


class UpdateFleetPortSettingsInputRequestTypeDef(
    _RequiredUpdateFleetPortSettingsInputRequestTypeDef,
    _OptionalUpdateFleetPortSettingsInputRequestTypeDef,
):
    pass


CreateFleetLocationsInputRequestTypeDef = TypedDict(
    "CreateFleetLocationsInputRequestTypeDef",
    {
        "FleetId": str,
        "Locations": Sequence[LocationConfigurationTypeDef],
    },
)

FleetAttributesTypeDef = TypedDict(
    "FleetAttributesTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "FleetType": FleetTypeType,
        "InstanceType": EC2InstanceTypeType,
        "Description": str,
        "Name": str,
        "CreationTime": datetime,
        "TerminationTime": datetime,
        "Status": FleetStatusType,
        "BuildId": str,
        "BuildArn": str,
        "ScriptId": str,
        "ScriptArn": str,
        "ServerLaunchPath": str,
        "ServerLaunchParameters": str,
        "LogPaths": List[str],
        "NewGameSessionProtectionPolicy": ProtectionPolicyType,
        "OperatingSystem": OperatingSystemType,
        "ResourceCreationLimitPolicy": ResourceCreationLimitPolicyTypeDef,
        "MetricGroups": List[str],
        "StoppedActions": List[Literal["AUTO_SCALING"]],
        "InstanceRoleArn": str,
        "CertificateConfiguration": CertificateConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateFleetAttributesInputRequestTypeDef = TypedDict(
    "_RequiredUpdateFleetAttributesInputRequestTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalUpdateFleetAttributesInputRequestTypeDef = TypedDict(
    "_OptionalUpdateFleetAttributesInputRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "NewGameSessionProtectionPolicy": ProtectionPolicyType,
        "ResourceCreationLimitPolicy": ResourceCreationLimitPolicyTypeDef,
        "MetricGroups": Sequence[str],
    },
    total=False,
)


class UpdateFleetAttributesInputRequestTypeDef(
    _RequiredUpdateFleetAttributesInputRequestTypeDef,
    _OptionalUpdateFleetAttributesInputRequestTypeDef,
):
    pass


CreateFleetLocationsOutputTypeDef = TypedDict(
    "CreateFleetLocationsOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "LocationStates": List[LocationStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFleetLocationsOutputTypeDef = TypedDict(
    "DeleteFleetLocationsOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "LocationStates": List[LocationStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LocationAttributesTypeDef = TypedDict(
    "LocationAttributesTypeDef",
    {
        "LocationState": LocationStateTypeDef,
        "StoppedActions": List[Literal["AUTO_SCALING"]],
        "UpdateStatus": Literal["PENDING_UPDATE"],
    },
    total=False,
)

GameServerGroupTypeDef = TypedDict(
    "GameServerGroupTypeDef",
    {
        "GameServerGroupName": str,
        "GameServerGroupArn": str,
        "RoleArn": str,
        "InstanceDefinitions": List[InstanceDefinitionTypeDef],
        "BalancingStrategy": BalancingStrategyType,
        "GameServerProtectionPolicy": GameServerProtectionPolicyType,
        "AutoScalingGroupArn": str,
        "Status": GameServerGroupStatusType,
        "StatusReason": str,
        "SuspendedActions": List[Literal["REPLACE_INSTANCE_TYPES"]],
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredUpdateGameServerGroupInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalUpdateGameServerGroupInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGameServerGroupInputRequestTypeDef",
    {
        "RoleArn": str,
        "InstanceDefinitions": Sequence[InstanceDefinitionTypeDef],
        "GameServerProtectionPolicy": GameServerProtectionPolicyType,
        "BalancingStrategy": BalancingStrategyType,
    },
    total=False,
)


class UpdateGameServerGroupInputRequestTypeDef(
    _RequiredUpdateGameServerGroupInputRequestTypeDef,
    _OptionalUpdateGameServerGroupInputRequestTypeDef,
):
    pass


_RequiredCreateGameSessionInputRequestTypeDef = TypedDict(
    "_RequiredCreateGameSessionInputRequestTypeDef",
    {
        "MaximumPlayerSessionCount": int,
    },
)
_OptionalCreateGameSessionInputRequestTypeDef = TypedDict(
    "_OptionalCreateGameSessionInputRequestTypeDef",
    {
        "FleetId": str,
        "AliasId": str,
        "Name": str,
        "GameProperties": Sequence[GamePropertyTypeDef],
        "CreatorId": str,
        "GameSessionId": str,
        "IdempotencyToken": str,
        "GameSessionData": str,
        "Location": str,
    },
    total=False,
)


class CreateGameSessionInputRequestTypeDef(
    _RequiredCreateGameSessionInputRequestTypeDef, _OptionalCreateGameSessionInputRequestTypeDef
):
    pass


_RequiredCreateMatchmakingConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredCreateMatchmakingConfigurationInputRequestTypeDef",
    {
        "Name": str,
        "RequestTimeoutSeconds": int,
        "AcceptanceRequired": bool,
        "RuleSetName": str,
    },
)
_OptionalCreateMatchmakingConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalCreateMatchmakingConfigurationInputRequestTypeDef",
    {
        "Description": str,
        "GameSessionQueueArns": Sequence[str],
        "AcceptanceTimeoutSeconds": int,
        "NotificationTarget": str,
        "AdditionalPlayerCount": int,
        "CustomEventData": str,
        "GameProperties": Sequence[GamePropertyTypeDef],
        "GameSessionData": str,
        "BackfillMode": BackfillModeType,
        "FlexMatchMode": FlexMatchModeType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMatchmakingConfigurationInputRequestTypeDef(
    _RequiredCreateMatchmakingConfigurationInputRequestTypeDef,
    _OptionalCreateMatchmakingConfigurationInputRequestTypeDef,
):
    pass


GameSessionTypeDef = TypedDict(
    "GameSessionTypeDef",
    {
        "GameSessionId": str,
        "Name": str,
        "FleetId": str,
        "FleetArn": str,
        "CreationTime": datetime,
        "TerminationTime": datetime,
        "CurrentPlayerSessionCount": int,
        "MaximumPlayerSessionCount": int,
        "Status": GameSessionStatusType,
        "StatusReason": Literal["INTERRUPTED"],
        "GameProperties": List[GamePropertyTypeDef],
        "IpAddress": str,
        "DnsName": str,
        "Port": int,
        "PlayerSessionCreationPolicy": PlayerSessionCreationPolicyType,
        "CreatorId": str,
        "GameSessionData": str,
        "MatchmakerData": str,
        "Location": str,
    },
    total=False,
)

MatchmakingConfigurationTypeDef = TypedDict(
    "MatchmakingConfigurationTypeDef",
    {
        "Name": str,
        "ConfigurationArn": str,
        "Description": str,
        "GameSessionQueueArns": List[str],
        "RequestTimeoutSeconds": int,
        "AcceptanceTimeoutSeconds": int,
        "AcceptanceRequired": bool,
        "RuleSetName": str,
        "RuleSetArn": str,
        "NotificationTarget": str,
        "AdditionalPlayerCount": int,
        "CustomEventData": str,
        "CreationTime": datetime,
        "GameProperties": List[GamePropertyTypeDef],
        "GameSessionData": str,
        "BackfillMode": BackfillModeType,
        "FlexMatchMode": FlexMatchModeType,
    },
    total=False,
)

_RequiredUpdateMatchmakingConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMatchmakingConfigurationInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateMatchmakingConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMatchmakingConfigurationInputRequestTypeDef",
    {
        "Description": str,
        "GameSessionQueueArns": Sequence[str],
        "RequestTimeoutSeconds": int,
        "AcceptanceTimeoutSeconds": int,
        "AcceptanceRequired": bool,
        "RuleSetName": str,
        "NotificationTarget": str,
        "AdditionalPlayerCount": int,
        "CustomEventData": str,
        "GameProperties": Sequence[GamePropertyTypeDef],
        "GameSessionData": str,
        "BackfillMode": BackfillModeType,
        "FlexMatchMode": FlexMatchModeType,
    },
    total=False,
)


class UpdateMatchmakingConfigurationInputRequestTypeDef(
    _RequiredUpdateMatchmakingConfigurationInputRequestTypeDef,
    _OptionalUpdateMatchmakingConfigurationInputRequestTypeDef,
):
    pass


_RequiredCreateGameSessionQueueInputRequestTypeDef = TypedDict(
    "_RequiredCreateGameSessionQueueInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateGameSessionQueueInputRequestTypeDef = TypedDict(
    "_OptionalCreateGameSessionQueueInputRequestTypeDef",
    {
        "TimeoutInSeconds": int,
        "PlayerLatencyPolicies": Sequence[PlayerLatencyPolicyTypeDef],
        "Destinations": Sequence[GameSessionQueueDestinationTypeDef],
        "FilterConfiguration": FilterConfigurationTypeDef,
        "PriorityConfiguration": PriorityConfigurationTypeDef,
        "CustomEventData": str,
        "NotificationTarget": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGameSessionQueueInputRequestTypeDef(
    _RequiredCreateGameSessionQueueInputRequestTypeDef,
    _OptionalCreateGameSessionQueueInputRequestTypeDef,
):
    pass


GameSessionQueueTypeDef = TypedDict(
    "GameSessionQueueTypeDef",
    {
        "Name": str,
        "GameSessionQueueArn": str,
        "TimeoutInSeconds": int,
        "PlayerLatencyPolicies": List[PlayerLatencyPolicyTypeDef],
        "Destinations": List[GameSessionQueueDestinationTypeDef],
        "FilterConfiguration": FilterConfigurationTypeDef,
        "PriorityConfiguration": PriorityConfigurationTypeDef,
        "CustomEventData": str,
        "NotificationTarget": str,
    },
    total=False,
)

_RequiredUpdateGameSessionQueueInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGameSessionQueueInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateGameSessionQueueInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGameSessionQueueInputRequestTypeDef",
    {
        "TimeoutInSeconds": int,
        "PlayerLatencyPolicies": Sequence[PlayerLatencyPolicyTypeDef],
        "Destinations": Sequence[GameSessionQueueDestinationTypeDef],
        "FilterConfiguration": FilterConfigurationTypeDef,
        "PriorityConfiguration": PriorityConfigurationTypeDef,
        "CustomEventData": str,
        "NotificationTarget": str,
    },
    total=False,
)


class UpdateGameSessionQueueInputRequestTypeDef(
    _RequiredUpdateGameSessionQueueInputRequestTypeDef,
    _OptionalUpdateGameSessionQueueInputRequestTypeDef,
):
    pass


CreateMatchmakingRuleSetOutputTypeDef = TypedDict(
    "CreateMatchmakingRuleSetOutputTypeDef",
    {
        "RuleSet": MatchmakingRuleSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMatchmakingRuleSetsOutputTypeDef = TypedDict(
    "DescribeMatchmakingRuleSetsOutputTypeDef",
    {
        "RuleSets": List[MatchmakingRuleSetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePlayerSessionOutputTypeDef = TypedDict(
    "CreatePlayerSessionOutputTypeDef",
    {
        "PlayerSession": PlayerSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePlayerSessionsOutputTypeDef = TypedDict(
    "CreatePlayerSessionsOutputTypeDef",
    {
        "PlayerSessions": List[PlayerSessionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePlayerSessionsOutputTypeDef = TypedDict(
    "DescribePlayerSessionsOutputTypeDef",
    {
        "PlayerSessions": List[PlayerSessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVpcPeeringAuthorizationOutputTypeDef = TypedDict(
    "CreateVpcPeeringAuthorizationOutputTypeDef",
    {
        "VpcPeeringAuthorization": VpcPeeringAuthorizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVpcPeeringAuthorizationsOutputTypeDef = TypedDict(
    "DescribeVpcPeeringAuthorizationsOutputTypeDef",
    {
        "VpcPeeringAuthorizations": List[VpcPeeringAuthorizationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEC2InstanceLimitsOutputTypeDef = TypedDict(
    "DescribeEC2InstanceLimitsOutputTypeDef",
    {
        "EC2InstanceLimits": List[EC2InstanceLimitTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef = TypedDict(
    "DescribeFleetAttributesInputDescribeFleetAttributesPaginateTypeDef",
    {
        "FleetIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef = TypedDict(
    "DescribeFleetCapacityInputDescribeFleetCapacityPaginateTypeDef",
    {
        "FleetIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef = TypedDict(
    "_RequiredDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef = TypedDict(
    "_OptionalDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef(
    _RequiredDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef,
    _OptionalDescribeFleetEventsInputDescribeFleetEventsPaginateTypeDef,
):
    pass


DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef = TypedDict(
    "DescribeFleetUtilizationInputDescribeFleetUtilizationPaginateTypeDef",
    {
        "FleetIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef = TypedDict(
    "_RequiredDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef = TypedDict(
    "_OptionalDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef",
    {
        "InstanceIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef(
    _RequiredDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef,
    _OptionalDescribeGameServerInstancesInputDescribeGameServerInstancesPaginateTypeDef,
):
    pass


DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef = TypedDict(
    "DescribeGameSessionDetailsInputDescribeGameSessionDetailsPaginateTypeDef",
    {
        "FleetId": str,
        "GameSessionId": str,
        "AliasId": str,
        "Location": str,
        "StatusFilter": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef = TypedDict(
    "DescribeGameSessionQueuesInputDescribeGameSessionQueuesPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef = TypedDict(
    "DescribeGameSessionsInputDescribeGameSessionsPaginateTypeDef",
    {
        "FleetId": str,
        "GameSessionId": str,
        "AliasId": str,
        "Location": str,
        "StatusFilter": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeInstancesInputDescribeInstancesPaginateTypeDef = TypedDict(
    "_RequiredDescribeInstancesInputDescribeInstancesPaginateTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeInstancesInputDescribeInstancesPaginateTypeDef = TypedDict(
    "_OptionalDescribeInstancesInputDescribeInstancesPaginateTypeDef",
    {
        "InstanceId": str,
        "Location": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeInstancesInputDescribeInstancesPaginateTypeDef(
    _RequiredDescribeInstancesInputDescribeInstancesPaginateTypeDef,
    _OptionalDescribeInstancesInputDescribeInstancesPaginateTypeDef,
):
    pass


DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef = TypedDict(
    "DescribeMatchmakingConfigurationsInputDescribeMatchmakingConfigurationsPaginateTypeDef",
    {
        "Names": Sequence[str],
        "RuleSetName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef = TypedDict(
    "DescribeMatchmakingRuleSetsInputDescribeMatchmakingRuleSetsPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef = TypedDict(
    "DescribePlayerSessionsInputDescribePlayerSessionsPaginateTypeDef",
    {
        "GameSessionId": str,
        "PlayerId": str,
        "PlayerSessionId": str,
        "PlayerSessionStatusFilter": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef = TypedDict(
    "_RequiredDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef",
    {
        "FleetId": str,
    },
)
_OptionalDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef = TypedDict(
    "_OptionalDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef",
    {
        "StatusFilter": ScalingStatusTypeType,
        "Location": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef(
    _RequiredDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef,
    _OptionalDescribeScalingPoliciesInputDescribeScalingPoliciesPaginateTypeDef,
):
    pass


ListAliasesInputListAliasesPaginateTypeDef = TypedDict(
    "ListAliasesInputListAliasesPaginateTypeDef",
    {
        "RoutingStrategyType": RoutingStrategyTypeType,
        "Name": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListBuildsInputListBuildsPaginateTypeDef = TypedDict(
    "ListBuildsInputListBuildsPaginateTypeDef",
    {
        "Status": BuildStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFleetsInputListFleetsPaginateTypeDef = TypedDict(
    "ListFleetsInputListFleetsPaginateTypeDef",
    {
        "BuildId": str,
        "ScriptId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef = TypedDict(
    "ListGameServerGroupsInputListGameServerGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListGameServersInputListGameServersPaginateTypeDef = TypedDict(
    "_RequiredListGameServersInputListGameServersPaginateTypeDef",
    {
        "GameServerGroupName": str,
    },
)
_OptionalListGameServersInputListGameServersPaginateTypeDef = TypedDict(
    "_OptionalListGameServersInputListGameServersPaginateTypeDef",
    {
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGameServersInputListGameServersPaginateTypeDef(
    _RequiredListGameServersInputListGameServersPaginateTypeDef,
    _OptionalListGameServersInputListGameServersPaginateTypeDef,
):
    pass


ListScriptsInputListScriptsPaginateTypeDef = TypedDict(
    "ListScriptsInputListScriptsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

SearchGameSessionsInputSearchGameSessionsPaginateTypeDef = TypedDict(
    "SearchGameSessionsInputSearchGameSessionsPaginateTypeDef",
    {
        "FleetId": str,
        "AliasId": str,
        "Location": str,
        "FilterExpression": str,
        "SortExpression": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeFleetEventsOutputTypeDef = TypedDict(
    "DescribeFleetEventsOutputTypeDef",
    {
        "Events": List[EventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetLocationUtilizationOutputTypeDef = TypedDict(
    "DescribeFleetLocationUtilizationOutputTypeDef",
    {
        "FleetUtilization": FleetUtilizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetUtilizationOutputTypeDef = TypedDict(
    "DescribeFleetUtilizationOutputTypeDef",
    {
        "FleetUtilization": List[FleetUtilizationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameServerInstancesOutputTypeDef = TypedDict(
    "DescribeGameServerInstancesOutputTypeDef",
    {
        "GameServerInstances": List[GameServerInstanceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstancesOutputTypeDef = TypedDict(
    "DescribeInstancesOutputTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FleetCapacityTypeDef = TypedDict(
    "FleetCapacityTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "InstanceType": EC2InstanceTypeType,
        "InstanceCounts": EC2InstanceCountsTypeDef,
        "Location": str,
    },
    total=False,
)

_RequiredGameServerGroupAutoScalingPolicyTypeDef = TypedDict(
    "_RequiredGameServerGroupAutoScalingPolicyTypeDef",
    {
        "TargetTrackingConfiguration": TargetTrackingConfigurationTypeDef,
    },
)
_OptionalGameServerGroupAutoScalingPolicyTypeDef = TypedDict(
    "_OptionalGameServerGroupAutoScalingPolicyTypeDef",
    {
        "EstimatedInstanceWarmup": int,
    },
    total=False,
)


class GameServerGroupAutoScalingPolicyTypeDef(
    _RequiredGameServerGroupAutoScalingPolicyTypeDef,
    _OptionalGameServerGroupAutoScalingPolicyTypeDef,
):
    pass


GameSessionConnectionInfoTypeDef = TypedDict(
    "GameSessionConnectionInfoTypeDef",
    {
        "GameSessionArn": str,
        "IpAddress": str,
        "DnsName": str,
        "Port": int,
        "MatchedPlayerSessions": List[MatchedPlayerSessionTypeDef],
    },
    total=False,
)

GameSessionPlacementTypeDef = TypedDict(
    "GameSessionPlacementTypeDef",
    {
        "PlacementId": str,
        "GameSessionQueueName": str,
        "Status": GameSessionPlacementStateType,
        "GameProperties": List[GamePropertyTypeDef],
        "MaximumPlayerSessionCount": int,
        "GameSessionName": str,
        "GameSessionId": str,
        "GameSessionArn": str,
        "GameSessionRegion": str,
        "PlayerLatencies": List[PlayerLatencyTypeDef],
        "StartTime": datetime,
        "EndTime": datetime,
        "IpAddress": str,
        "DnsName": str,
        "Port": int,
        "PlacedPlayerSessions": List[PlacedPlayerSessionTypeDef],
        "GameSessionData": str,
        "MatchmakerData": str,
    },
    total=False,
)

_RequiredStartGameSessionPlacementInputRequestTypeDef = TypedDict(
    "_RequiredStartGameSessionPlacementInputRequestTypeDef",
    {
        "PlacementId": str,
        "GameSessionQueueName": str,
        "MaximumPlayerSessionCount": int,
    },
)
_OptionalStartGameSessionPlacementInputRequestTypeDef = TypedDict(
    "_OptionalStartGameSessionPlacementInputRequestTypeDef",
    {
        "GameProperties": Sequence[GamePropertyTypeDef],
        "GameSessionName": str,
        "PlayerLatencies": Sequence[PlayerLatencyTypeDef],
        "DesiredPlayerSessions": Sequence[DesiredPlayerSessionTypeDef],
        "GameSessionData": str,
    },
    total=False,
)


class StartGameSessionPlacementInputRequestTypeDef(
    _RequiredStartGameSessionPlacementInputRequestTypeDef,
    _OptionalStartGameSessionPlacementInputRequestTypeDef,
):
    pass


InstanceAccessTypeDef = TypedDict(
    "InstanceAccessTypeDef",
    {
        "FleetId": str,
        "InstanceId": str,
        "IpAddress": str,
        "OperatingSystem": OperatingSystemType,
        "Credentials": InstanceCredentialsTypeDef,
    },
    total=False,
)

_RequiredPutScalingPolicyInputRequestTypeDef = TypedDict(
    "_RequiredPutScalingPolicyInputRequestTypeDef",
    {
        "Name": str,
        "FleetId": str,
        "MetricName": MetricNameType,
    },
)
_OptionalPutScalingPolicyInputRequestTypeDef = TypedDict(
    "_OptionalPutScalingPolicyInputRequestTypeDef",
    {
        "ScalingAdjustment": int,
        "ScalingAdjustmentType": ScalingAdjustmentTypeType,
        "Threshold": float,
        "ComparisonOperator": ComparisonOperatorTypeType,
        "EvaluationPeriods": int,
        "PolicyType": PolicyTypeType,
        "TargetConfiguration": TargetConfigurationTypeDef,
    },
    total=False,
)


class PutScalingPolicyInputRequestTypeDef(
    _RequiredPutScalingPolicyInputRequestTypeDef, _OptionalPutScalingPolicyInputRequestTypeDef
):
    pass


ScalingPolicyTypeDef = TypedDict(
    "ScalingPolicyTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "Name": str,
        "Status": ScalingStatusTypeType,
        "ScalingAdjustment": int,
        "ScalingAdjustmentType": ScalingAdjustmentTypeType,
        "ComparisonOperator": ComparisonOperatorTypeType,
        "Threshold": float,
        "EvaluationPeriods": int,
        "MetricName": MetricNameType,
        "PolicyType": PolicyTypeType,
        "TargetConfiguration": TargetConfigurationTypeDef,
        "UpdateStatus": Literal["PENDING_UPDATE"],
        "Location": str,
    },
    total=False,
)

RuntimeConfigurationTypeDef = TypedDict(
    "RuntimeConfigurationTypeDef",
    {
        "ServerProcesses": Sequence[ServerProcessTypeDef],
        "MaxConcurrentGameSessionActivations": int,
        "GameSessionActivationTimeoutSeconds": int,
    },
    total=False,
)

VpcPeeringConnectionTypeDef = TypedDict(
    "VpcPeeringConnectionTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "IpV4CidrBlock": str,
        "VpcPeeringConnectionId": str,
        "Status": VpcPeeringConnectionStatusTypeDef,
        "PeerVpcId": str,
        "GameLiftVpcId": str,
    },
    total=False,
)

CreateAliasOutputTypeDef = TypedDict(
    "CreateAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAliasOutputTypeDef = TypedDict(
    "DescribeAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAliasesOutputTypeDef = TypedDict(
    "ListAliasesOutputTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAliasOutputTypeDef = TypedDict(
    "UpdateAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartMatchBackfillInputRequestTypeDef = TypedDict(
    "_RequiredStartMatchBackfillInputRequestTypeDef",
    {
        "ConfigurationName": str,
        "Players": Sequence[PlayerTypeDef],
    },
)
_OptionalStartMatchBackfillInputRequestTypeDef = TypedDict(
    "_OptionalStartMatchBackfillInputRequestTypeDef",
    {
        "TicketId": str,
        "GameSessionArn": str,
    },
    total=False,
)


class StartMatchBackfillInputRequestTypeDef(
    _RequiredStartMatchBackfillInputRequestTypeDef, _OptionalStartMatchBackfillInputRequestTypeDef
):
    pass


_RequiredStartMatchmakingInputRequestTypeDef = TypedDict(
    "_RequiredStartMatchmakingInputRequestTypeDef",
    {
        "ConfigurationName": str,
        "Players": Sequence[PlayerTypeDef],
    },
)
_OptionalStartMatchmakingInputRequestTypeDef = TypedDict(
    "_OptionalStartMatchmakingInputRequestTypeDef",
    {
        "TicketId": str,
    },
    total=False,
)


class StartMatchmakingInputRequestTypeDef(
    _RequiredStartMatchmakingInputRequestTypeDef, _OptionalStartMatchmakingInputRequestTypeDef
):
    pass


CreateScriptOutputTypeDef = TypedDict(
    "CreateScriptOutputTypeDef",
    {
        "Script": ScriptTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeScriptOutputTypeDef = TypedDict(
    "DescribeScriptOutputTypeDef",
    {
        "Script": ScriptTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListScriptsOutputTypeDef = TypedDict(
    "ListScriptsOutputTypeDef",
    {
        "Scripts": List[ScriptTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateScriptOutputTypeDef = TypedDict(
    "UpdateScriptOutputTypeDef",
    {
        "Script": ScriptTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFleetOutputTypeDef = TypedDict(
    "CreateFleetOutputTypeDef",
    {
        "FleetAttributes": FleetAttributesTypeDef,
        "LocationStates": List[LocationStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetAttributesOutputTypeDef = TypedDict(
    "DescribeFleetAttributesOutputTypeDef",
    {
        "FleetAttributes": List[FleetAttributesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetLocationAttributesOutputTypeDef = TypedDict(
    "DescribeFleetLocationAttributesOutputTypeDef",
    {
        "FleetId": str,
        "FleetArn": str,
        "LocationAttributes": List[LocationAttributesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGameServerGroupOutputTypeDef = TypedDict(
    "CreateGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGameServerGroupOutputTypeDef = TypedDict(
    "DeleteGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameServerGroupOutputTypeDef = TypedDict(
    "DescribeGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGameServerGroupsOutputTypeDef = TypedDict(
    "ListGameServerGroupsOutputTypeDef",
    {
        "GameServerGroups": List[GameServerGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResumeGameServerGroupOutputTypeDef = TypedDict(
    "ResumeGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SuspendGameServerGroupOutputTypeDef = TypedDict(
    "SuspendGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameServerGroupOutputTypeDef = TypedDict(
    "UpdateGameServerGroupOutputTypeDef",
    {
        "GameServerGroup": GameServerGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGameSessionOutputTypeDef = TypedDict(
    "CreateGameSessionOutputTypeDef",
    {
        "GameSession": GameSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameSessionsOutputTypeDef = TypedDict(
    "DescribeGameSessionsOutputTypeDef",
    {
        "GameSessions": List[GameSessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GameSessionDetailTypeDef = TypedDict(
    "GameSessionDetailTypeDef",
    {
        "GameSession": GameSessionTypeDef,
        "ProtectionPolicy": ProtectionPolicyType,
    },
    total=False,
)

SearchGameSessionsOutputTypeDef = TypedDict(
    "SearchGameSessionsOutputTypeDef",
    {
        "GameSessions": List[GameSessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameSessionOutputTypeDef = TypedDict(
    "UpdateGameSessionOutputTypeDef",
    {
        "GameSession": GameSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMatchmakingConfigurationOutputTypeDef = TypedDict(
    "CreateMatchmakingConfigurationOutputTypeDef",
    {
        "Configuration": MatchmakingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMatchmakingConfigurationsOutputTypeDef = TypedDict(
    "DescribeMatchmakingConfigurationsOutputTypeDef",
    {
        "Configurations": List[MatchmakingConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMatchmakingConfigurationOutputTypeDef = TypedDict(
    "UpdateMatchmakingConfigurationOutputTypeDef",
    {
        "Configuration": MatchmakingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGameSessionQueueOutputTypeDef = TypedDict(
    "CreateGameSessionQueueOutputTypeDef",
    {
        "GameSessionQueue": GameSessionQueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameSessionQueuesOutputTypeDef = TypedDict(
    "DescribeGameSessionQueuesOutputTypeDef",
    {
        "GameSessionQueues": List[GameSessionQueueTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameSessionQueueOutputTypeDef = TypedDict(
    "UpdateGameSessionQueueOutputTypeDef",
    {
        "GameSessionQueue": GameSessionQueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetCapacityOutputTypeDef = TypedDict(
    "DescribeFleetCapacityOutputTypeDef",
    {
        "FleetCapacity": List[FleetCapacityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetLocationCapacityOutputTypeDef = TypedDict(
    "DescribeFleetLocationCapacityOutputTypeDef",
    {
        "FleetCapacity": FleetCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateGameServerGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateGameServerGroupInputRequestTypeDef",
    {
        "GameServerGroupName": str,
        "RoleArn": str,
        "MinSize": int,
        "MaxSize": int,
        "LaunchTemplate": LaunchTemplateSpecificationTypeDef,
        "InstanceDefinitions": Sequence[InstanceDefinitionTypeDef],
    },
)
_OptionalCreateGameServerGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateGameServerGroupInputRequestTypeDef",
    {
        "AutoScalingPolicy": GameServerGroupAutoScalingPolicyTypeDef,
        "BalancingStrategy": BalancingStrategyType,
        "GameServerProtectionPolicy": GameServerProtectionPolicyType,
        "VpcSubnets": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGameServerGroupInputRequestTypeDef(
    _RequiredCreateGameServerGroupInputRequestTypeDef,
    _OptionalCreateGameServerGroupInputRequestTypeDef,
):
    pass


MatchmakingTicketTypeDef = TypedDict(
    "MatchmakingTicketTypeDef",
    {
        "TicketId": str,
        "ConfigurationName": str,
        "ConfigurationArn": str,
        "Status": MatchmakingConfigurationStatusType,
        "StatusReason": str,
        "StatusMessage": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Players": List[PlayerTypeDef],
        "GameSessionConnectionInfo": GameSessionConnectionInfoTypeDef,
        "EstimatedWaitTime": int,
    },
    total=False,
)

DescribeGameSessionPlacementOutputTypeDef = TypedDict(
    "DescribeGameSessionPlacementOutputTypeDef",
    {
        "GameSessionPlacement": GameSessionPlacementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGameSessionPlacementOutputTypeDef = TypedDict(
    "StartGameSessionPlacementOutputTypeDef",
    {
        "GameSessionPlacement": GameSessionPlacementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopGameSessionPlacementOutputTypeDef = TypedDict(
    "StopGameSessionPlacementOutputTypeDef",
    {
        "GameSessionPlacement": GameSessionPlacementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInstanceAccessOutputTypeDef = TypedDict(
    "GetInstanceAccessOutputTypeDef",
    {
        "InstanceAccess": InstanceAccessTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeScalingPoliciesOutputTypeDef = TypedDict(
    "DescribeScalingPoliciesOutputTypeDef",
    {
        "ScalingPolicies": List[ScalingPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateFleetInputRequestTypeDef = TypedDict(
    "_RequiredCreateFleetInputRequestTypeDef",
    {
        "Name": str,
        "EC2InstanceType": EC2InstanceTypeType,
    },
)
_OptionalCreateFleetInputRequestTypeDef = TypedDict(
    "_OptionalCreateFleetInputRequestTypeDef",
    {
        "Description": str,
        "BuildId": str,
        "ScriptId": str,
        "ServerLaunchPath": str,
        "ServerLaunchParameters": str,
        "LogPaths": Sequence[str],
        "EC2InboundPermissions": Sequence[IpPermissionTypeDef],
        "NewGameSessionProtectionPolicy": ProtectionPolicyType,
        "RuntimeConfiguration": RuntimeConfigurationTypeDef,
        "ResourceCreationLimitPolicy": ResourceCreationLimitPolicyTypeDef,
        "MetricGroups": Sequence[str],
        "PeerVpcAwsAccountId": str,
        "PeerVpcId": str,
        "FleetType": FleetTypeType,
        "InstanceRoleArn": str,
        "CertificateConfiguration": CertificateConfigurationTypeDef,
        "Locations": Sequence[LocationConfigurationTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFleetInputRequestTypeDef(
    _RequiredCreateFleetInputRequestTypeDef, _OptionalCreateFleetInputRequestTypeDef
):
    pass


DescribeRuntimeConfigurationOutputTypeDef = TypedDict(
    "DescribeRuntimeConfigurationOutputTypeDef",
    {
        "RuntimeConfiguration": RuntimeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuntimeConfigurationInputRequestTypeDef = TypedDict(
    "UpdateRuntimeConfigurationInputRequestTypeDef",
    {
        "FleetId": str,
        "RuntimeConfiguration": RuntimeConfigurationTypeDef,
    },
)

UpdateRuntimeConfigurationOutputTypeDef = TypedDict(
    "UpdateRuntimeConfigurationOutputTypeDef",
    {
        "RuntimeConfiguration": RuntimeConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVpcPeeringConnectionsOutputTypeDef = TypedDict(
    "DescribeVpcPeeringConnectionsOutputTypeDef",
    {
        "VpcPeeringConnections": List[VpcPeeringConnectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGameSessionDetailsOutputTypeDef = TypedDict(
    "DescribeGameSessionDetailsOutputTypeDef",
    {
        "GameSessionDetails": List[GameSessionDetailTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMatchmakingOutputTypeDef = TypedDict(
    "DescribeMatchmakingOutputTypeDef",
    {
        "TicketList": List[MatchmakingTicketTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMatchBackfillOutputTypeDef = TypedDict(
    "StartMatchBackfillOutputTypeDef",
    {
        "MatchmakingTicket": MatchmakingTicketTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMatchmakingOutputTypeDef = TypedDict(
    "StartMatchmakingOutputTypeDef",
    {
        "MatchmakingTicket": MatchmakingTicketTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
