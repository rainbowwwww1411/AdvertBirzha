import database.requests as rq
import inlineKeyboards.adminikb as ikb
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from ban import BansMiddleware
from admin import IsAdmin, IsAdmin2
from settings import ADMINS

adminrouter = Router()
adminrouter.callback_query.middleware(BansMiddleware())

@adminrouter.message(Command('apanel'), IsAdmin(ADMINS))
async def apanel(message: Message):
    await message.answer("Вы упешно вошли в Админ-панель", reply_markup=await ikb.apanel())
    
@adminrouter.callback_query(F.data=="to_apanel", IsAdmin2(ADMINS))
async def apanel_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вы упешно вошли в Админ-панель", reply_markup=await ikb.apanel())
    
@adminrouter.callback_query(F.data=="send_msgs", IsAdmin2(ADMINS))
async def send_msgs(callback: CallbackQuery):
    await callback.message.edit_text("Выберите тип рассылки:", reply_markup=await ikb.send_msgs())

