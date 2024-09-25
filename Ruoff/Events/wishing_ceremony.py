import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime, timedelta
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

# wishing ceremony buttons
inline_wishing_ceremony_buttons = types.InlineKeyboardMarkup()

set_button = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_event')
remove_button = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_event')

inline_wishing_ceremony_buttons.add(set_button, remove_button)


# wishing ceremony SETTINGS
@dp.message_handler(commands=['event'])
async def about_event(message: types.Message):
    await message.answer('Церемония Желаний 11:00 и 21:00'
                         '\n', reply_markup=inline_wishing_ceremony_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_event'))
async def set_event(callback_query: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.event = True

        session.commit()

        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение для ивента установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_event'))
async def remove_event(callback_query: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.event = False

        session.commit()

        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение для event убрано')
    await callback_query.answer()


async def wishing_ceremony_notification_wrapper():
    with Session() as session:
        users = session.query(User).all()
        for user in users:

            setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
            if setting.event is True:
                await wishing_ceremony_notification(user)


async def wishing_ceremony_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '10:56' or now == '20:56':
        try:
            await mybot.send_message(user.telegram_id, 'Церемония Желаний начнется через 4 минуты')
            print(now, user.telegram_id, user.username, 'получил сообщение об ивенте')
        except:
            print(now, user.telegram_id, user.username, 'не отправлено сообщение')



