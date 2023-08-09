from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import Setting
from aiocron import crontab
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@dp.message_handler(commands=['mysettings'])
async def mysettings(message: types.Message):
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    setting_ruoff = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting_expanse = session.query(Expanse).filter_by(id_user=user.telegram_id).first()
    if user and user.server == 'ruoff':

        await message.answer(
            'Установленные настройки русских официальных серверов:\n'
            '\n'
            f'Круглосуточное оповещение - {setting_ruoff.fulltime}\n'
            f'Ивент - {setting_ruoff.event}\n'
            f'Одиночные РБ - {setting_ruoff.soloraidboss}\n'
            f"Кука и Джисра - {setting_ruoff.kuka}\n"
            f"Логово Антараса - {setting_ruoff.loa}\n"
            f"Замок Монарха Льда - {setting_ruoff.frost}\n"
            f"Крепость Орков - {setting_ruoff.fortress}\n"
            f"Битва с Валлоком - {setting_ruoff.balok}\n"
            f"Всемирная Олимпиада - {setting_ruoff.olympiad}\n"
            f"Остров Ада - {setting_ruoff.hellbound}\n"
            f"Осада Гирана - {setting_ruoff.siege}\n"
            f"Хот-тайм Зачистки - {setting_ruoff.primetime}\n"
            f"Зачистка - {setting_ruoff.purge}")

    elif user and user.server == 'expanse':
        await message.answer(
            'Установленные настройки сервера Expanse:\n'
            '\n'
            f'Круглосуточное оповещение - {setting_expanse.fulltime}\n'
            f'Ивент - {setting_expanse.event}\n'
            f'Одиночные РБ - {setting_expanse.soloraidboss}\n'
            f"Логово Антараса - {setting_expanse.loa}\n"
            f"Замок Монарха Льда - {setting_expanse.frost}\n"
            f"Битва с Валлоком - {setting_expanse.balok}\n"
            f"Всемирная Олимпиада - {setting_expanse.olympiad}\n"
            f"Остров Ада - {setting_expanse.hellbound}\n"
            f"Осада Гирана - {setting_expanse.siege}\n")
    else:
        await message.answer('Пожалуйста, вернитесь к /start')

    session.close()
