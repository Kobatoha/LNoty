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

inline_time_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить 24/7', callback_data='expanse_fulltime')
b2 = types.InlineKeyboardButton(text='Установить с 8:00 до 23:00', callback_data='expanse_hardworkertime')

inline_time_buttons.add(b1, b2)

@dp.message_handler(commands=['expanse_time'])
async def expanse_about_time(message: types.Message):
    await message.answer('Бот присылает оповещения с 8:00 до 23:00, но если ты хочешь, чтобы он работал круглосуточно,'
                         ' выбери "Установить 24/7"\n'
                         'Вернуться к обычному режиму можно в любое время, выбрав сообтвествующую кнопку.'
                         , reply_markup=inline_time_buttons)


@dp.callback_query_handler(filters.Text(contains='expanse_fulltime'))
async def expanse_fulltime(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.fulltime = True

    session.commit()
    session.close()

    await callback_query.message.answer('Круглосуточное оповещение установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='expanse_hardworkertime'))
async def expanse_hardworker_time(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.fulltime = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение установлено с 8:00 до 23:00')
    await callback_query.answer()
