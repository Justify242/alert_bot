
class BaseKeyboard:
    """
    Базовый класс создания клавиатуры.
    API схоже с API при создании представлений в DRF
    """

    row_width = 3
    data = []
    default_render_options = {
        "text": lambda x: x[1],
    }

    def __init__(self, render_options=None, user_id=None):
        self.render_options = render_options or self.default_render_options
        self.keyboard = []
        self.user_id = user_id

    def _get_markup_button(self, data):
        """
        Получение экземпляра кнопки
        """
        raise NotImplementedError()

    def _get_markup(self):
        """
        Получение экземпляра инлайн клавиатуры
        """
        raise NotImplementedError()

    def _get_button_text(self, data):
        """
        Получение теста кнопки на основе параметра text из render_options
        """
        render_option = self.render_options["text"]
        return render_option(data) if callable(render_option) else data[render_option]

    def _make_keyboard(self):
        """
        Создание клавиатуры
        """
        markup = self._get_markup()
        buttons_list = []
        data = self.perform_get_data()
        for obj in data:
            button = self._get_markup_button(data=obj)
            buttons_list.append(button)

            if len(buttons_list) == self.row_width - 1:
                markup.add(*buttons_list)
                buttons_list.clear()

        if buttons_list:
            markup.add(*buttons_list)
        return markup

    def _make(self):
        """
        Прослойка для дополнительной логики при создании клавиатуры
        """
        return self._make_keyboard()

    def perform_get_data(self):
        """
        Прослойка для пагинации и тд
        """
        return self.get_data()

    def get_data(self):
        """
        Прослойка для получения кастомной даты
        """
        return self.data

    def get_keyboard(self):
        """
        Получение клавиатуры
        """
        return self._make()