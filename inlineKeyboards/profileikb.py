from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq

async def profile(tg_id, balance):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📥 Пополнить", callback_data="top_up_balance"))
    kb.add(InlineKeyboardButton(text="📤 Вывести", callback_data="withdraw_balance"))
    row.append(2)
    rating = await rq.check_user_rating(tg_id)
    if rating != 0:
        kb.add(InlineKeyboardButton(text="🗂 Показать отзывы", callback_data="show_reviews"))
    kb.add(InlineKeyboardButton(text="👥 Реферальная система", callback_data="referal_system"))
    # kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_main"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def back():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="profile"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def pay_methods():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🪙 Crypto", callback_data="pay_NowPayments"))
    kb.add(InlineKeyboardButton(text="💸 CryptoBot", callback_data="pay_CryptoBot"))
    kb.add(InlineKeyboardButton(text="⭐️ Звёзды", callback_data="pay_Stars"))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="profile"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def pay_next(pay_url):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="💳 Перейти к оплате", url=pay_url))
    row.append(1)
    return kb.adjust(*row).as_markup()