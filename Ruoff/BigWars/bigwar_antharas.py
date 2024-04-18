import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.Base import Base
from DataBase.Ruoff import EssenceBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# ANTHARAS buttons
inline_antharas_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_antharas')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_antharas')

inline_antharas_buttons.add(button_set, button_remove)


# ANTHARAS SETTINGS
@dp.message_handler(commands=['bigwar_antharas'])
async def about_bigwar_antharas(message: types.Message):
    await message.answer('[BIGWAR] Антарас 22:00 [воскресенье] за 15 мин\n',
                         reply_markup=inline_antharas_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_antharas'))
async def set_bigwar_antharas(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.antharas = True
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение об Антарасе установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_antharas'))
async def remove_bigwar_antharas(callback_query: types.CallbackQuery):
    session = Session()

    bigwar_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bigwar_user.antharas = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] Оповещение об Антарасе убрано')
    await callback_query.answer()


async def bigwar_antharas_notification_wrapper():

    session = Session()
    users = session.query(EssenceBigWar).all()
    for user in users:
        if user.antharas is True:
            await bigwar_antharas_notification(user)
    session.close()


async def bigwar_antharas_notification(user: EssenceBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '21:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Антарас через 15 минут')
            print(now, '[BIGWAR]', user.id_user, 'получил сообщение об Антарасе')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
