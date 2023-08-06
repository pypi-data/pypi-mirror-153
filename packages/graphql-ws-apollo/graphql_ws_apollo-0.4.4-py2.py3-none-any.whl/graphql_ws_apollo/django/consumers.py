import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ..constants import WS_PROTOCOL
from .subscriptions import subscription_server


class GraphQLSubscriptionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.connection_context = None
        protocol = None

        for p in ["graphql-ws", "graphql-transport-ws"]:
            if p in self.scope["subprotocols"]:
                protocol = p
                break

        if protocol is not None:
            self.connection_context = await subscription_server.handle(
                ws=self, request_context=self.scope
            )
            await self.accept(subprotocol=protocol)
        else:
            await self.close()

    async def disconnect(self, code):
        if self.connection_context:
            self.connection_context.socket_closed = True
            await subscription_server.on_close(self.connection_context)

    async def receive_json(self, content):
        subscription_server.on_message(self.connection_context, content)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)
