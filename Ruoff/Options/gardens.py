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
from Commands.options import options_menu_text
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class GardensTime(StatesGroup):
    waiting_for_gardens_time = State()


# gardens buttons
inline_gardens_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_gardens')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_gardens')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_gardens')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_gardens')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_gardens')

inline_gardens_buttons.add(button_set, button_remove)


# GARDENS SETTINGS
@dp.message_handler(commands=['gardens'])
async def about_gardens(message: types.Message):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        if not option_setting:
            option = EssenceCustomSetting(id_user=user.telegram_id)
            session.add(option)
            session.commit()
        session.close()

        text = 'Забытые сады — межсерверная зона охоты для персонажей от 76 уровня и выше. Во время входа в Сады'\
               ' персонажи могут выбрать одну из трех зон охоты:\n'\
               '\n'\
               'Первобытный Забытый Сад: Талисман Скорости\n'\
               'Сады Богини Евы: Талисман Евы\n'\
               'Сад Властителя: Талисман Властителя\n'\
               '\n'\
               'С особых монстров (Зеленый Титул) можно получить Книги Мастера и Талисманы соответствующей зоны'      

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_gardens_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {message.from_user.id} - Произошла ошибка в функции about_gardens: {e}')


# SELECT MENU FOR GARDENS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_gardens'))
async def set_gardens(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Забытого Сада 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_gardens: {e}')


# CANCEL MENU GARDENS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_gardens'))
async def cancel_to_set_gardens(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_gardens: {e}')


# INPUT GARDENS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_gardens'))
async def set_gardens_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Забытых Садов в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await GardensTime.waiting_for_gardens_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_gardens_time: {e}')


# SAVE GARDENS TIME
@dp.message_handler(state=GardensTime.waiting_for_gardens_time)
async def save_gardens_time(message: types.Message, state: FSMContext):
    try:
        gardens = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(gardens) == 5 and gardens[:2] in hours and gardens[2] == ':' and gardens[3:5] in minutes:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.gardens = gardens
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Забытых Садов - {gardens}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_gardens_time: {e}')


# CANCEL SET GARDENS TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_gardens',
                           state=GardensTime.waiting_for_gardens_time)
async def cancel_to_set_gardens_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_gardens_time: {e}')


# REMOVE GARDENS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_gardens'))
async def remove_gardens(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
        option_setting.gardens = None

        session.commit()
        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Забытых Садах убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_gardens: {e}')


# SELECT USER WITH TRUE SETTING
async def gardens_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()

        for user in users:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            if option and option.gardens:
                await gardens_notification(user)
        session.close()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[GARDENS] {message.from_user.id} - '
                                      f'Произошла ошибка в функции gardens_notification_wrapper: {e}')


# SEND GARDENS MESSAGE
async def gardens_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()

        gardens = option.gardens if option.gardens else None
        # если не время и не место
        if gardens and now != gardens:
            return      

        # финальная напоминалка       
        elif gardens and now == gardens and datetime.today().strftime('%A').lower() == 'вторник':
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Завтра Забытые Сады обновятся, ты точно добил 1000 мобов в каждой зоне?'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Забытых Садах')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
                
         # ежедневная напоминалка
        elif gardens and now == gardens:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Забытые Сады ждут своих героев. '
                    'Задача: постоять час и нафармить ежедневный квест '
                    '(100 мобов с титулом) во всех трех зонах'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Забытых Садах')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[GARDENS] {message.from_user.id} - Произошла ошибка в функции gardens_notification: {e}'
        )
