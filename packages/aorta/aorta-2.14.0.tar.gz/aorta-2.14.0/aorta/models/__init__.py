# pylint: skip-file
from . import google
from .message import Message
from .messageheader import MessageHeader
from .messagemetadata import MessageMetadata


class Envelope:
    """Specifies the envelope of incoming messages."""

    def get_message(self) -> Message:
        """Return a :class:`~aorta.models.Message` object."""
        raise NotImplementedError
