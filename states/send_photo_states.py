from aiogram.dispatcher.filters.state import StatesGroup, State


class SendPhotoState(StatesGroup):
    send_photo = State()
