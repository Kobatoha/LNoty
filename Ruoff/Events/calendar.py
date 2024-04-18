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
import logging

logging.basicConfig(filename='Lineage2Notification.log', level=logging.INFO)


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

inline_calendar_buttons = types.InlineKeyboardMarkup()

button_add = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_calendar')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_calendar')

inline_calendar_buttons.add(button_add, button_remove)


@dp.message_handler(commands=['calendar'])
async def about_calendar(message: types.Message):
    try:
        await message.answer('Календарь - временное событие, когда за 30 минут онлайна можно лутнуть награду.'
                             ' Оповещение в 21:10 на время действия акции.',
                             reply_markup=inline_calendar_buttons)

    except Exception as e:
        logging.error(f' [CALENDAR] {callback_query.from_user.id} - ошибка в функции about_calendar: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CALENDAR] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции about_calendar: {e}')


@dp.callback_query_handler(filters.Text(contains='ruoff_set_calendar'))
async def set_calendar(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.calendar = True

        session.commit()

        user.upd_date = datetime.today()
        session.commit()

        session.close()

        await callback_query.message.answer('Оповещение об ивенте установлено')
        await callback_query.answer()

    except Exception as e:
        logging.error(f' [CALENDAR] {callback_query.from_user.id} - ошибка в функции set_calendar: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CALENDAR] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_calendar: {e}')


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_calendar'))
async def remove_calendar(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.calendar = False

        session.commit()

        user.upd_date = datetime.today()
        session.commit()

        session.close()

        await callback_query.message.answer('Оповещение об ивенте убрано')
        await callback_query.answer()

    except Exception as e:
        logging.error(f' [CALENDAR] {callback_query.from_user.id} - ошибка в функции remove_calendar: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CALENDAR] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции remove_calendar: {e}')


async def calendar_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()
        for user in users:
            setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
            if setting.calendar is True:
                await calendar_notification(user)
        session.close()

    except Exception as e:
        logging.error(f' [CALENDAR] {callback_query.from_user.id} - '
                      f'ошибка в функции calendar_notification_wrapper: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CALENDAR] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции calendar_notification_wrapper: {e}')


async def calendar_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:10':
            await mybot.send_message(user.telegram_id, '🗓 Не забудь забрать награду календаря')
            print(now, user.telegram_id, user.username, 'получил сообщение о календаре')
        else:
            print(now, 'Неподходящее время для ивента')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        logging.error(f' [CALENDAR] {callback_query.from_user.id} - ошибка в функции calendar_notification: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CALENDAR] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции calendar_notification: {e}')
