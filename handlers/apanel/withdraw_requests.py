import asyncio
import re
from states import WithdrawStates
import database.requests as rq
import inlineKeyboards.adminikb as ikb
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from function.ban import BansMiddleware
from function.admin import IsAdmin2
from settings import ADMINS
from datetime import datetime

chwrouter = Router()
chwrouter.callback_query.middleware(BansMiddleware())

@chwrouter.callback_query(F.data.startswith("check_withdraw_"), IsAdmin2(ADMINS))
async def check_withdraw(callback: CallbackQuery):
    withdraw_id = callback.data.split('_')[2]
    withdraw_data = await rq.get_withdraw(withdraw_id)
    for w in withdraw_data:
        await callback.message.edit_text(f"#{w.id}\nid | username: {w.tg_id} | @{w.username}\n\nБез ком | с ком: {w.sum} | {w.sum_last}\n\nМетод: {w.method}\nВалюта: {w.currency}\nАдрес: {w.address}", reply_markup=await ikb.check_withdraw(w.id))
        
@chwrouter.callback_query(F.data.startswith("awithdraw_"), IsAdmin2(ADMINS))
async def awithdraw(callback: CallbackQuery):
    action = callback.data.split('_')[1]
    withdraw_id = callback.data.split('_')[2]
    
    if action == "approve":
        await callback.message.edit_text("Прикрепить сообщение к выводу?", reply_markup=await ikb.next_withdraw_approve(withdraw_id))
    else:
        await callback.message.edit_text("Прикрепить сообщение к отказу?", reply_markup=await ikb.next_withdraw_decline(withdraw_id))
        
@chwrouter.callback_query(F.data.startswith("awithdrawapprove_"), IsAdmin2(ADMINS))
async def awithdrawapprove(callback: CallbackQuery, bot: Bot, state: FSMContext):
    action = callback.data.split('_')[1]
    withdraw_id = callback.data.split('_')[2]
    if action == "yes":
        await callback.message.edit_text("Отправьте сообщение:")
        await state.update_data(withdraw_id=withdraw_id)
        await state.set_state(WithdrawStates.message_text_approve)
    else:
        await rq.update_status_withdraw(withdraw_id, "successful")
        await callback.message.edit_text("Вы подтвердили вывод", reply_markup=await ikb.to_withdraws())
        w_data = await rq.get_withdraw(withdraw_id)
        print(1)
        for w in w_data:
            print(2)
            await bot.send_message(chat_id=w.tg_id, text="✅ Вывод был успешно выполнен!", reply_markup=await ikb.delete_msg())

@chwrouter.message(WithdrawStates.message_text_approve)
async def awithdrawapprove_message_text(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await rq.update_status_withdraw(data['withdraw_id'], "successful")
    await message.answer("Вы подтвердили вывод", reply_markup=await ikb.to_withdraws())
    w_data = await rq.get_withdraw(data['withdraw_id'])
    for w in w_data:
        await bot.send_message(chat_id=w.tg_id, text=f"✅ Вывод был успешно выполнен!\n\nСообщение от администрации: {message.text}", reply_markup=await ikb.delete_msg())

@chwrouter.callback_query(F.data.startswith("awithdrawdecline_"), IsAdmin2(ADMINS))
async def awithdrawdecline(callback: CallbackQuery, bot: Bot, state: FSMContext):
    action = callback.data.split('_')[1]
    withdraw_id = callback.data.split('_')[2]
    if action == "yes":
        await callback.message.edit_text("Отправьте сообщение:")
        await state.update_data(withdraw_id=withdraw_id)
        await state.set_state(WithdrawStates.message_text_decline)
    else:
        await rq.update_status_withdraw(withdraw_id, "unsuccessful")
        await callback.message.edit_text("Вы отклонили вывод", reply_markup=await ikb.to_withdraws())
        w_data = await rq.get_withdraw(withdraw_id)
        for w in w_data:
            user_data = await rq.get_user(w.tg_id)
            for user in user_data:
                new_balance = float(user.balance) + float(w.sum)
                await rq.update_balance(w.tg_id, new_balance)
            await bot.send_message(chat_id=w.tg_id, text="⛔️ Вывод был отклонён по решению администрации. Средства были возвращены.\n\nПовторите попытку или обратитесь к тех. поддержке за дополнительной информацией.", reply_markup=await ikb.withdraw_msg())

@chwrouter.message(WithdrawStates.message_text_decline)
async def awithdrawapprove_message_text(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await rq.update_status_withdraw(data['withdraw_id'], "unsuccessful")
    await message.answer("Вы отклонили вывод", reply_markup=await ikb.to_withdraws())
    w_data = await rq.get_withdraw(data['withdraw_id'])
    for w in w_data:
        user_data = await rq.get_user(w.tg_id)
        for user in user_data:
            new_balance = float(user.balance) + float(w.sum)
            await rq.update_balance(w.tg_id, new_balance)
        await bot.send_message(chat_id=w.tg_id, text=f"⛔️ Вывод был отклонён по решению администрации. Средства были возвращены.\n\nПовторите попытку или обратитесь к тех. поддержке за дополнительной информацией.\n\nСообщение от администрации: {message.text}", reply_markup=await ikb.withdraw_msg())