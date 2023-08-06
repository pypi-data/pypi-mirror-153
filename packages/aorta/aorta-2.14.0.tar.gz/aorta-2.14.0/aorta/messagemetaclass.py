"""Declares :class:`MessageMetaclass`."""
import typing

import pydantic

from .messagefielddescriptor import MessageFieldDescriptor
from .messageobjectdescriptor import MessageObjectDescriptor
from .messageoptions import MessageOptions
from .models import MessageHeader


RESERVED_NAMES: set = {
    "_envelope",
    "_meta",
    "_model",
    "as_message",
    "__bytes__"
}


class MessageMetaclass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        if attrs.pop('__abstract__', False):
            return super_new(cls, name, bases, attrs)

        # Use all annotated attributes to create a pydantic.BaseModel subclass.
        # Add descriptors to the base class.
        hints = attrs.pop('__annotations__', {})
        fields = {k: attrs.pop(k) for k in dict.keys(hints) if k in attrs}
        for k in dict.keys(hints):
            if k in RESERVED_NAMES\
            or str.startswith(k, '__'):
                raise ValueError(f"{k} is a reserved name.")
            attrs[k] = MessageFieldDescriptor(k)
        attrs['_model'] = type(f'{name}Parameters', (pydantic.BaseModel,), {
            **fields,
            '__annotations__': hints
        })

        # Create the envelope model with explicit typing for the message
        # spec or data.
        attrs['_envelope'] = type(f'{name}', (MessageHeader,), {
            '_params': MessageObjectDescriptor(cls.envelope_field),
            '__annotations__': {
                cls.envelope_field: attrs['_model']
            }
        })

        # Inspect attrs to find out if there is an inner Meta class.
        attrs['_meta'] = MessageOptions(
            meta=attrs.pop('Meta', None),
            name=name,
            type=cls.message_type,
            envelope_field=cls.envelope_field
        )

        return super_new(cls, name, bases, attrs)
