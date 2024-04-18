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


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# keber buttons
inline_keber_buttons = types.InlineKeyboardMarkup()

set_button = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_keber')
remove_button = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_keber')

inline_keber_buttons.add(set_button, remove_button)


# KEBER SETTINGS
@dp.message_handler(commands=['keber'])
async def about_keber(message: types.Message):
    await message.answer('Кебер и его шайка появляется каждый час в :00 минут\n'
                         'Кебер - само воплощение экспули для твинков\n', reply_markup=inline_keber_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_keber'))
async def set_keber(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.keber = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение для Кебера установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_keber'))
async def remove_keber(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
    setting.keber = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение для Кебера убрано')
    await callback_query.answer()


async def keber_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:

        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        if setting.keber is True and setting.fulltime is True:
            await keber_notification(user)
        elif setting.keber is True and setting.fulltime is False:
            await keber_notification_hardwork(user)
    session.close()


async def keber_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    keber_time = ['00:58', '01:58', '02:58', '03:58', '04:58', '05:58', '06:58', '07:58', '08:58', '09:58', '10:58',
                  '11:58', '12:58', '13:58', '14:58', '15:58', '16:58', '17:58', '18:58', '19:58', '20:58', '21:58',
                  '22:58', '23:58']
    try:
        if now in keber_time:
            await mybot.send_message(user.telegram_id, 'Кебер появится через 2 минуты')
            print(now, user.telegram_id, user.username, '(круглосуточник) получил сообщение о Кебере')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)


async def keber_notification_hardwork(user: User):
    now = datetime.now().strftime('%H:%M')
    keber_hardwork = ['08:58', '09:58', '10:58', '11:58', '12:58', '13:58', '14:58', '15:58', '16:58', '17:58', '18:58',
                      '19:58', '20:58', '21:58', '22:58']

    try:
        if now in keber_hardwork:
            await mybot.send_message(user.telegram_id, 'Кебер появится через 2 минуты')
            print(now, user.telegram_id, user.username, '(работяга) получил сообщение о Кебере')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
