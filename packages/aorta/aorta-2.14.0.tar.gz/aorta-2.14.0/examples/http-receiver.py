# pylint: skip-file
import asyncio
import fastapi
import pydantic
import uvicorn

import aorta
from aorta.transport.http import MessageReceiver


app = MessageReceiver(allowed_hosts=['*'])
publisher = aorta.EventPublisher(None)
issuer = aorta.CommandIssuer(None)


class Mutate(aorta.CommandHandler):

    class Meta:
        handles = [('v1', 'Mutate')]


class OnMutation(aorta.EventListener):

    class Meta:
        handles = [
            ('picqer.com/v1', 'Mutation')
        ]


aorta.register(Mutate)
aorta.register(OnMutation)

event = publisher.prepare({
    'apiVersion': "picqer.com/v1",
    'kind': "Mutation",
    'data': {'bar': "Foo"}
})

command = issuer.prepare({
    'apiVersion': "v1",
    'kind': "Mutate",
    'spec': {}
})

asyncio.run(aorta.run(aorta.runner.NullRunner(), command))

if __name__ == '__main__':
    uvicorn.run('__main__:app',
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        reload=True
    )
