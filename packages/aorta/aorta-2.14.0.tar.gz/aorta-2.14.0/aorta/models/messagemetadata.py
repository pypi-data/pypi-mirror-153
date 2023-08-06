"""Declares :class:`MessageMetadata`."""
import typing
import uuid

import pydantic
from unimatrix.lib import timezone


class MessageMetadata(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(
        alias='id',
        default_factory=uuid.uuid4
    )

    correlation_id: uuid.UUID = pydantic.Field(
        alias='correlationId',
        default_factory=uuid.uuid4
    )

    published: int = pydantic.Field(
        default_factory=timezone.now
    )

    delivery_count: int = pydantic.Field(0, alias='deliveryCount')

    ttl: typing.Optional[int] = None

    annotations: dict = pydantic.Field({})
    labels: dict = pydantic.Field({})
