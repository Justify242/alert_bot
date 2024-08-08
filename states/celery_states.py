from aiogram.dispatcher.filters.state import StatesGroup, State


class CeleryStates(StatesGroup):
    hello = State()