import database.requests as rq
import os
from inlineKeyboards.delete_message import delete_msg
import inlineKeyboards.profileikb as ikb
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states import get
from ban import BansMiddleware

prouter = Router()
prouter.callback_query.middleware(BansMiddleware())

@prouter.callback_query(F.data=="profile")
async def profile(callback: CallbackQuery):
    user_data = await rq.get_user(callback.from_user.id)
    rating = round(await rq.check_user_rating(callback.from_user.id), 2)
    for user in user_data:
        await callback.message.edit_text(f"""📋 Профиль
                                         
🙋🏻‍♂️ Ваш ID: <code>{callback.from_user.id}</code>

🏦 Ваш баланс: <code>{user.balance}</code>
⭐️ Ваша оценка: <code>{rating}</code>

🤝 Количество сделок: <code>{user.deals_count}</code>
👥 Количество рефералов: <code>{user.ref_count}</code>""", reply_markup=await ikb.profile(callback.from_user.id))