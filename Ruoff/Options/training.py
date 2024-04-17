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


class TrainingTime(StatesGroup):
    waiting_for_training_time = State()


# training buttons
inline_training_buttons = types.InlineKeyboardMarkup()

button_set = types.InlineKeyboardButton(text='Установить оповещение', callback_data='ruoff_option_set_training')
button_set_time = types.InlineKeyboardButton(text='Установить время', callback_data='ruoff_option_set_time_training')
button_remove = types.InlineKeyboardButton(text='Убрать оповещение', callback_data='ruoff_option_remove_training')

button_back = types.InlineKeyboardButton(text='<< резко передумать и вернуться',
                                         callback_data='ruoff_option_cancel_to_set_training')
button_menu = types.InlineKeyboardButton(text='Вернуться к списку активностей',
                                         callback_data='ruoff_option_cancel_to_set_training')

inline_training_buttons.add(button_set, button_remove)


# training SETTINGS
@dp.message_handler(commands=['training'])
async def about_training(message: types.Message):
    try:
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            if not option_setting:
                option = RuoffCustomSetting(id_user=user.telegram_id)
                session.add(option)
                session.commit()

        text = 'Тренировочное Подземелье — особая зона охоты для персонажей от 76 уровня и выше. Войти можно в любое время, а на прохождение'\
               ' дается 1 час (отчет начинается с момента входа в зону).\n'\
               '\n'\
               '!!Следует помнить, что Тренировка - этот сессионная зона, и выйти из тренировки, '\
               'чтобы быстро зайти, например, на валакаса или ивент с убийством эпиков, а потом вернуться - не получится.\n'\
               '\n'\
               'В тренировке можно выбрать самый идеальный спот и за 1500 руды духа забрать максимальный бафф = \n'\
               'час идеального кача, где никто не мешает, никто не пкашит и все мобы пренажлежат тебе.\n'\
               '\n'\
               'За 10 минут до конца появляется Босс. \n'\
               'Подсказка №1: если в 10:30 выйти из текущей локации, у НПС Гроун поменять зону на ТОИ12, '\
               'в 09:59 у того же НПС Гроун вернуть свою зону, то вас будет ждать максимальный босс в Тренировке. '\
               'С него сыпется больше всякого интересного. Конечно, только с учетом того, что вы не откинетесь 🫶\n'\
               'Подсказка №2: если зайти в тренировку в хоттайм зачистки, можно залутать ключики из тех локаций, '\
               'где обычно мест нет, например, на орках. А с босса такой локации, к слову, очков зачистки сыпет очень много.'

        await mybot.send_message(chat_id=message.from_user.id,
                                 text=text,
                                 reply_markup=inline_training_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {message.from_user.id} - Произошла ошибка в функции about_training: {e}')


# SELECT MENU FOR training TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_training'))
async def set_training(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_set_time, button_back)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Сейчас вы в меню настроек оповещений Тренировочного Подземелья 🧐',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_training: {e}')


# CANCEL MENU training TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_cancel_to_set_training'))
async def cancel_to_set_training(callback_query: types.CallbackQuery):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_training: {e}')


# INPUT training TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_set_time_training'))
async def set_training_time(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_back)
        text = f'НАПИШИТЕ время оповещения для Тренировочного Подземелья в формате час:минута (например, 10:21 или 01:24): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await TrainingTime.waiting_for_training_time.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции set_training_time: {e}')


# SAVE training TIME
@dp.message_handler(state=TrainingTime.waiting_for_training_time)
async def save_training_time(message: types.Message, state: FSMContext):
    try:
        training = message.text
        hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
        for h in range(10, 61):
            minutes.append(str(h))

        if len(training) == 5 and training[:2] in hours and training[2] == ':' and training[3:5] in minutes:
            with Session() as session:
                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
                
                option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                option_setting.training = training
                session.commit()
    
                user.upd_date = datetime.today()
                session.commit()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы установили время для оповещений Тренировочного Подземелья - {training}',
                                     reply_markup=keyboard)

        else:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Неправильный формат времени, пожалуйста, попробуйте еще раз.')
            return

        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_training_time: {e}')


# CANCEL SET training TIME
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ruoff_option_cancel_to_set_training',
                           state=TrainingTime.waiting_for_training_time)
async def cancel_to_set_training_time(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=options_menu_text)
        await state.finish()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_to_set_training_time: {e}')


# REMOVE training TIME
@dp.callback_query_handler(filters.Text(contains='ruoff_option_remove_training'))
async def remove_training(callback_query: types.CallbackQuery):
    try:
        with Session() as session:

            user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
            option_setting = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
            option_setting.training = None
    
            session.commit()

        keyboard = types.InlineKeyboardMarkup(row_width=2).add(button_menu)

        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text='Оповещение о Тренировочном Подземелье убрано',
                                      reply_markup=keyboard)
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {message.from_user.id} - '
                                      f'Произошла ошибка в функции remove_training: {e}')


# SELECT USER WITH TRUE SETTING
async def training_notification_wrapper():
    try:
        with Session() as session:
            users = session.query(User).all()
    
            for user in users:
                option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()
                if option and option.training:
                    await training_notification(user)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[training] {message.from_user.id} - '
                                      f'Произошла ошибка в функции training_notification_wrapper: {e}')


# SEND training MESSAGE
async def training_notification(user: User):
    try:
        now = datetime.now().strftime('%H:%M')

        with Session() as session:
            option = session.query(RuoffCustomSetting).filter_by(id_user=user.telegram_id).first()

        training = option.training if option.training else None
        # если не время и не место
        if training and now != training:
            return      
                
        # ежедневная напоминалка
        elif training and now == training:
            try:
                await mybot.send_message(
                    user.telegram_id,
                    'Тренировочное Подземелье ждет. '
                    'Не забудьте выбрать самого сочного босса до 10:00!'
                )
                print(now, user.telegram_id, user.username, 'получил сообщение о Тренировочном Подземелье')
            except BotBlocked:
                print('[ERROR] Пользователь заблокировал бота:', now, user.telegram_id, user.username)

    except Exception as e:
        await mybot.send_message(
            chat_id='952604184',
            text=f'[training] {message.from_user.id} - Произошла ошибка в функции training_notification: {e}'
        )
