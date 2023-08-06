"""Client example for sending 'hello world' as direct message"""
import grpc

from discordproxy.discord_api_pb2 import SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub

# opens a channel to Discord Proxy
with grpc.insecure_channel("localhost:50051") as channel:
    # create a client for the DiscordApi service
    client = DiscordApiStub(channel)
    # create a request to use the SendDirectMessageRequest method of the service
    request = SendDirectMessageRequest(user_id=123456789, content="Hello, world!")
    # send the request to Discord Proxy
    client.SendDirectMessage(request)
