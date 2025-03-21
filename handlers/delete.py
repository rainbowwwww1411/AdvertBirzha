from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from function.antiflood import AntiFloodMiddleware

drouter = Router()
drouter.callback_query.middleware(AntiFloodMiddleware())

@drouter.callback_query(F.data=='delete')
async def delete(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)