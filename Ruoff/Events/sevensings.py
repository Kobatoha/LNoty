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

# sevensings buttons
inline_sevensings_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_sevensings')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_sevensings')

inline_sevensings_buttons.add(button_set, button_remove)


# sevensings SETTINGS
@dp.message_handler(commands=['sevensings'])
async def about_sevensings(message: types.Message):
    await message.answer('Семь Печатей - ежедневное задание на 50 древней адены. '\
                         'Нужно убить 300 монстров в Катакомбах с 21:00 до 21:30',
                         reply_markup=inline_sevensings_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_sevensings'))
async def set_sevensings(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.sevensings = True
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение об открытии Катакомб установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_sevensings'))
async def remove_sevensings(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.sevensings = False

        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение об открытии Катакомб убрано')
    await callback_query.answer()


async def sevensings_notification_wrapper():

    with Session() as session:
        users = session.query(User).all()
    
        for user in users:
            setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
            if setting.sevensings is True:
                await sevensings_notification(user)

async def sevensings_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '20:55':
            await mybot.send_message(user.telegram_id, '🗿 [Семь Печатей] Через 5 минут откроются дверки в Катакомбочки')
            print(now, user.telegram_id, user.username, 'получил сообщение об открытии Катакомб')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
