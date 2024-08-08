from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils import Database
from states import CeleryStates

db = Database()


@dp.message_handler(Command("hello"))
async def handle_hello_command(message: types.Message):
    await CeleryStates.hello.set()
    await message.answer(f"Привет, {message.from_user.username}! Как ты сегодня?")
    db.add_to_queue(message.from_user.id)


@dp.message_handler(state=CeleryStates.hello)
async def handle_hello_answer(message: types.Message, state: FSMContext):
    await message.answer("Супер!")
    db.delete_from_queue(message.from_user.id)
