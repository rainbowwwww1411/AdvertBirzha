from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
import time
import asyncio

# Конфигурация
CAPTCHA_SIZE = 6  # Количество вариантов ответов
TIMEOUT = 300  # 5 минут хранения ответов (в секундах)

# База эмодзи по категориям (уникальные)
emoji_db = {
    "Смайл": ["😀", "😇", "🥶", "🤖", "👾", "💀", "👻", "🤡", "💩", "🎃"],
    "Животное": ["🐶", "🐱", "🦁", "🐴", "🦄", "🐸", "🦋", "🐢", "🐳", "🦑"],
    "Еду": ["🍎", "🍕", "🥑", "🍔", "🍣", "🍩", "🥦", "🍗", "🥞", "🍜"],
    "Профессию": ["👮", "👷", "💂", "👨‍🏭", "🧑‍🔧", "👩‍🚒", "👩‍🍳", "👩‍🏫", "🧑‍💻", "🧑‍🚀"],
    "Предмет": ["⌚", "⏰", "💡", "📱", "💻", "🔑", "🎁", "🧸", "📚", "🏺"]
}

# Генератор быстрого доступа
all_emoji = [
    (category_name, emoji) 
    for category_name, emojis in emoji_db.items() 
    for emoji in emojis
]

category_map = {
    emoji: category_name 
    for category_name, emojis in emoji_db.items() 
    for emoji in emojis
}

# Хранилище ответов {user_id: (correct_emoji, timestamp)}
captcha_store = {}

# Middleware для очистки устаревших капч
async def captcha_cleaner():
    while True:
        now = time.time()
        expired = [k for k, v in captcha_store.items() if now - v[1] > TIMEOUT]
        for key in expired:
            del captcha_store[key]
        await asyncio.sleep(60)


