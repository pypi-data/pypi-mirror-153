from unittest.mock import patch

import grpc

from .._cli import main
from ..exceptions import to_discord_proxy_exception
from .factories import create_rpc_error
from .helpers import NoSocketsTestCase

MODULE_PATH = "discordproxy._cli"


@patch(MODULE_PATH + ".sys")
@patch(MODULE_PATH + ".DiscordClient")
class TestCreateDirectMessage(NoSocketsTestCase):
    def test_should_send_direct_message(self, mock_DiscordClient, mock_sys):
        # given
        mock_sys.argv = ["discordproxymessage", "direct", "123", "test"]
        mock_client = mock_DiscordClient.return_value
        # when
        main()
        # then
        self.assertTrue(mock_client.create_direct_message.called)

    def test_should_send_channel_message(self, mock_DiscordClient, mock_sys):
        # given
        mock_sys.argv = ["discordproxymessage", "channel", "123", "test"]
        mock_client = mock_DiscordClient.return_value
        # when
        main()
        # then
        self.assertTrue(mock_client.create_channel_message.called)

    def test_should_raise_systemexit(self, mock_DiscordClient, mock_sys):
        # given
        mock_sys.argv = ["discordproxymessage", "channel", "123", "test"]
        mock_client = mock_DiscordClient.return_value
        error = to_discord_proxy_exception(
            create_rpc_error(code=grpc.StatusCode.UNAVAILABLE, details="text")
        )
        mock_client.create_channel_message.side_effect = error
        # when
        with self.assertRaises(SystemExit):
            main()
