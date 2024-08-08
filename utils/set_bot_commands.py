from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("echo", "Эхо"),
        types.BotCommand("photo", "Отправка изображения"),
        types.BotCommand("inline", "Инлайн клавиатура"),
        types.BotCommand("account", "Анкета пользователя"),
        types.BotCommand("users", "Пользователи"),
        types.BotCommand("weather", "Текущая погода"),
        types.BotCommand("hello", "Напоминание о необходимости ответа"),
    ])