"""Declares :class:`MessageFieldDescriptor`."""


class MessageFieldDescriptor:

    def __init__(self, attname: str):
        self.attname = attname

    def __set__(self, instance, value):
        raise TypeError(f"Can not set `{self.attname}`.")

    def __get__(self, instance, cls=None):
        return getattr(instance._params, self.attname)
