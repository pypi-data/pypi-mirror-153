"""
Type annotations for mq service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mq/type_defs/)

Usage::

    ```python
    from mypy_boto3_mq.type_defs import ActionRequiredTypeDef

    data: ActionRequiredTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AuthenticationStrategyType,
    BrokerStateType,
    BrokerStorageTypeType,
    ChangeTypeType,
    DayOfWeekType,
    DeploymentModeType,
    EngineTypeType,
    SanitizationWarningReasonType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActionRequiredTypeDef",
    "AvailabilityZoneTypeDef",
    "EngineVersionTypeDef",
    "BrokerInstanceTypeDef",
    "BrokerSummaryTypeDef",
    "ConfigurationIdTypeDef",
    "ConfigurationRevisionTypeDef",
    "EncryptionOptionsTypeDef",
    "LdapServerMetadataInputTypeDef",
    "LogsTypeDef",
    "UserTypeDef",
    "WeeklyStartTimeTypeDef",
    "ResponseMetadataTypeDef",
    "CreateConfigurationRequestRequestTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DeleteBrokerRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeBrokerEngineTypesRequestRequestTypeDef",
    "DescribeBrokerInstanceOptionsRequestRequestTypeDef",
    "DescribeBrokerRequestRequestTypeDef",
    "LdapServerMetadataOutputTypeDef",
    "UserSummaryTypeDef",
    "DescribeConfigurationRequestRequestTypeDef",
    "DescribeConfigurationRevisionRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "UserPendingChangesTypeDef",
    "PaginatorConfigTypeDef",
    "ListBrokersRequestRequestTypeDef",
    "ListConfigurationRevisionsRequestRequestTypeDef",
    "ListConfigurationsRequestRequestTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "PendingLogsTypeDef",
    "RebootBrokerRequestRequestTypeDef",
    "SanitizationWarningTypeDef",
    "UpdateConfigurationRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "BrokerInstanceOptionTypeDef",
    "BrokerEngineTypeTypeDef",
    "ConfigurationsTypeDef",
    "ConfigurationTypeDef",
    "CreateBrokerRequestRequestTypeDef",
    "UpdateBrokerRequestRequestTypeDef",
    "CreateBrokerResponseTypeDef",
    "CreateConfigurationResponseTypeDef",
    "DeleteBrokerResponseTypeDef",
    "DescribeConfigurationResponseTypeDef",
    "DescribeConfigurationRevisionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListBrokersResponseTypeDef",
    "ListConfigurationRevisionsResponseTypeDef",
    "ListTagsResponseTypeDef",
    "UpdateBrokerResponseTypeDef",
    "ListUsersResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "ListBrokersRequestListBrokersPaginateTypeDef",
    "LogsSummaryTypeDef",
    "UpdateConfigurationResponseTypeDef",
    "DescribeBrokerInstanceOptionsResponseTypeDef",
    "DescribeBrokerEngineTypesResponseTypeDef",
    "ListConfigurationsResponseTypeDef",
    "DescribeBrokerResponseTypeDef",
)

ActionRequiredTypeDef = TypedDict(
    "ActionRequiredTypeDef",
    {
        "ActionRequiredCode": str,
        "ActionRequiredInfo": str,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

EngineVersionTypeDef = TypedDict(
    "EngineVersionTypeDef",
    {
        "Name": str,
    },
    total=False,
)

BrokerInstanceTypeDef = TypedDict(
    "BrokerInstanceTypeDef",
    {
        "ConsoleURL": str,
        "Endpoints": List[str],
        "IpAddress": str,
    },
    total=False,
)

_RequiredBrokerSummaryTypeDef = TypedDict(
    "_RequiredBrokerSummaryTypeDef",
    {
        "DeploymentMode": DeploymentModeType,
        "EngineType": EngineTypeType,
    },
)
_OptionalBrokerSummaryTypeDef = TypedDict(
    "_OptionalBrokerSummaryTypeDef",
    {
        "BrokerArn": str,
        "BrokerId": str,
        "BrokerName": str,
        "BrokerState": BrokerStateType,
        "Created": datetime,
        "HostInstanceType": str,
    },
    total=False,
)

class BrokerSummaryTypeDef(_RequiredBrokerSummaryTypeDef, _OptionalBrokerSummaryTypeDef):
    pass

_RequiredConfigurationIdTypeDef = TypedDict(
    "_RequiredConfigurationIdTypeDef",
    {
        "Id": str,
    },
)
_OptionalConfigurationIdTypeDef = TypedDict(
    "_OptionalConfigurationIdTypeDef",
    {
        "Revision": int,
    },
    total=False,
)

class ConfigurationIdTypeDef(_RequiredConfigurationIdTypeDef, _OptionalConfigurationIdTypeDef):
    pass

_RequiredConfigurationRevisionTypeDef = TypedDict(
    "_RequiredConfigurationRevisionTypeDef",
    {
        "Created": datetime,
        "Revision": int,
    },
)
_OptionalConfigurationRevisionTypeDef = TypedDict(
    "_OptionalConfigurationRevisionTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class ConfigurationRevisionTypeDef(
    _RequiredConfigurationRevisionTypeDef, _OptionalConfigurationRevisionTypeDef
):
    pass

_RequiredEncryptionOptionsTypeDef = TypedDict(
    "_RequiredEncryptionOptionsTypeDef",
    {
        "UseAwsOwnedKey": bool,
    },
)
_OptionalEncryptionOptionsTypeDef = TypedDict(
    "_OptionalEncryptionOptionsTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class EncryptionOptionsTypeDef(
    _RequiredEncryptionOptionsTypeDef, _OptionalEncryptionOptionsTypeDef
):
    pass

_RequiredLdapServerMetadataInputTypeDef = TypedDict(
    "_RequiredLdapServerMetadataInputTypeDef",
    {
        "Hosts": Sequence[str],
        "RoleBase": str,
        "RoleSearchMatching": str,
        "ServiceAccountPassword": str,
        "ServiceAccountUsername": str,
        "UserBase": str,
        "UserSearchMatching": str,
    },
)
_OptionalLdapServerMetadataInputTypeDef = TypedDict(
    "_OptionalLdapServerMetadataInputTypeDef",
    {
        "RoleName": str,
        "RoleSearchSubtree": bool,
        "UserRoleName": str,
        "UserSearchSubtree": bool,
    },
    total=False,
)

class LdapServerMetadataInputTypeDef(
    _RequiredLdapServerMetadataInputTypeDef, _OptionalLdapServerMetadataInputTypeDef
):
    pass

LogsTypeDef = TypedDict(
    "LogsTypeDef",
    {
        "Audit": bool,
        "General": bool,
    },
    total=False,
)

_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {
        "Password": str,
        "Username": str,
    },
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "ConsoleAccess": bool,
        "Groups": Sequence[str],
    },
    total=False,
)

class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass

_RequiredWeeklyStartTimeTypeDef = TypedDict(
    "_RequiredWeeklyStartTimeTypeDef",
    {
        "DayOfWeek": DayOfWeekType,
        "TimeOfDay": str,
    },
)
_OptionalWeeklyStartTimeTypeDef = TypedDict(
    "_OptionalWeeklyStartTimeTypeDef",
    {
        "TimeZone": str,
    },
    total=False,
)

class WeeklyStartTimeTypeDef(_RequiredWeeklyStartTimeTypeDef, _OptionalWeeklyStartTimeTypeDef):
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

_RequiredCreateConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConfigurationRequestRequestTypeDef",
    {
        "EngineType": EngineTypeType,
        "EngineVersion": str,
        "Name": str,
    },
)
_OptionalCreateConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConfigurationRequestRequestTypeDef",
    {
        "AuthenticationStrategy": AuthenticationStrategyType,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateConfigurationRequestRequestTypeDef(
    _RequiredCreateConfigurationRequestRequestTypeDef,
    _OptionalCreateConfigurationRequestRequestTypeDef,
):
    pass

_RequiredCreateTagsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalCreateTagsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTagsRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateTagsRequestRequestTypeDef(
    _RequiredCreateTagsRequestRequestTypeDef, _OptionalCreateTagsRequestRequestTypeDef
):
    pass

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "BrokerId": str,
        "Password": str,
        "Username": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "ConsoleAccess": bool,
        "Groups": Sequence[str],
    },
    total=False,
)

class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass

DeleteBrokerRequestRequestTypeDef = TypedDict(
    "DeleteBrokerRequestRequestTypeDef",
    {
        "BrokerId": str,
    },
)

DeleteTagsRequestRequestTypeDef = TypedDict(
    "DeleteTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "BrokerId": str,
        "Username": str,
    },
)

DescribeBrokerEngineTypesRequestRequestTypeDef = TypedDict(
    "DescribeBrokerEngineTypesRequestRequestTypeDef",
    {
        "EngineType": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeBrokerInstanceOptionsRequestRequestTypeDef = TypedDict(
    "DescribeBrokerInstanceOptionsRequestRequestTypeDef",
    {
        "EngineType": str,
        "HostInstanceType": str,
        "MaxResults": int,
        "NextToken": str,
        "StorageType": str,
    },
    total=False,
)

DescribeBrokerRequestRequestTypeDef = TypedDict(
    "DescribeBrokerRequestRequestTypeDef",
    {
        "BrokerId": str,
    },
)

_RequiredLdapServerMetadataOutputTypeDef = TypedDict(
    "_RequiredLdapServerMetadataOutputTypeDef",
    {
        "Hosts": List[str],
        "RoleBase": str,
        "RoleSearchMatching": str,
        "ServiceAccountUsername": str,
        "UserBase": str,
        "UserSearchMatching": str,
    },
)
_OptionalLdapServerMetadataOutputTypeDef = TypedDict(
    "_OptionalLdapServerMetadataOutputTypeDef",
    {
        "RoleName": str,
        "RoleSearchSubtree": bool,
        "UserRoleName": str,
        "UserSearchSubtree": bool,
    },
    total=False,
)

class LdapServerMetadataOutputTypeDef(
    _RequiredLdapServerMetadataOutputTypeDef, _OptionalLdapServerMetadataOutputTypeDef
):
    pass

_RequiredUserSummaryTypeDef = TypedDict(
    "_RequiredUserSummaryTypeDef",
    {
        "Username": str,
    },
)
_OptionalUserSummaryTypeDef = TypedDict(
    "_OptionalUserSummaryTypeDef",
    {
        "PendingChange": ChangeTypeType,
    },
    total=False,
)

class UserSummaryTypeDef(_RequiredUserSummaryTypeDef, _OptionalUserSummaryTypeDef):
    pass

DescribeConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationRequestRequestTypeDef",
    {
        "ConfigurationId": str,
    },
)

DescribeConfigurationRevisionRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationRevisionRequestRequestTypeDef",
    {
        "ConfigurationId": str,
        "ConfigurationRevision": str,
    },
)

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "BrokerId": str,
        "Username": str,
    },
)

_RequiredUserPendingChangesTypeDef = TypedDict(
    "_RequiredUserPendingChangesTypeDef",
    {
        "PendingChange": ChangeTypeType,
    },
)
_OptionalUserPendingChangesTypeDef = TypedDict(
    "_OptionalUserPendingChangesTypeDef",
    {
        "ConsoleAccess": bool,
        "Groups": List[str],
    },
    total=False,
)

class UserPendingChangesTypeDef(
    _RequiredUserPendingChangesTypeDef, _OptionalUserPendingChangesTypeDef
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListBrokersRequestRequestTypeDef = TypedDict(
    "ListBrokersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListConfigurationRevisionsRequestRequestTypeDef = TypedDict(
    "_RequiredListConfigurationRevisionsRequestRequestTypeDef",
    {
        "ConfigurationId": str,
    },
)
_OptionalListConfigurationRevisionsRequestRequestTypeDef = TypedDict(
    "_OptionalListConfigurationRevisionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListConfigurationRevisionsRequestRequestTypeDef(
    _RequiredListConfigurationRevisionsRequestRequestTypeDef,
    _OptionalListConfigurationRevisionsRequestRequestTypeDef,
):
    pass

ListConfigurationsRequestRequestTypeDef = TypedDict(
    "ListConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsRequestRequestTypeDef = TypedDict(
    "ListTagsRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "BrokerId": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass

PendingLogsTypeDef = TypedDict(
    "PendingLogsTypeDef",
    {
        "Audit": bool,
        "General": bool,
    },
    total=False,
)

RebootBrokerRequestRequestTypeDef = TypedDict(
    "RebootBrokerRequestRequestTypeDef",
    {
        "BrokerId": str,
    },
)

_RequiredSanitizationWarningTypeDef = TypedDict(
    "_RequiredSanitizationWarningTypeDef",
    {
        "Reason": SanitizationWarningReasonType,
    },
)
_OptionalSanitizationWarningTypeDef = TypedDict(
    "_OptionalSanitizationWarningTypeDef",
    {
        "AttributeName": str,
        "ElementName": str,
    },
    total=False,
)

class SanitizationWarningTypeDef(
    _RequiredSanitizationWarningTypeDef, _OptionalSanitizationWarningTypeDef
):
    pass

_RequiredUpdateConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateConfigurationRequestRequestTypeDef",
    {
        "ConfigurationId": str,
        "Data": str,
    },
)
_OptionalUpdateConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateConfigurationRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateConfigurationRequestRequestTypeDef(
    _RequiredUpdateConfigurationRequestRequestTypeDef,
    _OptionalUpdateConfigurationRequestRequestTypeDef,
):
    pass

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "BrokerId": str,
        "Username": str,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "ConsoleAccess": bool,
        "Groups": Sequence[str],
        "Password": str,
    },
    total=False,
)

class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass

BrokerInstanceOptionTypeDef = TypedDict(
    "BrokerInstanceOptionTypeDef",
    {
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "EngineType": EngineTypeType,
        "HostInstanceType": str,
        "StorageType": BrokerStorageTypeType,
        "SupportedDeploymentModes": List[DeploymentModeType],
        "SupportedEngineVersions": List[str],
    },
    total=False,
)

BrokerEngineTypeTypeDef = TypedDict(
    "BrokerEngineTypeTypeDef",
    {
        "EngineType": EngineTypeType,
        "EngineVersions": List[EngineVersionTypeDef],
    },
    total=False,
)

ConfigurationsTypeDef = TypedDict(
    "ConfigurationsTypeDef",
    {
        "Current": ConfigurationIdTypeDef,
        "History": List[ConfigurationIdTypeDef],
        "Pending": ConfigurationIdTypeDef,
    },
    total=False,
)

_RequiredConfigurationTypeDef = TypedDict(
    "_RequiredConfigurationTypeDef",
    {
        "Arn": str,
        "AuthenticationStrategy": AuthenticationStrategyType,
        "Created": datetime,
        "Description": str,
        "EngineType": EngineTypeType,
        "EngineVersion": str,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
    },
)
_OptionalConfigurationTypeDef = TypedDict(
    "_OptionalConfigurationTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class ConfigurationTypeDef(_RequiredConfigurationTypeDef, _OptionalConfigurationTypeDef):
    pass

_RequiredCreateBrokerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBrokerRequestRequestTypeDef",
    {
        "AutoMinorVersionUpgrade": bool,
        "BrokerName": str,
        "DeploymentMode": DeploymentModeType,
        "EngineType": EngineTypeType,
        "EngineVersion": str,
        "HostInstanceType": str,
        "PubliclyAccessible": bool,
        "Users": Sequence[UserTypeDef],
    },
)
_OptionalCreateBrokerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBrokerRequestRequestTypeDef",
    {
        "AuthenticationStrategy": AuthenticationStrategyType,
        "Configuration": ConfigurationIdTypeDef,
        "CreatorRequestId": str,
        "EncryptionOptions": EncryptionOptionsTypeDef,
        "LdapServerMetadata": LdapServerMetadataInputTypeDef,
        "Logs": LogsTypeDef,
        "MaintenanceWindowStartTime": WeeklyStartTimeTypeDef,
        "SecurityGroups": Sequence[str],
        "StorageType": BrokerStorageTypeType,
        "SubnetIds": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateBrokerRequestRequestTypeDef(
    _RequiredCreateBrokerRequestRequestTypeDef, _OptionalCreateBrokerRequestRequestTypeDef
):
    pass

_RequiredUpdateBrokerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBrokerRequestRequestTypeDef",
    {
        "BrokerId": str,
    },
)
_OptionalUpdateBrokerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBrokerRequestRequestTypeDef",
    {
        "AuthenticationStrategy": AuthenticationStrategyType,
        "AutoMinorVersionUpgrade": bool,
        "Configuration": ConfigurationIdTypeDef,
        "EngineVersion": str,
        "HostInstanceType": str,
        "LdapServerMetadata": LdapServerMetadataInputTypeDef,
        "Logs": LogsTypeDef,
        "MaintenanceWindowStartTime": WeeklyStartTimeTypeDef,
        "SecurityGroups": Sequence[str],
    },
    total=False,
)

class UpdateBrokerRequestRequestTypeDef(
    _RequiredUpdateBrokerRequestRequestTypeDef, _OptionalUpdateBrokerRequestRequestTypeDef
):
    pass

CreateBrokerResponseTypeDef = TypedDict(
    "CreateBrokerResponseTypeDef",
    {
        "BrokerArn": str,
        "BrokerId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConfigurationResponseTypeDef = TypedDict(
    "CreateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "AuthenticationStrategy": AuthenticationStrategyType,
        "Created": datetime,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBrokerResponseTypeDef = TypedDict(
    "DeleteBrokerResponseTypeDef",
    {
        "BrokerId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationResponseTypeDef = TypedDict(
    "DescribeConfigurationResponseTypeDef",
    {
        "Arn": str,
        "AuthenticationStrategy": AuthenticationStrategyType,
        "Created": datetime,
        "Description": str,
        "EngineType": EngineTypeType,
        "EngineVersion": str,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationRevisionResponseTypeDef = TypedDict(
    "DescribeConfigurationRevisionResponseTypeDef",
    {
        "ConfigurationId": str,
        "Created": datetime,
        "Data": str,
        "Description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBrokersResponseTypeDef = TypedDict(
    "ListBrokersResponseTypeDef",
    {
        "BrokerSummaries": List[BrokerSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationRevisionsResponseTypeDef = TypedDict(
    "ListConfigurationRevisionsResponseTypeDef",
    {
        "ConfigurationId": str,
        "MaxResults": int,
        "NextToken": str,
        "Revisions": List[ConfigurationRevisionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBrokerResponseTypeDef = TypedDict(
    "UpdateBrokerResponseTypeDef",
    {
        "AuthenticationStrategy": AuthenticationStrategyType,
        "AutoMinorVersionUpgrade": bool,
        "BrokerId": str,
        "Configuration": ConfigurationIdTypeDef,
        "EngineVersion": str,
        "HostInstanceType": str,
        "LdapServerMetadata": LdapServerMetadataOutputTypeDef,
        "Logs": LogsTypeDef,
        "MaintenanceWindowStartTime": WeeklyStartTimeTypeDef,
        "SecurityGroups": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "BrokerId": str,
        "MaxResults": int,
        "NextToken": str,
        "Users": List[UserSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "BrokerId": str,
        "ConsoleAccess": bool,
        "Groups": List[str],
        "Pending": UserPendingChangesTypeDef,
        "Username": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBrokersRequestListBrokersPaginateTypeDef = TypedDict(
    "ListBrokersRequestListBrokersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredLogsSummaryTypeDef = TypedDict(
    "_RequiredLogsSummaryTypeDef",
    {
        "General": bool,
        "GeneralLogGroup": str,
    },
)
_OptionalLogsSummaryTypeDef = TypedDict(
    "_OptionalLogsSummaryTypeDef",
    {
        "Audit": bool,
        "AuditLogGroup": str,
        "Pending": PendingLogsTypeDef,
    },
    total=False,
)

class LogsSummaryTypeDef(_RequiredLogsSummaryTypeDef, _OptionalLogsSummaryTypeDef):
    pass

UpdateConfigurationResponseTypeDef = TypedDict(
    "UpdateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "Warnings": List[SanitizationWarningTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBrokerInstanceOptionsResponseTypeDef = TypedDict(
    "DescribeBrokerInstanceOptionsResponseTypeDef",
    {
        "BrokerInstanceOptions": List[BrokerInstanceOptionTypeDef],
        "MaxResults": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBrokerEngineTypesResponseTypeDef = TypedDict(
    "DescribeBrokerEngineTypesResponseTypeDef",
    {
        "BrokerEngineTypes": List[BrokerEngineTypeTypeDef],
        "MaxResults": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationsResponseTypeDef = TypedDict(
    "ListConfigurationsResponseTypeDef",
    {
        "Configurations": List[ConfigurationTypeDef],
        "MaxResults": int,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBrokerResponseTypeDef = TypedDict(
    "DescribeBrokerResponseTypeDef",
    {
        "ActionsRequired": List[ActionRequiredTypeDef],
        "AuthenticationStrategy": AuthenticationStrategyType,
        "AutoMinorVersionUpgrade": bool,
        "BrokerArn": str,
        "BrokerId": str,
        "BrokerInstances": List[BrokerInstanceTypeDef],
        "BrokerName": str,
        "BrokerState": BrokerStateType,
        "Configurations": ConfigurationsTypeDef,
        "Created": datetime,
        "DeploymentMode": DeploymentModeType,
        "EncryptionOptions": EncryptionOptionsTypeDef,
        "EngineType": EngineTypeType,
        "EngineVersion": str,
        "HostInstanceType": str,
        "LdapServerMetadata": LdapServerMetadataOutputTypeDef,
        "Logs": LogsSummaryTypeDef,
        "MaintenanceWindowStartTime": WeeklyStartTimeTypeDef,
        "PendingAuthenticationStrategy": AuthenticationStrategyType,
        "PendingEngineVersion": str,
        "PendingHostInstanceType": str,
        "PendingLdapServerMetadata": LdapServerMetadataOutputTypeDef,
        "PendingSecurityGroups": List[str],
        "PubliclyAccessible": bool,
        "SecurityGroups": List[str],
        "StorageType": BrokerStorageTypeType,
        "SubnetIds": List[str],
        "Tags": Dict[str, str],
        "Users": List[UserSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
