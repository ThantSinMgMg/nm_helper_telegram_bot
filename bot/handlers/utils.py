from telegram import Update
from telegram.ext import ContextTypes

async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the current chat's ID and information."""
    chat = update.effective_chat
    if not chat:
        return

    chat_id = chat.id
    chat_type = chat.type.capitalize()
    
    # Get the most appropriate title/name
    chat_title = chat.title or chat.username or chat.first_name or "Unknown"

    message = (
        "ℹ️ *Chat Information*\n"
        f"• *Chat Title/Name:* {chat_title}\n"
        f"• *Chat ID:* `{chat_id}`\n"
        f"• *Type:* {chat_type}"
    )
    
    await update.message.reply_text(message, parse_mode="Markdown")
