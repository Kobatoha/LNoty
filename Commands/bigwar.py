import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


bigwar_menu_text = '🌈🌈 Раздел для БигВара - уведомления за 15 минут до респа (Тои - за 20 минут):\n' \
                    '\n' \
                    '/bigwar_toi - Башня Дерзости 15:00 | 21:00 [ежедневно]\n' \
                    '/bigwar_gardens - Забытый Сад 23:00 [ежедневно]\n' \
                    '/bigwar_pagan - Языческий Храм/Крепость Кельбима 22:00 [пятница]\n' \
                    '/bigwar_antharas - Битва с Антарасом 22:00 [воскресенье]\n' \
                    '/bigwar_hellbound - Остров Ада 11:00 | 21:00 | 22:00 [суббота]\n' \
                    '/bigwar_chaotic - Хаотический Босс 20:00 [ежедневно]\n' \
                    '/bigwar_lilith - Лилит 19:00 [понедельник, четверг]\n' \
                    '/bigwar_anakim - Анаким 19:00 [вторник, пятница]\n' \
                    '/bigwar_gord - Горд 21:00 [ежедневно]\n' \
                    '/bigwar_frost - Замок Монарха Льда 21:30 | 22:00 [вторник, четверг]\n' \
                    '/bigwar_loa - Логово Антараса 22:00 [понедельник, среда]' \
                    '/bigwar_jakal - Секретная Крепость Фавносов 23:00 [ежедневно]'


# [BIGWAR]
@dp.message_handler(commands=['bigwar'])
async def bigwar_menu(message: types.CallbackQuery):
    try:
        now = datetime.now().strftime('%H:%M')
        session = Session()
        bg_user = session.query(EssenceBigWar).filter_by(id_user=message.from_user.id).first()
        if not bg_user:
            print(now, 'Добавление нового BIGWAR пользователя...')
            bg_user = EssenceBigWar(id_user=message.from_user.id)
            session.add(bg_user)
            session.commit()
        session.close()

        await message.answer(text=bigwar_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[BIGWAR] {message.from_user.id} - '
                                      f'Произошла ошибка в функции bigwar_menu: {e}')
