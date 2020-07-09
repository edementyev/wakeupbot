from typing import List, Union

import pendulum
import sqlalchemy as sa
from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino
from loguru import logger

from app import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

    __repr__ = __str__


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=pendulum.now,
        onupdate=pendulum.now,
        server_default=db.func.now(),
    )


async def on_startup(dispatcher: Union[Dispatcher, None]):
    logger.info("Setup PostgreSQL Connection")
    await db.set_bind(config.POSTGRES_URI)


async def on_shutdown(dispatcher: Union[Dispatcher, None]):
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
