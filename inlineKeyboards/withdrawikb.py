from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def withdraw_methods():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="💵 CryptoBot (от 100руб)", callback_data="withdraw_method_CryptoBot"))
    kb.add(InlineKeyboardButton(text="💰 TON (от 500руб)", callback_data="withdraw_method_TON"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="💸 СБП (от 500руб)", callback_data="withdraw_method_СБП"))
    kb.add(InlineKeyboardButton(text="💳 Карты РФ (от 1000руб)", callback_data="withdraw_method_Карты РФ"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="profile"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def to_withdraw():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="withdraw_balance"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def withdraw_next():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Продолжить", callback_data="withdraw_next"))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="withdraw_balance"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def back():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="profile"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def withdraw_choice():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="BTC", callback_data="withdraw_choice_BTC"))
    kb.add(InlineKeyboardButton(text="ETH", callback_data="withdraw_choice_ETH"))
    kb.add(InlineKeyboardButton(text="SOL", callback_data="withdraw_choice_SOL"))
    row.append(3)
    kb.add(InlineKeyboardButton(text="TRX", callback_data="withdraw_choice_TRX"))
    kb.add(InlineKeyboardButton(text="TON", callback_data="withdraw_choice_TON"))
    kb.add(InlineKeyboardButton(text="USDT(TRC20)", callback_data="withdraw_choice_USDT"))
    row.append(3)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="withdraw_balance"))
    row.append(1)
    return kb.adjust(*row).as_markup()