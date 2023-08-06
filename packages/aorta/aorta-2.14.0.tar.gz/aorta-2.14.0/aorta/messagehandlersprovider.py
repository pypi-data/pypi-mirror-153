# Copyright 2022 Cochise Ruhulessin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Declares :class:`MessageHandlersProvider`."""
import collections
import typing
from typing import Any

from .exceptions import UnknownMessageType
from .messagehandler import MessageHandler
from .messagehandlermetaclass import MessageHandlerMetaclass
from .models import MessageHeader
from .models import Message


class MessageHandlersProvider:
    """Implements a registry that can match handlers to messages."""
    __module__: str = 'aorta'
    _handlers: collections.defaultdict[
        tuple[str, str],
        list[type[MessageHandler]]
    ]
    _types: dict[tuple[str, str], type[Message]]

    def __init__(self):
        self._handlers = collections.defaultdict(list)
        self._types = {}

    def match(
        self,
        message: typing.Union[MessageHeader, Message]
    ) -> list[type[MessageHandler]]:
        """Return the list of handler classes for the given message."""
        return self.get(message)

    def get(
        self,
        message: typing.Union[MessageHeader, Message]
    ) -> list[type[MessageHandler]]:
        return self._handlers[message.api_version, message.kind]

    def parse(self, data: dict[str, Any]) -> Message:
        """Return a concrete message type by inspecting the metadata in the
        header.
        """
        try:
            header = MessageHeader(**data)
        except ValueError:
            raise UnknownMessageType
        else:
            key = (header.api_version, header.kind)
            if key not in self._types:
                raise UnknownMessageType
            return self._types[key](**data)

    def register(self, handler: type[MessageHandler]):
        """Register handler class `handler` for the message types it
        handles.
        """
        for spec in handler.handles:
            key = (spec._meta.api_version, spec._meta.name)
            self._handlers[key].append(handler)
            if key not in self._types:
                self._types[key] = spec._envelope


_default: MessageHandlersProvider = MessageHandlersProvider()


def match(
    message: typing.Union[MessageHeader, Message]
) -> typing.List[MessageHandlerMetaclass]:
    """Match a message against the registered handlers in the default
    provider.
    """
    return _default.match(message)


def parse(data: dict[str, Any]):
    """Parse a message using the default provider."""
    return _default.parse(data)


def register(handler: MessageHandlerMetaclass):
    """Register handler class `handler` for the message types it
    handles, using the default provider.
    """
    return _default.register(handler)
