from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.Base import Base
from DataBase.User import User
from DataBase.Ruoff import Setting, RuoffCustomSetting, RuoffClanDangeon
from DataBase.Feedback import Feedback
from aiocron import crontab
import asyncio
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Ruoff.events import *
from Ruoff.options import *
from Ruoff.bigwars import *

from Commands.about import about
from Commands.donate import donate, donate_sberbank, donate_ethereum, donate_bitcoin, donate_tinkoff
from Commands.help import help
from Commands.mysettings import mysettings
from Commands.options import options_menu
from Commands.server import choice_server, ruoff, expanse
from Commands.started import start
from Commands.stopped import stop, yes_stop, no_stop
from Commands.feedback import feedback, add_feedback, cancel_add_feedback, cancel_feedback, save_feedback, FeedbackState

# general settings: /start, /stop, /about, /time, /server
# servers settings: /help, /mysettings
# ruoff: /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olympiad, /hellbound, /siege, /primetime, /purge,
# /event, /calendar
# expanse:

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

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

dp.register_message_handler(feedback, commands=['feedback'])                                    # [FEEDBACK]
dp.register_callback_query_handler(cancel_feedback, text_contains='back_feedback')              # [CANCEL FEEDBACK]
dp.register_callback_query_handler(add_feedback, text_contains='add_feedback')                  # [ADD FEEDBACK]
dp.register_message_handler(save_feedback, state=FeedbackState.waiting_for_feedback)            # [SAVE FEEDBACK]
dp.register_callback_query_handler(cancel_add_feedback,
                                   text_contains='cancel_add_feedback',
                                   state=FeedbackState.waiting_for_feedback)                    # [CANCEL ADD FEEDBACK]

# CUSTOM EVENT SETTINGS
dp.register_message_handler(about_event, commands=['event'])
dp.register_callback_query_handler(set_event, text_contains='ruoff_set_event')
dp.register_callback_query_handler(remove_event, text_contains='ruoff_remove_event')

dp.register_message_handler(about_calendar, commands=['calendar'])
dp.register_callback_query_handler(set_calendar, text_contains='ruoff_set_calendar')
dp.register_callback_query_handler(remove_calendar, text_contains='ruoff_remove_calendar')

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

# dp.register_message_handler(about_soloraidboss, commands=['soloraidboss'])
# dp.register_callback_query_handler(set_soloraidboss, text_contains='ruoff_setsolorb')
# dp.register_callback_query_handler(remove_soloraidboss, text_contains='ruoff_removesolorb')

# [DREAM]
dp.register_message_handler(about_dream, commands=['dream'])
dp.register_callback_query_handler(set_dream, text_contains='ruoff_option_set_dream')
dp.register_callback_query_handler(cancel_to_set_dream, text_contains='ruoff_option_cancel_to_set_dream')

dp.register_callback_query_handler(set_dream_day, text_contains='ruoff_option_set_day_dream')
dp.register_callback_query_handler(save_dream_day, lambda c: c.data.startswith('add_dream_'))
dp.register_callback_query_handler(cancel_to_set_dream_day, text_contains='ruoff_option_cancel_to_set_dream')

dp.register_callback_query_handler(set_dream_time, text_contains='ruoff_option_set_time_dream')
dp.register_message_handler(save_dream_time, state=DreamTime.waiting_for_dream_time)
dp.register_callback_query_handler(cancel_to_set_dream_time, text_contains='ruoff_option_cancel_to_set_dream',
                                   state=DreamTime.waiting_for_dream_time)

dp.register_callback_query_handler(remove_dream, text_contains='ruoff_option_remove_dream')

# [VALAKAS]
dp.register_message_handler(about_valakas, commands=['valakas'])
dp.register_callback_query_handler(set_valakas, text_contains='ruoff_option_set_valakas')
dp.register_callback_query_handler(cancel_to_set_valakas, text_contains='ruoff_option_cancel_to_set_valakas')

dp.register_callback_query_handler(set_valakas_day, text_contains='ruoff_option_set_day_valakas')
dp.register_callback_query_handler(save_valakas_day, lambda c: c.data.startswith('add_valakas_'))
dp.register_callback_query_handler(cancel_to_set_valakas_day, text_contains='ruoff_option_cancel_to_set_valakas')

dp.register_callback_query_handler(set_valakas_time, text_contains='ruoff_option_set_time_valakas')
dp.register_message_handler(save_valakas_time, state=ValakasTime.waiting_for_valakas_time)
dp.register_callback_query_handler(cancel_to_set_valakas_time, text_contains='ruoff_option_cancel_to_set_valakas',
                                   state=ValakasTime.waiting_for_valakas_time)

dp.register_callback_query_handler(remove_valakas, text_contains='ruoff_option_remove_valakas')

# [FRINTEZZA]
dp.register_message_handler(about_frintezza, commands=['frintezza'])
dp.register_callback_query_handler(set_frintezza, text_contains='ruoff_option_set_frintezza')
dp.register_callback_query_handler(cancel_to_set_frintezza, text_contains='ruoff_option_cancel_to_set_frintezza')

dp.register_callback_query_handler(set_frintezza_day, text_contains='ruoff_option_set_day_frintezza')
dp.register_callback_query_handler(save_frintezza_day, lambda c: c.data.startswith('add_frintezza_'))
dp.register_callback_query_handler(cancel_to_set_frintezza_day, text_contains='ruoff_option_cancel_to_set_frintezza')

dp.register_callback_query_handler(set_frintezza_time, text_contains='ruoff_option_set_time_frintezza')
dp.register_message_handler(save_frintezza_time, state=FrintezzaTime.waiting_for_frintezza_time)
dp.register_callback_query_handler(cancel_to_set_frintezza_time, text_contains='ruoff_option_cancel_to_set_frintezza',
                                   state=FrintezzaTime.waiting_for_frintezza_time)

dp.register_callback_query_handler(remove_frintezza, text_contains='ruoff_option_remove_frintezza')

# [BIGWAR]
dp.register_message_handler(bigwar_menu, commands=['bigwar'])

dp.register_message_handler(about_bigwar_toi, commands=['bigwar_toi'])
dp.register_callback_query_handler(set_bigwar_toi, text_contains='ruoff_set_bigwar_toi')
dp.register_callback_query_handler(remove_bigwar_toi, text_contains='ruoff_remove_bigwar_toi')

dp.register_message_handler(about_bigwar_gardens, commands=['bigwar_gardens'])
dp.register_callback_query_handler(set_bigwar_gardens, text_contains='ruoff_set_bigwar_gardens')
dp.register_callback_query_handler(remove_bigwar_gardens, text_contains='ruoff_remove_bigwar_gardens')

dp.register_message_handler(about_bigwar_pagan, commands=['bigwar_pagan'])
dp.register_callback_query_handler(set_bigwar_pagan, text_contains='ruoff_set_bigwar_pagan')
dp.register_callback_query_handler(remove_bigwar_pagan, text_contains='ruoff_remove_bigwar_pagan')

dp.register_message_handler(about_bigwar_kelbim, commands=['bigwar_kelbim'])
dp.register_callback_query_handler(set_bigwar_kelbim, text_contains='ruoff_set_bigwar_kelbim')
dp.register_callback_query_handler(remove_bigwar_kelbim, text_contains='ruoff_remove_bigwar_kelbim')

dp.register_message_handler(about_bigwar_antharas, commands=['bigwar_antharas'])
dp.register_callback_query_handler(set_bigwar_antharas, text_contains='ruoff_set_bigwar_antharas')
dp.register_callback_query_handler(remove_bigwar_antharas, text_contains='ruoff_remove_bigwar_antharas')

dp.register_message_handler(about_bigwar_hellbound, commands=['bigwar_hellbound'])
dp.register_callback_query_handler(set_bigwar_hellbound, text_contains='ruoff_set_bigwar_hellbound')
dp.register_callback_query_handler(remove_bigwar_hellbound, text_contains='ruoff_remove_bigwar_hellbound')

dp.register_message_handler(about_bigwar_chaotic, commands=['bigwar_chaotic'])
dp.register_callback_query_handler(set_bigwar_chaotic, text_contains='ruoff_set_bigwar_chaotic')
dp.register_callback_query_handler(remove_bigwar_chaotic, text_contains='ruoff_remove_bigwar_chaotic')

dp.register_message_handler(about_bigwar_lilith, commands=['bigwar_lilith'])
dp.register_callback_query_handler(set_bigwar_lilith, text_contains='ruoff_set_bigwar_lilith')
dp.register_callback_query_handler(remove_bigwar_lilith, text_contains='ruoff_remove_bigwar_lilith')

dp.register_message_handler(about_bigwar_anakim, commands=['bigwar_anakim'])
dp.register_callback_query_handler(set_bigwar_anakim, text_contains='ruoff_set_bigwar_anakim')
dp.register_callback_query_handler(remove_bigwar_anakim, text_contains='ruoff_remove_bigwar_anakim')

dp.register_message_handler(about_bigwar_gord, commands=['bigwar_gord'])
dp.register_callback_query_handler(set_bigwar_gord, text_contains='ruoff_set_bigwar_gord')
dp.register_callback_query_handler(remove_bigwar_gord, text_contains='ruoff_remove_bigwar_gord')


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
    bigwar_gord_notification_wrapper
    ]


async def crontab_notifications():
    # Запускаем soloraidboss каждый час в :55
    # crontab('55 */2 * * *', func=soloraidboss_notification_wrapper)

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

    # Запускаем hellbound цитадель в субботу в 09:55
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

    # Запускаем bigwar_pagan в friday в 21:45
    crontab('45 21 * * 5', func=bigwar_pagan_notification_wrapper)

    # Запускаем bigwar_pagan в friday в 21:45
    crontab('45 21 * * 5', func=bigwar_kelbim_notification_wrapper)

    # Запускаем bigwar_antharas в воскресенье в 21:45
    crontab('45 21 * * 7', func=bigwar_antharas_notification_wrapper)

    # Запускаем bigwar_hellbound в субботу
    crontab('* * * * 6', func=bigwar_hellbound_notification_wrapper)

    # Запускаем bigwar_lilith в понедельник и четверг в 18:45
    crontab('45 18 * * 1,4', func=bigwar_lilith_notification_wrapper)

    # Запускаем bigwar_anakim в вторник и пятница в 18:45
    crontab('45 18 * * 2,5', func=bigwar_anakim_notification_wrapper)

    # Запускаем calendar ежедневно в 21:10
    crontab('10 21 * * *', func=calendar_notification_wrapper)

    for func in functions_to_crontab:
        crontab('* * * * *', func=func)

    # Запускаем event ежедневно в 10:56
    # crontab('56 10 * * *', func=rescue_notification_wrapper)

    # Запускаем event ежедневно в 21:00
    # crontab('0 21 * * *', func=tomb_notification_wrapper)


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
