"""
Type annotations for sso-oidc service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso_oidc/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso_oidc.type_defs import CreateTokenRequestRequestTypeDef

    data: CreateTokenRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateTokenRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RegisterClientRequestRequestTypeDef",
    "StartDeviceAuthorizationRequestRequestTypeDef",
    "CreateTokenResponseTypeDef",
    "RegisterClientResponseTypeDef",
    "StartDeviceAuthorizationResponseTypeDef",
)

_RequiredCreateTokenRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTokenRequestRequestTypeDef",
    {
        "clientId": str,
        "clientSecret": str,
        "grantType": str,
        "deviceCode": str,
    },
)
_OptionalCreateTokenRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTokenRequestRequestTypeDef",
    {
        "code": str,
        "refreshToken": str,
        "scope": Sequence[str],
        "redirectUri": str,
    },
    total=False,
)


class CreateTokenRequestRequestTypeDef(
    _RequiredCreateTokenRequestRequestTypeDef, _OptionalCreateTokenRequestRequestTypeDef
):
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

_RequiredRegisterClientRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterClientRequestRequestTypeDef",
    {
        "clientName": str,
        "clientType": str,
    },
)
_OptionalRegisterClientRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterClientRequestRequestTypeDef",
    {
        "scopes": Sequence[str],
    },
    total=False,
)


class RegisterClientRequestRequestTypeDef(
    _RequiredRegisterClientRequestRequestTypeDef, _OptionalRegisterClientRequestRequestTypeDef
):
    pass


StartDeviceAuthorizationRequestRequestTypeDef = TypedDict(
    "StartDeviceAuthorizationRequestRequestTypeDef",
    {
        "clientId": str,
        "clientSecret": str,
        "startUrl": str,
    },
)

CreateTokenResponseTypeDef = TypedDict(
    "CreateTokenResponseTypeDef",
    {
        "accessToken": str,
        "tokenType": str,
        "expiresIn": int,
        "refreshToken": str,
        "idToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterClientResponseTypeDef = TypedDict(
    "RegisterClientResponseTypeDef",
    {
        "clientId": str,
        "clientSecret": str,
        "clientIdIssuedAt": int,
        "clientSecretExpiresAt": int,
        "authorizationEndpoint": str,
        "tokenEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDeviceAuthorizationResponseTypeDef = TypedDict(
    "StartDeviceAuthorizationResponseTypeDef",
    {
        "deviceCode": str,
        "userCode": str,
        "verificationUri": str,
        "verificationUriComplete": str,
        "expiresIn": int,
        "interval": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
