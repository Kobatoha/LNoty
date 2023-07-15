from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN

# /start, /about, /help, /mysettings
# /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olympiad
# /hellbound, /antharas - skip, /siege, /primetime, /purge

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)


user_settings = {
    'soloraidboss': False,
    'kuka': False,
    'loa': False,
    'frost': False,
    'fortress': False,
    'balok': False,
    'olympiad': False,
    'hellbound': False,
    'siege': False,
    'primetime': False,
    'purge': False
}


# general button
b0 = types.InlineKeyboardButton(text='Вернуться', callback_data='back')

# solo raid boss buttons
inline_soloraidboss_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesolorb')

inline_soloraidboss_buttons.add(b1, b2)
inline_soloraidboss_buttons.row(b0)

# kuka buttons
inline_kuka_buttons = types.InlineKeyboardMarkup()

b4 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setkuka')
b5 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removekuka')

inline_kuka_buttons.add(b4, b5)
inline_kuka_buttons.row(b0)

# lair of antharas buttons
inline_loa_buttons = types.InlineKeyboardMarkup()

b6 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setloa')
b7 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeloa')

inline_loa_buttons.add(b6, b7)
inline_loa_buttons.row(b0)

# frost lord`s castle buttons
inline_frost_buttons = types.InlineKeyboardMarkup()

b8 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setfrost')
b9 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removefrost')

inline_frost_buttons.add(b8, b9)
inline_frost_buttons.row(b0)

# orc fortress buttons
inline_fortress_buttons = types.InlineKeyboardMarkup()

b10 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setfortress')
b11 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removefortress')

inline_fortress_buttons.add(b10, b11)
inline_fortress_buttons.row(b0)

# battle with balok buttons
inline_balok_buttons = types.InlineKeyboardMarkup()

b12 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setbalok')
b13 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removebalok')

inline_balok_buttons.add(b12, b13)
inline_balok_buttons.row(b0)

# olympiad buttons
inline_olympiad_buttons = types.InlineKeyboardMarkup()

b14 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setolympiad')
b15 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeolympiad')

inline_olympiad_buttons.add(b14, b15)
inline_olympiad_buttons.row(b0)

# hellbound buttons
inline_hellbound_buttons = types.InlineKeyboardMarkup()

b16 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='sethellbound')
b17 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removehellbound')

inline_hellbound_buttons.add(b16, b17)
inline_hellbound_buttons.row(b0)

# siege giran buttons
inline_siege_buttons = types.InlineKeyboardMarkup()

b18 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setsiege')
b19 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesiege')

inline_siege_buttons.add(b18, b19)
inline_siege_buttons.row(b0)

# prime time buttons
inline_primetime_buttons = types.InlineKeyboardMarkup()

b20 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setprimetime')
b21 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removeprimetime')

inline_primetime_buttons.add(b20, b21)
inline_primetime_buttons.row(b0)


# SOLO RAID BOSS SETTINGS
@dp.message_handler(commands=['soloraidboss'])
async def about_soloraidboss(message: types.Message):
    await message.answer('Одиночные Рейд Боссы ресаются каждый нечетный час в :00 минут\n'
                         'С них падает Магическая табличка, и шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Свитки модификации оружия и доспеха ранга В\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n'
                         '- Кристаллы души Адена')
    await message.answer('Выберите команду:', reply_markup=inline_soloraidboss_buttons)


@dp.callback_query_handler(filters.Text(contains='setsolorb'))
async def set_soloraidboss(callback_query: types.CallbackQuery):
    user_settings['soloraidboss'] = True
    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removesolorb'))
async def remove_soloraidboss(callback_query: types.CallbackQuery):
    user_settings['soloraidboss'] = False
    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов убрано')
    await callback_query.answer()


# KUKA SETTINGS
@dp.message_handler(commands=['kuka'])
async def about_kuka(message: types.Message):
    await message.answer('Одиночный босс Кука ресается каждый нечетный час в :50 минут\n'
                         'После его убийства появляется босс Джисра\n'
                         'С них шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Красящий порошок\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n'
                         )
    await message.answer('Выберите команду:', reply_markup=inline_kuka_buttons)


@dp.callback_query_handler(filters.Text(contains='setkuka'))
async def set_kuka(callback_query: types.CallbackQuery):
    user_settings['kuka'] = True
    await callback_query.message.answer('Оповещение о респе Куки установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removekuka'))
async def remove_kuka(callback_query: types.CallbackQuery):
    user_settings['kuka'] = False
    await callback_query.message.answer('Оповещение о респе Куки убрано')
    await callback_query.answer()


# LAIR OF ANTHARAS SETTINGS
@dp.message_handler(commands=['loa'])
async def about_loa(message: types.Message):
    await message.answer('Всемирная зона Логово Антараса открывается в'
                         ' понедельник и среду c 18:00 до полуночи.\n'
                         )
    await message.answer('Выберите команду:', reply_markup=inline_loa_buttons)


@dp.callback_query_handler(filters.Text(contains='setloa'))
async def set_loa(callback_query: types.CallbackQuery):
    user_settings['loa'] = True
    await callback_query.message.answer('Оповещение об открытии Логова Антараса установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeloa'))
async def remove_loa(callback_query: types.CallbackQuery):
    user_settings['loa'] = False
    await callback_query.message.answer('Оповещение об открытии Логова Антараса убрано')
    await callback_query.answer()


# FROST LORD`S CASTLE SETTINGS
@dp.message_handler(commands=['frost'])
async def about_frost(message: types.Message):
    await message.answer('Всемирная зона Замок Монарха Льда открывается во'
                         ' вторник и четверг c 18:00 до полуночи.\n'
                         )
    await message.answer('Выберите команду:', reply_markup=inline_frost_buttons)


@dp.callback_query_handler(filters.Text(contains='setfrost'))
async def set_frost(callback_query: types.CallbackQuery):
    user_settings['frost'] = True
    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removefrost'))
async def remove_frost(callback_query: types.CallbackQuery):
    user_settings['frost'] = False
    await callback_query.message.answer('Оповещение об открытии Замка Монарха Льда убрано')
    await callback_query.answer()


# ORC FORTRESS SETTINGS
@dp.message_handler(commands=['fortress'])
async def about_fortress(message: types.Message):
    await message.answer('Битва за Крепость Орков проводится ежедневно в 20:00')
    await message.answer('Выберите команду:', reply_markup=inline_fortress_buttons)


@dp.callback_query_handler(filters.Text(contains='setfortress'))
async def set_fortress(callback_query: types.CallbackQuery):
    user_settings['fortress'] = True
    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removefortress'))
async def remove_fortress(callback_query: types.CallbackQuery):
    user_settings['fortress'] = False
    await callback_query.message.answer('Оповещение о начале Битвы за Крепость Орков убрано')
    await callback_query.answer()


# BATTLE WITH BALOK SETTINGS
@dp.message_handler(commands=['balok'])
async def about_balok(message: types.Message):
    await message.answer('Битва с Валлоком проводится ежедневно, кроме воскресенья в 20:30')
    await message.answer('Выберите команду:', reply_markup=inline_balok_buttons)


@dp.callback_query_handler(filters.Text(contains='setbalok'))
async def set_balok(callback_query: types.CallbackQuery):
    user_settings['balok'] = True
    await callback_query.message.answer('Оповещение о начале Битвы с Валлоком установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removebalok'))
async def remove_balok(callback_query: types.CallbackQuery):
    user_settings['balok'] = False
    await callback_query.message.answer('Оповещение о начале Битвы с Валлоком убрано')
    await callback_query.answer()


# OLYMPIAD SETTINGS
@dp.message_handler(commands=['olympiad'])
async def about_olympiad(message: types.Message):
    await message.answer('Всемирная Олимпиада проводится с понедельника'
                         ' по пятницу с 21:30 до 22:00.')
    await message.answer('Выберите команду:', reply_markup=inline_olympiad_buttons)


@dp.callback_query_handler(filters.Text(contains='setolympiad'))
async def set_olympiad(callback_query: types.CallbackQuery):
    user_settings['olympiad'] = True
    await callback_query.message.answer('Оповещение о начале Олимпиады установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeolympiad'))
async def remove_olympiad(callback_query: types.CallbackQuery):
    user_settings['olympiad'] = False
    await callback_query.message.answer('Оповещение о начале Олимпиады убрано')
    await callback_query.answer()


# HELLBOUND SETTINGS
@dp.message_handler(commands=['hellbound'])
async def about_hellbound(message: types.Message):
    await message.answer('Остров Ада — межсерверная зона охоты для персонажей 85+ и'
                         ' доступен в субботу с 10:00 до 00:00. ')
    await message.answer('Выберите команду:', reply_markup=inline_hellbound_buttons)


@dp.callback_query_handler(filters.Text(contains='sethellbound'))
async def set_hellbound(callback_query: types.CallbackQuery):
    user_settings['hellbound'] = True
    await callback_query.message.answer('Оповещение об открытии и закрытии Острова Ада установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removehellbound'))
async def remove_hellbound(callback_query: types.CallbackQuery):
    user_settings['hellbound'] = False
    await callback_query.message.answer('Оповещение об открытии и закрытии Острова Ада убрано')
    await callback_query.answer()


# GIRAN`S SIEGE SETTINGS
@dp.message_handler(commands=['siege'])
async def about_siege(message: types.Message):
    await message.answer('Осада Замка Гиран приходит в '
                         ' доступен в субботу с 10:00 до 00:00. ')
    await message.answer('Выберите команду:', reply_markup=inline_siege_buttons)


@dp.callback_query_handler(filters.Text(contains='setsiege'))
async def set_siege(callback_query: types.CallbackQuery):
    user_settings['siege'] = True
    await callback_query.message.answer('Оповещение о начале Осады Гирана установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removesiege'))
async def remove_siege(callback_query: types.CallbackQuery):
    user_settings['siege'] = False
    await callback_query.message.answer('Оповещение о начале Осады Гирана убрано')
    await callback_query.answer()


# PRIME TIME SETTINGS
@dp.message_handler(commands=['primetime'])
async def about_primetime(message: types.Message):
    await message.answer('Ежедневно в прайм-тайм получаемые очки зачистки удваиваются:\n'
                         '- с 12:00 до 14:00\n'
                         '- с 19:00 до 23:00'
                         )
    await message.answer('Выберите команду:', reply_markup=inline_primetime_buttons)


@dp.callback_query_handler(filters.Text(contains='setprimetime'))
async def set_primetime(callback_query: types.CallbackQuery):
    user_settings['primetime'] = True
    await callback_query.message.answer('Оповещение о начале прайм-тайма установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removeprimetime'))
async def remove_primetime(callback_query: types.CallbackQuery):
    user_settings['primetime'] = False
    await callback_query.message.answer('Оповещение о начале прайм-тайма убрано')
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
    await message.answer(
        'Установленные настройки:\n'
        '\n'
        f'Одиночные РБ - '
        f"{user_settings['soloraidboss']}\n"
        f"Кука и Джисра - "
        f"{user_settings['kuka']}\n"
        f"Логово Антараса - "
        f"{user_settings['loa']}\n"
        f"Замок Монарха Льда - "
        f"{user_settings['frost']}\n"
        f"Крепость Орков - "
        f"{user_settings['fortress']}\n"
        f"Битва с Валлоком - "
        f"{user_settings['balok']}\n"
        f"Всемирная Олимпиада - "
        f"{user_settings['olympiad']}\n"
        f"Остров Ада - "
        f"{user_settings['hellbound']}\n"
        f"Осада Гирана - "
        f"{user_settings['siege']}\n"
        f"Прайм Тайм Зачистки - "
        f"{user_settings['primetime']}\n"
        f"Зачистка - "
        f"{user_settings['purge']}")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'В Меню ты найдешь все доступные команды.\n'
                         'Так же этот список можно вызвать командой /help\n'
                         '\n'
                         'Выбирай интересующую активность и нажми "Установить оповещение".'
                         ' В таком случае тебе будут приходить уведомления за 10 минут'
                         ' до начала события.\n\nЗа это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.')


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer('Я - телеграм-бот, который поможет не пропустить игровые активности.\n\n'
                         'Меня создали на добровольных началах, поэтому я свободен и независим.'
                         ' И конечно я всегда открыт для новых идей и предложений.\n\n'
                         'Мой мастер живет на сервере Lavender и у него везде глаза и уши.'
                         ' И если у тебя есть идея или предложение, урони свою мысль в мировом чате,'
                         ' и мастер обязательно её услышит.')


@dp.message_handler(commands=['help'])
async def helped(message: types.Message):
    await message.answer('Доступные команды:\n'
                         '\n'
                         '/start - запуск бота\n'
                         '/about - о боте\n'
                         '/mysettings - персональные настройки\n'
                         '/help - список команд\n'
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


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Kak dela?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
