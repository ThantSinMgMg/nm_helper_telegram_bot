"""
Telegram Copy Bot
=================
Modularized version of the Telegram Copy Bot.
Logic is isolated in bot/handlers/ directory.
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    filters,
)
from bot.handlers import start, price, setprice, id_handler, handle_text, copy_callback, inline_query

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_GROUP_ID =  os.getenv("ALLOWED_GROUP_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Check your .env file.")

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ── Main entry point ──────────────────────────────────────────────────────────
def main() -> None:
    """Run the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Store config in bot_data for handlers to access
    app.bot_data["ALLOWED_GROUP_ID"] = ALLOWED_GROUP_ID

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_handler))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("setprice", setprice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(copy_callback, pattern=r"^copy:"))
    app.add_handler(InlineQueryHandler(inline_query))

    logger.info("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
