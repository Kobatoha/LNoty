from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting, RuoffCustomSetting, RuoffClanDangeon
from aiocron import crontab
import asyncio
from datetime import datetime

from Ruoff.events import *
#from Ruoff.options import *

from Commands.about import about
from Commands.donate import donate, donate_sberbank, donate_ethereum, donate_bitcoin, donate_tinkoff
from Commands.help import help
from Commands.mysettings import mysettings
from Commands.options import options_menu
from Commands.server import choice_server, ruoff, expanse
from Commands.started import start
from Commands.stopped import stop, yes_stop, no_stop

# general settings: /start, /stop, /about, /time, /server
# servers settings: /help, /mysettings
# ruoff: /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olympiad, /hellbound, /siege, /primetime, /purge,
# /event
# expanse:

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# GENERAL SETTINGS
dp.register_message_handler(choice_server, commands=['server'])
dp.register_callback_query_handler(ruoff, text_contains='ruoff_server')
dp.register_callback_query_handler(expanse, text_contains='expanse')

dp.register_message_handler(mysettings, commands=['mysettings'])

dp.register_message_handler(start, commands=['start'])

dp.register_message_handler(about, commands=['about'])

dp.register_message_handler(help, commands=['help'])

dp.register_message_handler(options_menu, commands=['options'])

dp.register_message_handler(donate, commands=['donate'])
dp.register_callback_query_handler(donate_sberbank, text_contains='sberbank')
dp.register_callback_query_handler(donate_tinkoff, text_contains='tinkoff')
dp.register_callback_query_handler(donate_bitcoin, text_contains='bitcoin')
dp.register_callback_query_handler(donate_ethereum, text_contains='ethereum')

dp.register_message_handler(stop, commands=['stop'])
dp.register_callback_query_handler(yes_stop, text_contains='yes_stop')
dp.register_callback_query_handler(no_stop, text_contains='no_stop')

# CUSTOM EVENT SETTINGS
dp.register_message_handler(about_event, commands=['event'])
dp.register_callback_query_handler(set_event, text_contains='ruoff_setevent')
dp.register_callback_query_handler(remove_event, text_contains='ruoff_removeevent')

# REGULAR RUOFF SETTINGS
dp.register_message_handler(about_time, commands=['time'])
dp.register_callback_query_handler(fulltime, text_contains='ruoff_fulltime')
dp.register_callback_query_handler(hardworker_time, text_contains='ruoff_hardworkertime')

dp.register_message_handler(about_balok, commands=['balok'])
dp.register_callback_query_handler(set_balok, text_contains='ruoff_setbalok')
dp.register_callback_query_handler(remove_balok, text_contains='ruoff_removebalok')

dp.register_message_handler(about_fortress, commands=['fortress'])
dp.register_callback_query_handler(set_fortress, text_contains='ruoff_setfortress')
dp.register_callback_query_handler(remove_fortress, text_contains='ruoff_removefortress')

dp.register_message_handler(about_frost, commands=['frost'])
dp.register_callback_query_handler(set_frost, text_contains='ruoff_setfrost')
dp.register_callback_query_handler(remove_frost, text_contains='ruoff_removefrost')

dp.register_message_handler(about_hellbound, commands=['hellbound'])
dp.register_callback_query_handler(set_hellbound, text_contains='ruoff_sethellbound')
dp.register_callback_query_handler(remove_hellbound, text_contains='ruoff_removehellbound')

dp.register_message_handler(about_kuka, commands=['kuka'])
dp.register_callback_query_handler(set_kuka, text_contains='ruoff_setkuka')
dp.register_callback_query_handler(remove_kuka, text_contains='ruoff_removekuka')

dp.register_message_handler(about_loa, commands=['loa'])
dp.register_callback_query_handler(set_loa, text_contains='ruoff_setloa')
dp.register_callback_query_handler(remove_loa, text_contains='ruoff_removeloa')

dp.register_message_handler(about_olympiad, commands=['olympiad'])
dp.register_callback_query_handler(set_olympiad, text_contains='ruoff_setolympiad')
dp.register_callback_query_handler(remove_olympiad, text_contains='ruoff_removeolympiad')

dp.register_message_handler(about_purge, commands=['purge'])
dp.register_callback_query_handler(set_purge, text_contains='ruoff_setpurge')
dp.register_callback_query_handler(remove_purge, text_contains='ruoff_removepurge')

dp.register_message_handler(about_primetime, commands=['primetime'])
dp.register_callback_query_handler(set_primetime, text_contains='ruoff_setprimetime')
dp.register_callback_query_handler(remove_primetime, text_contains='ruoff_removeprimetime')

dp.register_message_handler(about_siege, commands=['siege'])
dp.register_callback_query_handler(set_siege, text_contains='ruoff_setsiege')
dp.register_callback_query_handler(remove_siege, text_contains='ruoff_removesiege')

dp.register_message_handler(about_soloraidboss, commands=['soloraidboss'])
dp.register_callback_query_handler(set_soloraidboss, text_contains='ruoff_setsolorb')
dp.register_callback_query_handler(remove_soloraidboss, text_contains='ruoff_removesolorb')


# GENERAL SETTINGS
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Бегите, гoлубцы!')


async def crontab_notifications():
    # Запускаем soloraidboss каждый час в :55
    crontab('55 */2 * * *', func=soloraidboss_notification_wrapper)

    # Запускаем kuka каждый час в :45
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

    # Запускаем hellbound открытие в субботу в 09:55
    crontab('55 09 * * 6', func=hellbound_notification_wrapper)

    # Запускаем hellbound открытие в субботу в 09:55
    crontab('55 17 * * 6', func=hellbound_notification_wrapper)

    # Запускаем hellbound закрытие в субботу в 23:55
    crontab('59 22 * * 6', func=hellbound_notification_wrapper)

    # Запускаем siege в воскресенье в 20:25
    crontab('25 20 * * 7', func=siege_notification_wrapper)

    # Запускаем primetime ежедневно в 11:55
    crontab('56 11 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 13:55
    crontab('56 13 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 18:56
    crontab('56 18 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 22:56
    crontab('56 22 * * *', func=primetime_notification_wrapper)

    # Запускаем purge в воскресенье в 23:30
    crontab('50 22 * * 7', func=purge_notification_wrapper)

    # Запускаем event ежедневно в 10:56
    #crontab('56 10 * * *', func=rescue_notification_wrapper)

    # Запускаем event ежедневно в 20:56
    #crontab('56 20 * * *', func=rescue_notification_wrapper)


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
