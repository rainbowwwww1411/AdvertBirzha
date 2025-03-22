from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq
from settings import technical_support

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

async def check_withdraws():
    kb = InlineKeyboardBuilder()
    row = []
    withdraws_data = await rq.get_withdraws()
    for withdraw in withdraws_data:
        kb.add(InlineKeyboardButton(text=f"id {withdraw.id} • Сумма {withdraw.sum_last} • @{withdraw.username}", callback_data=f"check_withdraw_{withdraw.id}"))
        row.append(1)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="to_apanel"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def check_withdraw(id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Подтвердить", callback_data=f"awithdraw_approve_{id}"))
    kb.add(InlineKeyboardButton(text="Отклонить", callback_data=f"awithdraw_decline_{id}"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="Отправить сообщение", callback_data=f"message_user_{id}"))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="check_withdraws"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def to_withdraws():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data="check_withdraws"))
    row.append(1)
    return kb.adjust(*row).as_markup()


async def next_withdraw_approve(id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Прикрепить сообщение", callback_data=f"awithdrawapprove_yes_{id}"))
    kb.add(InlineKeyboardButton(text="Без", callback_data=f"awithdrawapprove_no_{id}"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data=f"check_withdraw_{id}"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def next_withdraw_decline(id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Прикрепить сообщение", callback_data=f"awithdrawdecline_yes_{id}"))
    kb.add(InlineKeyboardButton(text="Без", callback_data=f"awithdrawdecline_no_{id}"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data=f"check_withdraw_{id}"))
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

async def withdraw_msg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🆘 Тех. Поддержка", url=technical_support))
    kb.add(InlineKeyboardButton(text="❌ Понятно", callback_data="delete"))
    row.append(1)
    return kb.adjust(*row).as_markup()