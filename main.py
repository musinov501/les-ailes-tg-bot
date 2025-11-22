import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.config import BOT_TOKEN, DEVELOPER
from core.database_settings import database
from handlers import text_handlers
from utils.set_default_commands import set_default_commands


async def startup(bot: Bot):
    await database.connect()
    # Delete webhook if exists to allow polling
    await bot.delete_webhook(drop_pending_updates=True)
    await set_default_commands(bot)
    await bot.send_message(text="Bot start to work", chat_id=DEVELOPER)


async def shutdown(bot: Bot):
    await database.disconnect()
    await bot.send_message(text="Bot stopped", chat_id=DEVELOPER)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router=text_handlers.router)


    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot, polling_timeout=0)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    asyncio.run(main())




