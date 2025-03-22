from database.models import async_session, engine
import database.models as md
from sqlalchemy import select, delete, update, exists, func

async def set_user(tg_id, invitefrom):
    async with async_session() as session:
        user = await session.scalar(select(md.User).where(md.User.tg_id == tg_id))
        
        if not user:
            session.add(md.User(tg_id=tg_id, invite_from=invitefrom, name='None', balance='0', deals_count='0', ref_count='0', verified='False'))
            await session.commit()

async def check_user(tg_id: int) -> bool:
    async with async_session() as session:
        stmt = select(exists().where(md.User.tg_id==tg_id))
        bool = await session.scalar(stmt)
        return bool
    
async def check_name(name: str) -> bool:
    async with async_session() as session:
        name_normalized = name.strip().lower()
        stmt = select(exists().where(md.User.name.ilike(name_normalized)))
        bool = await session.scalar(stmt)
        print(bool)
        return bool

async def get_users():
    async with async_session() as session:
        return await session.scalars(select(md.User))

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalars(select(md.User).where(md.User.tg_id==tg_id))
    
async def update_balance(tg_id, balance):
    async with engine.begin() as conn:
        return await conn.execute(update(md.User).where(md.User.tg_id==tg_id).values(balance=balance))

async def get_ban_user(tg_id):
    async with async_session() as session:
        return await session.scalars(select(md.BannedUser).where(md.BannedUser.tg_id==tg_id))

async def upd_name(tg_id, name):
    async with engine.begin() as conn:
        await conn.execute(update(md.User).where(md.User.tg_id==tg_id).values(name=name))
        
async def get_advs_buy():
    async with async_session() as session:
        return await session.scalars(select(md.AdvBuy))
    
async def get_advs_sell():
    async with async_session() as session:
        return await session.scalars(select(md.AdvSell))
    
async def get_deals():
    async with async_session() as session:
        return await session.scalars(select(md.Deal))
    
async def check_user_rating(tg_id: int) -> float:
    async with async_session() as session:
        stmt = select(exists().where(md.Review.to_tg_id==tg_id))
        reviews_bool = await session.scalar(stmt)
        
        if not reviews_bool:
            return 0
        else:
            return await get_user_rating(tg_id)
        
async def get_user_rating(tg_id: int) -> float:
    async with async_session() as session:
        reviews = await session.scalars(select(md.Review).where(md.Review.to_tg_id==tg_id))
        rating_list = list()
        for review in reviews:
            rating_list.append(review.rating)
        all_rate = 0
        for i in rating_list:
            all_rate += int(i)
        rating = all_rate/len(rating_list)
        return rating
    
async def create_pay(tg_id, invoice_id, date, sum, method, status):
    async with async_session() as session:
        session.add(md.pay(tg_id=tg_id, invoice_id=invoice_id, date=date, sum=sum, method=method, status=status))
        await session.commit()
        
async def delete_pay(id):
    async with engine.begin() as conn:
        await conn.execute(delete(md.pay).where(md.pay.id==id))
        
async def update_pay(id, status):
    async with engine.begin() as conn:
        await conn.execute(update(md.pay).where(md.pay.id==id).values(status=status))
        
async def get_pays(method):
    async with async_session() as session:
        return await session.scalars(select(md.pay).where(md.pay.method==method))
    
async def get_all_pays():
    async with async_session() as session:
        return await session.scalars(select(md.pay))
    
async def get_pay(invoice_id, method):
    async with async_session() as session:
        return await session.scalars(select(md.pay).where(md.pay.invoice_id==invoice_id).where(md.pay.method==method))
    
async def check_invoice_id(invoice_id, method: str) -> bool:
    async with async_session() as session:
        stmt = select(exists().where(md.pay.invoice_id==invoice_id).where(md.pay.method==method))
        reviews_bool = await session.scalar(stmt)
        
        if not reviews_bool:
            return False
        else:
            return True
        
async def create_withdraw(tg_id, username: str, sum: str, sum_last: str, currency: str, method: str, address: str) -> None:
    async with async_session() as session:
        session.add(md.withdraw(tg_id=tg_id, username=username, sum=sum, sum_last=sum_last, currency=currency, method=method, status="active", address=address))
        await session.commit()