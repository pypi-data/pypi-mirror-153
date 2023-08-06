"""Declares :class:`BaseMessage`."""
import base64
import uuid

import pydantic
from unimatrix.lib import timezone

from .models import Message
from .messageoptions import MessageOptions


class BaseMessage:
    """The base class for all message types."""
    __abstract__: bool = True
    _envelope: type[Message]
    _meta: MessageOptions

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, (dict, pydantic.BaseModel)):
            raise TypeError(f"Invalid type {type(value).__name__}")
        if isinstance(value, cls._envelope):
            # In this case, the parameters are considered priorly validated.
            result = value.get_object()
        elif isinstance(value, cls._model):
            # Also in the case that value is an instance of the message model,
            # validation was already done.
            result = value
        elif isinstance(value, Message):
            result = cls.validate(getattr(value, cls._meta.envelope_field))
        elif isinstance(value, pydantic.BaseModel):
            result = cls.validate(value.dict(by_alias=True))
        elif isinstance(value, dict) \
        and bool({'apiVersion', 'kind'} & set(dict.keys(value))):
            result = cls.validate(cls._envelope(**value))
        else:
            result = cls._model(**value)
        return result

    def __init__(self, **kwargs):
        self._params = self._model(**kwargs)

    def as_envelope(self, *args, **kwargs) -> Message:
        return self.as_message(*args, **kwargs)

    def serialize(
        self,
        correlation_id: str | None = None,
        ttl: int | None = None
    ) -> str:
        """Enclose the message in an envelope and serialize it to a
        Base64-encoded JSON string.
        """
        data = self.as_message(correlation_id=correlation_id, ttl=ttl)\
            .json(by_alias=True)\
            .encode('utf-8')
        return bytes.decode(base64.b64encode(data), 'ascii')

    def as_message(self,
        correlation_id: str | None = None,
        ttl: int | None = None
    ) -> Message:
        """Wrap the message in a :class:`aorta.models.Envelope` instance.

        The `correlation_id` specifies a correlation identifier that may be
        used to find relationships between various messages.

        A message time-to-live can be specified with the `ttl` argument, which
        indicates the time-to-live in milliseconds.
        """
        dto = {
            'apiVersion': self._meta.api_version,
            'kind': type(self).__name__,
            'type': self._meta.type,
            'metadata': {
                'id': uuid.uuid4(),
                'correlationId': correlation_id or uuid.uuid4(),
                'published': timezone.now(),
                'ttl': ttl
            },
            self._meta.envelope_field: self._params.dict()
        }
        return self._envelope(**dto)
