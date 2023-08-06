# pylint: skip-file
import unittest.mock

import pytest


class TestCommandHandler:

    @pytest.fixture
    def handler(self, command_handler):
        return command_handler

    @pytest.fixture
    def message(self, command):
        return command

    @pytest.mark.asyncio
    async def test_invoke_handler_with_success(self, handler, message):
        await handler(message)

    @pytest.mark.asyncio
    async def test_exception_is_raised_by_default(self, handler, message):
        handler.handle = unittest.mock.AsyncMock(side_effect=Exception)
        with pytest.raises(Exception):
            await handler(message)

    @pytest.mark.asyncio
    async def test_exception_supress(self, handler, message):
        handler.handle = unittest.mock.AsyncMock(side_effect=Exception)
        handler.on_exception = unittest.mock.AsyncMock(return_value=True)
        await handler(message)



class TestEventListener(TestCommandHandler):

    @pytest.fixture
    def message(self, event):
        return event

    @pytest.fixture
    def handler(self, event_listener):
        return event_listener
