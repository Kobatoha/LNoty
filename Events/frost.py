import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from models import User, Base, Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# frost lord`s castle buttons
inline_frost_buttons = types.InlineKeyboardMarkup()

b8 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setfrost')
b9 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removefrost')

inline_frost_buttons.add(b8, b9)


# FROST LORD`S CASTLE SETTINGS
@dp.message_handler(commands=['frost'])
async def about_frost(message: types.Message):
    await message.answer('Всемирная зона Замок Монарха Льда открывается во'
                         ' вторник и четверг c 18:00 до полуночи.\n',
                         reply_markup=inline_frost_buttons)


@dp.callback_query_handler(filters.Text(contains='setfrost'))
async def set_frost(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.frost = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removefrost'))
async def remove_frost(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.frost = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда убрано')
    await callback_query.answer()


async def frost_notification_wrapper():

    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.frost is True:
            await frost_notification(user)
    session.close()


async def frost_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '17:55':
        await mybot.send_message(user.telegram_id, '❄️❄️ Замок Монарха Льда откроется через 5 минут')
        print(now, user.telegram_id, user.username, 'получил сообщение о Замке Монарха Льда')
    else:
        print(now, 'Неподходящее время для Замка Монарха Льда')
