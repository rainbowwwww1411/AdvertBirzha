import database.requests as rq
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import CallbackQuery, Message
from states import get
import inlineKeyboards.startikb as ikb

srouter = Router()

@srouter.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if message.text == '/start':
        await rq.set_user(message.from_user.id, 'None')
    else:
        invatitefrom = decode_payload(message.text.split(' ')[1])
        new_if = f"{invatitefrom}"
        await rq.set_user(message.from_user.id, new_if)
    user_data = await rq.get_user(message.from_user.id)
    for user in user_data:
        if user.name == 'None':
            await message.answer("Введите ваше имя/псевдоним (не более 30 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
            await state.set_state(get.name)
        else:
            await message.answer("🚀")
            await message.answer("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=await ikb.start())

@srouter.message(get.name)
async def getname(message: Message, state: FSMContext):
    if len(message.text) <=30:
        await rq.upd_name(message.from_user.id, message.text)
        await state.clear()
        await message.answer("🚀")
        await message.answer("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=await ikb.start())
    else:
        await message.answer("Введите ваше имя/псевдоним (не более 30 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
        await state.set_state(get.name)
        
@srouter.callback_query(F.data=="to_main")
async def to_main(callback: CallbackQuery):
    await callback.message.edit_text("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=await ikb.start())