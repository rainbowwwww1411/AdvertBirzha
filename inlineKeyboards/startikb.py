from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def start():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📊 Биржа", callback_data="fed"))
    kb.add(InlineKeyboardButton(text="👤 Профиль", callback_data="night"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="⚙️ Настройки", callback_data="top"))
    row.append(1)
    return kb.adjust(*row).as_markup()