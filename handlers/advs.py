import inlineKeyboards.advsikb as ikb
from aiogram import Router, F
from aiogram.types import CallbackQuery
from ban import BansMiddleware

arouter = Router()
arouter.callback_query.middleware(BansMiddleware())

@arouter.callback_query(F.data=='advs')
async def advs(callback: CallbackQuery):
    await callback.message.edit_text('Здесь вы можете купить или продать рекламу.', reply_markup=await ikb.advs(callback.from_user.id))