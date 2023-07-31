import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from datetime import datetime
from models import User, Base, Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# kuka buttons
inline_kuka_buttons = types.InlineKeyboardMarkup()

b4 = types.InlineKeyboardButton(text='Установить оповещение', callback_data='setkuka')
b5 = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='removekuka')

inline_kuka_buttons.add(b4, b5)


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


async def kuka_notification_wrapper():
    session = Session()
    users = session.query(User).all()
    for user in users:

        setting = session.query(Setting).filter_by(id_user=user.telegram_id).first()
        if setting.kuka is True and setting.fulltime is True:
            await kuka_notification(user)
        elif setting.kuka is True and setting.fulltime is False:
            await kuka_notification_hardwork(user)
    session.close()


async def kuka_notification(user: User):
    now = datetime.now().strftime('%H:%M')
    kuka_time = ['00:45', '02:45', '04:45', '06:45', '08:45', '10:45', '12:45', '14:45', '16:45', '18:45', '20:45',
                 '22:45']

    if now in kuka_time:
        await mybot.send_message(user.telegram_id, 'Кука появится через 5 минут')
        print(now, user.telegram_id, user.username, '(круглосуточник) получил сообщение о Куке')



async def kuka_notification_hardwork(user: User):
    now = datetime.now().strftime('%H:%M')
    kuka_hardwork = ['08:45', '10:45', '12:45', '14:45', '16:45', '18:45', '20:45', '22:45']

    if now in kuka_hardwork:
        await mybot.send_message(user.telegram_id, 'Кука появится через 5 минут')
        print(now, user.telegram_id, user.username, '(работяга) получил сообщение о Куке')
