from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Reply to regular text messages."""

    message = update.effective_message

    if message is None or message.text is None:
        return

    await message.reply_text(
        f"You said: {message.text}"
    )


def register_message_handlers(
    application: Application,
) -> None:
    """Register handlers for non-command messages."""

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo,
        )
    )