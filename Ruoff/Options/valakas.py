import asyncio
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Ruoff import RuoffCustomSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL, TOKEN
from aiogram.utils.exceptions import BotBlocked
from aiocron import crontab
from Commands.options import options_menu_text
import locale
import logging

locale.setlocale(locale.LC_ALL, 'ru_RU')
logging.basicConfig(filename='Lineage2Notification.log', level=logging.INFO)


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class ValakasDay(StatesGroup):
    waiting_for_valakas_day = State()


class ValakasTime(StatesGroup):
    waiting_for_valakas_time = State()


# dream buttons
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


# VALAKAS TEMPLE SETTINGS
@dp.message_handler(commands=['valakas'])
async def about_valakas(message: types.Message):
    try:
        now = datetime.now().strftime('%H:%M:%S')
        logging.info(f' [VALAKAS] {now}: {message.from_user.id} - {message.from_user.username} used /valakas')
        session = Session()

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
        if not option_setting:
            option = RuoffCustomSetting(id_user=user.telegram_id)
            session.add(option)
            session.commit()
            logging.info(f' [VALAKAS] {now}: {message.from_user.id} - {message.from_user.username} add custom_settings')
        session.close()

        text = 'Храм Валакаса — временная зона охоты для 15+ персонажей'\
               ' от 76 уровня и выше. За время входа в Храм Валакаса'\
               ' персонажам предстоит убить трех боссов: Ифрит, Ифрин и Иф.\n'\
               '\n'\
               'Из дропа возможно выпадение:\n'\
               '- Свитки Благословения на доспех и оружие\n'\
               '- Улучшенные и проклятые свитки на оружие и доспехи\n'\
               '- Камни зачарования на оружие/доспех/аксессуар'\
               '- Таблички\n'\
               '- ТОП А доспехи и оружие\n'\
               '\n'\
               'А в конце с шансом может появиться Пылающий Дракон, с которого падают книги (и даже 4****)'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_valakas_buttons)

    except Exception as e:
        logging.error(f' [VALAKAS] {message.from_user.id} - ошибка в функции about_valakas: {e}')
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
        logging.error(f' [VALAKAS] {callback_query.from_user.id} - ошибка в функции set_valakas: {e}')
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
        logging.error(f' [VALAKAS] {callback_query.from_user.id} - ошибка в функции cancel_to_set_valakas: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_valakas: {e}')


# INPUT VALAKAS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_valakas'))
async def set_valakas_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'Введите время оповещения для Храма Валакаса в формате час:минута (например, 10:21): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await ValakasTime.waiting_for_valakas_time.set()
        await callback_query.answer()

    except Exception as e:
        logging.error(f' [VALAKAS] {callback_query.from_user.id} - ошибка в функции set_valakas_time: {e}')
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

        if len(valakas_time) == 5 and valakas_time[:2] in hours and valakas_time[2] == ':' \
                and valakas_time[3:5] in minutes:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.valakas_time = valakas_time
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_day, button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Храм Валакаса - {valakas_time}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        logging.error(f' [VALAKAS] {message.from_user.id} - ошибка в функции save_valakas_time: {e}')
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
        logging.error(f' [VALAKAS] {callback_query.from_user.id} - ошибка в функции cancel_to_set_valakas_time: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_valakas_time: {e}')


# INPUT VALAKAS DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_day_valakas'))
async def set_valakas_day(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        await callback_query.message.edit_text('Введите день недели оповещения для Храма Валакаса:\n '
                                               '[ понедельник | вторник | среда | четверг | пятница | суббота | '
                                               'воскресенье ]',
                                               reply_markup=keyboard)
        await ValakasDay.waiting_for_valakas_day.set()
        await callback_query.answer()

    except Exception as e:
        logging.error(f' [VALAKAS] {callback_query.from_user.id} - ошибка в функции set__day: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[VALAKAS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_dream_day: {e}')


# SAVE DREAM DAY
@dp.message_handler(state=DreamDay.waiting_for_dream_day)
async def save_dream_day(message: types.Message, state: FSMContext):
    try:
        dream_day = message.text
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

        if dream_day.lower() in days:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.dream_day = dream_day
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили день для оповещений Подземелье Грёз - {dream_day}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        logging.error(f' [DREAM] {message.from_user.id} - ошибка в функции save_dream_day: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[DREAM] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_dream_day: {e}')


# CANCEL SET DREAM DAY
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_dream',
                           state=DreamDay.waiting_for_dream_day)
async def cancel_to_set_dream_day(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        logging.error(f' [DREAM] {message.from_user.id} - ошибка в функции cancel_to_set_dream_day: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[DREAM] {message.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_dream_day: {e}')


# REMOVE DREAM TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_dream'))
async def remove_dream(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
        option_setting.dream_time = None
        option_setting.dream_day = None

        session.commit()
        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Подземелье Грёз убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        logging.error(f' [DREAM] {message.from_user.id} - ошибка в функции remove_dream: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[DREAM] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_dream: {e}')


# SELECT USER WITH TRUE SETTING
async def dream_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()

        for user in users:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            if option and option.dream_time and option.dream_day:
                await dream_notification(user)
        session.close()

    except Exception as e:
        logging.error(f' [DREAM] {message.from_user.id} - ошибка в функции dream_notification_wrapper: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[DREAM] {message.from_user.id} - '
                                      f'Произошла ошибка в функции dream_notification_wrapper: {e}')


# SEND DREAM MESSAGE
async def dream_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')
        today = datetime.now().strftime('%A').lower()

        session = Session()
        option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
        session.close()

        dream_day = option.dream_day.lower() if option.dream_day else None
        if dream_day and today != dream_day:
            return

        dream_time = option.dream_time if option.dream_time else None
        if dream_time and now != dream_time:
            return

        try:
            await mybot.send_message(user.telegram_id,
                                     'Подземелье Грёз ждет своих героев. '
                                     'Скорее собирай пати и отправляйся в Аден к Фонтану')
            print(now, user.telegram_id, user.username, 'получил сообщение о Подземелье Грёз')
        except BotBlocked:
            print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        logging.error(f' [DREAM] {message.from_user.id} - ошибка в функции dream_notification: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[DREAM] {message.from_user.id} - '
                                      f'Произошла ошибка в функции dream_notification: {e}')
