"""
Type annotations for appconfig service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/type_defs/)

Usage::

    ```python
    from mypy_boto3_appconfig.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DeploymentEventTypeType,
    DeploymentStateType,
    EnvironmentStateType,
    GrowthTypeType,
    ReplicateToType,
    TriggeredByType,
    ValidatorTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "ApplicationTypeDef",
    "ConfigurationProfileSummaryTypeDef",
    "ValidatorTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateDeploymentStrategyRequestRequestTypeDef",
    "MonitorTypeDef",
    "CreateHostedConfigurationVersionRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteConfigurationProfileRequestRequestTypeDef",
    "DeleteDeploymentStrategyRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteHostedConfigurationVersionRequestRequestTypeDef",
    "DeploymentEventTypeDef",
    "DeploymentStrategyTypeDef",
    "DeploymentSummaryTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetConfigurationProfileRequestRequestTypeDef",
    "GetConfigurationRequestRequestTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetDeploymentStrategyRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetHostedConfigurationVersionRequestRequestTypeDef",
    "HostedConfigurationVersionSummaryTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListConfigurationProfilesRequestRequestTypeDef",
    "ListDeploymentStrategiesRequestRequestTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListHostedConfigurationVersionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StopDeploymentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateDeploymentStrategyRequestRequestTypeDef",
    "ValidateConfigurationRequestRequestTypeDef",
    "ApplicationResponseMetadataTypeDef",
    "ConfigurationTypeDef",
    "DeploymentStrategyResponseMetadataTypeDef",
    "EmptyResponseMetadataTypeDef",
    "HostedConfigurationVersionTypeDef",
    "ResourceTagsTypeDef",
    "ApplicationsTypeDef",
    "ConfigurationProfilesTypeDef",
    "ConfigurationProfileTypeDef",
    "CreateConfigurationProfileRequestRequestTypeDef",
    "UpdateConfigurationProfileRequestRequestTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "EnvironmentResponseMetadataTypeDef",
    "EnvironmentTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "DeploymentTypeDef",
    "DeploymentStrategiesTypeDef",
    "DeploymentsTypeDef",
    "HostedConfigurationVersionsTypeDef",
    "EnvironmentsTypeDef",
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

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
    },
    total=False,
)

ConfigurationProfileSummaryTypeDef = TypedDict(
    "ConfigurationProfileSummaryTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
        "LocationUri": str,
        "ValidatorTypes": List[ValidatorTypeType],
        "Type": str,
    },
    total=False,
)

ValidatorTypeDef = TypedDict(
    "ValidatorTypeDef",
    {
        "Type": ValidatorTypeType,
        "Content": str,
    },
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredCreateDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentStrategyRequestRequestTypeDef",
    {
        "Name": str,
        "DeploymentDurationInMinutes": int,
        "GrowthFactor": float,
        "ReplicateTo": ReplicateToType,
    },
)
_OptionalCreateDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentStrategyRequestRequestTypeDef",
    {
        "Description": str,
        "FinalBakeTimeInMinutes": int,
        "GrowthType": GrowthTypeType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateDeploymentStrategyRequestRequestTypeDef(
    _RequiredCreateDeploymentStrategyRequestRequestTypeDef,
    _OptionalCreateDeploymentStrategyRequestRequestTypeDef,
):
    pass


_RequiredMonitorTypeDef = TypedDict(
    "_RequiredMonitorTypeDef",
    {
        "AlarmArn": str,
    },
)
_OptionalMonitorTypeDef = TypedDict(
    "_OptionalMonitorTypeDef",
    {
        "AlarmRoleArn": str,
    },
    total=False,
)


class MonitorTypeDef(_RequiredMonitorTypeDef, _OptionalMonitorTypeDef):
    pass


_RequiredCreateHostedConfigurationVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHostedConfigurationVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "Content": Union[str, bytes, IO[Any], StreamingBody],
        "ContentType": str,
    },
)
_OptionalCreateHostedConfigurationVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHostedConfigurationVersionRequestRequestTypeDef",
    {
        "Description": str,
        "LatestVersionNumber": int,
    },
    total=False,
)


class CreateHostedConfigurationVersionRequestRequestTypeDef(
    _RequiredCreateHostedConfigurationVersionRequestRequestTypeDef,
    _OptionalCreateHostedConfigurationVersionRequestRequestTypeDef,
):
    pass


DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

DeleteConfigurationProfileRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationProfileRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
    },
)

DeleteDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "DeleteDeploymentStrategyRequestRequestTypeDef",
    {
        "DeploymentStrategyId": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
    },
)

DeleteHostedConfigurationVersionRequestRequestTypeDef = TypedDict(
    "DeleteHostedConfigurationVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "VersionNumber": int,
    },
)

DeploymentEventTypeDef = TypedDict(
    "DeploymentEventTypeDef",
    {
        "EventType": DeploymentEventTypeType,
        "TriggeredBy": TriggeredByType,
        "Description": str,
        "OccurredAt": datetime,
    },
    total=False,
)

DeploymentStrategyTypeDef = TypedDict(
    "DeploymentStrategyTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "DeploymentDurationInMinutes": int,
        "GrowthType": GrowthTypeType,
        "GrowthFactor": float,
        "FinalBakeTimeInMinutes": int,
        "ReplicateTo": ReplicateToType,
    },
    total=False,
)

DeploymentSummaryTypeDef = TypedDict(
    "DeploymentSummaryTypeDef",
    {
        "DeploymentNumber": int,
        "ConfigurationName": str,
        "ConfigurationVersion": str,
        "DeploymentDurationInMinutes": int,
        "GrowthType": GrowthTypeType,
        "GrowthFactor": float,
        "FinalBakeTimeInMinutes": int,
        "State": DeploymentStateType,
        "PercentageComplete": float,
        "StartedAt": datetime,
        "CompletedAt": datetime,
    },
    total=False,
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)

GetConfigurationProfileRequestRequestTypeDef = TypedDict(
    "GetConfigurationProfileRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
    },
)

_RequiredGetConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetConfigurationRequestRequestTypeDef",
    {
        "Application": str,
        "Environment": str,
        "Configuration": str,
        "ClientId": str,
    },
)
_OptionalGetConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetConfigurationRequestRequestTypeDef",
    {
        "ClientConfigurationVersion": str,
    },
    total=False,
)


class GetConfigurationRequestRequestTypeDef(
    _RequiredGetConfigurationRequestRequestTypeDef, _OptionalGetConfigurationRequestRequestTypeDef
):
    pass


GetDeploymentRequestRequestTypeDef = TypedDict(
    "GetDeploymentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
        "DeploymentNumber": int,
    },
)

GetDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "GetDeploymentStrategyRequestRequestTypeDef",
    {
        "DeploymentStrategyId": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
    },
)

GetHostedConfigurationVersionRequestRequestTypeDef = TypedDict(
    "GetHostedConfigurationVersionRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "VersionNumber": int,
    },
)

HostedConfigurationVersionSummaryTypeDef = TypedDict(
    "HostedConfigurationVersionSummaryTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "VersionNumber": int,
        "Description": str,
        "ContentType": str,
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListConfigurationProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListConfigurationProfilesRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListConfigurationProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListConfigurationProfilesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Type": str,
    },
    total=False,
)


class ListConfigurationProfilesRequestRequestTypeDef(
    _RequiredListConfigurationProfilesRequestRequestTypeDef,
    _OptionalListConfigurationProfilesRequestRequestTypeDef,
):
    pass


ListDeploymentStrategiesRequestRequestTypeDef = TypedDict(
    "ListDeploymentStrategiesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredListDeploymentsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
    },
)
_OptionalListDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalListDeploymentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListDeploymentsRequestRequestTypeDef(
    _RequiredListDeploymentsRequestRequestTypeDef, _OptionalListDeploymentsRequestRequestTypeDef
):
    pass


_RequiredListEnvironmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentsRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalListEnvironmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListEnvironmentsRequestRequestTypeDef(
    _RequiredListEnvironmentsRequestRequestTypeDef, _OptionalListEnvironmentsRequestRequestTypeDef
):
    pass


_RequiredListHostedConfigurationVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListHostedConfigurationVersionsRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
    },
)
_OptionalListHostedConfigurationVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListHostedConfigurationVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListHostedConfigurationVersionsRequestRequestTypeDef(
    _RequiredListHostedConfigurationVersionsRequestRequestTypeDef,
    _OptionalListHostedConfigurationVersionsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredStartDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredStartDeploymentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
        "DeploymentStrategyId": str,
        "ConfigurationProfileId": str,
        "ConfigurationVersion": str,
    },
)
_OptionalStartDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalStartDeploymentRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class StartDeploymentRequestRequestTypeDef(
    _RequiredStartDeploymentRequestRequestTypeDef, _OptionalStartDeploymentRequestRequestTypeDef
):
    pass


StopDeploymentRequestRequestTypeDef = TypedDict(
    "StopDeploymentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
        "DeploymentNumber": int,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "ApplicationId": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDeploymentStrategyRequestRequestTypeDef",
    {
        "DeploymentStrategyId": str,
    },
)
_OptionalUpdateDeploymentStrategyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDeploymentStrategyRequestRequestTypeDef",
    {
        "Description": str,
        "DeploymentDurationInMinutes": int,
        "FinalBakeTimeInMinutes": int,
        "GrowthFactor": float,
        "GrowthType": GrowthTypeType,
    },
    total=False,
)


class UpdateDeploymentStrategyRequestRequestTypeDef(
    _RequiredUpdateDeploymentStrategyRequestRequestTypeDef,
    _OptionalUpdateDeploymentStrategyRequestRequestTypeDef,
):
    pass


ValidateConfigurationRequestRequestTypeDef = TypedDict(
    "ValidateConfigurationRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "ConfigurationVersion": str,
    },
)

ApplicationResponseMetadataTypeDef = TypedDict(
    "ApplicationResponseMetadataTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Content": StreamingBody,
        "ConfigurationVersion": str,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentStrategyResponseMetadataTypeDef = TypedDict(
    "DeploymentStrategyResponseMetadataTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "DeploymentDurationInMinutes": int,
        "GrowthType": GrowthTypeType,
        "GrowthFactor": float,
        "FinalBakeTimeInMinutes": int,
        "ReplicateTo": ReplicateToType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HostedConfigurationVersionTypeDef = TypedDict(
    "HostedConfigurationVersionTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
        "VersionNumber": int,
        "Description": str,
        "Content": StreamingBody,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResourceTagsTypeDef = TypedDict(
    "ResourceTagsTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ApplicationsTypeDef = TypedDict(
    "ApplicationsTypeDef",
    {
        "Items": List[ApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigurationProfilesTypeDef = TypedDict(
    "ConfigurationProfilesTypeDef",
    {
        "Items": List[ConfigurationProfileSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConfigurationProfileTypeDef = TypedDict(
    "ConfigurationProfileTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "LocationUri": str,
        "RetrievalRoleArn": str,
        "Validators": List[ValidatorTypeDef],
        "Type": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateConfigurationProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConfigurationProfileRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Name": str,
        "LocationUri": str,
    },
)
_OptionalCreateConfigurationProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConfigurationProfileRequestRequestTypeDef",
    {
        "Description": str,
        "RetrievalRoleArn": str,
        "Validators": Sequence[ValidatorTypeDef],
        "Tags": Mapping[str, str],
        "Type": str,
    },
    total=False,
)


class CreateConfigurationProfileRequestRequestTypeDef(
    _RequiredCreateConfigurationProfileRequestRequestTypeDef,
    _OptionalCreateConfigurationProfileRequestRequestTypeDef,
):
    pass


_RequiredUpdateConfigurationProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConfigurationProfileRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationProfileId": str,
    },
)
_OptionalUpdateConfigurationProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConfigurationProfileRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "RetrievalRoleArn": str,
        "Validators": Sequence[ValidatorTypeDef],
    },
    total=False,
)


class UpdateConfigurationProfileRequestRequestTypeDef(
    _RequiredUpdateConfigurationProfileRequestRequestTypeDef,
    _OptionalUpdateConfigurationProfileRequestRequestTypeDef,
):
    pass


_RequiredCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Name": str,
    },
)
_OptionalCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentRequestRequestTypeDef",
    {
        "Description": str,
        "Monitors": Sequence[MonitorTypeDef],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateEnvironmentRequestRequestTypeDef(
    _RequiredCreateEnvironmentRequestRequestTypeDef, _OptionalCreateEnvironmentRequestRequestTypeDef
):
    pass


EnvironmentResponseMetadataTypeDef = TypedDict(
    "EnvironmentResponseMetadataTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "State": EnvironmentStateType,
        "Monitors": List[MonitorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "State": EnvironmentStateType,
        "Monitors": List[MonitorTypeDef],
    },
    total=False,
)

_RequiredUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
    },
)
_OptionalUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Monitors": Sequence[MonitorTypeDef],
    },
    total=False,
)


class UpdateEnvironmentRequestRequestTypeDef(
    _RequiredUpdateEnvironmentRequestRequestTypeDef, _OptionalUpdateEnvironmentRequestRequestTypeDef
):
    pass


DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "ApplicationId": str,
        "EnvironmentId": str,
        "DeploymentStrategyId": str,
        "ConfigurationProfileId": str,
        "DeploymentNumber": int,
        "ConfigurationName": str,
        "ConfigurationLocationUri": str,
        "ConfigurationVersion": str,
        "Description": str,
        "DeploymentDurationInMinutes": int,
        "GrowthType": GrowthTypeType,
        "GrowthFactor": float,
        "FinalBakeTimeInMinutes": int,
        "State": DeploymentStateType,
        "EventLog": List[DeploymentEventTypeDef],
        "PercentageComplete": float,
        "StartedAt": datetime,
        "CompletedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentStrategiesTypeDef = TypedDict(
    "DeploymentStrategiesTypeDef",
    {
        "Items": List[DeploymentStrategyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeploymentsTypeDef = TypedDict(
    "DeploymentsTypeDef",
    {
        "Items": List[DeploymentSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HostedConfigurationVersionsTypeDef = TypedDict(
    "HostedConfigurationVersionsTypeDef",
    {
        "Items": List[HostedConfigurationVersionSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnvironmentsTypeDef = TypedDict(
    "EnvironmentsTypeDef",
    {
        "Items": List[EnvironmentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
