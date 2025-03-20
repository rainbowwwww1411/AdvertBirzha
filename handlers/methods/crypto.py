import requests, json
import database.requests as rq
import os
import asyncio
import inlineKeyboards.cryptoikb as ikb
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states import get
from ban import BansMiddleware
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from datetime import datetime

nprouter = Router()
nprouter.callback_query.middleware(BansMiddleware())


@nprouter.message(get.sum_nowp)
async def sum_nowp(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount < 500:
            await message.answer("Минимальная сумма пополнения 500 рублей.", reply_markup=await ikb.back())
            return
            
    except ValueError:
        await message.answer("Введите корректную сумму.", reply_markup=await ikb.back())
        return
    
    await state.update_data(sum_nowp=message.text)
    await message.answer("Выберите криптовалюту для пополнения:", reply_markup=await ikb.payn_crypto())

@nprouter.callback_query(F.data.startswith("payn_"))
async def sum_nowp(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.from_user.id
    crypto=callback.data.split('_')[1]
    data = await state.get_data()

    try:
        date = datetime.now()
        invoice=await create_payments(user_id, crypto, data["sum_nowp"])
        await rq.create_pay(user_id, invoice[0], date, data["sum_nowp"], "Crypto", "waiting")
        
        await callback.message.edit_text(
            f"✅ Отправьте <code>{invoice[2]}</code> {crypto} на адрес <code>{invoice[1]}</code>\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
            "⚠️ Время на оплату 12 часов\n"
            "<b>Баланс пополнится автоматически после платежа</b>"
        )
    except Exception as e:
        print(e)
        await callback.message.edit_text("⚠️ Произошла ошибка. Попробуйте позже.", reply_markup=await ikb.back())
    await state.clear()


async def check_payments_task_np() -> None: # Auto check complete pays
    async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        while True:
            try:
                
                payments = await rq.get_pays("Crypto")
                
                for payment in payments:
                    
                    status = await get_payment(payment.invoice_id)
                    if status == 'finished' and payment.status != 'finished':
                        user_id = payment.tg_id
                            
                        await rq.update_pay(payment.id, 'finished')
                            
                        user_data = await rq.get_user(user_id)
                        for user in user_data:
                            new_balance = float(user.balance)+float(payment.sum)
                            await rq.update_balance(user.tg_id, new_balance)
                                
                        await bot.send_message(
                        chat_id=user_id,
                            text=f"✅ Платеж на {payment.sum} RUB успешно получен!",
                            reply_markup=await ikb.back()
                            )
                        print(f"Payment received from user {user_id}")
                            
            except Exception as e:
                print(f"Error checking payments: {e}")
            await asyncio.sleep(10)


async def create_payments(id, crypto, price_rub):

    url = "https://api.nowpayments.io/v1/payment"

    payload = json.dumps({
      "price_amount": price_rub,
      "price_currency": "RUB",
      "pay_currency": crypto,
      "ipn_callback_url": "https://nowpayments.io",
      "order_id": id,
      "order_description": f"Сделка #{id}"
    })
    headers = {
      'x-api-key': os.getenv("NOWPAYMENTS_TOKEN"),
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    data = response.json()
    print(data)
    return data["payment_id"], data["pay_address"], data["pay_amount"]

# проверка статуса платежа
async def get_payment(id):

    url = f"https://api.nowpayments.io/v1/payment/{id}"

    payload={}
    headers = {
        'x-api-key': os.getenv("NOWPAYMENTS_TOKEN")
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data["payment_status"]


