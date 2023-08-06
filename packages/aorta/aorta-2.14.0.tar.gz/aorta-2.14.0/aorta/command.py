"""Declares :class:`Command`."""
from .basemessage import BaseMessage
from .messagemetaclass import MessageMetaclass


class CommandMetaclass(MessageMetaclass):
    envelope_field: str = 'spec'
    message_type: str = 'unimatrixone.io/command'


class Command(BaseMessage, metaclass=CommandMetaclass):
    """The parameters for a :term:`Command`."""
    __abstract__: bool = True
