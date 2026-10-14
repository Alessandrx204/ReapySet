import logging

import discord
from discord import app_commands
from discord.ext import commands


logger = logging.getLogger(__name__)


def register_error_handler(
    bot: commands.Bot,
) -> None:
    """Register the global slash-command error handler."""

    @bot.tree.error
    async def on_app_command_error(
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        logger.error(
            "Application command error: %s",
            error,
            exc_info=error,
        )

        message = "An unexpected error occurred."

        # A Discord interaction can only receive its first response once.
        if interaction.response.is_done():
            await interaction.followup.send(
                message,
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True,
            )