"""
Type annotations for sagemaker-edge service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_edge/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_edge.type_defs import EdgeMetricTypeDef

    data: EdgeMetricTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, Sequence, Union

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EdgeMetricTypeDef",
    "ResponseMetadataTypeDef",
    "GetDeviceRegistrationRequestRequestTypeDef",
    "ModelTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDeviceRegistrationResultTypeDef",
    "SendHeartbeatRequestRequestTypeDef",
)

EdgeMetricTypeDef = TypedDict(
    "EdgeMetricTypeDef",
    {
        "Dimension": str,
        "MetricName": str,
        "Value": float,
        "Timestamp": Union[datetime, str],
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

GetDeviceRegistrationRequestRequestTypeDef = TypedDict(
    "GetDeviceRegistrationRequestRequestTypeDef",
    {
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)

ModelTypeDef = TypedDict(
    "ModelTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
        "LatestSampleTime": Union[datetime, str],
        "LatestInference": Union[datetime, str],
        "ModelMetrics": Sequence[EdgeMetricTypeDef],
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeviceRegistrationResultTypeDef = TypedDict(
    "GetDeviceRegistrationResultTypeDef",
    {
        "DeviceRegistration": str,
        "CacheTTL": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSendHeartbeatRequestRequestTypeDef = TypedDict(
    "_RequiredSendHeartbeatRequestRequestTypeDef",
    {
        "AgentVersion": str,
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)
_OptionalSendHeartbeatRequestRequestTypeDef = TypedDict(
    "_OptionalSendHeartbeatRequestRequestTypeDef",
    {
        "AgentMetrics": Sequence[EdgeMetricTypeDef],
        "Models": Sequence[ModelTypeDef],
    },
    total=False,
)


class SendHeartbeatRequestRequestTypeDef(
    _RequiredSendHeartbeatRequestRequestTypeDef, _OptionalSendHeartbeatRequestRequestTypeDef
):
    pass
