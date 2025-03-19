import database.requests as rq

async def check_adv(tg_id):
    response = False
    
    advs_data = await rq.get_advs_buy()
    
    for adv in advs_data:
        if adv.tg_id == tg_id:
            response = True
            break
    
    if response == False:
        advs_data = await rq.get_advs_sell()
        for adv in advs_data:
            if adv.tg_id == tg_id:
                response = True
                break
    
    return response

