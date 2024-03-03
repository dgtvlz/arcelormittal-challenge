from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SalesMessage(_message.Message):
    __slots__ = ("item", "quantity", "price", "date")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    item: str
    quantity: int
    price: float
    date: str
    def __init__(self, item: _Optional[str] = ..., quantity: _Optional[int] = ..., price: _Optional[float] = ..., date: _Optional[str] = ...) -> None: ...

class ConfirmationReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
