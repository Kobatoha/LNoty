import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# solo raid boss buttons
inline_soloraidboss_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_setsolorb')
b2 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_removesolorb')

inline_soloraidboss_buttons.add(b1, b2)


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


@dp.callback_query_handler(filters.Text(contains='ruoff_setsolorb'))
async def set_soloraidboss(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.soloraidboss = True

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов установлено')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ruoff_removesolorb'))
async def remove_soloraidboss(callback_query: types.CallbackQuery):
    session = Session()

    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
    setting.soloraidboss = False

    session.commit()
    session.close()

    await callback_query.message.answer('Оповещение о респе одиночных рейд боссов убрано')
    await callback_query.answer()


async def soloraidboss_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:
        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.soloraidboss is True and setting.fulltime is True:
            await soloraidboss_notification(user)
        elif setting.soloraidboss is True and setting.fulltime is False:
            await soloraidboss_notification_hardwork(user)
    session.close()


async def soloraidboss_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    soloraidboss_time = ['00:55', '02:55', '04:55', '06:55', '08:55', '10:55', '12:55', '14:55', '16:55', '18:55',
                         '20:55', '22:55']
    try:
        if now in soloraidboss_time:
            await mybot.send_message(user.telegram_id, 'Одиночные Рейд Боссы появятся через 5 минут')
            print(now, user.telegram_id, user.username, '(круглосуточник) получил сообщение о Соло РБ')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)


async def soloraidboss_notification_hardwork(user: User):
    now = datetime.now().strftime('%H:%M')
    soloraidboss_hardwork = ['08:55', '10:55', '12:55', '14:55', '16:55', '18:55',
                             '20:55', '22:55']
    try:
        if now in soloraidboss_hardwork:
            await mybot.send_message(user.telegram_id, 'Одиночные Рейд Боссы появятся через 5 минут')
            print(now, user.telegram_id, user.username, '(работяга) получил сообщение о Соло РБ')
    except BotBlocked:
        print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
