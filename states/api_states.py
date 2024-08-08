from aiogram.dispatcher.filters.state import StatesGroup, State


class ApiState(StatesGroup):
    send_city_name = State()