import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import EssenceCustomSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN, test_token
from aiogram.utils.exceptions import BotBlocked
from aiocron import crontab
from Commands.options import options_menu_text
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class ValakasTime(StatesGroup):
    waiting_for_valakas_time = State()


# valakas buttons
inline_valakas_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_valakas')
button_set_day = types.InlineKeyboardButton(text='Установить день', callback_data='ruoff_option_set_day_valakas')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_valakas')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_valakas')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_valakas')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_valakas')

inline_valakas_buttons.add(button_set, button_remove)


# VALAKAS TEMP SETTINGS
@dp.message_handler(commands=['valakas'])
async def about_valakas(message: types.Message):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        if not option_setting:
            option = EssenceCustomSetting(id_user=user.telegram_id)
            session.add(option)
            session.commit()
        session.close()

        text = 'Храм Валакаса — временная зона охоты для 15+ персонажей'\
               ' от 76 уровня и выше. Доступна раз в неделю, откат зоны в среду в 6:30 по МСК.\n' \
               '\n' \
               'В зоне вас ждут мобы и парочка боссов, которые дропают:\n' \
               '- Магические таблички\n' \
               '- Камни зачарования\n' \
               '- Свитки благословения\n' \
               '- Топ А шмот и веапон\n' \
               '- Точки А веапон и армор\n' \
               '\n'\
               '🔥 В конце зоны ждет Босс, который может отсыпать дропа в виде книги 4*'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_valakas_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции about_valakas: {e}')


# SELECT MENU FOR VALAKAS TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_valakas'))
async def set_valakas(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_day, button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Храма Валакаса 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_valakas: {e}')


# CANCEL MENU VALAKAS TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_valakas'))
async def cancel_to_set_valakas(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_valakas: {e}')


# INPUT VALAKAS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_valakas'))
async def set_valakas_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Храма Валакаса в формате час:минута (например, 10:21 или 01:42): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await ValakasTime.waiting_for_valakas_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_valakas_time: {e}')


# SAVE VALAKAS TIME
@dp.message_handler(state=ValakasTime.waiting_for_valakas_time)
async def save_valakas_time(message: types.Message, state: FSMContext):
    try:
        valakas_time = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(valakas_time) == 5 and valakas_time[:2] in hours\
                and valakas_time[2] == ':' and valakas_time[3:5] in minutes:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.valakas_time = valakas_time
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_day, button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Храма Валакаса - {valakas_time}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_valakas_time: {e}')


# CANCEL SET VALAKAS TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_valakas',
                           state=ValakasTime.waiting_for_valakas_time)
async def cancel_to_set_valakas_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_valakas_time: {e}')


# INPUT VALAKAS DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_day_valakas'))
async def set_valakas_day(callback_query: types.CallbackQuery):
    try:
        button_mon = types.InlineKeyboardButton(text='понедельник', callback_data='add_valakas_monday')
        button_tue = types.InlineKeyboardButton(text='вторник', callback_data='add_valakas_tuesday')
        button_wed = types.InlineKeyboardButton(text='среда', callback_data='add_valakas_wednesday')
        button_thu = types.InlineKeyboardButton(text='четверг', callback_data='add_valakas_thursday')
        button_fri = types.InlineKeyboardButton(text='пятница', callback_data='add_valakas_friday')
        button_sat = types.InlineKeyboardButton(text='суббота', callback_data='add_valakas_saturday')
        button_sun = types.InlineKeyboardButton(text='воскресенье', callback_data='add_valakas_sunday')
        keyboard = types.InlineKeyboardMarkup(row_width=3).add(button_mon, button_tue, button_wed,
                                                               button_thu, button_fri, button_sat,
                                                               button_sun).row(button_back)
        await callback_query.message.edit_text('Выберите день недели оповещения для Храма Валакаса:\n ',
                                               reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_valakas_day: {e}')


# SAVE VALAKAS DAY
@dp.callback_query_handler(lambda c: c.data.startswith('add_valakas_'))
async def save_valakas_day(callback_query: types.CallbackQuery):
    try:
        day_valakas = None
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()

        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=callback_query.from_user.id).first()
        if callback_query.data == 'add_valakas_monday':
            option_setting.valakas_day = 'понедельник'
            session.commit()
            day_valakas = 'понедельник'
        elif callback_query.data == 'add_valakas_tuesday':
            option_setting.valakas_day = 'вторник'
            session.commit()
            day_valakas = 'вторник'
        elif callback_query.data == 'add_valakas_wednesday':
            option_setting.valakas_day = 'среда'
            session.commit()
            day_valakas = 'среда'
        elif callback_query.data == 'add_valakas_thursday':
            option_setting.valakas_day = 'четверг'
            session.commit()
            day_valakas = 'четверг'
        elif callback_query.data == 'add_valakas_friday':
            option_setting.valakas_day = 'пятница'
            session.commit()
            day_valakas = 'пятница'
        elif callback_query.data == 'add_valakas_saturday':
            option_setting.valakas_day = 'суббота'
            session.commit()
            day_valakas = 'суббота'
        elif callback_query.data == 'add_valakas_sunday':
            option_setting.valakas_day = 'воскресенье'
            session.commit()
            day_valakas = 'воскресенье'

        user.upd_date = datetime.today()
        session.commit()

        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=f'Вы установили день для оповещений Храма Валакаса - {day_valakas}',
                                      reply_markup=keyboard)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции save_valakas_day: {e}')


# CANCEL SET VALAKAS DAY
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_valakas')
async def cancel_to_set_valakas_day(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_valakas_day: {e}')


# REMOVE VALAKAS TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_valakas'))
async def remove_valakas(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        option_setting.valakas_time = None
        option_setting.valakas_day = None

        session.commit()
        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Храме Валакаса убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_valakas: {e}')


# SELECT USER WITH TRUE SETTING
async def valakas_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()

        for user in users:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            if option and option.valakas_time and option.valakas_day:
                await valakas_notification(user)
        session.close()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции valakas_notification_wrapper: {e}')


# SEND VALAKAS MESSAGE
async def valakas_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')
        today = datetime.now().strftime('%A').lower()

        session = Session()
        option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        session.close()

        valakas_day = option.valakas_day.lower() if option.valakas_day else None
        if valakas_day and today != valakas_day:
            return

        valakas_time = option.valakas_time if option.valakas_time else None
        if valakas_time and now != valakas_time:
            return

        try:
            await mybot.send_message(user.telegram_id,
                                     'Храм Валакаса ждет своих героев. '
                                     'Скорее собирай ЦЦ и отправляйся в Аден к Фонтану.')
            print(now, user.telegram_id, user.username, 'получил сообщение о Храме Валакаса')
        except BotBlocked:
            print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции valakas_notification: {e}')
