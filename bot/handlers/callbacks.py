from telegram import Update
from telegram.ext import ContextTypes

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
