import asyncio
import re
from states import BroadcastStates
import database.requests as rq
import inlineKeyboards.adminikb as ikb
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from ban import BansMiddleware
from admin import IsAdmin2
from settings import ADMINS
from datetime import datetime
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError

broadcastrouter = Router()
broadcastrouter.callback_query.middleware(BansMiddleware())

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Обработчик выбора типа контента
@broadcastrouter.callback_query(F.data.startswith("broadcast_"), IsAdmin2(ADMINS))
async def select_content_type(callback: CallbackQuery, state: FSMContext):
    content_type = callback.data.split("_")[1]
    
    await state.update_data(content_type=content_type)
    
    if content_type == "text":
        await callback.message.answer("Отправьте текст для рассылки:")
        await state.set_state(BroadcastStates.receive_text)
    elif content_type == "photo":
        await callback.message.answer("Отправьте фото с подписью:")
        await state.set_state(BroadcastStates.receive_photo)
    
    await callback.answer()

# Обработчик текста
@broadcastrouter.message(BroadcastStates.receive_text, F.text, IsAdmin2(ADMINS))
async def receive_text(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text)
    await ask_add_button(message, state)

# Обработчик фото
@broadcastrouter.message(BroadcastStates.receive_photo, F.photo, IsAdmin2(ADMINS))
async def receive_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption if message.caption else ""
    
    await state.update_data(photo=photo_id, caption=caption)
    await ask_add_button(message, state)

async def ask_add_button(message: Message, state: FSMContext):
    
    await message.answer(
        "Добавить инлайн кнопку к сообщению?",
        reply_markup=await ikb.choice_button()
    )
    await state.set_state(BroadcastStates.add_button)

# Обработчик решения о кнопке
@broadcastrouter.callback_query(BroadcastStates.add_button, F.data.startswith("add_button_"), IsAdmin2(ADMINS))
async def handle_button_decision(callback: CallbackQuery, state: FSMContext):
    decision = callback.data.split("_")[2]
    
    if decision == "yes":
        await callback.message.answer("Отправьте данные для кнопки в формате:\nНазвание кнопки - URL")
        await state.set_state(BroadcastStates.receive_button_data)
    else:
        await start_broadcast(callback.bot, state, callback.from_user.id, "no")
        await state.update_data(add_button="no")
    
    await callback.answer()

# Обработчик данных кнопки
@broadcastrouter.message(BroadcastStates.receive_button_data, IsAdmin2(ADMINS))
async def receive_button_data(message: Message, state: FSMContext):
    try:
        button_text, button_url = message.text.split(" - ", 1)
        await state.update_data(button_text=button_text.strip(), button_url=button_url.strip())
        await start_broadcast(message.bot, state, message.from_user.id, "yes")
    except:
        await message.answer("Неправильный формат! Используйте:\nНазвание кнопки - URL")
        return

async def start_broadcast(bot: Bot, state: FSMContext, user_id: int, add_button: str):
    data = await state.get_data()
    await bot.send_message(user_id, "✅ Рассылка начата!", reply_markup=await ikb.to_apanel())
    if add_button != "no":
        text=data['button_text']
        url=data['button_url']
    
        if data['content_type'] == 'text':
            await broadcast_text(
                bot=bot,
                text=data['text'],
                reply_markup=await ikb.button(text, url)
            )
        else:
            await broadcast_photo(
                bot=bot,
                photo=data['photo'],
                caption=data['caption'],
                reply_markup=await ikb.button(text, url)
            )
    else:
        if data['content_type'] == 'text':
            await broadcast_text(
                bot=bot,
                text=data['text'],
                reply_markup=await ikb.delete_msg()
            )
        else:
            await broadcast_photo(
                bot=bot,
                photo=data['photo'],
                caption=data['caption'],
                reply_markup=await ikb.delete_msg()
            )
    
    await state.clear()

async def broadcast_text(bot: Bot, text: str, reply_markup=None):
    users = await rq.get_users()
    start_time = datetime.now()
    successful = 0
    unsuccessful = 0
    
    for user_id in users:
        try:
            await bot.send_message(
                chat_id=user_id.tg_id,
                text=text,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            successful += 1
        except TelegramRetryAfter:
            await asyncio.sleep(10)
        except Exception as e:
            unsuccessful += 1
            print(f"Error: {e}")
    finish_time = datetime.now()
    time = finish_time - start_time
    for admin in ADMINS:
        await bot.send_message(
                        chat_id=admin,
                        text=f"Рассылка была завершена.\nВремя рассылки: {time}.\nУспешно: {successful}\nНеуспешно: {unsuccessful}",
                        reply_markup=await ikb.delete_msg())

async def broadcast_photo(bot: Bot, photo: str, caption: str, reply_markup=None):
    users = await rq.get_users()
    start_time = datetime.now()
    successful = 0
    unsuccessful = 0
    
    for user_id in users:
        try:
            await bot.send_photo(
                chat_id=user_id.tg_id,
                photo=photo,
                caption=caption,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            successful += 1
        except TelegramRetryAfter:
            await asyncio.sleep(10)
        except Exception as e:
            unsuccessful += 1
            print(f"Error: {e}")
    
    finish_time = datetime.now()
    time = finish_time - start_time
    for admin in ADMINS:
        await bot.send_message(
                        chat_id=admin,
                        text=f"Рассылка была завершена.\nВремя рассылки: {time}.\nУспешно: {successful}\nНеуспешно: {unsuccessful}",
                        reply_markup=await ikb.delete_msg())