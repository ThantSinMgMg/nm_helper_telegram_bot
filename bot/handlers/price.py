import os
from telegram import Update
from telegram.ext import ContextTypes

DEFAULT_PRICE_TEXT = (
    "💰 *Diamond Price*\n\n"
    "Weekly Pass: 10000 mmk\n"
    "10 💎 : 2000 mmk\n"
    "20 💎 : 4000 mmk\n"
    "30 💎 : 6000 mmk\n"
    "40 💎 : 8000 mmk\n"
    "50 💎 : 10000 mmk"
)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the contents of price.txt or the default list."""
    if os.path.exists("price.txt"):
        with open("price.txt", "r", encoding="utf-8") as f:
            price_text = f.read()
    else:
        price_text = DEFAULT_PRICE_TEXT
    
    await update.message.reply_text(price_text, parse_mode="Markdown")

async def setprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Update the price.txt file if the user is authorized."""
    allowed_group_id = context.bot_data.get("ALLOWED_GROUP_ID")
    
    # 1. Check if the command was sent in the allowed group
    if update.effective_chat.id != allowed_group_id:
        return

    # 2. Check if the user is an admin or creator
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=allowed_group_id, user_id=user_id)
        if member.status not in ["administrator", "creator"]:
            return
    except Exception:
        # Silently fail if we can't get member info
        return

    # 3. Extract text after /setprice
    # context.args is a list of strings split by whitespace
    # We want the original formatting, so we can use update.message.text
    # but the user said "extract all text sent after the /setprice command"
    command_text = update.message.text or ""
    new_price = command_text.split(None, 1)[1] if len(command_text.split(None, 1)) > 1 else ""

    if not new_price:
        return

    # 4. Save to price.txt
    with open("price.txt", "w", encoding="utf-8") as f:
        f.write(new_price)
    
    await update.message.reply_text("✅ Price list updated successfully!")
