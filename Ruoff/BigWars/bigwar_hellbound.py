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

# HELLBOUND buttons
inline_hellbound_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_hellbound')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_hellbound')

inline_hellbound_buttons.add(button_set, button_remove)


# HELLBOUND SETTINGS
@dp.message_handler(commands=['bigwar_hellbound'])
async def about_bigwar_hellbound(message: types.Message):
    await message.answer('[BIGWAR] Остров Ада 11:00 | 21:00 | 22:00 [суббота] за 15 минут\n',
                         reply_markup=inline_hellbound_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_hellbound'))
async def set_bigwar_hellbound(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.hellbound = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Остров Ада установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_hellbound'))
async def remove_bigwar_hellbound(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.hellbound = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Остров Ада убраны')
    await callback_query.answer()


async def bigwar_hellbound_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.hellbound is True:
            await bigwar_hellbound_notification(user)
    session.close()


async def bigwar_hellbound_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '10:45' or now == '20:45' or now == '21:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Остров Ада через 15 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Остров Ада')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
