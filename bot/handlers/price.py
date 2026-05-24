from telegram import Update
from telegram.ext import ContextTypes

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the static Diamond Price list."""
    price_text = (
        "💰 *Diamond Price*\n\n"
        "Weekly Pass: 10000 mmk\n"
        "10 💎 : 2000 mmk\n"
        "20 💎 : 4000 mmk\n"
        "30 💎 : 6000 mmk\n"
        "40 💎 : 8000 mmk\n"
        "50 💎 : 10000 mmk"
    )
    await update.message.reply_text(price_text, parse_mode="Markdown")
