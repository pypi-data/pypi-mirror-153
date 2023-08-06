from unittest.mock import Mock, patch

from ..client import DiscordClient, Message
from ..discord_api_pb2 import Channel, Embed
from ..exceptions import DiscordProxyException
from .factories import create_discordproxy_channel, create_rpc_error
from .helpers import NoSocketsTestCase

MODULE_PATH = "discordproxy.client"


@patch(MODULE_PATH + ".DiscordApiStub")
@patch(MODULE_PATH + ".grpc.insecure_channel", spec=True)
class TestFetchChannels(NoSocketsTestCase):
    def test_should_return_text_channels(
        self, mock_insecure_channel, mock_DiscordApiStub
    ):
        # given
        response = Mock()
        response.channels = [
            create_discordproxy_channel(
                id=1, name="dummy-1", type=Channel.Type.GUILD_TEXT
            ),
            create_discordproxy_channel(
                id=2, name="dummy-2", type=Channel.Type.GUILD_TEXT
            ),
            create_discordproxy_channel(
                id=3, name="dummy-2", type=Channel.Type.GUILD_VOICE
            ),
        ]
        mock_DiscordApiStub.return_value.GetGuildChannels.return_value = response
        client = DiscordClient()
        # when
        result = client.get_guild_channels(42)
        # then
        channel_ids = {obj.id for obj in result}
        self.assertSetEqual(channel_ids, {1, 2, 3})

    def test_should_raise_exception(self, mock_insecure_channel, mock_DiscordApiStub):
        # given
        error = create_rpc_error()
        mock_DiscordApiStub.return_value.GetGuildChannels.side_effect = error
        client = DiscordClient()
        # when/then
        with self.assertRaises(DiscordProxyException):
            client.get_guild_channels(42)


@patch(MODULE_PATH + ".DiscordApiStub")
@patch(MODULE_PATH + ".grpc.insecure_channel", spec=True)
class TestCreateChannelMessage(NoSocketsTestCase):
    def test_should_return_message(self, mock_insecure_channel, mock_DiscordApiStub):
        # given
        message = Message(
            channel_id=1, content="alpha", embeds=[Embed(description="test")]
        )
        mock_DiscordApiStub.return_value.SendChannelMessage.return_value.message = (
            message
        )
        client = DiscordClient()
        # when
        result = client.create_channel_message(
            channel_id=message.channel_id,
            content=message.content,
            embed=message.embeds[0],
        )
        # then
        self.assertEqual(result, message)

    def test_should_raise_error(self, mock_insecure_channel, mock_DiscordApiStub):
        # given
        error = create_rpc_error()
        mock_DiscordApiStub.return_value.SendChannelMessage.side_effect = error
        client = DiscordClient()
        # when/then
        with self.assertRaises(DiscordProxyException):
            client.create_channel_message(channel_id=1, content="alpha")

    def test_should_require_content_or_embed(
        self, mock_insecure_channel, mock_DiscordApiStub
    ):
        # given
        client = DiscordClient()
        # when/then
        with self.assertRaises(ValueError):
            client.create_channel_message(channel_id=1)


@patch(MODULE_PATH + ".DiscordApiStub")
@patch(MODULE_PATH + ".grpc.insecure_channel", spec=True)
class TestCreateDirectMessage(NoSocketsTestCase):
    def test_should_return_message(self, mock_insecure_channel, mock_DiscordApiStub):
        # given
        message = Message(content="alpha", embeds=[Embed(description="test")])
        mock_DiscordApiStub.return_value.SendDirectMessage.return_value.message = (
            message
        )
        client = DiscordClient()
        # when
        result = client.create_direct_message(
            user_id=1, content=message.content, embed=message.embeds[0]
        )
        # then
        self.assertEqual(result, message)

    def test_should_raise_error(self, mock_insecure_channel, mock_DiscordApiStub):
        # given
        error = create_rpc_error()
        mock_DiscordApiStub.return_value.SendDirectMessage.side_effect = error
        client = DiscordClient()
        # when/then
        with self.assertRaises(DiscordProxyException):
            client.create_direct_message(user_id=1, content="alpha")

    def test_should_require_content_or_embed(
        self, mock_insecure_channel, mock_DiscordApiStub
    ):
        # given
        client = DiscordClient()
        # when/then
        with self.assertRaises(ValueError):
            client.create_direct_message(user_id=1)
