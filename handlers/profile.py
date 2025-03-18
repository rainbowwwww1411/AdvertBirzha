import database.requests as rq
import os
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states import get
from ban import BansMiddleware

prouter = Router()
prouter.callback_query.middleware(BansMiddleware())

@prouter.callback_query(F.data=="profile")
async def profile(callback: CallbackQuery)