import database.requests as rq
import inlineKeyboards.starsikb as ikb
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from states import get
from ban import BansMiddleware
from datetime import datetime
from antiflood import AntiFloodMiddleware

psrouter = Router()
psrouter.message.middleware(AntiFloodMiddleware())
psrouter.callback_query.middleware(AntiFloodMiddleware())
psrouter.callback_query.middleware(BansMiddleware())

@psrouter.message(get.sum_stars)
async def sum(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        if amount < 1:
            await message.answer("Минимальная сумма пополнения 100 рублей.", reply_markup=ikb.back())
            return
            
    except ValueError:
        await message.answer("Введите корректную сумму.", reply_markup=ikb.back())
        return
    
    date = datetime.now()
    await rq.create_pay(message.from_user.id, 'None', date, message.text, "Stars", "active")
    
    stars=int(float(message.text)*1.8)
    prices=[LabeledPrice(label="XTR", amount=stars)]
    await message.answer_invoice(  
        title="Пополнение звёздами",  
        description=f"Пополнение {message.text} RUB за {stars} ⭐️. Оплатите счёт в течении 12 часов.",  
        prices=prices,  
        provider_token="",  
        payload=f"{user_id}_{message.text}",  
        currency="XTR",  
        reply_markup=ikb.pay_stars(stars)
    )
    await state.clear()

@psrouter.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):  
    await pre_checkout_query.answer(ok=True)
    
@psrouter.message(F.successful_payment)
async def success_payment_handler(message: Message):
    payload = message.successful_payment.invoice_payload
    sum = payload.split('_')[1]
    user_id = payload.split('_')[0]
    user_data = await rq.get_user(user_id)
    for user in user_data:
        new_balance = float(user.balance) + float(sum)
        await rq.update_balance(user_id, new_balance)
    await message.answer(f"✅ Платеж успешно получен!", reply_markup=ikb.back())
    print(f"Payment received from user {user_id}")