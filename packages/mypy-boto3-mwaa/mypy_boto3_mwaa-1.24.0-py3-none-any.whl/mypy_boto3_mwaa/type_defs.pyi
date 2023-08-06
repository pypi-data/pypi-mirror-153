"""
Type annotations for mwaa service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mwaa/type_defs/)

Usage::

    ```python
    from mypy_boto3_mwaa.type_defs import CreateCliTokenRequestRequestTypeDef

    data: CreateCliTokenRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EnvironmentStatusType,
    LoggingLevelType,
    UnitType,
    UpdateStatusType,
    WebserverAccessModeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CreateCliTokenRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "NetworkConfigurationTypeDef",
    "CreateWebLoginTokenRequestRequestTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DimensionTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "UpdateErrorTypeDef",
    "PaginatorConfigTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ModuleLoggingConfigurationInputTypeDef",
    "ModuleLoggingConfigurationTypeDef",
    "StatisticSetTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateNetworkConfigurationInputTypeDef",
    "CreateCliTokenResponseTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateWebLoginTokenResponseTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "LastUpdateTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "LoggingConfigurationInputTypeDef",
    "LoggingConfigurationTypeDef",
    "MetricDatumTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "EnvironmentTypeDef",
    "PublishMetricsInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
)

CreateCliTokenRequestRequestTypeDef = TypedDict(
    "CreateCliTokenRequestRequestTypeDef",
    {
        "Name": str,
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

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
    },
    total=False,
)

CreateWebLoginTokenRequestRequestTypeDef = TypedDict(
    "CreateWebLoginTokenRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteEnvironmentInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentInputRequestTypeDef",
    {
        "Name": str,
    },
)

DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

GetEnvironmentInputRequestTypeDef = TypedDict(
    "GetEnvironmentInputRequestTypeDef",
    {
        "Name": str,
    },
)

UpdateErrorTypeDef = TypedDict(
    "UpdateErrorTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
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

ListEnvironmentsInputRequestTypeDef = TypedDict(
    "ListEnvironmentsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ModuleLoggingConfigurationInputTypeDef = TypedDict(
    "ModuleLoggingConfigurationInputTypeDef",
    {
        "Enabled": bool,
        "LogLevel": LoggingLevelType,
    },
)

ModuleLoggingConfigurationTypeDef = TypedDict(
    "ModuleLoggingConfigurationTypeDef",
    {
        "CloudWatchLogGroupArn": str,
        "Enabled": bool,
        "LogLevel": LoggingLevelType,
    },
    total=False,
)

StatisticSetTypeDef = TypedDict(
    "StatisticSetTypeDef",
    {
        "Maximum": float,
        "Minimum": float,
        "SampleCount": int,
        "Sum": float,
    },
    total=False,
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateNetworkConfigurationInputTypeDef = TypedDict(
    "UpdateNetworkConfigurationInputTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
    },
)

CreateCliTokenResponseTypeDef = TypedDict(
    "CreateCliTokenResponseTypeDef",
    {
        "CliToken": str,
        "WebServerHostname": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWebLoginTokenResponseTypeDef = TypedDict(
    "CreateWebLoginTokenResponseTypeDef",
    {
        "WebServerHostname": str,
        "WebToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsOutputTypeDef = TypedDict(
    "ListEnvironmentsOutputTypeDef",
    {
        "Environments": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LastUpdateTypeDef = TypedDict(
    "LastUpdateTypeDef",
    {
        "CreatedAt": datetime,
        "Error": UpdateErrorTypeDef,
        "Source": str,
        "Status": UpdateStatusType,
    },
    total=False,
)

ListEnvironmentsInputListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

LoggingConfigurationInputTypeDef = TypedDict(
    "LoggingConfigurationInputTypeDef",
    {
        "DagProcessingLogs": ModuleLoggingConfigurationInputTypeDef,
        "SchedulerLogs": ModuleLoggingConfigurationInputTypeDef,
        "TaskLogs": ModuleLoggingConfigurationInputTypeDef,
        "WebserverLogs": ModuleLoggingConfigurationInputTypeDef,
        "WorkerLogs": ModuleLoggingConfigurationInputTypeDef,
    },
    total=False,
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef",
    {
        "DagProcessingLogs": ModuleLoggingConfigurationTypeDef,
        "SchedulerLogs": ModuleLoggingConfigurationTypeDef,
        "TaskLogs": ModuleLoggingConfigurationTypeDef,
        "WebserverLogs": ModuleLoggingConfigurationTypeDef,
        "WorkerLogs": ModuleLoggingConfigurationTypeDef,
    },
    total=False,
)

_RequiredMetricDatumTypeDef = TypedDict(
    "_RequiredMetricDatumTypeDef",
    {
        "MetricName": str,
        "Timestamp": Union[datetime, str],
    },
)
_OptionalMetricDatumTypeDef = TypedDict(
    "_OptionalMetricDatumTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "StatisticValues": StatisticSetTypeDef,
        "Unit": UnitType,
        "Value": float,
    },
    total=False,
)

class MetricDatumTypeDef(_RequiredMetricDatumTypeDef, _OptionalMetricDatumTypeDef):
    pass

_RequiredCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentInputRequestTypeDef",
    {
        "DagS3Path": str,
        "ExecutionRoleArn": str,
        "Name": str,
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "SourceBucketArn": str,
    },
)
_OptionalCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentInputRequestTypeDef",
    {
        "AirflowConfigurationOptions": Mapping[str, str],
        "AirflowVersion": str,
        "EnvironmentClass": str,
        "KmsKey": str,
        "LoggingConfiguration": LoggingConfigurationInputTypeDef,
        "MaxWorkers": int,
        "MinWorkers": int,
        "PluginsS3ObjectVersion": str,
        "PluginsS3Path": str,
        "RequirementsS3ObjectVersion": str,
        "RequirementsS3Path": str,
        "Schedulers": int,
        "Tags": Mapping[str, str],
        "WebserverAccessMode": WebserverAccessModeType,
        "WeeklyMaintenanceWindowStart": str,
    },
    total=False,
)

class CreateEnvironmentInputRequestTypeDef(
    _RequiredCreateEnvironmentInputRequestTypeDef, _OptionalCreateEnvironmentInputRequestTypeDef
):
    pass

_RequiredUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentInputRequestTypeDef",
    {
        "AirflowConfigurationOptions": Mapping[str, str],
        "AirflowVersion": str,
        "DagS3Path": str,
        "EnvironmentClass": str,
        "ExecutionRoleArn": str,
        "LoggingConfiguration": LoggingConfigurationInputTypeDef,
        "MaxWorkers": int,
        "MinWorkers": int,
        "NetworkConfiguration": UpdateNetworkConfigurationInputTypeDef,
        "PluginsS3ObjectVersion": str,
        "PluginsS3Path": str,
        "RequirementsS3ObjectVersion": str,
        "RequirementsS3Path": str,
        "Schedulers": int,
        "SourceBucketArn": str,
        "WebserverAccessMode": WebserverAccessModeType,
        "WeeklyMaintenanceWindowStart": str,
    },
    total=False,
)

class UpdateEnvironmentInputRequestTypeDef(
    _RequiredUpdateEnvironmentInputRequestTypeDef, _OptionalUpdateEnvironmentInputRequestTypeDef
):
    pass

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "AirflowConfigurationOptions": Dict[str, str],
        "AirflowVersion": str,
        "Arn": str,
        "CreatedAt": datetime,
        "DagS3Path": str,
        "EnvironmentClass": str,
        "ExecutionRoleArn": str,
        "KmsKey": str,
        "LastUpdate": LastUpdateTypeDef,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "MaxWorkers": int,
        "MinWorkers": int,
        "Name": str,
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "PluginsS3ObjectVersion": str,
        "PluginsS3Path": str,
        "RequirementsS3ObjectVersion": str,
        "RequirementsS3Path": str,
        "Schedulers": int,
        "ServiceRoleArn": str,
        "SourceBucketArn": str,
        "Status": EnvironmentStatusType,
        "Tags": Dict[str, str],
        "WebserverAccessMode": WebserverAccessModeType,
        "WebserverUrl": str,
        "WeeklyMaintenanceWindowStart": str,
    },
    total=False,
)

PublishMetricsInputRequestTypeDef = TypedDict(
    "PublishMetricsInputRequestTypeDef",
    {
        "EnvironmentName": str,
        "MetricData": Sequence[MetricDatumTypeDef],
    },
)

GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "Environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
