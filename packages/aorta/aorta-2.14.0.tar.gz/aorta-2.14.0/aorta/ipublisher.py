"""Declares :class:`IPublisher`."""
from .command import Command
from .event import Event


class IPublisher:
    """Specifies the interface for message publishers."""

    def event(self, event: Event):
        raise NotImplementedError

    def issue(self, command: Command):
        raise NotImplementedError
