from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting
from DataBase.Expanse import Expanse
from aiocron import crontab
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


# stop buttons
inline_stop_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Да', callback_data='yes_stop')
b2 = types.InlineKeyboardButton(text='Нет', callback_data='no_stop')

inline_stop_buttons.add(b1, b2)


@dp.message_handler(commands=['Stop'])
async def stop(message: types.Message):
    await message.answer('Вы уверены, что хотите отменить все установленные оповещения?',
                         reply_markup=inline_stop_buttons)


@dp.callback_query_handler(filters.Text(contains='yes_stop'))
async def yes_stop(callback_query: types.CallbackQuery):
    session = Session()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    ruoff_setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    expanse_setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()

    if user and user.server == 'ruoff':
        ruoff_setting.soloraidboss = False
        ruoff_setting.kuka = False
        ruoff_setting.loa = False
        ruoff_setting.frost = False
        ruoff_setting.fortress = False
        ruoff_setting.balok = False
        ruoff_setting.olympiad = False
        ruoff_setting.hellbound = False
        ruoff_setting.siege = False
        ruoff_setting.primetime = False
        ruoff_setting.purge = False
        ruoff_setting.event = False
        ruoff_setting.calendar = False
        print(user.telegram_id, 'отменил все оповещения руоффа')
        session.commit()

    elif user and user.server == 'expanse':
        expanse_setting.soloraidboss = False
        expanse_setting.loa = False
        expanse_setting.frost = False
        expanse_setting.balok = False
        expanse_setting.olympiad = False
        expanse_setting.hellbound = False
        expanse_setting.siege = False
        expanse_setting.fulltime = False
        print(user.telegram_id, 'отменил все оповещения expanse')
        session.commit()

    session.close()

    await callback_query.message.answer('Все оповещения отменены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='no_stop'))
async def no_stop(callback_query: types.CallbackQuery):

    await callback_query.message.answer('Отменяем отмену :)')
    await callback_query.answer()
