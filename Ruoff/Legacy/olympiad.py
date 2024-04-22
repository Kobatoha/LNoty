import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import LegacySetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# olympiad buttons
inline_olympiad_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_legacy_olympiad')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_legacy_olympiad')

inline_olympiad_buttons.add(button_set, button_remove)


# OLYMPIAD SETTINGS
@dp.message_handler(commands=['legacy_olympiad'])
async def about_legacy_olympiad(message: types.Message):
    await message.answer('Всемирная Олимпиада проводится с понедельника'
                         ' по субботу с 22:00 до 23:00.', reply_markup=inline_olympiad_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_legacy_olympiad'))
async def set_legacy_olympiad(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
        setting.olympiad = True
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение о начале [Legacy] Олимпиады установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_legacy_olympiad'))
async def remove_legacy_olympiad(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
        setting.olympiad = False
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение о начале [Legacy] Олимпиады убрано')
    await callback_query.answer()


async def legacy_olympiad_notification_wrapper():

    with Session() as session:
        users = session.query(User).all()
    
        for user in users:
            setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
            if setting.olympiad is True:
                await legacy_olympiad_notification(user)


async def legacy_olympiad_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:55':
            await mybot.send_message(user.telegram_id, '⚔️⚔️ [Legacy] Олимпиада начнется через 5 минут')
            print(now, user.telegram_id, user.username, 'получил сообщение об [Legacy] Олимпиаде')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
