"""
Type annotations for iot-data service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iot_data.client import IoTDataPlaneClient

    session = Session()
    client: IoTDataPlaneClient = session.client("iot-data")
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Type, Union

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .paginator import ListRetainedMessagesPaginator
from .type_defs import (
    DeleteThingShadowResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetRetainedMessageResponseTypeDef,
    GetThingShadowResponseTypeDef,
    ListNamedShadowsForThingResponseTypeDef,
    ListRetainedMessagesResponseTypeDef,
    UpdateThingShadowResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTDataPlaneClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    RequestEntityTooLargeException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnsupportedDocumentEncodingException: Type[BotocoreClientError]


class IoTDataPlaneClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTDataPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#can_paginate)
        """

    def delete_thing_shadow(
        self, *, thingName: str, shadowName: str = ...
    ) -> DeleteThingShadowResponseTypeDef:
        """
        Deletes the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.delete_thing_shadow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#delete_thing_shadow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#generate_presigned_url)
        """

    def get_retained_message(self, *, topic: str) -> GetRetainedMessageResponseTypeDef:
        """
        Gets the details of a single retained message for the specified topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.get_retained_message)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#get_retained_message)
        """

    def get_thing_shadow(
        self, *, thingName: str, shadowName: str = ...
    ) -> GetThingShadowResponseTypeDef:
        """
        Gets the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.get_thing_shadow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#get_thing_shadow)
        """

    def list_named_shadows_for_thing(
        self, *, thingName: str, nextToken: str = ..., pageSize: int = ...
    ) -> ListNamedShadowsForThingResponseTypeDef:
        """
        Lists the shadows for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.list_named_shadows_for_thing)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#list_named_shadows_for_thing)
        """

    def list_retained_messages(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListRetainedMessagesResponseTypeDef:
        """
        Lists summary information about the retained messages stored for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.list_retained_messages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#list_retained_messages)
        """

    def publish(
        self,
        *,
        topic: str,
        qos: int = ...,
        retain: bool = ...,
        payload: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Publishes an MQTT message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.publish)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#publish)
        """

    def update_thing_shadow(
        self,
        *,
        thingName: str,
        payload: Union[str, bytes, IO[Any], StreamingBody],
        shadowName: str = ...
    ) -> UpdateThingShadowResponseTypeDef:
        """
        Updates the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.update_thing_shadow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#update_thing_shadow)
        """

    def get_paginator(
        self, operation_name: Literal["list_retained_messages"]
    ) -> ListRetainedMessagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/client/#get_paginator)
        """
