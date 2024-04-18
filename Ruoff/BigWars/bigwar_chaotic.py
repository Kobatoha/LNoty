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

# CHAOTIC buttons
inline_chaotic_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_chaotic')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_chaotic')

inline_chaotic_buttons.add(button_set, button_remove)


# CHAOTIC SETTINGS
@dp.message_handler(commands=['bigwar_chaotic'])
async def about_bigwar_chaotic(message: types.Message):
    await message.answer('[BIGWAR] Хаотический Босс 20:00 [ежедневно] за 15 минут\n',
                         reply_markup=inline_chaotic_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_chaotic'))
async def set_bigwar_chaotic(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.chaotic = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Хаотический Босс установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_chaotic'))
async def remove_bigwar_chaotic(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.chaotic = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Хаотический Босс убраны')
    await callback_query.answer()


async def bigwar_chaotic_notification_wrapper():

    session = Session()
    users = session.query(EssenceBigWar).all()
    for user in users:
        if user.chaotic is True:
            await bigwar_chaotic_notification(user)
    session.close()


async def bigwar_chaotic_notification(user: EssenceBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '19:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Хаотический Босс через 15 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Хаотический Босс')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
