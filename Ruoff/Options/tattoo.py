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


class TattooTime(StatesGroup):
    waiting_for_tattoo_time = State()


# tattoo buttons
inline_tattoo_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_tattoo')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_tattoo')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_tattoo')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_tattoo')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_tattoo')

inline_tattoo_buttons.add(button_set, button_remove)


# tattoo SETTINGS
@dp.message_handler(commands=['tattoo'])
async def about_tattoo(message: types.Message):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            if not option_setting:
                option = EssenceCustomSetting(id_user=user.telegram_id)
                session.add(option)
                session.commit()

        text = 'Нанесение узора и прокачка скрытой силы - рутина, которая неслабо бустит внутрянку персонажа. '\
               'Прокачка происходит за счет Усилителя Скрытой Силы, бюджетно можно каждый день покупать 3шт '\
               'за 3кк адены в L магазине. С миру по нитке все однажды будут с 20-ым потенциалом, кек.'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_tattoo_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {message.from_user.id} - Произошла ошибка в функции about_tattoo: {e}')


# SELECT MENU FOR tattoo TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_tattoo'))
async def set_tattoo(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Прокачки Скрытой Силы 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_tattoo: {e}')


# CANCEL MENU tattoo TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_tattoo'))
async def cancel_to_set_tattoo(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_tattoo: {e}')


# INPUT tattoo TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_tattoo'))
async def set_tattoo_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Прокачки Скрытой Силы в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await TattooTime.waiting_for_tattoo_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_tattoo_time: {e}')


# SAVE tattoo TIME
@dp.message_handler(state=TattooTime.waiting_for_tattoo_time)
async def save_tattoo_time(message: types.Message, state: FSMContext):
    try:
        tattoo = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(tattoo) == 5 and tattoo[:2] in hours and tattoo[2] == ':' and tattoo[3:5] in minutes:
            with Session() as session:

                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    
                option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.tattoo = tattoo
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Прокачки Скрытой Силы - {tattoo}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_tattoo_time: {e}')


# CANCEL SET tattoo TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_tattoo',
                           state=TattooTime.waiting_for_tattoo_time)
async def cancel_to_set_tattoo_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_tattoo_time: {e}')


# REMOVE tattoo TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_tattoo'))
async def remove_tattoo(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.tattoo = None
    
            session.commit()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Прокачки Скрытой Силы убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_tattoo: {e}')


# SELECT USER WITH TRUE SETTING
async def tattoo_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                if option and option.tattoo:
                    await tattoo_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[tattoo] {message.from_user.id} - '
                                      f'Произошла ошибка в функции tattoo_notification_wrapper: {e}')


# SEND tattoo MESSAGE
async def tattoo_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()

        tattoo = option.tattoo if option.tattoo else None
        # если не время и не место
        if tattoo and now != tattoo:
            return      
                
        # ежедневная напоминалка
        elif tattoo and now == tattoo:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Купи Усилитель Скрытой Силы в L магазине и стань на полшишечки сильнее'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Прокачке Скрытой Силы')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[tattoo] {message.from_user.id} - Произошла ошибка в функции tattoo_notification: {e}'
        )
