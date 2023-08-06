import discord
from google.protobuf import json_format

from discordproxy import discord_api_pb2, discord_api_pb2_grpc
from discordproxy._decorators import handle_discord_exceptions, log_request


def discord_to_grpc_embed(embed) -> discord_api_pb2.Embed:
    embed_dict = embed.to_dict()
    return json_format.ParseDict(embed_dict, discord_api_pb2.Embed())


# def discord_to_grpc_role(role) -> discord_api_pb2.Role:
#     grpc_role = discord_api_pb2.Role(
#         id=role.id,
#         name=role.name,
#         color=role.color.value,
#         hoist=role.hoist,
#         position=role.position,
#         # permissions=role.permissions, TODO
#         managed=role.managed,
#         mentionable=role.mentionable,
#     )
#     if role.tags:
#         grpc_role.tags = [discord_to_grpc_role_tag(obj) for obj in role.tags]
#     return grpc_role


# def discord_to_grpc_role_tag(role_tag) -> discord_api_pb2.Role.Tag:
#     return discord_api_pb2.Role.Tag(
#         id=role_tag.bot_id,
#         integration_id=role_tag.integration_id,
#         premium_subscriber=role_tag.is_premium_subscriber(),
#     )


def discord_to_grpc_message(message) -> discord_api_pb2.Message:
    def user_avatar_adapter(user) -> str:
        """Get user's avatar hash. Works with both old and new pycord API."""
        version_info = discord.version_info
        if version_info.major < 2:
            return user.avatar  # works with pycord 1 only.
        return user.avatar.key

    author = discord_api_pb2.User(
        id=message.author.id,
        username=message.author.name,
        discriminator=message.author.discriminator,
        avatar=user_avatar_adapter(message.author),
        bot=message.author.bot,
        system=message.author.system,
    )
    if isinstance(message.author, discord.Member):
        member = discord_api_pb2.GuildMember(
            user=author,
            nick=message.author.nick,
            roles=[obj.id for obj in message.author.roles],
            joined_at=message.author.joined_at.isoformat()
            if message.author.joined_at
            else None,
            # permissions=message.author.permissions.value, TODO
        )
    else:
        member = None
    return discord_api_pb2.Message(
        id=message.id,
        channel_id=message.channel.id if message.channel else None,
        guild_id=message.guild.id if message.guild else None,
        author=author,
        member=member,
        content=message.content,
        embeds=[discord_to_grpc_embed(obj) for obj in message.embeds],
    )


def discord_to_grpc_channel_type(
    channel_type: discord.ChannelType,
) -> discord_api_pb2.Channel.Type:
    type_map = {
        discord.ChannelType.text: discord_api_pb2.Channel.Type.GUILD_TEXT,
        discord.ChannelType.private: discord_api_pb2.Channel.Type.DM,
        discord.ChannelType.voice: discord_api_pb2.Channel.Type.GUILD_VOICE,
        discord.ChannelType.group: discord_api_pb2.Channel.Type.GROUP_DM,
        discord.ChannelType.category: discord_api_pb2.Channel.Type.GUILD_CATEGORY,
        discord.ChannelType.news: discord_api_pb2.Channel.Type.GUILD_NEWS,
        # REMOVED FROM API
        # discord.ChannelType.store: discord_api_pb2.Channel.Type.GUILD_STORE,
    }
    return type_map.get(channel_type, discord_api_pb2.Channel.Type.UNDEFINED)


def discord_to_grpc_channel(
    channel: discord.abc.GuildChannel,
) -> discord_api_pb2.Channel:
    try:
        guild_id = channel.guild.id
    except AttributeError:
        guild_id = None
    try:
        topic = channel.topic
    except AttributeError:
        topic = None
    if channel.type == discord.ChannelType.text:
        nsfw = channel.is_nsfw()
        last_message_id = channel.last_message_id
    else:
        nsfw = None
        last_message_id = None
    return discord_api_pb2.Channel(
        id=channel.id,
        name=channel.name,
        type=discord_to_grpc_channel_type(channel.type),
        guild_id=guild_id,
        position=channel.position,
        topic=topic,
        nsfw=nsfw,
        last_message_id=last_message_id,
        parent_id=channel.category_id,
    )


class DiscordApi(discord_api_pb2_grpc.DiscordApiServicer):
    def __init__(self, discord_client) -> None:
        super().__init__()
        self.discord_client = discord_client

    @log_request
    @handle_discord_exceptions(discord_api_pb2.SendChannelMessageResponse)
    async def SendChannelMessage(self, request, context):
        channel = await self.discord_client.fetch_channel(request.channel_id)
        message = await self._send_message_to_channel(request, channel)
        return discord_api_pb2.SendChannelMessageResponse(
            message=discord_to_grpc_message(message)
        )

    @log_request
    @handle_discord_exceptions(discord_api_pb2.SendDirectMessageResponse)
    async def SendDirectMessage(self, request, context):
        user = await self.discord_client.fetch_user(request.user_id)
        channel = await user.create_dm()
        message = await self._send_message_to_channel(request, channel)
        return discord_api_pb2.SendDirectMessageResponse(
            message=discord_to_grpc_message(message)
        )

    @staticmethod
    async def _send_message_to_channel(request, channel):
        kwargs = {"content": request.content}
        if request.embed.ByteSize():
            embed_dct = json_format.MessageToDict(request.embed)
            kwargs["embed"] = discord.Embed.from_dict(embed_dct)
        return await channel.send(**kwargs)

    @log_request
    @handle_discord_exceptions(discord_api_pb2.GetGuildChannelsResponse)
    async def GetGuildChannels(self, request, context):
        guild = await self.discord_client.fetch_guild(request.guild_id)
        channels = await guild.fetch_channels()
        channels_2 = [discord_to_grpc_channel(channel) for channel in channels]
        return discord_api_pb2.GetGuildChannelsResponse(channels=channels_2)
