from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN

# /start, /about
# /soloraidboss, /kuka, /loa, /ice, /fortress, /vallok, /olimpiada
# /hellbound, /antharas, /siege, /hottime, /purge

mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)


inline_buttons = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text='Уставновить оповещение', callback_data='setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removesolorb')
b3 = types.InlineKeyboardButton(text='Вернуться', callback_data='back')

inline_buttons.add(b1, b2)
inline_buttons.row(b3)


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
    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов установлено')
    await callback_query.answer()


@dp.message_handler(commands=['start'])
async def cmd_handler(message: types.Message):
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'Вместе мы ничего не забудем и зафармим то, что зафармить невозможно!')


@dp.message_handler(commands=['about'])
async def cmd_handler(message: types.Message):
    await message.answer('Это телеграм-бот для оповещений в\n'
                         'Вместе мы ничего не забудем и зафармим то, что зафармить невозможно!')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Kak dela?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
