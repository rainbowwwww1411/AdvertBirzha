import database.requests as rq
import inlineKeyboards.withdrawikb as ikb
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import get
from ban import BansMiddleware
from settings import commission
from check_ton_price import CoinGeckoAPI
from withdraw_calculator import PaymentCalculator

wrouter = Router()
wrouter.callback_query.middleware(BansMiddleware())

cg = CoinGeckoAPI()
calculator = PaymentCalculator(cg)

@wrouter.callback_query(F.data=="withdraw_balance")
async def withdraw(callback: CallbackQuery):
    await callback.message.edit_text("Выберите способ вывода:", reply_markup=await ikb.withdraw_methods())
    
@wrouter.callback_query(F.data.startswith("withdraw_method_"))
async def withdraw(callback: CallbackQuery, state: FSMContext):
    withdraw_method=callback.data.split('_')[2]
    await state.update_data(withdraw_method=withdraw_method)
    if withdraw_method == "CryptoBot":
        await callback.message.edit_text(f"Выберите криптовалюту для вывода:", reply_markup=await ikb.withdraw_choice())
    else:
        await callback.message.edit_text(f"Введите сумму вывода в RUB\nНа вывод действует комиссия {commission}% и возможна комиссия банка/сети. Подробнее про комиссии /rules.", reply_markup=await ikb.to_withdraw())
        await state.set_state(get.withdraw_sum)
    
@wrouter.message(get.withdraw_sum)
async def withdraw_sum(message: Message, state: FSMContext):
    data = await state.get_data()
    user_data =await rq.get_user(message.from_user.id)
    try:
        withdraw_sum = float(message.text)
        if withdraw_sum < int(calculator.min_amounts[data['withdraw_method']]):
            await message.answer(f"Минимальная сумма для данного метода составляет {calculator.min_amounts[data['withdraw_method']]} рублей. Введите сумму равную или большую.", reply_markup=await ikb.to_withdraw())
            await state.set_state(get.withdraw_sum)
            return
    except Exception as e:
        print(e)
        await message.answer(f"Введите число!", reply_markup=await ikb.to_withdraw())
        await state.set_state(get.withdraw_sum)
        return
    
    for user in user_data:
        if float(user.balance) < float(message.text):
            await message.answer("На вашем балансе недостаточно средств.", reply_markup=await ikb.to_withdraw())
        else:
            result = calculator.calculate(data['withdraw_method'], withdraw_sum)
            await state.update_data(withdraw_sum=message.text)
            await state.update_data(withdraw_calc_sum=result)
            await message.answer(f"Сумма вывода с учётом комиссии сервиса и метода {result:.2f}. Продолжить?", reply_markup=await ikb.withdraw_next())

@wrouter.callback_query(F.data.startswith("withdraw_choice_"))
async def withdraw_choice(callback: CallbackQuery, state: FSMContext):
    withdraw_crypto = callback.data.split('_')[2]
    await state.update_data(withdraw_crypto=withdraw_crypto)
    await state.set_state(get.withdraw_sum)
    await callback.message.edit_text(f"Введите сумму вывода в RUB.\nНа вывод действует комиссия сервиса {commission}%. Подробнее про комиссии /rules.", reply_markup=await ikb.to_withdraw())

@wrouter.callback_query(F.data=="withdraw_next")
async def withdraw_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['withdraw_method'] == "CryptoBot":
        user_data = await rq.get_user(callback.from_user.id)
        for user in user_data:
            new_balance = float(user.balance) - float(data['withdraw_sum'])
            await rq.update_balance(callback.from_user.id, new_balance)
        await rq.create_withdraw(callback.from_user.id, callback.from_user.username, data['withdraw_sum'], data['withdraw_crypto'], data['withdraw_method'], 'CryptoBot')
        await callback.message.edit_text("⌛️ Заявка на вывод добавлена.\nОжидайте, средства обычно выводятся до 24 часов. Бот вам отправит чек.", reply_markup=await ikb.back())
        await state.clear()
    elif data['withdraw_method'] == "TON":
        await state.set_state(get.withdraw_address)
        await state.update_data(withdraw_crypto='TON')
        await callback.message.edit_text("Введите ваш адрес TON:", reply_markup=await ikb.to_withdraw())
    elif data['withdraw_method'] == "Карты РФ":
        await state.update_data(withdraw_crypto='RUB')
        await state.set_state(get.withdraw_address)
        await callback.message.edit_text("Введите ваши реквизиты:", reply_markup=await ikb.to_withdraw())
    elif data['withdraw_method'] == "СБП":
        await state.update_data(withdraw_crypto='RUB')
        await state.set_state(get.withdraw_address)
        await callback.message.edit_text("Введите ваши реквизиты и банк. Пример: +79998887766 - Сбербанк.", reply_markup=await ikb.to_withdraw())
        
@wrouter.message(get.withdraw_address)
async def withdraw_address(message: Message, state: FSMContext):
    data = await state.get_data()
    user_data = await rq.get_user(message.from_user.id)
    for user in user_data:
        new_balance = float(user.balance) - float(data['withdraw_sum'])
        await rq.update_balance(message.from_user.id, new_balance)
    await rq.create_withdraw(message.from_user.id, message.from_user.username, data['withdraw_sum'], data['withdraw_crypto'], data['withdraw_method'], message.text)
    await message.answer("⌛️ Заявка на вывод добавлена.\nОжидайте, средства обычно выводятся до 24 часов.", reply_markup=await ikb.back())
    await state.clear()