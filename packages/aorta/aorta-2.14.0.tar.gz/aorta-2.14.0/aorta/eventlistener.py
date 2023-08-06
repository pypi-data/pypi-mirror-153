"""Declares :class:`EventListener`."""
from .event import Event
from .eventlistenermetaclass import EventListenerMetaclass
from .messagehandler import MessageHandler


class EventListener(MessageHandler, metaclass=EventListenerMetaclass):
    """Handles event messages."""
    __module__: str = 'aorta'
    __abstract__: bool = True
