from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder
from settings import ADMINS

def start(tg_id):
    kb = ReplyKeyboardBuilder()
    row = []
    kb.add(KeyboardButton(text="📊 Биржа"))
    kb.add(KeyboardButton(text="👤 Профиль"))
    row.append(2)
    kb.add(KeyboardButton(text="📚 Информация"))
    row.append(1)
    if tg_id in ADMINS:
        kb.add(KeyboardButton(text="💎 Админ-Панель"))
        row.append(1)
    return kb.adjust(*row).as_markup(resize_keyboard=True)