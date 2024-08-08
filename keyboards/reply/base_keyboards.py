from crm_bot.keyboards import BaseKeyboard

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class BaseReplyKeyboard(BaseKeyboard):

    def _get_markup_button(self, data):
        """
        Получение экземпляра кнопки
        """
        return KeyboardButton(text=self._get_button_text(data))

    def _get_markup(self):
        """
        Получение экземпляра инлайн клавиатуры
        """
        return ReplyKeyboardMarkup(resize_keyboard=True)