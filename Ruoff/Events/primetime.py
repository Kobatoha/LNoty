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

# prime time buttons
inline_primetime_buttons = types.InlineKeyboardMarkup()

b20 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_setprimetime')
b21 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_removeprimetime')

inline_primetime_buttons.add(b20, b21)


# PRIME TIME SETTINGS
@dp.message_handler(commands=['primetime'])
async def about_primetime(message: types.Message):
    await message.answer('Ежедневно в хот-тайм получаемые очки зачистки удваиваются:\n'
                         '- с 12:00 до 14:00\n'
                         '- с 19:00 до 23:00', reply_markup=inline_primetime_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_setprimetime'))
async def set_primetime(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.primetime = True

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение о начале хот-тайма установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_removeprimetime'))
async def remove_primetime(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.primetime = False

    session.commit()

    user.upd_date = datetime.today()
    session.commit()

    session.close()

    await callback_query.message.answer('Оповещение о начале хот-тайма убрано')
    await callback_query.answer()


async def primetime_notification_wrapper():
    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.primetime is True:
            await primetime_notification(user)
    session.close()


async def primetime_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '11:56' or now == '18:56':
            await mybot.send_message(user.telegram_id, '☄️ Хот-тайм зачистки начнется через 4 минуты')
            print(now, user.telegram_id, user.username, 'получил сообщение о начале Прайм-тайма')
        elif now == '13:56' or now == '22:56':
            await mybot.send_message(user.telegram_id, '☄️ Хот-тайм зачистки закончится через 4 минуты')
            print(now, user.telegram_id, user.username, 'получил сообщение о конце Прайм-тайма')
        else:
            print(now, 'Неподходящее время для Прайм-тайма')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
