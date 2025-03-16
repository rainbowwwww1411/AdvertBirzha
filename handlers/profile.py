import database.requests as rq
import os
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import get

prouter = Router()