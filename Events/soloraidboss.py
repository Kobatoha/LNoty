import asyncio
from aiogram import types, Bot, Dispatcher
from datetime import datetime
from models import User, Base, Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


async def soloraidboss_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.soloraidboss is True and setting.fulltime is True:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения Соло РБ')
            await soloraidboss_notification(user)
        elif setting.soloraidboss is True and setting.fulltime is False:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения Соло РБ')
            await soloraidboss_notification_hardwork(user)
    session.close()


async def soloraidboss_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    soloraidboss_time = ['00:55', '02:55', '04:55', '06:55', '08:55', '10:55', '12:55', '14:55', '16:55', '18:55',
                         '20:55', '22:55']

    if now in soloraidboss_time:
        await mybot.send_message(user.telegram_id, 'Одиночные Рейд Боссы появятся через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о Соло РБ')
    else:
        print(now, 'Неподходящий час для Соло РБ')


async def soloraidboss_notification_hardwork(user: User):
    now = datetime.now().strftime('%H:%M')
    soloraidboss_hardwork = ['08:55', '10:55', '12:55', '14:55', '16:55', '18:55',
                             '20:55', '22:55']

    if now in soloraidboss_hardwork:
        await mybot.send_message(user.telegram_id, 'Одиночные Рейд Боссы появятся через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о Соло РБ')
    else:
        print(now, 'Неподходящий час для Соло РБ')
