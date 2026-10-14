from bot.client import DiscordBot
from config import BOT_TOKEN


def main() -> None:
    """Creates and starts the Discord bot."""

    bot = DiscordBot()
    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()