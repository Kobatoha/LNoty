from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting
from aiocron import crontab
import asyncio
from datetime import datetime

from Ruoff.events import *

from Commands.server import choice_server, ruoff, expanse
from Commands.stopped import stop, yes_stop, no_stop
from Commands.mysettings import mysettings
from Commands.started import start
from Commands.about import about

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
dp.register_callback_query_handler(ruoff, text_contains='ruoff')
dp.register_callback_query_handler(expanse, text_contains='expanse')

dp.register_message_handler(mysettings, commands=['mysettings'])

dp.register_message_handler(start, commands=['start'])

dp.register_message_handler(about, commands=['about'])

dp.register_message_handler(stop, commands=['stop'])
dp.register_callback_query_handler(yes_stop, text_contains='yes_stop')
dp.register_callback_query_handler(no_stop, text_contains='no_stop')

# CUSTOM EVENT SETTINGS
dp.register_message_handler(about_event, commands=['event'])
dp.register_callback_query_handler(set_event, text_contains='ruoffsetevent')
dp.register_callback_query_handler(remove_event, text_contains='ruoffremoveevent')

# REGULAR RUOFF SETTINGS
dp.register_message_handler(about_time, commands=['time'])
dp.register_callback_query_handler(fulltime, text_contains='ruofffulltime')
dp.register_callback_query_handler(hardworker_time, text_contains='ruoffhardworkertime')

dp.register_message_handler(about_balok, commands=['balok'])
dp.register_callback_query_handler(set_balok, text_contains='ruoffsetbalok')
dp.register_callback_query_handler(remove_balok, text_contains='ruoffremovebalok')

dp.register_message_handler(about_fortress, commands=['fortress'])
dp.register_callback_query_handler(set_fortress, text_contains='ruoffsetfortress')
dp.register_callback_query_handler(remove_fortress, text_contains='ruoffremovefortress')

dp.register_message_handler(about_frost, commands=['frost'])
dp.register_callback_query_handler(set_frost, text_contains='ruoffsetfrost')
dp.register_callback_query_handler(remove_frost, text_contains='ruoffremovefrost')

dp.register_message_handler(about_hellbound, commands=['hellbound'])
dp.register_callback_query_handler(set_hellbound, text_contains='ruoffsethellbound')
dp.register_callback_query_handler(remove_hellbound, text_contains='ruoffremovehellbound')

dp.register_message_handler(about_kuka, commands=['kuka'])
dp.register_callback_query_handler(set_kuka, text_contains='ruoffsetkuka')
dp.register_callback_query_handler(remove_kuka, text_contains='ruoffremovekuka')

dp.register_message_handler(about_loa, commands=['loa'])
dp.register_callback_query_handler(set_loa, text_contains='ruoffsetloa')
dp.register_callback_query_handler(remove_loa, text_contains='ruoffremoveloa')

dp.register_message_handler(about_olympiad, commands=['olympiad'])
dp.register_callback_query_handler(set_olympiad, text_contains='ruoffsetolympiad')
dp.register_callback_query_handler(remove_olympiad, text_contains='ruoffremoveolympiad')

dp.register_message_handler(about_purge, commands=['purge'])
dp.register_callback_query_handler(set_purge, text_contains='ruoffsetpurge')
dp.register_callback_query_handler(remove_purge, text_contains='ruoffremovepurge')

dp.register_message_handler(about_primetime, commands=['primetime'])
dp.register_callback_query_handler(set_primetime, text_contains='ruoffsetprimetime')
dp.register_callback_query_handler(remove_primetime, text_contains='ruoffremoveprimetime')

dp.register_message_handler(about_siege, commands=['siege'])
dp.register_callback_query_handler(set_siege, text_contains='ruoffsetsiege')
dp.register_callback_query_handler(remove_siege, text_contains='ruoffremovesiege')

dp.register_message_handler(about_soloraidboss, commands=['soloraidboss'])
dp.register_callback_query_handler(set_soloraidboss, text_contains='ruoffsetsolorb')
dp.register_callback_query_handler(remove_soloraidboss, text_contains='ruoffremovesolorb')


# GENERAL SETTINGS
@dp.message_handler(commands=['help'])
async def helped(message: types.Message):
    await message.answer('Доступные команды:\n'
                         '\n'
                         '/start - запуск бота\n'
                         '/about - о боте\n'
                         '/mysettings - персональные настройки\n'
                         '/help - список команд\n'
                         '\n'
                         '/stop - отменить все оповещения\n'
                         '/time - установить время работы оповещений\n'
                         '\n'
                         '/event - в данный момент нет\n'
                         '/soloraidboss - Одиночные РБ\n'
                         '/kuka - Кука и Джисра\n'
                         '/loa - Логово Антараса\n'
                         '/frost - Замок Монарха Льда\n'
                         '/fortress - Крепость Орков\n'
                         '/balok - Битва с Валлоком\n'
                         '/olympiad - Всемирная Олимпиада\n'
                         '/hellbound - Остров Ада\n'
                         '/siege - Осада Гирана\n'
                         '\n'
                         '/primetime - Прайм Тайм Зачистки\n'
                         '/purge - Зачистка\n')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Бегите, глупцы!')


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


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
