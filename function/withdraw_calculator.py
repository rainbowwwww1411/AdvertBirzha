from check_ton_price import CoinGeckoAPI
from settings import default_commission

class PaymentCalculator:
    def __init__(self, coin_gecko: CoinGeckoAPI):
        self.coin_gecko = coin_gecko
        self.default_commission = default_commission

        self.method_commissions = {
            'TON': {'percent': 0, 'fixed': 0},
            'CryptoBot': {'percent': 0, 'fixed': 0},
            'Карты РФ': {'percent': 0.05, 'fixed': 50},
            'СБП': {'percent': 0, 'fixed': 0}
        }

        self.min_amounts = {
            'TON': 500,
            'CryptoBot': 100,
            'Карты РФ': 1000,
            'СБП': 500
        }

        self.network_fees = {
            'TON': 0.1
        }

    def calculate(self, method: str, amount: float) -> float:
        if method not in self.method_commissions:
            return "Неверный метод выплаты"

        if amount < self.min_amounts[method]:
            return f"Минимальная сумма для {method}: {self.min_amounts[method]} руб. "
            

        commission = self.method_commissions[method]

        after_default = amount * (1 - self.default_commission)
        after_percent = after_default * (1 - commission['percent'])
        after_fixed = after_percent - commission['fixed']

        if after_fixed < 0:
            return 0.0

        if method == 'TON':
            ton_price = self.coin_gecko.get_ton_price()
            if ton_price is None:
                return "Вывод в TON недоступен. Попробуйте позже."

            ton_amount = after_fixed / ton_price
            ton_amount_after_fee = ton_amount - self.network_fees['TON']

            if ton_amount_after_fee < 0:
                return 0.0

            return round(ton_amount_after_fee * ton_price, 2)

        return max(round(after_fixed, 2), 0.0)