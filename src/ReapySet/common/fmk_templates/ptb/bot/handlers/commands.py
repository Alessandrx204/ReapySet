from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from bot.services.greetings import build_greeting


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handle the /start command."""

    message = update.effective_message

    if message is None:
        return

    user_name = (
        update.effective_user.first_name
        if update.effective_user
        else None
    )

    await message.reply_text(
        build_greeting(user_name)
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the available bot commands."""

    message = update.effective_message

    if message is None:
        return

    await message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this message\n"
        "/about - About this bot"
    )


async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show basic information about the bot."""

    message = update.effective_message

    if message is None:
        return

    await message.reply_text(
        "Telegram bot generated with ReapySet."
    )


def register_command_handlers(
    application: Application,
) -> None:
    """Register all command handlers in one place."""

    application.add_handlers(
        [
            CommandHandler("start", start),
            CommandHandler("help", help_command),
            CommandHandler("about", about),
        ]
    )