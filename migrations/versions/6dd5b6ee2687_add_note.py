"""add_note

Revision ID: 6dd5b6ee2687
Revises: b8bfbb8170b6
Create Date: 2020-07-19 11:14:00.168119

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6dd5b6ee2687"
down_revision = "b8bfbb8170b6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sleep_records", sa.Column("note", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sleep_records", "note")
    # ### end Alembic commands ###
