from aiogram.fsm.state import State, StatesGroup

class get(StatesGroup):
    name = State()
    sum = State() # CryptoBot in rub
    sum_nowp = State() # Crypto in rub
    sum_stars = State() # Stars in rub
    method = State()