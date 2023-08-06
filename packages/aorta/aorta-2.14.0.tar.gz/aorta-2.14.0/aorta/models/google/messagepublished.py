"""Declares :class:`MessagePublished`."""
import pydantic

from ..message import Message
from .pubsubmessage import PubsubMessage


class MessagePublished(pydantic.BaseModel):
    subscription: pydantic.constr(
        regex='^projects/[\-a-z0-9]{6,30}/subscriptions/.*$'
    )

    message: PubsubMessage

    def get_message(self) -> Message:
        return Message(**(self.message.get_data() or {}))
