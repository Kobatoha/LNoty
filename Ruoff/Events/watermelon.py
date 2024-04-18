import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

inline_watermelon_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoffsetevent')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoffremoveevent')

inline_watermelon_buttons.add(b1, b2)

# Watermelon - 12.07.23 - 02.08.23
# Арбузный сезон - временное событие, которое проводится с 12 июля до 2 августа.
# Дважды в день на Острове Грёз можно поохотиться на Королевских Арбузов и Снежных Тыкв
# в 11:00 и 21:00. В награду за последний удар можно получить:
# - Купон на книгу 3*
# - Улучшенные и проклятые свитки А ранга
# - Куклы 1го и 2го уровня


@dp.message_handler(commands=['event'])
async def about_event(message: types.Message):
    await message.answer('Арбузный сезон - временное событие, которое проводится с 12 июля до 2 августа.'
                         ' Дважды в день на Острове Грёз можно поохотиться на Королевских Арбузов и Снежных Тыкв'
                         ' в 11:00 и 21:00.\n'
                         'В награду за последний удар можно получить:\n'
                         '- Купон на книгу 3*\n'
                         '- Улучшенные и проклятые свитки А ранга\n'
                         '- Куклы 1го и 2го уровня', reply_markup=inline_watermelon_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoffsetevent'))
async def set_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.event = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об ивенте установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoffremoveevent'))
async def remove_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.event = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об ивенте убрано')
    await callback_query.answer()


async def watermelon_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        if setting.event is True:
            await watermelon_notification(user)
    session.close()


async def watermelon_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '10:56' or now == '20:56':
        await mybot.send_message(user.telegram_id, '🍉🍉 Арбузный сезон откроется через 4 минуты')
        print(now, user.telegram_id, user.username, 'получил сообщение об ивенте')
    else:
        print(now, 'Неподходящее время для ивента')
