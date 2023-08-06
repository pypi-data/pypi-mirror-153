"""Declares :class:`Event`."""
from .basemessage import BaseMessage
from .messagemetaclass import MessageMetaclass


class EventMetaclass(MessageMetaclass):
    envelope_field: str = 'data'
    message_type: str = "unimatrixone.io/event"


class Event(BaseMessage, metaclass=EventMetaclass):
    """The parameters for a :term:`Event`."""
    __abstract__: bool = True
