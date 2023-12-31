import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# siege giran buttons
inline_siege_buttons = types.InlineKeyboardMarkup()

b18 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='expanse_setsiege')
b19 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='expanse_removesiege')

inline_siege_buttons.add(b18, b19)


# GIRAN`S SIEGE SETTINGS
@dp.message_handler(commands=['expanse_siege'])
async def expanse_about_siege(message: types.Message):
    await message.answer('Осада Замка Гиран приходит в воскресенье с 20:30 до 21:00.',
                         reply_markup=inline_siege_buttons)


@dp.callback_query_handler(filters.Text(contains='expanse_setsiege'))
async def expanse_set_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.siege = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='expanse_removesiege'))
async def expanse_remove_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.siege = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана убрано')
    await callback_query.answer()


async def expanse_siege_notification_wrapper():
    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
        if setting.siege is True:
            await expanse_siege_notification(user)
    session.close()


async def expanse_siege_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '20:25':
        await mybot.send_message(user.telegram_id, '🗡️🗡️ Осада Гирана начнется через 5 минут')
        print(now, user.telegram_id, user.username, 'получил сообщение об Осаде Гирана')
    else:
        print(now, 'Неподходящее время для Осады Гирана')
