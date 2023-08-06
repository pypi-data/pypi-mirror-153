import logging

import discord

logger = logging.getLogger(__name__)


class DiscordClient(discord.Client):
    """Custom sub-class for handling Discord events"""

    async def on_connect(self):
        logger.info("%s has connected to Discord", self.user.name)

    async def on_ready(self):
        logger.info("%s as logged in successfully", self.user.name)

    async def on_disconnect(self):
        logger.info("Client has disconnected from Discord")
