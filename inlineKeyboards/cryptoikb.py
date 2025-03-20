from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def payn_crypto():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="BTC", callback_data="payn_BTC"))
    kb.add(InlineKeyboardButton(text="ETH", callback_data="payn_ETH"))
    kb.add(InlineKeyboardButton(text="SOL", callback_data="payn_SOL"))
    row.append(3)
    kb.add(InlineKeyboardButton(text="TRX", callback_data="payn_TRX"))
    kb.add(InlineKeyboardButton(text="LTC", callback_data="payn_LTC"))
    kb.add(InlineKeyboardButton(text="TON", callback_data="payn_TON"))
    row.append(3)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="back_payn"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def back():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="profile"))
    row.append(1)
    return kb.adjust(*row).as_markup()
