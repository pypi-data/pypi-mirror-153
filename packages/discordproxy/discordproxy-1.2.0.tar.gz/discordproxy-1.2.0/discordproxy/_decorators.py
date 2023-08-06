import functools
import json
import logging

import discord
import grpc

from discordproxy import discord_api_pb2

logger = logging.getLogger(__name__)


def handle_discord_exceptions(Response):
    """converts discord HTTP exceptions into gRPC context"""

    _CODES_MAPPING = {
        400: grpc.StatusCode.INVALID_ARGUMENT,
        401: grpc.StatusCode.UNAUTHENTICATED,
        403: grpc.StatusCode.PERMISSION_DENIED,
        404: grpc.StatusCode.NOT_FOUND,
        405: grpc.StatusCode.INVALID_ARGUMENT,
        429: grpc.StatusCode.RESOURCE_EXHAUSTED,
        500: grpc.StatusCode.INTERNAL,
        502: grpc.StatusCode.UNAVAILABLE,
        504: grpc.StatusCode.DEADLINE_EXCEEDED,
    }

    def wrapper(func):
        @functools.wraps(func)
        async def decorated(self, request, context):
            try:
                return await func(self, request, context)
            except discord.errors.HTTPException as ex:
                logger.warning(
                    "%s: Discord HTTP exception: %s:\n%s",
                    func.__name__,
                    ex,
                    request,
                )
                details = _gen_grpc_error_details(
                    status=ex.status, code=ex.code, text=ex.text
                )
                context.set_code(_CODES_MAPPING.get(ex.status, grpc.StatusCode.UNKNOWN))
                context.set_details(json.dumps(details))
                return Response()
            except Exception as ex:
                logger.warning(
                    "%s: Unexpected exception: %s:\n%s",
                    func.__name__,
                    ex,
                    request,
                )
                return Response()

        return decorated

    return wrapper


def _gen_grpc_error_details(status: int, code: int, text: str):
    return {
        "type": "HTTPException",
        "status": int(status),
        "code": int(code),
        "text": str(text),
    }


def log_request(func):
    """Log every request."""

    async def decorated(self, request, context):
        logger.info("Received request: %s", _request_to_info_str(request))
        logger.debug(
            "Received request content: %s{\n%s}",
            type(request).__name__,
            str(request),
        )
        return await func(self, request, context)

    return decorated


def _request_to_info_str(request):
    name = type(request).__name__
    if isinstance(request, discord_api_pb2.SendDirectMessageRequest):
        params = f"(user_id={request.user_id})"
    elif isinstance(request, discord_api_pb2.SendChannelMessageRequest):
        params = f"(channel_id={request.channel_id})"
    elif isinstance(request, discord_api_pb2.GetGuildChannelsRequest):
        params = f"(guild_id={request.guild_id})"
    else:
        params = ""
    return f"{name}{params}"
