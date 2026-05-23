"""
Telegram Copy Bot
=================
Send any text → get it back with a Copy button!

HOW TO RUN:
1. Install library:   pip install python-telegram-bot
2. Get a bot token from @BotFather on Telegram
3. Replace YOUR_BOT_TOKEN below
4. Run: python telegram_copy_bot.py

IMPORTANT: Also enable Inline Mode for your bot in @BotFather
  → /mybots → your bot → Bot Settings → Inline Mode → Enable
"""

import logging
import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    filters,
    ContextTypes,
)
from telegram import InlineQueryResultArticle, InputTextMessageContent
import uuid

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Check your .env file.")

# ── Config ────────────────────────────────────────────────────────────────────
# link -> https://t.me/riku_assistant_bot
# Bot Unique Name -> riku_assistant_bot
# Bot Name -> Riku's helper bot


# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# /start  command
# ─────────────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message explaining how the bot works."""
    await update.message.reply_text(
        "👋 *Welcome to Copy Bot!*\n\n"
        "Just send me any text and I'll give you a *Copy* button for it.\n\n"
        "You can also use me in any chat by typing:\n"
        "`@YourBotUsername your text here`",
        parse_mode="Markdown",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Handle text → reply with CopyTextButton
# ─────────────────────────────────────────────────────────────────────────────
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Uses CopyTextButton (Bot API 7.3+) — a special inline button that
    copies any text you specify directly to the user's clipboard in ONE tap.
    No popup, no long-press, no tricks needed!
    """
    user_text = update.message.text

    if not re.fullmatch(r"\d+ \(\d+\)", user_text.strip()):
        return
 
    keyboard = InlineKeyboardMarkup([
        [
            # CopyTextButton: tap → instantly copies user_text to clipboard
            InlineKeyboardButton(
                text="📋 Copy",
                copy_text=CopyTextButton(text=user_text),
            )
        ]
    ])
 
    await update.message.reply_text(
        user_text,
        reply_markup=keyboard,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Callback: user tapped "📋 Copy Text" button
# ─────────────────────────────────────────────────────────────────────────────
async def copy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send the stored text as a plain new message.
    On Android/iOS: long-press the message → Copy Text.
    This is the most reliable way to copy on mobile.
    """
    query = update.callback_query
    await query.answer("✅ Text sent below — long-press it to copy!")  # small toast

    key = query.data.split(":", 1)[1]
    text = context.bot_data.get(key)

    if text is None:
        await query.answer("⚠️ Text expired. Please send it again.", show_alert=True)
        return

    # Send the raw text as a NEW plain message — no markdown, no formatting.
    # Plain text is the easiest to select and copy on Android & iOS.
    await query.message.reply_text(
        f"👇 Long-press this message → tap Copy:\n\n{text}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Inline query: @BotUsername <text>  →  result card with Copy button
# ─────────────────────────────────────────────────────────────────────────────
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Allows users to type  @YourBot some text  inside ANY chat.
    They get a result card they can tap to insert the formatted text.
    """
    query_text = update.inline_query.query.strip()

    if not query_text:
        # Show a hint when no text typed yet
        await update.inline_query.answer(
            results=[],
            switch_pm_text="Send me text directly →",
            switch_pm_parameter="start",
            cache_time=0,
        )
        return

    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="📋 Insert this text",
        description=query_text[:100],
        input_message_content=InputTextMessageContent(
            message_text=f"```\n{query_text}\n```",
            parse_mode="Markdown",
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🔗 Use in another chat",
                switch_inline_query=query_text[:200],
            )]
        ]),
    )

    await update.inline_query.answer(results=[result], cache_time=0)


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    # app.add_handler(CallbackQueryHandler(copy_callback, pattern=r"^copy:"))
    # app.add_handler(InlineQueryHandler(inline_query))

    logger.info("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()