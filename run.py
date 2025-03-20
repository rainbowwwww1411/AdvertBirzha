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
from handlers.info import irouter
from handlers.delete import drouter
from handlers.methods.cryptobot import cbrouter, check_payments_task
from handlers.methods.crypto import nprouter, check_payments_task_np
from handlers.methods.stars import psrouter
from autoclean import auto_clean
from ban import brouter


async def main():
    await async_main()
    load_dotenv()
    async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(srouter)
        dp.include_router(prouter)
        dp.include_router(arouter)
        dp.include_router(irouter)
        dp.include_router(drouter)
        dp.include_router(brouter)
        dp.include_router(cbrouter)
        dp.include_router(nprouter)
        dp.include_router(psrouter)
        asyncio.create_task(auto_clean())
        asyncio.create_task(check_payments_task())
        asyncio.create_task(check_payments_task_np())
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    