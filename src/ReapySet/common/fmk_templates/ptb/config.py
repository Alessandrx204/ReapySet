import os


# Keep secrets outside the source code.
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not configured."
    )