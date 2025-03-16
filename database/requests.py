from database.models import async_session, engine
import database.models as md
from sqlalchemy import select, delete, update, or_, and_

async def set_user(tg_id, invitefrom):
    async with async_session() as session:
        user = await session.scalar(select(md.User).where(md.User.tg_id == tg_id))
        
        if not user:
            session.add(md.User(tg_id=tg_id, invite_from=invitefrom, name='None', balance='0', rating='0', deals_count='0', ref_count='0'))
            await session.commit()
            
async def get_users():
    async with async_session() as session:
        return await session.scalars(select(md.User))

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalars(select(md.User).where(md.User.tg_id==tg_id))
    
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