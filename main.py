from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Setting, User
from aiocron import crontab
import asyncio
from datetime import datetime

from Events.soloraidboss import soloraidboss_notification_wrapper
from Events.kuka import kuka_notification_wrapper
from Events.loa import loa_notification_wrapper
from Events.fortress import fortress_notification_wrapper
from Events.frost import frost_notification_wrapper
from Events.olympiad import olympiad_notification_wrapper
from Events.balok import balok_notification_wrapper
from Events.hellbound import hellbound_notification_wrapper
from Events.siege import siege_notification_wrapper
from Events.primetime import primetime_notification_wrapper
from Events.purge import purge_notification_wrapper

from Events.watermelon import about_event, set_event, remove_event, watermelon_notification_wrapper
from command_stop import stop, yes_stop, no_stop

# /start, /stop, /about, /help, /mysettings
# /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olympiad
# /hellbound, /antharas - skip, /siege, /primetime, /purge, /event

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

dp.register_message_handler(about_event, commands=['event'])
dp.register_callback_query_handler(set_event, text_contains='setevent')
dp.register_callback_query_handler(remove_event, text_contains='removeevent')

dp.register_message_handler(stop, commands=['stop'])
dp.register_callback_query_handler(yes_stop, text_contains='yes_stop')
dp.register_callback_query_handler(no_stop, text_contains='no_stop')

# general button
b0 = types.InlineKeyboardButton(text='Вернуться', callback_data='back')

# solo raid boss buttons
inline_soloraidboss_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesolorb')

inline_soloraidboss_buttons.add(b1, b2)


# kuka buttons
inline_kuka_buttons = types.InlineKeyboardMarkup()

b4 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setkuka')
b5 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removekuka')

inline_kuka_buttons.add(b4, b5)


# lair of antharas buttons
inline_loa_buttons = types.InlineKeyboardMarkup()

b6 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setloa')
b7 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeloa')

inline_loa_buttons.add(b6, b7)


# frost lord`s castle buttons
inline_frost_buttons = types.InlineKeyboardMarkup()

b8 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setfrost')
b9 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removefrost')

inline_frost_buttons.add(b8, b9)


# orc fortress buttons
inline_fortress_buttons = types.InlineKeyboardMarkup()

b10 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setfortress')
b11 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removefortress')

inline_fortress_buttons.add(b10, b11)


# battle with balok buttons
inline_balok_buttons = types.InlineKeyboardMarkup()

b12 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setbalok')
b13 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removebalok')

inline_balok_buttons.add(b12, b13)


# olympiad buttons
inline_olympiad_buttons = types.InlineKeyboardMarkup()

b14 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setolympiad')
b15 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeolympiad')

inline_olympiad_buttons.add(b14, b15)


# hellbound buttons
inline_hellbound_buttons = types.InlineKeyboardMarkup()

b16 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='sethellbound')
b17 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removehellbound')

inline_hellbound_buttons.add(b16, b17)


# siege giran buttons
inline_siege_buttons = types.InlineKeyboardMarkup()

b18 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setsiege')
b19 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesiege')

inline_siege_buttons.add(b18, b19)


# prime time buttons
inline_primetime_buttons = types.InlineKeyboardMarkup()

b20 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setprimetime')
b21 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeprimetime')

inline_primetime_buttons.add(b20, b21)


# purge buttons
inline_purge_buttons = types.InlineKeyboardMarkup()

b22 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setpurge')
b23 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removepurge')

inline_purge_buttons.add(b22, b23)


# SOLO RAID BOSS SETTINGS
@dp.message_handler(commands=['soloraidboss'])
async def about_soloraidboss(message: types.Message):
    await message.answer('Одиночные Рейд Боссы ресаются каждый нечетный час в :00 минут\n'
                         'С них падает Магическая табличка, и шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Свитки модификации оружия и доспеха ранга В\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n'
                         '- Кристаллы души Адена', reply_markup=inline_soloraidboss_buttons)


@dp.callback_query_handler(filters.Text(contains='setsolorb'))
async def set_soloraidboss(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.soloraidboss = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removesolorb'))
async def remove_soloraidboss(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.soloraidboss = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов убрано')
    await callback_query.answer()


# KUKA SETTINGS
@dp.message_handler(commands=['kuka'])
async def about_kuka(message: types.Message):
    await message.answer('Одиночный босс Кука ресается каждый четный час в :50 минут\n'
                         'После его убийства появляется босс Джисра\n'
                         'С них шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Красящий порошок\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n', reply_markup=inline_kuka_buttons)


@dp.callback_query_handler(filters.Text(contains='setkuka'))
async def set_kuka(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.kuka = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе Куки установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removekuka'))
async def remove_kuka(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.kuka = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе Куки убрано')
    await callback_query.answer()


# LAIR OF ANTHARAS SETTINGS
@dp.message_handler(commands=['loa'])
async def about_loa(message: types.Message):
    await message.answer('Всемирная зона Логово Антараса открывается в'
                         ' понедельник и среду c 18:00 до полуночи.\n',
                         reply_markup=inline_loa_buttons)


@dp.callback_query_handler(filters.Text(contains='setloa'))
async def set_loa(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.loa = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Логова Антараса установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeloa'))
async def remove_loa(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.loa = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Логова Антараса убрано')
    await callback_query.answer()


# FROST LORD`S CASTLE SETTINGS
@dp.message_handler(commands=['frost'])
async def about_frost(message: types.Message):
    await message.answer('Всемирная зона Замок Монарха Льда открывается во'
                         ' вторник и четверг c 18:00 до полуночи.\n',
                         reply_markup=inline_frost_buttons)


@dp.callback_query_handler(filters.Text(contains='setfrost'))
async def set_frost(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.frost = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removefrost'))
async def remove_frost(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.frost = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда убрано')
    await callback_query.answer()


# ORC FORTRESS SETTINGS
@dp.message_handler(commands=['fortress'])
async def about_fortress(message: types.Message):
    await message.answer('Битва за Крепость Орков проводится ежедневно в 20:00',
                         reply_markup=inline_fortress_buttons)


@dp.callback_query_handler(filters.Text(contains='setfortress'))
async def set_fortress(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.fortress = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removefortress'))
async def remove_fortress(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.fortress = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков убрано')
    await callback_query.answer()


# BATTLE WITH BALOK SETTINGS
@dp.message_handler(commands=['balok'])
async def about_balok(message: types.Message):
    await message.answer('Битва с Валлоком проводится ежедневно, кроме воскресенья в 20:30',
                         reply_markup=inline_balok_buttons)


@dp.callback_query_handler(filters.Text(contains='setbalok'))
async def set_balok(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.balok = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы с Валлоком установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removebalok'))
async def remove_balok(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.balok = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Битвы с Валлоком убрано')
    await callback_query.answer()


# OLYMPIAD SETTINGS
@dp.message_handler(commands=['olympiad'])
async def about_olympiad(message: types.Message):
    await message.answer('Всемирная Олимпиада проводится с понедельника'
                         ' по пятницу с 21:30 до 22:00.', reply_markup=inline_olympiad_buttons)


@dp.callback_query_handler(filters.Text(contains='setolympiad'))
async def set_olympiad(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.olympiad = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Олимпиады установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeolympiad'))
async def remove_olympiad(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.olympiad = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Олимпиады убрано')
    await callback_query.answer()


# HELLBOUND SETTINGS
@dp.message_handler(commands=['hellbound'])
async def about_hellbound(message: types.Message):
    await message.answer('Остров Ада — межсерверная зона охоты для персонажей 85+ и'
                         ' доступна в субботу с 10:00 до 00:00.',
                         reply_markup=inline_hellbound_buttons)


@dp.callback_query_handler(filters.Text(contains='sethellbound'))
async def set_hellbound(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.hellbound = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии и закрытии Острова Ада установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removehellbound'))
async def remove_hellbound(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.hellbound = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение об открытии и закрытии Острова Ада убрано')
    await callback_query.answer()


# GIRAN`S SIEGE SETTINGS
@dp.message_handler(commands=['siege'])
async def about_siege(message: types.Message):
    await message.answer('Осада Замка Гиран приходит в воскресенье с 20:30 до 21:00.',
                         reply_markup=inline_siege_buttons)


@dp.callback_query_handler(filters.Text(contains='setsiege'))
async def set_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.siege = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removesiege'))
async def remove_siege(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.siege = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале Осады Гирана убрано')
    await callback_query.answer()


# PRIME TIME SETTINGS
@dp.message_handler(commands=['primetime'])
async def about_primetime(message: types.Message):
    await message.answer('Ежедневно в прайм-тайм получаемые очки зачистки удваиваются:\n'
                         '- с 12:00 до 14:00\n'
                         '- с 19:00 до 23:00', reply_markup=inline_primetime_buttons)


@dp.callback_query_handler(filters.Text(contains='setprimetime'))
async def set_primetime(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.primetime = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале прайм-тайма установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeprimetime'))
async def remove_primetime(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.primetime = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о начале прайм-тайма убрано')
    await callback_query.answer()


# PURGE SETTINGS
@dp.message_handler(commands=['purge'])
async def about_purge(message: types.Message):
    await message.answer('Зачистка обнуляется в полночь в воскресенье, оповестим за 30 минут',
                         reply_markup=inline_purge_buttons)


@dp.callback_query_handler(filters.Text(contains='setpurge'))
async def set_purge(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.purge = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о сборе зачистки установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removepurge'))
async def remove_purge(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.purge = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о сборе зачистки убрано')
    await callback_query.answer()


# GENERAL SETTINGS
@dp.callback_query_handler(filters.Text(contains='back'))
async def return_menu(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        '/mysettings\n'
        '\n'
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
    await callback_query.answer()


@dp.message_handler(commands=['mysettings'])
async def get_settings(message: types.Message):
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()

    await message.answer(
        'Установленные настройки:\n'
        '\n'
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
        f"Прайм Тайм Зачистки - {setting.primetime}\n"
        f"Зачистка - {setting.purge}")

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
                         '\n'
                         'Выбирай интересующую активность и жми "Установить оповещение".'
                         ' В таком случае тебе будут приходить уведомления за 5 минут'
                         ' до начала события.\n'
                         '\n'
                         'За это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.')


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer('Братсво кольца приветствует тебя!'
                         ' Я - Kobatoha, и я создала этого бота для вас, мои маленькие любители l2essence!'
                         ' Мы поможем не пропустить игровые активности.\n'
                         'Бот создан на добровольных началах, поэтому он свободен и независим.'
                         ' Есть идеи и предложения по улучшению бота? Велком - kobatoha@yandex.ru\n')


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
    crontab('55 * * * *', func=soloraidboss_notification_wrapper)

    # Запускаем kuka каждый час в :45
    crontab('45 * * * *', func=kuka_notification_wrapper)

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
    crontab('55 23 * * 6', func=hellbound_notification_wrapper)

    # Запускаем siege в воскресенье в 20:25
    crontab('25 20 * * 7', func=siege_notification_wrapper)

    # Запускаем primetime ежедневно в 11:55
    crontab('55 11 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 13:55
    crontab('55 13 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 18:55
    crontab('55 18 * * *', func=primetime_notification_wrapper)

    # Запускаем primetime ежедневно в 22:55
    crontab('55 22 * * *', func=primetime_notification_wrapper)

    # Запускаем purge в воскресенье в 23:30
    crontab('30 23 * * 7', func=purge_notification_wrapper)

    # Запускаем event в ежедневно в 10:55
    crontab('55 10 * * *', func=watermelon_notification_wrapper)

    # Запускаем event в ежедневно в 20:55
    crontab('55 20 * * *', func=watermelon_notification_wrapper)


if __name__ == '__main__':
    now_start = datetime.now().strftime('%H:%M')
    print(now_start, 'Запуск Lineage2Notifications')
    loop = asyncio.get_event_loop()
    loop.create_task(crontab_notifications())
    executor.start_polling(dp, skip_updates=True)
