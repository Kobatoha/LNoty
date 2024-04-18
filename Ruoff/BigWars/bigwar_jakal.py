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

# jakal buttons
inline_jakal_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_bigwar_jakal')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_bigwar_jakal')

inline_gord_buttons.add(button_set, button_remove)


# jakal SETTINGS
@dp.message_handler(commands=['bigwar_jakal'])
async def about_bigwar_jakal(message: types.Message):
    await message.answer('[BIGWAR] Джакал 23:00 [ежедневно] за 15 минут\n',
                         reply_markup=inline_jakal_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_bigwar_jakal'))
async def set_bigwar_jakal(callback_query: types.CallbackQuery):
    with Session() as session:
  
        bg_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
        bg_user.jakal = True
        session.commit()

    await callback_query.message.answer('[BIGWAR] Оповещения о Джакале установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_bigwar_jakal'))
async def remove_bigwar_jakal(callback_query: types.CallbackQuery):
    with Session() as session:

        bg_user = session.query(EssenceBigWar).filter_by(id_user=callback_query.from_user.id).first()
        bg_user.jakal = False
        session.commit()

    await callback_query.message.answer('[BIGWAR] Оповещения о Джакале убраны')
    await callback_query.answer()


async def bigwar_jakal_notification_wrapper():

    with Session() as session:
        users = session.query(EssenceBigWar).all()
        for user in users:
            if user.jakal is True:
                await bigwar_jakal_notification(user)


async def bigwar_jakal_notification(user: EssenceBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        if now == '22:45':
            await mybot.send_message(user.id_user, '🌈🌈 [BIGWAR] Джакал через 15 минут (возможно)')
            print(now, user.id_user, 'получил сообщение о [BIGWAR] Джакале')

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
