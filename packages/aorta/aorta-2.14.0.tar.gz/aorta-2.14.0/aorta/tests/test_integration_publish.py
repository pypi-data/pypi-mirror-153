# pytest: skip-file
import pytest

import aorta


class TestPublisher:

    @pytest.mark.asyncio
    async def test_publish_command(self, publisher, command):
        await publisher.publish(command)

    @pytest.mark.asyncio
    async def test_publish_event(self, publisher, event):
        await publisher.publish(event)

    @pytest.mark.asyncio
    async def test_publish_event_many(self, publisher, event):
        await publisher.publish([event, event])
