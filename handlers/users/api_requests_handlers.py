import requests

import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import ApiState


# ===== Работа с API интеграцией ===== #


@dp.message_handler(Command("weather"))
async def handle_weather_command(message: types.Message):
    """
    Хандлер команды /weather
    """

    await message.answer("Отправьте название города")
    await ApiState.send_city_name.set()


@dp.message_handler(state=ApiState.send_city_name)
async def handle_city_name_message(message: types.Message, state: FSMContext):
    """
    Хандлер обработки названия города и получения погоды
    """

    resp = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": message.text,
            "APPID": config.OPEN_WEATHER_MAP_KEY,
            "units": "metric"
        }
    )
    if resp.status_code != 200:
        return await message.answer("Введено некорректное название города")

    json_resp = resp.json()

    main_temp = json_resp["main"]["temp"]
    feels_like = json_resp["main"]["feels_like"]

    message_text = f"Температура: {main_temp} (ощущается как {feels_like})"

    await state.finish()
    await message.answer(message_text)
