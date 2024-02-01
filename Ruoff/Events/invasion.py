import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime, timedelta
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

# invasion buttons
inline_invasion_buttons = types.InlineKeyboardMarkup()

set_button = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_invasion')
remove_button = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_invasion')

inline_invasion_buttons.add(set_button, remove_button)


# INVASION SETTINGS
@dp.message_handler(commands=['invasion'])
async def about_invasion(message: types.Message):
    await message.answer('Вторжение мобов каждые 4 часа в одной из следующих локаций:\n'
                         '- Долина Драконов (восток)\n'
                         '- Лагерь Тай\n'
                         '- Земли Ящеров Мелат\n'
                         '\n'
                         'Переместиться к месту вторжения можно от NPC Вранов Коготь,'
                         ' который появляется перед храмом в Адене, Гиране и Орене.\n'
                         'Суть мероприятия - колупать мобов и пытаться сделать ластхит промежуточным боссам.'
                         ' Главный босс появляется через 25 минут после начала вторжения на 10 минут, а затем исчезает'
                         ' независимо от того, побежден он или нет. За последний удар можно получить сундук'
                         ' с приятной мелочью:\n'
                         '- свитки А ранга\n'
                         '- камни эволюции\n'
                         '- камни зачарования\n'
                         '- маг.таблички\n'
                         '- свитки благословления\n'
                         '- усилитель краски'
                         '\n', reply_markup=inline_invasion_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_invasion'))
async def set_invasion(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.invasion = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение для Вторжения установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_invasion'))
async def remove_invasion(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.invasion = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение для Вторжения убрано')
    await callback_query.answer()


async def invasion_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:

        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.invasion is True and setting.fulltime is True:
            await invasion_notification(user)
        elif setting.invasion is True and setting.fulltime is False:
            await invasion_notification_hardwork(user)
    session.close()


async def invasion_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    invasion_time = ['12:21']
    invasion = []

    for time in invasion_time:
        current_time = datetime.strptime(time, "%H:%M")
        for i in range(6):  # Добавляем 4 часа 6 раз (через каждые 4 часа)
            invasion.append(current_time.strftime("%H:%M"))
            current_time += timedelta(hours=4)

    try:
        if now in invasion:
            await mybot.send_message(user.telegram_id, 'Вторжение начнется через 5 минут. Следите за анонсом в игре.')
            print(now, user.telegram_id, user.username, '(круглосуточник) получил сообщение о Вторжении')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)


async def invasion_notification_hardwork(user: User):
    now = datetime.now().strftime('%H:%M')
    invasion_time = ['12:21']
    invasion_hardwork = []

    for time in invasion_time:
        current_time = datetime.strptime(time, "%H:%M")
        for i in range(6):  # Добавляем 4 часа 6 раз (через каждые 4 часа)
            invasion_hardwork.append(current_time.strftime("%H:%M"))
            current_time += timedelta(hours=4)
    try:
        if now in invasion_hardwork:
            await mybot.send_message(user.telegram_id, 'Вторжение начнется через 5 минут. Следите за анонсом в игре.')
            print(now, user.telegram_id, user.username, '(работяга) получил сообщение о Вторжении')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
