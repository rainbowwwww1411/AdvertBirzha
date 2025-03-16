from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq
import func as fn

async def advs(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Купить", callback_data="buy"))
    kb.add(InlineKeyboardButton(text="Продать", callback_data="sell"))
    row.append(2)
    
    deal_data = await rq.get_deals()
    for deal in deal_data:
        if deal.tg_id == tg_id:
            kb.add(InlineKeyboardButton(text="Мои сделки", callback_data="my_deals"))
            break
    
    kb.add(InlineKeyboardButton(text="Создать объявление", callback_data="create_announcement"))
    
    response = await fn.check_adv(tg_id)
    if response:
        kb.add(InlineKeyboardButton(text="Мои объявление", callback_data="my_announcement"))
    row.append(1)
    return kb.adjust(*row).as_markup()