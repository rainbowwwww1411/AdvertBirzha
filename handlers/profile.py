import database.requests as rq
import os
from aiocryptopay import AioCryptoPay, Networks
import inlineKeyboards.profileikb as ikb
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from states import get
from ban import BansMiddleware

cryptopay = AioCryptoPay(
    token=os.getenv("CRYPTOPAY_TOKEN"),
    network=Networks.MAIN_NET
)

prouter = Router()
prouter.callback_query.middleware(BansMiddleware())

@prouter.callback_query(F.data=="profile")
async def profile(callback: CallbackQuery):
    user_data = await rq.get_user(callback.from_user.id)
    rating = round(await rq.check_user_rating(callback.from_user.id), 2)
    for user in user_data:
        await callback.message.edit_text(f"""📋 Профиль
                                         
🙋🏻‍♂️ Ваш ID: <code>{callback.from_user.id}</code>

🏦 Ваш баланс: <code>{user.balance}</code>
⭐️ Ваша оценка: <code>{rating}</code>

🤝 Количество сделок: <code>{user.deals_count}</code>
👥 Количество рефералов: <code>{user.ref_count}</code>""", reply_markup=await ikb.profile(callback.from_user.id, user.balance))
        
@prouter.callback_query(F.data=="referal_system")
async def referal_system(callback: CallbackQuery, bot: Bot):
    link = await create_start_link(bot,str(callback.from_user.id), encode=True)
    await callback.message.edit_text(f"🔗 Ваша реферальная ссылка: <code>{link}</code>\n\nВы получите 1% за выводы реферала.", reply_markup=await ikb.back())
    
@prouter.callback_query(F.data=="top_up_balance")
async def top_up_balance(callback: CallbackQuery):
    await callback.message.edit_text("Выберите метод пополнения:", reply_markup=await ikb.pay_methods())

@prouter.callback_query(F.data.startswith("pay_"))
async def pay(callback: CallbackQuery, state: FSMContext):
    method = callback.data.split('_')[1]
    await state.update_data(method=method)
    if method=="CryptoBot":
        await callback.message.edit_text("Введите сумму для оплаты в рублях (минимально 100руб):", reply_markup=await ikb.back())
        await state.set_state(get.sum)
    elif method=="NowPayments":
        await callback.message.edit_text("Введите сумму для оплаты в рублях (минимально 500руб):", reply_markup=await ikb.back())
        await state.set_state(get.sum_nowp)
    elif method=="Stars":
        await callback.message.edit_text("Введите сумму для оплаты в рублях (минимально 100руб):", reply_markup=await ikb.back())
        await state.set_state(get.sum_stars)






