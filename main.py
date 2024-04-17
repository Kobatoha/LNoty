from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting, RuoffCustomSetting, RuoffClanDangeon
from DataBase.RaidBoss import RaidBoss
from DataBase.Feedback import Feedback
from aiocron import crontab
import asyncio
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Ruoff.handlers import *

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# GENERAL SETTINGS
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Бегите, гoлубцы!')


functions_to_crontab = [
    dream_notification_wrapper,
    valakas_notification_wrapper,
    frintezza_notification_wrapper,
    bigwar_toi_notification_wrapper,
    bigwar_gardens_notification_wrapper,
    bigwar_chaotic_notification_wrapper,
    bigwar_gord_notification_wrapper,
    invasion_notification_wrapper,
    festival_notification_wrapper,
    gardens_notification_wrapper,
    goddard_notification_wrapper,
    toi_notification_wrapper,
    training_notification_wrapper,
    transcendent_notification_wrapper  
    ]


async def crontab_notifications():
    # Запускаем kuka каждый четный час в :45
    crontab('45 */2 * * *', func=kuka_notification_wrapper)

    # Запускаем loa каждый понедельник и среду в 17:55
    crontab('55 17 * * 1,3', func=loa_notification_wrapper)

    # Запускаем frost каждый вторник и четверг в 19:55
    crontab('55 17 * * 2,4', func=frost_notification_wrapper)

    # Запускаем fortress ежедневно в 19:55
    crontab('55 19 * * *', func=fortress_notification_wrapper)

    # Запускаем balok ежедневно, кроме воскресенья в 20:25
    crontab('25 20 * * 1,2,3,4,5,6', func=balok_notification_wrapper)

    # Запускаем olympiad по будням в 21:25
    crontab('25 21 * * 1,2,3,4,5', func=olympiad_notification_wrapper)

    # Запускаем hellbound открытие в субботу в 09:55 17:55 23:55
    crontab('55 09,17,23 * * 6', func=hellbound_notification_wrapper)

    # Запускаем siege в воскресенье в 20:25
    crontab('25 20 * * 7', func=siege_notification_wrapper)

    # Запускаем primetime ежедневно в 11:55 13:55 18:55 22:55
    crontab('55 11,13,18,22 * * *', func=primetime_notification_wrapper)

    # Запускаем purge в воскресенье в 23:30
    crontab('50 22 * * 7', func=purge_notification_wrapper)

    # Запускаем bigwar_pagan в friday в 21:45
    crontab('45 21 * * 5', func=bigwar_pagan_notification_wrapper)

    # Запускаем bigwar_antharas в воскресенье в 21:45
    crontab('45 21 * * 7', func=bigwar_antharas_notification_wrapper)

    # Запускаем bigwar_hellbound в субботу
    crontab('* * * * 6', func=bigwar_hellbound_notification_wrapper)

    # Запускаем bigwar_lilith в понедельник и четверг в 18:45
    crontab('45 18 * * 1,4', func=bigwar_lilith_notification_wrapper)

    # Запускаем bigwar_anakim в вторник и пятница в 18:45
    crontab('45 18 * * 2,5', func=bigwar_anakim_notification_wrapper)

    # Запускаем bigwar_frost в вторник и четверг в 21:15 и в 21:45
    crontab('15,45 21 * * 2,4', func=bigwar_frost_notification_wrapper)

    # Запускаем bigwar_loa в понедельник и среда в 21:45
    crontab('45 21 * * 1,3', func=bigwar_loa_notification_wrapper)

    # Запускаем calendar ежедневно в 21:10
    #crontab('10 21 * * *', func=calendar_notification_wrapper)

    # Запускаем event ежедневно в 11:25 и 21:25
    #crontab('25 11,21 * * *', func=fantasyisle_notification_wrapper)

    # Запускаем keber каждый час в :58
    crontab('58 * * * *', func=keber_notification_wrapper)

    for func in functions_to_crontab:
        crontab('* * * * *', func=func)


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M:%S')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
