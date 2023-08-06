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
"""Declares :class:`MessagePublisher`."""
from .command import Command
from .event import Event
from .sender import Sender


class MessagePublisher(Sender):
    """Provides an interface to published event messages."""
    __module__: str = 'aorta'

    async def publish(self,
        objects: Command | Event | list[Command | Event],
        correlation_id: str | None = None
    ) -> None:
        """Publish an message to the upstream peer."""
        if not isinstance(objects, list):
            objects = [objects]
        return await self.send([x.as_message(correlation_id) for x in objects])
