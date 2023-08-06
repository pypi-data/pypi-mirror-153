"""Declares :class:`PubsubMessage`."""
import datetime
import base64
import json
import typing

import pydantic


class PubsubMessage(pydantic.BaseModel):
    message_id: str = pydantic.Field(..., alias='messageId')
    publish_time: datetime.datetime = pydantic.Field(..., alias='publishTime')
    attributes: dict = None
    data: str = None

    def get_data(self) -> typing.Union[dict, list]:
        """Return a dictionary or a list containing the message
        data as specified by the ``.data`` attribute. The encoding
        is assumed JSON/UTF-8.
        """
        if self.data is None:
            return None
        return json.loads(base64.b64decode(self.data))
