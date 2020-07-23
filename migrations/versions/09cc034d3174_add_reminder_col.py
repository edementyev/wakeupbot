"""add reminder col

Revision ID: 09cc034d3174
Revises: 8ae6b9ae2c37
Create Date: 2020-07-23 11:34:42.948455

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "09cc034d3174"
down_revision = "8ae6b9ae2c37"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("reminder", sa.String(), nullable=True))
    # ### end Alembic commands ###
    op.execute("UPDATE users SET reminder = '-' WHERE reminder IS NULL")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "reminder")
    # ### end Alembic commands ###
