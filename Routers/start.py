from aiogram import Router, types, F
from aiogram.filters import Command
from DataBase.session import Session

from DataBase.User import User
from DataBase.Ruoff import LegacySetting, EssenceSetting, EssenceCustomSetting

router = Router()
from datetime import datetime
from Routers.server import inline_server_buttons


@router.message(Command("start"))
async def start(message: types.Message):
    now = datetime.now().strftime('%H:%M')
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        print(now, 'Добавление нового пользователя...')
        user = User(telegram_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
        setting = EssenceSetting(id_user=user.telegram_id)
        session.add(setting)
        session.commit()
        custom = EssenceCustomSetting(id_user=user.telegram_id)
        session.add(custom)
        session.commit()
        print(now, user.telegram_id, user.username, '- добавлен новый пользователь')

    else:
        user.upd_date = datetime.today()
        session.commit()
        if not user.username:  # если username еще не указан
            user.username = message.from_user.username  # обновляем username
            session.commit()
            print(now, user.telegram_id, user.username, '- username добавлен')
        else:
            print(now, user.telegram_id, user.username, '- уже добавлен')
    session.close()
    await message.answer('Привет! Я - твой помощник, брат, сват, мать и питомец.\n'
                         'В Меню ты найдешь все доступные команды.\n'
                         'Так же этот список можно вызвать командой /help\n' 
                         'Бот по-дефолту работает в работяжном режиме с 8:00 до 23:00,'
                         ' изменить эту настройку можно по команде /time\n'
                         '\n'
                         'Выбирай интересующую активность и жми [Установить оповещение].'
                         ' В таком случае тебе будут приходить уведомления за 5 минут'
                         ' до начала события.\n'
                         '\n'
                         'За это время ты успеешь налить чайку,'
                         ' закинуть в рот печеньку и удобно устроиться перед монитором.\n'
                         '\n'
                         'А теперь пора выбрать свой сервер :)',
                         reply_markup=inline_server_buttons)
