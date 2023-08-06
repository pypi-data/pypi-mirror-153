"""Declares :class:`MessageHandlerMetaclass`."""
import inspect
import types
import typing

from unimatrix.exceptions import ImproperlyConfigured

from .basemessage import BaseMessage


class MessageHandlerMetaclass(type):
    handles: type[BaseMessage] = None
    parameter_name: str = None

    def __new__(cls, name:str, bases: tuple, attrs: dict) -> type:
        # Do some checks to ensure that handlers are properly implemented.
        is_abstract = attrs.pop('__abstract__', False)
        new_class = super().__new__(cls, name, bases, {**attrs, 'handles': []})
        if is_abstract:
            return new_class

        # Ensure that the handle() method accepts the message as the first
        # parameter.
        sig = inspect.signature(new_class.handle)
        params = list(sig.parameters.values())
        if len(params) < 2:
            raise ImproperlyConfigured(
                f"Invalid number of arguments for {name}.handle(). "
                f"Ensure that the parameters accepted by this method are at "
                f"least {name}.handle(self, {cls.parameter_name}: "
                f"{cls.handles.__name__})."
            )

        arg = params[1]
        if arg.name != cls.parameter_name:
            raise ImproperlyConfigured(
                f'The first positional argument to {name}.handle() '
                f'must be named `{cls.parameter_name}`, got `{arg.name}`.'
            )

        # If the argument is a Union, then it accepts multiple message types.
        # Check if all definitions are of the required type.
        handles = [arg.annotation]
        if typing.get_origin(arg.annotation) in (typing.Union, types.UnionType):
            handles = typing.get_args(arg.annotation)
        for Message in set(handles):
            if not issubclass(Message, cls.handles):
                raise ImproperlyConfigured(
                    f"The first positional argument to {name}.handle() must "
                    "annotate itself with the message type that is handled by "
                    "this implementation."
                )
            new_class.handles.append(Message) # type: ignore

        return new_class

