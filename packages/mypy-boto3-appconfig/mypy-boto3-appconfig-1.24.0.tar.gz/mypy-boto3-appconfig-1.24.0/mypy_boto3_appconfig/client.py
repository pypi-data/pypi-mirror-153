"""
Type annotations for appconfig service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appconfig.client import AppConfigClient

    session = Session()
    client: AppConfigClient = session.client("appconfig")
    ```
"""
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import GrowthTypeType, ReplicateToType
from .type_defs import (
    ApplicationResponseMetadataTypeDef,
    ApplicationsTypeDef,
    ConfigurationProfilesTypeDef,
    ConfigurationProfileTypeDef,
    ConfigurationTypeDef,
    DeploymentStrategiesTypeDef,
    DeploymentStrategyResponseMetadataTypeDef,
    DeploymentsTypeDef,
    DeploymentTypeDef,
    EmptyResponseMetadataTypeDef,
    EnvironmentResponseMetadataTypeDef,
    EnvironmentsTypeDef,
    HostedConfigurationVersionsTypeDef,
    HostedConfigurationVersionTypeDef,
    MonitorTypeDef,
    ResourceTagsTypeDef,
    ValidatorTypeDef,
)

__all__ = ("AppConfigClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    PayloadTooLargeException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]


class AppConfigClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppConfigClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#can_paginate)
        """

    def create_application(
        self, *, Name: str, Description: str = ..., Tags: Mapping[str, str] = ...
    ) -> ApplicationResponseMetadataTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.create_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#create_application)
        """

    def create_configuration_profile(
        self,
        *,
        ApplicationId: str,
        Name: str,
        LocationUri: str,
        Description: str = ...,
        RetrievalRoleArn: str = ...,
        Validators: Sequence[ValidatorTypeDef] = ...,
        Tags: Mapping[str, str] = ...,
        Type: str = ...
    ) -> ConfigurationProfileTypeDef:
        """
        Creates a configuration profile, which is information that enables AppConfig to
        access the configuration source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.create_configuration_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#create_configuration_profile)
        """

    def create_deployment_strategy(
        self,
        *,
        Name: str,
        DeploymentDurationInMinutes: int,
        GrowthFactor: float,
        ReplicateTo: ReplicateToType,
        Description: str = ...,
        FinalBakeTimeInMinutes: int = ...,
        GrowthType: GrowthTypeType = ...,
        Tags: Mapping[str, str] = ...
    ) -> DeploymentStrategyResponseMetadataTypeDef:
        """
        Creates a deployment strategy that defines important criteria for rolling out
        your configuration to the designated targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.create_deployment_strategy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#create_deployment_strategy)
        """

    def create_environment(
        self,
        *,
        ApplicationId: str,
        Name: str,
        Description: str = ...,
        Monitors: Sequence[MonitorTypeDef] = ...,
        Tags: Mapping[str, str] = ...
    ) -> EnvironmentResponseMetadataTypeDef:
        """
        Creates an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.create_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#create_environment)
        """

    def create_hosted_configuration_version(
        self,
        *,
        ApplicationId: str,
        ConfigurationProfileId: str,
        Content: Union[str, bytes, IO[Any], StreamingBody],
        ContentType: str,
        Description: str = ...,
        LatestVersionNumber: int = ...
    ) -> HostedConfigurationVersionTypeDef:
        """
        Creates a new configuration in the AppConfig hosted configuration store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.create_hosted_configuration_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#create_hosted_configuration_version)
        """

    def delete_application(self, *, ApplicationId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.delete_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#delete_application)
        """

    def delete_configuration_profile(
        self, *, ApplicationId: str, ConfigurationProfileId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a configuration profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.delete_configuration_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#delete_configuration_profile)
        """

    def delete_deployment_strategy(
        self, *, DeploymentStrategyId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a deployment strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.delete_deployment_strategy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#delete_deployment_strategy)
        """

    def delete_environment(
        self, *, ApplicationId: str, EnvironmentId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.delete_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#delete_environment)
        """

    def delete_hosted_configuration_version(
        self, *, ApplicationId: str, ConfigurationProfileId: str, VersionNumber: int
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a version of a configuration from the AppConfig hosted configuration
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.delete_hosted_configuration_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#delete_hosted_configuration_version)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#generate_presigned_url)
        """

    def get_application(self, *, ApplicationId: str) -> ApplicationResponseMetadataTypeDef:
        """
        Retrieves information about an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_application)
        """

    def get_configuration(
        self,
        *,
        Application: str,
        Environment: str,
        Configuration: str,
        ClientId: str,
        ClientConfigurationVersion: str = ...
    ) -> ConfigurationTypeDef:
        """
        Retrieves the latest deployed configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_configuration)
        """

    def get_configuration_profile(
        self, *, ApplicationId: str, ConfigurationProfileId: str
    ) -> ConfigurationProfileTypeDef:
        """
        Retrieves information about a configuration profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_configuration_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_configuration_profile)
        """

    def get_deployment(
        self, *, ApplicationId: str, EnvironmentId: str, DeploymentNumber: int
    ) -> DeploymentTypeDef:
        """
        Retrieves information about a configuration deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_deployment)
        """

    def get_deployment_strategy(
        self, *, DeploymentStrategyId: str
    ) -> DeploymentStrategyResponseMetadataTypeDef:
        """
        Retrieves information about a deployment strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_deployment_strategy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_deployment_strategy)
        """

    def get_environment(
        self, *, ApplicationId: str, EnvironmentId: str
    ) -> EnvironmentResponseMetadataTypeDef:
        """
        Retrieves information about an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_environment)
        """

    def get_hosted_configuration_version(
        self, *, ApplicationId: str, ConfigurationProfileId: str, VersionNumber: int
    ) -> HostedConfigurationVersionTypeDef:
        """
        Retrieves information about a specific configuration version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.get_hosted_configuration_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#get_hosted_configuration_version)
        """

    def list_applications(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ApplicationsTypeDef:
        """
        Lists all applications in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_applications)
        """

    def list_configuration_profiles(
        self, *, ApplicationId: str, MaxResults: int = ..., NextToken: str = ..., Type: str = ...
    ) -> ConfigurationProfilesTypeDef:
        """
        Lists the configuration profiles for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_configuration_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_configuration_profiles)
        """

    def list_deployment_strategies(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> DeploymentStrategiesTypeDef:
        """
        Lists deployment strategies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_deployment_strategies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_deployment_strategies)
        """

    def list_deployments(
        self, *, ApplicationId: str, EnvironmentId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DeploymentsTypeDef:
        """
        Lists the deployments for an environment in descending deployment number order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_deployments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_deployments)
        """

    def list_environments(
        self, *, ApplicationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> EnvironmentsTypeDef:
        """
        Lists the environments for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_environments)
        """

    def list_hosted_configuration_versions(
        self,
        *,
        ApplicationId: str,
        ConfigurationProfileId: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> HostedConfigurationVersionsTypeDef:
        """
        Lists configurations stored in the AppConfig hosted configuration store by
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_hosted_configuration_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_hosted_configuration_versions)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ResourceTagsTypeDef:
        """
        Retrieves the list of key-value tags assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#list_tags_for_resource)
        """

    def start_deployment(
        self,
        *,
        ApplicationId: str,
        EnvironmentId: str,
        DeploymentStrategyId: str,
        ConfigurationProfileId: str,
        ConfigurationVersion: str,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> DeploymentTypeDef:
        """
        Starts a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.start_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#start_deployment)
        """

    def stop_deployment(
        self, *, ApplicationId: str, EnvironmentId: str, DeploymentNumber: int
    ) -> DeploymentTypeDef:
        """
        Stops a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.stop_deployment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#stop_deployment)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns metadata to an AppConfig resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a tag key and value from an AppConfig resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#untag_resource)
        """

    def update_application(
        self, *, ApplicationId: str, Name: str = ..., Description: str = ...
    ) -> ApplicationResponseMetadataTypeDef:
        """
        Updates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.update_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#update_application)
        """

    def update_configuration_profile(
        self,
        *,
        ApplicationId: str,
        ConfigurationProfileId: str,
        Name: str = ...,
        Description: str = ...,
        RetrievalRoleArn: str = ...,
        Validators: Sequence[ValidatorTypeDef] = ...
    ) -> ConfigurationProfileTypeDef:
        """
        Updates a configuration profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.update_configuration_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#update_configuration_profile)
        """

    def update_deployment_strategy(
        self,
        *,
        DeploymentStrategyId: str,
        Description: str = ...,
        DeploymentDurationInMinutes: int = ...,
        FinalBakeTimeInMinutes: int = ...,
        GrowthFactor: float = ...,
        GrowthType: GrowthTypeType = ...
    ) -> DeploymentStrategyResponseMetadataTypeDef:
        """
        Updates a deployment strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.update_deployment_strategy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#update_deployment_strategy)
        """

    def update_environment(
        self,
        *,
        ApplicationId: str,
        EnvironmentId: str,
        Name: str = ...,
        Description: str = ...,
        Monitors: Sequence[MonitorTypeDef] = ...
    ) -> EnvironmentResponseMetadataTypeDef:
        """
        Updates an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.update_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#update_environment)
        """

    def validate_configuration(
        self, *, ApplicationId: str, ConfigurationProfileId: str, ConfigurationVersion: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Uses the validators in a configuration profile to validate a configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig.Client.validate_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/client/#validate_configuration)
        """
