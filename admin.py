from aiogram.filters import BaseFilter
from typing import List, Union
from aiogram.types import Message, CallbackQuery

# Админка на message
class IsAdmin(BaseFilter):
    
    def __init__(self, user_ids: Union[int, List[int]]) -> None:
        self.user_ids = user_ids
        
    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            return message.from_user.id == self.user_ids
        return message.from_user.id in self.user_ids

# Админка на callback
class IsAdmin2(BaseFilter):
    
    def __init__(self, user_ids: Union[int, List[int]]) -> None:
        self.user_ids = user_ids
        
    async def __call__(self, callback: CallbackQuery) -> bool:
        if isinstance(self.user_ids, int):
            return callback.from_user.id == self.user_ids
        return callback.from_user.id in self.user_ids