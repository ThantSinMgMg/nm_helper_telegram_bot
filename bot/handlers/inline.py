import uuid
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

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
