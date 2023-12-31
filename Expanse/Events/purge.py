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

# purge buttons
inline_purge_buttons = types.InlineKeyboardMarkup()

b22 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='expanse_setpurge')
b23 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='expanse_removepurge')

inline_purge_buttons.add(b22, b23)


# PURGE SETTINGS
@dp.message_handler(commands=['expanse_purge'])
async def expanse_about_purge(message: types.Message):
    await message.answer('Зачистка обнуляется в полночь в воскресенье',
                         reply_markup=inline_purge_buttons)


@dp.callback_query_handler(filters.Text(contains='expanse_setpurge'))
async def expanse_set_purge(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.purge = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о сборе зачистки установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='expanse_removepurge'))
async def expanse_remove_purge(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    setting.purge = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о сборе зачистки убрано')
    await callback_query.answer()


async def expanse_purge_notification_wrapper():

    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
        if setting.purge is True:
            await expasne_purge_notification(user)
    session.close()


async def expanse_purge_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '22:50':
        await mybot.send_message(user.telegram_id, '🍾 Скорее соберите Зачистку :)')
        print(now, user.telegram_id, user.username, 'получил сообщение об сборе Зачистке')
    else:
        print(now, 'Неподходящее время для сбора Зачистки')
