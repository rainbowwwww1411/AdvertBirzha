from database.models import async_session, engine
import database.models as md
from sqlalchemy import select, delete, update, or_, and_, exists

async def set_user(tg_id, invitefrom):
    async with async_session() as session:
        user = await session.scalar(select(md.User).where(md.User.tg_id == tg_id))
        
        if not user:
            session.add(md.User(tg_id=tg_id, invite_from=invitefrom, name='None', balance='0', deals_count='0', ref_count='0'))
            await session.commit()
            
async def get_users():
    async with async_session() as session:
        return await session.scalars(select(md.User))

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalars(select(md.User).where(md.User.tg_id==tg_id))

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