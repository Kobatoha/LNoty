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


async def kuka_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:

        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.kuka is True:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения Куки')
            await kuka_notification(user)
    session.close()


async def kuka_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    kuka_time = ['00:45', '02:45', '04:45', '06:45', '08:45', '10:45', '12:45', '14:45', '16:45', '18:45', '20:45',
                 '22:45']

    if now in kuka_time:
        await mybot.send_message(user.telegram_id, 'Кука появится через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о Куке')
    else:
        print(now, 'Неподходящий час для Куки')
