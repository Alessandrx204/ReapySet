import os

from dotenv import load_dotenv


# Loads variables from the local .env file.
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN is not configured."
    )