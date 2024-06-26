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

# lair of antharas buttons
inline_loa_buttons = types.InlineKeyboardMarkup()

b6 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_setloa')
b7 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_removeloa')

inline_loa_buttons.add(b6, b7)


# LAIR OF ANTHARAS SETTINGS
@dp.message_handler(commands=['loa'])
async def about_loa(message: types.Message):
    await message.answer('Всемирная зона Логово Антараса открывается в'
                         ' понедельник и среду c 18:00 до полуночи.\n',
                         reply_markup=inline_loa_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_setloa'))
async def set_loa(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.loa = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение об открытии Логова Антараса установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_removeloa'))
async def remove_loa(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.loa = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение об открытии Логова Антараса убрано')
    await callback_query.answer()


async def loa_notification_wrapper():

    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        if setting.loa is True:
            await loa_notification(user)
    session.close()


async def loa_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '17:55':
            await mybot.send_message(user.telegram_id, '🔥🔥 Логово Антараса откроется через 5 минут')
            print(now, user.telegram_id, user.username, 'получил сообщение о Логове Антараса')
        else:
            print(now, 'Неподходящее время для Логова Антараса')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)