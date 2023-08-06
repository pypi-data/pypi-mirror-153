"""Declares :class:`MessageObjectDescriptor`."""


class MessageObjectDescriptor:

    def __init__(self, attname: str):
        self.attname = attname

    def __get__(self, instance, cls=None):
        return getattr(instance, self.attname)
