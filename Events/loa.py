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


async def loa_notification_wrapper():

    session = Session()
    users = session.query(User).all()
    for user in users:
        now = datetime.now().strftime('%H:%M')
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.loa is True:
            print(now, user.telegram_id, 'подходит под условия оповещения Логова Антараса')
            await loa_notification(user)
    session.close()


async def loa_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '17:55':
        await mybot.send_message(user.telegram_id, '🔥🔥 Логово Антараса откроется через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о Логове Антараса')
    else:
        print(now, 'Неподходящее время для Логова Антараса')
