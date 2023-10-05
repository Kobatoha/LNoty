from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Expanse import Expanse
from DataBase.Ruoff import Setting, RuoffCustomSetting
from aiocron import crontab
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class Feedback(StatesGroup):
    waiting_for_feedback = State()


button_back = types.InlineKeyboardButton(text='Передумать, бот - збс!',
                                         callback_data='cancel_feedback')
button_add = types.InlineKeyboardButton(text='Оставить обратную связь',
                                        callback_data='add_feedback')

inline_feedback_buttons = types.InlineKeyboardMarkup().add(button_back, button_add)


# [FEEDBACK] @dp.message_handler(commands=['feedback'])
async def feedback(message: types.Message):
    try:
        await message.answer('Вы можете оставить обратную связь - вопросы, предложения или пожелания',
                             reply_markup=inline_feedback_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FEEDBACK] {message.from_user.id} - '
                                      f'Произошла ошибка в функции feedback: {e}')


# [CANCEL FEEDBACK] @dp.callback_query_handler(filters.Text(contains='cancel_feedback'))
async def cancel_feedback(callback_query: types.CallbackQuery):
    try:
        text = ''
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CANCEL FEEDBACK] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_feedback: {e}')


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
