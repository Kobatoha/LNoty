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
        setting_option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

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


        if not setting_option:
            await message.answer(f'{ruoff_settings_text}')

        elif setting_option:
            option_settings_text = f''
            if setting_option.dream_day and setting_option.dream_time:
                option_settings_text = \
                    f'Подземелье Грёз - {setting_option.dream_day} в {setting_option.dream_time}\n' \
                    f'Храм Валакаса - {setting_option.valakas_day} в {setting_option.valakas_time}\n' \
                    f'Поход на Фринтезу - {setting_option.frintezza_day} в {setting_option.frintezza_time}\n'

            await message.answer(f'{ruoff_settings_text}\n{option_settings_text}')

    elif user and user.server == 'expanse':
        setting_expanse = session.query(Expanse).filter_by(id_user=user.telegram_id).first()

        await message.answer(
            'Установленные настройки сервера Expanse:\n'
            '\n'
            f'Круглосуточное оповещение - {"Да" if setting_expanse.fulltime else "Нет"}\n'
            f'Ивент - {"Да" if setting_expanse.event else "Нет"}\n'
            f'Одиночные РБ - {"Да" if setting_expanse.soloraidboss else "Нет"}\n'
            f'Логово Антараса - {"Да" if setting_expanse.loa else "Нет"}\n'
            f'Замок Монарха Льда - {"Да" if setting_expanse.frost else "Нет"}\n'
            f'Битва с Валлоком - {"Да" if setting_expanse.balok else "Нет"}\n'
            f'Всемирная Олимпиада - {"Да" if setting_expanse.olympiad else "Нет"}\n'
            f'Остров Ада - {"Да" if setting_expanse.hellbound else "Нет"}\n'
            f'Осада Гирана - {"Да" if setting_expanse.siege else "Нет"}\n')
    else:
        await message.answer('Пожалуйста, вернитесь к /start')

    session.close()
