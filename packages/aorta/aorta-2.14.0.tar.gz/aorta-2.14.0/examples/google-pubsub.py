# pylint: skip-file
import asyncio

import unimatrix.runtime

import aorta


class TestCommand(aorta.Command):
    foo: int
    bar: int
    baz: int


async def main():
    await unimatrix.runtime.startup()
    p = aorta.MessagePublisher(
        transport=aorta.transport.GoogleTransport(
            project='unimatrixinfra',
            topic_path=lambda message: f'aorta.commands'
        )
    )

    await p.publish([
        TestCommand(foo=1, bar=2, baz=3),
        TestCommand(foo=4, bar=5, baz=6),
        TestCommand(foo=7, bar=8, baz=9),
        TestCommand(foo=10, bar=11, baz=12),
    ])


if __name__ == '__main__':
    asyncio.run(main())
