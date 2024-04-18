import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


async def announcement():
    now = datetime.now().strftime('%H:%M')
    session = Session()
    users = session.query(User).all()
    for user in users:
        text = 'Привет! На наши сервера подвезли очередной календарь, поэтому такая молодец я сделала для вас' \
               ' напоминалочку, чтобы никто ничего не пропустил - /calendar\n' \
               'Так же напоминаю, что если у вас есть предложения или пожелания, то для связи есть почта ' \
               'kobatoha@yandex.ru' \
               '\n' \        
               'Всегда на страже вашего комфорта, kobatoha!'
        try:
            await mybot.send_message(text=text, chat_id=user.telegram_id)
            print(now, 'сообщение доставлено пользователю', user.telegram_id, user.username)
        except:
            print('[ERROR]', now, 'сообщение не может быть отправлено пользователю', user.telegram_id, user.username)
            continue


async def main():
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск announcement Lineage2Notifications')
    await announcement()


if __name__ == '__main__':
    asyncio.run(main())
    executor.start_polling(dp, skip_updates=True)
