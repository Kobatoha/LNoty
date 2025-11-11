from aiogram import Router, types, F
from aiogram.filters import Command
from DataBase.session import Session

from DataBase.User import User
from DataBase.Ruoff import LegacySetting, SamuraiSetting

router = Router()

# --- Кнопки ---
inline_server_buttons = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="ruoff essence", callback_data="ruoff_essence"),
            types.InlineKeyboardButton(text="ruoff legacy", callback_data="ruoff_legacy"),
            types.InlineKeyboardButton(text="ruoff samurai", callback_data="ruoff_samurai"),
        ]
    ]
)

@router.message(Command("server"))
async def choice_server(message: types.Message):
    await message.answer(
        "Выберите сервер, контент которого хотите отслеживать:",
        reply_markup=inline_server_buttons,
    )


@router.callback_query(F.data == "ruoff_essence")
async def ruoff_essence(callback: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
        if user:
            user.server = "essence"
            session.commit()
            await callback.message.answer(
                "✅ Вы выбрали получать оповещения с Essence серверов.\n"
                "[ Lilac | Plum | Amethyst ]"
            )
    await callback.answer()


@router.callback_query(F.data == "ruoff_legacy")
async def ruoff_legacy(callback: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
        setting = session.query(LegacySetting).filter_by(id_user=callback.from_user.id).first()
        if user:
            user.server = "legacy"
            if not setting:
                setting = LegacySetting(id_user=user.telegram_id)
                session.add(setting)
            session.commit()
            await callback.message.answer(
                "✅ Вы выбрали получать оповещения с Legacy серверов:\n"
                "[ Gran Kain | Valakas | Antharas | Lindvior ]"
            )
    await callback.answer()


@router.callback_query(F.data == "ruoff_samurai")
async def ruoff_samurai(callback: types.CallbackQuery):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
        setting = session.query(SamuraiSetting).filter_by(id_user=callback.from_user.id).first()
        if user:
            user.server = "ruoff_samurai"
            if not setting:
                setting = SamuraiSetting(id_user=user.telegram_id)
                session.add(setting)
            session.commit()
            await callback.message.answer(
                "✅ Вы выбрали получать оповещения с Samurai серверов.\n"
                "[ Samurai1 | Samurai2 ]"
            )
    await callback.answer()


@router.callback_query()
async def debug_all_callbacks(callback: types.CallbackQuery):
    print("Получен callback:", callback.data)
    await callback.answer("DEBUG")