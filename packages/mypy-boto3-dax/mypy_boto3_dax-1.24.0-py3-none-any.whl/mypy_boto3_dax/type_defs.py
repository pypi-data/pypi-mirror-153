"""
Type annotations for dax service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dax/type_defs/)

Usage::

    ```python
    from mypy_boto3_dax.type_defs import EndpointTypeDef

    data: EndpointTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ChangeTypeType,
    ClusterEndpointEncryptionTypeType,
    IsModifiableType,
    ParameterTypeType,
    SourceTypeType,
    SSEStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EndpointTypeDef",
    "NotificationConfigurationTypeDef",
    "ParameterGroupStatusTypeDef",
    "SSEDescriptionTypeDef",
    "SecurityGroupMembershipTypeDef",
    "SSESpecificationTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateParameterGroupRequestRequestTypeDef",
    "ParameterGroupTypeDef",
    "CreateSubnetGroupRequestRequestTypeDef",
    "DecreaseReplicationFactorRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteParameterGroupRequestRequestTypeDef",
    "DeleteSubnetGroupRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeDefaultParametersRequestRequestTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "EventTypeDef",
    "DescribeParameterGroupsRequestRequestTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "DescribeSubnetGroupsRequestRequestTypeDef",
    "IncreaseReplicationFactorRequestRequestTypeDef",
    "ListTagsRequestRequestTypeDef",
    "NodeTypeSpecificValueTypeDef",
    "ParameterNameValueTypeDef",
    "RebootNodeRequestRequestTypeDef",
    "SubnetTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateSubnetGroupRequestRequestTypeDef",
    "NodeTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DeleteParameterGroupResponseTypeDef",
    "DeleteSubnetGroupResponseTypeDef",
    "ListTagsResponseTypeDef",
    "TagResourceResponseTypeDef",
    "UntagResourceResponseTypeDef",
    "CreateParameterGroupResponseTypeDef",
    "DescribeParameterGroupsResponseTypeDef",
    "UpdateParameterGroupResponseTypeDef",
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    "DescribeDefaultParametersRequestDescribeDefaultParametersPaginateTypeDef",
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    "DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef",
    "DescribeParametersRequestDescribeParametersPaginateTypeDef",
    "DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "DescribeEventsResponseTypeDef",
    "ParameterTypeDef",
    "UpdateParameterGroupRequestRequestTypeDef",
    "SubnetGroupTypeDef",
    "ClusterTypeDef",
    "DescribeDefaultParametersResponseTypeDef",
    "DescribeParametersResponseTypeDef",
    "CreateSubnetGroupResponseTypeDef",
    "DescribeSubnetGroupsResponseTypeDef",
    "UpdateSubnetGroupResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DecreaseReplicationFactorResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DescribeClustersResponseTypeDef",
    "IncreaseReplicationFactorResponseTypeDef",
    "RebootNodeResponseTypeDef",
    "UpdateClusterResponseTypeDef",
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "URL": str,
    },
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "TopicArn": str,
        "TopicStatus": str,
    },
    total=False,
)

ParameterGroupStatusTypeDef = TypedDict(
    "ParameterGroupStatusTypeDef",
    {
        "ParameterGroupName": str,
        "ParameterApplyStatus": str,
        "NodeIdsToReboot": List[str],
    },
    total=False,
)

SSEDescriptionTypeDef = TypedDict(
    "SSEDescriptionTypeDef",
    {
        "Status": SSEStatusType,
    },
    total=False,
)

SecurityGroupMembershipTypeDef = TypedDict(
    "SecurityGroupMembershipTypeDef",
    {
        "SecurityGroupIdentifier": str,
        "Status": str,
    },
    total=False,
)

SSESpecificationTypeDef = TypedDict(
    "SSESpecificationTypeDef",
    {
        "Enabled": bool,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

_RequiredCreateParameterGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalCreateParameterGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateParameterGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreateParameterGroupRequestRequestTypeDef(
    _RequiredCreateParameterGroupRequestRequestTypeDef,
    _OptionalCreateParameterGroupRequestRequestTypeDef,
):
    pass


ParameterGroupTypeDef = TypedDict(
    "ParameterGroupTypeDef",
    {
        "ParameterGroupName": str,
        "Description": str,
    },
    total=False,
)

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
    },
    total=False,
)


class CreateSubnetGroupRequestRequestTypeDef(
    _RequiredCreateSubnetGroupRequestRequestTypeDef, _OptionalCreateSubnetGroupRequestRequestTypeDef
):
    pass


_RequiredDecreaseReplicationFactorRequestRequestTypeDef = TypedDict(
    "_RequiredDecreaseReplicationFactorRequestRequestTypeDef",
    {
        "ClusterName": str,
        "NewReplicationFactor": int,
    },
)
_OptionalDecreaseReplicationFactorRequestRequestTypeDef = TypedDict(
    "_OptionalDecreaseReplicationFactorRequestRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "NodeIdsToRemove": Sequence[str],
    },
    total=False,
)


class DecreaseReplicationFactorRequestRequestTypeDef(
    _RequiredDecreaseReplicationFactorRequestRequestTypeDef,
    _OptionalDecreaseReplicationFactorRequestRequestTypeDef,
):
    pass


DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
    },
)

DeleteParameterGroupRequestRequestTypeDef = TypedDict(
    "DeleteParameterGroupRequestRequestTypeDef",
    {
        "ParameterGroupName": str,
    },
)

DeleteSubnetGroupRequestRequestTypeDef = TypedDict(
    "DeleteSubnetGroupRequestRequestTypeDef",
    {
        "SubnetGroupName": str,
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

DescribeClustersRequestRequestTypeDef = TypedDict(
    "DescribeClustersRequestRequestTypeDef",
    {
        "ClusterNames": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeDefaultParametersRequestRequestTypeDef = TypedDict(
    "DescribeDefaultParametersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
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
        "ParameterGroupNames": Sequence[str],
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
        "Source": str,
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


DescribeSubnetGroupsRequestRequestTypeDef = TypedDict(
    "DescribeSubnetGroupsRequestRequestTypeDef",
    {
        "SubnetGroupNames": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredIncreaseReplicationFactorRequestRequestTypeDef = TypedDict(
    "_RequiredIncreaseReplicationFactorRequestRequestTypeDef",
    {
        "ClusterName": str,
        "NewReplicationFactor": int,
    },
)
_OptionalIncreaseReplicationFactorRequestRequestTypeDef = TypedDict(
    "_OptionalIncreaseReplicationFactorRequestRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
    },
    total=False,
)


class IncreaseReplicationFactorRequestRequestTypeDef(
    _RequiredIncreaseReplicationFactorRequestRequestTypeDef,
    _OptionalIncreaseReplicationFactorRequestRequestTypeDef,
):
    pass


_RequiredListTagsRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsRequestRequestTypeDef",
    {
        "ResourceName": str,
    },
)
_OptionalListTagsRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTagsRequestRequestTypeDef(
    _RequiredListTagsRequestRequestTypeDef, _OptionalListTagsRequestRequestTypeDef
):
    pass


NodeTypeSpecificValueTypeDef = TypedDict(
    "NodeTypeSpecificValueTypeDef",
    {
        "NodeType": str,
        "Value": str,
    },
    total=False,
)

ParameterNameValueTypeDef = TypedDict(
    "ParameterNameValueTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
    },
    total=False,
)

RebootNodeRequestRequestTypeDef = TypedDict(
    "RebootNodeRequestRequestTypeDef",
    {
        "ClusterName": str,
        "NodeId": str,
    },
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceName": str,
        "TagKeys": Sequence[str],
    },
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
        "PreferredMaintenanceWindow": str,
        "NotificationTopicArn": str,
        "NotificationTopicStatus": str,
        "ParameterGroupName": str,
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)


class UpdateClusterRequestRequestTypeDef(
    _RequiredUpdateClusterRequestRequestTypeDef, _OptionalUpdateClusterRequestRequestTypeDef
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


NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "NodeId": str,
        "Endpoint": EndpointTypeDef,
        "NodeCreateTime": datetime,
        "AvailabilityZone": str,
        "NodeStatus": str,
        "ParameterGroupStatus": str,
    },
    total=False,
)

_RequiredCreateClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateClusterRequestRequestTypeDef",
    {
        "ClusterName": str,
        "NodeType": str,
        "ReplicationFactor": int,
        "IamRoleArn": str,
    },
)
_OptionalCreateClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateClusterRequestRequestTypeDef",
    {
        "Description": str,
        "AvailabilityZones": Sequence[str],
        "SubnetGroupName": str,
        "SecurityGroupIds": Sequence[str],
        "PreferredMaintenanceWindow": str,
        "NotificationTopicArn": str,
        "ParameterGroupName": str,
        "Tags": Sequence[TagTypeDef],
        "SSESpecification": SSESpecificationTypeDef,
        "ClusterEndpointEncryptionType": ClusterEndpointEncryptionTypeType,
    },
    total=False,
)


class CreateClusterRequestRequestTypeDef(
    _RequiredCreateClusterRequestRequestTypeDef, _OptionalCreateClusterRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

DeleteParameterGroupResponseTypeDef = TypedDict(
    "DeleteParameterGroupResponseTypeDef",
    {
        "DeletionMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSubnetGroupResponseTypeDef = TypedDict(
    "DeleteSubnetGroupResponseTypeDef",
    {
        "DeletionMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
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

DescribeParameterGroupsResponseTypeDef = TypedDict(
    "DescribeParameterGroupsResponseTypeDef",
    {
        "NextToken": str,
        "ParameterGroups": List[ParameterGroupTypeDef],
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

DescribeClustersRequestDescribeClustersPaginateTypeDef = TypedDict(
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    {
        "ClusterNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDefaultParametersRequestDescribeDefaultParametersPaginateTypeDef = TypedDict(
    "DescribeDefaultParametersRequestDescribeDefaultParametersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsRequestDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    {
        "SourceName": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef",
    {
        "ParameterGroupNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeParametersRequestDescribeParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeParametersRequestDescribeParametersPaginateTypeDef",
    {
        "ParameterGroupName": str,
    },
)
_OptionalDescribeParametersRequestDescribeParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeParametersRequestDescribeParametersPaginateTypeDef",
    {
        "Source": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeParametersRequestDescribeParametersPaginateTypeDef(
    _RequiredDescribeParametersRequestDescribeParametersPaginateTypeDef,
    _OptionalDescribeParametersRequestDescribeParametersPaginateTypeDef,
):
    pass


DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef",
    {
        "SubnetGroupNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_RequiredListTagsRequestListTagsPaginateTypeDef",
    {
        "ResourceName": str,
    },
)
_OptionalListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "_OptionalListTagsRequestListTagsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsRequestListTagsPaginateTypeDef(
    _RequiredListTagsRequestListTagsPaginateTypeDef, _OptionalListTagsRequestListTagsPaginateTypeDef
):
    pass


DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef",
    {
        "NextToken": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterType": ParameterTypeType,
        "ParameterValue": str,
        "NodeTypeSpecificValues": List[NodeTypeSpecificValueTypeDef],
        "Description": str,
        "Source": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": IsModifiableType,
        "ChangeType": ChangeTypeType,
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

SubnetGroupTypeDef = TypedDict(
    "SubnetGroupTypeDef",
    {
        "SubnetGroupName": str,
        "Description": str,
        "VpcId": str,
        "Subnets": List[SubnetTypeDef],
    },
    total=False,
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "ClusterName": str,
        "Description": str,
        "ClusterArn": str,
        "TotalNodes": int,
        "ActiveNodes": int,
        "NodeType": str,
        "Status": str,
        "ClusterDiscoveryEndpoint": EndpointTypeDef,
        "NodeIdsToRemove": List[str],
        "Nodes": List[NodeTypeDef],
        "PreferredMaintenanceWindow": str,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
        "SubnetGroup": str,
        "SecurityGroups": List[SecurityGroupMembershipTypeDef],
        "IamRoleArn": str,
        "ParameterGroup": ParameterGroupStatusTypeDef,
        "SSEDescription": SSEDescriptionTypeDef,
        "ClusterEndpointEncryptionType": ClusterEndpointEncryptionTypeType,
    },
    total=False,
)

DescribeDefaultParametersResponseTypeDef = TypedDict(
    "DescribeDefaultParametersResponseTypeDef",
    {
        "NextToken": str,
        "Parameters": List[ParameterTypeDef],
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

CreateSubnetGroupResponseTypeDef = TypedDict(
    "CreateSubnetGroupResponseTypeDef",
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

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DecreaseReplicationFactorResponseTypeDef = TypedDict(
    "DecreaseReplicationFactorResponseTypeDef",
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

IncreaseReplicationFactorResponseTypeDef = TypedDict(
    "IncreaseReplicationFactorResponseTypeDef",
    {
        "Cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootNodeResponseTypeDef = TypedDict(
    "RebootNodeResponseTypeDef",
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
