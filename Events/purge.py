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


async def purge_notification_wrapper():

    session = Session()
    users = session.query(User).all()

    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.purge is True:
            now = datetime.now().strftime('%H:%M')
            print(now, user.telegram_id, 'подходит под условия оповещения сбора Зачистки')
            await purge_notification(user)
    session.close()


async def purge_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    if now == '22:50':
        await mybot.send_message(user.telegram_id, '🍾 Скорее соберите Зачистку :)')
        print(now, user.telegram_id, 'получил сообщение об сборе Зачистке')
    else:
        print(now, 'Неподходящее время для сбора Зачистки')
