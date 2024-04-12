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
from config import DB_URL, TOKEN, test_token
from aiogram.utils.exceptions import BotBlocked
from Commands.options import options_menu_text


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class GoddardTime(StatesGroup):
    waiting_for_goddard_time = State()


# goddard buttons
inline_goddard_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_goddard')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_goddard')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_goddard')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_goddard')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_goddard')

inline_goddard_buttons.add(button_set, button_remove)


# goddard SETTINGS
@dp.message_handler(commands=['goddard'])
async def about_goddard(message: types.Message):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
        if not option_setting:
            option = RuoffCustomSetting(id_user=user.telegram_id)
            session.add(option)
            session.commit()
        session.close()

        text = 'Исследование Годдарда - ежедневное задание для персонажей от 85 уровня и выше.\n'\
               'Цель: убить 1000 монстров\n'\
               'Награда: древняя адена х100\n'\
               'Локация:\n'\
               '- Горячие Источники 85~87\n'\
               '- Каньон Горда 87~90\n'\
               '- Крепость Фавносов 90~92\n'\
               '- Военная База Моргоса 90~92\n'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_goddard_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {message.from_user.id} - Произошла ошибка в функции about_goddard: {e}')


# SELECT MENU FOR goddard TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_goddard'))
async def set_goddard(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Исследование Годдарда 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_goddard: {e}')


# CANCEL MENU goddard TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_goddard'))
async def cancel_to_set_goddard(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_goddard: {e}')


# INPUT GARDENS TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_goddard'))
async def set_goddard_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Исследования Годдарда в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await GoddardTime.waiting_for_goddard_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_goddard_time: {e}')


# SAVE goddard TIME
@dp.message_handler(state=GardensTime.waiting_for_goddard_time)
async def save_goddard_time(message: types.Message, state: FSMContext):
    try:
        goddard = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(goddard) == 5 and goddard[:2] in hours and goddard[2] == ':' and goddard[3:5] in minutes:
            session = Session()

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.goddard = goddard
            session.commit()

            user.upd_date = datetime.today()
            session.commit()

            session.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Исследования Годдарда - {goddard}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_goddard_time: {e}')


# CANCEL SET goddard TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_goddard',
                           state=GardensTime.waiting_for_goddard_time)
async def cancel_to_set_goddard_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_goddard_time: {e}')


# REMOVE goddard TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_goddard'))
async def remove_goddard(callback_query: types.CallbackQuery):
    try:
        session = Session()

        user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
        option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
        option_setting.goddard = None

        session.commit()
        session.close()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Исследовании Годдарда убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_goddard: {e}')


# SELECT USER WITH TRUE SETTING
async def goddard_notification_wrapper():
    try:
        session = Session()
        users = session.query(User).all()

        for user in users:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            if option and option.goddard:
                await goddard_notification(user)
        session.close()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[goddard] {message.from_user.id} - '
                                      f'Произошла ошибка в функции goddard_notification_wrapper: {e}')


# SEND goddard MESSAGE
async def goddard_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

        goddard = option.goddard if option.goddard else None
        # если не время и не место
        if goddard and now != goddard:
            return      
                
         # ежедневная напоминалка
        elif goddard and now == goddard:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Пора исследовать Годдард.\n'
                    'Задача: убить 1000 мобов и залутать 100 антички'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение об Исследовании Годдарда')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[goddard] {message.from_user.id} - Произошла ошибка в функции goddard_notification: {e}'
        )
