import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# siege giran buttons
inline_siege_buttons = types.InlineKeyboardMarkup()

b18 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_setsiege')
b19 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_removesiege')

inline_siege_buttons.add(b18, b19)


# GIRAN`S SIEGE SETTINGS
@dp.message_handler(commands=['siege'])
async def about_siege(message: types.Message):
    await message.answer('Осада Замка Гиран приходит в воскресенье с 20:30 до 21:00.',
                         reply_markup=inline_siege_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_setsiege'))
async def set_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.siege = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_removesiege'))
async def remove_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.siege = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана убрано')
    await callback_query.answer()


async def siege_notification_wrapper():
    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        if setting.siege is True:
            await siege_notification(user)
    session.close()


async def siege_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '20:25':
            await mybot.send_message(user.telegram_id, '🗡️🗡️ Осада Гирана начнется через 5 минут')
            print(now, user.telegram_id, user.username, 'получил сообщение об Осаде Гирана')
        else:
            print(now, 'Неподходящее время для Осады Гирана')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
