import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select, func
from sqlalchemy import delete

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(300))
    balance: Mapped[str] = mapped_column(String(300))
    rating: Mapped[str] = mapped_column(String(300))
    deals_count: Mapped[str] = mapped_column(String(300))
    ref_count: Mapped[str] = mapped_column(String(300))
    invite_from: Mapped[str] = mapped_column(String(300))
    
class Post(Base):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    photo: Mapped[str] = mapped_column(String(300)) #url
    link: Mapped[str] = mapped_column(String(300))
    text: Mapped[str] = mapped_column(String(300))
    
class Deal(Base):
    __tablename__ = 'deals'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    post_id: Mapped[str] = mapped_column(String(300))
    adv_id: Mapped[str] = mapped_column(String(300))
    
class AdvBuy(Base):
    __tablename__ = 'advsbuy'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    post_id: Mapped[str] = mapped_column(String(300))
    theme: Mapped[str] = mapped_column(String(300))
    money: Mapped[str] = mapped_column(String(300))
    costforsub: Mapped[str] = mapped_column(String(300))
    eyes: Mapped[str] = mapped_column(String(300))
    date_from: Mapped[str] = mapped_column(String(300)) # 00.00.0000 00:00
    date_to: Mapped[str] = mapped_column(String(300)) # 00.00.0000 00:00
    time: Mapped[str] = mapped_column(String(300)) # time advertising 00:00
    subscribers: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(300)) # Open/Hidden/Delete
    top: Mapped[str] = mapped_column(String(300)) # Top/NotTop
    description: Mapped[str] = mapped_column(String(500))

class AdvSell(Base):
    __tablename__ = 'advssell'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    theme: Mapped[str] = mapped_column(String(300))
    money: Mapped[str] = mapped_column(String(300))
    costforsub: Mapped[str] = mapped_column(String(300))
    eyes: Mapped[str] = mapped_column(String(300))
    date_from: Mapped[str] = mapped_column(String(300)) # 00.00.0000 00:00
    date_to: Mapped[str] = mapped_column(String(300)) # 00.00.0000 00:00
    time: Mapped[str] = mapped_column(String(300)) # time advertising 00:00
    subscribers: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(300)) # Open/Hidden/Delete
    top: Mapped[str] = mapped_column(String(300)) # Top/NotTop
    description: Mapped[str] = mapped_column(String(500))
    
class pay(Base):
    __tablename__ = 'pays'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    sum: Mapped[str] = mapped_column(String(300))
    currency: Mapped[str] = mapped_column(String(300))
    method: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(300)) # Successful/Unsuccessful
    
class withdraw(Base):
    __tablename__ = 'withdraws'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    sum: Mapped[str] = mapped_column(String(300))
    currency: Mapped[str] = mapped_column(String(300))
    method: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(300)) # Successful/Unsuccessful
    
class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    to_tg_id = mapped_column(BigInteger) # to
    from_tg_id = mapped_column(BigInteger) # from
    rating: Mapped[str] = mapped_column(String(300)) # from 1 to 5
    text: Mapped[str] = mapped_column(String(300))
    
    
Session = async_sessionmaker(bind=engine)
session = Session()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)