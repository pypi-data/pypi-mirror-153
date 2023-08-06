"""
Type annotations for ec2-instance-connect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/type_defs/)

Usage::

    ```python
    from mypy_boto3_ec2_instance_connect.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = {...}
    ```
"""
import sys
from typing import Dict

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "SendSSHPublicKeyRequestRequestTypeDef",
    "SendSerialConsoleSSHPublicKeyRequestRequestTypeDef",
    "SendSSHPublicKeyResponseTypeDef",
    "SendSerialConsoleSSHPublicKeyResponseTypeDef",
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

_RequiredSendSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "_RequiredSendSSHPublicKeyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "InstanceOSUser": str,
        "SSHPublicKey": str,
    },
)
_OptionalSendSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "_OptionalSendSSHPublicKeyRequestRequestTypeDef",
    {
        "AvailabilityZone": str,
    },
    total=False,
)


class SendSSHPublicKeyRequestRequestTypeDef(
    _RequiredSendSSHPublicKeyRequestRequestTypeDef, _OptionalSendSSHPublicKeyRequestRequestTypeDef
):
    pass


_RequiredSendSerialConsoleSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "_RequiredSendSerialConsoleSSHPublicKeyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "SSHPublicKey": str,
    },
)
_OptionalSendSerialConsoleSSHPublicKeyRequestRequestTypeDef = TypedDict(
    "_OptionalSendSerialConsoleSSHPublicKeyRequestRequestTypeDef",
    {
        "SerialPort": int,
    },
    total=False,
)


class SendSerialConsoleSSHPublicKeyRequestRequestTypeDef(
    _RequiredSendSerialConsoleSSHPublicKeyRequestRequestTypeDef,
    _OptionalSendSerialConsoleSSHPublicKeyRequestRequestTypeDef,
):
    pass


SendSSHPublicKeyResponseTypeDef = TypedDict(
    "SendSSHPublicKeyResponseTypeDef",
    {
        "RequestId": str,
        "Success": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendSerialConsoleSSHPublicKeyResponseTypeDef = TypedDict(
    "SendSerialConsoleSSHPublicKeyResponseTypeDef",
    {
        "RequestId": str,
        "Success": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
