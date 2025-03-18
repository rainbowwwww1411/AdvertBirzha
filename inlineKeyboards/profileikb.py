from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq

async def profile(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📥 Пополнить баланс", callback_data="top_up_balance"))
    rating = await rq.check_user_rating(tg_id)
    if rating != 0:
        kb.add(InlineKeyboardButton(text="🗂 Показать отзывы", callback_data="show_reviews"))
    kb.add(InlineKeyboardButton(text="👥 Реферальная система", callback_data="referal_system"))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_main"))
    row.append(1)
    return kb.adjust(*row).as_markup()