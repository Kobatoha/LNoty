from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
from DataBase.Feedback import Feedback
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot, storage=MemoryStorage())

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


button_back = types.InlineKeyboardButton(text='Передумать, бот - збс!',
                                         callback_data='back_feedback')
button_add = types.InlineKeyboardButton(text='Написать отзыв',
                                        callback_data='add_feedback')
button_cancel = types.InlineKeyboardButton(text='Я стесняюсь! Вернемся назад!',
                                           callback_data='cancel_add_feedback')

inline_feedback_buttons = types.InlineKeyboardMarkup().add(button_add, button_back)


# [FEEDBACK]
async def feedback(message: types.Message):
    try:
        await message.answer('Вы обратились в службу доставки отзывов и предложений!\n'
                             '\n'
                             'Мы не Почта России, мы не теряем посылки и не предлагаем лотерейные билеты.'
                             ' Обращайтесь к нам и ваше послание всенепременно дойдет до разработчика!',
                             reply_markup=inline_feedback_buttons)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[FEEDBACK] {message.from_user.id} - '
                                      f'Произошла ошибка в функции feedback: {e}')


# [CANCEL FEEDBACK]
async def cancel_feedback(callback_query: types.CallbackQuery):
    try:
        text = 'Доступные команды:\n'\
               '\n'\
               '/start - запуск бота\n'\
               '/about - о боте\n'\
               '/mysettings - персональные настройки\n'\
               '/help - список команд\n'\
               '/donate - разработчику на мармелад\n' \
               '/feedback - оставить предложение\n'\
               '\n'\
               '/stop - отменить все оповещения\n'\
               '\n'\
               '/time - установить время работы оповещений\n'\
               '/event - пока не подвезли\n'\
               '/calendar - закончился\n'\
               '/kuka - Кука и Джисра\n'\
               '/loa - Логово Антараса\n'\
               '/frost - Замок Монарха Льда\n'\
               '/fortress - Крепость Орков\n'\
               '/balok - Битва с Валлоком\n'\
               '/olympiad - Всемирная Олимпиада\n'\
               '/hellbound - Остров Ада\n'\
               '/siege - Осада Гирана\n'\
               '\n'\
               '/primetime - Прайм Тайм Зачистки\n'\
               '/purge - Зачистка\n'

        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text)

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CANCEL FEEDBACK] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_feedback: {e}')


# [ADD FEEDBACK]
async def add_feedback(callback_query: types.CallbackQuery):
    try:
        keyboard = types.InlineKeyboardMarkup().add(button_cancel)
        text = f'Напишите отзыв, пожелание или конкретное предложение (ограничение 300 cимволов): '
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text,
                                      reply_markup=keyboard)

        await FeedbackState.waiting_for_feedback.set()
        await callback_query.answer()

    except Exception as e:
        await mybot.send_message(chat_id='952604184',
                                 text=f'[ADD FEEDBACK] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции add_feedback: {e}')


# [SAVE FEEDBACK]
async def save_feedback(message: types.Message, state: FSMContext):
    try:
        feedback_ = message.text

        if len(feedback_) > 300:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Слишком длинный текст, попробуйте еще раз (не более 300 символов).')
            return

        elif not feedback_ or len(feedback_) < 3:
            await mybot.send_message(chat_id=message.from_user.id,
                                     text='Если не хотите оставлять оставлять отзыв или предложение, '
                                          'так и скажите, я же не заставляю ))')
            await state.finish()
            return

        else:
            session = Session()
            user = Feedback(telegram_id=message.from_user.id,
                            username=message.from_user.username,
                            text=feedback_)
            session.add(user)
            session.commit()
            session.close()

            await mybot.send_message(chat_id=message.from_user.id,
                                     text=f'Вы успешно оставили свое послание. Спасибо, Добби свободен!\n'
                                          f'\n'
                                          f'Можете продолжить устанавливать оповещения или отменять их - /help')

        await state.finish()

    except Exception as e:
        logging.error(f' [SAVE FEEDBACK] {message.from_user.id} - ошибка в функции save_feedback: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[SAVE FEEDBACK] {message.from_user.id} - '
                                      f'Произошла ошибка в функции save_feedback: {e}')


# [CANCEL ADD FEEDBACK]
async def cancel_add_feedback(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        text = 'Вы обратились в службу доставки отзывов и предложений!\n'\
               '\n'\
               'И передумали.. понимаю, бывает ))\n' \
               'В таком случае могу предложить погулять по настройкам /help или убедиться,' \
               ' что все включено - /mysettings'
        await mybot.answer_callback_query(callback_query.id)
        await mybot.edit_message_text(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      text=text)
        await state.finish()

    except Exception as e:
        logging.error(f' [CANCEL ADD FEEDBACK] {callback_query.from_user.id} - '
                      f'ошибка в функции cancel_add_feedback: {e}')
        await mybot.send_message(chat_id='952604184',
                                 text=f'[CANCEL ADD FEEDBACK] {callback_query.from_user.id} - '
                                      f'Произошла ошибка в функции cancel_add_feedback: {e}')
