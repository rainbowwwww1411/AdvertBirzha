import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database.models import async_main
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers.start import srouter
from handlers.profile import prouter
from handlers.advs import arouter

async def main():
    await async_main()
    load_dotenv()
    async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(srouter)
        dp.include_router(prouter)
        dp.include_router(arouter)
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    