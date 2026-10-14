# Telegram Bot

A structured Telegram bot starter generated with **ReapySet** using `python-telegram-bot`.

## Getting Started

Create a bot with **BotFather** on Telegram and copy the bot token.

Set the token as an environment variable before starting the application.

### PowerShell

```powershell
$env:BOT_TOKEN="your_bot_token_here"
uv run python main.py
```

### macOS / Linux

```bash
export BOT_TOKEN="your_bot_token_here"
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
├── bot/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   └── messages.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── greetings.py
│   └── error_handler.py
├── .env.example
└── README.md
```

- `main.py` — Builds the Telegram application and starts polling.
- `config.py` — Loads configuration and environment variables.
- `bot/handlers/commands.py` — Handles commands such as `/start` and `/help`.
- `bot/handlers/messages.py` — Handles regular text messages.
- `bot/services/` — Contains reusable application logic.
- `bot/error_handler.py` — Handles and logs unexpected errors.
- `.env.example` — Example environment configuration.

## Available Commands

The starter bot includes:

```text
/start   Start the bot
/help    Show available commands
/about   Show basic bot information
```

Regular text messages are handled by the echo handler.

## Adding a Command

Create a new async handler in:

```text
bot/handlers/commands.py
```

Example:

```python
async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message is None:
        return

    await update.effective_message.reply_text("Pong!")
```

Then register it:

```python
CommandHandler("ping", ping)
```

inside `register_command_handlers()`.

The command will then be available as:

```text
/ping
```

## Adding Message Handlers

Message handlers are registered in:

```text
bot/handlers/messages.py
```

For example:

```python
MessageHandler(
    filters.PHOTO,
    handle_photo,
)
```

Use PTB filters to decide which updates each handler should receive.

## Application Logic

Keep Telegram-specific code inside `handlers/`.

Reusable logic should be placed inside:

```text
bot/services/
```

For example:

```text
handler
   ↓
service
   ↓
application logic
```

This keeps handlers small and makes the project easier to extend.

## Environment Variables

Never store the real bot token directly in the source code.

Example:

```text
BOT_TOKEN=your_bot_token_here
```

The provided `.env.example` can be used as a reference for required configuration.

If you choose to use a local `.env` file, make sure it is excluded from Git.

## Polling

The starter uses Telegram long polling:

```python
application.run_polling()
```

This is convenient for local development and small-to-medium deployments.

For production environments, you can later switch to webhooks if required.

## Documentation

Official `python-telegram-bot` documentation:

https://docs.python-telegram-bot.org/