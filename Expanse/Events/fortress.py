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

# orc fortress buttons
inline_fortress_buttons = types.InlineKeyboardMarkup()

b10 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='expanse_setfortress')
b11 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='expanse_removefortress')

inline_fortress_buttons.add(b10, b11)


# ORC FORTRESS SETTINGS
@dp.message_handler(commands=['expanse_fortress'])
async def expanse_about_fortress(message: types.Message):
    await message.answer('Битва за Крепость Орков проводится ежедневно в 20:00',
                         reply_markup=inline_fortress_buttons)


@dp.callback_query_handler(filters.Text(contains='expanse_setfortress'))
async def expanse_set_fortress(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.fortress = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='expanse_removefortress'))
async def expanse_remove_fortress(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.fortress = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков убрано')
    await callback_query.answer()


async def expanse_fortress_notification_wrapper():

    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
        if setting.fortress is True:
            await expanse_fortress_notification(user)

    session.close()


async def expanse_fortress_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '19:55':
        await mybot.send_message(user.telegram_id, '🐸🐸 Битва за Крепость Орков начнется через 5 минут')
        print(now, user.telegram_id, user.username, 'получил сообщение о Крепости Орков')
    else:
        print(now, 'Неподходящее время для Крепости Орков')
