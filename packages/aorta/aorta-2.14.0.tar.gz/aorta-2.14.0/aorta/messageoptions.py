"""Declares :class:`MessageOptions`."""


class MessageOptions:

    def __init__(self,
        meta: type,
        name: str,
        type: str,
        envelope_field: str,
    ):
        """Specifies the configured options for a :class:`aorta.Command` or
        :class:`aorta.Event`.
        """
        self.envelope_field = envelope_field
        self.group = None
        self.name = name
        self.meta = meta
        self.type = type
        self.version = 'v1'

        self.group = getattr(meta, 'group', None)
        self.api_version = f'{self.group}/{self.version}'\
            if self.group else self.version
