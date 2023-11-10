import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import Setting
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
        text = 'Всем привет!\n' \
               '\n' \
               'Сегодня будет кратко:\n' \
               '- добавила раздел /bigwar, ведь мж перчатки сами себя не сфармят.\n' \
               '- добавила команду /dream (Грезы), день выбираем, а время надо вводить самостоятельно\n' \
               '- добавила команды /valakas и /frintezza\n' \
               '\n' \
               'п.с. спасибо за обратную связь, мне очень приятно) Все прочла, буду делать по мере возможности\n' \
               '~ все еще ваша kobatoha'
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
