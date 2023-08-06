"""Declares :class:`CommandIssuer`."""
import asyncio
import typing

from .models import Message
from .sender import Sender


class CommandIssuer(Sender):
    """Provides an interface to issue commands."""

    def prepare(self, dto: dict, correlation_id: str = None) -> Message:
        """Prepares a Data Transfer Object (DTO) representing an event."""
        dto['type'] = "unimatrixone.io/command"
        return super().prepare(dto, correlation_id=correlation_id)

    async def publish(self,
        dto: typing.Union[dict, Message],
        correlation_id: str = None
    ):
        """Issue a command to the gateway."""
        if not isinstance(dto, Message):
            dto['type'] = "unimatrixone.io/command"
            dto = self.prepare(dto, correlation_id=correlation_id)
        await self.send(dto)
