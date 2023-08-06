"""Helpers for gRPC clients"""
import json
from collections import namedtuple

import grpc

GrpcErrorDetails = namedtuple("GrpcErrorDetails", ["type", "status", "code", "text"])


def parse_error_details(grpc_error: grpc.RpcError) -> GrpcErrorDetails:
    """Helper for parsing the details of a gRPC error exception into a nammed tuple.
    Recognizes a Discord error encoded as JSON
    """
    details = grpc_error.details()
    try:
        data = json.loads(details)
    except json.decoder.JSONDecodeError:
        data = {"text": details}
    return GrpcErrorDetails(
        type=data.get("type", "Other"),
        status=data.get("status", None),
        code=data.get("code", None),
        text=data.get("text", ""),
    )
