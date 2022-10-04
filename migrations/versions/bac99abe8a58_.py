"""empty message

Revision ID: bac99abe8a58
Revises: d51ea185b65b
Create Date: 2022-10-03 17:25:17.308178

"""

# revision identifiers, used by Alembic.
revision = "bac99abe8a58"
down_revision = "d51ea185b65b"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("confirmed", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "confirmed")
    # ### end Alembic commands ###