# Аларм на каждого босса на корал за 5 минут до респа + список-порядок респа боссов +
# автоматический отчет времени -2 часа после убийства босса

import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.Base import Base
from DataBase.RaidBoss import RaidBoss
from DataBase.Ruoff import RuoffBigWar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# CORAL RAIDBOSSES buttons
inline_coral_raidboss_buttons = types.InlineKeyboardMarkup()

button_coral_set = types.InlineKeyboardButton(
    text='Установить оповещение CORAL',
    callback_data='ruoff_set_coral_raidboss')
button_coral_remove = types.InlineKeyboardButton(
    text='Убрать оповещение CORAL',
    callback_data='ruoff_remove_coral_raidboss')

inline_coral_raidboss_buttons.add(button_coral_set, button_coral_remove)


# CORAL RAIDBOSS SETTINGS
@dp.message_handler(commands=['raidboss_coral'])
async def about_coral_raidboss(message: types.Message):
    await message.answer('[BIGWAR] Рейдовые Боссы 80-го, 85-го, 90-го уровней - оповещения за 15 минут\n',
                         reply_markup=inline_coral_raidboss_buttons)


@dp.callback_query_handler(filters.Text(contains='ruoff_set_coral_raidboss'))
async def set_coral_raidbosses(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.coral = True
    session.commit()
    session.close()

    await callback_query.message.answer('[BIGWAR] CORAL Оповещения о Рейдовых Боссов установлены')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_remove_coral_raidboss'))
async def remove_coral_raidbosses(callback_query: types.CallbackQuery):
    session = Session()

    bg_user = session.query(RuoffBigWar).filter_by(id_user=callback_query.from_user.id).first()
    bg_user.coral = False
    session.commit()

    session.close()

    await callback_query.message.answer('[BIGWAR] CORAL Оповещения о Рейдовых Боссов убраны')
    await callback_query.answer()


async def bigwar_coral_raidbosses_notification_wrapper():

    session = Session()
    users = session.query(RuoffBigWar).all()
    for user in users:
        if user.coral is True:
            await bigwar_coral_raidbosses_notification(user)
    session.close()


async def bigwar_coral_raidbosses_notification(user: RuoffBigWar):
    now = datetime.now().strftime('%H:%M')
    try:
        with Session() as session:
            bosses = session.query(RaidBoss).all()
            for boss in bosses:
                # time за 15 минут до респа
                time_split = boss.coral_time.split(":")
                hours = int(time_split[0])
                minutes = int(time_split[1])

                # Subtract 15 minutes
                new_minutes = minutes - 15
                if new_minutes < 0:
                    hours -= 1
                    new_minutes += 60

                if hours < 0:
                    hours += 24

                boss_time = str(hours) + ':' + str(new_minutes)

                if now == boss_time:
                    await mybot.send_message(
                        user.id_user,
                        f'👀👀 [CORAL] {boss.name} появится через 15 минут, в {boss.coral_time}')
                    print(now, user.id_user, f'получил сообщение о [CORAL] {boss.name}')

                    new_coral_time = boss.coral_time + datetime.timedelta(hours=22)
                    print(new_coral_time)
                    boss.coral_time = new_coral_time.strftime("%H:%M")
                    print(boss.coral_time)
                    session.commit()

    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.id_user)
