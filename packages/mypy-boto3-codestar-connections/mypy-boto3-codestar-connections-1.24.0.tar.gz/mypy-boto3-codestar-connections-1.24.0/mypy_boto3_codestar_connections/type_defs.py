"""
Type annotations for codestar-connections service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codestar_connections/type_defs/)

Usage::

    ```python
    from mypy_boto3_codestar_connections.type_defs import ConnectionTypeDef

    data: ConnectionTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import ConnectionStatusType, ProviderTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ConnectionTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "VpcConfigurationTypeDef",
    "DeleteConnectionInputRequestTypeDef",
    "DeleteHostInputRequestTypeDef",
    "GetConnectionInputRequestTypeDef",
    "GetHostInputRequestTypeDef",
    "ListConnectionsInputRequestTypeDef",
    "ListHostsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "CreateConnectionInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "CreateConnectionOutputTypeDef",
    "CreateHostOutputTypeDef",
    "GetConnectionOutputTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "CreateHostInputRequestTypeDef",
    "GetHostOutputTypeDef",
    "HostTypeDef",
    "UpdateHostInputRequestTypeDef",
    "ListHostsOutputTypeDef",
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ConnectionName": str,
        "ConnectionArn": str,
        "ProviderType": ProviderTypeType,
        "OwnerAccountId": str,
        "ConnectionStatus": ConnectionStatusType,
        "HostArn": str,
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

_RequiredVpcConfigurationTypeDef = TypedDict(
    "_RequiredVpcConfigurationTypeDef",
    {
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
)
_OptionalVpcConfigurationTypeDef = TypedDict(
    "_OptionalVpcConfigurationTypeDef",
    {
        "TlsCertificate": str,
    },
    total=False,
)


class VpcConfigurationTypeDef(_RequiredVpcConfigurationTypeDef, _OptionalVpcConfigurationTypeDef):
    pass


DeleteConnectionInputRequestTypeDef = TypedDict(
    "DeleteConnectionInputRequestTypeDef",
    {
        "ConnectionArn": str,
    },
)

DeleteHostInputRequestTypeDef = TypedDict(
    "DeleteHostInputRequestTypeDef",
    {
        "HostArn": str,
    },
)

GetConnectionInputRequestTypeDef = TypedDict(
    "GetConnectionInputRequestTypeDef",
    {
        "ConnectionArn": str,
    },
)

GetHostInputRequestTypeDef = TypedDict(
    "GetHostInputRequestTypeDef",
    {
        "HostArn": str,
    },
)

ListConnectionsInputRequestTypeDef = TypedDict(
    "ListConnectionsInputRequestTypeDef",
    {
        "ProviderTypeFilter": ProviderTypeType,
        "HostArnFilter": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListHostsInputRequestTypeDef = TypedDict(
    "ListHostsInputRequestTypeDef",
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

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredCreateConnectionInputRequestTypeDef = TypedDict(
    "_RequiredCreateConnectionInputRequestTypeDef",
    {
        "ConnectionName": str,
    },
)
_OptionalCreateConnectionInputRequestTypeDef = TypedDict(
    "_OptionalCreateConnectionInputRequestTypeDef",
    {
        "ProviderType": ProviderTypeType,
        "Tags": Sequence[TagTypeDef],
        "HostArn": str,
    },
    total=False,
)


class CreateConnectionInputRequestTypeDef(
    _RequiredCreateConnectionInputRequestTypeDef, _OptionalCreateConnectionInputRequestTypeDef
):
    pass


TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateConnectionOutputTypeDef = TypedDict(
    "CreateConnectionOutputTypeDef",
    {
        "ConnectionArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHostOutputTypeDef = TypedDict(
    "CreateHostOutputTypeDef",
    {
        "HostArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConnectionsOutputTypeDef = TypedDict(
    "ListConnectionsOutputTypeDef",
    {
        "Connections": List[ConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateHostInputRequestTypeDef = TypedDict(
    "_RequiredCreateHostInputRequestTypeDef",
    {
        "Name": str,
        "ProviderType": ProviderTypeType,
        "ProviderEndpoint": str,
    },
)
_OptionalCreateHostInputRequestTypeDef = TypedDict(
    "_OptionalCreateHostInputRequestTypeDef",
    {
        "VpcConfiguration": VpcConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateHostInputRequestTypeDef(
    _RequiredCreateHostInputRequestTypeDef, _OptionalCreateHostInputRequestTypeDef
):
    pass


GetHostOutputTypeDef = TypedDict(
    "GetHostOutputTypeDef",
    {
        "Name": str,
        "Status": str,
        "ProviderType": ProviderTypeType,
        "ProviderEndpoint": str,
        "VpcConfiguration": VpcConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HostTypeDef = TypedDict(
    "HostTypeDef",
    {
        "Name": str,
        "HostArn": str,
        "ProviderType": ProviderTypeType,
        "ProviderEndpoint": str,
        "VpcConfiguration": VpcConfigurationTypeDef,
        "Status": str,
        "StatusMessage": str,
    },
    total=False,
)

_RequiredUpdateHostInputRequestTypeDef = TypedDict(
    "_RequiredUpdateHostInputRequestTypeDef",
    {
        "HostArn": str,
    },
)
_OptionalUpdateHostInputRequestTypeDef = TypedDict(
    "_OptionalUpdateHostInputRequestTypeDef",
    {
        "ProviderEndpoint": str,
        "VpcConfiguration": VpcConfigurationTypeDef,
    },
    total=False,
)


class UpdateHostInputRequestTypeDef(
    _RequiredUpdateHostInputRequestTypeDef, _OptionalUpdateHostInputRequestTypeDef
):
    pass


ListHostsOutputTypeDef = TypedDict(
    "ListHostsOutputTypeDef",
    {
        "Hosts": List[HostTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
