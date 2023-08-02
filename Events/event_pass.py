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

inline_event_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setevent')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeevent')

inline_event_buttons.add(b1, b2)


@dp.message_handler(commands=['event'])
async def about_event(message: types.Message):
    await message.answer('В настоящее время никаких ивентов не подвезли', reply_markup=inline_event_buttons)


@dp.callback_query_handler(filters.Text(contains='setevent'))
async def set_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.event = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об ивенте установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeevent'))
async def remove_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.event = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об ивенте убрано')
    await callback_query.answer()
