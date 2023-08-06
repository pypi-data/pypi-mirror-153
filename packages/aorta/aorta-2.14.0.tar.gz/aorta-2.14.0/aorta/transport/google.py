"""Declares :class:`GoogleTransport`."""
import asyncio
import functools
import typing

from google.cloud import pubsub_v1

from ..models import Message
from .itransport import ITransport


class GoogleTransport(ITransport):
    __module__ = 'aorta.transport'

    @functools.cached_property
    def client(self) -> pubsub_v1.PublisherClient:
        """Return the client used to publish events."""
        return pubsub_v1.PublisherClient()

    def __init__(self,
        project: str,
        topic_path: typing.Union[str, list, typing.Callable] = None
    ):
        """Initialize a new :class:`GoogleTransport`:

        Args:
            project: the name of the Google Cloud project.
            topic_path: either a string, list of string, or a callable that
                returns a string or list of strings, that specify the topic
                to which messages must be published.
        """
        self.project = project
        self.topic_path = topic_path

    def get_topics(self, message: Message) -> typing.List[str]:
        """Return the list of topics to which the given `message` must be
        published.
        """
        if callable(self.topic_path):
            topics = self.topic_path(message)
        else:
            topics = self.topic_path
        assert isinstance(topics, (str, list)) # nosec
        topics = [topics] if isinstance(topics, str) else topics
        return [self.client.topic_path(self.project, x) for x in topics]

    async def send(self, objects: typing.List[Message]):
        return await self._send([(self.get_topics(m), m) for m in objects])

    async def _send(self, objects: typing.List[typing.Tuple[str, Message]]):
        futures = []
        for topics, message in objects:
            for topic in topics:
                futures.append(
                    asyncio.wrap_future(
                        future=self.client.publish(topic, bytes(message))
                    )
                )
        await asyncio.gather(*futures)
