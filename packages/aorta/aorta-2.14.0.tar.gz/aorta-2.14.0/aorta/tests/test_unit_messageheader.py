# pylint: skip-file
import time

import pytest


def test_ttl_not_set_is_not_expired(command):
    message = command.as_message()
    assert not message.is_expired()


def test_ttl_is_zero_is_not_expired(command):
    message = command.as_message(ttl=0)
    assert not message.is_expired()


def test_ttl_is_set_is_expired(command):
    message = command.as_message(ttl=100)
    time.sleep(0.11)
    assert message.is_expired()


def test_ttl_is_set_is_not_expired(command):
    message = command.as_message(ttl=100)
    time.sleep(0.09)
    assert not message.is_expired()


def test_expired_message_is_not_valid(command):
    message = command.as_message(ttl=100)
    time.sleep(0.11)
    assert message.is_expired()
    assert not message.is_valid()


def test_delivery_count_is_0(command):
    message = command.as_message(ttl=100)
    assert message.metadata.delivery_count == 0


def test_delivery_count_increase(command):
    message = command.as_message(ttl=100)
    assert message.metadata.delivery_count == 0
    message.accept()
    assert message.metadata.delivery_count == 1
    message.accept()
    assert message.metadata.delivery_count == 2
