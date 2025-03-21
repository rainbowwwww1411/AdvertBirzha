import schedule
import time
import requests
from threading import Thread, Lock

class CoinGeckoAPI:
    def __init__(self):
        self.ton_price = None
        self.lock = Lock()
        self._stop_event = False

        self.update_ton_price()

        schedule.every(1).minutes.do(self.update_ton_price)
        self.scheduler_thread = Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()

    def run_scheduler(self):
        while not self._stop_event:
            schedule.run_pending()
            time.sleep(1)

    def update_ton_price(self):
        try:
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'the-open-network', 'vs_currencies': 'rub'}
            )
            data = response.json()
            with self.lock:
                self.ton_price = data['the-open-network']['rub']
        except Exception as e:
            print(f"Ошибка обновления курса TON: {e}")

    def get_ton_price(self):
        with self.lock:
            return self.ton_price

    def stop(self):
        self._stop_event = True
        self.scheduler_thread.join()