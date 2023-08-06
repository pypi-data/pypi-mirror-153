import asyncio
import logging
from collections import namedtuple
from pathlib import Path

import grpc
from asynctest import TestCase

from discordproxy._server import _shutdown_server, run_server
from discordproxy.discord_api_pb2 import SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub

from .stubs import DiscordClientStub

MyArgsStub = namedtuple("MyArgsStub", ["host", "port"])

logging.basicConfig(
    filename=Path(__file__).with_suffix(".log"),
    format="%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class TestEnd2End(TestCase):
    async def setUp(self) -> None:
        self.host = "localhost"
        self.port = 50051
        token = "dummy"
        my_args = MyArgsStub(host=self.host, port=self.port)
        self.grpc_server = grpc.aio.server()
        self.discord_client = DiscordClientStub()
        asyncio.create_task(
            run_server(
                token=token,
                my_args=my_args,
                grpc_server=self.grpc_server,
                discord_client=self.discord_client,
            )
        )
        await asyncio.sleep(1)

    async def tearDown(self) -> None:
        await _shutdown_server(
            grpc_server=self.grpc_server, discord_client=self.discord_client
        )

    async def test_should_send_message_to_server(self):
        # given
        channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        client = DiscordApiStub(channel)
        request = SendDirectMessageRequest(user_id=1001, content="content")
        # when
        response = await client.SendDirectMessage(request, timeout=5)
        # then
        self.assertEqual(response.message.channel_id, 2010)
        self.assertEqual(response.message.content, "content")
