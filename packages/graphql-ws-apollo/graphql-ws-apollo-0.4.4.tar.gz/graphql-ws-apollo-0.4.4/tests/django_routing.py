from channels.routing import route
from graphql_ws_apollo.django_channels import GraphQLSubscriptionConsumer

channel_routing = [
    route("websocket.receive", GraphQLSubscriptionConsumer),
]
