import json

import grpc

from ..discord_api_pb2 import Channel


def id_generator() -> int:
    seed = 1
    while True:
        yield seed
        seed += 1


unique_ids = id_generator()


def create_discordproxy_channel(**kwargs) -> Channel:
    if "id" not in kwargs:
        kwargs["id"] = next(unique_ids)
    if "type" not in kwargs:
        kwargs["type"] = Channel.Type.GUILD_TEXT
    return Channel(**kwargs)


def create_rpc_error(**kwargs):
    error = grpc.RpcError()
    if "code" not in kwargs:
        kwargs["code"] = grpc.StatusCode.NOT_FOUND
    error.code = lambda: kwargs["code"]
    if "details" not in kwargs:
        kwargs["details"] = json.dumps(
            {
                "type": "HTTPException",
                "status": 404,
                "code": 50001,
                "text": "User not found",
            }
        )
    error.details = lambda: kwargs["details"]
    return error
