from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery
from sqlalchemy import select, func
from database.models import Review
import database.requests as rq
from database.models import async_session
import math

async def generate_keyboard(
    tg_id: int,
    current_page: int = 0,
    items_per_page: int = 10
) -> InlineKeyboardBuilder:
    async with async_session() as session:
        # Получаем общее количество элементов
        total_count = await session.scalar(
            select(func.count(Review.id)).where(Review.to_tg_id == tg_id)
        )
        
        # Получаем элементы для текущей страницы
        offset = current_page * items_per_page
        stmt = (
            select(Review)
            .where(Review.to_tg_id == tg_id)
            .order_by(Review.id)
            .offset(offset)
            .limit(items_per_page)
        )
        result = await session.scalars(stmt)
        reviews = result  # Преобразуем в список

        builder = InlineKeyboardBuilder()
        row = []
        # Добавляем элементы списка
        for review in reviews:
            user_data = await rq.get_user(review.from_tg_id)  # Предполагаем, что возвращает одного пользователя
            for user in user_data:
                builder.add(
                    InlineKeyboardButton(
                        text=f"Имя: {user.name} | Оценка: {review.rating}", 
                        callback_data=f"review_{review.id}"
                    )
                )
                row.append(1)
        # Добавляем кнопки пагинации
        
        if current_page > 0 and (current_page + 1) * items_per_page < total_count:
            builder.add(
                InlineKeyboardButton(
                    text="«", 
                    callback_data=f"page_{current_page - 1}"
                )
            )
            builder.add(
                InlineKeyboardButton(
                    text=f"{current_page+1}/{math.ceil(total_count/10)}", 
                    callback_data=f"dadada"
                ))
            builder.add(
                InlineKeyboardButton(
                    text="»", 
                    callback_data=f"page_{current_page + 1}"
                )
            )
            row.append(3)
        elif current_page > 0:
            builder.add(
                InlineKeyboardButton(
                    text="«", 
                    callback_data=f"page_{current_page - 1}"
                )
            )
            builder.add(
                InlineKeyboardButton(
                    text=f"{current_page+1}/{math.ceil(total_count/10)}", 
                    callback_data=f"dadada"
                ))
            row.append(2)
        elif (current_page + 1) * items_per_page < total_count:
            builder.add(
                InlineKeyboardButton(
                    text=f"{current_page+1}/{math.ceil(total_count/10)}", 
                    callback_data=f"dadada"
                ))
            builder.add(
                InlineKeyboardButton(
                    text="»", 
                    callback_data=f"page_{current_page + 1}"
                )
            )
            row.append(2)
        
        
    
        builder.add(
            InlineKeyboardButton(
                text=f"« Назад", 
                callback_data=f"profile"
                )
            )
        row.append(1)
        return builder.adjust(*row).as_markup()
