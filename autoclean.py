import database.requests as rq
import asyncio
from datetime import datetime, timedelta

async def auto_clean() -> None: # auto clean pays
    while True:
        payments = await rq.get_all_pays()
            
        for payment in payments:
            current_time = datetime.now()
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            start_time = datetime.strptime(payment.date, date_format)
            time_difference = current_time - start_time
            
            if time_difference >= timedelta(hours=12):
                await rq.delete_pay(payment.id)
            await asyncio.sleep(60)
                