"""
Type annotations for snow-device-management service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_snow_device_management/type_defs/)

Usage::

    ```python
    from mypy_boto3_snow_device_management.type_defs import CancelTaskInputRequestTypeDef

    data: CancelTaskInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    AttachmentStatusType,
    ExecutionStateType,
    InstanceStateNameType,
    IpAddressAssignmentType,
    PhysicalConnectorTypeType,
    TaskStateType,
    UnlockStateType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CancelTaskInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CapacityTypeDef",
    "CommandTypeDef",
    "CpuOptionsTypeDef",
    "DescribeDeviceEc2InputRequestTypeDef",
    "DescribeDeviceInputRequestTypeDef",
    "PhysicalNetworkInterfaceTypeDef",
    "SoftwareInformationTypeDef",
    "DescribeExecutionInputRequestTypeDef",
    "DescribeTaskInputRequestTypeDef",
    "DeviceSummaryTypeDef",
    "EbsInstanceBlockDeviceTypeDef",
    "ExecutionSummaryTypeDef",
    "InstanceStateTypeDef",
    "SecurityGroupIdentifierTypeDef",
    "PaginatorConfigTypeDef",
    "ListDeviceResourcesInputRequestTypeDef",
    "ResourceSummaryTypeDef",
    "ListDevicesInputRequestTypeDef",
    "ListExecutionsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTasksInputRequestTypeDef",
    "TaskSummaryTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "CancelTaskOutputTypeDef",
    "CreateTaskOutputTypeDef",
    "DescribeExecutionOutputTypeDef",
    "DescribeTaskOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "CreateTaskInputRequestTypeDef",
    "DescribeDeviceOutputTypeDef",
    "ListDevicesOutputTypeDef",
    "InstanceBlockDeviceMappingTypeDef",
    "ListExecutionsOutputTypeDef",
    "ListDeviceResourcesInputListDeviceResourcesPaginateTypeDef",
    "ListDevicesInputListDevicesPaginateTypeDef",
    "ListExecutionsInputListExecutionsPaginateTypeDef",
    "ListTasksInputListTasksPaginateTypeDef",
    "ListDeviceResourcesOutputTypeDef",
    "ListTasksOutputTypeDef",
    "InstanceTypeDef",
    "InstanceSummaryTypeDef",
    "DescribeDeviceEc2OutputTypeDef",
)

CancelTaskInputRequestTypeDef = TypedDict(
    "CancelTaskInputRequestTypeDef",
    {
        "taskId": str,
    },
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

CapacityTypeDef = TypedDict(
    "CapacityTypeDef",
    {
        "available": int,
        "name": str,
        "total": int,
        "unit": str,
        "used": int,
    },
    total=False,
)

CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "reboot": Mapping[str, Any],
        "unlock": Mapping[str, Any],
    },
    total=False,
)

CpuOptionsTypeDef = TypedDict(
    "CpuOptionsTypeDef",
    {
        "coreCount": int,
        "threadsPerCore": int,
    },
    total=False,
)

DescribeDeviceEc2InputRequestTypeDef = TypedDict(
    "DescribeDeviceEc2InputRequestTypeDef",
    {
        "instanceIds": Sequence[str],
        "managedDeviceId": str,
    },
)

DescribeDeviceInputRequestTypeDef = TypedDict(
    "DescribeDeviceInputRequestTypeDef",
    {
        "managedDeviceId": str,
    },
)

PhysicalNetworkInterfaceTypeDef = TypedDict(
    "PhysicalNetworkInterfaceTypeDef",
    {
        "defaultGateway": str,
        "ipAddress": str,
        "ipAddressAssignment": IpAddressAssignmentType,
        "macAddress": str,
        "netmask": str,
        "physicalConnectorType": PhysicalConnectorTypeType,
        "physicalNetworkInterfaceId": str,
    },
    total=False,
)

SoftwareInformationTypeDef = TypedDict(
    "SoftwareInformationTypeDef",
    {
        "installState": str,
        "installedVersion": str,
        "installingVersion": str,
    },
    total=False,
)

DescribeExecutionInputRequestTypeDef = TypedDict(
    "DescribeExecutionInputRequestTypeDef",
    {
        "managedDeviceId": str,
        "taskId": str,
    },
)

DescribeTaskInputRequestTypeDef = TypedDict(
    "DescribeTaskInputRequestTypeDef",
    {
        "taskId": str,
    },
)

DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "associatedWithJob": str,
        "managedDeviceArn": str,
        "managedDeviceId": str,
        "tags": Dict[str, str],
    },
    total=False,
)

EbsInstanceBlockDeviceTypeDef = TypedDict(
    "EbsInstanceBlockDeviceTypeDef",
    {
        "attachTime": datetime,
        "deleteOnTermination": bool,
        "status": AttachmentStatusType,
        "volumeId": str,
    },
    total=False,
)

ExecutionSummaryTypeDef = TypedDict(
    "ExecutionSummaryTypeDef",
    {
        "executionId": str,
        "managedDeviceId": str,
        "state": ExecutionStateType,
        "taskId": str,
    },
    total=False,
)

InstanceStateTypeDef = TypedDict(
    "InstanceStateTypeDef",
    {
        "code": int,
        "name": InstanceStateNameType,
    },
    total=False,
)

SecurityGroupIdentifierTypeDef = TypedDict(
    "SecurityGroupIdentifierTypeDef",
    {
        "groupId": str,
        "groupName": str,
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

_RequiredListDeviceResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListDeviceResourcesInputRequestTypeDef",
    {
        "managedDeviceId": str,
    },
)
_OptionalListDeviceResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListDeviceResourcesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "type": str,
    },
    total=False,
)

class ListDeviceResourcesInputRequestTypeDef(
    _RequiredListDeviceResourcesInputRequestTypeDef, _OptionalListDeviceResourcesInputRequestTypeDef
):
    pass

_RequiredResourceSummaryTypeDef = TypedDict(
    "_RequiredResourceSummaryTypeDef",
    {
        "resourceType": str,
    },
)
_OptionalResourceSummaryTypeDef = TypedDict(
    "_OptionalResourceSummaryTypeDef",
    {
        "arn": str,
        "id": str,
    },
    total=False,
)

class ResourceSummaryTypeDef(_RequiredResourceSummaryTypeDef, _OptionalResourceSummaryTypeDef):
    pass

ListDevicesInputRequestTypeDef = TypedDict(
    "ListDevicesInputRequestTypeDef",
    {
        "jobId": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListExecutionsInputRequestTypeDef = TypedDict(
    "_RequiredListExecutionsInputRequestTypeDef",
    {
        "taskId": str,
    },
)
_OptionalListExecutionsInputRequestTypeDef = TypedDict(
    "_OptionalListExecutionsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "state": ExecutionStateType,
    },
    total=False,
)

class ListExecutionsInputRequestTypeDef(
    _RequiredListExecutionsInputRequestTypeDef, _OptionalListExecutionsInputRequestTypeDef
):
    pass

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTasksInputRequestTypeDef = TypedDict(
    "ListTasksInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "state": TaskStateType,
    },
    total=False,
)

_RequiredTaskSummaryTypeDef = TypedDict(
    "_RequiredTaskSummaryTypeDef",
    {
        "taskId": str,
    },
)
_OptionalTaskSummaryTypeDef = TypedDict(
    "_OptionalTaskSummaryTypeDef",
    {
        "state": TaskStateType,
        "tags": Dict[str, str],
        "taskArn": str,
    },
    total=False,
)

class TaskSummaryTypeDef(_RequiredTaskSummaryTypeDef, _OptionalTaskSummaryTypeDef):
    pass

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

CancelTaskOutputTypeDef = TypedDict(
    "CancelTaskOutputTypeDef",
    {
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTaskOutputTypeDef = TypedDict(
    "CreateTaskOutputTypeDef",
    {
        "taskArn": str,
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeExecutionOutputTypeDef = TypedDict(
    "DescribeExecutionOutputTypeDef",
    {
        "executionId": str,
        "lastUpdatedAt": datetime,
        "managedDeviceId": str,
        "startedAt": datetime,
        "state": ExecutionStateType,
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTaskOutputTypeDef = TypedDict(
    "DescribeTaskOutputTypeDef",
    {
        "completedAt": datetime,
        "createdAt": datetime,
        "description": str,
        "lastUpdatedAt": datetime,
        "state": TaskStateType,
        "tags": Dict[str, str],
        "targets": List[str],
        "taskArn": str,
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateTaskInputRequestTypeDef = TypedDict(
    "_RequiredCreateTaskInputRequestTypeDef",
    {
        "command": CommandTypeDef,
        "targets": Sequence[str],
    },
)
_OptionalCreateTaskInputRequestTypeDef = TypedDict(
    "_OptionalCreateTaskInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateTaskInputRequestTypeDef(
    _RequiredCreateTaskInputRequestTypeDef, _OptionalCreateTaskInputRequestTypeDef
):
    pass

DescribeDeviceOutputTypeDef = TypedDict(
    "DescribeDeviceOutputTypeDef",
    {
        "associatedWithJob": str,
        "deviceCapacities": List[CapacityTypeDef],
        "deviceState": UnlockStateType,
        "deviceType": str,
        "lastReachedOutAt": datetime,
        "lastUpdatedAt": datetime,
        "managedDeviceArn": str,
        "managedDeviceId": str,
        "physicalNetworkInterfaces": List[PhysicalNetworkInterfaceTypeDef],
        "software": SoftwareInformationTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDevicesOutputTypeDef = TypedDict(
    "ListDevicesOutputTypeDef",
    {
        "devices": List[DeviceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceBlockDeviceMappingTypeDef = TypedDict(
    "InstanceBlockDeviceMappingTypeDef",
    {
        "deviceName": str,
        "ebs": EbsInstanceBlockDeviceTypeDef,
    },
    total=False,
)

ListExecutionsOutputTypeDef = TypedDict(
    "ListExecutionsOutputTypeDef",
    {
        "executions": List[ExecutionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListDeviceResourcesInputListDeviceResourcesPaginateTypeDef = TypedDict(
    "_RequiredListDeviceResourcesInputListDeviceResourcesPaginateTypeDef",
    {
        "managedDeviceId": str,
    },
)
_OptionalListDeviceResourcesInputListDeviceResourcesPaginateTypeDef = TypedDict(
    "_OptionalListDeviceResourcesInputListDeviceResourcesPaginateTypeDef",
    {
        "type": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDeviceResourcesInputListDeviceResourcesPaginateTypeDef(
    _RequiredListDeviceResourcesInputListDeviceResourcesPaginateTypeDef,
    _OptionalListDeviceResourcesInputListDeviceResourcesPaginateTypeDef,
):
    pass

ListDevicesInputListDevicesPaginateTypeDef = TypedDict(
    "ListDevicesInputListDevicesPaginateTypeDef",
    {
        "jobId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListExecutionsInputListExecutionsPaginateTypeDef = TypedDict(
    "_RequiredListExecutionsInputListExecutionsPaginateTypeDef",
    {
        "taskId": str,
    },
)
_OptionalListExecutionsInputListExecutionsPaginateTypeDef = TypedDict(
    "_OptionalListExecutionsInputListExecutionsPaginateTypeDef",
    {
        "state": ExecutionStateType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListExecutionsInputListExecutionsPaginateTypeDef(
    _RequiredListExecutionsInputListExecutionsPaginateTypeDef,
    _OptionalListExecutionsInputListExecutionsPaginateTypeDef,
):
    pass

ListTasksInputListTasksPaginateTypeDef = TypedDict(
    "ListTasksInputListTasksPaginateTypeDef",
    {
        "state": TaskStateType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDeviceResourcesOutputTypeDef = TypedDict(
    "ListDeviceResourcesOutputTypeDef",
    {
        "nextToken": str,
        "resources": List[ResourceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTasksOutputTypeDef = TypedDict(
    "ListTasksOutputTypeDef",
    {
        "nextToken": str,
        "tasks": List[TaskSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "amiLaunchIndex": int,
        "blockDeviceMappings": List[InstanceBlockDeviceMappingTypeDef],
        "cpuOptions": CpuOptionsTypeDef,
        "createdAt": datetime,
        "imageId": str,
        "instanceId": str,
        "instanceType": str,
        "privateIpAddress": str,
        "publicIpAddress": str,
        "rootDeviceName": str,
        "securityGroups": List[SecurityGroupIdentifierTypeDef],
        "state": InstanceStateTypeDef,
        "updatedAt": datetime,
    },
    total=False,
)

InstanceSummaryTypeDef = TypedDict(
    "InstanceSummaryTypeDef",
    {
        "instance": InstanceTypeDef,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

DescribeDeviceEc2OutputTypeDef = TypedDict(
    "DescribeDeviceEc2OutputTypeDef",
    {
        "instances": List[InstanceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
