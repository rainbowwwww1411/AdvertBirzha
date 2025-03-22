from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from collections import defaultdict
import time
from inlineKeyboards.delete_message import delete_msg

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=3, interval=2):
        self.user_timestamps = defaultdict(list)
        self.rate_limit = rate_limit
        self.interval = interval

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        now = time.time()

        # Фильтрация старых записей
        self.user_timestamps[user_id] = [
            t for t in self.user_timestamps[user_id] 
            if now - t < self.interval
        ]

        if len(self.user_timestamps[user_id]) >= self.rate_limit:
            # Определяем тип события
            if isinstance(event, Message):
                await event.answer(
                    "🛑 Слишком много запросов! Подождите.", 
                    reply_markup=await delete_msg()
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "⚠️ Вы слишком активны! Подождите 2 секунды",
                    show_alert=True
                )
            return

        self.user_timestamps[user_id].append(now)
        return await handler(event, data)
