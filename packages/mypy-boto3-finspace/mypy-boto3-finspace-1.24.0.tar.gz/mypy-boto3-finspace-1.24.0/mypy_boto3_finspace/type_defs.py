"""
Type annotations for finspace service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/type_defs/)

Usage::

    ```python
    from mypy_boto3_finspace.type_defs import FederationParametersTypeDef

    data: FederationParametersTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import EnvironmentStatusType, FederationModeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FederationParametersTypeDef",
    "SuperuserParametersTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "EnvironmentTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "GetEnvironmentResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "UpdateEnvironmentResponseTypeDef",
)

FederationParametersTypeDef = TypedDict(
    "FederationParametersTypeDef",
    {
        "samlMetadataDocument": str,
        "samlMetadataURL": str,
        "applicationCallBackURL": str,
        "federationURN": str,
        "federationProviderName": str,
        "attributeMap": Mapping[str, str],
    },
    total=False,
)

SuperuserParametersTypeDef = TypedDict(
    "SuperuserParametersTypeDef",
    {
        "emailAddress": str,
        "firstName": str,
        "lastName": str,
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

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
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

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "environmentUrl": str,
        "description": str,
        "environmentArn": str,
        "sageMakerStudioDomainUrl": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
    },
    total=False,
)

_RequiredUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
    },
    total=False,
)


class UpdateEnvironmentRequestRequestTypeDef(
    _RequiredUpdateEnvironmentRequestRequestTypeDef, _OptionalUpdateEnvironmentRequestRequestTypeDef
):
    pass


_RequiredCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentRequestRequestTypeDef",
    {
        "description": str,
        "kmsKeyId": str,
        "tags": Mapping[str, str],
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
        "superuserParameters": SuperuserParametersTypeDef,
        "dataBundles": Sequence[str],
    },
    total=False,
)


class CreateEnvironmentRequestRequestTypeDef(
    _RequiredCreateEnvironmentRequestRequestTypeDef, _OptionalCreateEnvironmentRequestRequestTypeDef
):
    pass


CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "environmentArn": str,
        "environmentUrl": str,
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

GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "environments": List[EnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentResponseTypeDef = TypedDict(
    "UpdateEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
