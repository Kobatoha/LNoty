from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import EssenceSetting, EssenceBigWar, EssenceCustomSetting
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
    ruoff_setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    bigwar_setting = session.query(EssenceBigWar).filter_by(id_user=user.telegram_id).first()
    custom_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()

    if user and user.server == 'ruoff':
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
        ruoff_setting.festival = False
        ruoff_setting.invasion = False
        ruoff_setting.keber = False

        bigwar_setting.toi = False
        bigwar_setting.gardens = False
        bigwar_setting.pagan = False
        bigwar_setting.antharas = False
        bigwar_setting.hellbound = False
        bigwar_setting.chaotic = False
        bigwar_setting.lilith = False
        bigwar_setting.anakim = False
        bigwar_setting.gord = False
        bigwar_setting.frost = False
        bigwar_setting.loa = False

        custom_setting.dream_day = None
        custom_setting.dream_time = None
        custom_setting.valakas_day = None
        custom_setting.valakas_time = None
        custom_setting.frintezza_day = None
        custom_setting.frintezza_time = None
        custom_setting.gardens_time = None

        print(user.telegram_id, 'отменил все оповещения руоффа')
        session.commit()

    session.close()

    await callback_query.message.answer('Все оповещения отменены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='no_stop'))
async def no_stop(callback_query: types.CallbackQuery):

    await callback_query.message.answer('Отменяем отмену :)')
    await callback_query.answer()
