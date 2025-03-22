import database.requests as rq
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import CallbackQuery, Message
from states import get
import inlineKeyboards.startikb as ikb
import keyboards.startkb as kb
from function.antiflood import AntiFloodMiddleware
import random
from function.captcha import emoji_db, all_emoji, CAPTCHA_SIZE, captcha_store, TIMEOUT
import time
from aiogram.utils.keyboard import InlineKeyboardBuilder

srouter = Router()
srouter.message.middleware(AntiFloodMiddleware())

@srouter.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    check_user = await rq.check_user(user_id)
    await state.clear()
    if not check_user:
        await state.update_data(message_text=message.text)
        category = random.choice(list(emoji_db.keys()))
        correct_emoji = random.choice(emoji_db[category])
        
        # Генерируем варианты ответов
        other_emojis = random.sample(
            # Берем только смайлы из других категорий
            [e[1] for e in all_emoji if e[0] != category],  # e[1] - сам эмодзи
            CAPTCHA_SIZE - 1
        )

        variants = [correct_emoji] + other_emojis  # Только эмодзи!
        random.shuffle(variants)

        # Создаем клавиатуру
        builder = InlineKeyboardBuilder()
        for emoji in variants:  # Теперь emoji - строка с эмодзи
            builder.button(text=emoji, callback_data=f"captcha_{emoji}")

        
        # Оптимизированное расположение кнопок
        builder.adjust(3, 3)
        
        # Сохраняем ответ
        captcha_store[user_id] = (correct_emoji, time.time())
        
        await message.answer(
            f"🔐 <b>Подтвердите, что вы не бот!</b>\n"
            f"Выберите: <i>{category}</i>",
            reply_markup=builder.as_markup()
        )
    else:
        user_data = await rq.get_user(user_id)
        for user in user_data:
            if user.name != 'None':
                await message.answer("🚀")
                await message.answer("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=kb.start(user_id))
            else:
                await message.answer("Введите ваше имя/псевдоним (не более 10 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
                await state.set_state(get.name)
                
        
@srouter.callback_query(F.data.startswith("captcha_"))
async def check_captcha(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    selected_emoji = callback.data.split("_")[1]
    
    # Проверка наличия капчи
    if user_id not in captcha_store:
        await callback.answer("Время вышло! Начните заново: /start", show_alert=True)
        return
    
    # Проверка тайм-аута
    correct_emoji, timestamp = captcha_store[user_id]
    if time.time() - timestamp > TIMEOUT:
        del captcha_store[user_id]
        await callback.answer("Время вышло! Начните заново: /start", show_alert=True)
        return
    
    # Проверка ответа
    if selected_emoji != correct_emoji:
        await callback.answer("❌ Неверно! Попробуйте еще раз.", show_alert=True)
        return
    data = await state.get_data()
    del captcha_store[user_id]
    if data['message_text'] == '/start':
        await rq.set_user(user_id, 'None')
    else:
        invatitefrom = decode_payload(data['message_text'].split(' ')[1])
        new_if = f"{invatitefrom}"
        await rq.set_user(user_id, new_if)
    user_data = await rq.get_user(user_id)
    for user in user_data:
        if user.name == 'None':
            await callback.message.edit_text("✅ Вы успешно прошли капчу!\nВведите ваше имя/псевдоним (не более 10 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
            await state.set_state(get.name)
        else:
            await callback.message.answer("🚀")
            await callback.message.answer("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=kb.start(user_id))

@srouter.message(get.name)
async def getname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if len(message.text) <=10 and message.text != 'None':
        check_name = await rq.check_name(message.text)
        if not check_name:
            await rq.upd_name(message.from_user.id, message.text)
        else:
            await message.answer("Это имя уже занято. Введите ваше имя/псевдоним (не более 10 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
            await state.set_state(get.name)
            return
        await state.clear()
        await message.answer("🚀")
        await message.answer("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=kb.start(user_id))
    else:
        await message.answer("Введите ваше имя/псевдоним (не более 10 символов, а также будет выдаваться бан за мат/ругань и т.д.):")
        await state.set_state(get.name)
        
@srouter.callback_query(F.data=="to_main")
async def to_main(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text("Покупайте и продавайте рекламу безопасно и автоматически с нашим сервисом.\n\nПодписывайтесь на наш канал и вступайте в наш чат.", reply_markup=kb.start(user_id))