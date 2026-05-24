import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from telegram.ext import ContextTypes

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
