from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq

async def apanel():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Создать рассылку", callback_data="send_msgs"))
    row.append(1)
    kb.add(InlineKeyboardButton(text="Выводы", callback_data="check_withdraws"))
    row.append(1)
    kb.add(InlineKeyboardButton(text="Пользователи", callback_data="check_users"))
    kb.add(InlineKeyboardButton(text="Объявления", callback_data="check_advs"))
    row.append(2)
    return kb.adjust(*row).as_markup()

async def to_apanel():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_apanel"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def send_msgs():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="С фото", callback_data="broadcast_photo"))
    kb.add(InlineKeyboardButton(text="Текст", callback_data="broadcast_text"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_apanel"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def to_send_msgs():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="send_msgs"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def choice_button():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="✅ Да, добавить кнопку", callback_data="add_button_yes"))
    kb.add(InlineKeyboardButton(text="❌ Нет, начать рассылку", callback_data="add_button_no"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def button(text, url):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text=text, url=url))
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def delete_msg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()