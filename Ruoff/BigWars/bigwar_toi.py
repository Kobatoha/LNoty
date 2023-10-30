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

# TOWER OF INSOLENCE buttons
inline_toi_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_toi')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_toi')

inline_toi_buttons.add(button_set, button_remove)


# TOWER OF INSOLENCE SETTINGS
@dp.message_handler(commands=['bigwar_toi'])
async def about_bigwar_toi(message: types.Message):
    await message.answer('[BIGWAR] Башня Дерзости 15:00 | 21:00 [ежедневно]\n'
                         'Уведомления за 20 минут - расставить точки и раздуплить нераздупляемое',
                         reply_markup=inline_toi_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_toi'))
async def set_bigwar_toi(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.toi = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Башне Дерзости установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_toi'))
async def remove_bigwar_toi(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.toi = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Башне Дерзости убраны')
    await callback_query.answer()


async def bigwar_toi_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.toi is True:
            await bigwar_toi_notification(user)
    session.close()


async def bigwar_toi_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '14:40' or now == '20:40':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Башня Дерзости через 20 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Башня Дерзости')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
