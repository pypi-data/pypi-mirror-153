# pylint: skip-file
import pytest

from ..exceptions import UnknownMessageType
from ..messagehandlersprovider import MessageHandlersProvider
from .conftest import FooCommand
from .conftest import BarCommand
from .conftest import BazCommand
from .conftest import MultiCommandHandler
from .conftest import TestCommand
from .conftest import TestCommandHandler
from .conftest import TestEvent
from .conftest import TestEventListener


class TestMessageHandlersProvider:

    @pytest.fixture
    def foo(self):
        return FooCommand(foo=1)

    @pytest.fixture
    def bar(self):
        return BarCommand(bar=2)

    @pytest.fixture
    def baz(self):
        return BazCommand(baz=3)

    @pytest.fixture
    def handler_class_multi(self):
        return MultiCommandHandler

    @pytest.fixture
    def handler_class(self):
        return TestCommandHandler

    @pytest.fixture
    def message(self, command):
        return command

    @pytest.fixture
    def envelope(self, message):
        return message.as_envelope().dict(by_alias=True)

    def test_register_single(self, provider, handler_class):
        provider.register(handler_class)

    def test_register_multi(self, provider, handler_class_multi):
        provider.register(handler_class_multi)

    def test_match_single(self, provider, handler_class, message):
        provider.register(handler_class)
        assert handler_class in provider.match(message.as_envelope())

    def test_match_multi(self, provider, handler_class_multi, foo, bar, baz):
        provider.register(handler_class_multi)
        assert handler_class_multi in provider.match(foo.as_envelope())
        assert handler_class_multi in provider.match(bar.as_envelope())
        assert handler_class_multi in provider.match(baz.as_envelope())

    def test_parse_message_unregistered(self, provider, envelope):
        with pytest.raises(UnknownMessageType):
            provider.parse(envelope)

    def test_parse_single(self, provider, envelope, handler_class):
        provider.register(handler_class)
        provider.parse(envelope)

    def test_parse_multi(self, provider, handler_class_multi, foo, bar, baz):
        provider.register(handler_class_multi)
        provider.parse(foo.as_envelope().dict(by_alias=True))
        provider.parse(bar.as_envelope().dict(by_alias=True))
        provider.parse(baz.as_envelope().dict(by_alias=True))
