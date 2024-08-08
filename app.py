import logging

from utils import set_default_commands

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
    handlers=[
        logging.FileHandler('bot.log'),  # Записывать лог в файл
        logging.StreamHandler()  # Также выводить лог в консоль (опционально)
    ]
)


async def on_startup(dp):
    from utils import on_startup_notify

    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)