import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import RuoffBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN, test_token
from aiogram.utils.exceptions import BotBlocked

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


bigwar_menu_text = 'Раздел для БигВара - уведомления за 15 минут до респа (Тои - за 20 минут):\n' \
                    '\n' \
                    '/bg_toi - Башня Дерзости 15:00 | 21:00 [ежедневно]\n' \
                    '/bg_gardens - Забытый Сад 23:00 [ежедневно]\n' \
                    '/bg_pagan - Языческий Храм 22:00 [пятница]\n' \
                    '/bg_kelbim - Крепость Кельбима 22:00 [пятница]\n' \
                    '/bg_antharas - Битва с Антарасом 22:00 [воскресенье]\n' \
                    '/bg_hellbound - Остров Ада 11:00 | 22:00 | 23:00 [суббота]\n' \
                    '/bg_chaotic - Хаотический Босс 20:00 [ежедневно]\n' \
                    '/bg_lilith - Лилит 19:00 [понедельник, четверг]\n' \
                    '/bg_anakim - Анаким 19:00 [вторник, пятница]\n' \
                    '/bg_gord - Горд 21:00 [ежедневно]\n' \
                    '/bg_frost - Замок Монарха Льда 21:30 | 22:00 [вторник, четверг]\n' \
                    '/bg_loa - Логово Антараса 22:00 [понедельник, среда]'


# [BIGWAR]
@dp.message_handler(commands=['bigwar'])
async def bigwar_menu(message: types.CallbackQuery):
    try:
        now = datetime.now().strftime('%H:%M')
        session = Session()
        bg_user = session.query(RuoffBigWar).filter_by(id_user=message.from_user.id).first()
        if not bg_user:
            print(now, 'Добавление нового BIGWAR пользователя...')
            bg_user = RuoffBigWar(id_user=message.from_user.id)
            session.add(bg_user)
            session.commit()
        session.close()

        await message.answer(text=bigwar_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[BIGWAR] {message.from_user.id} - '
                                      f'Произошла ошибка в функции bigwar_menu: {e}')
