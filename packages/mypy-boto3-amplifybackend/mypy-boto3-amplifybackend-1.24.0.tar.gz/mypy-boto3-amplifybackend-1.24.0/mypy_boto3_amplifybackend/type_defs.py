"""
Type annotations for amplifybackend service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifybackend/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplifybackend.type_defs import BackendAPIAppSyncAuthSettingsTypeDef

    data: BackendAPIAppSyncAuthSettingsTypeDef = {...}
    ```
"""
import sys
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    AdditionalConstraintsElementType,
    AuthenticatedElementType,
    AuthResourcesType,
    DeliveryMethodType,
    MFAModeType,
    MfaTypesElementType,
    ModeType,
    OAuthGrantTypeType,
    OAuthScopesElementType,
    RequiredSignUpAttributesElementType,
    ResolutionStrategyType,
    SignInMethodType,
    StatusType,
    UnAuthenticatedElementType,
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
    "BackendAPIAppSyncAuthSettingsTypeDef",
    "BackendAPIConflictResolutionTypeDef",
    "BackendAuthAppleProviderConfigTypeDef",
    "BackendAuthSocialProviderConfigTypeDef",
    "BackendJobRespObjTypeDef",
    "BackendStoragePermissionsTypeDef",
    "CloneBackendRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "EmailSettingsTypeDef",
    "SmsSettingsTypeDef",
    "CreateBackendAuthIdentityPoolConfigTypeDef",
    "SettingsTypeDef",
    "CreateBackendAuthPasswordPolicyConfigTypeDef",
    "CreateBackendConfigRequestRequestTypeDef",
    "CreateBackendRequestRequestTypeDef",
    "CreateTokenRequestRequestTypeDef",
    "DeleteBackendAuthRequestRequestTypeDef",
    "DeleteBackendRequestRequestTypeDef",
    "DeleteBackendStorageRequestRequestTypeDef",
    "DeleteTokenRequestRequestTypeDef",
    "GenerateBackendAPIModelsRequestRequestTypeDef",
    "GetBackendAPIModelsRequestRequestTypeDef",
    "GetBackendAuthRequestRequestTypeDef",
    "GetBackendJobRequestRequestTypeDef",
    "GetBackendRequestRequestTypeDef",
    "GetBackendStorageRequestRequestTypeDef",
    "GetTokenRequestRequestTypeDef",
    "ImportBackendAuthRequestRequestTypeDef",
    "ImportBackendStorageRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListBackendJobsRequestRequestTypeDef",
    "ListS3BucketsRequestRequestTypeDef",
    "S3BucketInfoTypeDef",
    "LoginAuthConfigReqObjTypeDef",
    "RemoveAllBackendsRequestRequestTypeDef",
    "RemoveBackendConfigRequestRequestTypeDef",
    "UpdateBackendAuthIdentityPoolConfigTypeDef",
    "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    "UpdateBackendJobRequestRequestTypeDef",
    "BackendAPIAuthTypeTypeDef",
    "SocialProviderSettingsTypeDef",
    "CreateBackendStorageResourceConfigTypeDef",
    "GetBackendStorageResourceConfigTypeDef",
    "UpdateBackendStorageResourceConfigTypeDef",
    "CloneBackendResponseTypeDef",
    "CreateBackendAPIResponseTypeDef",
    "CreateBackendAuthResponseTypeDef",
    "CreateBackendConfigResponseTypeDef",
    "CreateBackendResponseTypeDef",
    "CreateBackendStorageResponseTypeDef",
    "CreateTokenResponseTypeDef",
    "DeleteBackendAPIResponseTypeDef",
    "DeleteBackendAuthResponseTypeDef",
    "DeleteBackendResponseTypeDef",
    "DeleteBackendStorageResponseTypeDef",
    "DeleteTokenResponseTypeDef",
    "GenerateBackendAPIModelsResponseTypeDef",
    "GetBackendAPIModelsResponseTypeDef",
    "GetBackendJobResponseTypeDef",
    "GetBackendResponseTypeDef",
    "GetTokenResponseTypeDef",
    "ImportBackendAuthResponseTypeDef",
    "ImportBackendStorageResponseTypeDef",
    "ListBackendJobsResponseTypeDef",
    "RemoveAllBackendsResponseTypeDef",
    "RemoveBackendConfigResponseTypeDef",
    "UpdateBackendAPIResponseTypeDef",
    "UpdateBackendAuthResponseTypeDef",
    "UpdateBackendJobResponseTypeDef",
    "UpdateBackendStorageResponseTypeDef",
    "CreateBackendAuthForgotPasswordConfigTypeDef",
    "CreateBackendAuthVerificationMessageConfigTypeDef",
    "UpdateBackendAuthForgotPasswordConfigTypeDef",
    "UpdateBackendAuthVerificationMessageConfigTypeDef",
    "CreateBackendAuthMFAConfigTypeDef",
    "UpdateBackendAuthMFAConfigTypeDef",
    "ListBackendJobsRequestListBackendJobsPaginateTypeDef",
    "ListS3BucketsResponseTypeDef",
    "UpdateBackendConfigRequestRequestTypeDef",
    "UpdateBackendConfigResponseTypeDef",
    "BackendAPIResourceConfigTypeDef",
    "CreateBackendAuthOAuthConfigTypeDef",
    "UpdateBackendAuthOAuthConfigTypeDef",
    "CreateBackendStorageRequestRequestTypeDef",
    "GetBackendStorageResponseTypeDef",
    "UpdateBackendStorageRequestRequestTypeDef",
    "CreateBackendAPIRequestRequestTypeDef",
    "DeleteBackendAPIRequestRequestTypeDef",
    "GetBackendAPIRequestRequestTypeDef",
    "GetBackendAPIResponseTypeDef",
    "UpdateBackendAPIRequestRequestTypeDef",
    "CreateBackendAuthUserPoolConfigTypeDef",
    "UpdateBackendAuthUserPoolConfigTypeDef",
    "CreateBackendAuthResourceConfigTypeDef",
    "UpdateBackendAuthResourceConfigTypeDef",
    "CreateBackendAuthRequestRequestTypeDef",
    "GetBackendAuthResponseTypeDef",
    "UpdateBackendAuthRequestRequestTypeDef",
)

BackendAPIAppSyncAuthSettingsTypeDef = TypedDict(
    "BackendAPIAppSyncAuthSettingsTypeDef",
    {
        "CognitoUserPoolId": str,
        "Description": str,
        "ExpirationTime": float,
        "OpenIDAuthTTL": str,
        "OpenIDClientId": str,
        "OpenIDIatTTL": str,
        "OpenIDIssueURL": str,
        "OpenIDProviderName": str,
    },
    total=False,
)

BackendAPIConflictResolutionTypeDef = TypedDict(
    "BackendAPIConflictResolutionTypeDef",
    {
        "ResolutionStrategy": ResolutionStrategyType,
    },
    total=False,
)

BackendAuthAppleProviderConfigTypeDef = TypedDict(
    "BackendAuthAppleProviderConfigTypeDef",
    {
        "ClientId": str,
        "KeyId": str,
        "PrivateKey": str,
        "TeamId": str,
    },
    total=False,
)

BackendAuthSocialProviderConfigTypeDef = TypedDict(
    "BackendAuthSocialProviderConfigTypeDef",
    {
        "ClientId": str,
        "ClientSecret": str,
    },
    total=False,
)

_RequiredBackendJobRespObjTypeDef = TypedDict(
    "_RequiredBackendJobRespObjTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
    },
)
_OptionalBackendJobRespObjTypeDef = TypedDict(
    "_OptionalBackendJobRespObjTypeDef",
    {
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
    },
    total=False,
)


class BackendJobRespObjTypeDef(
    _RequiredBackendJobRespObjTypeDef, _OptionalBackendJobRespObjTypeDef
):
    pass


_RequiredBackendStoragePermissionsTypeDef = TypedDict(
    "_RequiredBackendStoragePermissionsTypeDef",
    {
        "Authenticated": Sequence[AuthenticatedElementType],
    },
)
_OptionalBackendStoragePermissionsTypeDef = TypedDict(
    "_OptionalBackendStoragePermissionsTypeDef",
    {
        "UnAuthenticated": Sequence[UnAuthenticatedElementType],
    },
    total=False,
)


class BackendStoragePermissionsTypeDef(
    _RequiredBackendStoragePermissionsTypeDef, _OptionalBackendStoragePermissionsTypeDef
):
    pass


CloneBackendRequestRequestTypeDef = TypedDict(
    "CloneBackendRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "TargetEnvironmentName": str,
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

EmailSettingsTypeDef = TypedDict(
    "EmailSettingsTypeDef",
    {
        "EmailMessage": str,
        "EmailSubject": str,
    },
    total=False,
)

SmsSettingsTypeDef = TypedDict(
    "SmsSettingsTypeDef",
    {
        "SmsMessage": str,
    },
    total=False,
)

CreateBackendAuthIdentityPoolConfigTypeDef = TypedDict(
    "CreateBackendAuthIdentityPoolConfigTypeDef",
    {
        "IdentityPoolName": str,
        "UnauthenticatedLogin": bool,
    },
)

SettingsTypeDef = TypedDict(
    "SettingsTypeDef",
    {
        "MfaTypes": Sequence[MfaTypesElementType],
        "SmsMessage": str,
    },
    total=False,
)

_RequiredCreateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthPasswordPolicyConfigTypeDef",
    {
        "MinimumLength": float,
    },
)
_OptionalCreateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthPasswordPolicyConfigTypeDef",
    {
        "AdditionalConstraints": Sequence[AdditionalConstraintsElementType],
    },
    total=False,
)


class CreateBackendAuthPasswordPolicyConfigTypeDef(
    _RequiredCreateBackendAuthPasswordPolicyConfigTypeDef,
    _OptionalCreateBackendAuthPasswordPolicyConfigTypeDef,
):
    pass


_RequiredCreateBackendConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBackendConfigRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalCreateBackendConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBackendConfigRequestRequestTypeDef",
    {
        "BackendManagerAppId": str,
    },
    total=False,
)


class CreateBackendConfigRequestRequestTypeDef(
    _RequiredCreateBackendConfigRequestRequestTypeDef,
    _OptionalCreateBackendConfigRequestRequestTypeDef,
):
    pass


_RequiredCreateBackendRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBackendRequestRequestTypeDef",
    {
        "AppId": str,
        "AppName": str,
        "BackendEnvironmentName": str,
    },
)
_OptionalCreateBackendRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBackendRequestRequestTypeDef",
    {
        "ResourceConfig": Mapping[str, Any],
        "ResourceName": str,
    },
    total=False,
)


class CreateBackendRequestRequestTypeDef(
    _RequiredCreateBackendRequestRequestTypeDef, _OptionalCreateBackendRequestRequestTypeDef
):
    pass


CreateTokenRequestRequestTypeDef = TypedDict(
    "CreateTokenRequestRequestTypeDef",
    {
        "AppId": str,
    },
)

DeleteBackendAuthRequestRequestTypeDef = TypedDict(
    "DeleteBackendAuthRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)

DeleteBackendRequestRequestTypeDef = TypedDict(
    "DeleteBackendRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
    },
)

DeleteBackendStorageRequestRequestTypeDef = TypedDict(
    "DeleteBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
        "ServiceName": Literal["S3"],
    },
)

DeleteTokenRequestRequestTypeDef = TypedDict(
    "DeleteTokenRequestRequestTypeDef",
    {
        "AppId": str,
        "SessionId": str,
    },
)

GenerateBackendAPIModelsRequestRequestTypeDef = TypedDict(
    "GenerateBackendAPIModelsRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)

GetBackendAPIModelsRequestRequestTypeDef = TypedDict(
    "GetBackendAPIModelsRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)

GetBackendAuthRequestRequestTypeDef = TypedDict(
    "GetBackendAuthRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)

GetBackendJobRequestRequestTypeDef = TypedDict(
    "GetBackendJobRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
    },
)

_RequiredGetBackendRequestRequestTypeDef = TypedDict(
    "_RequiredGetBackendRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalGetBackendRequestRequestTypeDef = TypedDict(
    "_OptionalGetBackendRequestRequestTypeDef",
    {
        "BackendEnvironmentName": str,
    },
    total=False,
)


class GetBackendRequestRequestTypeDef(
    _RequiredGetBackendRequestRequestTypeDef, _OptionalGetBackendRequestRequestTypeDef
):
    pass


GetBackendStorageRequestRequestTypeDef = TypedDict(
    "GetBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)

GetTokenRequestRequestTypeDef = TypedDict(
    "GetTokenRequestRequestTypeDef",
    {
        "AppId": str,
        "SessionId": str,
    },
)

_RequiredImportBackendAuthRequestRequestTypeDef = TypedDict(
    "_RequiredImportBackendAuthRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "NativeClientId": str,
        "UserPoolId": str,
        "WebClientId": str,
    },
)
_OptionalImportBackendAuthRequestRequestTypeDef = TypedDict(
    "_OptionalImportBackendAuthRequestRequestTypeDef",
    {
        "IdentityPoolId": str,
    },
    total=False,
)


class ImportBackendAuthRequestRequestTypeDef(
    _RequiredImportBackendAuthRequestRequestTypeDef, _OptionalImportBackendAuthRequestRequestTypeDef
):
    pass


_RequiredImportBackendStorageRequestRequestTypeDef = TypedDict(
    "_RequiredImportBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ServiceName": Literal["S3"],
    },
)
_OptionalImportBackendStorageRequestRequestTypeDef = TypedDict(
    "_OptionalImportBackendStorageRequestRequestTypeDef",
    {
        "BucketName": str,
    },
    total=False,
)


class ImportBackendStorageRequestRequestTypeDef(
    _RequiredImportBackendStorageRequestRequestTypeDef,
    _OptionalImportBackendStorageRequestRequestTypeDef,
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

_RequiredListBackendJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListBackendJobsRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
    },
)
_OptionalListBackendJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListBackendJobsRequestRequestTypeDef",
    {
        "JobId": str,
        "MaxResults": int,
        "NextToken": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)


class ListBackendJobsRequestRequestTypeDef(
    _RequiredListBackendJobsRequestRequestTypeDef, _OptionalListBackendJobsRequestRequestTypeDef
):
    pass


ListS3BucketsRequestRequestTypeDef = TypedDict(
    "ListS3BucketsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

S3BucketInfoTypeDef = TypedDict(
    "S3BucketInfoTypeDef",
    {
        "CreationDate": str,
        "Name": str,
    },
    total=False,
)

LoginAuthConfigReqObjTypeDef = TypedDict(
    "LoginAuthConfigReqObjTypeDef",
    {
        "AwsCognitoIdentityPoolId": str,
        "AwsCognitoRegion": str,
        "AwsUserPoolsId": str,
        "AwsUserPoolsWebClientId": str,
    },
    total=False,
)

_RequiredRemoveAllBackendsRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveAllBackendsRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalRemoveAllBackendsRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveAllBackendsRequestRequestTypeDef",
    {
        "CleanAmplifyApp": bool,
    },
    total=False,
)


class RemoveAllBackendsRequestRequestTypeDef(
    _RequiredRemoveAllBackendsRequestRequestTypeDef, _OptionalRemoveAllBackendsRequestRequestTypeDef
):
    pass


RemoveBackendConfigRequestRequestTypeDef = TypedDict(
    "RemoveBackendConfigRequestRequestTypeDef",
    {
        "AppId": str,
    },
)

UpdateBackendAuthIdentityPoolConfigTypeDef = TypedDict(
    "UpdateBackendAuthIdentityPoolConfigTypeDef",
    {
        "UnauthenticatedLogin": bool,
    },
    total=False,
)

UpdateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    {
        "AdditionalConstraints": Sequence[AdditionalConstraintsElementType],
        "MinimumLength": float,
    },
    total=False,
)

_RequiredUpdateBackendJobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBackendJobRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
    },
)
_OptionalUpdateBackendJobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBackendJobRequestRequestTypeDef",
    {
        "Operation": str,
        "Status": str,
    },
    total=False,
)


class UpdateBackendJobRequestRequestTypeDef(
    _RequiredUpdateBackendJobRequestRequestTypeDef, _OptionalUpdateBackendJobRequestRequestTypeDef
):
    pass


BackendAPIAuthTypeTypeDef = TypedDict(
    "BackendAPIAuthTypeTypeDef",
    {
        "Mode": ModeType,
        "Settings": BackendAPIAppSyncAuthSettingsTypeDef,
    },
    total=False,
)

SocialProviderSettingsTypeDef = TypedDict(
    "SocialProviderSettingsTypeDef",
    {
        "Facebook": BackendAuthSocialProviderConfigTypeDef,
        "Google": BackendAuthSocialProviderConfigTypeDef,
        "LoginWithAmazon": BackendAuthSocialProviderConfigTypeDef,
        "SignInWithApple": BackendAuthAppleProviderConfigTypeDef,
    },
    total=False,
)

_RequiredCreateBackendStorageResourceConfigTypeDef = TypedDict(
    "_RequiredCreateBackendStorageResourceConfigTypeDef",
    {
        "Permissions": BackendStoragePermissionsTypeDef,
        "ServiceName": Literal["S3"],
    },
)
_OptionalCreateBackendStorageResourceConfigTypeDef = TypedDict(
    "_OptionalCreateBackendStorageResourceConfigTypeDef",
    {
        "BucketName": str,
    },
    total=False,
)


class CreateBackendStorageResourceConfigTypeDef(
    _RequiredCreateBackendStorageResourceConfigTypeDef,
    _OptionalCreateBackendStorageResourceConfigTypeDef,
):
    pass


_RequiredGetBackendStorageResourceConfigTypeDef = TypedDict(
    "_RequiredGetBackendStorageResourceConfigTypeDef",
    {
        "Imported": bool,
        "ServiceName": Literal["S3"],
    },
)
_OptionalGetBackendStorageResourceConfigTypeDef = TypedDict(
    "_OptionalGetBackendStorageResourceConfigTypeDef",
    {
        "BucketName": str,
        "Permissions": BackendStoragePermissionsTypeDef,
    },
    total=False,
)


class GetBackendStorageResourceConfigTypeDef(
    _RequiredGetBackendStorageResourceConfigTypeDef, _OptionalGetBackendStorageResourceConfigTypeDef
):
    pass


UpdateBackendStorageResourceConfigTypeDef = TypedDict(
    "UpdateBackendStorageResourceConfigTypeDef",
    {
        "Permissions": BackendStoragePermissionsTypeDef,
        "ServiceName": Literal["S3"],
    },
)

CloneBackendResponseTypeDef = TypedDict(
    "CloneBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackendAPIResponseTypeDef = TypedDict(
    "CreateBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackendAuthResponseTypeDef = TypedDict(
    "CreateBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackendConfigResponseTypeDef = TypedDict(
    "CreateBackendConfigResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackendResponseTypeDef = TypedDict(
    "CreateBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackendStorageResponseTypeDef = TypedDict(
    "CreateBackendStorageResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTokenResponseTypeDef = TypedDict(
    "CreateTokenResponseTypeDef",
    {
        "AppId": str,
        "ChallengeCode": str,
        "SessionId": str,
        "Ttl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendAPIResponseTypeDef = TypedDict(
    "DeleteBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendAuthResponseTypeDef = TypedDict(
    "DeleteBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendResponseTypeDef = TypedDict(
    "DeleteBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendStorageResponseTypeDef = TypedDict(
    "DeleteBackendStorageResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTokenResponseTypeDef = TypedDict(
    "DeleteTokenResponseTypeDef",
    {
        "IsSuccess": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateBackendAPIModelsResponseTypeDef = TypedDict(
    "GenerateBackendAPIModelsResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackendAPIModelsResponseTypeDef = TypedDict(
    "GetBackendAPIModelsResponseTypeDef",
    {
        "Models": str,
        "Status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackendJobResponseTypeDef = TypedDict(
    "GetBackendJobResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackendResponseTypeDef = TypedDict(
    "GetBackendResponseTypeDef",
    {
        "AmplifyFeatureFlags": str,
        "AmplifyMetaConfig": str,
        "AppId": str,
        "AppName": str,
        "BackendEnvironmentList": List[str],
        "BackendEnvironmentName": str,
        "Error": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTokenResponseTypeDef = TypedDict(
    "GetTokenResponseTypeDef",
    {
        "AppId": str,
        "ChallengeCode": str,
        "SessionId": str,
        "Ttl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportBackendAuthResponseTypeDef = TypedDict(
    "ImportBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportBackendStorageResponseTypeDef = TypedDict(
    "ImportBackendStorageResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackendJobsResponseTypeDef = TypedDict(
    "ListBackendJobsResponseTypeDef",
    {
        "Jobs": List[BackendJobRespObjTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveAllBackendsResponseTypeDef = TypedDict(
    "RemoveAllBackendsResponseTypeDef",
    {
        "AppId": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveBackendConfigResponseTypeDef = TypedDict(
    "RemoveBackendConfigResponseTypeDef",
    {
        "Error": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendAPIResponseTypeDef = TypedDict(
    "UpdateBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendAuthResponseTypeDef = TypedDict(
    "UpdateBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendJobResponseTypeDef = TypedDict(
    "UpdateBackendJobResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendStorageResponseTypeDef = TypedDict(
    "UpdateBackendStorageResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "JobId": str,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthForgotPasswordConfigTypeDef",
    {
        "DeliveryMethod": DeliveryMethodType,
    },
)
_OptionalCreateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthForgotPasswordConfigTypeDef",
    {
        "EmailSettings": EmailSettingsTypeDef,
        "SmsSettings": SmsSettingsTypeDef,
    },
    total=False,
)


class CreateBackendAuthForgotPasswordConfigTypeDef(
    _RequiredCreateBackendAuthForgotPasswordConfigTypeDef,
    _OptionalCreateBackendAuthForgotPasswordConfigTypeDef,
):
    pass


_RequiredCreateBackendAuthVerificationMessageConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthVerificationMessageConfigTypeDef",
    {
        "DeliveryMethod": DeliveryMethodType,
    },
)
_OptionalCreateBackendAuthVerificationMessageConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthVerificationMessageConfigTypeDef",
    {
        "EmailSettings": EmailSettingsTypeDef,
        "SmsSettings": SmsSettingsTypeDef,
    },
    total=False,
)


class CreateBackendAuthVerificationMessageConfigTypeDef(
    _RequiredCreateBackendAuthVerificationMessageConfigTypeDef,
    _OptionalCreateBackendAuthVerificationMessageConfigTypeDef,
):
    pass


UpdateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "UpdateBackendAuthForgotPasswordConfigTypeDef",
    {
        "DeliveryMethod": DeliveryMethodType,
        "EmailSettings": EmailSettingsTypeDef,
        "SmsSettings": SmsSettingsTypeDef,
    },
    total=False,
)

_RequiredUpdateBackendAuthVerificationMessageConfigTypeDef = TypedDict(
    "_RequiredUpdateBackendAuthVerificationMessageConfigTypeDef",
    {
        "DeliveryMethod": DeliveryMethodType,
    },
)
_OptionalUpdateBackendAuthVerificationMessageConfigTypeDef = TypedDict(
    "_OptionalUpdateBackendAuthVerificationMessageConfigTypeDef",
    {
        "EmailSettings": EmailSettingsTypeDef,
        "SmsSettings": SmsSettingsTypeDef,
    },
    total=False,
)


class UpdateBackendAuthVerificationMessageConfigTypeDef(
    _RequiredUpdateBackendAuthVerificationMessageConfigTypeDef,
    _OptionalUpdateBackendAuthVerificationMessageConfigTypeDef,
):
    pass


_RequiredCreateBackendAuthMFAConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthMFAConfigTypeDef",
    {
        "MFAMode": MFAModeType,
    },
)
_OptionalCreateBackendAuthMFAConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthMFAConfigTypeDef",
    {
        "Settings": SettingsTypeDef,
    },
    total=False,
)


class CreateBackendAuthMFAConfigTypeDef(
    _RequiredCreateBackendAuthMFAConfigTypeDef, _OptionalCreateBackendAuthMFAConfigTypeDef
):
    pass


UpdateBackendAuthMFAConfigTypeDef = TypedDict(
    "UpdateBackendAuthMFAConfigTypeDef",
    {
        "MFAMode": MFAModeType,
        "Settings": SettingsTypeDef,
    },
    total=False,
)

_RequiredListBackendJobsRequestListBackendJobsPaginateTypeDef = TypedDict(
    "_RequiredListBackendJobsRequestListBackendJobsPaginateTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
    },
)
_OptionalListBackendJobsRequestListBackendJobsPaginateTypeDef = TypedDict(
    "_OptionalListBackendJobsRequestListBackendJobsPaginateTypeDef",
    {
        "JobId": str,
        "Operation": str,
        "Status": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListBackendJobsRequestListBackendJobsPaginateTypeDef(
    _RequiredListBackendJobsRequestListBackendJobsPaginateTypeDef,
    _OptionalListBackendJobsRequestListBackendJobsPaginateTypeDef,
):
    pass


ListS3BucketsResponseTypeDef = TypedDict(
    "ListS3BucketsResponseTypeDef",
    {
        "Buckets": List[S3BucketInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateBackendConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBackendConfigRequestRequestTypeDef",
    {
        "AppId": str,
    },
)
_OptionalUpdateBackendConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBackendConfigRequestRequestTypeDef",
    {
        "LoginAuthConfig": LoginAuthConfigReqObjTypeDef,
    },
    total=False,
)


class UpdateBackendConfigRequestRequestTypeDef(
    _RequiredUpdateBackendConfigRequestRequestTypeDef,
    _OptionalUpdateBackendConfigRequestRequestTypeDef,
):
    pass


UpdateBackendConfigResponseTypeDef = TypedDict(
    "UpdateBackendConfigResponseTypeDef",
    {
        "AppId": str,
        "BackendManagerAppId": str,
        "Error": str,
        "LoginAuthConfig": LoginAuthConfigReqObjTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BackendAPIResourceConfigTypeDef = TypedDict(
    "BackendAPIResourceConfigTypeDef",
    {
        "AdditionalAuthTypes": Sequence[BackendAPIAuthTypeTypeDef],
        "ApiName": str,
        "ConflictResolution": BackendAPIConflictResolutionTypeDef,
        "DefaultAuthType": BackendAPIAuthTypeTypeDef,
        "Service": str,
        "TransformSchema": str,
    },
    total=False,
)

_RequiredCreateBackendAuthOAuthConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthOAuthConfigTypeDef",
    {
        "OAuthGrantType": OAuthGrantTypeType,
        "OAuthScopes": Sequence[OAuthScopesElementType],
        "RedirectSignInURIs": Sequence[str],
        "RedirectSignOutURIs": Sequence[str],
    },
)
_OptionalCreateBackendAuthOAuthConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthOAuthConfigTypeDef",
    {
        "DomainPrefix": str,
        "SocialProviderSettings": SocialProviderSettingsTypeDef,
    },
    total=False,
)


class CreateBackendAuthOAuthConfigTypeDef(
    _RequiredCreateBackendAuthOAuthConfigTypeDef, _OptionalCreateBackendAuthOAuthConfigTypeDef
):
    pass


UpdateBackendAuthOAuthConfigTypeDef = TypedDict(
    "UpdateBackendAuthOAuthConfigTypeDef",
    {
        "DomainPrefix": str,
        "OAuthGrantType": OAuthGrantTypeType,
        "OAuthScopes": Sequence[OAuthScopesElementType],
        "RedirectSignInURIs": Sequence[str],
        "RedirectSignOutURIs": Sequence[str],
        "SocialProviderSettings": SocialProviderSettingsTypeDef,
    },
    total=False,
)

CreateBackendStorageRequestRequestTypeDef = TypedDict(
    "CreateBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": CreateBackendStorageResourceConfigTypeDef,
        "ResourceName": str,
    },
)

GetBackendStorageResponseTypeDef = TypedDict(
    "GetBackendStorageResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": GetBackendStorageResourceConfigTypeDef,
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendStorageRequestRequestTypeDef = TypedDict(
    "UpdateBackendStorageRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": UpdateBackendStorageResourceConfigTypeDef,
        "ResourceName": str,
    },
)

CreateBackendAPIRequestRequestTypeDef = TypedDict(
    "CreateBackendAPIRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": BackendAPIResourceConfigTypeDef,
        "ResourceName": str,
    },
)

_RequiredDeleteBackendAPIRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBackendAPIRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)
_OptionalDeleteBackendAPIRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBackendAPIRequestRequestTypeDef",
    {
        "ResourceConfig": BackendAPIResourceConfigTypeDef,
    },
    total=False,
)


class DeleteBackendAPIRequestRequestTypeDef(
    _RequiredDeleteBackendAPIRequestRequestTypeDef, _OptionalDeleteBackendAPIRequestRequestTypeDef
):
    pass


_RequiredGetBackendAPIRequestRequestTypeDef = TypedDict(
    "_RequiredGetBackendAPIRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)
_OptionalGetBackendAPIRequestRequestTypeDef = TypedDict(
    "_OptionalGetBackendAPIRequestRequestTypeDef",
    {
        "ResourceConfig": BackendAPIResourceConfigTypeDef,
    },
    total=False,
)


class GetBackendAPIRequestRequestTypeDef(
    _RequiredGetBackendAPIRequestRequestTypeDef, _OptionalGetBackendAPIRequestRequestTypeDef
):
    pass


GetBackendAPIResponseTypeDef = TypedDict(
    "GetBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "ResourceConfig": BackendAPIResourceConfigTypeDef,
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateBackendAPIRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBackendAPIRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceName": str,
    },
)
_OptionalUpdateBackendAPIRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBackendAPIRequestRequestTypeDef",
    {
        "ResourceConfig": BackendAPIResourceConfigTypeDef,
    },
    total=False,
)


class UpdateBackendAPIRequestRequestTypeDef(
    _RequiredUpdateBackendAPIRequestRequestTypeDef, _OptionalUpdateBackendAPIRequestRequestTypeDef
):
    pass


_RequiredCreateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthUserPoolConfigTypeDef",
    {
        "RequiredSignUpAttributes": Sequence[RequiredSignUpAttributesElementType],
        "SignInMethod": SignInMethodType,
        "UserPoolName": str,
    },
)
_OptionalCreateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthUserPoolConfigTypeDef",
    {
        "ForgotPassword": CreateBackendAuthForgotPasswordConfigTypeDef,
        "Mfa": CreateBackendAuthMFAConfigTypeDef,
        "OAuth": CreateBackendAuthOAuthConfigTypeDef,
        "PasswordPolicy": CreateBackendAuthPasswordPolicyConfigTypeDef,
        "VerificationMessage": CreateBackendAuthVerificationMessageConfigTypeDef,
    },
    total=False,
)


class CreateBackendAuthUserPoolConfigTypeDef(
    _RequiredCreateBackendAuthUserPoolConfigTypeDef, _OptionalCreateBackendAuthUserPoolConfigTypeDef
):
    pass


UpdateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "UpdateBackendAuthUserPoolConfigTypeDef",
    {
        "ForgotPassword": UpdateBackendAuthForgotPasswordConfigTypeDef,
        "Mfa": UpdateBackendAuthMFAConfigTypeDef,
        "OAuth": UpdateBackendAuthOAuthConfigTypeDef,
        "PasswordPolicy": UpdateBackendAuthPasswordPolicyConfigTypeDef,
        "VerificationMessage": UpdateBackendAuthVerificationMessageConfigTypeDef,
    },
    total=False,
)

_RequiredCreateBackendAuthResourceConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthResourceConfigTypeDef",
    {
        "AuthResources": AuthResourcesType,
        "Service": Literal["COGNITO"],
        "UserPoolConfigs": CreateBackendAuthUserPoolConfigTypeDef,
    },
)
_OptionalCreateBackendAuthResourceConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthResourceConfigTypeDef",
    {
        "IdentityPoolConfigs": CreateBackendAuthIdentityPoolConfigTypeDef,
    },
    total=False,
)


class CreateBackendAuthResourceConfigTypeDef(
    _RequiredCreateBackendAuthResourceConfigTypeDef, _OptionalCreateBackendAuthResourceConfigTypeDef
):
    pass


_RequiredUpdateBackendAuthResourceConfigTypeDef = TypedDict(
    "_RequiredUpdateBackendAuthResourceConfigTypeDef",
    {
        "AuthResources": AuthResourcesType,
        "Service": Literal["COGNITO"],
        "UserPoolConfigs": UpdateBackendAuthUserPoolConfigTypeDef,
    },
)
_OptionalUpdateBackendAuthResourceConfigTypeDef = TypedDict(
    "_OptionalUpdateBackendAuthResourceConfigTypeDef",
    {
        "IdentityPoolConfigs": UpdateBackendAuthIdentityPoolConfigTypeDef,
    },
    total=False,
)


class UpdateBackendAuthResourceConfigTypeDef(
    _RequiredUpdateBackendAuthResourceConfigTypeDef, _OptionalUpdateBackendAuthResourceConfigTypeDef
):
    pass


CreateBackendAuthRequestRequestTypeDef = TypedDict(
    "CreateBackendAuthRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": CreateBackendAuthResourceConfigTypeDef,
        "ResourceName": str,
    },
)

GetBackendAuthResponseTypeDef = TypedDict(
    "GetBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "ResourceConfig": CreateBackendAuthResourceConfigTypeDef,
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackendAuthRequestRequestTypeDef = TypedDict(
    "UpdateBackendAuthRequestRequestTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "ResourceConfig": UpdateBackendAuthResourceConfigTypeDef,
        "ResourceName": str,
    },
)
