"""Declares :class:`Message`."""
import pydantic
from unimatrix.lib import timezone

from .messagemetadata import MessageMetadata


class MessageHeader(pydantic.BaseModel):
    api_version: str = pydantic.Field(..., alias='apiVersion')
    kind: str = pydantic.Field(...)
    type: str = pydantic.Field(None)
    metadata: MessageMetadata = pydantic.Field(
        default_factory=MessageMetadata
    )

    @property
    def age(self) -> int:
        """Return the age of the message as a UNIX timestamp, in milliseconds
        since the UNIX epoch.
        """
        return timezone.now() - self.metadata.published

    @property
    def qualname(self) -> tuple:
        """Return the qualified name of the message type."""
        return (self.api_version, self.kind)

    def accept(self):
        """Accepts the message. This method is invoked by the runner of the
        message handlers.
        """
        self.metadata.delivery_count += 1

    def is_command(self) -> bool:
        """Return a boolean indicating if the message is a command."""
        return self.type == "unimatrixone.io/command"

    def is_event(self) -> bool:
        """Return a boolean indicating if the message is an event."""
        return self.type == "unimatrixone.io/event"

    def is_expired(self) -> bool:
        """Return a boolean indicating if the message is expired."""
        return (self.age > self.metadata.ttl)\
            if self.metadata.ttl\
            else False

    def is_valid(self, now: int = None) -> bool:
        """Return a boolean indicating if the message is still valid."""
        return not self.is_expired()

    def get_object(self):
        """Return the concrete object type for this message."""
        return self._params

    def __bytes__(self) -> bytes:
        return str.encode(
            self.json(by_alias=True, exclude_defaults=True),
            "utf-8"
        )
