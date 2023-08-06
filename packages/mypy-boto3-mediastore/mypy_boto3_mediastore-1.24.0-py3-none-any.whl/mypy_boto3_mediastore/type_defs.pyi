"""
Type annotations for mediastore service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediastore.type_defs import ContainerTypeDef

    data: ContainerTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import ContainerLevelMetricsType, ContainerStatusType, MethodNameType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ContainerTypeDef",
    "CorsRuleTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteContainerInputRequestTypeDef",
    "DeleteContainerPolicyInputRequestTypeDef",
    "DeleteCorsPolicyInputRequestTypeDef",
    "DeleteLifecyclePolicyInputRequestTypeDef",
    "DeleteMetricPolicyInputRequestTypeDef",
    "DescribeContainerInputRequestTypeDef",
    "GetContainerPolicyInputRequestTypeDef",
    "GetCorsPolicyInputRequestTypeDef",
    "GetLifecyclePolicyInputRequestTypeDef",
    "GetMetricPolicyInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListContainersInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "MetricPolicyRuleTypeDef",
    "PutContainerPolicyInputRequestTypeDef",
    "PutLifecyclePolicyInputRequestTypeDef",
    "StartAccessLoggingInputRequestTypeDef",
    "StopAccessLoggingInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "PutCorsPolicyInputRequestTypeDef",
    "CreateContainerInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "CreateContainerOutputTypeDef",
    "DescribeContainerOutputTypeDef",
    "GetContainerPolicyOutputTypeDef",
    "GetCorsPolicyOutputTypeDef",
    "GetLifecyclePolicyOutputTypeDef",
    "ListContainersOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListContainersInputListContainersPaginateTypeDef",
    "MetricPolicyTypeDef",
    "GetMetricPolicyOutputTypeDef",
    "PutMetricPolicyInputRequestTypeDef",
)

ContainerTypeDef = TypedDict(
    "ContainerTypeDef",
    {
        "Endpoint": str,
        "CreationTime": datetime,
        "ARN": str,
        "Name": str,
        "Status": ContainerStatusType,
        "AccessLoggingEnabled": bool,
    },
    total=False,
)

_RequiredCorsRuleTypeDef = TypedDict(
    "_RequiredCorsRuleTypeDef",
    {
        "AllowedOrigins": List[str],
        "AllowedHeaders": List[str],
    },
)
_OptionalCorsRuleTypeDef = TypedDict(
    "_OptionalCorsRuleTypeDef",
    {
        "AllowedMethods": List[MethodNameType],
        "MaxAgeSeconds": int,
        "ExposeHeaders": List[str],
    },
    total=False,
)

class CorsRuleTypeDef(_RequiredCorsRuleTypeDef, _OptionalCorsRuleTypeDef):
    pass

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)

class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
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

DeleteContainerInputRequestTypeDef = TypedDict(
    "DeleteContainerInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

DeleteContainerPolicyInputRequestTypeDef = TypedDict(
    "DeleteContainerPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

DeleteCorsPolicyInputRequestTypeDef = TypedDict(
    "DeleteCorsPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

DeleteLifecyclePolicyInputRequestTypeDef = TypedDict(
    "DeleteLifecyclePolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

DeleteMetricPolicyInputRequestTypeDef = TypedDict(
    "DeleteMetricPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

DescribeContainerInputRequestTypeDef = TypedDict(
    "DescribeContainerInputRequestTypeDef",
    {
        "ContainerName": str,
    },
    total=False,
)

GetContainerPolicyInputRequestTypeDef = TypedDict(
    "GetContainerPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

GetCorsPolicyInputRequestTypeDef = TypedDict(
    "GetCorsPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

GetLifecyclePolicyInputRequestTypeDef = TypedDict(
    "GetLifecyclePolicyInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

GetMetricPolicyInputRequestTypeDef = TypedDict(
    "GetMetricPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
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

ListContainersInputRequestTypeDef = TypedDict(
    "ListContainersInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "Resource": str,
    },
)

MetricPolicyRuleTypeDef = TypedDict(
    "MetricPolicyRuleTypeDef",
    {
        "ObjectGroup": str,
        "ObjectGroupName": str,
    },
)

PutContainerPolicyInputRequestTypeDef = TypedDict(
    "PutContainerPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
        "Policy": str,
    },
)

PutLifecyclePolicyInputRequestTypeDef = TypedDict(
    "PutLifecyclePolicyInputRequestTypeDef",
    {
        "ContainerName": str,
        "LifecyclePolicy": str,
    },
)

StartAccessLoggingInputRequestTypeDef = TypedDict(
    "StartAccessLoggingInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

StopAccessLoggingInputRequestTypeDef = TypedDict(
    "StopAccessLoggingInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "Resource": str,
        "TagKeys": Sequence[str],
    },
)

PutCorsPolicyInputRequestTypeDef = TypedDict(
    "PutCorsPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
        "CorsPolicy": Sequence[CorsRuleTypeDef],
    },
)

_RequiredCreateContainerInputRequestTypeDef = TypedDict(
    "_RequiredCreateContainerInputRequestTypeDef",
    {
        "ContainerName": str,
    },
)
_OptionalCreateContainerInputRequestTypeDef = TypedDict(
    "_OptionalCreateContainerInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateContainerInputRequestTypeDef(
    _RequiredCreateContainerInputRequestTypeDef, _OptionalCreateContainerInputRequestTypeDef
):
    pass

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "Resource": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateContainerOutputTypeDef = TypedDict(
    "CreateContainerOutputTypeDef",
    {
        "Container": ContainerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeContainerOutputTypeDef = TypedDict(
    "DescribeContainerOutputTypeDef",
    {
        "Container": ContainerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContainerPolicyOutputTypeDef = TypedDict(
    "GetContainerPolicyOutputTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCorsPolicyOutputTypeDef = TypedDict(
    "GetCorsPolicyOutputTypeDef",
    {
        "CorsPolicy": List[CorsRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLifecyclePolicyOutputTypeDef = TypedDict(
    "GetLifecyclePolicyOutputTypeDef",
    {
        "LifecyclePolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContainersOutputTypeDef = TypedDict(
    "ListContainersOutputTypeDef",
    {
        "Containers": List[ContainerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContainersInputListContainersPaginateTypeDef = TypedDict(
    "ListContainersInputListContainersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredMetricPolicyTypeDef = TypedDict(
    "_RequiredMetricPolicyTypeDef",
    {
        "ContainerLevelMetrics": ContainerLevelMetricsType,
    },
)
_OptionalMetricPolicyTypeDef = TypedDict(
    "_OptionalMetricPolicyTypeDef",
    {
        "MetricPolicyRules": List[MetricPolicyRuleTypeDef],
    },
    total=False,
)

class MetricPolicyTypeDef(_RequiredMetricPolicyTypeDef, _OptionalMetricPolicyTypeDef):
    pass

GetMetricPolicyOutputTypeDef = TypedDict(
    "GetMetricPolicyOutputTypeDef",
    {
        "MetricPolicy": MetricPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMetricPolicyInputRequestTypeDef = TypedDict(
    "PutMetricPolicyInputRequestTypeDef",
    {
        "ContainerName": str,
        "MetricPolicy": MetricPolicyTypeDef,
    },
)
