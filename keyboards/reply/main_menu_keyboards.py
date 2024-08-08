from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from crm_bot.keyboards.reply import BaseReplyKeyboard


def send_phone_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(
        text="Отправить контакт 📱",
        request_contact=True
    ))
    return markup


class MainMenuReplyKeyboard(BaseReplyKeyboard):
    data = [
        ("account", "Личный кабинет 👤"),
        ("tasks", "Задачи 📊"),
    ]