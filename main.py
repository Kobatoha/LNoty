from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Setting, User
from aiocron import crontab
import asyncio
from datetime import datetime

from Events.soloraidboss import soloraidboss_notification_wrapper, about_soloraidboss, set_soloraidboss, remove_soloraidboss
from Events.kuka import kuka_notification_wrapper, about_kuka, set_kuka, remove_kuka
from Events.loa import loa_notification_wrapper, about_loa, set_loa, remove_loa
from Events.fortress import fortress_notification_wrapper, about_fortress, set_fortress, remove_fortress
from Events.frost import frost_notification_wrapper, about_frost, set_frost, remove_frost
from Events.olympiad import olympiad_notification_wrapper, about_olympiad, set_olympiad, remove_olympiad
from Events.balok import balok_notification_wrapper, about_balok, set_balok, remove_balok
from Events.hellbound import hellbound_notification_wrapper, about_hellbound, set_hellbound, remove_hellbound
from Events.siege import siege_notification_wrapper, about_siege, set_siege, remove_siege
from Events.primetime import primetime_notification_wrapper, about_primetime, set_primetime, remove_primetime
from Events.purge import purge_notification_wrapper, about_purge, set_purge, remove_purge

#from Events.watermelon import watermelon_notification_wrapper, about_event, set_event, remove_event
from Events.event_pass import about_event, set_event, remove_event


from command_stop import stop, yes_stop, no_stop
from Events.fulltime import about_time, fulltime, hardworker_time

# /start, /stop, /about, /help, /mysettings, /time
# /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olympiad
# /hellbound, /antharas - skip, /siege, /primetime, /purge, /event

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# CUSTOM EVENT SETTINGS
dp.register_message_handler(about_event, commands=['event'])
dp.register_callback_query_handler(set_event, text_contains='setevent')
dp.register_callback_query_handler(remove_event, text_contains='removeevent')

# REGULAR SETTINGS
dp.register_message_handler(stop, commands=['stop'])
dp.register_callback_query_handler(yes_stop, text_contains='yes_stop')
dp.register_callback_query_handler(no_stop, text_contains='no_stop')

dp.register_message_handler(about_time, commands=['time'])
dp.register_callback_query_handler(fulltime, text_contains='fulltime')
dp.register_callback_query_handler(hardworker_time, text_contains='hardworkertime')

dp.register_message_handler(about_balok, commands=['balok'])
dp.register_callback_query_handler(set_balok, text_contains='setbalok')
dp.register_callback_query_handler(remove_balok, text_contains='removebalok')

dp.register_message_handler(about_fortress, commands=['fortress'])
dp.register_callback_query_handler(set_fortress, text_contains='setfortress')
dp.register_callback_query_handler(remove_fortress, text_contains='removefortress')

dp.register_message_handler(about_frost, commands=['frost'])
dp.register_callback_query_handler(set_frost, text_contains='setfrost')
dp.register_callback_query_handler(remove_frost, text_contains='removefrost')

dp.register_message_handler(about_hellbound, commands=['hellbound'])
dp.register_callback_query_handler(set_hellbound, text_contains='sethellbound')
dp.register_callback_query_handler(remove_hellbound, text_contains='removehellbound')

dp.register_message_handler(about_kuka, commands=['kuka'])
dp.register_callback_query_handler(set_kuka, text_contains='setkuka')
dp.register_callback_query_handler(remove_kuka, text_contains='removekuka')

dp.register_message_handler(about_loa, commands=['loa'])
dp.register_callback_query_handler(set_loa, text_contains='setloa')
dp.register_callback_query_handler(remove_loa, text_contains='removeloa')

dp.register_message_handler(about_olympiad, commands=['olympiad'])
dp.register_callback_query_handler(set_olympiad, text_contains='setolympiad')
dp.register_callback_query_handler(remove_olympiad, text_contains='removeolympiad')

dp.register_message_handler(about_purge, commands=['purge'])
dp.register_callback_query_handler(set_purge, text_contains='setpurge')
dp.register_callback_query_handler(remove_purge, text_contains='removepurge')

dp.register_message_handler(about_primetime, commands=['primetime'])
dp.register_callback_query_handler(set_primetime, text_contains='setprimetime')
dp.register_callback_query_handler(remove_primetime, text_contains='removeprimetime')

dp.register_message_handler(about_siege, commands=['siege'])
dp.register_callback_query_handler(set_siege, text_contains='setsiege')
dp.register_callback_query_handler(remove_siege, text_contains='removesiege')

dp.register_message_handler(about_soloraidboss, commands=['soloraidboss'])
dp.register_callback_query_handler(set_soloraidboss, text_contains='setsolorb')
dp.register_callback_query_handler(remove_soloraidboss, text_contains='removesolorb')


# GENERAL SETTINGS
@dp.message_handler(commands=['mysettings'])
async def get_settings(message: types.Message):
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    if user:
        await message.answer(
            'Установленные настройки:\n'
            '\n'
            f'Круглосуточное оповещение - {setting.fulltime}\n'
            f'Арбузный сезон (ивент) - {setting.event}\n'
            f'Одиночные РБ - {setting.soloraidboss}\n'
            f"Кука и Джисра - {setting.kuka}\n"
            f"Логово Антараса - {setting.loa}\n"
            f"Замок Монарха Льда - {setting.frost}\n"
            f"Крепость Орков - {setting.fortress}\n"
            f"Битва с Валлоком - {setting.balok}\n"
            f"Всемирная Олимпиада - {setting.olympiad}\n"
            f"Остров Ада - {setting.hellbound}\n"
            f"Осада Гирана - {setting.siege}\n"
            f"Хот-тайм Зачистки - {setting.primetime}\n"
            f"Зачистка - {setting.purge}")
    else:
        await message.answer('Пожалуйста, вернитесь к /start')

    session.close()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    now = datetime.now().strftime('%H:%M')
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        print(now, 'Добавление нового пользователя...')
        user = User(telegram_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
        setting = Setting(id_user=user.telegram_id)
        session.add(setting)
        session.commit()
        print(now, user.telegram_id, user.username, '- добавлен новый пользователь')

    else:
        user.upd_date = datetime.today()
        session.commit()
        if not user.username:  # если username еще не указан
            user.username = message.from_user.username  # обновляем username
            session.commit()
            print(now, user.telegram_id, user.username, '- username добавлен')
        else:
            print(now, user.telegram_id, user.username, '- уже добавлен')
    session.close()
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'В Меню ты найдешь все доступные команды.\n'
                         'Так же этот список можно вызвать командой /help\n' 
                         'Бот по-дефолту работает в работяжном режиме с 8:00 до 23:00,'
                         ' изменить эту настройку можно по команде /time\n'
                         '\n'
                         'Выбирай интересующую активность и жми "Установить оповещение".'
                         ' В таком случае тебе будут приходить уведомления за 5 минут'
                         ' до начала события.\n'
                         '\n'
                         'За это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.')


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer('Приветствую :)'
                         ' Я - Kobatoha, и я создала этого бота для вас, мои маленькие любители l2essence!'
                         ' Мы поможем не пропустить игровые активности.\n'
                         'Бот создан на добровольных началах, поэтому он свободен и независим.'
                         ' Есть идеи и предложения по улучшению бота? Велком - kobatoha@yandex.ru\n'
                         'Или ищите меня на Lavender под ником vsenaprasno')


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
                         '/event - Арбузный сезон (до 02.08)\n'
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

    # Запускаем event в ежедневно в 10:55
    #crontab('56 10 * * *', func=watermelon_notification_wrapper)

    # Запускаем event в ежедневно в 20:56
    #crontab('56 20 * * *', func=watermelon_notification_wrapper)


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
