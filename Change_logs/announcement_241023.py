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
        text = 'Вечера, друзья!\n' \
               '\n' \
               'Иннова выкатила патчноут с завтрашним обновлением Seven Sings - ' \
               'https://ru.4game.com/patchnotes/lineage2essence/8041/\n' \
               'Там что-то на богатом про 6-е куклы и новые цацки.\n' \
               'Можете в последний раз пробежаться по соло боссикам - больше вы их не увидите 🙈\n' \
               'Так же завтра завершается календарь, последний шанс потратить монетки и забрать оставшиеся награды.\n' \
               '\n' \
               '- добавила команду /feedback - можно оставить отзыв прямо в боте. ' \
               'Принимаются только восхваления и пожелания, все остальное можете писать Громе, туда можно\n' \
               '- будет убрана команда /soloraidboss во время профилактики\n' \
               '\n' \
               '~ ваша kobatoha'
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
