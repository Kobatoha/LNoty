from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Setting, User
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
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    if user:
        setting.soloraidboss = False
        setting.kuka = False
        setting.loa = False
        setting.frost = False
        setting.fortress = False
        setting.balok = False
        setting.olympiad = False
        setting.hellbound = False
        setting.siege = False
        setting.primetime = False
        setting.purge = False
        setting.event = False
        print(user.telegram_id, 'отменил все оповещения')

        session.commit()
        session.close()

    await callback_query.message.answer('Все оповещения отменены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='no_stop'))
async def no_stop(callback_query: types.CallbackQuery):

    await callback_query.message.answer('Отменяем отмену :)')
    await callback_query.answer()
