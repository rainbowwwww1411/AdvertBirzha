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
from handlers.withdraw import wrouter
from handlers.advs import arouter
from handlers.info import irouter
from handlers.delete import drouter
from handlers.apanel.apanel import adminrouter
from handlers.apanel.broadcast import broadcastrouter
from handlers.apanel.withdraw_requests import chwrouter
from handlers.methods.cryptobot import cbrouter, check_payments_task
from handlers.methods.crypto import nprouter, check_payments_task_np
from handlers.methods.stars import psrouter
from function.autoclean import auto_clean
from function.ban import brouter
from function.captcha import captcha_cleaner

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
        dp.include_router(wrouter)
        dp.include_router(adminrouter)
        dp.include_router(broadcastrouter)
        dp.include_router(chwrouter)
        asyncio.create_task(captcha_cleaner())
        asyncio.create_task(auto_clean())
        asyncio.create_task(check_payments_task())
        asyncio.create_task(check_payments_task_np())
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    