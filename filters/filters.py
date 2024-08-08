import re

from django.utils import timezone

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from extra_settings.models import Setting

from crm_core.models import CustomUser


class BotActive(BoundFilter):
    """
    Фильтр активности бота. Если бот отключен, то ответа на сообщение не будет
    """
    async def check(self, message: types.message):
        try:
            bot_active = Setting.objects.get(name="BOT_ACTIVE")
        except Setting.DoesNotExist:
            return True

        return bot_active.value


class IsUser(BoundFilter):
    """
    Проверка зарегистрирован ли пользователь
    """
    async def check(self, message: types.message):
        user = CustomUser.objects.filter(
            telegram_id=message.from_user.id,
            can_use_bot=True,
            bot_activated=True,
            is_active=True,
        ).first()

        # Установка метки последней активности, если пользователь может пользоваться ботом
        if user:
            user.last_bot_activity = timezone.now()
            user.save()

        return bool(user)


class BaseTextFilter(BoundFilter):
    text = ""

    @staticmethod
    def clean_text(text):
        pattern = (
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002500-\U00002BEF"
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"
            "\u3030"
            "]+"
        )
        emoji_pattern = re.compile(pattern, flags=re.UNICODE)
        return emoji_pattern.sub(r'', text).strip()

    async def check(self, message: types.message):
        cleaned_text = self.clean_text(message.text)
        return self.text.lower() == cleaned_text.lower()


class MainMenu(BaseTextFilter):
    text = "Главное меню"


class Account(BaseTextFilter):
    text = "Личный кабинет"


class Tasks(BaseTextFilter):
    text = "Задачи"
