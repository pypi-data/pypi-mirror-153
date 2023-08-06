# pylint: skip-file
import pydantic
import pytest

from .conftest import Model
from .conftest import PydanticCommand


def test_validate_model():
    m = Model(
        command={'foo': 1}
    )


def test_from_message_envelope():
    message = PydanticCommand(foo=1).as_message()
    model = Model(command=message)


def test_from_message_envelope_dict():
    model = Model(command={
        'apiVersion': 'v1',
        'kind': 'PydanticCommand',
        'spec': {
            'foo': '1'
        }
    })


def test_from_spec():
    message = PydanticCommand(foo=1).as_message()
    model = Model(command=message.spec)


def test_validate_model_invalid():
    with pytest.raises(pydantic.ValidationError):
        m = Model(
            command=None
        )
