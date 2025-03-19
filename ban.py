from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Router, Bot
from aiogram.types import Message, TelegramObject, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select, delete
from database.models import async_session, BannedUser
from datetime import datetime
import database.requests as rq
from admin import IsAdmin
import inlineKeyboards.infoikb as ikb


class Database:
    @staticmethod
    async def is_banned(tg_id: int) -> bool:
        async with async_session() as session:
            return await session.scalar(select(BannedUser).where(BannedUser.tg_id == tg_id)) is not None

    @staticmethod
    async def ban_user(tg_id: int, reason: str = "Нарушение правил"):
        datetime_now = str(datetime.now()).split('.')[0]
        async with async_session() as session:
            try:
                user = BannedUser(tg_id=tg_id, reason=reason, date=datetime_now)
                session.add(user)
                await session.commit()
            except Exception as e:
                print(f"Ошибка в бане: {e}")

    @staticmethod
    async def unban_user(tg_id: int):
        async with async_session() as session:
            stmt = delete(BannedUser).where(BannedUser.tg_id == tg_id)
            await session.execute(stmt)
            await session.commit()

class BansMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user = data.get("event_from_user")
            check = await Database.is_banned(user.id)
            if user and check:
                user_data = await rq.get_ban_user(user.id)
                for user in user_data:
                    await event.answer(f"🚫 <b>Вы забанены.</b>\nПричина: {user.reason}.\nДата и время бана по мск: {user.date}.\n\n<b>Получить разбан можно лишь по условиям, указанных в правилах.</b>\nЕсли вас забанили по ошибке, обратитесь в тех. поддержку.", reply_markup=await ikb.rules())
                return
        elif isinstance(event, CallbackQuery):
            user = data.get("event_from_user")
            check = await Database.is_banned(user.id)
            if user and check:
                user_data = await rq.get_ban_user(user.id)
                for user in user_data:
                    await event.message.answer(f"🚫 <b>Вы забанены.</b>\nПричина: {user.reason}.\nДата и время бана по мск: {user.date}.\n\n<b>Получить разбан можно лишь по условиям, указанных в правилах.</b>\nЕсли вас забанили по ошибке, обратитесь в тех. поддержку.", reply_markup=await ikb.rules())
                return
        return await handler(event, data)



# Инициализация роутера и middleware
brouter = Router()
brouter.message.middleware(BansMiddleware())

@brouter.message(Command("ban"), IsAdmin(6299587911))
async def ban_user(message: Message, bot: Bot):
    try:
        parts = message.text.split()
        tg_id = int(message.text.split(' ')[1])
        reason = ' '.join(parts[2:]) or "Нарушение правил"
        await Database.ban_user(tg_id, reason)
        await message.answer(f"✅ Пользователь {tg_id} заблокирован. Причина: {reason}")
    except (IndexError, ValueError):
        await message.answer("Использование: /ban <tg_id> [причина]")

@brouter.message(Command("unban"), IsAdmin(6299587911))
async def unban_user(message: Message, bot: Bot):
    try:
        tg_id = int(message.text.split()[1])
        await Database.unban_user(tg_id)
        await message.answer(f"✅ Пользователь {tg_id} разблокирован")
    except (IndexError, ValueError):
        await message.answer("Использование: /unban <tg_id>")

@brouter.message(Command("ban_info"))
async def ban_info(message: Message):
    user_data = await rq.get_ban_user(message.from_user.id)
    if user_data:
        for user in user_data:
            await message.answer(f"ℹ️ Вы забанены. Причина: {user.reason}. Время бана по мск: {user.date}")

@brouter.message(Command("myid"))
async def get_id(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")

