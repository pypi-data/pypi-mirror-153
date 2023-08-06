import json
import logging

import grpc
from asynctest import TestCase

from discordproxy import _api, discord_api_pb2

from .stubs import DiscordClientErrorStub, DiscordClientStub, ServicerContextStub

logging.basicConfig()


class TestMapDiscordErrors(TestCase):
    def setUp(self) -> None:
        self.request = discord_api_pb2.SendDirectMessageRequest(
            user_id=666, content="content"
        )
        self.context = ServicerContextStub()

    async def test_should_map_all_http_codes_to_grpc_codes(self):
        codes_mapping = {
            400: grpc.StatusCode.INVALID_ARGUMENT,
            401: grpc.StatusCode.UNAUTHENTICATED,
            403: grpc.StatusCode.PERMISSION_DENIED,
            404: grpc.StatusCode.NOT_FOUND,
            405: grpc.StatusCode.INVALID_ARGUMENT,
            429: grpc.StatusCode.RESOURCE_EXHAUSTED,
            500: grpc.StatusCode.INTERNAL,
            502: grpc.StatusCode.UNAVAILABLE,
            504: grpc.StatusCode.DEADLINE_EXCEEDED,
            599: grpc.StatusCode.UNKNOWN,
        }
        for status_code, grpc_code in codes_mapping.items():
            # given
            my_api = _api.DiscordApi(DiscordClientErrorStub(status_code))
            # when
            result = await my_api.SendDirectMessage(self.request, self.context)
            # then
            self.assertEqual(result, discord_api_pb2.SendDirectMessageResponse())
            self.assertEqual(self.context._code, grpc_code)
            details = json.loads(self.context._details)
            self.assertEqual(details["status"], status_code)
            self.assertEqual(details["code"], 0)

    async def test_should_return_error_details(self):
        # given
        my_api = _api.DiscordApi(DiscordClientErrorStub(404, "my_message"))
        # when
        await my_api.SendDirectMessage(self.request, self.context)
        # then
        details = json.loads(self.context._details)
        self.assertEqual(details["status"], 404)
        self.assertEqual(details["code"], 0)
        self.assertEqual(details["text"], "my_message")


class TestApi(TestCase):
    def setUp(self) -> None:
        self.my_api = _api.DiscordApi(DiscordClientStub())
        self.context = ServicerContextStub()
        self.my_embed = discord_api_pb2.Embed(
            title="title",
            type="rich",
            description="description",
            url="url",
            timestamp="2021-03-09T18:25:42.081000+00:00",
            color=0,
            footer=discord_api_pb2.Embed.Footer(
                text="text", icon_url="icon_url", proxy_icon_url="proxy_icon_url"
            ),
            image=discord_api_pb2.Embed.Image(
                url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
            ),
            thumbnail=discord_api_pb2.Embed.Thumbnail(
                url="url", proxy_url="proxy_url", height=42, width=66
            ),
            video=discord_api_pb2.Embed.Video(
                url="url", proxy_icon_url="proxy_icon_url", height=42, width=66
            ),
            provider=discord_api_pb2.Embed.Provider(name="name", url="url"),
            author=discord_api_pb2.Embed.Author(
                name="name",
                url="url",
                icon_url="icon_url",
                proxy_icon_url="proxy_icon_url",
            ),
            fields=[
                discord_api_pb2.Embed.Field(name="name", value="value", inline=True)
            ],
        )

    async def test_should_send_channel_message(self):
        # given
        request = discord_api_pb2.SendChannelMessageRequest(
            channel_id=2001, content="content"
        )
        # when
        result = await self.my_api.SendChannelMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendChannelMessageResponse)
        self.assertEqual(result.message.channel_id, 2001)
        self.assertEqual(result.message.content, "content")

    async def test_should_send_direct_message(self):
        # given
        request = discord_api_pb2.SendDirectMessageRequest(
            user_id=1001, content="content"
        )
        # when
        result = await self.my_api.SendDirectMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)
        self.assertEqual(result.message.content, "content")

    async def test_should_send_direct_message_with_embed(self):
        # given
        request = discord_api_pb2.SendDirectMessageRequest(
            user_id=1001, embed=self.my_embed
        )
        # when
        result = await self.my_api.SendDirectMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)
        self.assertEqual(result.message.embeds[0].description, "description")

    async def test_should_send_direct_message_with_content_and_embed(self):
        # given
        request = discord_api_pb2.SendDirectMessageRequest(
            user_id=1001, content="content", embed=self.my_embed
        )
        # when
        result = await self.my_api.SendDirectMessage(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.SendDirectMessageResponse)
        self.assertEqual(result.message.content, "content")
        self.assertEqual(result.message.embeds[0].description, "description")

    async def test_should_get_guild_channels(self):
        # given
        request = discord_api_pb2.GetGuildChannelsRequest(guild_id=3001)
        # when
        result = await self.my_api.GetGuildChannels(
            request=request, context=self.context
        )
        # then
        self.assertIsInstance(result, discord_api_pb2.GetGuildChannelsResponse)
        self.assertSetEqual(
            {obj.id for obj in result.channels}, {2001, 2002, 2051, 2100}
        )
