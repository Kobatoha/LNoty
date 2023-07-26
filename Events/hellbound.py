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


async def hellbound_notification_wrapper():
    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.hellbound is True:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения Острова Ада')
            await hellbound_notification(user)
    session.close()


async def hellbound_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '09:55':
        await mybot.send_message(user.telegram_id, 'Остров Ада откроется через 5 минут')
        print(now, user.telegram_id, 'получил сообщение об открытии Острова Ада')
    elif now == '23:55':
        await mybot.send_message(user.telegram_id, 'Злая энергия Острова Ада начнет убивать через 5 минут')
        print(now, user.telegram_id, 'получил сообщение о закрытии Острова Ада')
    else:
        print(now, 'Неподходящее время для Острова Ада')
