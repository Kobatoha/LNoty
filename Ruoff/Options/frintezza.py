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


class FrintezzaTime(StatesGroup):
    waiting_for_frintezza_time = State()


# frintezza buttons
inline_frintezza_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_frintezza')
button_set_day = types.InlineKeyboardButton(text='Установить день', callback_data='ruoff_option_set_day_frintezza')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_frintezza')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_frintezza')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_frintezza')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_frintezza')

inline_frintezza_buttons.add(button_set, button_remove)


# FRINTEZZA TEMP SETTINGS
@dp.message_handler(commands=['frintezza'])
async def about_frintezza(message: types.Message):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        if not option_setting:
            option = EssenceCustomSetting(id_user=user.telegram_id)
            session.add(option)
            session.commit()
        session.close()

        text = 'Поход на Фринтезу — временная зона охоты для 15+ персонажей'\
               ' от 76 уровня и выше. Доступна раз в неделю, откат зоны в среду в 6:30 по МСК.\n' \
               '\n' \
               'В зоне вас ждут мобы и финальный босс, который по фану может отхиливаться на фуллхп. Дроп:\n' \
               '- Ожерелье Фринтезы\n' \
               '- Камни зачарования\n' \
               '- Свитки благословения\n' \
               '- Топ А армор и веапон\n' \
               '- Точки А армор и веапон\n' \
               '- Краски ур.3\n' \
               '- Кристаллы крови\n' \
               '\n'\
               '🔥 Самым удачливым может отсыпать дропа в виде книги 4*'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_frintezza_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {message.from_user.id} - '
                                      f'Произошла ошибка в функции about_frintezza: {e}')


# SELECT MENU FOR FRINTEZZA TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_frintezza'))
async def set_frintezza(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_day, button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Похода на Фринтезу 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_frintezza: {e}')


# CANCEL MENU FRINTEZZA TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_frintezza'))
async def cancel_to_set_frintezza(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_frintezza: {e}')


# INPUT FRINTEZZA TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_frintezza'))
async def set_frintezza_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Похода на Фринтезу в формате час:минута (например, 10:21 или 01:42): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await FrintezzaTime.waiting_for_frintezza_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_frintezza_time: {e}')


# SAVE FRINTEZZA TIME
@dp.message_handler(state=FrintezzaTime.waiting_for_frintezza_time)
async def save_frintezza_time(message: types.Message, state: FSMContext):
    try:
        frintezza_time = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(frintezza_time) == 5 and frintezza_time[:2] in hours\
                and frintezza_time[2] == ':' and frintezza_time[3:5] in minutes:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.frintezza_time = frintezza_time
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_day, button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Похода на Фринтезу - {frintezza_time}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_frintezza_time: {e}')


# CANCEL SET FRINTEZZA TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_frintezza',
                           state=FrintezzaTime.waiting_for_frintezza_time)
async def cancel_to_set_frintezza_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_frintezza_time: {e}')


# INPUT FRINTEZZA DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_day_frintezza'))
async def set_frintezza_day(callback_query: types.CallbackQuery):
    try:
        button_mon = types.InlineKeyboardButton(text='понедельник', callback_data='add_frintezza_monday')
        button_tue = types.InlineKeyboardButton(text='вторник', callback_data='add_frintezza_tuesday')
        button_wed = types.InlineKeyboardButton(text='среда', callback_data='add_frintezza_wednesday')
        button_thu = types.InlineKeyboardButton(text='четверг', callback_data='add_frintezza_thursday')
        button_fri = types.InlineKeyboardButton(text='пятница', callback_data='add_frintezza_friday')
        button_sat = types.InlineKeyboardButton(text='суббота', callback_data='add_frintezza_saturday')
        button_sun = types.InlineKeyboardButton(text='воскресенье', callback_data='add_frintezza_sunday')
        keyboard = types.InlineKeyboardMarkup(row_width=3).add(button_mon, button_tue, button_wed,
                                                               button_thu, button_fri, button_sat,
                                                               button_sun).row(button_back)
        await callback_query.message.edit_text('Выберите день недели оповещения для Похода на Фринтезу:\n ',
                                               reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_frintezza_day: {e}')


# SAVE FRINTEZZA DAY
@dp.callback_query_handler(lambda c: c.data.startswith('add_frintezza_'))
async def save_frintezza_day(callback_query: types.CallbackQuery):
    try:
        day_frintezza = None
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()

        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=callback_query.from_user.id).first()
        if callback_query.data == 'add_frintezza_monday':
            option_setting.frintezza_day = 'понедельник'
            session.commit()
            day_frintezza = 'понедельник'
        elif callback_query.data == 'add_frintezza_tuesday':
            option_setting.frintezza_day = 'вторник'
            session.commit()
            day_frintezza = 'вторник'
        elif callback_query.data == 'add_frintezza_wednesday':
            option_setting.frintezza_day = 'среда'
            session.commit()
            day_frintezza = 'среда'
        elif callback_query.data == 'add_frintezza_thursday':
            option_setting.frintezza_day = 'четверг'
            session.commit()
            day_frintezza = 'четверг'
        elif callback_query.data == 'add_frintezza_friday':
            option_setting.frintezza_day = 'пятница'
            session.commit()
            day_frintezza = 'пятница'
        elif callback_query.data == 'add_frintezza_saturday':
            option_setting.frintezza_day = 'суббота'
            session.commit()
            day_frintezza = 'суббота'
        elif callback_query.data == 'add_frintezza_sunday':
            option_setting.frintezza_day = 'воскресенье'
            session.commit()
            day_frintezza = 'воскресенье'

        user.upd_date = datetime.today()
        session.commit()

        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=f'Вы установили день для оповещений Похода на Фринтезу - {day_frintezza}',
                                      reply_markup=keyboard)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции save_frintezza_day: {e}')


# CANCEL SET FRINTEZZA DAY
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_frintezza')
async def cancel_to_set_frintezza_day(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_frintezza_day: {e}')


# REMOVE FRINTEZZA TIME AND DAY
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_frintezza'))
async def remove_frintezza(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        option_setting.frintezza_time = None
        option_setting.frintezza_day = None

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
                                 text=f'[FRINTEZZA] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_frintezza: {e}')


# SELECT USER WITH TRUE SETTING
async def frintezza_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()

        for user in users:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            if option and option.frintezza_time and option.frintezza_day:
                await frintezza_notification(user)
        session.close()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {message.from_user.id} - '
                                      f'Произошла ошибка в функции frintezza_notification_wrapper: {e}')


# SEND FRINTEZZA MESSAGE
async def frintezza_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')
        today = datetime.now().strftime('%A').lower()

        session = Session()
        option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        session.close()

        frintezza_day = option.frintezza_day.lower() if option.frintezza_day else None
        if frintezza_day and today != frintezza_day:
            return

        frintezza_time = option.frintezza_time if option.frintezza_time else None
        if frintezza_time and now != frintezza_time:
            return

        try:
            await mybot.send_message(user.telegram_id,
                                     'Пора отправляться в Поход на Фринтезу! '
                                     'Скорее собирай ЦЦ и отправляйся в Аден к Фонтану.')
            print(now, user.telegram_id, user.username, 'получил сообщение о Походе на Фринтезу')
        except BotBlocked:
            print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FRINTEZZA] {message.from_user.id} - '
                                      f'Произошла ошибка в функции frintezza_notification: {e}')
