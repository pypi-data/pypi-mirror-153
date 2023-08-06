"""
Type annotations for autoscaling-plans service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/type_defs/)

Usage::

    ```python
    from mypy_boto3_autoscaling_plans.type_defs import TagFilterTypeDef

    data: TagFilterTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ForecastDataTypeType,
    LoadMetricTypeType,
    MetricStatisticType,
    PredictiveScalingMaxCapacityBehaviorType,
    PredictiveScalingModeType,
    ScalableDimensionType,
    ScalingMetricTypeType,
    ScalingPlanStatusCodeType,
    ScalingPolicyUpdateBehaviorType,
    ScalingStatusCodeType,
    ServiceNamespaceType,
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
    "TagFilterTypeDef",
    "ResponseMetadataTypeDef",
    "MetricDimensionTypeDef",
    "DatapointTypeDef",
    "DeleteScalingPlanRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeScalingPlanResourcesRequestRequestTypeDef",
    "GetScalingPlanResourceForecastDataRequestRequestTypeDef",
    "PredefinedLoadMetricSpecificationTypeDef",
    "PredefinedScalingMetricSpecificationTypeDef",
    "ApplicationSourceTypeDef",
    "CreateScalingPlanResponseTypeDef",
    "CustomizedLoadMetricSpecificationTypeDef",
    "CustomizedScalingMetricSpecificationTypeDef",
    "GetScalingPlanResourceForecastDataResponseTypeDef",
    "DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef",
    "DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef",
    "DescribeScalingPlansRequestRequestTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "ScalingInstructionTypeDef",
    "ScalingPolicyTypeDef",
    "CreateScalingPlanRequestRequestTypeDef",
    "ScalingPlanTypeDef",
    "UpdateScalingPlanRequestRequestTypeDef",
    "ScalingPlanResourceTypeDef",
    "DescribeScalingPlansResponseTypeDef",
    "DescribeScalingPlanResourcesResponseTypeDef",
)

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
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

MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

DatapointTypeDef = TypedDict(
    "DatapointTypeDef",
    {
        "Timestamp": datetime,
        "Value": float,
    },
    total=False,
)

DeleteScalingPlanRequestRequestTypeDef = TypedDict(
    "DeleteScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
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

_RequiredDescribeScalingPlanResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeScalingPlanResourcesRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
    },
)
_OptionalDescribeScalingPlanResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeScalingPlanResourcesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeScalingPlanResourcesRequestRequestTypeDef(
    _RequiredDescribeScalingPlanResourcesRequestRequestTypeDef,
    _OptionalDescribeScalingPlanResourcesRequestRequestTypeDef,
):
    pass


GetScalingPlanResourceForecastDataRequestRequestTypeDef = TypedDict(
    "GetScalingPlanResourceForecastDataRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "ForecastDataType": ForecastDataTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)

_RequiredPredefinedLoadMetricSpecificationTypeDef = TypedDict(
    "_RequiredPredefinedLoadMetricSpecificationTypeDef",
    {
        "PredefinedLoadMetricType": LoadMetricTypeType,
    },
)
_OptionalPredefinedLoadMetricSpecificationTypeDef = TypedDict(
    "_OptionalPredefinedLoadMetricSpecificationTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredefinedLoadMetricSpecificationTypeDef(
    _RequiredPredefinedLoadMetricSpecificationTypeDef,
    _OptionalPredefinedLoadMetricSpecificationTypeDef,
):
    pass


_RequiredPredefinedScalingMetricSpecificationTypeDef = TypedDict(
    "_RequiredPredefinedScalingMetricSpecificationTypeDef",
    {
        "PredefinedScalingMetricType": ScalingMetricTypeType,
    },
)
_OptionalPredefinedScalingMetricSpecificationTypeDef = TypedDict(
    "_OptionalPredefinedScalingMetricSpecificationTypeDef",
    {
        "ResourceLabel": str,
    },
    total=False,
)


class PredefinedScalingMetricSpecificationTypeDef(
    _RequiredPredefinedScalingMetricSpecificationTypeDef,
    _OptionalPredefinedScalingMetricSpecificationTypeDef,
):
    pass


ApplicationSourceTypeDef = TypedDict(
    "ApplicationSourceTypeDef",
    {
        "CloudFormationStackARN": str,
        "TagFilters": Sequence[TagFilterTypeDef],
    },
    total=False,
)

CreateScalingPlanResponseTypeDef = TypedDict(
    "CreateScalingPlanResponseTypeDef",
    {
        "ScalingPlanVersion": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCustomizedLoadMetricSpecificationTypeDef = TypedDict(
    "_RequiredCustomizedLoadMetricSpecificationTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
    },
)
_OptionalCustomizedLoadMetricSpecificationTypeDef = TypedDict(
    "_OptionalCustomizedLoadMetricSpecificationTypeDef",
    {
        "Dimensions": Sequence[MetricDimensionTypeDef],
        "Unit": str,
    },
    total=False,
)


class CustomizedLoadMetricSpecificationTypeDef(
    _RequiredCustomizedLoadMetricSpecificationTypeDef,
    _OptionalCustomizedLoadMetricSpecificationTypeDef,
):
    pass


_RequiredCustomizedScalingMetricSpecificationTypeDef = TypedDict(
    "_RequiredCustomizedScalingMetricSpecificationTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
    },
)
_OptionalCustomizedScalingMetricSpecificationTypeDef = TypedDict(
    "_OptionalCustomizedScalingMetricSpecificationTypeDef",
    {
        "Dimensions": Sequence[MetricDimensionTypeDef],
        "Unit": str,
    },
    total=False,
)


class CustomizedScalingMetricSpecificationTypeDef(
    _RequiredCustomizedScalingMetricSpecificationTypeDef,
    _OptionalCustomizedScalingMetricSpecificationTypeDef,
):
    pass


GetScalingPlanResourceForecastDataResponseTypeDef = TypedDict(
    "GetScalingPlanResourceForecastDataResponseTypeDef",
    {
        "Datapoints": List[DatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef = TypedDict(
    "_RequiredDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
    },
)
_OptionalDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef = TypedDict(
    "_OptionalDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef(
    _RequiredDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef,
    _OptionalDescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef,
):
    pass


DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef = TypedDict(
    "DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef",
    {
        "ScalingPlanNames": Sequence[str],
        "ScalingPlanVersion": int,
        "ApplicationSources": Sequence[ApplicationSourceTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeScalingPlansRequestRequestTypeDef = TypedDict(
    "DescribeScalingPlansRequestRequestTypeDef",
    {
        "ScalingPlanNames": Sequence[str],
        "ScalingPlanVersion": int,
        "ApplicationSources": Sequence[ApplicationSourceTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredTargetTrackingConfigurationTypeDef = TypedDict(
    "_RequiredTargetTrackingConfigurationTypeDef",
    {
        "TargetValue": float,
    },
)
_OptionalTargetTrackingConfigurationTypeDef = TypedDict(
    "_OptionalTargetTrackingConfigurationTypeDef",
    {
        "PredefinedScalingMetricSpecification": PredefinedScalingMetricSpecificationTypeDef,
        "CustomizedScalingMetricSpecification": CustomizedScalingMetricSpecificationTypeDef,
        "DisableScaleIn": bool,
        "ScaleOutCooldown": int,
        "ScaleInCooldown": int,
        "EstimatedInstanceWarmup": int,
    },
    total=False,
)


class TargetTrackingConfigurationTypeDef(
    _RequiredTargetTrackingConfigurationTypeDef, _OptionalTargetTrackingConfigurationTypeDef
):
    pass


_RequiredScalingInstructionTypeDef = TypedDict(
    "_RequiredScalingInstructionTypeDef",
    {
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "MinCapacity": int,
        "MaxCapacity": int,
        "TargetTrackingConfigurations": Sequence[TargetTrackingConfigurationTypeDef],
    },
)
_OptionalScalingInstructionTypeDef = TypedDict(
    "_OptionalScalingInstructionTypeDef",
    {
        "PredefinedLoadMetricSpecification": PredefinedLoadMetricSpecificationTypeDef,
        "CustomizedLoadMetricSpecification": CustomizedLoadMetricSpecificationTypeDef,
        "ScheduledActionBufferTime": int,
        "PredictiveScalingMaxCapacityBehavior": PredictiveScalingMaxCapacityBehaviorType,
        "PredictiveScalingMaxCapacityBuffer": int,
        "PredictiveScalingMode": PredictiveScalingModeType,
        "ScalingPolicyUpdateBehavior": ScalingPolicyUpdateBehaviorType,
        "DisableDynamicScaling": bool,
    },
    total=False,
)


class ScalingInstructionTypeDef(
    _RequiredScalingInstructionTypeDef, _OptionalScalingInstructionTypeDef
):
    pass


_RequiredScalingPolicyTypeDef = TypedDict(
    "_RequiredScalingPolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyType": Literal["TargetTrackingScaling"],
    },
)
_OptionalScalingPolicyTypeDef = TypedDict(
    "_OptionalScalingPolicyTypeDef",
    {
        "TargetTrackingConfiguration": TargetTrackingConfigurationTypeDef,
    },
    total=False,
)


class ScalingPolicyTypeDef(_RequiredScalingPolicyTypeDef, _OptionalScalingPolicyTypeDef):
    pass


CreateScalingPlanRequestRequestTypeDef = TypedDict(
    "CreateScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ApplicationSource": ApplicationSourceTypeDef,
        "ScalingInstructions": Sequence[ScalingInstructionTypeDef],
    },
)

_RequiredScalingPlanTypeDef = TypedDict(
    "_RequiredScalingPlanTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ApplicationSource": ApplicationSourceTypeDef,
        "ScalingInstructions": List[ScalingInstructionTypeDef],
        "StatusCode": ScalingPlanStatusCodeType,
    },
)
_OptionalScalingPlanTypeDef = TypedDict(
    "_OptionalScalingPlanTypeDef",
    {
        "StatusMessage": str,
        "StatusStartTime": datetime,
        "CreationTime": datetime,
    },
    total=False,
)


class ScalingPlanTypeDef(_RequiredScalingPlanTypeDef, _OptionalScalingPlanTypeDef):
    pass


_RequiredUpdateScalingPlanRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
    },
)
_OptionalUpdateScalingPlanRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateScalingPlanRequestRequestTypeDef",
    {
        "ApplicationSource": ApplicationSourceTypeDef,
        "ScalingInstructions": Sequence[ScalingInstructionTypeDef],
    },
    total=False,
)


class UpdateScalingPlanRequestRequestTypeDef(
    _RequiredUpdateScalingPlanRequestRequestTypeDef, _OptionalUpdateScalingPlanRequestRequestTypeDef
):
    pass


_RequiredScalingPlanResourceTypeDef = TypedDict(
    "_RequiredScalingPlanResourceTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "ScalingStatusCode": ScalingStatusCodeType,
    },
)
_OptionalScalingPlanResourceTypeDef = TypedDict(
    "_OptionalScalingPlanResourceTypeDef",
    {
        "ScalingPolicies": List[ScalingPolicyTypeDef],
        "ScalingStatusMessage": str,
    },
    total=False,
)


class ScalingPlanResourceTypeDef(
    _RequiredScalingPlanResourceTypeDef, _OptionalScalingPlanResourceTypeDef
):
    pass


DescribeScalingPlansResponseTypeDef = TypedDict(
    "DescribeScalingPlansResponseTypeDef",
    {
        "ScalingPlans": List[ScalingPlanTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeScalingPlanResourcesResponseTypeDef = TypedDict(
    "DescribeScalingPlanResourcesResponseTypeDef",
    {
        "ScalingPlanResources": List[ScalingPlanResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
