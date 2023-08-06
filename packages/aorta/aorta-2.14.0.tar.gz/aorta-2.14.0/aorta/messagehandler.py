"""Declares :class:`MessageHandler`."""
import asyncio
import inspect
import logging
import typing

from .command import Command
from .event import Event
from .ipublisher import IPublisher
from .models import Message as Envelope


class MessageHandler:
    """The base class for all message handlers."""
    __module__: str = 'aorta'
    __abstract__: bool = True
    handles: list[type[Command] | type[Event]]
    logger: logging.Logger = logging.getLogger('uvicorn')

    @property
    def args(self) -> typing.Union[Command, Event]:
        """Return the message arguments."""
        return self._object

    async def handle(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        raise NotImplementedError

    def issue(self, command: Command):
        """Issue a command using the default command issuer."""
        self._publisher.issue(command)

    async def on_exception(self, exception: Exception) -> bool:
        """Hook to perform cleanup after a fatal exception. Return a boolean
        indicating if the exception may be suppressed.
        """
        return False

    def publish(self, event: Event):
        """Publish an event using the default event publisher."""
        self._publisher.publish(event)