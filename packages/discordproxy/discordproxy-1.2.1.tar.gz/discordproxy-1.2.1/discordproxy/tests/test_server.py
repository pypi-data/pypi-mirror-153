import asyncio
import logging
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from discord.errors import LoginFailure

from .._server import _handle_uncaught_exception

SERVER_MODULE = "discordproxy._server"

logging.basicConfig(
    filename=Path(__file__).with_suffix(".log"),
    format="%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@patch(SERVER_MODULE + ".asyncio", autospec=True)
class TestHandleUncaughtException(TestCase):
    def test_should_call_shutdown_for_client_exception(self, mock_asyncio):
        # given
        mock_loop = Mock(autospec=asyncio.BaseEventLoop)
        exception = LoginFailure()
        context = {"message": str(exception), "exception": exception}
        grpc_server = Mock()
        discord_client = Mock()
        # when
        with patch(
            SERVER_MODULE + "._shutdown_server", spec=True, new=Mock()
        ) as mock_shutdown_server:
            _handle_uncaught_exception(
                mock_loop,
                context,
                grpc_server=grpc_server,
                discord_client=discord_client,
            )
            # then
            self.assertTrue(mock_shutdown_server.called)

    def test_should_handle_message_only(self, mock_asyncio):
        # given
        mock_loop = Mock(autospec=asyncio.BaseEventLoop)
        exception = LoginFailure()
        context = {"message": str(exception)}
        mock_grpc_server = Mock()
        mock_discord_client = Mock()
        # when
        _handle_uncaught_exception(
            mock_loop,
            context,
            grpc_server=mock_grpc_server,
            discord_client=mock_discord_client,
        )
        # then
        self.assertTrue(mock_loop.default_exception_handler.called)
