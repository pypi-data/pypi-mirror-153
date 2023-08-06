"""Declares :class:`NullTransport`."""
import typing

from ..models import MessageHeader
from .itransport import ITransport


class NullTransport(ITransport):
    """A transport implementation that does nothing."""

    async def send(self, objects: typing.List[MessageHeader]):
        pass
