import database.requests as rq
import os
import inlineKeyboards.advsikb as ikb
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import get

arouter = Router()

@arouter.callback_query(F.data=='advs')
async def advs(callback: types.CallbackQuery):
    await callback.message.edit_text('Здесь вы можете купить или продать рекламу.', reply_markup=await ikb.advs(callback.from_user.id))