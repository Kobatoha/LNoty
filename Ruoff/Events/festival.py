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

inline_festival_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_festival')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_festival')

inline_festival_buttons.add(b1, b2)


@dp.message_handler(commands=['festival'])
async def about_festival(message: types.Message):
    await message.answer('Фестиваль Legacy 12:00 | 20:00 | 22:00',
                         reply_markup=inline_festival_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_festival'))
async def set_festival(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.festival = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о Фeстивале установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_festival'))
async def remove_festival(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.festival = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о Фeстивале убрано')
    await callback_query.answer()


async def festival_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.festival is True:
            await festival_notification(user)
    session.close()


async def festival_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '11:57' or now == '19:57' or now == '21:57':
        await mybot.send_message(user.telegram_id, 'Фестивалька начнется через 3 минуты')
        print(now, user.telegram_id, user.username, 'получил сообщение о Фестивале')
    else:
        print(now, 'Неподходящее время для фестиваля')
