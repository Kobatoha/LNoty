from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import Setting
from aiocron import crontab
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


# server buttons
inline_server_buttons = types.InlineKeyboardMarkup()

button_ruoff = types.InlineKeyboardButton(text='ru official', callback_data='ruoff_server')
button_kroff = types.InlineKeyboardButton(text='ru official', callback_data='kroff')
button_expanse = types.InlineKeyboardButton(text='expanse', callback_data='expanse')
button_sog = types.InlineKeyboardButton(text='stageofglory', callback_data='stageofglory')
button_imbadon = types.InlineKeyboardButton(text='imbadon', callback_data='imbadon')

inline_server_buttons.add(button_ruoff)
#inline_server_buttons.row(button_expanse)


@dp.message_handler(commands=['server'])
async def choice_server(message: types.Message):
    await message.answer('Выберите сервер, контент которого хотите отслеживать',
                         reply_markup=inline_server_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_server'))
async def ruoff(callback_query: types.CallbackQuery):
    session = Session()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    if user:
        user.server = 'ruoff'
        print(user.telegram_id, user.username, 'выбрал оповещения с сервера', user.server)
        session.commit()
        session.close()
        await callback_query.message.answer('Вы выбрали получать оповещения с русских официальных серверов')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='expanse'))
async def expanse(callback_query: types.CallbackQuery):
    session = Session()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(telegram_id=callback_query.from_user.id).first()
    if user:
        user.server = 'expanse'
        print(user.telegram_id, user.username, 'выбрал оповещения с сервера', user.server)
        session.commit()
        if not setting:
            setting = Expanse(id_user=user.telegram_id)
            session.add(setting)
            session.commit()
            session.close()
    await callback_query.message.answer('Вы выбрали получать оповещения с сервера Expanse')
    await callback_query.answer()
