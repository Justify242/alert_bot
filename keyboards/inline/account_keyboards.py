from crm_bot.keyboards.inline import BaseInlineKeyboard, PaginatedInlineKeyboard

from crm_core.models import Region


class AccountKeyboard(BaseInlineKeyboard):
    data = [
        ("active_tasks", "Задачи 📊"),
        # ("archive_tasks", "Архив задач 📚"),
    ]


class RegionSelectKeyboard(PaginatedInlineKeyboard):
    data = Region.objects.values_list("id", "name")
    default_render_options = {
        "action_type": "select_region",
        "text": lambda x: x[1],
        "value": lambda x: x[0]
    }
