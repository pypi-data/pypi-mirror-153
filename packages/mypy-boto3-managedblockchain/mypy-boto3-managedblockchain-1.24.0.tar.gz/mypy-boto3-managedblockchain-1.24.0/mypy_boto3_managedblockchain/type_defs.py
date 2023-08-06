"""
Type annotations for managedblockchain service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain/type_defs/)

Usage::

    ```python
    from mypy_boto3_managedblockchain.type_defs import ApprovalThresholdPolicyTypeDef

    data: ApprovalThresholdPolicyTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    EditionType,
    FrameworkType,
    InvitationStatusType,
    MemberStatusType,
    NetworkStatusType,
    NodeStatusType,
    ProposalStatusType,
    StateDBTypeType,
    ThresholdComparatorType,
    VoteValueType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApprovalThresholdPolicyTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteMemberInputRequestTypeDef",
    "DeleteNodeInputRequestTypeDef",
    "GetMemberInputRequestTypeDef",
    "GetNetworkInputRequestTypeDef",
    "GetNodeInputRequestTypeDef",
    "GetProposalInputRequestTypeDef",
    "NetworkSummaryTypeDef",
    "InviteActionTypeDef",
    "ListInvitationsInputRequestTypeDef",
    "ListMembersInputRequestTypeDef",
    "MemberSummaryTypeDef",
    "ListNetworksInputRequestTypeDef",
    "ListNodesInputRequestTypeDef",
    "NodeSummaryTypeDef",
    "ListProposalVotesInputRequestTypeDef",
    "VoteSummaryTypeDef",
    "ListProposalsInputRequestTypeDef",
    "ProposalSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "LogConfigurationTypeDef",
    "MemberFabricAttributesTypeDef",
    "MemberFabricConfigurationTypeDef",
    "NetworkEthereumAttributesTypeDef",
    "NetworkFabricAttributesTypeDef",
    "NetworkFabricConfigurationTypeDef",
    "NodeEthereumAttributesTypeDef",
    "NodeFabricAttributesTypeDef",
    "RemoveActionTypeDef",
    "RejectInvitationInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "VoteOnProposalInputRequestTypeDef",
    "VotingPolicyTypeDef",
    "CreateMemberOutputTypeDef",
    "CreateNetworkOutputTypeDef",
    "CreateNodeOutputTypeDef",
    "CreateProposalOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "InvitationTypeDef",
    "ListNetworksOutputTypeDef",
    "ListMembersOutputTypeDef",
    "ListNodesOutputTypeDef",
    "ListProposalVotesOutputTypeDef",
    "ListProposalsOutputTypeDef",
    "LogConfigurationsTypeDef",
    "MemberFrameworkAttributesTypeDef",
    "MemberFrameworkConfigurationTypeDef",
    "NetworkFrameworkAttributesTypeDef",
    "NetworkFrameworkConfigurationTypeDef",
    "NodeFrameworkAttributesTypeDef",
    "ProposalActionsTypeDef",
    "ListInvitationsOutputTypeDef",
    "MemberFabricLogPublishingConfigurationTypeDef",
    "NodeFabricLogPublishingConfigurationTypeDef",
    "NetworkTypeDef",
    "CreateProposalInputRequestTypeDef",
    "ProposalTypeDef",
    "MemberLogPublishingConfigurationTypeDef",
    "NodeLogPublishingConfigurationTypeDef",
    "GetNetworkOutputTypeDef",
    "GetProposalOutputTypeDef",
    "MemberConfigurationTypeDef",
    "MemberTypeDef",
    "UpdateMemberInputRequestTypeDef",
    "NodeConfigurationTypeDef",
    "NodeTypeDef",
    "UpdateNodeInputRequestTypeDef",
    "CreateMemberInputRequestTypeDef",
    "CreateNetworkInputRequestTypeDef",
    "GetMemberOutputTypeDef",
    "CreateNodeInputRequestTypeDef",
    "GetNodeOutputTypeDef",
)

ApprovalThresholdPolicyTypeDef = TypedDict(
    "ApprovalThresholdPolicyTypeDef",
    {
        "ThresholdPercentage": int,
        "ProposalDurationInHours": int,
        "ThresholdComparator": ThresholdComparatorType,
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

DeleteMemberInputRequestTypeDef = TypedDict(
    "DeleteMemberInputRequestTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
    },
)

_RequiredDeleteNodeInputRequestTypeDef = TypedDict(
    "_RequiredDeleteNodeInputRequestTypeDef",
    {
        "NetworkId": str,
        "NodeId": str,
    },
)
_OptionalDeleteNodeInputRequestTypeDef = TypedDict(
    "_OptionalDeleteNodeInputRequestTypeDef",
    {
        "MemberId": str,
    },
    total=False,
)


class DeleteNodeInputRequestTypeDef(
    _RequiredDeleteNodeInputRequestTypeDef, _OptionalDeleteNodeInputRequestTypeDef
):
    pass


GetMemberInputRequestTypeDef = TypedDict(
    "GetMemberInputRequestTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
    },
)

GetNetworkInputRequestTypeDef = TypedDict(
    "GetNetworkInputRequestTypeDef",
    {
        "NetworkId": str,
    },
)

_RequiredGetNodeInputRequestTypeDef = TypedDict(
    "_RequiredGetNodeInputRequestTypeDef",
    {
        "NetworkId": str,
        "NodeId": str,
    },
)
_OptionalGetNodeInputRequestTypeDef = TypedDict(
    "_OptionalGetNodeInputRequestTypeDef",
    {
        "MemberId": str,
    },
    total=False,
)


class GetNodeInputRequestTypeDef(
    _RequiredGetNodeInputRequestTypeDef, _OptionalGetNodeInputRequestTypeDef
):
    pass


GetProposalInputRequestTypeDef = TypedDict(
    "GetProposalInputRequestTypeDef",
    {
        "NetworkId": str,
        "ProposalId": str,
    },
)

NetworkSummaryTypeDef = TypedDict(
    "NetworkSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Framework": FrameworkType,
        "FrameworkVersion": str,
        "Status": NetworkStatusType,
        "CreationDate": datetime,
        "Arn": str,
    },
    total=False,
)

InviteActionTypeDef = TypedDict(
    "InviteActionTypeDef",
    {
        "Principal": str,
    },
)

ListInvitationsInputRequestTypeDef = TypedDict(
    "ListInvitationsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListMembersInputRequestTypeDef = TypedDict(
    "_RequiredListMembersInputRequestTypeDef",
    {
        "NetworkId": str,
    },
)
_OptionalListMembersInputRequestTypeDef = TypedDict(
    "_OptionalListMembersInputRequestTypeDef",
    {
        "Name": str,
        "Status": MemberStatusType,
        "IsOwned": bool,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListMembersInputRequestTypeDef(
    _RequiredListMembersInputRequestTypeDef, _OptionalListMembersInputRequestTypeDef
):
    pass


MemberSummaryTypeDef = TypedDict(
    "MemberSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Status": MemberStatusType,
        "CreationDate": datetime,
        "IsOwned": bool,
        "Arn": str,
    },
    total=False,
)

ListNetworksInputRequestTypeDef = TypedDict(
    "ListNetworksInputRequestTypeDef",
    {
        "Name": str,
        "Framework": FrameworkType,
        "Status": NetworkStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListNodesInputRequestTypeDef = TypedDict(
    "_RequiredListNodesInputRequestTypeDef",
    {
        "NetworkId": str,
    },
)
_OptionalListNodesInputRequestTypeDef = TypedDict(
    "_OptionalListNodesInputRequestTypeDef",
    {
        "MemberId": str,
        "Status": NodeStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListNodesInputRequestTypeDef(
    _RequiredListNodesInputRequestTypeDef, _OptionalListNodesInputRequestTypeDef
):
    pass


NodeSummaryTypeDef = TypedDict(
    "NodeSummaryTypeDef",
    {
        "Id": str,
        "Status": NodeStatusType,
        "CreationDate": datetime,
        "AvailabilityZone": str,
        "InstanceType": str,
        "Arn": str,
    },
    total=False,
)

_RequiredListProposalVotesInputRequestTypeDef = TypedDict(
    "_RequiredListProposalVotesInputRequestTypeDef",
    {
        "NetworkId": str,
        "ProposalId": str,
    },
)
_OptionalListProposalVotesInputRequestTypeDef = TypedDict(
    "_OptionalListProposalVotesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListProposalVotesInputRequestTypeDef(
    _RequiredListProposalVotesInputRequestTypeDef, _OptionalListProposalVotesInputRequestTypeDef
):
    pass


VoteSummaryTypeDef = TypedDict(
    "VoteSummaryTypeDef",
    {
        "Vote": VoteValueType,
        "MemberName": str,
        "MemberId": str,
    },
    total=False,
)

_RequiredListProposalsInputRequestTypeDef = TypedDict(
    "_RequiredListProposalsInputRequestTypeDef",
    {
        "NetworkId": str,
    },
)
_OptionalListProposalsInputRequestTypeDef = TypedDict(
    "_OptionalListProposalsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListProposalsInputRequestTypeDef(
    _RequiredListProposalsInputRequestTypeDef, _OptionalListProposalsInputRequestTypeDef
):
    pass


ProposalSummaryTypeDef = TypedDict(
    "ProposalSummaryTypeDef",
    {
        "ProposalId": str,
        "Description": str,
        "ProposedByMemberId": str,
        "ProposedByMemberName": str,
        "Status": ProposalStatusType,
        "CreationDate": datetime,
        "ExpirationDate": datetime,
        "Arn": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

LogConfigurationTypeDef = TypedDict(
    "LogConfigurationTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

MemberFabricAttributesTypeDef = TypedDict(
    "MemberFabricAttributesTypeDef",
    {
        "AdminUsername": str,
        "CaEndpoint": str,
    },
    total=False,
)

MemberFabricConfigurationTypeDef = TypedDict(
    "MemberFabricConfigurationTypeDef",
    {
        "AdminUsername": str,
        "AdminPassword": str,
    },
)

NetworkEthereumAttributesTypeDef = TypedDict(
    "NetworkEthereumAttributesTypeDef",
    {
        "ChainId": str,
    },
    total=False,
)

NetworkFabricAttributesTypeDef = TypedDict(
    "NetworkFabricAttributesTypeDef",
    {
        "OrderingServiceEndpoint": str,
        "Edition": EditionType,
    },
    total=False,
)

NetworkFabricConfigurationTypeDef = TypedDict(
    "NetworkFabricConfigurationTypeDef",
    {
        "Edition": EditionType,
    },
)

NodeEthereumAttributesTypeDef = TypedDict(
    "NodeEthereumAttributesTypeDef",
    {
        "HttpEndpoint": str,
        "WebSocketEndpoint": str,
    },
    total=False,
)

NodeFabricAttributesTypeDef = TypedDict(
    "NodeFabricAttributesTypeDef",
    {
        "PeerEndpoint": str,
        "PeerEventEndpoint": str,
    },
    total=False,
)

RemoveActionTypeDef = TypedDict(
    "RemoveActionTypeDef",
    {
        "MemberId": str,
    },
)

RejectInvitationInputRequestTypeDef = TypedDict(
    "RejectInvitationInputRequestTypeDef",
    {
        "InvitationId": str,
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

VoteOnProposalInputRequestTypeDef = TypedDict(
    "VoteOnProposalInputRequestTypeDef",
    {
        "NetworkId": str,
        "ProposalId": str,
        "VoterMemberId": str,
        "Vote": VoteValueType,
    },
)

VotingPolicyTypeDef = TypedDict(
    "VotingPolicyTypeDef",
    {
        "ApprovalThresholdPolicy": ApprovalThresholdPolicyTypeDef,
    },
    total=False,
)

CreateMemberOutputTypeDef = TypedDict(
    "CreateMemberOutputTypeDef",
    {
        "MemberId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNetworkOutputTypeDef = TypedDict(
    "CreateNetworkOutputTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNodeOutputTypeDef = TypedDict(
    "CreateNodeOutputTypeDef",
    {
        "NodeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProposalOutputTypeDef = TypedDict(
    "CreateProposalOutputTypeDef",
    {
        "ProposalId": str,
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

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {
        "InvitationId": str,
        "CreationDate": datetime,
        "ExpirationDate": datetime,
        "Status": InvitationStatusType,
        "NetworkSummary": NetworkSummaryTypeDef,
        "Arn": str,
    },
    total=False,
)

ListNetworksOutputTypeDef = TypedDict(
    "ListNetworksOutputTypeDef",
    {
        "Networks": List[NetworkSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersOutputTypeDef = TypedDict(
    "ListMembersOutputTypeDef",
    {
        "Members": List[MemberSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNodesOutputTypeDef = TypedDict(
    "ListNodesOutputTypeDef",
    {
        "Nodes": List[NodeSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProposalVotesOutputTypeDef = TypedDict(
    "ListProposalVotesOutputTypeDef",
    {
        "ProposalVotes": List[VoteSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProposalsOutputTypeDef = TypedDict(
    "ListProposalsOutputTypeDef",
    {
        "Proposals": List[ProposalSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LogConfigurationsTypeDef = TypedDict(
    "LogConfigurationsTypeDef",
    {
        "Cloudwatch": LogConfigurationTypeDef,
    },
    total=False,
)

MemberFrameworkAttributesTypeDef = TypedDict(
    "MemberFrameworkAttributesTypeDef",
    {
        "Fabric": MemberFabricAttributesTypeDef,
    },
    total=False,
)

MemberFrameworkConfigurationTypeDef = TypedDict(
    "MemberFrameworkConfigurationTypeDef",
    {
        "Fabric": MemberFabricConfigurationTypeDef,
    },
    total=False,
)

NetworkFrameworkAttributesTypeDef = TypedDict(
    "NetworkFrameworkAttributesTypeDef",
    {
        "Fabric": NetworkFabricAttributesTypeDef,
        "Ethereum": NetworkEthereumAttributesTypeDef,
    },
    total=False,
)

NetworkFrameworkConfigurationTypeDef = TypedDict(
    "NetworkFrameworkConfigurationTypeDef",
    {
        "Fabric": NetworkFabricConfigurationTypeDef,
    },
    total=False,
)

NodeFrameworkAttributesTypeDef = TypedDict(
    "NodeFrameworkAttributesTypeDef",
    {
        "Fabric": NodeFabricAttributesTypeDef,
        "Ethereum": NodeEthereumAttributesTypeDef,
    },
    total=False,
)

ProposalActionsTypeDef = TypedDict(
    "ProposalActionsTypeDef",
    {
        "Invitations": Sequence[InviteActionTypeDef],
        "Removals": Sequence[RemoveActionTypeDef],
    },
    total=False,
)

ListInvitationsOutputTypeDef = TypedDict(
    "ListInvitationsOutputTypeDef",
    {
        "Invitations": List[InvitationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MemberFabricLogPublishingConfigurationTypeDef = TypedDict(
    "MemberFabricLogPublishingConfigurationTypeDef",
    {
        "CaLogs": LogConfigurationsTypeDef,
    },
    total=False,
)

NodeFabricLogPublishingConfigurationTypeDef = TypedDict(
    "NodeFabricLogPublishingConfigurationTypeDef",
    {
        "ChaincodeLogs": LogConfigurationsTypeDef,
        "PeerLogs": LogConfigurationsTypeDef,
    },
    total=False,
)

NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "Framework": FrameworkType,
        "FrameworkVersion": str,
        "FrameworkAttributes": NetworkFrameworkAttributesTypeDef,
        "VpcEndpointServiceName": str,
        "VotingPolicy": VotingPolicyTypeDef,
        "Status": NetworkStatusType,
        "CreationDate": datetime,
        "Tags": Dict[str, str],
        "Arn": str,
    },
    total=False,
)

_RequiredCreateProposalInputRequestTypeDef = TypedDict(
    "_RequiredCreateProposalInputRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NetworkId": str,
        "MemberId": str,
        "Actions": ProposalActionsTypeDef,
    },
)
_OptionalCreateProposalInputRequestTypeDef = TypedDict(
    "_OptionalCreateProposalInputRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateProposalInputRequestTypeDef(
    _RequiredCreateProposalInputRequestTypeDef, _OptionalCreateProposalInputRequestTypeDef
):
    pass


ProposalTypeDef = TypedDict(
    "ProposalTypeDef",
    {
        "ProposalId": str,
        "NetworkId": str,
        "Description": str,
        "Actions": ProposalActionsTypeDef,
        "ProposedByMemberId": str,
        "ProposedByMemberName": str,
        "Status": ProposalStatusType,
        "CreationDate": datetime,
        "ExpirationDate": datetime,
        "YesVoteCount": int,
        "NoVoteCount": int,
        "OutstandingVoteCount": int,
        "Tags": Dict[str, str],
        "Arn": str,
    },
    total=False,
)

MemberLogPublishingConfigurationTypeDef = TypedDict(
    "MemberLogPublishingConfigurationTypeDef",
    {
        "Fabric": MemberFabricLogPublishingConfigurationTypeDef,
    },
    total=False,
)

NodeLogPublishingConfigurationTypeDef = TypedDict(
    "NodeLogPublishingConfigurationTypeDef",
    {
        "Fabric": NodeFabricLogPublishingConfigurationTypeDef,
    },
    total=False,
)

GetNetworkOutputTypeDef = TypedDict(
    "GetNetworkOutputTypeDef",
    {
        "Network": NetworkTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProposalOutputTypeDef = TypedDict(
    "GetProposalOutputTypeDef",
    {
        "Proposal": ProposalTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMemberConfigurationTypeDef = TypedDict(
    "_RequiredMemberConfigurationTypeDef",
    {
        "Name": str,
        "FrameworkConfiguration": MemberFrameworkConfigurationTypeDef,
    },
)
_OptionalMemberConfigurationTypeDef = TypedDict(
    "_OptionalMemberConfigurationTypeDef",
    {
        "Description": str,
        "LogPublishingConfiguration": MemberLogPublishingConfigurationTypeDef,
        "Tags": Mapping[str, str],
        "KmsKeyArn": str,
    },
    total=False,
)


class MemberConfigurationTypeDef(
    _RequiredMemberConfigurationTypeDef, _OptionalMemberConfigurationTypeDef
):
    pass


MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "NetworkId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "FrameworkAttributes": MemberFrameworkAttributesTypeDef,
        "LogPublishingConfiguration": MemberLogPublishingConfigurationTypeDef,
        "Status": MemberStatusType,
        "CreationDate": datetime,
        "Tags": Dict[str, str],
        "Arn": str,
        "KmsKeyArn": str,
    },
    total=False,
)

_RequiredUpdateMemberInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMemberInputRequestTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
    },
)
_OptionalUpdateMemberInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMemberInputRequestTypeDef",
    {
        "LogPublishingConfiguration": MemberLogPublishingConfigurationTypeDef,
    },
    total=False,
)


class UpdateMemberInputRequestTypeDef(
    _RequiredUpdateMemberInputRequestTypeDef, _OptionalUpdateMemberInputRequestTypeDef
):
    pass


_RequiredNodeConfigurationTypeDef = TypedDict(
    "_RequiredNodeConfigurationTypeDef",
    {
        "InstanceType": str,
    },
)
_OptionalNodeConfigurationTypeDef = TypedDict(
    "_OptionalNodeConfigurationTypeDef",
    {
        "AvailabilityZone": str,
        "LogPublishingConfiguration": NodeLogPublishingConfigurationTypeDef,
        "StateDB": StateDBTypeType,
    },
    total=False,
)


class NodeConfigurationTypeDef(
    _RequiredNodeConfigurationTypeDef, _OptionalNodeConfigurationTypeDef
):
    pass


NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "NetworkId": str,
        "MemberId": str,
        "Id": str,
        "InstanceType": str,
        "AvailabilityZone": str,
        "FrameworkAttributes": NodeFrameworkAttributesTypeDef,
        "LogPublishingConfiguration": NodeLogPublishingConfigurationTypeDef,
        "StateDB": StateDBTypeType,
        "Status": NodeStatusType,
        "CreationDate": datetime,
        "Tags": Dict[str, str],
        "Arn": str,
        "KmsKeyArn": str,
    },
    total=False,
)

_RequiredUpdateNodeInputRequestTypeDef = TypedDict(
    "_RequiredUpdateNodeInputRequestTypeDef",
    {
        "NetworkId": str,
        "NodeId": str,
    },
)
_OptionalUpdateNodeInputRequestTypeDef = TypedDict(
    "_OptionalUpdateNodeInputRequestTypeDef",
    {
        "MemberId": str,
        "LogPublishingConfiguration": NodeLogPublishingConfigurationTypeDef,
    },
    total=False,
)


class UpdateNodeInputRequestTypeDef(
    _RequiredUpdateNodeInputRequestTypeDef, _OptionalUpdateNodeInputRequestTypeDef
):
    pass


CreateMemberInputRequestTypeDef = TypedDict(
    "CreateMemberInputRequestTypeDef",
    {
        "ClientRequestToken": str,
        "InvitationId": str,
        "NetworkId": str,
        "MemberConfiguration": MemberConfigurationTypeDef,
    },
)

_RequiredCreateNetworkInputRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkInputRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Name": str,
        "Framework": FrameworkType,
        "FrameworkVersion": str,
        "VotingPolicy": VotingPolicyTypeDef,
        "MemberConfiguration": MemberConfigurationTypeDef,
    },
)
_OptionalCreateNetworkInputRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkInputRequestTypeDef",
    {
        "Description": str,
        "FrameworkConfiguration": NetworkFrameworkConfigurationTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateNetworkInputRequestTypeDef(
    _RequiredCreateNetworkInputRequestTypeDef, _OptionalCreateNetworkInputRequestTypeDef
):
    pass


GetMemberOutputTypeDef = TypedDict(
    "GetMemberOutputTypeDef",
    {
        "Member": MemberTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateNodeInputRequestTypeDef = TypedDict(
    "_RequiredCreateNodeInputRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NetworkId": str,
        "NodeConfiguration": NodeConfigurationTypeDef,
    },
)
_OptionalCreateNodeInputRequestTypeDef = TypedDict(
    "_OptionalCreateNodeInputRequestTypeDef",
    {
        "MemberId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateNodeInputRequestTypeDef(
    _RequiredCreateNodeInputRequestTypeDef, _OptionalCreateNodeInputRequestTypeDef
):
    pass


GetNodeOutputTypeDef = TypedDict(
    "GetNodeOutputTypeDef",
    {
        "Node": NodeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
