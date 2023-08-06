"""Declares :class:`EventListenerMetaclass`."""
from .event import Event
from .messagehandlermetaclass import MessageHandlerMetaclass


class EventListenerMetaclass(MessageHandlerMetaclass):
    handles: type = Event
    parameter_name: str = 'event'
