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

# frost lord`s castle buttons
inline_frost_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_legacy_frost')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_legacy_frost')

inline_frost_buttons.add(button_set, button_remove)


# FROST LORD`S CASTLE SETTINGS
@dp.message_handler(commands=['legacy_frost'])
async def about_legacy_frost(message: types.Message):
    await message.answer('[Legacy] Замок Монарха Льда открывается в'
                         ' субботу и воскресенье c 18:00 до полуночи для персонажей 85+\n',
                         reply_markup=inline_frost_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_legacy_frost'))
async def set_legacy_frost(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
        setting.frost = True
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение об открытии [Legacy] Замка Монарха Льда установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_legacy_frost'))
async def remove_legacy_frost(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
        setting.frost = False
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение об открытии [Legacy] Замка Монарха Льда убрано')
    await callback_query.answer()


async def legacy_frost_notification_wrapper():

    with Session() as session:
        users = session.query(User).all()
        for user in users:
            setting = session.query(LegacySetting).filter_by(id_user=user.telegram_id).first()
            if setting.frost is True:
                await legacy_frost_notification(user)


async def legacy_frost_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '17:55':
            await mybot.send_message(user.telegram_id, '❄️❄️ [Legacy] Замок Монарха Льда откроется через 5 минут')
            print(now, user.telegram_id, user.username, 'получил сообщение о [Legacy] Замке Монарха Льда')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
