"""
Type annotations for sts service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sts/type_defs/)

Usage::

    ```python
    from mypy_boto3_sts.type_defs import PolicyDescriptorTypeTypeDef

    data: PolicyDescriptorTypeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "PolicyDescriptorTypeTypeDef",
    "TagTypeDef",
    "AssumedRoleUserTypeDef",
    "CredentialsTypeDef",
    "ResponseMetadataTypeDef",
    "DecodeAuthorizationMessageRequestRequestTypeDef",
    "FederatedUserTypeDef",
    "GetAccessKeyInfoRequestRequestTypeDef",
    "GetSessionTokenRequestRequestTypeDef",
    "AssumeRoleWithSAMLRequestRequestTypeDef",
    "AssumeRoleWithWebIdentityRequestRequestTypeDef",
    "AssumeRoleRequestRequestTypeDef",
    "GetFederationTokenRequestRequestTypeDef",
    "AssumeRoleResponseTypeDef",
    "AssumeRoleWithSAMLResponseTypeDef",
    "AssumeRoleWithWebIdentityResponseTypeDef",
    "DecodeAuthorizationMessageResponseTypeDef",
    "GetAccessKeyInfoResponseTypeDef",
    "GetCallerIdentityResponseTypeDef",
    "GetSessionTokenResponseTypeDef",
    "GetFederationTokenResponseTypeDef",
)

PolicyDescriptorTypeTypeDef = TypedDict(
    "PolicyDescriptorTypeTypeDef",
    {
        "arn": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AssumedRoleUserTypeDef = TypedDict(
    "AssumedRoleUserTypeDef",
    {
        "AssumedRoleId": str,
        "Arn": str,
    },
)

CredentialsTypeDef = TypedDict(
    "CredentialsTypeDef",
    {
        "AccessKeyId": str,
        "SecretAccessKey": str,
        "SessionToken": str,
        "Expiration": datetime,
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

DecodeAuthorizationMessageRequestRequestTypeDef = TypedDict(
    "DecodeAuthorizationMessageRequestRequestTypeDef",
    {
        "EncodedMessage": str,
    },
)

FederatedUserTypeDef = TypedDict(
    "FederatedUserTypeDef",
    {
        "FederatedUserId": str,
        "Arn": str,
    },
)

GetAccessKeyInfoRequestRequestTypeDef = TypedDict(
    "GetAccessKeyInfoRequestRequestTypeDef",
    {
        "AccessKeyId": str,
    },
)

GetSessionTokenRequestRequestTypeDef = TypedDict(
    "GetSessionTokenRequestRequestTypeDef",
    {
        "DurationSeconds": int,
        "SerialNumber": str,
        "TokenCode": str,
    },
    total=False,
)

_RequiredAssumeRoleWithSAMLRequestRequestTypeDef = TypedDict(
    "_RequiredAssumeRoleWithSAMLRequestRequestTypeDef",
    {
        "RoleArn": str,
        "PrincipalArn": str,
        "SAMLAssertion": str,
    },
)
_OptionalAssumeRoleWithSAMLRequestRequestTypeDef = TypedDict(
    "_OptionalAssumeRoleWithSAMLRequestRequestTypeDef",
    {
        "PolicyArns": Sequence[PolicyDescriptorTypeTypeDef],
        "Policy": str,
        "DurationSeconds": int,
    },
    total=False,
)


class AssumeRoleWithSAMLRequestRequestTypeDef(
    _RequiredAssumeRoleWithSAMLRequestRequestTypeDef,
    _OptionalAssumeRoleWithSAMLRequestRequestTypeDef,
):
    pass


_RequiredAssumeRoleWithWebIdentityRequestRequestTypeDef = TypedDict(
    "_RequiredAssumeRoleWithWebIdentityRequestRequestTypeDef",
    {
        "RoleArn": str,
        "RoleSessionName": str,
        "WebIdentityToken": str,
    },
)
_OptionalAssumeRoleWithWebIdentityRequestRequestTypeDef = TypedDict(
    "_OptionalAssumeRoleWithWebIdentityRequestRequestTypeDef",
    {
        "ProviderId": str,
        "PolicyArns": Sequence[PolicyDescriptorTypeTypeDef],
        "Policy": str,
        "DurationSeconds": int,
    },
    total=False,
)


class AssumeRoleWithWebIdentityRequestRequestTypeDef(
    _RequiredAssumeRoleWithWebIdentityRequestRequestTypeDef,
    _OptionalAssumeRoleWithWebIdentityRequestRequestTypeDef,
):
    pass


_RequiredAssumeRoleRequestRequestTypeDef = TypedDict(
    "_RequiredAssumeRoleRequestRequestTypeDef",
    {
        "RoleArn": str,
        "RoleSessionName": str,
    },
)
_OptionalAssumeRoleRequestRequestTypeDef = TypedDict(
    "_OptionalAssumeRoleRequestRequestTypeDef",
    {
        "PolicyArns": Sequence[PolicyDescriptorTypeTypeDef],
        "Policy": str,
        "DurationSeconds": int,
        "Tags": Sequence[TagTypeDef],
        "TransitiveTagKeys": Sequence[str],
        "ExternalId": str,
        "SerialNumber": str,
        "TokenCode": str,
        "SourceIdentity": str,
    },
    total=False,
)


class AssumeRoleRequestRequestTypeDef(
    _RequiredAssumeRoleRequestRequestTypeDef, _OptionalAssumeRoleRequestRequestTypeDef
):
    pass


_RequiredGetFederationTokenRequestRequestTypeDef = TypedDict(
    "_RequiredGetFederationTokenRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetFederationTokenRequestRequestTypeDef = TypedDict(
    "_OptionalGetFederationTokenRequestRequestTypeDef",
    {
        "Policy": str,
        "PolicyArns": Sequence[PolicyDescriptorTypeTypeDef],
        "DurationSeconds": int,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class GetFederationTokenRequestRequestTypeDef(
    _RequiredGetFederationTokenRequestRequestTypeDef,
    _OptionalGetFederationTokenRequestRequestTypeDef,
):
    pass


AssumeRoleResponseTypeDef = TypedDict(
    "AssumeRoleResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "AssumedRoleUser": AssumedRoleUserTypeDef,
        "PackedPolicySize": int,
        "SourceIdentity": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssumeRoleWithSAMLResponseTypeDef = TypedDict(
    "AssumeRoleWithSAMLResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "AssumedRoleUser": AssumedRoleUserTypeDef,
        "PackedPolicySize": int,
        "Subject": str,
        "SubjectType": str,
        "Issuer": str,
        "Audience": str,
        "NameQualifier": str,
        "SourceIdentity": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssumeRoleWithWebIdentityResponseTypeDef = TypedDict(
    "AssumeRoleWithWebIdentityResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "SubjectFromWebIdentityToken": str,
        "AssumedRoleUser": AssumedRoleUserTypeDef,
        "PackedPolicySize": int,
        "Provider": str,
        "Audience": str,
        "SourceIdentity": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DecodeAuthorizationMessageResponseTypeDef = TypedDict(
    "DecodeAuthorizationMessageResponseTypeDef",
    {
        "DecodedMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessKeyInfoResponseTypeDef = TypedDict(
    "GetAccessKeyInfoResponseTypeDef",
    {
        "Account": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCallerIdentityResponseTypeDef = TypedDict(
    "GetCallerIdentityResponseTypeDef",
    {
        "UserId": str,
        "Account": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionTokenResponseTypeDef = TypedDict(
    "GetSessionTokenResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFederationTokenResponseTypeDef = TypedDict(
    "GetFederationTokenResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "FederatedUser": FederatedUserTypeDef,
        "PackedPolicySize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
