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


async def balok_notification_wrapper():

    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.balok is True:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения Битвы с Валлоком')
            await balok_notification(user)
    session.close()


async def balok_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '20:25':
        await mybot.send_message(user.telegram_id, 'Битва с Валлоком начнется через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о Битве с Валлоком')
    else:
        print(now, 'Неподходящее время для Битвы с Валлоком')
