from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def start():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📊 Биржа", callback_data="advs"))
    kb.add(InlineKeyboardButton(text="👤 Профиль", callback_data="profile"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"))
    row.append(1)
    return kb.adjust(*row).as_markup()