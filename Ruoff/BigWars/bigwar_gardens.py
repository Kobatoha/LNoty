import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from DataBase.Base import Base
from DataBase.Ruoff import RuoffBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN, test_token
from aiogram.utils.exceptions import BotBlocked
from aiocron import crontab
from Commands.bigwar import bigwar_menu_text


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# FORGOTTEN GARDENS buttons
inline_gardens_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_gardens')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_gardens')

inline_gardens_buttons.add(button_set, button_remove)


# FORGOTTEN GARDENS SETTINGS
@dp.message_handler(commands=['bigwar_gardens'])
async def about_bigwar_gardens(message: types.Message):
    await message.answer('[BIGWAR] Забытые Сады 23:00 [ежедневно]\n',
                         reply_markup=inline_gardens_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_gardens'))
async def set_bigwar_gardens(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.gardens = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Забытых Садах установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_gardens'))
async def remove_bigwar_gardens(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.gardens = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Забытых Садах убрано')
    await callback_query.answer()


async def bigwar_gardens_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.gardens is True:
            await bigwar_gardens_notification(user)
    session.close()


async def bigwar_gardens_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '22:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Забытые Сады через 15 минут')
            print(now, '[BIGWAR]', user.id_user, 'получил сообщение о  Забытых Садах')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
