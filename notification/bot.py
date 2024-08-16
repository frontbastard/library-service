import asyncio
from decouple import config
from telegram.ext import ApplicationBuilder


async def send_telegram_message(message):
    app = ApplicationBuilder().token(config("TELEGRAM_BOT_TOKEN")).build()
    chat_id = config("TELEGRAM_CHAT_ID")
    await app.bot.send_message(chat_id=chat_id, text=message)
    await app.shutdown()


def send_telegram_message_sync(message):
    asyncio.run(send_telegram_message(message))
