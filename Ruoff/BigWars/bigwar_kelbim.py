import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.Base import Base
from DataBase.Ruoff import EssenceBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# KELBIM buttons
inline_kelbim_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_kelbim')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_kelbim')

inline_kelbim_buttons.add(button_set, button_remove)


# KELBIM SETTINGS
@dp.message_handler(commands=['bigwar_kelbim'])
async def about_bigwar_kelbim(message: types.Message):
    await message.answer('[BIGWAR] Крепость Кельбима 22:00 [пятница] за 15 мин\n',
                         reply_markup=inline_kelbim_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_kelbim'))
async def set_bigwar_kelbim(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.kelbim = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Крепость Кельбима установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_kelbim'))
async def remove_bigwar_kelbim(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.kelbim = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Крепость Кельбима убрано')
    await callback_query.answer()


async def bigwar_kelbim_notification_wrapper():

    session = Session()
    users = session.query(EssenceBigWar).all()
    for user in users:
        if user.kelbim is True:
            await bigwar_kelbim_notification(user)
    session.close()


async def bigwar_kelbim_notification(user: EssenceBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Крепость Кельбима через 15 минут')
            print(now, '[BIGWAR]', user.id_user, 'получил сообщение о Крепость Кельбима')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
