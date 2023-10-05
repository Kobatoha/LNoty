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

inline_rescue_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_setevent')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_removeevent')

inline_rescue_buttons.add(b1, b2)


@dp.message_handler(commands=['event'])
async def about_event(message: types.Message):
    await message.answer('Спасение питомцев - временное событие, которое проводится с 23 августа до 6 сентября.'
                         ' Дважды в день в Загоне Диких Зверей проводоится рейд на Главных Инструкторов'
                         ' в 11:00 и 21:00.\n'
                         'В награду за последний удар можно получить:\n'
                         '- Шкатулка с самоцветом 5ур\n'
                         '- Сундук с приколюхами для персонажа и его питомца\n'
                         'Так же можно будет словить питомца с некоторым шансом и расходку на него.',
                         reply_markup=inline_rescue_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_setevent'))
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


@dp.callback_query_handler(filters.Text(contains='ruoff_removeevent'))
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


async def rescue_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.event is True:
            await rescue_notification(user)
    session.close()


async def rescue_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '10:56' or now == '20:56':
            await mybot.send_message(user.telegram_id, '🦊🦊 Спасать питомцев отправляемся через 4 минуты')
            print(now, user.telegram_id, user.username, 'получил сообщение об ивенте')
        else:
            print(now, 'Неподходящее время для ивента')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
