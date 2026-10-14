import logging

import discord
from discord.ext import commands

from bot.commands import register_commands
from bot.errors import register_error_handler


logger = logging.getLogger(__name__)


class DiscordBot(commands.Bot):
    """Main Discord bot client."""

    def __init__(self) -> None:
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self) -> None:
        """Configure commands before the bot connects."""

        register_commands(self)
        register_error_handler(self)

        # Register slash commands with Discord.
        synced_commands = await self.tree.sync()

        logger.info(
            "Synced %s application command(s)",
            len(synced_commands),
        )

    async def on_ready(self) -> None:
        """Called when the bot is connected and ready."""

        if self.user is None:
            return

        logger.info(
            "Logged in as %s (%s)",
            self.user,
            self.user.id,
        )