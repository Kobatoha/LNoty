import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.Base import Base
from DataBase.Ruoff import RuoffBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# FROST buttons
inline_frost_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_frost')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_frost')

inline_frost_buttons.add(button_set, button_remove)


# FROST SETTINGS
@dp.message_handler(commands=['bigwar_frost'])
async def about_bigwar_frost(message: types.Message):
    await message.answer('[BIGWAR] Замок Монарха Льда 21:30 | 22:00 [вторник, четверг] за 15 минут\n',
                         reply_markup=inline_frost_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_frost'))
async def set_bigwar_frost(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.frost = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Замок монарха Льда установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_frost'))
async def remove_bigwar_frost(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.frost = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Замок монарха Льда убраны')
    await callback_query.answer()


async def bigwar_frost_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.frost is True:
            await bigwar_frost_notification(user)
    session.close()


async def bigwar_frost_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '20:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Горд через 15 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Горд')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
