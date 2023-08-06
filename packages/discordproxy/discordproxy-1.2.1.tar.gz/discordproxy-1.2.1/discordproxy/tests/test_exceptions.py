import json
from unittest import TestCase

import grpc

from ..exceptions import (
    DiscordProxyGrpcError,
    DiscordProxyHttpError,
    DiscordProxyTimeoutError,
    to_discord_proxy_exception,
)
from .factories import create_rpc_error


class TestToDiscordProxyException(TestCase):
    def test_should_return_other_exceptions(self):
        # when
        result = to_discord_proxy_exception(OSError)
        # then
        self.assertIs(result, OSError)

    def test_should_return_http_exception(self):
        # given
        details = json.dumps(
            {
                "type": "HTTPException",
                "status": 404,
                "code": 10013,
                "text": "Unknown User",
            }
        )
        error = create_rpc_error(code=grpc.StatusCode.NOT_FOUND, details=details)
        # when
        result = to_discord_proxy_exception(error)
        # then
        self.assertIsInstance(result, DiscordProxyHttpError)
        self.assertEqual(result.status, 404)
        self.assertEqual(result.code, 10013)
        self.assertEqual(result.text, "Unknown User")

    def test_should_return_grpc_exception(self):
        # given
        error = create_rpc_error(code=grpc.StatusCode.ABORTED, details="text")
        # when
        result = to_discord_proxy_exception(error)
        # then
        self.assertIsInstance(result, DiscordProxyGrpcError)
        self.assertIs(result.status, grpc.StatusCode.ABORTED)
        self.assertEqual(result.details, "text")

    def test_should_return_timeout_exception(self):
        # given
        error = create_rpc_error(code=grpc.StatusCode.DEADLINE_EXCEEDED, details="text")
        # when
        # when
        result = to_discord_proxy_exception(error)
        # then
        self.assertIsInstance(result, DiscordProxyTimeoutError)


class TestDiscordProxyHttpError(TestCase):
    def test_str(self):
        # given
        ex = DiscordProxyHttpError(status=404, code=10013, text="Unknown User")
        # when
        self.assertEqual(
            str(ex),
            (
                "HTTP error from the Discord API. HTTP status code: 404 - "
                "JSON error code: 10013 - Error message: Unknown User"
            ),
        )


class TestDiscordProxyGrpcError(TestCase):
    def test_str(self):
        # given
        ex = DiscordProxyGrpcError(status=grpc.StatusCode.ABORTED, details="some text")
        # when
        self.assertEqual(
            str(ex), ("gRPC error. Status code: ABORTED - Error message: some text")
        )
