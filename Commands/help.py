from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from aiocron import crontab
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

    text = 'Доступные команды:\n'\
           '\n'\
           '/start - запуск бота и выбор сервера\n'\
           '/about - о боте\n'\
           '/mysettings - персональные настройки\n'\
           '/help - список команд\n'\
           '/donate - разработчику на проездной Т_Т\n'\
           '/feedback - оставить предложение\n'\
           '\n'\
           '/stop - отменить все оповещения\n'\
           '\n'\
           '/time - установить время работы оповещений\n'\

    if user and user.server == 'ruoff':
        await message.answer(text + 
                             '/event - Храм Воды до 22 мая 2024\n'
                             '/festival - Секретная лавка\n'
                             '/calendar - идет, берем награды и радуемся\n'
                             '/kuka - Кука и Джисра\n'
                             '/keber - Кебер\n'
                             '/loa - Логово Антараса\n'
                             '/frost - Замок Монарха Льда\n'
                             '/fortress - Крепость Орков\n'
                             '/balok - Битва с Валлоком\n'
                             '/olympiad - Всемирная Олимпиада\n'
                             '/hellbound - Остров Ада\n'
                             '/siege - Осада Гирана\n'                             
                             '/primetime - Прайм Тайм Зачистки\n'
                             '/purge - Зачистка\n'
                             '/invasion - Вторжение\n'
                             '\n'
                             '/options - раздел ручных настроек (сады, ацтакан, грёзы и т.д.)\n'
                             '/bigwar - раздел для бигвара (респы рейд боссов)\n')
    elif user and user.server == 'legacy':
        await message.answer(text + 
                             '/frost - Замок Монарха Льда\n'
                             '/olympiad - Всемирная Олимпиада\n')

    session.close()
