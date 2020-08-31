from typing import Optional

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(
        data: dict, user: types.User, chat: Optional[types.Chat] = None
    ):
        user_id = user.id
        chat_type = chat.type if chat else "private"

        if chat_type != "private":
            logger.info(
                "User {user} tried to chat with bot in non-private chat, which is not permitted!",
                user=user,
            )
            raise CancelHandler()

        user = await User.get(user_id)
        if user is None:
            user = await User.create(id=user_id)
            logger.info("User {user} created!", user=user)

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.chat)

    async def on_pre_process_callback_query(
        self, query: types.CallbackQuery, data: dict
    ):
        await self.setup_chat(
            data, query.from_user, query.message.chat if query.message else None,
        )
