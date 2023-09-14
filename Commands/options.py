import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import RuoffCustomSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN, test_token
from aiogram.utils.exceptions import BotBlocked
import logging


logging.basicConfig(filename='Lineage2Notification.log', level=logging.INFO)


mybot = Bot(token=test_token)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

options_menu_text = 'Добро пожаловать в меню персональных настроек, ' \
                    'где вы самостоятельно указываете время и день, когда нужна напоминалка:\n' \
                    '\n' \
                    '/dream - Подземелье Грез [раз в неделю]\n' \
                    '/valakas - Храм Валакаса [раз в неделю]\n' \
                    '/frintezza - Битва с Фринтезой [раз в неделю]\n' \
                    '\n' \
                    '/gardens - Забытые сады [ежедневно]\n' \
                    '/goddard - Исследование Годдарда [ежедневно]\n' \
                    '/training - Тренировочное подземелье [ежедневно]\n' \
                    '/transcendent - Невероятная временная зона [ежедневно]\n' \
                    '/toi - Башня Дерзости [ежедневно]\n' \
                    '/pagan - Языческий Храм/Крепость Кельбима [понедельник - пятница]\n' \
                    '/aztacan - Храм Ацтакана [ежедневно]\n' \
                    '\n' \
                    '/tattoo - Прокачать тату [ежедневно]'


@dp.message_handler(commands=['options'])
async def options_menu(message: types.CallbackQuery):
    try:
        await message.answer(text=options_menu_text)

    except Exception as e:
        logging.error(f' [OPTIONS] {message.from_user.id} - ошибка в функции options_menu: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[OPTIONS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции options_menu: {e}')
