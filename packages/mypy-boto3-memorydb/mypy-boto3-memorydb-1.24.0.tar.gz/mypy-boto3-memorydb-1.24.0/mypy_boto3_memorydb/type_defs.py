"""
Type annotations for memorydb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/type_defs/)

Usage::

    ```python
    from mypy_boto3_memorydb.type_defs import ACLPendingChangesTypeDef

    data: ACLPendingChangesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import AuthenticationTypeType, AZStatusType, ServiceUpdateStatusType, SourceTypeType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ACLPendingChangesTypeDef",
    "ACLsUpdateStatusTypeDef",
    "AuthenticationModeTypeDef",
    "AuthenticationTypeDef",
    "AvailabilityZoneTypeDef",
    "ServiceUpdateRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UnprocessedClusterTypeDef",
    "PendingModifiedServiceUpdateTypeDef",
    "EndpointTypeDef",
    "SecurityGroupMembershipTypeDef",
    "TagTypeDef",
    "ParameterGroupTypeDef",
    "DeleteACLRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteParameterGroupRequestRequestTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSubnetGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeACLsRequestRequestTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeEngineVersionsRequestRequestTypeDef",
    "EngineVersionInfoTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "EventTypeDef",
    "DescribeParameterGroupsRequestRequestTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "ParameterTypeDef",
    "DescribeServiceUpdatesRequestRequestTypeDef",
    "ServiceUpdateTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeSubnetGroupsRequestRequestTypeDef",
    "FilterTypeDef",
    "FailoverShardRequestRequestTypeDef",
    "ListAllowedNodeTypeUpdatesRequestRequestTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ParameterNameValueTypeDef",
    "ReplicaConfigurationRequestTypeDef",
    "ResetParameterGroupRequestRequestTypeDef",
    "SlotMigrationTypeDef",
    "ShardConfigurationRequestTypeDef",
    "ShardConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateACLRequestRequestTypeDef",
    "UpdateSubnetGroupRequestRequestTypeDef",
    "ACLTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UserTypeDef",
    "SubnetTypeDef",
    "BatchUpdateClusterRequestRequestTypeDef",
    "ListAllowedNodeTypeUpdatesResponseTypeDef",
    "NodeTypeDef",
    "CopySnapshotRequestRequestTypeDef",
    "CreateACLRequestRequestTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateParameterGroupRequestRequestTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateSubnetGroupRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResponseTypeDef",
    "UntagResourceResponseTypeDef",
    "CreateParameterGroupResponseTypeDef",
    "DeleteParameterGroupResponseTypeDef",
    "DescribeParameterGroupsResponseTypeDef",
    "ResetParameterGroupResponseTypeDef",
    "UpdateParameterGroupResponseTypeDef",
    "DescribeEngineVersionsResponseTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeParametersResponseTypeDef",
    "DescribeServiceUpdatesResponseTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "UpdateParameterGroupRequestRequestTypeDef",
    "ReshardingStatusTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "ShardDetailTypeDef",
    "CreateACLResponseTypeDef",
    "DeleteACLResponseTypeDef",
    "DescribeACLsResponseTypeDef",
    "UpdateACLResponseTypeDef",
    "CreateUserResponseTypeDef",
    "DeleteUserResponseTypeDef",
    "DescribeUsersResponseTypeDef",
    "UpdateUserResponseTypeDef",
    "SubnetGroupTypeDef",
    "ShardTypeDef",
    "ClusterPendingUpdatesTypeDef",
    "ClusterConfigurationTypeDef",
    "CreateSubnetGroupResponseTypeDef",
    "DeleteSubnetGroupResponseTypeDef",
    "DescribeSubnetGroupsResponseTypeDef",
    "UpdateSubnetGroupResponseTypeDef",
    "ClusterTypeDef",
    "SnapshotTypeDef",
    "BatchUpdateClusterResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DescribeClustersResponseTypeDef",
    "FailoverShardResponseTypeDef",
    "UpdateClusterResponseTypeDef",
    "CopySnapshotResponseTypeDef",
    "CreateSnapshotResponseTypeDef",
    "DeleteSnapshotResponseTypeDef",
    "DescribeSnapshotsResponseTypeDef",
)

ACLPendingChangesTypeDef = TypedDict(
    "ACLPendingChangesTypeDef",
    {
        "UserNamesToRemove": List[str],
        "UserNamesToAdd": List[str],
    },
    total=False,
)

ACLsUpdateStatusTypeDef = TypedDict(
    "ACLsUpdateStatusTypeDef",
    {
        "ACLToApply": str,
    },
    total=False,
)

AuthenticationModeTypeDef = TypedDict(
    "AuthenticationModeTypeDef",
    {
        "Type": Literal["password"],
        "Passwords": Sequence[str],
    },
    total=False,
)

AuthenticationTypeDef = TypedDict(
    "AuthenticationTypeDef",
    {
        "Type": AuthenticationTypeType,
        "PasswordCount": int,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

ServiceUpdateRequestTypeDef = TypedDict(
    "ServiceUpdateRequestTypeDef",
    {
        "ServiceUpdateNameToApply": str,
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

UnprocessedClusterTypeDef = TypedDict(
    "UnprocessedClusterTypeDef",
    {
        "ClusterName": str,
        "ErrorType": str,
        "ErrorMessage": str,
    },
    total=False,
)

PendingModifiedServiceUpdateTypeDef = TypedDict(
    "PendingModifiedServiceUpdateTypeDef",
    {
        "ServiceUpdateName": str,
        "Status": ServiceUpdateStatusType,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
    },
    total=False,
)

SecurityGroupMembershipTypeDef = TypedDict(
    "SecurityGroupMembershipTypeDef",
    {
        "SecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ParameterGroupTypeDef = TypedDict(
    "ParameterGroupTypeDef",
    {
        "Name": str,
        "Family": str,
        "Description": str,
        "ARN": str,
    },
    total=False,
)

DeleteACLRequestRequestTypeDef = TypedDict(
    "DeleteACLRequestRequestTypeDef",
    {
        "ACLName": str,
    },
)

_RequiredDeleteClusterRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
    },
)
_OptionalDeleteClusterRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteClusterRequestRequestTypeDef",
    {
        "FinalSnapshotName": str,
    },
    total=False,
)


class DeleteClusterRequestRequestTypeDef(
    _RequiredDeleteClusterRequestRequestTypeDef, _OptionalDeleteClusterRequestRequestTypeDef
):
    pass


DeleteParameterGroupRequestRequestTypeDef = TypedDict(
    "DeleteParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)

DeleteSnapshotRequestRequestTypeDef = TypedDict(
    "DeleteSnapshotRequestRequestTypeDef",
    {
        "SnapshotName": str,
    },
)

DeleteSubnetGroupRequestRequestTypeDef = TypedDict(
    "DeleteSubnetGroupRequestRequestTypeDef",
    {
        "SubnetGroupName": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)

DescribeACLsRequestRequestTypeDef = TypedDict(
    "DescribeACLsRequestRequestTypeDef",
    {
        "ACLName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeClustersRequestRequestTypeDef = TypedDict(
    "DescribeClustersRequestRequestTypeDef",
    {
        "ClusterName": str,
        "MaxResults": int,
        "NextToken": str,
        "ShowShardDetails": bool,
    },
    total=False,
)

DescribeEngineVersionsRequestRequestTypeDef = TypedDict(
    "DescribeEngineVersionsRequestRequestTypeDef",
    {
        "EngineVersion": str,
        "ParameterGroupFamily": str,
        "MaxResults": int,
        "NextToken": str,
        "DefaultOnly": bool,
    },
    total=False,
)

EngineVersionInfoTypeDef = TypedDict(
    "EngineVersionInfoTypeDef",
    {
        "EngineVersion": str,
        "EnginePatchVersion": str,
        "ParameterGroupFamily": str,
    },
    total=False,
)

DescribeEventsRequestRequestTypeDef = TypedDict(
    "DescribeEventsRequestRequestTypeDef",
    {
        "SourceName": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceName": str,
        "SourceType": SourceTypeType,
        "Message": str,
        "Date": datetime,
    },
    total=False,
)

DescribeParameterGroupsRequestRequestTypeDef = TypedDict(
    "DescribeParameterGroupsRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeParametersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeParametersRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalDescribeParametersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeParametersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeParametersRequestRequestTypeDef(
    _RequiredDescribeParametersRequestRequestTypeDef,
    _OptionalDescribeParametersRequestRequestTypeDef,
):
    pass


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Name": str,
        "Value": str,
        "Description": str,
        "DataType": str,
        "AllowedValues": str,
        "MinimumEngineVersion": str,
    },
    total=False,
)

DescribeServiceUpdatesRequestRequestTypeDef = TypedDict(
    "DescribeServiceUpdatesRequestRequestTypeDef",
    {
        "ServiceUpdateName": str,
        "ClusterNames": Sequence[str],
        "Status": Sequence[ServiceUpdateStatusType],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ServiceUpdateTypeDef = TypedDict(
    "ServiceUpdateTypeDef",
    {
        "ClusterName": str,
        "ServiceUpdateName": str,
        "ReleaseDate": datetime,
        "Description": str,
        "Status": ServiceUpdateStatusType,
        "Type": Literal["security-update"],
        "NodesUpdated": str,
        "AutoUpdateStartDate": datetime,
    },
    total=False,
)

DescribeSnapshotsRequestRequestTypeDef = TypedDict(
    "DescribeSnapshotsRequestRequestTypeDef",
    {
        "ClusterName": str,
        "SnapshotName": str,
        "Source": str,
        "NextToken": str,
        "MaxResults": int,
        "ShowDetail": bool,
    },
    total=False,
)

DescribeSubnetGroupsRequestRequestTypeDef = TypedDict(
    "DescribeSubnetGroupsRequestRequestTypeDef",
    {
        "SubnetGroupName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

FailoverShardRequestRequestTypeDef = TypedDict(
    "FailoverShardRequestRequestTypeDef",
    {
        "ClusterName": str,
        "ShardName": str,
    },
)

ListAllowedNodeTypeUpdatesRequestRequestTypeDef = TypedDict(
    "ListAllowedNodeTypeUpdatesRequestRequestTypeDef",
    {
        "ClusterName": str,
    },
)

ListTagsRequestRequestTypeDef = TypedDict(
    "ListTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ParameterNameValueTypeDef = TypedDict(
    "ParameterNameValueTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
    },
    total=False,
)

ReplicaConfigurationRequestTypeDef = TypedDict(
    "ReplicaConfigurationRequestTypeDef",
    {
        "ReplicaCount": int,
    },
    total=False,
)

_RequiredResetParameterGroupRequestRequestTypeDef = TypedDict(
    "_RequiredResetParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalResetParameterGroupRequestRequestTypeDef = TypedDict(
    "_OptionalResetParameterGroupRequestRequestTypeDef",
    {
        "AllParameters": bool,
        "ParameterNames": Sequence[str],
    },
    total=False,
)


class ResetParameterGroupRequestRequestTypeDef(
    _RequiredResetParameterGroupRequestRequestTypeDef,
    _OptionalResetParameterGroupRequestRequestTypeDef,
):
    pass


SlotMigrationTypeDef = TypedDict(
    "SlotMigrationTypeDef",
    {
        "ProgressPercentage": float,
    },
    total=False,
)

ShardConfigurationRequestTypeDef = TypedDict(
    "ShardConfigurationRequestTypeDef",
    {
        "ShardCount": int,
    },
    total=False,
)

ShardConfigurationTypeDef = TypedDict(
    "ShardConfigurationTypeDef",
    {
        "Slots": str,
        "ReplicaCount": int,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateACLRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateACLRequestRequestTypeDef",
    {
        "ACLName": str,
    },
)
_OptionalUpdateACLRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateACLRequestRequestTypeDef",
    {
        "UserNamesToAdd": Sequence[str],
        "UserNamesToRemove": Sequence[str],
    },
    total=False,
)


class UpdateACLRequestRequestTypeDef(
    _RequiredUpdateACLRequestRequestTypeDef, _OptionalUpdateACLRequestRequestTypeDef
):
    pass


_RequiredUpdateSubnetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubnetGroupRequestRequestTypeDef",
    {
        "SubnetGroupName": str,
    },
)
_OptionalUpdateSubnetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubnetGroupRequestRequestTypeDef",
    {
        "Description": str,
        "SubnetIds": Sequence[str],
    },
    total=False,
)


class UpdateSubnetGroupRequestRequestTypeDef(
    _RequiredUpdateSubnetGroupRequestRequestTypeDef, _OptionalUpdateSubnetGroupRequestRequestTypeDef
):
    pass


ACLTypeDef = TypedDict(
    "ACLTypeDef",
    {
        "Name": str,
        "Status": str,
        "UserNames": List[str],
        "MinimumEngineVersion": str,
        "PendingChanges": ACLPendingChangesTypeDef,
        "Clusters": List[str],
        "ARN": str,
    },
    total=False,
)

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "UserName": str,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "AuthenticationMode": AuthenticationModeTypeDef,
        "AccessString": str,
    },
    total=False,
)


class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass


UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Name": str,
        "Status": str,
        "AccessString": str,
        "ACLNames": List[str],
        "MinimumEngineVersion": str,
        "Authentication": AuthenticationTypeDef,
        "ARN": str,
    },
    total=False,
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "Identifier": str,
        "AvailabilityZone": AvailabilityZoneTypeDef,
    },
    total=False,
)

_RequiredBatchUpdateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredBatchUpdateClusterRequestRequestTypeDef",
    {
        "ClusterNames": Sequence[str],
    },
)
_OptionalBatchUpdateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalBatchUpdateClusterRequestRequestTypeDef",
    {
        "ServiceUpdate": ServiceUpdateRequestTypeDef,
    },
    total=False,
)


class BatchUpdateClusterRequestRequestTypeDef(
    _RequiredBatchUpdateClusterRequestRequestTypeDef,
    _OptionalBatchUpdateClusterRequestRequestTypeDef,
):
    pass


ListAllowedNodeTypeUpdatesResponseTypeDef = TypedDict(
    "ListAllowedNodeTypeUpdatesResponseTypeDef",
    {
        "ScaleUpNodeTypes": List[str],
        "ScaleDownNodeTypes": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "Name": str,
        "Status": str,
        "AvailabilityZone": str,
        "CreateTime": datetime,
        "Endpoint": EndpointTypeDef,
    },
    total=False,
)

_RequiredCopySnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredCopySnapshotRequestRequestTypeDef",
    {
        "SourceSnapshotName": str,
        "TargetSnapshotName": str,
    },
)
_OptionalCopySnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalCopySnapshotRequestRequestTypeDef",
    {
        "TargetBucket": str,
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopySnapshotRequestRequestTypeDef(
    _RequiredCopySnapshotRequestRequestTypeDef, _OptionalCopySnapshotRequestRequestTypeDef
):
    pass


_RequiredCreateACLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateACLRequestRequestTypeDef",
    {
        "ACLName": str,
    },
)
_OptionalCreateACLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateACLRequestRequestTypeDef",
    {
        "UserNames": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateACLRequestRequestTypeDef(
    _RequiredCreateACLRequestRequestTypeDef, _OptionalCreateACLRequestRequestTypeDef
):
    pass


_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
        "NodeType": str,
        "ACLName": str,
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
        "Description": str,
        "NumShards": int,
        "NumReplicasPerShard": int,
        "SubnetGroupName": str,
        "SecurityGroupIds": Sequence[str],
        "MaintenanceWindow": str,
        "Port": int,
        "SnsTopicArn": str,
        "TLSEnabled": bool,
        "KmsKeyId": str,
        "SnapshotArns": Sequence[str],
        "SnapshotName": str,
        "SnapshotRetentionLimit": int,
        "Tags": Sequence[TagTypeDef],
        "SnapshotWindow": str,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
    },
    total=False,
)


class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
):
    pass


_RequiredCreateParameterGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
        "Family": str,
    },
)
_OptionalCreateParameterGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateParameterGroupRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateParameterGroupRequestRequestTypeDef(
    _RequiredCreateParameterGroupRequestRequestTypeDef,
    _OptionalCreateParameterGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSnapshotRequestRequestTypeDef",
    {
        "ClusterName": str,
        "SnapshotName": str,
    },
)
_OptionalCreateSnapshotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSnapshotRequestRequestTypeDef",
    {
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSnapshotRequestRequestTypeDef(
    _RequiredCreateSnapshotRequestRequestTypeDef, _OptionalCreateSnapshotRequestRequestTypeDef
):
    pass


_RequiredCreateSubnetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubnetGroupRequestRequestTypeDef",
    {
        "SubnetGroupName": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateSubnetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubnetGroupRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSubnetGroupRequestRequestTypeDef(
    _RequiredCreateSubnetGroupRequestRequestTypeDef, _OptionalCreateSubnetGroupRequestRequestTypeDef
):
    pass


_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationMode": AuthenticationModeTypeDef,
        "AccessString": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateParameterGroupResponseTypeDef = TypedDict(
    "CreateParameterGroupResponseTypeDef",
    {
        "ParameterGroup": ParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteParameterGroupResponseTypeDef = TypedDict(
    "DeleteParameterGroupResponseTypeDef",
    {
        "ParameterGroup": ParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeParameterGroupsResponseTypeDef = TypedDict(
    "DescribeParameterGroupsResponseTypeDef",
    {
        "NextToken": str,
        "ParameterGroups": List[ParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResetParameterGroupResponseTypeDef = TypedDict(
    "ResetParameterGroupResponseTypeDef",
    {
        "ParameterGroup": ParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateParameterGroupResponseTypeDef = TypedDict(
    "UpdateParameterGroupResponseTypeDef",
    {
        "ParameterGroup": ParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngineVersionsResponseTypeDef = TypedDict(
    "DescribeEngineVersionsResponseTypeDef",
    {
        "NextToken": str,
        "EngineVersions": List[EngineVersionInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef",
    {
        "NextToken": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeParametersResponseTypeDef = TypedDict(
    "DescribeParametersResponseTypeDef",
    {
        "NextToken": str,
        "Parameters": List[ParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeServiceUpdatesResponseTypeDef = TypedDict(
    "DescribeServiceUpdatesResponseTypeDef",
    {
        "NextToken": str,
        "ServiceUpdates": List[ServiceUpdateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUsersRequestRequestTypeDef = TypedDict(
    "DescribeUsersRequestRequestTypeDef",
    {
        "UserName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

UpdateParameterGroupRequestRequestTypeDef = TypedDict(
    "UpdateParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterNameValues": Sequence[ParameterNameValueTypeDef],
    },
)

ReshardingStatusTypeDef = TypedDict(
    "ReshardingStatusTypeDef",
    {
        "SlotMigration": SlotMigrationTypeDef,
    },
    total=False,
)

_RequiredUpdateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
    },
)
_OptionalUpdateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterRequestRequestTypeDef",
    {
        "Description": str,
        "SecurityGroupIds": Sequence[str],
        "MaintenanceWindow": str,
        "SnsTopicArn": str,
        "SnsTopicStatus": str,
        "ParameterGroupName": str,
        "SnapshotWindow": str,
        "SnapshotRetentionLimit": int,
        "NodeType": str,
        "EngineVersion": str,
        "ReplicaConfiguration": ReplicaConfigurationRequestTypeDef,
        "ShardConfiguration": ShardConfigurationRequestTypeDef,
        "ACLName": str,
    },
    total=False,
)


class UpdateClusterRequestRequestTypeDef(
    _RequiredUpdateClusterRequestRequestTypeDef, _OptionalUpdateClusterRequestRequestTypeDef
):
    pass


ShardDetailTypeDef = TypedDict(
    "ShardDetailTypeDef",
    {
        "Name": str,
        "Configuration": ShardConfigurationTypeDef,
        "Size": str,
        "SnapshotCreationTime": datetime,
    },
    total=False,
)

CreateACLResponseTypeDef = TypedDict(
    "CreateACLResponseTypeDef",
    {
        "ACL": ACLTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteACLResponseTypeDef = TypedDict(
    "DeleteACLResponseTypeDef",
    {
        "ACL": ACLTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeACLsResponseTypeDef = TypedDict(
    "DescribeACLsResponseTypeDef",
    {
        "ACLs": List[ACLTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateACLResponseTypeDef = TypedDict(
    "UpdateACLResponseTypeDef",
    {
        "ACL": ACLTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserResponseTypeDef = TypedDict(
    "DeleteUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUsersResponseTypeDef = TypedDict(
    "DescribeUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubnetGroupTypeDef = TypedDict(
    "SubnetGroupTypeDef",
    {
        "Name": str,
        "Description": str,
        "VpcId": str,
        "Subnets": List[SubnetTypeDef],
        "ARN": str,
    },
    total=False,
)

ShardTypeDef = TypedDict(
    "ShardTypeDef",
    {
        "Name": str,
        "Status": str,
        "Slots": str,
        "Nodes": List[NodeTypeDef],
        "NumberOfNodes": int,
    },
    total=False,
)

ClusterPendingUpdatesTypeDef = TypedDict(
    "ClusterPendingUpdatesTypeDef",
    {
        "Resharding": ReshardingStatusTypeDef,
        "ACLs": ACLsUpdateStatusTypeDef,
        "ServiceUpdates": List[PendingModifiedServiceUpdateTypeDef],
    },
    total=False,
)

ClusterConfigurationTypeDef = TypedDict(
    "ClusterConfigurationTypeDef",
    {
        "Name": str,
        "Description": str,
        "NodeType": str,
        "EngineVersion": str,
        "MaintenanceWindow": str,
        "TopicArn": str,
        "Port": int,
        "ParameterGroupName": str,
        "SubnetGroupName": str,
        "VpcId": str,
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "NumShards": int,
        "Shards": List[ShardDetailTypeDef],
    },
    total=False,
)

CreateSubnetGroupResponseTypeDef = TypedDict(
    "CreateSubnetGroupResponseTypeDef",
    {
        "SubnetGroup": SubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSubnetGroupResponseTypeDef = TypedDict(
    "DeleteSubnetGroupResponseTypeDef",
    {
        "SubnetGroup": SubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSubnetGroupsResponseTypeDef = TypedDict(
    "DescribeSubnetGroupsResponseTypeDef",
    {
        "NextToken": str,
        "SubnetGroups": List[SubnetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubnetGroupResponseTypeDef = TypedDict(
    "UpdateSubnetGroupResponseTypeDef",
    {
        "SubnetGroup": SubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "Name": str,
        "Description": str,
        "Status": str,
        "PendingUpdates": ClusterPendingUpdatesTypeDef,
        "NumberOfShards": int,
        "Shards": List[ShardTypeDef],
        "AvailabilityMode": AZStatusType,
        "ClusterEndpoint": EndpointTypeDef,
        "NodeType": str,
        "EngineVersion": str,
        "EnginePatchVersion": str,
        "ParameterGroupName": str,
        "ParameterGroupStatus": str,
        "SecurityGroups": List[SecurityGroupMembershipTypeDef],
        "SubnetGroupName": str,
        "TLSEnabled": bool,
        "KmsKeyId": str,
        "ARN": str,
        "SnsTopicArn": str,
        "SnsTopicStatus": str,
        "SnapshotRetentionLimit": int,
        "MaintenanceWindow": str,
        "SnapshotWindow": str,
        "ACLName": str,
        "AutoMinorVersionUpgrade": bool,
    },
    total=False,
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "Name": str,
        "Status": str,
        "Source": str,
        "KmsKeyId": str,
        "ARN": str,
        "ClusterConfiguration": ClusterConfigurationTypeDef,
    },
    total=False,
)

BatchUpdateClusterResponseTypeDef = TypedDict(
    "BatchUpdateClusterResponseTypeDef",
    {
        "ProcessedClusters": List[ClusterTypeDef],
        "UnprocessedClusters": List[UnprocessedClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClustersResponseTypeDef = TypedDict(
    "DescribeClustersResponseTypeDef",
    {
        "NextToken": str,
        "Clusters": List[ClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailoverShardResponseTypeDef = TypedDict(
    "FailoverShardResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterResponseTypeDef = TypedDict(
    "UpdateClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopySnapshotResponseTypeDef = TypedDict(
    "CopySnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotResponseTypeDef = TypedDict(
    "CreateSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSnapshotResponseTypeDef = TypedDict(
    "DeleteSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSnapshotsResponseTypeDef = TypedDict(
    "DescribeSnapshotsResponseTypeDef",
    {
        "NextToken": str,
        "Snapshots": List[SnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
