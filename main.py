import asyncio

import aiogram

from bd.base import create_tables
from bot.routers import router
from config.config import BOT_TOKEN

bot = aiogram.Bot(BOT_TOKEN)
dp = aiogram.Dispatcher()


async def start_bot():
    await create_tables()


async def main():
    dp.include_router(router=router)
    dp.startup.register(start_bot)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
