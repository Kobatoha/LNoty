from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import Setting, RuoffCustomSetting, RuoffBigWar
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
        bw = session.query(RuoffBigWar).filter_by(id_user=user.telegram_id).first()

        v = " в "
        no = "не установлено"

        ruoff_settings_text = f'Установленные настройки русских официальных серверов:\n' \
                              f'\n' \
                              f'Круглосуточное оповещение - {"🌵" if setting_ruoff.fulltime else no}\n' \
                              f'Ивент - {"🌵" if setting_ruoff.event else no}\n' \
                              f'Секретная лавка - {"🌵" if setting_ruoff.festival else no}\n' \
                              f'Календарь - {"🌵" if setting_ruoff.calendar else no}\n' \
                              f'Кука и Джисра - {"🌵" if setting_ruoff.kuka else no}\n' \
                              f'Логово Антараса - {"🌵" if setting_ruoff.loa else no}\n' \
                              f'Замок Монарха Льда - {"🌵" if setting_ruoff.frost else no}\n' \
                              f'Крепость Орков - {"🌵" if setting_ruoff.fortress else no}\n' \
                              f'Битва с Валлоком - {"🌵" if setting_ruoff.balok else no}\n' \
                              f'Всемирная Олимпиада - {"🌵" if setting_ruoff.olympiad else no}\n' \
                              f'Остров Ада - {"🌵" if setting_ruoff.hellbound else no}\n' \
                              f'Осада Гирана - {"🌵" if setting_ruoff.siege else no}\n' \
                              f'Прайм-тайм Зачистки - {"🌵" if setting_ruoff.primetime else no}\n' \
                              f'Зачистка - {"🌵" if setting_ruoff.purge else no}\n' \
                              f'Кебер - {"🌵" if setting_ruoff.keber else no}\n' \
                              f'Вторжение - {"🌵" if setting_ruoff.invasion else no}\n' \

        if not op and not bw:
            await message.answer(f'{ruoff_settings_text}')

        elif op:
            option_settings_text = \
                f'Подземелье Грёз - ' \
                f'{"🌵" + op.dream_day + v + op.dream_time if op.dream_day and op.dream_time else no}\n'\
                f'Храм Валакаса - ' \
                f'{"🌵" op.valakas_day + v + op.valakas_time if op.valakas_day and op.valakas_time else no}\n'\
                f'Поход на Фринтезу - ' \
                f'{"🌵" op.frintezza_day + v + op.frintezza_time if op.frintezza_day and op.frintezza_time else no}\n' \
                f'Забытые Сады - ' \
                f'ежедневно {"🌵" + v + op.gardens if op.gardens else no}\n' \
                f'Исследование Годдарда - ' \
                f'ежедневно {"🌵" + v + op.goddard if op.goddard else no}\n' \

            if bw:
                bigwar_setting_text = f'🌈 Башня Дерзости - {"🍌" if bw.toi else no}\n' \
                                      f'🌈 Забытый Сад - {"🍌" if bw.gardens else no}\n' \
                                      f'🌈 Языческий Храм/Крепость Кельбима - {"🍌" if bw.pagan else no}\n' \
                                      f'🌈 Битва с Антарасом - {"🍌" if bw.antharas else no}\n' \
                                      f'🌈 Остров Ада - {"🍌" if bw.hellbound else no}\n' \
                                      f'🌈 Хаотический Босс - {"🍌" if bw.chaotic else no}\n' \
                                      f'🌈 Лилит - {"🍌" if bw.lilith else no}\n' \
                                      f'🌈 Анаким - {"🍌" if bw.anakim else no}\n' \
                                      f'🌈 Горд - {"🍌" if bw.gord else no}\n' \
                                      f'🌈 Замок Монарха Льда - {"🍌" if bw.frost else no}\n' \
                                      f'🌈 Логово Антараса - {"🍌" if bw.loa else no}\n'

                await message.answer(f'{ruoff_settings_text}\n{option_settings_text}\n{bigwar_setting_text}')

            else:
                await message.answer(f'{ruoff_settings_text}\n{option_settings_text}')
    else:
        await message.answer('Пожалуйста, вернитесь к /start')

    session.close()
