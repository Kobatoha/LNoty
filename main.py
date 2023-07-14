from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN

# /start, /about, /help, /mysettings
# /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olimpiad
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
    'olimpiad': False,
    'hellbound': False,
    'siege': False,
    'primetime': False,
    'purge': False
}

inline_buttons = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text='Уставновить оповещение', callback_data='setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesolorb')
b3 = types.InlineKeyboardButton(text='Вернуться', callback_data='back')

inline_buttons.add(b1, b2)
inline_buttons.row(b3)


@dp.message_handler(commands=['soloraidboss'])
async def about_soloraidboss(message: types.Message):
    await message.answer('Одиночные Рейд Боссы ресаются каждый нечетный час в :00 минут\n'
                         'С них падает Магическая табличка, и шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Свитки модификации оружия и доспеха ранга В\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n'
                         '- Кристаллы души Адена')
    await message.answer('Выберите команду:', reply_markup=inline_buttons)


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


@dp.callback_query_handler(filters.Text(contains='back'))
async def return_menu(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        '/soloraidboss - Одиночные РБ\n'
        '/kuka - Кука и Джисра\n'
        '/loa - Логово Антараса\n'
        '/frost - Замок Монарха Льда\n'
        '/fortress - Крепость Орков\n'
        '/balok - Битва с Валлоком\n'
        '/olimpiad - Всемирная Олимпиада\n'
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
        f"{user_settings['olimpiad']}\n"
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
async def help(message: types.Message):
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
                         '/olimpiad - Всемирная Олимпиада\n'
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
