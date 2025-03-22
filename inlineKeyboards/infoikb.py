from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def info():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🆘 Тех. поддержка", url="t.me/durov"))
    row.append(1)
    kb.add(InlineKeyboardButton(text="🛠 Инструкция", callback_data="instructions"))
    kb.add(InlineKeyboardButton(text="🧠 Правила", callback_data="rules"))
    row.append(2)
    # kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_main"))
    # row.append(1)
    return kb.adjust(*row).as_markup()

async def rules():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🧠 Правила", callback_data="rules"))
    kb.add(InlineKeyboardButton(text="🆘 Тех. поддержка", url="t.me/durov"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def delete_msg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()