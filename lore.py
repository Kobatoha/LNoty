from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import EssenceSetting, EssenceCustomSetting, EssenceClanDangeon
from DataBase.RaidBoss import RaidBoss
from DataBase.Feedback import Feedback
from aiocron import crontab
import asyncio
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

lore_path = [
  """
  Баюм - императором Эльморадена возвел Башню для обретения вечной жизни. 
  Дерзость Баюма навлекла на него гнев Эйнхасад. Рассказывают, что Баюм в итоге 
  обрел вечную жизнь и вечную молодость, как сам того хотел, но взамен лишился свободы. 
  Он стал пленником собственной башни и сошел там с ума.
  """,
  """
  
  """
]


@dp.message_handler()
async def echo_lore(message: types.Message):
    await message.answer(lore_part)
