"""This is an example for an async client. It sends 50 direct messages concurrently."""
import asyncio
import logging

import grpc

from discordproxy.discord_api_pb2 import SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub


async def send_hello_world(num) -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        client = DiscordApiStub(channel)
        request = SendDirectMessageRequest(
            user_id=152878250039705600, content=f"Hello, world! #{num + 1}"
        )
        await client.SendDirectMessage(request)


async def start_workers():
    await asyncio.gather(*[send_hello_world(i) for i in range(50)])


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(start_workers())
