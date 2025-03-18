from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def delete_msg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()