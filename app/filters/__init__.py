from aiogram import Dispatcher
from aiogram.dispatcher.filters import IsReplyFilter
from loguru import logger


def setup(dispatcher: Dispatcher):
    logger.info("Configure filters...")
    from .has_permissions import BotHasPermissions, HasPermissions
    from .superuser import IsSuperuserFilter
    from .sleep_tracker import UserAwakeFilter

    text_messages = [
        dispatcher.message_handlers,
        dispatcher.edited_message_handlers,
        dispatcher.channel_post_handlers,
        dispatcher.edited_channel_post_handlers,
    ]

    dispatcher.filters_factory.bind(IsReplyFilter, event_handlers=text_messages)
    dispatcher.filters_factory.bind(HasPermissions, event_handlers=text_messages)
    dispatcher.filters_factory.bind(BotHasPermissions, event_handlers=text_messages)
    dispatcher.filters_factory.bind(IsSuperuserFilter)
    dispatcher.filters_factory.bind(UserAwakeFilter)
