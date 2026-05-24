from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message explaining how the bot works."""
    await update.message.reply_text(
        "👋 *Welcome to Copy Bot!*\n\n"
        "Just send me any text and I'll give you a *Copy* button for it.\n\n"
        "You can also use me in any chat by typing:\n"
        "`@YourBotUsername your text here`",
        parse_mode="Markdown",
    )
