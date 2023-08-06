"""
Type annotations for iot-data service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot_data.client import IoTDataPlaneClient
    from mypy_boto3_iot_data.paginator import (
        ListRetainedMessagesPaginator,
    )

    session = Session()
    client: IoTDataPlaneClient = session.client("iot-data")

    list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListRetainedMessagesResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListRetainedMessagesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListRetainedMessagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Paginator.ListRetainedMessages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRetainedMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Paginator.ListRetainedMessages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
        """
