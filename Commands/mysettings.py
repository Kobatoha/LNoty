from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import Setting, RuoffCustomSetting
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
    if user and user.server == 'ruoff':
        setting_ruoff = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        op = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

        ruoff_settings_text = f'Установленные настройки русских официальных серверов:\n' \
                              f'\n' \
                              f'Круглосуточное оповещение - {"Да" if setting_ruoff.fulltime else "Нет"}\n' \
                              f'Ивент - {"Да" if setting_ruoff.event else "Нет"}\n' \
                              f'Календарь - {"Да" if setting_ruoff.calendar else "Нет"}\n' \
                              f'Кука и Джисра - {"Да" if setting_ruoff.kuka else "Нет"}\n' \
                              f'Логово Антараса - {"Да" if setting_ruoff.loa else "Нет"}\n' \
                              f'Замок Монарха Льда - {"Да" if setting_ruoff.frost else "Нет"}\n' \
                              f'Крепость Орков - {"Да" if setting_ruoff.fortress else "Нет"}\n' \
                              f'Битва с Валлоком - {"Да" if setting_ruoff.balok else "Нет"}\n' \
                              f'Всемирная Олимпиада - {"Да" if setting_ruoff.olympiad else "Нет"}\n' \
                              f'Остров Ада - {"Да" if setting_ruoff.hellbound else "Нет"}\n' \
                              f'Осада Гирана - {"Да" if setting_ruoff.siege else "Нет"}\n' \
                              f'Прайм-тайм Зачистки - {"Да" if setting_ruoff.primetime else "Нет"}\n' \
                              f'Зачистка - {"Да" if setting_ruoff.purge else "Нет"}\n' \

        v = " в "
        no = "не установлено"

        if not op:
            await message.answer(f'{ruoff_settings_text}')

        elif op:
            option_settings_text = \
                f'Подземелье Грёз - ' \
                f'{op.dream_day + v + op.dream_time if op.dream_day and op.dream_time else no}\n'\
                f'Храм Валакаса - ' \
                f'{op.valakas_day + v + op.valakas_time if op.valakas_day and op.valakas_time else no}\n'\
                f'Поход на Фринтезу - ' \
                f'{op.frintezza_day  + v + op.frintezza_time if op.frintezza_day and op.frintezza_time else no}\n'

            await message.answer(f'{ruoff_settings_text}\n{option_settings_text}')

    else:
        await message.answer('Пожалуйста, вернитесь к /start')

    session.close()
