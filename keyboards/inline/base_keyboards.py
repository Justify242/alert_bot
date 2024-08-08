import math
import emoji

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards import BaseKeyboard

"""
data = [
    ("main_menu", "Главное меню")
]

data = [
    ("1", "test")
]

render_options = {
    "action_type": "view_booking" or lambda x: x[0],
    "text": "name" or lambda obj, emoji: f"Бронь {obj[0]} {emoji(':arrow_left:', language='alias')}"
    "value": "click" or lambda x: x[0]
}
"""

callback_data = CallbackData(
    'inline_actions',
    'action_type',
    'value'
)


class BaseInlineKeyboard(BaseKeyboard):
    """
    Базовый класс создания инлайн клавиатуры.
    API схоже с API при создании представлений в DRF
    """

    default_render_options = {
        "action_type": lambda x: x[0],
        "text": lambda x: x[1],
        "value": lambda x: x[0]
    }

    def _get_markup_button(self, data):
        """
        Получение экземпляра кнопки
        """
        return InlineKeyboardButton(
            text=self._get_button_text(data),
            callback_data=self._get_button_callback_data(data)
        )

    def _get_markup(self):
        """
        Получение экземпляра инлайн клавиатуры
        """
        return InlineKeyboardMarkup(row_width=self.row_width)

    def _get_button_callback_data(self, data):
        """
        Получение callback_data кнопки на основе параметра
        action_type и value из render_options
        """
        action_type_render_option = self.render_options["action_type"]
        value_render_option = self.render_options["value"]

        action_type = action_type_render_option(data) if callable(
            action_type_render_option) else action_type_render_option
        value = value_render_option(data) if callable(value_render_option) else value_render_option

        return callback_data.new(action_type=action_type, value=value)


class PaginatedInlineKeyboard(BaseInlineKeyboard):
    default_control_button_action = "roll_page"

    def __init__(self, render_options=None, user_id=None, page_size=10, control_button_action=""):
        self.page_size = page_size
        self.current_page = 1
        self.control_button_action = (
            control_button_action
            if control_button_action else self.default_control_button_action
        )
        super().__init__(render_options=render_options, user_id=user_id)

    def _get_offset(self):
        """
        Получение начальной и конечной позиции для пагинации
        """
        start = (self.current_page - 1) * self.page_size
        return start, start + self.page_size

    def _paginate_data(self, data):
        """
        Пагинация данных кнопок
        """
        start, end = self._get_offset()
        return data[start: end]

    def _get_pages_count(self):
        """
        Получение количества страниц
        """
        count = len(self.get_data())
        return math.ceil(count / self.page_size)

    def _get_control_button(self, current_page=1, direction="left"):
        """
        Получение кнопок управления для переключения страниц
        """
        return InlineKeyboardButton(
            text=emoji.emojize(f':arrow_{direction}:', language='alias'),
            callback_data=callback_data.new(
                action_type=self.control_button_action if self.control_button_action else 'roll_page',
                value=current_page - 1 if direction == "left" else current_page + 1
            )
        )

    def _get_paginator(self):
        """
        Получение кнопок пагинации
        """
        pages_count = self._get_pages_count()
        buttons_list = [
            InlineKeyboardButton(
                text=f'{self.current_page if pages_count > 0 else 0}/{pages_count}',
                callback_data=callback_data.new(action_type='', value=''),
            )
        ]

        if self.current_page != 1:
            buttons_list.insert(0, self._get_control_button(self.current_page, "left"))
        if self.current_page != pages_count and pages_count > 1:
            buttons_list.append(self._get_control_button(self.current_page, "right"))

        return buttons_list

    def _make(self):
        markup = self._make_keyboard()
        pagination_buttons = self._get_paginator()
        return markup.add(*pagination_buttons)

    def perform_get_data(self):
        return self._paginate_data(self.get_data())

    def get_keyboard(self, current_page=1):
        self.current_page = current_page
        return self._make()
