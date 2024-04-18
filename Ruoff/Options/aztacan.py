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
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class AztacanTime(StatesGroup):
    waiting_for_aztacan_time = State()


# aztacan buttons
inline_aztacan_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_aztacan')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_aztacan')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_aztacan')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_aztacan')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_aztacan')

inline_aztacan_buttons.add(button_set, button_remove)


# aztacan SETTINGS
@dp.message_handler(commands=['aztacan'])
async def about_aztacan(message: types.Message):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            if not option_setting:
                option = RuoffCustomSetting(id_user=user.telegram_id)
                session.add(option)
                session.commit()

        text = 'Храм Ацтакана — межсерверная зона охоты для персонажей от 60 уровня и выше. Ежедневно дается 1 час времени + '\
               'можно продлить на 2 часа. С монстров зоны с определенной вероятностью можно получить Кристалл Тантар, '\
               ' из которых с шансом можно сварить Серьгу Охотника. Во время еженедельной профилактики все кристаллы сгорают.'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_aztacan_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {message.from_user.id} - Произошла ошибка в функции about_aztacan: {e}')


# SELECT MENU FOR aztacan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_aztacan'))
async def set_aztacan(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Храма Ацтакана 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_aztacan: {e}')


# CANCEL MENU aztacan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_aztacan'))
async def cancel_to_set_aztacan(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_aztacan: {e}')


# INPUT aztacan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_aztacan'))
async def set_aztacan_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Храма Ацтакана в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await AztacanTime.waiting_for_aztacan_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_aztacan_time: {e}')


# SAVE aztacan TIME
@dp.message_handler(state=AztacanTime.waiting_for_aztacan_time)
async def save_aztacan_time(message: types.Message, state: FSMContext):
    try:
        aztacan = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(aztacan) == 5 and aztacan[:2] in hours and aztacan[2] == ':' and aztacan[3:5] in minutes:
            with Session() as session:

                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    
                option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.aztacan = aztacan
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Храма Ацтакана - {aztacan}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_aztacan_time: {e}')


# CANCEL SET aztacan TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_aztacan',
                           state=AztacanTime.waiting_for_aztacan_time)
async def cancel_to_set_aztacan_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_aztacan_time: {e}')


# REMOVE aztacan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_aztacan'))
async def remove_aztacan(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.aztacan = None
    
            session.commit()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Храме Ацтакана убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_aztacan: {e}')


# SELECT USER WITH TRUE SETTING
async def aztacan_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                if option and option.aztacan:
                    await aztacan_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[aztacan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции aztacan_notification_wrapper: {e}')


# SEND aztacan MESSAGE
async def aztacan_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

        aztacan = option.aztacan if option.aztacan else None
        # если не время и не место
        if aztacan and now != aztacan:
            return      

        # финальная напоминалка       
        elif aztacan and now == aztacan and datetime.today().strftime('%A').lower() == 'вторник':
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Завтра профилактика, успей использовать все-все-все Кристаллы Тантар'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Храме Ацтакана')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)
                
         # ежедневная напоминалка
        elif aztacan and now == aztacan:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Пора в Храм Ацтакана фармить Серьгу Охотника, кек'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Храме Ацтакана')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[aztacan] {message.from_user.id} - Произошла ошибка в функции aztacan_notification: {e}'
        )
