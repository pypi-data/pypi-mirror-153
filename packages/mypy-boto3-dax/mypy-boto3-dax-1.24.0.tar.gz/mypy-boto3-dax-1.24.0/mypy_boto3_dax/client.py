"""
Type annotations for dax service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dax.client import DAXClient

    session = Session()
    client: DAXClient = session.client("dax")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ClusterEndpointEncryptionTypeType, SourceTypeType
from .paginator import (
    DescribeClustersPaginator,
    DescribeDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeParameterGroupsPaginator,
    DescribeParametersPaginator,
    DescribeSubnetGroupsPaginator,
    ListTagsPaginator,
)
from .type_defs import (
    CreateClusterResponseTypeDef,
    CreateParameterGroupResponseTypeDef,
    CreateSubnetGroupResponseTypeDef,
    DecreaseReplicationFactorResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteParameterGroupResponseTypeDef,
    DeleteSubnetGroupResponseTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeDefaultParametersResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    IncreaseReplicationFactorResponseTypeDef,
    ListTagsResponseTypeDef,
    ParameterNameValueTypeDef,
    RebootNodeResponseTypeDef,
    SSESpecificationTypeDef,
    TagResourceResponseTypeDef,
    TagTypeDef,
    UntagResourceResponseTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateParameterGroupResponseTypeDef,
    UpdateSubnetGroupResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DAXClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClusterAlreadyExistsFault: Type[BotocoreClientError]
    ClusterNotFoundFault: Type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: Type[BotocoreClientError]
    InsufficientClusterCapacityFault: Type[BotocoreClientError]
    InvalidARNFault: Type[BotocoreClientError]
    InvalidClusterStateFault: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterGroupStateFault: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    NodeNotFoundFault: Type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: Type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    ParameterGroupNotFoundFault: Type[BotocoreClientError]
    ParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    SubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    SubnetGroupInUseFault: Type[BotocoreClientError]
    SubnetGroupNotFoundFault: Type[BotocoreClientError]
    SubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    SubnetInUse: Type[BotocoreClientError]
    SubnetQuotaExceededFault: Type[BotocoreClientError]
    TagNotFoundFault: Type[BotocoreClientError]
    TagQuotaPerResourceExceeded: Type[BotocoreClientError]


class DAXClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DAXClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#can_paginate)
        """

    def create_cluster(
        self,
        *,
        ClusterName: str,
        NodeType: str,
        ReplicationFactor: int,
        IamRoleArn: str,
        Description: str = ...,
        AvailabilityZones: Sequence[str] = ...,
        SubnetGroupName: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        PreferredMaintenanceWindow: str = ...,
        NotificationTopicArn: str = ...,
        ParameterGroupName: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SSESpecification: SSESpecificationTypeDef = ...,
        ClusterEndpointEncryptionType: ClusterEndpointEncryptionTypeType = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.create_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#create_cluster)
        """

    def create_parameter_group(
        self, *, ParameterGroupName: str, Description: str = ...
    ) -> CreateParameterGroupResponseTypeDef:
        """
        Creates a new parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.create_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#create_parameter_group)
        """

    def create_subnet_group(
        self, *, SubnetGroupName: str, SubnetIds: Sequence[str], Description: str = ...
    ) -> CreateSubnetGroupResponseTypeDef:
        """
        Creates a new subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.create_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#create_subnet_group)
        """

    def decrease_replication_factor(
        self,
        *,
        ClusterName: str,
        NewReplicationFactor: int,
        AvailabilityZones: Sequence[str] = ...,
        NodeIdsToRemove: Sequence[str] = ...
    ) -> DecreaseReplicationFactorResponseTypeDef:
        """
        Removes one or more nodes from a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.decrease_replication_factor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#decrease_replication_factor)
        """

    def delete_cluster(self, *, ClusterName: str) -> DeleteClusterResponseTypeDef:
        """
        Deletes a previously provisioned DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.delete_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#delete_cluster)
        """

    def delete_parameter_group(
        self, *, ParameterGroupName: str
    ) -> DeleteParameterGroupResponseTypeDef:
        """
        Deletes the specified parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.delete_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#delete_parameter_group)
        """

    def delete_subnet_group(self, *, SubnetGroupName: str) -> DeleteSubnetGroupResponseTypeDef:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.delete_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#delete_subnet_group)
        """

    def describe_clusters(
        self, *, ClusterNames: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeClustersResponseTypeDef:
        """
        Returns information about all provisioned DAX clusters if no cluster identifier
        is specified, or about a specific DAX cluster if a cluster identifier is
        supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_clusters)
        """

    def describe_default_parameters(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDefaultParametersResponseTypeDef:
        """
        Returns the default system parameter information for the DAX caching software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_default_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_default_parameters)
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
        Returns events related to DAX clusters and parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_events)
        """

    def describe_parameter_groups(
        self,
        *,
        ParameterGroupNames: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeParameterGroupsResponseTypeDef:
        """
        Returns a list of parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_parameter_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_parameter_groups)
        """

    def describe_parameters(
        self,
        *,
        ParameterGroupName: str,
        Source: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeParametersResponseTypeDef:
        """
        Returns the detailed parameter list for a particular parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_parameters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_parameters)
        """

    def describe_subnet_groups(
        self, *, SubnetGroupNames: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeSubnetGroupsResponseTypeDef:
        """
        Returns a list of subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.describe_subnet_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#describe_subnet_groups)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#generate_presigned_url)
        """

    def increase_replication_factor(
        self, *, ClusterName: str, NewReplicationFactor: int, AvailabilityZones: Sequence[str] = ...
    ) -> IncreaseReplicationFactorResponseTypeDef:
        """
        Adds one or more nodes to a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.increase_replication_factor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#increase_replication_factor)
        """

    def list_tags(self, *, ResourceName: str, NextToken: str = ...) -> ListTagsResponseTypeDef:
        """
        List all of the tags for a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#list_tags)
        """

    def reboot_node(self, *, ClusterName: str, NodeId: str) -> RebootNodeResponseTypeDef:
        """
        Reboots a single node of a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.reboot_node)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#reboot_node)
        """

    def tag_resource(
        self, *, ResourceName: str, Tags: Sequence[TagTypeDef]
    ) -> TagResourceResponseTypeDef:
        """
        Associates a set of tags with a DAX resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceName: str, TagKeys: Sequence[str]
    ) -> UntagResourceResponseTypeDef:
        """
        Removes the association of tags from a DAX resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#untag_resource)
        """

    def update_cluster(
        self,
        *,
        ClusterName: str,
        Description: str = ...,
        PreferredMaintenanceWindow: str = ...,
        NotificationTopicArn: str = ...,
        NotificationTopicStatus: str = ...,
        ParameterGroupName: str = ...,
        SecurityGroupIds: Sequence[str] = ...
    ) -> UpdateClusterResponseTypeDef:
        """
        Modifies the settings for a DAX cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.update_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#update_cluster)
        """

    def update_parameter_group(
        self, *, ParameterGroupName: str, ParameterNameValues: Sequence[ParameterNameValueTypeDef]
    ) -> UpdateParameterGroupResponseTypeDef:
        """
        Modifies the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.update_parameter_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#update_parameter_group)
        """

    def update_subnet_group(
        self, *, SubnetGroupName: str, Description: str = ..., SubnetIds: Sequence[str] = ...
    ) -> UpdateSubnetGroupResponseTypeDef:
        """
        Modifies an existing subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.update_subnet_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#update_subnet_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_clusters"]
    ) -> DescribeClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_default_parameters"]
    ) -> DescribeDefaultParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_parameter_groups"]
    ) -> DescribeParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_parameters"]
    ) -> DescribeParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subnet_groups"]
    ) -> DescribeSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/client/#get_paginator)
        """
