from crm_bot.keyboards.inline import PaginatedInlineKeyboard, BaseInlineKeyboard

from crm_core.models import CustomUser, RegionTask, RegionTaskFeedback


class TaskListKeyboard(PaginatedInlineKeyboard):
    """
    Клавиатура списка задач
    """
    default_render_options = {
        "action_type": "view_task",
        "text": lambda x: x[1],
        "value": lambda x: x[0]
    }

    def __init__(self, **kwargs):
        self.completed = kwargs.pop("completed", False)
        super().__init__(**kwargs)

    def get_data(self):
        """
        Нужно получать список задач, соответствующий региону пользователя
        """
        user = (
            CustomUser.objects
            .select_related("region")
            .only("region")
            .get(telegram_id=self.user_id)
        )

        tasks = RegionTask.objects.filter(
            region=user.region,
            completed_by_moderator=self.completed
        ).values_list("id", "task__name")

        return tasks


class TaskFeedbackListKeyboard(PaginatedInlineKeyboard):
    default_render_options = {
        "action_type": "download_feedback",
        "text": lambda x: x[1].split("/")[-1],
        "value": lambda x: x[0]
    }

    def __init__(self, **kwargs):
        self.task_id = kwargs.pop("task_id", False)
        super().__init__(**kwargs)

    def get_data(self):
        return (
            RegionTaskFeedback.objects
            .filter(task_id=self.task_id)
            .values_list("id", "file")
        )


class CompletedTaskKeyboard(BaseInlineKeyboard):
    """
    Клавиатура детального представления завершенной модератором задачи
    """
    data = [
        ("active_tasks", "Назад"),
        ("feedbacks", "Обратная связь")
    ]


class NotCompletedTaskKeyboard(BaseInlineKeyboard):
    """
    Клавиатура детального представления незавершенной модератором задачи
    """
    data = [
        ("active_tasks", "Назад"),
        ("start_fill", "Начать заполнение"),
        ("feedbacks", "Обратная связь")
    ]

    def __init__(self, **kwargs):
        task_id = kwargs.pop("task_id", None)
        super().__init__(**kwargs)

        # Нужно в value передавать id задачи, чтобы работала кнопка
        # завершения отправки результата выполнения
        self.render_options = {
            "action_type": lambda x: x[0],
            "text": lambda x: x[1],
            "value": task_id
        }


class CompleteTaskFillKeyboard(NotCompletedTaskKeyboard):
    """
    Клавиатура завершения отправки результата выполнения задачи
    """
    data = [
        ("stop_fill", "Завершить"),
    ]