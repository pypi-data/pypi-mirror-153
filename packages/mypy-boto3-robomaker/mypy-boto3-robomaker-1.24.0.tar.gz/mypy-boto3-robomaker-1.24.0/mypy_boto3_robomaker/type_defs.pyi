"""
Type annotations for robomaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_robomaker.type_defs import BatchDeleteWorldsRequestRequestTypeDef

    data: BatchDeleteWorldsRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ArchitectureType,
    ComputeTypeType,
    DataSourceTypeType,
    DeploymentJobErrorCodeType,
    DeploymentStatusType,
    ExitBehaviorType,
    FailureBehaviorType,
    RobotDeploymentStepType,
    RobotSoftwareSuiteTypeType,
    RobotSoftwareSuiteVersionTypeType,
    RobotStatusType,
    SimulationJobBatchStatusType,
    SimulationJobErrorCodeType,
    SimulationJobStatusType,
    SimulationSoftwareSuiteTypeType,
    UploadBehaviorType,
    WorldExportJobErrorCodeType,
    WorldExportJobStatusType,
    WorldGenerationJobErrorCodeType,
    WorldGenerationJobStatusType,
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
    "BatchDeleteWorldsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDescribeSimulationJobRequestRequestTypeDef",
    "BatchPolicyTypeDef",
    "CancelDeploymentJobRequestRequestTypeDef",
    "CancelSimulationJobBatchRequestRequestTypeDef",
    "CancelSimulationJobRequestRequestTypeDef",
    "CancelWorldExportJobRequestRequestTypeDef",
    "CancelWorldGenerationJobRequestRequestTypeDef",
    "ComputeResponseTypeDef",
    "ComputeTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "EnvironmentTypeDef",
    "RobotSoftwareSuiteTypeDef",
    "SourceConfigTypeDef",
    "SourceTypeDef",
    "CreateRobotApplicationVersionRequestRequestTypeDef",
    "CreateRobotRequestRequestTypeDef",
    "RenderingEngineTypeDef",
    "SimulationSoftwareSuiteTypeDef",
    "CreateSimulationApplicationVersionRequestRequestTypeDef",
    "DataSourceConfigTypeDef",
    "LoggingConfigTypeDef",
    "OutputLocationTypeDef",
    "VPCConfigTypeDef",
    "VPCConfigResponseTypeDef",
    "WorldCountTypeDef",
    "TemplateLocationTypeDef",
    "S3KeyOutputTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteRobotApplicationRequestRequestTypeDef",
    "DeleteRobotRequestRequestTypeDef",
    "DeleteSimulationApplicationRequestRequestTypeDef",
    "DeleteWorldTemplateRequestRequestTypeDef",
    "DeploymentLaunchConfigTypeDef",
    "S3ObjectTypeDef",
    "DeregisterRobotRequestRequestTypeDef",
    "DescribeDeploymentJobRequestRequestTypeDef",
    "DescribeFleetRequestRequestTypeDef",
    "RobotTypeDef",
    "DescribeRobotApplicationRequestRequestTypeDef",
    "DescribeRobotRequestRequestTypeDef",
    "DescribeSimulationApplicationRequestRequestTypeDef",
    "DescribeSimulationJobBatchRequestRequestTypeDef",
    "SimulationJobSummaryTypeDef",
    "DescribeSimulationJobRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "DescribeWorldExportJobRequestRequestTypeDef",
    "DescribeWorldGenerationJobRequestRequestTypeDef",
    "DescribeWorldRequestRequestTypeDef",
    "DescribeWorldTemplateRequestRequestTypeDef",
    "WorldFailureTypeDef",
    "FilterTypeDef",
    "FleetTypeDef",
    "GetWorldTemplateBodyRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "SimulationJobBatchSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorldTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "WorldSummaryTypeDef",
    "PortMappingTypeDef",
    "ProgressDetailTypeDef",
    "RegisterRobotRequestRequestTypeDef",
    "RestartSimulationJobRequestRequestTypeDef",
    "ToolTypeDef",
    "UploadConfigurationTypeDef",
    "WorldConfigTypeDef",
    "SyncDeploymentJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "BatchDeleteWorldsResponseTypeDef",
    "CreateFleetResponseTypeDef",
    "CreateRobotResponseTypeDef",
    "CreateWorldTemplateResponseTypeDef",
    "DeregisterRobotResponseTypeDef",
    "DescribeRobotResponseTypeDef",
    "DescribeWorldResponseTypeDef",
    "DescribeWorldTemplateResponseTypeDef",
    "GetWorldTemplateBodyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RegisterRobotResponseTypeDef",
    "UpdateWorldTemplateResponseTypeDef",
    "RobotApplicationSummaryTypeDef",
    "CreateRobotApplicationRequestRequestTypeDef",
    "UpdateRobotApplicationRequestRequestTypeDef",
    "CreateRobotApplicationResponseTypeDef",
    "CreateRobotApplicationVersionResponseTypeDef",
    "DescribeRobotApplicationResponseTypeDef",
    "UpdateRobotApplicationResponseTypeDef",
    "CreateSimulationApplicationRequestRequestTypeDef",
    "CreateSimulationApplicationResponseTypeDef",
    "CreateSimulationApplicationVersionResponseTypeDef",
    "DescribeSimulationApplicationResponseTypeDef",
    "SimulationApplicationSummaryTypeDef",
    "UpdateSimulationApplicationRequestRequestTypeDef",
    "UpdateSimulationApplicationResponseTypeDef",
    "CreateWorldExportJobRequestRequestTypeDef",
    "CreateWorldExportJobResponseTypeDef",
    "DescribeWorldExportJobResponseTypeDef",
    "WorldExportJobSummaryTypeDef",
    "CreateWorldGenerationJobRequestRequestTypeDef",
    "CreateWorldGenerationJobResponseTypeDef",
    "WorldGenerationJobSummaryTypeDef",
    "CreateWorldTemplateRequestRequestTypeDef",
    "UpdateWorldTemplateRequestRequestTypeDef",
    "DataSourceTypeDef",
    "DeploymentApplicationConfigTypeDef",
    "DeploymentConfigTypeDef",
    "DescribeFleetResponseTypeDef",
    "ListRobotsResponseTypeDef",
    "ListSimulationJobsResponseTypeDef",
    "FailureSummaryTypeDef",
    "ListDeploymentJobsRequestRequestTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListRobotApplicationsRequestRequestTypeDef",
    "ListRobotsRequestRequestTypeDef",
    "ListSimulationApplicationsRequestRequestTypeDef",
    "ListSimulationJobBatchesRequestRequestTypeDef",
    "ListSimulationJobsRequestRequestTypeDef",
    "ListWorldExportJobsRequestRequestTypeDef",
    "ListWorldGenerationJobsRequestRequestTypeDef",
    "ListWorldsRequestRequestTypeDef",
    "ListFleetsResponseTypeDef",
    "ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef",
    "ListFleetsRequestListFleetsPaginateTypeDef",
    "ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef",
    "ListRobotsRequestListRobotsPaginateTypeDef",
    "ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef",
    "ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef",
    "ListSimulationJobsRequestListSimulationJobsPaginateTypeDef",
    "ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef",
    "ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef",
    "ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef",
    "ListWorldsRequestListWorldsPaginateTypeDef",
    "ListSimulationJobBatchesResponseTypeDef",
    "ListWorldTemplatesResponseTypeDef",
    "ListWorldsResponseTypeDef",
    "PortForwardingConfigTypeDef",
    "RobotDeploymentTypeDef",
    "ListRobotApplicationsResponseTypeDef",
    "ListSimulationApplicationsResponseTypeDef",
    "ListWorldExportJobsResponseTypeDef",
    "ListWorldGenerationJobsResponseTypeDef",
    "CreateDeploymentJobRequestRequestTypeDef",
    "CreateDeploymentJobResponseTypeDef",
    "DeploymentJobTypeDef",
    "SyncDeploymentJobResponseTypeDef",
    "FinishedWorldsSummaryTypeDef",
    "LaunchConfigTypeDef",
    "DescribeDeploymentJobResponseTypeDef",
    "ListDeploymentJobsResponseTypeDef",
    "DescribeWorldGenerationJobResponseTypeDef",
    "RobotApplicationConfigTypeDef",
    "SimulationApplicationConfigTypeDef",
    "CreateSimulationJobRequestRequestTypeDef",
    "CreateSimulationJobResponseTypeDef",
    "DescribeSimulationJobResponseTypeDef",
    "SimulationJobRequestTypeDef",
    "SimulationJobTypeDef",
    "FailedCreateSimulationJobRequestTypeDef",
    "StartSimulationJobBatchRequestRequestTypeDef",
    "BatchDescribeSimulationJobResponseTypeDef",
    "DescribeSimulationJobBatchResponseTypeDef",
    "StartSimulationJobBatchResponseTypeDef",
)

BatchDeleteWorldsRequestRequestTypeDef = TypedDict(
    "BatchDeleteWorldsRequestRequestTypeDef",
    {
        "worlds": Sequence[str],
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

BatchDescribeSimulationJobRequestRequestTypeDef = TypedDict(
    "BatchDescribeSimulationJobRequestRequestTypeDef",
    {
        "jobs": Sequence[str],
    },
)

BatchPolicyTypeDef = TypedDict(
    "BatchPolicyTypeDef",
    {
        "timeoutInSeconds": int,
        "maxConcurrency": int,
    },
    total=False,
)

CancelDeploymentJobRequestRequestTypeDef = TypedDict(
    "CancelDeploymentJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

CancelSimulationJobBatchRequestRequestTypeDef = TypedDict(
    "CancelSimulationJobBatchRequestRequestTypeDef",
    {
        "batch": str,
    },
)

CancelSimulationJobRequestRequestTypeDef = TypedDict(
    "CancelSimulationJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

CancelWorldExportJobRequestRequestTypeDef = TypedDict(
    "CancelWorldExportJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

CancelWorldGenerationJobRequestRequestTypeDef = TypedDict(
    "CancelWorldGenerationJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

ComputeResponseTypeDef = TypedDict(
    "ComputeResponseTypeDef",
    {
        "simulationUnitLimit": int,
        "computeType": ComputeTypeType,
        "gpuUnitLimit": int,
    },
    total=False,
)

ComputeTypeDef = TypedDict(
    "ComputeTypeDef",
    {
        "simulationUnitLimit": int,
        "computeType": ComputeTypeType,
        "gpuUnitLimit": int,
    },
    total=False,
)

_RequiredCreateFleetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateFleetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateFleetRequestRequestTypeDef(
    _RequiredCreateFleetRequestRequestTypeDef, _OptionalCreateFleetRequestRequestTypeDef
):
    pass

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "uri": str,
    },
    total=False,
)

RobotSoftwareSuiteTypeDef = TypedDict(
    "RobotSoftwareSuiteTypeDef",
    {
        "name": RobotSoftwareSuiteTypeType,
        "version": RobotSoftwareSuiteVersionTypeType,
    },
    total=False,
)

SourceConfigTypeDef = TypedDict(
    "SourceConfigTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
        "architecture": ArchitectureType,
    },
    total=False,
)

SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
        "etag": str,
        "architecture": ArchitectureType,
    },
    total=False,
)

_RequiredCreateRobotApplicationVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRobotApplicationVersionRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalCreateRobotApplicationVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRobotApplicationVersionRequestRequestTypeDef",
    {
        "currentRevisionId": str,
        "s3Etags": Sequence[str],
        "imageDigest": str,
    },
    total=False,
)

class CreateRobotApplicationVersionRequestRequestTypeDef(
    _RequiredCreateRobotApplicationVersionRequestRequestTypeDef,
    _OptionalCreateRobotApplicationVersionRequestRequestTypeDef,
):
    pass

_RequiredCreateRobotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRobotRequestRequestTypeDef",
    {
        "name": str,
        "architecture": ArchitectureType,
        "greengrassGroupId": str,
    },
)
_OptionalCreateRobotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRobotRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateRobotRequestRequestTypeDef(
    _RequiredCreateRobotRequestRequestTypeDef, _OptionalCreateRobotRequestRequestTypeDef
):
    pass

RenderingEngineTypeDef = TypedDict(
    "RenderingEngineTypeDef",
    {
        "name": Literal["OGRE"],
        "version": str,
    },
    total=False,
)

SimulationSoftwareSuiteTypeDef = TypedDict(
    "SimulationSoftwareSuiteTypeDef",
    {
        "name": SimulationSoftwareSuiteTypeType,
        "version": str,
    },
    total=False,
)

_RequiredCreateSimulationApplicationVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSimulationApplicationVersionRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalCreateSimulationApplicationVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSimulationApplicationVersionRequestRequestTypeDef",
    {
        "currentRevisionId": str,
        "s3Etags": Sequence[str],
        "imageDigest": str,
    },
    total=False,
)

class CreateSimulationApplicationVersionRequestRequestTypeDef(
    _RequiredCreateSimulationApplicationVersionRequestRequestTypeDef,
    _OptionalCreateSimulationApplicationVersionRequestRequestTypeDef,
):
    pass

_RequiredDataSourceConfigTypeDef = TypedDict(
    "_RequiredDataSourceConfigTypeDef",
    {
        "name": str,
        "s3Bucket": str,
        "s3Keys": Sequence[str],
    },
)
_OptionalDataSourceConfigTypeDef = TypedDict(
    "_OptionalDataSourceConfigTypeDef",
    {
        "type": DataSourceTypeType,
        "destination": str,
    },
    total=False,
)

class DataSourceConfigTypeDef(_RequiredDataSourceConfigTypeDef, _OptionalDataSourceConfigTypeDef):
    pass

LoggingConfigTypeDef = TypedDict(
    "LoggingConfigTypeDef",
    {
        "recordAllRosTopics": bool,
    },
    total=False,
)

OutputLocationTypeDef = TypedDict(
    "OutputLocationTypeDef",
    {
        "s3Bucket": str,
        "s3Prefix": str,
    },
    total=False,
)

_RequiredVPCConfigTypeDef = TypedDict(
    "_RequiredVPCConfigTypeDef",
    {
        "subnets": Sequence[str],
    },
)
_OptionalVPCConfigTypeDef = TypedDict(
    "_OptionalVPCConfigTypeDef",
    {
        "securityGroups": Sequence[str],
        "assignPublicIp": bool,
    },
    total=False,
)

class VPCConfigTypeDef(_RequiredVPCConfigTypeDef, _OptionalVPCConfigTypeDef):
    pass

VPCConfigResponseTypeDef = TypedDict(
    "VPCConfigResponseTypeDef",
    {
        "subnets": List[str],
        "securityGroups": List[str],
        "vpcId": str,
        "assignPublicIp": bool,
    },
    total=False,
)

WorldCountTypeDef = TypedDict(
    "WorldCountTypeDef",
    {
        "floorplanCount": int,
        "interiorCountPerFloorplan": int,
    },
    total=False,
)

TemplateLocationTypeDef = TypedDict(
    "TemplateLocationTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
    },
)

S3KeyOutputTypeDef = TypedDict(
    "S3KeyOutputTypeDef",
    {
        "s3Key": str,
        "etag": str,
    },
    total=False,
)

DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "fleet": str,
    },
)

_RequiredDeleteRobotApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRobotApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalDeleteRobotApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRobotApplicationRequestRequestTypeDef",
    {
        "applicationVersion": str,
    },
    total=False,
)

class DeleteRobotApplicationRequestRequestTypeDef(
    _RequiredDeleteRobotApplicationRequestRequestTypeDef,
    _OptionalDeleteRobotApplicationRequestRequestTypeDef,
):
    pass

DeleteRobotRequestRequestTypeDef = TypedDict(
    "DeleteRobotRequestRequestTypeDef",
    {
        "robot": str,
    },
)

_RequiredDeleteSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSimulationApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalDeleteSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSimulationApplicationRequestRequestTypeDef",
    {
        "applicationVersion": str,
    },
    total=False,
)

class DeleteSimulationApplicationRequestRequestTypeDef(
    _RequiredDeleteSimulationApplicationRequestRequestTypeDef,
    _OptionalDeleteSimulationApplicationRequestRequestTypeDef,
):
    pass

DeleteWorldTemplateRequestRequestTypeDef = TypedDict(
    "DeleteWorldTemplateRequestRequestTypeDef",
    {
        "template": str,
    },
)

_RequiredDeploymentLaunchConfigTypeDef = TypedDict(
    "_RequiredDeploymentLaunchConfigTypeDef",
    {
        "packageName": str,
        "launchFile": str,
    },
)
_OptionalDeploymentLaunchConfigTypeDef = TypedDict(
    "_OptionalDeploymentLaunchConfigTypeDef",
    {
        "preLaunchFile": str,
        "postLaunchFile": str,
        "environmentVariables": Mapping[str, str],
    },
    total=False,
)

class DeploymentLaunchConfigTypeDef(
    _RequiredDeploymentLaunchConfigTypeDef, _OptionalDeploymentLaunchConfigTypeDef
):
    pass

_RequiredS3ObjectTypeDef = TypedDict(
    "_RequiredS3ObjectTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)
_OptionalS3ObjectTypeDef = TypedDict(
    "_OptionalS3ObjectTypeDef",
    {
        "etag": str,
    },
    total=False,
)

class S3ObjectTypeDef(_RequiredS3ObjectTypeDef, _OptionalS3ObjectTypeDef):
    pass

DeregisterRobotRequestRequestTypeDef = TypedDict(
    "DeregisterRobotRequestRequestTypeDef",
    {
        "fleet": str,
        "robot": str,
    },
)

DescribeDeploymentJobRequestRequestTypeDef = TypedDict(
    "DescribeDeploymentJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

DescribeFleetRequestRequestTypeDef = TypedDict(
    "DescribeFleetRequestRequestTypeDef",
    {
        "fleet": str,
    },
)

RobotTypeDef = TypedDict(
    "RobotTypeDef",
    {
        "arn": str,
        "name": str,
        "fleetArn": str,
        "status": RobotStatusType,
        "greenGrassGroupId": str,
        "createdAt": datetime,
        "architecture": ArchitectureType,
        "lastDeploymentJob": str,
        "lastDeploymentTime": datetime,
    },
    total=False,
)

_RequiredDescribeRobotApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRobotApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalDescribeRobotApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRobotApplicationRequestRequestTypeDef",
    {
        "applicationVersion": str,
    },
    total=False,
)

class DescribeRobotApplicationRequestRequestTypeDef(
    _RequiredDescribeRobotApplicationRequestRequestTypeDef,
    _OptionalDescribeRobotApplicationRequestRequestTypeDef,
):
    pass

DescribeRobotRequestRequestTypeDef = TypedDict(
    "DescribeRobotRequestRequestTypeDef",
    {
        "robot": str,
    },
)

_RequiredDescribeSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSimulationApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalDescribeSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSimulationApplicationRequestRequestTypeDef",
    {
        "applicationVersion": str,
    },
    total=False,
)

class DescribeSimulationApplicationRequestRequestTypeDef(
    _RequiredDescribeSimulationApplicationRequestRequestTypeDef,
    _OptionalDescribeSimulationApplicationRequestRequestTypeDef,
):
    pass

DescribeSimulationJobBatchRequestRequestTypeDef = TypedDict(
    "DescribeSimulationJobBatchRequestRequestTypeDef",
    {
        "batch": str,
    },
)

SimulationJobSummaryTypeDef = TypedDict(
    "SimulationJobSummaryTypeDef",
    {
        "arn": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": SimulationJobStatusType,
        "simulationApplicationNames": List[str],
        "robotApplicationNames": List[str],
        "dataSourceNames": List[str],
        "computeType": ComputeTypeType,
    },
    total=False,
)

DescribeSimulationJobRequestRequestTypeDef = TypedDict(
    "DescribeSimulationJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "networkInterfaceId": str,
        "privateIpAddress": str,
        "publicIpAddress": str,
    },
    total=False,
)

DescribeWorldExportJobRequestRequestTypeDef = TypedDict(
    "DescribeWorldExportJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

DescribeWorldGenerationJobRequestRequestTypeDef = TypedDict(
    "DescribeWorldGenerationJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

DescribeWorldRequestRequestTypeDef = TypedDict(
    "DescribeWorldRequestRequestTypeDef",
    {
        "world": str,
    },
)

DescribeWorldTemplateRequestRequestTypeDef = TypedDict(
    "DescribeWorldTemplateRequestRequestTypeDef",
    {
        "template": str,
    },
)

WorldFailureTypeDef = TypedDict(
    "WorldFailureTypeDef",
    {
        "failureCode": WorldGenerationJobErrorCodeType,
        "sampleFailureReason": str,
        "failureCount": int,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
    total=False,
)

FleetTypeDef = TypedDict(
    "FleetTypeDef",
    {
        "name": str,
        "arn": str,
        "createdAt": datetime,
        "lastDeploymentStatus": DeploymentStatusType,
        "lastDeploymentJob": str,
        "lastDeploymentTime": datetime,
    },
    total=False,
)

GetWorldTemplateBodyRequestRequestTypeDef = TypedDict(
    "GetWorldTemplateBodyRequestRequestTypeDef",
    {
        "template": str,
        "generationJob": str,
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

SimulationJobBatchSummaryTypeDef = TypedDict(
    "SimulationJobBatchSummaryTypeDef",
    {
        "arn": str,
        "lastUpdatedAt": datetime,
        "createdAt": datetime,
        "status": SimulationJobBatchStatusType,
        "failedRequestCount": int,
        "pendingRequestCount": int,
        "createdRequestCount": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListWorldTemplatesRequestRequestTypeDef = TypedDict(
    "ListWorldTemplatesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "name": str,
        "version": str,
    },
    total=False,
)

WorldSummaryTypeDef = TypedDict(
    "WorldSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "generationJob": str,
        "template": str,
    },
    total=False,
)

_RequiredPortMappingTypeDef = TypedDict(
    "_RequiredPortMappingTypeDef",
    {
        "jobPort": int,
        "applicationPort": int,
    },
)
_OptionalPortMappingTypeDef = TypedDict(
    "_OptionalPortMappingTypeDef",
    {
        "enableOnPublicIp": bool,
    },
    total=False,
)

class PortMappingTypeDef(_RequiredPortMappingTypeDef, _OptionalPortMappingTypeDef):
    pass

ProgressDetailTypeDef = TypedDict(
    "ProgressDetailTypeDef",
    {
        "currentProgress": RobotDeploymentStepType,
        "percentDone": float,
        "estimatedTimeRemainingSeconds": int,
        "targetResource": str,
    },
    total=False,
)

RegisterRobotRequestRequestTypeDef = TypedDict(
    "RegisterRobotRequestRequestTypeDef",
    {
        "fleet": str,
        "robot": str,
    },
)

RestartSimulationJobRequestRequestTypeDef = TypedDict(
    "RestartSimulationJobRequestRequestTypeDef",
    {
        "job": str,
    },
)

_RequiredToolTypeDef = TypedDict(
    "_RequiredToolTypeDef",
    {
        "name": str,
        "command": str,
    },
)
_OptionalToolTypeDef = TypedDict(
    "_OptionalToolTypeDef",
    {
        "streamUI": bool,
        "streamOutputToCloudWatch": bool,
        "exitBehavior": ExitBehaviorType,
    },
    total=False,
)

class ToolTypeDef(_RequiredToolTypeDef, _OptionalToolTypeDef):
    pass

UploadConfigurationTypeDef = TypedDict(
    "UploadConfigurationTypeDef",
    {
        "name": str,
        "path": str,
        "uploadBehavior": UploadBehaviorType,
    },
)

WorldConfigTypeDef = TypedDict(
    "WorldConfigTypeDef",
    {
        "world": str,
    },
    total=False,
)

SyncDeploymentJobRequestRequestTypeDef = TypedDict(
    "SyncDeploymentJobRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "fleet": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

BatchDeleteWorldsResponseTypeDef = TypedDict(
    "BatchDeleteWorldsResponseTypeDef",
    {
        "unprocessedWorlds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFleetResponseTypeDef = TypedDict(
    "CreateFleetResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "createdAt": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRobotResponseTypeDef = TypedDict(
    "CreateRobotResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "createdAt": datetime,
        "greengrassGroupId": str,
        "architecture": ArchitectureType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorldTemplateResponseTypeDef = TypedDict(
    "CreateWorldTemplateResponseTypeDef",
    {
        "arn": str,
        "clientRequestToken": str,
        "createdAt": datetime,
        "name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterRobotResponseTypeDef = TypedDict(
    "DeregisterRobotResponseTypeDef",
    {
        "fleet": str,
        "robot": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRobotResponseTypeDef = TypedDict(
    "DescribeRobotResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "fleetArn": str,
        "status": RobotStatusType,
        "greengrassGroupId": str,
        "createdAt": datetime,
        "architecture": ArchitectureType,
        "lastDeploymentJob": str,
        "lastDeploymentTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorldResponseTypeDef = TypedDict(
    "DescribeWorldResponseTypeDef",
    {
        "arn": str,
        "generationJob": str,
        "template": str,
        "createdAt": datetime,
        "tags": Dict[str, str],
        "worldDescriptionBody": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorldTemplateResponseTypeDef = TypedDict(
    "DescribeWorldTemplateResponseTypeDef",
    {
        "arn": str,
        "clientRequestToken": str,
        "name": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "tags": Dict[str, str],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorldTemplateBodyResponseTypeDef = TypedDict(
    "GetWorldTemplateBodyResponseTypeDef",
    {
        "templateBody": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterRobotResponseTypeDef = TypedDict(
    "RegisterRobotResponseTypeDef",
    {
        "fleet": str,
        "robot": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorldTemplateResponseTypeDef = TypedDict(
    "UpdateWorldTemplateResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RobotApplicationSummaryTypeDef = TypedDict(
    "RobotApplicationSummaryTypeDef",
    {
        "name": str,
        "arn": str,
        "version": str,
        "lastUpdatedAt": datetime,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
    },
    total=False,
)

_RequiredCreateRobotApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRobotApplicationRequestRequestTypeDef",
    {
        "name": str,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
    },
)
_OptionalCreateRobotApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRobotApplicationRequestRequestTypeDef",
    {
        "sources": Sequence[SourceConfigTypeDef],
        "tags": Mapping[str, str],
        "environment": EnvironmentTypeDef,
    },
    total=False,
)

class CreateRobotApplicationRequestRequestTypeDef(
    _RequiredCreateRobotApplicationRequestRequestTypeDef,
    _OptionalCreateRobotApplicationRequestRequestTypeDef,
):
    pass

_RequiredUpdateRobotApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRobotApplicationRequestRequestTypeDef",
    {
        "application": str,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
    },
)
_OptionalUpdateRobotApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRobotApplicationRequestRequestTypeDef",
    {
        "sources": Sequence[SourceConfigTypeDef],
        "currentRevisionId": str,
        "environment": EnvironmentTypeDef,
    },
    total=False,
)

class UpdateRobotApplicationRequestRequestTypeDef(
    _RequiredUpdateRobotApplicationRequestRequestTypeDef,
    _OptionalUpdateRobotApplicationRequestRequestTypeDef,
):
    pass

CreateRobotApplicationResponseTypeDef = TypedDict(
    "CreateRobotApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "tags": Dict[str, str],
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRobotApplicationVersionResponseTypeDef = TypedDict(
    "CreateRobotApplicationVersionResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRobotApplicationResponseTypeDef = TypedDict(
    "DescribeRobotApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "revisionId": str,
        "lastUpdatedAt": datetime,
        "tags": Dict[str, str],
        "environment": EnvironmentTypeDef,
        "imageDigest": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRobotApplicationResponseTypeDef = TypedDict(
    "UpdateRobotApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSimulationApplicationRequestRequestTypeDef",
    {
        "name": str,
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
    },
)
_OptionalCreateSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSimulationApplicationRequestRequestTypeDef",
    {
        "sources": Sequence[SourceConfigTypeDef],
        "renderingEngine": RenderingEngineTypeDef,
        "tags": Mapping[str, str],
        "environment": EnvironmentTypeDef,
    },
    total=False,
)

class CreateSimulationApplicationRequestRequestTypeDef(
    _RequiredCreateSimulationApplicationRequestRequestTypeDef,
    _OptionalCreateSimulationApplicationRequestRequestTypeDef,
):
    pass

CreateSimulationApplicationResponseTypeDef = TypedDict(
    "CreateSimulationApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "renderingEngine": RenderingEngineTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "tags": Dict[str, str],
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSimulationApplicationVersionResponseTypeDef = TypedDict(
    "CreateSimulationApplicationVersionResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "renderingEngine": RenderingEngineTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSimulationApplicationResponseTypeDef = TypedDict(
    "DescribeSimulationApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "renderingEngine": RenderingEngineTypeDef,
        "revisionId": str,
        "lastUpdatedAt": datetime,
        "tags": Dict[str, str],
        "environment": EnvironmentTypeDef,
        "imageDigest": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SimulationApplicationSummaryTypeDef = TypedDict(
    "SimulationApplicationSummaryTypeDef",
    {
        "name": str,
        "arn": str,
        "version": str,
        "lastUpdatedAt": datetime,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
    },
    total=False,
)

_RequiredUpdateSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSimulationApplicationRequestRequestTypeDef",
    {
        "application": str,
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
    },
)
_OptionalUpdateSimulationApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSimulationApplicationRequestRequestTypeDef",
    {
        "sources": Sequence[SourceConfigTypeDef],
        "renderingEngine": RenderingEngineTypeDef,
        "currentRevisionId": str,
        "environment": EnvironmentTypeDef,
    },
    total=False,
)

class UpdateSimulationApplicationRequestRequestTypeDef(
    _RequiredUpdateSimulationApplicationRequestRequestTypeDef,
    _OptionalUpdateSimulationApplicationRequestRequestTypeDef,
):
    pass

UpdateSimulationApplicationResponseTypeDef = TypedDict(
    "UpdateSimulationApplicationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "sources": List[SourceTypeDef],
        "simulationSoftwareSuite": SimulationSoftwareSuiteTypeDef,
        "robotSoftwareSuite": RobotSoftwareSuiteTypeDef,
        "renderingEngine": RenderingEngineTypeDef,
        "lastUpdatedAt": datetime,
        "revisionId": str,
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateWorldExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorldExportJobRequestRequestTypeDef",
    {
        "worlds": Sequence[str],
        "outputLocation": OutputLocationTypeDef,
        "iamRole": str,
    },
)
_OptionalCreateWorldExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorldExportJobRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateWorldExportJobRequestRequestTypeDef(
    _RequiredCreateWorldExportJobRequestRequestTypeDef,
    _OptionalCreateWorldExportJobRequestRequestTypeDef,
):
    pass

CreateWorldExportJobResponseTypeDef = TypedDict(
    "CreateWorldExportJobResponseTypeDef",
    {
        "arn": str,
        "status": WorldExportJobStatusType,
        "createdAt": datetime,
        "failureCode": WorldExportJobErrorCodeType,
        "clientRequestToken": str,
        "outputLocation": OutputLocationTypeDef,
        "iamRole": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorldExportJobResponseTypeDef = TypedDict(
    "DescribeWorldExportJobResponseTypeDef",
    {
        "arn": str,
        "status": WorldExportJobStatusType,
        "createdAt": datetime,
        "failureCode": WorldExportJobErrorCodeType,
        "failureReason": str,
        "clientRequestToken": str,
        "worlds": List[str],
        "outputLocation": OutputLocationTypeDef,
        "iamRole": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorldExportJobSummaryTypeDef = TypedDict(
    "WorldExportJobSummaryTypeDef",
    {
        "arn": str,
        "status": WorldExportJobStatusType,
        "createdAt": datetime,
        "worlds": List[str],
        "outputLocation": OutputLocationTypeDef,
    },
    total=False,
)

_RequiredCreateWorldGenerationJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorldGenerationJobRequestRequestTypeDef",
    {
        "template": str,
        "worldCount": WorldCountTypeDef,
    },
)
_OptionalCreateWorldGenerationJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorldGenerationJobRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "tags": Mapping[str, str],
        "worldTags": Mapping[str, str],
    },
    total=False,
)

class CreateWorldGenerationJobRequestRequestTypeDef(
    _RequiredCreateWorldGenerationJobRequestRequestTypeDef,
    _OptionalCreateWorldGenerationJobRequestRequestTypeDef,
):
    pass

CreateWorldGenerationJobResponseTypeDef = TypedDict(
    "CreateWorldGenerationJobResponseTypeDef",
    {
        "arn": str,
        "status": WorldGenerationJobStatusType,
        "createdAt": datetime,
        "failureCode": WorldGenerationJobErrorCodeType,
        "clientRequestToken": str,
        "template": str,
        "worldCount": WorldCountTypeDef,
        "tags": Dict[str, str],
        "worldTags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorldGenerationJobSummaryTypeDef = TypedDict(
    "WorldGenerationJobSummaryTypeDef",
    {
        "arn": str,
        "template": str,
        "createdAt": datetime,
        "status": WorldGenerationJobStatusType,
        "worldCount": WorldCountTypeDef,
        "succeededWorldCount": int,
        "failedWorldCount": int,
    },
    total=False,
)

CreateWorldTemplateRequestRequestTypeDef = TypedDict(
    "CreateWorldTemplateRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "name": str,
        "templateBody": str,
        "templateLocation": TemplateLocationTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

_RequiredUpdateWorldTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorldTemplateRequestRequestTypeDef",
    {
        "template": str,
    },
)
_OptionalUpdateWorldTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorldTemplateRequestRequestTypeDef",
    {
        "name": str,
        "templateBody": str,
        "templateLocation": TemplateLocationTypeDef,
    },
    total=False,
)

class UpdateWorldTemplateRequestRequestTypeDef(
    _RequiredUpdateWorldTemplateRequestRequestTypeDef,
    _OptionalUpdateWorldTemplateRequestRequestTypeDef,
):
    pass

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "name": str,
        "s3Bucket": str,
        "s3Keys": List[S3KeyOutputTypeDef],
        "type": DataSourceTypeType,
        "destination": str,
    },
    total=False,
)

DeploymentApplicationConfigTypeDef = TypedDict(
    "DeploymentApplicationConfigTypeDef",
    {
        "application": str,
        "applicationVersion": str,
        "launchConfig": DeploymentLaunchConfigTypeDef,
    },
)

DeploymentConfigTypeDef = TypedDict(
    "DeploymentConfigTypeDef",
    {
        "concurrentDeploymentPercentage": int,
        "failureThresholdPercentage": int,
        "robotDeploymentTimeoutInSeconds": int,
        "downloadConditionFile": S3ObjectTypeDef,
    },
    total=False,
)

DescribeFleetResponseTypeDef = TypedDict(
    "DescribeFleetResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "robots": List[RobotTypeDef],
        "createdAt": datetime,
        "lastDeploymentStatus": DeploymentStatusType,
        "lastDeploymentJob": str,
        "lastDeploymentTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRobotsResponseTypeDef = TypedDict(
    "ListRobotsResponseTypeDef",
    {
        "robots": List[RobotTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSimulationJobsResponseTypeDef = TypedDict(
    "ListSimulationJobsResponseTypeDef",
    {
        "simulationJobSummaries": List[SimulationJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailureSummaryTypeDef = TypedDict(
    "FailureSummaryTypeDef",
    {
        "totalFailureCount": int,
        "failures": List[WorldFailureTypeDef],
    },
    total=False,
)

ListDeploymentJobsRequestRequestTypeDef = TypedDict(
    "ListDeploymentJobsRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListFleetsRequestRequestTypeDef = TypedDict(
    "ListFleetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListRobotApplicationsRequestRequestTypeDef = TypedDict(
    "ListRobotApplicationsRequestRequestTypeDef",
    {
        "versionQualifier": str,
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListRobotsRequestRequestTypeDef = TypedDict(
    "ListRobotsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListSimulationApplicationsRequestRequestTypeDef = TypedDict(
    "ListSimulationApplicationsRequestRequestTypeDef",
    {
        "versionQualifier": str,
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListSimulationJobBatchesRequestRequestTypeDef = TypedDict(
    "ListSimulationJobBatchesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListSimulationJobsRequestRequestTypeDef = TypedDict(
    "ListSimulationJobsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWorldExportJobsRequestRequestTypeDef = TypedDict(
    "ListWorldExportJobsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWorldGenerationJobsRequestRequestTypeDef = TypedDict(
    "ListWorldGenerationJobsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWorldsRequestRequestTypeDef = TypedDict(
    "ListWorldsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListFleetsResponseTypeDef = TypedDict(
    "ListFleetsResponseTypeDef",
    {
        "fleetDetails": List[FleetTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef = TypedDict(
    "ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFleetsRequestListFleetsPaginateTypeDef = TypedDict(
    "ListFleetsRequestListFleetsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef = TypedDict(
    "ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef",
    {
        "versionQualifier": str,
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRobotsRequestListRobotsPaginateTypeDef = TypedDict(
    "ListRobotsRequestListRobotsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef = TypedDict(
    "ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef",
    {
        "versionQualifier": str,
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef = TypedDict(
    "ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSimulationJobsRequestListSimulationJobsPaginateTypeDef = TypedDict(
    "ListSimulationJobsRequestListSimulationJobsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef = TypedDict(
    "ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef = TypedDict(
    "ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef = TypedDict(
    "ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorldsRequestListWorldsPaginateTypeDef = TypedDict(
    "ListWorldsRequestListWorldsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSimulationJobBatchesResponseTypeDef = TypedDict(
    "ListSimulationJobBatchesResponseTypeDef",
    {
        "simulationJobBatchSummaries": List[SimulationJobBatchSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorldTemplatesResponseTypeDef = TypedDict(
    "ListWorldTemplatesResponseTypeDef",
    {
        "templateSummaries": List[TemplateSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorldsResponseTypeDef = TypedDict(
    "ListWorldsResponseTypeDef",
    {
        "worldSummaries": List[WorldSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PortForwardingConfigTypeDef = TypedDict(
    "PortForwardingConfigTypeDef",
    {
        "portMappings": List[PortMappingTypeDef],
    },
    total=False,
)

RobotDeploymentTypeDef = TypedDict(
    "RobotDeploymentTypeDef",
    {
        "arn": str,
        "deploymentStartTime": datetime,
        "deploymentFinishTime": datetime,
        "status": RobotStatusType,
        "progressDetail": ProgressDetailTypeDef,
        "failureReason": str,
        "failureCode": DeploymentJobErrorCodeType,
    },
    total=False,
)

ListRobotApplicationsResponseTypeDef = TypedDict(
    "ListRobotApplicationsResponseTypeDef",
    {
        "robotApplicationSummaries": List[RobotApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSimulationApplicationsResponseTypeDef = TypedDict(
    "ListSimulationApplicationsResponseTypeDef",
    {
        "simulationApplicationSummaries": List[SimulationApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorldExportJobsResponseTypeDef = TypedDict(
    "ListWorldExportJobsResponseTypeDef",
    {
        "worldExportJobSummaries": List[WorldExportJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorldGenerationJobsResponseTypeDef = TypedDict(
    "ListWorldGenerationJobsResponseTypeDef",
    {
        "worldGenerationJobSummaries": List[WorldGenerationJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDeploymentJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentJobRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "fleet": str,
        "deploymentApplicationConfigs": Sequence[DeploymentApplicationConfigTypeDef],
    },
)
_OptionalCreateDeploymentJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentJobRequestRequestTypeDef",
    {
        "deploymentConfig": DeploymentConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateDeploymentJobRequestRequestTypeDef(
    _RequiredCreateDeploymentJobRequestRequestTypeDef,
    _OptionalCreateDeploymentJobRequestRequestTypeDef,
):
    pass

CreateDeploymentJobResponseTypeDef = TypedDict(
    "CreateDeploymentJobResponseTypeDef",
    {
        "arn": str,
        "fleet": str,
        "status": DeploymentStatusType,
        "deploymentApplicationConfigs": List[DeploymentApplicationConfigTypeDef],
        "failureReason": str,
        "failureCode": DeploymentJobErrorCodeType,
        "createdAt": datetime,
        "deploymentConfig": DeploymentConfigTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentJobTypeDef = TypedDict(
    "DeploymentJobTypeDef",
    {
        "arn": str,
        "fleet": str,
        "status": DeploymentStatusType,
        "deploymentApplicationConfigs": List[DeploymentApplicationConfigTypeDef],
        "deploymentConfig": DeploymentConfigTypeDef,
        "failureReason": str,
        "failureCode": DeploymentJobErrorCodeType,
        "createdAt": datetime,
    },
    total=False,
)

SyncDeploymentJobResponseTypeDef = TypedDict(
    "SyncDeploymentJobResponseTypeDef",
    {
        "arn": str,
        "fleet": str,
        "status": DeploymentStatusType,
        "deploymentConfig": DeploymentConfigTypeDef,
        "deploymentApplicationConfigs": List[DeploymentApplicationConfigTypeDef],
        "failureReason": str,
        "failureCode": DeploymentJobErrorCodeType,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FinishedWorldsSummaryTypeDef = TypedDict(
    "FinishedWorldsSummaryTypeDef",
    {
        "finishedCount": int,
        "succeededWorlds": List[str],
        "failureSummary": FailureSummaryTypeDef,
    },
    total=False,
)

LaunchConfigTypeDef = TypedDict(
    "LaunchConfigTypeDef",
    {
        "packageName": str,
        "launchFile": str,
        "environmentVariables": Dict[str, str],
        "portForwardingConfig": PortForwardingConfigTypeDef,
        "streamUI": bool,
        "command": List[str],
    },
    total=False,
)

DescribeDeploymentJobResponseTypeDef = TypedDict(
    "DescribeDeploymentJobResponseTypeDef",
    {
        "arn": str,
        "fleet": str,
        "status": DeploymentStatusType,
        "deploymentConfig": DeploymentConfigTypeDef,
        "deploymentApplicationConfigs": List[DeploymentApplicationConfigTypeDef],
        "failureReason": str,
        "failureCode": DeploymentJobErrorCodeType,
        "createdAt": datetime,
        "robotDeploymentSummary": List[RobotDeploymentTypeDef],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentJobsResponseTypeDef = TypedDict(
    "ListDeploymentJobsResponseTypeDef",
    {
        "deploymentJobs": List[DeploymentJobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorldGenerationJobResponseTypeDef = TypedDict(
    "DescribeWorldGenerationJobResponseTypeDef",
    {
        "arn": str,
        "status": WorldGenerationJobStatusType,
        "createdAt": datetime,
        "failureCode": WorldGenerationJobErrorCodeType,
        "failureReason": str,
        "clientRequestToken": str,
        "template": str,
        "worldCount": WorldCountTypeDef,
        "finishedWorldsSummary": FinishedWorldsSummaryTypeDef,
        "tags": Dict[str, str],
        "worldTags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRobotApplicationConfigTypeDef = TypedDict(
    "_RequiredRobotApplicationConfigTypeDef",
    {
        "application": str,
        "launchConfig": LaunchConfigTypeDef,
    },
)
_OptionalRobotApplicationConfigTypeDef = TypedDict(
    "_OptionalRobotApplicationConfigTypeDef",
    {
        "applicationVersion": str,
        "uploadConfigurations": List[UploadConfigurationTypeDef],
        "useDefaultUploadConfigurations": bool,
        "tools": List[ToolTypeDef],
        "useDefaultTools": bool,
    },
    total=False,
)

class RobotApplicationConfigTypeDef(
    _RequiredRobotApplicationConfigTypeDef, _OptionalRobotApplicationConfigTypeDef
):
    pass

_RequiredSimulationApplicationConfigTypeDef = TypedDict(
    "_RequiredSimulationApplicationConfigTypeDef",
    {
        "application": str,
        "launchConfig": LaunchConfigTypeDef,
    },
)
_OptionalSimulationApplicationConfigTypeDef = TypedDict(
    "_OptionalSimulationApplicationConfigTypeDef",
    {
        "applicationVersion": str,
        "uploadConfigurations": List[UploadConfigurationTypeDef],
        "worldConfigs": List[WorldConfigTypeDef],
        "useDefaultUploadConfigurations": bool,
        "tools": List[ToolTypeDef],
        "useDefaultTools": bool,
    },
    total=False,
)

class SimulationApplicationConfigTypeDef(
    _RequiredSimulationApplicationConfigTypeDef, _OptionalSimulationApplicationConfigTypeDef
):
    pass

_RequiredCreateSimulationJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSimulationJobRequestRequestTypeDef",
    {
        "maxJobDurationInSeconds": int,
        "iamRole": str,
    },
)
_OptionalCreateSimulationJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSimulationJobRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "outputLocation": OutputLocationTypeDef,
        "loggingConfig": LoggingConfigTypeDef,
        "failureBehavior": FailureBehaviorType,
        "robotApplications": Sequence[RobotApplicationConfigTypeDef],
        "simulationApplications": Sequence[SimulationApplicationConfigTypeDef],
        "dataSources": Sequence[DataSourceConfigTypeDef],
        "tags": Mapping[str, str],
        "vpcConfig": VPCConfigTypeDef,
        "compute": ComputeTypeDef,
    },
    total=False,
)

class CreateSimulationJobRequestRequestTypeDef(
    _RequiredCreateSimulationJobRequestRequestTypeDef,
    _OptionalCreateSimulationJobRequestRequestTypeDef,
):
    pass

CreateSimulationJobResponseTypeDef = TypedDict(
    "CreateSimulationJobResponseTypeDef",
    {
        "arn": str,
        "status": SimulationJobStatusType,
        "lastStartedAt": datetime,
        "lastUpdatedAt": datetime,
        "failureBehavior": FailureBehaviorType,
        "failureCode": SimulationJobErrorCodeType,
        "clientRequestToken": str,
        "outputLocation": OutputLocationTypeDef,
        "loggingConfig": LoggingConfigTypeDef,
        "maxJobDurationInSeconds": int,
        "simulationTimeMillis": int,
        "iamRole": str,
        "robotApplications": List[RobotApplicationConfigTypeDef],
        "simulationApplications": List[SimulationApplicationConfigTypeDef],
        "dataSources": List[DataSourceTypeDef],
        "tags": Dict[str, str],
        "vpcConfig": VPCConfigResponseTypeDef,
        "compute": ComputeResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSimulationJobResponseTypeDef = TypedDict(
    "DescribeSimulationJobResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "status": SimulationJobStatusType,
        "lastStartedAt": datetime,
        "lastUpdatedAt": datetime,
        "failureBehavior": FailureBehaviorType,
        "failureCode": SimulationJobErrorCodeType,
        "failureReason": str,
        "clientRequestToken": str,
        "outputLocation": OutputLocationTypeDef,
        "loggingConfig": LoggingConfigTypeDef,
        "maxJobDurationInSeconds": int,
        "simulationTimeMillis": int,
        "iamRole": str,
        "robotApplications": List[RobotApplicationConfigTypeDef],
        "simulationApplications": List[SimulationApplicationConfigTypeDef],
        "dataSources": List[DataSourceTypeDef],
        "tags": Dict[str, str],
        "vpcConfig": VPCConfigResponseTypeDef,
        "networkInterface": NetworkInterfaceTypeDef,
        "compute": ComputeResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSimulationJobRequestTypeDef = TypedDict(
    "_RequiredSimulationJobRequestTypeDef",
    {
        "maxJobDurationInSeconds": int,
    },
)
_OptionalSimulationJobRequestTypeDef = TypedDict(
    "_OptionalSimulationJobRequestTypeDef",
    {
        "outputLocation": OutputLocationTypeDef,
        "loggingConfig": LoggingConfigTypeDef,
        "iamRole": str,
        "failureBehavior": FailureBehaviorType,
        "useDefaultApplications": bool,
        "robotApplications": List[RobotApplicationConfigTypeDef],
        "simulationApplications": List[SimulationApplicationConfigTypeDef],
        "dataSources": List[DataSourceConfigTypeDef],
        "vpcConfig": VPCConfigTypeDef,
        "compute": ComputeTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class SimulationJobRequestTypeDef(
    _RequiredSimulationJobRequestTypeDef, _OptionalSimulationJobRequestTypeDef
):
    pass

SimulationJobTypeDef = TypedDict(
    "SimulationJobTypeDef",
    {
        "arn": str,
        "name": str,
        "status": SimulationJobStatusType,
        "lastStartedAt": datetime,
        "lastUpdatedAt": datetime,
        "failureBehavior": FailureBehaviorType,
        "failureCode": SimulationJobErrorCodeType,
        "failureReason": str,
        "clientRequestToken": str,
        "outputLocation": OutputLocationTypeDef,
        "loggingConfig": LoggingConfigTypeDef,
        "maxJobDurationInSeconds": int,
        "simulationTimeMillis": int,
        "iamRole": str,
        "robotApplications": List[RobotApplicationConfigTypeDef],
        "simulationApplications": List[SimulationApplicationConfigTypeDef],
        "dataSources": List[DataSourceTypeDef],
        "tags": Dict[str, str],
        "vpcConfig": VPCConfigResponseTypeDef,
        "networkInterface": NetworkInterfaceTypeDef,
        "compute": ComputeResponseTypeDef,
    },
    total=False,
)

FailedCreateSimulationJobRequestTypeDef = TypedDict(
    "FailedCreateSimulationJobRequestTypeDef",
    {
        "request": SimulationJobRequestTypeDef,
        "failureReason": str,
        "failureCode": SimulationJobErrorCodeType,
        "failedAt": datetime,
    },
    total=False,
)

_RequiredStartSimulationJobBatchRequestRequestTypeDef = TypedDict(
    "_RequiredStartSimulationJobBatchRequestRequestTypeDef",
    {
        "createSimulationJobRequests": Sequence[SimulationJobRequestTypeDef],
    },
)
_OptionalStartSimulationJobBatchRequestRequestTypeDef = TypedDict(
    "_OptionalStartSimulationJobBatchRequestRequestTypeDef",
    {
        "clientRequestToken": str,
        "batchPolicy": BatchPolicyTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class StartSimulationJobBatchRequestRequestTypeDef(
    _RequiredStartSimulationJobBatchRequestRequestTypeDef,
    _OptionalStartSimulationJobBatchRequestRequestTypeDef,
):
    pass

BatchDescribeSimulationJobResponseTypeDef = TypedDict(
    "BatchDescribeSimulationJobResponseTypeDef",
    {
        "jobs": List[SimulationJobTypeDef],
        "unprocessedJobs": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSimulationJobBatchResponseTypeDef = TypedDict(
    "DescribeSimulationJobBatchResponseTypeDef",
    {
        "arn": str,
        "status": SimulationJobBatchStatusType,
        "lastUpdatedAt": datetime,
        "createdAt": datetime,
        "clientRequestToken": str,
        "batchPolicy": BatchPolicyTypeDef,
        "failureCode": Literal["InternalServiceError"],
        "failureReason": str,
        "failedRequests": List[FailedCreateSimulationJobRequestTypeDef],
        "pendingRequests": List[SimulationJobRequestTypeDef],
        "createdRequests": List[SimulationJobSummaryTypeDef],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSimulationJobBatchResponseTypeDef = TypedDict(
    "StartSimulationJobBatchResponseTypeDef",
    {
        "arn": str,
        "status": SimulationJobBatchStatusType,
        "createdAt": datetime,
        "clientRequestToken": str,
        "batchPolicy": BatchPolicyTypeDef,
        "failureCode": Literal["InternalServiceError"],
        "failureReason": str,
        "failedRequests": List[FailedCreateSimulationJobRequestTypeDef],
        "pendingRequests": List[SimulationJobRequestTypeDef],
        "createdRequests": List[SimulationJobSummaryTypeDef],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
