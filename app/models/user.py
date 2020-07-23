from __future__ import annotations

from sqlalchemy.sql import expression

from app.models.db import BaseModel, TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    username = db.Column(db.String)

    locale = db.Column(db.String)
    timezone = db.Column(db.String, default="+00:00")
    reminder = db.Column(db.String, default="-")
    is_superuser = db.Column(db.Boolean, server_default=expression.false())

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    conversation_started = db.Column(db.Boolean, server_default=expression.true())
    active = db.Column(db.Boolean, server_default=expression.true())
    do_not_disturb = db.Column(db.Boolean, server_default=expression.true())


class UserRelatedModel(BaseModel):
    __abstract__ = True

    user_id = db.Column(
        db.ForeignKey(
            f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
