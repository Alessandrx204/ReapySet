# Discord Bot

A simple and structured Discord bot template generated with **ReapySet** using `discord.py`.

## Getting Started ('ω')/

Create a Discord application and bot from the Discord Developer Portal, then copy the bot token.

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

Then start the bot:

```bash
uv run python main.py
```

If you are not using `uv`:

```bash
python main.py
```

## Project Structure

```text
.
├── main.py
├── config.py
├── .env.example
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── commands.py
│   └── errors.py
└── README.md
```

- `main.py` — Application entry point.
- `config.py` — Loads environment variables and bot configuration.
- `bot/client.py` — Defines and configures the Discord bot client.
- `bot/commands.py` — Contains the bot's slash commands.
- `bot/errors.py` — Handles application command errors.
- `.env.example` — Example environment configuration.

## Environment Variables

The bot token must never be stored directly in the source code.

Copy `.env.example` to `.env` and replace the placeholder:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

The `.env` file should not be committed to Git.

## Available Commands

The starter bot includes:

```text
/ping
/hello
/about
```

### `/ping`

Checks whether the bot is responding and displays its current latency.

### `/hello`

Replies with a greeting mentioning the user.

### `/about`

Displays basic information about the bot using a Discord embed.

## Adding a Command guide

Add new slash commands inside:

```text
bot/commands.py
```

Example:

```python
@bot.tree.command(
    name="server",
    description="Show the current server name.",
)
async def server(
    interaction: discord.Interaction,
) -> None:
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "This command must be used inside a server.",
            ephemeral=True,
        )
        return

    await interaction.response.send_message(
        f"Server: {guild.name}"
    )
```

After restarting the bot, the command tree is synchronized with Discord automatically.

## Slash Commands

This starter uses Discord application commands:

```text
/ping
/hello
/about
```

rather than traditional prefix commands such as:

```text
!ping
```

Slash commands integrate directly with Discord's command interface and do not require the Message Content Intent for normal usage.

## Bot Setup

Before running the bot:

1. Create an application in the Discord Developer Portal.
2. Add a bot to the application.
3. Copy the bot token into `.env`.
4. Invite the bot to your server with the required bot and application command permissions.
5. Start the application.

## Error Handling

Unexpected slash-command errors are handled globally in:

```text
bot/errors.py
```

Errors are logged, while users receive a short private error message when possible.

## Documentation

Official `discord.py` documentation:

https://discordpy.readthedocs.io/

Discord Developer Portal:

https://discord.com/developers/applications