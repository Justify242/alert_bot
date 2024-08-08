import logging

from aiogram import Dispatcher
from config import BOT_ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in BOT_ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")
        except Exception as err:
            logging.exception(err)