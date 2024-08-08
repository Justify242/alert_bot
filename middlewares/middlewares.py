from aiogram.types import Update
from aiogram.dispatcher.middlewares import BaseMiddleware

from crm_core.models import CustomUser


class UserMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: Update, data: dict):
        if update.message:
            telegram_id = update.message.from_user.id
        elif update.callback_query:
            telegram_id = update.callback_query.from_user.id
        else:
            telegram_id = None

        if telegram_id:
            try:
                user = CustomUser.objects.get(telegram_id=telegram_id)
                data['user'] = user
            except CustomUser.DoesNotExist:
                data['user'] = None
