"""
Type annotations for mq service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mq.client import MQClient

    session = Session()
    client: MQClient = session.client("mq")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AuthenticationStrategyType,
    BrokerStorageTypeType,
    DeploymentModeType,
    EngineTypeType,
)
from .paginator import ListBrokersPaginator
from .type_defs import (
    ConfigurationIdTypeDef,
    CreateBrokerResponseTypeDef,
    CreateConfigurationResponseTypeDef,
    DeleteBrokerResponseTypeDef,
    DescribeBrokerEngineTypesResponseTypeDef,
    DescribeBrokerInstanceOptionsResponseTypeDef,
    DescribeBrokerResponseTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeUserResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionOptionsTypeDef,
    LdapServerMetadataInputTypeDef,
    ListBrokersResponseTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsResponseTypeDef,
    ListTagsResponseTypeDef,
    ListUsersResponseTypeDef,
    LogsTypeDef,
    UpdateBrokerResponseTypeDef,
    UpdateConfigurationResponseTypeDef,
    UserTypeDef,
    WeeklyStartTimeTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MQClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class MQClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MQClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#can_paginate)
        """

    def create_broker(
        self,
        *,
        AutoMinorVersionUpgrade: bool,
        BrokerName: str,
        DeploymentMode: DeploymentModeType,
        EngineType: EngineTypeType,
        EngineVersion: str,
        HostInstanceType: str,
        PubliclyAccessible: bool,
        Users: Sequence[UserTypeDef],
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        Configuration: ConfigurationIdTypeDef = ...,
        CreatorRequestId: str = ...,
        EncryptionOptions: EncryptionOptionsTypeDef = ...,
        LdapServerMetadata: LdapServerMetadataInputTypeDef = ...,
        Logs: LogsTypeDef = ...,
        MaintenanceWindowStartTime: WeeklyStartTimeTypeDef = ...,
        SecurityGroups: Sequence[str] = ...,
        StorageType: BrokerStorageTypeType = ...,
        SubnetIds: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateBrokerResponseTypeDef:
        """
        Creates a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_broker)
        """

    def create_configuration(
        self,
        *,
        EngineType: EngineTypeType,
        EngineVersion: str,
        Name: str,
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new configuration for the specified configuration name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_configuration)
        """

    def create_tags(
        self, *, ResourceArn: str, Tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_tags)
        """

    def create_user(
        self,
        *,
        BrokerId: str,
        Password: str,
        Username: str,
        ConsoleAccess: bool = ...,
        Groups: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Creates an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#create_user)
        """

    def delete_broker(self, *, BrokerId: str) -> DeleteBrokerResponseTypeDef:
        """
        Deletes a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_broker)
        """

    def delete_tags(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_tags)
        """

    def delete_user(self, *, BrokerId: str, Username: str) -> Dict[str, Any]:
        """
        Deletes an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#delete_user)
        """

    def describe_broker(self, *, BrokerId: str) -> DescribeBrokerResponseTypeDef:
        """
        Returns information about the specified broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker)
        """

    def describe_broker_engine_types(
        self, *, EngineType: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeBrokerEngineTypesResponseTypeDef:
        """
        Describe available engine types and versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker_engine_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker_engine_types)
        """

    def describe_broker_instance_options(
        self,
        *,
        EngineType: str = ...,
        HostInstanceType: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        StorageType: str = ...
    ) -> DescribeBrokerInstanceOptionsResponseTypeDef:
        """
        Describe available broker instance options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker_instance_options)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_broker_instance_options)
        """

    def describe_configuration(
        self, *, ConfigurationId: str
    ) -> DescribeConfigurationResponseTypeDef:
        """
        Returns information about the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_configuration)
        """

    def describe_configuration_revision(
        self, *, ConfigurationId: str, ConfigurationRevision: str
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns the specified configuration revision for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_configuration_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_configuration_revision)
        """

    def describe_user(self, *, BrokerId: str, Username: str) -> DescribeUserResponseTypeDef:
        """
        Returns information about an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#describe_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#generate_presigned_url)
        """

    def list_brokers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListBrokersResponseTypeDef:
        """
        Returns a list of all brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_brokers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_brokers)
        """

    def list_configuration_revisions(
        self, *, ConfigurationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all revisions for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_configuration_revisions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_configuration_revisions)
        """

    def list_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_configurations)
        """

    def list_tags(self, *, ResourceArn: str) -> ListTagsResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_tags)
        """

    def list_users(
        self, *, BrokerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Returns a list of all ActiveMQ users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#list_users)
        """

    def reboot_broker(self, *, BrokerId: str) -> Dict[str, Any]:
        """
        Reboots a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.reboot_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#reboot_broker)
        """

    def update_broker(
        self,
        *,
        BrokerId: str,
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Configuration: ConfigurationIdTypeDef = ...,
        EngineVersion: str = ...,
        HostInstanceType: str = ...,
        LdapServerMetadata: LdapServerMetadataInputTypeDef = ...,
        Logs: LogsTypeDef = ...,
        MaintenanceWindowStartTime: WeeklyStartTimeTypeDef = ...,
        SecurityGroups: Sequence[str] = ...
    ) -> UpdateBrokerResponseTypeDef:
        """
        Adds a pending configuration change to a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_broker)
        """

    def update_configuration(
        self, *, ConfigurationId: str, Data: str, Description: str = ...
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_configuration)
        """

    def update_user(
        self,
        *,
        BrokerId: str,
        Username: str,
        ConsoleAccess: bool = ...,
        Groups: Sequence[str] = ...,
        Password: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the information for an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#update_user)
        """

    def get_paginator(self, operation_name: Literal["list_brokers"]) -> ListBrokersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/client/#get_paginator)
        """
