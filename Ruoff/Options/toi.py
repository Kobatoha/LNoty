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


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class ToiTime(StatesGroup):
    waiting_for_toi_time = State()


# toi buttons
inline_toi_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_toi')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_toi')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_toi')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_toi')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_toi')

inline_toi_buttons.add(button_set, button_remove)


# toi SETTINGS
@dp.message_handler(commands=['toi'])
async def about_toi(message: types.Message):
    try:
        with Session() as session:

          user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
          option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
          if not option_setting:
              option = EssenceCustomSetting(id_user=user.telegram_id)
              session.add(option)
              session.commit()

        text = 'Башня Дерзости — межсерверная зона охоты для персонажей от 80 уровня и выше.\n'\
               'В ТОИ можно ежедневно выполнять задание - Охота в Башне Дерзости - за убийство 100 мобов '\
               'с зеленым титулом дадут 2 плаща защиты\n'\
               'Но самое интересное в Башне Дерзости - опыт и адена целых 14 часов в неделю'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_toi_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {message.from_user.id} - Произошла ошибка в функции about_toi: {e}')


# SELECT MENU FOR toi TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_toi'))
async def set_toi(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Башни Дерзости 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_toi: {e}')


# CANCEL MENU toi TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_toi'))
async def cancel_to_set_toi(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_toi: {e}')


# INPUT toi TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_toi'))
async def set_toi_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Башни Дерзости в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await ToiTime.waiting_for_toi_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_toi_time: {e}')


# SAVE toi TIME
@dp.message_handler(state=ToiTime.waiting_for_toi_time)
async def save_toi_time(message: types.Message, state: FSMContext):
    try:
        toi = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(toi) == 5 and toi[:2] in hours and toi[2] == ':' and toi[3:5] in minutes:
            with Session() as session:

                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    
                option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.toi = toi
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Башни Дерзости - {toi}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_toi_time: {e}')


# CANCEL SET toi TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_toi',
                           state=ToiTime.waiting_for_toi_time)
async def cancel_to_set_toi_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_toi_time: {e}')


# REMOVE toi TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_toi'))
async def remove_toi(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.toi = None
    
            session.commit()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Башне Дерзости убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_toi: {e}')


# SELECT USER WITH TRUE SETTING
async def toi_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                if user.server == 'ruoff':
                    option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                    if option and option.toi:
                        await toi_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[toi] {message.from_user.id} - '
                                      f'Произошла ошибка в функции toi_notification_wrapper: {e}')


# SEND toi MESSAGE
async def toi_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()

        toi = option.toi if option.toi else None
        # если не время и не место
        if toi and now != toi:
            return      
              
        # ежедневная напоминалка
        elif toi and now == toi:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Не забудь потратить все отведенное время в ТОИ - там классно!'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Башне Дерзости')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[toi] {message.from_user.id} - Произошла ошибка в функции toi_notification: {e}'
        )
