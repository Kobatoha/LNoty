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


class TranscendentTime(StatesGroup):
    waiting_for_transcendent_time = State()


# transcendent buttons
inline_transcendent_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_transcendent')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_transcendent')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_transcendent')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_transcendent')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_transcendent')

inline_transcendent_buttons.add(button_set, button_remove)


# transcendent SETTINGS
@dp.message_handler(commands=['transcendent'])
async def about_transcendent(message: types.Message):
    try:
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            if not option_setting:
                option = RuoffCustomSetting(id_user=user.telegram_id)
                session.add(option)
                session.commit()

        text = 'Невероятная временная зона — 10 минут безудержного опыта (нет).'  

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_transcendent_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {message.from_user.id} - Произошла ошибка в функции about_transcendent: {e}')


# SELECT MENU FOR transcendent TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_transcendent'))
async def set_transcendent(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Невероятной временной зоны 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_transcendent: {e}')


# CANCEL MENU transcendent TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_transcendent'))
async def cancel_to_set_transcendent(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_transcendent: {e}')


# INPUT transcendent TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_transcendent'))
async def set_transcendent_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Невероятной временной зоны в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await TranscendentTime.waiting_for_transcendent_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_transcendent_time: {e}')


# SAVE transcendent TIME
@dp.message_handler(state=TranscendentTime.waiting_for_transcendent_time)
async def save_transcendent_time(message: types.Message, state: FSMContext):
    try:
        transcendent = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(transcendent) == 5 and transcendent[:2] in hours and transcendent[2] == ':' and transcendent[3:5] in minutes:
            with Session() as session: 

                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    
                option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.transcendent = transcendent
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Невероятной временной зоны - {transcendent}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_transcendent_time: {e}')


# CANCEL SET transcendent TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_transcendent',
                           state=TranscendentTime.waiting_for_transcendent_time)
async def cancel_to_set_transcendent_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_transcendent_time: {e}')


# REMOVE transcendent TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_transcendent'))
async def remove_transcendent(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.transcendent = None
    
            session.commit()
            
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Невероятной временной зоне убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_transcendent: {e}')


# SELECT USER WITH TRUE SETTING
async def transcendent_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                if option and option.transcendent:
                    await transcendent_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[transcendent] {message.from_user.id} - '
                                      f'Произошла ошибка в функции transcendent_notification_wrapper: {e}')


# SEND transcendent MESSAGE
async def transcendent_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

        transcendent = option.transcendent if option.transcendent else None
        # если не время и не место
        if transcendent and now != transcendent:
            return      

        # ежедневная напоминалка
        elif transcendent and now == transcendent:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Иди фарми Невероятку'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Невероятной Временной Зоне')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[transcendent] {message.from_user.id} - Произошла ошибка в функции transcendent_notification: {e}'
        )
