"""
Type annotations for ec2-instance-connect service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ec2_instance_connect.client import EC2InstanceConnectClient

    session = Session()
    client: EC2InstanceConnectClient = session.client("ec2-instance-connect")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import SendSerialConsoleSSHPublicKeyResponseTypeDef, SendSSHPublicKeyResponseTypeDef

__all__ = ("EC2InstanceConnectClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AuthException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    EC2InstanceNotFoundException: Type[BotocoreClientError]
    EC2InstanceStateInvalidException: Type[BotocoreClientError]
    EC2InstanceTypeInvalidException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    SerialConsoleAccessDisabledException: Type[BotocoreClientError]
    SerialConsoleSessionLimitExceededException: Type[BotocoreClientError]
    SerialConsoleSessionUnavailableException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class EC2InstanceConnectClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EC2InstanceConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/#generate_presigned_url)
        """

    def send_serial_console_ssh_public_key(
        self, *, InstanceId: str, SSHPublicKey: str, SerialPort: int = ...
    ) -> SendSerialConsoleSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.send_serial_console_ssh_public_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/#send_serial_console_ssh_public_key)
        """

    def send_ssh_public_key(
        self,
        *,
        InstanceId: str,
        InstanceOSUser: str,
        SSHPublicKey: str,
        AvailabilityZone: str = ...
    ) -> SendSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance for use by the specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.send_ssh_public_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/client/#send_ssh_public_key)
        """
