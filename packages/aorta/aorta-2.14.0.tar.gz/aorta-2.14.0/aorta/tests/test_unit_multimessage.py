# pylint: skip-file
import pytest

from .conftest import BarCommand
from .conftest import BazCommand
from .conftest import FooCommand
from .conftest import MultiCommandHandler


def test_handles_accepts_foocommand():
    assert FooCommand in MultiCommandHandler.handles


def test_handles_accepts_barcommand():
    assert BarCommand in MultiCommandHandler.handles


def test_handles_accepts_bazcommand():
    assert BazCommand in MultiCommandHandler.handles
