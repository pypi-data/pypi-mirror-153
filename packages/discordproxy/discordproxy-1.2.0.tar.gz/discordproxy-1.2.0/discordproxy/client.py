from typing import Iterable

import grpc

from .discord_api_pb2 import (
    Channel,
    Embed,
    GetGuildChannelsRequest,
    Message,
    SendChannelMessageRequest,
    SendDirectMessageRequest,
)
from .discord_api_pb2_grpc import DiscordApiStub
from .exceptions import to_discord_proxy_exception


class DiscordClient:
    """Client for interacting with Discord.

    Raises:
        DiscordProxyHttpError: HTTP error from the Discord API
        DiscordProxyGrpcError: gRPC error from the gRPC protocol
    """

    def __init__(self, target: str = None, options=None, timeout=None) -> None:
        """
        Args:
            target: The address of the Discord Proxy gRPC server.
                Default is: "localhost:50051"
            options: An optional list of key-value pairs to configure the gRPC channel.
            timeout: Default timeout for gRPC method invocations in seconds.
                If not specified the timeout is about 30 minutes.
        """
        self._target = str(target) if target else "localhost:50051"
        self._options = options
        self._timeout = timeout

    def get_guild_channels(self, guild_id: int) -> Iterable[Channel]:
        """Get all channels.

        Args:
            guild_id: ID of guild to get the channel for

        Returns:
            Guild channels
        """
        with grpc.insecure_channel(self._target, self._options) as channel:
            client = DiscordApiStub(channel)
            request = GetGuildChannelsRequest(guild_id=guild_id)
            try:
                params = self._build_rpc_method_params(request)
                response = client.GetGuildChannels(**params)
            except Exception as ex:
                raise to_discord_proxy_exception(ex) from ex
        return response.channels

    def create_channel_message(
        self, channel_id: int, content: str = "", embed: Embed = None
    ) -> Message:
        """Create new message in a channel.

        Args:
            channel_id: ID of channel to create message in
            content: Text of the message
            embed: Embed of the message

        Returns:
            Created message
        """
        if not content and not embed:
            raise ValueError("Either content or embed need to be specified.")
        with grpc.insecure_channel(self._target, self._options) as grpc_channel:
            client = DiscordApiStub(grpc_channel)
            request = SendChannelMessageRequest(
                content=content, channel_id=channel_id, embed=embed
            )
            try:
                params = self._build_rpc_method_params(request)
                response = client.SendChannelMessage(**params)
            except Exception as ex:
                raise to_discord_proxy_exception(ex) from ex
        return response.message

    def create_direct_message(
        self, user_id: int, content: str = "", embed: Embed = None
    ) -> Message:
        """Create new direct message.

        Args:
            user_id: ID of user to create direct message for
            content: Text of the message
            embed: Embed of the message

        Returns:
            Created message
        """
        if not content and not embed:
            raise ValueError("Either content or embed need to be specified.")
        with grpc.insecure_channel(self._target, self._options) as grpc_channel:
            client = DiscordApiStub(grpc_channel)
            request = SendDirectMessageRequest(
                content=content, user_id=user_id, embed=embed
            )
            try:
                params = self._build_rpc_method_params(request)
                response = client.SendDirectMessage(**params)
            except Exception as ex:
                raise to_discord_proxy_exception(ex) from ex
        return response.message

    def _build_rpc_method_params(self, request) -> dict:
        params = {"request": request}
        if self._timeout:
            params["timeout"] = self._timeout
        return params
