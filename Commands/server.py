from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import EssenceSetting, LegacySetting
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

button_ruoff_essence = types.InlineKeyboardButton(text='ruoff essence', callback_data='ruoff_server')
button_ruoff_eva = types.InlineKeyboardButton(text='ruoff eva', callback_data='ruoff_eva')
button_ruoff_legacy = types.InlineKeyboardButton(text='ruoff legacy', callback_data='ruoff_legacy')
button_ruoff_main = types.InlineKeyboardButton(text='ruoff main', callback_data='ruoff_main')
button_kroff = types.InlineKeyboardButton(text='kr official', callback_data='kroff')
button_expanse = types.InlineKeyboardButton(text='expanse', callback_data='expanse')
button_sog = types.InlineKeyboardButton(text='stageofglory', callback_data='stageofglory')
button_imbadon = types.InlineKeyboardButton(text='imbadon', callback_data='imbadon')

inline_server_buttons.add(button_ruoff_essence)
inline_server_buttons.row(button_ruoff_legacy)


@dp.message_handler(commands=['server'])
async def choice_server(message: types.Message):
    await message.answer('Выберите сервер, контент которого хотите отслеживать',
                         reply_markup=inline_server_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_server'))
async def ruoff(callback_query: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        if user:
            user.server = 'ruoff'
            print(user.telegram_id, user.username, 'выбрал оповещения с сервера', user.server)
            session.commit()
            await callback_query.message.answer(
                'Вы выбрали получать оповещения с русских официальных серверов Essence:\n'
                '[ Magenta | Coral | Skyblue | Aqua ]'
            )
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_legacy'))
async def ruoff_legacy(callback_query: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=callback_query.from_user.id).first()
        if user:
            user.server = 'legacy'
            print(user.telegram_id, user.username, 'выбрал оповещения с сервера', user.server)
            session.commit()
            if not setting:
                setting = LegacySetting(id_user=user.telegram_id)
                session.add(setting)
                session.commit()
    await callback_query.message.answer('Вы выбрали получать оповещения с русских официальных серверов Legacy:\n'
                                        '[ Gran Kain | Valakas | Antharas | Lindvior ]')
    await callback_query.answer()
