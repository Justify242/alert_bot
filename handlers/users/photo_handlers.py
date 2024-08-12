import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import SendPhotoState


logger = logging.getLogger(__name__)

# ===== Работа с изображениями ===== #


@dp.message_handler(Command("photo"), state="*")
async def handle_photo_command(message: types.Message, state: FSMContext):
    """
    Хандлер команды /photo
    """
    
    await state.finish()

    await SendPhotoState.send_photo.set()
    await message.answer("Отправьте изображение")


@dp.message_handler(content_types=types.ContentType.ANY, state=SendPhotoState.send_photo)
async def handle_photo_send(message: types.Message, state: FSMContext):
    """
    Хандлер обработки изображения и отправки пользователю сообщения с размерами
    """

    if not message.photo:
        msg = "В сообщении отсутствуют изображения"
        logger.warning("There is no images in message")
        return await message.answer(msg)

    # Берем изображение наивысшего качества
    photo = message.photo[-1]

    await state.finish()
    await message.answer(
        text=(
            f"Ширина изображения: {photo.width} px\n"
            f"Высота изображения: {photo.height} px\n"
        )
    )
