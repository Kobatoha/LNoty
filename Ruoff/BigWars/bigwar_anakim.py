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

# ANAKIM buttons
inline_anakim_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_anakim')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_anakim')

inline_anakim_buttons.add(button_set, button_remove)


# ANAKIM SETTINGS
@dp.message_handler(commands=['bigwar_anakim'])
async def about_bigwar_anakim(message: types.Message):
    await message.answer('[BIGWAR] Анаким 19:00 [вторник, пятница] за 15 минут\n',
                         reply_markup=inline_anakim_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_anakim'))
async def set_bigwar_anakim(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.anakim = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Анаким установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_anakim'))
async def remove_bigwar_anakim(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.anakim = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Анаким убраны')
    await callback_query.answer()


async def bigwar_anakim_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.anakim is True:
            await bigwar_anakim_notification(user)
    session.close()


async def bigwar_anakim_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '18:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Анаким через 15 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Анаким')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
