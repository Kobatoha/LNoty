from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN

# /start, /about, /help, /mysettings
# /soloraidboss, /kuka, /loa, /frost, /fortress, /balok, /olimpiad
# /hellbound, /antharas, /siege, /primetime, /purge

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)


inline_buttons = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text='Уставновить оповещение', callback_data='setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesolorb')
b3 = types.InlineKeyboardButton(text='Вернуться', callback_data='back')

inline_buttons.add(b1, b2)
inline_buttons.row(b3)

user_results = {
    'soloraidboss': False
}


@dp.message_handler(commands=['soloraidboss'])
async def cmd_handler(message: types.Message):
    await message.answer('Одиночные Рейд Боссы ресаются каждый нечетный час в :00 минут\n'
                         'С них падает Магическая табличка, и шансово могут упасть:\n'
                         '- Свитки модификации оружия и доспеха ранга А\n'
                         '- Свитки модификации оружия и доспеха ранга В\n'
                         '- Камни зачарования оружия и доспеха\n'
                         '- Камни Эволюции\n'
                         '- Кристаллы души Адена')
    await message.answer('Выберите команду:', reply_markup=inline_buttons)


@dp.callback_query_handler(filters.Text(contains='setsolorb'))
async def some_callback_handler(callback_query: types.CallbackQuery):
    user_results['soloraidboss'] = True
    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='removesolorb'))
async def some_callback_handler(callback_query: types.CallbackQuery):
    user_results['soloraidboss'] = False
    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов убрано')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='back'))
async def some_callback_handler(callback_query: types.CallbackQuery):
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
async def cmd_handler(message: types.Message):
    await message.answer(
        'Установленные настройки:\n'
        '\n'
        f'Одиночные РБ - '
        f"{user_results['soloraidboss']}")


@dp.message_handler(commands=['start'])
async def cmd_handler(message: types.Message):
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'В Меню ты найдешь все доступные команды.\n'
                         'Так же этот список можно вызвать командой /help\n'
                         '\n'
                         'Выбирай интересующую активность и нажми "Установить оповещение".'
                         ' В таком случае тебе будут приходить уведомления за 10 минут'
                         ' до начала события.\n\nЗа это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.')


@dp.message_handler(commands=['about'])
async def cmd_handler(message: types.Message):
    await message.answer('Я - телеграм-бот, который поможет не пропустить игровые активности.\n\n'
                         'Меня создали на добровольных началах, поэтому я свободен и независим.'
                         ' И конечно я всегда открыт для новых идей и предложений.\n\n'
                         'Мой мастер живет на сервере Lavender и у него везде глаза и уши.'
                         ' И если у тебя есть идея или предложение, урони свою мысль в мировом чате,'
                         ' и мастер обязательно её услышит.')


@dp.message_handler(commands=['help'])
async def cmd_handler(message: types.Message):
    await message.answer('Доступные команды:\n'
                         '\n'
                         '/start - запуск бота\n'
                         '/about - о боте\n'
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
