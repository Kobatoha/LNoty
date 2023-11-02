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

# PAGAN buttons
inline_pagan_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_pagan')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_pagan')

inline_pagan_buttons.add(button_set, button_remove)


# PAGAN SETTINGS
@dp.message_handler(commands=['bigwar_pagan'])
async def about_bigwar_pagan(message: types.Message):
    await message.answer('[BIGWAR] Языческий Храм 22:00 [пятница] за 15 мин\n',
                         reply_markup=inline_pagan_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_pagan'))
async def set_bigwar_pagan(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.pagan = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Языческом Храме установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_pagan'))
async def remove_bigwar_pagan(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.pagan = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Языческом Храме убрано')
    await callback_query.answer()


async def bigwar_pagan_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.pagan is True:
            await bigwar_pagan_notification(user)
    session.close()


async def bigwar_pagan_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Языческий Храм через 15 минут')
            print(now, '[BIGWAR]', user.id_user, 'получил сообщение о Языческом Храме')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
