import inlineKeyboards.advsikb as ikb
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from function.ban import BansMiddleware
from function.antiflood import AntiFloodMiddleware

arouter = Router()
arouter.message.middleware(AntiFloodMiddleware())
arouter.callback_query.middleware(AntiFloodMiddleware())
arouter.callback_query.middleware(BansMiddleware())

@arouter.callback_query(F.data=='advs')
async def advs(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Здесь вы можете купить или продать рекламу.', reply_markup=await ikb.advs(callback.from_user.id))
    
@arouter.message(F.text=='📊 Биржа')
async def advs(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Здесь вы можете купить или продать рекламу.', reply_markup=await ikb.advs(message.from_user.id))