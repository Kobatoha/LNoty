from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer('Приветствую :)'
                         ' Я - Kobatoha, и я создала этого бота для вас, мои маленькие любители l2essence!'
                         ' Мы поможем не пропустить игровые активности.\n'
                         'Бот создан на добровольных началах, поэтому он свободен и независим.'
                         ' Есть идеи и предложения по улучшению бота? Велком - kobatoha@yandex.ru\n'
                         'Или ищите меня на Lavender под ником vsenaprasno')
