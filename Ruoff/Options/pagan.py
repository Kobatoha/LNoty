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


class PaganTime(StatesGroup):
    waiting_for_pagan_time = State()


# pagan buttons
inline_pagan_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_pagan')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_pagan')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_pagan')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_pagan')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_pagan')

inline_pagan_buttons.add(button_set, button_remove)


# pagan SETTINGS
@dp.message_handler(commands=['pagan'])
async def about_pagan(message: types.Message):
    try:
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            if not option_setting:
                option = EssenceCustomSetting(id_user=user.telegram_id)
                session.add(option)
                session.commit()

        text = 'Исследование Крепости Кельбима и Языческого Храма — межсерверная зона для персонажей от 85 уровня и выше. '\
               'Доступна с понедельника по пятницу + в воскресенье после 00:00 можно выполнить квест 6-й раз за неделю.'\
               'Дается 10 часов в неделю + каждый день можно лутать по проходке за задание на убийство 300 мобов. '\
               'Каждую неделю меняется локация, но проходки падают ежедневно на обе зоны.'\

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_pagan_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {message.from_user.id} - Произошла ошибка в функции about_pagan: {e}')


# SELECT MENU FOR pagan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_pagan'))
async def set_pagan(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Пагана и Кельбима 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_pagan: {e}')


# CANCEL MENU pagan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_pagan'))
async def cancel_to_set_pagan(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_pagan: {e}')


# INPUT pagan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_pagan'))
async def set_pagan_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Пагана и Кельбами в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await PaganTime.waiting_for_pagan_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_pagan_time: {e}')


# SAVE pagan TIME
@dp.message_handler(state=PaganTime.waiting_for_pagan_time)
async def save_pagan_time(message: types.Message, state: FSMContext):
    try:
        pagan = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(pagan) == 5 and pagan[:2] in hours and pagan[2] == ':' and pagan[3:5] in minutes:
            with Session() as session: 

                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    
                option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.pagan = pagan
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Пагана и Кельбима - {pagan}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_pagan_time: {e}')


# CANCEL SET pagan TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_pagan',
                           state=PaganTime.waiting_for_pagan_time)
async def cancel_to_set_pagan_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_pagan_time: {e}')


# REMOVE pagan TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_pagan'))
async def remove_pagan(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.pagan = None
    
            session.commit()
            
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Пагане и Кельбиме убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_pagan: {e}')


# SELECT USER WITH TRUE SETTING
async def pagan_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()
                if option and option.pagan:
                    await pagan_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[pagan] {message.from_user.id} - '
                                      f'Произошла ошибка в функции pagan_notification_wrapper: {e}')


# SEND pagan MESSAGE
async def pagan_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(EssenceCustomSetting).filter_by(id_user=user.telegram_id).first()

        pagan = option.pagan if option.pagan else None
        # если не время и не место
        if pagan and now != pagan:
            return      

        # ежедневная напоминалка
        elif pagan and now == pagan:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Пора на межсервер - Паган или Кельбим, что-то там точно есть.'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Пагане и Кельбима')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[pagan] {message.from_user.id} - Произошла ошибка в функции pagan_notification: {e}'
        )
