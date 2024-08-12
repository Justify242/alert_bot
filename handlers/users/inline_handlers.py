from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.inline import SelectionInlineKeyboard
from keyboards.inline.base_keyboards import callback_data as cd


# ===== Работа с inline кнопками ===== #


@dp.message_handler(Command("inline"), state="*")
async def handle_inline_command(message: types.Message, state: FSMContext):
    """
    Хандлер команды /inline
    """
    
    await state.finish()
    
    markup = SelectionInlineKeyboard()
    await message.answer("Выберите действие", reply_markup=markup.get_keyboard())


@dp.callback_query_handler(cd.filter(action_type=["Выбор 1", "Выбор 2"]))
async def handle_press_inline_button(call: types.CallbackQuery, callback_data: dict):
    """
    Хандлер нажатия инлайн кнопок
    """

    value = callback_data.get("value")
    await call.message.answer(f"Вы выбрали {value}")
