import logging

from telegram.ext import Application, ApplicationBuilder

from bot.error_handler import error_handler
from bot.handlers.commands import register_command_handlers
from bot.handlers.messages import register_message_handlers
from config import BOT_TOKEN


# Basic application logging.
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def build_application() -> Application:
    """Create and configure the Telegram bot application."""

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    # Register bot commands and regular message handlers.
    register_command_handlers(application)
    register_message_handlers(application)

    # Catch unhandled exceptions raised while processing updates.
    application.add_error_handler(error_handler)

    return application


def main() -> None:
    """Start the bot using long polling."""

    logger.info("Starting Telegram bot...")

    application = build_application()

    application.run_polling(
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()