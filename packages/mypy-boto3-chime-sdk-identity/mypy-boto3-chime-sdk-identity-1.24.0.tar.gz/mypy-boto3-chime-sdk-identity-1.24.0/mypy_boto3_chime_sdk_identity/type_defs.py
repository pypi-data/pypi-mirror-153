"""
Type annotations for chime-sdk-identity service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_identity/type_defs/)

Usage::

    ```python
    from mypy_boto3_chime_sdk_identity.type_defs import IdentityTypeDef

    data: IdentityTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AllowMessagesType,
    AppInstanceUserEndpointTypeType,
    EndpointStatusReasonType,
    EndpointStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "IdentityTypeDef",
    "ChannelRetentionSettingsTypeDef",
    "AppInstanceSummaryTypeDef",
    "AppInstanceTypeDef",
    "EndpointStateTypeDef",
    "EndpointAttributesTypeDef",
    "AppInstanceUserSummaryTypeDef",
    "AppInstanceUserTypeDef",
    "CreateAppInstanceAdminRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "DeleteAppInstanceAdminRequestRequestTypeDef",
    "DeleteAppInstanceRequestRequestTypeDef",
    "DeleteAppInstanceUserRequestRequestTypeDef",
    "DeregisterAppInstanceUserEndpointRequestRequestTypeDef",
    "DescribeAppInstanceAdminRequestRequestTypeDef",
    "DescribeAppInstanceRequestRequestTypeDef",
    "DescribeAppInstanceUserEndpointRequestRequestTypeDef",
    "DescribeAppInstanceUserRequestRequestTypeDef",
    "GetAppInstanceRetentionSettingsRequestRequestTypeDef",
    "ListAppInstanceAdminsRequestRequestTypeDef",
    "ListAppInstanceUserEndpointsRequestRequestTypeDef",
    "ListAppInstanceUsersRequestRequestTypeDef",
    "ListAppInstancesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppInstanceRequestRequestTypeDef",
    "UpdateAppInstanceUserEndpointRequestRequestTypeDef",
    "UpdateAppInstanceUserRequestRequestTypeDef",
    "AppInstanceAdminSummaryTypeDef",
    "AppInstanceAdminTypeDef",
    "AppInstanceRetentionSettingsTypeDef",
    "AppInstanceUserEndpointSummaryTypeDef",
    "AppInstanceUserEndpointTypeDef",
    "RegisterAppInstanceUserEndpointRequestRequestTypeDef",
    "CreateAppInstanceAdminResponseTypeDef",
    "CreateAppInstanceResponseTypeDef",
    "CreateAppInstanceUserResponseTypeDef",
    "DescribeAppInstanceResponseTypeDef",
    "DescribeAppInstanceUserResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListAppInstanceUsersResponseTypeDef",
    "ListAppInstancesResponseTypeDef",
    "RegisterAppInstanceUserEndpointResponseTypeDef",
    "UpdateAppInstanceResponseTypeDef",
    "UpdateAppInstanceUserEndpointResponseTypeDef",
    "UpdateAppInstanceUserResponseTypeDef",
    "CreateAppInstanceRequestRequestTypeDef",
    "CreateAppInstanceUserRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListAppInstanceAdminsResponseTypeDef",
    "DescribeAppInstanceAdminResponseTypeDef",
    "GetAppInstanceRetentionSettingsResponseTypeDef",
    "PutAppInstanceRetentionSettingsRequestRequestTypeDef",
    "PutAppInstanceRetentionSettingsResponseTypeDef",
    "ListAppInstanceUserEndpointsResponseTypeDef",
    "DescribeAppInstanceUserEndpointResponseTypeDef",
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "Arn": str,
        "Name": str,
    },
    total=False,
)

ChannelRetentionSettingsTypeDef = TypedDict(
    "ChannelRetentionSettingsTypeDef",
    {
        "RetentionDays": int,
    },
    total=False,
)

AppInstanceSummaryTypeDef = TypedDict(
    "AppInstanceSummaryTypeDef",
    {
        "AppInstanceArn": str,
        "Name": str,
        "Metadata": str,
    },
    total=False,
)

AppInstanceTypeDef = TypedDict(
    "AppInstanceTypeDef",
    {
        "AppInstanceArn": str,
        "Name": str,
        "CreatedTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "Metadata": str,
    },
    total=False,
)

_RequiredEndpointStateTypeDef = TypedDict(
    "_RequiredEndpointStateTypeDef",
    {
        "Status": EndpointStatusType,
    },
)
_OptionalEndpointStateTypeDef = TypedDict(
    "_OptionalEndpointStateTypeDef",
    {
        "StatusReason": EndpointStatusReasonType,
    },
    total=False,
)


class EndpointStateTypeDef(_RequiredEndpointStateTypeDef, _OptionalEndpointStateTypeDef):
    pass


_RequiredEndpointAttributesTypeDef = TypedDict(
    "_RequiredEndpointAttributesTypeDef",
    {
        "DeviceToken": str,
    },
)
_OptionalEndpointAttributesTypeDef = TypedDict(
    "_OptionalEndpointAttributesTypeDef",
    {
        "VoipDeviceToken": str,
    },
    total=False,
)


class EndpointAttributesTypeDef(
    _RequiredEndpointAttributesTypeDef, _OptionalEndpointAttributesTypeDef
):
    pass


AppInstanceUserSummaryTypeDef = TypedDict(
    "AppInstanceUserSummaryTypeDef",
    {
        "AppInstanceUserArn": str,
        "Name": str,
        "Metadata": str,
    },
    total=False,
)

AppInstanceUserTypeDef = TypedDict(
    "AppInstanceUserTypeDef",
    {
        "AppInstanceUserArn": str,
        "Name": str,
        "Metadata": str,
        "CreatedTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

CreateAppInstanceAdminRequestRequestTypeDef = TypedDict(
    "CreateAppInstanceAdminRequestRequestTypeDef",
    {
        "AppInstanceAdminArn": str,
        "AppInstanceArn": str,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteAppInstanceAdminRequestRequestTypeDef = TypedDict(
    "DeleteAppInstanceAdminRequestRequestTypeDef",
    {
        "AppInstanceAdminArn": str,
        "AppInstanceArn": str,
    },
)

DeleteAppInstanceRequestRequestTypeDef = TypedDict(
    "DeleteAppInstanceRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
    },
)

DeleteAppInstanceUserRequestRequestTypeDef = TypedDict(
    "DeleteAppInstanceUserRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
    },
)

DeregisterAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "DeregisterAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
    },
)

DescribeAppInstanceAdminRequestRequestTypeDef = TypedDict(
    "DescribeAppInstanceAdminRequestRequestTypeDef",
    {
        "AppInstanceAdminArn": str,
        "AppInstanceArn": str,
    },
)

DescribeAppInstanceRequestRequestTypeDef = TypedDict(
    "DescribeAppInstanceRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
    },
)

DescribeAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "DescribeAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
    },
)

DescribeAppInstanceUserRequestRequestTypeDef = TypedDict(
    "DescribeAppInstanceUserRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
    },
)

GetAppInstanceRetentionSettingsRequestRequestTypeDef = TypedDict(
    "GetAppInstanceRetentionSettingsRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
    },
)

_RequiredListAppInstanceAdminsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppInstanceAdminsRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
    },
)
_OptionalListAppInstanceAdminsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppInstanceAdminsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAppInstanceAdminsRequestRequestTypeDef(
    _RequiredListAppInstanceAdminsRequestRequestTypeDef,
    _OptionalListAppInstanceAdminsRequestRequestTypeDef,
):
    pass


_RequiredListAppInstanceUserEndpointsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppInstanceUserEndpointsRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
    },
)
_OptionalListAppInstanceUserEndpointsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppInstanceUserEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAppInstanceUserEndpointsRequestRequestTypeDef(
    _RequiredListAppInstanceUserEndpointsRequestRequestTypeDef,
    _OptionalListAppInstanceUserEndpointsRequestRequestTypeDef,
):
    pass


_RequiredListAppInstanceUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListAppInstanceUsersRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
    },
)
_OptionalListAppInstanceUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListAppInstanceUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAppInstanceUsersRequestRequestTypeDef(
    _RequiredListAppInstanceUsersRequestRequestTypeDef,
    _OptionalListAppInstanceUsersRequestRequestTypeDef,
):
    pass


ListAppInstancesRequestRequestTypeDef = TypedDict(
    "ListAppInstancesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAppInstanceRequestRequestTypeDef = TypedDict(
    "UpdateAppInstanceRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
        "Name": str,
        "Metadata": str,
    },
)

_RequiredUpdateAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
    },
)
_OptionalUpdateAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "Name": str,
        "AllowMessages": AllowMessagesType,
    },
    total=False,
)


class UpdateAppInstanceUserEndpointRequestRequestTypeDef(
    _RequiredUpdateAppInstanceUserEndpointRequestRequestTypeDef,
    _OptionalUpdateAppInstanceUserEndpointRequestRequestTypeDef,
):
    pass


UpdateAppInstanceUserRequestRequestTypeDef = TypedDict(
    "UpdateAppInstanceUserRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "Name": str,
        "Metadata": str,
    },
)

AppInstanceAdminSummaryTypeDef = TypedDict(
    "AppInstanceAdminSummaryTypeDef",
    {
        "Admin": IdentityTypeDef,
    },
    total=False,
)

AppInstanceAdminTypeDef = TypedDict(
    "AppInstanceAdminTypeDef",
    {
        "Admin": IdentityTypeDef,
        "AppInstanceArn": str,
        "CreatedTimestamp": datetime,
    },
    total=False,
)

AppInstanceRetentionSettingsTypeDef = TypedDict(
    "AppInstanceRetentionSettingsTypeDef",
    {
        "ChannelRetentionSettings": ChannelRetentionSettingsTypeDef,
    },
    total=False,
)

AppInstanceUserEndpointSummaryTypeDef = TypedDict(
    "AppInstanceUserEndpointSummaryTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
        "Name": str,
        "Type": AppInstanceUserEndpointTypeType,
        "AllowMessages": AllowMessagesType,
        "EndpointState": EndpointStateTypeDef,
    },
    total=False,
)

AppInstanceUserEndpointTypeDef = TypedDict(
    "AppInstanceUserEndpointTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
        "Name": str,
        "Type": AppInstanceUserEndpointTypeType,
        "ResourceArn": str,
        "EndpointAttributes": EndpointAttributesTypeDef,
        "CreatedTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "AllowMessages": AllowMessagesType,
        "EndpointState": EndpointStateTypeDef,
    },
    total=False,
)

_RequiredRegisterAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "Type": AppInstanceUserEndpointTypeType,
        "ResourceArn": str,
        "EndpointAttributes": EndpointAttributesTypeDef,
        "ClientRequestToken": str,
    },
)
_OptionalRegisterAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "Name": str,
        "AllowMessages": AllowMessagesType,
    },
    total=False,
)


class RegisterAppInstanceUserEndpointRequestRequestTypeDef(
    _RequiredRegisterAppInstanceUserEndpointRequestRequestTypeDef,
    _OptionalRegisterAppInstanceUserEndpointRequestRequestTypeDef,
):
    pass


CreateAppInstanceAdminResponseTypeDef = TypedDict(
    "CreateAppInstanceAdminResponseTypeDef",
    {
        "AppInstanceAdmin": IdentityTypeDef,
        "AppInstanceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppInstanceResponseTypeDef = TypedDict(
    "CreateAppInstanceResponseTypeDef",
    {
        "AppInstanceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppInstanceUserResponseTypeDef = TypedDict(
    "CreateAppInstanceUserResponseTypeDef",
    {
        "AppInstanceUserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppInstanceResponseTypeDef = TypedDict(
    "DescribeAppInstanceResponseTypeDef",
    {
        "AppInstance": AppInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppInstanceUserResponseTypeDef = TypedDict(
    "DescribeAppInstanceUserResponseTypeDef",
    {
        "AppInstanceUser": AppInstanceUserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppInstanceUsersResponseTypeDef = TypedDict(
    "ListAppInstanceUsersResponseTypeDef",
    {
        "AppInstanceArn": str,
        "AppInstanceUsers": List[AppInstanceUserSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppInstancesResponseTypeDef = TypedDict(
    "ListAppInstancesResponseTypeDef",
    {
        "AppInstances": List[AppInstanceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterAppInstanceUserEndpointResponseTypeDef = TypedDict(
    "RegisterAppInstanceUserEndpointResponseTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppInstanceResponseTypeDef = TypedDict(
    "UpdateAppInstanceResponseTypeDef",
    {
        "AppInstanceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppInstanceUserEndpointResponseTypeDef = TypedDict(
    "UpdateAppInstanceUserEndpointResponseTypeDef",
    {
        "AppInstanceUserArn": str,
        "EndpointId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppInstanceUserResponseTypeDef = TypedDict(
    "UpdateAppInstanceUserResponseTypeDef",
    {
        "AppInstanceUserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAppInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppInstanceRequestRequestTypeDef",
    {
        "Name": str,
        "ClientRequestToken": str,
    },
)
_OptionalCreateAppInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppInstanceRequestRequestTypeDef",
    {
        "Metadata": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAppInstanceRequestRequestTypeDef(
    _RequiredCreateAppInstanceRequestRequestTypeDef, _OptionalCreateAppInstanceRequestRequestTypeDef
):
    pass


_RequiredCreateAppInstanceUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppInstanceUserRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
        "AppInstanceUserId": str,
        "Name": str,
        "ClientRequestToken": str,
    },
)
_OptionalCreateAppInstanceUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppInstanceUserRequestRequestTypeDef",
    {
        "Metadata": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAppInstanceUserRequestRequestTypeDef(
    _RequiredCreateAppInstanceUserRequestRequestTypeDef,
    _OptionalCreateAppInstanceUserRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListAppInstanceAdminsResponseTypeDef = TypedDict(
    "ListAppInstanceAdminsResponseTypeDef",
    {
        "AppInstanceArn": str,
        "AppInstanceAdmins": List[AppInstanceAdminSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppInstanceAdminResponseTypeDef = TypedDict(
    "DescribeAppInstanceAdminResponseTypeDef",
    {
        "AppInstanceAdmin": AppInstanceAdminTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppInstanceRetentionSettingsResponseTypeDef = TypedDict(
    "GetAppInstanceRetentionSettingsResponseTypeDef",
    {
        "AppInstanceRetentionSettings": AppInstanceRetentionSettingsTypeDef,
        "InitiateDeletionTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAppInstanceRetentionSettingsRequestRequestTypeDef = TypedDict(
    "PutAppInstanceRetentionSettingsRequestRequestTypeDef",
    {
        "AppInstanceArn": str,
        "AppInstanceRetentionSettings": AppInstanceRetentionSettingsTypeDef,
    },
)

PutAppInstanceRetentionSettingsResponseTypeDef = TypedDict(
    "PutAppInstanceRetentionSettingsResponseTypeDef",
    {
        "AppInstanceRetentionSettings": AppInstanceRetentionSettingsTypeDef,
        "InitiateDeletionTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppInstanceUserEndpointsResponseTypeDef = TypedDict(
    "ListAppInstanceUserEndpointsResponseTypeDef",
    {
        "AppInstanceUserEndpoints": List[AppInstanceUserEndpointSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppInstanceUserEndpointResponseTypeDef = TypedDict(
    "DescribeAppInstanceUserEndpointResponseTypeDef",
    {
        "AppInstanceUserEndpoint": AppInstanceUserEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
