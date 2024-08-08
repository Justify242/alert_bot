from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from states import EchoState


# ===== Эхо бот ===== #


@dp.message_handler(Command("echo"))
async def handle_echo_command(message: types.Message):
    """
    Хандлер команды /echo
    """

    await message.answer("Введите текст сообщения")
    await EchoState.echo.set()


@dp.message_handler(state=EchoState.echo)
async def handle_echo_message(message: types.Message):
    """
    Хандлер сообщения эхо-бота
    """

    await message.answer(message.text)