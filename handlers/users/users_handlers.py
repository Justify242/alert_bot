import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import AccountState
from utils import Database


logger = logging.getLogger(__name__)
db = Database()


# ===== Работа с пользователями ===== #


@dp.message_handler(Command("account"), state="*")
async def handle_account_command(message: types.Message, state: FSMContext):
    """
    Хандлер команды /account
    """
    
    await state.finish()

    await message.answer("Как Вас зовут?")
    await AccountState.enter_full_name.set()


@dp.message_handler(Command("users"))
async def handle_users_command(message: types.Message):
    """
    Хандлер команды /users
    """

    users_str = "\n".join(
        f"- {user[1]}, {user[2]} лет"
        for user in db.select_list_of_users()
    )
    await message.answer(f"== Список пользователей ==\n\n{users_str}")


@dp.message_handler(state=AccountState.enter_full_name)
async def handle_enter_full_name(message: types.Message, state: FSMContext):
    """
    Хандлер сохранения введенного имени в стейт
    """

    await state.update_data(full_name=message.text)

    await AccountState.enter_age.set()
    await message.answer("Сколько Вам лет?")


@dp.message_handler(state=AccountState.enter_age)
async def handle_enter_age(message: types.Message, state: FSMContext):
    """
    Хандлер ввода возраста и отправки сообщения пользователю с
    введенным именем и возрастом
    """

    # Проверяем, что введенный возраст - число
    try:
        int(message.text)
    except ValueError:
        logger.error("Provided age value is not digit")
        return await message.answer("Введите корректный возраст")

    data = await state.get_data()

    # Сохранение данных пользователя в таблицу
    result = db.add_new_user(
        full_name=data.get('full_name'),
        age=int(message.text),
        chat_id=message.from_user.id
    )

    message_text = (
        f"Введенное имя: <b>{data.get('full_name')}</b>\n"
        f"Введенный возраст: <b>{message.text}</b> лет\n"
    )

    if result:
        message_text += f"\n{result}"

    await state.finish()
    await message.answer(message_text)
