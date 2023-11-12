import pytest
from unittest.mock import AsyncMock, patch
from Ruoff.BigWars.bigwar_gardens import bigwar_gardens_notification


@pytest.mark.asyncio
async def test_bigwar_gardens_notification():
    user = ...  # Создайте объект RuoffBigWar для тестирования
    with patch('file_with_your_code.mybot.send_message', new_callable=AsyncMock) as send_message_mock:
        await bigwar_gardens_notification(user)
        send_message_mock.assert_awaited_once_with(user.id_user, '🌈🌈 [BIGWAR] Забытые Сады через 15 минут')

    # Тест обработки исключения
    with patch('file_with_your_code.mybot.send_message', side_effect=BotBlocked):
        with pytest.raises(BotBlocked):
            await bigwar_gardens_notification(user)