"""
Type annotations for memorydb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_memorydb.client import MemoryDBClient

    session = Session()
    client: MemoryDBClient = session.client("memorydb")
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import ServiceUpdateStatusType, SourceTypeType
from .type_defs import (
    AuthenticationModeTypeDef,
    BatchUpdateClusterResponseTypeDef,
    CopySnapshotResponseTypeDef,
    CreateACLResponseTypeDef,
    CreateClusterResponseTypeDef,
    CreateParameterGroupResponseTypeDef,
    CreateSnapshotResponseTypeDef,
    CreateSubnetGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    DeleteACLResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteParameterGroupResponseTypeDef,
    DeleteSnapshotResponseTypeDef,
    DeleteSubnetGroupResponseTypeDef,
    DeleteUserResponseTypeDef,
    DescribeACLsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeEngineVersionsResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeServiceUpdatesResponseTypeDef,
    DescribeSnapshotsResponseTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    DescribeUsersResponseTypeDef,
    FailoverShardResponseTypeDef,
    FilterTypeDef,
    ListAllowedNodeTypeUpdatesResponseTypeDef,
    ListTagsResponseTypeDef,
    ParameterNameValueTypeDef,
    ReplicaConfigurationRequestTypeDef,
    ResetParameterGroupResponseTypeDef,
    ServiceUpdateRequestTypeDef,
    ShardConfigurationRequestTypeDef,
    TagResourceResponseTypeDef,
    TagTypeDef,
    UntagResourceResponseTypeDef,
    UpdateACLResponseTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateParameterGroupResponseTypeDef,
    UpdateSubnetGroupResponseTypeDef,
    UpdateUserResponseTypeDef,
)

__all__ = ("MemoryDBClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ACLAlreadyExistsFault: Type[BotocoreClientError]
    ACLNotFoundFault: Type[BotocoreClientError]
    ACLQuotaExceededFault: Type[BotocoreClientError]
    APICallRateForCustomerExceededFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterAlreadyExistsFault: Type[BotocoreClientError]
    ClusterNotFoundFault: Type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: Type[BotocoreClientError]
    DefaultUserRequired: Type[BotocoreClientError]
    DuplicateUserNameFault: Type[BotocoreClientError]
    InsufficientClusterCapacityFault: Type[BotocoreClientError]
    InvalidACLStateFault: Type[BotocoreClientError]
    InvalidARNFault: Type[BotocoreClientError]
    InvalidClusterStateFault: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidKMSKeyFault: Type[BotocoreClientError]
    InvalidNodeStateFault: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterGroupStateFault: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidSnapshotStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidUserStateFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    NoOperationFault: Type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: Type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    ParameterGroupNotFoundFault: Type[BotocoreClientError]
    ParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: Type[BotocoreClientError]
    ServiceUpdateNotFoundFault: Type[BotocoreClientError]
    ShardNotFoundFault: Type[BotocoreClientError]
    ShardsPerClusterQuotaExceededFault: Type[BotocoreClientError]
    SnapshotAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotNotFoundFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    SubnetGroupInUseFault: Type[BotocoreClientError]
    SubnetGroupNotFoundFault: Type[BotocoreClientError]
    SubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    SubnetInUse: Type[BotocoreClientError]
    SubnetNotAllowedFault: Type[BotocoreClientError]
    SubnetQuotaExceededFault: Type[BotocoreClientError]
    TagNotFoundFault: Type[BotocoreClientError]
    TagQuotaPerResourceExceeded: Type[BotocoreClientError]
    TestFailoverNotAvailableFault: Type[BotocoreClientError]
    UserAlreadyExistsFault: Type[BotocoreClientError]
    UserNotFoundFault: Type[BotocoreClientError]
    UserQuotaExceededFault: Type[BotocoreClientError]


class MemoryDBClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MemoryDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#exceptions)
        """

    def batch_update_cluster(
        self, *, ClusterNames: Sequence[str], ServiceUpdate: ServiceUpdateRequestTypeDef = ...
    ) -> BatchUpdateClusterResponseTypeDef:
        """
        Apply the service update to a list of clusters supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.batch_update_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#batch_update_cluster)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#can_paginate)
        """

    def copy_snapshot(
        self,
        *,
        SourceSnapshotName: str,
        TargetSnapshotName: str,
        TargetBucket: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CopySnapshotResponseTypeDef:
        """
        Makes a copy of an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.copy_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#copy_snapshot)
        """

    def create_acl(
        self, *, ACLName: str, UserNames: Sequence[str] = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> CreateACLResponseTypeDef:
        """
        Creates an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_acl)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_acl)
        """

    def create_cluster(
        self,
        *,
        ClusterName: str,
        NodeType: str,
        ACLName: str,
        ParameterGroupName: str = ...,
        Description: str = ...,
        NumShards: int = ...,
        NumReplicasPerShard: int = ...,
        SubnetGroupName: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        MaintenanceWindow: str = ...,
        Port: int = ...,
        SnsTopicArn: str = ...,
        TLSEnabled: bool = ...,
        KmsKeyId: str = ...,
        SnapshotArns: Sequence[str] = ...,
        SnapshotName: str = ...,
        SnapshotRetentionLimit: int = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SnapshotWindow: str = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_cluster)
        """

    def create_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        Family: str,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateParameterGroupResponseTypeDef:
        """
        Creates a new MemoryDB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_parameter_group)
        """

    def create_snapshot(
        self,
        *,
        ClusterName: str,
        SnapshotName: str,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateSnapshotResponseTypeDef:
        """
        Creates a copy of an entire cluster at a specific moment in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_snapshot)
        """

    def create_subnet_group(
        self,
        *,
        SubnetGroupName: str,
        SubnetIds: Sequence[str],
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateSubnetGroupResponseTypeDef:
        """
        Creates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_subnet_group)
        """

    def create_user(
        self,
        *,
        UserName: str,
        AuthenticationMode: AuthenticationModeTypeDef,
        AccessString: str,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a MemoryDB user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#create_user)
        """

    def delete_acl(self, *, ACLName: str) -> DeleteACLResponseTypeDef:
        """
        Deletes an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_acl)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_acl)
        """

    def delete_cluster(
        self, *, ClusterName: str, FinalSnapshotName: str = ...
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_cluster)
        """

    def delete_parameter_group(
        self, *, ParameterGroupName: str
    ) -> DeleteParameterGroupResponseTypeDef:
        """
        Deletes the specified parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_parameter_group)
        """

    def delete_snapshot(self, *, SnapshotName: str) -> DeleteSnapshotResponseTypeDef:
        """
        Deletes an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_snapshot)
        """

    def delete_subnet_group(self, *, SubnetGroupName: str) -> DeleteSubnetGroupResponseTypeDef:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_subnet_group)
        """

    def delete_user(self, *, UserName: str) -> DeleteUserResponseTypeDef:
        """
        Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#delete_user)
        """

    def describe_acls(
        self, *, ACLName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeACLsResponseTypeDef:
        """
        Returns a list of ACLs See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/DescribeACLs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_acls)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_acls)
        """

    def describe_clusters(
        self,
        *,
        ClusterName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ShowShardDetails: bool = ...
    ) -> DescribeClustersResponseTypeDef:
        """
        Returns information about all provisioned clusters if no cluster identifier is
        specified, or about a specific cluster if a cluster name is supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_clusters)
        """

    def describe_engine_versions(
        self,
        *,
        EngineVersion: str = ...,
        ParameterGroupFamily: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        DefaultOnly: bool = ...
    ) -> DescribeEngineVersionsResponseTypeDef:
        """
        Returns a list of the available Redis engine versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_engine_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_engine_versions)
        """

    def describe_events(
        self,
        *,
        SourceName: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns events related to clusters, security groups, and parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_events)
        """

    def describe_parameter_groups(
        self, *, ParameterGroupName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeParameterGroupsResponseTypeDef:
        """
        Returns a list of parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_parameter_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_parameter_groups)
        """

    def describe_parameters(
        self, *, ParameterGroupName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeParametersResponseTypeDef:
        """
        Returns the detailed parameter list for a particular parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_parameters)
        """

    def describe_service_updates(
        self,
        *,
        ServiceUpdateName: str = ...,
        ClusterNames: Sequence[str] = ...,
        Status: Sequence[ServiceUpdateStatusType] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeServiceUpdatesResponseTypeDef:
        """
        Returns details of the service updates See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/DescribeServiceUpdates).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_service_updates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_service_updates)
        """

    def describe_snapshots(
        self,
        *,
        ClusterName: str = ...,
        SnapshotName: str = ...,
        Source: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ShowDetail: bool = ...
    ) -> DescribeSnapshotsResponseTypeDef:
        """
        Returns information about cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_snapshots)
        """

    def describe_subnet_groups(
        self, *, SubnetGroupName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeSubnetGroupsResponseTypeDef:
        """
        Returns a list of subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_subnet_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_subnet_groups)
        """

    def describe_users(
        self,
        *,
        UserName: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeUsersResponseTypeDef:
        """
        Returns a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#describe_users)
        """

    def failover_shard(self, *, ClusterName: str, ShardName: str) -> FailoverShardResponseTypeDef:
        """
        Used to failover a shard See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/FailoverShard).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.failover_shard)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#failover_shard)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#generate_presigned_url)
        """

    def list_allowed_node_type_updates(
        self, *, ClusterName: str
    ) -> ListAllowedNodeTypeUpdatesResponseTypeDef:
        """
        Lists all available node types that you can scale to from your cluster's current
        node type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.list_allowed_node_type_updates)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#list_allowed_node_type_updates)
        """

    def list_tags(self, *, ResourceArn: str) -> ListTagsResponseTypeDef:
        """
        Lists all tags currently on a named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#list_tags)
        """

    def reset_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        AllParameters: bool = ...,
        ParameterNames: Sequence[str] = ...
    ) -> ResetParameterGroupResponseTypeDef:
        """
        Modifies the parameters of a parameter group to the engine or system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.reset_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#reset_parameter_group)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> TagResourceResponseTypeDef:
        """
        A tag is a key-value pair where the key and value are case-sensitive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> UntagResourceResponseTypeDef:
        """
        Use this operation to remove tags on a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#untag_resource)
        """

    def update_acl(
        self,
        *,
        ACLName: str,
        UserNamesToAdd: Sequence[str] = ...,
        UserNamesToRemove: Sequence[str] = ...
    ) -> UpdateACLResponseTypeDef:
        """
        Changes the list of users that belong to the Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_acl)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#update_acl)
        """

    def update_cluster(
        self,
        *,
        ClusterName: str,
        Description: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        MaintenanceWindow: str = ...,
        SnsTopicArn: str = ...,
        SnsTopicStatus: str = ...,
        ParameterGroupName: str = ...,
        SnapshotWindow: str = ...,
        SnapshotRetentionLimit: int = ...,
        NodeType: str = ...,
        EngineVersion: str = ...,
        ReplicaConfiguration: ReplicaConfigurationRequestTypeDef = ...,
        ShardConfiguration: ShardConfigurationRequestTypeDef = ...,
        ACLName: str = ...
    ) -> UpdateClusterResponseTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#update_cluster)
        """

    def update_parameter_group(
        self, *, ParameterGroupName: str, ParameterNameValues: Sequence[ParameterNameValueTypeDef]
    ) -> UpdateParameterGroupResponseTypeDef:
        """
        Updates the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#update_parameter_group)
        """

    def update_subnet_group(
        self, *, SubnetGroupName: str, Description: str = ..., SubnetIds: Sequence[str] = ...
    ) -> UpdateSubnetGroupResponseTypeDef:
        """
        Updates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#update_subnet_group)
        """

    def update_user(
        self,
        *,
        UserName: str,
        AuthenticationMode: AuthenticationModeTypeDef = ...,
        AccessString: str = ...
    ) -> UpdateUserResponseTypeDef:
        """
        Changes user password(s) and/or access string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_memorydb/client/#update_user)
        """
