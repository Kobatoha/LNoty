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

# LOA buttons
inline_loa_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_loa')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_loa')

inline_loa_buttons.add(button_set, button_remove)


# LOA SETTINGS
@dp.message_handler(commands=['bigwar_loa'])
async def about_bigwar_loa(message: types.Message):
    await message.answer('[BIGWAR] Логово Антараса 22:00 [понедельник, среда] за 15 минут\n',
                         reply_markup=inline_loa_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_loa'))
async def set_bigwar_loa(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.loa = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение о Логово Антараса установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_loa'))
async def remove_bigwar_loa(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.loa = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещения о Логово Антараса убраны')
    await callback_query.answer()


async def bigwar_loa_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.loa is True:
            await bigwar_loa_notification(user)
    session.close()


async def bigwar_loa_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Логово Антараса через 15 минут')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Логово Антараса')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
