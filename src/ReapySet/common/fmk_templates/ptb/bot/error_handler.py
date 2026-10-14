import logging

from telegram import Update
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Log unexpected errors and notify the user when possible."""

    logger.exception(
        "Unhandled exception while processing an update",
        exc_info=context.error,
    )

    if not isinstance(update, Update):
        return

    message = update.effective_message

    if message is not None:
        await message.reply_text(
            "An unexpected error occurred."
        )