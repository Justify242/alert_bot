import logging
import config

import requests

from celery import Celery
from celery.schedules import crontab

from utils import Database

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)


app.conf.update(
    result_expires=3600,
    timezone="Europe/Moscow",
    enable_utc=True,
    beat_schedule={
        "check_notifications_reminder_worker": {
            "task": "tasks.notify_users",
            "schedule": crontab(hour="10", minute="17")
        },
        "response_reminder_worker": {
            "task": "tasks.check_user_response",
            "schedule": 60,
        },
    }
)

db = Database()


@app.task()
def notify_users():
    users = db.select_list_of_users()
    for user in users:
        chat_id = user[-1]
        payload = {
            "chat_id": chat_id,
            "text": "Не забудьте проверить уведомления!"
        }
        requests.post(f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage", data=payload)


@app.task()
def check_user_response():
    messages = db.select_message_queue()

    for message in messages:
        message_id, chat_id, created_at = message
        payload = {
            "chat_id": chat_id,
            "text": "Вы забыли ответить"
        }
        requests.post(f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage", data=payload)




