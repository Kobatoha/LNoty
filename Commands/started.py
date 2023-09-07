from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting, RuoffCustomSetting, RuoffClanDangeon
from aiocron import crontab
import asyncio
from datetime import datetime
from Commands.server import inline_server_buttons

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    now = datetime.now().strftime('%H:%M')
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        print(now, 'Добавление нового пользователя...')
        user = User(telegram_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
        setting = Setting(id_user=user.telegram_id)
        session.add(setting)
        session.commit()
        custom = RuoffCustomSetting(id_user=user.telegram_id)
        session.add(custom)
        session.commit()
        print(now, user.telegram_id, user.username, '- добавлен новый пользователь')

    else:
        user.upd_date = datetime.today()
        session.commit()
        if not user.username:  # если username еще не указан
            user.username = message.from_user.username  # обновляем username
            session.commit()
            print(now, user.telegram_id, user.username, '- username добавлен')
        else:
            print(now, user.telegram_id, user.username, '- уже добавлен')
    session.close()
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'В Меню ты найдешь все доступные команды.\n'
                         'Так же этот список можно вызвать командой /help\n' 
                         'Бот по-дефолту работает в работяжном режиме с 8:00 до 23:00,'
                         ' изменить эту настройку можно по команде /time\n'
                         '\n'
                         'Выбирай интересующую активность и жми [Установить оповещение].'
                         ' В таком случае тебе будут приходить уведомления за 5 минут'
                         ' до начала события.\n'
                         '\n'
                         'За это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.\n'
                         '\n'
                         'А теперь пора выбрать свой сервер :)',
                         reply_markup=inline_server_buttons)
