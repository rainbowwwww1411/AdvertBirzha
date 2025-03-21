from aiogram.fsm.state import State, StatesGroup

class get(StatesGroup):
    name = State()
    sum = State() # CryptoBot in rub
    sum_nowp = State() # Crypto in rub
    sum_stars = State() # Stars in rub
    method = State()
    send_photo = State()
    send_msg = State()
    withdraw_sum = State()
    withdraw_method = State()
    withdraw_crypto = State()
    withdraw_calc_sum = State()
    withdraw_address = State()
    
class BroadcastStates(StatesGroup):
    select_content_type = State()
    receive_text = State()
    receive_photo = State()
    add_button = State()
    receive_button_data = State()
