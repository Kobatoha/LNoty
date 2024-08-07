import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime, timedelta
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# celestial tower buttons
inline_celestial_tower_buttons = types.InlineKeyboardMarkup()

set_button = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_set_celestial_tower')
remove_button = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_remove_celestial_tower')

inline_celestial_tower_buttons.add(set_button, remove_button)


# celestial tower SETTINGS
@dp.message_handler(commands=['celestial_tower'])
async def about_celestial_tower(message: types.Message):
    await message.answer('Небесная Башня - всемирная зона для персонажей 90 уровня и выше.\n'
                         'Хороший опыт и фарм адены. Открывается каждые 3 недели (после Языческого и Кельбима).\n'
                         'Из интересного - в пятницу с 21:00 до 23:59 появляются особые монстры, с которых сыпятся '
                         'перья и небесные талисманы. '
                         'Перья можно использовать в особом создании в крафте Небесных Талисманов. '
                         '\n', reply_markup=inline_celestial_tower_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_celestial_tower'))
async def set_celestial_tower(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.celestial_tower = True
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение для Небесной Башни установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_celestial_tower'))
async def remove_celestial_tower(callback_query: types.CallbackQuery):
    with Session() as session:

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
        setting.celestial_tower = False
    
        session.commit()
    
        user.upd_date = datetime.today()
        session.commit()

    await callback_query.message.answer('Оповещение для Небесной Башни убрано')
    await callback_query.answer()


async def celestial_tower_notification_wrapper():
    with Session() as session:
        users = session.query(User).all()
        for user in users:
    
            setting = session.query(EssenceSetting).filter_by(id_user=user.telegram_id).first()
            if setting.celestial_tower is True:
                await celestial_tower_notification(user)


async def celestial_tower_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    today = datetime.now().strftime('%Y-%m-%d')
    celestial_tower_time = ['20:55']
    celestial_tower_fridays = []
    
    start_date = datetime(2024, 6, 7)
    
    first_friday = start_date
    while first_friday.weekday() != 4:
        first_friday += timedelta(days=1)
    
    current_date = first_friday
    while len(celestial_tower_fridays) < 15:
        celestial_tower_fridays.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=21)

    try:
        if today in celestial_tower_fridays and now in celestial_tower_time:
            await mybot.send_message(user.telegram_id, 'Небесная Башня начнет терять перья через 5 минут.')
            print(now, user.telegram_id, user.username, ' получил сообщение о Вторжении')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
