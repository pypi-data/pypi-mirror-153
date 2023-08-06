"""Declares :class:`Message`."""
import pydantic

from .messageheader import MessageHeader


class Message(MessageHeader):
    data: dict = pydantic.Field({})
    spec: dict = pydantic.Field({})
