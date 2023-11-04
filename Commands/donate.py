from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBase.User import User
from DataBase.Base import Base
import asyncio
from datetime import datetime


mybot = Bot(token=TOKEN)
dp = Dispatcher(mybot)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


# donate buttons
inline_donate_buttons = types.InlineKeyboardMarkup()

b1 = types.InlineKeyboardButton(text='Сбербанк', callback_data='sberbank')
b2 = types.InlineKeyboardButton(text='Tinkoff', callback_data='tinkoff')
b3 = types.InlineKeyboardButton(text='BTC', callback_data='bitcoin')
b4 = types.InlineKeyboardButton(text='ETH', callback_data='ethereum')

inline_donate_buttons.add(b1, b2)
inline_donate_buttons.row(b3, b4)


@dp.message_handler(commands=['donate'])
async def donate(message: types.Message):
    await message.answer('Сказать спасибо можно по-разному, но ничего лучше нет'
                         ' звона чеканной монеты 💰', reply_markup=inline_donate_buttons)


@dp.callback_query_handler(filters.Text(contains='sberbank'))
async def donate_sberbank(callback_query: types.CallbackQuery):

    await callback_query.message.answer('2202203654131582')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='tinkoff'))
async def donate_tinkoff(callback_query: types.CallbackQuery):

    await callback_query.message.answer('5536913992791521')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='bitcoin'))
async def donate_bitcoin(callback_query: types.CallbackQuery):

    await callback_query.message.answer('bc1q3fdst4yce8nywz724crqgn2dttalxjl67jmn5a')
    await callback_query.answer()


@dp.callback_query_handler(filters.Text(contains='ethereum'))
async def donate_ethereum(callback_query: types.CallbackQuery):

    await callback_query.message.answer('0x8aed63048C527f09cE1960cDbA40c137412494e9')
    await callback_query.answer()
