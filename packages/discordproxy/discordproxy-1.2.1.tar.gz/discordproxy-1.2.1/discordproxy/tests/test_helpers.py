import json
import unittest

import grpc

from discordproxy.helpers import GrpcErrorDetails, parse_error_details


class TestParseErrorDetails(unittest.TestCase):
    def test_should_return_full_details(self):
        # given
        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.NOT_FOUND
        error.details = lambda: json.dumps(
            {
                "type": "HTTPException",
                "status": 404,
                "code": 50001,
                "text": "User not found",
            }
        )
        # when
        result = parse_error_details(error)
        # then
        self.assertEqual(
            result, GrpcErrorDetails("HTTPException", 404, 50001, "User not found")
        )

    def test_should_return_text_only(self):
        # given
        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.ABORTED
        error.details = lambda: "text"
        # when
        result = parse_error_details(error)
        # then
        self.assertEqual(result, GrpcErrorDetails("Other", None, None, "text"))
