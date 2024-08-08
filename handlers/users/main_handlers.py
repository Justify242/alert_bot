from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def handle_start_command(message: types.Message, state: FSMContext):
    """
    Хандлер команды /start
    """

    await state.finish()
    await message.answer(text="Добро пожаловать в наш бот!")


@dp.message_handler(CommandHelp(), state="*")
async def handle_help_command(message: types.Message, state: FSMContext):
    """
    Хандлер команды /help
    """

    await state.finish()
    await message.answer("Доступные команды: /start, /help, /echo, /photo")






