from aiogram.filters import BaseFilter
from typing import List, Union, Tuple
from aiogram.types import Message, CallbackQuery

class IsAdmin(BaseFilter): # Админка на message
    
    def __init__(self, user_ids: Union[int, List[int], Tuple[int]]) -> None:
        self.user_ids = user_ids
        
    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            return message.from_user.id == self.user_ids
        return message.from_user.id in self.user_ids

class IsAdmin2(BaseFilter): # Админка на callback
    
    def __init__(self, user_ids: Union[int, List[int], Tuple[int]]) -> None:
        self.user_ids = user_ids
        
    async def __call__(self, callback: CallbackQuery) -> bool:
        if isinstance(self.user_ids, int):
            return callback.from_user.id == self.user_ids
        return callback.from_user.id in self.user_ids