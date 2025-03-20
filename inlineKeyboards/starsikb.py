from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def back():
    kb = InlineKeyboardBuilder()
    kb.button(text="« Назад", callback_data="profile")
    return kb.as_markup()

def pay_stars(stars):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"Оплатить ⭐️ {stars}", pay=True)
    return kb.as_markup()