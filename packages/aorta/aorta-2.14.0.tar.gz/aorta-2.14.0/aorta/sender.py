"""Declares :class:`Sender`."""
import uuid

from unimatrix.lib import timezone

from .models import Message
from .transport import ITransport


class Sender:

    @property
    def transport(self) -> ITransport:
        """Return the transport used to publish message."""
        return self._transport

    def __init__(self, transport: ITransport):
        self._transport = transport

    def prepare(self, dto: dict, correlation_id: str = None) -> Message:
        """Prepares a Data Transfer Object (DTO) representing a message."""
        metadata = dto.setdefault('metadata', {})
        metadata.update({
            'messageId': uuid.uuid4(),
            'correlationId': correlation_id or uuid.uuid4(),
            'published': timezone.now()
        })
        return Message(**dto)

    async def send(self, message: Message | list[Message]) -> None:
        """Sends `message` to the upstream peer."""
        return await self._transport.publish(message)
