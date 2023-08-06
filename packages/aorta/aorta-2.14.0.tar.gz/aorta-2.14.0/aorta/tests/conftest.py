# pylint: skip-file
import typing

import pytest

from ..messagehandlersprovider import MessageHandlersProvider
import aorta


class TestCommand(aorta.Command):
    foo: int


class TestEvent(aorta.Event):
    foo: int


class TestCommandHandler(aorta.CommandHandler):

    async def handle(self, command: TestCommand):
        pass


class TestEventListener(aorta.EventListener):

    async def handle(self, event: TestEvent):
        pass


class FooCommand(aorta.Command):
    foo: int


class BarCommand(aorta.Command):
    bar: int


class BazCommand(aorta.Command):
    baz: int


class MultiCommandHandler(aorta.CommandHandler):

    async def handle(self, command: typing.Union[FooCommand, BarCommand, BazCommand]):
        pass


@pytest.fixture
def command():
    return TestCommand(foo=1)


@pytest.fixture
def command_handler(command):
    return TestCommandHandler(
        message=command.as_message()
    )


@pytest.fixture
def event_listener(event):
    return TestEventListener(
        message=event.as_message()
    )


@pytest.fixture
def event():
    return TestEvent(foo=1)


@pytest.fixture
def publisher():
    return aorta.MessagePublisher(
        transport=aorta.transport.NullTransport()
    )


@pytest.fixture
def provider():
    return MessageHandlersProvider()
