import database.requests as rq
import os
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import get

drouter = Router()

@drouter.callback_query(F.data=='delete')
async def delete(callback: types.CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)