import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# olympiad buttons
inline_olympiad_buttons = types.InlineKeyboardMarkup()

b14 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setolympiad')
b15 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeolympiad')

inline_olympiad_buttons.add(b14, b15)


# OLYMPIAD SETTINGS
@dp.message_handler(commands=['olympiad'])
async def about_olympiad(message: types.Message):
    await message.answer('Всемирная Олимпиада проводится с понедельника'
                         ' по пятницу с 21:30 до 22:00.', reply_markup=inline_olympiad_buttons)


@dp.callback_query_handler(filters.Text(contains='setolympiad'))
async def set_olympiad(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.olympiad = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Олимпиады установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeolympiad'))
async def remove_olympiad(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.olympiad = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Олимпиады убрано')
    await callback_query.answer()


async def olympiad_notification_wrapper():

    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.olympiad is True:
            await olympiad_notification(user)
    session.close()


async def olympiad_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '21:25':
        await mybot.send_message(user.telegram_id, '⚔️⚔️ Олимпиада начнется через 5 минут')
        print(now, user.telegram_id, user.username, 'получил сообщение об Олимпиаде')
    else:
        print(now, 'Неподходящее время для Олимпиады')
