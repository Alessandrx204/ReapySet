def build_greeting(
    name: str | None,
) -> str:
    """Build the greeting used by the /start command."""

    if name:
        return (
            f"Hello, {name}!\n\n"
            "Your Telegram bot is up and running."
        )

    return "Hello! Your Telegram bot is up and running."