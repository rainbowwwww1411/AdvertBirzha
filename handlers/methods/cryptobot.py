import database.requests as rq
import os
import asyncio
from aiocryptopay import AioCryptoPay, Networks
import inlineKeyboards.profileikb as ikb
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states import get
from ban import BansMiddleware
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from datetime import datetime, timedelta
import time

cryptopay = AioCryptoPay(
    token=os.getenv("CRYPTOPAY_TOKEN"),
    network=Networks.MAIN_NET
)


cbrouter = Router()
cbrouter.callback_query.middleware(BansMiddleware())


@cbrouter.message(get.sum)
async def sum(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        if amount < 100:
            await message.answer("Минимальная сумма пополнения 100 рублей.", reply_markup=await ikb.back())
            return
            
    except ValueError:
        await message.answer("Введите корректную сумму.", reply_markup=await ikb.back())
        return
    
    data = await state.get_data()
    method = data["method"]

    if method == "CryptoBot":
        try:
            
            date = datetime.now()
            
            invoice=await create_invoice(amount, user_id)
            await rq.create_pay(user_id, invoice.invoice_id, date, invoice.amount, "CryptoBot", "active")

            await message.answer(
                f"✅ Счет на {amount} RUB создан!\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "⚠️ Оплатите счет в течение 24 часов\n"
                "Баланс обновится автоматически после платежа",
                reply_markup=await ikb.pay_next(invoice.bot_invoice_url)
            )
        except Exception as e:
            print(e)
            await message.answer("⚠️ Произошла ошибка. Попробуйте позже.", reply_markup=await ikb.back())
    else:
        await message.answer("🚧 Этот метод оплаты временно недоступен", reply_markup=await ikb.back())

    await state.clear()

async def check_payments_task():
    async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        while True:
            try:
                
                invoices = await cryptopay.get_invoices(status='paid')
                
                for invoice in invoices:
                    pays_bool = await rq.check_invoice_id(invoice.invoice_id, "CryptoBot")
                    
                    if pays_bool:
                        pays_data = await rq.get_pay(invoice.invoice_id, "CryptoBot")
                        
                        for pay in pays_data:
                            current_time = datetime.now()
                            date_format = "%Y-%m-%d %H:%M:%S.%f"
                            start_time = datetime.strptime(pay.date, date_format)
                            time_difference = current_time - start_time
                            
                            if time_difference >= timedelta(hours=24):
                                await rq.delete_pay(pay.id)
                            else:
                                if invoice.status == 'paid' and pay.status != 'paid':
                                    user_id = pay.tg_id
                                        
                                    await rq.update_pay(pay.id, 'paid')
                                        
                                    user_data = await rq.get_user(user_id)
                                    for user in user_data:
                                        new_balance = float(user.balance)+float(invoice.amount)
                                        await rq.update_balance(user.tg_id, new_balance)
                                        
                                    await bot.send_message(
                                        chat_id=user_id,
                                        text=f"✅ Платеж на {invoice.amount} RUB успешно получен!",
                                        reply_markup=await ikb.back()
                                    )
                                    print(f"Payment received from user {user_id}")
                            
            except Exception as e:
                print(f"Error checking payments: {e}")
            await asyncio.sleep(5)
            
async def create_invoice(amount, user_id):
    invoice = await cryptopay.create_invoice(
                asset="USDT",
                amount=amount,
                description=f"Пополнение баланса для {user_id}",
                payload=str(user_id),
                allow_comments=False,
                allow_anonymous=False,
                currency_type="fiat",
                fiat="RUB"
            )
    return invoice