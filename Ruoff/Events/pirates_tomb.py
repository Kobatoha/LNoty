import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

inline_event_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_event')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_event')

inline_event_buttons.add(b1, b2)


@dp.message_handler(commands=['event'])
async def about_event(message: types.Message):
    await message.answer('Зов Гробницы - временное событие, которое проводится с 27 сентября до 18 октября.'
                         ' Попасть в Гробницу Древних Пиратов можно ежедневно в любое время персонажами'
                         ' 80+ уровня в составе пати.\n'
                         'Время оповещения - 21:05 (между валлоком и олимпом)\n'
                         '\n'
                         'За 20 минут в Гробнице вы получите:\n'
                         '- Хороший опыт, можно стоять и качаться\n'
                         '- Древние монеты (100шт дропом, 200шт за награды)\n'
                         'За древние монеты можно слегка закрыть коллекцию, рекомендую',
                         reply_markup=inline_event_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_event'))
async def set_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.event = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение об ивенте установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_event'))
async def remove_event(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.event = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение об ивенте убрано')
    await callback_query.answer()


async def tomb_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.event is True:
            await tomb_notification(user)
    session.close()


async def tomb_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:00':
            await mybot.send_message(user.telegram_id, '🏴‍☠️🏴‍☠️ Вперед, на битву с пиратами! Вход у НПС Деллос')
            print(now, user.telegram_id, user.username, 'получил сообщение об ивенте')
        else:
            print(now, 'Неподходящее время для ивента')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
