"""Declares :class:`CommandHandlerMetaclass`."""
from .command import Command
from .messagehandlermetaclass import MessageHandlerMetaclass


class CommandHandlerMetaclass(MessageHandlerMetaclass):
    handles: type = Command
    parameter_name: str = 'command'
