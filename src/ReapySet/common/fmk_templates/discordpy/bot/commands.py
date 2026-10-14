import discord
from discord.ext import commands


def register_commands(bot: commands.Bot) -> None:
    """Register the bot's slash commands."""

    @bot.tree.command(
        name="ping",
        description="Check if the bot is responding.",
    )
    async def ping(
        interaction: discord.Interaction,
    ) -> None:
        latency_ms = round(bot.latency * 1000)

        await interaction.response.send_message(
            f"Pong! {latency_ms} ms"
        )

    @bot.tree.command(
        name="hello",
        description="Receive a greeting from the bot.",
    )
    async def hello(
        interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message(
            f"Hello, {interaction.user.mention}!"
        )

    @bot.tree.command(
        name="about",
        description="Show information about this bot.",
    )
    async def about(
        interaction: discord.Interaction,
    ) -> None:
        embed = discord.Embed(
            title="Discord Bot",
            description=(
                "A Discord bot generated with ReapySet."
            ),
        )

        embed.add_field(
            name="Library",
            value="discord.py",
            inline=True,
        )

        await interaction.response.send_message(
            embed=embed,
        )